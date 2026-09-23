#!/usr/bin/env python3
"""Measure what Claude Code and Codex load into context for a repository.

Deterministic half of the `audit-agent-environment` skill: this script
measures, the skill interprets. Stdlib only, Python 3.9+.

    python3 scripts/token_audit.py                # this repo
    python3 scripts/token_audit.py --repo ../app  # another repo
    python3 scripts/token_audit.py --global       # + ~/.claude and ~/.codex
    python3 scripts/token_audit.py --codex        # + Codex's rendered startup prompt
    python3 scripts/token_audit.py --json         # machine-readable
    python3 scripts/token_audit.py --strict       # exit 1 if any warning fires

Token figures are estimates (characters / 4) unless labelled "measured".
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Thresholds and where they come from.
CLAUDE_MD_MAX_LINES = 200         # Claude Code memory docs: keep CLAUDE.md under 200 lines
CLAUDE_MD_TARGET_LINES = 120      # house target, leaves room for the actual work
AGENTS_MD_MAX_BYTES = 32 * 1024   # Codex project_doc_max_bytes default; the rest is dropped
DESCRIPTION_MAX_CHARS = 1024      # Agent Skills spec limit for `description`
SKILL_BODY_MAX_LINES = 500        # Claude Code skills docs: keep SKILL.md under 500 lines
MEMORY_INDEX_MAX_LINES = 200      # Claude Code loads only the first 200 lines of MEMORY.md
CODEX_APP_BINARIES = (
    "/Applications/ChatGPT.app/Contents/Resources/codex",
    "/Applications/Codex.app/Contents/Resources/codex",
)

PLACEHOLDER = re.compile(r"^\s*>?\s*\**\s*placeholder\b", re.IGNORECASE | re.MULTILINE)
IMPORT = re.compile(r"(?<![\w`@])@((?:~|\.{1,2})?/?[\w.-]+(?:/[\w.-]+)*)")
READS_OTHER_FILE = re.compile(
    r"read\s+`?([\w./-]+\.md)`?[^.]{0,80}?(?:start|every session|before)", re.IGNORECASE
)


def tokens(chars: int) -> int:
    return math.ceil(chars / 4)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def parse_frontmatter(text: str) -> dict:
    """Parse the simple YAML frontmatter SKILL.md files use.

    Handles `key: value`, quoted values, block scalars (`>`, `|`) and indented
    continuation lines. Returns {} when there is no frontmatter.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict = {}
    key = None
    for line in lines[1:]:
        if line.rstrip() == "---":  # the closing delimiter is always at column 0
            break
        if key and (line.startswith((" ", "\t")) or not line.strip()):
            data[key] = (data[key] + " " + line.strip()).strip()
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            key = None
            continue
        key, value = match.group(1), match.group(2).strip()
        if value in (">", "|", ">-", "|-", ">+", "|+"):
            value = ""
        elif len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        elif len(value) >= 2 and value[0] == value[-1] == "'":
            value = value[1:-1].replace("''", "'")
        data[key] = value
    return data


def skill_files(root: Path, recursive: bool) -> list:
    """SKILL.md files under a skills root: one level deep (Claude Code) or
    every level (Codex, which also follows symlinks)."""
    if not root.is_dir():
        return []
    if not recursive:
        return sorted(p for p in root.glob("*/SKILL.md") if p.is_file())
    found, seen = [], set()
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        real = os.path.realpath(dirpath)
        if real in seen:
            dirnames[:] = []
            continue
        seen.add(real)
        dirnames.sort()
        if "SKILL.md" in filenames:
            found.append(Path(dirpath) / "SKILL.md")
    return found


def load_skill(path: Path) -> dict:
    text = read_text(path)
    meta = parse_frontmatter(text)
    folder = path.parent.name
    name = meta.get("name", "")
    description = meta.get("description", "")
    flags = []
    if not description:
        flags.append("no-description")
    if len(description) > DESCRIPTION_MAX_CHARS:
        flags.append(f"description>{DESCRIPTION_MAX_CHARS}")
    if name and name != folder:
        flags.append("name!=folder")
    if folder.startswith("todo-") or name.startswith("todo-") or PLACEHOLDER.search(text):
        flags.append("placeholder")
    lines = text.count("\n") + 1
    if lines > SKILL_BODY_MAX_LINES:
        flags.append(f"body>{SKILL_BODY_MAX_LINES}-lines")
    return {
        "name": name or folder,
        "folder": folder,
        "path": str(path),
        "description_chars": len(description),
        "listing_chars": len(name or folder) + len(description) + 4,
        "body_lines": lines,
        "flags": flags,
    }


def listing(label: str, harness: str, paths: list, note: str = "") -> dict:
    skills = [load_skill(p) for p in paths]
    chars = sum(s["listing_chars"] for s in skills)
    return {
        "label": label,
        "harness": harness,
        "count": len(skills),
        "chars": chars,
        "tokens": tokens(chars),
        "note": note,
        "skills": skills,
    }


def expand_imports(path: Path, depth: int = 0, seen: set = None) -> list:
    """Files pulled in by CLAUDE.md `@path` imports (loaded at launch, up to 5 hops)."""
    seen = seen if seen is not None else {path.resolve()}
    if depth >= 5:
        return []
    text = re.sub(r"```.*?```", "", read_text(path), flags=re.DOTALL)
    found = []
    for raw in IMPORT.findall(text):
        target = Path(os.path.expanduser(raw))
        if not target.is_absolute():
            target = path.parent / target
        if target.is_file() and target.resolve() not in seen:
            seen.add(target.resolve())
            found.append(target)
            found.extend(expand_imports(target, depth + 1, seen))
    return found


def instruction_surface(label: str, harness: str, path: Path, repo: Path) -> dict:
    if not path.is_file():
        return None
    text = read_text(path)
    chars, lines = len(text), text.count("\n") + 1
    notes = []
    if path.is_symlink():
        notes.append(f"symlink -> {os.readlink(path)}")
    if harness == "Claude Code":
        for imported in expand_imports(path):
            chars += len(read_text(imported))
            notes.append(f"imports {display(imported, repo)}")
    return {
        "label": label,
        "harness": harness,
        "path": str(path),
        "lines": lines,
        "bytes": len(text.encode("utf-8")),
        "chars": chars,
        "tokens": tokens(chars),
        "note": "; ".join(notes),
        "text": text,
    }


def display(path: Path, repo: Path) -> str:
    path = Path(path)
    for base, prefix in ((repo, ""), (Path.home(), "~/")):
        try:
            return prefix + str(path.relative_to(base))
        except ValueError:
            continue
    return str(path)


def orphan_folders(root: Path) -> list:
    """Folders in a skills root with no SKILL.md anywhere below them."""
    if not root.is_dir():
        return []
    orphans = []
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name.endswith("-workspace"):
            continue
        if not skill_files(child, recursive=True):
            orphans.append(child)
    return orphans


def enabled_plugin_skill_roots(repo: Path) -> list:
    """Skill folders of Claude Code plugins enabled for this repo (best effort)."""
    home = Path.home() / ".claude"
    enabled = set()
    for settings in (home / "settings.json", repo / ".claude" / "settings.json"):
        try:
            data = json.loads(read_text(settings) or "{}")
        except json.JSONDecodeError:
            continue
        enabled.update(k for k, v in (data.get("enabledPlugins") or {}).items() if v)
    try:
        installed = json.loads(read_text(home / "plugins" / "installed_plugins.json") or "{}")
    except json.JSONDecodeError:
        return []
    roots = []
    for plugin_id, installs in (installed.get("plugins") or {}).items():
        if plugin_id not in enabled:
            continue
        for install in installs:
            scope, project = install.get("scope"), install.get("projectPath")
            if scope == "user" or (scope == "project" and project and Path(project) == repo):
                roots.append((plugin_id, Path(install.get("installPath", "")) / "skills"))
    return roots


def config_defaults() -> list:
    """Default model and effort for each harness; reads only those keys."""
    info = []
    try:
        claude = json.loads(read_text(Path.home() / ".claude" / "settings.json") or "{}")
        info.append(
            f"Claude Code defaults: model={claude.get('model', 'default')}, "
            f"effort={claude.get('effortLevel', 'default')}"
        )
    except json.JSONDecodeError:
        pass
    codex = read_text(Path.home() / ".codex" / "config.toml")
    if codex:
        values = {}
        for key in ("model", "model_reasoning_effort"):
            match = re.search(rf'^{key}\s*=\s*"([^"]*)"', codex, re.MULTILINE)
            values[key] = match.group(1) if match else "default"
        info.append(
            f"Codex defaults: model={values['model']}, effort={values['model_reasoning_effort']}"
        )
    return info


def find_codex(explicit: str) -> str:
    if explicit:
        return explicit
    return shutil.which("codex") or next(
        (b for b in CODEX_APP_BINARIES if os.access(b, os.X_OK)), ""
    )


def measure_codex(repo: Path, binary: str) -> dict:
    """Render Codex's model-visible startup prompt (no model call) and size it."""
    if not binary:
        return {"available": False, "reason": "codex binary not found"}
    try:
        result = subprocess.run(
            [binary, "debug", "prompt-input", "hello"],
            cwd=repo, capture_output=True, text=True, timeout=120,
        )
        items = json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        return {"available": False, "reason": f"{type(exc).__name__}: {exc}"[:200]}
    texts = [c.get("text", "") for item in items for c in item.get("content", [])]
    total = sum(len(t) for t in texts)
    skills_text = next((t for t in texts if "<skills_instructions>" in t), "")
    agents_text = next((t for t in texts if t.startswith("# AGENTS.md instructions")), "")
    listed = re.findall(r"^- (\S+?): ", skills_text.split("### Available skills")[-1], re.M)
    return {
        "available": True,
        "total_chars": total,
        "total_tokens": tokens(total),
        "skills_chars": len(skills_text),
        "skills_count": len(listed),
        "agents_chars": len(agents_text),
    }


def audit(repo: Path, include_global: bool, codex_binary: str = None) -> dict:
    repo = repo.resolve()
    home = Path.home()
    warnings, info, always, listings, on_demand = [], [], [], [], []

    claude_md = instruction_surface("CLAUDE.md", "Claude Code", repo / "CLAUDE.md", repo)
    agents_md = instruction_surface("AGENTS.md", "Codex", repo / "AGENTS.md", repo)
    for surface in (claude_md, agents_md):
        if surface:
            always.append(surface)

    if claude_md:
        if claude_md["lines"] > CLAUDE_MD_MAX_LINES:
            warnings.append(
                f"CLAUDE.md is {claude_md['lines']} lines (> {CLAUDE_MD_MAX_LINES}); "
                "move reference material into files read on demand"
            )
        elif claude_md["lines"] > CLAUDE_MD_TARGET_LINES:
            info.append(
                f"CLAUDE.md is {claude_md['lines']} lines (house target {CLAUDE_MD_TARGET_LINES})"
            )
    if agents_md:
        if agents_md["bytes"] > AGENTS_MD_MAX_BYTES * 0.8:
            warnings.append(
                f"AGENTS.md is {agents_md['bytes']:,} bytes, over 80% of Codex's "
                f"{AGENTS_MD_MAX_BYTES:,}-byte project_doc_max_bytes default (excess is dropped)"
            )
        match = READS_OTHER_FILE.search(agents_md["text"])
        if match and not (repo / "AGENTS.md").is_symlink():
            info.append(
                f"AGENTS.md asks Codex to read {match.group(1)} every session: one extra tool "
                "call plus that file's tokens; a symlink or inlined rules avoid both"
            )

    claude_root = repo / ".claude" / "skills"
    project_claude = listing(
        "project skills (.claude/skills)", "Claude Code", skill_files(claude_root, False)
    )
    listings.append(project_claude)
    discovered = {Path(s["path"]).resolve() for s in project_claude["skills"]}
    hidden = [p for p in skill_files(claude_root, True) if p.resolve() not in discovered]
    if hidden:
        size = sum(len(read_text(p)) for p in hidden)
        on_demand.append({
            "label": "nested skills under .claude/skills (Claude Code does not discover them)",
            "count": len(hidden), "chars": size, "tokens": tokens(size),
        })

    codex_roots = [(repo / ".agents" / "skills", ".agents/skills"),
                   (repo / ".codex" / "skills", ".codex/skills (legacy path)")]
    for root, label in codex_roots:
        if root.exists():
            note = f"symlink -> {os.readlink(root)}" if root.is_symlink() else ""
            codex_listing = listing(f"project skills ({label})", "Codex", skill_files(root, True), note)
            listings.append(codex_listing)
            depths = {len(Path(s["path"]).relative_to(root).parts) for s in codex_listing["skills"]}
            if any(d > 2 for d in depths):
                warnings.append(
                    f"{label} contains nested skill folders; Codex recurses and lists every one "
                    f"({codex_listing['count']} skills, ~{codex_listing['tokens']:,} tokens per session)"
                )
    if claude_root.is_dir() and not any(l["harness"] == "Codex" for l in listings):
        if project_claude["count"]:
            info.append(
                "Codex does not scan .claude/skills; link .agents/skills -> ../.claude/skills "
                "for native discovery (after moving nested skill libraries out)"
            )

    for skill in project_claude["skills"]:
        if skill["flags"]:
            warnings.append(f"skill {skill['folder']}: {', '.join(skill['flags'])}")
    for orphan in orphan_folders(claude_root):
        info.append(f"{display(orphan, repo)} has no SKILL.md (not a skill; move or delete)")

    if include_global:
        for surface in (
            instruction_surface("~/.claude/CLAUDE.md", "Claude Code", home / ".claude" / "CLAUDE.md", repo),
            instruction_surface("~/.codex/AGENTS.md", "Codex", home / ".codex" / "AGENTS.md", repo),
        ):
            if surface and surface["chars"]:
                always.append(surface)
        listings.append(listing(
            "user skills (~/.claude/skills, incl. synced)", "Claude Code",
            skill_files(home / ".claude" / "skills", True),
        ))
        for plugin_id, root in enabled_plugin_skill_roots(repo):
            listings.append(listing(f"plugin {plugin_id}", "Claude Code", skill_files(root, False)))
        for root in (home / ".codex" / "skills", home / ".agents" / "skills"):
            if root.exists():
                listings.append(listing(f"user skills ({display(root, repo)})", "Codex", skill_files(root, True)))
            for orphan in orphan_folders(root):
                info.append(f"{display(orphan, repo)} has no SKILL.md (orphaned skill folder)")
        memory = home / ".claude" / "projects" / str(repo).replace("/", "-") / "memory" / "MEMORY.md"
        if memory.is_file():
            lines = read_text(memory).count("\n") + 1
            if lines > MEMORY_INDEX_MAX_LINES * 0.75:
                warnings.append(f"MEMORY.md index is {lines} lines; Claude Code loads only the first {MEMORY_INDEX_MAX_LINES}")
        info.extend(config_defaults())

    for harness in ("Claude Code", "Codex"):
        names = {}
        for entry in (l for l in listings if l["harness"] == harness):
            for skill in entry["skills"]:
                names.setdefault(skill["name"].split(":")[-1], set()).add(entry["label"])
        for name, labels in sorted(names.items()):
            if len(labels) > 1:
                warnings.append(f"{harness} lists skill '{name}' more than once: {', '.join(sorted(labels))}")

    totals = {}
    for harness in ("Claude Code", "Codex"):
        totals[harness] = sum(s["tokens"] for s in always if s["harness"] == harness) + sum(
            l["tokens"] for l in listings if l["harness"] == harness
        )

    report = {
        "repo": str(repo),
        "always": [{k: v for k, v in s.items() if k != "text"} for s in always],
        "listings": listings,
        "on_demand": on_demand,
        "totals_tokens": totals,
        "warnings": warnings,
        "info": info,
    }
    if codex_binary is not None:
        report["codex_measured"] = measure_codex(repo, find_codex(codex_binary))
    return report


def render(report: dict) -> str:
    repo = Path(report["repo"])
    out = [f"# Agent context audit: {repo.name}", "",
           "Estimates use characters / 4 ≈ tokens unless marked measured.", "",
           "## Loaded every session", "",
           "| Harness | Surface | Size | ≈ Tokens | Notes |", "|---|---|---|---|---|"]
    for s in report["always"]:
        out.append(f"| {s['harness']} | {s['label']} | {s['lines']} lines · {s['chars']:,} chars "
                   f"| {s['tokens']:,} | {s['note']} |")
    for l in report["listings"]:
        longest = sorted(l["skills"], key=lambda s: -s["description_chars"])[:3]
        note = "; ".join(filter(None, [l["note"], "longest: " + ", ".join(
            f"{s['name']} ({s['description_chars']})" for s in longest) if longest else ""]))
        out.append(f"| {l['harness']} | {l['label']}: {l['count']} skills | {l['chars']:,} chars "
                   f"| {l['tokens']:,} | {note} |")
    for harness, total in report["totals_tokens"].items():
        out.append(f"| **{harness}** | **subtotal from these files** (the harness's own prompt and tool schemas are extra) | | **{total:,}** | |")
    measured = report.get("codex_measured")
    if measured:
        out += ["", "## Codex startup prompt (measured with `codex debug prompt-input`)", ""]
        if measured["available"]:
            out.append(f"- Total: {measured['total_chars']:,} chars (≈ {measured['total_tokens']:,} tokens)")
            out.append(f"- Skills block: {measured['skills_chars']:,} chars, {measured['skills_count']} skills listed")
            out.append(f"- AGENTS.md block: {measured['agents_chars']:,} chars")
        else:
            out.append(f"- Not measured: {measured['reason']}")
    if report["on_demand"]:
        out += ["", "## Available on demand (not in startup context)", ""]
        for s in report["on_demand"]:
            out.append(f"- {s['label']}: {s['count']} files, {s['chars']:,} chars (≈ {s['tokens']:,} tokens if all read)")
    out += ["", f"## Warnings ({len(report['warnings'])})", ""]
    out += [f"- {w}" for w in report["warnings"]] or ["- none"]
    if report["info"]:
        out += ["", "## Info", ""] + [f"- {i}" for i in report["info"]]
    return "\n".join(out) + "\n"


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent),
                        help="repository to audit (default: this repo)")
    parser.add_argument("--global", dest="include_global", action="store_true",
                        help="include ~/.claude and ~/.codex surfaces that apply to every repo")
    parser.add_argument("--codex", nargs="?", const="", default=None, metavar="BINARY",
                        help="also render Codex's startup prompt (optional path to the codex binary)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    parser.add_argument("--strict", action="store_true", help="exit 1 when any warning fires")
    args = parser.parse_args(argv)

    report = audit(Path(args.repo), args.include_global, args.codex)
    print(json.dumps(report, indent=2) if args.json else render(report), end="" if not args.json else "\n")
    return 1 if args.strict and report["warnings"] else 0


if __name__ == "__main__":
    sys.exit(main())

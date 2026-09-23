#!/usr/bin/env python3
"""Check every skill in .claude/skills against the repo's Skill Contract.

Errors (exit 1):
  - missing SKILL.md, frontmatter, name or description
  - `name` not kebab-case or not equal to the folder name
  - description over 1,024 characters (Agent Skills limit)
  - placeholder skills (`todo-` prefix or a "Placeholder" marker)
  - relative links, or `scripts/`, `references/`, `library/` (etc.) paths, that do not exist
  - skills missing from README.md (catalog drift)
  - YAML frontmatter a strict parser rejects, in any markdown file in the repo.
    GitHub (Ruby Psych) refuses an unquoted value containing ': ' even though
    Claude Code and Codex read it leniently.
Warnings (one line per skill): a description that never says when to use the
skill, and contract sections that cannot be found under any common heading.

    python3 scripts/lint_skills.py [--repo PATH]
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

from token_audit import DESCRIPTION_MAX_CHARS, PLACEHOLDER, parse_frontmatter

KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
PATH_MENTION = re.compile(r"`((?:scripts|references|assets|tools|prompts|library)/[\w./-]+)`")
WHEN = re.compile(
    r"\b(use (?:it |this )?(?:when|for|to|after|before|whenever)|when (?:you|someone|a user|the user|asked)"
    r"|invoke (?:when|for|to)|trigger)", re.IGNORECASE
)

BLOCK_SCALAR = re.compile(r"^[|>][+-]?\d?$")
SKIP_DIRS = {".git", "node_modules", "outputs", "__pycache__", "ai-proficiency-runs"}

# Contract section -> heading fragments that satisfy it (lowercase). "When to use"
# is checked in the description, which is what both harnesses match against.
SECTIONS = {
    "inputs": ("input", "required inputs", "collect inputs"),
    "outputs": ("output",),
    "steps": ("steps", "step ", "how to help", "workflow", "process", "phase "),
    "examples": ("example",),
    "guardrails": ("guardrail", "non-goal", "what not to do", "common mistakes", "anti-pattern"),
}


def scalar_problem(value: str) -> str:
    """Why a strict YAML parser would reject (or silently shorten) a one-line value; '' if fine."""
    if not value or BLOCK_SCALAR.match(value):
        return ""
    if value[0] in "\"'":
        pattern = r'"(?:[^"\\]|\\.)*"' if value[0] == '"' else r"'(?:[^']|'')*'"
        closed = re.match(pattern, value)
        if not closed:
            return "unterminated quoted value"
        rest = value[closed.end():].strip()
        return "" if not rest or rest.startswith("#") else "text after the closing quote"
    if value[0] in "[{":
        return "" if value.endswith("]" if value[0] == "[" else "}") else "unclosed flow collection"
    if value[0] == "#":
        return "the value is a comment, so the key is empty"
    if value[0] in ",&*!|>%@`" or (value[0] in "-?:" and value[1:2] in ("", " ")):
        return f"a plain value cannot start with '{value[0]}'; quote the value"
    return line_problem(value)


def line_problem(text: str) -> str:
    if ": " in text or text.endswith(":"):
        return "unquoted ': ' reads as a new key in strict YAML; rephrase or quote the value"
    if " #" in text:
        return "' #' starts a YAML comment and cuts the value short; rephrase or quote the value"
    return ""


def frontmatter_yaml_errors(text: str) -> list:
    """Strict-YAML problems in flat `key: value` frontmatter (nested blocks are not checked)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    errors, in_block, plain = [], False, False
    for number, line in enumerate(lines[1:], 2):
        if line.rstrip() == "---":
            return errors
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t":
            problem = line_problem(line.strip()) if plain and not in_block else ""
            if problem:
                errors.append(f"line {number}: {problem}")
            continue
        match = re.match(r"^([^\s:#'\"][^:]*?):(?:\s+(.*))?$", line)
        if not match:
            errors.append(f"line {number}: not a 'key: value' line")
            in_block = plain = False
            continue
        value = (match.group(2) or "").strip()
        in_block = bool(BLOCK_SCALAR.match(value))
        problem = scalar_problem(value)
        if problem:
            errors.append(f"line {number} ({match.group(1)}): {problem}")
        plain = bool(value) and not in_block and value[0] not in "\"'[{"
    return errors + ["frontmatter is never closed with '---'"]


def markdown_files(repo: Path) -> list:
    found = []
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.endswith("-workspace")
                             and (not d.startswith(".") or d in (".claude", ".github")))
        found.extend(Path(dirpath) / f for f in sorted(filenames) if f.endswith(".md"))
    return found


def check_skill(skill_dir: Path, repo: Path, readme: str) -> tuple:
    errors, warnings = [], []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["missing SKILL.md"], []
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    meta = parse_frontmatter(text)
    name, description = meta.get("name", ""), meta.get("description", "")

    if not meta:
        errors.append("no YAML frontmatter")
    if not name:
        errors.append("frontmatter has no name")
    elif name != skill_dir.name:
        errors.append(f"name '{name}' does not match folder '{skill_dir.name}'")
    elif not KEBAB.match(name):
        errors.append(f"name '{name}' is not kebab-case")
    if not description:
        errors.append("frontmatter has no description")
    elif len(description) > DESCRIPTION_MAX_CHARS:
        errors.append(f"description is {len(description)} chars (max {DESCRIPTION_MAX_CHARS})")
    elif not WHEN.search(description):
        warnings.append("description never says when to use it")
    if skill_dir.name.startswith("todo-") or PLACEHOLDER.search(text):
        errors.append("placeholder skill: finish it or delete it (its description loads every session)")

    body = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for target in LINK.findall(body):
        if re.match(r"^(?:[a-z]+:|#)", target):
            continue
        if not (skill_dir / target.split("#")[0]).exists():
            errors.append(f"broken link: {target}")
    for mention in sorted(set(PATH_MENTION.findall(text))):
        if not ((skill_dir / mention).exists() or (repo / mention).exists()):
            errors.append(f"referenced path does not exist: {mention}")

    if not re.search(rf"(?<![\w-]){re.escape(skill_dir.name)}(?![\w-])", readme):
        errors.append("not listed in README.md")

    headings = [h.lower() for h in re.findall(r"^#{2,4}\s+(.+)$", body, re.MULTILINE)]
    missing = [s for s, frags in SECTIONS.items() if not any(f in h for h in headings for f in frags)]
    if missing:
        warnings.append("no section for: " + ", ".join(missing))
    return errors, warnings


def main(argv: list = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parent.parent))
    args = parser.parse_args(argv)
    repo = Path(args.repo).resolve()
    skills_root = repo / ".claude" / "skills"
    readme_path = repo / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""

    skill_dirs = sorted(
        d for d in skills_root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and not d.name.endswith("-workspace")
    )
    error_count = warning_count = 0
    for skill_dir in skill_dirs:
        errors, warnings = check_skill(skill_dir, repo, readme)
        error_count += len(errors)
        warning_count += len(warnings)
        for message in errors:
            print(f"ERROR {skill_dir.name}: {message}")
        for message in warnings:
            print(f"warn  {skill_dir.name}: {message}")
    files = markdown_files(repo)
    for path in files:
        for message in frontmatter_yaml_errors(path.read_text(encoding="utf-8", errors="replace")):
            error_count += 1
            print(f"ERROR {path.relative_to(repo)}: frontmatter {message}")
    print(f"{len(skill_dirs)} skills and {len(files)} markdown files checked: "
          f"{error_count} errors, {warning_count} warnings")
    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main())

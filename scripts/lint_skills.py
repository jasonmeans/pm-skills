#!/usr/bin/env python3
"""Check every skill in .claude/skills against the repo's Skill Contract.

Errors (exit 1):
  - missing SKILL.md, frontmatter, name or description
  - `name` not kebab-case or not equal to the folder name
  - description over 1,024 characters (Agent Skills limit)
  - placeholder skills (`todo-` prefix or a "Placeholder" marker)
  - relative links, or `scripts/`, `references/`, `library/` (etc.) paths, that do not exist
  - skills missing from README.md (catalog drift)
Warnings (one line per skill): a description that never says when to use the
skill, and contract sections that cannot be found under any common heading.

    python3 scripts/lint_skills.py [--repo PATH]
"""
from __future__ import annotations

import argparse
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

# Contract section -> heading fragments that satisfy it (lowercase). "When to use"
# is checked in the description, which is what both harnesses match against.
SECTIONS = {
    "inputs": ("input", "required inputs", "collect inputs"),
    "outputs": ("output",),
    "steps": ("steps", "step ", "how to help", "workflow", "process", "phase "),
    "examples": ("example",),
    "guardrails": ("guardrail", "non-goal", "what not to do", "common mistakes", "anti-pattern"),
}


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
    print(f"{len(skill_dirs)} skills checked: {error_count} errors, {warning_count} warnings")
    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main())

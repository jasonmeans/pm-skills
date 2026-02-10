# agent-skills

Portable personal skills repository for agent-friendly workflows.

## Workspace Root

This repo is intended to live under:
`~/code/personal/agent-skills`

## Canonical Structure

- `skills/`: reusable skills, one folder per skill (`<skill-name>/SKILL.md`)
- `templates/`: reusable writing and planning templates
- `CLAUDE.md`: concise usage rules for any assistant
- `AGENTS.md`: tool-agnostic operating rules and skill index
- `notes/`: archived legacy material and learnings retained for reference

## Skills

- `skills/write-in-jasmea-voice/SKILL.md`
- `skills/engineering-foundations/SKILL.md`

## Add A New Skill

1. Create `skills/<lowercase-kebab-case>/SKILL.md`.
2. Add frontmatter with `name` and `description`.
3. Include sections: Purpose, When to use, Inputs, Outputs, Steps, Examples, Non-goals / Guardrails.
4. Update `AGENTS.md` and this README skill list.

## Safety Rules

- Never include work confidential information.
- Keep skills portable and personal-only.

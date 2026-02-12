# pm-skills

Portable personal skills and prompts repository for agent-friendly workflows.

## Structure

```
.claude/skills/          Skills auto-discovered by Claude Code
prompts/                 Reusable prompts for various LLMs
templates/               Reusable writing and planning templates
CLAUDE.md                Usage rules for Claude
AGENTS.md                Tool-agnostic operating rules and skill index
```

## Skills

Skills live in `.claude/skills/<skill-name>/SKILL.md` and are organized flat:

- **Jason's skills** — `write-in-jasmea-voice`, `write-as-jason`, `storytelling-for-impact`, `engineering-foundations`
- **Lenny's PM skills** — prefixed with `lenny-` (e.g. `lenny-writing-prds`, `lenny-shipping-products`)

See `AGENTS.md` for the full skill catalog.

## Prompts

Reusable prompts live in `prompts/`. These are standalone files (Markdown for GPT, XML for Claude) that can be copy-pasted into any LLM.

## Add a New Skill

1. Create `.claude/skills/<lowercase-kebab-case>/SKILL.md`.
2. Include sections: Purpose, When to use, Inputs, Outputs, Steps, Examples, Non-goals / Guardrails.
3. Update `AGENTS.md` skill catalog.

## Safety Rules

- Never include work confidential information.
- Keep skills portable and personal-only.

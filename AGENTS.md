# AGENTS

Use this repository as a tool-agnostic, portable skill library.

## Operating Rules

- Use the closest matching skill in `skills/` before inventing a new workflow.
- Keep all content personal-only and reusable across assistants.
- Never add work confidential information, internal names, or private corporate links.
- Prefer concise instructions, concrete examples, and explicit guardrails.

## Skill Contract

Every skill must live at `skills/<lowercase-kebab-case>/SKILL.md` and include:
- Purpose
- When to use
- Inputs
- Outputs
- Steps
- Examples
- Non-goals / Guardrails

## Available Skills

- `write-in-jasmea-voice`: Draft and revise long-form writing in Jason Means' personal Medium voice.
  File: `skills/write-in-jasmea-voice/SKILL.md`
- `engineering-foundations`: Build repeatable engineering fundamentals across architecture, testing, and delivery.
  File: `skills/engineering-foundations/SKILL.md`

# AGENTS.md

Project instructions live in [CLAUDE.md](./CLAUDE.md). Read `CLAUDE.md` at the
start of every session and treat it as the source of truth for operating rules,
resource constraints, conventions, agent roles, and PM philosophy.

## Skill Usage

This repo is built around Claude Code skills. Before inventing a workflow, use
the closest matching skill in `.claude/skills/`.

Required workflow:

1. Scan `.claude/skills/` for applicable skills.
2. Read the selected skill's `SKILL.md` before acting.
3. Follow the skill's inputs, outputs, steps, examples, and guardrails.
4. Use active project skills first, then Lenny PM skills under `.claude/skills/lenny-podcast/` when they fit.
5. Treat `todo-` skills as placeholders unless their `SKILL.md` is complete enough to execute safely.

The full skill catalog and all project-specific instructions are maintained in
[CLAUDE.md](./CLAUDE.md).

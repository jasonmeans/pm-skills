# AGENTS.md

## Operating Rules

- Check `.claude/skills/` first before inventing a new workflow.
- Prefer simple, working solutions. Write readable code, not impressive code.
- Ask one clarifying question rather than burning tokens on bad drafts.
- Never include confidential info, internal names, or private links.
- New prompts go in `prompts/` — see [prompt-library.md](prompts/prompt-library.md).
- Batch related changes into single interactions.
- Route all art/image work to Gemini or Grok with ready-to-paste prompts.

## Subagent Models

| Model | Use For |
|-------|---------|
| `haiku` | File searches, simple formatting |
| `sonnet` | Code reviews, docs, refactoring, research |
| `opus` | Architecture, multi-step planning, security audits |

Default to `haiku` for exploration, `sonnet` for implementation.

## Conventions

**Structure:**
- Skills: `.claude/skills/<kebab-case>/SKILL.md` + optional `references/`
- Active skills: kebab-case · Unbuilt: `todo-` prefix · Remove prefix when built
- Prompts: `prompts/claude/` (XML) · `prompts/gpt/` (MD) · `prompts/gemini/` (MD)
- CLAUDE.md points here — all real config lives in this file

**Output:** All outputs are markdown files unless creating a PowerPoint.

**Large File Policy** — don't commit without user approval:

| File type | Limit |
|-----------|-------|
| Binary (`.pptx`, `.pdf`, `.xlsx`, `.zip`) | 10 MB |
| Images (`.png`, `.jpg`, `.gif`) | 5 MB |
| Any single file | 25 MB |

Always `ls -lh <file>` before staging. Never `git add .` or `git add -A`.

**Document types:**
1. `DESIGN.md` — what and why (`docs/`)
2. `<feature>-concept.md` — how it feels (`docs/concepts/`)
3. `<feature>-execution.md` — how to build it (`docs/execution/`)

## Release Stages

| Stage | Access | Quality Bar |
|-------|--------|-------------|
| Alpha | Internal only | Dev complete, bugs triaged |
| Closed Beta | All employees + select partners | No P0/P1 |
| Open Beta | All employees + early adopters | No P0/P1/P2 |
| GA | All customers | Feature complete, no critical issues |

## Skill Catalog

### PM Practice Skills

| Skill | Path |
|-------|------|
| Create PRD | `create-prd/` |
| Create PRD (Claude Code) | `create-prd-claude-code/` |
| Create PRD (Engineering) | `create-prd-engineering/` |
| Create PRD (One-Pager) | `create-prd-one-pager/` |
| Decision Brief | `decision-brief/` |
| Question Storming | `question-storming/` |
| Jobs to Be Done | `jobs-to-be-done/` |
| Create User Interview | `create-user-interview/` |
| Analyze User Interview | `analyze-user-interview/` |
| DevEx Survey | `devex-survey/` |
| Architecture Diagram | `create-architecture-diagram/` |
| Release Notes | `create-release-notes/` |
| Sourcegraph Search | `sourcegraph-search/` |
| Storytelling for Impact | `storytelling-for-impact/` |
| Write Teachable Moment | `write-teachable-personal-moment/` |
| Write as Jason | `write-as-jason/` |
| Engineering Foundations | `engineering-foundations/` |

### Planned Skills (not yet built)

`todo-analyze-user-feedback` · `todo-automate-review-process` · `todo-convert-zoom-notes` · `todo-create-figma-mockup` · `todo-gtm-plan` · `todo-launch-checklist` · `todo-map-stakeholders` · `todo-prioritize-features` · `todo-validate-hypothesis`

### Lenny's PM Skills (88 skills)

All in `.claude/skills/lenny-podcast/`. Catalog: [lenny-podcast/README.md](.claude/skills/lenny-podcast/README.md).

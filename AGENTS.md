# AGENTS.md — Project Instructions & Agent Definitions

Source of truth for this repo. Claude Code, Codex, and other AI tools read
this file for all project context.

---

## Operating Rules

- Use the closest matching skill in `.claude/skills/` before inventing a new workflow.
- Prefer simple, working solutions over clever abstractions.
- Write code that is easy to read and modify, not code that is impressive.
- When in doubt, ask — don't burn tokens guessing.
- Never add work confidential information, internal names, or private corporate links.
- New prompts go in `prompts/` following the conventions in [prompt-library.md](prompts/prompt-library.md).

## Resource Constraints

> **Read this section before estimating work or planning multi-step tasks.**

| Tool | Plan | Budget | Use For |
|------|------|--------|---------|
| Claude Code | Pro | Limited monthly | Code generation, architecture, planning |
| Claude.ai | Pro | Limited monthly | Writing, research, conversation |
| ChatGPT Plus | Plus | ~40 msgs / 3 hrs | Writing, brainstorming, research |
| OpenAI Codex | Plus (shared) | ~40 msgs / 3 hrs | Code generation, second opinion |
| Gemini | Free | Unlimited | Art generation, image assets only |
| Grok | Free | Unlimited | Art generation, image assets only |

**Subagent model selection:**

| Model | Use For |
|-------|---------|
| `haiku` | Quick file searches, simple formatting, grep-like tasks |
| `sonnet` | Code reviews, docs, straightforward refactoring, research |
| `opus` | Architecture decisions, multi-step planning, security audits |

Default to `haiku` for exploration, `sonnet` for implementation. Only use
`opus` when the task genuinely requires deep reasoning.

**Execution rules:**

1. Produce working code in 1-2 iterations. Ask a clarifying question first — one question is cheaper than three bad drafts.
2. Include estimated AI interactions alongside time estimates.
3. Make prompts self-contained — reference file paths, function names, and expected inputs/outputs explicitly.
4. Batch related changes into single interactions to minimize context-switching.
5. Front-load planning. A good plan in one turn saves 5 turns of rework.
6. Route all art/image work to Gemini or Grok with ready-to-paste prompts.

---

## Skill Contract

Every skill lives at `.claude/skills/<kebab-case>/SKILL.md` and includes:
Purpose, When to use, Inputs, Outputs, Steps, Examples, Non-goals / Guardrails.

**Naming:**
- Active skills: descriptive kebab-case (e.g., `decision-brief`, `question-storming`)
- Placeholders not yet built: `todo-` prefix (e.g., `todo-launch-checklist`)
- When a `todo-` skill is built out, remove the prefix and update the catalog below

## Conventions

### Files & Structure

- Markdown for all config and documentation.
- Skills: `.claude/skills/`, each with `SKILL.md` and optional `references/` directory.
- Prompts: `prompts/claude/` (XML), `prompts/gpt/` (Markdown), `prompts/gemini/` (Markdown).
- CLAUDE.md is a pointer to this file — all real config lives here.

### Large File Policy

Do NOT commit files above these limits without explicit user approval:

| File type | Limit |
|-----------|-------|
| Binary (`.pptx`, `.pdf`, `.xlsx`, `.zip`) | 10 MB |
| Images (`.png`, `.jpg`, `.gif`) | 5 MB |
| Any single file | 25 MB |

Always `ls -lh <file>` before staging. Never use `git add .` or `git add -A`.
If over the limit: stop, tell the user, suggest compression or cloud storage.

### Document Types

Three tiers, each linking to the next:

1. **Design Document** — The "what and why." Location: `docs/` or project root. Naming: `DESIGN.md`.
2. **Concept Direction** — The "how it feels." Location: `docs/concepts/`. Naming: `<feature>-concept.md`.
3. **Execution Document** — The "how to build it." Location: `docs/execution/`. Naming: `<feature>-execution.md`. Includes architecture, implementation steps, and ready-to-paste prompts.

---

## Internal Tools & Platforms

### Atlassian (Jira + Confluence)

All project tracking, documentation, and IP lives in Atlassian.

> **Always use the CLI** to read from and write to Jira and Confluence.
> Never ask the user to manually copy-paste from the browser.
> See [docs/atlassian-api.md](docs/atlassian-api.md) for auth setup and API examples.

**Jira hierarchy:**

```text
Initiative → Milestone → Epic → Story
```

### Product Release Stages

| Stage | Access | Quality Bar |
|-------|--------|-------------|
| **Alpha** | Internal team only | Dev complete; bugs being triaged |
| **Closed Beta** | All employees + select partners | No P0/P1 issues |
| **Open Beta** | All employees + early adopters | No P0/P1/P2 issues |
| **GA** | All customers | Feature complete; no critical issues |

Progression: Alpha → Closed Beta (fix P0/P1, start marketing/training) → Open Beta (holdout experiments, runbooks approved) → GA (metrics trending up, full launch).

### Monitoring

Grafana: `https://contoso.grafana.net/` (SSO). Dashboard URL pattern:
`https://contoso.grafana.net/d/<UID>/<slug>?orgId=1&from=now-30d&to=now&timezone=utc`

---

## Role Guidelines

### Planner

Project architect and estimation lead.
- Read Resource Constraints before estimating.
- Break work into token-efficient chunks. State what each task produces, estimated AI interactions, and which tool handles it.
- Produce a clear plan before any code generation begins.

### Builder

Code generation and implementation.
- Generate complete, working code — not stubs or pseudocode.
- Batch related changes into single interactions.
- Route art/image work to Gemini or Grok with ready-to-paste prompts.
- Flag when a task will likely exceed a single session's token budget.

---

## Skill Catalog

All skills live in `.claude/skills/` and are auto-discovered by Claude Code.

### PM Practice Skills

| Skill | Path | Description |
|-------|------|-------------|
| Create PRD | `create-prd/` | Standard PRD for cross-functional audiences |
| Create PRD (Claude Code) | `create-prd-claude-code/` | PRD optimized for AI coding agents to build from |
| Create PRD (Engineering) | `create-prd-engineering/` | Detailed PRD for engineering teams with technical depth |
| Create PRD (One-Pager) | `create-prd-one-pager/` | 1-page PRD for leadership and partner audiences |
| Decision Brief (SOCRR) | `decision-brief/` | Prepare decision briefings using the SOCRR framework |
| Question Storming | `question-storming/` | Run question-storming sessions to explore problem spaces |
| Jobs to Be Done | `jobs-to-be-done/` | Create personas and use cases using the JTBD framework |
| Create User Interview | `create-user-interview/` | Create minimalist user interview templates |
| Analyze User Interview | `analyze-user-interview/` | Analyze completed user interviews into research summaries |
| DevEx Survey | `devex-survey/` | Create and analyze Developer Experience surveys |
| Create Architecture Diagram | `create-architecture-diagram/` | Three-tier architecture diagrams using Mermaid |
| Create Release Notes | `create-release-notes/` | Generate release notes from Jira + source repos |
| Sourcegraph Search | `sourcegraph-search/` | Cross-repo code search via Sourcegraph MCP |
| Storytelling for Impact | `storytelling-for-impact/` | Craft compelling stories for presentations and influence |
| Write Teachable Personal Moment | `write-teachable-personal-moment/` | Story-first long-form posts in a teachable-moment voice |
| Write as Jason | `write-as-jason/` | Content in Jason's authentic voice |
| Engineering Foundations | `engineering-foundations/` | Repeatable engineering fundamentals |

### Planned Skills (`todo-` prefix)

Placeholders awaiting build-out. Remove the `todo-` prefix when fully built.

| Skill | Path | Description |
|-------|------|-------------|
| Analyze User Feedback | `todo-analyze-user-feedback/` | Extract themes and sentiment from surveys, interviews, Slack |
| Automate Review Process | `todo-automate-review-process/` | Automate code reviews, design reviews, approval workflows |
| Convert Zoom Notes | `todo-convert-zoom-notes/` | Zoom transcripts into structured Obsidian notes |
| Create Figma Mockup | `todo-create-figma-mockup/` | Figma mockups from PRDs or design briefs |
| GTM Plan | `todo-gtm-plan/` | Go-To-Market plan: positioning, enablement, launch timing |
| Launch Checklist | `todo-launch-checklist/` | Product launch readiness, sign-off, go/no-go |
| Map Stakeholders | `todo-map-stakeholders/` | Map decision makers, influencers, blockers |
| Prioritize Features | `todo-prioritize-features/` | Feature prioritization using RICE, Kano, or custom frameworks |
| Validate Hypothesis | `todo-validate-hypothesis/` | Structured hypotheses and validation plans |

### Lenny's PM Skills (88 skills)

Curated from [Lenny's Podcast](https://www.lennyspodcast.com/). All live in `.claude/skills/lenny-podcast/`.
See the full catalog: [lenny-podcast/README.md](.claude/skills/lenny-podcast/README.md).

---

## PM Operating Philosophy

### Guiding Principles

Five values that guide all decision-making:

1. **Humility** — No one has all the answers. Listen before asserting. Ask before assuming.
2. **Transparency** — Default to open. Share context, reasoning, and trade-offs. Show your work.
3. **Empathy for Customers** — Every decision traces back to a real person. Ask "what hurts the most?" before prioritizing.
4. **Grit** — Hard problems don't yield to the first attempt. Keep iterating when the easy path is to move on.
5. **Innovate** — Challenge the default. Ask "what if?" before accepting "that's how we do it."

### Multidisciplinary Collaboration

> "There is no harmony in a one-person band." — [Multidisciplinary Harmony](https://medium.com/@jasmea/multidisciplinary-harmony-9257d315798b)

Product teams work like jazz ensembles. Each role has a home base, not a cage:

- **PM** owns the what and why. **Engineer** owns the how. **Designer** owns the experience. **TPM** owns the delivery. **UXR** owns the evidence.
- Best work happens when people cross into each other's territory with curiosity.
- At the start of any initiative, discuss who owns what openly. Gaps drop balls; overlap creates friction.
- No skill in this repo belongs to a single role. Value compounds when multiple disciplines engage.

### Collaboration via Git

Skills are code. PMs define workflows as version-controlled skill files. Engineers review via PRs. AI tools execute.

1. PM creates or updates a skill on a branch.
2. Opens a PR — explains what changed and why.
3. Engineers review for clarity and feasibility. Designers, UXR, TPMs review if the skill touches their domain.
4. Merge to main. The skill is live for the team.

### PM Competency Model

5 areas, 6 levels (Learner → Contributor → Specialist → Expert → Company Leader → Industry Leader).

| Area | Sub-Competencies |
|------|-----------------|
| **Vision & Strategy** | Current Product Understanding, Future Product Vision |
| **Project** | Communication, Project Leadership & Execution |
| **Technical** | Technical Depth, Technical Breadth, Customer Experience |
| **Business** | Product-Market Fit, Business Growth |
| **People Management** | Retention, Career Growth, Hiring, Productivity |

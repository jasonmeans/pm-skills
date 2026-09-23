# pm-skills

AI-executable skills, tested helper scripts, and copy-paste prompts for product managers and the engineers, designers, and researchers they work with.

Skills are structured instructions that Claude Code and Codex discover and run, such as writing a PRD, analyzing feedback, ranking a backlog, or planning a launch. Because they are files in git, PM workflows become repeatable, shareable, and improvable through pull requests, the same way code is. PMs write and refine skills, engineers review them, and AI tools run them the same way for everyone.

## Quick Start

**Claude Code:** open this repo, then name a skill or just describe the task.

```text
/create-prd
/prioritize-features backlog.csv
/analyze-user-feedback ~/Downloads/nps-comments.csv
```

**Codex:** open this repo. Skills are discovered through `.agents/skills`, a symlink to `.claude/skills`. Mention one with `$`, as in `$launch-checklist`, or describe the task.

**Any chat tool:** copy a prompt from `prompts/` (see the [prompt library](prompts/prompt-library.md)).

**Requirements:** Python 3.9 or later for the helper scripts (standard library only; nothing to install). `analyze-ai-proficiency` needs Python 3.11 or 3.12 and sets up its own environment. On Windows, clone with `git config core.symlinks true` so the two symlinks work.

## Skills

A **(script)** tag marks skills whose counting, math, or parsing runs in a tested script instead of in the model.

### Discovery and research

| Skill | What it does |
|---|---|
| `question-storming` | Explore a problem space by generating and prioritizing questions |
| `create-user-interview` | Interview template with Mom Test-aligned questions |
| `analyze-user-interview` | Research summary from a Zoom transcript plus interview notes (script) |
| `analyze-user-feedback` | Ranked themes, sentiment, and quotes from surveys, tickets, and reviews (script) |
| `jobs-to-be-done` | Personas and a use-case table of outcomes, today, future, and north star |
| `validate-hypothesis` | Testable hypothesis, cheapest test, pre-set criteria, and sample size (script) |
| `devex-survey` | Create or analyze developer experience surveys |

### Strategy and decisions

| Skill | What it does |
|---|---|
| `prioritize-features` | RICE, ICE, weighted, or Kano ranking with a sensitivity check (script) |
| `decision-brief` | Decision briefing with the SOCRR framework |
| `map-stakeholders` | Power/interest grid, RACI, and engagement plan |

### Specs and design

| Skill | What it does |
|---|---|
| `create-prd` | Standard PRD for cross-functional teams (the default) |
| `create-prd-one-pager` | One-page PRD for leadership and partners |
| `create-prd-engineering` | Detailed PRD with data models, APIs, and acceptance criteria |
| `create-prd-claude-code` | PRD an AI coding agent can build from |
| `create-figma-mockup` | Wireframe spec plus a Figma-importable HTML mockup |
| `create-architecture-diagram` | Three-tier architecture diagrams in Mermaid |

### Launch and delivery

| Skill | What it does |
|---|---|
| `gtm-plan` | Go-to-market plan: tier, positioning, channels, enablement, timeline |
| `launch-checklist` | Stage-gate readiness review ending in go / no-go |
| `create-release-notes` | Weekly release notes from merged MRs and a feature list |
| `automate-review-process` | Risk-tiered code and design review design with a measured baseline (script) |
| `convert-meeting-notes` | Obsidian-ready notes with decisions and action items from a transcript (script) |

### Communication

| Skill | What it does |
|---|---|
| `storytelling-for-impact` | Story map for a persuasive presentation or pitch |
| `write-as-jason` | Content in Jason's voice |
| `write-teachable-personal-moment` | Story-first long-form posts in a teachable-moment voice |

### Engineering and AI workflow

| Skill | What it does |
|---|---|
| `engineering-foundations` | Weekly drills for architecture, testing, and review habits |
| `sourcegraph-search` | Cross-repo code search through the Sourcegraph MCP server |
| `analyze-ai-proficiency` | Developer AI-workflow proficiency analysis from local exports (tools/) |
| `audit-agent-environment` | Token and workflow audit of a Claude Code and Codex setup (script) |

## Scripts

Skills handle judgment. Scripts handle anything deterministic (parsing, counting, scoring, statistics, validation) because they are cheaper, testable, and add nothing to the model's context. Every script is stdlib Python with a test in `scripts/tests/`.

| Script | Purpose |
|---|---|
| `scripts/check.sh` | Run before every commit: skill lint, script tests, token audit |
| `scripts/token_audit.py` | What Claude Code and Codex load every session, for any repo (`--global`, `--codex`) |
| `scripts/lint_skills.py` | Enforce the Skill Contract (frontmatter, links, no placeholders, README catalog) |
| `scripts/vtt_to_transcript.py` | Compact a VTT transcript and flag room or device speaker labels |
| `scripts/feedback_tally.py` | Merge, de-duplicate, sample, and tally coded feedback |
| `scripts/prioritize.py` | RICE, ICE, and weighted scores with a sensitivity check; Kano classification |
| `scripts/experiment_calc.py` | A/B test sample size, duration, and significance |
| `scripts/pr_review_stats.py` | Code-review latency baseline from `gh pr list` JSON |

## How the Repo Stays Lean

Both harnesses pay for two things before your first message: the instruction file and one description line per visible skill. This repo keeps both small:

- **One instruction file.** `CLAUDE.md` is short, and `AGENTS.md` is a symlink to it, so Claude Code and Codex get the same rules with no extra file reads.
- **One skill folder.** `.agents/skills` points to `.claude/skills`, so Codex discovers the same skills Claude Code does. The instruction file never repeats a skill catalog, because both harnesses already list the skills.
- **On-demand reference.** Templates live in each skill's `references/`, long-form material lives in `docs/` and `library/`, and nothing is `@`-imported.
- **Scripts first.** Deterministic steps run in scripts, not in prose the model has to follow.
- **No placeholders.** Unbuilt skills are ideas in an issue, not descriptions loaded every session.

To audit any repo the same way ("analyze my Claude Code and Codex environment, including CLAUDE.md and AGENTS.md, for token usage, workflow optimizations, and tools vs. skills vs. scripts"), run the `audit-agent-environment` skill. Or measure directly:

```bash
python3 scripts/token_audit.py --repo ~/code/my-app --global --codex
```

## Lenny's Playbooks

`library/lenny-podcast/` holds 88 playbooks curated from [Lenny's Podcast](https://www.lennyspodcast.com/) (source: [refoundai.com/lenny-skills](https://refoundai.com/lenny-skills)), from writing PRDs to running offsites. They are reference material, read on demand and not loaded as skills. Several skills link to the relevant one. Browse the [catalog](library/lenny-podcast/README.md).

## Prompt Library

More than 30 prompts for tools without file access. XML prompts for Claude live in `prompts/claude/`, and Markdown prompts for ChatGPT and Gemini live in `prompts/gpt/` and `prompts/gemini/`. They cover PRDs, research, strategy, meetings, and developer workflows. See the [prompt library](prompts/prompt-library.md).

## Repo Structure

```text
CLAUDE.md               Agent instructions for Claude Code and Codex
AGENTS.md               -> CLAUDE.md (symlink)
.claude/skills/         Skills: SKILL.md plus optional references/ and evals/
.agents/skills          -> .claude/skills (symlink, for Codex)
scripts/                Deterministic helpers and their tests (stdlib Python)
tools/ai-proficiency/   Analysis package behind analyze-ai-proficiency
library/lenny-podcast/  88 reference playbooks (not auto-loaded)
prompts/                Copy-paste prompts by tool
docs/                   Operating philosophy and optional references
```

## Adding a Skill

1. **Deterministic?** Write a script in `scripts/` with a test instead, or have the skill call one.
2. Create `.claude/skills/<kebab-case>/SKILL.md` following the Skill Contract in [CLAUDE.md](CLAUDE.md). The description must say what the skill produces and when to use it.
3. Add it to the tables above.
4. Run `bash scripts/check.sh`.
5. Open a pull request.

## Contributing

Changes go through pull requests:

1. A PM creates or updates a skill or prompt on a branch.
2. The PR explains what changed and why.
3. Engineers review for clarity and feasibility. Design, research, and TPM review when a skill touches their area.
4. Merge to `main`, and the skill is live for everyone who uses the repo.

The collaboration model and principles behind this are in [docs/pm-operating-philosophy.md](docs/pm-operating-philosophy.md).

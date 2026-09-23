# pm-skills: Agent Instructions

Shared by Claude Code and Codex. `AGENTS.md` is a symlink to this file and `.agents/skills` is a symlink to `.claude/skills`, so both harnesses load the same rules and discover the same skills. Edit this file only.

This is a **public** library of PM and engineering skills, helper scripts, and copy-paste prompts. Never add confidential information, internal names, customer data, or private links.

## Operating Rules

- Use the closest matching skill before inventing a workflow: `/skill-name` in Claude Code, `$skill-name` in Codex, or let the description match. Prefer one workflow skill per task; if two apply, state the order.
- When in doubt, ask one clarifying question. One question is cheaper than three bad drafts.
- Prefer simple, working solutions. Write code that is easy to read and change, not code that is impressive.
- Front-load the plan for multi-step work: what each step produces, estimated AI interactions alongside time, and which tool does it. Batch related changes. Aim for working output in 1–2 iterations, and flag work likely to exceed one session.
- Outputs are markdown unless a skill says otherwise. Save them where the skill specifies (`outputs/` is gitignored); if it doesn't say, ask, and default to `~/Desktop`. Never commit user data, transcripts, feedback exports, or deliverables.
- Prompts written for another tool or a subagent must be self-contained: file paths, inputs, and the expected output.

## Scripts First: tools vs. scripts vs. skills vs. subagents

Use the lightest mechanism that does the job well:

1. **Tools**: direct commands for one-off reads, searches, git or gh queries, and single edits.
2. **Scripts** (`scripts/`): anything deterministic, such as parsing, merging, counting, scoring, math, validation, or formatting. **Never create a skill for a deterministic task.** Scripts are stdlib-only Python 3.9+, read files and write files, print a short summary, and ship with a test in `scripts/tests/`.
3. **Skills** (`.claude/skills/`): judgment-heavy procedures that repeat. A skill calls scripts for its deterministic steps and never counts or does arithmetic by hand.
4. **Subagents**: only for independent, parallel, sizable work where you need just the conclusion. Never for a single read, grep, or git status.

Graduation rule: a one-off check stays a command. The third time you run it, make it a script. A script plus recurring judgment becomes a skill that calls the script.

| Script | Purpose | Used by |
|---|---|---|
| `scripts/check.sh` | Skill lint, script tests, token audit. Run before every commit. | everyone |
| `scripts/token_audit.py` | What Claude Code and Codex load every session (`--global`, `--codex`) | `audit-agent-environment` |
| `scripts/lint_skills.py` | Enforces the Skill Contract below | `check.sh` |
| `scripts/vtt_to_transcript.py` | Compact VTT transcripts; flag room or device speaker labels | `analyze-user-interview`, `convert-meeting-notes` |
| `scripts/feedback_tally.py` | Merge, dedupe, sample, and tally coded feedback | `analyze-user-feedback` |
| `scripts/prioritize.py` | RICE, ICE, and weighted scores with sensitivity; Kano classification | `prioritize-features` |
| `scripts/experiment_calc.py` | A/B sample size, duration, significance | `validate-hypothesis` |
| `scripts/pr_review_stats.py` | Review-latency baseline from `gh pr list` JSON | `automate-review-process` |

`tools/ai-proficiency/` is the one multi-module package, with its own venv and tests. Use it through `analyze-ai-proficiency`.

## Context Budget

- Aim to finish routine tasks within 20–40% of the context window. This file and every skill description load at the start of every session in both harnesses, so keep them short.
- Read only what the active skill needs. Target sections (`rg`, `sed -n`) instead of whole files, and don't reread unchanged files.
- Large inputs (transcripts, feedback exports, PR histories) go through a script first. Read the compact output, not the raw file.
- Load heavy references only on demand: `prompts/ai-proficiency-spec.md` (42 KB), `library/lenny-podcast/` (88 playbooks, about 2.6 MB), and skill `references/` folders.
- Link, don't import. An `@path` import loads at launch; a plain path loads only when read.
- After editing this file or any skill, run `python3 scripts/token_audit.py` and keep it warning-free.

## Model and Tool Routing

- Treat Claude and Codex usage as finite budgets.
- Claude subagents: `haiku` for search and formatting, `sonnet` for docs, reviews, and routine implementation, and `opus` only for architecture, security, or multi-step planning.
- Codex runs the same skills through `.agents/skills`. Use it for a second opinion on scripts and high-stakes documents.
- Image and art work goes to Gemini or Grok as a ready-to-paste prompt.

## Skill Contract

Each skill lives at `.claude/skills/<kebab-case>/SKILL.md`, with optional `references/` for templates and deep material and optional `evals/` for trigger tests (see `create-prd`).

- **Frontmatter:** `name` matches the folder. `description` says what the skill produces and **when to use it**, plus when not to if a sibling skill is close, in under about 400 characters (hard limit 1,024). The description is the only part loaded every session and the part both harnesses match against.
- **Body:** intro, Reasoning Framework (why it exists), Output Contract table, When to Use and When NOT to Use, Inputs, Steps (calling scripts for deterministic work), Examples, Guardrails, and Related Skills. Keep it under 500 lines; move templates to `references/`.
- **No placeholders.** Never commit an unbuilt skill; its description costs tokens every session and can trigger on real requests. Track ideas in an issue.
- List every skill in the README catalog. `bash scripts/check.sh` must pass.

## Conventions

- Prompts: `prompts/claude/` (XML), `prompts/gpt/` and `prompts/gemini/` (Markdown). The catalog lives in `prompts/prompt-library.md`.
- `library/lenny-podcast/` holds reference playbooks, not skills. Check its README catalog when no skill covers a topic.
- Document tiers: `DESIGN.md` (what and why) → `docs/concepts/<feature>-concept.md` (how it feels) → `docs/execution/<feature>-execution.md` (how to build it, with ready-to-paste prompts).
- Git: stage files by name; never `git add .` or `git add -A`. Run `ls -lh` before staging binaries. Stop and ask before committing a binary over 10 MB, an image over 5 MB, or any file over 25 MB.
- Read only when relevant: `docs/pm-operating-philosophy.md` (principles, collaboration model, competency model) and `docs/atlassian-api.md` (optional Jira and Confluence REST reference).

# pm-skills

A version-controlled library of AI-executable skills and reusable prompts for Product Management and Engineering teams.

Skills are not documents. They are structured instructions that AI coding tools (Claude Code, Codex, Copilot) can discover and execute directly. This means PM workflows -- writing PRDs, analyzing user feedback, running prioritization exercises, preparing decision briefs -- become repeatable, shareable, and improvable through the same pull request process teams already use for code.

The result is a new collaboration model: PMs define and refine skills, Engineers review and sign off, and AI tools execute them consistently across the team.

---

## Quick Start

### Run a Skill

Skills are auto-discovered by Claude Code. Open your terminal and invoke one by name:

```
/create-prd
/decision-brief
/analyze-user-interview
```

Claude Code finds the matching `SKILL.md` file in `.claude/skills/` and follows its instructions. Each skill defines its purpose, required inputs, expected outputs, and step-by-step execution.

### Use a Prompt

Prompts are standalone files you copy-paste into any AI tool. They live in `prompts/` and are organized by tool:

- **Claude prompts** (XML) -- `prompts/claude/`
- **GPT prompts** (Markdown) -- `prompts/gpt/`
- **Gemini prompts** (Markdown) -- `prompts/gemini/`

Open the file, copy the contents, paste into the corresponding tool. See the [Prompt Library](prompts/prompt-library.md) for the full catalog.

---

## What Is in This Repo

### PM Practice Skills

13 active skills covering the full PM lifecycle, plus 12 planned skills (prefixed `todo-`) awaiting build-out:

**Active skills:**
- **User research** -- `create-user-interview`, `analyze-user-interview`, `jobs-to-be-done`
- **Strategy and decisions** -- `decision-brief`, `question-storming`
- **Execution** -- `create-release-notes`, `devex-survey`, `create-architecture-diagram`
- **Communication** -- `write-as-jason`, `write-teachable-personal-moment`, `storytelling-for-impact`
- **Foundations** -- `engineering-foundations`, `sourcegraph-search`

**Planned skills (`todo-` prefix):**
- `todo-create-prd`, `todo-create-prd-one-pager`, `todo-create-prd-engineering`, `todo-create-prd-claude-code`
- `todo-analyze-user-feedback`, `todo-validate-hypothesis`, `todo-prioritize-features`, `todo-map-stakeholders`
- `todo-launch-checklist`, `todo-automate-review-process`, `todo-convert-zoom-notes`, `todo-create-figma-mockup`

### Lenny's PM Skills (88 skills)

Curated from [Lenny's Podcast](https://www.lennyspodcast.com/), covering topics from writing PRDs to running offsites. All prefixed with `lenny-` (e.g., `lenny-writing-prds`, `lenny-shipping-products`, `lenny-stakeholder-alignment`). Source: [refoundai.com/lenny-skills](https://refoundai.com/lenny-skills).

### Prompt Library (30+ prompts)

XML prompts for Claude and Markdown prompts for GPT/Gemini spanning PRDs, user research, strategy docs, release notes, meeting prep, and developer workflows. See the full catalog at [prompts/prompt-library.md](prompts/prompt-library.md).

---

## Repo Structure

```
.claude/skills/          Skills auto-discovered by Claude Code (SKILL.md files)
prompts/                 Reusable prompts organized by AI tool
  claude/                XML prompts for Claude
  gpt/                   Markdown prompts for ChatGPT
  gemini/                Markdown prompts for Gemini
  prompt-library.md      Master prompt catalog and meta-prompts
docs/                    Supporting documentation
CLAUDE.md                Entry point for Claude Code (points to AGENTS.md)
AGENTS.md                Operating rules, skill catalog, and collaboration model
```

---

## Adding a New Skill

1. Create `.claude/skills/<lowercase-kebab-case>/SKILL.md`.
2. Include these sections: Purpose, When to use, Inputs, Outputs, Steps, Examples, Non-goals / Guardrails.
3. Update the skill catalog in `AGENTS.md`.

---

## Contributing

This repo uses a PR-based collaboration model:

1. **PMs** create or update skills and prompts on a branch.
2. **Engineering** reviews the PR for clarity, feasibility, and alignment with how the skill will be executed.
3. Once approved, merge to `main`.

This keeps skills version-controlled and ensures PM and Engineering stay aligned on what AI tools are doing and how.

---

## Further Reading

- [AGENTS.md](AGENTS.md) -- Guiding principles, collaboration model, skill catalog, operating rules, and project conventions
- [prompts/prompt-library.md](prompts/prompt-library.md) -- Complete prompt catalog with meta-prompts for generating new prompts

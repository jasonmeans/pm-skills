# Prompt Library

Reusable, version-controlled prompts for PM workflows across AI tools.

## Getting Started

Welcome! This library is a shared collection of prompts that make common PM tasks faster and more consistent. Here's how to get going:

### Using a prompt

1. Browse the catalog below and find a prompt that fits your task.
2. Open the file — Claude prompts are XML in `claude/`, GPT prompts are Markdown in `gpt/`.
3. Copy the content into your AI tool of choice:
   - **Claude Projects** — Paste the XML into a Project's system prompt or first message.
   - **Claude Code** — Reference prompts directly from this repo; they're version-controlled and always up to date.
   - **GPT** — Paste the Markdown into a Office 365 Copilot prompt using the GPT model as a conversation starter.
4. Follow the `<instructions>` in the prompt — most ask you to provide specific inputs (a problem statement, a feedback dump, a meeting transcript, etc.) and then produce structured output.

### Adding a new prompt

1. Pick the right folder: `claude/` for XML prompts, `gpt/` for Markdown prompts.
2. Use **kebab-case** for the filename (e.g., `sprint-retrospective-analyzer.xml`).
3. Follow the conventions of existing prompts:
   - **Claude (XML)**: Use semantic tags — `<role>`, `<context>`, `<instructions>`, `<output_template>`. Include a version in the metadata (start at `v1.0`).
   - **GPT (Markdown)**: Use Markdown with YAML frontmatter for metadata.
4. Add the prompt to the catalog table below in the appropriate section.
5. Commit and push — that's it.

### Tips

- Start with the prompts marked with a star below if you're new to the team.
- Iterate on prompts — bump the version when you improve one.
- If a prompt doesn't exist for your workflow, build it and share it back.

---

## Folder Structure

```
prompts/
  claude/       # XML-format prompts for Claude Projects & Claude Code
  gpt/          # Markdown-format prompts for ChatGPT Projects
```

## Prompt Catalog

### Claude (XML)

#### PRD & Product Documentation
| File | Purpose |
|------|---------|
| `write-prd.xml` | Generate a full Milestone PRD from a problem statement using Contoso's template |
| `prd-reviewer.xml` | Red-team a draft PRD — find gaps, missing edge cases, unclear metrics, unstated assumptions |
| `one-pager-generator.xml` | Distill a complex initiative into a 1-page executive summary |
| `technical-spec-translator.xml` | Translate between engineering specs and product-facing language |
| `api-documentation-reviewer.xml` | Review API docs for clarity, completeness, and DX best practices |
| `release-notes-writer.xml` | Generate developer-facing release notes from shipped changes |
| `rfc-decision-doc-writer.xml` | Structure a decision doc with options analysis, recommendation, and risks |

#### User & Customer Insights
| File | Purpose |
|------|---------|
| `user-feedback-analyzer.xml` | Extract themes, severity, and actionable insights from raw feedback |
| `developer-journey-mapper.xml` | Map end-to-end developer experience and identify friction points |
| `competitive-analysis-structurer.xml` | Structured comparison of competitor developer platforms |
| `customer-interview-prep.xml` | Generate interview guides with questions, probes, and listening cues |
| `feedback-to-backlog-converter.xml` | Convert feedback themes into backlog items with user stories and acceptance criteria |

#### Strategy & Communication
| File | Purpose |
|------|---------|
| `stakeholder-update-writer.xml` | Generate concise status updates — progress, blockers, decisions needed |
| `prioritization-framework-builder.xml` | Apply RICE/ICE scoring to a set of initiatives |
| `meeting-prep-brief.xml` | Generate agenda, key questions, pre-read summary, and desired outcomes |
| `quarterly-planning-narrative.xml` | Connect OKRs to strategy with sequenced initiatives |
| `exec-presentation-storyline.xml` | Structure a presentation narrative arc for leadership |

#### New PM Ramp-Up (First 90 Days)
| File | Purpose |
|------|---------|
| `codebase-architecture-interrogator.xml` | Generate smart questions about system architecture and technical debt |
| `stakeholder-map-builder.xml` | Map the org — decision makers, influencers, relationships to build |
| `domain-knowledge-accelerator.xml` | Structured learning plan for a new domain area |
| `thirty-sixty-ninety-day-plan.xml` | Structure and track onboarding goals and milestones |
| `what-ive-learned-synthesis.xml` | Synthesize raw onboarding notes into a structured knowledge base |

#### Dev Workflow (Claude Code)
| File | Purpose |
|------|---------|
| `code-review-context.xml` | Give Claude Code context for meaningful code reviews |
| `script-generator-pm-workflows.xml` | Generate utility scripts for PM data/reporting tasks |
| `gitlab-mr-description-writer.xml` | Generate well-structured MR descriptions from diffs |

#### Office 365 / Copilot
| File | Purpose |
|------|---------|
| `teams-meeting-summarizer.xml` | Extract decisions, action items, and open questions from transcripts |
| `email-thread-synthesizer.xml` | Summarize email threads into key points and required responses |
| `excel-data-analyzer.xml` | Analyze product metrics — trends, anomalies, chart recommendations |
| `powerpoint-narrative-builder.xml` | Structure a deck with narrative arc and speaker notes |
| `deep-dive-podcast-script.xml` | Generate conversational deep-dive scripts for knowledge sharing |

### GPT (Markdown)

| File | Purpose |
|------|---------|
| `craft-framework-prompt-generator.md` | Meta-prompt using CRAFT framework to generate new prompts |

## Conventions

- **Claude prompts** use XML format with semantic tags (`<role>`, `<context>`, `<instructions>`, `<output_template>`)
- **GPT prompts** use Markdown with YAML frontmatter for metadata
- **File naming**: kebab-case, descriptive (e.g., `prd-reviewer.xml`)
- **Versioning**: Each prompt tracks its version in metadata (v1.0, v1.1, etc.)

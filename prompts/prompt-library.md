# Prompt Library — Master Catalog & Generator Prompts

> **Owner:** Jason Means
> **Created:** 2026-02-12
> **Last updated:** 2026-02-25
> **Tools:** Claude (work), Claude Code (dev), ChatGPT (personal), Gemini (transcription), Grok (image/video), Office 365 Copilot (work productivity)

---

## How This Document Works

This document has three parts:

1. **Prompt Catalog** — Every prompt in the repo, organized by tool and category, with file paths
2. **Meta-Prompt for Claude (XML)** — Paste into Claude to generate new work prompts
3. **Meta-Prompt for ChatGPT (Markdown)** — Paste into ChatGPT to generate new personal prompts

For quick-start usage instructions and contribution guidelines, see [README.md](./README.md).

---

## Part 1: Prompt Catalog

### Claude Prompts — XML Format (`claude/`)

#### PRD & Product Documentation

| File | Prompt Name | Purpose |
|------|------------|---------|
| `claude/write-prd.xml` | **PRD Writer** | Generate a full Milestone PRD from a problem statement — goals, non-goals, user stories, success metrics, technical considerations, and milestones. |
| `claude/prd-reviewer.xml` | **PRD Reviewer / Red Team** | Critique a draft PRD — find gaps in scope, missing edge cases, unclear success metrics, unstated assumptions, and dependencies. |
| `claude/one-pager-generator.xml` | **One-Pager Generator** | Distill a complex initiative into a 1-page executive summary for leadership with problem, proposal, impact, and ask. |
| `claude/technical-spec-translator.xml` | **Technical Spec Translator** | Translate between engineering technical design docs and product-facing language for stakeholders. |
| `claude/api-documentation-reviewer.xml` | **API Documentation Reviewer** | Review developer-facing API docs for clarity, completeness, consistency, and DX best practices. |
| `claude/release-notes-writer.xml` | **Release Notes Writer** | Generate external-facing release notes from shipped features, bug fixes, and changes — written for a developer audience. |
| `claude/rfc-decision-doc-writer.xml` | **RFC / Decision Doc Writer** | Structure a decision document with context, options analysis, recommendation, risks, and reversibility assessment. |

#### User & Customer Insights

| File | Prompt Name | Purpose |
|------|------------|---------|
| `claude/user-feedback-analyzer.xml` | **User Feedback Analyzer** | Extract themes, severity, frequency, and actionable insights from raw user/developer feedback (support tickets, Slack threads, survey responses). |
| `claude/developer-journey-mapper.xml` | **Developer Journey Mapper** | Map end-to-end developer experience for a specific workflow — identify friction points, drop-offs, and opportunities. |
| `claude/competitive-analysis-structurer.xml` | **Competitive Analysis Structurer** | Structured comparison of a competitor's developer platform (API design, docs, DX) against your offering. |
| `claude/customer-interview-prep.xml` | **Customer Interview Prep** | Generate an interview guide with open-ended questions, follow-up probes, and things to listen for. |
| `claude/feedback-to-backlog-converter.xml` | **Feedback-to-Backlog Converter** | Convert synthesized feedback themes into backlog items with user stories, acceptance criteria, and priority rationale. |

#### Strategy & Communication

| File | Prompt Name | Purpose |
|------|------------|---------|
| `claude/stakeholder-update-writer.xml` | **Stakeholder Update Writer** | Generate concise status updates for cross-functional stakeholders — progress, blockers, decisions needed, next steps. |
| `claude/prioritization-framework-builder.xml` | **Prioritization Framework Builder** | Apply RICE, ICE, or custom prioritization to a set of initiatives with structured scoring and rationale. |
| `claude/meeting-prep-brief.xml` | **Meeting Prep Brief** | Generate agenda, key questions, pre-read summary, and desired outcomes for a meeting. |
| `claude/quarterly-planning-narrative.xml` | **Quarterly Planning Narrative** | Connect team OKRs to company strategy, articulate the "why now," and sequence initiatives. |
| `claude/exec-presentation-storyline.xml` | **Exec Presentation Storyline** | Structure a presentation narrative arc for leadership — situation, complication, resolution format with data callouts. |

#### New PM Ramp-Up (First 90 Days)

| File | Prompt Name | Purpose |
|------|------------|---------|
| `claude/codebase-architecture-interrogator.xml` | **Codebase & Architecture Interrogator** | Generate smart questions about system architecture, data flows, and technical debt — tailored to developer platforms. |
| `claude/stakeholder-map-builder.xml` | **Stakeholder Map Builder** | Map the org — decision makers, influencers, relationships to build and why. |
| `claude/domain-knowledge-accelerator.xml` | **Domain Knowledge Accelerator** | Generate a structured learning plan for a topic area with key concepts, questions to ask, and things to read. |
| `claude/thirty-sixty-ninety-day-plan.xml` | **30-60-90 Day Plan** | Structure and track onboarding goals, learnings, quick wins, and relationship-building milestones. |
| `claude/what-ive-learned-synthesis.xml` | **"What I've Learned" Synthesis** | Synthesize raw onboarding notes into a structured knowledge base — themes, open questions, hypotheses. |

#### Dev Workflow (Claude Code)

| File | Prompt Name | Purpose |
|------|------------|---------|
| `claude/code-review-context.xml` | **Code Review Context** | Give Claude Code context about codebase patterns, conventions, and architecture for meaningful code reviews. |
| `claude/script-generator-pm-workflows.xml` | **Script Generator for PM Workflows** | Generate utility scripts (Python/bash) for PM tasks — data extraction, metric dashboards, automated reporting. |
| `claude/gitlab-mr-description-writer.xml` | **MR Description Writer** | Generate well-structured merge request descriptions from a diff — what changed, why, testing done, rollback plan. |

#### Office 365 / Copilot

| File | Prompt Name | Purpose |
|------|------------|---------|
| `claude/teams-meeting-summarizer.xml` | **Teams Meeting Summarizer** | Extract decisions, action items, owners, deadlines, and open questions from a Teams transcript. |
| `claude/email-thread-synthesizer.xml` | **Email Thread Synthesizer** | Summarize a long Outlook email thread into key points, decisions, and what response is needed. |
| `claude/excel-data-analyzer.xml` | **Excel Data Analyzer** | Analyze product metrics in Excel — trends, anomalies, pivot table suggestions, chart recommendations. |
| `claude/powerpoint-narrative-builder.xml` | **PowerPoint Narrative Builder** | Structure a deck with a clear narrative arc, speaker notes, and data visualization suggestions. |
| `claude/deep-dive-podcast-script.xml` | **Deep Dive Podcast Script** | Generate a conversational deep-dive script from uploaded docs — good for team knowledge sharing. |

#### General / Uncategorized

| File | Prompt Name | Purpose |
|------|------------|---------|
| `claude/es-product-manager.xml` | **ES Product Manager** | Product management prompt tailored for ES (engineering systems) context. |

---

### GPT Prompts — Markdown Format (`gpt/`)

| File | Prompt Name | Purpose |
|------|------------|---------|
| `gpt/craft-framework-prompt-generator.md` | **CRAFT Framework Prompt Generator** | Meta-prompt using the CRAFT framework to generate new prompts for any tool or use case. |

---

### Gemini Prompts — Markdown Format (`gemini/`)

| File | Prompt Name | Purpose |
|------|------------|---------|
| `gemini/youtube-summary.md` | **YouTube Summary** | Summarize and structure a YouTube video transcript into readable markdown with key points and timestamps. |

---

## Part 2: Meta-Prompt for Claude (XML Format)

Use this prompt in a Claude Project to generate any work prompt from the catalog above. Paste this as your project's system prompt or as the first message when creating a new prompt.

```xml
<system>
<role>
You are a senior prompt engineer specializing in creating production-grade prompts
for product managers working on developer platforms in adtech. You create prompts
that are structured in XML format, designed for use in Claude Projects.
</role>

<context>
<user_profile>
  <title>Product Manager, Developer Platforms</title>
  <domain>Programmatic advertising, developer tools, APIs, SDKs, developer experience</domain>
  <tools>
    <primary_ai>Claude (chat + projects)</primary_ai>
    <dev_ai>Claude Code</dev_ai>
    <work_notes>Markdown and XML files in a version-controlled repo</work_notes>
    <work_suite>Office 365 with Copilot</work_suite>
  </tools>
  <workflow>
    Uses Claude Projects for high-context, ongoing workstreams.
    Each project has persistent context and specialized prompts.
    Outputs are typically markdown docs, PRDs, analysis, or structured data.
  </workflow>
</user_profile>
</context>

<instructions>
When I ask you to create a prompt, follow this process:

<step number="1" name="Clarify">
  Confirm which prompt I want (I'll reference by file name or give a description).
  Ask 1-2 clarifying questions ONLY if truly needed — do not over-ask.
</step>

<step number="2" name="Design">
  Design the prompt with these components:
  <component name="prompt_metadata">
    Include: file name, prompt name, version, last updated, category
  </component>
  <component name="role_definition">
    Define who Claude is acting as — be specific to the task domain.
    Ground the role in the developer platform context where relevant.
  </component>
  <component name="task_specification">
    Crystal clear description of what the prompt should accomplish.
    Include explicit input format (what the user will provide).
    Include explicit output format (what Claude should produce).
  </component>
  <component name="constraints_and_guidelines">
    Quality bars, anti-patterns to avoid, company-specific conventions.
    Include both positive examples (do this) and negative examples (not this).
  </component>
  <component name="output_structure">
    XML-tagged output sections so results are parseable and consistent.
    Every prompt should produce structured, reusable output.
  </component>
  <component name="examples" optional="true">
    Include 1-2 few-shot examples for complex prompts.
    Keep examples realistic to the developer platform / adtech domain.
  </component>
</step>

<step number="3" name="Deliver">
  Output the final prompt wrapped in a code block as valid XML.
  The prompt should be copy-paste ready for a Claude Project.
  After delivering, suggest 2-3 ways to customize or extend the prompt.
</step>

<quality_standards>
  <standard>Every prompt must produce output that is immediately usable — no fluff, no filler</standard>
  <standard>Prompts should be opinionated about best practices, not wishy-washy</standard>
  <standard>Include domain-specific context where it sharpens the output — omit where generic is fine</standard>
  <standard>Prefer structured output (tables, tagged sections) over walls of prose</standard>
  <standard>Every prompt should handle edge cases gracefully with fallback instructions</standard>
  <standard>Prompts should encourage Claude to ask for missing critical inputs rather than guessing</standard>
</quality_standards>

<formatting_rules>
  <rule>All prompts use XML structure with semantic tag names</rule>
  <rule>Use snake_case for XML tag names</rule>
  <rule>Include xml comments for sections that need explanation</rule>
  <rule>Keep prompts under 2000 tokens unless the task requires few-shot examples</rule>
  <rule>Version prompts as v1.0, v1.1, etc.</rule>
</formatting_rules>
</instructions>
</system>
```

---

## Part 3: Meta-Prompt for ChatGPT (Markdown Format)

Use this prompt in a ChatGPT Project to generate any personal prompt from the catalog above.

````markdown
# System: Personal Prompt Generator

## Who You Are
You are an expert prompt engineer creating high-quality, reusable prompts for personal
projects. You create prompts in clean Markdown format, optimized for storage in Obsidian
and Notion.

## About Me
- I'm a product manager who applies structured thinking to personal interests
- My personal tools: ChatGPT (chat + projects), Gemini (video transcription),
  Grok (image/video creation), Notion (knowledge base), Obsidian (local markdown)
- I value: evidence-based information, structured outputs, actionable takeaways,
  and building a personal knowledge system over time
- My interests: personal/family health, audio equipment & vinyl records,
  photography, continuous learning via YouTube

## How to Create a Prompt
When I ask you to create a prompt (I'll describe what I need or reference the planned prompts list):

### 1. Confirm & Clarify
- Confirm which prompt I want
- Ask 1-2 clarifying questions only if critical

### 2. Design the Prompt with These Sections

**Header Block:**
```
---
name: [prompt name]
version: v1.0
category: [health | audio | photography | learning | creative]
tool: [ChatGPT | Gemini | Grok]
output_format: [markdown | notion page | obsidian note | image prompt]
last_updated: YYYY-MM-DD
---
```

**Role:** Define who the AI is acting as — be specific and expert-level.

**Context:** What background knowledge the AI needs to do this well.

**Task:** Exactly what the prompt accomplishes. Include:
- What input the user provides
- What output the AI produces
- The structure/format of the output

**Quality Standards:**
- What "good" looks like
- Common mistakes to avoid
- How to handle ambiguity or missing info

**Output Template:** A reusable template that structures every response consistently.

### 3. Deliver
- Output the final prompt in a clean markdown code block
- Make it copy-paste ready
- Suggest 2-3 ways to customize it

## Quality Rules
- Every prompt produces output I can directly paste into Notion or Obsidian
- Outputs should build my personal knowledge base over time — accumulative, not disposable
- Be opinionated about quality — don't give me wishy-washy "it depends" outputs
- Personal health prompts should always caveat with "discuss with your doctor"
- Gear/purchase prompts should always include budget context
- Learning prompts should connect new knowledge to what I already know
````

---

## Part 4: Quick Reference — Where Everything Lives

| What | Format | Stored In | AI Tool |
|------|--------|-----------|---------|
| Work prompts | XML | `prompts/claude/` in this repo | Claude Projects / Claude Code |
| GPT prompts | Markdown | `prompts/gpt/` in this repo | ChatGPT |
| Gemini prompts | Markdown | `prompts/gemini/` in this repo | Gemini |
| Personal prompts (planned) | Markdown | TBD — `prompts/gpt/` or Obsidian | ChatGPT / Gemini / Grok |
| Meeting/email analysis | Natural language | O365 | Copilot |

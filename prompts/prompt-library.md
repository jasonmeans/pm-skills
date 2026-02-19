# Prompt Library — Master Catalog & Generator Prompts

> **Owner:** Jason Means
> **Created:** 2026-02-12
> **Tools:** Claude (work), Claude Code (dev), ChatGPT (personal), Gemini (transcription), Grok (image/video), Office 365 Copilot (work productivity)

---

## How This Document Works

This document has three parts:

1. **Prompt Catalog** — Every prompt you need, organized by tool and context
2. **Meta-Prompt for Claude (XML)** — Paste this into Claude to generate any work prompt from the catalog
3. **Meta-Prompt for ChatGPT (Markdown)** — Paste this into ChatGPT to generate any personal prompt from the catalog

---

## Part 1: Prompt Catalog

### 🏢 WORK — Claude Projects (XML Format, stored in GitLab)

#### Project: PRD & Product Documentation

| # | Prompt Name | Purpose |
|---|------------|---------|
| W-01 | **PRD Writer** | Generate a full PRD from a problem statement, including goals, non-goals, user stories, success metrics, technical considerations, and milestones. Tailored to TTD's developer platform context. |
| W-02 | **PRD Reviewer / Red Team** | Critique a draft PRD — find gaps in scope, missing edge cases, unclear success metrics, unstated assumptions, and dependencies. |
| W-03 | **One-Pager Generator** | Distill a complex initiative into a 1-page executive summary for leadership with problem, proposal, impact, and ask. |
| W-04 | **Technical Spec Translator** | Take an engineering technical design doc and translate it into product-facing language for stakeholders, or vice versa. |
| W-05 | **API Documentation Reviewer** | Review developer-facing API docs for clarity, completeness, consistency, and developer experience best practices. |
| W-06 | **Release Notes Writer** | Generate external-facing release notes from a list of shipped features, bug fixes, and changes — written for a developer audience. |
| W-07 | **RFC/Decision Doc Writer** | Structure a decision document with context, options analysis, recommendation, risks, and reversibility assessment. |

#### Project: User & Customer Insights

| # | Prompt Name | Purpose |
|---|------------|---------|
| W-08 | **User Feedback Analyzer** | Take raw user/developer feedback (support tickets, Slack threads, survey responses) and extract themes, severity, frequency, and actionable insights. |
| W-09 | **Developer Journey Mapper** | Map the end-to-end developer experience for a specific workflow on TTD's platform — identify friction points, drop-offs, and opportunities. |
| W-10 | **Competitive Analysis Structurer** | Analyze a competitor's developer platform (API design, docs, DX) against TTD's offering with a structured comparison framework. |
| W-11 | **Customer Interview Prep** | Generate an interview guide with open-ended questions, follow-up probes, and things to listen for, given a research objective. |
| W-12 | **Feedback-to-Backlog Converter** | Take synthesized feedback themes and convert them into well-structured backlog items with user stories, acceptance criteria, and priority rationale. |

#### Project: Strategy & Communication

| # | Prompt Name | Purpose |
|---|------------|---------|
| W-13 | **Stakeholder Update Writer** | Generate a concise status update email/doc for cross-functional stakeholders — progress, blockers, decisions needed, next steps. |
| W-14 | **Prioritization Framework Builder** | Apply RICE, ICE, or custom prioritization to a set of initiatives with structured scoring and rationale. |
| W-15 | **Meeting Prep Brief** | Given a meeting topic and attendees, generate an agenda, key questions to drive, pre-read summary, and desired outcomes. |
| W-16 | **Quarterly Planning Narrative** | Write a planning narrative that connects team OKRs to company strategy, articulates the "why now," and sequences initiatives. |
| W-17 | **Exec Presentation Storyline** | Structure a presentation narrative arc for leadership — situation, complication, resolution format with data callouts. |

#### Project: New PM Ramp-Up (First 90 Days @ TTD)

| # | Prompt Name | Purpose |
|---|------------|---------|
| W-18 | **Codebase & Architecture Interrogator** | Generate smart questions to ask engineers about system architecture, data flows, and technical debt — tailored to developer platforms. |
| W-19 | **Stakeholder Map Builder** | Help map the org — who owns what, who are decision makers vs. influencers, who to build relationships with and why. |
| W-20 | **Domain Knowledge Accelerator** | Given a topic area (e.g., programmatic advertising, RTB, identity resolution), generate a structured learning plan with key concepts, questions to ask, and things to read. |
| W-21 | **30-60-90 Day Plan Tracker** | Structure and track onboarding goals, learnings, quick wins, and relationship-building milestones. |
| W-22 | **"What I've Learned" Synthesis** | Take raw notes from onboarding conversations and synthesize into a structured knowledge base — themes, open questions, hypotheses. |

#### Project: Claude Code (Dev Workflow)

| # | Prompt Name | Purpose |
|---|------------|---------|
| W-23 | **Code Review Context Prompt** | Give Claude Code context about TTD's codebase patterns, conventions, and architecture so it can do meaningful code reviews. |
| W-24 | **Script Generator for PM Workflows** | Generate utility scripts (Python/bash) for PM tasks — data extraction, metric dashboards, automated reporting. |
| W-25 | **GitLab MR Description Writer** | Generate well-structured merge request descriptions from a diff — what changed, why, testing done, rollback plan. |

#### Project: Office 365 Copilot Prompts

| # | Prompt Name | Purpose |
|---|------------|---------|
| W-26 | **Teams Meeting Summarizer** | Post-meeting: extract decisions, action items, owners, deadlines, and open questions from a Teams transcript. |
| W-27 | **Email Thread Synthesizer** | Summarize a long Outlook email thread into key points, decisions, and what response is needed from you. |
| W-28 | **Excel Data Analyzer** | Analyze product metrics in Excel — trends, anomalies, pivot table suggestions, chart recommendations. |
| W-29 | **PowerPoint Narrative Builder** | Structure a deck in PowerPoint with a clear narrative arc, speaker notes, and data visualization suggestions. |
| W-30 | **Deep Dive Podcast Script (NotebookLM-style)** | Generate a conversational deep-dive script from uploaded docs for the O365 podcast feature — good for team knowledge sharing. |

---

### 🏠 PERSONAL — ChatGPT Projects (Markdown Format, stored in Notion/Obsidian)

#### Project: Personal Health

| # | Prompt Name | Purpose |
|---|------------|---------|
| P-01 | **Health Research Synthesizer** | Take a health topic and provide an evidence-based summary with key findings, what to discuss with your doctor, and reliable sources. |
| P-02 | **Supplement/Medication Interaction Checker** | Given a list of supplements/medications, flag potential interactions, timing considerations, and questions for your physician. |
| P-03 | **Family Health Tracker Organizer** | Structure health information for family members — appointments, medications, history, provider contacts — as a Notion database template. |
| P-04 | **Fitness & Nutrition Plan Reviewer** | Review a workout/nutrition plan for balance, sustainability, and alignment with stated health goals. |
| P-05 | **Lab Results Interpreter** | Help understand lab work results — what's in range, what's flagged, what questions to ask your doctor at follow-up. |

#### Project: Audio / Music Equipment / Vinyl Records

| # | Prompt Name | Purpose |
|---|------------|---------|
| P-06 | **Gear Research & Comparison** | Compare audio equipment (turntables, speakers, DACs, amps) with specs, pros/cons, and value-for-money analysis at a given budget. |
| P-07 | **Vinyl Record Valuation** | Research a specific pressing — identify edition, pressing plant, value range, and condition grading guidance. |
| P-08 | **Audio Setup Optimizer** | Given your current equipment chain, suggest optimal placement, settings, cables, and upgrades for best sound quality. |
| P-09 | **Record Collection Cataloger** | Structure a vinyl collection database for Notion — artist, album, pressing, condition, purchase price, current value, notes. |
| P-10 | **Music Discovery Engine** | Based on artists/albums you love, surface deep-cut recommendations with reasoning, pressing recommendations, and where to find them. |

#### Project: Photography

| # | Prompt Name | Purpose |
|---|------------|---------|
| P-11 | **Photo Trip Planner** | Plan a photography outing — golden hour times, location scouting, shot list, gear checklist, weather considerations. |
| P-12 | **Editing Workflow Advisor** | Given a style reference or mood, suggest Lightroom/editing settings, presets, and processing workflow. |
| P-13 | **Gear Purchase Advisor** | Compare camera bodies, lenses, or accessories for specific use cases with real-world performance considerations. |
| P-14 | **Portfolio Curator** | Help select and sequence photos for a portfolio or social media series with narrative and visual flow guidance. |
| P-15 | **Photography Learning Path** | Structure a skill-building plan for a specific technique (e.g., astrophotography, street photography) with resources and practice exercises. |

#### Project: Gemini — YouTube Learning Pipeline

| # | Prompt Name | Purpose |
|---|------------|---------|
| P-16 | **Video Transcript Cleaner** | Take a raw YouTube transcript and clean it into readable, structured markdown with headers, key points, and timestamps. |
| P-17 | **Video-to-Notion Knowledge Page** | Transform a cleaned transcript into a structured Notion page — summary, key takeaways, quotes, action items, related topics. |
| P-18 | **Learning Synthesis Connector** | Take multiple video transcripts on related topics and synthesize into a unified knowledge document with cross-references. |
| P-19 | **Video Recommendation Engine** | Given topics you're learning about, suggest the highest-quality YouTube channels and specific videos with reasoning. |

#### Project: Grok — Visual Content Creation

| # | Prompt Name | Purpose |
|---|------------|---------|
| P-20 | **Image Generation Brief** | Given a concept, generate a detailed Grok image prompt with style, composition, lighting, mood, and technical specifications. |
| P-21 | **Short Video Storyboard** | Plan a short-form video — shot list, transitions, text overlays, music cues, and aspect ratio considerations. |
| P-22 | **Image Modification Director** | Describe precise modifications to an existing image — what to change, what to preserve, style consistency notes. |

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
  <company>The Trade Desk (TTD)</company>
  <tenure>New hire, approximately 2 months in</tenure>
  <domain>Programmatic advertising, developer tools, APIs, SDKs, developer experience</domain>
  <tools>
    <primary_ai>Claude (chat + projects)</primary_ai>
    <dev_ai>Claude Code</dev_ai>
    <work_notes>Markdown and XML files in GitLab</work_notes>
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
  Confirm which prompt from the catalog I want (I'll reference by ID like W-01 or give a description).
  Ask 1-2 clarifying questions ONLY if truly needed — do not over-ask.
</step>

<step number="2" name="Design">
  Design the prompt with these components:
  <component name="prompt_metadata">
    Include: prompt ID, name, version, last updated, category
  </component>
  <component name="role_definition">
    Define who Claude is acting as — be specific to the task domain.
    Ground the role in TTD's developer platform context where relevant.
  </component>
  <component name="task_specification">
    Crystal clear description of what the prompt should accomplish.
    Include explicit input format (what the user will provide).
    Include explicit output format (what Claude should produce).
  </component>
  <component name="constraints_and_guidelines">
    Quality bars, anti-patterns to avoid, TTD-specific conventions.
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
  <standard>Include TTD/adtech context where it sharpens the output — omit where generic is fine</standard>
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
When I ask you to create a prompt (I'll reference an ID like P-01 or describe what I need):

### 1. Confirm & Clarify
- Confirm which prompt I want
- Ask 1-2 clarifying questions only if critical

### 2. Design the Prompt with These Sections

**Header Block:**
```
---
id: [prompt ID]
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
| Work prompts (W-01 to W-30) | XML | GitLab repo | Claude Projects |
| Personal prompts (P-01 to P-22) | Markdown | GitHub / Obsidian | ChatGPT Projects |
| Video transcripts | Markdown | Notion | Gemini |
| Visual content prompts | Plain text | Obsidian | Grok |
| Meeting/email analysis | Natural language | O365 | Copilot |
| Dev scripts & automation | Code files | GitLab | Claude Code |

---

## Getting Started — Recommended Build Order

### Week 1: High-Impact Work Prompts
1. **W-01** PRD Writer — you'll use this constantly
2. **W-08** User Feedback Analyzer — immediate value from incoming signals
3. **W-18** Codebase & Architecture Interrogator — accelerate your ramp
4. **W-20** Domain Knowledge Accelerator — learn adtech/TTD faster
5. **W-13** Stakeholder Update Writer — weekly visibility

### Week 2: Workflow & Communication
6. **W-02** PRD Reviewer — pair with W-01 for self-review
7. **W-15** Meeting Prep Brief — win every meeting
8. **W-26** Teams Meeting Summarizer — stop losing action items
9. **W-07** RFC/Decision Doc Writer — drive decisions cleanly
10. **W-22** "What I've Learned" Synthesis — compound your onboarding

### Week 3: Personal Prompts
11. **P-16** Video Transcript Cleaner — improve your learning pipeline
12. **P-17** Video-to-Notion Knowledge Page — build your knowledge base
13. **P-06** Gear Research & Comparison — for your next audio purchase
14. **P-01** Health Research Synthesizer — family health decisions
15. **P-20** Image Generation Brief — level up Grok outputs

### Ongoing
Build remaining prompts as needs arise. Version and iterate.

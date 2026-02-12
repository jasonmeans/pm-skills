# AGENTS

Use this repository as a tool-agnostic, portable skill library.

### Token Budgets

The developer has limited token budgets across all AI coding assistants:

| Tool | Plan | Budget | Context | Use For |
|------|------|--------|---------|---------|
| Claude Code | Pro | Limited monthly | — | Code generation, architecture, planning |
| Claude.ai | Pro | Limited monthly | — | Writing, research, conversation |
| ChatGPT Plus | Plus | ~40 msgs / 3 hrs | 128K tokens | Writing, brainstorming, research |
| OpenAI Codex | Plus (shared) | ~40 msgs / 3 hrs | 128K tokens | Code generation, second opinion |

Available for **unlimited** use:

| Tool | Plan | Use For |
|------|------|---------|
| Gemini | Free | Art generation, image assets only |
| Grok | Free | Art generation, image assets only |

## Operating Rules

- Use the closest matching skill in `.claude/skills/` before inventing a new workflow.
- Keep all content personal-only and reusable across assistants.
- Never add work confidential information, internal names, or private corporate links.
- Prefer concise instructions, concrete examples, and explicit guardrails.

## Skill Contract

Every skill must live at `.claude/skills/<lowercase-kebab-case>/SKILL.md` and include:
- Purpose
- When to use
- Inputs
- Outputs
- Steps
- Examples
- Non-goals / Guardrails

## Skill Catalog

All skills live in `.claude/skills/` and are auto-discovered by Claude Code.

### Jason's Skills

Personal skills by Jason Means.

| Skill | Path | Description |
|-------|------|-------------|
| Write in Jasmea Voice | `.claude/skills/write-in-jasmea-voice/` | Draft and revise long-form writing in Jason's Medium voice |
| Write as Jason | `.claude/skills/write-as-jason/` | Write content in Jason's authentic voice — blog posts, LinkedIn, memos, talks |
| Storytelling for Impact | `.claude/skills/storytelling-for-impact/` | Craft compelling stories for presentations and influence |
| Engineering Foundations | `.claude/skills/engineering-foundations/` | Build repeatable engineering fundamentals across architecture, testing, and delivery |

### Lenny's PM Skills (prefixed `lenny-`)

Curated from [Lenny's Podcast](https://www.lennyspodcast.com/). Source: [refoundai.com/lenny-skills](https://refoundai.com/lenny-skills).

| Skill | Path | Description |
|-------|------|-------------|
| AI Evals | `lenny-ai-evals` | AI evaluation strategies |
| AI Product Strategy | `lenny-ai-product-strategy` | AI product strategy |
| Analytical Thinking Interviews | `lenny-analytical-thinking-interviews` | Analytical thinking interview prep |
| Analyzing User Feedback | `lenny-analyzing-user-feedback` | Analyzing user feedback |
| Behavioral Product Design | `lenny-behavioral-product-design` | Behavioral product design |
| Brand Storytelling | `lenny-brand-storytelling` | Brand storytelling |
| Building a Promotion Case | `lenny-building-a-promotion-case` | Building a promotion case |
| Building Sales Team | `lenny-building-sales-team` | Building a sales team |
| Building Team Culture | `lenny-building-team-culture` | Building team culture |
| Building with LLMs | `lenny-building-with-llms` | Building with LLMs |
| Career Transitions | `lenny-career-transitions` | Career transitions |
| Coaching PMs | `lenny-coaching-pms` | Coaching PMs |
| Community Building | `lenny-community-building` | Community building |
| Competitive Analysis | `lenny-competitive-analysis` | Competitive analysis |
| Conducting Interviews | `lenny-conducting-interviews` | Conducting interviews |
| Conducting User Interviews | `lenny-conducting-user-interviews` | Conducting user interviews |
| Content Marketing | `lenny-content-marketing` | Content marketing |
| Cross-Functional Collaboration | `lenny-cross-functional-collaboration` | Cross-functional collaboration |
| Defining Product Vision | `lenny-defining-product-vision` | Defining product vision |
| Delegating Work | `lenny-delegating-work` | Delegating work |
| Design Engineering | `lenny-design-engineering` | Design engineering |
| Design Systems | `lenny-design-systems` | Design systems |
| Designing Growth Loops | `lenny-designing-growth-loops` | Designing growth loops |
| Designing Surveys | `lenny-designing-surveys` | Designing surveys |
| Dogfooding | `lenny-dogfooding` | Dogfooding |
| Energy Management | `lenny-energy-management` | Energy management |
| Engineering Culture | `lenny-engineering-culture` | Engineering culture |
| Enterprise Sales | `lenny-enterprise-sales` | Enterprise sales |
| Evaluating Candidates | `lenny-evaluating-candidates` | Evaluating candidates |
| Evaluating New Technology | `lenny-evaluating-new-technology` | Evaluating new technology |
| Evaluating Trade-offs | `lenny-evaluating-trade-offs` | Evaluating trade-offs |
| Finding Mentors & Sponsors | `lenny-finding-mentors-sponsors` | Finding mentors and sponsors |
| Founder Sales | `lenny-founder-sales` | Founder sales |
| Fundraising | `lenny-fundraising` | Fundraising |
| Giving Presentations | `lenny-giving-presentations` | Giving presentations |
| Having Difficult Conversations | `lenny-having-difficult-conversations` | Having difficult conversations |
| Launch Marketing | `lenny-launch-marketing` | Launch marketing |
| Managing Imposter Syndrome | `lenny-managing-imposter-syndrome` | Managing imposter syndrome |
| Managing Tech Debt | `lenny-managing-tech-debt` | Managing tech debt |
| Managing Timelines | `lenny-managing-timelines` | Managing timelines |
| Managing Up | `lenny-managing-up` | Managing up |
| Marketplace Liquidity | `lenny-marketplace-liquidity` | Marketplace liquidity |
| Measuring Product-Market Fit | `lenny-measuring-product-market-fit` | Measuring product-market fit |
| Media Relations | `lenny-media-relations` | Media relations |
| Negotiating Offers | `lenny-negotiating-offers` | Negotiating offers |
| Onboarding New Hires | `lenny-onboarding-new-hires` | Onboarding new hires |
| Organizational Design | `lenny-organizational-design` | Organizational design |
| Organizational Transformation | `lenny-organizational-transformation` | Organizational transformation |
| Partnership & BD | `lenny-partnership-bd` | Partnership and business development |
| Personal Productivity | `lenny-personal-productivity` | Personal productivity |
| Planning Under Uncertainty | `lenny-planning-under-uncertainty` | Planning under uncertainty |
| Platform Infrastructure | `lenny-platform-infrastructure` | Platform infrastructure |
| Platform Strategy | `lenny-platform-strategy` | Platform strategy |
| Positioning & Messaging | `lenny-positioning-messaging` | Positioning and messaging |
| Post-Mortems & Retrospectives | `lenny-post-mortems-retrospectives` | Post-mortems and retrospectives |
| Pricing Strategy | `lenny-pricing-strategy` | Pricing strategy |
| Prioritizing Roadmap | `lenny-prioritizing-roadmap` | Prioritizing roadmap |
| Problem Definition | `lenny-problem-definition` | Problem definition |
| Product-Led Sales | `lenny-product-led-sales` | Product-led sales |
| Product Operations | `lenny-product-operations` | Product operations |
| Product Sense Interviews | `lenny-product-sense-interviews` | Product sense interview prep |
| Product Taste & Intuition | `lenny-product-taste-intuition` | Product taste and intuition |
| Retention & Engagement | `lenny-retention-engagement` | Retention and engagement |
| Running Decision Processes | `lenny-running-decision-processes` | Running decision processes |
| Running Design Reviews | `lenny-running-design-reviews` | Running design reviews |
| Running Effective 1:1s | `lenny-running-effective-1-1s` | Running effective 1:1s |
| Running Effective Meetings | `lenny-running-effective-meetings` | Running effective meetings |
| Running Offsites | `lenny-running-offsites` | Running offsites |
| Sales Compensation | `lenny-sales-compensation` | Sales compensation |
| Sales Qualification | `lenny-sales-qualification` | Sales qualification |
| Scoping & Cutting | `lenny-scoping-cutting` | Scoping and cutting |
| Setting OKRs & Goals | `lenny-setting-okrs-goals` | Setting OKRs and goals |
| Shipping Products | `lenny-shipping-products` | Shipping products |
| Stakeholder Alignment | `lenny-stakeholder-alignment` | Stakeholder alignment |
| Startup Ideation | `lenny-startup-ideation` | Startup ideation |
| Startup Pivoting | `lenny-startup-pivoting` | Startup pivoting |
| Systems Thinking | `lenny-systems-thinking` | Systems thinking |
| Team Rituals | `lenny-team-rituals` | Team rituals |
| Technical Roadmaps | `lenny-technical-roadmaps` | Technical roadmaps |
| Usability Testing | `lenny-usability-testing` | Usability testing |
| User Onboarding | `lenny-user-onboarding` | User onboarding |
| Vibe Coding | `lenny-vibe-coding` | Vibe coding |
| Working Backwards | `lenny-working-backwards` | Working backwards |
| Writing Job Descriptions | `lenny-writing-job-descriptions` | Writing job descriptions |
| Writing North Star Metrics | `lenny-writing-north-star-metrics` | Writing north star metrics |
| Writing PRDs | `lenny-writing-prds` | Writing PRDs |
| Writing Specs & Designs | `lenny-writing-specs-designs` | Writing specs and designs |
| Written Communication | `lenny-written-communication` | Written communication |

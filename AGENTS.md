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

- Use the closest matching skill in `skills/` before inventing a new workflow.
- Keep all content personal-only and reusable across assistants.
- Never add work confidential information, internal names, or private corporate links.
- Prefer concise instructions, concrete examples, and explicit guardrails.

## Skill Contract

Every skill must live at `skills/<lowercase-kebab-case>/SKILL.md` and include:
- Purpose
- When to use
- Inputs
- Outputs
- Steps
- Examples
- Non-goals / Guardrails

## Available Skills

- `write-in-jasmea-voice`: Draft and revise long-form writing in Jason Means' personal Medium voice.
  File: `skills/write-in-jasmea-voice/SKILL.md`
- `engineering-foundations`: Build repeatable engineering fundamentals across architecture, testing, and delivery.
  File: `skills/engineering-foundations/SKILL.md`

## Skill Catalog

All skills live in `.claude/skills/` and are auto-discovered by Claude Code. Invoke any skill with `/skill-name` or let Claude load them automatically when relevant.

### Jason's PM Skills (`.claude/skills/jasons-pm-skills/`)

Personal skills by Jason Means (jason.means@thetradedesk.com).

| Skill | Invoke | Description |
|-------|--------|-------------|
| Write as Jason | `/write-as-jason` | Write content in Jason's authentic voice — blog posts, LinkedIn posts, memos, talks |
| Storytelling for Impact | `/storytelling-for-impact` | Craft compelling stories for presentations, writing, and influence |

### Lenny's PM Skills (`.claude/skills/lennys-pm-skills/`)

Curated from [Lenny's Podcast](https://www.lennyspodcast.com/). Source: [refoundai.com/lenny-skills](https://refoundai.com/lenny-skills).

| Skill | Invoke | Description |
|-------|--------|-------------|
| AI Evals | `/ai-evals` | AI evaluation strategies |
| AI Product Strategy | `/ai-product-strategy` | AI product strategy |
| Analytical Thinking Interviews | `/analytical-thinking-interviews` | Analytical thinking interview prep |
| Analyzing User Feedback | `/analyzing-user-feedback` | Analyzing user feedback |
| Behavioral Product Design | `/behavioral-product-design` | Behavioral product design |
| Brand Storytelling | `/brand-storytelling` | Brand storytelling |
| Building a Promotion Case | `/building-a-promotion-case` | Building a promotion case |
| Building Sales Team | `/building-sales-team` | Building a sales team |
| Building Team Culture | `/building-team-culture` | Building team culture |
| Building with LLMs | `/building-with-llms` | Building with LLMs |
| Career Transitions | `/career-transitions` | Career transitions |
| Coaching PMs | `/coaching-pms` | Coaching PMs |
| Community Building | `/community-building` | Community building |
| Competitive Analysis | `/competitive-analysis` | Competitive analysis |
| Conducting Interviews | `/conducting-interviews` | Conducting interviews |
| Conducting User Interviews | `/conducting-user-interviews` | Conducting user interviews |
| Content Marketing | `/content-marketing` | Content marketing |
| Cross-Functional Collaboration | `/cross-functional-collaboration` | Cross-functional collaboration |
| Defining Product Vision | `/defining-product-vision` | Defining product vision |
| Delegating Work | `/delegating-work` | Delegating work |
| Design Engineering | `/design-engineering` | Design engineering |
| Design Systems | `/design-systems` | Design systems |
| Designing Growth Loops | `/designing-growth-loops` | Designing growth loops |
| Designing Surveys | `/designing-surveys` | Designing surveys |
| Dogfooding | `/dogfooding` | Dogfooding |
| Energy Management | `/energy-management` | Energy management |
| Engineering Culture | `/engineering-culture` | Engineering culture |
| Enterprise Sales | `/enterprise-sales` | Enterprise sales |
| Evaluating Candidates | `/evaluating-candidates` | Evaluating candidates |
| Evaluating New Technology | `/evaluating-new-technology` | Evaluating new technology |
| Evaluating Trade-offs | `/evaluating-trade-offs` | Evaluating trade-offs |
| Finding Mentors & Sponsors | `/finding-mentors-sponsors` | Finding mentors and sponsors |
| Founder Sales | `/founder-sales` | Founder sales |
| Fundraising | `/fundraising` | Fundraising |
| Giving Presentations | `/giving-presentations` | Giving presentations |
| Having Difficult Conversations | `/having-difficult-conversations` | Having difficult conversations |
| Launch Marketing | `/launch-marketing` | Launch marketing |
| Managing Imposter Syndrome | `/managing-imposter-syndrome` | Managing imposter syndrome |
| Managing Tech Debt | `/managing-tech-debt` | Managing tech debt |
| Managing Timelines | `/managing-timelines` | Managing timelines |
| Managing Up | `/managing-up` | Managing up |
| Marketplace Liquidity | `/marketplace-liquidity` | Marketplace liquidity |
| Measuring Product-Market Fit | `/measuring-product-market-fit` | Measuring product-market fit |
| Media Relations | `/media-relations` | Media relations |
| Negotiating Offers | `/negotiating-offers` | Negotiating offers |
| Onboarding New Hires | `/onboarding-new-hires` | Onboarding new hires |
| Organizational Design | `/organizational-design` | Organizational design |
| Organizational Transformation | `/organizational-transformation` | Organizational transformation |
| Partnership & BD | `/partnership-bd` | Partnership and business development |
| Personal Productivity | `/personal-productivity` | Personal productivity |
| Planning Under Uncertainty | `/planning-under-uncertainty` | Planning under uncertainty |
| Platform Infrastructure | `/platform-infrastructure` | Platform infrastructure |
| Platform Strategy | `/platform-strategy` | Platform strategy |
| Positioning & Messaging | `/positioning-messaging` | Positioning and messaging |
| Post-Mortems & Retrospectives | `/post-mortems-retrospectives` | Post-mortems and retrospectives |
| Pricing Strategy | `/pricing-strategy` | Pricing strategy |
| Prioritizing Roadmap | `/prioritizing-roadmap` | Prioritizing roadmap |
| Problem Definition | `/problem-definition` | Problem definition |
| Product-Led Sales | `/product-led-sales` | Product-led sales |
| Product Operations | `/product-operations` | Product operations |
| Product Sense Interviews | `/product-sense-interviews` | Product sense interview prep |
| Product Taste & Intuition | `/product-taste-intuition` | Product taste and intuition |
| Retention & Engagement | `/retention-engagement` | Retention and engagement |
| Running Decision Processes | `/running-decision-processes` | Running decision processes |
| Running Design Reviews | `/running-design-reviews` | Running design reviews |
| Running Effective 1:1s | `/running-effective-1-1s` | Running effective 1:1s |
| Running Effective Meetings | `/running-effective-meetings` | Running effective meetings |
| Running Offsites | `/running-offsites` | Running offsites |
| Sales Compensation | `/sales-compensation` | Sales compensation |
| Sales Qualification | `/sales-qualification` | Sales qualification |
| Scoping & Cutting | `/scoping-cutting` | Scoping and cutting |
| Setting OKRs & Goals | `/setting-okrs-goals` | Setting OKRs and goals |
| Shipping Products | `/shipping-products` | Shipping products |
| Stakeholder Alignment | `/stakeholder-alignment` | Stakeholder alignment |
| Startup Ideation | `/startup-ideation` | Startup ideation |
| Startup Pivoting | `/startup-pivoting` | Startup pivoting |
| Systems Thinking | `/systems-thinking` | Systems thinking |
| Team Rituals | `/team-rituals` | Team rituals |
| Technical Roadmaps | `/technical-roadmaps` | Technical roadmaps |
| Usability Testing | `/usability-testing` | Usability testing |
| User Onboarding | `/user-onboarding` | User onboarding |
| Vibe Coding | `/vibe-coding` | Vibe coding |
| Working Backwards | `/working-backwards` | Working backwards |
| Writing Job Descriptions | `/writing-job-descriptions` | Writing job descriptions |
| Writing North Star Metrics | `/writing-north-star-metrics` | Writing north star metrics |
| Writing PRDs | `/writing-prds` | Writing PRDs |
| Writing Specs & Designs | `/writing-specs-designs` | Writing specs and designs |
| Written Communication | `/written-communication` | Written communication |
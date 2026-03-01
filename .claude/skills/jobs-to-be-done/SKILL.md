---
name: jobs-to-be-done
description: Help users create personas and end-to-end use case scenarios using the Jobs to Be Done (JTBD) framework. Use when someone needs to understand who their users are, document what those users are trying to accomplish, map out end-to-end workflows, or build a shared understanding of primary use cases for a product or platform.
---

# JTBD Personas & Use Cases

Help the user create a comprehensive personas and use cases document using the Jobs to Be Done framework. The output is a single markdown file that gives any reader a clear understanding of who uses the product, what they're trying to accomplish, and how the product helps them do it.

## How to Help

When the user asks for personas and use cases:

1. **Understand the product** -- Read available documentation, code, design docs, or ask the user to describe the system
2. **Identify the personas** -- Who are the distinct user types? What are their roles, tools, needs, and pain points?
3. **Map the use cases** -- What are the major things the product does? Group them into product areas
4. **Write JTBD statements** -- For each use case, write a "When / I want to / So that" statement grounded in motivation
5. **Connect personas to jobs** -- Show which personas are involved in each job and how
6. **Add context** -- Scale metrics, competitive landscape, and source references

## The JTBD Framework

### Core Principle

People don't buy products -- they hire them to do a job. The "job" is the progress a person is trying to make in a particular circumstance. Focus on the job, not the feature.

### The JTBD Statement Format

```
When [situation/trigger],
I want to [action/capability],
So that [desired outcome/progress].
```

**Rules for good JTBD statements:**
- **Situation-first** -- Start with the circumstance that creates the need, not the feature
- **Solution-agnostic action** -- Describe what the user wants to accomplish, not how the product implements it
- **Outcome over output** -- The "so that" should be a business or personal outcome, not a product behavior
- **One job per statement** -- Don't combine multiple jobs. If you need "and" in the action, it's probably two jobs

**Good example:**
> When I am deploying new code to production, I want to gate the new functionality so only specific users see it, so that I can deploy safely without risking all users if something goes wrong.

**Bad example:**
> When I click the feature flag button, I want to create a boolean flag with targeting rules, so that the flag is created in the system.

The bad example describes product mechanics, not the job. The user doesn't care about "boolean flags" -- they care about deploying safely.

### Functional vs. Emotional vs. Social Jobs

Every job has three dimensions. Most product teams only think about functional jobs. The best teams address all three:

| Dimension | Question | Example |
|-----------|----------|---------|
| **Functional** | What task are they trying to get done? | "Roll out a feature to 10% of users" |
| **Emotional** | How do they want to feel? | "Confident that this won't break production" |
| **Social** | How do they want to be perceived? | "Seen as someone who ships reliably" |

When writing JTBD statements, the primary statement covers the functional job. Add a note about emotional and social dimensions when they are strong motivators.

## Persona Format

For each persona, create a structured profile:

```markdown
### [Role Title]

| Attribute | Detail |
|-----------|--------|
| **Role** | What they do in relation to the product |
| **Tools** | What tools and interfaces they use |
| **Key needs** | Their top 3-5 requirements from the product |
| **Pain points** | Their top 3-5 frustrations or unmet needs |
| **Frequency** | How often they interact with the product and in what patterns |
```

### Rules for Good Personas

- **Role, not person** -- Describe the role and its responsibilities, not a fictional character with a name and photo. "Sarah, 34, loves hiking" adds nothing
- **Grounded in evidence** -- Every attribute should come from research, interviews, usage data, or documentation. Flag assumptions explicitly
- **Distinct from each other** -- If two personas have the same needs, tools, and pain points, they're the same persona. Merge them
- **Include the "why they care" dimension** -- Don't just list needs; explain what's at stake for them if those needs aren't met
- **Capture frequency and patterns** -- A user who touches the product daily has fundamentally different needs than one who uses it quarterly

### How to Discover Personas

Ask these questions:

**From documentation:**
- Who is mentioned as a user, stakeholder, or audience in design docs, PRDs, and strategy docs?
- Who appears in the RBAC/permissions model? Different permission levels often indicate different personas
- Who is mentioned in onboarding guides? Are there different guides for different roles?
- Who files bugs, requests features, or gives feedback in Slack or issue trackers?

**From the codebase:**
- What authentication roles exist? (admin, developer, viewer, integrations)
- Are there different UI views or dashboards for different user types?
- Does the API have different access patterns (SDK vs. UI vs. API key)?

**From the user directly:**
- "Who uses this product day-to-day?"
- "Who uses it occasionally but has high-stakes interactions?"
- "Who cares about this product's output even if they never log in?"
- "Who gets paged when this product breaks?"
- "Who decides whether to invest more in this product?"

## Use Case Format

Group use cases by product area, then write each one as:

```markdown
### [Product Area Name]

[1-2 sentence description of what this area does and why it matters]

**Key capabilities:**
- Capability 1
- Capability 2
- Capability 3
```

## JTBD Scenario Format

For each major job, create a full scenario:

```markdown
### JTBD [N]: [Job Title]

> **When** [situation],
> **I want to** [action],
> **So that** [outcome].

| Who | How [Product] Helps |
|-----|---------------------|
| Persona 1 | What they specifically do in this job |
| Persona 2 | What they specifically do in this job |
| Persona 3 | What they specifically do in this job |

**Metrics:** [How you'd measure whether this job is being done well]
```

### Rules for Good JTBD Scenarios

- **Every job must map to at least two personas** -- If only one persona cares about a job, it might be too narrow. If only one persona is involved, the "Who" table still shows how they interact
- **Metrics are required** -- If you can't measure whether the job is being done well, the job statement is too vague
- **Include the "done poorly" version** -- What happens today without the product, or what happens when the product fails at this job? This grounds the scenario in real stakes
- **Order jobs by impact** -- Put the highest-impact, most-used jobs first. The reader should understand the product's core value in the first three JTBD scenarios

## Document Structure

The complete output should follow this structure:

```markdown
# [Product]: Personas, Use Cases & JTBD

> [1-2 sentence product description including origin story if relevant]

---

## 1. Personas

### 1.1 [Persona Name]
[Persona table]

### 1.2 [Persona Name]
[Persona table]

...

---

## 2. Primary Use Cases

### 2.1 [Product Area]
[Description + key capabilities]

### 2.2 [Product Area]
[Description + key capabilities]

...

---

## 3. Jobs to Be Done (JTBD)

### JTBD 1: [Job Title]
[JTBD statement + persona table + metrics]

### JTBD 2: [Job Title]
[JTBD statement + persona table + metrics]

...

---

## 4. Context
[Scale metrics, competitive landscape, platform stats]

---

## 5. Sources
[Where the information came from]
```

## Questions to Ask Users

### To understand the product
- "What does this product do in one sentence?"
- "Why was it built? What problem did it replace or solve?"
- "How long has it been around, and how has it grown?"
- "What are the major feature areas or capabilities?"

### To identify personas
- "Who are the primary users? Walk me through the different roles."
- "Do different people use different parts of the product?"
- "Who is the most frequent user? Who is the most important user? Are they the same person?"
- "Who benefits from this product without ever logging in?"
- "What are the top pain points you hear from each user type?"

### To map jobs
- "What's the single most important thing this product helps people do?"
- "Walk me through what happens when [primary user] needs to [primary action]."
- "What would happen if this product didn't exist? How would people do this work?"
- "What are the top 3 things users ask for that the product doesn't do yet?"
- "Are there use cases where people use the product in ways you didn't intend?"

### To find sources
- "Are there design docs, PRDs, strategy docs, or onboarding guides I can read?"
- "Is there a codebase I can explore for architecture and permissions?"
- "Are there user interview transcripts, survey results, or feedback channels?"
- "Is there an existing persona doc or competitive analysis?"

## Common Mistakes to Flag

- **Feature lists disguised as use cases** -- "Create a flag, edit a flag, delete a flag" are CRUD operations, not jobs to be done. The job is "ship features safely"
- **Personas with no pain points** -- If a persona has no frustrations, they're either not a real persona or you haven't done enough research
- **JTBD statements that describe product mechanics** -- "When I click the submit button" is not a situation. "When I have a feature ready for testing" is
- **Missing the emotional/social dimension** -- Engineers want to "deploy safely" (functional), but they also want to "feel confident" (emotional) and "be seen as reliable" (social). The best products address all three
- **Too many personas** -- If you have more than 8 personas, some probably overlap. Merge aggressively. The test: if you removed a persona, would any JTBD scenario lose a row in its table?
- **Jobs without metrics** -- If you can't measure it, it's too vague. Push for specific, observable indicators of whether the job is done well
- **Confusing current product capabilities with jobs** -- The product's current feature set is one way to do the job. The job exists independent of the product. Write the job first, then show how the product addresses it
- **Skipping "What happens without this product?"** -- The strongest JTBD documents include the status quo or competitor comparison so readers understand what's at stake

## Related Skills

- Problem Definition
- Conducting User Interviews
- Analyzing User Feedback
- Product Sense Interviews
- Writing PRDs
- Defining Product Vision

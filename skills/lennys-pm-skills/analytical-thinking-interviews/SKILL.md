---
name: analytical-thinking-interviews
description: Practice Analytical Thinking PM interviews. Use when someone wants to practice an AT interview, get coached on their AT interview template, or learn the AT interview framework. Can act as the candidate (user plays interviewer) or as a coach (user submits their template for scoring).
---

# Analytical Thinking Interview Practice

Help the user practice Analytical Thinking PM interviews using Ben Erez's framework. This skill supports two modes: **AI as candidate** (user plays interviewer) and **AI as coach** (user submits a filled-out template for scoring).

## How to Help

When the user invokes this skill:

1. **Determine the mode** - Ask if they want you to be the candidate (they play interviewer) or if they want coaching on their own submission
2. **For candidate mode** - Ask for an AT interview question, then work through the full framework with interviewer check-ins
3. **For coaching mode** - Ask them to share their filled-out template, then score it section by section
4. **Default company** - Unless specified otherwise, assume the interview is at the company whose product is mentioned in the question

## Candidate Mode: Interview Framework

Each chat is an Analytical Thinking interview. Work through the question following the structured framework below. Stop and check in with the interviewer after each milestone. Each check-in should ask if things make sense and state where you'd like to go next. **Wait for the user to respond before continuing.**

Assume you speak 120 words per minute. Append the speaking time at the end of each message (e.g., "3.5 minutes").

### Milestones (check in after each)

1. Stating up-front assumptions
2. Walking through your game plan
3. Product rationale and mission
4. Ecosystem metrics
5. North star metric and guardrails
6. Team goals
7. Tradeoff question

### Section 1: Product Rationale (<5 min)

- Describe the product: functionality, use cases, and maturity stage
- Identify the revenue/business model
- Explain the biggest problems this product solves and why they matter (what was wrong with the status quo)
- Review competitors and the company's unique positioning
- Connect to the parent company's mission
- Create a succinct mission statement (single sentence, under 15 words, captures core purpose)
- Make the interviewer "feel something" about why the world needs this product
- Establish a clear through-line from company mission to product mission

### Section 2: Measuring Impact (~15 min)

#### Ecosystem Players and Health Metrics

1. List the **THREE** most important ecosystem players
2. State the primary value proposition for each (why they participate)
3. List the **key actions** each player MUST take to realize their value (if they can get value without the action, don't list it)
4. Define primary metrics for each player to track those must-take actions

**Metric Guidelines:**
- Primary health metrics track fluctuations in key actions over time
- Use counts: how many people take key actions per day/week/month (DWM), how many times actions are taken overall per DWM
- If you use "Active" in any metric, **always define what active means** (e.g., "an active user is someone who completed at least one search within the week")
- State you'll track metrics for daily, weekly, and monthly ("DWM")
- Revenue is good to mention but likely not a top-line ecosystem health metric
- Stick primarily with raw counts for ecosystem health metrics, not percentages or ratios
- Be specific enough that a data scientist could run a query
- Frame metrics so they could be visualized as a chart on a dashboard

#### North Star Metric (NSM)

- Choose a metric that captures value creation for **multiple** ecosystem players
- Ensure it can grow continuously as the product succeeds (avoid natural ceilings)
- Select raw counts rather than percentages when possible
- Use "per time period" metrics rather than cumulative totals
- Avoid averages or medians — they can be misleading when ecosystem size changes
- Be cautious with percentages — ratio can increase while ecosystem declines

**Timeframe Selection — Consider:**
- Natural usage cadence of the product
- Signal-to-noise ratio (daily may be too volatile for slow-changing products)
- Business cycle relevance
- Ability to take action on the data
- Consistency across related metrics

**Critique your NSM** by listing the top TWO strengths and top TWO drawbacks. Drawbacks inform guardrails.

#### Ratio and Average Metrics

For any ratio or average metrics, always define precisely with a clear numerator and denominator. For example, instead of "Average sessions per user per week," specify "Total number of app sessions per week ÷ Number of weekly active users (where an active user is defined as someone who opened the app at least once during the week)."

#### Guardrail Metrics

- Define **one guardrail metric for each NSM drawback** you listed
- Unlike NSM, percentages often work better than raw counts for guardrails
- Raw counts of negative events may increase with scale even when ecosystem is healthy
- Example: use "% of transactions resulting in disputes" rather than "total disputes"
- Guardrails should directly address main drawbacks of NSM
- Good test: "I want NSM to go up as long as guardrails stay within healthy range"

### Section 3: Setting Goals (~5 min)

Make a clear **"altitude shift"** from product-level metrics to team-level goals.

1. **Select one ecosystem player** to focus on (with clear rationale — who unlocks the biggest growth based on current state/maturity)
2. **Map the complete user journey** leading to your NSM event for that ecosystem player
3. **Brainstorm exactly 3 goals** — frame as directional improvements (e.g., "increase session starts per user" not "increase by 15%")
4. **Do not set averages as goals** — aim for conversion rate improvements between key steps of the user journey
5. **Score each goal** on:
   - Ability to influence: Low/Medium/High (consider organizational boundaries and sphere of influence)
   - Impact on NSM: Low/Medium/High
6. **Select ONE goal** as top priority — choose the one with highest weighted score
7. Explain specifically how this goal moves the NSM
8. Keep timeframe realistic (3-6 months for a product team)

**Organizational Considerations:**
- Goals requiring changes to areas owned by other PMs have lower "ability to influence"
- Be realistic about sphere of influence
- Consider political capital required for cross-team goals

### Section 4: Evaluating Tradeoffs (~10 min)

After being asked a tradeoff question:

1. **Identify the tradeoff type**:
   - Breadth vs. Depth (e.g., "100 reels with 1M views or 1M reels with 100 views?")
   - Real Estate Prioritization (e.g., "Should we put Reels at the top instead of Stories?")
   - Required vs. Optional Features (e.g., "Should profile photo be required during signup?")
   - Ship or Don't Ship (e.g., "Test reduces comments but increases reactions — ship to all?")
   - Kill or Keep a Feature (e.g., "Remove low-usage but high-satisfaction feature?")

2. **Clarify the common goal** shared by both options
3. **Frame TWO pros and TWO cons** for each option
4. **Summarize the fundamental tradeoff**
5. **Make a decisive recommendation** with clear rationale tied to product mission and metrics
6. **Specify what would need to be true to change your stance**

**Important:**
- Do NOT just say "I would run a test" — make a decision
- Connect decision back to product mission and company strategy
- Consider product lifecycle stage
- If a tradeoff triggers a guardrail metric, be very cautious
- Do not hedge or defer to others
- Use product mission statement as anchor for recommendation

### After Completion

Offer to score your performance according to the rubric. When recapping, include a summary of minutes spent on each section (based on 120 words/minute).

## Coaching Mode: Scoring Submissions

When the user submits a filled-out AT interview template, score it section by section using these rubrics. Be constructively critical rather than overly generous.

### Product Rationale

- **5/5**: States product description, use cases, maturity level, and business model; explains why users and company care; reviews competitors and limitations; articulates company mission and creates product mission statement; makes interviewer "feel something"
- **4/5**: Covers most product context elements with clear mission statements; minor gaps in competitive analysis or business model
- **3/5**: Basic product description with some mission thinking and limited competitive context
- **2/5**: Superficial overview with weak or missing mission statements
- **1/5**: Confused product understanding; no mission statements; relies on insider knowledge

### Measuring Impact

- **5/5**: Identifies ecosystem players with clear value propositions; defines specific metrics with timeframes and mathematical precision; selects NSM that captures multi-player value and can grow infinitely; creates guardrails using percentages that directly address NSM weaknesses
- **4/5**: Good ecosystem analysis with mostly specific metrics; solid NSM with adequate guardrails; minor issues in definitions or timeframe justification
- **3/5**: Identifies key players with basic metrics; acceptable NSM selection; some vague definitions
- **2/5**: Unclear ecosystem players; uses vanity metrics or averages inappropriately; weak NSM or missing guardrails
- **1/5**: Confused ecosystem analysis; undefined metrics like "engagement"; inappropriate NSM choice; no guardrails

### Setting Goals

- **5/5**: Clear altitude shift from product-level to team-level; justifies ecosystem player focus; proposes 1-3 goals for 3-6 months; scores on impact and feasibility; selects one goal decisively with clear NSM connection
- **4/5**: Good team-level transition with reasonable player focus; solid prioritization with clear rationale
- **3/5**: Some altitude shift thinking with basic goal identification; limited prioritization rationale
- **2/5**: Unclear transition from product to team level; goals require too much cross-team collaboration
- **1/5**: No altitude shift; goals too high-level or disconnected from metrics; indecisive

### Evaluating Tradeoffs

- **5/5**: Identifies tradeoff type; clarifies common goal; frames pros/cons systematically; makes decisive recommendation tied to mission; specifies what would change their mind
- **4/5**: Good tradeoff structure with clear decision framework; solid recommendation
- **3/5**: Basic tradeoff evaluation with some structured thinking; makes recommendation with limited rationale
- **2/5**: Unclear tradeoff framing; weak rationale; hedges or avoids clear recommendation
- **1/5**: No clear framework; indecisive or contradictory; doesn't connect back to mission

### Evaluation Principles

- A score of 3 is passing. Must pass ALL dimensions.
- Focus on quality of thinking and systematic approach, not perfection
- Strong AT thinking can take multiple valid forms
- Be constructively critical rather than overly generous

## Key Interview Strategy Tips

- **Own the interview** — treat it as a meeting you are driving
- **Strategic pauses**: 1-2 minutes at transition points. Consider muting yourself during thinking periods
- **Don't share your screen** — prevents distractions
- **Nudges from interviewers are help** — pause, reconsider, clarify or pivot
- **Backtracking is OK** — correct your path thoughtfully
- **Be ruthless with time management**
- **Check in with interviewer before moving to new sections**
- **Avoid vague terms** like "engagement" or vanity metrics like "installs"
- **Be decisive** — waffling is viewed negatively
- **No right answer** — be reasonable, make assumptions, walk through thinking
- **Don't contradict yourself**

## Why Averages Can Be Misleading

Averages can mask important distribution patterns. Better alternatives:

- **Percentages and thresholds**: "% of users who do X at least N times per period"
- **Distributions**: Segment into meaningful cohorts, track by percentile (p50, p90)
- **Combination metrics**: Pair volume metrics with quality signals

Instead of "average posts per creator," use "% of creators posting weekly" or "creator retention rate by posting frequency cohort."

## Deep Dive

For the complete question bank, company mission statements, product archetypes, and example interviews, see `references/interview-guide.md`

## Related Skills

- Product Sense Interviews
- Conducting Interviews
- Evaluating Candidates

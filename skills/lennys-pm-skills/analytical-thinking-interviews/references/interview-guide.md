# Analytical Thinking Interview Practice — Reference Guide

Based on Ben Erez's frameworks, Lenny's Newsletter guest posts, and Meta/Google PM interview best practices.

---

## Question Bank

Practice questions for Analytical Thinking interviews:

1. How would you define success for Instagram Reels?
2. You are the PM for Meta Verified. What are your goals and success metrics?
3. You are a PM at Meta building an AI chatbot in Instagram DMs. Why should Meta build this, and how would you measure success?
4. You are a PM for Meta Pay. What are your goals, success metrics, and how would you measure success over time?
5. You are a PM for Facebook Events. How would you set goals and measure success for this product?
6. You are a PM at Netflix for the Podcast feature. How would you define goals and success metrics?
7. You are a PM for Work Chat (part of Workplace). Why should Meta continue investing in it, and how would you measure success?
8. You are a PM for Facebook Local Ads. Why should Meta build this, and what goals and success metrics would you set?
9. You are the PM for Facebook Notifications. How would you define success and measure it, and what tradeoffs would you consider?
10. You are the PM for Facebook Live before launch. Should Meta build it, and if so, what goals and metrics would define success?
11. You are the PM for Zoom (or a Meta competitor). Why does this product exist, and what goals and metrics would you define?
12. You are the PM for the Facebook Feed. If we run an experiment showing 1% of users more ads, how would you measure success?
13. You are a PM for anti-scamming products at Meta. Why should Meta build it, and how would you set goals and measure success?
14. You are a PM for Instagram Reels Ads. How would you measure success and evaluate tradeoffs between time spent and monetization?
15. You are the PM for the Instagram AI chatbot, and your North Star Metric is declining. How would you diagnose the problem and respond?

For additional questions, use Lewis Lin's PM Question Bank.

---

## Company Mission Statements

| Company | Mission | Strategic Advantages |
|---------|---------|---------------------|
| **Meta** | Build the future of human connection and the technology that makes it possible | Large-scale social/messaging ecosystem; AR/VR investments; data & advertising platform; rapid innovation culture |
| **Netflix** | To entertain the world | Global streaming reach; original content; data-driven personalization; fully digital delivery |
| **Google** | To organize the world's information and make it universally accessible and useful | Dominant search; ML/AI capabilities; product ecosystem (Maps, Gmail, YouTube, Android); brand trust and global scale |

---

## Interview Structure and Time Management

- **Meta interviews**: 45 minutes total (5 min intro, 35 min core, 5 min Q&A)
- **Full loop**: Product Sense + Analytical Thinking + Leadership & Drive (45 min each)
- Speaking time should be 80-90% of total

### Time Allocation

| Section | Time |
|---------|------|
| Assumptions + Game Plan | 1-2 min |
| Product Rationale & Mission | <5 min |
| Ecosystem Players & Health Metrics | <8 min |
| North Star Metric + Guardrails | <4 min |
| Team Goals | <5 min |
| Tradeoff Question | <10 min |

---

## What Meta Looks For (Four Focus Areas)

1. **Articulating a product's rationale** — Clear understanding of why the product exists and matters
2. **Setting reasonable, measurable and prioritized goals** — Ability to define actionable team goals
3. **Measuring impact and identifying metrics** — Systematic approach to ecosystem health and NSM
4. **Evaluating trade-offs** — Making principled decisions under uncertainty

Meta is deeply data-driven with 3B+ users. Focus on how you identify and prioritize opportunities, analyze constraints, define metrics, and adapt plans with new information.

---

## Ecosystem Analysis Framework

### Step-by-Step Process

1. **Identify the 3 most important ecosystem players**
2. **Define each player's value proposition** — Why do they participate?
3. **Map must-take actions** — What does each player HAVE to do to get value? (If they can get value without that action, don't list it)
4. **Create health metrics** for each player tracking those actions

### Metric Construction Guidelines

For each key action representing value creation:
- Count unique users who perform the action (within a timeframe)
- Count total times the action occurs (within same timeframe)
- Consider adding a depth/quality metric if relevant

### Timeframe Selection

- **Daily**: High-frequency actions or when immediate signals are needed
- **Weekly**: Moderate-frequency actions (often a good default)
- **Monthly**: Less frequent but significant actions
- State you'll track "DWM" (daily, weekly, monthly) for primary metrics
- Stick primarily with raw counts, not percentages or ratios

---

## North Star Metric Best Practices

### Good NSM Characteristics

- Captures value creation for multiple ecosystem players
- Can grow continuously / indefinitely as the product succeeds
- Raw counts rather than percentages (no natural ceiling)
- "Per time period" rather than cumulative totals
- Specific enough for a data scientist to write a query
- Only goes up if the product is truly succeeding

### NSM Anti-Patterns

- **Averages/medians**: Can be misleading when ecosystem size changes
- **Percentages**: Have natural ceiling at 100%, can increase while ecosystem declines
- **Vague metrics**: "Engagement" without definition is meaningless
- **Vanity metrics**: Cumulative totals, installs, or metrics that only go up
- **Generic DAU**: Must define what "active" means specifically

### Critiquing Your NSM

Always list:
- **Top 2 strengths** — why this is a good NSM
- **Top 2 drawbacks** — what this NSM could miss or incentivize wrongly
- Use drawbacks to directly inform guardrail selection

---

## Guardrail Metrics Best Practices

- Define **one guardrail per NSM drawback** you identified
- Percentages often work better than raw counts for guardrails
- Raw counts of negative events increase with scale even when ecosystem is healthy
- Example: "% of transactions resulting in disputes" > "total disputes"
- Focus on 2-3 guardrails representing most critical health checks
- **Good test**: "I want NSM to go up as long as guardrails stay within healthy range"

---

## Goal Setting Framework

### The "Altitude Shift"

Move from 50,000-foot product-level metrics to specific team-level goals:

1. **Choose one ecosystem player** — who unlocks biggest growth given current maturity
2. **Work backward from NSM** — map the user journey that leads to the NSM event
3. **Identify leading metrics** — conversion rates between journey steps
4. **Brainstorm exactly 3 goals** framed as directional improvements
5. **Do NOT use averages as goals** — use conversion rates between key steps
6. **Do NOT set specific percentage targets** — use directional improvement framing
7. **Score goals on two dimensions**:
   - Ability to Influence: Low/Medium/High
   - Impact on NSM: Low/Medium/High
8. **Select ONE top priority** — highest weighted score wins

### "Ability to Influence" Considerations

- Internal friction (influencing areas owned by other PMs = Low-Med influence)
- Organizational boundaries matter
- Goals requiring too many other teams' involvement score lower
- Be realistic about sphere of influence
- Consider political capital required

---

## Tradeoff Decision Framework

### Five Types of Tradeoff Questions

1. **Breadth vs. Depth** — "100 reels with 1M views or 1M reels with 100 views?"
2. **Real Estate Prioritization** — "Should we put Reels at the top instead of Stories?"
3. **Required vs. Optional Features** — "Should profile photo be required during signup?"
4. **Ship or Don't Ship** — "Test reduces comments but increases reactions — ship to all?"
5. **Kill or Keep a Feature** — "Remove low-usage but high-satisfaction feature?"

### Decision-Making Process

1. Both options align with product and company mission
2. Both would contribute to NSM if successful
3. Chosen option aligns with prioritized goals
4. Chosen option does not trigger any guardrail metrics

### Execution Checklist

- Identify the tradeoff type
- Clarify the common goal shared by both options
- Frame exactly **TWO pros and TWO cons** for each option
- Summarize the fundamental tradeoff in one sentence
- Make a decisive recommendation with clear rationale
- Specify what would need to be true to change your stance
- Connect back to product mission and NSM

---

## Why Averages Can Be Misleading

### Common Scenarios Where Averages Mislead

- User engagement metrics (e.g., posts per user)
- Content creation frequency
- Transaction volumes
- Time-based metrics (e.g., time spent in app)
- Revenue or monetization metrics

### Better Alternatives

**Percentages and Thresholds:**
- "% of users who do X at least N times per period"
- "% of users above threshold Y"
- Retention rates by cohort

**Distributions:**
- Segment users into meaningful cohorts
- Track by percentile (p50, p90)
- Look at distribution shapes and changes

**Combination Metrics:**
- Pair volume metrics with quality signals
- Track both breadth and depth of engagement
- Monitor leading and lagging indicators together

### Best Practices

1. Always question if average is the right metric
2. Consider what behaviors you want to drive
3. Test if metric moves as expected in edge cases
4. Ensure metric aligns with user/business value
5. Monitor for unintended consequences
6. Segment data before drawing conclusions

---

## Product Archetypes for Preparation

Instead of memorizing metrics for every product, learn frameworks for these archetypes:

- **Messaging products** (WhatsApp, Messenger, Instagram DM)
- **Feed/Stream products** (Facebook, Instagram, TikTok, YouTube)
- **Marketplace products** (Uber, Airbnb, Facebook Marketplace)
- **Streaming products** (Netflix, YouTube, Facebook Live)
- **Notification systems**

---

## Example Interview: Instagram Reels

**Product Rationale:**
- Meta's short-form vertical video product, up to 90 seconds
- Discovered through feed, explore page, or dedicated reels tab
- Revenue via ads inserted between reels and shopping features
- Growth stage — significant adoption but still expanding creator base
- Competing with TikTok, YouTube Shorts
- Meta uniquely positioned: massive user base, creator relationships, recommendation systems, advertising infrastructure
- Mission: "Empower creators to share engaging short-form videos that entertain and connect the Instagram community"

**Ecosystem Players:**
- Viewers/consumers: entertainment discovery, accessing personalized content
- Creators: producing and sharing content
- Advertisers: reaching audiences through ad inventory
- Meta: platform revenue and engagement

**North Star Metric:** Total reels watch time per week
- Strengths: indicates engaging content, signals creator quality, gives ad inventory, drives revenue
- Drawbacks: could increase even if quality degrades; could incentivize longer videos

**Guardrails:**
- Average completion rate per reel should not drop below baseline
- Creator retention rate (% of creators posting in consecutive months)

**Goals:**
- Focus on creators (content supply drives watch time)
- Journey: create/edit → post → reach viewers → generate engagement → understand performance → monetize
- Goal options: increase reel creation completion rate, increase creator posting frequency, improve new creator retention
- Prioritized: Creator posting frequency (highest ability to influence + high NSM impact)

**Tradeoff: Reels vs Stories at top of Instagram**
- Common goal: connecting people through visual sharing
- Reels pros: accelerates TikTok competition, higher engagement, more monetization
- Reels cons: reduces authentic sharing, shifts identity away from social, risks Stories engagement
- Stories pros: maintains core social value prop, preserves familiar UX, protects engagement
- Stories cons: slower Reels growth, less TikTok competition, lower entertainment engagement
- Fundamental tradeoff: social connections vs. entertainment/discovery
- Recommendation: Keep Stories (core differentiator of authentic sharing)
- What would change mind: Stories engagement plateaus while Reels grows rapidly

---

## Google vs. Meta Differences

- Core framework applies across companies
- Google interviews may:
  - Place less emphasis on tradeoff questions
  - Focus more on ecosystem than specific product
  - Place greater emphasis on business activity/monetary impact
  - Include estimation questions more frequently
- Google types: Product Insight, Strategic Insights, Craft and Execution, Analytical Thinking

---

## Common Pitfalls to Avoid

- Using vague metric definitions (if a data scientist can't query it, it's not a good metric)
- Too many metrics (focus on 3-5 per ecosystem player)
- Using percentages/ratios as NSM (NSM should grow infinitely)
- Skipping guardrails
- Not defining what "active" means
- Choosing vanity metrics over actionable ones
- Using averages as North Star or goals
- Missing ecosystem-wide implications
- Not tying decisions back to product mission
- Failing to identify what would change your recommendation
- Waffling or being indecisive on tradeoffs
- Setting goals requiring too much cross-team collaboration
- Using cumulative metrics instead of per-time-period
- Forgetting to consider global patterns and time zones

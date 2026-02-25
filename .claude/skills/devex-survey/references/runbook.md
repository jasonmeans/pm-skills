# DevEx Survey Runbook

End-to-end operational process for planning, launching, analyzing, and communicating the Developer Experience (DevEx) Survey.

The goal is to generate statistically credible workflow insights that inform quarterly prioritization and build developer trust.

---

## 1. Objectives

The DevEx Survey exists to:

- Measure workflow sentiment over time
- Identify high-friction areas
- Detect leverage opportunities
- Inform planning
- Close the feedback loop visibly

The survey is **not** a performance tool.

---

## 2. Cadence

**Default: Quarterly**

Cadence must:

- Align with planning cycles
- Avoid performance review deadlines
- Avoid holidays and major company disruptions
- Allow 2 weeks open + 1 week analysis

### Example Timeline

| Week | Activity |
|------|----------|
| Week 0 | Survey prep |
| Week 1-2 | Survey open |
| Week 3 | Analysis |
| Week 4 | Shareout + planning alignment |

---

## 3. Roles & Responsibilities

### Survey Owner (PM / DevEx Lead)
- Own survey creation
- Coordinate distribution
- Lead analysis synthesis
- Drive company shareout

### Engineering Managers
- Signal boost participation
- Review team-level results
- Support follow-up conversations

### Tech Leads
- Analyze workflow-specific friction
- Identify leverage opportunities

### Executive Sponsor
- Signal boost importance
- Reinforce prioritization alignment

---

## 4. Distribution Plan

### Initial Send

- Personalized email from a real human (not a distribution list)
- Mail merge or scripted personalization
- Short URL to survey
- Include: 3-5 minute time estimate, clear close date
- Expected early response: ~15% within 48 hours

### Midway Reminder (Day 7)

Send reminder email to non-respondents.

### Signal Boosting (Critical)

Leadership reinforces participation through three channels:

#### A. Reply to Reminder Email

VP Eng / CTO replies-all with:
- Why survey matters
- How data informs planning
- Clear encouragement to complete

#### B. All-Hands Mention

60-90 second reminder covering:
- Survey closes on [date]
- Takes 5 minutes
- Drives prioritization decisions

#### C. Team-Level Mentions

EMs mention in staff meetings and standups.

### Targeted Follow-Up (After Day 10)

- Identify low-response teams
- Ask EMs to encourage completion directly

### Slack Follow-Up (Optional)

- Personal DM from EM or PM
- Never automated, never bot-driven
- Quality over quantity

---

## 5. Statistical Integrity

### Always Report

| Metric | Required |
|--------|----------|
| Total invited | Yes |
| Total responded | Yes |
| Response rate | Yes |
| Confidence interval | Yes |
| Satisfaction % | Yes |
| Dissatisfaction % | Yes |

**Target CI: 1-3%**

Never publish sentiment without confidence interval.

---

## 6. Analysis Process

**Timeline:** Complete within 5 business days of survey close.

### Step 1: Human Read-Through

Read every comment. AI may assist categorization but a human must read each response.

### Step 2: AI Categorization

- Cluster themes from verbatim responses
- Count mention frequency
- Identify leverage areas (dissatisfied-to-neutral, neutral-to-satisfied)
- Detect quarter-over-quarter deltas

### Step 3: Metadata Segmentation

Join responses with organizational metadata:

- Programming language / tech stack
- Tenure at company
- Geographic location
- Discipline (frontend, backend, infra, mobile, etc.)
- Tool usage patterns
- Team / org distribution

Identify hotspots, outliers, and sharp deltas.

### Step 4: Champion Identification

Flag thoughtful respondents. Reach out to invite them into a DevEx Champion Network for ongoing feedback and co-design.

---

## 7. Deliverables

Within 1 week of survey close:

### Internal Report
- Trend charts (quarter-over-quarter)
- Confidence interval calculation
- Top 3 pain points with representative quotes
- Segmented insights by metadata dimensions
- Leverage recommendations with prioritization

### Company Shareout
- Slide deck (5-10 minute presentation)
- Written summary
- Must include:
  - What changed since last quarter
  - What we are investing in next
  - What we are NOT addressing (and why)

---

## 8. Communication Strategy

### Close the Feedback Loop

When improvements ship that were informed by survey data, communicate clearly:

> "This improvement came directly from survey feedback."

Repeat every cycle. This is the single most important thing for sustained participation.

### Best Practices

1. **Always share** how survey data drove priorities
2. **When addressing feedback**, explicitly connect it back to survey results
3. **Include survey insights** in company or team-wide engineering all-hands
4. **Publish a full write-up** of survey results — transparency builds trust

---

## 9. Success Criteria

- Confidence interval of 1-3%
- Strong and improving response rate quarter-over-quarter
- Clear trend visibility across quarters
- Identified leverage opportunities with owners
- Documented actions taken from survey data
- Increasing participation over time (trust signal)

---

## 10. Operating Loop

```
Plan → Survey → Analyze → Share → Act → Repeat
```

Consistency builds trust.
Trust sharpens signal.
Signal improves investment.
Investment reduces friction.
Reduced friction increases trust.

# Engineering PRD: [Feature Name]

| Field | Value |
|-------|-------|
| **Author** | [PM Name] |
| **Eng Lead** | [Name] |
| **Design Lead** | [Name] |
| **TPM** | [Name] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft / Eng Review / Approved / In Progress |
| **Design Spec** | [Link] |
| **Architecture Doc** | [Link, if applicable] |

---

## 1. Problem Statement

### User Impact

[What problem do users face? How does it affect their workflow? Quantify if possible -- support tickets, time wasted, workarounds used.]

### Business Impact

[Why does this matter to the business? Revenue at risk, competitive gap, retention impact, strategic alignment.]

---

## 2. Goals & Success Metrics

### Goals

1. [Measurable goal 1]
2. [Measurable goal 2]
3. [Measurable goal 3]

### Non-Goals

- [Explicitly out of scope]
- [Adjacent problem we are deferring]

### Success Metrics

| Metric | Baseline | Target | Measurement | Timeframe |
|--------|----------|--------|-------------|-----------|
| [Metric 1] | [Current value] | [Target] | [How/where measured] | [Post-launch window] |
| [Metric 2] | [Current value] | [Target] | [How/where measured] | [Post-launch window] |

---

## 3. Functional Requirements

### [Area 1: e.g., User Registration]

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1.1 | [When X happens, the system does Y] | Must Have |
| FR-1.2 | [When X happens, the system does Y] | Must Have |
| FR-1.3 | [When X happens, the system does Y] | Nice to Have |

### [Area 2: e.g., Notification Delivery]

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-2.1 | [When X happens, the system does Y] | Must Have |
| FR-2.2 | [When X happens, the system does Y] | Must Have |

### [Area 3: e.g., Admin Controls]

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-3.1 | [When X happens, the system does Y] | Must Have |

---

## 4. Technical Constraints

| Constraint | Details |
|-----------|---------|
| **Performance** | [e.g., P95 latency < 200ms for queries < 100 results] |
| **Scale** | [e.g., Must support 10K concurrent users, 1M events/day] |
| **Backwards Compatibility** | [e.g., Existing API v1 must continue working for 6 months] |
| **Security** | [e.g., All PII encrypted at rest, audit logging required] |
| **Data Retention** | [e.g., Event data retained for 90 days, then archived] |
| **Browser/Platform Support** | [e.g., Chrome, Firefox, Safari latest 2 versions] |
| **Dependencies** | [e.g., Requires Auth Service v2.3+, Kafka cluster available] |

---

## 5. Data Model

### New Tables

```sql
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  [column] [TYPE] [CONSTRAINTS],
  [column] [TYPE] [CONSTRAINTS],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_[table]_[column] ON [table_name]([column]);
```

### Schema Changes to Existing Tables

```sql
ALTER TABLE [existing_table]
  ADD COLUMN [column] [TYPE] [CONSTRAINTS];
```

### Migration Notes

- [Ordering requirements]
- [Backfill requirements]
- [Estimated migration duration for production data volume]

---

## 6. API Contracts

### [Endpoint 1: e.g., POST /api/v1/webhooks]

**Request:**

```json
{
  "url": "https://example.com/webhook",
  "events": ["order.created", "order.updated"],
  "secret": "optional-signing-secret"
}
```

**Response (201):**

```json
{
  "id": "wh_abc123",
  "url": "https://example.com/webhook",
  "events": ["order.created", "order.updated"],
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors:**

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Invalid URL format | `{ "error": "url must be a valid HTTPS URL" }` |
| 401 | Unauthorized | `{ "error": "Unauthorized" }` |
| 422 | Unknown event type | `{ "error": "Unknown event: order.deleted" }` |

### [Endpoint 2]

[Same format]

---

## 7. Edge Cases & Error Handling

| # | Scenario | Expected Behavior |
|---|----------|-------------------|
| 1 | [e.g., User submits empty form] | [e.g., Validation error with field-level messages] |
| 2 | [e.g., Downstream service timeout] | [e.g., Retry 3x with exponential backoff, then queue for later] |
| 3 | [e.g., User has no data] | [e.g., Show empty state with onboarding prompt] |
| 4 | [e.g., Concurrent updates to same record] | [e.g., Optimistic locking with 409 Conflict response] |
| 5 | [e.g., Rate limit exceeded] | [e.g., Return 429 with Retry-After header] |

---

## 8. User Stories & Acceptance Criteria

### Story 1: [Story title]

**As a** [user type], **I want to** [action], **so that** [outcome].

**Acceptance Criteria:**

- **Given** [precondition], **When** [action], **Then** [expected result]
- **Given** [precondition], **When** [action], **Then** [expected result]
- **Given** [error condition], **When** [action], **Then** [error handling behavior]

---

### Story 2: [Story title]

**As a** [user type], **I want to** [action], **so that** [outcome].

**Acceptance Criteria:**

- **Given** [precondition], **When** [action], **Then** [expected result]
- **Given** [precondition], **When** [action], **Then** [expected result]

---

### Story 3: [Story title]

[Same format]

---

## 9. Release Stages

| Stage | Scope | Entrance Criteria | Target Date |
|-------|-------|-------------------|-------------|
| **Alpha** | Internal team only | [e.g., Core CRUD complete, basic happy path works] | [Date] |
| **Closed Beta** | All employees + select partners | [e.g., No P0/P1 bugs, support runbooks reviewed] | [Date] |
| **Open Beta** | Early adopters | [e.g., No P0/P1/P2 bugs, holdout experiments complete] | [Date] |
| **GA** | All customers | [e.g., Feature complete, docs published, no critical issues] | [Date] |

### Stage Transition Checklist

**Alpha to Closed Beta:**
- [ ] All P0/P1 issues resolved
- [ ] Learnings documented
- [ ] Support runbooks drafted
- [ ] Analytics instrumentation verified

**Closed Beta to Open Beta:**
- [ ] Holdout experiments analyzed
- [ ] Support runbooks approved by leadership
- [ ] Release exceptions closed
- [ ] Documentation complete

**Open Beta to GA:**
- [ ] Metrics trending positive
- [ ] GA promotional plan confirmed
- [ ] Knowledge base articles published
- [ ] No open P0/P1/P2 issues

---

## 10. Cross-Functional Tracking

| Function | Deliverable | Owner | Status | Target Date |
|----------|-------------|-------|--------|-------------|
| Design | [e.g., Final mockups for settings page] | [Name] | [Status] | [Date] |
| Docs | [e.g., API reference updated] | [Name] | [Status] | [Date] |
| Support | [e.g., Runbook for webhook failures] | [Name] | [Status] | [Date] |
| Analytics | [e.g., Dashboard for delivery metrics] | [Name] | [Status] | [Date] |
| Marketing | [e.g., Beta announcement blog post] | [Name] | [Status] | [Date] |

---

## 11. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk 1] | High / Med / Low | High / Med / Low | [Mitigation plan] |
| [Risk 2] | High / Med / Low | High / Med / Low | [Mitigation plan] |

---

## 12. Open Questions

| # | Question | Owner | Target Date | Resolution |
|---|----------|-------|-------------|------------|
| 1 | [Question] | [Name] | [Date] | [Blank until resolved] |
| 2 | [Question] | [Name] | [Date] | [Blank until resolved] |

---

## Appendix

### Related Documents

- [Design spec link]
- [Architecture decision record link]
- [Competitive analysis link]
- [User research link]

### Glossary

| Term | Definition |
|------|-----------|
| [Term] | [Definition] |

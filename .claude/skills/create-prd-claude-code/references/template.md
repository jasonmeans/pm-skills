# PRD: [Feature Name]

> **Audience:** AI coding agent (Claude Code, Codex, or similar). This document is designed to be read and executed by an AI coding tool.

| Field | Value |
|-------|-------|
| **Author** | [Name] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft / Ready for Build |
| **Target Repo** | [repo path or URL] |
| **Language/Framework** | [e.g., TypeScript / Express.js / PostgreSQL] |
| **Design Doc** | [path/to/doc.md or N/A] |

---

## 1. Product Context

### Problem

[What user problem does this solve? Be specific -- the AI needs to understand intent to make good implementation decisions.]

### Goals

1. [Goal 1 -- measurable]
2. [Goal 2 -- measurable]

### Non-Goals

- [What this feature does NOT do]

### Success Metrics

| Metric | Target |
|--------|--------|
| [Metric 1] | [Target value] |
| [Metric 2] | [Target value] |

---

## 2. Codebase Context

### Repository Structure

```
[repo-root]/
  src/
    [relevant directories and their purposes]
  tests/
    [test directory structure]
  [other relevant top-level files]
```

### Key Patterns to Follow

- **Naming:** [e.g., camelCase for variables, PascalCase for classes, kebab-case for files]
- **Error handling:** [e.g., "All API errors use the ErrorResponse class in src/utils/errors.ts"]
- **Auth:** [e.g., "All endpoints use the authMiddleware in src/middleware/auth.ts"]
- **Database:** [e.g., "Use Prisma ORM. Migrations live in prisma/migrations/"]
- **Testing:** [e.g., "Jest with supertest for API tests. Tests mirror src/ structure in tests/"]

### Reference Files

These existing files demonstrate the patterns new code should match:

| File | Why It Matters |
|------|---------------|
| `[path/to/file]` | [e.g., "Example of a well-structured controller"] |
| `[path/to/file]` | [e.g., "Shows the standard service pattern"] |
| `[path/to/file]` | [e.g., "Example test file for API endpoints"] |

---

## 3. API Contracts

### [Endpoint 1: e.g., Create Notification Preference]

```
POST /api/v1/[resource]
Authorization: Bearer <token>
Content-Type: application/json
```

**Request body:**

```json
{
  "field1": "string",
  "field2": 123,
  "field3": true
}
```

**Response (201 Created):**

```json
{
  "id": "uuid-string",
  "field1": "string",
  "field2": 123,
  "field3": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error responses:**

| Status | Condition | Body |
|--------|-----------|------|
| 400 | Missing required field | `{ "error": "field1 is required" }` |
| 401 | Invalid or missing token | `{ "error": "Unauthorized" }` |
| 409 | Duplicate resource | `{ "error": "Resource already exists" }` |

### [Endpoint 2: e.g., Get Notification Preferences]

[Same format as above]

---

## 4. Data Model Changes

### New Tables / Collections

```sql
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  [column1] VARCHAR(255) NOT NULL,
  [column2] INTEGER NOT NULL DEFAULT 0,
  [column3] BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_[table]_[column] ON [table_name]([column1]);
```

### Modified Tables

```sql
ALTER TABLE [existing_table]
  ADD COLUMN [new_column] [TYPE] [CONSTRAINTS];
```

### Migration Notes

- [Any ordering or dependency notes for migrations]
- [Data backfill requirements, if any]

---

## 5. File Plan

### New Files to Create

| File | Purpose |
|------|---------|
| `src/[path]/[file]` | [What this file does] |
| `src/[path]/[file]` | [What this file does] |
| `tests/[path]/[file]` | [Tests for what] |

### Files to Modify

| File | Change |
|------|--------|
| `src/[path]/[file]` | [What to add or change] |
| `src/[path]/[file]` | [What to add or change] |

---

## 6. Build Sequence

Execute these steps in order. Each step should be completable and testable before moving to the next.

### Step 1: [Database / Data Model]

- [ ] Create migration file for [table/schema changes]
- [ ] Run migration and verify schema
- [ ] Create/update ORM models

### Step 2: [Core Logic / Service Layer]

- [ ] Create `src/[path]/[service-file]`
- [ ] Implement [core function 1]
- [ ] Implement [core function 2]
- [ ] Write unit tests for service layer

### Step 3: [API Layer / Controllers]

- [ ] Create `src/[path]/[controller-file]`
- [ ] Wire up routes in `src/[path]/[routes-file]`
- [ ] Add input validation
- [ ] Write API integration tests

### Step 4: [Integration / Wiring]

- [ ] Connect to existing [system/service]
- [ ] Update [existing file] to use new [module]
- [ ] End-to-end test

### Step 5: [Cleanup / Documentation]

- [ ] Update API docs
- [ ] Add logging for key operations
- [ ] Review for TODO/FIXME comments

---

## 7. Test Cases

### Unit Tests

| Test | Input | Expected Output |
|------|-------|----------------|
| [Test name] | [Input data] | [Expected result] |
| [Test name] | [Input data] | [Expected result] |
| [Edge case name] | [Edge case input] | [Expected result] |

### Integration Tests

| Test | Setup | Action | Assertion |
|------|-------|--------|-----------|
| [Test name] | [Preconditions] | [API call or action] | [What to verify] |
| [Test name] | [Preconditions] | [API call or action] | [What to verify] |

### What NOT to Test

- [Things that are already covered by existing tests]
- [Things that are out of scope]

---

## 8. Migration & Rollback

### Deploy Steps

1. [Step 1 -- e.g., "Run database migration"]
2. [Step 2 -- e.g., "Deploy service with feature flag OFF"]
3. [Step 3 -- e.g., "Enable feature flag for internal users"]
4. [Step 4 -- e.g., "Monitor for errors, then enable for all users"]

### Rollback Steps

1. [Step 1 -- e.g., "Disable feature flag"]
2. [Step 2 -- e.g., "Revert database migration with: `[command]`"]
3. [Step 3 -- e.g., "Deploy previous version"]

---

## 9. Constraints & Anti-Patterns

### Do

- [Pattern to follow]
- [Convention to match]

### Do NOT

- [Anti-pattern to avoid]
- [Thing that must not change]
- [Assumption that must not be made]

---

## 10. Open Blockers

| # | Blocker | Impact | Owner |
|---|---------|--------|-------|
| 1 | [BLOCKED -- description] | [Cannot build X without this] | [Name] |

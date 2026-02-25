---
name: create-release-notes
description: Monitor MRs into a codebase area and generate release notes summarizing all changes.
---

# PM: Create Release Notes

Generate weekly release notes by querying Jira Milestones (and optionally Epics)
for a date range, cross-referencing with source code merge requests in GitLab,
and checking Confluence for gaps. The primary source of truth is Jira; source code
and Confluence serve as validation layers.

This skill mirrors the weekly release notes process run by the release management
team (e.g., the "[Action Required] Weekly Release Notes" emails), which
queries Milestones with End Dates in a given week and asks PMs to contribute
business-facing release notes for their features.

---

## How to Help

When the user invokes this skill, follow this process:

### Phase 1: Confirm Scope

Before doing any work, confirm the following with the user:

1. **Date Range** — Default to the **current ship week** (Monday through Friday
   of the current week). If today is not a weekday, use the next upcoming week.
   Present the default and ask:

   > The default date range covers this week's ship window:
   > **Monday YYYY-MM-DD through Friday YYYY-MM-DD**.
   >
   > Would you like to:
   > - Use this week's ship window (default)
   > - Use a different week (e.g., next week, last week)
   > - Specify a longer duration (e.g., last 14 days, last 30 days, full quarter)
   > - Specify a custom date range (including future dates for upcoming releases)

   Calculate the dates based on today's date and the user's choice.

2. **Issue Types** — Default to **Milestones** (matching the weekly release notes
   process). Ask if the user also wants to include Epics:

   > By default I'll query **Milestones** (matching the weekly release notes format).
   > Should I also include **Epics**? This is useful for a more granular view.

3. **Source Repository (optional)** — Ask if the user wants to cross-reference
   a GitLab source repository. If yes, collect:
   - The repository path (e.g., `your-org/platform/your-product`)
   - How far back to look for MRs (default: same as the Jira date range)

4. **Scrum Team or Product (required for Confluence check)** — Ask which scrum
   team or product area to search Confluence for. Examples:
   - **Product:** Product A, Product B, Product C
   - **Scrum Team:** Team Alpha, Team Beta, Team Gamma

### Phase 2: Query Jira Milestones (Primary Source of Truth)

Run a JQL query to find all Milestones shipping in the date range:

```bash
AUTH_HEADER=$(python3 -c "import base64, os; u=os.environ['ATLASSIAN_USER']; t=os.environ['ATLASSIAN_TOKEN']; print(base64.b64encode(f'{u}:{t}'.encode()).decode())")

# Query Milestones with End Date in the specified range
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  -G --data-urlencode "jql=issuetype = Milestone AND \"End Date\" >= \"START_DATE\" AND \"End Date\" <= \"END_DATE\" ORDER BY assignee ASC, created DESC" \
  --data-urlencode "maxResults=100" \
  --data-urlencode "fields=summary,status,assignee,labels,customfield_10015,customfield_10014,project,description,components,fixVersions" \
  "https://contoso.atlassian.net/rest/api/3/search" | jq .
```

If the user also wants Epics, run a second query:

```bash
# Query Epics with End Date in the specified range
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  -G --data-urlencode "jql=issuetype = Epic AND \"End Date\" >= \"START_DATE\" AND \"End Date\" <= \"END_DATE\" ORDER BY assignee ASC, created DESC" \
  --data-urlencode "maxResults=100" \
  --data-urlencode "fields=summary,status,assignee,labels,customfield_10015,customfield_10014,project,description,components,fixVersions" \
  "https://contoso.atlassian.net/rest/api/3/search" | jq .
```

**Fields to extract for each Milestone/Epic:**
- **Assignee** — PM or owner responsible for the feature
- **Summary** — Title/description of the feature
- **Key** — Jira issue key (e.g., PROJ-4875)
- **End Date** — Ship date (`customfield_10015` — verify on first run)
- **Current Release Stage** — The current stage (Alpha, Closed Beta, Open Beta, GA).
  Look in labels, fixVersions, or a custom field. If not available directly,
  check the linked release in your feature flag platform or infer from labels.
- **Next Release Stage Date** — When the next stage transition is planned.
  Look in custom fields or linked issues.
- **Status** — Jira status (Done, In Progress, etc.)
- **Project** — Jira project
- **Components** — Component labels
- **Description** — First 200 chars for context

**If the user specified a scrum team**, add a team/label filter to the JQL:

```
AND (labels = "team-alpha" OR "Scrum Team" = "Team Alpha")
```

**If the user specified a product**, add a project or component filter:

```
AND (project = "PROD" OR component = "Product A")
```

**Present results in the weekly release notes format, sorted by Assignee:**

| Assignee | Summary | Key | End Date | Current Release Stage | Next Release Stage Date |
|----------|---------|-----|----------|-----------------------|-------------------------|
| Jane Smith | Campaign Level Portfolio View Settings Snapshot | PROJ-4875 | 1/30/26 | Alpha | 1/14/26 |
| Alex Johnson | Generate weekly summary of Reliability SLOs | PROJ-5123 | 1/30/26 | | |

This table matches the format sent by the release management team in the weekly
"[Action Required] Weekly Release Notes" email.

### Phase 3: Cross-Reference with Source Code (Secondary Validation)

**Skip this phase if the user did not provide a GitLab repository.**

If a source repository was specified, use the Sourcegraph MCP tools to find
merge requests / commits completed in the same date range:

```
sg_commit_search with:
  - repos: ["gitlab.example.com/your-org/<repo-path>"]  (or the user-provided path)
  - after: START_DATE
  - before: END_DATE
```

Also use `sg_diff_search` for broader pattern matching if needed.

**Compare Jira Milestones vs. Source Code:**

1. **Behind schedule (in Jira but no MR):** Flag any Milestones marked as "Done"
   or with an End Date in the range that have NO corresponding MR in the repository.
   These may be behind or may live in a different repo.

2. **Not in Jira (MR exists but no Milestone):** Flag any significant MRs (not
   just small fixes/refactors) that don't match any Jira Milestone. These might
   need to be added to release notes as undocumented changes.

Present findings as a gap analysis:

#### Potential Gaps: Milestones Without MRs
| Key | Summary | Status | Concern |
|-----|---------|--------|---------|
| PROJ-1234 | Feature X | Done | No matching MR found in repo |

#### Potential Gaps: MRs Without Jira Milestones
| MR / Commit | Description | Author | Concern |
|-------------|-------------|--------|---------|
| abc1234 | Major refactor of auth module | author@example.com | No matching Milestone found |

### Phase 4: Check Confluence for Gaps (Tertiary Validation)

**This phase requires a Scrum Team or Product to be specified.**

Search Confluence for pages related to the scrum team or product that were
created or updated in the date range:

```bash
# Search Confluence for relevant pages
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  -G --data-urlencode "cql=text ~ 'TEAM_OR_PRODUCT' AND type = page AND lastModified >= 'START_DATE' ORDER BY lastModified DESC" \
  --data-urlencode "limit=25" \
  "https://contoso.atlassian.net/wiki/rest/api/content/search" | jq .
```

**What to look for in Confluence:**
- PRDs or design docs for features not captured in the Jira query
- Existing weekly release notes pages that may have additional context
- Sprint review or demo pages with shipped features
- Decision logs or architecture docs indicating significant changes

Flag anything in Confluence that suggests a shipped feature NOT already
captured in the Jira Milestones list.

### Phase 5: Generate Release Notes

Using the data from all three sources, generate two outputs:

#### Output A: Weekly Release Notes Table (for the release manager)

This is the table format matching the weekly email. PMs use this to confirm
what's shipping and update their entries:

| Assignee | Summary | Key | End Date | Current Release Stage | Next Release Stage Date |
|----------|---------|-----|----------|-----------------------|-------------------------|

Include instructions matching the release manager's email:
1. If business-facing and shipping this week, the item belongs in release notes
2. If not scheduled to ship, flag it so the End Date can be updated in Jira
3. Note the deadline (typically EOD Thursday before the ship week)

#### Output B: Business-Facing Release Notes (for stakeholders)

Generate release notes following the template in
`prompts/claude/release-notes-writer.xml`. Categorize each item using standard
changelog categories:

- **New** — New features, capabilities, endpoints
- **Changed** — Modified behavior, performance improvements, updated defaults
- **Fixed** — Bug fixes (describe what was broken and what's fixed now)
- **Deprecated** — Features being phased out (include timeline and migration path)
- **Removed** — Features that have been removed
- **Security** — Security-related changes

**Writing guidelines:**
- Lead with developer/user impact, not implementation details
- Be precise about what changed and where
- For breaking changes, include migration guidance
- Reference Jira Milestone/Epic keys so readers can drill into details
- Note the release stage (Alpha, Closed Beta, Open Beta, GA) for each item
- Group items by product area or scrum team when multiple teams are covered

**Present a draft to the user for review before finalizing.**

### Phase 6: Review & Iterate

After presenting the draft:
1. Ask if any items should be added, removed, or reworded
2. Ask about audience — is this for external developers, internal teams, or both?
3. Ask if any items are breaking changes requiring migration guidance
4. Flag items that appear to be missing release stage information
5. Flag items where the End Date may need updating (not actually shipping)
6. Iterate until the user approves

---

## Custom Field Reference

Jira custom fields vary by instance. On first run, if the End Date field
(`customfield_10015`) doesn't return data, discover the correct field:

```bash
# Get all fields to find the End Date custom field ID
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  "https://contoso.atlassian.net/rest/api/3/field" | jq '.[] | select(.name | test("end date"; "i"))'
```

Similarly, discover fields for Current Release Stage and Next Release Stage Date:

```bash
# Find release stage fields
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  "https://contoso.atlassian.net/rest/api/3/field" | jq '.[] | select(.name | test("release stage"; "i"))'
```

---

## Weekly Process Context

This skill supports the weekly release notes process:

1. **Release management** sends a weekly email on Wednesday
   titled "[Action Required] Weekly Release Notes MM/DD-MM/DD"
2. The email contains a table of Milestones with End Dates in the upcoming ship week
3. PMs review the table and either:
   - Add business-facing release notes to the shared document if their feature is shipping
   - Update the End Date in Jira if the feature is not shipping that week
4. Deadline is **EOD Thursday** before the ship week
5. Once reviewed and approved, release notes are moved to Confluence

### Published Release Notes Reference

The canonical published release notes live on the **Product Weekly Release Notes**
Confluence page. Check your Confluence instance for the published release notes page
in the PROD space.

This page is the best reference for the final published format. Key structural
elements to match when generating release notes:

- **Weekly heading** — `Week MM/DD` with a blue heading style
- **Table of Contents** — Numbered list of feature titles linking to anchors
- **Per-feature sections** include:
  - **Release Stage Timeline** — Table with columns: Release Stage (Alpha, Closed Beta, Open Beta, GA) and Date for each
  - **Feature Overview** — Business-facing description of what changed and why it matters
  - **How to use this feature** — Step-by-step instructions with screenshots
  - **How do I get access?** — Internal vs. external access instructions
  - **Where can I learn more or ask questions?** — POC contact
  - **Product Resources** — Slack channels, Confluence links
  - **Product Marketing Narrative & Commercial Training Resources** — Training links, recordings, guides
- **Index + Past Notes** — Link to archived notes and a TOC of all past entries
- Notes are published every **Tuesday at 1:00 PM ET** and announced in `#product-updates`

Use this page as a reference when formatting the final output in Phase 5.

This skill automates step 2 — generating the table and drafting business-facing
release notes — so PMs can review and refine rather than write from scratch.

---

## Example Invocation

```
User: /create-release-notes

Claude: I'll generate release notes for you. Let me confirm the scope:

**Date Range:** This week's ship window is **Monday 2026-02-16 through Friday 2026-02-20**.

Would you like to:
1. Use this week's ship window (default)
2. Use a different week (e.g., next week, last week)
3. Specify a longer duration (e.g., last 30 days, full quarter)
4. Specify a custom date range (including future dates)

**Issue Types:** I'll query Milestones by default (matching the weekly release
notes format). Should I also include Epics for a more granular view?

**Optional — Source Code:** Do you want to cross-reference a GitLab repository?
If so, which one?

**Required — Team/Product:** What scrum team or product should I search in
Confluence? (e.g., "Product A" as a product, or "Team Alpha" as a scrum team)
```

---

## Dependencies

- **Required:** `ATLASSIAN_USER` and `ATLASSIAN_TOKEN` environment variables
- **Required:** Jira access with permission to query Milestones and Epics
- **Optional:** Sourcegraph MCP tools (for GitLab cross-reference)
- **Optional:** Confluence access (for gap analysis)
- **Reference:** `prompts/claude/release-notes-writer.xml` for output template

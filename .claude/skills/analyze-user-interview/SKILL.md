---
name: analyze-user-interview
description: Analyze a Zoom user interview — merges a VTT transcript with Confluence interview notes to produce a complete research summary with themes, pain points, friction points, and product signals, formatted for Confluence or saved as a local markdown file.
---

# User Interview Analyzer

You are acting as a hybrid expert — part senior UX researcher, part Product Manager — analyzing a completed user interview. These sessions typically involve one user (the interviewee), a PM (the interviewer), and one or two engineers as observers. Treat this like a rigorous research artifact: extract signal, not noise.

Your job is to merge two required inputs (Zoom VTT transcript + Confluence interview notes) and an optional third (Zoom video recording) into a single, cohesive, well-structured research summary.

---

## Step 0: Collect Inputs

Before doing anything, confirm which inputs are available. Ask for any missing required inputs.

| # | Input | Required | Description |
|---|-------|----------|-------------|
| 1 | **Zoom VTT transcript** | Yes | Path to the `.vtt` file from the Zoom recording |
| 2 | **Confluence interview notes** | Yes | URL or page ID of the Confluence page with the interview template and PM notes |
| 3 | **Zoom video recording link** | No | Zoom cloud recording URL |

If the user has not provided both required inputs, ask for them before proceeding. Do not guess file paths. Also ask for the Zoom video link if not provided — it will be referenced on the final page.

---

## Step 1: Read the Confluence Interview Notes

Fetch the Confluence page using the REST API:

```bash
AUTH_HEADER=$(python3 -c "import base64, os; u=os.environ['ATLASSIAN_USER']; t=os.environ['ATLASSIAN_TOKEN']; print(base64.b64encode(f'{u}:{t}'.encode()).decode())")

# If the user provided a page URL, extract the page ID from it
# URL pattern: https://YOUR_DOMAIN.atlassian.net/wiki/spaces/SPACE/pages/PAGE_ID/...
# Or search by title if they gave a title instead of URL

curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  "https://YOUR_DOMAIN.atlassian.net/wiki/rest/api/content/PAGE_ID?expand=body.storage,body.view,version,space,ancestors" | jq .
```

Extract and understand:

- **Interview goals** — What the PM was trying to learn; what decisions this informs
- **Interview structure** — What questions/tasks were in the template
- **PM notes** — Any observations, quotes, or highlights captured during the session
- **Participant info** — Name, role, team, tenure if captured
- **Product context** — Which product area or feature was being evaluated

### 1a. Identify Existing Template Fields

Scan the existing page for these fields. They are typically at the top of the page or in the interview template:

- Date
- Interviewer (name, role)
- Interviewee (name, role, team)
- Observers (names, roles)
- Interview Type (Open interview / Usability study / Mixture)
- Duration
- Interview Goals

Record which fields are present and which are missing or empty. You will fill in missing fields from the transcript analysis in Step 6.

---

## Step 2: Parse the VTT Transcript

Read the `.vtt` file using the Read tool. VTT files follow this format:

```
WEBVTT

1
00:00:01.000 --> 00:00:04.500
Speaker Name: Thank you for joining today.

2
00:00:05.000 --> 00:00:08.200
Conference Room A: We were looking at the dashboard and...
```

### 2a. Detect Conference Room Names

Scan the speaker labels in the transcript. Flag any that appear to be conference room names or device names rather than real people, including patterns like:

- `Conference Room`, `Room [A-Z0-9]`, `Room [Name]`
- `iPhone`, `iPad`, `Android`
- `H.323`, `SIP`, or other hardware endpoint labels
- Any label that does not look like a person's name

**If conference room names are detected:** Stop and ask the user:

> "I found the following speaker labels in the transcript that appear to be conference room names rather than real names:
>
> - **Conference Room A** — Who is this? (Name and role: interviewer, interviewee, or observer)
> - **Conference Room B** — Who is this? (Name and role)
>
> Please provide a mapping so I can attribute quotes and comments correctly."

Wait for the user's response before continuing. Replace all conference room labels with real names in your working analysis.

### 2b. Build a Cleaned Transcript

After resolving all speaker names, produce a cleaned version of the transcript:

- Merge consecutive utterances by the same speaker
- Remove filler words sparingly (e.g., trailing "um um um" strings), but **preserve all substantive speech verbatim** — do not paraphrase or clean up the user's words
- Note timestamps for key moments (large topic shifts, notable reactions, screen-share starts/stops)
- Tag the interviewee's turns with their name; tag PM and engineers separately

---

## Step 3: Handle Video Input (Optional)

If a Zoom video link was provided, you will reference it on the page (see Step 6). If the user also provided a local video file path:

> Note: Direct video analysis is not available. However, the video is valuable for observing screen-sharing portions of usability studies.

Ask the user:

> "You provided a video recording. Since I can't analyze video directly, would you like to:
>
> 1. Describe key visual moments from the video (e.g., where the user hesitated, struggled, or expressed confusion while sharing their screen)?
> 2. Provide timestamps of moments worth noting, and I'll reference them in the analysis?
> 3. Skip the video for now and work from transcript + notes only?
>
> If this was a usability study with screen sharing, option 1 or 2 will significantly improve the analysis."

Incorporate any visual observations the user provides as **Screen Observation** annotations in the analysis.

---

## Step 4: Analyze — Extract Signal

Working from the merged transcript + Confluence notes + any video observations, run a full research analysis. Apply your expertise as both a UX researcher and a PM. Look for:

### Themes
Group related comments, behaviors, and moments across the session into 3–7 coherent themes. A theme is a pattern that appeared more than once — either in words, hesitation, a repeated question, or a consistent behavior.

Name each theme concisely. Example: "Navigation Confusion Around Release Stages" not "Users had trouble with things."

### Pain Points
Specific, discrete problems the user encountered or described. These are the moments where something didn't work, was confusing, or required a workaround. Pull direct quotes where possible.

Distinguish between:
- **Functional pain points** — the product broke, failed, or was missing a needed feature
- **Comprehension pain points** — the user didn't understand what something was, meant, or did
- **Workflow pain points** — the product interrupted or didn't support the user's natural workflow

### Friction Points
Moments where the user paused, hesitated, re-read something, clicked the wrong thing, asked a clarifying question, or took longer than expected. These are often not verbalized — they show up as behavioral signals in the transcript (e.g., long silence, "wait, where is...", "hmm", re-asking a question that was already answered).

### Frustrations
Emotionally charged moments — explicit or implicit. The user expressing irritation, resignation, skepticism, surprise, or annoyance. Pull verbatim quotes. Do not soften the language.

### What's Working
Moments of ease, delight, or positive confirmation. "Oh that's nice", task completion without hesitation, statements of preference. Do not omit these — they anchor what to protect.

### Product Signals
Opportunities, feature gaps, or design directions implied by the session. These are not direct quotes — they are the PM's inference from observed behavior + stated problems. Label these as inferences clearly.

---

## Step 4b: Clean Up Interview Notes

Before composing the AI summary, clean up the human-written "Interview Notes:" sections in the original template. These notes are jotted down quickly during a live interview and often contain grammar errors, typos, abbreviations, and half-baked thoughts.

**Do:**
- Fix spelling, grammar, and punctuation errors
- Expand obvious abbreviations (e.g., "ff" -> "feature flags", "perf" -> "performance")
- Lightly clarify half-finished thoughts where the intent is obvious from context — keep the original meaning intact
- Remove trailing blank lines / empty paragraphs (`<p />`) after the last bullet in each Interview Notes section to keep the document compact
- Preserve the bullet structure and content — do not add, remove, or reorder bullets

**Do NOT:**
- Rewrite or rephrase the notes — the interviewer's voice should still come through
- Add new observations or insights that weren't in the original notes
- Change the meaning or emphasis of any note
- Touch anything outside of "Interview Notes:" bullet sections (e.g., template questions, guidance panels, probing questions are left as-is)

---

## Step 5: Compose the Research Summary

Produce a structured, well-formatted research summary. **Do NOT include an "Interview Summary" header with Date/Interviewer/Interviewee/Observers/Duration/Goals in the AI analysis.** That information belongs in the interview template fields at the top of the page and will be updated there directly (see Step 6). The AI analysis starts with the Executive Summary.

Use this structure for the AI analysis content:

---

### Executive Summary

2–4 sentences. What was the most important finding? What should the PM do with this? Write for someone who will only read this section.

---

### Key Themes

For each theme:

**Theme: [Name]**
> Supporting quote 1 — *[Speaker]*
> Supporting quote 2 — *[Speaker]*

Brief synthesis (2–3 sentences): what this theme means for the product.

---

### Pain Points

Table format:

| Pain Point | Type | Quote / Evidence | Severity |
|------------|------|-----------------|----------|
| [concise label] | Functional / Comprehension / Workflow | "[verbatim quote]" — *[Speaker]* | High / Medium / Low |

Severity guidance:
- **High** — blocked the user, required a workaround, or was mentioned unprompted multiple times
- **Medium** — slowed the user down or caused confusion, but they recovered
- **Low** — minor friction, mentioned once, user moved past it quickly

---

### Friction Points

| Moment | Timestamp | What Happened | Interpreted Signal |
|--------|-----------|---------------|-------------------|
| [brief label] | [HH:MM] | [behavioral observation] | [what this suggests] |

---

### Frustrations

Pull verbatim quotes. Do not summarize. Let the user's voice come through.

> "[Exact quote]" — *[Speaker], [HH:MM]*

---

### What's Working

> "[Exact quote]" — *[Speaker], [HH:MM]*

Brief note on what to protect or reinforce.

---

### Product Signals

These are PM inferences, not direct quotes. Label them as such.

| Signal | Source | Confidence | Suggested Next Step |
|--------|--------|------------|---------------------|
| [opportunity or gap] | Behavior / Direct statement | High / Medium / Hypothesis | [concrete action] |

---

### Notable Quotes

The most quotable moments from the session — the lines worth putting in a slide, a PRD, or a stakeholder update.

> "[Quote]" — *[Speaker]*

---

### Transcript Coverage Notes

Flag any issues with the transcript: gaps, crosstalk, off-topic segments, etc.

---

### Recommended Next Steps

Concrete actions for the PM, ranked by priority:

1. [Action] — [brief rationale]
2. [Action] — [brief rationale]
3. [Action] — [brief rationale]

---

## Step 6: Confirm Output Destination

**Before writing or modifying anything**, ask the user:

> "The analysis is ready. How would you like me to save it?
>
> 1. **Save locally as markdown** — I'll save the summary to your Desktop as `interview-analysis-[product-slug]-[YYYY-MM-DD].md`.
> 2. **Update the Confluence interview page** — I'll append the AI analysis and update the interview metadata directly on the linked Confluence page.
>
> Which would you prefer?"

Wait for confirmation. Do not write to Confluence or disk without the user's explicit choice.

---

## Step 7: Deliver Output

### Confluence Page Layout — MANDATORY STRUCTURE

When writing to Confluence (whether updating or creating a copy), the page MUST follow this exact layout from top to bottom. This layout is **non-negotiable** and must be consistent across ALL interview pages produced by this skill.

#### Section 1: Interview Participant Info (very top of page)

These fields go at the **very top** of the page, above everything else. Check the existing interview template for these fields and update them directly. If any are missing, add them.

**Do NOT include:**
- The interviewee's name as a heading — the Confluence page title already contains it
- Interview Goals — these are part of the interview template and belong in the Interview Notes section
- Duration — this is captured in the Interview Metadata table at the bottom

**Required fields** — render as a **single `<p>` block** with `<br />` between each line (no separate paragraphs, no blank lines). This keeps the section tight and compact:

```xml
<p><strong>Zoom Video Recording:</strong> <a href="[URL]">[URL]</a><br />
<strong>Date:</strong> [date]<br />
<strong>Interviewer:</strong> <ac:link><ri:user ri:account-id="[ACCOUNT_ID]" /></ac:link>, [role]<br />
<strong>Interviewee:</strong> <ac:link><ri:user ri:account-id="[ACCOUNT_ID]" /></ac:link>, [role, team, tenure if known]<br />
<strong>Observers:</strong> <ac:link><ri:user ri:account-id="[ACCOUNT_ID]" /></ac:link> ([role]) &middot; <ac:link><ri:user ri:account-id="[ACCOUNT_ID]" /></ac:link> ([role])<br />
<strong>Interview Type:</strong> [Open interview / Usability study / Mixture]<br />
<strong>Product / Repo:</strong> [product area]<br />
<strong>Relevant Context:</strong> [context]</p>
```

**@ mentioning people:** For every person referenced (interviewer, interviewee, observers), attempt to tag them using the Confluence `<ac:link><ri:user ri:account-id="..." /></ac:link>` markup. To find account IDs, search the Atlassian user directory:

```bash
AUTH_HEADER=$(python3 -c "import base64, os; u=os.environ['ATLASSIAN_USER']; t=os.environ['ATLASSIAN_TOKEN']; print(base64.b64encode(f'{u}:{t}'.encode()).decode())")

# Search for a user by name
curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  "https://YOUR_DOMAIN.atlassian.net/wiki/rest/api/search/user?cql=type=user%20AND%20user.fullname~%22[NAME]%22" | jq '.results[] | {accountId, displayName: .user.displayName}'
```

If the existing page already contains `<ri:user ri:account-id="...">` tags for any participants, reuse those account IDs. If a user cannot be found, fall back to plain text for that name.

Do NOT duplicate these in the AI analysis section. If the template already has these fields, update them with data from the transcript. If a field is missing (e.g., "Interview Type" is not in the template), add it.

#### Section 2: Interview Notes Callout Box

Wrap the human interview notes in a Confluence panel with these exact colors:

```xml
<ac:structured-macro ac:name="panel" ac:schema-version="1" data-layout="default">
  <ac:parameter ac:name="borderColor">#00875A</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:parameter ac:name="borderWidth">2</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#00875A</ac:parameter>
  <ac:parameter ac:name="title">Interview Notes</ac:parameter>
  <ac:rich-text-body>
    <p>These are the original interview notes captured by the interviewer during the session. They include the interview template questions, real-time observations, and post-interview reflections.</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

**Color: Green (#00875A)** — This callout introduces the human-written interview notes section.

The human interview notes content follows immediately after this callout. This includes:
- Interview Goals
- Warm-Up section
- General Feedback section
- Core Questions (all sub-questions)
- Magic Wand section
- Wrap-Up section
- Post-Interview Notes table

#### Section 3: AI Interview Analysis Callout Box

After all human interview notes, add the AI analysis section wrapped in its own callout:

```xml
<ac:structured-macro ac:name="panel" ac:schema-version="1" data-layout="default">
  <ac:parameter ac:name="borderColor">#0052CC</ac:parameter>
  <ac:parameter ac:name="titleColor">#FFFFFF</ac:parameter>
  <ac:parameter ac:name="borderWidth">2</ac:parameter>
  <ac:parameter ac:name="titleBGColor">#0052CC</ac:parameter>
  <ac:parameter ac:name="title">AI Interview Analysis &mdash; Generated [YYYY-MM-DD]</ac:parameter>
  <ac:rich-text-body>
    <p>This analysis was generated by the <strong>analyze-user-interview</strong> skill, merging the Zoom VTT transcript with the PM interview notes above. See the Interview Notes section above for the original template and observations.</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

**Color: Blue (#0052CC)** — This callout introduces the AI-generated analysis section.

The AI analysis content follows immediately after this callout:
- Executive Summary
- Key Themes (with sub-theme headings)
- Pain Points (table)
- Friction Points (table)
- Frustrations (verbatim quotes)
- What's Working (verbatim quotes)
- Product Signals (table)
- Notable Quotes
- Transcript Coverage Notes
- Recommended Next Steps

#### Section 4: Interview Metadata Table (very bottom)

The Interview Metadata table goes at the **very bottom** of the page, below everything else. This is the enriched reference table with all metadata about the interview.

```xml
<h2>Interview Metadata</h2>
<table data-table-width="1800" data-layout="default">
  <tbody>
    <tr><th>Field</th><th>Value</th></tr>
    <tr><td><strong>Interviewee</strong></td><td>[Name]</td></tr>
    <tr><td><strong>Role / Title</strong></td><td>[Role]</td></tr>
    <tr><td><strong>Team</strong></td><td>[Team name]</td></tr>
    <tr><td><strong>Tenure</strong></td><td>[If known]</td></tr>
    <tr><td><strong>Geographic Location</strong></td><td>[If known]</td></tr>
    <tr><td><strong>Products They Work On</strong></td><td>[Products mentioned in interview]</td></tr>
    <tr><td><strong>Repos They Work Out Of</strong></td><td>[If mentioned]</td></tr>
    <tr><td><strong>Interviewer</strong></td><td>[Name, role]</td></tr>
    <tr><td><strong>Observers</strong></td><td>[Names, roles]</td></tr>
    <tr><td><strong>Interview Date</strong></td><td>[Date]</td></tr>
    <tr><td><strong>Interview Type</strong></td><td>[Type]</td></tr>
    <tr><td><strong>Duration</strong></td><td>[Duration]</td></tr>
    <tr><td><strong>Zoom Video Recording</strong></td><td><a href="[ZOOM_URL]">[ZOOM_URL]</a></td></tr>
    <tr><td><strong>Champion Candidate</strong></td><td>[Yes/No/Unknown]</td></tr>
    <tr><td><strong>Early Adopter Candidate</strong></td><td>[Yes/No/Unknown]</td></tr>
    <tr><td><strong>Follow-Up Needed</strong></td><td>[Yes/No — details]</td></tr>
  </tbody>
</table>
```

Fill in every field you can from the transcript and interview notes. If a field was already populated in the existing Post-Interview Notes table, preserve that value. If you discovered additional information from the transcript (e.g., products they mentioned working on, repos referenced), add it. Leave fields blank only if truly unknown.

### Callout Box Summary

| Callout | Color | Hex | Position |
|---------|-------|-----|----------|
| **Interview Notes** | Green | `#00875A` border + title BG, `#FFFFFF` title text | After participant info, before AI analysis |
| **AI Interview Analysis** | Blue | `#0052CC` border + title BG, `#FFFFFF` title text | After interview notes, before metadata table |

These colors and positions must be identical on every interview page. No exceptions.

---

### If writing to Confluence (update existing page)

Read the current page version first, then update:

```bash
AUTH_HEADER=$(python3 -c "import base64, os; u=os.environ['ATLASSIAN_USER']; t=os.environ['ATLASSIAN_TOKEN']; print(base64.b64encode(f'{u}:{t}'.encode()).decode())")

# Get current version number
VERSION=$(curl -s -H "Authorization: Basic $AUTH_HEADER" -H "Accept: application/json" \
  "https://YOUR_DOMAIN.atlassian.net/wiki/rest/api/content/PAGE_ID?expand=version" | jq '.version.number')

# Update the page (increment version)
curl -s -H "Authorization: Basic $AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PUT \
  -d '{
    "version": {"number": '$((VERSION + 1))'},
    "title": "PAGE_TITLE",
    "type": "page",
    "body": {
      "storage": {
        "value": "[FULL_PAGE_XHTML]",
        "representation": "storage"
      }
    }
  }' \
  "https://YOUR_DOMAIN.atlassian.net/wiki/rest/api/content/PAGE_ID" | jq '._links.webui'
```

### If creating a copy (sibling page)

```bash
AUTH_HEADER=$(python3 -c "import base64, os; u=os.environ['ATLASSIAN_USER']; t=os.environ['ATLASSIAN_TOKEN']; print(base64.b64encode(f'{u}:{t}'.encode()).decode())")

# Create sibling page under the same parent
curl -s -H "Authorization: Basic $AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  -d '{
    "type": "page",
    "title": "[Interviewee Name] - [Interview Topic] (AI Enhanced)",
    "space": {"key": "SPACE_KEY"},
    "ancestors": [{"id": "PARENT_PAGE_ID"}],
    "body": {
      "storage": {
        "value": "[FULL_PAGE_XHTML]",
        "representation": "storage"
      }
    }
  }' \
  "https://YOUR_DOMAIN.atlassian.net/wiki/rest/api/content" | jq '.id, ._links.webui'
```

Return the page URL so the user can view it immediately.

### If saving locally

Save the markdown file to the user's Desktop:

```
~/Desktop/interview-analysis-[product-slug]-[YYYY-MM-DD].md
```

Confirm the file path after writing.

---

## Analyst Mindset — Rules for Quality

These rules apply throughout the analysis. Never violate them.

**Do:**
- Use verbatim quotes from the interviewee wherever possible. The user's own words are more powerful than your summary.
- Distinguish between what the user *said*, what they *did*, and what you *infer*. Label each clearly.
- Follow the interview goals. Every theme and pain point should connect back to what the PM was trying to learn.
- Note absence of signal. If the interview template had a goal the session didn't address, flag it: "This goal was not covered in the session."
- Attribute all quotes. Never present a quote without the speaker's name.
- Be specific. "Users struggled with navigation" is weak. "The interviewee spent 47 seconds searching for the Release Pipeline button before asking the PM where it was" is useful.

**Do not:**
- Soften or editorialize user frustrations. If they said "this is confusing as hell," quote it.
- Over-infer. Product signals should be labeled as inferences, not conclusions.
- Generate themes from a single data point. One quote is a data point; a pattern across multiple moments is a theme.
- Omit positive findings to appear more analytical. A balanced report builds more PM credibility.
- Write for the user who was in the room. Write for the stakeholder who wasn't there.
- Include an "Interview Summary" section with Date/Interviewer/Interviewee/etc. in the AI analysis — that information belongs in the template fields at the top of the page.

---

## Common Pitfalls to Flag

- **Transcript gaps:** Long silences, "[inaudible]", or missing chunks — flag these so the PM knows what was lost.
- **Crosstalk:** If multiple people spoke at once and the transcript is garbled, note the approximate time and flag it.
- **Off-topic segments:** If significant time was spent on setup, technical difficulties, or off-topic conversation, note it so it doesn't distort the analysis.
- **Facilitator influence:** If the PM's questions were leading or the interviewee appeared to be telling the PM what they wanted to hear (Mom Test failures in the live session), flag this as a caveat on that finding's reliability.

---

## Related Skills

- `/create-user-interview` — Create the interview template used as input to this skill
- `/jobs-to-be-done` — Turn interview findings into JTBD personas and use cases
- `/storytelling-for-impact` — Craft a stakeholder narrative from research findings
- `/create-prd` — Feed interview learnings into a product requirements document

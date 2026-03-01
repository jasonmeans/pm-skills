---
name: analyze-user-interview
description: Analyze a Zoom user interview — merges a VTT transcript with PM interview notes (markdown) to produce a complete research summary saved as a local markdown file.
---

# User Interview Analyzer

You are acting as a hybrid expert — part senior UX researcher, part Product Manager — analyzing a completed user interview. These sessions typically involve one user (the interviewee), a PM (the interviewer), and one or two engineers as observers. Treat this like a rigorous research artifact: extract signal, not noise.

Your job is to merge two required inputs (Zoom VTT transcript + PM interview notes markdown file) and an optional third (Zoom video recording) into a single, cohesive, well-structured research summary saved as a local markdown file.

---

## Step 0: Collect Inputs

Before doing anything, confirm which inputs are available. Ask for any missing required inputs.

| # | Input | Required | Description |
|---|-------|----------|-------------|
| 1 | **Zoom VTT transcript** | Yes | Path to the `.vtt` file from the Zoom recording |
| 2 | **PM interview notes** | Yes | Path to the markdown file with the interview template and PM notes |
| 3 | **Zoom video recording link** | No | Zoom cloud recording URL |

If the user has not provided both required inputs, ask for them before proceeding. Do not guess file paths. Also ask for the Zoom video link if not provided — it will be referenced in the output.

---

## Step 1: Read the PM Interview Notes

Read the markdown file using the Read tool. Extract and understand:

- **Interview goals** — What the PM was trying to learn; what decisions this informs
- **Interview structure** — What questions/tasks were in the template
- **PM notes** — Any observations, quotes, or highlights captured during the session
- **Participant info** — Name, role, team, tenure if captured
- **Product context** — Which product area or feature was being evaluated

### 1a. Identify Existing Template Fields

Scan the existing file for these fields. They are typically at the top:

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

If a Zoom video link was provided, you will reference it in the output. If the user also provided a local video file path:

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

Working from the merged transcript + PM notes + any video observations, run a full research analysis. Apply your expertise as both a UX researcher and a PM. Look for:

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
- Remove trailing blank lines / empty paragraphs after the last bullet in each Interview Notes section to keep the document compact
- Preserve the bullet structure and content — do not add, remove, or reorder bullets

**Do NOT:**
- Rewrite or rephrase the notes — the interviewer's voice should still come through
- Add new observations or insights that weren't in the original notes
- Change the meaning or emphasis of any note
- Touch anything outside of "Interview Notes:" bullet sections (e.g., template questions, guidance panels, probing questions are left as-is)

---

## Step 5: Compose the Research Summary

Produce a structured, well-formatted research summary. **Do NOT include an "Interview Summary" header with Date/Interviewer/Interviewee/Observers/Duration/Goals in the AI analysis.** That information belongs in the metadata section at the top of the output file. The AI analysis starts with the Executive Summary.

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

## Step 6: Save Output as Markdown

Save the analysis to the user's Desktop:

```
~/Desktop/interview-analysis-[interviewee-slug]-[YYYY-MM-DD].md
```

The output file follows this structure:

```markdown
# Interview Analysis: [Interviewee Name] — [YYYY-MM-DD]

## Interview Metadata

| Field | Value |
|-------|-------|
| **Date** | [date] |
| **Interviewer** | [name, role] |
| **Interviewee** | [name, role, team, tenure if known] |
| **Observers** | [names, roles] |
| **Interview Type** | [Open interview / Usability study / Mixture] |
| **Product / Area** | [product area] |
| **Duration** | [duration] |
| **Zoom Recording** | [URL or N/A] |
| **Champion Candidate** | [Yes / No / Unknown] |
| **Early Adopter Candidate** | [Yes / No / Unknown] |
| **Follow-Up Needed** | [Yes / No — details] |

---

## Original PM Interview Notes

[Cleaned-up version of the PM's notes from the markdown input file, preserving structure]

---

## AI Interview Analysis — Generated [YYYY-MM-DD]

[Executive Summary through Recommended Next Steps as composed in Step 5]
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
- Include an "Interview Summary" section with Date/Interviewer/Interviewee/etc. in the AI analysis — that information belongs in the metadata table at the top.

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

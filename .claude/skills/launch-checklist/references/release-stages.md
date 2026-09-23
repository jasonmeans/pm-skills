# Release Stages

Default stage model for launches. Teams can rename stages, but keep the idea: each stage widens access only after it clears a stricter quality bar.

| Stage | Access | Quality bar | Typical length |
|---|---|---|---|
| **Alpha** | Internal team only | Dev complete; bugs are being triaged | 1–4 weeks |
| **Closed Beta** | All employees plus selected partners or customers | No open P0 or P1 bugs | 2–6 weeks |
| **Open Beta** | All employees plus opt-in early adopters | No open P0, P1, or P2 bugs | 2–8 weeks |
| **GA** | All customers | Feature complete, no critical issues, success metrics trending the right way | n/a |

## Promotion Criteria

**Alpha → Closed Beta**
- P0 and P1 bugs fixed; known issues documented
- Feature flag or allowlist controls access; rollback path tested
- Basic monitoring and error alerting in place
- Beta participants identified; feedback channel ready
- Marketing and training prep starts (see `gtm-plan`)

**Closed Beta → Open Beta**
- P2 bugs fixed or explicitly accepted by the approvers
- Support trained; FAQ and troubleshooting guide published internally
- Runbooks approved; on-call owner named
- Public docs drafted; opt-in or waitlist mechanism works
- Holdout or A/B measurement ready if success needs proving

**Open Beta → GA**
- Success metrics trending up against the baseline; no unresolved guardrail regressions
- Public docs, changelog, and release notes final (see `create-release-notes`)
- Sales and customer success enabled; pricing and packaging live if applicable
- Security, privacy, legal, and accessibility sign-offs recorded
- Launch communications scheduled; go/no-go meeting held

## Priority Definitions (for the quality bar)

| Priority | Meaning |
|---|---|
| **P0** | Data loss, security exposure, outage, or no workaround for a core flow. Stop the launch. |
| **P1** | Core flow broken or badly degraded for many users; a painful workaround exists. |
| **P2** | Secondary flow broken, or a core-flow defect with an easy workaround. |
| **P3** | Cosmetic or edge-case issues. Never blocks a stage. |

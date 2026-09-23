# Launch Readiness: [Feature] → [Target stage]

**Launch DRI:** [name] · **Target date:** [YYYY-MM-DD] · **Review date:** [YYYY-MM-DD]
**Links:** PRD [..] · GTM plan [..] · Dashboard [..] · Runbook [..]

Status key: ✅ done (evidence linked) · ⚠️ at risk (plan, owner, date) · ❌ blocked · N/A (reason)
Stage tags: **A** Alpha · **CB** Closed Beta · **OB** Open Beta · **GA**. Include every item tagged with the target stage or an earlier one.

## Quality Bar

| Open bugs | Count | Allowed at [stage] | Pass? |
|---|---|---|---|
| P0 | | 0 | |
| P1 | | 0 from CB onward | |
| P2 | | 0 from OB onward | |

## Checklist

| Area | Item | Stage | Owner | Status | Evidence |
|---|---|---|---|---|---|
| Product | Scope matches the PRD; cut items documented | A | | | |
| Product | Success metrics defined with baseline and target | A | | | |
| Product | Known issues and limitations written down | CB | | | |
| Engineering | Feature flag or allowlist controls access | A | | | |
| Engineering | Automated tests cover core flows; CI green | A | | | |
| Engineering | Rollback or kill switch tested | CB | | | |
| Engineering | Performance and load checked at expected scale | OB | | | |
| Operations | Monitoring, dashboards, and alerts live | CB | | | |
| Operations | Runbook approved; on-call owner named | OB | | | |
| Operations | Capacity and cost limits reviewed | OB | | | |
| Security & privacy | Threat review or security sign-off | CB | | | |
| Security & privacy | Data handling and privacy review (PII, retention) | CB | | | |
| Legal | Terms, licensing, and claims reviewed | OB | | | |
| Design & accessibility | Design QA on supported platforms | CB | | | |
| Design & accessibility | Accessibility check (keyboard, screen reader, contrast) | OB | | | |
| Data | Analytics events instrumented and verified | CB | | | |
| Data | Experiment or holdout configured (if needed) | OB | | | |
| Docs | Internal docs and FAQ | CB | | | |
| Docs | Public docs, changelog, release notes | OB | | | |
| Support | Support trained; macros and escalation path ready | OB | | | |
| Marketing | Launch communications ready (per GTM tier) | GA | | | |
| Sales & CS | Enablement done; pricing and packaging live | GA | | | |
| Feedback | Beta feedback channel monitored; themes reviewed | CB | | | |

## Blockers and Risks

| Item | Impact | Plan | Owner | Due |
|---|---|---|---|---|

## Recommendation

**[Go | Go with conditions | No-go]** for [stage] on [date].
Conditions or blockers: [..] · Next review: [date if no-go]

## Sign-offs

| Function | Approver | Decision | Date | Notes |
|---|---|---|---|---|
| Product | | | | |
| Engineering | | | | |
| Design | | | | |
| Support | | | | |
| Security / Legal | | | | |
| Marketing | | | | |

## Post-launch Checks

- **+1 day:** error rates, alerts, support volume, top feedback
- **+1 week:** adoption and success metrics against target; decision to hold, roll back, or continue
- **Retro** scheduled: [date]

# Review Process Design: [Team or Repo]

**Owner:** [name] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Pilot / Adopted
**Baseline:** [link to review-baseline.md] · **Pilot:** [repo/team, dates]

## Problem

[Two or three sentences with numbers from the baseline, e.g. "Median time to first review is 19h and p90 is 70h; XL PRs are 30% of merges and 80% of the p90."]

## Risk Tiers

| Tier | Paths (allowlist) | Automated checks | AI review | Human approval | Merge |
|---|---|---|---|---|---|
| 0 | `docs/**`, `**/*.md`, tests only | All required | Optional, non-blocking | Optional | Auto after checks |
| 1 | Everything not listed in 0 or 2 | All required | First pass, blocks on high severity | 1 reviewer | Author after approval |
| 2 | `auth/**`, `billing/**`, `migrations/**`, `infra/**`, `.github/workflows/**` | All required plus security scan | Required, blocks on medium or higher | Code owner | Owner merges; no auto-merge |

Unrecognized paths fall into Tier 1, or Tier 2 if they match a sensitive marker (secret, token, auth, key, lockfile).

## Automated Checks (required on every PR)

- [ ] Format and lint · [ ] Type check · [ ] Unit tests · [ ] Secret scan · [ ] Dependency review
- [ ] PR size warning above 400 changed lines · [ ] Forbidden-file check · [ ] PR template complete

## AI Review Gate

- **Runs:** [pre-PR locally | CI check] · **Model/effort by tier:** [..]
- **Blocks on:** [severity threshold] · **Records:** [check run | PR-body stamp]
- **Round cap:** 3, then a human decides · **Skip protocol:** Tier 0–1 only; record reason and substitute review

## Human Review

- **SLA:** first response within [1 business day]; re-review within [4 business hours]
- **Assignment:** CODEOWNERS plus [rotation tool]
- **Humans review:** intent, design, correctness in risky areas, operability. Style belongs to the checks.
- **Emergency path:** hotfix merges with one approval; full review within 24h; logged

## Metrics (reviewed monthly)

| Metric | Baseline | Target |
|---|---|---|
| First review p50 / p90 (h) | | |
| Merge p50 (h) | | |
| PRs over 400 lines | | |
| Change-request rounds per PR | | |
| Escaped defects per tier | | |

## Rollout

1. Pilot [repo/team] for [2–4] weeks → 2. Rerun `scripts/pr_review_stats.py` → 3. Adjust → 4. Expand

---

## Starter Config

### `.github/CODEOWNERS`

```text
# Tier 2 paths need an owner's approval (enable "Require review from Code Owners").
/auth/        @org/security-owners
/billing/     @org/payments-owners
/migrations/  @org/data-owners
/infra/       @org/platform-owners
/.github/     @org/platform-owners
```

### `.github/pull_request_template.md`

```markdown
## What and why
<!-- One paragraph. Link the issue or spec. -->

## Risk tier
- [ ] 0 (docs/tests)  - [ ] 1 (standard)  - [ ] 2 (auth, billing, data, infra)

## How it was verified
<!-- Tests run, screenshots, manual steps. -->

## Review record
<!-- AI review verdict and round, or the skip reason and substitute review. -->

## Rollback
<!-- How to undo this if it misbehaves in production. -->
```

### Branch protection (main)

- [ ] Require a pull request before merging, with 1 approval (Tier 2 paths via CODEOWNERS)
- [ ] Require review from Code Owners
- [ ] Require status checks: [lint, typecheck, test, secret-scan, ai-review]
- [ ] Dismiss stale approvals when new commits are pushed
- [ ] Restrict who can push to main; allow admins to bypass only for the emergency path

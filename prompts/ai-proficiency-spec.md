# Developer AI workflow proficiency: analysis specification and Claude Code handoff

Version 1.2 · 2026-09-08 · Intended runner: Claude Code with the user's chosen model

## Executive overview — for leadership

### Problem and decision

We want to understand how broadly developers use AI in engineering so we can target training, improve tooling, and track adoption. We have usage records for captured tools and voluntary survey responses from roughly half of developers in April and August. Usage volume alone does not tell us whether someone asks questions, delegates a task, or automates a workflow.

**The question:** Can measured usage patterns reliably predict the workflow level a developer would select in the survey? This analysis tests that relationship and reports uncertainty for each developer. It measures reported workflow scope; it does not establish underlying skill or engineering performance.

### Inputs and outputs

**Inputs:** a complete developer roster; identity mappings, survey dates, and verified tracking coverage; 30 days of AI usage before each survey; and the April/August survey answers. Jira, merge-request, spend, team, and role data provide context for checking who responded.

**Outputs:** one record per developer in the latest period, containing a provisional level when supported, probabilities for Levels 1–4, their separate survey selection if available, and an explanation when evidence is insufficient. A companion report explains accuracy, probability reliability, coverage, and survey-selection limitations.

### What defines a level?

| Level | Defining evidence from the workflow survey |
|---|---|
| 0 | No engineering AI use; the current survey cannot establish this |
| 1 | Small tasks: snippets, questions, advice |
| 2 | Larger tasks: debugging, tests, refactoring |
| 3 | Multiple workflow steps: code, tools, validation |
| 4 | End-to-end agent workflows with human review |

### Which measured signals help estimate it?

| Signal | What it measures |
|---|---|
| Input, output, and total AI tokens | Amount of interaction with captured AI tools |
| Days with positive AI usage | How regularly the developer uses those tools |
| Sessions with positive AI usage, when available | How often the developer starts or participates in recorded AI sessions |

**There is no predetermined token, session, or spending threshold for a level.** The model learns whether combinations of these signals distinguish survey answers. High usage can reflect repeated failed attempts as well as effective delegation. Model choice, spend, and code output do not award proficiency points.

### How the logic works

Learn patterns from April, then predict August before using August's answers to check the predictions. Check whether the percentages match observed answers and whether respondents differ from nonrespondents. Release a provisional level only when both the model and the individual's evidence meet the specified criteria.

**Illustration only:** probabilities of 5%, 10%, 70%, and 15% make Level 3 the leading estimate, conditional on AI use. The 70% concerns a possible survey answer, not independently verified competence. Even this estimate is withheld if evidence checks fail. Level 0 remains unknown; zero recorded usage is insufficient proof.

**Decision value:** identify supported adoption patterns and evidence gaps. Reliable classification of every developer is not guaranteed; insufficient evidence is a valid outcome.

## Technical one-pager — for the data scientist

### Problem, unit, and target

Estimate a four-class survey-response distribution from telemetry for each developer-window. The observation unit is **one developer × one survey wave**, not a session. The target is `P(Y=k | X, AI use, usable survey response)`, for `k=1…4`. Transport to nonrespondents requires an unverified selection assumption. True competence and Level 0 are unidentified.

### Inputs → analysis table → outputs

Join the complete wave-specific roster, audited observation coverage, dated telemetry, and survey exports using canonical developer IDs. Build fixed 30-day windows ending before survey opening. Remove aggregate rows; reject duplicate keys and overlapping metric sources. Sum additive daily/session events, but select a single correctly dated rolling snapshot. Preserve missing values unless explicit zero-fill conditions hold.

Map only the workflow-use answer to `Y=1…4`; preserve its text and mapped self-selection. Exclude incompatible or unmapped labels from fitting. Use complete-coverage, positive-usage rows for prediction. Output the latest roster with conditional probabilities, separate self-selection, candidate/provisional levels, and abstention status, plus validation and selection diagnostics.

### How signals become probabilities

`X` contains input/output/total tokens, positive-use days, and positive-use sessions where available. Apply `log1p`, training-fold median imputation with missing indicators, and standardization. Fit L2 multinomial logistic regression with fixed `C=0.3`.

For transformed features `z`, class scores are `s_k = intercept_k + coefficients_k · z`. Base probabilities are `softmax(s)`; temperature calibration returns `softmax(log(p_base)/T)`. The survey data determine coefficients; grouped out-of-fold predictions determine `T`. No coefficients, signal directions, or level cutoffs have been empirically established on company data yet. Team, role, productivity, spend, and survey context are excluded from this classifier.

### Validation and release logic

Use three outer developer-grouped folds within April, with three-fold grouped temperature calibration inside each outer training partition. Then fit the April pipeline and freeze it before predicting August. August labels evaluate predictions only. Distinguish returning respondents from unseen respondents.

Compare against a smoothed April class-frequency prior using log loss, Brier score, ranked probability score, confusion matrices, and classwise reliability bins. Each fitting partition requires ≥80 labeled rows and ≥12 developers per class, so nesting requires more data overall.

Temporal release requires ≥80 usable answers, ≥10 per class, every class's calibration error ≤0.10 and recall ≥0.35, and a paired developer-bootstrap Brier-difference interval wholly below zero. Individual release additionally requires complete positive telemetry, support checks, maximum probability ≥0.65, and a top-two margin ≥0.15. Otherwise leave the provisional level blank.

### Selection and interpretation

Report respondent balance, cross-fitted usable-label propensity, clipped/capped inverse-selection weighted scores, and assumed nonresponse-shift scenarios. These cannot identify unobserved selection bias. Bootstrap intervals describe fixed-model held-out error variability, not individual skill uncertainty. Failed validation means the available features may not distinguish the scale; changing the model or scale after examining August requires fresh validation.

---

The following sections provide the full operational specification and exact file contracts.

## 1. Assignment and deliverable

Work locally with the supplied company CSV or spreadsheet exports. Use the scripts in `tools/ai-proficiency/` to estimate each developer's **reported AI workflow scope**, using telemetry as predictors and self-selected survey answers as the only outcome labels. No company data was available when this package was designed. Synthetic fixtures verify software behavior only.

Deliver one row for every developer in the latest company roster: a provisional level when evidence permits, the full conditional probability distribution, the corresponding survey selection when available, and a clear reason when the model abstains. Preserve the distinction between observed responses and predicted responses. Produce the aggregate methodology and validation report alongside the row-level file.

The intended use is understanding adoption patterns and planning enablement. The available evidence does not establish engineering performance, code quality, or an individual's underlying competence.

**Success does not require classifying everyone.** If aggregate usage fails to predict workflow scope, the correct result is that these inputs cannot support the requested individual classification. Do not invent thresholds that force a distribution across levels.

## 2. What can be estimated

The primary estimand is:

`P(Y = k | X = x, AI use, usable survey response), k ∈ {1,2,3,4}`

Here, `Y` is the mapped answer to the workflow-use question, `X` is the preceding 30-day telemetry, and a usable response is a recognized, internally compatible answer. Applying this model to nonrespondents additionally assumes that response selection does not change the relationship between telemetry and reported scope, after conditioning on measured features. That assumption is not testable with these data alone.

For example, a synthetic distribution of 10%, 25%, 50%, 15% means the model assigns those probabilities to four possible **survey scope answers**, conditional on AI use. It is not a 50% independently verified chance that the person possesses Level 3 skill. Calibration is a property assessed across comparable predictions, not proof about a particular person.

The study is supervised probabilistic classification with an imperfect, self-selected reference outcome. It is not unsupervised discovery of true proficiency. Do not cluster users by spend and name the clusters proficiency levels. Do not label records using token thresholds and validate against those same labels. Do not treat telemetry sessions as independent labeled people.

## 3. Revised scale and relationship to the original

Call this **AI workflow scope, version 1**. Retain the familiar numbers, but narrow the claims to what the survey actually measures.

| Level | Operational definition | Difference from the original scale |
|---|---|---|
| 0 | No AI use for engineering in the reference period | Retained conceptually; unidentifiable from the supplied survey and incomplete tool coverage |
| 1 | Small tasks and assistance: snippets, questions, advice | Broader than chat-only use; the survey does not identify the interface |
| 2 | Larger bounded tasks: debugging, tests, refactoring | Measures task scope; does not require autonomous execution |
| 3 | Multiple workflow steps: code, tools, and validation | Does not assert that an agent automatically merges or deploys |
| 4 | Agents or automation complete workflows end-to-end with human review | Does not establish harness design, multi-agent orchestration, or that this is the person's primary work style |

These are ordered categories of reported scope, not equally spaced amounts of skill. Broader automation is not always the best choice for a task. Tight steering can reflect expert practice, and delegating can reflect either effective design or excessive trust.

Model 1–4 as four distinct categories initially. Use ordinal error metrics, but do not force the proportional-odds assumption. The supplied classifier is multinomial logistic regression. It can learn nonmonotonic relationships between telemetry and class probabilities.

**Level 0:** the supplied question has no “no AI for engineering” option. “I don't use AI for coding” allows use for explanations, reviews, design, or other engineering work. Zero measured tokens means no recorded use of the captured tools; it does not prove no use of other tools. Consequently, `p_0_pct` is blank, not zero, and probabilities for 1–4 are explicitly conditional. Never describe those four columns as an unconditional five-class distribution.

If distinguishing 3 and 4 fails, the script reports an exploratory merged-category accuracy. This is a diagnostic, not permission to claim the merged scale was independently validated. Freeze a proposed revision and validate it in a fresh wave, or pre-register scale/model selection inside a fully nested evaluation before examining outcomes. Do not renumber historical survey responses without a versioned crosswalk.

## 4. Exact survey treatment

Only “Which best describes how you use AI tools today?” defines the training outcome:

| Exact supplied answer | Mapped self-selected level |
|---|---|
| I use AI for small tasks (snippets, quick questions) | 1 |
| I use AI for larger tasks (debugging, writing tests, refactoring) | 2 |
| I use AI across multiple steps in a workflow (code + tools + validation) | 3 |
| I use AI agents/automation to complete workflows end-to-end (with human review) | 4 |

`self_selected_level` is this deterministic crosswalk, not an answer to a numeric-level question the user never saw. Keep the original text in the prepared local file. Missing answers remain missing. Unknown wording is marked `unmapped_usage`; inspect the distinct wording locally and add an explicit versioned crosswalk only if its meaning matches. No fuzzy matching or LLM-generated labels.

Other answers are retained as context:

- **Default style:** separate steering/delegation dimension; subgroup diagnostics, never training labels or predictors.
- **Model preference:** task preference, never a proficiency bonus. “No AI for coding” plus workflow scope 2–4 is marked contradictory and excluded from outcome fitting. The original mapped selection remains visible. Scope 1 plus no AI coding can be compatible.
- **Barriers:** retain for enablement interpretation. Training needs, limits, trust concerns, and orchestration complexity are not direct evidence of low proficiency. Multi-select answers remain multi-select text; do not count them as mutually exclusive people.

The current script does not perform thematic coding or infer skill from free text. No session-content review, manager ratings, code-quality scores, or synthetic labels may be introduced as validation outcomes under this assignment.

## 5. Files and commands

**Recommended Claude Code entrypoint:** run `/analyze-ai-proficiency /path/to/exports` or `/analyze-ai-proficiency /path/to/manifest.json` from this repository. The [skill](../.claude/skills/analyze-ai-proficiency/SKILL.md) handles environment setup, file inspection, manifest preparation, execution, and result checks. `/analyze-ai-proficiency setup` prepares the environment; `/analyze-ai-proficiency demo` uses invented data only. Python 3.11 or 3.12 must already be available.

The implementation consists of:

| File | Responsibility |
|---|---|
| `tools/ai-proficiency/workflow.py` | Bootstrap dependencies, inspect file schemas, run preflight/analysis, verify results in a unique run directory |
| `tools/ai-proficiency/prepare.py` | Load files, enforce grain/units/joins/windows, map labels, build developer-wave rows |
| `tools/ai-proficiency/model.py` | Fixed feature whitelist, grouped nested validation, temperature calibration, metrics, release gate |
| `tools/ai-proficiency/analyze.py` | Temporal analysis, selection diagnostics, abstentions, row-level and aggregate exports |
| `tools/ai-proficiency/synthetic.py` | Generate invented CSV/XLSX fixtures with optional absent signal |
| `tools/ai-proficiency/tests/test_pipeline.py` | Statistical invariants and ingestion/end-to-end regression tests |
| `tools/ai-proficiency/tests/test_workflow.py` | Input inventory, run lifecycle, and output verification tests |
| `tools/ai-proficiency/requirements.txt` | Compatible dependency ranges |

From the repository root, using Python 3.11 or 3.12:

```bash
python3 -m venv tools/ai-proficiency/.venv
tools/ai-proficiency/.venv/bin/python -m pip install -r tools/ai-proficiency/requirements.txt
tools/ai-proficiency/.venv/bin/python -m pytest tools/ai-proficiency/tests -q
tools/ai-proficiency/.venv/bin/python tools/ai-proficiency/synthetic.py --out /tmp/ai-scope-demo --xlsx
tools/ai-proficiency/.venv/bin/python tools/ai-proficiency/analyze.py --manifest /tmp/ai-scope-demo/manifest.json --out /tmp/ai-scope-demo-results
```

For real inputs, create a manifest next to the approved local files and run:

```bash
tools/ai-proficiency/.venv/bin/python tools/ai-proficiency/prepare.py --manifest /path/to/local/manifest.json --out /path/to/new/preflight
tools/ai-proficiency/.venv/bin/python tools/ai-proficiency/analyze.py --manifest /path/to/local/manifest.json --out /path/to/new/analysis
```

Output directories must not already exist. Each execution is a new run. Real data, generated predictions, and identity mappings belong outside version control; the package's `data/`, `outputs/`, and `demo/` directories are ignored as a convenience. Do not commit company records or paste them into this handoff document. The analysis scripts contain no network calls and do not require data to be sent to the creator of this package. Retain the runtime version and code/input hashes in each local run.

The `workflow.py` bootstrap installs Python dependencies from the package index when needed; this setup step uses the network without sending input files. `workflow.py run --manifest /path/to/manifest.json` creates a unique timestamped directory under `ai-proficiency-runs/` beside the manifest unless `--out` is supplied. It adds `run-complete.json` only after output verification succeeds. A failed statistical gate can still be a successfully completed, verified run with abstentions. The lower-level commands above remain available for direct use.

## 6. Required input contract

### Company roster and identity

Provide one row per developer per wave, including nonusers, nonrespondents, and people with no telemetry. The company denominator cannot be recovered from an AI usage export alone.

Required canonical roster columns: `username`, `wave`, `team`, `userlevel`, `invited`, `ai_observed_days`.

- `username`: stable canonical developer ID. Use exact joins and an optional explicit alias-to-ID table. Do not fuzzy-join similar names. Service/shared accounts must be resolved or excluded with documented counts before running.
- `wave`: exact manifest wave name. The roster must contain both waves, with one row per identity per wave. A developer can be present in only one wave.
- `team`, `userlevel`: descriptive context and response-selection diagnostics. Use metadata effective at the wave, or explicitly document that only current metadata exists. These fields never define level labels.
- `invited`: `true`/`false` or `1`/`0`. Response rate denominator is invited developers; the prediction denominator is the latest company roster.
- `ai_observed_days`: audited integer 0–30 indicating days of functioning observation of the declared AI tool universe for this developer. This is monitoring/access metadata, **not the number of days with positive AI events**. If unknown, conservatively use 0 and document “unknown coverage”; the row will abstain. Never manufacture complete coverage merely to get predictions.

If no roster or no auditable dates/coverage exist, prepare a specific missing-input report. Do not pretend the observed AI-user table represents every company developer. This is the principal additional metadata requirement beyond the supplied export fields.

### Survey export

Required: `username`, `wave`, `response_date`, `usage`. Optional: `style`, `preference`, `barriers`. Header mappings allow the original full question text to be used without editing source files. `response_date` must be inside the declared collection period. Survey respondents must join to invited roster members. Duplicate submissions stop the run; choose and document a rule such as final submission within collection dates before creating a resolved derivative. Do not silently keep the most convenient answer.

### Windows

Use the same 30 calendar days for every person within a wave, ending before the survey opens. The example uses March 2–31 before April collection and July 2–31 before August collection; these are examples, not assumptions about the real survey dates or year.

Use explicit ISO dates in the manifest. Normalize timestamps to UTC before deriving calendar days; if exports use local calendar days, convert consistently in an auditable adapter and document the timezone. Do not use a September rolling snapshot to reconstruct April or August.

The fixed windows avoid using behavior after a respondent answers. They also introduce a lag for late respondents. Report that limitation. If individual response-relative windows are required, implement and test them separately; do not silently mix dates within this protocol. The original “today” wording also lacks a precise recall window, which weakens temporal alignment.

### Telemetry grain

Every source declares `daily`, `session`, or `snapshot`. Different source files may contribute different canonical metrics, but a metric can have only one authoritative source. Combine tool-specific event exports into one auditable canonical source before the run; never append daily totals and the sessions underlying them.

| Grain | Required keys | Aggregation |
|---|---|---|
| daily | `username`, `date` | Sum additive AI token fields inside the window; derive positive-use days |
| session | `username`, `date`, `session_id` | Unique session keys, sum additive AI token fields; derive positive-use sessions and days |
| snapshot | `username`, `date`; `window_days: 30` | Select the record exactly at the wave's window end; never sum rolling snapshots |

Duplicate daily keys or duplicate developer/session IDs stop execution. If a session export repeats request-level rows, aggregate by session first using documented semantics. A session spanning days needs a declared attribution rule. This package treats `date` as the attributed session day and does not infer session boundaries or durations.

`ordering` rows 0, 1, and 2 are removed; only individual rows with 3 remain. If no ordering field exists, the source must declare `individual_only: true`.

Missing events may become zero **only** for daily/session sources declaring `absent_means_zero: true` and developers with all 30 days of independently verified coverage. Blank metric values inside existing events make that window metric unknown. Missing snapshots remain missing. The package refuses to combine a partial sum with an assumption that unknown values were zero.

### Canonical metrics and interpretation

| Export field | Canonical name | Use |
|---|---|---|
| Input / Output / Total tokens | `ai_input`, `ai_output`, `ai_total` | Primary predictors; total is required |
| Positive usage days / sessions, if genuinely available | `ai_active_days`, `ai_sessions` | Primary predictors; leave unavailable fields missing |
| MRs Merged / LOC Changed / Avg MR Size | `mrs_merged`, `loc_changed`, `avg_mr_size` | Response-balance context only |
| MRs Commented / MRs Reviewed | `mrs_commented`, `mrs_reviewed` | Response-balance context only |
| Total Issues | `issues` | Response-balance context only |
| Feature Stories / Epics / Spikes / KLON fractions | `feature_share`, `epic_share`, `spike_share`, `klon_share` | Response-balance context only |
| Small fraction | `small_share` | Omit until the truncated definition is clarified |
| Claude / Cursor / Total Spend | `claude_spend`, `cursor_spend`, `total_spend` | Response-balance context only |
| Cursor % | `cursor_share` | Response-balance context only |
| Primary / Secondary / Third Model | No primary feature mapping | Retain source for context; no capability ranking or probability bonus |

Activity, spend, and share metrics must come from a separate or combined authoritative 30-day snapshot in this implementation. Daily additive AI fields are supported directly; daily Jira rolling fields are not additive. Fractions from daily exports must not be summed or averaged without their correct denominators. Ratios such as LOC/MR should be recomputed from window totals in an adapter if needed, with missing output for a zero denominator.

`Total` may include cache-input tokens beyond `Input + Output`. Check the provider's definitions: input can sometimes already include cached tokens. The script allows total to exceed input plus output and permits a 2% rounding tolerance in the other direction. It does not infer cache hits, autonomous run duration, prompt complexity, model mix, review quality, or agent orchestration from these totals. If definitions overlap, map a consistent authoritative token basis locally and document it before running.

All numeric mappings declare a unit: `number`, `fraction`, `percent`, `usd`, or `cents`. `1.2m` and `2k` are expanded. `25%` or `25` with `percent` becomes 0.25. A bare 0.25 with `fraction` stays 0.25. Currency conversion from cents is explicit. Do not divide spend by 100 if the export already contains dollars. Blank, NA, and dashes mean missing; invalid/negative numbers stop execution.

### Manifest example

Paths are relative to the manifest. XLSX/XLS files require an explicit `sheet`; CSV and TSV do not. The following minimal example uses rolling snapshots with the original telemetry headers:

```json
{
  "waves": [
    {"name": "April", "start": "2026-03-02", "end": "2026-03-31", "survey_start": "2026-04-01", "survey_end": "2026-04-10"},
    {"name": "August", "start": "2026-07-02", "end": "2026-07-31", "survey_start": "2026-08-01", "survey_end": "2026-08-10"}
  ],
  "roster": {"path": "roster.csv"},
  "survey": {
    "path": "survey.xlsx",
    "sheet": "Responses",
    "columns": {"usage": "Which best describes how you use AI tools today?"}
  },
  "telemetry": [{
    "path": "snapshots.csv",
    "grain": "snapshot",
    "window_days": 30,
    "metrics": {
      "ai_input": {"column": "Input", "unit": "number"},
      "ai_output": {"column": "Output", "unit": "number"},
      "ai_total": {"column": "Total", "unit": "number"},
      "total_spend": {"column": "Total Spend", "unit": "usd"},
      "cursor_share": {"column": "Cursor %", "unit": "percent"},
      "mrs_merged": {"column": "MRs Merged", "unit": "number"}
    }
  }]
}
```

For aliases, add `"aliases": {"path": "aliases.csv"}` with `alias,username` columns. Multiple aliases may identify one developer, but duplicate aliases and resulting duplicate source keys must be resolved. All source-specific header mappings use canonical-name → actual-header direction. Metric `column` names refer to the table after that header mapping.

## 7. Model and validation protocol implemented now

1. **Freeze the protocol before inspecting outcomes.** Use exactly two ordered waves. Training responses must end before the later telemetry window starts. Do not tune this protocol on August and continue calling August untouched.
2. **Choose usable training rows.** First-wave respondents with a mapped compatible scope answer, complete observation coverage, and positive recorded AI total. This restricts the modeled domain and must appear in the report. Missing usage does not imply Level 0.
3. **Transform a fixed feature set.** `log1p` of input/output/total tokens, positive-use days, and sessions. Median imputation, missing indicators, and standardization are fitted inside each training fold. Structurally unavailable fields stay missing. No survey fields, identity, team, role, spend, or code throughput enter the scope model.
4. **Fit a simple baseline classifier.** L2-regularized multinomial logistic regression, fixed `C=0.3`; no hyperparameter search and no class balancing or oversampling that would alter class priors. Compare with a Laplace-smoothed training class-frequency prior.
5. **Calibrate within training only.** Three-fold developer-grouped out-of-fold probabilities fit one temperature, bounded to 0.5–5. Refit the base estimator on that training partition. This OOF-calibrator/refit approach can experience distribution shift between fold models and the refit; the outer and temporal evaluations assess the resulting pipeline. Do not describe temperature scaling itself as proof of calibration.
6. **Measure first-wave generalization with nested evaluation.** Three outer developer-grouped folds; every outer training set performs its own inner calibration. A developer cannot appear in both sides of an outer or inner split. Preprocessing is repeated inside the folds. Each fitting partition needs at least 80 labeled rows and at least 12 distinct developers per class; all inner folds must contain all four classes. In practice the full first wave needs more than 80 rows because of nesting. Failure produces an evidence-shortfall result, not synthetic classes or zeros for absent classes.
7. **Freeze first-wave training and score the entire second-wave roster.** Fit once on usable first-wave labels; August labels do not enter features, fitting, or calibration. Evaluate against usable August answers only. Report returning first-wave respondents and new respondents separately, with metrics only for subgroups of at least 20. Temporal validation among returning users allows prior-wave labels from the same person in training; this answers a different question from unseen-person generalization.
8. **Report proper scores and ordinal errors.** Multiclass log loss; unnormalized multiclass Brier score `sum_k (p_k - 1[Y=k])²`; ranked probability score averaging the three cumulative-boundary errors; accuracy, macro-F1, MAE, and the 4×4 confusion matrix. Brier ranges from 0 to 2. A uniform four-class model has Brier 0.75. Class reliability tables use five fixed probability bins with counts, mean prediction, and observed frequency. Low Brier alone does not demonstrate calibration.
9. **Compare with the prior using a paired cluster bootstrap.** 500 developer resamples of fixed held-out prediction errors yield a 95% percentile interval for model Brier minus prior Brier. This estimates evaluation-sample variability conditional on the fitted models. It does not capture training-refit variability, measurement error, nonresponse bias, or population calibration uncertainty.
10. **Apply predeclared reporting gates.** At least 80 usable temporal responses and 10 per class; upper paired Brier-difference interval below zero; each class's binned calibration error ≤0.10; every class recall ≥0.35. These are explicit conservative operating defaults, not research-established universal cutoffs. A passing gate is permission for provisional reporting against this respondent reference, not certification of proficiency or company-wide validity.

Only a passing gate permits `predicted_level`. Each individual must also have max probability ≥0.65, a first-versus-second probability margin ≥0.15, complete positive telemetry, and no feature outside the training min/max or novel missing/present feature regime. Otherwise abstain. The support check is deliberately simple and conservative; it cannot prove covariate overlap in high dimensions. Conditional probabilities remain visible as exploratory estimates where computable, even when no level is released.

The model is frozen on the first wave for this analysis; it is not refit on August afterward. The resulting August values are historical estimates for the declared period, not current September proficiency. Future scoring requires a versioned new observation window and an explicit reuse/revalidation policy. Do not silently carry an August label forward as truth.

## 8. Self-selection and uncertainty

About 50% participation does not imply representativeness. Report, separately by wave: company roster count, invited count, responded count, usable-label count, observation eligibility, and label exclusions. Distinguish survey nonresponse from missing/contradictory item answers and missing telemetry.

The implementation supplies:

- Respondent/nonrespondent standardized mean differences and missingness by telemetry/context field. These are descriptive differences, not evidence of causality.
- A separate cross-fitted usable-label propensity model among invited, observable active users. Predict label availability from AI features, observation coverage, team, and role. Report AUC, extreme propensities, capped weights, and effective sample size. One row per person per wave avoids duplicate-person leakage here.
- Weighted held-out scores as a sensitivity check, using stabilized inverse selection weights, propensity clipping to [0.05,0.95], and weight caps of 10. They rely on selection being explained by measured variables; they do not correct unknown selection mechanisms or certify nonrespondent accuracy. Weight-estimation uncertainty is not included in the reported error interval.
- Exponential-tilt scenarios for unobserved scope answers: multiply each successive level's odds by 0.5, 1, or 2 and renormalize. These are deliberately chosen stress scenarios, not learned probabilities. They apply only to observable active users with predictions; known usable labels remain fixed. People outside that domain remain unclassified.
- No-assumption category-share bounds in that same conditional domain: `observed category count / N` to `(observed category count + unknown outcomes) / N`. These are marginal bounds, not a jointly attainable probability vector or confidence intervals; even the observed survey labels can contain error.

Use all three perspectives—unweighted held-out results, measured-selection weighting, and unknown-selection scenarios. If conclusions depend materially on the scenario, say so. Do not publish a classical company-wide margin of error for a voluntary sample. No bootstrap can reveal the unseen respondents' true answers from nothing.

## 9. Outputs and interpretation

| Output | Contents |
|---|---|
| `developer_predictions.csv` | Every latest-wave roster member, conditional percentages, separate mapped self-selection, candidate/provisional levels, evidence status |
| `prepared.csv` | Auditable developer-wave table, original survey context, mapped labels, coverage, features |
| `input_audit.json` | Input hashes, median-row removals, outside-window counts, joins/label coverage summaries |
| `development_oof.csv` | Held-out first-wave developer predictions and outer fold assignments, when fitting succeeds |
| `calibration.csv` | Temporal class reliability bins, when temporal labels exist |
| `response_balance.csv` | Response imbalance and missingness diagnostics |
| `label_propensity.csv` | Cross-fitted usable-label propensity and sensitivity weight, when supported |
| `selection_sensitivity.csv` | Conditional-domain scenario shares and no-assumption bounds |
| `analysis.json` | Metrics, gates, subgroups, software versions, manifest/code hashes |
| `report.md` | Concise locally generated methods/results/limitations summary |

Probabilities are percentages in the developer file, proportions elsewhere. The four conditional percentages sum to 100 up to export rounding. `candidate_probability_pct` is the probability of the argmax candidate, not a calibrated probability that the released label is “correct proficiency.” `entropy_normalized` describes concentration of the modeled distribution, not a confidence interval on true skill.

`self_selected_level` is populated only from that wave's recognized survey answer. `label_status` discloses contradictions or unrecognized/missing text. Do not replace a developer's self-selection with a prediction, or turn their self-selection into a 100% model probability.

Primary row statuses are `provisional_estimate`, `low_confidence`, `out_of_training_support`, `validation_gate_failed`, `insufficient_training_evidence`, `incomplete_telemetry`, and `no_recorded_AI_use_level_0_unidentified`. Blank outputs are intentional. A first-wave respondent flag identifies temporal scores for returning respondents; it does not mean the August outcome was used in training.

The generated report is a factual starting point. Claude should add a concise synthesis of actual observed failures, selection sensitivity, and what the evidence permits. Do not infer causes from model coefficients or differences in team output. Do not equate a change in sample composition or tool coverage with a proficiency improvement.

## 10. Acceptance tests and execution instructions for Claude

Read this specification and the code before accessing exports. Inventory only schemas, sheet names, date ranges, grain, units, identity coverage, and row counts at first. Build the manifest and any necessary narrow local adapters. Record transformations and exclusions. Ask the data owner one focused question when missing definitions prevent a defensible join or window; do not guess the meaning of “Small,” snapshot dates, cache fields, or unknown observation coverage.

Run the provided tests before analyzing real data. The suite checks numeric units, missing-vs-zero behavior, aggregate exclusion, duplicate detection, snapshot selection, exact survey mapping, contradiction handling, CSV/XLSX equivalence, feature leakage, group separation, missing classes, probability normalization, small-sample abstention, and independence of predictions from holdout labels. Daily/session tests enforce event deduplication and honest missing totals.

Run preflight and inspect the audit. Then run the frozen two-wave analysis once. Explain every failed gate; do not relax gates to make the result look successful. Report real sample counts and class supports. A synthetic passing test only demonstrates functioning code. If training fails, deliver all roster rows with explicit missing-evidence statuses and preserved survey selections.

Before delivery, verify:

1. Exactly one output row for every latest roster developer, including people with zero usage or no survey response.
2. Every nonmissing probability is finite, in [0,100], and the four conditional columns sum to approximately 100; `p_0_pct` remains blank.
3. No later-wave outcome entered fitting/calibration, and model features match the fixed whitelist.
4. No aggregate median rows, duplicate source keys, or rolling-window double counts remain.
5. All estimates identify their period, scale version, probability target, validation scope, and abstention reasons.
6. The report explicitly distinguishes respondent validation from unverified transport to nonrespondents.

Deliver `developer_predictions.csv`, `report.md`, and the supporting audit/metrics files together. Do not send company data or findings back to the author of this package.

## 11. Optional next-wave improvements; not implemented or validated now

Keep the current workflow question stable for a bridge wave. Add a separate explicit engineering-AI nonuse option or question with a last-30-days reference period. Ask about typical rather than maximum-ever task scope. Measure steering/delegation independently. If harness design is important, add distinct behavioral items for designing reusable agent instructions, tool permissions, evaluation loops, recovery/checkpoints, and orchestration; avoid a single double-barreled “expert” option. These remain self-reports and do not objectively validate skill.

With larger samples, pre-register comparisons against an ordinal model, an AI-total-only baseline, and a richer telemetry model including independently measured tool/validation events. Compare ablations with and without spend, model family, role, and task-mix context under nested developer-grouped evaluation; do not assume extra predictive signal reflects proficiency. Add leave-team-out evaluation when transfer to unseen teams matters. Rich session content is outside this run and must not become a validation label under the user's survey-only constraint.

Per-person bootstrap refit intervals, conformal sets, calibration-bin intervals, automatic chart generation, empirical tuning, and an operational daily scoring service are not implemented in this reference package. Additional uncertainty methods would still need to address selection and temporal drift; they would not establish latent true proficiency.

## 12. Research basis

- Voluntary-sample population inference depends on assumptions that a high participation rate alone cannot establish. Weighting observed covariates may leave selection bias. See the [AAPOR Task Force report on non-probability sampling](https://aapor.org/wp-content/uploads/2022/11/NPS_TF_Report_Final_7_revised_FNL_6_22_13-2.pdf) and [AAPOR's distinction between model-based intervals and sampling margins of error](https://aapor.org/statements/understanding-a-credibility-interval-and-how-it-differs-from-the-margin-of-sampling-error-in-a-public-opinion-poll/).
- Calibrators need predictions generated independently of the fitting observations. Proper scores assess more than calibration; reliability diagrams provide complementary evidence. See [scikit-learn probability calibration](https://scikit-learn.org/stable/modules/calibration.html). Developer grouping follows the separation principles documented in [StratifiedGroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html), with transformations fitted inside folds as described in [common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).
- Software activity is only one dimension of developer productivity. Using counts as a proficiency scale would require separate validity evidence. See [The SPACE of Developer Productivity](https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/?lang=ja).

The revised scale, chosen features, sample-size floors, and reporting thresholds are design proposals for this assignment. These sources motivate the measurement discipline; they do not validate this particular scale or prove that the listed telemetry predicts it.

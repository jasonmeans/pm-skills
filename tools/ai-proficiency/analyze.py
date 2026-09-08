"""Run a frozen first-wave model against second-wave survey validation, locally."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import softmax
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from prepare import AI, CONTEXT, prepare
from model import (CalibratedModel, InsufficientEvidence, metrics, nested_oof,
                   release_gate, reliability)


def selection_audit(frame):
    """Response and label availability are distinct selection events."""
    summaries, balance, propensity_rows = [], [], []
    for wave, all_rows in frame.groupby('wave', sort=False):
        invited = all_rows.loc[all_rows.invited].copy()
        summaries.append({'wave': wave, 'company_n': len(all_rows), 'invited_n': len(invited),
                          'responded_n': int(invited.responded.sum()),
                          'response_rate': float(invited.responded.mean()) if len(invited) else None,
                          'eligible_n': int(invited.eligible.sum()),
                          'usable_label_n': int((invited.eligible & invited.label.notna()).sum())})
        for col in AI + CONTEXT:
            yes = invited.loc[invited.responded, col].dropna().astype(float)
            no = invited.loc[~invited.responded, col].dropna().astype(float)
            denom = np.sqrt((yes.var() + no.var()) / 2) if min(len(yes), len(no)) > 1 else np.nan
            diff = (yes.mean() - no.mean()) / denom if denom > 0 else np.nan
            balance.append({'wave': wave, 'feature': col, 'respondent_n': len(yes), 'nonrespondent_n': len(no),
                            'standardized_mean_difference': diff,
                            'respondent_missing_rate': float(invited.loc[invited.responded, col].isna().mean()),
                            'nonrespondent_missing_rate': float(invited.loc[~invited.responded, col].isna().mean())})
        # Propensity is a diagnostic of usable-label selection within observable active users.
        eligible = invited.loc[invited.eligible].copy()
        y = eligible.label.notna().astype(int).to_numpy()
        if len(y) < 30 or len(np.unique(y)) < 2 or np.bincount(y).min() < 5:
            continue
        numeric = AI + ['ai_observed_days']
        x = eligible[numeric + ['team', 'userlevel']].copy()
        x[numeric] = np.log1p(x[numeric])
        transform = ColumnTransformer([
            ('numeric', make_pipeline(SimpleImputer(keep_empty_features=True), StandardScaler()), numeric),
            ('context', OneHotEncoder(handle_unknown='ignore'), ['team', 'userlevel'])])
        p = np.zeros(len(y))
        for train, test in StratifiedKFold(5, shuffle=True, random_state=42).split(x, y):
            # One row per developer in each wave, so this split cannot duplicate developers.
            import sklearn.base
            estimator = make_pipeline(sklearn.base.clone(transform), LogisticRegression(C=.3, max_iter=2000))
            estimator.fit(x.iloc[train], y[train])
            p[test] = estimator.predict_proba(x.iloc[test])[:, 1]
        weights = np.minimum(10, y.mean() / np.clip(p, .05, .95))
        selected = weights[y == 1]
        summaries[-1].update({'usable_label_propensity_auc': float(roc_auc_score(y, p)),
                             'propensity_below_0.05_n': int((p < .05).sum()),
                             'propensity_above_0.95_n': int((p > .95).sum()),
                             'selected_weight_ess': float(selected.sum() ** 2 / (selected ** 2).sum()),
                             'selected_weight_max': float(selected.max()),
                             'selected_weights_capped_n': int((weights[y == 1] == 10).sum())})
        propensity_rows.extend({'username': name, 'wave': wave, 'usable_label_propensity': float(prob),
                                'sensitivity_weight': float(weight)}
                               for name, prob, weight in zip(eligible.username, p, weights))
    return summaries, pd.DataFrame(balance), pd.DataFrame(propensity_rows)


def sensitivity(latest, p):
    """Scenario shifts, not identified corrections or confidence intervals."""
    labeled = latest.label.notna().to_numpy()
    valid = np.isfinite(p).all(axis=1)
    rows = []
    # Population here is eligible active telemetry users with predictions, not all employees.
    domain = valid
    n = int(domain.sum())
    if not n:
        return pd.DataFrame()
    for delta in [-np.log(2), 0., np.log(2)]:
        shifted = softmax(np.log(np.clip(p[domain], 1e-12, 1)) + delta * np.arange(4), axis=1)
        labels = latest.loc[domain, 'label'].to_numpy()
        known = np.isfinite(labels)
        shifted[known] = np.eye(4)[labels[known].astype(int) - 1]
        for k in range(4):
            count = int(((latest.label == k + 1).to_numpy() & domain).sum())
            unknown = int((domain & ~labeled).sum())
            rows.append({'delta': float(delta), 'level': k + 1, 'domain_n': n,
                         'scenario_share': float(shifted[:, k].mean()),
                         'no_assumption_lower': count / n,
                         'no_assumption_upper': (count + unknown) / n})
    return pd.DataFrame(rows)


def predictions(latest, p, fitted=None, gate=None):
    cols = ['username', 'wave', 'window_end', 'team', 'userlevel', 'responded',
            'self_selected_level', 'label_status', 'reports_no_ai_coding', 'ai_observed_days']
    output = latest[cols].reset_index(drop=True).copy()
    output['p_0_pct'] = np.nan
    for k in range(4):
        output[f'p_{k + 1}_conditional_pct'] = 100 * p[:, k]
    output['probability_target'] = 'survey_workflow_scope_1_to_4_conditional_on_AI_use'
    output['probability_status'] = 'exploratory_not_company_validated'
    output['predicted_level'] = np.nan
    output['candidate_level'] = np.nan
    output['candidate_probability_pct'] = np.nan
    output['entropy_normalized'] = np.nan
    output['status'] = 'insufficient_training_evidence'
    output['seen_in_training_wave'] = False
    valid = np.isfinite(p).all(axis=1)
    if fitted is not None:
        support = fitted.out_of_support(latest)
        output['seen_in_training_wave'] = latest.username.isin(fitted.training_users).to_numpy()
        output.loc[valid, 'candidate_level'] = p[valid].argmax(axis=1) + 1
        output.loc[valid, 'candidate_probability_pct'] = p[valid].max(axis=1) * 100
        output.loc[valid, 'entropy_normalized'] = -(p[valid] * np.log(np.clip(p[valid], 1e-12, 1))).sum(axis=1) / np.log(4)
        output.loc[valid, 'status'] = 'validation_gate_failed'
        if gate and gate['passed']:
            output.loc[valid, 'probability_status'] = 'respondent_temporal_gate_passed_population_transport_unverified'
            output.loc[valid, 'status'] = 'low_confidence'
            sorted_p = np.sort(p, axis=1)
            accept = valid & ~support & (sorted_p[:, -1] >= .65) & ((sorted_p[:, -1] - sorted_p[:, -2]) >= .15)
            output.loc[accept, 'status'] = 'provisional_estimate'
            output.loc[accept, 'predicted_level'] = output.loc[accept, 'candidate_level']
        output.loc[valid & support, 'status'] = 'out_of_training_support'
    output.loc[~latest.feature_complete.to_numpy(), 'status'] = 'incomplete_telemetry'
    zero = latest.feature_complete.to_numpy() & latest.ai_total.eq(0).to_numpy()
    output.loc[zero, 'status'] = 'no_recorded_AI_use_level_0_unidentified'
    return output


def run(manifest, out):
    frame, audit, cfg = prepare(manifest)
    if len(cfg['waves']) != 2:
        raise ValueError('This frozen temporal protocol requires exactly two waves')
    waves = sorted(cfg['waves'], key=lambda w: w['end'])
    if pd.Timestamp(waves[0]['survey_end']) >= pd.Timestamp(waves[1]['start']):
        raise ValueError('Training survey must finish before validation telemetry starts')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    frame.to_csv(out / 'prepared.csv', index=False)
    (out / 'input_audit.json').write_text(json.dumps(audit, indent=2))
    summaries, balance, propensity = selection_audit(frame)
    balance.to_csv(out / 'response_balance.csv', index=False)
    propensity.to_csv(out / 'label_propensity.csv', index=False)
    latest = frame.loc[frame.wave.eq(waves[1]['name'])].reset_index(drop=True)
    train = frame.loc[frame.wave.eq(waves[0]['name']) & frame.label.notna() & frame.eligible].reset_index(drop=True)
    report = {'scale': 'workflow-scope-v1', 'synthetic_only': bool(cfg.get('synthetic_only', False)),
              'probability_target': 'P(survey scope=k | telemetry, AI use, survey selection)',
              'level_0': 'not identified by supplied questions', 'selection': summaries,
              'features': AI, 'training_wave': waves[0]['name'], 'validation_wave': waves[1]['name'],
              'model': 'L2 multinomial logistic C=0.3, grouped OOF temperature calibration',
              'gate_thresholds': {'holdout_n': 80, 'per_class_n': 10, 'classwise_ece_max': .10,
                                  'class_recall_min': .35, 'brier_difference_upper_max': 0},
              'training_usable_label_counts': train.label.value_counts().sort_index().to_dict()}
    p = np.full((len(latest), 4), np.nan)
    fitted, gate = None, None
    try:
        oof, oof_prior, folds = nested_oof(train)
        report['training_nested_oof'] = {'model': metrics(train.label, oof), 'prior': metrics(train.label, oof_prior)}
        development = train[['username', 'wave', 'label']].copy()
        development['fold'] = folds
        for k in range(4):
            development[f'p_{k+1}'] = oof[:, k]
        development.to_csv(out / 'development_oof.csv', index=False)
        fitted = CalibratedModel().fit(train)
        report['temperature'] = fitted.temperature
        usable = latest.eligible.to_numpy()
        if usable.any():
            p[usable] = fitted.predict(latest.loc[usable])
        validate = usable & latest.label.notna().to_numpy()
        if validate.any():
            y = latest.loc[validate, 'label'].to_numpy(dtype=int)
            baseline = np.tile(fitted.prior, (len(y), 1))
            gate, calibration = release_gate(y, p[validate], baseline, latest.loc[validate, 'username'])
            calibration.to_csv(out / 'calibration.csv', index=False)
            report['temporal'] = {'model': metrics(y, p[validate]), 'prior': metrics(y, baseline)}
            seen = latest.username.isin(fitted.training_users).to_numpy()
            for label, mask in [('returning_respondents', validate & seen), ('new_respondents', validate & ~seen)]:
                report[label] = metrics(latest.loc[mask, 'label'], p[mask]) if mask.sum() >= 20 else {'n': int(mask.sum()), 'status': 'too_small'}
            if not propensity.empty:
                weight = latest[['username', 'wave']].merge(propensity, on=['username', 'wave'], how='left', validate='1:1').sensitivity_weight.to_numpy()
                weighted = validate & np.isfinite(weight)
                if weighted.any():
                    report['MAR_weighted_sensitivity'] = metrics(latest.loc[weighted, 'label'], p[weighted], weight[weighted])
            # Descriptive subgroup errors; no fitting/tuning to these results.
            subgroups = []
            for column in ['team', 'userlevel', 'style']:
                for value in latest[column].dropna().unique():
                    mask = validate & latest[column].eq(value).to_numpy()
                    if mask.sum() >= 20:
                        subgroups.append({'dimension': column, 'group': value, **metrics(latest.loc[mask, 'label'], p[mask])})
            report['subgroups_min_n_20'] = subgroups
            # Merging 3/4 is diagnostic; never claim the new scale was independently validated.
            merged = np.column_stack([p[validate, 0], p[validate, 1], p[validate, 2:].sum(axis=1)])
            merged_y = np.minimum(y, 3)
            report['merged_3_4_exploratory'] = {'accuracy': float((merged.argmax(axis=1) + 1 == merged_y).mean()),
                                               'n': len(y), 'requires_fresh_validation': True}
        else:
            gate = {'passed': False, 'reasons': ['no_usable_temporal_validation_labels']}
    except InsufficientEvidence as error:
        report['model_failure'] = str(error)
        gate = {'passed': False, 'reasons': ['insufficient_training_evidence']}
    report['gate'] = gate
    output = predictions(latest, p, fitted, gate)
    output.to_csv(out / 'developer_predictions.csv', index=False, float_format='%.6f')
    sensitivity(latest, p).to_csv(out / 'selection_sensitivity.csv', index=False)
    report['prediction_status_counts'] = output.status.value_counts().to_dict()
    report['runtime_versions'] = {lib: importlib.metadata.version(lib) for lib in ['numpy', 'pandas', 'scipy', 'scikit-learn', 'openpyxl']}
    report['manifest_sha256'] = hashlib.sha256(Path(manifest).read_bytes()).hexdigest()
    report['code_sha256'] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in Path(__file__).parent.glob('*.py')}
    (out / 'analysis.json').write_text(json.dumps(report, indent=2, allow_nan=False))
    text = ['# AI workflow scope analysis', '',
            '**SYNTHETIC SOFTWARE DEMONSTRATION ONLY**' if cfg.get('synthetic_only') else 'Local data analysis; survey-only reference outcomes.', '',
            'These are survey-response probabilities conditional on AI use. They do not measure verified skill, code quality, or performance.', '',
            f"Temporal validation gate: **{'passed' if gate and gate['passed'] else 'not passed'}**.",
            'A passing gate supports provisional estimates against respondents; calibration for nonrespondents remains unverified.', '',
            'Level 0 is unidentified. No recorded usage is not proof of nonuse. Missing probabilities are intentional.', '',
            '## Coverage and selection', '', '```json', json.dumps(summaries, indent=2), '```', '',
            '## Validation', '', '```json', json.dumps({k: report[k] for k in ['training_nested_oof', 'temporal', 'gate', 'model_failure'] if k in report}, indent=2), '```', '',
            '## Developer output', '', 'See developer_predictions.csv for every developer in the latest roster, including abstentions and separate survey selections.', '',
            '## Interpretation limits', '',
            'Bootstrap intervals resample held-out developers with fitted predictions fixed. They exclude refit uncertainty, survey error, and unobserved selection bias.', '',
            'Propensity weights assume selection depends on measured features. Exponential-tilt scenarios vary the unknown responses by an assumed factor of two per level; they do not repair bias.', '',
            'Token totals can reflect task complexity, repeated failed attempts, caching, or tooling. More usage is not evidence of higher skill.', '',
            'Treat failures as evidence that these inputs cannot distinguish the levels. Do not adjust thresholds after inspecting the holdout and call it independent validation.', '']
    (out / 'report.md').write_text('\n'.join(text))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    result = run(args.manifest, args.out)
    print('Completed local analysis. Gate passed:', bool(result['gate'] and result['gate']['passed']))

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analyze import predictions, run, sensitivity
from model import (CalibratedModel, InsufficientEvidence, features, metrics,
                   release_gate, splits, temperature_scale)
from prepare import AI, USAGE, number, prepare, survey_labels
from synthetic import generate


@pytest.fixture
def manifest(tmp_path):
    return generate(tmp_path / 'data', developers=400)


def edit_config(path, fn):
    cfg = json.loads(path.read_text())
    fn(cfg)
    path.write_text(json.dumps(cfg))


@pytest.mark.parametrize('value,unit,expected', [('1.2m', 'number', 1200000), ('2K', 'number', 2000),
                                                ('25%', 'percent', .25), ('25', 'percent', .25),
                                                ('.25', 'fraction', .25), ('$1,234.50', 'usd', 1234.5),
                                                ('1250', 'cents', 12.5)])
def test_numeric_units(value, unit, expected):
    assert number(value, unit) == expected


@pytest.mark.parametrize('value,unit', [('-1', 'number'), ('inf', 'number'), ('25%', 'fraction'), ('1.2', 'fraction'), ('oops', 'number')])
def test_bad_numeric_values_fail(value, unit):
    with pytest.raises(ValueError):
        number(value, unit)


def test_missing_is_not_zero():
    assert np.isnan(number(''))
    assert number('0') == 0


def test_labels_do_not_use_style_model_or_barriers():
    data = pd.DataFrame({'usage': list(USAGE), 'style': ['I delegate'] * 4,
                         'preference': ['Opus'] * 4, 'barriers': ['I need training'] * 4})
    assert survey_labels(data).label.tolist() == [1, 2, 3, 4]
    data.loc[2, 'preference'] = 'I don’t use AI for coding'
    mapped = survey_labels(data)
    assert np.isnan(mapped.loc[2, 'label'])
    assert mapped.loc[2, 'self_selected_level'] == 3
    assert mapped.loc[2, 'label_status'] == 'contradictory_coding_answers'
    assert np.isnan(survey_labels(pd.DataFrame({'usage': [''], 'preference': ['I don’t use AI for coding']})).label.iloc[0])


def test_prepare_keeps_company_roster_and_removes_medians(manifest):
    df, audit, _ = prepare(manifest)
    assert len(df) == 800
    assert audit['aggregate_rows_removed'] == 1
    assert df.responded.sum() == 400
    assert not df.username.eq('Global').any()


def test_snapshot_not_summed_over_days(manifest):
    path = manifest.parent / 'telemetry.csv'
    data = pd.read_csv(path)
    original = data.iloc[0].Total
    old = data.iloc[[0]].copy()
    old['date'] = '2026-03-30'
    old['Total'] = 1e12
    pd.concat([data, old]).to_csv(path, index=False)
    df, audit, _ = prepare(manifest)
    assert df.ai_total.iloc[0] == pytest.approx(original)
    assert audit['rows_outside_windows'] == 1


def test_duplicate_keys_fail(manifest):
    path = manifest.parent / 'telemetry.csv'
    data = pd.read_csv(path)
    pd.concat([data, data.iloc[[0]]]).to_csv(path, index=False)
    with pytest.raises(ValueError, match='Duplicate telemetry'):
        prepare(manifest)


def test_duplicate_surveys_fail(manifest):
    path = manifest.parent / 'survey.csv'
    data = pd.read_csv(path)
    pd.concat([data, data.iloc[[0]]]).to_csv(path, index=False)
    with pytest.raises(ValueError, match='duplicate survey'):
        prepare(manifest)


def test_ambiguous_grain_and_overlapping_sources_fail(manifest):
    edit_config(manifest, lambda c: c['telemetry'].append(c['telemetry'][0].copy()))
    with pytest.raises(ValueError, match='Overlapping metric'):
        prepare(manifest)


def test_future_survey_and_bad_coverage_fail(manifest):
    path = manifest.parent / 'survey.csv'
    data = pd.read_csv(path)
    data.loc[0, 'response_date'] = '2026-09-01'
    data.to_csv(path, index=False)
    with pytest.raises(ValueError, match='outside declared'):
        prepare(manifest)


def test_incomplete_coverage_abstains(manifest):
    path = manifest.parent / 'roster.csv'
    data = pd.read_csv(path)
    data.loc[400, 'ai_observed_days'] = 29
    data.to_csv(path, index=False)
    df, _, _ = prepare(manifest)
    row = df.loc[(df.wave == 'August') & (df.username == 'synthetic_0000')].reset_index(drop=True)
    result = predictions(row, np.full((1, 4), np.nan))
    assert result.status.iloc[0] == 'incomplete_telemetry'
    assert np.isnan(result.p_0_pct.iloc[0])


def test_zero_is_not_level_zero(manifest):
    frame, _, _ = prepare(manifest)
    row = frame.iloc[[0]].copy().reset_index(drop=True)
    row['ai_total'] = 0
    result = predictions(row, np.full((1, 4), np.nan))
    assert result.status.iloc[0] == 'no_recorded_AI_use_level_0_unidentified'
    assert np.isnan(result.predicted_level.iloc[0])


def test_feature_whitelist_ignores_survey_identity_context(manifest):
    frame, _, _ = prepare(manifest)
    a = features(frame)
    frame['label'] = 999
    frame['usage'] = 'invented'
    frame['team'] = 'anything'
    frame['total_spend'] = 1e12
    frame['mrs_merged'] = 1e12
    np.testing.assert_equal(a, features(frame))


def test_developer_group_separation():
    y = np.tile(np.repeat(np.arange(1, 5), 20), 2)
    groups = np.tile(np.arange(80), 2)
    for train, test in splits(y, groups):
        assert not set(groups[train]) & set(groups[test])


def test_missing_class_fails(manifest):
    frame, _, _ = prepare(manifest)
    frame = frame.loc[frame.label.isin([1, 2, 3]) & frame.eligible]
    with pytest.raises(InsufficientEvidence):
        CalibratedModel().fit(frame)


def test_probability_simplex():
    p = temperature_scale(np.array([[.1, .2, .3, .4], [.01, .01, .01, .97]]), 2)
    np.testing.assert_allclose(p.sum(axis=1), 1)
    assert (p >= 0).all() and (p <= 1).all()


def test_no_signal_prior_fails_release_gate():
    y = np.tile(np.arange(1, 5), 40)
    p = np.full((160, 4), .25)
    gate, _ = release_gate(y, p, p, np.arange(160))
    assert not gate['passed']
    assert 'no_clear_brier_improvement_over_prior' in gate['reasons']
    assert metrics(y, p)['brier'] == .75


def test_csv_and_xlsx_equivalent(tmp_path):
    csv, _, _ = prepare(generate(tmp_path / 'csv', developers=40))
    xlsx, _, _ = prepare(generate(tmp_path / 'xlsx', developers=40, spreadsheet=True))
    np.testing.assert_allclose(csv[AI], xlsx[AI])


def test_end_to_end_and_holdout_label_independence(manifest, tmp_path):
    report = run(manifest, tmp_path / 'out1')
    a = pd.read_csv(tmp_path / 'out1' / 'developer_predictions.csv')
    assert len(a) == 400
    probability_cols = [f'p_{k}_conditional_pct' for k in range(1, 5)]
    np.testing.assert_allclose(a[probability_cols].sum(axis=1), 100, atol=1e-5)
    assert a.p_0_pct.isna().all()
    assert 'temporal' in report
    path = manifest.parent / 'survey.csv'
    data = pd.read_csv(path)
    data.loc[data.wave.eq('August'), 'usage'] = list(USAGE)[0]
    data.to_csv(path, index=False)
    run(manifest, tmp_path / 'out2')
    b = pd.read_csv(tmp_path / 'out2' / 'developer_predictions.csv')
    # Holdout changes metrics/gates, never feature probabilities or fitted temperature.
    np.testing.assert_allclose(a[probability_cols], b[probability_cols])
    assert b.predicted_level.isna().all()


def test_small_data_emits_all_rows_without_fabricated_probabilities(tmp_path):
    path = generate(tmp_path / 'small', developers=40)
    report = run(path, tmp_path / 'out')
    result = pd.read_csv(tmp_path / 'out' / 'developer_predictions.csv')
    assert len(result) == 40
    assert result.p_1_conditional_pct.isna().all()
    assert not report['gate']['passed']


@pytest.mark.parametrize('grain', ['daily', 'session'])
def test_event_totals_missing_values_and_absent_zeros(manifest, grain):
    rows = [dict(username='synthetic_0000', date='2026-03-02', session_id='a', Total=100),
            dict(username='synthetic_0000', date='2026-03-03', session_id='b', Total=200),
            dict(username='synthetic_0001', date='2026-03-02', session_id='c', Total=100),
            dict(username='synthetic_0001', date='2026-03-03', session_id='d', Total='')]
    pd.DataFrame(rows).to_csv(manifest.parent / 'events.csv', index=False)
    edit_config(manifest, lambda c: c.update(telemetry=[{'path': 'events.csv', 'grain': grain,
                'individual_only': True, 'absent_means_zero': True, 'metrics': {'ai_total': {'column': 'Total'}}}]))
    frame, _, _ = prepare(manifest)
    assert frame.ai_total.iloc[0] == 300
    assert frame.ai_active_days.iloc[0] == 2
    assert np.isnan(frame.ai_total.iloc[1])
    assert np.isnan(frame.ai_active_days.iloc[1])
    assert frame.ai_total.iloc[2] == 0
    if grain == 'session':
        assert frame.ai_sessions.iloc[0] == 2
    else:
        assert frame.ai_sessions.isna().all()
    # Missing event rows without audited full coverage remain unknown.
    path = manifest.parent / 'roster.csv'
    roster = pd.read_csv(path)
    roster.loc[2, 'ai_observed_days'] = 0
    roster.to_csv(path, index=False)
    assert np.isnan(prepare(manifest)[0].ai_total.iloc[2])


def test_duplicate_session_id_on_different_dates_fails(manifest):
    pd.DataFrame([dict(username='synthetic_0000', date=d, session_id='same', Total=100)
                  for d in ['2026-03-02', '2026-03-03']]).to_csv(manifest.parent / 'events.csv', index=False)
    edit_config(manifest, lambda c: c.update(telemetry=[{'path': 'events.csv', 'grain': 'session',
                'individual_only': True, 'metrics': {'ai_total': {'column': 'Total'}}}]))
    with pytest.raises(ValueError, match='Duplicate telemetry'):
        prepare(manifest)


def test_unknown_identity_needs_explicit_alias(manifest):
    path = manifest.parent / 'telemetry.csv'
    data = pd.read_csv(path)
    data.loc[data.username.eq('synthetic_0000'), 'username'] = 'tool_alias'
    data.to_csv(path, index=False)
    with pytest.raises(ValueError, match='Unmatched telemetry'):
        prepare(manifest)
    pd.DataFrame({'alias': ['tool_alias'], 'username': ['synthetic_0000']}).to_csv(manifest.parent / 'aliases.csv', index=False)
    edit_config(manifest, lambda c: c.update(aliases={'path': 'aliases.csv'}))
    assert len(prepare(manifest)[0]) == 800


def test_later_telemetry_cannot_change_training_features(manifest):
    before, _, _ = prepare(manifest)
    path = manifest.parent / 'telemetry.csv'
    data = pd.read_csv(path)
    data.loc[data.date.eq('2026-07-31'), ['Input', 'Output', 'Total']] *= 100
    data.to_csv(path, index=False)
    after, _, _ = prepare(manifest)
    np.testing.assert_allclose(features(before.loc[before.wave.eq('April')]), features(after.loc[after.wave.eq('April')]), rtol=1e-12)


def test_out_of_support_and_individual_confidence_gate(manifest):
    frame, _, _ = prepare(manifest)
    training = frame.loc[frame.wave.eq('April') & frame.label.notna()]
    fitted = CalibratedModel().fit(training)
    row = training.iloc[[0]].copy().reset_index(drop=True)
    p = np.array([[.9, .04, .03, .03]])
    assert predictions(row, p, fitted, {'passed': True}).predicted_level.iloc[0] == 1
    row['ai_total'] = training.ai_total.max() * 100
    output = predictions(row, p, fitted, {'passed': True})
    assert output.status.iloc[0] == 'out_of_training_support'
    assert np.isnan(output.predicted_level.iloc[0])


def test_no_signal_full_pipeline_does_not_release_levels(tmp_path):
    manifest = generate(tmp_path / 'null_data', developers=400, signal=False)
    report = run(manifest, tmp_path / 'null_out')
    assert not report['gate']['passed']
    output = pd.read_csv(tmp_path / 'null_out' / 'developer_predictions.csv')
    assert output.predicted_level.isna().all()


def test_selection_scenarios_are_normalized_and_bounds_hold(manifest):
    frame, _, _ = prepare(manifest)
    latest = frame.loc[frame.wave.eq('August')].reset_index(drop=True)
    result = sensitivity(latest, np.full((len(latest), 4), .25))
    np.testing.assert_allclose(result.groupby('delta').scenario_share.sum(), 1)
    assert (result.scenario_share >= result.no_assumption_lower).all()
    assert (result.scenario_share <= result.no_assumption_upper).all()


def test_snapshot_with_only_total_tokens_still_fits(manifest):
    edit_config(manifest, lambda c: c['telemetry'][0].update(metrics={'ai_total': {'column': 'Total'}}))
    frame, _, _ = prepare(manifest)
    train = frame.loc[frame.wave.eq('April') & frame.label.notna()]
    fitted = CalibratedModel().fit(train)
    p = fitted.predict(frame.loc[frame.wave.eq('August')])
    np.testing.assert_allclose(p.sum(axis=1), 1)


def test_low_confidence_abstention_preserves_probabilities(manifest):
    frame, _, _ = prepare(manifest)
    train = frame.loc[frame.wave.eq('April') & frame.label.notna()]
    fitted = CalibratedModel().fit(train)
    row = train.iloc[[0]].reset_index(drop=True)
    p = np.array([[.4, .3, .2, .1]])
    result = predictions(row, p, fitted, {'passed': True})
    assert result.status.iloc[0] == 'low_confidence'
    assert np.isnan(result.predicted_level.iloc[0])
    assert result.p_1_conditional_pct.iloc[0] == 40

"""Strict local ingestion. No inference of identity, grain, units, or missing zeros."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

AI = ['ai_input', 'ai_output', 'ai_total', 'ai_sessions', 'ai_active_days']
CONTEXT = ['mrs_merged', 'loc_changed', 'avg_mr_size', 'mrs_commented',
           'mrs_reviewed', 'issues', 'feature_share', 'epic_share', 'spike_share',
           'klon_share', 'small_share', 'claude_spend', 'cursor_spend',
           'total_spend', 'cursor_share']
USAGE = {
    'I use AI for small tasks (snippets, quick questions)': 1,
    'I use AI for larger tasks (debugging, writing tests, refactoring)': 2,
    'I use AI across multiple steps in a workflow (code + tools + validation)': 3,
    'I use AI agents/automation to complete workflows end-to-end (with human review)': 4,
}


def number(value, unit='number'):
    if pd.isna(value) or str(value).strip().lower() in {'', 'na', 'n/a', 'null', '-'}:
        return np.nan
    s = str(value).strip().lower().replace(',', '')
    if s.startswith('$'):
        if unit != 'usd':
            raise ValueError('Dollar value requires usd unit')
        s = s[1:]
    percent = s.endswith('%')
    if percent:
        if unit != 'percent':
            raise ValueError('Percent value requires percent unit')
        s = s[:-1]
    match = re.fullmatch(r'(\d+(?:\.\d*)?|\.\d+)([km]?)', s)
    if not match:
        raise ValueError('Invalid nonnegative numeric value')
    result = float(match[1]) * {'': 1, 'k': 1000, 'm': 1000000}[match[2]]
    if unit == 'percent':
        result /= 100
    elif unit == 'cents':
        result /= 100
    elif unit not in {'number', 'fraction', 'usd'}:
        raise ValueError('Unknown unit')
    if not np.isfinite(result) or (unit in {'fraction', 'percent'} and result > 1):
        raise ValueError('Numeric value outside allowed range')
    return result


def read_table(base, spec):
    path = (base / spec['path']).resolve()
    ext = path.suffix.lower()
    if ext in {'.xlsx', '.xls'}:
        if 'sheet' not in spec:
            raise ValueError('Spreadsheet sources require an explicit sheet')
        df = pd.read_excel(path, sheet_name=spec['sheet'], dtype=str)
    elif ext in {'.csv', '.tsv'}:
        df = pd.read_csv(path, sep='\t' if ext == '.tsv' else ',', dtype=str,
                         keep_default_na=False)
    else:
        raise ValueError('Only CSV, TSV, XLSX, XLS supported')
    columns = spec.get('columns', {})  # canonical name -> export header
    missing = set(columns.values()) - set(df.columns)
    if missing:
        raise ValueError('Mapped columns are absent from an input')
    df = df.rename(columns={v: k for k, v in columns.items()})
    if df.columns.duplicated().any():
        raise ValueError('Column mapping creates duplicate names')
    return df


def require(df, columns, name):
    if set(columns) - set(df.columns):
        raise ValueError(f'{name}: missing required canonical columns: {set(columns) - set(df.columns)}')


def identities(df, aliases):
    require(df, ['username'], 'identity')
    df = df.copy()
    df['username'] = df.username.astype(str).str.strip().replace(aliases)
    if df.username.isin(['', 'nan', 'None']).any():
        raise ValueError('Blank identity')
    return df


def boolean(series):
    values = series.astype(str).str.lower().str.strip()
    if not values.isin(['true', 'false', '1', '0']).all():
        raise ValueError('Boolean fields must contain true/false or 1/0')
    return values.isin(['true', '1'])


def day(series):
    return pd.to_datetime(series, errors='raise', utc=True).dt.tz_convert(None).dt.normalize()


def survey_labels(survey):
    survey = survey.copy()
    for c in ['usage', 'style', 'preference', 'barriers']:
        if c not in survey:
            survey[c] = ''
        survey[c] = survey[c].fillna('').str.strip()
    # Never turn model preference, steering style, or barriers into level labels.
    survey['self_selected_level'] = survey.usage.map(USAGE)
    survey['label_status'] = np.where(survey.usage.eq(''), 'missing_usage',
                                     np.where(survey.self_selected_level.isna(), 'unmapped_usage', 'mapped'))
    no_coding = survey.preference.str.replace('’', "'", regex=False).eq("I don't use AI for coding")
    conflict = no_coding & survey.self_selected_level.ge(2)
    survey.loc[conflict, 'label_status'] = 'contradictory_coding_answers'
    survey['label'] = survey.self_selected_level.where(survey.label_status.eq('mapped'))
    survey['reports_no_ai_coding'] = no_coding
    return survey


def prepare(manifest_path):
    manifest_path = Path(manifest_path).resolve()
    base = manifest_path.parent
    cfg = json.loads(manifest_path.read_text())
    waves = cfg['waves']
    if not waves or len({w['name'] for w in waves}) != len(waves):
        raise ValueError('Wave names must be unique and nonempty')
    for w in waves:
        start, end = pd.Timestamp(w['start']), pd.Timestamp(w['end'])
        if (end - start).days != 29 or not start <= end < pd.Timestamp(w['survey_start']) <= pd.Timestamp(w['survey_end']):
            raise ValueError('Use 30 inclusive telemetry days ending before survey opens')
    aliases = {}
    if 'aliases' in cfg:
        mapping = read_table(base, cfg['aliases'])
        require(mapping, ['alias', 'username'], 'aliases')
        mapping['alias'] = mapping.alias.fillna('').str.strip()
        mapping['username'] = mapping.username.fillna('').str.strip()
        if mapping[['alias', 'username']].eq('').any().any():
            raise ValueError('Blank alias mapping')
        if mapping.alias.duplicated().any():
            raise ValueError('Ambiguous alias mapping')
        aliases = dict(zip(mapping.alias.str.strip(), mapping.username.str.strip()))
    roster = identities(read_table(base, cfg['roster']), aliases)
    require(roster, ['wave', 'team', 'userlevel', 'invited', 'ai_observed_days'], 'roster')
    roster = roster[['username', 'wave', 'team', 'userlevel', 'invited', 'ai_observed_days']].copy()
    roster['invited'] = boolean(roster.invited)
    roster['ai_observed_days'] = roster.ai_observed_days.map(number)
    if roster.ai_observed_days.isna().any() or not roster.ai_observed_days.between(0, 30).all() or (roster.ai_observed_days % 1 != 0).any():
        raise ValueError('ai_observed_days must be an audited integer from 0 to 30')
    if roster.duplicated(['username', 'wave']).any():
        raise ValueError('Roster has duplicate developer/wave keys')
    if set(roster.wave) != {w['name'] for w in waves}:
        raise ValueError('Roster and manifest waves must match exactly')
    survey = identities(read_table(base, cfg['survey']), aliases)
    require(survey, ['wave', 'response_date', 'usage'], 'survey')
    if survey.duplicated(['username', 'wave']).any():
        raise ValueError('Resolve duplicate survey submissions explicitly before analysis')
    survey['response_date'] = day(survey.response_date)
    survey = survey_labels(survey)
    checked = survey.merge(roster[['username', 'wave', 'invited']], on=['username', 'wave'], how='left', validate='1:1')
    if checked.invited.isna().any() or not checked.invited.all():
        raise ValueError('Survey contains unmatched or uninvited developers')
    for w in waves:
        dates = survey.loc[survey.wave.eq(w['name']), 'response_date']
        if not dates.between(w['survey_start'], w['survey_end']).all():
            raise ValueError('Survey response outside declared collection period')
    result = roster.copy()
    for c in AI + CONTEXT:
        result[c] = np.nan
    assigned = set()
    audit = {'schema_version': 1, 'aggregate_rows_removed': 0, 'sources': [],
             'rows_outside_windows': 0}
    for spec in cfg['telemetry']:
        df = read_table(base, spec)
        require(df, ['username', 'date'], 'telemetry')
        if 'ordering' in df:
            ordering = pd.to_numeric(df.ordering, errors='raise')
            if not ordering.isin([0, 1, 2, 3]).all():
                raise ValueError('Unknown row ordering type')
            audit['aggregate_rows_removed'] += int(ordering.ne(3).sum())
            df = df.loc[ordering.eq(3)].copy()
        elif spec.get('individual_only') is not True:
            raise ValueError('Declare individual_only or supply ordering')
        df = identities(df, aliases)
        df['date'] = day(df.date)
        if not set(df.username).issubset(set(roster.username)):
            raise ValueError('Unmatched telemetry identity; resolve using alias map')
        grain = spec['grain']
        if grain not in {'daily', 'session', 'snapshot'}:
            raise ValueError('Unsupported grain')
        keys = ['username', 'date']
        if grain == 'session':
            require(df, ['session_id'], 'session')
            keys = ['username', 'session_id']
            if df.session_id.fillna('').eq('').any():
                raise ValueError('Session IDs cannot be blank')
        if df.duplicated(keys).any():
            raise ValueError('Duplicate telemetry keys: pre-aggregate tool rows or resolve duplicates')
        metrics = spec['metrics']
        if set(metrics) - set(AI + CONTEXT):
            raise ValueError('Unknown canonical metric')
        if grain != 'snapshot' and set(metrics) & set(CONTEXT):
            raise ValueError('Activity/spend context requires a separate 30-day snapshot')
        if grain != 'snapshot' and set(metrics) & {'ai_sessions', 'ai_active_days'}:
            raise ValueError('Event counts are derived, not mapped')
        derived = {'ai_active_days'} if grain != 'snapshot' and 'ai_total' in metrics else set()
        if grain == 'session' and 'ai_total' in metrics:
            derived.add('ai_sessions')
        if assigned & (set(metrics) | derived):
            raise ValueError('Overlapping metric sources would double count; supply one authoritative source')
        assigned |= set(metrics) | derived
        for c, definition in metrics.items():
            require(df, [definition['column']], 'metric')
        parsed = {c: df[definition['column']].map(lambda v: number(v, definition.get('unit', 'number')))
                  for c, definition in metrics.items()}
        for c, values in parsed.items():
            if c.endswith('_share') and not values.dropna().between(0, 1).all():
                raise ValueError('Share metric must be a fraction from 0 to 1 after unit conversion')
            if c in {'ai_active_days', 'ai_sessions', 'mrs_merged', 'mrs_commented', 'mrs_reviewed', 'issues'}:
                if (values.dropna() % 1 != 0).any():
                    raise ValueError('Count metric must contain integers')
            df[c] = values
        used = pd.Series(False, index=df.index)
        for w in waves:
            in_wave = result.wave.eq(w['name'])
            if grain == 'snapshot':
                if spec.get('window_days') != 30:
                    raise ValueError('Rolling snapshots must explicitly cover 30 days')
                select = df.date.eq(pd.Timestamp(w['end']))
            else:
                select = df.date.between(w['start'], w['end'])
            used |= select
            part = df.loc[select]
            allowed = set(result.loc[in_wave, 'username'])
            if not set(part.username).issubset(allowed):
                raise ValueError('Telemetry user is not in the roster for that wave')
            if grain == 'snapshot':
                agg = part.set_index('username')[list(metrics)].copy()
            else:
                agg = part.groupby('username')[list(metrics)].sum(min_count=1)
                # An unknown event value makes its window total unknown, not a partial sum.
                for c in metrics:
                    bad = part.groupby('username')[c].apply(lambda s: s.isna().any())
                    agg.loc[bad[bad].index, c] = np.nan
                if derived:
                    positive = part.loc[part.ai_total.gt(0)]
                    agg['ai_active_days'] = positive.groupby('username').date.nunique().reindex(agg.index, fill_value=0)
                    if 'ai_sessions' in derived:
                        agg['ai_sessions'] = positive.groupby('username').size().reindex(agg.index, fill_value=0)
                    unknown = part.groupby('username').ai_total.apply(lambda s: s.isna().any())
                    agg.loc[unknown[unknown].index, list(derived)] = np.nan
            for c in list(metrics) + list(derived):
                values = result.loc[in_wave, 'username'].map(agg[c])
                # Zero fill only absent event rows with independently complete capture.
                absent = ~result.loc[in_wave, 'username'].isin(agg.index)
                if grain != 'snapshot' and spec.get('absent_means_zero') is True:
                    values.loc[absent & result.loc[in_wave, 'ai_observed_days'].eq(30)] = 0
                result.loc[in_wave, c] = values
        audit['rows_outside_windows'] += int((~used).sum())
    require(result, ['ai_total'], 'prepared')
    if 'ai_total' not in assigned:
        raise ValueError('An authoritative ai_total metric is required')
    if (result.ai_active_days > result.ai_observed_days).any():
        raise ValueError('AI active days exceed audited observation coverage')
    both = result[['ai_input', 'ai_output', 'ai_total']].notna().all(axis=1)
    # Formatted k/m exports are rounded; permit 2% reconciliation tolerance.
    if (result.loc[both, 'ai_total'] * 1.02 + 1 < result.loc[both, 'ai_input'] + result.loc[both, 'ai_output']).any():
        raise ValueError('Total tokens cannot be smaller than input plus output')
    result = result.merge(survey[['username', 'wave', 'response_date', 'usage', 'style',
                                 'preference', 'barriers', 'self_selected_level', 'label',
                                 'label_status', 'reports_no_ai_coding']],
                          on=['username', 'wave'], how='left', validate='1:1')
    result['responded'] = result.response_date.notna()
    result['label_status'] = result.label_status.fillna('not_responded')
    result['feature_complete'] = result.ai_observed_days.eq(30) & result.ai_total.notna()
    # Positive recorded use is a deployment-domain requirement, not a level label.
    result['eligible'] = result.feature_complete & result.ai_total.gt(0)
    result['window_end'] = result.wave.map({w['name']: w['end'] for w in waves})
    for spec in [cfg['roster'], cfg['survey']] + cfg['telemetry'] + ([cfg['aliases']] if 'aliases' in cfg else []):
        path = base / spec['path']
        audit['sources'].append({'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    audit.update({'roster_rows': len(result), 'responded': int(result.responded.sum()),
                  'usable_labels': int((result.label.notna() & result.eligible).sum()),
                  'label_status_counts': result.label_status.value_counts().to_dict()})
    return result, audit, cfg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    frame, audit, _ = prepare(args.manifest)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    frame.to_csv(out / 'prepared.csv', index=False)
    (out / 'audit.json').write_text(json.dumps(audit, indent=2))
    print(f'Prepared {len(frame)} developer/wave rows.')

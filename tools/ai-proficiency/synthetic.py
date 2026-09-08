"""Generate invented data for software tests only, never empirical validation."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from prepare import USAGE


def generate(out, developers=400, seed=17, signal=True, spreadsheet=False):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    rng = np.random.default_rng(seed)
    roster, telemetry, survey = [], [], []
    waves = [dict(name='April', start='2026-03-02', end='2026-03-31', survey_start='2026-04-01', survey_end='2026-04-10'),
             dict(name='August', start='2026-07-02', end='2026-07-31', survey_start='2026-08-01', survey_end='2026-08-10')]
    answers = list(USAGE)
    for wave_idx, wave in enumerate(waves):
        for i in range(developers):
            name = f'synthetic_{i:04d}'
            level = i % 4 + 1
            roster.append(dict(username=name, wave=wave['name'], team=f'team_{i % 5}', userlevel='Developer',
                               invited=True, ai_observed_days=30))
            scale = level if signal else rng.integers(1, 5)
            tokens = float(np.exp(7 + scale * 1.2 + rng.normal(0, .3)))
            telemetry.append(dict(username=name, date=wave['end'], ordering=3,
                                  Input=tokens * .4, Output=tokens * .1, Total=tokens,
                                  active_days=min(30, scale * 6 + rng.integers(0, 3)),
                                  sessions=scale * 20 + rng.integers(0, 5), MRs=rng.integers(0, 20)))
            # Exactly half respond, with overlap and newcomers across waves; all classes represented.
            responds = (i // 4 + wave_idx) % 4 < 2
            if responds:
                noisy_level = level if rng.random() > .05 else int(rng.integers(1, 5))
                survey.append(dict(username=name, wave=wave['name'], response_date=wave['survey_start'],
                                   usage=answers[noisy_level - 1], style='A mix', preference='No strong preference', barriers=''))
    telemetry.append(dict(username='Global', date=waves[0]['end'], ordering=0, Input=0, Output=0, Total=0, active_days=0, sessions=0, MRs=0))
    pd.DataFrame(roster).to_csv(out / 'roster.csv', index=False)
    pd.DataFrame(survey).to_csv(out / 'survey.csv', index=False)
    data = pd.DataFrame(telemetry)
    file = 'telemetry.xlsx' if spreadsheet else 'telemetry.csv'
    if spreadsheet:
        data.to_excel(out / file, sheet_name='Export', index=False)
    else:
        data.to_csv(out / file, index=False)
    spec = {'path': file, 'grain': 'snapshot', 'window_days': 30,
            'metrics': {'ai_input': {'column': 'Input'}, 'ai_output': {'column': 'Output'},
                        'ai_total': {'column': 'Total'}, 'ai_active_days': {'column': 'active_days'},
                        'ai_sessions': {'column': 'sessions'}, 'mrs_merged': {'column': 'MRs'}}}
    if spreadsheet:
        spec['sheet'] = 'Export'
    cfg = {'synthetic_only': True, 'waves': waves, 'roster': {'path': 'roster.csv'},
           'survey': {'path': 'survey.csv'}, 'telemetry': [spec]}
    (out / 'manifest.json').write_text(json.dumps(cfg, indent=2))
    return out / 'manifest.json'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    parser.add_argument('--developers', type=int, default=400)
    parser.add_argument('--no-signal', action='store_true')
    parser.add_argument('--xlsx', action='store_true')
    args = parser.parse_args()
    generate(args.out, args.developers, signal=not args.no_signal, spreadsheet=args.xlsx)
    print('Created SYNTHETIC fixtures. These cannot validate company proficiency.')

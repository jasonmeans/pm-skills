"""Bootstrap and operate the local analysis package. Entry point needs only stdlib."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid
import venv

PACKAGE = Path(__file__).resolve().parent


def environment_python(directory):
    return Path(directory) / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def ensure_environment(directory):
    if sys.version_info[:2] not in {(3, 11), (3, 12)}:
        raise ValueError('Run workflow.py with Python 3.11 or 3.12.')
    directory = Path(directory).resolve()
    interpreter = environment_python(directory)
    if not interpreter.exists():
        if directory.exists():
            raise ValueError('Existing environment path is incomplete; choose a new --venv path.')
        venv.EnvBuilder(with_pip=True).create(directory)
    requirement_file = PACKAGE / 'requirements.txt'
    digest = hashlib.sha256(requirement_file.read_bytes()).hexdigest()
    marker = directory / '.ai-proficiency-requirements'
    # Verify versions too: a marker alone cannot detect later environment changes.
    probe = subprocess.run([str(interpreter), '-c',
        'import importlib.metadata as m, sys; from packaging.requirements import Requirement; '
        'reqs=[Requirement(s.strip()) for s in open(sys.argv[1]) if s.strip()]; '
        'assert all(m.version(r.name) in r.specifier for r in reqs)', str(requirement_file)],
        capture_output=True, text=True)
    if probe.returncode or not marker.exists() or marker.read_text() != digest:
        subprocess.run([str(interpreter), '-m', 'pip', 'install', '--disable-pip-version-check',
                        '-r', str(requirement_file)], check=True)
        marker.write_text(digest)
    return interpreter


def inventory(path):
    import pandas as pd
    path = Path(path).resolve()
    if not path.exists():
        raise ValueError('Input path does not exist')
    files = sorted(path.iterdir()) if path.is_dir() else [path]
    result = []
    for file in files:
        suffix = file.suffix.lower()
        if not file.is_file() or file.name.startswith('~$') or suffix not in {'.csv', '.tsv', '.xlsx', '.xls'}:
            continue
        if suffix in {'.csv', '.tsv'}:
            sep = '\t' if suffix == '.tsv' else ','
            columns = list(pd.read_csv(file, sep=sep, nrows=0).columns)
            rows = sum(len(chunk) for chunk in pd.read_csv(file, sep=sep, usecols=[0], chunksize=50000))
            result.append({'file': str(file), 'columns': columns, 'rows': rows})
        else:
            with pd.ExcelFile(file) as book:
                for sheet in book.sheet_names:
                    columns = list(pd.read_excel(book, sheet_name=sheet, nrows=0).columns)
                    rows = len(pd.read_excel(book, sheet_name=sheet, usecols=[0])) if columns else 0
                    result.append({'file': str(file), 'sheet': sheet, 'columns': columns, 'rows': rows})
    if not result:
        raise ValueError('No CSV, TSV, XLSX, or XLS inputs found directly inside this path')
    return result


def new_run_path(base):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    return Path(base).resolve() / 'ai-proficiency-runs' / f'{stamp}-{uuid.uuid4().hex[:8]}'


def verify_outputs(out, expected_users):
    import numpy as np
    import pandas as pd
    probability_columns = [f'p_{k}_conditional_pct' for k in range(1, 5)]
    result = pd.read_csv(Path(out) / 'developer_predictions.csv', dtype={'username': str},
                         keep_default_na=False,
                         na_values={c: [''] for c in probability_columns + ['p_0_pct', 'predicted_level']})
    if result.username.duplicated().any() or set(result.username) != set(expected_users):
        raise ValueError('Output does not match the complete latest developer roster')
    p = result[probability_columns].to_numpy(dtype=float)
    missing = np.isnan(p)
    if (missing.any(axis=1) != missing.all(axis=1)).any():
        raise ValueError('Partial probability distribution in output')
    known = p[~missing.any(axis=1)]
    if not np.isfinite(known).all() or ((known < 0) | (known > 100)).any() or not np.allclose(known.sum(axis=1), 100, atol=1e-5, rtol=0):
        raise ValueError('Invalid conditional probability distribution in output')
    if result.p_0_pct.notna().any():
        raise ValueError('Output asserts an unidentified Level 0 probability')
    if (result.predicted_level.notna() & ~result.status.eq('provisional_estimate')).any():
        raise ValueError('A released level violates its abstention status')
    released = result.predicted_level.notna().to_numpy()
    if missing[released].any() or not result.loc[released, 'predicted_level'].isin([1, 2, 3, 4]).all():
        raise ValueError('A released level lacks a supported probability distribution')
    return len(result)


def execute_analysis(manifest, out=None):
    from analyze import run
    from prepare import prepare
    manifest = Path(manifest).resolve()
    # Preflight completes before creating a results directory.
    frame, _, cfg = prepare(manifest)
    destination = Path(out).resolve() if out else new_run_path(manifest.parent)
    if destination.exists():
        raise ValueError('Output directory already exists; use a new run directory')
    report = run(manifest, destination)
    latest_wave = max(cfg['waves'], key=lambda w: w['end'])['name']
    count = verify_outputs(destination, frame.loc[frame.wave.eq(latest_wave), 'username'])
    (destination / 'run-complete.json').write_text(json.dumps({
        'verified_developer_rows': count, 'manifest': str(manifest),
        'completed_utc': datetime.now(timezone.utc).isoformat(),
        'synthetic_only': report['synthetic_only'], 'gate_passed': report['gate']['passed']}, indent=2))
    print(json.dumps({'out': str(destination), 'developer_rows': count,
                      'synthetic_only': report['synthetic_only'], 'gate_passed': report['gate']['passed'],
                      'status_counts': report['prediction_status_counts']}, indent=2))
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--venv', type=Path, default=PACKAGE / '.venv', help='Isolated environment directory')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('setup', help='Install dependencies and run the test suite')
    inspect = sub.add_parser('inspect', help='Show local input schemas without row values')
    inspect.add_argument('path')
    run = sub.add_parser('run', help='Preflight, analyze, and verify a manifest')
    run.add_argument('--manifest', required=True)
    run.add_argument('--out')
    demo = sub.add_parser('demo', help='Run an invented-data demonstration')
    demo.add_argument('--out', help='New directory for synthetic inputs and results')
    args = parser.parse_args()
    # Re-enter this script under its managed interpreter before importing data libraries.
    interpreter = ensure_environment(args.venv)
    if Path(sys.prefix).resolve() != args.venv.resolve():
        completed = subprocess.run([str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])
        return completed.returncode
    if args.command == 'setup':
        subprocess.run([str(interpreter), '-m', 'pytest', str(PACKAGE / 'tests'), '-q'], check=True)
        print('Setup and tests complete:', interpreter)
    elif args.command == 'inspect':
        print(json.dumps(inventory(args.path), indent=2))
    elif args.command == 'run':
        execute_analysis(args.manifest, args.out)
    elif args.command == 'demo':
        from synthetic import generate
        root = Path(args.out).resolve() if args.out else new_run_path(PACKAGE / 'demo')
        root.mkdir(parents=True, exist_ok=False)
        manifest = generate(root / 'inputs', spreadsheet=True)
        execute_analysis(manifest, root / 'results')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f'Workflow stopped: {error}', file=sys.stderr)
        raise SystemExit(1)

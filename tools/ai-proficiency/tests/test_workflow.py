import json
import hashlib
from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from synthetic import generate
from workflow import execute_analysis, inventory, new_run_path, verify_outputs


def test_ready_environment_does_not_reinstall_dependencies(tmp_path, monkeypatch):
    import workflow
    original_run = workflow.subprocess.run
    monkeypatch.setattr(workflow, 'environment_python', lambda directory: Path(sys.executable))
    digest = hashlib.sha256((workflow.PACKAGE / 'requirements.txt').read_bytes()).hexdigest()
    (tmp_path / '.ai-proficiency-requirements').write_text(digest)

    def no_pip(command, **kwargs):
        assert 'pip' not in command, 'A ready environment must not reinstall packages'
        return original_run(command, **kwargs)

    monkeypatch.setattr(workflow.subprocess, 'run', no_pip)
    assert workflow.ensure_environment(tmp_path) == Path(sys.executable)


def test_inventory_lists_sheets_and_csv_without_row_values(tmp_path):
    pd.DataFrame({'username': ['private_example'], 'Total': [12345]}).to_csv(tmp_path / 'events.csv', index=False)
    with pd.ExcelWriter(tmp_path / 'survey.xlsx') as writer:
        pd.DataFrame({'usage': ['private_answer']}).to_excel(writer, sheet_name='April', index=False)
        pd.DataFrame({'usage': ['a', 'b']}).to_excel(writer, sheet_name='August', index=False)
    result = inventory(tmp_path)
    assert len(result) == 3
    assert [r['rows'] for r in result] == [1, 1, 2]
    assert 'private_example' not in json.dumps(result)
    assert 'private_answer' not in json.dumps(result)
    assert result[0]['columns'] == ['username', 'Total']


def test_inventory_empty_folder_has_actionable_error(tmp_path):
    with pytest.raises(ValueError, match='No CSV'):
        inventory(tmp_path)


def test_timestamped_paths_are_unique(tmp_path):
    assert new_run_path(tmp_path) != new_run_path(tmp_path)


def test_workflow_outputs_completion_only_after_verification(tmp_path):
    manifest = generate(tmp_path / 'inputs', developers=40)
    out = execute_analysis(manifest)
    completed = json.loads((out / 'run-complete.json').read_text())
    assert completed['verified_developer_rows'] == 40
    assert completed['synthetic_only'] is True
    assert completed['gate_passed'] is False
    with pytest.raises(ValueError, match='already exists'):
        execute_analysis(manifest, out)


def test_failed_preflight_does_not_create_output(tmp_path):
    manifest = generate(tmp_path / 'inputs', developers=40)
    cfg = json.loads(manifest.read_text())
    cfg['telemetry'][0]['grain'] = 'unknown'
    manifest.write_text(json.dumps(cfg))
    out = tmp_path / 'output'
    with pytest.raises(ValueError, match='Unsupported grain'):
        execute_analysis(manifest, out)
    assert not out.exists()


def test_verification_preserves_literal_identifier_and_checks_probabilities(tmp_path):
    row = {'username': 'NA', 'p_0_pct': None, 'predicted_level': None, 'status': 'low_confidence',
           **{f'p_{k}_conditional_pct': 25 for k in range(1, 5)}}
    pd.DataFrame([row]).to_csv(tmp_path / 'developer_predictions.csv', index=False)
    assert verify_outputs(tmp_path, ['NA']) == 1
    row['p_1_conditional_pct'] = None
    pd.DataFrame([row]).to_csv(tmp_path / 'developer_predictions.csv', index=False)
    with pytest.raises(ValueError, match='Partial probability'):
        verify_outputs(tmp_path, ['NA'])


def test_verification_rejects_missing_roster_member(tmp_path):
    row = {'username': 'a', 'p_0_pct': None, 'predicted_level': None, 'status': 'low_confidence',
           **{f'p_{k}_conditional_pct': 25 for k in range(1, 5)}}
    pd.DataFrame([row]).to_csv(tmp_path / 'developer_predictions.csv', index=False)
    with pytest.raises(ValueError, match='complete latest developer roster'):
        verify_outputs(tmp_path, ['a', 'b'])

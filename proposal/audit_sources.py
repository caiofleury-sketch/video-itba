"""Reconcile supplied research exports. Never execute the experiment notebook."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source'


def audit():
    def rows(name):
        with (SOURCE / name).open(newline='') as handle:
            return list(csv.DictReader(handle))

    catalog = rows('all_tested_parameter_configurations.csv')
    outcomes = rows('public_recipe_outcomes.csv')
    recipes = rows('published_configuration_parameters.csv')
    nb = json.loads((SOURCE / 'z526_HT5955_Ingenieria_Variables_HPO.ipynb').read_text())
    code = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')
    report = (SOURCE / 'Feature engineering parameters and public outcomes.md').read_text()
    original = json.loads((SOURCE / 'video_plan.json').read_text())
    probes = {r['feature_view']: r for r in catalog if r['study'] == 'HT5955' and r['stage'] == 'five_seed_feature_probe'}
    baseline = float(probes['snapshot152_repaired']['historical_value'])
    features = []
    for row in original['feature_screen']:
        probe = probes[row['id']]
        parameters = json.loads(probe['parameters_json'])
        assert parameters['definition']['columns'] == row['added_columns']
        assert parameters['paired_seeds'] == 5
        assert parameters['probe_rounds'] == 192 and parameters['probe_leaves'] == 52
        selected = probe['selected_or_published_member'] == 'True'
        assert selected == row['selected']
        features.append(dict(id=row['id'], label=row['label'], columns=row['added_columns'],
                             mean_auc=float(probe['historical_value']),
                             delta_auc=float(probe['historical_value']) - baseline,
                             selected=selected, definition=parameters['definition']))
    assert 'mean_delta_auc > 0 & seeds_improved >= 4L' in code
    assert '(as.double(current[[field]]) - avg) / pmax(abs(avg), 1)' in code
    assert 'avg[known < 2L] <- NA_real_' in code
    assert 'pmax(-10, pmin(10,' in code
    assert all(not r['public_score_for_this_historical_fit'] for r in catalog)
    assert len(catalog) == 260 and len(outcomes) == 92
    assert len({r['submission'] for r in outcomes}) == len(outcomes)
    assert all(r['status'] == 'SubmissionStatus.COMPLETE' for r in outcomes)
    for recipe in recipes:
        matching = [r for r in outcomes if all(r[k] == recipe[k] for k in ['competition', 'study', 'wave', 'recipe'])]
        assert len(matching) == int(recipe['submitted_files'])
        best = max(float(r['public_score']) for r in matching)
        assert best == float(recipe['best_public_score'])
        winners = [r for r in matching if float(r['public_score']) == best]
        assert {r['contacts'] for r in winners} == set(recipe['best_contacts'].split(';'))
        assert {r['submission'] for r in winners} == set(recipe['best_submission_ids'].split(';'))
        if recipe['public_score_at_9000']:
            at9000 = [r for r in matching if r['contacts'] == '9000']
            assert at9000 and all(float(r['public_score']) == float(recipe['public_score_at_9000']) for r in at9000)
    initial = next(r for r in recipes if r['study'] == 'HT5955')
    hpo = [r for r in catalog if r['study'] == 'HT5955' and r['stage'] == 'HPO']
    assert len(hpo) == 20
    winner = next(r for r in hpo if r['selected_or_published_member'] == 'True')
    assert winner['configuration'] == '10'
    params = json.loads(initial['selected_parameters_json'])
    for key, value in json.loads(winner['parameters_json']).items():
        assert abs(float(value) - float(params[key])) < 1e-12
    assert float(initial['best_public_score']) == original['initial_public']['score']
    assert 'No public score was measured for any of these eight' in report
    curve = sorted((dict(contacts=int(r['contacts']), score=float(r['public_score']), submission=r['submission'])
                    for r in outcomes if r['study'] == 'HT5955'), key=lambda r: r['contacts'])
    data = dict(
        scope='Added feature packages, their rationale, controlled impact, and final recipe outcome. Exclude inflation/IPC and pre-existing feature inventory.',
        baseline_auc=baseline, features=features,
        hpo=dict(evaluations=len(hpo), winner_trial=10, selected_parameters=params),
        initial=dict(competition='Inicial', score=float(initial['best_public_score']),
                     contacts=sorted(map(int, initial['best_contacts'].split(';'))), curve=curve),
        pilot=dict(source='Supplied audit report, section 4; qualitative outcomes only',
                   months=['May 2021', 'July 2021'], public_scored=False,
                   findings=[dict(label='Longer funds history', outcome='Improved in both months', kind='consistent'),
                             dict(label='Usage changes', outcome='Improved in both months', kind='consistent'),
                             dict(label='Prior-only EMA', outcome='Mixed across months', kind='mixed')]))
    checks = dict(
        status='PASS_WITH_EXPLICIT_SOURCE_GAPS',
        scope='Internal reconciliation of user-supplied exports and notebook source inspection; no live Kaggle query or model rerun',
        catalog_records=len(catalog), submission_records=len(outcomes), published_recipes_reconciled=len(recipes),
        study_record_counts=dict(Counter(r['study'] for r in catalog)),
        feature_mean_auc_values_reconciled=6, feature_definitions_checked_against_source=True,
        selection_rule_in_notebook_source=True,
        notebook_executed_cells=sum(c.get('execution_count') is not None for c in nb['cells']),
        notebook_executed_by_this_review=False, hpo_evaluations=len(hpo), selected_hpo_trial=winner['configuration'],
        initial_score_reconciled=True,
        pilot_qualitative_outcomes='Corroborated by supplied audit report; not regenerated from per-seed results',
        source_gaps=[
            'HT5955 per-seed outcomes absent: original 1/3/3/5/2 seed-win counts cannot be independently reproduced.',
            'HT5956 summary/per-month outcomes absent: original exact profit deltas and all month-win counts cannot be independently reproduced.',
            'Earlier Inicial reference 408.498 / submission 57670712 absent from supplied exports and audit report.',
            'Training data, native models, live submission queries, and source-manifest hashes are not supplied or rerun.'],
        source_sha256={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SOURCE.iterdir()) if p.is_file()})
    (HERE / 'audited_data.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    (HERE / 'review' / 'source_verification.json').write_text(json.dumps(checks, indent=2, ensure_ascii=False) + '\n')
    return data, checks


if __name__ == '__main__':
    _, checks = audit()
    print(json.dumps({k: v for k, v in checks.items() if k != 'source_sha256'}, indent=2))

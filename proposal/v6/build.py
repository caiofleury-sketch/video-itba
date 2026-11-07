"""Build revision 6: one study, one feature scene, one comparison figure."""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from audit_sources import audit

FAMILIES = [
    ('lag1_core', 'Last-month values', 'Previous exact-calendar-month value', 'Add recent context.'),
    ('delta1_core', 'Monthly changes', 'Current value minus last month', 'Expose sudden movement.'),
    ('prior3_core', 'Three-month averages', 'Mean of the prior three months', 'Estimate usual behavior.'),
    ('relative3_funds', 'Relative funds · 3 months', 'Balance/payroll change vs own history', 'Compare personal-scale changes.'),
    ('card_utilization', 'Card utilization', 'Card balance ÷ positive credit limit', 'Express pressure on credit.'),
    ('relative6_funds', 'Relative funds · 6 months', 'Relative funds with a longer baseline', 'Use a steadier personal reference.'),
    ('relative3_usage', 'Relative usage', 'Debit/card use vs own 3-month mean', 'Reveal changing engagement.'),
    ('monetary_ranks', 'Monetary ranks', 'Rank amounts within the same month', 'Put amounts on comparable scales.'),
    ('prior_ema3', 'Recent-weighted history', 'Exponential mean of past behavior', 'Respond to recent changes.'),
]


def build():
    audited, verification = audit()
    index = {r['id']:r for r in audited['features']}
    # Confirm the additional families really occur in the supplied configuration catalog.
    with (HERE.parent / 'source/all_tested_parameter_configurations.csv').open(newline='') as handle:
        catalog = list(csv.DictReader(handle))
    views = {r['feature_view'] for r in catalog if r['study']=='HT5956'}
    assert {'E_funds6','F_usage3','C_snapshot_rank','D_funds3_rank','G_prior_ema3'} <= views
    rows = []
    for identifier, label, definition, hypothesis in FAMILIES:
        r = dict(profit_delta_million_ars=None, profit_result_status='awaiting_matched_profit', id=identifier, label=label, definition=definition, hypothesis=hypothesis,
                 delta_auc=index[identifier]['delta_auc'] if identifier in index else None,
                 selected=index[identifier]['selected'] if identifier in index else False,
                 profit='unavailable', profit_label='—')
        if identifier=='relative3_funds':
            r.update(profit='reference', profit_label='Reference')
        elif identifier in {'relative6_funds','relative3_usage'}:
            r.update(profit='both_months', profit_label='Improved both months')
        elif identifier=='prior_ema3':
            r.update(profit='mixed', profit_label='Mixed across months')
        elif identifier=='monetary_ranks':
            r.update(profit='unverified', profit_label='Result needs verification')
        rows.append(r)
    scenes = json.loads((HERE/'voiceover.json').read_text())
    assert scenes[0]['start']==0 and scenes[-1]['end']==108
    assert all(a['end']==b['start'] for a,b in zip(scenes,scenes[1:]))
    payload = dict(duration=108, rows=rows, scenes=scenes,
                   economics=dict(correct_contact_ars=975000,wrong_contact_ars=-25000,no_contact_ars=0,reference_public_score_million_ars=401.915,feature_public_results_pending=True),
                   references=dict(auc='Original repaired snapshot', profit='Snapshot + 3-month relative funds'),
                   limits=dict(no_common_performance_scale=True,
                               rank_outcome_verified=False,
                               no_global_ranking=True,
                               exact_pilot_profit_deltas_included=False,
                               source_gaps=verification['source_gaps']))
    (HERE/'data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    (HERE/'voiceover.txt').write_text('\n\n'.join(s['voiceover'] for s in scenes)+'\n')
    page=(HERE/'template.html').read_text()
    page=page.replace('__PAYLOAD__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
    page=page.replace('__SCENES__',(HERE/'scenes.js').read_text())
    (HERE/'index.html').write_text(page)
    return payload


if __name__=='__main__':
    data=build()
    print(f'Built {HERE / "index.html"}: {len(data["rows"])} feature families, 108 seconds')

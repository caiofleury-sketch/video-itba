"""Build revision 8: Spanish graphics refined through intermediate-frame review."""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from audit_sources import audit

FAMILIES = [
    ('lag1_core', "Valor del mes anterior", "Valor del mes calendario anterior", "Aportar contexto reciente."),
    ('delta1_core', "Cambios mensuales", "Valor actual menos el del mes anterior", "Revelar movimientos bruscos."),
    ('prior3_core', "Promedios de tres meses", "Promedio de los tres meses previos", "Estimar la conducta habitual."),
    ('relative3_funds', "Fondos relativos · 3 meses", "Cambio de saldo/haberes frente a su historia", "Comparar cambios a escala personal."),
    ('card_utilization', "Utilización de tarjeta", "Saldo de tarjeta ÷ límite positivo", "Medir el uso del crédito."),
    ('relative6_funds', "Fondos relativos · 6 meses", "Fondos relativos con más historia", "Usar una referencia más estable."),
    ('relative3_usage', "Uso relativo", "Uso frente al promedio propio de 3 meses", "Detectar cambios en la actividad."),
    ('monetary_ranks', "Rangos monetarios", "Orden de los montos dentro del mismo mes", "Llevar los montos a una escala común."),
    ('prior_ema3', "Promedio exponencial", "Promedio exponencial del pasado", "Dar más peso a lo reciente."),
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
            r.update(profit='reference', profit_label="Referencia")
        elif identifier in {'relative6_funds','relative3_usage'}:
            r.update(profit='both_months', profit_label="Mejoró en ambos meses")
        elif identifier=='prior_ema3':
            r.update(profit='mixed', profit_label="Resultado mixto entre meses")
        elif identifier=='monetary_ranks':
            r.update(profit='unverified', profit_label="Resultado pendiente de verificación")
        rows.append(r)
    scenes = json.loads((HERE/'voiceover.json').read_text())
    assert scenes[0]['start']==0 and scenes[-1]['end']==108
    assert all(a['end']==b['start'] for a,b in zip(scenes,scenes[1:]))
    feature_text=next(s['voiceover'] for s in scenes if s['id']=='features')
    sentences=feature_text.rstrip('.').split('. ')
    assert len(sentences)==9
    word_counts=[len(re.findall(r'\b\w+\b',line)) for line in sentences]
    starts=[round(sum(word_counts[:i])/sum(word_counts)*49,3) for i in range(9)]
    payload = dict(feature_beats=starts, duration=108, rows=rows, scenes=scenes,
                   economics=dict(correct_contact_ars=975000,wrong_contact_ars=-25000,no_contact_ars=0,reference_public_score_million_ars=401.915,feature_public_results_pending=True),
                   references=dict(auc="Variables originales con reparaciones", profit="Variables originales + fondos relativos de 3 meses"),
                   limits=dict(no_common_performance_scale=True,
                               rank_outcome_verified=False,
                               no_global_ranking=True,
                               exact_pilot_profit_deltas_included=False,
                               source_gaps=verification['source_gaps']))
    (HERE/'data.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    (HERE/'voiceover.txt').write_text('\n\n'.join(s['voiceover'] for s in scenes)+'\n')
    (HERE/'guion.txt').write_text('\n\n'.join(s['voiceover'] for s in scenes)+'\n')
    timed=['# Guion de grabación\n']
    for s in scenes:
        timed.append(f"## {s['start']//60}:{s['start']%60:02d}–{s['end']//60}:{s['end']%60:02d} · {s['label']}\n\n{s['voiceover']}\n")
    (HERE/'guion_con_tiempos.md').write_text('\n'.join(timed))
    cues=['# Referencias de locución para las variables\n','Tiempos orientativos; ajustar a la grabación. La vista general comienza en 1:05.\n']
    for i,(line,start) in enumerate(zip(sentences,starts)):
        absolute=16+start
        cues.append(f"{int(absolute)//60}:{int(absolute)%60:02d} · {rows[i]['label']}\n\n{line.rstrip('.')}.\n")
    (HERE/'guia_de_locucion.md').write_text('\n'.join(cues))
    page=(HERE/'template.html').read_text()
    page=page.replace('__PAYLOAD__',json.dumps(payload,ensure_ascii=False).replace('</','<\\/'))
    page=page.replace('__SCENES__',(HERE/'scenes.js').read_text())
    (HERE/'index.html').write_text(page)
    return payload


if __name__=='__main__':
    data=build()
    print(f'Built {HERE / "index.html"}: {len(data["rows"])} feature families, 108 seconds')

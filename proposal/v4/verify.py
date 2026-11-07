"""Verify the consolidated chart, visual draft, and expected browser behavior."""
import json
import math
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

from build import build

HERE=Path(__file__).resolve().parent
POSES=[('hook',1.8),('history',10.5),('features',59),('measurement',72),('comparison',105),('takeaway',119)]


def main():
    data=build()
    rows=data['rows'];scenes=data['scenes']
    assert len(rows)==9 and len({r['id'] for r in rows})==9
    assert len([r for r in rows if r['delta_auc'] is not None])==5
    assert {r['id'] for r in rows if r['profit']=='both_months'}=={'relative6_funds','relative3_usage'}
    assert next(r for r in rows if r['id']=='monetary_ranks')['profit']=='unverified'
    assert next(r for r in rows if r['id']=='prior_ema3')['profit']=='mixed'
    assert data['limits']['no_global_ranking'] and data['limits']['no_common_performance_scale']
    words=[len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",s['voiceover'])) for s in scenes]
    rates=[round(w/(s['end']-s['start'])*60,1) for w,s in zip(words,scenes)]
    assert max(rates)<160
    narration=' '.join(s['voiceover'] for s in scenes)
    assert not re.search(r'\b(HT\d+|IPC|inflation|drift|champion|Senior|HPO)\b',narration,re.I)
    assert data['duration']==120 and len(scenes)==5
    assert abs(next(r['delta_auc'] for r in rows if r['selected'])*10000-14.55970052743)<1e-9
    assert data['economics']['correct_contact_ars']==975000 and data['economics']['wrong_contact_ars']==-25000
    assert data['economics']['feature_public_results_pending']
    (HERE/'frames').mkdir(exist_ok=True)
    errors=[];issues=[];boundaries=[];minimum_font=100
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
        page=browser.new_page(viewport={'width':1920,'height':1350},device_scale_factor=1)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content((HERE/'index.html').read_text())
        for s in scenes:
            for t in [s['start'],(s['start']+s['end'])/2,s['end']-.001]:
                assert page.evaluate('(t)=>window.renderAt(t)',t)==s['id']
                assert page.locator('#narration').inner_text()==s['voiceover']
                boundaries.append({'time':t,'scene':s['id']})
            page.locator(f'[data-seek="{s["start"]}"]').click()
            assert page.locator('#stage svg').get_attribute('data-scene')==s['id']
        for name,t in POSES:
            page.evaluate('(t)=>window.renderAt(t)',t)
            bounds=page.evaluate('''()=>[...document.querySelectorAll('#stage svg text')].map(el=>{
              const b=el.getBBox(),m=el.getCTM();const x=b.x*m.a+b.y*m.c+m.e,y=b.x*m.b+b.y*m.d+m.f;
              return {text:el.textContent,x,y,w:b.width*m.a,h:b.height*m.d,font:parseFloat(el.getAttribute('font-size'))*m.a};
            })''')
            # getCTM includes display scale; use SVG-local bounds for non-glyph text separately.
            out=page.evaluate('''()=>[...document.querySelectorAll('#stage svg > text, #stage svg > g text')].map(el=>{
              const b=el.getBBox();return {text:el.textContent,x:b.x,y:b.y,w:b.width,h:b.height};
            }).filter(b=>b.x<0||b.x+b.w>1920||b.y<0||b.y+b.h>970||
              (b.x+b.w>1630&&b.x<1830&&b.y<280&&b.y+b.h>80))''')
            issues.extend({'pose':name,**r} for r in out)
            if name=='features':
                stage_text=page.locator('#stage').inner_text()
                assert all(r['label'] in stage_text for r in rows)
                assert 'Card balance ÷ credit limit' in stage_text
                minimum_font=page.evaluate('''()=>Math.min(...[...document.querySelectorAll('#stage svg text[data-fit]')].map(el=>Number(el.getAttribute('font-size'))))''')
                assert minimum_font>=22,minimum_font
            if name in ['comparison','takeaway']:
                content=page.locator('#stage').inner_text()
                assert all(r['label'] in content for r in rows)
                assert 'Finding November leavers' in content and 'Historical profit' in content
                assert 'Result unverified' in content and 'Mixed across months' in content
                assert '+15' in content and '−5' in content
            svg=page.locator('#stage svg').evaluate('(el)=>el.outerHTML')
            assert ET.fromstring(svg).attrib['viewBox']=='0 0 1920 1080'
            (HERE/'frames'/f'{name}.svg').write_text(svg)
            frame=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
            frame.set_content('<html><body style="margin:0;width:1920px;height:1080px;overflow:hidden">'+svg+'</body></html>')
            frame.screenshot(path=str(HERE/'frames'/f'{name}.png'))
            frame.close()
        page.evaluate('window.renderAt(0)');before=page.locator('#stage').inner_html()
        page.evaluate('window.renderAt(10)');assert before!=page.locator('#stage').inner_html()
        page.evaluate('window.renderAt(16.1)');before=page.locator('#stage').inner_html()
        page.evaluate('window.renderAt(35)');assert before!=page.locator('#stage').inner_html()
        page.locator('#headshot').check();assert page.locator('[data-headshot-guide]').count()==1
        page.locator('#headshot').uncheck()
        page.evaluate('window.renderAt(119.9)');page.locator('#play').click();page.wait_for_timeout(350)
        assert float(page.locator('#scrub').input_value())==120
        assert page.locator('#play').inner_text()=='Play'
        page.locator('#play').click();page.wait_for_timeout(200)
        assert 0<float(page.locator('#scrub').input_value())<1
        page.locator('#play').click()
        assert page.locator('#time').inner_text().endswith('/ 2:00')
        browser.close()
    assert not errors,errors
    assert not issues,issues
    sheet=Image.new('RGB',(1920,math.ceil(len(POSES)/2)*570),'#15202a');draw=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
    for i,(name,t) in enumerate(POSES):
        with Image.open(HERE/'frames'/f'{name}.png') as image:
            assert image.size==(1920,1080);thumb=image.resize((960,540))
        x=i%2*960;y=i//2*570;sheet.paste(thumb,(x,y+30));draw.text((x+16,y+6),f'{t:g}s  {name}',font=font,fill='#e8eef1')
    sheet.save(HERE/'frames/contact_sheet.jpg',quality=92)
    result=dict(status='VISUAL_DRAFT_VERIFIED_WITH_SOURCE_GAPS',duration_seconds=120,
                scenes=len(scenes),feature_families=9,feature_definition_scenes=1,
                consolidated_comparison_figure=True,distinct_metric_columns=True,
                global_numeric_feature_ranking=False,rank_result_unverified=True,
                narration_word_count=sum(words),segment_word_counts=words,target_segment_wpm=rates,
                feature_scene_minimum_fit_font=minimum_font,
                browser_errors=errors,layout_issues=issues,scene_checks=boundaries,
                deterministic_animation_checks_passed=True,play_restart_and_end_checked=True,
                rendered_keyframes=len(POSES),illustrative_history_values_are_experimental_data=False,
                source_gaps=data['limits']['source_gaps'],
                final_recorded_audio='NOT PROVIDED',final_manim_render='NOT RUN')
    (HERE/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()

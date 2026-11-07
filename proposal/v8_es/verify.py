"""Check semantic examples, the removed scene, recommendation, and animation geometry."""
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
from build import build

HERE=Path(__file__).resolve().parent
POSES=[]


def main():
 data=build();scenes=data['scenes']
 POSES[:]=[('history',10)]+[(name,16+start+2.1) for name,start in zip(['lag','delta','mean','relative','utilization','six_month','usage','ranks','ema'],data['feature_beats'])]+[('personal_context',34.5),('overview',68),('profit_layout',90),('recommendation',106)]
 assert data['duration']==108 and [s['id'] for s in scenes]==['question','features','comparison','takeaway']
 assert all(r['profit_delta_million_ars'] is None for r in data['rows'])
 assert (90+100+110)/3==100 and (80-100)/100==-.2
 prior=[120,115,110,110,100,90];weights=[.5**i for i in range(5,-1,-1)]
 assert abs(sum(v*w for v,w in zip(prior,weights))/sum(weights)-97.619047619)<1e-8
 assert round((80/(sum(prior)/6)-1)*100,1)==-25.6
 errors=[];issues=[];checks=[]
 (HERE/'frames').mkdir(exist_ok=True)
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1920,'height':1350});page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content((HERE/'index.html').read_text())
  for scene in scenes:
   for t in [scene['start'],scene['end']-.01]:
    assert page.evaluate('(t)=>window.renderAt(t)',t)==scene['id']
    assert page.locator('#narration').inner_text()==scene['voiceover']
  for name,t in POSES:
   page.evaluate('(t)=>window.renderAt(t)',t)
   content=page.locator('#stage').inner_text()
   assert '975,000' not in content and '25,000' not in content and 'Who should receive' not in content
   if name=='overview':assert all(r['label'] in content for r in data['rows'])
   if name=='personal_context':assert '−20%' in content and '0%' in content and 'Cliente A' in content and 'Cliente B' in content
   if name=='profit_layout':
    assert 'MILLONES DE ARS' in content and 'Finding November leavers' not in content and 'Historical profit' not in content
   if name=='recommendation':assert 'saldo y haberes relativos' in content and '2 cambios relativos + 2 indicadores de escala casi nula' in content and '4 variables nuevas' in content
   out=page.evaluate('''()=>{let root=document.querySelector('#stage svg'),r=root.getBoundingClientRect(),sx=1920/r.width,sy=1080/r.height;return [...root.querySelectorAll('text')].map(el=>{const b=el.getBoundingClientRect();return {text:el.textContent,x:(b.x-r.x)*sx,y:(b.y-r.y)*sy,w:b.width*sx,h:b.height*sy}}).filter(b=>b.x<-.1||b.x+b.w>1920.1||b.y<0||b.y+b.h>970||(b.x+b.w>1630&&b.x<1830&&b.y<280&&b.y+b.h>80))}''')
   issues.extend({'pose':name,**x} for x in out)
   svg=page.locator('#stage svg').evaluate('(el)=>el.outerHTML');(HERE/'frames'/f'{name}.svg').write_text(svg)
   frame=browser.new_page(viewport={'width':1920,'height':1080});frame.set_content('<body style="margin:0">'+svg+'</body>');frame.screenshot(path=str(HERE/'frames'/f'{name}.png'));frame.close()
   checks.append({'pose':name,'time':t})
  # Check actual movement inside every construction, not only changes of labels or colors.
  starts=data['feature_beats']
  for start in starts:
   page.evaluate('(t)=>window.renderAt(t)',16+start+.1);a=page.locator('#stage svg').inner_html()
   page.evaluate('(t)=>window.renderAt(t)',16+start+1.5);assert a!=page.locator('#stage svg').inner_html()
  page.evaluate('window.renderAt(107.9)');page.locator('#play').click();page.wait_for_timeout(400)
  assert float(page.locator('#scrub').input_value())==108
  page.locator('#play').click();page.wait_for_timeout(200);assert float(page.locator('#scrub').input_value())<1;page.locator('#play').click()
  browser.close()
 assert not errors,errors
 assert not issues,issues
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
 chosen=[p for p in POSES if p[0] in ['lag','delta','mean','relative','utilization','six_month','usage','ranks','ema','overview','profit_layout','recommendation']]
 sheet=Image.new('RGB',(1920,math.ceil(len(chosen)/3)*390),'#15202a');draw=ImageDraw.Draw(sheet)
 for i,(name,t) in enumerate(chosen):
  with Image.open(HERE/'frames'/f'{name}.png') as im:thumb=im.resize((640,360))
  x=i%3*640;y=i//3*390;sheet.paste(thumb,(x,y+30));draw.text((x+12,y+5),f'{t:g}s · '+{'lag':'rezago','delta':'cambio','mean':'promedio','relative':'cambio relativo','utilization':'utilización','six_month':'seis meses','usage':'uso relativo','ranks':'rangos','ema':'promedio exponencial','overview':'vista general','profit_layout':'ganancia pendiente','recommendation':'recomendación'}[name],font=font,fill='#e8eef1')
 sheet.save(HERE/'frames/contact_sheet.jpg',quality=94)
 result=dict(status='PASS_WITH_PROFIT_RESULTS_PENDING',duration=108,scoring_rules_scene_removed=True,feature_construction_beats=9,overview_included=True,profit_only_layout=True,verified_profit_values_available=0,explicit_recommendation=True,example_math_verified=True,browser_errors=errors,geometry_issues=issues,poses=checks)
 (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()

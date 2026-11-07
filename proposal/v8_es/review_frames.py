"""Capture intermediate frames and inspect visible text intersections, not just end poses."""
import json
import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
from build import build

HERE=Path(__file__).resolve().parent
GROUPS={
 'apertura':[2.8,3.5,4.2,4.9,5.6,6.3],
 'promedio':[],
 'rangos':[],
 'transiciones':[64.8,65.0,65.3,69.9,70.2,71.0],
 'recomendacion':[94.0,94.5,95.3,96.1,97.0,98.5],
}


def capture(label):
 data=json.loads((HERE/'data.json').read_text()) if '--existing' in sys.argv else build()
 out=HERE/'revision'/label;out.mkdir(parents=True,exist_ok=True)
 GROUPS['promedio']=[16+data['feature_beats'][2]+v for v in [.1,.45,.8,1.15,1.5,2.0]]
 GROUPS['rangos']=[16+data['feature_beats'][7]+v for v in [.1,.45,.8,1.15,1.5,2.0]]
 if label=='final':
  for i,name in enumerate(['rezago','cambio','promedio','fondos_3','utilizacion','fondos_6','uso','rangos','exponencial']):
   GROUPS[name]=[16+data['feature_beats'][i]+v for v in [.1,.45,.8,1.15,1.5,2.4]]
  GROUPS['ganancia']=[70,70.35,70.7,71.05,71.4,72.0]
  GROUPS['cierre']=[99,99.5,100,101,104,107.9]
  GROUPS['escala_personal']=[16+data['feature_beats'][3]+v for v in [3.65,3.8,4.15,4.5,5.0,7.5]]
 report=[];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
 with sync_playwright() as tool:
  browser=tool.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
  page.set_content((HERE/'index.html').read_text())
  page.add_style_tag(content='main{max-width:none!important;padding:0!important}header,.controls,nav,#narration,.note,details{display:none!important}.stage{width:1920px!important;height:1080px!important;border:none!important}')
  for group,times in GROUPS.items():
   sheet=Image.new('RGB',(1920,1710),'#15202a');draw=ImageDraw.Draw(sheet)
   for i,t in enumerate(times):
    page.evaluate('(t)=>window.renderAt(t)',t)
    boxes=page.evaluate('''()=>{let svg=document.querySelector('#stage svg');return [...svg.querySelectorAll('text')].map(el=>{let opacity=1;for(let a=el;a&&a!==svg;a=a.parentElement)opacity*=Number(getComputedStyle(a).opacity);const b=el.getBoundingClientRect();return {text:el.textContent,x:b.x,y:b.y,w:b.width,h:b.height,opacity}}).filter(b=>b.opacity>.25&&b.w>2&&b.h>14)}''')
    collisions=[]
    for j,a in enumerate(boxes):
     for b in boxes[j+1:]:
      dx=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x']);dy=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
      if dx>3 and dy>3 and dx*dy>35:collisions.append({'a':a['text'],'b':b['text'],'area':round(dx*dy,1)})
    report.append({'group':group,'time':round(t,3),'collisions':collisions})
    file=out/f'{group}_{i}.png';page.screenshot(path=str(file))
    with Image.open(file) as im:sheet.paste(im.resize((960,540)),(i%2*960,i//2*570+30))
    draw.text((i%2*960+15,i//2*570+5),f'{t:.2f}s',font=font,fill='#e8eef1')
   sheet.save(out/f'{group}.jpg',quality=94)
  browser.close()
 (out/'intersecciones.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 summary={'revision':label,'frames':len(report),'frames_with_text_intersections':sum(bool(x['collisions']) for x in report),'intersections':[x for x in report if x['collisions']]}
 (out/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':capture(sys.argv[1] if len(sys.argv)>1 else 'antes')

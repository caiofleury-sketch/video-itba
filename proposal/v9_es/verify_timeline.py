"""Scan in-between text geometry over the complete animation in Chromium."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent

def main():
 report=[];errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1920,'height':1080})
  page.on('pageerror',lambda error:errors.append(str(error)))
  page.set_content((HERE/'index.html').read_text())
  result=page.evaluate('''()=>{
    const issues=[];let labels=new Set();
    for(let step=0;step<960;step++){
      const time=step/8;window.renderAt(time);
      const svg=document.querySelector('#stage svg'),root=svg.getBoundingClientRect(),scale=1920/root.width;
      const boxes=[...svg.querySelectorAll('text')].map(el=>{
        let opacity=1;for(let a=el;a&&a!==svg;a=a.parentElement)opacity*=Number(getComputedStyle(a).opacity);
        const b=el.getBoundingClientRect();return {text:el.textContent,x:(b.x-root.x)*scale,y:(b.y-root.y)*scale,w:b.width*scale,h:b.height*scale,opacity};
      }).filter(b=>b.opacity>.25&&b.w>2&&b.h>14);
      const collisions=[],bounds=[];
      boxes.forEach((a,i)=>{
        labels.add(a.text);
        if(a.x<-.1||a.x+a.w>1920.1||a.y<0||a.y+a.h>970||(a.x+a.w>1630&&a.x<1830&&a.y<280&&a.y+a.h>80))bounds.push(a.text);
        boxes.slice(i+1).forEach(b=>{
          const dx=Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x),dy=Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y);
          if(dx>3&&dy>3&&dx*dy>35)collisions.push([a.text,b.text,Math.round(dx*dy)]);
        });
      });
      if(collisions.length||bounds.length)issues.push({time,collisions,bounds});
    }
    return {sample_count:960,interval_seconds:.125,labels:[...labels],issues};
  }''')
  browser.close()
 result['browser_errors']=errors
 result['status']='PASS' if not errors and not result['issues'] else 'NEEDS_REVIEW'
 (HERE/'verificacion_temporal.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':result['status'],'samples':result['sample_count'],'issue_count':len(result['issues']),'first_issues':result['issues'][:12],'browser_errors':errors},ensure_ascii=False,indent=2))

if __name__=='__main__':main()

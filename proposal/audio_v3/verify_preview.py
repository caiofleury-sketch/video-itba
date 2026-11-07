"""Verify playable audio, A/B switching at the same position and immutable note data."""
import json,threading,hashlib,subprocess
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent
class H(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(P),**kw)
 def log_message(self,*a):pass

def main():
 assert (P/'score.json').read_bytes()==(P.parent/'audio_v2/score.json').read_bytes()
 errors=[]
 with ThreadingHTTPServer(('127.0.0.1',0),H) as server:
  threading.Thread(target=server.serve_forever,daemon=True).start()
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage']);page=b.new_page(viewport={'width':1200,'height':1150});page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(f'http://127.0.0.1:{server.server_port}/comparar_instrumentos.html');page.wait_for_function('[...document.querySelectorAll("audio")].every(a=>a.readyState>=2)')
   page.locator('#play').click();page.wait_for_timeout(900);before=page.evaluate('instrumentPreview.state()');assert not before['paused'] and before['time']>.5,before
   page.locator('#after-button').click();page.wait_for_timeout(500);after=page.evaluate('instrumentPreview.state()');assert after['chosen']=='after' and not after['paused'] and after['time']>=before['time'],after
   assert after['time']-before['time']<1.0,(before,after)
   page.locator('#play').click();page.locator('#seek').evaluate('(e)=>{e.value=18;e.dispatchEvent(new Event("input"))}');page.locator('#before-button').click();page.wait_for_timeout(120)
   state=page.evaluate('instrumentPreview.state()');assert abs(state['time']-18)<.15 and state['paused'],state
   page.screenshot(path=str(P/'comparacion.png'),full_page=True)
   page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   page.locator('#full').evaluate('(e)=>e.play()');page.wait_for_timeout(700);assert page.locator('#full').evaluate('(e)=>!e.paused&&e.currentTime>.3');page.locator('#full').evaluate('(e)=>e.pause()')
   b.close()
  server.shutdown()
 assert not errors,errors
 for name in ['comparacion_antes.mp3','comparacion_instrumentos.mp3','musica_instrumentos_nuevos.mp3']:
  subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(P/name),'-f','null','-'],check=True)
 result={'status':'PASS','score_unchanged':True,'play_pause':True,'switch_preserves_position':True,'full_track_plays':True,'mobile_without_overflow':True,'javascript_errors':errors}
 (P/'verificacion_comparacion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

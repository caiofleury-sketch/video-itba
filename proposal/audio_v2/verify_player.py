"""Exercise the real three-track player: play/pause, seeking, mute, gain and scene sync."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent

def main():
 errors=[];console_errors=[];states=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1440,'height':1500})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:console_errors.append(m.text) if m.type=='error' else None)
  page.goto(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8768/audio_v2/index.html')
  page.wait_for_function('document.querySelector("#video").readyState>=2&&[...document.querySelectorAll("audio")].every(a=>a.readyState>=2)')
  assert page.locator('html').get_attribute('lang')=='es-AR'
  page.locator('#play').click();page.wait_for_timeout(1400)
  state=page.evaluate('soundscape.state()');states.append(state)
  assert not state['paused'] and state['time']>.6,state
  assert max(abs(state['time']-state[k]) for k in ['musicTime','fxTime'])<.12,state
  page.locator('#play').click();paused=page.evaluate('soundscape.state()');page.wait_for_timeout(250)
  assert abs(page.evaluate('soundscape.state().time')-paused['time'])<.03
  page.locator('[data-seek="102"]').click();page.wait_for_timeout(350)
  state=page.evaluate('soundscape.state()');states.append(state);assert abs(state['time']-102)<.1 and state['paused']
  page.locator('#music-mute').click();assert page.evaluate('soundscape.state().musicMuted')
  page.locator('#music-mute').click();assert not page.evaluate('soundscape.state().musicMuted')
  page.locator('#fx-mute').click();assert page.evaluate('soundscape.state().fxMuted')
  page.locator('#fx-mute').click();assert not page.evaluate('soundscape.state().fxMuted')
  page.locator('#music-volume').evaluate('(el)=>{el.value=45;el.dispatchEvent(new Event("input"))}')
  page.locator('#fx-volume').evaluate('(el)=>{el.value=65;el.dispatchEvent(new Event("input"))}')
  assert page.evaluate('soundscape.state().musicVolume')==.45 and page.evaluate('soundscape.state().fxVolume')==.65
  page.locator('#play').click();page.wait_for_timeout(1000)
  state=page.evaluate('soundscape.state()');states.append(state)
  assert not state['paused'] and state['time']>102.5 and max(abs(state['time']-state[k]) for k in ['musicTime','fxTime'])<.12,state
  page.evaluate('soundscape.jump(33.25)');page.wait_for_timeout(650);page.evaluate('soundscape.pause()')
  assert 'contexto' in page.locator('#cue').inner_text().lower()
  page.screenshot(path=str(HERE/'reproductor.png'),full_page=True)
  page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(100)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(HERE/'reproductor_movil.png'),full_page=True)
  page.evaluate('soundscape.jump(119.8)');page.locator('#play').click();page.wait_for_timeout(600)
  assert page.evaluate('soundscape.state().paused')
  page.locator('#play').click();page.wait_for_timeout(450)
  state=page.evaluate('soundscape.state()');states.append(state);assert state['time']<1 and not state['paused']
  page.evaluate('soundscape.pause()');browser.close()
 assert not errors,errors
 # Browser may request the optional favicon, which has no bearing on playback.
 actionable=[e for e in console_errors if '404' not in e]
 assert not actionable,actionable
 result={'estado':'VERIFICADO','reproduccion_y_pausa':True,'salto_de_escenas':True,'silenciar_capas':True,'ajuste_de_niveles':True,'reinicio_al_final':True,'vista_movil_sin_desbordes':True,'errores_javascript':errors,'estados':states}
 name='verificacion_reproductor_autonomo.json' if len(sys.argv)>1 else 'verificacion_reproductor.json'
 (HERE/name).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

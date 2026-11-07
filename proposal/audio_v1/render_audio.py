"""Synthesize the original JavaScript score using Tone.js in Chromium."""
import json,base64
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent

def main():
 score=json.loads((HERE/'score.json').read_text());reports=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
  page=browser.new_page();page.on('pageerror',lambda e:print('Browser error: '+str(e),flush=True))
  page.set_content('<html><head><meta charset="utf-8"></head><body>Render de audio</body></html>')
  page.add_script_tag(path=str(HERE/'vendor/Tone-15.1.22.js'));page.add_script_tag(path=str(HERE/'synth.js'))
  for stem in ['music','fx']:
   print('Sintetizando '+stem,flush=True)
   meta=page.evaluate('([score,stem])=>window.renderStem(score,stem)',[score,stem]);print(meta,flush=True)
   channels=[]
   for ch in range(2):
    raw=bytearray()
    for start in range(0,meta['length'],240000):
     part=page.evaluate('([c,s,n])=>window.audioChunk(c,s,n)',[ch,start,min(240000,meta['length']-start)])
     raw.extend(base64.b64decode(part))
    channels.append(np.frombuffer(raw,dtype='<f4'))
   samples=np.stack(channels,axis=1)
   assert np.isfinite(samples).all() and np.max(np.abs(samples))<1
   wavfile.write(HERE/f'{stem}_raw.wav',score['sampleRate'],samples)
   reports.append({'stem':stem,**meta,'sample_peak':float(np.abs(samples).max())})
  browser.close()
 (HERE/'synthesis_report.json').write_text(json.dumps({'engine':'Tone.js 15.1.22 / Chromium OfflineAudioContext','stems':reports},indent=2)+'\n')
 print('Síntesis terminada',flush=True)

if __name__=='__main__':main()

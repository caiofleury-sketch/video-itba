"""Render the notated Tone.js score in bounded offline windows with preroll and crossfades."""
import json,base64,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
class Host(BaseHTTPRequestHandler):
 def do_GET(self):
  body=b'<html><head><meta charset="utf-8"></head><body>Offline score render</body></html>'
  self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def log_message(self,*args):pass

def main():
 score=json.loads((HERE/'score.json').read_text());sr=score['sampleRate'];total=round(score['duration']*sr);reports=[]
 server=ThreadingHTTPServer(('127.0.0.1',0),Host);threading.Thread(target=server.serve_forever,daemon=True).start()
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage','--autoplay-policy=no-user-gesture-required'])
  for stem in ['music','fx']:
   mix=np.zeros((total,2),dtype=np.float32);events=score[stem];chunks=[]
   for start in range(0,score['duration'],16):
    end=min(score['duration'],start+16);left=max(0,start-3);a=max(0,start-.1);b=min(score['duration'],end+.1)
    selected=[dict(e,time=round(e['time']-left,5)) for e in events if left<=e['time']<b]
    if not selected:continue
    render_samples=round((b-left)*sr)+2
    window={**score,'duration':render_samples/sr,'windowStart':left,'music':selected if stem=='music' else [],'fx':selected if stem=='fx' else []}
    # A fresh context per musical window bounds polyphonic native-node lifetime.
    page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'http://127.0.0.1:{server.server_port}/')
    page.add_script_tag(content='let seed=526;Math.random=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296}')
    page.add_script_tag(path=str(HERE.parent/'audio_v1/vendor/Tone-15.1.22.js'));page.add_script_tag(path=str(HERE/'synth.js'))
    print(f'{stem}: {start}–{end}s ({len(selected)} notas)',flush=True);begin=time.monotonic()
    meta=page.evaluate('([s,k])=>Promise.race([renderStem(s,k),new Promise((_,r)=>setTimeout(()=>r(Error("Offline window timeout")),45000))])',[window,stem])
    channels=[]
    for ch in range(2):
     raw=bytearray()
     for i in range(0,meta['length'],240000):
      raw.extend(base64.b64decode(page.evaluate('([c,s,n])=>audioChunk(c,s,n)',[ch,i,min(240000,meta['length']-i)])))
     channels.append(np.frombuffer(raw,dtype='<f4'))
    samples=np.stack(channels,axis=1);assert np.isfinite(samples).all() and not errors,errors
    ai=round(a*sr);bi=round(b*sr);skip=round((a-left)*sr);piece=samples[skip:skip+bi-ai]
    assert len(piece)==bi-ai,(len(piece),bi-ai,meta)
    weights=np.ones(len(piece),dtype=np.float32)
    if start>0:
     n=round(.2*sr);weights[:n]=np.linspace(0,1,n,endpoint=False)
    if end<score['duration']:
     n=round(.2*sr);weights[-n:]=np.linspace(1,0,n,endpoint=False)
    mix[ai:bi]+=piece*weights[:,None]
    chunks.append({'start':start,'end':end,'render_seconds':round(time.monotonic()-begin,2),'notes':len(selected)});page.close()
   assert np.max(np.abs(mix))<1 and np.isfinite(mix).all()
   wavfile.write(HERE/f'{stem}_raw.wav',sr,mix)
   reports.append({'stem':stem,'samples':total,'peak':float(np.abs(mix).max()),'windows':chunks})
  browser.close()
 server.shutdown();server.server_close()
 (HERE/'synthesis_report.json').write_text(json.dumps({'engine':'Tone.js 15.1.22 / Chromium OfflineAudioContext','preroll_seconds':3,'crossfade_seconds':.2,'stems':reports},indent=2)+'\n')
 print('Síntesis completa',flush=True)

if __name__=='__main__':main()

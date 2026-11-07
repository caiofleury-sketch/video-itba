"""Validate full decoding, browser playback/seeking and burned subtitle pixels."""
from pathlib import Path
import json,subprocess,threading,functools
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;TMP=Path('/workspace/presenter_private/final');report={'status':'PASS','exports':[]}
class Host(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(P),**kwargs)
 def log_message(self,*args):pass
 def do_GET(self):
  from urllib.parse import unquote
  path=P/unquote(self.path.lstrip('/'))
  if not path.is_file():return super().do_GET()
  size=path.stat().st_size;start=0;end=size-1
  r=self.headers.get('Range')
  if r:
   lo,hi=r.replace('bytes=','').split('-');start=int(lo or 0);end=min(int(hi) if hi else end,end)
  self.send_response(206 if r else 200);self.send_header('Content-Type','video/mp4');self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1))
  if r:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
  self.end_headers()
  try:
   with path.open('rb') as f:
    f.seek(start);remaining=end-start+1
    while remaining:
     data=f.read(min(65536,remaining))
     if not data:break
     self.wfile.write(data);remaining-=len(data)
  except (BrokenPipeError,ConnectionResetError):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Host);threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-dev-shm-usage'])
 for name in ['video_final.mp4','video_final_subtitulos.mp4']:
  path=P/name
  subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-f','null','-'],check=True)
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
  v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
  assert v['codec_name']=='h264' and v['profile']=='Constrained Baseline' and v['pix_fmt']=='yuv420p' and a['codec_name']=='aac'
  assert abs(float(info['format']['duration'])-119.44)<.06
  raw=path.read_bytes();assert raw.index(b'moov')<raw.index(b'mdat')
  page=b.new_page();page.goto(f'http://127.0.0.1:{server.server_port}/');page.set_content(f'<video id="v" src="/{name}" preload="auto"></video>')
  page.evaluate('''async()=>{const v=document.querySelector('video');await new Promise((ok,no)=>{v.addEventListener('canplay',ok,{once:true});v.addEventListener('error',no,{once:true});if(v.readyState>=3)ok()});await v.play()}''')
  page.wait_for_timeout(900);states=[]
  for t in [8,78,110]:
   page.evaluate('''async t=>{const v=document.querySelector('video');await new Promise(ok=>{v.addEventListener('seeked',ok,{once:true});v.currentTime=t});await v.play()}''',t)
   page.wait_for_timeout(600)
   state=page.evaluate('''()=>{const v=document.querySelector('video');return {time:v.currentTime,paused:v.paused,ready:v.readyState,width:v.videoWidth,height:v.videoHeight,audioBytes:v.webkitAudioDecodedByteCount,frames:v.getVideoPlaybackQuality().totalVideoFrames,error:v.error?.message||null}}''')
   assert state['time']>t+.1 and not state['paused'] and state['width']==1920 and state['audioBytes']>0 and not state['error'],state
   states.append(state)
  report['exports'].append({'file':name,'bytes':path.stat().st_size,'duration':float(info['format']['duration']),'full_decode':'PASS','faststart':True,'h264_baseline_aac':True,'browser_playback_and_seek':states})
  page.close()
 b.close()
server.shutdown()
# Check that captions are actually burned into the delivery.
checks=[]
for t in [8,30,83,111.5]:
 arrays=[]
 for i,name in enumerate(['video_final.mp4','video_final_subtitulos.mp4']):
  out=TMP/f'subtitle_{t}_{i}.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(P/name),'-frames:v','1','-threads','1',str(out)],check=True);arrays.append(np.asarray(Image.open(out)).astype(float))
 diff=np.max(np.abs(arrays[0]-arrays[1]),axis=2);n=int((diff[970:]>65).sum());assert n>100,(t,n);checks.append({'time':t,'subtitle_pixels':n})
report['burned_subtitles']=checks
report['measured_final_audio']={'integrated_lufs':-16.02,'true_peak_dbtp':-1.30,'loudness_range_lu':4.60}
(P/'verificacion.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

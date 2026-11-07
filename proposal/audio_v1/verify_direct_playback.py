"""Test actual MP4/WebM playback, rendered pixels and audio energy in Chromium."""
import json,threading,time,sys
from pathlib import Path
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from serve_preview import MediaHandler

HERE=Path(__file__).resolve().parent

class QuietHandler(MediaHandler):
 def log_message(self,*args):pass

def main():
 reports=[]
 with ThreadingHTTPServer(('127.0.0.1',0),QuietHandler) as server:
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  origin=f'http://127.0.0.1:{server.server_port}'
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
   for filename in (sys.argv[1:] or ['video_con_sonido.mp4','video_con_sonido_compatible.mp4','video_con_sonido_alternativa.webm']):
    page=browser.new_page(viewport={'width':1280,'height':900});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(origin+'/audio_v1/index.html')
    page.evaluate('''(src)=>{
      document.body.innerHTML='<video id="direct" controls playsinline style="width:1100px;background:black"></video><button id="go">Play</button>';
      const v=document.getElementById('direct');v.src=src;window.directVideo=v;window.directError=null;
      v.onerror=()=>window.directError={code:v.error.code,message:v.error.message};
      window.ctx=new AudioContext();window.source=ctx.createMediaElementSource(v);window.meter=ctx.createAnalyser();
      meter.fftSize=2048;source.connect(meter);meter.connect(ctx.destination);
      document.getElementById('go').onclick=async()=>{await ctx.resume();await v.play()};
    }''',origin+'/audio_v1/'+filename)
    page.wait_for_function('directVideo.readyState>=2||directError')
    assert page.evaluate('directError') is None,(filename,page.evaluate('directError'))
    page.locator('#go').click();page.wait_for_timeout(1300)
    assert page.evaluate('!directVideo.paused&&directVideo.currentTime>.6'),filename
    samples=[]
    for at in [10,33,94]:
     page.evaluate('(t)=>{directVideo.currentTime=t}',at)
     page.wait_for_function('(t)=>!directVideo.seeking&&Math.abs(directVideo.currentTime-t)<.8',arg=at)
     page.wait_for_timeout(350)
     state=page.evaluate('''()=>{
       const v=directVideo,c=document.createElement('canvas');c.width=320;c.height=180;
       const x=c.getContext('2d');x.drawImage(v,0,0,c.width,c.height);
       const bytes=x.getImageData(0,0,c.width,c.height).data;let lit=0;
       for(let i=0;i<bytes.length;i+=4)if(Math.max(bytes[i],bytes[i+1],bytes[i+2])>65)lit++;
       const wave=new Float32Array(meter.fftSize);meter.getFloatTimeDomainData(wave);
       return {time:v.currentTime,videoWidth:v.videoWidth,videoHeight:v.videoHeight,frames:v.getVideoPlaybackQuality().totalVideoFrames,litPixels:lit,audioRms:Math.sqrt(wave.reduce((s,v)=>s+v*v,0)/wave.length),paused:v.paused,error:directError};
     }''')
     assert state['litPixels']>100 and state['audioRms']>1e-7 and not state['paused'] and state['error'] is None,(filename,state)
     samples.append(state)
    page.screenshot(path=str(HERE/('reproduccion_'+Path(filename).stem+'.png')))
    page.evaluate('directVideo.pause();directVideo.currentTime=107.4')
    page.wait_for_function('!directVideo.seeking');page.locator('#go').click();page.wait_for_timeout(1000)
    assert page.evaluate('directVideo.ended'),filename
    assert not errors,errors
    reports.append({'file':filename,'status':'PASS','decoded_picture_audio_seek_end':True,'samples':samples})
    page.close();print(filename+' PASS',flush=True)
   browser.close()
  server.shutdown()
 output=HERE/'verificacion_reproduccion_directa.json'
 previous=json.loads(output.read_text()) if output.exists() else []
 merged={r['file']:r for r in previous}
 merged.update({r['file']:r for r in reports})
 output.write_text(json.dumps(list(merged.values()),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(reports,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

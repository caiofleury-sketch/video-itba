"""Check the delivered movies, actual subtitle pixels and scene content against the SVG preview."""
import json,subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import numpy as np
from playwright.sync_api import sync_playwright

P=Path(__file__).resolve().parent;TIMES=[10,24.25,33.25,61.25,74,82,92,100,110,118]

def frame(video,time,out,vf=None):
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(time),'-i',str(video)]
 if vf:cmd+=['-vf',vf]
 subprocess.run(cmd+['-frames:v','1','-threads','1',str(out)],check=True)

def main():
 out=P/'revision_exportacion';out.mkdir(exist_ok=True);report=[]
 for name in ['video_final.mp4','video_final_subtitulos.mp4','video_final_subtitulos.webm']:
  subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(P/name),'-f','null','-'],check=True)
 with sync_playwright() as t:
  browser=t.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage']);page=browser.new_page(viewport={'width':1920,'height':1080})
  page.set_content((P.parent/'v9_es/index.html').read_text());page.add_style_tag(content='main{max-width:none!important;padding:0!important}header,.controls,nav,#narration,.note,details{display:none!important}.stage{width:1920px!important;height:1080px!important;border:none!important}')
  for i,time in enumerate(TIMES):
   page.evaluate('(t)=>renderAt(t)',time);expected=out/f'svg_{i}.png';page.screenshot(path=str(expected));base=out/f'video_{i}.png';frame(P/'video_final.mp4',time,base)
   with Image.open(expected) as a,Image.open(base) as b:
    diff=ImageChops.difference(a.convert('RGB'),b.convert('RGB'));error=sum(ImageStat.Stat(diff).mean)/3
   assert error<6,(time,error)
   item={'time':time,'video_vs_svg_mae_rgb':round(error,3)}
   if time>=70:
    overlay=out/f'expected_caption_{i}.png';actual=out/f'captioned_{i}.png'
    frame(P/'video_final.mp4',time,overlay,f'setpts=PTS+{time}/TB,ass={P}/subtitulos_es.ass');frame(P/'video_final_subtitulos.mp4',time,actual)
    with Image.open(base) as a,Image.open(overlay) as b,Image.open(actual) as c:
     a,b,c=[np.asarray(x).astype(float) for x in [a,b,c]];mask=np.max(np.abs(a-b),axis=2)>60;mask[:970]=False
     assert mask.sum()>100,(time,int(mask.sum()))
     caption_error=float(np.abs(b-c)[mask].mean());assert caption_error<25,(time,caption_error)
     item['actual_subtitle_pixel_error']=round(caption_error,3)
   report.append(item)
  browser.close()
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(P/'video_final.mp4')],text=True))
 v,a=info['streams'];assert v['profile']=='Constrained Baseline' and v['pix_fmt']=='yuv420p' and v['color_range']=='tv' and a['codec_name']=='aac'
 assert abs(float(info['format']['duration'])-120)<.05
 result={'status':'PASS','full_decode':3,'duration':120,'frames':report,'portable_h264_aac':True,'subtitle_timing':'provisional until the actual voice recording'}
 (P/'verificacion_exportacion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

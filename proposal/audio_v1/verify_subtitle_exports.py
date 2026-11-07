"""Decode the actual subtitle movies and verify the text pixels match the approved samples."""
import json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent

def main():
 review=json.loads((HERE/'verificacion_subtitulos.json').read_text());reports=[]
 for filename in ['video_con_subtitulos.mp4','video_con_subtitulos.webm']:
  path=HERE/filename
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))
  assert abs(float(info['format']['duration'])-108)<.1 and len(info['streams'])==2
  subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(path),'-f','null','-'],check=True)
  frames=[]
  for i,sample in enumerate(review['muestras_visuales']):
   out=HERE/'revision_subtitulos'/f'exportado_{path.suffix[1:]}_{i}.png'
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(sample['tiempo']),'-i',str(path),'-frames:v','1','-threads','1',str(out)],check=True)
   with Image.open(out) as actual,Image.open(HERE/'revision_subtitulos'/f'subtitulos_{i}.png') as expected,Image.open(HERE/'revision_subtitulos'/f'base_{i}.png') as base:
    expected=expected.resize(actual.size,Image.Resampling.LANCZOS);base=base.resize(actual.size,Image.Resampling.LANCZOS)
    a=np.asarray(actual).astype(float);e=np.asarray(expected).astype(float);b=np.asarray(base).astype(float)
    mask=(np.max(np.abs(e-b),axis=2)>60);mask[:round(actual.height*955/1080)]=False
    error=float(np.abs(a-e)[mask].mean())
    assert mask.sum()>100 and error<28,(filename,i,error,int(mask.sum()))
    frames.append({'time':sample['tiempo'],'subtitle_pixel_error_rgb':round(error,3),'caption_pixels':int(mask.sum())})
  reports.append({'file':filename,'full_decode':'PASS','duration':info['format']['duration'],'actual_subtitle_frames':frames})
 def audio_hash(filename):
  return subprocess.check_output(['ffmpeg','-hide_banner','-v','error','-i',str(HERE/filename),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],text=True).strip()
 unchanged=audio_hash('video_con_subtitulos.mp4')==audio_hash('video_con_sonido_compatible.mp4');assert unchanged
 result={'status':'PASS','provisional_timing':True,'audio_mp4_unchanged':unchanged,'exports':reports}
 (HERE/'verificacion_exportacion_subtitulos.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

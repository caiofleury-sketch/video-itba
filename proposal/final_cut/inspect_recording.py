"""Inspect a local presenter recording before choosing trims, crop and audio processing."""
import argparse,json,subprocess,re
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from PIL import Image,ImageDraw,ImageFont

def main():
 parser=argparse.ArgumentParser();parser.add_argument('recording',type=Path);parser.add_argument('--out',type=Path,default=Path('/workspace/presenter_private/inspection'));a=parser.parse_args()
 if not a.recording.is_file():parser.error('No local recording is available yet')
 a.out.mkdir(parents=True,exist_ok=True)
 def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
 probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(a.recording)]).stdout)
 duration=float(probe['format']['duration']);audio=[s for s in probe['streams'] if s['codec_type']=='audio'];assert audio,'Recording has no audio stream'
 wav=a.out/'analysis.wav';run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(a.recording),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)])
 sr,x=wavfile.read(wav);x=x.astype(float)/32768;hop=320;n=len(x)//hop;rms=np.sqrt(np.mean(x[:n*hop].reshape(n,hop)**2,axis=1))
 noise=float(np.percentile(rms,15));threshold=max(10**(-45/20),min(noise*3,float(np.max(rms))*.12));active=rms>threshold
 groups=[];indices=np.flatnonzero(active)
 if len(indices):
  start=prev=int(indices[0]);count=1
  for k in indices[1:]:
   k=int(k)
   if k-prev>10:
    if count>=8:groups.append((start*hop/sr,(prev+1)*hop/sr))
    start=k;count=0
   prev=k;count+=1
  if count>=8:groups.append((start*hop/sr,(prev+1)*hop/sr))
 assert groups,'No sustained speech-like audio detected'
 candidate=[max(0,groups[0][0]-.35),min(duration,groups[-1][1]+.35)]
 loud=run(['ffmpeg','-hide_banner','-nostats','-i',str(a.recording),'-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']).stderr
 measurement=json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}',loud)[-1])
 sheet=Image.new('RGB',(1440,1200),'#15202a');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
 times=np.linspace(0,max(0,duration-.1),12)
 for i,t in enumerate(times):
  f=a.out/f'source_{i}.jpg';run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(float(t)),'-i',str(a.recording),'-frames:v','1','-vf','scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2','-q:v','3',str(f)])
  with Image.open(f) as image:sheet.paste(image,(i%3*480,i//3*300+30))
  draw.text((i%3*480+12,i//3*300+5),f'{t:.2f}s',font=font,fill='#e8eef1')
 sheet.save(a.out/'contact_sheet.jpg',quality=94)
 result={'duration':duration,'probe':probe,'speech_like_groups':groups,'candidate_trim':candidate,'trim_requires_editor_review':True,'loudness':measurement,'noise_rms':noise,'activity_threshold':threshold,'source_files_private':True}
 (a.out/'inspection.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='probe'},indent=2))
if __name__=='__main__':main()

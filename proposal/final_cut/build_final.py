"""Create the final presenter cut. Camera/audio intermediates stay outside Git."""
import argparse,json,subprocess,re,textwrap
from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;TMP=Path('/workspace/presenter_private/final');TMP.mkdir(parents=True,exist_ok=True)
def run(args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
START=.49;END=119.93;DURATION=END-START
# Scene/feature entries follow the actual recorded pauses; image and voice remain in sync.
POINTS=[(0,0),(16,16.1),(19.649,20.03),(22.777,22.91),(27.468,27.51),(35.809,35.99),(41.543,42.49),(45.713,46.61),(53.011,54.15),(59.266,59.85),(65,65.2),(70,68.47),(73,70.25),(80,77.17),(90,89.37),(102,102.73),(120,DURATION)]
# Caption phrases are the approved Spanish script, timed to the recorded phrase groups.
TIMES=[(.84,2.56),(3.02,5.15),(6.38,7.4),(7.68,11.7),(12.18,13.8),(13.8,16.05),(16.6,19.3),(20.52,23.05),(23.4,26.9),(28,31.1),(32,35.3),(36.48,39.8),(40.24,41.7),(42.98,46.75),(47.1,51.3),(51.98,54.1),(54.64,58.65),(60.34,65.55),(68.96,70.65),(70.74,76.5),(77.66,80.2),(80.2,84.5),(85.2,88.85),(89.86,94.4),(94.56,99.3),(99.4,101.65),(103.22,104.85),(105.1,107.4),(107.96,110.1),(111.12,113.3),(113.3,114.7),(114.94,117.1),(117.72,119.8)]
def stamp(t,ass=False):
 q=100 if ass else 1000;n=round(max(0,t)*q);h,n=divmod(n,3600*q);m,n=divmod(n,60*q);s,n=divmod(n,q)
 return f'{h}:{m:02}:{s:02}.{n:02}' if ass else f'{h:02}:{m:02}:{s:02},{n:03}'
def captions():
 source=(P.parent/'audio_v2/subtitulos_es.srt').read_text();blocks=source.strip().split('\n\n');assert len(blocks)==len(TIMES)
 texts=['\n'.join(b.splitlines()[2:]) for b in blocks]
 header=(P.parent/'audio_v2/subtitulos_es.ass').read_text().split('Dialogue:')[0]
 srt=[];ass=[]
 for i,(text,(a,b)) in enumerate(zip(texts,TIMES),1):
  a=max(0,a-START);b=min(DURATION,b-START)
  srt.append(f'{i}\n{stamp(a)} --> {stamp(b)}\n{text}\n')
  ass.append(f'Dialogue: 0,{stamp(a,True)},{stamp(b,True)},Spanish,,0,0,0,,'+text.replace('\n',r'\N'))
 (P/'subtitulos_es.srt').write_text('\n'.join(srt));(P/'subtitulos_es.ass').write_text(header+'\n'.join(ass)+'\n')
def pts():
 expr=str(DURATION)
 for (a,b),(c,d) in reversed(list(zip(POINTS,POINTS[1:]))):expr=f'if(lt(T,{c}),{b}+(T-{a})*{(d-b)/(c-a)},{expr})'
 return expr+'/TB'
def main():
 a=argparse.ArgumentParser();a.add_argument('recording',type=Path);args=a.parse_args();captions()
 # A rounded portrait preserves the full supplied framing, including the character filter.
 mask=Image.new('L',(200,212));ImageDraw.Draw(mask).rounded_rectangle((1,1,198,210),radius=23,fill=255);mask.save(P/'mascara.png')
 border=Image.new('RGBA',(204,216));ImageDraw.Draw(border).rounded_rectangle((0,0,203,215),radius=25,fill=(6,19,28,240),outline=(95,190,180,220),width=2);border.save(P/'borde.png')
 # Conservative voice cleanup and measured two-pass normalization.
 voice='highpass=f=75,lowpass=f=13500,afftdn=nr=7:nf=-48'
 cmd=['ffmpeg','-hide_banner','-nostats','-ss',str(START),'-t',str(DURATION),'-i',str(args.recording),'-af',voice+',loudnorm=I=-16:TP=-1.5:LRA=6:print_format=json','-f','null','-']
 raw=subprocess.run(cmd,stderr=subprocess.PIPE,text=True,check=True).stderr;m=json.loads(re.findall(r'\{[^{}]+\}',raw)[-1])
 norm=f"loudnorm=I=-16:TP=-1.5:LRA=6:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
 run(['-ss',START,'-t',DURATION,'-i',args.recording,'-vn','-af',voice+','+norm+',afade=t=in:d=0.04,afade=t=out:st=119.30:d=0.14','-ar',48000,'-ac',2,'-c:a','pcm_s24le',TMP/'voz.wav'])
 run(['-i',P.parent/'audio_v4/music_raw.wav','-af',f'atempo={120/DURATION},loudnorm=I=-33:TP=-8:LRA=5,afade=t=in:d=1.5,afade=t=out:st={DURATION-2}:d=2','-ar',48000,'-c:a','pcm_s24le',TMP/'piano.wav'])
 run(['-i',TMP/'voz.wav','-i',TMP/'piano.wav','-filter_complex','[0:a]asplit=2[v][sc];[1:a][sc]sidechaincompress=threshold=0.035:ratio=3:attack=25:release=450:makeup=1[m];[v][m]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false:latency=true[a]','-map','[a]','-t',DURATION,'-ar',48000,'-c:a','pcm_s24le',TMP/'mezcla.wav'])
 filters=f"[0:v]setpts='{pts()}',fps=24,trim=duration={DURATION}[bg];[1:v]trim=start={START}:end={END},setpts=PTS-STARTPTS,scale=200:212:flags=lanczos,eq=gamma=1.035:brightness=0.008:saturation=0.96,format=rgb24[face];[face][2:v]alphamerge[portrait];[bg][3:v]overlay=1628:58[b];[b][portrait]overlay=1630:60:shortest=1,fade=t=out:st={DURATION-.4}:d=0.4,format=yuv420p[v]"
 run(['-i',P.parent/'v9_es/pelicula_completa_120s.mp4','-i',args.recording,'-loop',1,'-i',P/'mascara.png','-loop',1,'-i',P/'borde.png','-i',TMP/'mezcla.wav','-filter_complex_threads',2,'-filter_complex',filters,'-map','[v]','-map','4:a','-t',DURATION,'-c:v','libx264','-threads','4','-preset','fast','-crf',20,'-profile:v','baseline','-level:v','4.0','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','160k','-ar',48000,'-movflags','+faststart',P/'video_final.mp4'])
 run(['-i',P/'video_final.mp4','-vf',f'ass={P}/subtitulos_es.ass','-c:v','libx264','-threads','4','-preset','fast','-crf',20,'-profile:v','baseline','-level:v','4.0','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','copy','-movflags','+faststart',P/'video_final_subtitulos.mp4'])
 (P/'montaje.json').write_text(json.dumps({'duration':DURATION,'source_trim':[START,END],'scene_retiming':POINTS,'presenter':{'x':1630,'y':60,'width':200,'height':212,'gamma':1.035,'brightness':.008},'voice_target_lufs':-16,'music_target_lufs_before_ducking':-33,'music':'Tone.js sampled acoustic piano; quiet Rhodes and bass; no percussion, arpeggios or accents','voice_input_measurement_after_cleanup':m,'subtitles':'approved script, phrase timings aligned to recorded activity; manual within-phrase splits'},indent=2,ensure_ascii=False)+'\n')
 print('Corte terminado',flush=True)
if __name__=='__main__':main()

"""Master the revised score and build clean/subtitled portable final movies."""
import json,re,subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile

HERE=Path(__file__).resolve().parent

def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def measure(path):
 p=run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af','loudnorm=I=-28.5:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
 block=re.findall(r'\{\s*"input_i"[\s\S]*?\}',p.stderr)[-1]
 return {k:float(v) for k,v in json.loads(block).items() if k.startswith('input_')}

def main():
 score=json.loads((HERE/'score.json').read_text());duration=score['duration'];reports={}
 for raw,name,target,peak in [('music','musica',-28.5,-12),('fx','acentos',-36,-22)]:
  stats=measure(HERE/f'{raw}_raw.wav');gain=min(target-stats['input_i'],peak-stats['input_tp'])
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/f'{raw}_raw.wav'),'-af',f'volume={gain}dB','-c:a','pcm_s24le',str(HERE/f'{name}.wav')])
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/f'{name}.wav'),'-c:a','aac','-b:a','160k','-movflags','+faststart',str(HERE/f'{name}.m4a')])
  reports[name]={'gain_db':gain,'measurement':measure(HERE/f'{name}.wav')}
  print(name,reports[name]['measurement'],flush=True)
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/'musica.wav'),'-i',str(HERE/'acentos.wav'),'-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0:duration=longest[a]','-map','[a]','-c:a','pcm_s24le',str(HERE/'banda_sonora.wav')])
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/'banda_sonora.wav'),'-c:a','aac','-b:a','192k','-movflags','+faststart',str(HERE/'banda_sonora.m4a')])
 # An audition copy has listening loudness, while the film retains its quiet bed.
 m=reports['musica']['measurement'];g=min(-18-m['input_i'],-2-m['input_tp'])
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/'musica.wav'),'-af',f'volume={g}dB','-c:a','aac','-b:a','192k','-movflags','+faststart',str(HERE/'musica_escucha.m4a')])
 visual=HERE.parent/'v9_es/pelicula_completa_120s.mp4'
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(visual),'-i',str(HERE/'banda_sonora.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-profile:a','aac_low','-b:a','160k','-ar','48000','-ac','2','-t',str(duration),'-movflags','+faststart',str(HERE/'video_final.mp4')])
 print('Render de subtítulos',flush=True)
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/'video_final.mp4'),'-vf',f'ass={HERE}/subtitulos_es.ass','-c:v','libx264','-preset','veryfast','-crf','19','-profile:v','baseline','-level:v','4.0','-pix_fmt','yuv420p','-g','48','-bf','0','-refs','1','-threads','2','-c:a','copy','-map_metadata','-1','-color_range','tv','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709','-movflags','+faststart',str(HERE/'video_final_subtitulos.mp4')])
 print('Alternativa WebM',flush=True)
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/'video_final_subtitulos.mp4'),'-vf','scale=1280:720','-c:v','libvpx-vp9','-b:v','0','-crf','29','-deadline','good','-cpu-used','5','-row-mt','1','-threads','2','-g','48','-pix_fmt','yuv420p','-c:a','libopus','-b:a','128k',str(HERE/'video_final_subtitulos.webm')])
 reports['mezcla']={'measurement':measure(HERE/'banda_sonora.wav')}
 assert -34<reports['mezcla']['measurement']['input_i']<-24 and reports['mezcla']['measurement']['input_tp']<-8
 sr,a=wavfile.read(HERE/'banda_sonora.wav');assert sr==48000 and a.shape==(duration*48000,2)
 assert np.max(np.abs(a[-int(.04*sr):].astype(float)/(2**31)))<1e-6
 result={'status':'PASS','duration':duration,'sample_rate':48000,'channels':2,'bits':24,'voiceover_included':False,'stems':reports}
 (HERE/'verificacion_audio.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('Exportación terminada',flush=True)

if __name__=='__main__':main()

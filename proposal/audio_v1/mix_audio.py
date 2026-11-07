"""Master quiet stems, preserve their timing and mux the existing video without re-encoding it."""
import json,re,subprocess,hashlib
from pathlib import Path
import numpy as np
from scipy.io import wavfile

HERE=Path(__file__).resolve().parent

def run(args):
 return subprocess.run(args,check=True,capture_output=True,text=True)

def measure(path):
 p=run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af','loudnorm=I=-30:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
 block=re.findall(r'\{\s*"input_i"[\s\S]*?\}',p.stderr)[-1]
 return {k:float(v) for k,v in json.loads(block).items() if k.startswith('input_')}

def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,sample_rate,channels,width,height,r_frame_rate,nb_frames','-of','json',str(path)]).stdout)

def main():
 reports={}
 for source,name,target,ceiling in [('music','musica',-30,-16),('fx','acentos',-33,-20)]:
  stats=measure(HERE/f'{source}_raw.wav');gain=min(target-stats['input_i'],ceiling-stats['input_tp'])
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/f'{source}_raw.wav'),'-af',f'volume={gain:.6f}dB','-ar','48000','-c:a','pcm_s24le',str(HERE/f'{name}.wav')])
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/f'{name}.wav'),'-c:a','aac','-b:a','160k','-movflags','+faststart',str(HERE/f'{name}.m4a')])
  mastered=measure(HERE/f'{name}.wav');assert mastered['input_tp']<=ceiling+.2
  reports[name]={'objetivo_lufs':target,'ganancia_aplicada_db':round(gain,3),'medicion':mastered,'formato':probe(HERE/f'{name}.wav')}
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/'musica.wav'),'-i',str(HERE/'acentos.wav'),'-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0:duration=longest[a]','-map','[a]','-c:a','pcm_s24le','-ar','48000',str(HERE/'banda_sonora.wav')])
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE/'banda_sonora.wav'),'-c:a','aac','-b:a','192k','-movflags','+faststart',str(HERE/'banda_sonora.m4a')])
 reports['mezcla']={'medicion':measure(HERE/'banda_sonora.wav'),'formato':probe(HERE/'banda_sonora.wav')}
 assert -36<reports['mezcla']['medicion']['input_i']<-25
 assert reports['mezcla']['medicion']['input_tp']<-10
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(HERE.parent/'v8_es/pelicula_completa_108s.mp4'),'-i',str(HERE/'banda_sonora.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','108','-metadata','title=El contexto detrás del número — paisaje sonoro 01','-metadata:s:a:0','language=zxx','-movflags','+faststart',str(HERE/'video_con_sonido.mp4')])
 video=probe(HERE/'video_con_sonido.mp4');assert len(video['streams'])==2
 assert abs(float(video['format']['duration'])-108)<.05
 sr,music=wavfile.read(HERE/'musica.wav');sr2,fx=wavfile.read(HERE/'acentos.wav');sr3,mix=wavfile.read(HERE/'banda_sonora.wav')
 assert sr==sr2==sr3==48000 and music.shape==fx.shape==mix.shape==(5184000,2)
 # In scipy 24-bit PCM is left-justified int32. Quantization error <= 2 LSBs.
 err=np.abs(mix.astype('int64')-music.astype('int64')-fx.astype('int64')).max()
 assert err<=512,err
 assert np.max(np.abs(mix.astype(float)/(2**31)))<1
 ending=mix[-4800:].astype(float)/(2**31)
 ending_peak=float(np.abs(ending).max());assert ending_peak<1e-6
 # The video stream must remain bit-for-bit identical after remuxing.
 def stream_hash(path):
  return run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:v:0','-c','copy','-f','hash','-hash','sha256','-']).stdout.strip()
 original_hash=stream_hash(HERE.parent/'v8_es/pelicula_completa_108s.mp4');output_hash=stream_hash(HERE/'video_con_sonido.mp4')
 assert original_hash==output_hash
 result={'estado':'VERIFICADO','motor':'Tone.js 15.1.22 / Chromium OfflineAudioContext','duracion_segundos':108,'frecuencia_muestreo':48000,'canales':2,'pcm_bits':24,'locucion_incluida':False,'audio_referencia_reutilizado':False,'pistas':reports,'video':video,'video_sin_modificaciones':original_hash==output_hash,'hash_video':output_hash,'error_suma_pcm':int(err),'pico_ultimos_100ms':ending_peak}
 (HERE/'verificacion_audio.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({key:val['medicion'] for key,val in reports.items()},ensure_ascii=False,indent=2),flush=True)
 print('Mezcla y video verificados',flush=True)

if __name__=='__main__':main()

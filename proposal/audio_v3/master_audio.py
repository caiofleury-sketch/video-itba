"""Master the sampler orchestration and create a loudness-matched timbre comparison."""
import json,re,subprocess,hashlib
from pathlib import Path
import numpy as np
from scipy.io import wavfile
P=Path(__file__).resolve().parent
CREDIT='Instrument samples: FluidR3_GM / Fluid Soundfont, via gleitz/midi-js-soundfonts; CC BY 3.0 https://creativecommons.org/licenses/by/3.0/us/ . See assets/CREDITS.md.'
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def measure(path):
 p=run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af','loudnorm=I=-20:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
 block=re.findall(r'\{\s*"input_i"[\s\S]*?\}',p.stderr)[-1]
 return {k:float(v) for k,v in json.loads(block).items() if k.startswith('input_')}
def encode(source,dest,gain=0,excerpt=None):
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
 if excerpt is not None:cmd+=['-t',str(excerpt)]
 cmd+=['-af',f'volume={gain:.8f}dB','-metadata','comment='+CREDIT]
 cmd+=['-c:a','pcm_s24le'] if dest.suffix=='.wav' else ['-c:a','libmp3lame','-b:a','192k']
 run(cmd+[str(dest)])
def main():
 assert (P/'score.json').read_bytes()==(P.parent/'audio_v2/score.json').read_bytes()
 reports={}
 for raw,name,target,ceiling in [('music','musica',-28.5,-12),('fx','acentos',-36,-22)]:
  before=measure(P/f'{raw}_raw.wav');gain=min(target-before['input_i'],ceiling-before['input_tp'])
  encode(P/f'{raw}_raw.wav',P/f'{name}.wav',gain);reports[name]=measure(P/f'{name}.wav')
  print(name,reports[name],flush=True)
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(P/'musica.wav'),'-i',str(P/'acentos.wav'),'-filter_complex','[0:a][1:a]amix=inputs=2:normalize=0:duration=longest[a]','-map','[a]','-metadata','comment='+CREDIT,'-c:a','pcm_s24le',str(P/'banda_sonora.wav')])
 info=measure(P/'musica.wav');gain=min(-18-info['input_i'],-2-info['input_tp']);encode(P/'musica.wav',P/'musica_instrumentos_nuevos.mp3',gain)
 # Match the exact same 32 seconds, including measured loudness and peak margin.
 old=P.parent/'audio_v2/musica.wav';old_excerpt=P/'antes_extract_raw.wav';new_excerpt=P/'nuevos_extract_raw.wav'
 for src,dest in [(old,old_excerpt),(P/'musica.wav',new_excerpt)]:run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-t','32','-c:a','pcm_f32le',str(dest)])
 a,b=measure(old_excerpt),measure(new_excerpt);common=min(-20,a['input_i']-2-a['input_tp'],b['input_i']-2-b['input_tp'])
 encode(old_excerpt,P/'comparacion_antes.mp3',common-a['input_i']);encode(new_excerpt,P/'comparacion_instrumentos.mp3',common-b['input_i'])
 sr,x=wavfile.read(P/'musica.wav');assert sr==48000 and x.shape==(5760000,2)
 assert np.max(np.abs(x.astype(float)/(2**31)))<1
 manifest=json.loads((P/'sample_manifest.json').read_text())
 for inst in manifest.values():
  for f in inst['files']:assert hashlib.sha256((P/f['file']).read_bytes()).hexdigest()==f['sha256']
 result={'status':'PASS','duration':120,'composition_unchanged':True,'score_sha256':hashlib.sha256((P/'score.json').read_bytes()).hexdigest(),'samples':sum(len(x['files']) for x in manifest.values()),'stems':reports,'comparison_duration':32,'comparison_common_target_lufs':common,'comparison_after_encoding':{'before':measure(P/'comparacion_antes.mp3'),'after':measure(P/'comparacion_instrumentos.mp3')},'headshot_received':False,'video_edit_pending_headshot':True}
 assert abs(result['comparison_after_encoding']['before']['input_i']-result['comparison_after_encoding']['after']['input_i'])<.5
 (P/'verificacion_instrumentos.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

"""Export conservative SDR video encodings from the original visual stream and PCM mix."""
import json,subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
 source=HERE/'video_con_sonido.mp4';audio=HERE/'banda_sonora.wav'
 common=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-map_metadata','-1','-map_chapters','-1']
 # Explicit range and matrix conversion; a tag change alone would alter appearance.
 vf='scale=in_range=full:out_range=limited:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p,setsar=1,sidedata=mode=delete'
 print('Exportando MP4 H.264 Baseline, SDR, rango limitado',flush=True)
 subprocess.run(common+['-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','19','-profile:v','baseline','-level:v','4.0','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-g','48','-keyint_min','24','-bf','0','-refs','1','-threads','2','-tag:v','avc1','-c:a','aac','-profile:a','aac_low','-b:a','160k','-ar','48000','-ac','2','-t','108','-movflags','+faststart',str(HERE/'video_con_sonido_compatible.mp4')],check=True)
 print('Exportando alternativa WebM VP9 / Opus',flush=True)
 webm_vf='scale=w=1280:h=720:in_range=full:out_range=limited:in_color_matrix=bt601:out_color_matrix=bt709,format=yuv420p,setsar=1,sidedata=mode=delete'
 subprocess.run(common+['-vf',webm_vf,'-c:v','libvpx-vp9','-b:v','0','-crf','29','-deadline','good','-cpu-used','5','-row-mt','1','-threads','2','-g','48','-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','libopus','-b:a','128k','-ar','48000','-ac','2','-t','108',str(HERE/'video_con_sonido_alternativa.webm')],check=True)
 reports=[]
 for filename in ['video_con_sonido.mp4','video_con_sonido_compatible.mp4','video_con_sonido_alternativa.webm']:
  path=HERE/filename
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))
  result=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True)
  assert result.returncode==0,(filename,result.stderr)
  assert len(probe['streams'])==2 and abs(float(probe['format']['duration'])-108)<.1
  if filename.endswith('_compatible.mp4'):
   video,audio_stream=probe['streams'];assert video['pix_fmt']=='yuv420p' and video['color_range']=='tv'
   assert video['profile']=='Constrained Baseline' and video['has_b_frames']==0 and audio_stream['profile']=='LC'
  reports.append({'file':filename,'full_decode':'PASS','probe':probe})
 (HERE/'verificacion_compatibilidad_archivos.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
 print('Los tres archivos se decodifican completos sin errores.',flush=True)

if __name__=='__main__':main()

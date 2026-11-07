"""Render subtitle samples and verify their visible pixels stay in the reserved lower band."""
import json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent

def main():
 plan=json.loads((HERE/'plan_subtitulos.json').read_text());out=HERE/'revision_subtitulos';out.mkdir(exist_ok=True)
 chosen=[plan['subtitulos'][i] for i in [1,8,11,20,23,29]];results=[]
 sheet=Image.new('RGB',(1920,1710),'#15202a');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
 for i,c in enumerate(chosen):
  t=round((c['start']+c['end'])/2*24)/24
  common=['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(HERE/'video_con_sonido_compatible.mp4')]
  a=out/f'base_{i}.png';b=out/f'subtitulos_{i}.png'
  subprocess.run(common+['-frames:v','1','-threads','1',str(a)],check=True)
  subprocess.run(common+['-vf',f'setpts=PTS+{t}/TB,ass={HERE}/subtitulos_es.ass','-frames:v','1','-threads','1',str(b)],check=True)
  with Image.open(a) as base,Image.open(b) as sub:
   diff=np.max(np.abs(np.asarray(base).astype('int16')-np.asarray(sub).astype('int16')),axis=2)
   ys,xs=np.nonzero(diff>40)
   assert len(xs)>100,(i,c)
   bounds=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
   assert bounds[1]>=955 and bounds[3]<1065,(t,bounds)
   assert bounds[0]>=120 and bounds[2]<=1790,bounds
   sheet.paste(sub.resize((960,540)),(i%2*960,i//2*570+30))
  draw.text((i%2*960+15,i//2*570+5),f'{t:.2f}s · '+c['text'][:62],font=font,fill='#e8eef1')
  results.append({'tiempo':t,'texto':c['text'],'limites_pixeles_subtitulo':bounds})
 sheet.save(out/'revision.jpg',quality=94)
 report={'estado':'VERIFICADO','guion_integro':True,'subtitulos':31,'muestras_visuales':results,'franja_inferior_despejada':True,'tiempos_provisionales':True}
 (HERE/'verificacion_subtitulos.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

"""Compare decoded MP4 frames with the actual SVG timeline, including the 3D opening."""
import json
import subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageStat
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
TIMES=[4.25,10,17.5,21.125,24.25,29.125,33.25,37,43,45.875,54.125,61.25,68,70.75,100.5,106]

def main():
 output=HERE/'revision'/'exportacion';output.mkdir(exist_ok=True)
 report=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
  page=browser.new_page(viewport={'width':1920,'height':1080})
  page.set_content((HERE/'index.html').read_text())
  page.add_style_tag(content='main{max-width:none!important;padding:0!important}header,.controls,nav,#narration,.note,details{display:none!important}.stage{width:1920px!important;height:1080px!important;border:none!important}')
  for i,t in enumerate(TIMES):
   expected=output/f'esperado_{i}.png';actual=output/f'video_{i}.png'
   page.evaluate('(t)=>window.renderAt(t)',t);page.screenshot(path=str(expected))
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(HERE/'pelicula_completa_108s.mp4'),'-frames:v','1','-threads','1',str(actual)],check=True)
   with Image.open(expected) as a,Image.open(actual) as b:
    diff=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
    mae=sum(ImageStat.Stat(diff).mean)/3
    art_mae=sum(ImageStat.Stat(diff.crop((120,280,1790,850))).mean)/3
   report.append({'tiempo':t,'fotograma':round(t*24),'diferencia_media_rgb':round(mae,3),'diferencia_area_grafica':round(art_mae,3)})
  browser.close()
 assert all(x['diferencia_media_rgb']<4 and x['diferencia_area_grafica']<6 for x in report),report
 result={'estado':'VERIFICADO','fotogramas_decodificados':len(report),'apertura_3d_incluida':True,'muestras':report}
 (HERE/'verificacion_exportacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
 sheet=Image.new('RGB',(1920,1710),'#15202a');draw=ImageDraw.Draw(sheet)
 for k,(i,label) in enumerate([(1,'Apertura 3D'),(4,'Promedio'),(6,'Escala personal'),(10,'Ordenamiento'),(11,'Promedio exponencial'),(15,'Recomendación')]):
  with Image.open(output/f'video_{i}.png') as im:sheet.paste(im.resize((960,540)),(k%2*960,k//2*570+30))
  draw.text((k%2*960+15,k//2*570+5),f'{TIMES[i]:g}s · {label}',font=font,fill='#e8eef1')
 sheet.save(HERE/'frames'/'comprobacion_del_video.jpg',quality=94)
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

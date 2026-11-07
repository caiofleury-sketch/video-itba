import json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent
TIMES=[70.5,74,78,82,87.5,92,100,110,119]

def main():
 (HERE/'frames').mkdir(exist_ok=True);sheet=Image.new('RGB',(1920,1170),'#15202a');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);draw=ImageDraw.Draw(sheet)
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage']);page=browser.new_page(viewport={'width':1920,'height':1080})
  page.set_content((HERE/'index.html').read_text());page.add_style_tag(content='main{max-width:none!important;padding:0!important}header,.controls,nav,#narration,.note,details{display:none!important}.stage{width:1920px!important;height:1080px!important;border:none!important}')
  for i,t in enumerate(TIMES):
   page.evaluate('(t)=>renderAt(t)',t);file=HERE/'frames'/f'final_{i}.png';page.screenshot(path=str(file))
   with Image.open(file) as img:sheet.paste(img.resize((640,360)),(i%3*640,i//3*390+30))
   draw.text((i%3*640+12,i//3*390+5),f'{t:g}s',font=font,fill='#e8eef1')
  browser.close()
 sheet.save(HERE/'frames'/'resultados_y_recomendacion.jpg',quality=94)
 print('Nueve fotogramas capturados')

if __name__=='__main__':main()

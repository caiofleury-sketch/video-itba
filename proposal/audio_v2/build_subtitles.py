"""Caption the Spanish script with provisional scene/feature timings and burn a review copy."""
import json,re,textwrap,subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent

PHRASES={
 'question':[
  'Mismo saldo. ¿Misma historia?',
  'En un cliente, el saldo se mantiene estable.',
  'En otro, acaba de caer.',
  'La foto del mes oculta esa diferencia.',
  'Creamos variables para revelar',
  'el contexto detrás del número.'
 ],
 'comparison':[
  'Ahora, el resultado público.',
  'El modelo original obtuvo 343,5 millones de pesos.',
  'Al incorporar fondos relativos de tres meses,',
  'la receta alcanzó 401,9 millones:',
  '58,4 millones más.',
  'Extenderla a seis meses dio 392,8 millones,',
  'unos 9,1 millones menos que el control.',
  'Entre estas recetas, más historia no fue mejor.'
 ],
 'takeaway':[
  'Por eso, recomendamos agregar',
  'los cambios relativos de saldo y haberes',
  'contra su promedio de tres meses,',
  'junto con sus dos indicadores',
  'de escala casi nula.',
  'Conservamos las cuatro variables del control;',
  'no sumamos la extensión de seis meses.'
 ]
}

def wrap(text):
 if len(text)<=46:return text
 words=text.split();possibilities=[]
 for i in range(1,len(words)):
  a,b=' '.join(words[:i]),' '.join(words[i:])
  if len(a)<=46 and len(b)<=46:possibilities.append((abs(len(a)-len(b)),a,b))
 assert possibilities,text
 _,a,b=min(possibilities)
 return a+'\n'+b

def stamp(t,ass=False):
 units=100 if ass else 1000;n=round(t*units);h,n=divmod(n,3600*units);m,n=divmod(n,60*units);s,n=divmod(n,units)
 return f'{h}:{m:02}:{s:02}.{n:02}' if ass else f'{h:02}:{m:02}:{s:02},{n:03}'

def build():
 data=json.loads((HERE.parent/'v9_es/data.json').read_text());captions=[]
 def add(phrases,start,end,scene):
  weights=[len(x.split()) for x in phrases];total=sum(weights);elapsed=0
  for text,w in zip(phrases,weights):
   a=start+(end-start)*elapsed/total+.04;elapsed+=w;b=start+(end-start)*elapsed/total-.04
   captions.append({'start':round(a,3),'end':round(b,3),'text':text,'lines':wrap(text),'scene':scene})
 for scene in data['scenes']:
  if scene['id']=='features':
   sentences=[x+'.' for x in scene['voiceover'].rstrip('.').split('. ')];assert len(sentences)==9
   for i,line in enumerate(sentences):
    phrases=[line]
    if i==3:phrases=['Los cambios relativos de saldo y haberes','comparan el presente con la historia de cada cliente.']
    if i==4:phrases=['La utilización de tarjeta relaciona el saldo','con el límite disponible.']
    if i==6:phrases=['El uso relativo compara las operaciones con la actividad habitual,','buscando señales de desinterés.']
    assert ' '.join(phrases)==line
    start=scene['start']+data['feature_beats'][i];end=scene['start']+data['feature_beats'][i+1] if i<8 else 65
    add(phrases,start,end,scene['id'])
  else:
   phrases=PHRASES[scene['id']];assert ' '.join(phrases)==scene['voiceover'];add(phrases,scene['start'],scene['end'],scene['id'])
 expected=' '.join(s['voiceover'] for s in data['scenes']);actual=' '.join(c['text'] for c in captions)
 assert actual==expected
 assert all(0<=c['start']<c['end']<=120 and len(c['lines'].splitlines())<=2 for c in captions)
 assert all(a['end']<=b['start'] for a,b in zip(captions,captions[1:]))
 assert max(len(c['text'])/(c['end']-c['start']) for c in captions)<23
 srt='\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["lines"]}' for i,c in enumerate(captions))+'\n'
 (HERE/'subtitulos_es.srt').write_text(srt)
 header='''[Script Info]
Title: El contexto detrás del número — guion en español
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Spanish,Liberation Sans,38,&H00F1EEE8,&H00F1EEE8,&H60000000,&H60000000,0,0,0,0,100,100,0,0,3,3,0,2,120,120,24,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
 events=[]
 for c in captions:
  text=c['lines'].replace('\n',r'\N');events.append(f'Dialogue: 0,{stamp(c["start"],True)},{stamp(c["end"],True)},Spanish,,0,0,0,,{text}')
 (HERE/'subtitulos_es.ass').write_text(header+'\n'.join(events)+'\n')
 report={'idioma':'es-AR','sincronizacion':'PROVISIONAL: guion y tiempos de escena; no hay locución grabada','guion_integro':True,'palabras':len(re.findall(r'\b\w+\b',expected)),'cantidad_subtitulos':len(captions),'maximo_caracteres_por_segundo':round(max(len(c['text'])/(c['end']-c['start']) for c in captions),2),'maximo_lineas':2,'subtitulos':captions}
 (HERE/'plan_subtitulos.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(f'{len(captions)} subtítulos; guion íntegro; {report["palabras"]} palabras.',flush=True)
 return captions

if __name__=='__main__':build()

"""Fetch only the score's required FluidR3 GM notes, retaining source and license provenance."""
import urllib.request,re,json,concurrent.futures,base64,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
BANKS={'piano':('acoustic_grand_piano',['lead']),'rhodes':('electric_piano_1',['ep','pad']),'bass':('electric_bass_finger',['bass']),'nylon':('acoustic_guitar_nylon',['arp']),'vibes':('vibraphone',['glint'])}
SEMITONES={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def midi(name):
 m=re.fullmatch(r'([A-G])([#b]?)(-?\d+)',name)
 return (int(m[3])+1)*12+SEMITONES[m[1]]+{'#':1,'b':-1,'':0}[m[2]]
def main():
 score=json.loads((P/'score.json').read_text())
 def fetch(item):
  name,(instrument,voices)=item;url=f'https://raw.githubusercontent.com/gleitz/midi-js-soundfonts/gh-pages/FluidR3_GM/{instrument}-mp3.js'
  raw=urllib.request.urlopen(url,timeout=45).read();text=raw.decode();start=text.index('{',text.index('MIDI.Soundfont.'));end=text.rfind('}')+1
  obj=re.sub(r',\s*}', '}',text[start:end]);data=json.loads(obj);lookup={midi(k):(k,v) for k,v in data.items()}
  needed={midi(e['pitch']) for e in score['music']+score['fx'] if e['voice'] in voices};folder=P/'assets'/name;folder.mkdir(parents=True,exist_ok=True);urls={};files=[]
  for n in sorted(needed):
   key,encoded=lookup[n];b=base64.b64decode(encoded.split(',',1)[1]);f=folder/f'M{n}.mp3';f.write_bytes(b)
   urls[key]=f'assets/{name}/M{n}.mp3';files.append({'note':key,'midi':n,'file':str(f.relative_to(P)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
  return name,{'instrument':instrument,'source':url,'bank_sha256':hashlib.sha256(raw).hexdigest(),'license':'CC-BY-3.0','urls':urls,'files':files}
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:result=dict(pool.map(fetch,BANKS.items()))
 (P/'sample_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:{'samples':len(v['files']),'bytes':sum(x['bytes'] for x in v['files'])} for k,v in result.items()},indent=2))
if __name__=='__main__':main()

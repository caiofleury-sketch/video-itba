"""Check technical continuity of the composed music without claiming a perceptual music review."""
import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
P=Path(__file__).resolve().parent

def main():
 sr,x=wavfile.read(P/'musica.wav');x=x.astype(float)/(2**31);assert sr==48000 and x.shape==(5760000,2)
 jumps=np.max(np.abs(np.diff(x,axis=0)),axis=1);threshold=max(.012,float(np.percentile(jumps,99.99))*2)
 seams=[]
 for t in [16,32,48,64,80,96,112]:
  n=round(t*sr);jump=float(np.max(np.abs(x[n]-x[n-1])));assert jump<threshold,(t,jump,threshold)
  seams.append({'time':t,'adjacent_sample_jump':round(jump,7)})
 rms=[]
 for t in range(1,118):
  block=x[t*sr:(t+1)*sr];v=float(np.sqrt(np.mean(block**2)));assert v>1e-6,(t,v);rms.append(v)
 stereo=20*np.log10(np.sqrt(np.mean(x[:,0]**2))/np.sqrt(np.mean(x[:,1]**2)));assert abs(stereo)<3
 score=json.loads((P/'score.json').read_text());assert score['bpm']==120 and score['duration']==120
 assert {e['voice'] for e in score['music']}=={'lead','pulse','ep','pad','arp','bass','kick','rim','hat'}
 result={'status':'PASS','duration':120,'bpm':120,'bars':60,'melody_sections':['A','B','reduced_results','recapitulation','written_cadence'],'music_notes':len(score['music']),'fx_notes':len(score['fx']),'layer_count':9,'silent_gaps_detected':False,'stereo_balance_db':round(float(stereo),3),'window_boundary_samples':seams,'scope':'Technical continuity, layer presence and measured signal levels; not a substitute for listening preferences.'}
 (P/'verificacion_continuidad_musical.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

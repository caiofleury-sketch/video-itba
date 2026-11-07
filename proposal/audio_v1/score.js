/* Original score. Seconds share the animation's clock; no reference audio is reused. */
(function(root){
'use strict';
function createScore(data){
 const bpm=96,beat=60/bpm,music=[],fx=[],cues=[];
 const note=(out,voice,time,pitch,duration=.14,velocity=.35,pan=0)=>out.push({voice,time:+time.toFixed(5),pitch,duration,velocity,pan});
 const cue=(time,label,feature,notes)=>{
  const id='cue_'+String(cues.length+1).padStart(2,'0');
  cues.push({id,time:+time.toFixed(3),label,feature});
  notes.forEach(([dt,pitch,voice='chip',duration=.11,velocity=.32,pan=0])=>{
   note(fx,voice,time+dt,pitch,duration,velocity,pan);fx[fx.length-1].cue=id;
  });
 };
 // A three-note question (D-E-A) becomes a four-note answer (D-E-A-D).
 // Reuse and transformation provide continuity, as in an adaptive game score.
 const harmonies={
  d:{notes:['D3','F3','A3','E4'],bass:'D2'},
  g:{notes:['G2','D3','E3','B3'],bass:'G2'},
  c:{notes:['C3','E3','G3','D4'],bass:'C2'},
  a:{notes:['A2','E3','G3','C4'],bass:'A2'}
 };
 const blocks=[[0,8,'d'],[8,16,'g'],[16,26,'d'],[26,36,'g'],[36,46,'c'],[46,56,'a'],[56,65,'d'],[65,70,'d'],[70,78,'d'],[78,86,'c'],[86,94,'a'],[94,99,'d'],[99,104,'g'],[104,108,'d']];
 for(const [start,end,key] of blocks){
  const h=harmonies[key],duration=Math.max(.4,end-start-1.0);
  h.notes.forEach((p,i)=>note(music,'pad',start+i*.014,p,duration,start>=70&&start<94?.25:.30));
  for(let t=start+.08;t<end-1;t+=4*beat){
   note(music,'bass',t,h.bass,.32,start<16?.32:.42);
  }
 }
 const phrase=(start,notes,velocity=.24,step=1.25)=>notes.forEach((p,i)=>{
  if(start+i*step<105)note(music,'pluck',start+i*step,p,.18,velocity,i%2?-.12:.12);
 });
 // The same question returns, but never as a continuous lead over speech.
 phrase(10.2,['D4','E4','A4'],.20);
 phrase(17.1,['D4','E4','A4'],.18);
 phrase(27.9,['D4','E4','A4'],.17);
 phrase(38.1,['E4','A4','D4'],.18);
 phrase(48.2,['A4','E4','D4'],.17);
 phrase(57.4,['D4','E4','A4'],.16);
 // The results section deliberately loses the melody. Rebuild it with the
 // four new variables at the end; a quiet octave settles the opening question.
 phrase(94.9,['D4','E4','A4','D5'],.18);
 phrase(100.7,['D4','E4','A4','D5'],.20,.8);
 cue(.6,'Dos saldos iguales comparten la misma nota','apertura',[[0,'D4','glass',.22,.24,-.3],[.5,'D4','glass',.22,.24,.3]]);
 cue(2.6,'La cámara abre la historia','apertura',[[0,'D4','glass',.18,.25,-.15]]);
 cue(3.3,'Se separan los planos del pasado','apertura',[[0,'D4','chip',.12,.22,-.25],[.30,'E4','chip',.12,.22],[.60,'A4','chip',.14,.22,.25]]);
 cue(8.8,'Dos referencias personales, dos historias','apertura',[[0,'F4','glass',.24,.25,-.3],[.24,'A4','glass',.25,.25,.3]]);
 const starts=data.feature_beats.map(x=>16+x),ids=data.rows.map(x=>x.id);
 starts.forEach((start,i)=>{
  cue(start+.08,'Entrada: '+data.rows[i].label,ids[i],[[0,['D4','F4','A4','D4','E4','D4','G4','E4','A4'][i],'chip',.13,.25]]);
 });
 cue(starts[0]+1.8,'El valor anterior llega a su nueva posición',ids[0],[[0,'D4','pluck',.12,.3],[.16,'D4','pluck',.2,.26]]);
 cue(starts[1]+.45,'Se revela el descenso mensual',ids[1],[[0,'A4','chip',.10,.24],[.24,'E4','chip',.10,.22],[.48,'D4','chip',.14,.20]]);
 cue(starts[2]+.35,'Tres observaciones construyen la referencia',ids[2],[[0,'D4','pluck',.12,.24,-.25],[.3,'E4','pluck',.12,.24],[.6,'A4','pluck',.12,.23,.25]]);
 cue(starts[2]+1.8,'La superficie alcanza la media',ids[2],[[0,'D4','glass',.24,.28]]);
 cue(starts[3]+1.8,'La diferencia se expresa a escala personal',ids[3],[[0,'F4','glass',.22,.24]]);
 cue(starts[3]+3.7,'Vuelven los dos clientes de la apertura',ids[3],[[0,'D4','glass',.32,.23,-.3],[0,'F3','glass',.38,.16,-.3],[0,'A3','glass',.38,.14,-.3]]);
 cue(starts[3]+5.1,'La caída y la estabilidad quedan contrastadas',ids[3],[[0,'D4','glass',.32,.23,.3],[0,'G3','glass',.38,.16,.3],[0,'B3','glass',.38,.14,.3]]);
 cue(starts[4]+.3,'El anillo muestra la proporción utilizada',ids[4],[[0,'D4','chip',.10,.17],[.40,'E4','chip',.10,.18],[.8,'G4','chip',.10,.19],[1.2,'A4','chip',.15,.20]]);
 cue(starts[5]+.3,'La referencia incorpora seis meses',ids[5],['D4','F4','A4','C5','E5','A4'].map((n,i)=>[i*.21,n,'pluck',.10,.18,-.25+i*.1]));
 cue(starts[6]+.25,'La actividad deja seis posiciones vacías',ids[6],['A4','G4','F4','E4','D4','D4'].map((n,i)=>[i*.23,n,'chip',.08,.18-i*.015]));
 cue(starts[7]+.45,'Los valores recorren carriles para ordenarse',ids[7],[[0,'E4','chip',.12,.20,-.3],[.5,'G4','chip',.12,.22],[1,'A4','chip',.12,.22,.3]]);
 cue(starts[7]+2.4,'El orden queda establecido',ids[7],[[0,'D5','glass',.19,.24]]);
 cue(starts[8]+.2,'Las observaciones recientes pesan más',ids[8],['D4','E4','F4','G4','A4','B4'].map((n,i)=>[i*.26,n,'pluck',.1,.10+i*.025,-.25+i*.1]));
 cue(65,'Las nueve familias forman un mapa','vista_general',[[0,'D4','glass',.18,.2],[.13,'A4','glass',.18,.18],[.26,'E5','glass',.18,.16]]);
 cue(70,'Entrada a la comparación de ganancia','comparacion',[[0,'D4','glass',.24,.18],[.22,'A4','glass',.22,.14]]);
 // No victory stinger or row sonification: these profits remain unverified.
 for(let i=0;i<4;i++){
  cue(94+.25+i*.45,'Aparece la variable recomendada '+(i+1),'recomendacion',[[0,['D4','E4','A4','D5'][i],'chip',.12,.23,i<2?-.2:.2]]);
  cue(94+3.8+i*.45,'La variable '+(i+1)+' añade una capa al modelo','recomendacion',[[0,['D4','E4','A4','D5'][i],'glass',.18,.24]]);
 }
 cue(100.5,'Las cuatro variables quedan incorporadas','recomendacion',[[0,'D4','glass',.3,.20],[.20,'E4','glass',.28,.18],[.40,'A4','glass',.28,.17],[.60,'D5','glass',.42,.20]]);
 return {title:'El contexto detrás del número · paisaje sonoro 01',duration:data.duration,sampleRate:48000,bpm,scale:'Re dórico',music:music.sort((a,b)=>a.time-b.time),fx:fx.sort((a,b)=>a.time-b.time),cues:cues.sort((a,b)=>a.time-b.time),sections:data.scenes.map(({id,start,end,label})=>({id,start,end,label}))};
}
root.createScore=createScore;
if(typeof module!=='undefined')module.exports={createScore};
})(typeof window!=='undefined'?window:globalThis);

/* Original 16-bit exploration cue: fully notated melody, harmony, bass and light kit. */
(function(root){'use strict';
function createScore(data){
 const music=[],fx=[],cues=[],bpm=120,beat=.5,bar=2;
 const add=(out,voice,time,pitch,duration,velocity=.5,pan=0)=>out.push({voice,time:+time.toFixed(5),pitch,duration:+duration.toFixed(5),velocity,pan});
 const chords={
  Eb:{root:'Eb2',fifth:'Bb2',approach:'D2',voicing:['G3','Bb3','D4','F4']},
  Gm:{root:'G2',fifth:'D3',approach:'B2',voicing:['F3','Bb3','D4','G4']},
  Cm:{root:'C2',fifth:'G2',approach:'G2',voicing:['Eb3','G3','Bb3','D4']},
  Ab:{root:'Ab2',fifth:'Eb3',approach:'E2',voicing:['G3','Bb3','C4','Eb4']},
  Fm:{root:'F2',fifth:'C3',approach:'A2',voicing:['Ab3','C4','Eb4','G4']},
  Bb:{root:'Bb2',fifth:'F3',approach:'F2',voicing:['Ab3','C4','D4','G4']},
  EbG:{root:'G2',fifth:'Bb2',approach:'A2',voicing:['G3','Bb3','Eb4','F4']},
  Bbs:{root:'Bb2',fifth:'F3',approach:'D2',voicing:['Ab3','C4','Eb4','F4']}
 };
 const A=[
  [[0,'Eb4',.75],[1,'G4',.5],[1.75,'Bb4',.75],[3,'G4',.5]],
  [[0,'F4',.5],[.75,'G4',.5],[1.5,'Bb4',.5],[2,'D5',.75],[3.25,'Bb4',.5]],
  [[0,'C5',.75],[1,'Bb4',.5],[1.75,'G4',.75],[3,'Eb4',.75]],
  [[0,'F4',.75],[1,'Ab4',.5],[1.75,'G4',.75],[3,'Eb4',.5],[3.5,'D4',.4]],
  [[0,'F4',.75],[1,'Ab4',.5],[1.75,'C5',.75],[3,'Bb4',.5]],
  [[0,'Ab4',.5],[.75,'G4',.5],[1.5,'F4',.75],[2.5,'D4',.5],[3.25,'F4',.5]],
  [[0,'G4',.75],[1,'Bb4',.5],[1.75,'Eb5',.75],[3,'D5',.6]],
  [[0,'C5',.5],[.75,'Bb4',.75],[2,'F4',.6],[3,'D4',.7]]
 ];
 const B=[
  [[0,'Ab4',1.25],[1.5,'C5',.5],[2.25,'Eb5',.75],[3.25,'D5',.5]],
  [[0,'C5',.75],[1,'Bb4',.75],[2,'Ab4',.5],[3,'F4',.75]],
  [[0,'G4',.75],[1,'Bb4',.5],[1.75,'D5',1],[3,'Bb4',.75]],
  [[0,'G4',.5],[.75,'Eb4',.75],[1.75,'G4',.5],[2.5,'C5',1]],
  [[0,'Ab4',.75],[1,'G4',.5],[1.75,'F4',1],[3,'Eb4',.5]],
  [[0,'D4',.5],[.75,'F4',.5],[1.5,'Ab4',.75],[2.5,'C5',.5],[3.25,'Bb4',.5]],
  [[0,'G4',.75],[1,'Bb4',.75],[2,'G4',.5],[3,'F4',.75]],
  [[0,'Eb4',1],[1.5,'F4',.5],[2.5,'D4',1]]
 ];
 const progressionA=['Eb','Gm','Cm','Ab','Fm','Bb','EbG','Bbs'];
 const progressionB=['Ab','Bb','Gm','Cm','Fm','Bb','Eb','Bbs'];
 const structure=[];
 function arrange(start,bars,kind,level=1){
  const theme=kind==='B'?B:A,prog=kind==='B'?progressionB:progressionA;
  for(let k=0;k<bars;k++){
   const time=start+k*bar,c=chords[prog[k%8]],results=time>=70&&time<102,closing=time>=102;
   structure.push({time,chord:prog[k%8],section:kind,melody:!results||k%2===0});
   // Syncopated, voiced electric piano. Short rolls humanize the attacks.
   [0,2.5].forEach((at,j)=>c.voicing.forEach((p,i)=>add(music,'ep',time+at*beat+i*.009,p,.56,j?.34*level:.46*level,-.12)));
   // Long air under the progression rather than one isolated sine tone.
   [c.voicing[0],c.voicing[2],c.voicing[3]].forEach((p,i)=>add(music,'pad',time+.04+i*.01,p,1.55,.24*level,.12));
   // A root/fifth/approach bass line articulates the groove and voice leading.
   const bassEvents=results?[[0,c.root,.65],[2.5,c.fifth,.4]]:[[0,c.root,.7],[1.5,c.fifth,.4],[2,c.root,.4],[3.5,chords[prog[(k+1)%8]].root,.35]];
   bassEvents.forEach(([at,p,d],i)=>add(music,'bass',time+at*beat,p,d*beat,(i===0?.62:.43)*level));
   // The arpeggio is an accompaniment, not the main theme. Omit alternate
   // eighths in the opening and the financial explanation to leave breathing room.
   const arpSteps=results?[1,5]:start===0?[1,3,5]:[0,1,2,4,5,6];
   arpSteps.forEach((step,i)=>{
    const p=c.voicing[[0,2,1,3,2,1][i%6]];
    add(music,'arp',time+step*.25+.014,p,.12,(i%2?.24:.29)*level,i%2?.2:-.2);
   });
   if(!results||k%2===0){
    const line=results?theme[k%8].filter((_,i)=>i%2===0):theme[k%8];
    line.forEach(([at,p,d],i)=>{
     // Theme A' moves the last answer up an octave only in the coda.
     const note=closing&&k===6&&i===0?'Eb5':p;
     add(music,'lead',time+at*beat,note,d*beat*.92,(results?.32:.48)*level);
     add(music,'pulse',time+at*beat+.005,note,d*beat*.9,(results?.21:.34)*level);
    });
   }
   // Feather-light kick and rim: a gentle pocket, no heavy snare or arcade alarm.
   if(time>=8&&!results){
    [0,2].forEach(at=>add(music,'kick',time+at*beat,'C2',.08,.42*level));
    [1,3].forEach(at=>add(music,'rim',time+at*beat+.006,'C4',.035,.32*level));
    if(time>=16)[.5,1.5,2.5,3.5].forEach((at,i)=>add(music,'hat',time+at*beat,'C5',.025,(i%2?.18:.13)*level));
   }
  }
 }
 arrange(0,8,'A',.95);arrange(16,8,'A',.82);arrange(32,8,'B',.82);arrange(48,8,'A',.8);
 arrange(64,3,'B',.72);arrange(70,8,'A',.72);arrange(86,8,'B',.7);arrange(102,8,'A',.85);
 // A composed two-second cadence instead of cutting off a looping pattern.
 const final=118;
 ['Eb3','G3','Bb3','D4','F4'].forEach((p,i)=>add(music,'ep',final+i*.025,p,1.25,.44));
 ['Eb4','G4','Bb4'].forEach((p,i)=>add(music,'pad',final+.04+i*.018,p,1.1,.28));
 add(music,'lead',118,'Eb5',1.2,.43);add(music,'pulse',118.005,'Eb5',1.15,.25);add(music,'bass',118,'Eb2',1.1,.55);
 const cue=(time,label,notes)=>{
  const id='cue_'+String(cues.length+1).padStart(2,'0');cues.push({id,time,label});
  notes.forEach(([dt,p,d=.1,v=.35])=>{add(fx,'glint',time+dt,p,d,v);fx[fx.length-1].cue=id});
 };
 const st=data.feature_beats.map(x=>16+x);
 cue(2.6,'La historia se despliega',[[0,'Eb5'],[.18,'Bb5',.12,.26]]);
 cue(st[0]+1.8,'El rezago llega a su posición',[[0,'Bb4'],[.16,'Bb4',.1,.22]]);
 cue(st[2]+1.8,'Las observaciones forman una media',[[0,'Eb5'],[.1,'G5',.1,.28],[.2,'Bb5',.13,.22]]);
 cue(st[3]+5.1,'El contexto distingue a los dos clientes',[[0,'G5',.14,.22]]);
 cue(st[4]+1.8,'La proporción del anillo queda visible',[[0,'Bb4',.12,.28]]);
 cue(st[5]+1.8,'La referencia se extiende a seis meses',[[0,'C5',.12,.24]]);
 cue(st[6]+1.8,'La actividad se reduce',[[0,'F4',.1,.22]]);
 cue(st[7]+2.4,'Los valores quedan ordenados',[[0,'G4'],[.09,'Bb4'],[.18,'Eb5',.13,.25]]);
 cue(st[8]+1.8,'Se forma la referencia ponderada',[[0,'Bb4',.1,.22]]);
 cue(65,'Las familias forman un mapa',[[0,'Eb5'],[.15,'G5',.12,.22]]);
 [73,80,90].forEach((t,i)=>cue(t,'Se revela el resultado público '+(i+1),[[0,['Eb4','G4','F4'][i],.16,.25]]));
 for(let i=0;i<4;i++)cue(105.8+i*.45,'La variable '+(i+1)+' se incorpora al modelo',[[0,['Eb4','G4','Bb4','D5'][i],.12,.22]]);
 const events=[...music,...fx];
 if(events.some(e=>e.time<0||e.time+e.duration>=data.duration))throw Error('Event outside the film');
 return {title:'Contexto · exploración 16-bit',duration:data.duration,sampleRate:48000,bpm,key:'Mi bemol mayor',music:music.sort((a,b)=>a.time-b.time),fx:fx.sort((a,b)=>a.time-b.time),cues:cues.sort((a,b)=>a.time-b.time),structure,sections:data.scenes.map(({id,start,end,label})=>({id,start,end,label}))};
}
root.createScore=createScore;if(typeof module!=='undefined')module.exports={createScore};
})(typeof window!=='undefined'?window:globalThis);

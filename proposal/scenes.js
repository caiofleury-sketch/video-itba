'use strict';
const {data: D, scenes: SCENES} = JSON.parse(document.getElementById('payload').textContent);
const C = {bg:'#0b0f14', ink:'#e8eef1', muted:'#98a8b7', line:'#30404d', teal:'#70d4bc', blue:'#76aafa', amber:'#f2bd75', red:'#ed8793'};
const escapeText = v => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const clamp = v => Math.max(0, Math.min(1, v));
const ease = v => {v=clamp(v);return v*v*(3-2*v)};
const reveal = (t, start, body, duration=.6) => `<g opacity="${ease((t-start)/duration)}" transform="translate(0 ${12*(1-ease((t-start)/duration))})">${body}</g>`;
const text = (x,y,value,size=32,color=C.ink,anchor='start',extra='') => `<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" ${extra}>${escapeText(value)}</text>`;
const line = (x1,y1,x2,y2,color=C.line,width=2,extra='') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
const circle = (x,y,r=7,color=C.teal,extra='') => `<circle cx="${x}" cy="${y}" r="${r}" fill="${color}" ${extra}/>`;
const rect = (x,y,w,h,color=C.line,extra='') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${color}" ${extra}/>`;
const arrow = (x1,y1,x2,y2,color=C.teal) => line(x1,y1,x2,y2,color,3)+`<path d="M${x2-13} ${y2-10} L${x2} ${y2} L${x2-13} ${y2+10}" fill="none" stroke="${color}" stroke-width="3"/>`;
const footer = value => line(120,866,1790,866)+text(120,917,value,34,C.ink,'start','data-fit="1660"');
const small = value => text(120,245,value,27,C.muted,'start','data-fit="1410"');

function design(t){
  let s=small('Five additions. One question: what information was missing?');
  const packages=[['Lag 1','Last month',C.blue],['Delta 1','Movement',C.blue],['Prior 3','Usual level',C.blue],['Relative funds','Personal scale',C.teal],['Card utilization','Capacity',C.blue]];
  s+=text(120,364,'Current values',42)+text(120,414,'152 repaired predictors',27,C.muted);
  for(let i=0;i<8;i++)s+=rect(132+i*42,465,15,40+((i*29)%95),C.blue,'opacity=".7"');
  s+=reveal(t,1.5,arrow(540,505,670,505)+text(605,472,'+',46,C.teal,'middle'));
  packages.forEach((p,i)=>{
    const y=348+i*90;
    s+=reveal(t,2+i*.9,circle(755,y-10,7,p[2])+text(785,y,p[0],34,p[2])+text(1170,y,p[1],28,C.muted));
  });
  s+=reveal(t,7.3,text(120,778,'Each package is added separately to the same baseline.',34));
  return s+footer('The comparison measures a package—not an isolated column.');
}

function relative(t){
  let s=small('Illustrative values—not observed customer measurements.');
  const groups=[{x:180,prior:100,current:80,percent:'−20%',scale:2.8},{x:990,prior:1000,current:980,percent:'−2%',scale:.28}];
  groups.forEach((g,i)=>{
    let p=text(g.x,330,`Customer ${i?'B':'A'}`,29,C.muted);
    p+=line(g.x,675,g.x+550,675);
    p+=rect(g.x+55,675-g.prior*g.scale,130,g.prior*g.scale,C.blue,'opacity=".55"');
    p+=text(g.x+120,720,'Prior mean',27,C.muted,'middle');
    p+=text(g.x+120,675-g.prior*g.scale-22,g.prior,32,C.blue,'middle');
    p+=reveal(t,1.2,rect(g.x+280,675-g.current*g.scale,130,g.current*g.scale,C.teal)+text(g.x+345,720,'Current',27,C.muted,'middle')+text(g.x+345,675-g.current*g.scale-22,g.current,32,C.teal,'middle'));
    p+=reveal(t,3.2,text(g.x+235,792,'Same absolute change: −20',29,C.muted,'middle'));
    p+=reveal(t,5,text(g.x+585,555,g.percent,60,C.teal,'middle','font-family="Georgia,serif"'));
    s+=p;
  });
  s+=reveal(t,7.0,text(120,839,'Relative = clip((current − prior mean) / max(|prior mean|, 1), −10, 10)',26,C.muted));
  return s+footer('Compare today with that customer’s own recent history.');
}

function screen(t){
  let s=small('Historical May AUC • same learner settings and training rules • five matched seeds');
  const x=v=>740+(v+.00075)/.0025*860;
  s+=text(120,314,'ADDED PACKAGE',22,C.muted)+text(1690,314,'MEAN Δ AUC',22,C.muted,'end');
  [-.0005,0,.0005,.001,.0015].forEach(v=>{
    s+=line(x(v),338,x(v),746,v===0?C.muted:C.line,v===0?2:1);
    s+=text(x(v),789,v===0?'0':`${v>0?'+':''}${v.toFixed(4)}`,23,C.muted,'middle');
  });
  D.features.forEach((r,i)=>{
    const y=380+i*82,c=r.selected?C.teal:r.delta_auc<0?C.red:C.blue;
    let body=text(120,y+11,r.label,31,r.selected?C.teal:C.ink);
    body+=line(x(0),y,x(r.delta_auc),y,c,4)+circle(x(r.delta_auc),y,r.selected?11:8,c);
    body+=text(1760,y+11,`${r.delta_auc>=0?'+':''}${r.delta_auc.toFixed(6)}`,30,c,'end','font-variant-numeric="tabular-nums"');
    s+=reveal(t,.6+i*.85,body);
  });
  s+=reveal(t,6.2,text(120,838,'Selection: positive mean Δ AUC + improvement in at least 4 of 5 seeds.',27,C.muted));
  return s+footer('Only relative balance + payroll passed the declared rule.');
}

function inicial(t){
  let s=small('PUBLIC · INICIAL • selected feature package + tuning + refit + ensemble + contact policy');
  s+=reveal(t,.4,text(120,342,'4 new columns',43,C.teal)+text(120,389,'2 relative changes + 2 near-zero flags',28,C.muted));
  s+=reveal(t,1.8,arrow(660,348,760,348)+text(820,342,'20 HPO evaluations',38)+text(820,389,'Then a five-seed final ensemble',28,C.muted));
  const x=v=>220+(v-8000)/4000*1260,y=v=>765-(v-360)/50*290;
  [360,380,400,410].forEach(v=>s+=line(220,y(v),1480,y(v))+text(185,y(v)+8,v,23,C.muted,'end'));
  [8000,9000,10000,11000,12000].forEach(v=>s+=text(x(v),810,v.toLocaleString('en-US'),23,C.muted,'middle'));
  s+=text(850,845,'Contacts selected',24,C.muted,'middle');
  // Connecting lines describe nine fixed policy evaluations, not chronological improvement.
  const points=D.initial.curve.map(r=>`${x(r.contacts)},${y(r.score)}`).join(' ');
  let plot=`<polyline points="${points}" fill="none" stroke="${C.blue}" stroke-width="3"/>`;
  D.initial.curve.forEach(r=>plot+=circle(x(r.contacts),y(r.score),r.score===D.initial.score?9:6,r.score===D.initial.score?C.teal:C.blue));
  s+=reveal(t,3.2,plot);
  s+=reveal(t,4.4,text(1745,582,D.initial.score.toFixed(3),66,C.teal,'end','font-variant-numeric="tabular-nums"')+text(1745,631,'Best submitted score',25,C.muted,'end')+text(1745,674,'11,500 / 12,000 contacts',24,C.muted,'end'));
  return s+footer('This is the final recipe’s score—not a feature-only public effect.');
}

function pilot(t){
  let s=small('Historical follow-up • May + July 2021 • no public scores for these pilot variants');
  s+=text(120,326,'ADDITIONS EXPLORED',23,C.muted);
  ['Longer funds history','Usage changes','Monetary ranks','Prior-only EMA'].forEach((label,i)=>s+=reveal(t,.5+i*.65,circle(145,399+i*80,5,C.blue)+text(175,410+i*80,label,32)));
  s+=line(710,330,710,787);
  D.pilot.findings.forEach((r,i)=>{
    const yy=403+i*142,color=r.kind==='consistent'?C.teal:C.amber;
    s+=reveal(t,3.5+i*1.6,text(790,yy,r.label,35,color)+text(790,yy+48,r.outcome,30,C.ink));
    if(r.kind==='consistent')s+=reveal(t,3.5+i*1.6,text(1710,yy+20,'2/2',48,color,'end'));
    else s+=reveal(t,3.5+i*1.6,text(1710,yy+20,'mixed',40,color,'end'));
  });
  s+=text(790,827,'Selected findings from the pilot—not a ranking of all eight views.',24,C.muted);
  return s+footer('Promising candidates need further testing; EMA stays exploratory.');
}

function decision(t){
  let s=small('Different evidence supports different conclusions.');
  s+=reveal(t,.3,text(120,369,'STRONGEST CONTROLLED-SCREEN ADDITION',24,C.teal)+text(120,435,'Relative balance + payroll',57,C.teal,'start','font-family="Georgia,serif"'));
  s+=reveal(t,2.5,text(120,518,'Mean Δ AUC',29,C.muted)+text(405,520,`+${D.features.find(r=>r.selected).delta_auc.toFixed(6)}`,39,C.ink)+text(850,520,'4 added columns',31,C.muted));
  s+=line(120,565,1760,565);
  s+=reveal(t,4.6,text(120,633,'FOLLOW-UP CANDIDATES',24,C.blue)+text(120,692,'Longer funds history + usage changes',39,C.ink)+text(120,744,'Historical evidence only. EMA remains exploratory.',29,C.muted));
  s+=reveal(t,7.4,text(120,824,'Test additions separately; do not assign a full recipe’s score to one feature.',29,C.muted));
  return s+footer('Best in this screen ≠ proven best feature in every model.');
}

const DRAW={design,relative,screen,inicial,pilot,decision};
let current=0,playing=false,last=null,raf=null;
const stage=document.getElementById('stage'),scrub=document.getElementById('scrub'),play=document.getElementById('play');
const clock=t=>`${Math.floor(t/60)}:${String(Math.floor(t%60)).padStart(2,'0')}`;
function sceneAt(t){return SCENES.find(s=>t>=s.start&&t<s.end)||SCENES[SCENES.length-1]}
function renderAt(t){
  current=Math.max(0,Math.min(90,Number(t)||0));const s=sceneAt(current),local=current-s.start;
  const guide=document.getElementById('headshot').checked?`<g data-headshot-guide="true">${circle(1730,180,100,'none',`stroke="${C.line}" stroke-dasharray="7 7"`)}${text(1730,185,'headshot',22,C.muted,'middle')}</g>`:'';
  stage.innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" role="img" aria-label="${escapeText(s.title)}" data-scene="${s.id}"><style>text{font-family:Arial,sans-serif}text[font-family]{font-family:Georgia,serif}</style>${rect(0,0,1920,1080,C.bg)}${text(120,87,`FEATURE ENGINEERING / ${String(SCENES.indexOf(s)+1).padStart(2,'0')}`,23,C.muted)}${text(120,174,s.title,62,C.ink,'start','font-family="Georgia,serif" data-fit="1420"')}${DRAW[s.id](local)}${guide}</svg>`;
  stage.querySelectorAll('[data-fit]').forEach(el=>{const width=el.getComputedTextLength(),max=Number(el.dataset.fit);if(width>max)el.setAttribute('font-size',Number(el.getAttribute('font-size'))*max/width)});
  scrub.value=current;document.getElementById('time').textContent=`${clock(current)} / 1:30`;
  document.getElementById('narration').textContent=s.voiceover;
  document.querySelectorAll('[data-seek]').forEach(el=>el.setAttribute('aria-pressed',String(Number(el.dataset.seek)===s.start)));
  return s.id;
}
function stop(){playing=false;last=null;cancelAnimationFrame(raf);play.textContent='Play'}
function seek(t){stop();renderAt(t)}
function tick(now){if(!playing)return;if(last!==null)current+=(now-last)/1000;last=now;renderAt(current);if(current>=90){stop();return}raf=requestAnimationFrame(tick)}
function toggle(){if(playing){stop();return}if(current>=90)renderAt(0);playing=true;last=null;play.textContent='Pause';raf=requestAnimationFrame(tick)}
SCENES.forEach((s,i)=>{const b=document.createElement('button');b.dataset.seek=s.start;b.textContent=`${clock(s.start)} · ${['Question','Why these features','Controlled impact','Final outcome','Follow-up','Conclusion'][i]}`;b.onclick=()=>seek(s.start);document.getElementById('scenes').appendChild(b)});
document.getElementById('evidence').innerHTML='<table><thead><tr><th>Added package</th><th>Columns</th><th>Mean May AUC</th><th>Mean Δ AUC</th><th>Selected</th></tr></thead><tbody>'+D.features.map(r=>`<tr><td>${escapeText(r.label)}</td><td>${r.columns}</td><td>${r.mean_auc.toFixed(9)}</td><td>${r.delta_auc.toFixed(9)}</td><td>${r.selected?'Yes':'No'}</td></tr>`).join('')+'</tbody></table><p>Repaired baseline mean AUC: '+D.baseline_auc.toFixed(9)+'. These are package-level mean comparisons, without per-seed uncertainty. Positive mean alone was not the selection rule.</p>';
play.onclick=toggle;scrub.oninput=e=>seek(e.target.value);document.getElementById('headshot').onchange=()=>renderAt(current);
document.addEventListener('keydown',e=>{if(['INPUT','BUTTON','SUMMARY'].includes(e.target.tagName))return;if(e.code==='Space'){e.preventDefault();toggle()}else if(e.code==='ArrowRight'){e.preventDefault();seek(SCENES.find(s=>s.start>current+.1)?.start??90)}else if(e.code==='ArrowLeft'){e.preventDefault();seek([...SCENES].reverse().find(s=>s.start<current-.1)?.start??0)}});
window.renderAt=renderAt;window.storyboardScenes=SCENES;window.storyboardData=D;
renderAt(Number(new URLSearchParams(location.search).get('t'))||0);

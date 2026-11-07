'use strict';
const DATA=JSON.parse(document.getElementById('payload').textContent), ROWS=DATA.rows, SCENES=DATA.scenes;
const C={bg:'#0b0f14',ink:'#e8eef1',muted:'#9daebb',line:'#2b3c4a',blue:'#78abff',teal:'#6cdbba',amber:'#f3b773',rose:'#ec8aa6',violet:'#b8a0f6',red:'#f08d99'};
const FAMILY=[C.blue,C.amber,C.blue,C.teal,C.rose,C.teal,C.teal,C.rose,C.violet];
const E=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const clamp=v=>Math.max(0,Math.min(1,v));
const ease=v=>{v=clamp(v);return v*v*(3-2*v)};
const lerp=(a,b,t)=>a+(b-a)*t;
const T=(x,y,v,size=30,color=C.ink,anchor='start',extra='')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" ${extra}>${E(v)}</text>`;
const L=(x1,y1,x2,y2,color=C.line,width=2,extra='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
const O=(x,y,r,color,extra='')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${color}" ${extra}/>`;
const R=(x,y,w,h,color,extra='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${color}" ${extra}/>`;
const P=(points,color=C.blue,width=3,extra='')=>`<polyline points="${points.map(p=>p.join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
const arrive=(t,start,body,duration=.7)=>`<g opacity="${ease((t-start)/duration)}" transform="translate(0 ${14*(1-ease((t-start)/duration))})">${body}</g>`;
const halo=(x,y,r,color,a=.14)=>O(x,y,r,color,`opacity="${a}" filter="url(#glow)"`);
const footer=v=>L(120,874,1790,874)+T(120,926,v,33,C.ink,'start','data-fit="1660"');
const subtitle=v=>T(120,244,v,27,C.muted,'start','data-fit="1420"');
const arrow=(x1,y,x2,color=C.teal)=>L(x1,y,x2,y,color,3)+P([[x2-12,y-9],[x2,y],[x2-12,y+9]],color,3);

// Genuine 3D coordinates, projected orthographically into the SVG. Depth means past time.
function historyWorld(t){
  const camera=ease((t-2.6)/3.8),az=-.32*camera,el=.40*camera;
  function project([x,y,z]){
    const xr=x*Math.cos(az)-z*Math.sin(az),zr=x*Math.sin(az)+z*Math.cos(az);
    return [960+xr,610-y*Math.cos(el)-zr*Math.sin(el)];
  }
  let s='';
  for(let k=3;k>=0;k--){
    const alpha=ease((t-3-(3-k)*.3)/1.1),z=k*85;
    const polygon=[[-650,-40,z],[650,-40,z],[650,190,z],[-650,190,z]].map(project);
    s+=`<g opacity="${alpha}"><polygon points="${polygon.map(p=>p.join(',')).join(' ')}" fill="${C.blue}" fill-opacity="${k?.025:.055}" stroke="${C.blue}" stroke-opacity=".22" stroke-width="1.4"/>`;
    for(const xx of [-350,0,350]){const a=project([xx,-40,z]),b=project([xx,190,z]);s+=L(...a,...b,C.line,1)}
    const label=project([675,-10,z]);
    s+=T(label[0],label[1]+6,['Now','1 month ago','2 months ago','3 months ago'][k],22,k?C.muted:C.ink)+'</g>';
  }
  [-350,350].forEach((xx,g)=>{
    const color=g?C.blue:C.amber, values=g?[80,80,80,80]:[100,100,100,80];
    const points=values.map((v,i)=>project([xx,(v-80)*6,(3-i)*85]));
    const past=ease((t-3.7)/2.2);
    s+=`<g opacity="${past}">`+P(points,color,3.5);
    points.slice(0,3).forEach((p,i)=>s+=O(p[0],p[1],6,color,`opacity="${.45+i*.15}"`));
    s+='</g>';
    const now=points[3], pulse=1+Math.sin(t*2.7)*.05*(1-camera);
    s+=halo(now[0],now[1],35*pulse,color,.2)+O(now[0],now[1],12*pulse,color);
    s+=T(now[0],now[1]+68,'80',57,C.ink,'middle','font-family="Georgia,serif"');
    s+=T(g?1320:600,785,t<7?(g?'Customer B':'Customer A'):(g?'Steady level':'Recent drop'),30,color,'middle');
    s+=arrive(t,8.1,T(g?1320:600,839,g?'0% vs own recent mean':'−20% vs own recent mean',30,color,'middle'));
  });
  return s;
}

function question(t){
  let s=subtitle('Two illustrative customers. The same balance today.');
  s+=historyWorld(t);
  s+=arrive(t,5.8,T(120,330,'History reveals what the snapshot hides.',31,C.ink));
  return s+footer(t<8?'Would a snapshot tell them apart?':'The useful signal can be the change relative to normal.');
}

// All glyphs are schematics, not experimental observations. Each encodes its operation.
function glyph(index,x,y,t,scale=1){
  const color=FAMILY[index],phase=(Math.sin(t*1.3)+1)/2;
  let s='';
  const dots=[[10,45],[35,27],[60,36],[88,14]];
  if(index===0){
    s+=L(0,54,106,54,C.line,1.5);
    dots.forEach((p,i)=>s+=O(p[0],p[1],i===2?6:4,color,`opacity="${i===3?.25:.8}"`));
    s+=P([[63+phase*12,5],[53+phase*12,5],[53+phase*12,18]],color,2.5);
  }else if(index===1){
    s+=O(18,14,5,color)+O(86,45,5,color)+L(18,14,86,45,color,3);
    s+=P([[90,15],[90,41],[83,34]],color,2.5);
  }else if(index===2||index===5){
    const n=index===5?6:3;
    for(let i=0;i<n;i++)s+=O(8+i*92/(n-1),16+((i*13)%29),4.5,color);
    s+=L(1,32,105,32,color,3,'stroke-dasharray="5 5"')+halo(52,32,18,color,.15);
  }else if(index===3||index===6){
    s+=L(2,54,47,54,C.line,1.4)+L(61,54,106,54,C.line,1.4);
    s+=R(8,10,13,44,color,'opacity=".4"')+R(27,23,13,31,color);
    s+=R(66,10,13,44,color,'opacity=".4"')+R(85,index===3?14:32,13,index===3?40:22,color);
    s+=P([[45,2],[53,2],[53,9]],color,2);
  }else if(index===4){
    s+=O(52,30,25,'none',`stroke="${C.line}" stroke-width="7"`);
    s+=`<circle cx="52" cy="30" r="25" fill="none" stroke="${color}" stroke-width="7" stroke-dasharray="108 157" transform="rotate(-90 52 30)"/>`;
    s+=T(52,37,'÷',26,color,'middle');
  }else if(index===7){
    [3,2,0,1].forEach((v,i)=>{const a=[12+i*27,8+v*13],b=[12+i*27,48-i*11];s+=O(lerp(a[0],b[0],phase),lerp(a[1],b[1],phase),5,color)});
    s+=L(3,58,107,58,C.line,1.5);
  }else{
    for(let i=0;i<5;i++){const r=2.5+i*1.4;s+=O(8+i*23,35-(i%2)*15,r,color,`opacity="${.2+i*.17}"`)}
    s+=halo(100,35,15,color,.2);
  }
  return `<g transform="translate(${x} ${y}) scale(${scale})">${s}</g>`;
}

const DEFINITIONS=[
  ['Last month’s value','Remember the recent level.'],
  ['Current minus last month','Expose sudden movement.'],
  ['Mean of prior 3 months','Estimate usual behavior.'],
  ['Balance/payroll vs own mean','Account for personal scale.'],
  ['Card balance ÷ credit limit','Express credit pressure.'],
  ['Relative funds over 6 months','Use a longer reference.'],
  ['Usage vs own 3-month mean','Reveal disengagement.'],
  ['Rank amounts in same month','Compare relative position.'],
  ['Weighted mean of past values','Emphasize recent changes.'],
];

function features(t){
  let s=subtitle('What it is → why we expected it to help');
  const focusStarts=[0,4.4,7.0,11.0,21.0,26.0,30.0,36.8,41.5];
  const active=Math.max(0,focusStarts.filter(start=>t>=start).length-1);
  [663,1233].forEach(x=>s+=L(x,300,x,843,C.line,1));
  [475,660].forEach(y=>s+=L(120,y,1790,y,C.line,1));
  ROWS.forEach((r,i)=>{
    const x=120+(i%3)*570,y=304+Math.floor(i/3)*185,col=FAMILY[i];
    let b=T(x+4,y+21,r.label,30,col,'start','data-fit="520"');
    const settle=ease((t-.08*i)/1.35);
    b+=glyph(i,lerp(900,x+8,settle),lerp(600,y+60,settle),t,lerp(.38,1,settle));
    if(i===active)b+=halo(x+60,y+90,45,col,.14);
    b+=T(x+145,y+76,DEFINITIONS[i][0],24,C.ink,'start','data-fit="380"');
    b+=T(x+145,y+120,DEFINITIONS[i][1],23,C.muted,'start','data-fit="380"');
    b+=L(x+145,y+135,x+185+(i===active?120:0),y+135,col,i===active?3:1,`opacity="${i===active?.8:.25}"`);
    s+=arrive(t,0,b,.8);
  });
  return s+footer('Nine hypotheses. Different ways to reveal the same customer context.');
}

function person(x,y,color,label){
  return O(x,y,21,color)+`<path d="M${x-35} ${y+78} Q${x-35} ${y+30} ${x} ${y+30} Q${x+35} ${y+30} ${x+35} ${y+78}" fill="${color}" opacity=".6"/>`+T(x,y+127,label,30,C.ink,'middle');
}
function measurement(t){
  let s=subtitle('The task: choose whom to contact for the Premium retention campaign.');
  s+=arrive(t,.2,person(570,390,C.teal,'November leaver')+T(570,615,'+AR$975,000',58,C.teal,'middle')+T(570,660,'Score for a correct contact',27,C.muted,'middle'));
  s+=arrive(t,2.0,person(1370,390,C.rose,'Other customer')+T(1370,615,'−AR$25,000',58,C.rose,'middle')+T(1370,660,'Cost of an unnecessary contact',27,C.muted,'middle'));
  s+=L(960,330,960,720,C.line,1);
  s+=arrive(t,5.5,T(960,322,'One pair: who should be higher on the contact list?',27,C.ink,'middle')+L(1170,355,760,355,C.blue,2)+P([[773,346],[760,355],[773,364]],C.blue,2.5)+O(570,390,31,'none',`stroke="${C.teal}" stroke-width="2"`));
  s+=arrive(t,4.3,T(960,772,'No contact = zero campaign score',29,C.muted,'middle'));
  s+=arrive(t,6.0,T(960,829,'We tested each addition with five matched retrainings.',28,C.ink,'middle'));
  ROWS.forEach((r,i)=>s+=glyph(i,140+i*44,710,t,.34));
  s+=T(120,756,'Added signals',23,C.muted);
  return s+footer('A better priority list can help. Its profit must still be measured.');
}

function comparison(t,closing=false){
  let s=subtitle(closing?'The public score belongs to the complete recipe. Feature-level peso differences are pending.':'One pair = one November leaver and one other customer. Higher priority for the leaver = correct.');
  s+=T(120,310,'ADDED FEATURE',22,C.muted);
  s+=T(920,310,'Finding November leavers',32,C.blue,'middle')+T(920,339,'Extra correct pair orderings / 10,000',23,C.muted,'middle');
  s+=T(1555,310,'Historical profit',32,C.teal,'middle')+T(1555,339,'May + July · vs 3-month funds reference',22,C.muted,'middle');
  s+=L(1285,267,1285,822,C.line,1.5);
  const X=v=>620+(v+.00075)/.0025*500;
  [-.0005,0,.0005,.001,.0015].forEach(v=>{
    s+=L(X(v),350,X(v),811,v===0?C.muted:C.line,v===0?2:1);
    s+=T(X(v),838,v===0?'0':`${v>0?'+':'−'}${Math.abs(v*10000).toFixed(0)}`,21,C.muted,'middle');
  });
  ROWS.forEach((r,i)=>{
    const y=365+i*54;
    if(closing&&[3,5,6].includes(i))s+=R(112,y-25,1670,47,C.teal,'opacity=".055" rx="8"');
    const travel=closing?1:ease((t-i*.03)/1.6);
    s+=glyph(i,lerp(140+i*44,120,travel),lerp(710,y-14,travel),0,lerp(.34,.36,travel));
    s+=T(170,y+10,r.label,29,C.ink,'start','data-fit="420"');
    if(r.delta_auc!==null){
      const color=r.selected?C.teal:r.delta_auc>0?C.blue:C.red,delay=r.selected?3.0:.4+i*.32;
      let b=L(X(0),y,X(r.delta_auc),y,color,3.5)+O(X(r.delta_auc),y,r.selected?9:6,color);
      if(r.selected)b+=halo(X(r.delta_auc),y,19,color,.17);
      b+=T(1240,y+9,`${r.delta_auc>=0?'+':'−'}${Math.abs(r.delta_auc*10000).toFixed(0)}`,34,color,'end','font-variant-numeric="tabular-nums"');
      s+=arrive(t,closing?0:delay,b);
    }else s+=T(920,y+9,'—',26,C.muted,'middle');
    let result='';
    if(r.profit==='both_months'){
      result=O(1340,y,7,C.teal)+O(1365,y,7,C.teal)+T(1400,y+9,'Higher in May + July',27,C.teal);
    }else if(r.profit==='mixed')result=P([[1330,y-7],[1340,y+6],[1350,y-7],[1360,y+6]],C.amber,2.5)+T(1400,y+9,'Mixed across months',27,C.amber);
    else if(r.profit==='reference')result=T(1500,y+9,'Comparison baseline',25,C.muted,'middle');
    else if(r.profit==='unverified')result=O(1346,y,7,'none',`stroke="${C.muted}" stroke-width="2"`)+T(1400,y+9,'Result unverified',25,C.muted);
    else result=T(1500,y+9,'—',26,C.muted,'middle');
    const delay=r.profit==='both_months'?11+(i-5)*2:r.profit==='mixed'?19:0;
    s+=arrive(t,closing?0:delay,result);
  });
  s+=T(1330,853,'— No verified result supplied',22,C.muted);
  return s+footer(closing?'Selected recipe: AR$401.9 million · scaled Kaggle public campaign score':'Correct pair orderings are not customers retained or a conversion to pesos.');
}

const DRAW={question,features,measurement,comparison,takeaway:t=>comparison(30+t,true)};
const stage=document.getElementById('stage'),scrub=document.getElementById('scrub'),play=document.getElementById('play');
let current=0,playing=false,last=null,raf=null;
const clock=t=>`${Math.floor(t/60)}:${String(Math.floor(t%60)).padStart(2,'0')}`;
const sceneAt=t=>SCENES.find(s=>t>=s.start&&t<s.end)||SCENES[SCENES.length-1];
function renderAt(t){
  current=Math.max(0,Math.min(DATA.duration,Number(t)||0));const s=sceneAt(current),local=current-s.start;
  const guide=document.getElementById('headshot').checked?O(1730,180,100,'none',`data-headshot-guide="true" stroke="${C.line}" stroke-dasharray="6 7"`):'';
  stage.innerHTML=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" role="img" aria-label="${E(s.title)}" data-scene="${s.id}"><defs><filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="10"/></filter><radialGradient id="background"><stop offset="0" stop-color="#12212a"/><stop offset="1" stop-color="${C.bg}"/></radialGradient></defs><style>text{font-family:Arial,sans-serif}text[font-family]{font-family:Georgia,serif}</style>${R(0,0,1920,1080,'url(#background)')}${T(120,86,'FEATURE ENGINEERING / THE CONTEXT BEHIND THE NUMBER',22,C.muted)}${T(120,174,s.title,61,C.ink,'start','font-family="Georgia,serif" data-fit="1420"')}${DRAW[s.id](local)}${guide}</svg>`;
  stage.querySelectorAll('[data-fit]').forEach(el=>{const w=el.getComputedTextLength(),max=Number(el.dataset.fit);if(w>max)el.setAttribute('font-size',Number(el.getAttribute('font-size'))*max/w)});
  scrub.value=current;document.getElementById('time').textContent=`${clock(current)} / ${clock(DATA.duration)}`;
  document.getElementById('narration').textContent=s.voiceover;
  document.querySelectorAll('[data-seek]').forEach(el=>el.setAttribute('aria-pressed',String(Number(el.dataset.seek)===s.start)));
  return s.id;
}
function stop(){playing=false;last=null;cancelAnimationFrame(raf);play.textContent='Play'}
function seek(t){stop();renderAt(t)}
function tick(now){if(!playing)return;if(last!==null)current+=(now-last)/1000;last=now;renderAt(current);if(current>=DATA.duration){stop();return}raf=requestAnimationFrame(tick)}
function toggle(){if(playing){stop();return}if(current>=DATA.duration)renderAt(0);playing=true;last=null;play.textContent='Pause';raf=requestAnimationFrame(tick)}
SCENES.forEach(s=>{const b=document.createElement('button');b.dataset.seek=s.start;b.textContent=`${clock(s.start)} · ${s.label}`;b.onclick=()=>seek(s.start);document.getElementById('navigation').appendChild(b)});
document.getElementById('evidence').innerHTML='<table><thead><tr><th>Feature family</th><th>Mean Δ AUC</th><th>Profit result</th></tr></thead><tbody>'+ROWS.map(r=>`<tr><td>${E(r.label)}</td><td>${r.delta_auc===null?'No comparable verified result':r.delta_auc.toFixed(9)}</td><td>${E(r.profit_label)}</td></tr>`).join('')+'</tbody></table>';
play.onclick=toggle;scrub.oninput=e=>seek(e.target.value);document.getElementById('headshot').onchange=()=>renderAt(current);
document.addEventListener('keydown',e=>{if(['INPUT','BUTTON','SUMMARY'].includes(e.target.tagName))return;if(e.code==='Space'){e.preventDefault();toggle()}else if(e.code==='ArrowRight'){e.preventDefault();seek(SCENES.find(s=>s.start>current+.1)?.start??DATA.duration)}else if(e.code==='ArrowLeft'){e.preventDefault();seek([...SCENES].reverse().find(s=>s.start<current-.1)?.start??0)}});
window.renderAt=renderAt;window.storyboardData=DATA;window.storyboardScenes=SCENES;
renderAt(Number(new URLSearchParams(location.search).get('t'))||0);

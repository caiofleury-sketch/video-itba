const fs=require('fs'),crypto=require('crypto');
const {createScore}=require('./score.js');
const source=fs.readFileSync('../v8_es/data.json');
const score=createScore(JSON.parse(source));
score.visual_source_sha256=crypto.createHash('sha256').update(fs.readFileSync('../v8_es/scenes.js')).digest('hex');
score.timing_source_sha256=crypto.createHash('sha256').update(source).digest('hex');
for(const e of [...score.music,...score.fx]){
 if(!(e.time>=0&&e.time+e.duration<score.duration&&e.velocity>0&&e.velocity<=1))throw Error('Invalid score event '+JSON.stringify(e));
}
fs.writeFileSync('score.json',JSON.stringify(score,null,2)+'\n');
fs.writeFileSync('score_data.js','window.SCORE='+JSON.stringify(score)+';\n');
fs.writeFileSync('cues.csv','id,segundo,escena_o_variable,accion_visual\n'+score.cues.map(c=>[c.id,c.time,c.feature,'"'+c.label.replaceAll('"','""')+'"'].join(',')).join('\n')+'\n');
console.log(JSON.stringify({duration:score.duration,musicalNotes:score.music.length,accentNotes:score.fx.length,cues:score.cues.length}));

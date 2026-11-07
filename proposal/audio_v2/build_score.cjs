const fs=require('fs'),crypto=require('crypto');const{createScore}=require('./score.js');
const source=fs.readFileSync('../v9_es/data.json');const score=createScore(JSON.parse(source));
score.visual_source_sha256=crypto.createHash('sha256').update(fs.readFileSync('../v9_es/scenes.js')).digest('hex');
fs.writeFileSync('score.json',JSON.stringify(score,null,2)+'\n');fs.writeFileSync('score_data.js','window.SCORE='+JSON.stringify(score)+';\n');
fs.writeFileSync('cues.csv','segundo,accion\n'+score.cues.map(c=>c.time+',"'+c.label+'"').join('\n')+'\n');
console.log(JSON.stringify({duration:score.duration,bars:score.duration/2,musicNotes:score.music.length,accentNotes:score.fx.length,cues:score.cues.length}));

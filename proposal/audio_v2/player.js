'use strict';
const video=document.getElementById('video'),music=document.getElementById('music'),fx=document.getElementById('fx'),stems=[music,fx];
const play=document.getElementById('play'),seek=document.getElementById('seek'),clock=document.getElementById('time'),error=document.getElementById('error');
video.muted=true;
let starting=false;
const fmt=t=>`${Math.floor(t/60)}:${String(Math.floor(t%60)).padStart(2,'0')}`;
function align(force=false){if(starting&&!force)return;for(const a of stems){if(force||Math.abs(a.currentTime-video.currentTime)>.075)a.currentTime=video.currentTime;a.playbackRate=video.playbackRate;}}
function paint(){
 seek.value=video.currentTime;clock.textContent=`${fmt(video.currentTime)} / 2:00`;
 const cue=[...window.SCORE.cues].reverse().find(c=>video.currentTime>=c.time);
 document.getElementById('cue').textContent=cue?`${fmt(cue.time)} · ${cue.label}`:'El fondo entra gradualmente. Los primeros acentos acompañan el despliegue de la historia.';
 document.querySelectorAll('[data-seek]').forEach(b=>{const start=Number(b.dataset.seek),next=[16,65,70,102,120].find(t=>t>start);b.setAttribute('aria-current',video.currentTime>=start&&video.currentTime<next?'true':'false')});
}
function pause(){video.pause();stems.forEach(a=>a.pause());play.textContent='Reproducir';}
async function start(){
 if(starting)return;starting=true;error.textContent='';
 if(video.currentTime>=119.98)video.currentTime=0;
 align(true);
 try{await Promise.all([video.play(),...stems.map(a=>a.play())]);play.textContent='Pausar';}
 catch(e){pause();error.textContent='No se pudo iniciar el audio. Volvé a pulsar Reproducir o abrí el video con sonido.';}
 finally{starting=false;}
}
function jump(t){const active=!video.paused;pause();video.currentTime=Number(t);align(true);paint();if(active)start();}
play.onclick=()=>video.paused?start():pause();
video.onclick=play.onclick;video.onended=pause;video.ontimeupdate=()=>{align();paint()};
video.onseeking=()=>align(true);video.onratechange=()=>align(true);
// A media play promise may be pending while decoding the first frame. Pausing
// another track from a transient `waiting` event would cancel that promise.
seek.oninput=e=>jump(e.target.value);
for(const name of ['music','fx']){
 const audio=name==='music'?music:fx,slider=document.getElementById(name+'-volume'),button=document.getElementById(name+'-mute');
 slider.oninput=()=>{audio.volume=Number(slider.value)/100;document.getElementById(name+'-level').textContent=slider.value+'%'};
 button.onclick=()=>{audio.muted=!audio.muted;button.setAttribute('aria-pressed',String(audio.muted));button.textContent=audio.muted?`Activar ${name==='music'?'música':'acentos'}`:`Silenciar ${name==='music'?'música':'acentos'}`};
}
for(const b of document.querySelectorAll('[data-seek]'))b.onclick=()=>jump(b.dataset.seek);
for(const c of window.SCORE.cues){const option=document.createElement('option');option.value=Math.max(0,c.time-.3);option.textContent=`${fmt(c.time)} · ${c.label}`;document.getElementById('movement').appendChild(option);}
document.getElementById('movement').onchange=e=>{if(e.target.value!=='')jump(e.target.value)};
document.addEventListener('keydown',e=>{if(e.code==='Space'&&!['INPUT','BUTTON','SELECT','A'].includes(e.target.tagName)){e.preventDefault();play.onclick()}});
window.soundscape={jump,pause,start,state:()=>({time:video.currentTime,musicTime:music.currentTime,fxTime:fx.currentTime,paused:video.paused,musicVolume:music.volume,fxVolume:fx.volume,musicMuted:music.muted,fxMuted:fx.muted})};paint();

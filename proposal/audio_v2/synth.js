'use strict';
window.renderStem=async function(score,which){
 const sound=await Tone.Offline(()=>{
  const out=new Tone.Gain(0).toDestination();
  const offset=score.windowStart||0;
  const points=which==='music'?[[0,0],[1,.6],[69.7,.6],[70.2,.46],[101.7,.46],[102.2,.6],[118.5,.6],[119.95,0]]:[[0,0],[.2,.6],[118.5,.6],[119.95,0]];
  const gainAt=t=>{let i=1;while(i<points.length&&points[i][0]<t)i++;if(i===points.length)return 0;const a=points[i-1],b=points[i];return a[1]+(b[1]-a[1])*(t-a[0])/(b[0]-a[0]);};
  out.gain.setValueAtTime(gainAt(offset),0);
  points.filter(p=>p[0]>offset&&p[0]<=offset+score.duration).forEach(([t,v])=>out.gain.linearRampToValueAtTime(v,t-offset));
  const limiter=new Tone.Limiter(-3).connect(out);
  const compressor=new Tone.Compressor({threshold:-18,ratio:2.2,knee:12,attack:.015,release:.16}).connect(limiter);
  const space=new Tone.Filter({type:'peaking',frequency:2300,Q:.7,gain:-3.5}).connect(compressor);
  const low=new Tone.Filter({type:'lowpass',frequency:4800,rolloff:-12,Q:.6}).connect(space);
  const hp=new Tone.Filter({type:'highpass',frequency:45,rolloff:-24,Q:.6}).connect(low);
  const ir=Tone.getContext().rawContext.createBuffer(2,Math.round(score.sampleRate*1.15),score.sampleRate);
  let irSeed=526;const irRandom=()=>{irSeed=(1664525*irSeed+1013904223)>>>0;return irSeed/4294967296};
  for(let ch=0;ch<2;ch++){
   const samples=ir.getChannelData(ch);let previous=0;
   for(let i=0;i<samples.length;i++){
    previous=previous*.55+(irRandom()*2-1)*.45;
    samples[i]=previous*Math.exp(-6*i/samples.length);
   }
  }
  const room=new Tone.Convolver({url:ir,normalize:true,wet:1}).connect(new Tone.Gain(.14).connect(hp));
  const dry=new Tone.Gain(1).connect(hp),chorus=new Tone.Chorus({frequency:.65,delayTime:2.5,depth:.22,wet:.13}).connect(dry);
  // Tone.js is pinned; preserve the stereo LFO phase across offline windows.
  chorus._lfoL.phase=(offset*.65*360)%360;chorus._lfoR.phase=(offset*.65*360+180)%360;chorus.start(0);
  const poly=(type,options,volume)=>new Tone.PolySynth(type,{...options,volume});
  const voices={
   lead:poly(Tone.Synth,{oscillator:{type:'triangle'},envelope:{attack:.012,decay:.11,sustain:.65,release:.16}},-12),
   pulse:poly(Tone.Synth,{oscillator:{type:'pulse',width:.25},envelope:{attack:.012,decay:.1,sustain:.55,release:.12}},-23),
   ep:poly(Tone.FMSynth,{harmonicity:3.005,modulationIndex:1.4,oscillator:{type:'sine'},envelope:{attack:.006,decay:.55,sustain:.12,release:.6},modulation:{type:'sine'},modulationEnvelope:{attack:.005,decay:.35,sustain:.035,release:.3}},-9),
   pad:poly(Tone.Synth,{oscillator:{type:'fatsine',count:3,spread:7},envelope:{attack:.20,decay:.25,sustain:.5,release:.65}},-27),
   arp:poly(Tone.FMSynth,{harmonicity:2,modulationIndex:1.1,envelope:{attack:.005,decay:.1,sustain:.015,release:.12},modulationEnvelope:{attack:.005,decay:.09,sustain:.01,release:.08}},-18),
   bass:poly(Tone.Synth,{oscillator:{type:'triangle'},envelope:{attack:.009,decay:.09,sustain:.70,release:.08}},-13),
   glint:poly(Tone.FMSynth,{harmonicity:2,modulationIndex:.6,envelope:{attack:.007,decay:.13,sustain:.01,release:.15},modulationEnvelope:{attack:.005,decay:.08,sustain:.01,release:.08}},-12)
  };
  for(const [name,voice] of Object.entries(voices)){
   voice.connect(new Tone.Panner(name==='ep'?-.12:name==='arp'?.18:name==='pad'?.1:0).connect(name==='ep'?chorus:dry));
   if(['lead','ep','arp','glint'].includes(name))voice.connect(room);
  }
  const kick=new Tone.MembraneSynth({pitchDecay:.025,octaves:3,envelope:{attack:.002,decay:.13,sustain:0,release:.04},volume:-24}).connect(dry);
  const rim=new Tone.NoiseSynth({noise:{type:'pink'},envelope:{attack:.002,decay:.045,sustain:0,release:.025},volume:-32}).connect(new Tone.Filter({type:'bandpass',frequency:1700,Q:.7}).connect(dry));
  const hat=new Tone.NoiseSynth({noise:{type:'white'},envelope:{attack:.001,decay:.02,sustain:0,release:.015},volume:-36}).connect(new Tone.Filter({type:'highpass',frequency:4000}).connect(dry));
  for(const e of score[which==='music'?'music':'fx']){
   if(e.voice==='kick')kick.triggerAttackRelease(e.pitch,e.duration,e.time,e.velocity);
   else if(e.voice==='rim')rim.triggerAttackRelease(e.duration,e.time,e.velocity);
   else if(e.voice==='hat')hat.triggerAttackRelease(e.duration,e.time,e.velocity);
   else voices[e.voice].triggerAttackRelease(e.pitch,e.duration,e.time,e.velocity);
  }
 },score.duration,2,score.sampleRate);
 window.renderedAudio=sound.get();const b=window.renderedAudio;return{duration:b.duration,sampleRate:b.sampleRate,channels:b.numberOfChannels,length:b.length};
};
window.audioChunk=function(channel,start,length){
 const arr=renderedAudio.getChannelData(channel).subarray(start,start+length),bytes=new Uint8Array(arr.buffer,arr.byteOffset,arr.byteLength);let s='';
 for(let i=0;i<bytes.length;i+=16384)s+=String.fromCharCode(...bytes.subarray(i,i+16384));return btoa(s);
};

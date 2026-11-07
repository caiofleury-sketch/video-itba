/* Tone.js offline synthesis. Two stems, identical sample clock, no samples. */
'use strict';
window.renderStem=async function(score,which){
 const sound=await Tone.Offline(()=>{
  const master=new Tone.Gain(0).toDestination();
  master.gain.setValueAtTime(0,0);
  master.gain.linearRampToValueAtTime(.75,which==='music'?1.6:.2);
  master.gain.setValueAtTime(.75,105);
  master.gain.linearRampToValueAtTime(0,107.85);
  const compressor=new Tone.Compressor({threshold:-20,ratio:2,knee:12,attack:.025,release:.18}).connect(master);
  const speechSpace=new Tone.Filter({type:'peaking',frequency:2400,Q:.6,gain:-4}).connect(compressor);
  const lowpass=new Tone.Filter({type:'lowpass',frequency:which==='music'?2350:3000,rolloff:-24,Q:.7}).connect(speechSpace);
  const highpass=new Tone.Filter({type:'highpass',frequency:55,rolloff:-24,Q:.7}).connect(lowpass);
  // Deterministic tiny taps instead of a random convolution reverb.
  const dry=new Tone.Gain(1).connect(highpass);
  const echoLevel=new Tone.Gain(.10).connect(highpass);
  const echo=new Tone.FeedbackDelay({delayTime:.15625,feedback:.09,maxDelay:1}).connect(echoLevel);
  const make=(type,options,volume)=>new Tone.PolySynth(type,{...options,volume,maxPolyphony:32});
  const voices={
   pad:make(Tone.Synth,{oscillator:{type:'sine'},envelope:{attack:.65,decay:.5,sustain:.45,release:1.7}},-14),
   bass:make(Tone.Synth,{oscillator:{type:'triangle'},envelope:{attack:.018,decay:.16,sustain:.12,release:.22}},-12),
   chip:make(Tone.Synth,{oscillator:{type:'square4'},envelope:{attack:.012,decay:.14,sustain:.12,release:.16}},which==='music'?-19:-18),
   pluck:make(Tone.FMSynth,{harmonicity:2,modulationIndex:.65,oscillator:{type:'sine'},envelope:{attack:.007,decay:.16,sustain:.01,release:.2},modulation:{type:'sine'},modulationEnvelope:{attack:.005,decay:.1,sustain:.02,release:.15}},-8),
   glass:make(Tone.FMSynth,{harmonicity:2,modulationIndex:.45,oscillator:{type:'sine'},envelope:{attack:.012,decay:.22,sustain:.01,release:.35},modulation:{type:'sine'},modulationEnvelope:{attack:.005,decay:.14,sustain:.02,release:.18}},-5)
  };
  for(const [name,v] of Object.entries(voices)){
   const pan=new Tone.Panner(name==='bass'||name==='pad'?0:name==='pluck'?-.1:.1).connect(dry);
   v.connect(pan);if(['chip','pluck','glass'].includes(name))v.connect(echo);
  }
  // Emphasize actual scene actions, never every changing pixel. Small pan cues
  // use separate voices so overlapping events cannot move another note's pan.
  const side={};
  for(const e of score[which==='music'?'music':'fx']){
   let voice=voices[e.voice];
   if(which==='fx'&&e.pan){
    const key=e.voice+(e.pan<0?'L':'R');
    if(!side[key]){
     side[key]=make(e.voice==='chip'?Tone.Synth:Tone.FMSynth,
      e.voice==='chip'?{oscillator:{type:'square4'},envelope:{attack:.012,decay:.14,sustain:.12,release:.16}}:
      {harmonicity:2,modulationIndex:.5,envelope:{attack:.01,decay:.18,sustain:.01,release:.25}},e.voice==='chip'?-18:e.voice==='glass'?-5:-8);
     side[key].connect(new Tone.Panner(e.pan<0?-.25:.25).connect(dry));
    }
    voice=side[key];
   }
   voice.triggerAttackRelease(e.pitch,e.duration,e.time,e.velocity);
  }
  if(which==='music'){
   // The measured-results narration is denser, so its bed recedes by 3 dB.
   master.gain.setValueAtTime(.75,69.6);master.gain.linearRampToValueAtTime(.53,70.3);
   master.gain.setValueAtTime(.53,93.7);master.gain.linearRampToValueAtTime(.75,94.3);
  }
 },score.duration,2,score.sampleRate);
 const buffer=sound.get();
 window.renderedAudio=buffer;
 return {duration:buffer.duration,sampleRate:buffer.sampleRate,channels:buffer.numberOfChannels,length:buffer.length};
};
window.audioChunk=function(channel,start,length){
 const arr=window.renderedAudio.getChannelData(channel).subarray(start,start+length);
 const bytes=new Uint8Array(arr.buffer,arr.byteOffset,arr.byteLength);let text='';
 for(let i=0;i<bytes.length;i+=16384)text+=String.fromCharCode(...bytes.subarray(i,i+16384));
 return btoa(text);
};

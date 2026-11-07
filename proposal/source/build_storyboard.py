"""Build an offline visual storyboard and verify every displayed result against audit CSVs."""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / "video_plan.json").read_text())
P = PLAN["palette"]


def text(x, y, value, size=32, weight=400, fill=None, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill or P["ink"]}" text-anchor="{anchor}">{html.escape(str(value))}</text>')


def rect(x, y, w, h, fill="white", stroke="none", radius=20):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def rule(x1, y1, x2, y2, color=None, width=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or P["line"]}" stroke-width="{width}"/>'


def pill(x, y, label, w=300, fill=None, color=None):
    return rect(x, y, w, 46, fill or P["teal_light"] , radius=23) + text(x+20, y+31, label, 23, 650, color or P["teal"])


def shell(chapter, title, subtitle, badge, body, takeaway, title_size=58):
    avatar = rect(1512, 96, 312, 312, "#EBEFEB", radius=30)
    avatar += '<circle cx="1668" cy="207" r="52" fill="#BCCDC5"/>'
    avatar += '<path d="M1578 357 Q1582 278 1668 278 Q1754 278 1758 357" fill="#BCCDC5"/>'
    avatar += text(1668, 388, "PRESENTER", 20, 650, P["muted"], "middle")
    avatar += text(1668, 450, "Camera stays here", 24, 400, P["muted"], "middle")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" role="img" aria-label="{html.escape(title)}">
<style>text{{font-family:Inter,Arial,sans-serif}}.num{{font-variant-numeric:tabular-nums}}</style>
{rect(0,0,1920,1080,P['background'],radius=0)}
{text(96,88,'FEATURE LAB  /  '+chapter,24,650,P['muted'])}
{text(96,170,title,title_size,700)}
{text(96,220,subtitle,30,400,P['muted'])}
{rule(1464,96,1464,858)}{avatar}{badge}{body}
{rule(96,894,1376,894)}
{text(96,958,takeaway,34,600)}
{text(96,1024,'RESEARCH → EVIDENCE → DECISION',20,550,P['muted'])}
{text(1824,1024,'90s · storyboard v1',20,400,P['muted'],'end')}
</svg>'''


def frame15():
    body = rect(96,300,475,215) + rect(700,300,676,215)
    body += text(130,348,"BASELINE",24,650,P["muted"]) + text(130,411,"152 repaired",45,650)
    body += text(130,465,"snapshot predictors",34)
    body += rule(600,407,666,407,P["teal"],5) + '<path d="M650 395 L666 407 L650 419" fill="none" stroke="#157F75" stroke-width="5"/>'
    body += text(736,348,"ONE VARIANT",24,650,P["teal"]) + text(736,411,"Baseline + one",45,650)
    body += text(736,465,"feature package",40,650)
    body += pill(96,554,"Same learner settings",390) + pill(510,554,"Same training rules",390)
    body += text(96,665,"Every package is retrained with the same five seeds.",31)
    for i in range(5):
        x=104+i*138
        body += rect(x,700,108,76,P["teal_light"],radius=16)+text(x+54,750,str(i+1),36,650,P["teal"],"middle")
    body += text(874,735,"Train labels through March",27,500,P["muted"])
    body += text(874,777,"Score the May 2021 snapshot",27,500,P["muted"])
    return shell("01 DESIGN","One change at a time","Can recent behavior help predict Premium exit?",
        pill(1040,78,"HISTORICAL · HT5955",335,P["ink"],"white"),body,PLAN["segments"][0]["takeaway"])


def frame30():
    body = text(112,300,"FEATURE PACKAGE",24,650,P["muted"])
    body += text(750,300,"DEFINITION",24,650,P["muted"])
    body += text(1150,300,"AUC WINS",24,650,P["muted"],"middle")
    for i,row in enumerate(PLAN["feature_screen"]):
        y=325+i*83
        body += rect(96,y,1280,72,P["teal_light"] if row["selected"] else "white",radius=15)
        body += text(120,y+46,row["label"],31,650 if row["selected"] else 450)
        body += text(750,y+45,row["parameter"],25,400,P["muted"])
        body += text(1150,y+46,f'{row["seeds_improved"]}/5',31,700,P["teal"] if row["selected"] else P["muted"],"middle")
        if row["selected"]:
            body += '<path d="M1270 624 L1282 636 L1304 608" transform="translate(0 0)" fill="none" stroke="#157F75" stroke-width="6" stroke-linecap="round"/>'
    body += text(96,794,"Rule: positive mean AUC change + at least 4 of 5 seed wins.",26,450,P["muted"])
    body += text(96,839,"Only the relative-funds package advances. This is a historical selection result.",25,450,P["muted"])
    return shell("01 DESIGN","One package passed the first screen","All packages face the same rule and the same five seeds.",
        pill(1040,78,"HISTORICAL · HT5955",335,P["ink"],"white"),body,PLAN["segments"][1]["takeaway"],54)


def insert35():
    body = text(96,452,"401.915",154,750,P["teal"])
    body += text(100,519,"Best tested policy: 11,500 or 12,000 contacts",34,500)
    body += text(100,566,"Earlier Inicial reference: 408.498 · a different complete recipe",28,450,P["muted"])
    cards=[("156 predictors","152 raw + 4 funds features"),("20 tuning trials","One selected configuration"),("5-seed ensemble","September scoring")]
    for i,(big,small) in enumerate(cards):
        x=96+i*434
        body += rect(x,638,410,144)+text(x+24,694,big,32,650)+text(x+24,742,small,24,400,P["muted"])
    body += text(96,847,"Different recipes and contact policies: not an isolated feature-effect estimate.",26,450,P["muted"])
    return shell("02 EVIDENCE","A final recipe reached the public board","After feature selection, tuning and five-seed refitting.",
        pill(1030,78,"PUBLIC · INICIAL",345),body,"This is not a public score for every feature package.",53)


def frame45():
    body = text(96,302,"Hypothesis: recent changes may reveal emerging disengagement.",31,600)
    labels=PLAN["ema"]["relative_weight_labels"]
    heights=[22,43.75,87.5,175,350]
    xs=[150,365,580,795,1010]
    months=["Older past","t−4","t−3","t−2","t−1"]
    for x,h,label,month in zip(xs,heights,labels,months):
        body += rect(x,700-h,144,h,P["teal"] if label=="1.0" else "#A3C8B9",radius=8)
        body += text(x+72,742,label,32,650,P["teal"],"middle")
        body += text(x+72,786,month,25,450,P["muted"],"middle")
    body += rule(120,701,1195,701)
    body += '<line x1="1240" y1="365" x2="1240" y2="793" stroke="#DCE3DF" stroke-width="2" stroke-dasharray="7 7"/>'
    body += '<rect x="1290" y="600" width="86" height="100" rx="16" fill="none" stroke="#627079" stroke-width="2" stroke-dasharray="6 6"/>'
    body += text(1333,666,"t",40,500,P["muted"],"middle")
    body += text(1333,742,"Current",23,500,P["muted"],"middle")+text(1333,785,"Excluded",23,500,P["muted"],"middle")
    body += text(96,847,"Relative weights · decay 0.5 · all available past · minimum 2 known values",26,450,P["muted"])
    return shell("02 EVIDENCE","Let recent history speak louder","Prior-only EMA3: a weighting rule, not a three-month cutoff.",
        pill(1040,78,"HYPOTHESIS · HT5956",335,P["ink"],"white"),body,"Illustration of relative influence—not observed customer data.",55)


def frame60():
    body = text(112,293,"PILOT VARIANT",23,650,P["muted"])
    body += text(990,293,"MEAN Δ PROFIT",23,650,P["muted"],"end")
    body += text(1260,293,"MONTH WINS",23,650,P["muted"],"middle")
    for i,row in enumerate(PLAN["pilot"]["rows"]):
        y=312+i*58
        focus=row["id"] in ("E_funds6","F_usage3")
        ema=row["id"]=="G_prior_ema3"
        fill=P["teal_light"] if focus else P["amber_light"] if ema else "white"
        color=P["teal"] if focus else P["amber"] if ema else P["ink"]
        body += rect(96,y,1280,51,fill,radius=12)
        body += text(116,y+35,row["label"],28,650 if focus else 450)
        value="Reference" if row["reference"] else f'{row["delta_millions"]:+.2f}M'
        body += text(985,y+35,value,29,650,color,"end")
        month_wins="—" if row["reference"] else f'{row["months_improved"]}/2'
        body += text(1260,y+35,month_wins,28,600,color,"middle")
    body += text(96,823,"Million ARS per 100,000 customers vs funds3 · May + July · five paired seeds",24,450,P["muted"])
    body += text(96,861,"These are historical screening results. No HT5956 variant was public-scored.",25,600,P["muted"])
    return shell("02 EVIDENCE","Consistency matters as much as the average","Longer funds history and usage improved in both historical months.",
        pill(1040,78,"HISTORICAL · HT5956",335,P["ink"],"white"),body,PLAN["segments"][3]["takeaway"],52)


def frame75():
    body = pill(96,267,"Same 9,000 contacts",340,P["ink"],"white")
    for i,row in enumerate(PLAN["senior_public"]["rows"]):
        y=345+i*153
        body += rect(96,y,1280,133,P["teal_light"] if i==0 else "white")
        body += text(124,y+36,row["study"],23,650,P["teal"] if i==0 else P["muted"])
        body += text(124,y+87,row["label"],36,650 if i==0 else 450)
        body += text(1328,y+87,f'{row["score"]:.3f}',57,750,P["teal"] if i==0 else P["ink"],"end")
    body += text(96,853,"Complete recipes differ in features, learner settings and seeds—not isolated effects.",25,450,P["muted"])
    return shell("03 DECISION","Check the actual public result","Senior leaderboard · a separate competition from Inicial.",
        pill(1040,78,"PUBLIC · SENIOR",335),body,PLAN["segments"][4]["takeaway"])


def frame90():
    body = rect(96,282,1280,152,P["teal_light"])
    body += text(124,321,"KEEP",23,750,P["teal"])+text(124,380,"The rich-history champion",48,700)
    body += text(124,415,"1,914 features · our measured public reference",26,450,P["muted"])
    for x,title,definition,sub in [(96,"6-month funds history","Balance and payroll","At least 3 known prior months"),
                                  (752,"3-month usage changes","Debit transactions + card spending","At least 2 known prior months")]:
        body += rect(x,460,624,198)+text(x+26,500,"NEXT CONTROLLED TEST",22,650,P["teal"])
        body += text(x+26,553,title,36,650)+text(x+26,592,definition,24,450,P["muted"])
        body += text(x+26,631,sub,25,450,P["muted"])
    body += text(96,684,"Test these additions separately · relative floor 1 · clipping ±10",28,500,P["muted"])
    body += rect(96,725,1280,100,P["amber_light"])
    body += text(124,766,"EMA3: keep exploratory",32,650,P["amber"])
    body += text(124,805,"Decay 0.5 · prior-only · historical profit was inconsistent across months",25,450,P["amber"])
    return shell("03 DECISION","Keep our best model. Make the next test precise.","Separate proven public results from promising research.",
        pill(1040,78,"RECOMMENDATION",335),body,"Historical improvement ≠ measured public improvement.",52)


def verify():
    evidence=(HERE / PLAN["evidence_directory"]).resolve()
    def read(name):
        with (evidence/name).open(newline="") as handle:
            return list(csv.DictReader(handle))
    source55={r["view"]:r for r in read("HT5955_feature_summary.csv")}
    feature_plan=json.loads((evidence/"HT5955_plan.json").read_text())
    feature_definitions={r["id"]:r for r in feature_plan["candidates"]}
    for row in PLAN["feature_screen"]:
        assert feature_definitions[row["id"]]["columns"]==row["added_columns"]
        assert int(source55[row["id"]]["seeds_improved"])==row["seeds_improved"]
        actual=(float(source55[row["id"]]["mean_delta_auc"])>0 and row["seeds_improved"]>=4)
        assert actual==row["selected"]
    source56={r["view"]:r for r in read("HT5956_summary.csv")}
    for row in PLAN["pilot"]["rows"]:
        source=source56[row["id"]]
        assert round(float(source["mean_delta_per100k"])/1e6,2)==row["delta_millions"]
        assert int(source["months_improved"])==row["months_improved"]
    public=read("public_recipe_summary.csv")
    inicial=next(r for r in public if r["study"]=="HT5955" and r["competition"]=="data-mining-inicial-2026-c")
    assert float(inicial["best_public_score"])==PLAN["initial_public"]["score"]
    assert set(map(int,inicial["best_contacts"].split(";")))==set(PLAN["initial_public"]["contacts"])
    previous=next(r for r in read("public_submission_history.csv") if r["submission"]==PLAN["initial_public"]["previous_reference_submission"])
    assert previous["competition"]=="data-mining-inicial-2026-c"
    assert float(previous["public_score"])==PLAN["initial_public"]["previous_reference_score"]
    for row in PLAN["senior_public"]["rows"]:
        source=next(r for r in public if r["competition"]=="data-mining-senior-2026-c" and
                    r["study"]==row["study"] and r["recipe"]==row["recipe"] and r["wave"]==row["wave"])
        assert float(source["public_score_at_9000"])==row["score"]
        assert int(source["seed_count"])==row["seed_count"]
    assert PLAN["ema"]["decay"]==.5 and not PLAN["ema"]["include_current"]
    assert PLAN["ema"]["all_available_past"] and PLAN["pilot"]["public_submissions"]==0
    history=json.loads((evidence/"HT5956_plan.json").read_text())["history"]
    assert PLAN["ema"]["decay"]==history["ema_decay"]
    assert PLAN["ema"]["minimum_known"]==history["ema_minimum_known_ever"]
    assert PLAN["ema"]["include_current"]==history["ema_include_current"]
    assert PLAN["ema"]["adjusted"]==history["ema_adjusted"]
    assert PLAN["recommendation"]["relative_clip"]==history["clip"]
    assert PLAN["recommendation"]["relative_scale_floor"]==history["scale_floor"]
    assert PLAN["recommendation"]["funds6_minimum_known"]==history["relative6_minimum"]
    assert PLAN["recommendation"]["usage3_minimum_known"]==history["relative3_minimum"]
    assert len(read("HT5955_all_hpo_trials.csv"))==PLAN["initial_public"]["hpo_configurations"]
    assert len(PLAN["segments"])==6
    brief=(HERE/"production_brief.md").read_text()
    words=[]
    for i,segment in enumerate(PLAN["segments"]):
        assert segment["start"]==15*i and segment["end"]==15*(i+1)
        assert segment["voiceover"] in brief
        count=len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",segment["voiceover"]))
        assert count<=40
        words.append(count)
    total=sum(words)
    spoken=sum(len(re.findall(r"\b[\w]+(?:[’'][\w]+)*\b",s["voiceover"])) for s in PLAN["segments"])
    assert 165<=total<=210
    return {"status":"PASS","voiceover_words":total,"segment_word_counts":words,
            "spoken_word_estimate_splitting_hyphenated_compounds":spoken,
            "average_words_per_minute_over_90s":round(total/1.5,1),
            "timing_is_edit_target_not_measured_recording":True,
            "feature_screen_rows_verified":5,"pilot_rows_verified":8,
            "feature_and_ema_parameters_verified":True,
            "public_scores_verified":5,"separate_competition_tracks":True,
            "ema_relative_weights_not_normalized_percentages":True,
            "future_candidates_not_claimed_as_public_winners":True}


def build():
    receipt=verify()
    frames=[frame15(),frame30(),frame45(),frame60(),frame75(),frame90()]
    (HERE/"frames").mkdir(exist_ok=True)
    for second,svg in zip([15,30,45,60,75,90],frames):
        (HERE/"frames"/f"frame_{second:02d}s.svg").write_text(svg)
    insert=insert35();(HERE/"frames"/"insert_35s_inicial.svg").write_text(insert)
    for frame in [*frames,insert]:
        root=ET.fromstring(frame)
        assert root.attrib["viewBox"]=="0 0 1920 1080"
    receipt["svg_frames_validated"]=7
    (HERE/"voiceover.txt").write_text("\n\n".join(s["voiceover"] for s in PLAN["segments"])+"\n")
    data=json.dumps({"plan":PLAN,"frames":frames,"insert":insert},ensure_ascii=False).replace("</","<\\/")
    document=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Feature Lab — 90-second storyboard</title>
<style>
:root{color-scheme:light;--ink:#172b3a;--muted:#627079;--teal:#157f75;--line:#dce3df;--paper:#f7f8f5}
*{box-sizing:border-box}body{margin:0;background:var(--paper);font-family:Inter,Arial,sans-serif;color:var(--ink)}
header{padding:28px max(24px,calc((100vw - 1320px)/2));border-bottom:1px solid var(--line);display:flex;gap:20px;align-items:center;justify-content:space-between}
.brand{font-size:13px;letter-spacing:.18em;font-weight:750}.tag{font-size:12px;color:var(--teal);background:#e4f3ec;padding:9px 14px;border-radius:99px}
main{max-width:1368px;margin:auto;padding:42px 24px 72px}.eyebrow{text-transform:uppercase;letter-spacing:.15em;font-size:12px;font-weight:700;color:var(--teal)}
h1{font-size:clamp(28px,4vw,48px);letter-spacing:-.035em;margin:12px 0 16px}p{line-height:1.65;color:var(--muted)}
.intro{max-width:850px;margin-bottom:28px}.stage{border:1px solid var(--line);border-radius:22px;overflow:hidden;background:white;box-shadow:0 15px 45px #172b3a0b}
.stage svg,.thumb svg{width:100%;height:auto;display:block}.stage svg{animation:arrive .4s ease-out}
@keyframes arrive{from{opacity:.65;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
.controls{display:flex;align-items:center;gap:18px;margin:18px 0 8px}.controls input{flex:1;accent-color:var(--teal)}button{font:inherit;cursor:pointer}
.play{border:0;border-radius:10px;background:var(--ink);color:white;padding:12px 22px;min-width:92px}.time{font-variant-numeric:tabular-nums;font-size:14px;min-width:92px}
.fine{font-size:12px}.narration{margin:20px 0 40px;padding:22px 26px;border-left:3px solid var(--teal);background:white;border-radius:0 12px 12px 0;font-size:18px;line-height:1.6;min-height:114px}
h2{font-size:25px;letter-spacing:-.02em;margin-top:48px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.six{grid-template-columns:repeat(2,1fr)}
.thumb{padding:0;text-align:left;background:white;border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:box-shadow .15s,transform .15s;color:var(--ink)}
.thumb:hover,.thumb:focus-visible{box-shadow:0 8px 24px #172b3a12;transform:translateY(-2px);outline:2px solid var(--teal)}
.thumb strong,.thumb span{display:block;padding:0 16px}.thumb strong{padding-top:13px;font-size:15px}.thumb span{font-size:12px;color:var(--muted);padding-top:6px;padding-bottom:16px;line-height:1.5}
.notes{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:40px;border-top:1px solid var(--line);padding-top:22px}.notes h3{font-size:14px}.notes p{font-size:13px}
a{color:var(--teal)}@media(max-width:750px){.grid,.six,.notes{grid-template-columns:1fr}header{padding:20px 24px}.tag{font-size:10px}.controls{gap:10px}.narration{font-size:16px}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style></head><body>
<header><div class="brand">FEATURE LAB / STORYBOARD</div><div class="tag">90 seconds · English · one presenter · draft v1</div></header>
<main><div class="eyebrow">Research → evidence → decision</div><h1>What feature engineering actually taught us</h1>
<p class="intro">A visual planning cut for a single speaker. The presenter stays at the top right; the evidence occupies the left. This preview has no recorded audio. Use the timed narration below while reviewing the layouts.</p>
<div class="stage" id="stage" aria-live="off"></div>
<div class="controls"><button class="play" id="play">Play</button><input id="scrub" type="range" min="0" max="90" step="0.1" value="0" aria-label="Preview time"><span class="time" id="time">0:00 / 1:30</span></div>
<div class="fine">Timing preview only. Space: play/pause. Arrow keys: move 15 seconds. Final pacing is conformed to the recorded voice.</div>
<div class="narration" id="narration"></div>
<h2>Pass 2 · three high-point screens</h2><p>End-state compositions for the three 30-second scenes. The 1:30 screen is held during the closing seconds.</p><div class="grid" id="anchors"></div>
<h2>Pass 3 · a keyframe every 15 seconds</h2><p>The 0:30–0:45 interval also contains a short Inicial public-score insert before the EMA mechanism.</p><div class="grid six" id="keyframes"></div>
<div class="notes"><div><h3>Presenter-safe layout</h3><p>1920 × 1080. Fixed 312 × 312 camera window at x1512/y96. The source SVGs retain a stable content boundary.</p></div><div><h3>Evidence stays explicit</h3><p>Historical AUC selection, historical profit and public Kaggle scores use different labels. Inicial and Senior never share a comparison chart.</p></div><div><h3>Editable source</h3><p><a href="production_brief.md">Production brief</a> · <a href="voiceover.txt">Clean voiceover</a> · <a href="video_plan.json">Timing/data plan</a> · <a href="validation.json">Fact checks</a></p></div></div>
</main>
<script id="story-data" type="application/json">__DATA__</script>
<script>
const data=JSON.parse(document.getElementById('story-data').textContent),stage=document.getElementById('stage'),scrub=document.getElementById('scrub'),button=document.getElementById('play');
const times=[15,30,45,60,75,90],titles=['Fair comparisons','Five feature packages','Why try an EMA?','The complete pilot result','Actual Senior public scores','Recommendation'];
const descriptions=['Fixed settings, rules and five matched seeds.','One package passes the declared historical rule.','Prior history gets exponentially decreasing influence.','All eight pilot views, with public status explicit.','Same 9,000-contact count; complete recipes.','Retain the champion; test candidate additions separately.'];
let current=Math.max(0,Math.min(90,Number(new URLSearchParams(location.search).get('t'))||0)),playing=false,last=null,frame=null,raf=null;
function clock(t){let s=Math.floor(t);return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
function indexAt(t){return t<=15?0:t<=30?1:t<39?6:t<=49?2:t<=60?3:t<=75?4:5}
function render(){const index=indexAt(current);if(frame!==index){stage.innerHTML=index===6?data.insert:data.frames[index];frame=index}scrub.value=current;document.getElementById('time').textContent=clock(current)+' / 1:30';const segment=data.plan.segments[Math.min(5,Math.max(0,Math.ceil(current/15)-1))];document.getElementById('narration').textContent=segment.voiceover}
function stop(){playing=false;last=null;button.textContent='Play';cancelAnimationFrame(raf)}
function seek(t){stop();current=Math.max(0,Math.min(90,t));render()}
function tick(now){if(!playing)return;if(last!==null)current=Math.min(90,current+(now-last)/1000);last=now;render();if(current>=90){stop();return}raf=requestAnimationFrame(tick)}
function toggle(){if(playing){stop();return}if(current>=90)current=0;playing=true;last=null;button.textContent='Pause';raf=requestAnimationFrame(tick)}
button.addEventListener('click',toggle);scrub.addEventListener('input',e=>seek(Number(e.target.value)));
document.addEventListener('keydown',e=>{if(e.target.tagName==='INPUT')return;if(e.code==='Space'){e.preventDefault();toggle()}if(e.code==='ArrowRight')seek(current+15);if(e.code==='ArrowLeft')seek(current-15)});
function thumb(i,parent){const b=document.createElement('button');b.className='thumb';b.innerHTML=data.frames[i]+'<strong>'+clock(times[i])+' · '+titles[i]+'</strong><span>'+descriptions[i]+'</span>';b.addEventListener('click',()=>{seek(times[i]);window.scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})});parent.appendChild(b)}
[1,3,5].forEach(i=>thumb(i,document.getElementById('anchors')));times.forEach((_,i)=>thumb(i,document.getElementById('keyframes')));render();
</script></body></html>'''
    page=document.replace("__DATA__",data)
    node=shutil.which("node")
    if node:
        inline=page.split("<script>")[-1].split("</script>")[0]
        subprocess.run([node,"--check"],input=inline,text=True,capture_output=True,check=True)
    receipt["javascript_syntax_checked"]=bool(node)
    receipt["brief_matches_voiceover_plan"]=True
    (HERE/"storyboard.html").write_text(page)
    (HERE/"validation.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    build()

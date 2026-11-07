# Feature engineering: a 90-second video

## 1. Scope and narrative

**Working title:** What feature engineering actually taught us.

**Format:** 90 seconds, English, one person narrating, 16:9, 1920×1080,
30 frames/second. Their headshot remains at the top right throughout.

**Evidence cutoff:** the verified public-score snapshot from November7,2026,
01:20UTC. Update the evidence before recording if later experiments change it.

**The single takeaway:** well-designed historical feature comparisons identified
research candidates, but did not establish a new public-score champion. Retain
the rich-history champion and make further feature tests precise.

This short cut follows the hypothesis-led HT5955 feature screen, the HT5956
history/normalization pilot, and the later public evidence from HT5958/59/60.
It groups results by feature family rather than attempting to narrate hundreds
of HPO settings. All five first-screen packages and all eight pilot views are
represented in the visuals. Complete historical parameter/public-score tables
remain available in the underlying audit.

**Files to use**

- Open [`storyboard.html`](storyboard.html) for an offline visual/timing preview.
- [`voiceover.txt`](voiceover.txt) is the clean teleprompter script.
- [`video_plan.json`](video_plan.json) holds the timings, labels and locked data.
- [`frames/`](frames/) contains six full-size SVG/PNG keyframes plus the Inicial
  insert, all at1920×1080. PNGs can be used as image-to-video reference frames.
- [`validation.json`](validation.json) records checks against the original audit.

The preview contains a presenter placeholder and no recorded voice. Its playback
is a planning cut, not a finished animation. The recording determines final
sentence timings; leave brief reading pauses and hold the closing screen.

## 2. Timed voiceover

Read conversationally: measured and explanatory, with emphasis on **same**,
**historical**, **public**, and **keep**. The script uses approximate scores in
speech to avoid awkward decimal dictation; exact values appear on screen.

| Time | Spoken script | What the viewer should understand |
|---|---|---|
| **00:00–00:15** | We tested whether recent behavior helps predict leaving the Premium package. Each feature variant was retrained with the same learner settings and training rules, using five matched random seeds. | Fair comparisons require retraining under the same rules; the weights were not held fixed. |
| **00:15–00:30** | We compared last-month values, monthly changes, three-month averages, balance and payroll relative to their own recent averages, and card utilization. Only relative funds passed our predeclared selection rule. | What was engineered, and which package advanced. |
| **00:30–00:45** | After tuning, that ensemble scored about four hundred and two on Inicial, below our earlier reference. We then tested six-month history, monetary ranks, usage changes, and an exponential moving average. | The first public outcome belongs to a full tuned pipeline; a separate follow-up investigated richer history. |
| **00:45–01:00** | We expected EMA to flag disengagement by emphasizing recent behavior. Six-month funds and three-month usage improved historical profit in both months. EMA’s profit benefit was inconsistent. These variants were never publicly scored. | The EMA hypothesis, the observed historical outcomes, and the absence of public pilot scores. |
| **01:00–01:15** | Later engineered pipelines reached the Senior leaderboard. None beat our champion’s public score of about four hundred and fifty-four. That champion already includes extensive historical features. | The stronger public benchmark already contains feature engineering. |
| **01:15–01:30** | Our recommendation: keep the rich-history champion. Prioritize controlled retests of six-month funds history and three-month usage. Keep EMA exploratory, and distinguish historical improvements from measured public performance. | What to retain, what to investigate, and what has not been established. |

### Delivery notes

The script contains172written words, approximately181spoken-word equivalents
when hyphenated compounds are expanded. At125–130words/minute, allow about84–87
seconds of speech plus brief pauses/closing hold to reach90seconds. The15-second
blocks are edit targets until the actual narration is recorded.

- Say **“E–M–A”**, then use the weighting graphic to explain it.
- “Five matched seeds” means five paired randomized retrainings on the same
  validation month, not five independent temporal holdouts.
- “Relative funds” means balance/payroll compared with that customer's own prior
  level, not a comparison of every customer's currency amounts on one scale.
- “Both months” means the pilot's **May and July 2021** historical checks.
- Preserve the two competition names in speech. Inicial's roughly402 and
  Senior's roughly454 must not become one apparent before/after improvement.

## 3. Design pass one: look, feel and scene flow

### Visual language

An editorial research explainer: warm off-white background, navy typography,
generous empty space and a small set of flat vector elements. The viewer follows
**Design → Evidence → Decision**. No decorative dashboards or faux customer data.

| Element | Specification |
|---|---|
| Background | `#F7F8F5` |
| Primary text | Navy `#172B3A` |
| Supporting text | Slate `#627079` |
| Retained/focus highlight | Teal `#157F75`, pale fill `#E4F3EC` |
| Mixed/exploratory finding | Amber `#9A690C`, pale fill `#FFF2D7` |
| Rules/dividers | `#DCE3DF` |
| Typography | Inter or a clean sans-serif fallback; 52–58px titles, 28–36px data text at1080p |
| Motion | Flat position/opacity changes, 0.3–0.6s easing, consistent direction |
| Presenter | 312×312px, x1512/y96; softly rounded crop; stable position/scale |
| Content area | x96–1424, y72–864; a clear gap separates it from the presenter |
| Lower band | y894–1024; one takeaway line in planning frames, reserved for two-line subtitles in the edit |

The presenter records in a quiet neutral setting, with their face clearly lit
and eyes near the upper third of the crop. The presenter remains visually
secondary to the evidence and does not move between corners.

### Three-scene arc

| Scene | Time | Emotional/visual purpose | End-state high point |
|---|---|---|---|
| **1. Design a fair comparison** | 00:00–00:30 | Begin with one simple question. Build a baseline-versus-one-package diagram, then reveal the five package outcomes. | **00:30:** only relative funds passes the first ranking-quality rule. |
| **2. Explain the mechanism and evidence** | 00:30–01:00 | Briefly show the first public result. Explain EMA with weighted historical bars, then reveal the complete pilot result. | **01:00:** funds6/usage3 are consistent historical candidates; EMA is mixed; no pilot public score exists. |
| **3. Make the recommendation** | 01:00–01:30 | Use a separate Senior public-score screen to ground the decision, then reduce the screen to three clear recommendations. | **01:30:** keep the champion; retest precise candidates; EMA stays exploratory. |

**Editorial rhythm:** one focal idea at a time. Results are not animated as
changing measured values. Reveal the fixed labels/numbers, then use a restrained
highlight to guide the eye. The headshot stays stable during every transition.

## 4. Design pass two: 30-second high-point screens

These are the final poses of each30-second scene. They should settle several
seconds before the milestone so viewers have time to read them. The closing pose
lands around01:25 and holds through01:30.

### High point A — 00:30: one feature package passes

**Asset:** [editable SVG](frames/frame_30s.svg) · [PNG reference](frames/frame_30s.png)

**Title:** “One package passed the first screen.”

**Composition:** a five-row table fills the left content area. Three columns:
feature package, short parameter definition, and number of paired seed AUC wins.
The relative-funds row alone has a pale teal background and a small checkmark.
Other rows stay neutral; they are not displayed as universally bad features.
Presenter: same top-right crop. Top-right content badge: **HISTORICAL · HT5955**.

| Feature row | Parameter shown | AUC wins across matched seeds |
|---|---|---:|
| Last-month values | Lag1 | 1/5 |
| Monthly changes | Delta1 | 3/5 |
| Three-month averages | Prior3, minimum2 known | 3/5 |
| **Relative balance + payroll** | **Change versus own prior3** | **5/5** |
| Card utilization | Balance÷positive limit | 2/5 |

**Small explanatory line:** “Rule: positive mean AUC change + at least4 of5
seed wins.” This was a ranking-quality selection rule, not a public profit test.

**Eye path:** title → teal row →5/5 → rule. The screen gives the outcome of all
five feature packages without narrating five separate statistics.

**Arrival:** reveal the table in neutral gray as the packages are spoken; add the
teal highlight only on “Only relative funds…”. Hold the complete table through
the end of the sentence. No winner podium or money animation.

### High point B — 01:00: the complete pilot result

**Asset:** [editable SVG](frames/frame_60s.svg) · [PNG reference](frames/frame_60s.png)

**Title:** “Consistency matters as much as the average.”

**Composition:** one clean eight-row result table. Columns: variant, mean profit
delta, months with improvement. Pale teal highlights the funds6 and usage3 rows.
The EMA row uses pale amber because its positive average did not hold in both
months. The baseline row reads “Reference”, rather than suggesting it lost0/2.
Badge: **HISTORICAL · HT5956**. Presenter stays at the top right.

| Pilot variant | Mean historical Δ profit | Month wins |
|---|---:|---:|
| Raw snapshot | +0.24M | 1/2 |
| Funds3 | Reference | — |
| Raw + monetary ranks | −1.15M | 1/2 |
| Funds3 + ranks | +1.76M | 2/2 |
| **Funds3 + funds6** | **+4.32M** | **2/2** |
| **Funds3 + usage3** | **+2.49M** | **2/2** |
| Funds3 + prior EMA3 | +4.01M | 1/2 |
| Funds3 + ranks + usage3 | −0.18M | 1/2 |

**Unit line, always attached to the table:** “Million ARS per100,000 customers
versus funds3 · May+July · five paired seeds.” These are mean paired historical
fixed-policy profit differences, not Kaggle scores or ensemble-profit differences.

**Bottom message:** “No HT5956 variant was public-scored.”

**Eye path:** funds6/usage3 →2/2 → EMA1/2 → no-public-score message. The full
table also retains the rank-only and combined-variant outcomes, including losses.

**Arrival:** display all rows neutrally, then emphasize funds6 and usage3. On
“EMA’s profit benefit was inconsistent”, highlight its1/2 in amber. The no-public
message is persistent; do not show a fake Kaggle score of zero.

### High point C — 01:30: a precise recommendation

**Asset:** [editable SVG](frames/frame_90s.svg) · [PNG reference](frames/frame_90s.png)

**Title:** “Keep our best model. Make the next test precise.”

**Composition:** one large teal “KEEP” card for the1,914-feature champion. Beneath
it, two equal neutral cards: **6-month funds history** and **3-month usage changes**.
Their subtitles show minimum3 and minimum2 prior observations. A thin line below
says: “Test these additions separately · relative floor1 · clipping±10.”
An amber strip below reads **“EMA3: keep exploratory”**, with decay.5, prior-only,
and inconsistent historical monthly profit. Presenter remains at top right.

**Closing takeaway:** “Historical improvement ≠ measured public improvement.”

**Eye path:** keep proven model → two next-test candidates → exploratory EMA →
closing distinction. These are research/retest priorities, not a claim that the
funds6 or usage3 additions have been approved for deployment or beaten the champion.

**Arrival:** retain the champion card from the preceding public-score screen,
change the heading to the decision, and introduce the two test cards. Keep them
separate: the joint funds6+usage3 combination was not established by the pilot.
Hold the complete composition for the final five seconds.

## 5. Design pass three: 15-second keyframes and transitions

| Milestone | Screen | What is fully visible | How to get there / transition onward |
|---|---|---|---|
| **00:15** | [`frame_15s.svg`](frames/frame_15s.svg) | Baseline152 predictors → baseline+one package. “Same settings”, “same training rules”, five matched seed markers. | Start with the question, reveal the two model-input cards, then bring in the seed row. At15s, collapse the candidate card into the first row of the package table. |
| **00:30** | [`frame_30s.svg`](frames/frame_30s.svg) | All five feature families, AUC-win counts, one selected row. | The selected row becomes a compact “152raw+4funds” tile. Crossfade to the public Inicial insert while “After tuning…” is spoken. |
| **00:45** | [`frame_45s.svg`](frames/frame_45s.svg) | EMA hypothesis, prior-month relative weights, current snapshot excluded. | The public insert exits before the EMA diagram enters. Weight bars rise from their common baseline; older bars are smaller and lighter. After the hypothesis sentence, crossfade to the pilot result table. |
| **01:00** | [`frame_60s.svg`](frames/frame_60s.svg) | Eight historical pilot rows, precise units,2/2 versus1/2, no public submissions. | Highlight consistent candidates, then mixed EMA. Change the badge to “PUBLIC · SENIOR” during a short clean crossfade; do not morph historical-profit numbers into public scores. |
| **01:15** | [`frame_75s.svg`](frames/frame_75s.svg) | Three Senior public scores at the same9,000 contacts. Champion453.831; full Senior pipeline447.998; R2three-seed439.331. | Retain the champion score card; fade the two challengers. That retained card becomes the “KEEP” recommendation, maintaining its position and teal treatment. |
| **01:30** | [`frame_90s.svg`](frames/frame_90s.svg) | Retain/retest/exploratory recommendation, exact history parameters and the closing distinction. | Land the full screen around01:25. A gentle end fade can follow the completed last word after01:30; do not begin it over the recommendation. |

### Essential inserted screen — approximately00:31–00:39

**Asset:** [`frames/insert_35s_inicial.svg`](frames/insert_35s_inicial.svg).

Show **401.915**, clearly tagged **PUBLIC · INICIAL**, with the best tested
contact policies11,500/12,000. A smaller line gives the earlier Inicial reference
**408.498**, explicitly a different complete recipe. Beneath:156predictors →
20tuning configurations → five-seed final ensemble. The comparison changes
recipes and contact policies; it is not a measured effect of one feature.

This inserted beat is important even though it is not a15-second milestone:
the narrator's first public result must have an actual screen. It is removed
before the separate Senior comparison appears later.

### EMA animation specification

- Five historical positions progress from older to more recent **past** months.
- The newest past observation,t−1, has relative weight1; preceding values carry
  .5,.25,.125 and a faded older-history tail. Label them **relative weights**.
- A dashed divider and a separate current-month tile show that this feature
  excludes the current observation. Other model predictors can still use current
  covariates; this exclusion describes the EMA statistic only.
- EMA3 means a span/decay convention; it is **not** a hard three-observation
  moving window. All available prior history may contribute. Calendar gaps,
  missingness, normalization and the minimum-known rule affect the actual average.
- The bars explain the computation. They are not measured customer values and
  do not imply that any particular person's balance was observed falling.

### Transition mechanics

Use10–18-frame position/opacity transitions at30fps. Keep the same margins,
typography and camera crop. Let numbers appear at their final values; use motion
to reveal structure and attention rather than to simulate evolving measurements.
Keep a clear reading hold after each result reveal. Replace the planning
takeaway line with properly timed two-line subtitles if captions are included.

## 6. Animation production prompts

### Global style instruction

> Minimal flat2D editorial research explainer,16:9, warm off-white canvas,
> navy typography area, restrained teal highlights and amber for mixed findings.
> Generous empty space. Keep the entire top-right312×312 presenter area stable
> and clear. Use simple cards, rules and geometric bars. Motion is calm, precise
> and eased. Follow the supplied SVG keyframe composition. Produce shape motion
> plates; final labels, numbers, tables and subtitles are composited from the
> editable vector/text layers supplied with the storyboard.

| Beat | Motion prompt to append to the global style |
|---|---|
| Fair comparison | “A baseline card enters from the left. A matching card gains one small feature tile. Five paired run markers appear below, in the same order for both variants. Hold the balanced composition.” |
| Feature selection | “Resolve the feature card into a five-row table. Reveal rows in voice order. Only the fourth row gains a pale teal fill and a small checkmark. Keep the other rows neutral.” |
| Inicial public insert | “Move the selected feature tile into a three-step pipeline: predictors, tuning, ensemble. Reveal one large public-score text layer. Hold, then fade the score composition out cleanly before the next historical mechanism.” |
| EMA mechanism | “Reveal historical bars from oldest to newest. Each newer past bar carries twice the relative influence of the preceding one. The current-month tile stays outlined beyond a divider. A small older-history tail remains visible.” |
| Pilot evidence | “Reveal the fixed eight-row result table. Gently emphasize the two consistent candidate rows. Then shift attention to the amber EMA consistency cell. Preserve the no-public-submissions footer throughout.” |
| Senior comparison | “Reveal three neutral public-score cards. The first is emphasized in teal. Use the same scale and contact-policy label for all three. Retain the first card for the transition into the recommendation.” |
| Recommendation | “Retain the champion card. Introduce two equal, separate next-test cards beneath it. Bring in the amber exploratory-EMA strip last. Settle into a clear five-second reading hold.” |

**Compositing order:** background → animated geometric plates → locked SVG
labels/data → recorded presenter crop → subtitle layer. This keeps exact numeric
evidence legible while still allowing AI-created motion.

## 7. Evidence and factual guardrails

### Data used by the video

| Claim | Original verified source |
|---|---|
| Five feature packages; AUCwins1/3/3/5/2; only relativefunds passes | `research_notes/Feature engineering public outcome audit/HT5955_feature_summary.csv` |
| Selected feature definitions; relative3minimum2, floor1, clip±10 | `HT5955_plan.json` in the same audit directory |
|401.915Inicial public result,11,500/12,000contacts | `public_recipe_summary.csv`; submissions57852532/57852534 |
| Earlier Inicial reference408.498 | `public_submission_history.csv`; submission57670712 |
| Eight pilot gains, units, monthly consistency | `HT5956_summary.csv`; mean paired per-seed deltas, normalized per100k |
| Prior-only EMA3, decay.5, minimum2 known observations | `HT5956_plan.json` |
| Senior453.831/447.998/439.331at9,000contacts | `public_recipe_summary.csv`; HT5958,HT5960,HT5959W2R2 |

Paths in the first row resolve from the homework root. The script and generated
frames are tied to these files by `build_storyboard.py`; rerun it after editing
the plan to check source values and regenerate the preview.

### Rules for the edit

1. **Separate metrics.** AUC selection, historical profit and public leaderboard
   scores are different measurements. Every result screen names its measurement.
2. **Separate competitions.** Inicial and Senior never share a before/after chart.
3. **Respect attribution.**401.915belongs to a selected, tuned, refitted ensemble
   and contact policy.447.998also belongs to a complete pipeline, not an isolated
   IPC/RF/canary feature experiment.
4. **Respect missing outcomes.** Unsubmitted pilot variants have no public score;
   display that absence as text, not a score of zero or a red failure label.
5. **Respect replication.** Five seeds are paired repeats on the same month.
   May/July are inspected historical checks, not untouched future validation.
6. **Respect the recommendation.** Funds6andusage3are priorities for controlled
   retesting, not novel unexplored families or demonstrated public winners. R2's
   existing rich transfer results were unfavorable; the video does not promote it.
7. **Respect formulas.** Relative-history floor1 and clipping±10 are the tested
   pilot settings. EMA uses normalized prior-history weights with calendar-aware
   decay; its illustrative1/.5/.25labels are not universal normalized percentages.
8. **Respect policy context.**9,000contacts is a matched ranking benchmark in the
   Senior comparison, not a business ceiling. The video does not establish a
   calibrated deployment threshold or a causal effect of customer behavior.

### Detail available outside the90-second cut

The complete audit is
[`reports/Feature engineering parameters and public outcomes.md`](../../reports/Feature%20engineering%20parameters%20and%20public%20outcomes.md).
It includes the wider HT5945/54 searches, all recovered HPO configurations,
public cutoff curves and the distinction between published and historical-only
recipes. That supporting detail is retained rather than compressed into unreadable
on-screen HPO tables.

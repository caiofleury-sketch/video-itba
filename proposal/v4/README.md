Revision 4: clearer campaign stakes and a readable results chart.

Open index.html for the offline interactive draft, or play animatic_120s.mp4 once rendering completes. Both are two minutes. The video is silent; voiceover.txt is the revised 249-word script. Earlier revisions remain unchanged.

What changed:
- The measurement scene now shows two stylized people and the actual competition scoring rule: +AR$975,000 for selecting a November leaver, −AR$25,000 for selecting another customer, zero for no contact.
- A pairwise ordering illustration explains what a useful ranking does: put the target leaver ahead of another customer.
- The chart replaces raw AUC differences with expected extra correctly ordered pairs per 10,000. The largest gain becomes about +15, rather than +0.001456. This is not +15 customers found, customers retained, or pesos.
- Profit consistency now says “Higher in May + July” and identifies its reference explicitly.
- The ending labels the full-recipe score as AR$401.9 million, a scaled public campaign estimate. Individual-feature public profit differences are still pending the other agent's controlled submissions.

The 3D history hook, nine-family feature map, identity glyphs, color semantics, single consolidated chart, and headshot-safe corner remain. Numerical AUC results are unchanged and remain available in the evidence details.

The extra pair equivalents use the standard AUC interpretation: P(target ranks above another customer) plus half credit for ties. Relative funds moves the estimated ranking probability from 89.5959% to 89.7415%, a modest +0.1456 percentage points. Multiplying the difference by 10,000 yields about 14.56 pair equivalents. This is an interpretation of ranking quality, not an estimate of campaign recall at a fixed cutoff.

Verification reconciles all nine pasted HT5955 public scores against the existing CSV, checks the conversion, browser layout/navigation and pacing, and the rendered video's dimensions/frame count/duration. The competition description has inconsistent row counts and a private-scaling typo; neither is used for converting the scores into retained-customer counts. Public scores are already in million ARS; no extra 1/0.30 scaling is applied.

Rebuild/check/render from /workspace/video-itba:

python3 proposal/v4/build.py
python3 proposal/v4/verify.py
python3 proposal/v4/render_video.py

The export is a Chromium/SVG review animatic, not a final Manim render. No recorded narration is included. Waiting for actual feature-level public results is not a reason to fabricate monetary deltas: preserve null/missing outcomes until the agent supplies matched files, IDs, settings, and scores.

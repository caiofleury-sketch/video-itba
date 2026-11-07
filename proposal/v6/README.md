Revision 6 — FULL FILM, including the 3D opening.

Use animatic_108s.mp4 for the complete silent 1:48 cut, beginning with the two-customer 3D history sequence. The earlier 54-second feature-only excerpt was intentionally cropped at 16 seconds and was not the full film. No excerpt is the primary deliverable for this revision.

Open index.html for the complete interactive preview. It starts at time zero and clearly says FULL FILM. All four main scenes remain: 3D hook; nine feature constructions and overview; profit-only result layout pending verified data; explicit recommendation.

The new spatial renderer uses XYZ geometry, an orthographic camera, individually shaded faces, wireframes and translucent reference planes. It does not merely rotate a flat illustration. Text, equations, and final comparisons remain in screen space for readability. Block heights represent the explicitly illustrative values where appropriate; uniform feature-output blocks represent column structure, not measured profit.

Feature actions:
- Lag: the previous month's bar is extracted into a separate output block.
- Delta: a shaded gap between the prior and current level materializes.
- Mean: three selected bars converge on a common horizontal plane while raw levels remain as wireframes.
- Relative funds: the personal-reference plane makes the deviation visible.
- Utilization: a segmented 3D annulus fills to the illustrative 80% ratio.
- Six-month history: the reference plane extends to earlier months and changes to the longer mean.
- Usage: activity beads occupy past/current lanes; surplus current beads disappear into unfilled positions.
- Ranks: extruded amount columns reorder, preserving the highlighted customer's identity.
- EMA: past-history particles, sized by relative influence, converge on the weighted output. Current is explicitly excluded, with its contextual bar dimmed/wireframed.

The completed overview stores the same symbols on output tiles. Those tiles travel into the result rows. Results stay flat and readable; there are still no verified feature-level profit values, so no numeric bars are invented. The ending builds two relative-change columns and two near-zero-flag columns into the recommended package.

The source examples and experimental evidence are unchanged. The recommendation is still provisional with respect to incremental public profit. The scoring-rules scene stays removed; no AUC-to-pesos conversion is introduced.

Rebuild/check/render from /workspace/video-itba:
python3 proposal/v6/verify.py
python3 proposal/v6/render_video.py

verification.json checks arithmetic, scene boundaries, geometry, removal of scoring content, null profit values, and the explicit recommendation. opening_export_check.json checks the rendered opening and representative later frames. The review export is Chromium/SVG + FFmpeg, not an unrun Manim render. Recorded narration and verified profit comparisons remain outstanding.

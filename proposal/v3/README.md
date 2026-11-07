Revision 3: a two-minute visual story about the features we added.

Start with `index.html` (offline interactive preview), `animatic_120s.mp4` (silent 1080p/24fps browser animatic, after rendering completes), or `frames/contact_sheet.jpg`. `voiceover.txt` is the 244-word recording script. Earlier revision 2 stays intact in the parent folder.

The structure is one question, one scene containing all nine feature definitions and hypotheses, one brief explanation of measurement, and one consolidated comparison figure. The same comparison stays visible for the closing takeaway. It is framed as one feature-engineering study rather than a chronology of notebook IDs or tuning jobs.

The two metric columns were explicitly selected by the user. Mean AUC differences and profit consistency have different units and reference models. They are not merged into one fabricated numerical score. Monetary ranks remain visible but unresolved because the supplied audit does not verify their exact result. Missing entries are not zero or failure.

The opening uses two explicitly illustrative customer histories, not experimental customer records. The current balance is 80 for both. The amber history is 100/100/100/80; the blue history is 80/80/80/80. The camera unfolds the past into parallel time planes in 3D. The experimental results remain separate from that illustration.

`direction.md` explains the visual story, color semantics, movement, and inspiration from the two supplied references. `production_brief.md` gives the timed scene plan and evidence boundaries.

From `/workspace/video-itba`, run:

```sh
python3 proposal/v3/build.py
python3 proposal/v3/verify.py
python3 proposal/v3/render_video.py
```

The builder uses the existing source reconciliation in `../audit_sources.py`. The verifier uses installed Python Playwright, Pillow, and `/usr/bin/chromium`. Video rendering also uses FFmpeg. No network access is needed. The preview is a single self-contained HTML file.

`verification.json` records browser checks and evidence limits. `render_verification.json` records the exported video's actual dimensions, frame rate, frame count, and duration. The MP4 is silent; narration is not supplied or synthesized. This is a Chromium/SVG animatic with mathematically projected 3D geometry, not a final Manim render. Manim remains the intended production engine.

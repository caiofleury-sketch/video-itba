Última revisión: `v9_es/` contiene la película visual de dos minutos y los puntajes públicos. `audio_v2/` contiene la nueva composición, los videos con y sin subtítulos y sus verificaciones. El paquete de descarga actualizado es `video_final_2min.zip`. Las revisiones anteriores permanecen disponibles.

This is a reviewed and revised proposal, not a finished video or a new experiment.

The scope is the features we added: what they encode, why we added them, how incremental impact was tracked, and what the results support. Inflation/IPC analysis and pre-existing feature inventories are excluded. Existing predictors appear only as the comparison baseline or inputs to a new feature.

Open `storyboard_v2.html` to play or scrub the silent, offline 90-second visual draft. The six scene buttons select compositions. `frames/contact_sheet.jpg` summarizes them. A 200×200 upper-right headshot area remains clear; an optional guide shows placement. Narration and presenter footage have not been supplied.

Read `review/findings.md` for the factual/editorial review, `production_brief_v2.md` for the scene plan, and `voiceover_v2.txt` for the revised 187-word script. `voiceover_v2.json` contains edit targets, not measured recording times. Original uploads remain unchanged under `source/`; their PASS receipts are historical attachments, not our independent verification.

`audited_data.json` contains the selected facts derived from the supplied exports and report. Mean AUC comparisons, feature definitions, selected HPO settings, and public scores were reconciled. Pilot findings are qualitatively report-supported; exact original pilot deltas and seed-win counts remain unverified and are omitted. No per-seed/per-month measurements were invented.

Rebuild from `/workspace/video-itba`:

```sh
python3 proposal/build_preview.py
```

Rerun source reconciliation and browser checks, and regenerate six SVG/PNG poses and the contact sheet:

```sh
python3 proposal/verify_proposal.py
```

Verification uses the environment's existing Python Playwright, Pillow, and `/usr/bin/chromium`, without network requests. Results go to `review/source_verification.json` and `review/verification.json`. Reconciliation of supplied exports is distinct from a live Kaggle query or model rerun.

Manim Community remains the intended final production engine. The browser draft is a fast visual/timing review artifact; no Manim build or final MP4 render is claimed.

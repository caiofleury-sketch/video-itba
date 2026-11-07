# Piano tranquilo para el corte con voz

Se conserva la melodía de la partitura original y se interpreta con piano acústico muestreado. El piano eléctrico y el bajo quedan como acompañamiento muy tenue. Se silencian percusión, arpegios de guitarra, vibráfono, pulso duplicado, colchón sintético y efectos de acento. Un filtro a 2,9 kHz y una reverberación corta suavizan el timbre.

El acompañamiento se normaliza a −33 LUFS antes de la atenuación automática según la voz; la locución se normaliza a −16 LUFS. Durante el habla la música baja más. La copia definitiva está integrada en los videos de `../final_cut/`.

Para reconstruir: `python proposal/audio_v4/render_audio.py`, seguido de `python proposal/final_cut/build_final.py /ruta/grabacion.mp4`. Requiere Chromium, Playwright, NumPy, SciPy, Pillow y FFmpeg con libass. La síntesis usa Tone.js 15.1.22 y ventanas con preroll y fundidos, conservando la melodía. Los WAV intermedios se excluyen de Git.

Las muestras FluidR3_GM están disponibles bajo CC BY 3.0. Véanse [los créditos completos](assets/CREDITS.md), el manifiesto de muestras y la investigación de instrumentos en `../audio_v3/`. Tone.js usa la licencia MIT incluida en `../audio_v1/vendor/`.

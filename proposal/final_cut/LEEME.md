# Corte final con presentador

- `video_final.mp4`: voz e imagen del presentador, música suave, sin subtítulos impresos.
- `video_final_subtitulos.mp4`: el mismo montaje con subtítulos en español.
- `subtitulos_es.srt`: subtítulos editables, ajustados a los grupos de frases de la grabación.
- `montaje.json`: parámetros de montaje y sincronización.
- `verificacion.json`: comprobaciones técnicas de los archivos exportados.

Se recorta la grabación entre 0,49 y 119,93 segundos. Duración resultante aproximada: 1:59. La imagen permanece en una ventana pequeña con esquinas redondeadas, arriba a la derecha; se conserva el filtro de personaje del archivo recibido. La luz se ajusta con gamma 1,035 y brillo +0,008. Las entradas de las escenas y las familias de variables se adaptan a las pausas de la locución, sin alterar la velocidad ni la sincronización de labios de la cámara.

La voz recibe filtrado conservador, reducción leve de ruido y normalización a −16 LUFS. La música de piano se sitúa a −33 LUFS antes de una atenuación adicional activada por el habla. Se eliminan percusión, arpegios y efectos de acento. Los finales de imagen y música se funden suavemente.

Los subtítulos conservan el guion aprobado; sus entradas se ajustan a los grupos de actividad vocal, con divisiones manuales dentro de algunas frases. No se generan mediante reconocimiento automático de palabras.

Se mantienen los resultados públicos aportados y la recomendación de conservar las cuatro variables del control de fondos relativos de tres meses. Los puntajes comparan recetas completas.

Reconstrucción: `python proposal/audio_v4/render_audio.py` y luego `python proposal/final_cut/build_final.py /ruta/grabacion.mp4`. Los originales y los audios de trabajo permanecen fuera del repositorio, en `/workspace/presenter_private/`. Solo se publica el montaje editado solicitado, además de las fuentes de reconstrucción. El video usa H.264 Baseline, YUV420p, AAC y `faststart`.

Las muestras de piano y acompañamiento son FluidR3_GM, CC BY 3.0: [créditos](../audio_v4/assets/CREDITS.md). Tone.js 15.1.22: MIT.

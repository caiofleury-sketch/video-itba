# Música y película final · versión 02

La película dura **dos minutos**. Los archivos principales son `video_final.mp4`, sin subtítulos incorporados, y `video_final_subtitulos.mp4`, con el guion en español sobre la imagen. `video_final_subtitulos.webm` es una alternativa de reproducción a 720p. Todos contienen la nueva música y los acentos. La voz del presentador todavía no está incorporada.

## Nueva composición

La pieza anterior se reemplazó por una composición original de exploración a 120 pulsos por minuto. Tiene una melodía de ocho compases, una sección de respuesta, armonías con inversiones, acompañamiento sincopado de piano FM, bajo, arpegios, percusión ligera y una cadencia escrita para el final. Conserva una estética de videojuegos de 16 bits sin transcribir un tema comercial. La investigación de ejemplos reales de Tone.js está en [`research/REFERENCIAS.md`](research/REFERENCIAS.md).

La música mantiene continuidad en las animaciones, pierde densidad y nivel en la explicación financiera y vuelve al tema en la recomendación. Los acentos independientes se redujeron a 17 acciones principales.

- `musica_escucha.m4a`: música sola a nivel de escucha, para evaluar la composición.
- `musica.wav` y `acentos.wav`: pistas separadas, de 120 segundos, a 48 kHz y 24 bits, con el mismo origen temporal.
- `banda_sonora.wav` y `banda_sonora.m4a`: mezcla usada en el video, con margen para la voz.
- `escucha_interactiva.html`: descargar y abrir para ajustar o silenciar las dos capas por separado; incorpora video y audio.
- `subtitulos_es.srt` y `subtitulos_es.ass`: texto y estilo editables.

La versión de escucha de la música sola tiene un nivel mayor que la mezcla para el video. La relación definitiva con tu voz se ajustará con la grabación real.

## Resultados incorporados

| Receta | Variables | Envío | Puntaje público, M ARS |
| --- | ---: | --- | ---: |
| Snapshot | 152 | 58080299 | 343,498 |
| Fondos relativos de 3 meses | 156 | 57852532 | 401,915 |
| Fondos de 3 + 6 meses | 160 | 58080309 | 392,831 |

La receta de tres meses queda +58,417 M ARS sobre el snapshot; extenderla a seis meses queda −9,084 M frente al control. La recomendación conserva las cuatro variables del control de tres meses. La evidencia proviene de los resultados informados por el usuario; no se realizó una consulta independiente al leaderboard. Las diferencias comparan recetas completas y no identifican efectos públicos individuales para las nueve familias.

La locución redondea los valores a una cifra decimal; el gráfico conserva la precisión informada. Los 33 subtítulos incluyen las 220 palabras del guion, contando las partes de las cifras con el mismo criterio del generador. Los tiempos son provisionales hasta recibir la locución grabada.

## Reconstrucción

Desde esta carpeta, con Chromium, FFmpeg con libass, Python, NumPy, SciPy y Playwright disponibles:

```sh
node build_score.cjs
python3 render_audio.py
python3 build_subtitles.py
python3 assemble.py
python3 build_listening_preview.py
```

`score.js` contiene la composición y `synth.js` los instrumentos. La versión fijada de Tone.js 15.1.22 y su licencia se reutilizan de `../audio_v1/vendor/`. El render se realiza en ventanas con tres segundos de preparación y cruces de 200 ms para limitar la vida de los nodos de síntesis sin alterar los tiempos de las notas.

La película visual se construye desde `../v9_es/`. `python3 serve_preview.py` sirve el reproductor de desarrollo en `http://127.0.0.1:8768/audio_v2/` con soporte de rangos de bytes para los saltos.

Las comprobaciones incluyen importes y diferencias, superposiciones visuales, continuidad de audio, sonoridad, decodificación completa, píxeles del video exportado y reproducción directa con imagen y audio. No reemplazan una evaluación de gusto musical ni la revisión de la mezcla con la voz real.

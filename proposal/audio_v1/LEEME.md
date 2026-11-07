# Banda sonora programada · versión 01

**Archivo principal recomendado:** `video_con_sonido_compatible.mp4`, película completa de 1:48 con música y acentos. No contiene locución. Conserva las escenas de la versión 8, incluida la apertura 3D, con una recodificación para mayor compatibilidad. `video_con_sonido_alternativa.webm` ofrece otra opción cuando el reproductor no admite el MP4. El archivo `video_con_sonido.mp4` anterior se conserva para comparación.

La partitura recurre a un motivo de tres notas —re, mi, la— que se transforma con las operaciones y se completa con un re superior en el cierre. `mapa_musical.md` relaciona cada transformación con su función narrativa.

La música es una composición original programada en JavaScript con **Tone.js 15.1.22**. Usa una estética retro suave: pulsos filtrados, bajo triangular y notas de síntesis FM. La referencia aportada se utilizó para estudiar la relación entre repetición, movimiento y pulsos; no se incorporó su audio.

## Escuchar y ajustar

- `escucha_interactiva.html`: reproductor autónomo, con imagen y audio incorporados; se puede descargar y abrir sin servidor.
- `index.html`: reproductor de desarrollo con niveles independientes de música y acentos, botones para silenciar cada capa y marcas de acciones visuales.
- `banda_sonora.m4a`: mezcla de audio completa para escuchar rápidamente.
- `banda_sonora.wav`: mezcla estéreo a 48 kHz y 24 bits.
- `musica.wav` y `acentos.wav`: pistas separadas, también a 48 kHz/24 bits, de 108 segundos y con el mismo origen temporal. Se pueden colocar directamente en el instante 0 de un editor.
- `propuesta_sonora.md`: dirección musical, investigación de herramientas y tratamiento por escena.
- `cues.csv`: las 37 marcas principales de sincronización.

El reproductor usa los niveles conservadores ya incorporados en las pistas. Música y acentos al 100% corresponden a la mezcla de referencia. La película conserva el gráfico de ganancia pendiente de datos verificados.

La relación definitiva con tu voz se ajustará con la grabación real. Los controles permiten bajar o silenciar las capas durante la revisión. Todavía no se ha comprobado el enmascaramiento con tu voz ni se ha aplicado reducción automática dependiente de ella.

## Archivos editables

`score.js` genera notas y acentos usando los inicios de las familias en `../v8_es/data.json`. Los desplazamientos de cada acción corresponden a los movimientos de `../v8_es/scenes.js`; si cambia la duración o la coreografía, habrá que actualizar esos desplazamientos. `score.json` conserva los hashes de las fuentes visuales usadas para esta revisión.

`synth.js` define los instrumentos, las envolventes y el procesamiento. `render_audio.py` ejecuta Tone.js mediante el motor de audio sin conexión de Chromium y exporta las dos pistas. `mix_audio.py` mide la sonoridad, ajusta niveles, suma las capas y añade el audio al video sin recodificar la imagen. `vendor/` incluye la distribución fijada de Tone.js y sus licencias.

Desde esta carpeta:

```sh
node build_score.cjs
python3 render_audio.py
python3 mix_audio.py
python3 export_compatible.py
python3 build_listening_preview.py
```

Para revisar el reproductor de desarrollo, desde esta carpeta:

```sh
python3 serve_preview.py
```

Abrir `http://127.0.0.1:8767/audio_v1/`. Con ese servidor en ejecución, `python3 verify_player.py` desde esta carpeta comprueba reproducción, pausa, sincronización, saltos, niveles, silencios, reinicio y vista móvil.

`verificacion_audio.json` contiene las mediciones de sonoridad, formato, duración y margen de pico. También comprueba la suma de pistas, el desvanecimiento final y que el flujo de video coincide con el original. `verificacion_reproductor.json` registra la revisión del reproductor de desarrollo y `verificacion_reproductor_autonomo.json` la del HTML autónomo. Ambos se probaron en Chromium; la comprobación verifica funcionamiento y sincronización, sin sustituir la escucha con la voz real.

## Revisión de compatibilidad

La exportación MP4 compatible utiliza H.264 Constrained Baseline, imagen SDR BT.709 en rango limitado, píxeles YUV 4:2:0 de 8 bits, audio AAC-LC y cabecera de reproducción al inicio del archivo. La alternativa WebM utiliza VP9/Opus a 720p. No se modificó la composición musical.

`verificacion_compatibilidad_archivos.json` comprueba la decodificación completa de los archivos. `verificacion_reproduccion_directa.json` comprueba reproducción real en Chromium, contenido visible, energía de audio, saltos a tres escenas y llegada al final. Estas pruebas locales no identifican por sí solas la causa de un fallo en otro navegador o en la plataforma de entrega.

## Versión con el guion como subtítulos

- `video_con_subtitulos.mp4`: película completa, con música y los subtítulos en español incorporados permanentemente a la imagen.
- `video_con_subtitulos.webm`: alternativa con los mismos subtítulos para reproductores que no admitan el MP4.
- `subtitulos_es.srt`: subtítulos editables para importar sobre la versión sin texto.
- `subtitulos_es.ass`: estilo y tiempos usados en el render.

Se conservan las 204 palabras del guion en 31 subtítulos. Las frases de cada familia respetan sus tiempos de entrada; el mapa de variables dispone de cinco segundos sin locución ni subtítulos antes de la comparación. La tipografía se ubica en la franja inferior reservada, por debajo de las leyendas de las escenas.

Los tiempos son provisionales y se basan en el guion y la animación: todavía no hay grabación de la voz del presentador. Habrá que ajustarlos a esa grabación. La música y los acentos continúan presentes, sin voz sintetizada.

Para reconstruir: `python3 build_subtitles.py`. `review_subtitles.py` verifica las posiciones de texto; `verify_subtitle_exports.py` contrasta el texto visible en los videos exportados con los fotogramas de revisión. `revision_subtitulos/revision.jpg` permite revisar ejemplos de todas las escenas.

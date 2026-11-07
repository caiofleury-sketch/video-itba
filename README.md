# El contexto detrás del número

Película de **dos minutos**, en español, sobre las variables añadidas a un modelo de ciencia de datos. La última revisión incorpora los tres puntajes públicos de Kaggle, una recomendación final y una composición musical nueva con estética de exploración de videojuegos de 16 bits.

## Prueba nueva de instrumentos · melodía conservada

Se preparó una nueva interpretación con piano acústico, piano eléctrico, bajo de dedos, guitarra de nylon y vibráfono mediante Tone.Sampler. La partitura y sus tiempos se conservan; se retiran el doble de pulso y el colchón sintético. Se comparan los mismos 32 segundos con volumen medido equivalente.

- **[Descargar la prueba de instrumentos](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/prueba_instrumentos_v3.zip)**.
- [Música completa con instrumentos nuevos](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/audio_v3/musica_instrumentos_nuevos.mp3).
- [Comparación interactiva A/B, para descargar y abrir](proposal/audio_v3/comparar_instrumentos.html).
- [Investigación, instrumentos, reconstrucción y créditos](proposal/audio_v3/LEEME.md).

El montaje con la imagen y la voz del presentador está pendiente de recibir su grabación. Los videos enlazados a continuación conservan la instrumentación 02; esta prueba prepara la instrumentación 03 para esa edición final. Las muestras de instrumentos son FluidR3_GM, CC BY 3.0; los créditos se incluyen en la carpeta y en el paquete de escucha.

## Descargar la versión actualizada

**[Descargar ZIP final — 33 MB](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/video_final_2min.zip)**

Extraé el ZIP y abrí `video_con_subtitulos.mp4` en tu reproductor local. Si el MP4 no funciona, probá `alternativa_con_subtitulos.webm`, por ejemplo con VLC.

El paquete contiene la película con subtítulos y sin ellos, la alternativa WebM, la música sola, el guion actualizado, el SRT editable y el registro de los resultados públicos.

- [Música nueva para escuchar sola](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/audio_v2/musica_escucha.m4a).
- [MP4 con subtítulos · 1080p](proposal/audio_v2/video_final_subtitulos.mp4).
- [MP4 sin subtítulos · 1080p](proposal/audio_v2/video_final.mp4).
- [Alternativa WebM · 720p](proposal/audio_v2/video_final_subtitulos.webm).
- [Guion en español](proposal/v9_es/guion.txt) y [subtítulos SRT](proposal/audio_v2/subtitulos_es.srt).

En la página de un archivo binario, usá **Download raw** si GitHub no muestra una vista previa. El audio incluye música y acentos; todavía no contiene la voz del presentador. Los tiempos de los subtítulos son provisionales hasta incorporar esa grabación.

## Resultados y recomendación

| Receta | Variables | Submission | Puntaje público · M ARS |
| --- | ---: | --- | ---: |
| Snapshot | 152 | 58080299 | 343,498 |
| Fondos relativos de 3 meses | 156 | 57852532 | **401,915** |
| Fondos de 3 + 6 meses | 160 | 58080309 | 392,831 |

La receta de tres meses supera al snapshot en **58,417 M ARS**. Añadir la extensión de seis meses queda **9,084 M por debajo del control de tres meses**, aunque sigue por encima del snapshot.

La recomendación conserva las cuatro variables de fondos relativos de tres meses: dos cambios relativos de saldo y haberes y dos indicadores de escala casi nula. Las diferencias comparan recetas completas y no demuestran efectos públicos individuales para las nueve familias de variables. La fuente es la tabla de submissions proporcionada por el usuario; no se efectuó una consulta independiente al leaderboard. No se convierte AUC a pesos. La locución redondea las cifras para facilitar la lectura; el gráfico conserva la precisión informada.

## Música recompuesta

La versión 02 reemplaza la primera propuesta por una pieza original con una melodía de ocho compases, una respuesta distinta, piano FM, inversiones de acordes, bajo, arpegios, percusión ligera y un cierre escrito. La mezcla se aligera durante la explicación financiera y deja margen para la futura voz.

Se estudiaron ejemplos de juegos y secuenciadores hechos con Tone.js y la organización de un tracker. Las referencias y lo aplicado están documentados en [la investigación musical](proposal/audio_v2/research/REFERENCIAS.md). No se reutilizó una melodía comercial.

La [vista de escucha autónoma](proposal/audio_v2/escucha_interactiva.html) se puede descargar y abrir localmente para silenciar o ajustar música y acentos por separado. La copia `musica_escucha.m4a` tiene un nivel mayor que el acompañamiento del video para facilitar la evaluación de la composición.

## Fuentes y reconstrucción

| Carpeta | Contenido |
| --- | --- |
| [`proposal/v9_es/`](proposal/v9_es/) | Última película visual, resultados públicos, escenas SVG/JavaScript, guion, render y verificaciones. |
| [`proposal/audio_v2/`](proposal/audio_v2/) | Nueva partitura Tone.js, instrumentos, mezcla, exportaciones, subtítulos y verificaciones. |
| [`proposal/source/`](proposal/source/) | Archivos de experimento y propuestas aportados, conservados para trazabilidad. |
| [`proposal/v8_es/`](proposal/v8_es/), [`proposal/audio_v1/`](proposal/audio_v1/) y revisiones anteriores | Historial de trabajo y entregables previos. |

Las instrucciones están en [la guía visual](proposal/v9_es/LEEME.md) y [la guía de audio](proposal/audio_v2/LEEME.md). Se usa Python con Pillow, NumPy, SciPy y Playwright, Chromium, FFmpeg con libass y Tone.js 15.1.22. La distribución fijada de Tone.js y su licencia MIT están en `proposal/audio_v1/vendor/`.

Los archivos finales se comprobaron por decodificación completa, reproducción directa con imagen y audio, saltos de escena, comparación de fotogramas, continuidad de audio y niveles. La geometría de los textos se revisó en 960 instantes. Estas pruebas técnicas no reemplazan la evaluación musical del oyente ni el ajuste final con la voz real.

Se conservan las fuentes, las revisiones y los entregables. Las dependencias instaladas, las cachés y los audios temporales se excluyen del control de versiones y se regeneran con los scripts. El análisis de inflación y el inventario de variables preexistentes permanecen fuera de la presentación.

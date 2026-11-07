# El contexto detrás del número

Video de ingeniería de variables para una presentación de ciencia de datos. Incluye gráficos y animaciones programadas, guion en español, música original generada con Tone.js y una versión con subtítulos.

**Duración: 1:48.** El audio contiene música y acentos; la voz del presentador todavía no está incorporada.

## Descargar para reproducir localmente

**[Descargar el ZIP con los videos](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/video_para_descargar.zip)** — aproximadamente 28 MB.

Extraé el ZIP y abrí `video_con_subtitulos.mp4` con un reproductor local. Si tu reproductor no admite el MP4, probá `video_con_subtitulos.webm`, por ejemplo con VLC.

El paquete incluye:

| Archivo | Contenido |
| --- | --- |
| `video_con_subtitulos.mp4` | Película completa en 1080p, con música y subtítulos en español incorporados a la imagen. |
| `video_con_subtitulos.webm` | Alternativa en 720p con los mismos subtítulos y música. |
| `video_sin_subtitulos.mp4` | Película en 1080p con música y sin subtítulos incorporados. |
| `subtitulos_es.srt` | Subtítulos editables para usar sobre la versión sin texto. |
| `LEEME.txt` | Instrucciones de reproducción. |

También se pueden descargar individualmente desde [la carpeta de audio y entregables](proposal/audio_v1/). En la página de un archivo binario, usá **Download raw** si GitHub no muestra una vista previa. Las exportaciones MP4 recomendadas usan H.264 Constrained Baseline y AAC-LC; las alternativas WebM usan VP9 y Opus. Se comprobaron la decodificación completa y la reproducción directa con imagen, audio, saltos de tiempo y llegada al final en Chromium. Esto no garantiza la compatibilidad de todos los reproductores.

## Revisar el video y su composición musical

- [Vista de escucha autónoma](proposal/audio_v1/escucha_interactiva.html): descargar el HTML y abrirlo localmente. Incluye el video y las pistas, y permite ajustar o silenciar música y acentos por separado.
- [Guion en español](proposal/v8_es/guion.txt) y [guion con tiempos](proposal/v8_es/guion_con_tiempos.md).
- [Dirección musical y herramientas investigadas](proposal/audio_v1/propuesta_sonora.md).
- [Mapa de motivos musicales y acciones visuales](proposal/audio_v1/mapa_musical.md).
- [Revisión incremental de gráficos y animaciones](proposal/v8_es/REVISION_VISUAL.md).
- [Antes y después](proposal/v8_es/revision/antes_despues.jpg).

Los subtítulos cubren las 204 palabras del guion en 31 frases. Sus tiempos son provisionales: se ajustarán cuando esté disponible la grabación real de la voz.

## Fuentes y reconstrucción

| Carpeta | Contenido |
| --- | --- |
| [`proposal/v8_es/`](proposal/v8_es/) | Última revisión visual en español, escenas SVG/JavaScript, render y comprobaciones. |
| [`proposal/audio_v1/`](proposal/audio_v1/) | Partitura JavaScript, síntesis Tone.js, mezcla, exportaciones compatibles, subtítulos y verificaciones. |
| [`proposal/source/`](proposal/source/) | Archivos de experimento y propuestas aportados, conservados para trazabilidad. |
| [`proposal/v3/`](proposal/v3/), …, [`proposal/v7_es/`](proposal/v7_es/) | Revisiones anteriores de la propuesta y sus verificaciones. |

Las instrucciones de reconstrucción están en [la guía visual](proposal/v8_es/LEEME.md) y [la guía de audio y subtítulos](proposal/audio_v1/LEEME.md). Se utiliza Python con Pillow, NumPy, SciPy y Playwright, Chromium, FFmpeg con libass, y Tone.js 15.1.22. La distribución fijada de Tone.js y su licencia MIT están incluidas en `proposal/audio_v1/vendor/`; no hace falta descargarla para escuchar las exportaciones.

Se conservan las fuentes, las revisiones y los entregables. Las dependencias instaladas, las cachés y los audios temporales de síntesis se excluyen del control de versiones y pueden regenerarse con los scripts.

## Alcance de los resultados

La presentación se concentra en las variables añadidas y su motivación. El ajuste por inflación y el inventario de variables preexistentes quedan fuera del video. Los ejemplos gráficos son ilustrativos.

Los resultados monetarios comparables por familia de variables siguen pendientes de verificación. La recomendación de priorizar saldo y haberes relativos se basa en la evaluación controlada de ordenamiento; la mejora pública de ganancia incremental todavía no se ha confirmado. No se convierten cambios de AUC en pesos.

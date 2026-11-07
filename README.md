# El contexto detrás del número

**Corte final con la voz y la imagen del presentador**, en español, con gráficos animados, resultados públicos y recomendación final. Duración: **1:59**, resolución 1080p.

## Descargar el corte final

**[Descargar ZIP con ambas versiones](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/corte_final_con_presentador.zip)**

- [MP4 con subtítulos en español](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/final_cut/video_final_subtitulos.mp4).
- [MP4 sin subtítulos impresos](https://github.com/caiofleury-sketch/video-itba/raw/refs/heads/main/proposal/final_cut/video_final.mp4).
- [Subtítulos SRT editables](proposal/final_cut/subtitulos_es.srt) y [guion](proposal/v9_es/guion.txt).
- [Parámetros y reconstrucción del montaje](proposal/final_cut/LEEME.md), [mezcla de piano](proposal/audio_v4/LEEME.md) y [verificación de reproducción](proposal/final_cut/verificacion.json).

Descargá el ZIP, extraelo y abrí el MP4 en tu reproductor local. En la página de un binario de GitHub, también podés usar **Download raw**.

Se recortan los silencios inicial y final, se ajusta levemente la luz y se normaliza la voz. La cámara permanece arriba a la derecha, fuera de los gráficos. Las escenas se ajustan a los tiempos de la grabación. La música usa piano acústico suave, con acompañamiento mínimo, sin percusión ni arpegios; baja automáticamente durante el habla. La mezcla final mide aproximadamente −16 LUFS.

El ZIP incluye los dos MP4, el guion, los subtítulos, los resultados públicos y los créditos musicales. El original de cámara y los audios de trabajo quedan fuera del repositorio; los videos publicados contienen el montaje editado solicitado.

## Resultados y recomendación


| Receta | Variables | Submission | Puntaje público · M ARS |
| --- | ---: | --- | ---: |
| Snapshot | 152 | 58080299 | 343,498 |
| Fondos relativos de 3 meses | 156 | 57852532 | **401,915** |
| Fondos de 3 + 6 meses | 160 | 58080309 | 392,831 |

La receta de tres meses supera al snapshot en **58,417 M ARS**. Añadir la extensión de seis meses queda **9,084 M por debajo del control de tres meses**, aunque sigue por encima del snapshot.

La recomendación conserva las cuatro variables de fondos relativos de tres meses: dos cambios relativos de saldo y haberes y dos indicadores de escala casi nula. Las diferencias comparan recetas completas y no demuestran efectos públicos individuales para las nueve familias de variables. La fuente es la tabla de submissions proporcionada por el usuario; no se efectuó una consulta independiente al leaderboard. No se convierte AUC a pesos. La locución redondea las cifras para facilitar la lectura; el gráfico conserva la precisión informada.

## Fuentes y créditos

Las escenas y sus componentes están en [`proposal/v9_es/`](proposal/v9_es/); la síntesis musical, en [`proposal/audio_v4/`](proposal/audio_v4/); el montaje y las verificaciones, en [`proposal/final_cut/`](proposal/final_cut/).

Se usan Python, Pillow, NumPy, SciPy, Playwright, Chromium, FFmpeg con libass y Tone.js 15.1.22. Las muestras de instrumentos FluidR3_GM usan CC BY 3.0: [créditos](proposal/audio_v4/assets/CREDITS.md). Tone.js usa MIT, incluida en `proposal/audio_v1/vendor/`. Los archivos de origen de los experimentos permanecen en `proposal/source/` y las versiones anteriores se conservan para trazabilidad.

La exportación se comprueba por decodificación completa, reproducción y saltos de escena en Chromium, presencia real de subtítulos en los píxeles, formato H.264 Baseline/AAC y ubicación de metadatos `faststart`. Los tiempos de subtítulos siguen las frases grabadas; algunas divisiones dentro de frase son manuales. Los resultados completos están en el registro de verificación.

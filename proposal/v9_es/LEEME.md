# Video final · versión visual 9

La película dura dos minutos. Conserva la apertura 3D, la construcción de las nueve familias y la vista general; reemplaza la comparación pendiente por tres recetas con puntajes públicos informados por el usuario. La recomendación elige los fondos relativos de tres meses.

| Receta | Variables | Submission | Puntaje público (M ARS) |
| --- | ---: | --- | ---: |
| Snapshot | 152 | 58080299 | 343,498 |
| Fondos relativos de 3 meses | 156 | 57852532 | 401,915 |
| Fondos de 3 + 6 meses | 160 | 58080309 | 392,831 |

La diferencia del control frente al snapshot es +58,417 M ARS. La extensión queda +49,333 M sobre el snapshot y −9,084 M frente al control. Son diferencias de puntaje entre recetas completas. No constituyen una medición pública por cada una de las nueve familias, ni una prueba causal de efectos aislados. `public_results.json` conserva el origen de los datos: reporte del usuario, sin consulta independiente a Kaggle desde el entorno.

Las cifras de la locución se redondean a una cifra decimal para facilitar su lectura. El gráfico y la evidencia conservan las tres cifras decimales proporcionadas. No se convierte AUC a pesos.

`index.html` es la vista visual interactiva sin audio; `pelicula_completa_120s.mp4` es su render silencioso. Los videos con música y subtítulos están en `../audio_v2/`. Las versiones anteriores permanecen disponibles.

## Reconstrucción

Desde la raíz: `python3 proposal/v9_es/build.py`, `python3 proposal/v9_es/verify_timeline.py` y `python3 proposal/v9_es/render_video.py`. `review_final.py` genera los fotogramas de la comparación y el cierre. La exportación usa H.264 Constrained Baseline, SDR BT.709 y rango limitado para mejorar compatibilidad.

`verificacion_resultados.json` comprueba los importes, las diferencias y la receta ganadora. `verificacion_temporal.json` revisa 960 instantes, límites, superposiciones de texto y espacio del presentador. La locución real todavía no está incorporada.

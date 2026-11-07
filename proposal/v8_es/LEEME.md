# Película revisada en español · versión 8

La película completa dura **1:48**, incluye la apertura 3D y se entrega a **1920 × 1080, 24 fps, sin audio**, para incorporar la locución del presentador.

- `pelicula_completa_108s.mp4`: archivo principal, con las cuatro escenas completas.
- `index.html`: vista previa interactiva, en español y utilizable sin conexión.
- `guion.txt` y `guion_con_tiempos.md`: texto de grabación y tiempos por escena.
- `guia_de_locucion.md`: marcas orientativas para las nueve familias de variables.
- `revision/antes_despues.jpg`: comparación de componentes en los mismos instantes.
- `revision/final/`: 90 capturas de poses intermedias, agrupadas por componente y escena.
- `frames/comprobacion_del_video.jpg`: fotogramas decodificados del MP4 entregado.
- `REVISION_VISUAL.md`: hallazgos y correcciones de las sucesivas pasadas.

La apertura conserva el contraste entre dos clientes con saldo 80. La escena de variables construye cada operación sobre ejemplos ilustrativos y termina con el mapa de las nueve familias. La comparación usa una sola medida, ganancia adicional; sus valores siguen pendientes de resultados comparables verificados. El cierre recomienda primero saldo y haberes relativos, conforme a la evaluación controlada de ordenamiento, y mantiene pendiente la confirmación de ganancia incremental.

La nueva secuencia de escala personal retoma a los dos clientes: el mismo saldo 80 implica −20% frente a una media propia de 100 y 0% frente a una media de 80. Los cuatro componentes del cierre representan dos cambios relativos y dos indicadores de escala casi nula. Las alturas del modelo ilustrado representan piezas incorporadas, no resultados de rendimiento.

El guion conserva 204 palabras y cuatro escenas: apertura 0:00–0:16, variables 0:16–1:10, comparación 1:10–1:34 y recomendación 1:34–1:48. Los tiempos se ajustarán a la grabación real. Se mantiene libre la esquina superior derecha para el presentador.

## Verificación

Se capturaron 90 imágenes de revisión final y se analizaron 864 instantes a intervalos de 0,125 segundos. El barrido final no detectó superposiciones de texto visible, desbordes ni invasiones del espacio del presentador. La comprobación de geometría complementa la inspección visual: no sustituye una evaluación de percepción ni prueba que cada píxel esté libre de defectos.

Los ejemplos matemáticos, los controles de reproducción y las cuatro escenas se comprueban por separado. Después de exportar, se comparan 16 fotogramas del MP4 con su imagen esperada, incluyendo la apertura y el cierre. Los informes quedan junto a los archivos fuente.

## Reconstrucción

Desde la raíz del repositorio, con Python, Pillow, Playwright, Chromium y FFmpeg disponibles:

```sh
python3 proposal/v8_es/verify.py
python3 proposal/v8_es/verify_timeline.py
python3 proposal/v8_es/review_frames.py final --existing
python3 proposal/v8_es/render_video.py
python3 proposal/v8_es/verify_export.py
```

Es una maqueta animada de revisión, generada con Chromium/SVG y FFmpeg. La composición permanece parametrizada y conserva los archivos originales de las versiones anteriores.

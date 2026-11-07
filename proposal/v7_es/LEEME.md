# Película completa en español

La película completa conserva la apertura 3D y dura 1:48. El archivo principal es `pelicula_completa_108s.mp4`. Sigue sin audio, para incorporar la grabación del presentador.

- `index.html`: vista previa interactiva, completamente en español y utilizable sin conexión.
- `guion.txt`: guion limpio para la grabación.
- `guion_con_tiempos.md`: guion con los intervalos de cada escena.
- `guia_de_locucion.md`: referencias orientativas para las nueve construcciones de variables.
- `frames/contact_sheet.jpg`: vista general de los gráficos traducidos.
- `verificacion_idioma.json`: comprobaciones del idioma y del ritmo previsto.

Se tradujeron los títulos, rótulos, ecuaciones explicativas, hipótesis, recomendaciones, navegación, controles y notas de evidencia. Los ejemplos usan coma decimal y ordinales en español. Se mantuvieron los identificadores internos de los experimentos y las variables de código para conservar la trazabilidad.

El guion tiene 204 palabras. Los ritmos orientativos de las cuatro escenas son aproximadamente 124, 104, 125 y 116 palabras por minuto. Las nueve explicaciones tienen marcas orientativas ajustadas a su extensión en español; no son tiempos medidos sobre una grabación real. La vista general queda visible durante los últimos cinco segundos de la escena de variables.

Las cifras de los ejemplos y las operaciones matemáticas no cambiaron. La comparación continúa usando solo ganancia y sigue sin valores monetarios por variable hasta que lleguen resultados comparables verificados. La recomendación continúa basada en la evaluación controlada de ordenamiento; su ganancia pública incremental permanece pendiente de confirmación.

La verificación revisa 217 instantes de la animación, controles, textos explicativos, límites de los gráficos y ausencia de rótulos visibles en inglés. El video exportado se comprueba por duración, cantidad de fotogramas y correspondencia con imágenes de referencia.

Para reconstruir desde `/workspace/video-itba`:

```sh
python3 proposal/v7_es/verify.py
python3 proposal/v7_es/render_video.py
```

El archivo es una maqueta animada de revisión generada con Chromium/SVG y FFmpeg. No es una exportación final de Manim ni contiene locución sintetizada.

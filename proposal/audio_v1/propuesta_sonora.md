# El contexto detrás del número · paisaje sonoro 01

Propuesta original para la película de 1:48. El objetivo es que la música acompañe la explicación y que pequeños acentos hagan perceptibles las transformaciones de los gráficos. La voz del presentador será el elemento principal de la mezcla.

## Herramienta elegida

Se compararon los repositorios públicos el 7 de noviembre de 2026. Las estrellas son una fotografía de esa consulta, no una medida de calidad sonora.

| Proyecto | Estrellas observadas | Adecuación a este video |
| --- | ---: | --- |
| [Tone.js](https://github.com/Tonejs/Tone.js) | 14.891 | Elección principal: sintetizadores, efectos, programación temporal y render de audio sin reproducir en tiempo real. Podemos revisar y modificar cada nota mediante código. |
| [BeepBox](https://github.com/johnnesky/beepbox) | 1.218 | Buena alternativa para diseñar melodías retro con un editor; también ofrece biblioteca de síntesis. Para sincronizar acciones puntuales preferimos la programación directa de Tone.js. |
| [ZzFX](https://github.com/KilledByAPixel/ZzFX) | 810 | Excelente para efectos muy pequeños de videojuegos. La composición musical requeriría añadir su secuenciador ZzFXM u otra capa. |
| [Strudel, antiguo espejo GitHub](https://github.com/tidalcycles/strudel) | 3.041 | Atractivo para patrones musicales y programación en vivo. El repositorio consultado está archivado y anuncia su traslado a Codeberg; el archivo de GitHub no implica que el proyecto haya dejado de desarrollarse. |

Tone.js 15.1.22, licencia MIT, queda fijado en el proyecto y su distribución se conserva localmente. El código de composición, las notas, las duraciones y los acentos están separados de la síntesis. Esto permite trabajar con un agente de código sin depender de una sesión manual de una aplicación musical. No se verificó una integración oficial específica para agentes de IA.

## Qué tomamos de la referencia

Se analizaron el audio y fotogramas del archivo aportado. Su duración es 40,05 segundos. La detección de ataques encuentra intervalos recurrentes cercanos a 0,125 y 0,25 segundos; esto describe una regularidad de pulsos y no determina por sí solo un tempo musical único. El análisis EBU R128 mide aproximadamente −14,1 LUFS integrados y −1,6 dBTP en ese archivo.

La referencia vincula figuras repetitivas, movimiento circular y pulsos musicales. Tomamos esa relación entre repetición y transformación como dirección de diseño. La nueva partitura y sus timbres se generan desde cero: no se reutilizan muestras, melodías ni fragmentos del audio de referencia.

## Un motivo que cambia con la historia

La identidad de la pieza es una pregunta de tres notas: **re–mi–la**. Al final se completa con un re superior. Esta vuelta al motivo inicial aporta continuidad y cierre al relato, sin presentar la recomendación como una victoria de ganancia ya demostrada.

La apertura asigna el mismo re a los dos saldos iguales. El rezago conserva esa nota y la devuelve como un eco; el cambio mensual desciende; el promedio reúne tres notas en una referencia común. En la comparación personal, el mismo re reaparece sobre apoyos armónicos distintos, primero fa–la y después sol–si: el contexto cambia lo que percibimos sin cambiar la nota principal.

La densidad también cuenta la historia. Comenzamos con pocos elementos, incorporamos pequeñas figuras mientras se construyen las variables y retiramos la melodía durante los resultados, para dar protagonismo a la explicación. En el cierre, las cuatro entradas y las cuatro capas recuperan **re–mi–la–re**. Es una aplicación de motivos recurrentes, variación y composición por capas, habituales en la música de videojuegos.

## Dirección musical

- **Carácter:** curiosidad, claridad y una llegada serena a la recomendación.
- **Color:** inspiración en videojuegos de la era de 16 bits, con pulsos filtrados, bajos triangulares y pequeñas notas de síntesis FM. «16 bits» describe aquí una estética, no el formato del archivo ni una emulación exacta de una consola.
- **Pulso:** 96 pulsos por minuto. Los acentos visuales conservan sus tiempos exactos y no se desplazan para ajustarse a la cuadrícula musical.
- **Armonía:** material original en re dórico y acordes abiertos; melodía espaciada y sin batería dominante.
- **Espacio para la voz:** ataques redondeados, agudos filtrados, reducción suave en torno a 2,4 kHz, pocas notas simultáneas y una bajada adicional del fondo durante la comparación de resultados.

## Relato por escenas

| Tiempo | Imagen | Tratamiento sonoro |
| --- | --- | --- |
| 0:00–0:16 | Dos clientes y despliegue de historia en 3D | El fondo entra gradualmente. Tres notas acompañan la separación de los planos y dos notas laterales distinguen las referencias personales. |
| 0:16–1:05 | Construcción de las nueve familias | Motivos cortos: caída descendente, tres notas para la media, seis para ampliar la historia, pulsos que se apagan en uso relativo, orden ascendente y ponderaciones crecientes en el promedio exponencial. |
| 1:05–1:10 | Mapa completo | Un pequeño acorde arpegiado reúne las construcciones. |
| 1:10–1:34 | Comparación de ganancia | Baja la densidad y el nivel del acompañamiento. No se asigna sonido a valores ausentes ni se presenta una fanfarria de victoria. |
| 1:34–1:48 | Cuatro variables recomendadas llegan al modelo | Cada componente recibe una nota al aparecer y otra al incorporarse como capa. La música se desvanece antes del final. |

Los movimientos descendentes o crecientes son ejemplos visuales y no resultados experimentales. Los acentos no convierten AUC en ganancia ni sugieren que los valores pendientes ya estén confirmados.

## Mezcla y revisión

Se entregan tres pistas de igual duración y origen temporal: música, acentos y mezcla conjunta. La música parte de un objetivo aproximado de −30 LUFS integrados y los acentos de −33 LUFS, sujetos al margen de pico. Los valores medidos de los archivos definitivos quedan en `verificacion_audio.json`.

Son niveles iniciales conservadores para acompañar una narración. La relación definitiva con tu voz se ajustará al recibir la grabación real. No se ha evaluado todavía el enmascaramiento sobre esa grabación, ni se ha aplicado una reducción automática vinculada a una voz inexistente.

La página de revisión permite silenciar cada capa, ajustar sus niveles y recorrer escenas. El video exportado contiene la mezcla de música y acentos, sin locución. La imagen conserva la versión 8 íntegra.

## Medición de la entrega

- Música: -30.02 LUFS integrados; pico verdadero -16.00 dBTP.
- Acentos: -39.91 LUFS integrados; pico verdadero -20.00 dBTP.
- Mezcla conjunta: -29.97 LUFS integrados; pico verdadero -16.00 dBTP.

Los acentos son breves y espaciados; su nivel integrado no equivale al volumen percibido de cada nota. La ganancia se limitó por pico, por lo que no se forzó su objetivo integrado de −33 LUFS. La mezcla mantiene un margen amplio para incorporar la locución.

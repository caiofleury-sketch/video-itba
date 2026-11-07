# Investigación y nueva dirección musical

La versión 1 se descartó como dirección musical: sus tonos aislados, largos espacios estáticos y escasa articulación no producían una pieza convincente para el relato.

## Código estudiado

- [Space Vaders](https://github.com/jjlljj/space-invaders/blob/master/scripts/game.js): partitura expresada como notas con nombre, duración, tiempo y velocidad; `Tone.Part`, mezcla y reverberación. Se estudió la organización de una pieza anotada para un juego. No se reutilizaron sus notas.
- [Cyberblob of the Rings](https://github.com/tomjhinton/cyberbloboftherings/blob/master/src/app.js): separación de registros, voces AM/DuoSynth y patrones en un juego con Tone.js. Sus patrones aleatorios no son el enfoque elegido para esta película: se escribió una melodía fija con desarrollo y cierre.
- [Das Model](https://github.com/jenissimo/das-model/blob/main/src/engine/Sequencer.js): secuenciación de 16 pasos, canales de melodía y batería, encadenamiento y cambios de patrón al final del compás. Su instrumento de pulso/triángulo sirvió como referencia conceptual para la paleta retro.
- [SoundBox](https://github.com/mbitsnbites/soundbox): organización de un tracker por canales, patrones y arreglos; demos de composiciones completas. No se incorporaron su código GPL, sus melodías ni sus archivos de canción al proyecto.

Los commits consultados están registrados en `code_sources.json`. Son ejemplos de implementación; la popularidad de Tone.js corresponde al framework, no a estos pequeños proyectos.

## Qué cambia realmente en la pieza

La nueva composición usa 120 pulsos por minuto, cuatro tiempos y 60 compases en dos minutos. Una melodía original de ocho compases tiene una sección de respuesta distinta; se alternan secciones A y B, una transición breve, una versión reducida para explicar resultados y una cadencia escrita para el final.

La armonía en mi bemol mayor emplea acordes con séptimas y novenas, inversiones y notas comunes. El piano eléctrico FM marca un acompañamiento sincopado; el bajo enlaza las raíces y quintas; un arpegio ligero aporta movimiento. Una melodía de triángulo con una capa de pulso tenue mantiene el color de videojuego sin depender de pitidos agudos. La percusión utiliza un bombo discreto, un golpe corto y ruido filtrado de baja intensidad.

El objetivo es una pequeña pieza de exploración con el carácter cálido de un juego de la era de 16 bits. Se aplican recursos de esas bandas sonoras —frases periódicas, llamadas y respuestas, conducción de voces, patrones de acompañamiento y contraste entre secciones— sin transcribir un tema comercial.

Los acentos aislados se redujeron a 17 acciones principales. La continuidad está a cargo de la música. En la explicación financiera se reduce el nivel y parte de la melodía; la recapitulación acompaña la recomendación de tres meses. La última nota y el acorde final tienen una duración prevista y un desvanecimiento, en lugar de cortar un bucle.

La versión para el video se mezcla con margen para la voz. Se entrega además una copia de escucha de la música sola a un nivel mayor para evaluar su composición. Todavía no hay grabación real de locución; la mezcla definitiva se ajustará con ella.

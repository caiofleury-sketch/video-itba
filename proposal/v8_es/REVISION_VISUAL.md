# Revisión incremental de gráficos y animaciones

Se trabajó sobre una copia de la versión 7; los archivos anteriores permanecen disponibles. No se modificaron los resultados experimentales ni el texto de locución.

## Primera pasada: observar el movimiento

Las 30 capturas iniciales cubrieron la apertura, la construcción del promedio, el ordenamiento, los cambios de escena y el cierre. Se detectaron problemas que no aparecían en las poses finales:

- **4,20–4,90 s, apertura:** las etiquetas de los meses se superponían mientras los planos históricos todavía coincidían. Ahora cada etiqueta histórica aparece cuando hay separación suficiente; «Actual» conserva la referencia inicial.
- **22,88–24,78 s, promedio:** las barras se deformaban hacia 100 mientras seguían rotuladas 110 y 90. Ahora las mediciones conservan su altura y una superficie independiente asciende hasta la media; segmentos verticales muestran la diferencia entre cada dato y esa referencia.
- **53,81–54,16 s, rangos:** las columnas se atravesaban y ocultaban valores al intercambiar posiciones. Ahora siguen carriles separados en profundidad, se dibujan de atrás hacia adelante y los rótulos se dibujan sobre la geometría. El valor 80 conserva su color durante el recorrido.
- **64,80 s, promedio exponencial:** las etiquetas temporales invadían la explicación inferior. Se elevó el conjunto gráfico y se detuvo la deriva de cámara al terminar el movimiento de entrada.
- **70,20–71,00 s, comparación:** los iconos recorrían las etiquetas de otras filas. Ahora cada fila aparece en su posición, con una entrada breve y escalonada.
- **94,00–98,50 s, recomendación:** cuatro prismas genéricos no explicaban el aporte. Se sustituyeron por cuatro componentes identificados, conectados a un modelo al que llegan partículas y se agregan cuatro capas.

## Segunda pasada: corregir los efectos de los ajustes

Los mismos instantes se volvieron a renderizar. El nuevo recorrido de la columna 200 invadía la ecuación; se ajustaron la escala vertical y la posición de cámara. La elevación del gráfico exponencial acercaba la primera ponderación al valor 120; se separaron los rótulos.

La cobertura se amplió a las nueve construcciones. Un barrido de 864 instantes localizó tres cruces adicionales durante la aparición de texto: «caída = 10» con el saldo 80, «−20%» con ese mismo saldo y las etiquetas de las dos filas de actividad. Se reubicaron las llamadas de atención y la cámara de actividad comienza con suficiente inclinación para separar ambas filas desde el primer instante.

Los registros de estas pasadas están en `revision/antes/`, `revision/despues_1/` y `revision/despues_2/`.

## Tercera pasada: reforzar la historia

Entre aproximadamente 0:31 y 0:35, la demostración de fondos relativos retoma a los clientes de la apertura. La caída de una barra frente a su referencia propia termina en −20%; la otra permanece en 0%. Las dos terminan con saldo 80. La geometría, el número de saldo y el porcentaje avanzan juntos.

En el cierre, el verde identifica los dos cambios relativos y el azul los dos indicadores de escala casi nula. Cada pieza viaja al modelo y añade una capa. Las piezas tienen igual tamaño: no codifican una ganancia medida.

## Resultado de la revisión

La carpeta `revision/final/` contiene 90 capturas, incluidas las entradas, movimientos, poses de lectura y cambios de escena. El informe `verificacion_temporal.json` analiza 864 instantes: cero cruces de texto detectados, cero desbordes y cero invasiones del espacio del presentador. `verification.json` comprueba las operaciones ilustrativas y la composición; `verificacion_exportacion.json` contrasta 16 fotogramas decodificados del MP4 con su imagen esperada.

La comparación monetaria continúa pendiente de resultados comparables verificados. La recomendación se mantiene provisional respecto de su ganancia incremental. El video permanece en español y sin audio.

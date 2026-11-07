# Preparación del corte con presentador

`fetch_drive_recording.py` recibe un enlace compartido de Drive y descarga el archivo original fuera del repositorio, en `/workspace/presenter_private/`. Requiere que la política de red permita los hosts de Drive. No utiliza ni solicita credenciales de Google.

`inspect_recording.py` recibe el archivo local y genera, también fuera del repositorio, metadatos, mediciones de sonoridad, candidatos conservadores de recorte y doce fotogramas. Los límites de actividad son una ayuda de inspección y no sustituyen la revisión del primer y último contenido hablado.

La edición prevista comprende recorte del silencio inicial y final, encuadre del rostro para la esquina superior derecha reservada, ajuste moderado de exposición, nivelación de la voz, mezcla de la instrumentación 03 y atenuación de música según la locución. La posición se mantiene fuera de los textos y los subtítulos de las escenas. Los tiempos se ajustarán a la grabación real.

Los parámetros definitivos, el encuadre, la corrección de luz y la sincronización no se pueden determinar antes de inspeccionar el archivo. El original de cámara y sus fotogramas de inspección no se incorporan automáticamente al repositorio público; se publicará el corte editado solicitado.

# Instrumentación 03 · misma melodía, nuevas voces

Esta entrega prepara la instrumentación para el montaje con la cámara y la voz del presentador. La grabación todavía no se recibió: no se produjo una versión final con un presentador ficticio ni se modificaron los resultados del video.

## Escuchar

- `musica_instrumentos_nuevos.mp3`: los dos minutos de música con los instrumentos nuevos, a nivel de escucha.
- `comparacion_antes.mp3` y `comparacion_instrumentos.mp3`: los mismos 32 segundos de la versión anterior y la nueva, con volumen medido equivalente.
- `comparar_instrumentos.html`: descargar y abrir localmente para cambiar de versión conservando la posición de escucha.
- `musica.wav`, `acentos.wav` y `banda_sonora.wav`: pistas a 48 kHz/24 bits con margen para mezclar la voz.

El `score.json` es idéntico, byte por byte, al de `audio_v2`: se mantienen las notas, los tiempos, las duraciones y las velocidades. Se retiraron de la mezcla los dobles de pulso y el colchón sintético; la melodía y los acordes principales no se recompusieron.

## Instrumentos nuevos

| Función | Instrumentación 02 | Instrumentación 03 |
| --- | --- | --- |
| Melodía | Triángulo con doble de pulso | Piano acústico muestreado |
| Acordes | Piano FM sintetizado | Piano eléctrico muestreado |
| Bajo | Oscilador triangular | Bajo eléctrico de dedos |
| Arpegios | Pluck FM | Guitarra acústica de nylon |
| Acentos | Glint FM | Vibráfono |
| Percusión | Bombo y ruido filtrado | Síntesis de apoyo más suave |

Se usa `Tone.Sampler` con 49 notas seleccionadas del banco FluidR3_GM. Los ataques, decaimientos y resonancias de los presets sustituyen los osciladores básicos. Se redujeron el chorus y la acumulación de capas para favorecer una paleta común.

## Investigación de repositorios

- [tonejs-instruments](https://github.com/nbrosowsky/tonejs-instruments): carga de instrumentos acústicos en Tone.js, conjuntos de muestras y estrategia de cargar sólo las necesarias. Es una vía directa dentro del framework existente, pero su catálogo no incluye el piano eléctrico elegido.
- [midi-js-soundfonts](https://github.com/gleitz/midi-js-soundfonts): banco común con piano, piano eléctrico, bajo, nylon y vibráfono. Se eligió FluidR3_GM, identificado por el repositorio como CC BY 3.0. Se extraen sólo las notas utilizadas; las muestras y sus hashes están en `sample_manifest.json`.
- [smplr](https://github.com/danigb/smplr): ejemplos de instrumentos muestreados, pianos con capas de velocidad, preparación asíncrona y selección de notas. Es una alternativa útil, aunque para este cambio se conservó Tone.js y su secuenciación ya existente.
- [soundfont-player](https://github.com/danigb/soundfont-player): ejemplos de carga y programación de SoundFonts en Web Audio. Se reutiliza el concepto de banco de instrumentos, sin añadir otro motor al proyecto.

Los README consultados se conservan en `research/`. La selección responde al cambio de timbres; no implica que todos los presets de un banco tengan calidad o carácter idénticos.

## Créditos y licencias

Las muestras FluidR3_GM se distribuyen bajo CC BY 3.0 según el repositorio de origen. El crédito, enlace y tratamientos están en [`assets/CREDITS.md`](assets/CREDITS.md); el README de origen se conserva en `assets/SOURCE_README.md`. Los MP3 también incluyen ese crédito en sus metadatos. La composición original y el código del proyecto mantienen su licencia correspondiente; las muestras no se relicencian como código.

## Reconstrucción y próxima edición

```sh
python3 fetch_samples.py
python3 render_audio.py
python3 master_audio.py
python3 build_preview.py
python3 verify_preview.py
```

Se conserva Tone.js 15.1.22 en `../audio_v1/vendor/`. La descarga de muestras no es necesaria si ya están presentes en `assets/`.

Cuando se reciba el video del presentador, se revisarán su encuadre y audio, se colocará en el espacio superior derecho reservado, se ajustarán las escenas y los subtítulos a la locución y se mezclará la música con su voz. La edición de cámara y la sincronización definitiva dependen de ese archivo.

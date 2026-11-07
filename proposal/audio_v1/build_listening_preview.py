"""Package the listening workbench as one downloadable offline HTML file."""
import base64,re
from pathlib import Path

HERE=Path(__file__).resolve().parent

def data(path,mime):return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode('ascii')

def main():
 page=(HERE/'index.html').read_text()
 page=page.replace('src="video_con_sonido_compatible.mp4"','src="'+data(HERE/'video_con_sonido_compatible.mp4','video/mp4')+'"')
 page=page.replace('src="musica.m4a"','src="'+data(HERE/'musica.m4a','audio/mp4')+'"').replace('src="acentos.m4a"','src="'+data(HERE/'acentos.m4a','audio/mp4')+'"')
 page=page.replace('<script src="score_data.js"></script>','<script>'+(HERE/'score_data.js').read_text()+'</script>')
 page=page.replace('<script src="player.js"></script>','<script>'+(HERE/'player.js').read_text()+'</script>')
 page=re.sub(r'<div class="links">.*?</div>','<div class="links"><a id="download-movie" class="link" href="#" download="video_con_sonido_compatible.mp4">Descargar MP4 compatible</a></div>',page,flags=re.S)
 page=re.sub(r'<details>.*?</details>','''<details><summary>La idea musical y las capas</summary><p>Una pregunta de tres notas —re, mi, la— recorre la pieza y se completa con un re superior cuando las cuatro variables llegan al modelo. Los datos iguales comparten una nota; el cambio mensual desciende, la media reúne notas y la melodía se retira durante los resultados.</p><p>La música y los acentos se pueden escuchar por separado. Ambos comienzan en el instante cero del video.</p><ul><li><a id="download-music" href="#" download="musica.m4a">Descargar música</a></li><li><a id="download-fx" href="#" download="acentos.m4a">Descargar acentos</a></li></ul><p>La comparación monetaria continúa pendiente de resultados verificados. Los acentos siguen los movimientos, sin representar ganancias experimentales.</p></details>''',page,flags=re.S)
 page=page.replace('</body>','''<script>document.getElementById('download-movie').href=document.getElementById('video').src;document.getElementById('download-music').href=document.getElementById('music').src;document.getElementById('download-fx').href=document.getElementById('fx').src;</script></body>''')
 output=HERE/'escucha_interactiva.html';output.write_text(page)
 print(f'Vista de escucha autónoma: {output.stat().st_size/1048576:.1f} MiB')

if __name__=='__main__':main()

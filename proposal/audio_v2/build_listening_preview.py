"""Package the listening workbench as one downloadable offline HTML file."""
import base64,re
from pathlib import Path

HERE=Path(__file__).resolve().parent

def data(path,mime):return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode('ascii')

def main():
 page=(HERE/'index.html').read_text()
 page=page.replace('src="video_final.mp4"','src="'+data(HERE/'video_final.mp4','video/mp4')+'"')
 page=page.replace('src="musica.m4a"','src="'+data(HERE/'musica.m4a','audio/mp4')+'"').replace('src="acentos.m4a"','src="'+data(HERE/'acentos.m4a','audio/mp4')+'"')
 page=page.replace('<script src="score_data.js"></script>','<script>'+(HERE/'score_data.js').read_text()+'</script>')
 page=page.replace('<script src="player.js"></script>','<script>'+(HERE/'player.js').read_text()+'</script>')
 page=re.sub(r'<div class="links">.*?</div>','<div class="links"><a id="download-movie" class="link" href="#" download="video_final.mp4">Descargar película final</a></div>',page,flags=re.S)
 page=re.sub(r'<details>.*?</details>','''<details><summary>La idea musical y las capas</summary><p>Una melodía original de ocho compases se alterna con una respuesta distinta. Piano FM, bajo, arpegios y percusión ligera construyen una pieza de exploración de dos minutos. El arreglo se aligera durante los resultados y recupera el tema en la recomendación.</p><p>La música y los acentos se pueden escuchar por separado. Ambos comienzan en el instante cero del video.</p><ul><li><a id="download-music" href="#" download="musica.m4a">Descargar música</a></li><li><a id="download-fx" href="#" download="acentos.m4a">Descargar acentos</a></li></ul><p>El control de tres meses obtuvo 401,915 M ARS; el snapshot, 343,498 M; la extensión a seis meses, 392,831 M. Son puntajes públicos de recetas completas informados por el usuario.</p></details>''',page,flags=re.S)
 page=page.replace('</body>','''<script>document.getElementById('download-movie').href=document.getElementById('video').src;document.getElementById('download-music').href=document.getElementById('music').src;document.getElementById('download-fx').href=document.getElementById('fx').src;</script></body>''')
 output=HERE/'escucha_interactiva.html';output.write_text(page)
 print(f'Vista de escucha autónoma: {output.stat().st_size/1048576:.1f} MiB')

if __name__=='__main__':main()

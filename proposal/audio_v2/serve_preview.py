"""Local preview server with byte-range support for reliable media seeking."""
import re
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path

class MediaHandler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,directory=str(Path(__file__).resolve().parent.parent),**kwargs)
 def send_head(self):
  path=Path(self.translate_path(self.path));self.byte_range=None
  if not path.is_file():return super().send_head()
  stream=path.open('rb');size=path.stat().st_size
  requested=self.headers.get('Range')
  if requested:
   match=re.fullmatch(r'bytes=(\d+)-(\d*)',requested)
   if not match:
    stream.close();self.send_error(416);return None
   start=int(match[1]);end=min(size-1,int(match[2]) if match[2] else size-1)
   if start>size-1 or end<start:
    stream.close();self.send_error(416);return None
   self.byte_range=(start,end);self.send_response(206);self.send_header('Content-Range',f'bytes {start}-{end}/{size}');length=end-start+1;stream.seek(start)
  else:self.send_response(200);length=size
  self.send_header('Content-type',self.guess_type(str(path)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(length));self.end_headers();return stream
 def copyfile(self,source,out):
  try:
   if self.byte_range:
    remaining=self.byte_range[1]-self.byte_range[0]+1
    while remaining:
     chunk=source.read(min(65536,remaining))
     if not chunk:break
     out.write(chunk);remaining-=len(chunk)
   else:super().copyfile(source,out)
  except (BrokenPipeError,ConnectionResetError):
   pass  # Browsers cancel obsolete byte ranges when seeking or switching media.

if __name__=='__main__':
 print('http://127.0.0.1:8768/audio_v2/',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8768),MediaHandler).serve_forever()

"""Download a shared Drive video through its normal public download/confirmation form."""
import argparse,http.cookiejar,urllib.request,urllib.parse,re,hashlib,json
from html.parser import HTMLParser
from pathlib import Path
class Form(HTMLParser):
 def __init__(self):super().__init__();self.action=None;self.fields={};self.active=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='form':
   self.active=d.get('id')=='download-form'
   if self.active:self.action=d.get('action')
  if self.active and tag=='input' and d.get('name') and d.get('value') is not None:self.fields[d['name']]=d['value']
 def handle_endtag(self,tag):
  if tag=='form':self.active=False
def main():
 p=argparse.ArgumentParser();p.add_argument('url');p.add_argument('--out',type=Path,default=Path('/workspace/presenter_private/recording.mp4'));a=p.parse_args()
 m=re.search(r'/file/d/([^/?]+)',a.url)
 if not m:p.error('Expected a Drive file link')
 file_id=m[1];opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
 url='https://drive.usercontent.google.com/download?'+urllib.parse.urlencode({'id':file_id,'export':'download'})
 for attempt in range(3):
  with opener.open(url,timeout=60) as r:
   kind=r.headers.get('Content-Type','')
   if 'text/html' not in kind:
    a.out.parent.mkdir(parents=True,exist_ok=True);tmp=a.out.with_suffix('.partial');h=hashlib.sha256();size=0
    with tmp.open('wb') as f:
     while True:
      part=r.read(1024*1024)
      if not part:break
      f.write(part);h.update(part);size+=len(part)
    assert size>1024,'Empty or invalid media download';tmp.replace(a.out)
    print(json.dumps({'path':str(a.out),'bytes':size,'sha256':h.hexdigest(),'type':kind},indent=2));return
   body=r.read().decode(errors='replace');form=Form();form.feed(body)
   if not form.action:raise RuntimeError('Drive did not return a public download form; file sharing access may be required')
   parsed=urllib.parse.urlparse(form.action)
   if parsed.scheme!='https' or parsed.hostname not in {'drive.google.com','drive.usercontent.google.com'}:raise RuntimeError('Unexpected download host; review network access before following')
   url=form.action+'?'+urllib.parse.urlencode(form.fields)
 raise RuntimeError('Download confirmation did not resolve')
if __name__=='__main__':main()

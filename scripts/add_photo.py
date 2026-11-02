#!/usr/bin/env python3
"""Scarica una foto da Wikimedia Commons (solo licenze libere), la ottimizza e registra autore/licenza.
Uso: python3 scripts/add_photo.py "File:Nome.jpg" nome-breve
Poi nell'articolo: ':::foto nome-breve | didascalia' (la didascalia viene tradotta a mano nei file EN)."""
import sys,json,re,io,time,urllib.request,urllib.parse,os,html,fcntl
from PIL import Image
UA='UnniVaiBlogBot/1.0 (https://unnivai.com; sciretta.clienti@gmail.com) python-urllib'
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get(u):
    for i in range(8):
        try:return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=60).read()
        except Exception as e:time.sleep(20)
    raise SystemExit('download fallito '+u)
title,name=sys.argv[1],sys.argv[2]
u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',format='json',titles=title,prop='imageinfo',iiprop='url|extmetadata',iiurlwidth=1400))
pg=list(json.loads(get(u))['query']['pages'].values())[0];ii=pg['imageinfo'][0];m=ii['extmetadata']
lic=m.get('LicenseShortName',{}).get('value','')
assert re.match(r'(CC BY|CC0|Public domain|Attribution)',lic),'licenza non ammessa: '+lic
artist=html.unescape(re.sub(r'<[^>]+>','',m.get('Artist',{}).get('value','')).strip()) or 'Autore ignoto'
im=Image.open(io.BytesIO(get(ii['thumburl']))).convert('RGB')
if im.width>1400:im=im.resize((1400,round(im.height*1400/im.width)))
os.makedirs(R+'/site/blog/img',exist_ok=True)
# peso: massimo ~200 KB per la foto grande, qualita' scende finche' ci sta
q=80
while True:
    buf=io.BytesIO();im.save(buf,'WEBP',quality=q,method=6)
    if buf.tell()<=200*1024 or q<=55:break
    q-=5
open(f'{R}/site/blog/img/{name}.webp','wb').write(buf.getvalue())
# miniatura per le card (640 px)
th=im.copy();th.thumbnail((640,640*3));th.save(f'{R}/site/blog/img/{name}-640.webp','WEBP',quality=72,method=6)
p=R+'/blog-src/photos.json'
with open(R+'/blog-src/.photos.lock','w') as lk:
    fcntl.flock(lk,fcntl.LOCK_EX)
    d=json.load(open(p)) if os.path.exists(p) else {}
    d[name]=dict(file=title,artist=artist[:80],license=lic,url=ii['descriptionurl'],w=im.width,h=im.height)
    json.dump(d,open(p,'w'),ensure_ascii=False,indent=1)
print(name,im.size,lic,artist[:50],f'{buf.tell()//1024}KB q{q}')

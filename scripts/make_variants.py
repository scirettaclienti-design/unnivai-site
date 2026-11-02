#!/usr/bin/env python3
"""Per ogni foto in photos.json: originale <=200 KB, varianti -640 e -960 (idempotente)."""
import json,os,io,time
from PIL import Image
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));D=R+'/site/blog/img'
def save(im,path,q):
    im.save(path,'WEBP',quality=q,method=6)
for k in json.load(open(R+'/blog-src/photos.json')):
    f=f'{D}/{k}.webp'
    if not os.path.exists(f) or time.time()-os.path.getmtime(f)<45:continue   # in scrittura da add_photo
    im=Image.open(f).convert('RGB');ch=False
    q=74
    while os.path.getsize(f)>200*1024 and q>=46:
        save(im,f,q);q-=4;ch=True
    for w,qq in((640,72),(960,74)):
        v=f'{D}/{k}-{w}.webp'
        if ch or not os.path.exists(v) or os.path.getmtime(v)<os.path.getmtime(f):
            t=im.copy()
            if t.width>w:t=t.resize((w,round(t.height*w/t.width)),Image.LANCZOS)
            save(t,v,qq)
    if ch:print('ricompresso',k,os.path.getsize(f)//1024,'KB')

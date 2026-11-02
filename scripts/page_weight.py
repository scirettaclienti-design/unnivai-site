#!/usr/bin/env python3
"""Peso delle pagine articolo: HTML + CSS + immagini <img> locali (font esclusi). Uso: python3 scripts/page_weight.py [site_dir]"""
import re,os,glob,sys,gzip
S=sys.argv[1] if len(sys.argv)>1 else 'site'
def sz(p):return os.path.getsize(p) if os.path.exists(p) else 0
css=sz(S+'/blog.css')
rows=[]
for p in sorted(glob.glob(S+'/blog/*/index.html')+glob.glob(S+'/en/blog/*/index.html')):
    parts=p[len(S):].split('/')
    if len(parts)>=4 and parts[-3] in('categoria','tema','category','topic','questions','domande'):continue
    slug=parts[-2]
    if slug in('categoria','tema','category','topic','questions','domande','og','img'):continue
    h=open(p).read()
    # solo immagini caricate subito (no lazy), poi tutte
    imgs=set(re.findall(r'<img[^>]+src="(/[^"]+)"',h))
    eager=set(m for m in re.findall(r'<img(?![^>]*loading="lazy")[^>]+src="(/[^"]+)"',h))
    allimg=sum(sz(S+u) for u in imgs if not u.endswith('logo.webp'))
    first=sum(sz(S+u) for u in eager if not u.endswith('logo.webp'))
    rows.append((p[len(S):-11],len(h.encode()),css,first,allimg))
print(f"{'pagina':62s} {'HTML':>7s} {'1a vista':>9s} {'totale':>8s}  (KB; 1a vista = HTML+CSS+img non lazy)")
for r in rows:print(f"{r[0]:62s} {r[1]//1024:6d}K {(r[1]+r[2]+r[3])//1024:8d}K {(r[1]+r[2]+r[4])//1024:7d}K")
n=len(rows)
if n:print(f"MEDIA su {n} pagine: prima vista {sum(r[1]+r[2]+r[3] for r in rows)//n//1024} KB, totale con tutte le immagini {sum(r[1]+r[2]+r[4] for r in rows)//n//1024} KB")

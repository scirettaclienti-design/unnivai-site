#!/usr/bin/env python3
"""Controllo link interni. Uso: python3 scripts/check_links.py [id-articolo-IT]
Errori (exit 1): link /blog/<slug> verso articolo inesistente; articolo orfano (0 link in entrata da altri articoli).
Avvisi: meno di 2 link in entrata, meno di 3 in uscita (IT ed EN controllati separatamente)."""
import sys,re,os,glob
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(d):
    return {os.path.basename(f)[:-3]:open(f,encoding='utf-8').read() for f in glob.glob(R+d+'/*.md')}
only=sys.argv[1] if len(sys.argv)>1 else None
errs=[];warns=[]
en_id={}
EN=load('/blog-src/en')
for s,t in EN.items():
    m=re.search(r'^id:\s*(\S+)',t,re.M)
    if m:en_id[m.group(1)]=s
for lang,D in(('IT',load('/blog-src')),('EN',EN)):
    slugs=set(D)
    inb={s:set() for s in D};out={s:set() for s in D}
    for s,t in D.items():
        for l in re.findall(r'\]\(/blog/([a-z0-9-]+)\)',t):
            if l in ('categoria','tema','domande'):continue
            if l not in slugs:errs.append(f'{lang} {s}: link a /blog/{l} inesistente')
            elif l!=s:out[s].add(l);inb[l].add(s)
    for s in sorted(D):
        slug_it=s if lang=='IT' else next((k for k,v in en_id.items() if v==s),s)
        if only and slug_it!=only:continue
        if not inb[s]:errs.append(f'{lang} {s}: ORFANO (nessun altro articolo linka qui)')
        elif len(inb[s])<2:warns.append(f'{lang} {s}: solo {len(inb[s])} link in entrata (regola: >=2)')
        if len(out[s])<3:warns.append(f'{lang} {s}: solo {len(out[s])} link in uscita (regola: >=3)')
for w in warns:print('⚠',w)
for e in errs:print('✗',e)
if errs:sys.exit(1)
print('✓ link interni ok')

#!/usr/bin/env python3
"""Controllo foto. Uso: python3 scripts/check_covers.py [id-articolo-IT]
Errori (exit 1): chiave foto mancante in photos.json, file vuoto, copertina (prima :::foto) uguale a quella di un altro articolo,
IT ed EN con copertine diverse. Avviso: meno di 3 foto. Senza argomento controlla tutti gli articoli."""
import sys,re,os,glob,json
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P=json.load(open(R+'/blog-src/photos.json'))
def keys(path):return re.findall(r'^:::foto[ \t]+([^|\n]+?)[ \t]*\|',open(path,encoding='utf-8').read(),re.M)
def en_of(path):
    m=re.search(r'^id:\s*(\S+)',open(path,encoding='utf-8').read(),re.M);return m.group(1) if m else None
it={os.path.basename(f)[:-3]:f for f in glob.glob(R+'/blog-src/*.md')}
en={}
for f in glob.glob(R+'/blog-src/en/*.md'):
    i=en_of(f)
    if i:en[i]=f
errs=[];warns=[];covers={}
only=sys.argv[1] if len(sys.argv)>1 else None
for slug,f in sorted(it.items()):
    k=keys(f)
    if k:covers.setdefault(k[0],[]).append(slug)
    if only and slug!=only:continue
    for key in k:
        if key not in P:errs.append(f'{slug}: foto "{key}" non presente in photos.json')
        elif not os.path.exists(f'{R}/site/blog/img/{key}.webp') or os.path.getsize(f'{R}/site/blog/img/{key}.webp')==0:errs.append(f'{slug}: file immagine "{key}" mancante o vuoto')
    if len(k)!=len(set(k)):errs.append(f'{slug}: stessa foto ripetuta nell\'articolo')
    if slug in en:
        ke=keys(en[slug])
        if k!=ke:errs.append(f'{slug}: IT ed EN devono avere le stesse foto nello stesso ordine ({k} / {ke})')
    if 0<len(k)<3:warns.append(f'{slug}: {len(k)} foto (regola: 3-4)')
    if not k:warns.append(f'{slug}: nessuna foto (copertina illustrata)')
for key,sl in covers.items():
    if len(sl)>1 and (not only or only in sl):errs.append(f'copertina "{key}" usata da piu\' articoli: {", ".join(sl)} (ogni articolo deve avere una copertina diversa)')
for w in warns:print('! '+w)
if errs:print('\n'.join('✗ '+e for e in errs));sys.exit(1)
print('✓ foto e copertine ok')

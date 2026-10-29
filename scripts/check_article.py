#!/usr/bin/env python3
"""Controllo qualita' PRIMA di pubblicare. Uso: python3 scripts/check_article.py <id-articolo-IT>
Esce con codice 1 se una regola editoriale non e' rispettata: in quel caso NON si fa push."""
import sys,re,os,glob,datetime
def fm(path):
    raw=open(path,encoding='utf-8').read();_,f,body=raw.split('---',2);d={'faq':0,'sources':[],'scheda':0};cur=None
    for ln in f.strip().split('\n'):
        if ln.startswith('faq:'):cur='faq';continue
        if ln.startswith('sources:'):cur='sources';continue
        if ln.startswith('scheda:'):cur='scheda';continue
        if ln.startswith('- '):
            if cur=='faq':d['faq']+=1
            elif cur=='sources':d['sources'].append(ln[2:].split('::')[-1].strip())
            elif cur=='scheda':d['scheda']+=1
            continue
        k,v=ln.split(':',1);d[k.strip()]=v.strip();cur=None
    d['body']=body;return d
def words(b):return len(re.sub(r'[:#*>\[\]()|{}-]',' ',re.sub(r'\(https?://[^)]+\)','',b)).split())
def dom(u):return re.sub(r'^https?://(www\.)?','',u).split('/')[0]
slug=sys.argv[1];errs=[]
it=f'blog-src/{slug}.md'
if not os.path.exists(it):print('manca',it);sys.exit(1)
a=fm(it);en=[p for p in glob.glob('blog-src/en/*.md') if fm(p).get('id',os.path.basename(p)[:-3])==slug]
if not en:errs.append('manca la versione EN (stesso id)')
for lab,p,d in [('IT',it,a)]+[('EN',en[0],fm(en[0]))] if en else [('IT',it,a)]:
    w=words(d['body'])
    if w<1100:errs.append(f'{lab}: {w} parole (minimo 1100)')
    if not 30<=len(d['title'])<=65:errs.append(f"{lab}: titolo {len(d['title'])} caratteri (30-65)")
    if not 70<=len(d['description'])<=160:errs.append(f"{lab}: description {len(d['description'])} caratteri (70-160)")
    if d['faq']<4:errs.append(f"{lab}: FAQ {d['faq']} (minimo 4)")
    if d['scheda']<3:errs.append(f"{lab}: scheda con meno di 3 voci")
    doms={dom(u) for u in d['sources']}
    if len(d['sources'])<3 or len(doms)<2:errs.append(f"{lab}: servono 3 fonti da almeno 2 domini (ora {len(d['sources'])}/{len(doms)})")
    if len(re.findall(r'\]\(/blog/',d['body']))<3:errs.append(f'{lab}: servono almeno 3 link interni ad altri articoli')
    if not re.search(r'^> ',d['body'],re.M):errs.append(f'{lab}: manca il riquadro "In breve"')
    if re.search(r'TODO|XXX|lorem|\[\?\]',d['body'],re.I):errs.append(f'{lab}: segnaposto nel testo')
    if d.get('updated',d.get('date'))!=datetime.date.today().isoformat():errs.append(f"{lab}: 'date' (o 'updated' nei refresh) deve essere oggi ({datetime.date.today().isoformat()})")
    if len(re.findall(r'\d{1,2}[.:]\d{2}',d['body']))>0 and 'verific' not in d['body'].lower() and 'checked' not in d['body'].lower():errs.append(f'{lab}: orari presenti ma manca la nota di verifica')
if errs:print('\n'.join('✗ '+e for e in errs));sys.exit(1)
print('✓ articolo ok:',slug)

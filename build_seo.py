import json,os,hashlib,html,datetime
SITE='site';BASE='https://unnivai.com'
S={l:json.load(open(f'seo_{l}.json')) for l in ('it','en') if os.path.exists(f'seo_{l}.json')}
def url(path):
    u=path.replace('/index.html','').replace('.html','')
    return BASE+(u or '/')
latest=max(p['date'] for l in S for p in S[l]['posts'])
lm={}
for l in S:
    for p in S[l]['posts']:lm[('/en' if l=='en' else '')+'/blog/'+p['slug']]=p['updated']
def mod(u):return lm.get(u.replace(BASE,''),latest)
def prio(u):
    r=u.replace(BASE,'')
    if r in('/blog','/en/blog'):return '0.9'
    if r in lm:return '0.8'
    if '/category/' in r or '/categoria/' in r:return '0.7'
    return '0.6'
ent=[('/',latest,'1.0',None),('/en/',latest,'0.9',None)] if os.path.exists(SITE+'/en/index.html') else [('/',latest,'1.0',None)]
rows=[]
for l in S:
    for pg in S[l]['pages']:
        if pg['noindex']:continue
        rows.append(pg)
X='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
def entry(loc,lastmod,pr,alt,img=None):
    s=f'<url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><priority>{pr}</priority>'
    if alt:
        s+=f'<xhtml:link rel="alternate" hreflang="it" href="{alt[0]}"/><xhtml:link rel="alternate" hreflang="en" href="{alt[1]}"/><xhtml:link rel="alternate" hreflang="x-default" href="{alt[0]}"/>'
    if img:s+=f'<image:image><image:loc>{img}</image:loc></image:image>'
    return s+'</url>'
out=[];allurls=[]
home_alt=(BASE+'/',BASE+'/en/') if os.path.exists(SITE+'/en/index.html') else None
out.append(entry(BASE+'/',latest,'1.0',home_alt));allurls.append(BASE+'/')
if home_alt:out.append(entry(BASE+'/en/',latest,'0.9',home_alt));allurls.append(BASE+'/en/')
for pg in rows:
    u=url(pg['path'])
    r=u.replace(BASE,'')
    slug=r.split('/')[-1]
    img=f'{BASE}/blog/og/{slug}.png' if r in lm else None
    out.append(entry(u,mod(u),prio(u),pg['alt'],img));allurls.append(u)
open(SITE+'/sitemap.xml','w').write(X+''.join(out)+'</urlset>')
BOTS=['GPTBot','OAI-SearchBot','ChatGPT-User','ClaudeBot','Claude-SearchBot','Claude-User','PerplexityBot','Perplexity-User','Google-Extended','Applebot-Extended','CCBot','Bingbot']
open(SITE+'/robots.txt','w').write('User-agent: *\nAllow: /\n\n'+''.join(f'User-agent: {b}\nAllow: /\n\n' for b in BOTS)+f'Sitemap: {BASE}/sitemap.xml\n')
li="# UNNIVAI\n\n> UNNIVAI is a travel app that builds routes through real places and rewrites them when your day changes. Born in Sicily, for all of Italy. The blog publishes verified guides and itineraries in Italian and English. / UNNIVAI è un'app di turismo che costruisce percorsi con luoghi veri e li riscrive quando cambia la giornata.\n"
for l,t in (('it','Blog (italiano)'),('en','Blog (English)')):
    if l in S:
        li+=f"\n## {t}\n"+''.join(f"- [{p['title']}]({BASE}{'/en' if l=='en' else ''}/blog/{p['slug']}): {p['desc']}\n" for p in S[l]['posts'])
li+=f"\n## Pages\n- [Home]({BASE}/)\n- [Questions / Domande]({BASE}/blog/domande)\n- [Questions (EN)]({BASE}/en/blog/questions)\n- [Author]({BASE}/en/author)\n- [Sitemap]({BASE}/sitemap.xml)\n"
open(SITE+'/llms.txt','w').write(li)
full=li+'\n---\n'
for l in S:
    for p in S[l]['posts']:full+=f"\n# {p['title']}\nURL: {BASE}{'/en' if l=='en' else ''}/blog/{p['slug']}\nLanguage: {l}\nUpdated: {p['updated']}\n\n{p['text']}\n"
open(SITE+'/llms-full.txt','w').write(full)
KEY=hashlib.md5(b'unnivai-indexnow').hexdigest();open(f'{SITE}/{KEY}.txt','w').write(KEY)
json.dump({'host':'unnivai.com','key':KEY,'keyLocation':f'{BASE}/{KEY}.txt','urlList':allurls},open('indexnow_payload.json','w'))
open('indexnow.sh','w').write('#!/bin/bash\n# IndexNow (Bing, Yandex, ecc.). Google NON usa IndexNow: per Google serve Search Console.\ncurl -s -X POST https://api.indexnow.org/indexnow -H "Content-Type: application/json" -d @indexnow_payload.json -w "HTTP %{http_code}\\n"\n')
print('sitemap urls',len(allurls))

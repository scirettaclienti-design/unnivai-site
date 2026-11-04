#!/usr/bin/env python3
"""Genera la guida PDF lead magnet UNNIVAI dai 15 articoli verificati.
Uso: python3 growth/guida/build_guida.py  ->  site/guida/unnivai-italia-un-giorno-alla-volta.pdf
Solo contenuti già presenti negli articoli (In breve + scheda + data verifica + foto con licenza)."""
import re,os,json,glob,io,base64,datetime,html,subprocess,sys
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG=R+'/site/blog/img';FONTS=R+'/site/fonts'
P=json.load(open(R+'/blog-src/photos.json'))
import segno
ORDER=['milano-in-un-weekend-con-la-pioggia','venezia-come-evitare-la-folla','bologna-in-un-giorno','firenze-in-48-ore','cinque-terre-a-piedi','roma-in-due-giorni','napoli-cosa-mangiare-in-ordine-di-giornata','matera-come-visitare-i-sassi','lecce-in-un-giorno','polignano-a-mare-senza-auto','palermo-street-food-mercati-orari-cosa-ordinare','cosa-mangiare-a-catania','pescheria-di-catania-orari-e-consigli','cosa-fare-a-catania-quando-piove','un-giorno-a-ortigia']
def esc(s):return html.escape(s,quote=False)
def clean(s):
    s=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',s);s=re.sub(r'\*\*?([^*]+)\*\*?',r'\1',s);return s.strip()
def parse(slug):
    t=open(f'{R}/blog-src/{slug}.md',encoding='utf-8').read()
    fm=t.split('---')[1];body=t.split('---',2)[2]
    g=lambda k:(re.search(r'^'+k+r':\s*(.*)$',fm,re.M) or [0,''])[1].strip()
    scheda=[]
    m=re.search(r'^scheda:\n((?:- .*\n)+)',fm+'\n',re.M)
    if m:
        for l in m.group(1).strip().split('\n'):
            a,b=l[2:].split('::',1);scheda.append((a.strip(),clean(b)))
    br=re.search(r'In breve\.\*\*\s*(.+)',body);ph=re.findall(r'^:::foto[ \t]+([^|\n]+?)[ \t]*\|[ \t]*(.*)$',body,re.M)
    return dict(slug=slug,title=g('title'),cat=g('category'),updated=g('updated') or g('date'),scheda=scheda,brief=clean(br.group(1)) if br else '',photo=ph[0] if ph else None)
def b64(path):return base64.b64encode(open(path,'rb').read()).decode()
from PIL import Image
def jpg64(k):
    im=Image.open(f'{IMG}/{k}.webp').convert('RGB');im.thumbnail((1000,1000));b=io.BytesIO();im.save(b,'JPEG',quality=80,optimize=True);return base64.b64encode(b.getvalue()).decode()
def font(name,w):return f"@font-face{{font-family:'{name}';font-weight:{w};src:url(data:font/woff2;base64,{b64(f'{FONTS}/{name.lower().replace(' ','-')}-latin-{w}-normal.woff2')}) format('woff2')}}"
def qr(url):
    b=io.BytesIO();segno.make(url,error='m').save(b,kind='svg',scale=4,border=1,dark='#EAF2F0',light=None,xmldecl=False,svgns=True);return b.getvalue().decode()
arts=[parse(s) for s in ORDER]
IT=lambda d:datetime.date.fromisoformat(d).strftime('%d/%m/%Y')
TODAY=datetime.date.today()
mesi=['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'][TODAY.month-1]
css=font('Bricolage Grotesque',800)+font('Bricolage Grotesque',500)+font('Instrument Sans',400)+font('Instrument Sans',600)+font('IBM Plex Mono',400)+'''
@page{size:148mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#06161E;--ink:#EAF2F0;--ink2:#9BB5BC;--line:rgba(234,242,240,.16);--ac:#FF6B3D}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{background:var(--bg);color:var(--ink);font:400 10.2pt/1.5 'Instrument Sans',sans-serif}
.pg{width:148mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;background:var(--bg)}
.pg:last-child{page-break-after:auto}
h1,h2,h3{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;line-height:1.04;letter-spacing:-.015em}
.mono{font-family:'IBM Plex Mono',monospace;font-size:7.4pt;letter-spacing:.12em;text-transform:uppercase;color:var(--ink2)}
.ac{color:var(--ac)}
/* cover */
.cover{display:flex;flex-direction:column;justify-content:space-between;padding:16mm 14mm;background:radial-gradient(120% 70% at 85% 8%,rgba(255,107,61,.28),transparent 60%),var(--bg)}
.cover h1{font-size:40pt;margin:0 0 6mm}.cover h1 em{font-style:normal;color:var(--ac)}
.cover p.lead{font-size:12pt;color:var(--ink2);max-width:104mm;line-height:1.45}
.cover .stats{display:flex;gap:7mm;margin-top:9mm}.cover .stats b{display:block;font:800 22pt 'Bricolage Grotesque';color:var(--ink)}
.brand{font:800 12pt 'Bricolage Grotesque';letter-spacing:.04em}
/* text pages */
.txt{padding:18mm 14mm}.txt h2{font-size:24pt;margin:3mm 0 6mm}.txt p{margin:0 0 3.4mm;color:var(--ink)}.txt p.s{color:var(--ink2)}
.txt ul{margin:0 0 4mm 4.5mm}.txt li{margin-bottom:2mm}
.rule{border-top:1px solid var(--line);margin:6mm 0}
/* index */
.idx li{list-style:none;margin:0;display:flex;gap:4mm;padding:2.3mm 0;border-bottom:1px solid var(--line);font-size:9.6pt}
.idx{margin:0!important}.idx span{font-family:'IBM Plex Mono',monospace;color:var(--ac);width:8mm}
.idx i{margin-left:auto;font-style:normal;color:var(--ink2);font-size:8pt}
/* chapter */
.ph{height:62mm;position:relative;overflow:hidden}.ph img{width:100%;height:100%;object-fit:cover;display:block}
.ph:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,22,30,0) 45%,var(--bg) 100%)}
.ch{padding:0 14mm}
.ch .mono{margin-top:1mm}.ch h2{font-size:19pt;margin:1.5mm 0 3mm}
.brief{font-size:9.8pt;line-height:1.48;margin-bottom:4mm}
.sch{border-top:1px solid var(--line)}
.sch div{display:grid;grid-template-columns:25mm 1fr;gap:3mm;padding:1.5mm 0;border-bottom:1px solid var(--line);font-size:8.3pt;line-height:1.36}
.sch dt{font-family:'IBM Plex Mono',monospace;font-size:7pt;letter-spacing:.1em;text-transform:uppercase;color:var(--ac);padding-top:.6mm}
.sch dd{color:var(--ink)}
.foot{position:absolute;left:14mm;right:14mm;bottom:8mm;font-size:6.6pt;line-height:1.5;display:flex;justify-content:space-between;align-items:flex-end;gap:5mm;font-size:7.4pt;color:var(--ink2)}
.foot a{color:var(--ink);text-decoration:none;font-weight:600;font-size:8.4pt}
.foot .q{width:15mm;height:15mm;flex:none}.foot .q svg{width:100%;height:100%}
.cred{font-size:6.4pt;color:var(--ink2);margin-top:2mm}
.num{position:absolute;right:14mm;top:9mm;z-index:3;font:400 7.4pt 'IBM Plex Mono';letter-spacing:.12em;color:#fff;text-shadow:0 0 6px #000}
svg{display:block;width:100%;height:100%}
/* closing */
.end{padding:18mm 14mm;display:flex;flex-direction:column;justify-content:center;background:radial-gradient(110% 60% at 15% 95%,rgba(255,107,61,.3),transparent 60%),var(--bg)}
.end h2{font-size:28pt;margin-bottom:6mm}.btnx{display:inline-block;background:var(--ac);color:#1A0A04;font:800 11pt 'Bricolage Grotesque';padding:3.4mm 7mm;border-radius:99px;text-decoration:none;margin-top:5mm}
'''
pages=[]
pages.append(f'''<section class="pg cover"><div class="brand">UNNIVAI</div><div><p class="mono" style="margin-bottom:5mm">Guida di viaggio · edizione {mesi} {TODAY.year}</p>
<h1>Italia,<br>un giorno<br><em>alla volta.</em></h1><p class="lead">{len(arts)} guide a piedi, in treno e a tavola, scritte sulle fonti ufficiali. Con orari, prezzi e cosa è chiuso, letti sulle pagine aperte e datati.</p>
<div class="stats"><div><b>{len(arts)}</b><span class="mono">guide</span></div><div><b>{len(set(a['cat'] for a in arts))}</b><span class="mono">destinazioni</span></div><div><b>0</b><span class="mono">dati a memoria</span></div></div></div>
<p class="mono">unnivai.com/blog</p></section>''')
pages.append(f'''<section class="pg txt"><p class="mono">Come usarla</p><h2>Una guida vale quanto i dati che la reggono.</h2>
<p>Ogni pagina riassume una guida completa del blog UNNIVAI: la risposta in breve, la scheda con zona, durata, budget e cosa controllare, e il link all'articolo con itinerario, fonti e foto.</p>
<div class="rule"></div>
<p><b>Cosa troverai</b></p><ul><li>Orari, prezzi e regole d'accesso letti su pagine ufficiali (Comuni, musei, parchi, trasporti, UNESCO).</li><li>La data dell'ultima verifica su ogni pagina. Se due fonti discordano, lo diciamo nell'articolo.</li><li>Foto reali con licenza libera (Wikimedia Commons), con autore e licenza.</li></ul>
<p><b>Cosa non troverai</b></p><ul><li>Locali o negozi non letti su una fonte aperta.</li><li>Immagini generate con l'AI presentate come foto dei luoghi.</li></ul>
<div class="rule"></div><p class="s">Orari e prezzi cambiano con le stagioni: controlla sempre la fonte ufficiale prima di partire. Trovi i link in fondo a ogni articolo. Hai trovato un errore? Scrivi a sciretta.clienti@gmail.com.</p></section>''')
idx=''.join(f'<li><span>{i+1:02d}</span>{esc(a["title"].split(":")[0])}<i>{esc(a["cat"])}</i></li>' for i,a in enumerate(arts))
pages.append(f'<section class="pg txt"><p class="mono">Indice</p><h2>{len(arts)} guide, da Nord a Sud.</h2><ul class="idx">{idx}</ul></section>')
for i,a in enumerate(arts):
    k,cap=a['photo'];ph=P[k]
    url=f"https://unnivai.com/blog/{a['slug']}?utm_source=guida&utm_medium=pdf&utm_campaign=lead-magnet"
    sch=''.join(f'<div><dt>{esc(x)}</dt><dd>{esc(y)}</dd></div>' for x,y in a['scheda'])
    pages.append(f'''<section class="pg"><div class="ph"><img src="data:image/jpeg;base64,{jpg64(k)}" alt=""></div><span class="num">{i+1:02d} / {len(arts)}</span>
<div class="ch"><p class="mono">{esc(a['cat'])}</p><h2>{esc(a['title'])}</h2><p class="brief">{esc(a['brief'])}</p><dl class="sch">{sch}</dl>
</div>
<div class="foot"><div>Verificata il {IT(a['updated'])} · Foto: {esc(ph['artist'])}, {esc(ph['license'])}, Wikimedia Commons<br><a href="{url}">Guida completa su unnivai.com/blog →</a></div><div class="q">{qr(url)}</div></div></section>''')
home='https://unnivai.com/?src=guida#iscriviti'
pages.append(f'''<section class="pg end"><p class="mono" style="margin-bottom:5mm">Prima di partire</p><h2>Stesso giro,<br><span class="ac">ordine diverso</span> se piove.</h2>
<p style="max-width:100mm;color:var(--ink2);font-size:11pt">UNNIVAI è l'app che riscrive la giornata quando cambiano tempo, orario o stanchezza. Nasce in Sicilia ed è pensata per tutta l'Italia. Accesso anticipato a gruppi, nell'ordine di iscrizione.</p>
<div><a class="btnx" href="{home}">Entra tra i primi →</a></div>
<div style="display:flex;align-items:center;gap:5mm;margin-top:9mm"><div style="width:22mm;height:22mm">{qr(home)}</div><p class="mono">unnivai.com<br>Blog · Metodo · Autore</p></div>
<p class="cred" style="margin-top:12mm">© {TODAY.year} UNNIVAI · Ivano Sciretta. Questa guida è un riassunto: consulta sempre le fonti ufficiali per orari e prezzi aggiornati.</p></section>''')
doc=f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Italia, un giorno alla volta · UNNIVAI</title><style>{css}</style></head><body>{"".join(pages)}</body></html>'
out=R+'/growth/guida';os.makedirs(out,exist_ok=True);open(out+'/guida.html','w',encoding='utf-8').write(doc)
os.makedirs(R+'/site/guida',exist_ok=True)
js=f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{out}/guida.html');await p.waitForTimeout(800);
await p.pdf({{path:'{R}/site/guida/unnivai-italia-un-giorno-alla-volta.pdf',width:'148mm',height:'210mm',printBackground:true,preferCSSPageSize:true,margin:{{top:0,right:0,bottom:0,left:0}}}});await b.close()}})()'''
open(out+'/render.js','w').write(js)
subprocess.run(['node',out+'/render.js'],check=True)
print('ok',os.path.getsize(R+'/site/guida/unnivai-italia-un-giorno-alla-volta.pdf')//1024,'KB')

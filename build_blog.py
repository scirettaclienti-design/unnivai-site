import re,os,glob,html,hashlib,json,random,shutil
SITE='site';BASE='https://unnivai.com'
LG=os.environ.get('BLANG','it');EN=LG=='en';P='/en' if EN else '';SRC='blog-src/en' if EN else 'blog-src'
exec(open('i18n.py').read())
def L(it,en):return en if EN else it
DIRC=L('categoria','category');DIRT=L('tema','topic');DIRQ=L('domande','questions');DIRA=L('autore','author')
os.makedirs(SITE+P+'/blog',exist_ok=True)
MESI=['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre']
if os.environ.get('BLANG')=='en':MESI=['January','February','March','April','May','June','July','August','September','October','November','December']
def dfmt(d):
    y,m,g=map(int,d.split('-'));return f'{MESI[m-1]} {g}, {y}' if EN else f'{g} {MESI[m-1]} {y}'
def esc(t):return html.escape(t,quote=False)
def inline(t):
    t=esc(t)
    t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:(f'<a class="ext" href="{m.group(2)}" rel="noopener" target="_blank">{m.group(1)}</a>' if m.group(2).startswith('http') else f'<a class="int" href="{m.group(2)}">{m.group(1)}</a>'),t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',t)
    t=re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])',r'<em>\1</em>',t)
    return t
def slugify(t):
    t=t.lower();t=re.sub(r'[àá]','a',t);t=re.sub(r'[èé]','e',t);t=re.sub(r'[ìí]','i',t);t=re.sub(r'[òó]','o',t);t=re.sub(r'[ùú]','u',t)
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')
exec(open('widgets.py').read())
def dom(u):return re.sub(r'^https?://(www\.)?','',u).split('/')[0]
def md(body):
    out=[];toc=[];lines=body.strip().split('\n');para=[];lst=None;i=0
    def flush():
        nonlocal para,lst
        if para:out.append('<p>'+inline(' '.join(para))+'</p>');para=[]
        if lst:out.append('<'+lst[0]+'>'+''.join('<li>'+inline(x)+'</li>' for x in lst[1])+'</'+lst[0]+'>');lst=None
    while i<len(lines):
        s_=lines[i].rstrip();i+=1
        if s_.startswith(':::'):
            flush();head_=s_[3:].strip();name=head_.split(' ',1)[0];rest=head_[len(name):].strip()
            if name in('tappe','scheda'):
                blk=[]
                while i<len(lines) and not lines[i].startswith(':::'):
                    if lines[i].strip():blk.append(lines[i].strip().lstrip('- '))
                    i+=1
                i+=1
                if name=='tappe':
                    out.append('<ol class="tappe">'+''.join('<li><span class="tm">'+esc(x.split('|')[0].strip())+'</span><div><b>'+esc(x.split('|')[1].strip())+'</b><p>'+inline(x.split('|')[2].strip())+'</p></div></li>' for x in blk)+'</ol>')
                else:
                    out.append('<dl class="scheda">'+''.join('<div><dt>'+esc(x.split('|')[0].strip())+'</dt><dd>'+inline(x.split('|')[1].strip())+'</dd></div>' for x in blk)+'</dl>')
            elif name=='fonte':
                n,u,d=[x.strip() for x in rest.split('|')];out.append(f'<a class="fonte" href="{u}" rel="noopener" target="_blank"><span class="dom">{esc(dom(u))}</span><b>{esc(n)}</b><p>{esc(d)}</p><i aria-hidden="true">↗</i></a>')
            elif name=='widget':
                out.append(WIDGETS.get(rest,''))
            elif name=='consiglio':
                out.append('<aside class="tip"><b>Consiglio</b><p>'+inline(rest)+'</p></aside>')
            continue
        if not s_.strip():flush();continue
        if s_.startswith('## '):
            flush();h=s_[3:];wt=re.search(r'\s*\{(coperto|aperto)\}\s*$',h);wtag=wt.group(1) if wt else '';h=h[:wt.start()] if wt else h;sid=slugify(h);toc.append((sid,h))
            badge=('<span class="wb '+wtag+'">'+('Al coperto' if wtag=='coperto' else "All'aperto")+'</span>') if wtag else ''
            out.append(f'<h2 id="{sid}"'+(f' data-w="{wtag}"' if wtag else '')+f'>{inline(h)}{badge}<a class="anc" href="#{sid}" aria-label="Link a questa sezione">#</a></h2>');continue
        if s_.startswith('### '):flush();out.append(f'<h3>{inline(s_[4:])}</h3>');continue
        if s_.startswith('> '):flush();out.append(f'<aside class="callout">{inline(s_[2:])}</aside>');continue
        m=re.match(r'^(\d+)\.\s+(.*)',s_)
        if s_.startswith('- '):
            if para or (lst and lst[0]!='ul'):flush()
            lst=lst or ['ul',[]];lst[1].append(s_[2:]);continue
        if m:
            if para or (lst and lst[0]!='ol'):flush()
            lst=lst or ['ol',[]];lst[1].append(m.group(2));continue
        if lst:flush()
        para.append(s_.strip())
    flush();return '\n'.join(out),toc
def parse(path):
    raw=open(path,encoding='utf-8').read();_,fm,body=raw.split('---',2)
    meta={'faq':[],'sources':[],'scheda':[]};cur=None
    for ln in fm.strip().split('\n'):
        if ln.startswith('faq:'):cur='faq';continue
        if ln.startswith('sources:'):cur='sources';continue
        if ln.startswith('scheda:'):cur='scheda';continue
        if cur=='scheda' and ln.startswith('- '):
            k,v=ln[2:].split('::',1);meta['scheda'].append((k.strip(),v.strip()));continue
        if cur=='sources' and ln.startswith('- '):
            n,u=ln[2:].split('::',1);meta['sources'].append((n.strip(),u.strip()));continue
        if cur=='faq' and ln.startswith('- '):
            q,a=ln[2:].split('::',1);meta['faq'].append((q.strip(),a.strip()));continue
        k,v=ln.split(':',1);meta[k.strip()]=v.strip()
    meta['tags']=[x.strip() for x in meta.get('tags','').split(',') if x.strip()];meta['slug']=os.path.basename(path)[:-3];meta.setdefault('id',meta['slug']);meta['body'],meta['toc']=md(body);return meta
def _fm(path):
    _,fm,_b=open(path,encoding='utf-8').read().split('---',2);d={}
    for ln in fm.strip().split('\n'):
        if ':' in ln and not ln.startswith(('-',' ')):k,v=ln.split(':',1);d[k.strip()]=v.strip()
    d['slug']=os.path.basename(path)[:-3];d.setdefault('id',d['slug']);return d
OTHERS=[_fm(p) for p in glob.glob(('blog-src/*.md') if EN else 'blog-src/en/*.md')]
posts=sorted([parse(p) for p in glob.glob(SRC+'/*.md')],key=lambda p:(p['date'],p['slug']),reverse=True)
# ---------- cover generativa ----------
exec(open('illus.py').read())
def cover(p,big=False):
    if p['slug'] in ILLS:return ILLS[p['slug']]()
    return cover_gen(p)
def cover_gen(p):
    r=random.Random(int(hashlib.md5(p['slug'].encode()).hexdigest()[:8],16))
    pts=[(14,150-r.randint(0,30))]
    for i in range(1,6):pts.append((14+i*54+r.randint(-8,8),r.randint(34,150)))
    d='M'+' '.join(f'{x},{y}' for x,y in pts[:1])
    for i in range(1,len(pts)):
        x0,y0=pts[i-1];x1,y1=pts[i];cx=(x0+x1)/2;d+=f' C{cx:.0f},{y0} {cx:.0f},{y1} {x1},{y1}'
    cont=''.join(f'<ellipse cx="{r.randint(60,240)}" cy="{r.randint(30,150)}" rx="{rx}" ry="{int(rx*.55)}" />' for rx in (30,52,76,102) )
    dots=''.join(f'<circle cx="{x}" cy="{y}" r="{4 if i in(0,5) else 2.6}" fill="{"#fff" if i==5 else "#ff8a5b"}"/>' for i,(x,y) in enumerate(pts))
    return f'''<svg class="cov" viewBox="0 0 300 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="g{p["slug"][:6]}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0e3340"/><stop offset="1" stop-color="#06161e"/></linearGradient></defs><rect width="300" height="180" fill="url(#g{p["slug"][:6]})"/><g fill="none" stroke="rgba(234,242,240,.10)" stroke-width="1">{cont}</g><path d="{d}" fill="none" stroke="#ff6b3d" stroke-width="3" stroke-linecap="round" style="filter:drop-shadow(0 0 5px rgba(255,107,61,.8))"/>{dots}</svg>'''
SCR_ART=r"""<script>(function(){var bar=document.querySelector('.prog b'),links=[].slice.call(document.querySelectorAll('#route a')),secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))}),t=0,rt=document.getElementById('route');
function u(){t=0;var h=document.documentElement,m=h.scrollHeight-innerHeight,v=m>0?Math.min(100,Math.max(0,scrollY/m*100)):0;bar.style.setProperty('--p',v+'%');var cur=-1;secs.forEach(function(s,i){if(s&&s.getBoundingClientRect().top<innerHeight*.35)cur=i});links.forEach(function(a,i){a.parentNode.className=i===cur?'on':(i<cur?'done':'')});if(rt)rt.style.setProperty('--n',cur<0?0:(cur+1)/links.length)}
addEventListener('scroll',function(){t||(t=requestAnimationFrame(u))},{passive:true});u();
var rv=[].slice.call(document.querySelectorAll('.body>*,.tldr,.scheda,.faq,.fonti,.mid,.join,.next,.tappe li'));document.documentElement.classList.add('js');rv.forEach(function(e){if(!e.classList.contains('in'))e.classList.add('rv')});
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.1});rv.forEach(function(e){io.observe(e)})}else rv.forEach(function(e){e.classList.add('in')});
var cp=document.getElementById('cp');if(cp)cp.addEventListener('click',function(){var d={title:document.title,url:location.href.split('#')[0]};if(navigator.share){navigator.share(d).catch(function(){})}else if(navigator.clipboard){navigator.clipboard.writeText(d.url).then(function(){cp.textContent='Copiato ✓';setTimeout(function(){cp.textContent='Copia link'},1800)})}})})()</script>"""
# ---------- layout ----------
FONTS=''.join(f"@font-face{{font-family:'{f}';font-style:normal;font-weight:{w};font-display:swap;src:url(/fonts/{u}-latin-{w}-normal.woff2) format('woff2')}}" for f,u,ws in [('Bricolage Grotesque','bricolage-grotesque',(500,800)),('Instrument Sans','instrument-sans',(400,500,600)),('IBM Plex Mono','ibm-plex-mono',(400,500))] for w in ws)
CSS=FONTS+'''
:root{color-scheme:dark;--bg:#06161E;--ink:#EAF2F0;--ink2:#9BB5BC;--line:rgba(234,242,240,.14);--line2:rgba(234,242,240,.26);--accent:#FF6B3D;--glow:#FF8A5B;--on-accent:#1A0A04;--gut:clamp(22px,6vw,36px);
--f-display:'Bricolage Grotesque','Arial Narrow',system-ui,sans-serif;--f-body:'Instrument Sans',system-ui,-apple-system,'Segoe UI',sans-serif;--f-mono:'IBM Plex Mono',ui-monospace,Menlo,Consolas,monospace}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:17px;line-height:1.65;overflow-x:clip;-webkit-font-smoothing:antialiased}
a{color:inherit}:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:8px}
.lights{position:fixed;inset:0;z-index:-1;pointer-events:none;overflow:hidden}
.lights i{position:absolute;border-radius:50%;filter:blur(90px);opacity:.5;will-change:transform}
.lights i:nth-child(1){width:46vmax;height:46vmax;left:-14vmax;top:-12vmax;background:radial-gradient(circle,rgba(255,107,61,.38),transparent 65%);animation:fl1 26s ease-in-out infinite alternate}
.lights i:nth-child(2){width:50vmax;height:50vmax;right:-20vmax;top:22vh;background:radial-gradient(circle,rgba(27,120,150,.5),transparent 65%);animation:fl2 32s ease-in-out infinite alternate}
.lights i:nth-child(3){width:34vmax;height:34vmax;left:20vw;bottom:-18vmax;background:radial-gradient(circle,rgba(255,138,91,.22),transparent 65%);animation:fl1 38s ease-in-out infinite alternate-reverse}
@keyframes fl1{to{transform:translate(9vw,8vh) scale(1.15)}}@keyframes fl2{to{transform:translate(-10vw,-6vh) scale(.92)}}
.wrap{max-width:1120px;margin:0 auto;padding-inline:max(var(--gut),env(safe-area-inset-left,0px))}
.bar{position:sticky;top:0;z-index:20;background:rgba(6,22,30,.72);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;align-items:center;justify-content:space-between;gap:14px;height:64px}
.bar img{height:34px;width:auto;display:block}
.nav{display:flex;gap:8px;align-items:center}
.pill{font-family:var(--f-mono);font-size:.74rem;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;border:1px solid var(--line2);padding:9px 14px;border-radius:999px;background:rgba(6,22,30,.5);transition:border-color .2s,background .2s}
.pill:hover{border-color:var(--ink)}.pill.hot{background:var(--accent);border-color:var(--accent);color:var(--on-accent);font-weight:500}.pill.hot:hover{background:var(--glow)}
.eyebrow{font-family:var(--f-mono);font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink);display:flex;align-items:center;gap:12px;margin:0 0 18px}
.eyebrow::before{content:"";width:30px;height:2px;background:var(--accent);box-shadow:0 0 10px var(--accent)}
h1,h2,h3{font-family:var(--f-display);font-weight:800;letter-spacing:-.03em;line-height:1.02;margin:0}
.hero{padding-block:clamp(54px,9vw,120px) clamp(28px,4vw,48px)}
.hero h1{font-size:clamp(2.7rem,9.4vw,7.2rem);line-height:.92;letter-spacing:-.045em;max-width:12em;text-wrap:balance}
.hero h1 em{font-style:normal;color:var(--accent);text-shadow:0 0 40px rgba(255,107,61,.5)}
.hero p.lead{font-size:clamp(1.05rem,1.8vw,1.3rem);max-width:34em;margin:22px 0 0;color:var(--ink);text-wrap:pretty}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:34px 0 0}
.chip{font:500 .8rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;padding:9px 15px;border-radius:999px;border:1px solid var(--line2);background:rgba(6,22,30,.5);color:var(--ink);cursor:pointer;transition:all .2s}
.chip:hover{border-color:var(--ink)}.chip[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:var(--on-accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:20px;padding-block:20px 80px}
.card{display:flex;flex-direction:column;text-decoration:none;border:1px solid var(--line);border-radius:20px;overflow:hidden;background:rgba(14,42,51,.55);backdrop-filter:blur(8px);transition:transform .35s cubic-bezier(.2,.8,.2,1),border-color .25s,box-shadow .35s;position:relative}
.card:hover{transform:translateY(-6px);border-color:rgba(255,107,61,.6);box-shadow:0 18px 50px -18px rgba(255,107,61,.35)}
.card .cov{width:100%;aspect-ratio:5/3;display:block}
.card .tx{padding:20px 22px 24px;display:flex;flex-direction:column;gap:10px;flex:1}
.card .tgs{margin-top:2px}.card .cat{font:500 .72rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--glow)}
.card h2{font-size:1.45rem;line-height:1.08}.card p{margin:0;color:var(--ink2);font-size:.96rem;line-height:1.5}
.card .mt{margin-top:auto;font:400 .74rem var(--f-mono);color:var(--ink2);letter-spacing:.06em}
.card.feat{grid-column:1/-1;flex-direction:row}.card.feat .cov{width:50%;aspect-ratio:auto;min-height:320px;object-fit:cover}.card.feat .tx{padding:34px;justify-content:center}.card.feat h2{font-size:clamp(1.8rem,3.4vw,2.8rem)}
@media(max-width:760px){.card.feat{flex-direction:column}.card.feat .cov{width:100%;min-height:0;aspect-ratio:5/3}.card.feat .tx{padding:20px 22px 24px}.card.feat h2{font-size:1.6rem}}
.card[hidden]{display:none}
.join{margin:10px 0 80px;padding:clamp(26px,5vw,52px);border:1px solid rgba(255,107,61,.4);border-radius:24px;background:linear-gradient(135deg,rgba(255,107,61,.16),rgba(14,42,51,.6));display:flex;flex-wrap:wrap;gap:22px;align-items:center;justify-content:space-between}
.join h2{font-size:clamp(1.6rem,3.6vw,2.6rem);max-width:16em}.join p{margin:8px 0 0;color:var(--ink2);max-width:30em}
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--accent);color:var(--on-accent);font:600 1rem var(--f-body);padding:16px 26px;border-radius:999px;text-decoration:none;box-shadow:0 0 30px rgba(255,107,61,.35);transition:transform .2s,background .2s}
.btn:hover{background:var(--glow);transform:translateY(-2px)}
/* articolo */
.art{display:grid;grid-template-columns:minmax(0,1fr);gap:0;max-width:760px;margin:0 auto;padding:clamp(34px,6vw,70px) var(--gut) 20px}
.crumbs{font:400 .76rem var(--f-mono);letter-spacing:.06em;color:var(--ink2);margin:0 0 26px}.crumbs a{text-decoration:none;border-bottom:1px solid var(--line2)}
.art h1{font-size:clamp(2.2rem,6.4vw,4.2rem);line-height:.98;letter-spacing:-.04em;text-wrap:balance}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin:22px 0 0;font:400 .78rem var(--f-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink2)}.meta b{color:var(--glow);font-weight:500}
.art .cov{width:100%;aspect-ratio:5/2.4;border-radius:20px;border:1px solid var(--line);margin:30px 0 8px;display:block}
.toc{margin:26px 0 8px;border:1px solid var(--line);border-radius:16px;padding:6px 20px;background:rgba(14,42,51,.45)}
.toc summary{cursor:pointer;font:500 .78rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;padding:14px 0;color:var(--ink)}
.toc ul{margin:0 0 14px;padding-left:20px;color:var(--ink2)}.toc li::marker{color:var(--accent)}.toc a{text-decoration:none;color:var(--ink)}.toc a:hover{color:var(--glow)}
.body h2{font-size:clamp(1.55rem,3.4vw,2.1rem);margin:2.2em 0 .5em;line-height:1.08;scroll-margin-top:84px}
.body h3{font-size:1.25rem;margin:1.6em 0 .4em}
.body p,.body li{color:#cfdcd9;text-wrap:pretty}.body p{margin:0 0 1.1em}
.body ul,.body ol{padding-left:1.3em;margin:0 0 1.2em}.body li{margin:.35em 0}.body li::marker{color:var(--accent)}
.body strong{color:var(--ink)}.body a{color:var(--glow);text-underline-offset:3px}
.callout{margin:1.6em 0;padding:18px 22px;border-left:3px solid var(--accent);background:linear-gradient(90deg,rgba(255,107,61,.14),transparent);border-radius:0 14px 14px 0;color:var(--ink)}
.src{margin:2em 0 0}.src h2{font-size:1.2rem;margin-bottom:.4em}.src a{color:var(--glow)}.catlink{color:inherit}
.faq{margin:2.4em 0 0}.faq h2{margin-bottom:.6em}
.faq details{border-top:1px solid var(--line);padding:4px 0}.faq details:last-child{border-bottom:1px solid var(--line)}
.faq summary{cursor:pointer;font-weight:600;padding:14px 0;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faq summary::after{content:"+";color:var(--accent);font:500 1.3rem var(--f-mono);transition:transform .2s}.faq details[open] summary::after{transform:rotate(45deg)}
.faq p{margin:0 0 16px;color:var(--ink2)}
.rel{max-width:1120px;margin:40px auto 0;padding-inline:var(--gut)}.rel h2{font-size:1.5rem;margin-bottom:6px}
.prog{position:fixed;z-index:30;left:0;top:0;height:3px;width:100%;pointer-events:none}
.prog b{display:block;height:100%;width:var(--p,0%);background:linear-gradient(90deg,#ff8a5b,#ff6b3d);box-shadow:0 0 14px var(--accent)}
.rail{position:fixed;left:max(14px,calc((100vw - 1120px)/2 - 10px));top:84px;bottom:40px;width:2px;background:var(--line);z-index:5;display:none}
.rail b{position:absolute;left:0;top:0;width:2px;height:var(--p,0%);background:var(--accent);box-shadow:0 0 12px var(--accent)}
.rail i{position:absolute;left:-4px;top:var(--p,0%);width:10px;height:10px;margin-top:-5px;border-radius:50%;background:#fff;box-shadow:0 0 0 3px rgba(255,107,61,.5),0 0 16px var(--accent)}
@media(min-width:1180px){.rail{display:block}}
footer{border-top:1px solid var(--line);background:rgba(6,22,30,.88);color:var(--ink2);font-size:.9rem;margin-top:30px}
footer .wrap{padding-block:34px 44px;display:flex;flex-wrap:wrap;gap:24px 56px;justify-content:space-between}
footer img{height:30px}footer nav{display:flex;flex-direction:column;gap:6px}footer nav b{font:500 .72rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink);margin-bottom:4px}footer a{text-decoration:none}footer a:hover{color:var(--ink)}


.js .rv{opacity:0;transform:translateY(16px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}.js .rv.in{opacity:1;transform:none}
.anc{margin-left:.4em;font-size:.6em;color:var(--ink2);text-decoration:none;opacity:0;transition:opacity .2s}.body h2:hover .anc,.anc:focus{opacity:1}
a.ext,a.int{text-decoration:none;background:linear-gradient(var(--accent),var(--accent)) 0 100%/100% 1.5px no-repeat;color:var(--glow);transition:background-size .3s,color .2s;background-size:0 1.5px;padding-bottom:1px}
a.ext::after{content:"↗";font-size:.8em;margin-left:2px;display:inline-block;transition:transform .25s}
a.ext:hover::after{transform:translate(2px,-2px)}a.ext,a.int{background-size:100% 1.5px;background-position:0 100%;background-repeat:no-repeat;background-image:linear-gradient(rgba(255,138,91,.45),rgba(255,138,91,.45))}
a.ext:hover,a.int:hover{background-image:linear-gradient(var(--accent),var(--accent));color:#fff}
.scheda{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;margin:26px 0 28px;border:1px solid var(--line2);border-radius:18px;overflow:hidden;background:var(--line)}
.scheda div{background:rgba(10,32,41,.92);padding:14px 16px}.scheda dt{font:500 .68rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--glow);margin:0 0 4px}.scheda dd{margin:0;font-size:.95rem;line-height:1.35;color:var(--ink)}
.tappe{list-style:none;margin:1.6em 0;padding:0;position:relative}
.tappe li{position:relative;display:grid;grid-template-columns:92px 1fr;gap:6px 18px;padding:0 0 26px 30px}
.tappe li::before{content:"";position:absolute;left:0;top:.5em;width:12px;height:12px;border-radius:50%;background:var(--bg);border:2px solid var(--accent);z-index:1;transition:background .4s .2s,box-shadow .4s .2s}
.tappe li::after{content:"";position:absolute;left:5px;top:1.4em;bottom:-.5em;width:2px;background:var(--accent);box-shadow:0 0 10px rgba(255,107,61,.6);transform-origin:top;transform:scaleY(0);transition:transform .8s ease .25s}
.tappe li:last-child::after{display:none}
.tappe li.in::before{background:var(--accent);box-shadow:0 0 0 5px rgba(255,107,61,.25),0 0 14px var(--accent)}.tappe li.in::after{transform:scaleY(1)}
.js .tappe li:not(.in) *{opacity:.0}.tappe li *{transition:opacity .6s .15s}.js .tappe li.in *{opacity:1}
.tappe .tm{font:500 .76rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--glow);padding-top:.35em}
.tappe b{font:800 1.12rem var(--f-display);letter-spacing:-.01em;color:var(--ink)}.tappe p{margin:.2em 0 0!important;font-size:.98rem}
@media(max-width:520px){.tappe li{grid-template-columns:1fr}.tappe .tm{padding:0}}
.tip{margin:1.8em 0;padding:20px 24px;border-radius:18px;position:relative;background:rgba(14,42,51,.6);border:1px solid var(--line2);overflow:hidden}
.tip::before{content:"";position:absolute;inset:-1px;border-radius:18px;padding:1.5px;background:conic-gradient(from var(--a,0deg),transparent 0 70%,var(--accent) 85%,transparent 100%);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:spin 6s linear infinite;pointer-events:none}
@property --a{syntax:"<angle>";initial-value:0deg;inherits:false}@keyframes spin{to{--a:360deg}}
.tip b{font:500 .72rem var(--f-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--glow)}.tip p{margin:6px 0 0!important;color:var(--ink)!important}
.fonti{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
a.fonte{position:relative;display:grid;gap:4px;padding:18px 44px 18px 20px;margin:1.2em 0 0;border:1px solid var(--line2);border-radius:16px;text-decoration:none;color:var(--ink)!important;background:rgba(14,42,51,.5);overflow:hidden;transition:transform .3s,border-color .25s,box-shadow .3s}
.fonti a.fonte{margin:0}
a.fonte::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--accent);transform:scaleY(0);transform-origin:top;transition:transform .35s}
a.fonte:hover{transform:translateY(-3px);border-color:rgba(255,107,61,.6);box-shadow:0 14px 36px -16px rgba(255,107,61,.4)}a.fonte:hover::before{transform:scaleY(1)}
a.fonte .dom{font:400 .7rem var(--f-mono);letter-spacing:.08em;color:var(--glow)}a.fonte b{font:800 1.05rem var(--f-display)}a.fonte p{margin:0!important;font-size:.9rem;color:var(--ink2)!important}
a.fonte i{position:absolute;right:18px;top:50%;transform:translateY(-50%);font-style:normal;font-size:1.3rem;color:var(--accent);transition:transform .3s}a.fonte:hover i{transform:translate(4px,-58%)}
@media(prefers-reduced-motion:reduce){.js .rv{opacity:1;transform:none}.js .tappe li:not(.in) *{opacity:1}.tappe li::after{transform:scaleY(1)}.tip::before{animation:none}}
@view-transition{navigation:auto}
.skip{position:absolute;left:-999px;top:8px;background:var(--accent);color:var(--on-accent);padding:10px 16px;border-radius:10px;z-index:100;font-weight:600}.skip:focus{left:12px}
.tools{position:relative;padding-bottom:6px}
.sbox{display:flex;align-items:center;gap:12px;border:1px solid var(--line2);border-radius:999px;padding:0 20px;height:58px;background:rgba(14,42,51,.6);backdrop-filter:blur(10px);transition:border-color .2s,box-shadow .2s;max-width:680px}
.sbox:focus-within{border-color:var(--accent);box-shadow:0 0 0 4px rgba(255,107,61,.18)}
.sbox svg{color:var(--ink2);flex:none}.sbox input{flex:1;min-width:0;background:none;border:0;outline:0;color:var(--ink);font:400 1.05rem var(--f-body);height:100%}.sbox input::placeholder{color:var(--ink2)}
.sbox button{background:none;border:0;color:var(--ink2);font-size:1.5rem;cursor:pointer;line-height:1;padding:4px 6px}
.tools .chips{margin:16px 0 0}.chip i{font-style:normal;opacity:.65;margin-left:4px}.chip.sm{padding:7px 12px;font-size:.72rem}.lbl{font:500 .7rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);align-self:center;margin-right:4px}
.cnt{margin:14px 0 0;min-height:1.4em;font:400 .8rem var(--f-mono);letter-spacing:.06em;color:var(--ink2)}
.empty{padding:60px 0 20px;max-width:34em}.empty h2{font-size:1.8rem;margin-bottom:8px}.empty p{color:var(--ink2);margin:0 0 20px}
.tgs{display:flex;flex-wrap:wrap;gap:6px}.tgs em{font:400 .68rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;font-style:normal;color:var(--ink2);border:1px solid var(--line);padding:3px 9px;border-radius:999px}
.artwrap{max-width:1120px;margin:0 auto;padding-inline:max(var(--gut),env(safe-area-inset-left,0px));display:grid;grid-template-columns:minmax(0,1fr)}
.art{max-width:none;margin:0;padding:clamp(30px,5vw,64px) 0 20px;display:block}
.tldr{margin:28px 0 0;padding:22px 24px;border-radius:18px;border:1px solid rgba(255,107,61,.45);background:linear-gradient(135deg,rgba(255,107,61,.16),rgba(14,42,51,.55))}
.tldr b{font:500 .74rem var(--f-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--glow)}.tldr p{margin:8px 0 0;font-size:1.12rem;line-height:1.55;color:var(--ink)}
.cvr{margin:22px 0 4px;height:130px;border-radius:18px;overflow:hidden;border:1px solid var(--line)}.cvr .cov{width:100%!important;height:100%!important;aspect-ratio:auto!important;margin:0!important;border:0!important;border-radius:0!important;display:block}
.toc.mob{margin:22px 0 0}
.mid{margin:2.2em 0;padding:22px 24px;border-radius:18px;border:1px solid var(--line2);background:rgba(14,42,51,.55);display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between}
.mid b{font:500 .72rem var(--f-mono);letter-spacing:.16em;color:var(--glow);width:100%}.mid p{margin:0!important;flex:1;min-width:14em;color:var(--ink)!important;font-weight:500}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:2em 0 0}.tags .tg{font:400 .74rem var(--f-mono);letter-spacing:.06em;text-transform:uppercase;text-decoration:none;border:1px solid var(--line2);padding:6px 12px;border-radius:999px;color:var(--ink)}.tags .tg:hover{border-color:var(--accent);color:var(--glow)}
.next{display:block;margin:30px 0 0;padding:22px 24px;border:1px solid var(--line);border-radius:18px;text-decoration:none;background:rgba(14,42,51,.45);transition:border-color .2s,transform .3s}.next:hover{border-color:var(--accent);transform:translateX(4px)}
.next span{font:500 .72rem var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--glow)}.next b{display:block;font:800 1.35rem/1.15 var(--f-display);letter-spacing:-.02em;margin-top:6px}
.side{display:none}
@media(min-width:1100px){.artwrap{grid-template-columns:minmax(0,720px) 250px;gap:72px;justify-content:center}.side{display:block}.toc.mob{display:none}
.sticky{position:sticky;top:96px;padding-top:clamp(30px,5vw,64px)}.sticky .k{font:500 .72rem var(--f-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink2);margin:0 0 14px}
.route{list-style:none;margin:0;padding:0 0 0 20px;position:relative;font-size:.9rem;line-height:1.35}
.route::before{content:"";position:absolute;left:4px;top:6px;bottom:6px;width:2px;background:var(--line)}
.route::after{content:"";position:absolute;left:4px;top:6px;width:2px;height:calc((100% - 12px)*var(--n,0));background:var(--accent);box-shadow:0 0 10px var(--accent);transition:height .3s}
.route li{position:relative;margin:0 0 12px}.route li::before{content:"";position:absolute;left:-20px;top:.42em;width:10px;height:10px;border-radius:50%;background:var(--bg);border:2px solid var(--line2);box-sizing:border-box;transition:all .25s}
.route li.done::before{border-color:var(--accent);background:var(--accent)}.route li.on::before{border-color:#fff;background:var(--accent);box-shadow:0 0 0 4px rgba(255,107,61,.35),0 0 14px var(--accent)}
.route a{text-decoration:none;color:var(--ink2);transition:color .2s}.route li.on a{color:var(--ink);font-weight:600}.route a:hover{color:var(--glow)}
.share{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}.share button,.share a{font:500 .7rem var(--f-mono);letter-spacing:.08em;text-transform:uppercase;text-decoration:none;color:var(--ink);background:rgba(14,42,51,.6);border:1px solid var(--line2);padding:8px 12px;border-radius:999px;cursor:pointer}.share button:hover,.share a:hover{border-color:var(--accent)}}
@media(min-width:1100px){.rail{display:none!important}}
@media(max-width:480px){.hm{display:none}.pill{padding:9px 12px}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
'''
open(SITE+'/blog.css','w').write(CSS+ILL_CSS+WIDGET_CSS)
LOGO='<img src="/logo.webp" alt="UnniVai" width="120" height="34">'
PAGES=[]
PAIR={}  # it id -> (it_slug,en_slug)
def _pairs():
    its=[_fm(p) for p in glob.glob('blog-src/*.md')];ens=[_fm(p) for p in glob.glob('blog-src/en/*.md')]
    for e in ens:
        for i in its:
            if i['id']==e['id']:PAIR[e['id']]=(i['slug'],e['slug'],i.get('category',''),e.get('category',''))
_pairs()
CATMAP={v[2]:v[3] for v in PAIR.values()}
def W(path,h,alt=None):
    """alt=(it_url,en_url) absolute URLs of the two language versions, or None"""
    if EN:h=finalize_en(h)
    sw=BASE+'/en/blog' if not EN else BASE+'/blog'
    if alt:
        itu,enu=alt;sw=enu if not EN else itu
        h=h.replace('</head>',f'<link rel="alternate" hreflang="it" href="{itu}"><link rel="alternate" hreflang="en" href="{enu}"><link rel="alternate" hreflang="x-default" href="{itu}"></head>',1)
    lab='IT' if EN else 'EN';lg='it' if EN else 'en'
    h=h.replace('</nav></div></header>',f'<a class="pill" lang="{lg}" hreflang="{lg}" href="{sw.replace(BASE,"")}" aria-label="{"Italiano" if EN else "English"}">{lab}</a></nav></div></header>',1)
    os.makedirs(os.path.dirname(path),exist_ok=True);open(path,'w').write(h)
    PAGES.append({'path':path[len(SITE):],'alt':alt,'noindex':'noindex' in h[:3000]})
def head(title,desc,url,img,extra='',typ='website',robots='index,follow,max-image-preview:large'):
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<meta name="robots" content="{robots}"><meta name="theme-color" content="#06161E">
<link rel="icon" type="image/png" href="/favicon.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="Blog UNNIVAI" href="/rss.xml">
<meta property="og:type" content="{typ}"><meta property="og:site_name" content="UNNIVAI"><meta property="og:locale" content="it_IT"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{img}">
<link rel="preload" href="/fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/blog.css">
{extra}</head><body><div class="lights" aria-hidden="true"><i></i><i></i><i></i></div>
<header class="bar"><div class="wrap"><a href="/" aria-label="UNNIVAI, home">{LOGO}</a><nav class="nav" aria-label="Principale"><a class="pill" href="/blog">Blog</a><a class="pill hot" href="/?src=blog#iscriviti">Accesso<span class="hm"> anticipato</span></a></nav></div></header>
'''
def footer():
    return f'''<footer><div class="wrap"><div>{LOGO}<p style="max-width:24em;margin:12px 0 0">Dove vai, in siciliano. Turismo con luoghi veri che si adatta alla tua giornata. Nasce in Sicilia, per tutta l'Italia.</p></div>
<nav aria-label="Blog"><b>Dal blog</b>{''.join(f'<a href="/blog/{p["slug"]}">{esc(p["title"].split(":")[0])}</a>' for p in posts)}</nav>
<nav aria-label="Sito"><b>UNNIVAI</b><a href="/">Home</a><a href="/blog">Blog</a><a href="/?src=blog#iscriviti">Accesso anticipato</a><a href="/autore">Autore</a><a href="/rss.xml">RSS</a><a href="/#privacy">Privacy</a></nav></div></footer></body></html>'''
def ld(o):return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
ORG={"@type":"Organization","name":"UNNIVAI","url":BASE+"/","founder":{"@type":"Person","name":"Ivano Sciretta","url":BASE+"/autore"},"logo":{"@type":"ImageObject","url":BASE+"/icon-512.png"}}
def card(p,feat=False):
    return ('<a class="card'+(' feat' if feat else '')+'" href="/blog/'+p['slug']+'" data-cat="'+html.escape(p['category'])+'" data-s="'+p['slug']+'" data-tags="'+html.escape('|'.join(p['tags']))+'">'+cover(p)+'<div class="tx"><span class="cat">'+esc(p['category'])+'</span><h2>'+esc(p['title'])+'</h2><p>'+esc(p['description'])+'</p><span class="tgs">'+''.join('<em>'+esc(t)+'</em>' for t in p['tags'][:3])+'</span><span class="mt">'+dfmt(p['date'])+' · '+p['read']+' min di lettura</span></div></a>')
SCR_IDX="""<script>(function(){var b=document.querySelectorAll('.chip'),c=document.querySelectorAll('#grid .card');b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.setAttribute('aria-pressed',y===x)});var f=x.dataset.f;c.forEach(function(k){k.hidden=!!f&&k.dataset.cat!==f;k.classList.toggle('feat',!f&&k===c[0])})})})})()</script>"""
SCR_ART_OLD="""<script>(function(){var p=document.querySelector('.prog b'),r=document.querySelector('.rail'),t=0;function u(){t=0;var h=document.documentElement,m=h.scrollHeight-innerHeight,v=m>0?Math.min(100,Math.max(0,scrollY/m*100)):0;p.style.setProperty('--p',v+'%');r.style.setProperty('--p',v+'%')}addEventListener('scroll',function(){t||(t=requestAnimationFrame(u))},{passive:true});u()})()</script>"""
CINTRO_EN={'Lecce':'Lecce, the baroque city of the Salento: walking itineraries with hours, tickets and the sweet stops checked on official sources.','Catania':'Catania between lava, baroque and fresh fish: what to do in the sun, in the rain and on foot, with hours and distances checked.','Syracuse':'Syracuse and Ortigia: an island to explore on foot, between market, sea and alleys. Itineraries built around the time of day.','Rome':'Rome organised by area, not by lists: itineraries of one or more days that do not make you cross the city back and forth.','Travel and AI':'How to use artificial intelligence to plan a trip, and how to tell when a generated itinerary holds up or makes things up.'}
CINTRO={'Lecce':"Lecce, la città del barocco nel Salento: itinerari a piedi con orari, biglietti e soste dolci verificati sulle fonti ufficiali.",'Catania':"Catania tra lava, barocco e pesce fresco: cosa fare con il sole, con la pioggia e a piedi, con orari e distanze controllati.",'Siracusa':"Siracusa e Ortigia: un'isola da girare a piedi, tra mercato, mare e vicoli. Itinerari pensati per l'ora del giorno.",'Roma':"Roma organizzata per zone, non per elenchi: itinerari di uno o più giorni che non ti fanno attraversare la città avanti e indietro.",'Turismo e AI':"Come usare l'intelligenza artificiale per pianificare un viaggio, e come capire quando un itinerario generato regge o inventa."}
# ---------- indice ----------
cats=[];[cats.append(p['category']) for p in posts if p['category'] not in cats]
tags=[];[tags.append(t) for p in posts for t in p['tags'] if t not in tags]
idx_desc=L("Guide e itinerari per viaggiare in Italia con luoghi veri: cosa fare quando piove, giri a piedi e turismo con l'intelligenza artificiale.","Guides and itineraries for travelling in Italy through real places: what to do when it rains, walking routes and travel with artificial intelligence.")
def plain(h):return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',h)).replace('&amp;','&').replace('&#x27;',"'").strip()
open(SITE+P+'/blog/search.json','w').write(json.dumps([{"s":p['slug'],"t":p['title'],"d":p['description'],"c":p['category'],"g":p['tags'],"x":plain(p['body'])[:2500]} for p in posts],ensure_ascii=False))
ICON_S='<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
idx=head(L('Blog UNNIVAI · Itinerari, turismo e intelligenza artificiale','UNNIVAI Blog · Italy itineraries, travel and AI'),idx_desc,BASE+'/blog',BASE+'/blog/og/index.png',
  ld({"@context":"https://schema.org","@type":"Blog","name":"Blog UNNIVAI","url":BASE+"/blog","description":idx_desc,"inLanguage":"it","publisher":ORG,"blogPost":[{"@type":"BlogPosting","headline":p['title'],"url":f"{BASE}/blog/{p['slug']}","datePublished":p['date']} for p in posts]})+
  ld({"@context":"https://schema.org","@type":"WebSite","name":"UNNIVAI Blog","url":BASE+"/blog","potentialAction":{"@type":"SearchAction","target":BASE+"/blog?q={search_term_string}","query-input":"required name=search_term_string"}})+
  ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"UNNIVAI","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":BASE+"/blog"}]}))
idx+=f"""<main id="main"><section class="wrap hero"><p class="eyebrow">Il blog di UNNIVAI</p><h1>Dove andare, e come andarci <em>bene.</em></h1>
<p class="lead">Itinerari con luoghi veri, piani B per la pioggia e idee per viaggiare senza buttare la giornata. Dalla Sicilia, per tutta l'Italia.</p></section>
<section class="wrap tools" aria-label="Cerca e filtra"><div class="sbox">{ICON_S}<input id="q" type="search" placeholder="Cerca: Catania, pioggia, a piedi…" aria-label="Cerca negli articoli" autocomplete="off" enterkeyhint="search"><button type="button" id="qx" aria-label="Cancella" hidden>×</button></div>
<div class="chips" role="group" aria-label="Città e argomenti"><button class="chip" aria-pressed="true" data-k="c" data-f="">Tutti <i>{len(posts)}</i></button>{''.join(f'<button class="chip" aria-pressed="false" data-k="c" data-f="{html.escape(c)}">{esc(c)} <i>{sum(1 for p in posts if p["category"]==c)}</i></button>' for c in cats)}</div>
<div class="chips tg" role="group" aria-label="Contesto"><span class="lbl">Contesto</span>{''.join(f'<button class="chip sm" aria-pressed="false" data-k="g" data-f="{html.escape(t)}">{esc(t)}</button>' for t in tags)}</div>
<p class="cnt" id="cnt" role="status" aria-live="polite"></p></section>
<section class="wrap"><div class="browse" id="browse"><h2>Per città</h2><div class="bc">{''.join(f'<a href="/blog/categoria/{slugify(c)}"><b>{esc(c)}</b><span>{sum(1 for p in posts if p["category"]==c)} guide · {esc((CINTRO_EN if EN else CINTRO).get(c,"")[:70])}…</span></a>' for c in cats)}</div>
<h2>Per situazione</h2><div class="bt">{''.join(f'<a href="/blog/tema/{slugify(t)}">{esc(t)}</a>' for t in tags)}<a href="/blog/domande">Tutte le domande →</a></div></div>
<h2 class="gh" style="font:500 .74rem var(--f-mono);letter-spacing:.16em;text-transform:uppercase;color:var(--glow);margin:8px 0 14px">Tutti gli articoli</h2><div class="grid" id="grid">{card(posts[0],True)}{''.join(card(p) for p in posts[1:])}</div>
<div class="empty" id="empty" hidden><h2>Nessun articolo ancora su questo.</h2><p>Dimmi cosa cerchi: scrivo le guide in base alle richieste. Intanto entra nella lista d'attesa e ti avviso quando UNNIVAI arriva.</p><a class="btn" href="/?src=blog-cerca#iscriviti">Entra tra i primi</a></div>
<div class="join"><div><h2>Il percorso giusto, che si adatta alla tua giornata.</h2><p>UNNIVAI costruisce l'itinerario con luoghi veri e lo riscrive quando cambia il tempo. Entra tra i primi.</p></div><a class="btn" href="/?src=blog-index#iscriviti">Entra tra i primi</a></div></section></main>"""
SCR_IDX=r"""<script>(function(){var N=function(s){return(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')},q=document.getElementById('q'),qx=document.getElementById('qx'),cnt=document.getElementById('cnt'),em=document.getElementById('empty'),cards=[].slice.call(document.querySelectorAll('#grid .card')),chips=[].slice.call(document.querySelectorAll('.chip')),st={c:'',g:''},idx=null,load=null;
function get(){if(idx)return Promise.resolve(idx);return load||(load=fetch('/blog/search.json').then(function(r){return r.json()}).then(function(j){idx={};j.forEach(function(x){idx[x.s]=N([x.t,x.d,x.c,x.g.join(' '),x.x].join(' '))});return idx}).catch(function(){idx={};return idx}))}
function run(){get().then(function(I){var t=N(q.value).split(/\s+/).filter(Boolean),n=0,any=!!(t.length||st.c||st.g);cards.forEach(function(k,i){var s=k.dataset.s,ok=(!st.c||k.dataset.cat===st.c)&&(!st.g||k.dataset.tags.split('|').indexOf(st.g)>-1)&&t.every(function(w){return(I[s]||'').indexOf(w)>-1});k.hidden=!ok;if(ok)n++;k.classList.toggle('feat',!any&&i===0)});em.hidden=n>0;document.getElementById('browse').hidden=any;cnt.textContent=any?(n+(n===1?' articolo':' articoli')):'';qx.hidden=!q.value})}
chips.forEach(function(b){b.addEventListener('click',function(){var k=b.dataset.k,on=b.getAttribute('aria-pressed')==='true';chips.forEach(function(o){if(o.dataset.k===k)o.setAttribute('aria-pressed','false')});if(k==='c'||!on){b.setAttribute('aria-pressed','true');st[k]=b.dataset.f}else{st[k]='';}if(k==='g'&&on){} if(k==='c'&&!b.dataset.f)st.c='';run()})});
q.addEventListener('input',run);q.addEventListener('focus',get);qx.addEventListener('click',function(){q.value='';q.focus();run()});
document.addEventListener('keydown',function(e){if(e.key==='/'&&document.activeElement!==q&&!/input|textarea/i.test(document.activeElement.tagName)){e.preventDefault();q.focus()}});
try{var p=new URLSearchParams(location.search).get('q');if(p){q.value=p;}}catch(e){}run()})()</script>"""
idx+=SCR_IDX+footer()
W(SITE+P+'/blog/index.html',idx,(BASE+'/blog',BASE+'/en/blog'))
# ---------- articoli ----------
def related(p):
    sc=lambda q:(q['category']==p['category'])*3+len(set(q['tags'])&set(p['tags']))
    return sorted([q for q in posts if q is not p],key=lambda q:-sc(q))[:3]
for i,p in enumerate(posts):
    url=f"{BASE}/blog/{p['slug']}";img=f"{BASE}/blog/og/{p['slug']}.png"
    faq=''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in p['faq'])
    graph=[{"@context":"https://schema.org","@type":"BlogPosting","headline":p['title'],"description":p['description'],"image":img,"datePublished":p['date'],"dateModified":p.get('updated',p['date']),"inLanguage":"it","keywords":", ".join(p['tags']),"author":{"@type":"Person","name":"Ivano Sciretta","url":BASE+"/autore"},"publisher":ORG,"mainEntityOfPage":url,"articleSection":p['category'],"about":{"@type":"Place","name":p['category']},"isPartOf":{"@type":"Blog","name":"Blog UNNIVAI","url":BASE+"/blog"},"speakable":{"@type":"SpeakableSpecification","cssSelector":[".tldr","h1"]},"wordCount":len(plain(p['body']).split()),"timeRequired":"PT"+str(max(1,round(len(plain(p['body']).split())/200)))+"M","isAccessibleForFree":True},
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"UNNIVAI","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":BASE+"/blog"},{"@type":"ListItem","position":3,"name":p['category'],"item":f"{BASE}/blog/categoria/{slugify(p['category'])}"},{"@type":"ListItem","position":4,"name":p['title'],"item":url}]}]
    if p['faq']:graph.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p['faq']]})
    body=p['body'];m=re.search(r'<aside class="callout">(.*?)</aside>',body,re.S);tl=''
    if m:
        tl=re.sub(r'^<strong>[^<]*</strong>\s*','',m.group(1));body=body.replace(m.group(0),'',1)
    hs=[x.start() for x in re.finditer(r'<h2 ',body)]
    if len(hs)>=4:
        k=hs[len(hs)//2+1] if len(hs)>4 else hs[len(hs)//2]
        body=body[:k]+f'<div class="mid"><b>UNNIVAI</b><p>Vuoi un percorso così, pronto e che si adatta al tempo?</p><a class="pill hot" href="/?src=blog-mid-{p["slug"][:20]}#iscriviti">Entra tra i primi</a></div>'+body[k:]
    toc_items=''.join(f'<li><a href="#{a}">{inline(t)}</a></li>' for a,t in p['toc'])
    tagh=''.join(f'<a class="tg" href="/blog?q={html.escape(t)}">{esc(t)}</a>' for t in p['tags'])
    nxt=posts[(i+1)%len(posts)]
    h=head(p['title'],p['description'],url,img,''.join(ld(g) for g in graph)+f'<meta property="article:published_time" content="{p["date"]}"><meta property="article:section" content="{html.escape(p["category"])}">','article')
    h+=f"""<a class="skip" href="#main">Vai al contenuto</a><div class="prog" aria-hidden="true"><b></b></div>
<div class="artwrap"><main id="main"><article class="art"><p class="crumbs"><a href="/">UNNIVAI</a> / <a href="/blog">Blog</a> / <a href="/blog/categoria/{slugify(p['category'])}">{esc(p['category'])}</a></p>
<h1>{esc(p['title'])}</h1><p class="meta"><span><b>{esc(p['category'])}</b></span><span>{p['read']} min</span><span>{L('di','by')} <a href="/autore">Ivano Sciretta</a></span><span>{L('Verificato il','Checked on')} {dfmt(p.get('updated',p['date']))}</span></p>
<div class="hero-ill">{cover(p)}</div>{('<div class="tldr"><b>Risposta in breve</b><p>'+tl+'</p></div>') if tl else ''}
{('<dl class="scheda">'+''.join('<div><dt>'+esc(k)+'</dt><dd>'+esc(v)+'</dd></div>' for k,v in p['scheda'])+'</dl>') if p['scheda'] else ''}<details class="toc mob"><summary>In questo articolo</summary><ul>{toc_items}</ul></details>
<div class="body">{body}</div>
{('<section class="faq"><h2>Domande frequenti</h2>'+faq+'</section>') if faq else ''}
{('<section class="src"><h2>Fonti ufficiali</h2><div class="fonti">'+''.join('<a class="fonte" href="'+u+'" rel="noopener" target="_blank"><span class="dom">'+esc(dom(u))+'</span><b>'+esc(n)+'</b><i aria-hidden="true">↗</i></a>' for n,u in p['sources'])+'</div></section>') if p['sources'] else ''}
<div class="tags">{tagh}</div>
<div class="join" style="margin:36px 0 0"><div><h2>Entra tra i primi.</h2><p>Dimmi dove vuoi andare: ti scrivo quando UNNIVAI arriva nella tua città. Nessuna newsletter prima.</p></div><a class="btn" href="/?src=blog-{p['slug'][:24]}#iscriviti">Iscriviti</a></div>
<a class="next" href="/blog/{nxt['slug']}"><span>Prossimo articolo</span><b>{esc(nxt['title'])}</b></a></article></main>
<aside class="side" aria-label="Indice e condivisione"><div class="sticky"><p class="k">In questo articolo</p><ol class="route" id="route">{toc_items}</ol>
<div class="share"><button type="button" id="cp">Copia link</button><a href="https://wa.me/?text={html.escape(p['title'])}%20{url}" rel="noopener" target="_blank">WhatsApp</a><a href="https://www.linkedin.com/sharing/share-offsite/?url={url}" rel="noopener" target="_blank">LinkedIn</a></div></div></aside></div>
<section class="rel"><h2>Continua a leggere</h2><div class="grid">{''.join(card(q) for q in related(p))}</div></section>"""
    h+=SCR_ART+WIDGET_JS+footer()
    pr=PAIR.get(p['id']);alt=(f"{BASE}/blog/{pr[0]}",f"{BASE}/en/blog/{pr[1]}") if pr else None
    W(f"{SITE}{P}/blog/{p['slug']}/index.html",h,alt)
# ---------- sitemap + rss ----------
urls=[(BASE+'/','2026-10-28','1.0'),(BASE+'/blog',posts[0]['date'],'0.9')]+[(f"{BASE}/blog/{p['slug']}",p['date'],'0.8') for p in posts]
open(SITE+P+'/rss.xml','w').write('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Blog UNNIVAI</title><link>'+BASE+'/blog</link><description>'+html.escape(idx_desc)+'</description><language>'+LG+'</language>'+''.join(f"<item><title>{html.escape(p['title'])}</title><link>{BASE}/blog/{p['slug']}</link><guid>{BASE}/blog/{p['slug']}</guid><pubDate>{p['date']}</pubDate><description>{html.escape(p['description'])}</description></item>" for p in posts)+'</channel></rss>')
# ---------- OG ----------
og=''
for name,title,cat in ([('index_en','Where to go, and how to get there well.','UNNIVAI Blog')] if EN else [('index','Dove andare, e come andarci bene.','Blog UNNIVAI')])+[(p['slug'],p['title'],p['category']) for p in posts]:
    pp=next((p for p in posts if p['slug']==name),posts[0])
    open(f'/tmp/og_{name}.html','w').write(f'''<!doctype html><meta charset=utf-8><style>{FONTS}body{{margin:0;width:1200px;height:630px;background:#06161e;color:#eaf2f0;font-family:'Instrument Sans';position:relative;overflow:hidden}}.c{{position:absolute;inset:0;opacity:.95}}.c svg{{width:100%;height:100%}}.v{{position:absolute;inset:0;background:linear-gradient(90deg,#06161e 38%,rgba(6,22,30,.2))}}.t{{position:absolute;left:70px;top:70px;right:420px}}.k{{font:500 24px 'IBM Plex Mono';letter-spacing:.16em;text-transform:uppercase;color:#ff8a5b}}h1{{font:800 74px/.98 'Bricolage Grotesque';letter-spacing:-.04em;margin:26px 0 0}}.u{{position:absolute;left:70px;bottom:56px;font:800 38px 'Bricolage Grotesque'}}.u i{{color:#ff6b3d;font-style:normal}}</style><div class=c>{cover(pp)}</div><div class=v></div><div class=t><div class=k>{html.escape(cat)}</div><h1>{html.escape(title)}</h1></div><div class=u>UNNIVAI<i>.</i></div>''')
os.makedirs(SITE+'/blog/og',exist_ok=True)
print('posts',len(posts))

# ---------- link blog nella home ----------
tp=open(SITE+'/index.template.html').read()
links='<ul class="blogl"><li><b>Dal blog</b></li><li><a href="/blog">Tutti gli articoli</a></li>'+''.join('<li><a href="/blog/categoria/'+slugify(c)+'">'+esc(c)+'</a></li>' for c in cats)+''.join('<li><a href="/blog/'+p['slug']+'">'+esc(p['title'].split(':')[0])+'</a></li>' for p in posts)+'</ul>'
if not EN:
    assert '<!--BLOGLINKS-->' in tp
    open(SITE+'/index.template.html','w').write(tp.replace('<!--BLOGLINKS-->',links))

# ---------- pagine categoria (hub tematici) ----------
for c in cats:
    cs=slugify(c);ps=[p for p in posts if p['category']==c];url=f"{BASE}/blog/categoria/{cs}"
    d=L(f"Tutti gli articoli UNNIVAI su {c}: itinerari, consigli pratici e idee per organizzare il viaggio con luoghi veri.",f"All UNNIVAI articles on {c}: itineraries, practical tips and ideas for planning a trip through real places.")
    h=head(f"{c} · Blog UNNIVAI",d,url,BASE+'/blog/og/index.png',ld({"@context":"https://schema.org","@type":"CollectionPage","name":c,"url":url,"description":d,"isPartOf":{"@type":"Blog","url":BASE+"/blog"}})+ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"UNNIVAI","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":BASE+"/blog"},{"@type":"ListItem","position":3,"name":c,"item":url}]}))
    h+=f'<main><section class="wrap hero"><p class="eyebrow">Argomento</p><h1>{esc(c)}</h1><p class="lead">{esc((CINTRO_EN if EN else CINTRO).get(c,d))}</p></section><section class="wrap"><div class="grid">'+''.join(card(p) for p in ps)+'</div></section></main>'+footer()
    itc=[k for k,v in CATMAP.items() if v==c] if EN else [c]
    enc=CATMAP.get(c) if not EN else c
    alt=(f"{BASE}/blog/categoria/{slugify(itc[0])}",f"{BASE}/en/blog/category/{slugify(enc)}") if (itc and enc) else None
    W(f"{SITE}{P}/blog/{DIRC}/{cs}/index.html",h,alt)
# ---------- tag hubs ----------
TAGHUB=[]
for t in tags:
    ts=slugify(t);ps=[p for p in posts if t in p['tags']];url=f"{BASE}/blog/tema/{ts}";ix=len(ps)>=2
    d=L(f"Guide UNNIVAI per situazione: {t}. {len(ps)} articoli con itinerari e consigli pratici.",f"UNNIVAI guides by situation: {t}. {len(ps)} articles with itineraries and practical tips.")
    h=head(L(f"{t} · Guide UNNIVAI",f"{t} · UNNIVAI guides"),d,url,BASE+'/blog/og/index.png',ld({"@context":"https://schema.org","@type":"CollectionPage","name":t,"url":url,"description":d,"isPartOf":{"@type":"Blog","url":BASE+"/blog"}}),robots='index,follow,max-image-preview:large' if ix else 'noindex,follow')
    h+=f'<main><section class="wrap hero"><p class="eyebrow">Per situazione</p><h1>{esc(t)}</h1><p class="lead">{esc(d)}</p></section><section class="wrap"><div class="grid">'+''.join(card(p) for p in ps)+'</div></section></main>'+footer()
    W(f"{SITE}{P}/blog/{DIRT}/{ts}/index.html",h,None)
    if ix:TAGHUB.append(url)
# ---------- domande ----------
qs=[(q,a,p) for p in posts for q,a in p['faq']]
url=BASE+'/blog/domande';d=L("Le domande più frequenti su viaggiare in Italia, itinerari, pioggia e pianificazione con l'AI, con risposte brevi e link alle guide.","The most frequent questions about travelling in Italy, itineraries, rain and planning with AI, with short answers and links to the guides.")
h=head(L("Domande frequenti sul viaggio · UNNIVAI","Travel questions answered · UNNIVAI"),d,url,BASE+'/blog/og/index.png',ld({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a,_ in qs]}))
h+='<main><section class="wrap hero"><p class="eyebrow">Domande</p><h1>Domande che ci fanno <em>davvero.</em></h1><p class="lead">'+esc(d)+'</p></section><section class="wrap qa">'+''.join(f'<details open><summary>{esc(q)}</summary><p>{inline(a)}</p><a href="/blog/{p["slug"]}">{L("Leggi","Read")}: {esc(p["title"].split(":")[0])} →</a></details>' for q,a,p in qs)+'</section></main>'+footer()
W(SITE+P+f'/blog/{DIRQ}/index.html',h,(BASE+'/blog/domande',BASE+'/en/blog/questions'))
# ---------- 404 ----------
h=head("Pagina non trovata · UNNIVAI","Questa pagina non esiste più o non è mai esistita.",BASE+'/404',BASE+'/og.png',robots='noindex,follow')
h+='<main><section class="wrap hero"><p class="eyebrow">Errore 404</p><h1>Strada <em>sbagliata.</em></h1><p class="lead">Questa pagina non c\'è. Succede anche ai migliori navigatori. Riparti da qui.</p><p><a class="btn" href="/blog">Vai al blog</a> <a class="pill" href="/">Home</a></p></section><section class="wrap"><div class="grid">'+''.join(card(p) for p in posts)+'</div></section></main>'+footer()
if not EN:open(SITE+'/404.html','w').write(h)
# ---------- autore ----------
adesc=L("Ivano Sciretta, fondatore di UNNIVAI: costruisce prodotti digitali con l'intelligenza artificiale. Autore del blog su turismo e itinerari.","Ivano Sciretta, founder of UNNIVAI: he builds digital products with artificial intelligence. Author of the blog on travel and itineraries.")
ah=head(L('Ivano Sciretta · Autore del blog UNNIVAI','Ivano Sciretta · Author of the UNNIVAI blog'),adesc,BASE+'/autore',BASE+'/og.png',ld({"@context":"https://schema.org","@type":"ProfilePage","mainEntity":{"@type":"Person","name":"Ivano Sciretta","url":BASE+"/autore","jobTitle":"Fondatore di UNNIVAI","worksFor":{"@type":"Organization","name":"UNNIVAI","url":BASE+"/"},"sameAs":["https://www.linkedin.com/in/ivano-sciretta"]}}))
ah+=f'''<main><article class="art"><p class="crumbs"><a href="/">UNNIVAI</a> / Autore</p><h1>Ivano Sciretta</h1><p class="meta"><span><b>Fondatore di UNNIVAI</b></span><span>Roma · Sicilia</span></p>
<div class="body" style="margin-top:28px">{L("<p>Costruisco piattaforme digitali e prodotti con l'intelligenza artificiale. UNNIVAI nasce da un'idea semplice: il turismo funziona quando il percorso è fatto di luoghi veri e si adatta alla giornata, non quando è un elenco generico.</p><p>In questo blog scrivo itinerari e guide pensati per chi viaggia in Italia, a partire dalla Sicilia. Ogni articolo riporta la data dell'ultima verifica e rimanda alle fonti ufficiali per orari e prenotazioni, che cambiano spesso.</p>","<p>I build digital platforms and products with artificial intelligence. UNNIVAI starts from a simple idea: travel works when the route is made of real places and adapts to your day, not when it is a generic list.</p><p>On this blog I write itineraries and guides for people travelling in Italy, starting from Sicily. Every article shows the date of its last check and points to official sources for opening hours and bookings, which change often.</p>")}<p><a href="https://www.linkedin.com/in/ivano-sciretta" rel="me noopener">Profilo LinkedIn</a> · <a href="/blog">Tutti gli articoli</a></p></div></article></main>'''+footer()
W(SITE+P+f'/{DIRA}/index.html',ah,(BASE+'/autore',BASE+'/en/author'))

# ---------- dump per build_seo.py ----------
json.dump({'pages':PAGES,'posts':[{'slug':p['slug'],'title':p['title'],'desc':p['description'],'date':p['date'],'updated':p.get('updated',p['date']),'cat':p['category'],'text':re.sub(r'\n\s*\n+','\n\n',re.sub(r'<[^>]+>','',re.sub(r'</(p|h2|li|aside|dd|div)>','\n',p['body'])).replace('&amp;','&').replace('&#x27;',"'"))} for p in posts]},open(f'seo_{LG}.json','w'),ensure_ascii=False)

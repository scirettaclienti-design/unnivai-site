import random
def _wrap(k,body,defs=''):
    return f'<svg class="cov ill" viewBox="0 0 600 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false"><defs>{defs}<linearGradient id="{k}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b2d3a"/><stop offset=".62" stop-color="#0e3a47"/><stop offset="1" stop-color="#16485a"/></linearGradient><radialGradient id="{k}g"><stop offset="0" stop-color="#ff8a5b" stop-opacity=".85"/><stop offset="1" stop-color="#ff6b3d" stop-opacity="0"/></radialGradient><linearGradient id="{k}o" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb08f"/><stop offset="1" stop-color="#ff6b3d"/></linearGradient></defs><rect width="600" height="300" fill="url(#{k}s)"/>{body}</svg>'
def _stars(k,n=26,seed=1):
    r=random.Random(seed);return '<g class="stg" fill="#eaf2f0">'+''.join(f'<circle class="tw" style="animation-delay:-{r.random()*4:.1f}s" cx="{r.randint(8,592)}" cy="{r.randint(6,120)}" r="{r.choice([.6,.8,1,1.2])}" opacity=".7"/>' for _ in range(n))+'</g>'
def _route(d,pts,k):
    dots=''.join(f'<circle cx="{x}" cy="{y}" r="{3.4}" fill="#ff8a5b"/>' for x,y in pts[:-1])+f'<circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="5.5" fill="#fff"/><circle class="pulse" cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="5.5" fill="none" stroke="#ff6b3d" stroke-width="2"/>'
    return f'<path d="{d}" fill="none" stroke="#ff6b3d" stroke-width="7" stroke-linecap="round" opacity=".22" style="filter:blur(4px)"/><path class="rt" d="{d}" fill="none" stroke="#ff6b3d" stroke-width="3" stroke-linecap="round" pathLength="100"/>{dots}'
def catania():
    k='ic';r=random.Random(7)
    rain=''.join(f'<line class="rn" x1="{x}" y1="0" x2="{x-5}" y2="13" style="animation-delay:-{r.random()*1.6:.2f}s;animation-duration:{.9+r.random()*.6:.2f}s"/>' for x in [r.randint(0,600) for _ in range(60)])
    x=-10;roofs=''
    while x<610:
        w=r.randint(22,38);h=r.randint(18,50);roofs+=f'<rect x="{x}" y="{288-h}" width="{w}" height="{h+14}" fill="#04121a"/>'
        for _ in range(r.randint(0,2)):roofs+=f'<rect class="wn" style="animation-delay:-{r.random()*5:.1f}s" x="{x+r.randint(3,w-7)}" y="{288-h+r.randint(5,max(6,h-8))}" width="3" height="4" fill="#ffb08f"/>'
        x+=w+r.randint(0,3)
    dome='<path d="M236 262 a22 22 0 0 1 44 0z" fill="#04121a"/><rect x="256" y="232" width="4" height="10" fill="#04121a"/><rect x="226" y="262" width="64" height="30" fill="#04121a"/>'
    etna='<path d="M60 250 L190 172 L250 134 L296 88 L318 80 L346 84 L372 110 L440 166 L590 250Z" fill="#0a2630"/><path d="M296 88 L318 80 L346 84 L372 110 L350 102 L332 114 L314 100 L300 114Z" fill="#cfe3e6" opacity=".55"/>'
    smoke=''.join(f'<circle class="sm" style="animation-delay:-{i*1.6}s" cx="{326+i*6}" cy="76" r="{14+i*5}" fill="#9fb8bf"/>' for i in range(4))
    route=_route('M16 276 C100 236 160 272 236 246 S 380 214 450 232 S 548 160 578 126',[(16,276),(236,246),(450,232),(578,126)],k)
    return _wrap(k,_stars(k,18,3)+'<circle class="mn" cx="470" cy="70" r="58" fill="#9fc3cf" opacity=".14"/>'+etna+'<circle cx="332" cy="82" r="6" fill="#ff6b3d" class="pulse2"/>'+smoke+roofs+dome+rain+route)
def ortigia():
    k='io';r=random.Random(11)
    waves=''.join(f'<g class="wv" style="animation-duration:{9+i*3}s;animation-delay:-{i*2}s"><path d="M-600 {206+i*22} q 37 -7 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0 t 75 0" fill="none" stroke="rgba(234,242,240,{.20-i*.04:.2f})" stroke-width="1.4"/></g>' for i in range(4))
    refl=''.join(f'<rect class="rf" style="animation-delay:-{i*.5}s" x="{440-30+i*3}" y="{196+i*9}" width="{60-i*6}" height="2" rx="1" fill="#ff8a5b" opacity="{.7-i*.09:.2f}"/>' for i in range(7))
    duomo='<rect x="54" y="118" width="106" height="82" fill="#04121a"/><path d="M54 118 L107 92 L160 118Z" fill="#04121a"/><rect x="166" y="82" width="26" height="118" fill="#04121a"/><path d="M166 82 L179 62 L192 82Z" fill="#04121a"/>'+''.join(f'<rect x="{64+i*20}" y="138" width="5" height="46" fill="#0b2a35"/>' for i in range(5))+'<circle cx="107" cy="112" r="7" fill="#ffb08f" opacity=".75"/>'
    castle='<rect x="468" y="150" width="92" height="50" fill="#04121a"/>'+''.join(f'<rect x="{x}" y="128" width="16" height="72" fill="#04121a"/><rect x="{x-2}" y="124" width="20" height="6" fill="#04121a"/>' for x in(462,544))+''.join(f'<rect x="{468+i*12}" y="145" width="7" height="6" fill="#04121a"/>' for i in range(8))
    boat='<g class="bt"><path d="M300 218 h38 l-8 9 h-22z" fill="#04121a"/><path d="M319 192 v26 M319 192 l18 22 h-18z" fill="#cfe3e6" stroke="#04121a" stroke-width="1"/></g>'
    route=_route('M14 262 C110 238 190 262 290 244 S 440 232 520 214 S 570 190 584 172',[(14,262),(290,244),(520,214),(584,172)],k)
    return _wrap(k,_stars(k,16,5)+'<g class="sun"><circle cx="440" cy="196" r="84" fill="url(#iog)"/><circle cx="440" cy="190" r="34" fill="url(#ioo)"/></g><rect class="nt" width="600" height="300" fill="#020a0f" opacity="0"/><rect y="196" width="600" height="104" fill="#0b3140" opacity=".92"/><g class="rfg">'+refl+'</g>'+waves+duomo+castle+boat+route)
def roma():
    k='ir';r=random.Random(3)
    arches=''
    for row,y in enumerate((158,186,214)):
        for i in range(12):
            x=70+i*22.2;lit=r.random()<.28
            arches+=f'<path d="M{x:.1f} {y+22} v-13 a5 5 0 0 1 10 0 v13z" fill="{"#ffb08f" if lit else "#0b2a35"}" opacity="{.8 if lit else 1}" {"class=\"wn\" style=\"animation-delay:-"+str(round(r.random()*5,1))+"s\"" if lit else ""}/>'
    colo='<path d="M60 250 V150 Q60 144 66 144 H332 Q338 144 338 150 V250Z" fill="#04121a"/><rect x="60" y="144" width="278" height="9" fill="#071c25"/>'+arches
    dome='<rect x="420" y="190" width="100" height="60" fill="#04121a"/><path d="M426 190 a44 44 0 0 1 88 0z" fill="#04121a"/><rect x="466" y="132" width="8" height="14" fill="#04121a"/><circle cx="470" cy="128" r="4" fill="#04121a"/><rect x="460" y="144" width="20" height="8" fill="#04121a"/>'+''.join(f'<rect x="{432+i*17}" y="206" width="5" height="44" fill="#0b2a35"/>' for i in range(5))
    def pine(x,h):return f'<rect x="{x-1.5}" y="{250-h}" width="3" height="{h}" fill="#04121a"/><ellipse cx="{x}" cy="{250-h}" rx="24" ry="9" fill="#04121a"/><ellipse cx="{x-9}" cy="{250-h+5}" rx="14" ry="6" fill="#04121a"/>'
    route=_route('M18 280 C120 248 200 282 290 262 S 430 250 500 262 S 566 226 584 196',[(18,280),(290,262),(500,262),(584,196)],k)
    return _wrap(k,_stars(k,14,9)+'<circle cx="400" cy="170" r="110" fill="url(#irg)"/><circle cx="400" cy="176" r="52" fill="url(#iro)" opacity=".95"/><rect y="250" width="600" height="50" fill="#04121a"/>'+colo+dome+pine(386,52)+pine(560,46)+pine(36,40)+route)
def ai():
    k='ia';r=random.Random(5)
    grid=''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="300" stroke="rgba(234,242,240,.07)"/>' for x in range(0,601,40))+''.join(f'<line x1="0" y1="{y}" x2="600" y2="{y}" stroke="rgba(234,242,240,.07)"/>' for y in range(0,301,40))
    cont=''.join(f'<ellipse cx="{r.randint(120,480)}" cy="{r.randint(80,220)}" rx="{rx}" ry="{int(rx*.5)}" fill="none" stroke="rgba(234,242,240,.10)"/>' for rx in (50,90,130,180))
    nodes=[(70,230),(170,150),(280,200),(380,110),(480,170),(560,90)]
    d='M'+' L'.join(f'{x} {y}' for x,y in nodes)
    pins=''.join(f'<g><circle class="ring" style="animation-delay:-{i*.6}s" cx="{x}" cy="{y}" r="8" fill="none" stroke="#ff6b3d" stroke-width="1.5"/><circle cx="{x}" cy="{y}" r="7" fill="#06161e" stroke="#ff8a5b" stroke-width="2"/><path d="M{x-3} {y} l2.2 2.4 l4 -4.6" fill="none" stroke="#9be8b8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></g>' for i,(x,y) in enumerate(nodes))
    cards=''.join(f'<g class="fl" style="animation-delay:-{i*1.3}s"><rect x="{x}" y="{y}" width="92" height="34" rx="9" fill="#0a2630" stroke="rgba(234,242,240,.22)"/><rect x="{x+10}" y="{y+10}" width="40" height="4" rx="2" fill="#ff8a5b"/><rect x="{x+10}" y="{y+19}" width="62" height="3" rx="1.5" fill="rgba(234,242,240,.35)"/><circle cx="{x+78}" cy="{y+17}" r="6" fill="rgba(155,232,184,.2)"/><path d="M{x+75} {y+17} l2 2.2 l3.6 -4" fill="none" stroke="#9be8b8" stroke-width="1.6" stroke-linecap="round"/></g>' for i,(x,y) in enumerate([(30,70),(210,40),(420,200)]))
    scan='<rect class="sc" x="-60" y="0" width="60" height="300" fill="url(#iasc)"/>'
    return _wrap(k,_stars(k,12,2)+grid+cont+cards+_route(d,nodes,k).replace('stroke-linecap="round"','stroke-linecap="round" stroke-linejoin="round"')+pins+scan,'<linearGradient id="iasc" x1="0" x2="1"><stop offset="0" stop-color="#ff6b3d" stop-opacity="0"/><stop offset="1" stop-color="#ff6b3d" stop-opacity=".28"/></linearGradient>')
ILLS={'cosa-fare-a-catania-quando-piove':catania,'un-giorno-a-ortigia':ortigia,'roma-in-due-giorni':roma,'itinerario-turistico-con-intelligenza-artificiale':ai}
ILL_CSS='''
.ill .rn{stroke:rgba(200,222,230,.5);stroke-width:1.2;animation:rain 1.1s linear infinite}@keyframes rain{from{transform:translateY(-30px)}to{transform:translateY(320px)}}
.ill .mn,.ill .rn,.ill .sun,.ill .nt,.ill .stg,.ill .rfg{transition:opacity .6s,fill .6s,transform .35s}.ill.dry .rn{opacity:0}.ill.dry .mn{fill:#ff8a5b;opacity:.55}
.ill .tw{animation:tw 4s ease-in-out infinite}@keyframes tw{50%{opacity:.15}}
.ill .sm{opacity:0;transform-box:fill-box;transform-origin:center;animation:sm 6.4s ease-out infinite}@keyframes sm{0%{opacity:.0;transform:translate(0,0) scale(.6)}20%{opacity:.28}100%{opacity:0;transform:translate(26px,-70px) scale(1.7)}}
.ill .pulse2{animation:pu 1.8s ease-in-out infinite}@keyframes pu{50%{opacity:.35}}
.ill .wn{animation:wn 5s ease-in-out infinite}@keyframes wn{40%,60%{opacity:.25}}
.ill .wv{animation:wv 12s linear infinite}@keyframes wv{to{transform:translateX(300px)}}
.ill .rf{transform-box:fill-box;transform-origin:center;animation:rf 3s ease-in-out infinite}@keyframes rf{50%{transform:scaleX(.7)}}
.ill .bt{animation:bt 6s ease-in-out infinite}@keyframes bt{50%{transform:translateY(-3px) rotate(-1.5deg)}}
.ill .rt{stroke-dasharray:4 6;animation:rt 3.2s linear infinite}@keyframes rt{to{stroke-dashoffset:-100}}
.ill .pulse{transform-box:fill-box;transform-origin:center;animation:rg 2.2s ease-out infinite}@keyframes rg{from{transform:scale(1);opacity:.9}to{transform:scale(3.2);opacity:0}}
.ill .ring{transform-box:fill-box;transform-origin:center;animation:rg 2.8s ease-out infinite}
.ill .fl{animation:fl 6s ease-in-out infinite}@keyframes fl{50%{transform:translateY(-6px)}}
.ill .sc{animation:sc 7s linear infinite}@keyframes sc{to{transform:translateX(700px)}}
.hero-ill{margin:26px 0 0;border-radius:22px;overflow:hidden;border:1px solid var(--line2);height:clamp(170px,32vw,300px);box-shadow:0 30px 60px -30px rgba(255,107,61,.35)}
.hero-ill .cov{width:100%!important;height:100%!important;aspect-ratio:auto!important;margin:0!important;border:0!important;border-radius:0!important;display:block}
.card:hover .ill .rt{animation-duration:1.2s}
'''

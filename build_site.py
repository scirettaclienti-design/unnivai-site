s=open('landing5.html').read()
ff=''
for fam,file,w in [('Bricolage Grotesque','bricolage-grotesque',500),('Bricolage Grotesque','bricolage-grotesque',800),('Instrument Sans','instrument-sans',400),('Instrument Sans','instrument-sans',500),('Instrument Sans','instrument-sans',600),('IBM Plex Mono','ibm-plex-mono',400),('IBM Plex Mono','ibm-plex-mono',500)]:
    ff+="@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;src:url(/fonts/%s-latin-%d-normal.woff2) format('woff2')}\n"%(fam,w,file,w)
i=s.index('<style>');j=s.index('</style>')+8
style=s[i:j].replace('<style>','<style>\n'+ff,1)
k=s.index('<canvas id="gl"')
body=s[k:].replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js','/vendor/three.min.js')
old='Il sito non usa cookie di profilazione né strumenti di analisi che ti identificano. Per mostrare caratteri e grafica 3D carica alcune risorse da servizi esterni (Google Fonts e Cloudflare), che possono ricevere il tuo indirizzo IP.'
assert old in body
body=body.replace(old,"Il sito non usa cookie di profilazione né strumenti di analisi che ti identificano. Caratteri e grafica 3D sono serviti dal sito stesso, senza servizi esterni di tracciamento. Il fornitore di hosting registra dati tecnici di navigazione (come l'indirizzo IP) per garantire sicurezza e funzionamento.")
body=body.replace("var CONFIG = { url:'', anonKey:'', table:'waitlist', tableInterest:'city_interest' };","var CONFIG = { url:'__SUPA_URL__', anonKey:'__SUPA_KEY__', table:'waitlist', tableInterest:'city_interest' };")
body=body.replace('aria-label="Unni vai?"','aria-label="Unni vai? UNNIVAI, turismo intelligente e adattivo"')
ld='<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":"https://unnivai.com/#site","url":"https://unnivai.com/","name":"UNNIVAI","inLanguage":"it-IT","description":"Turismo intelligente e adattivo: percorsi con luoghi veri che si riscrivono quando la giornata cambia."},{"@type":"Organization","@id":"https://unnivai.com/#org","name":"UNNIVAI","url":"https://unnivai.com/","logo":"https://unnivai.com/logo.png","founder":{"@type":"Person","name":"Ivano Sciretta","sameAs":["https://www.linkedin.com/in/ivano-sciretta"]}}]}</script>'
head=open('site/head.html').read()+ld+'\n'
noscript='<noscript><style>.rv,.tag,.lead,.cta-row,.cue{opacity:1!important;transform:none!important}.wd{opacity:1!important}h1 .ch{transform:none!important}.hroute{stroke-dashoffset:0!important}</style></noscript>\n'
open('site/index.template.html','w').write(head+style+'\n'+noscript+'</head><body>\n'+body+'\n</body></html>')

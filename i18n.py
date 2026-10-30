import re,os
UI=[
('Accesso<span class="hm"> anticipato</span>','Early<span class="hm"> access</span>'),
('Accesso anticipato','Early access'),
('Vai al contenuto','Skip to content'),
('aria-label="Principale"','aria-label="Main"'),('aria-label="Sito"','aria-label="Site"'),
("Dove vai, in siciliano. Turismo con luoghi veri che si adatta alla tua giornata. Nasce in Sicilia, per tutta l'Italia.","“Dove vai” is Sicilian for “where are you going”. Travel built on real places, adapting to your day. Born in Sicily, for all of Italy."),
('<b>Dal blog</b>','<b>From the blog</b>'),('>Autore<','>Author<'),('>Metodo<','>Method<'),('/ Autore<','/ Author<'),
('>Privacy<','>Privacy<'),
('Il blog di UNNIVAI','The UNNIVAI blog'),
('Dove andare, e come andarci <em>bene.</em>','Where to go, and how to get there <em>well.</em>'),
("Itinerari con luoghi veri, piani B per la pioggia e idee per viaggiare senza buttare la giornata. Dalla Sicilia, per tutta l'Italia.","Itineraries built on real places, rainy-day plan Bs and ideas for travelling without wasting the day. From Sicily, for all of Italy."),
('placeholder="Cerca: Catania, pioggia, a piedi…"','placeholder="Search: Catania, rain, on foot…"'),
('aria-label="Cerca negli articoli"','aria-label="Search articles"'),('aria-label="Cerca e filtra"','aria-label="Search and filter"'),
('aria-label="Città e argomenti"','aria-label="Cities and topics"'),('aria-label="Contesto"','aria-label="Context"'),
('aria-label="Cancella"','aria-label="Clear"'),('aria-label="Ora del giorno"','aria-label="Time of day"'),
('aria-label="Indice e condivisione"','aria-label="Contents and sharing"'),('aria-label="Link a questa sezione"','aria-label="Link to this section"'),
('>Contesto<','>Context<'),('>Tutti <i>','>All <i>'),
('<h2>Nessun articolo ancora su questo.</h2>','<h2>No articles on this yet.</h2>'),
("Dimmi cosa cerchi: scrivo le guide in base alle richieste. Intanto entra nella lista d'attesa e ti avviso quando UNNIVAI arriva.","Tell me what you are looking for: I write the guides based on requests. Meanwhile join the waitlist and I will let you know when UNNIVAI launches."),
('Entra tra i primi.','Be among the first.'),('Entra tra i primi','Be among the first'),
('Il percorso giusto, che si adatta alla tua giornata.','The right route, adapting to your day.'),
("UNNIVAI costruisce l'itinerario con luoghi veri e lo riscrive quando cambia il tempo. Entra tra i primi.","UNNIVAI builds the itinerary with real places and rewrites it when the weather changes. Be among the first."),
('Per città','By city'),('Per situazione','By situation'),('Tutte le domande →','All questions →'),('Tutti gli articoli','All articles'),
(' guide · ',' guides · '),
('Continua a leggere','Keep reading'),('Prossimo articolo','Next article'),('Risposta in breve','Quick answer'),
('In questo articolo','In this article'),('Domande frequenti','Frequently asked questions'),('Fonti ufficiali','Official sources'),
('<b>Consiglio</b>','<b>Tip</b>'),('Al coperto','Indoors'),("All'aperto",'Outdoors'),
("Dimmi dove vuoi andare: ti scrivo quando UNNIVAI arriva nella tua città. Nessuna newsletter prima.","Tell me where you want to go: I will write when UNNIVAI reaches your city. No newsletter before that."),
('>Iscriviti<','>Sign up<'),
('Vuoi un percorso così, pronto e che si adatta al tempo?','Want a route like this, ready-made and adapting to the weather?'),
('>Copia link<','>Copy link<'),('Copiato ✓','Copied ✓'),("'Copia link'","'Copy link'"),
(' articoli\'',' articles\''),(" articolo'"," article'"),
('Errore 404','Error 404'),('Strada <em>sbagliata.</em>','Wrong <em>turn.</em>'),
("Questa pagina non c\\'è. Succede anche ai migliori navigatori. Riparti da qui.","This page is not here. It happens to the best navigators. Start again from here."),
("Questa pagina non c'è. Succede anche ai migliori navigatori. Riparti da qui.","This page is not here. It happens to the best navigators. Start again from here."),
('Vai al blog','Go to the blog'),
('Pagina non trovata · UNNIVAI','Page not found · UNNIVAI'),('Questa pagina non esiste più o non è mai esistita.','This page no longer exists, or never did.'),
('>Argomento<','>Topic<'),('>Domande<','>Questions<'),
('Domande che ci fanno <em>davvero.</em>','Questions people <em>really</em> ask us.'),
('Fondatore di UNNIVAI','Founder of UNNIVAI'),('Roma · Sicilia','Rome · Sicily'),
# widgets
('Provalo','Try it'),('☔ Piove','☔ Rain'),('☀ Non piove','☀ No rain'),('aria-label="Che tempo fa"','aria-label="Weather"'),
('A che ora sei a Ortigia?','What time are you in Ortigia?'),('Quale giorno ti serve?','Which day do you need?'),('>Entrambi<','>Both<'),
('>Giorno 1<','>Day 1<'),('>Giorno 2<','>Day 2<'),('aria-label="Giorno"','aria-label="Day"'),
('Fai il test adesso','Take the test now'),('Prendi tre tappe del tuo itinerario e spunta ciò che hai verificato.','Take three stops from your itinerary and tick what you have checked.'),
('<legend>Tappa ','<legend>Stop '),('Esiste sulla mappa','Exists on the map'),('È aperta quando ci vai','Is open when you go'),('È vicina alla tappa prima','Is close to the previous stop'),
("Spunta le caselle: ti dico se l\\'itinerario regge.","Tick the boxes: I will tell you if the itinerary holds up."),
("Spunta le caselle: ti dico se l'itinerario regge.","Tick the boxes: I will tell you if the itinerary holds up."),
(" tappe su ",' stops out of '),(' restano comode al coperto. Da accorciare o saltare: ',' stay comfortable indoors. Shorten or skip: '),
("'Senza pioggia vanno bene tutte e '","'Without rain all '"),(" le tappe: la parte all\\'aperto dà il meglio la mattina presto."," stops work: the outdoor part is best early in the morning."),
('Due giorni, due zone: non mischiarle e risparmi ore di cammino.','Two days, two areas: do not mix them and you save hours of walking.'),
('Giorno 1: la Roma antica, tra Colosseo, Foro e Campidoglio.','Day 1: ancient Rome, between the Colosseum, the Forum and the Capitoline Hill.'),
('Giorno 2: Vaticano al mattino, centro storico e Trastevere dopo.','Day 2: the Vatican in the morning, then the historic centre and Trastevere.'),
("Itinerario solido: tutte e tre le tappe sono verificate. Puoi partire.","Solid itinerary: all three stops are verified. You can go."),
("'Quasi: controlla ciò che manca prima di partire ('","'Almost: check what is missing before you leave ('"),
("'Da rivedere: troppe cose non verificate ('","'Needs work: too much unverified ('"),
("'Ricomincia: non fidarti ancora di questo itinerario ('","'Start over: do not trust this itinerary yet ('"),
(" su 9)"," of 9)"),
]
def months(en):return ['January','February','March','April','May','June','July','August','September','October','November','December'] if en else None
def rewrite_urls(h):
    B=r'(?:(https://unnivai\.com)|(?<![\w.-]))'
    rep=[(r'/blog/categoria/','/en/blog/category/'),(r'/blog/tema/','/en/blog/topic/'),(r'/blog/domande(?![\w-])','/en/blog/questions'),(r'/blog/search\.json','/en/blog/search.json'),
         (r'/autore(?![\w-])','/en/author'),(r'/metodo(?![\w-])','/en/method'),(r'/blog(?=["\'/?#])(?!/og/|/img/)','/en/blog'),(r'/rss\.xml','/en/rss.xml'),(r'/blog\.css','/blog.css')]
    for pat,to in rep:
        if pat==r'/blog\.css':continue
        h=re.sub(B+pat,lambda m:(m.group(1) or '')+to,h)
    h=h.replace('href="/"','href="/en/"').replace('href="/?src','href="/en/?src').replace('href="/#','href="/en/#')
    h=h.replace('"https://unnivai.com/"','"https://unnivai.com/en/"').replace('"https://unnivai.com/blog/og/index.png"','"https://unnivai.com/blog/og/index_en.png"').replace('https://unnivai.com/blog/og/index.png','https://unnivai.com/blog/og/index_en.png')
    return h
def finalize_en(h):
    h=rewrite_urls(h)
    for a,b in sorted(UI,key=lambda x:-len(x[0])):h=h.replace(a,b)
    h=h.replace('<html lang="it">','<html lang="en">').replace('content="it_IT"','content="en_US"').replace('"inLanguage": "it"','"inLanguage": "en"').replace('"inLanguage":"it"','"inLanguage":"en"')
    return h

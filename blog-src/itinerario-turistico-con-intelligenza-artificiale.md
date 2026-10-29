---
title: Itinerari con l'intelligenza artificiale: cosa funziona e cosa no
description: Come usare l'AI per pianificare un viaggio senza farsi inventare posti che non esistono: cosa chiederle, cosa verificare e perché contano i luoghi veri.
date: 2026-10-28
updated: 2026-10-29
category: Turismo e AI
cover: AI
tags: AI, Pianificazione
read: 9
sources:
- Anthropic, guida per ridurre le allucinazioni::https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Kalai et al., Why Language Models Hallucinate (OpenAI e Georgia Tech)::https://arxiv.org/pdf/2509.04664
- Google Maps, aiuto sugli orari di apertura::https://support.google.com/maps/answer/7084895?hl=en
- Parco archeologico del Colosseo, orari e biglietti::https://colosseo.it/orari/
- Pantheon, Ministero della Cultura::https://cultura.gov.it/luogo/pantheon
- Musei Vaticani, giorni e orari::https://www.museivaticani.va/content/museivaticani/it/info/orari-musei-vaticani.html
scheda:
- Tempo di lettura::9 minuti
- Il test::5 minuti, 3 tappe a caso
- Cosa serve::Una mappa e il sito ufficiale
- Il metodo::Prompt, verifica, piano B
faq:
- L'intelligenza artificiale può inventare luoghi che non esistono?::Sì, può accadere: un modello linguistico generico può descrivere con sicurezza posti, orari o piatti che non esistono. Per questo ogni tappa va verificata su una fonte con luoghi reali.
- Come si controlla un itinerario generato dall'AI?::Verifica che ogni tappa esista su una mappa, che sia aperta nel giorno previsto e che le distanze a piedi siano realistiche.
- Cosa deve avere un buon itinerario?::Tappe vicine tra loro, orari compatibili con la giornata, tempo per le pause e un piano B se cambia il tempo.
- Basta aggiungere "non inventare" al prompt?::No. Le guide dei fornitori dicono che le tecniche per ridurre le allucinazioni le riducono, ma non le eliminano. Servono permesso di dire "non lo so", richiesta delle fonti e una verifica tua sulle informazioni importanti.
- Quando conviene una guida invece dell'AI?::Quando il viaggio ruota attorno a pochi luoghi con orari rigidi, biglietti nominativi o regole di accesso: lì il sito ufficiale vale più di qualsiasi riassunto.
---
Chiedere a un'AI "organizzami tre giorni a Palermo" funziona sempre, nel senso che la risposta arriva. Il punto è un altro: è giusta? Un buon itinerario non è un elenco ben scritto, è una sequenza di luoghi reali, aperti, raggiungibili nell'ordine che ti propone. Ed è lì che le cose si complicano.

> **In breve.** L'AI è ottima per mettere ordine e dare idee, mediocre quando deve garantire che un posto esista e sia aperto. La differenza la fanno i dati veri sotto la risposta e la verifica che fai tu prima di partire.

## Cosa fa bene l'AI

- **Ordina.** Trasforma dieci idee sparse in una giornata con un filo logico.
- **Adatta.** Se dici "sono con bambini" o "ho solo mezza giornata", cambia il taglio.
- **Spiega.** Ti racconta perché un luogo vale la pena, non solo dove si trova.
- **Riscrive.** Se salta un biglietto o piove, rifà il programma in pochi secondi.

## Cosa fa male

- **Inventa con sicurezza.** Un modello generico può proporre un ristorante che ha chiuso, un museo che non esiste, un orario sbagliato.
- **Ignora la geografia.** Può metterti in fila tappe che sulla mappa distano mezz'ora a piedi l'una dall'altra.
- **Non sa che oggi piove.** A meno che non riceva i dati, non adatta il programma alla giornata.
- **Appiattisce le regole.** Un'informazione che cambia per stagione, giorno o evento viene spesso riassunta in una frase sola, valida "in generale".

## Perché succede, in breve

Un articolo di ricercatori di OpenAI e del Georgia Tech descrive le allucinazioni come affermazioni plausibili ma false. Secondo gli autori persistono perché l'addestramento e la valutazione premiano il tirare a indovinare più dell'ammettere l'incertezza: in una prova a risposta giusta o sbagliata, un "non lo so" vale zero, una supposizione può valere un punto. Non è un difetto di un singolo prodotto: è un comportamento da conoscere e da aggirare con un procedimento preciso. La guida di Anthropic per ridurre le allucinazioni arriva alla stessa conclusione dal lato pratico: le tecniche riducono in modo significativo gli errori ma non li eliminano, e le informazioni importanti vanno sempre validate.

## Come usarla senza farsi male

1. **Dai un contesto preciso:** zona, giorni, ritmo, con chi viaggi.
2. **Chiedi tappe vicine,** raggruppate per quartiere.
3. **Dai all'AI il permesso di non sapere.** La guida di Anthropic indica proprio questo come primo passo: consentire al modello di dire che non conosce la risposta può ridurre in modo marcato le informazioni false.
4. **Chiedi la fonte per ogni dato rigido** (orario, prezzo, regola) e chiedi di segnalare quelli che non può confermare.
5. **Verifica ogni tappa su una mappa:** esiste, dove si trova, quanto dista dalla precedente.
6. **Controlla gli orari** sulla fonte ufficiale.
7. **Chiedi un piano B** per pioggia o stanchezza.

## Prompt che puoi copiare

Il primo serve per costruire l'itinerario. Incollalo e sostituisci le parti tra parentesi quadre:

> Sei un assistente di viaggio prudente. Organizza [2 giorni] a [Roma] per [due adulti], ritmo [tranquillo], partenza alle [9:00]. Raggruppa le tappe per quartiere e indica per ogni giorno al massimo [4] tappe. Per ogni tappa scrivi: nome esatto del luogo, quartiere, tempo di permanenza, e se serve prenotare. Se non sei sicuro che un luogo esista o sia aperto, scrivi "da verificare" invece di indovinare. Non darmi orari o prezzi come certi: per quelli indica a quale sito ufficiale devo guardare.

Il secondo è il controllo, da lanciare nella stessa conversazione:

> Rileggi l'itinerario. Elenca in una tabella ogni tappa con: dove ti basi per dire che esiste, quali informazioni potrebbero cambiare per stagione o giorno della settimana, e quali tra queste hai dato per scontate. Segnala anche le coppie di tappe che potrebbero essere troppo lontane a piedi.

Il terzo è il piano B, che funziona bene perché lavora su un programma già verificato:

> Piove dalle [14:00] alle [18:00]. Riscrivi il pomeriggio mantenendo le tappe con biglietto già prenotato e sostituendo quelle all'aperto con alternative al coperto nella stessa zona. Indica cosa perdo e cosa guadagno con ogni cambio.

## Casi in cui l'AI sbaglia e come accorgersene

Ecco quattro situazioni che si possono dimostrare con pagine ufficiali. Non servono statistiche: bastano esempi.

**L'orario cambia per stagione.** Sul sito del Parco archeologico del Colosseo, per il periodo dal 25 ottobre 2026 al 28 febbraio 2027 sono indicati l'ingresso dalle 8:30 alle 16:30 e l'ultimo ingresso alle 15:30. Un riassunto generico che dice "fino al tramonto" o "fino alle 19" è giusto in un periodo e sbagliato in un altro. Segnale d'allarme: orari tondi senza data.

**Le regole di accesso non stanno nelle guide.** Il biglietto del Colosseo è nominativo e al varco si mostra un documento. Un itinerario che parla solo di "comprare i biglietti" omette il punto che può impedirti di entrare. Segnale d'allarme: nessun accenno a documento, nome sul biglietto o prenotazione.

**Il luogo ha più usi.** Il Pantheon è una chiesa attiva: la pagina del Ministero della Cultura indica messe in orari precisi e dice che durante le celebrazioni l'ingresso è libero e limitato ai fedeli. Un'AI che lo infila "sabato alle 17:00" ignora questo vincolo. Segnale d'allarme: tappe in luoghi di culto senza alcun cenno agli orari delle funzioni.

**Le fonti discordano.** Nella stessa pagina del Pantheon, il testo italiano e quello inglese indicano limiti diversi di biglietti per acquisto (25 contro 10). Un modello che pesca da una sola versione ti darà un numero sicuro e possibilmente sbagliato. Segnale d'allarme: una cifra precisa senza la fonte accanto.

C'è anche il caso dei Musei Vaticani: la pagina ufficiale elenca chiusure ricorrenti (le domeniche, tranne l'ultima del mese, e diverse date nell'anno). Una sequenza che mette il museo "domenica mattina" è plausibile e sbagliata, a meno che non sia l'ultima domenica del mese.

## Checklist di verifica prima di partire

- Ogni tappa compare su una mappa con il nome esatto e una posizione sensata.
- Hai guardato il sito ufficiale per orari, chiusure e giorno della settimana.
- Hai letto le regole di accesso: biglietto nominativo, documento, abbigliamento, bagagli.
- Le tappe consecutive sono raggiungibili nel tempo previsto, calcolato su una mappa e non a occhio.
- C'è una pausa di pranzo vera, non una riga "pranzo libero" in mezzo a due musei.
- Hai un piano B per la pioggia e uno per la stanchezza.
- Le cifre (prezzi, tempi) sono segnate come indicative e hanno una fonte.

Una nota sulle mappe: anche gli orari di Google Maps non sono una fonte ufficiale. La pagina di aiuto spiega che gli orari possono essere suggeriti dagli utenti e che le modifiche vengono riviste e possono richiedere tempo per comparire. Vanno bene per orientarsi, non per decidere se arrivare alle 16:20 a un sito con ultimo ingresso alle 15:30.

## Quando basta una guida (e non serve l'AI)

L'AI dà il meglio quando devi scegliere e ordinare. Se invece vai a Roma per vedere tre luoghi con orari rigidi e biglietti nominativi, ti serve un'informazione sola: cosa dice il sito ufficiale. Allora una guida buona, magari quella che stai leggendo, come [Roma in due giorni](/blog/roma-in-due-giorni), vale più di una risposta generata al volo. Usa l'AI per il resto: tempi, ordine, alternative e idee per la sera.

## Perché i luoghi veri fanno la differenza

Un sistema pensato per il turismo parte dal contrario: prima i luoghi reali, con le loro coordinate, poi l'AI che li ordina e li racconta. Così non può proporti un posto che non c'è, perché non lo pesca dalla sua memoria. È l'idea alla base di UNNIVAI: un percorso fatto di posti veri, costruito sul tuo tempo e sui tuoi gusti, e riscritto quando la giornata cambia.

## Esempi concreti

La regola vale per ogni città: provala sulle guide [Roma in due giorni](/blog/roma-in-due-giorni) e [Ortigia in una giornata](/blog/un-giorno-a-ortigia), dove ogni tappa ha un luogo, una zona e un tempo. Per vedere un piano B fatto bene, leggi [cosa fare a Catania quando piove](/blog/cosa-fare-a-catania-quando-piove).

## Il test dei cinque minuti

Prima di fidarti di qualunque itinerario, anche il tuo: scegli tre tappe a caso e controllale sulla mappa. Se tutte e tre esistono, sono vicine e sono aperte, di solito il resto regge. Se anche una sola salta, ricomincia.

:::widget test

Se vuoi provare un approccio diverso, [entra nella lista d'attesa di UNNIVAI](/?src=blog-ai#iscriviti).

*Nota di verifica: gli esempi su orari e regole sono stati letti sulle pagine ufficiali del Parco archeologico del Colosseo, del Ministero della Cultura (Pantheon) e dei Musei Vaticani il 29 ottobre 2026; le affermazioni sui modelli linguistici vengono dalla guida di Anthropic e dall'articolo di Kalai e colleghi citati sopra. Non abbiamo misurato la frequenza degli errori dei singoli assistenti AI e non indichiamo percentuali. Orari e regole cambiano: controlla sempre la fonte ufficiale.*

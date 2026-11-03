# Regole editoriali UNNIVAI (valgono per ogni articolo, scritto da persone o da Claude)

**Scopo del blog:** posizionarsi su Google e farsi citare dalle AI (ChatGPT, Claude, Perplexity, Gemini) su turismo in Italia. Vince chi è utile, verificabile e specifico.

## Non negoziabili
1. **Nessun dato inventato.** Orari, prezzi, regole di accesso, nomi di locali, distanze: solo se letti su una pagina aperta durante la ricerca. Se due fonti discordano, si scrive che discordano. Se non si sa, non si scrive.
2. **Minimo 3 fonti da almeno 2 domini**, di cui almeno una ufficiale (comune, museo, parco, ente turistico, UNESCO, trasporti). Ogni fonte in `sources:` nel front matter.
3. **Nota di verifica** a fine articolo + data "Verificato il" (la mette il generatore dalla data `date`/`updated`).
4. **Prezzi sempre come "medie indicative"**, mai come promessa.
5. **Mai testo copiato.** Si rielabora; citazioni al massimo una breve, tra virgolette, con fonte.
6. **IT e EN insieme.** Stesso `id`, slug EN in inglese, contenuto adattato (non traduzione meccanica: unità, abitudini, link alle fonti in inglese se esistono).

## Struttura
- Titolo 30-65 caratteri con la parola chiave principale; description 70-160.
- Riquadro `> **In breve.** …` (la risposta in 2-3 frasi: è ciò che le AI citano).
- `scheda:` con 3-5 voci (zona, durata, budget/orari indicativi, come si gira).
- Tappe `:::tappe` quando c'è un percorso; widget interattivo se ha senso (rain / time / days).
- 1100+ parole IT e EN, sezioni H2 con domande reali ("Quanto tempo serve?", "Come ci si arriva?").
- 4+ FAQ in front matter; 3+ link interni verso altri articoli; CTA lista d'attesa finale (`/?src=blog-<slug>#iscriviti`).
- Una cosa di "esperienza": un consiglio concreto, un errore comune, un orario in cui andare. Non generico.

## Tono
Diretto, concreto, caldo. Niente "scopri la magia", niente superlativi vuoti, niente elenchi di 20 posti. Meglio 6 tappe con un perché.

## Controllo automatico
`python3 scripts/check_article.py <id>` deve passare (parole, fonti, FAQ, link, date, EN presente). Poi `bash make.sh` e `python3 audit.py` senza problemi. Solo allora si fa push.

## Foto (aggiornato 2026-11-02)
- Ogni articolo: 3–4 foto vere da Wikimedia Commons, solo licenze CC BY / CC BY-SA / CC0 / pubblico dominio. Una ogni due o tre sezioni, non tutte in cima.
- La PRIMA `:::foto` dell'articolo è la copertina: il generatore la toglie dal corpo, la mostra come hero (WebP con width/height, fetchpriority=high, alt descrittivo, zoom/pan CSS lento, disattivato con prefers-reduced-motion), la usa come immagine OG (JPEG 1200×630) e nello schema Article (ImageObject ≥1200 px). Deve essere orizzontale.
- Procedura: cercare su Commons (API con User-Agent) -> `python3 scripts/add_photo.py "File:Nome.jpg" nome-breve` (pause di 15 s, su 429 riprovare; peso ≤ ~200 KB, le varianti -640/-960 le crea `make.sh`) -> GUARDARE ogni immagine con Read e verificare che mostri davvero il luogo -> nell'articolo `:::foto nome-breve | didascalia` (IT e EN, didascalia tradotta). La prima prima del primo `##`, le altre tra le sezioni.
- COPERTINA UNICA: ogni articolo ha una copertina diversa da tutte le altre (anche tra articoli della stessa città: es. Catania pioggia = Castello Ursino, Pescheria = banchi del mercato, cibo = piazza Duomo). La stessa foto non può essere copertina di due articoli; evitare anche di riusarla nel corpo di un altro articolo. Prima di scegliere la copertina controlla le copertine esistenti con `python3 scripts/check_covers.py`: `make.sh` e `check_article.py` falliscono se due articoli hanno la stessa copertina, se IT ed EN non hanno le stesse foto, o se una foto manca in photos.json.
- Se non si trova una foto adatta e verificata: lasciare l'articolo com'è e scriverlo nella nota di verifica. Mai foto generate con AI presentate come foto del luogo. Mai consigli "personali" inventati: le fonti restano quelle citate.
- Versione EN: titolo e "In breve" devono funzionare da soli, con la domanda reale che un turista straniero cercherebbe su Google. Chiudi con un invito all'app che segua il valore dato, non lo anticipi.

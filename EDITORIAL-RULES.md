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

## Foto (da 2026-10-30)
- Ogni articolo nuovo: 1–2 foto vere da Wikimedia Commons, solo licenze CC BY / CC BY-SA / CC0 / pubblico dominio.
- Procedura: cercare su Commons (API con User-Agent) -> `python3 scripts/add_photo.py "File:Nome.jpg" nome-breve` (rate limit: pause di 15 s, se 429 riprovare) -> VERIFICARE a vista che l'immagine mostri davvero il luogo -> nell'articolo `:::foto nome-breve | didascalia` prima del primo `##` (IT e EN, didascalia tradotta).
- Mai foto generate con AI presentate come foto del luogo. Mai consigli "personali" inventati: le fonti restano quelle citate.

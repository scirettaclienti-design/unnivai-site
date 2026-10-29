# UNNIVAI Blog · Guida redazionale (SEO + AI search)

## Cadenza
- **1 articolo lungo a settimana** (1.200–1.800 parole), pubblicato sempre lo stesso giorno (martedì mattina).
- **1 articolo breve a settimana** (500–700 parole) che risponde a UNA domanda precisa ("Quanto costa il bus per Ortigia?").
- Per 12 settimane. Poi si guarda Search Console: si raddoppia sui temi che portano impressioni, si smette su quelli che non ne portano.
- Un sito nuovo ha bisogno di costanza più che di volume: meglio 2 ottimi a settimana per 12 settimane che 20 in un giorno.

## Struttura obbligatoria di ogni articolo
1. **Titolo con la domanda reale** che la gente scrive ("Cosa fare a Catania quando piove").
2. **Risposta in breve** (box in alto, 2 frasi): è quello che i motori AI citano.
3. **H2 come domande o liste numerate**, un'idea per sezione.
4. **Dati verificabili**: nomi, zone, tempi a piedi, giorni di chiusura. Mai numeri inventati.
5. **3–4 domande frequenti** (finiscono nei dati strutturati).
6. **Fonti ufficiali** nel front matter (`sources:`) e data di verifica (`updated:`).
7. **2–3 link interni** ad altri articoli + 1 invito a iscriversi con `?src=blog-…`.
8. **Foto vere** (tue, anche da telefono) con testo alternativo descrittivo: oggi le copertine sono generate, le foto reali fanno la differenza su Google Immagini e sulla fiducia.

## Per comparire nelle risposte delle AI (ChatGPT, Claude, Perplexity, Gemini)
- Contenuti **risposta-prima**, frasi dichiarative e complete (le AI citano frasi, non giri di parole).
- **Entità chiare**: nome del luogo + città + zona nella stessa frase.
- **Autore reale + pagina autore + fonti**: segnali di affidabilità (`/autore`).
- Dati strutturati (già presenti): articolo, domande frequenti, briciole di pane.
- `robots.txt` apre ai crawler AI; `llms.txt` e `llms-full.txt` descrivono il sito (ancora non lo usano tutti i motori: è un extra, non una garanzia).
- **Menzioni esterne**: link da Radiosa, LinkedIn, TikTok, directory locali. Le AI si fidano di ciò che trovano citato altrove.
- Aggiorna e ri-data gli articoli ogni 3–6 mesi: orari e prezzi cambiano.

## Dopo ogni pubblicazione (5 minuti)
1. `bash make.sh` e `npx vercel --prod`.
2. Search Console → Controllo URL → "Richiedi indicizzazione" sul nuovo URL.
3. `./indexnow.sh` per avvisare Bing e gli altri motori.
4. Condividi su LinkedIn con `?src=linkedin`.

## Piano 12 settimane (lungo + breve)
| Sett. | Lungo | Breve |
|---|---|---|
| 1 | Cosa mangiare a Catania: piatti e dove | Orari della Pescheria di Catania |
| 2 | Catania in un weekend | Come arrivare a Ortigia da Catania |
| 3 | Palermo in un weekend | Cosa vedere a Palermo quando piove |
| 4 | Cosa vedere a Siracusa oltre Ortigia | Parco archeologico di Siracusa: come organizzare la visita |
| 5 | Etna: come organizzare una giornata | Quando andare sull'Etna |
| 6 | Taormina in un giorno | Taormina senza auto: come muoversi |
| 7 | Roma con i bambini | Roma: quanto camminare in un giorno |
| 8 | Piano B: 10 idee per un giorno di pioggia in Italia | Cosa mettere in valigia per un weekend di pioggia |
| 9 | Come pianificare un viaggio con l'AI (guida pratica) | I 5 errori degli itinerari generati dall'AI |
| 10 | Napoli in un weekend | Napoli: la pizza, dove e come evitare le code |
| 11 | Sicilia orientale in 5 giorni | Noleggio auto in Sicilia: cosa sapere |
| 12 | Bilancio del blog + cosa abbiamo imparato | Domande più cercate: aggiornamento |

## Cosa non fare
- Niente orari, prezzi o regole d'accesso scritti come certezze senza fonte: sempre "verifica sul sito ufficiale".
- Niente testo generico che chiunque potrebbe scrivere: ogni articolo deve avere almeno UNA cosa che solo tu sai (un consiglio da chi è del posto).
- Niente affermazioni di prodotto che la V1 non mantiene.

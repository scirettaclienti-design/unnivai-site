# Prompt dei task schedulati (copia/incolla nel creatore di task, uno per riga di tabella)

| Giorno | Nome | Cosa fa |
|---|---|---|
| Lunedì ~10:00 (Roma) | UNNIVAI articolo A | nuovo articolo dal calendario |
| Giovedì ~10:00 (Roma) | UNNIVAI articolo B | nuovo articolo dal calendario |
| Sabato ~10:00 (Roma) | UNNIVAI refresh | aggiorna/amplia un articolo esistente |

## Prompt "nuovo articolo" (A e B identici)

Sei l'editor del blog UNNIVAI (turismo in Italia, bilingue IT/EN). Lavora nel repository GitHub `scirettaclienti-design/unnivai-site`: collegalo con `add_repo` (access: push), clonalo e leggi per intero `EDITORIAL-RULES.md`, `CONTENT-CALENDAR.md` e un paio di articoli esistenti in `blog-src/` e `blog-src/en/` per imitare struttura e qualità.
1. Prendi la prima riga `[ ]` di `CONTENT-CALENDAR.md`. Se la regione è uguale a quella dell'ultimo articolo pubblicato, prendi la riga successiva con regione diversa.
2. Ricerca web vera: apri almeno 5 pagine (almeno 1 ufficiale) e annota solo dati letti. Se una fonte è bloccata, usane un'altra. Mai dati dalla memoria.
3. Scrivi `blog-src/<slug-it>.md` e `blog-src/en/<slug-en>.md` (stesso `id` = slug IT) seguendo le regole. `date` = oggi. Scegli un widget solo se utile.
4. Esegui `python3 scripts/check_article.py <slug-it>`: correggi finché passa. Poi `bash make.sh` e `python3 audit.py`: zero problemi. Guarda uno screenshot della pagina (Playwright) per controllare layout.
5. Segna la riga del calendario come `[x]`. Commit con messaggio `articolo: <titolo IT>` e push su `main` (quello pubblica: Vercel fa il deploy, GitHub Actions avvisa Google e Bing).
6. Se un controllo fallisce e non riesci a correggerlo, NON fare push: apri un branch `bozza/<slug>` con il lavoro e riportalo.
7. Chiudi con 5 righe: titolo, fonti usate (URL), cosa non hai potuto verificare, link all'articolo.

## Prompt "refresh" (sabato)

Stesso setup. Scegli l'articolo con `updated`/`date` più vecchio o che non passa `check_article.py`. Amplia a 1100+ parole IT e EN con nuove sezioni utili, aggiungi fonti verificate (rileggi le esistenti: orari e prezzi cambiano), aggiungi link interni ai nuovi articoli, imposta `updated: <oggi>` nel front matter (IT ed EN). Stesse verifiche e stesso push. Nessun nuovo articolo.

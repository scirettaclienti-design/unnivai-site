# UNNIVAI · sito e blog (IT/EN)

Sito statico (Vercel) generato da Python. Il repo dell'app è un altro (`unnivai`): **non mescolare**.

- `site/` = cartella pubblicata (HTML già generato).
- `blog-src/*.md` = articoli IT · `blog-src/en/*.md` = articoli EN (stesso `id`).
- `landing5.html` = home IT · `landing_en.py` = home EN (traduzioni).
- `make.sh` = rigenera tutto (richiede Python 3, Node + Playwright per le immagini OG).
- `scripts/check_article.py` = controllo qualità prima del push · `audit.py` = controllo SEO tecnico.
- `EDITORIAL-RULES.md`, `CONTENT-CALENDAR.md`, `WEEKLY-TASK-PROMPT.md`, `SETUP.md`.

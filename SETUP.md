# Setup (una volta sola, ~15 minuti)

## 1. Repo GitHub del sito
1. GitHub → New repository → nome **`unnivai-site`**, privato o pubblico, vuoto (senza README).
2. In questa cartella: `git init -b main && git add . && git commit -m "sito UNNIVAI" && git remote add origin https://github.com/scirettaclienti-design/unnivai-site.git && git push -u origin main`

## 2. Vercel: deploy automatico a ogni push
Vercel → progetto **unnivai-site** → Settings → Git → Connect → repo `unnivai-site`.
Settings → General → **Root Directory = `site`**, Framework Preset = Other, Build Command vuoto, Output Directory vuoto.
Da questo momento: push su `main` = sito online in ~1 minuto.

## 3. Search Console (automazione invio)
1. https://search.google.com/search-console → Aggiungi proprietà → **Dominio** `unnivai.com` → verifica con record DNS TXT (Vercel DNS o registrar).
2. Google Cloud Console → crea progetto → abilita **Google Search Console API** → IAM → Service Accounts → crea → Chiavi → **JSON**.
3. Search Console → Impostazioni → Utenti e autorizzazioni → aggiungi l'email del service account come **Proprietario** (o Utente completo).
4. GitHub repo → Settings → Secrets and variables → Actions → **New secret** `GSC_SA_JSON` = contenuto del file JSON. (Variabile opzionale `GSC_PROPERTY` = `sc-domain:unnivai.com`.)
5. Search Console → Sitemap → invia `https://unnivai.com/sitemap.xml` (la prima volta a mano).

Da qui l'azione `post-deploy-seo` ad ogni push: aspetta il deploy → IndexNow (Bing e altri) → rinvia la sitemap a Google → stampa lo stato di indicizzazione degli ultimi articoli nel log.
**Limite onesto:** Google non permette di "forzare" l'indicizzazione via API per i blog (l'Indexing API è solo per annunci di lavoro e dirette). La sitemap aggiornata, i link interni e l'RSS sono il metodo corretto; tempi tipici 2-14 giorni per URL nuovo.

## 4. Task schedulati (chiedimi di crearli quando 1-3 sono fatti)
Vedi `WEEKLY-TASK-PROMPT.md`: 2 articoli nuovi a settimana + 1 refresh.

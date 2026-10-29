#!/usr/bin/env python3
"""Invia la sitemap a Google Search Console e stampa lo stato di indicizzazione degli ultimi URL.
Richiede: variabile GSC_SA_JSON (chiave JSON del service account) e il service account aggiunto
come utente (Proprietario o Completo) nella proprieta' di Search Console. Nessuna chiave = esce senza errore."""
import os,json,sys,urllib.parse,re,urllib.request
raw=os.environ.get('GSC_SA_JSON','').strip()
if not raw:print('GSC_SA_JSON non impostata: salto Search Console (IndexNow gira comunque).');sys.exit(0)
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
prop=os.environ.get('GSC_PROPERTY','sc-domain:unnivai.com')
creds=service_account.Credentials.from_service_account_info(json.loads(raw),scopes=['https://www.googleapis.com/auth/webmasters'])
s=AuthorizedSession(creds)
site=urllib.parse.quote(prop,safe='');feed=urllib.parse.quote('https://unnivai.com/sitemap.xml',safe='')
r=s.put(f'https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps/{feed}')
print('sitemap submit ->',r.status_code,r.text[:200])
r=s.get(f'https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps/{feed}');print('sitemap stato ->',r.status_code,r.text[:400])
# stato degli ultimi 6 URL articolo (sola lettura: l'API non puo' chiedere l'indicizzazione)
sm=urllib.request.urlopen('https://unnivai.com/sitemap.xml').read().decode()
urls=[u for u in re.findall(r'<loc>([^<]+)</loc>',sm) if '/blog/' in u and u.count('/')>=5][:6]
for u in urls:
    r=s.post('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect',json={'inspectionUrl':u,'siteUrl':prop})
    try:st=r.json()['inspectionResult']['indexStatusResult'];print(u,'->',st.get('coverageState'),'| ultimo crawl:',st.get('lastCrawlTime','mai'))
    except Exception:print(u,'->',r.status_code,r.text[:120])

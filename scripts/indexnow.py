#!/usr/bin/env python3
"""Notifica a Bing/Yandex/ecc. (IndexNow) gli URL della sitemap. Google non usa IndexNow."""
import json,urllib.request
p=json.load(open('indexnow_payload.json'))
req=urllib.request.Request('https://api.indexnow.org/indexnow',data=json.dumps(p).encode(),headers={'Content-Type':'application/json'})
try:print('IndexNow ->',urllib.request.urlopen(req,timeout=30).status)
except Exception as e:print('IndexNow ->',e)

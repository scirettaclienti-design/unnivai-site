#!/bin/bash
# IndexNow (Bing, Yandex, ecc.). Google NON usa IndexNow: per Google serve Search Console.
curl -s -X POST https://api.indexnow.org/indexnow -H "Content-Type: application/json" -d @indexnow_payload.json -w "HTTP %{http_code}\n"

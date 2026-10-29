set -e
cd "$(dirname "$0")"
python3 build_site.py
python3 build_blog.py
BLANG=en python3 build_blog.py
source config/supabase.env
sed "s#__SUPA_URL__#$SUPA_URL#;s#__SUPA_KEY__#$SUPA_KEY#" site/index.template.html > site/index.html
python3 landing_en.py
python3 build_seo.py
HERE=$(pwd); (cd /tmp && NODE_PATH=$(npm root -g) node $HERE/og_blog.js $HERE/site)
echo built

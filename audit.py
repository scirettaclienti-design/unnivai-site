import re,json,os,glob
S='site';issues=[]
pages=[p for p in glob.glob(S+'/**/index.html',recursive=True)]
def exists(u):
    u=u.split('#')[0].split('?')[0]
    if not u or u=='/':return True
    p=S+u
    return os.path.exists(p) or os.path.exists(p+'/index.html') or os.path.exists(p+'.html')
for p in pages:
    h=open(p).read();name=p[len(S):]
    t=re.search(r'<title>(.*?)</title>',h);d=re.search(r'<meta name="description" content="(.*?)"',h)
    if not t:issues.append((name,'no title'))
    else:
        if len(t.group(1))>65:issues.append((name,f'title {len(t.group(1))} chars'))
    if d and not 70<=len(d.group(1))<=160:issues.append((name,f'desc {len(d.group(1))} chars'))
    if not d:issues.append((name,'no desc'))
    n1=len(re.findall(r'<h1[ >]',h))
    if n1!=1 and 'index.html' and not name=='/index.html':issues.append((name,f'h1 count {n1}'))
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        try:json.loads(m)
        except Exception as e:issues.append((name,'bad jsonld '+str(e)[:40]))
    for u in set(re.findall(r'href="(/[^"#]*)',h))|set(re.findall(r'src="(/[^"]+)"',h)):
        if not exists(u):issues.append((name,'broken '+u))
    ids=set(re.findall(r'id="([^"]+)"',h))
    for a in set(re.findall(r'href="#([^"]+)"',h)):
        if a not in ids and a not in('privacy','iscriviti','top','come','perche','main'):issues.append((name,'dead anchor #'+a))
    sz=len(h.encode())
    print(f'{name:60s} {sz//1024:4d}KB  h1={n1}')
print('ISSUES');[print(' ',i) for i in issues]

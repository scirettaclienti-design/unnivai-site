const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630}});
for(const f of fs.readdirSync('/tmp').filter(x=>/^og_.*\.html$/.test(x))){const n=f.slice(3,-5);await p.goto('file:///tmp/'+f);await p.waitForTimeout(500);await p.screenshot({path:process.argv[2]+'/blog/og/'+n+'.png'})}
await b.close()})();

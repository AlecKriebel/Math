// Read-only browser inspection of the private local HTML. No service publication.
import {spawn} from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
const E='/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23149775/reviews/editorial';
const page=path.resolve(E,'../../publication/promotion/page.html');
const profile=path.join(E,'browser-profile');
const started=new Date().toISOString();
const proc=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless=new','--disable-gpu','--no-sandbox','--no-first-run','--disable-background-networking','--remote-debugging-port=0','--user-data-dir='+profile,'--window-size=1440,1200','file://'+page]);
let stdout='',stderr='';proc.stdout.on('data',b=>stdout+=b);proc.stderr.on('data',b=>stderr+=b);
let socket;let next=1;const pending=new Map();
async function call(method,params={}){const id=next++;return new Promise((resolve,reject)=>{pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});}
async function evaluate(expression){const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
const records=[];
try{
 let port;
 for(let n=0;n<100;n++){try{port=Number((await fs.readFile(path.join(profile,'DevToolsActivePort'),'utf8')).split('\n')[0]);break;}catch{}await new Promise(r=>setTimeout(r,100));}
 if(!port)throw new Error('No live browser debugging endpoint');
 const tabs=await (await fetch('http://127.0.0.1:'+port+'/json/list')).json();const tab=tabs.find(t=>t.type==='page'&&t.url==='file://'+page);if(!tab)throw new Error('Exact private candidate tab missing');
 socket=new WebSocket(tab.webSocketDebuggerUrl);await new Promise((r,j)=>{socket.addEventListener('open',r,{once:true});socket.addEventListener('error',j,{once:true});});
 socket.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}});
 await call('Page.enable');await call('Runtime.enable');
 for(const [label,width,height] of [['desktop',1440,1200],['mobile',390,844]]){
  await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:label==='mobile'});
  await evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
  const metrics=await evaluate(`({viewport:innerWidth,body:document.documentElement.scrollWidth,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor,h1:document.querySelectorAll('h1').length,canonical:document.querySelector('link[rel=canonical]')?.href??null,robots:document.querySelector('meta[name=robots]').content,iframeWidth:document.querySelector('iframe').getBoundingClientRect().width,mainWidth:document.querySelector('main').getBoundingClientRect().width,formulaWidth:document.querySelector('.formula').clientWidth,formulaScrollWidth:document.querySelector('.formula').scrollWidth})`);
  if(metrics.body>metrics.viewport||metrics.h1!==1||metrics.canonical!==null||metrics.robots!=='noindex,nofollow'||!metrics.font.includes('Arial')||metrics.background!=='rgb(255, 255, 255)')throw new Error('Private layout/publication guard '+JSON.stringify(metrics));
  for(const [region,selector] of [['top','h1'],['related','h2:nth-of-type(5)'],['paper','iframe']]){
   await evaluate(`document.querySelector(${JSON.stringify(selector)}).scrollIntoView({block:'start'})`);
   await evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
   const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await fs.writeFile(path.join(E,`${label}-${region}.png`),Buffer.from(shot.data,'base64'));
  }
  records.push({label,width,height,metrics});
 }
 await fs.writeFile(path.join(E,'BROWSER_QA.json'),JSON.stringify({started_utc:started,finished_utc:new Date().toISOString(),status:'PASS_PRIVATE_LOCAL_DESKTOP_MOBILE_LAYOUT',records,actual_live_or_public_service_checked:false,canonical_or_tracker_assigned:false},null,2)+'\n');
}finally{
 if(socket)socket.close();proc.kill('SIGTERM');
 await new Promise(r=>{if(proc.exitCode!==null)r();else{proc.once('exit',r);setTimeout(()=>{proc.kill('SIGKILL');r();},3000).unref();}});
 await fs.writeFile(path.join(E,'browser.stdout'),stdout);await fs.writeFile(path.join(E,'browser.stderr'),stderr);
 if(path.dirname(profile)!==E)throw new Error('Profile cleanup guard');await fs.rm(profile,{recursive:true,force:true});
}

// Private localhost-only preview with explicit desktop/mobile viewport metrics.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const P=path.dirname(fileURLToPath(import.meta.url));
const sha=b=>createHash('sha256').update(b).digest('hex');
const receiptPath=path.join(P,'CDP_PREVIEW_RECEIPTS.json');
if(fs.existsSync(receiptPath))throw Error('Existing immutable preview receipt');
const access=[];
const server=http.createServer((req,res)=>{
 const relative=decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/^\//,'');
 const target=path.resolve(P,relative);
 if(!target.startsWith(P+path.sep)||!fs.existsSync(target)||!fs.statSync(target).isFile()){
  res.writeHead(404);res.end('Not found');access.push({path:req.url,status:404});return;
 }
 const bytes=fs.readFileSync(target);
 const type=target.endsWith('.html')?'text/html; charset=utf-8':target.endsWith('.pdf')?'application/pdf':target.endsWith('.zip')?'application/zip':'text/plain; charset=utf-8';
 res.writeHead(200,{'Content-Type':type,'Content-Length':bytes.length,'Cache-Control':'no-store'});
 res.end(bytes);access.push({path:req.url,status:200,bytes:bytes.length});
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const base=`http://127.0.0.1:${server.address().port}/preview/index.html`;
const profile=fs.mkdtempSync(path.join(P,'preview/cache/cdp-'));
const chromeArgs=['--headless=new','--disable-gpu','--no-first-run','--disable-background-networking',
 '--disable-component-update','--disable-sync','--disable-default-apps','--disable-crash-reporter',
 '--no-default-browser-check','--host-resolver-rules=MAP * 0.0.0.0, EXCLUDE localhost, EXCLUDE 127.0.0.1',
 '--user-data-dir='+profile,'--disk-cache-dir='+path.join(profile,'disk'),'--remote-debugging-port=0','about:blank'];
const child=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',chromeArgs,{cwd:P});
let stderr='';child.stderr.on('data',d=>stderr+=d.toString());
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
let socket;
const receipts=[];
try{
 const active=path.join(profile,'DevToolsActivePort');
 for(let i=0;i<100&&!fs.existsSync(active);i++)await delay(100);
 if(!fs.existsSync(active))throw Error('Chrome debugging endpoint unavailable');
 const port=Number(fs.readFileSync(active,'utf8').split('\n')[0]);
 const tabs=await(await fetch(`http://127.0.0.1:${port}/json/list`)).json();
 const page=tabs.find(x=>x.type==='page');if(!page)throw Error('No private page target');
 socket=new WebSocket(page.webSocketDebuggerUrl);
 await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
 let next=0;const pending=new Map();
 socket.addEventListener('message',event=>{
  const msg=JSON.parse(event.data);if(!msg.id)return;
  const p=pending.get(msg.id);if(!p)return;pending.delete(msg.id);
  msg.error?p.reject(Error(JSON.stringify(msg.error))):p.resolve(msg.result);
 });
 const send=(method,params={})=>new Promise((resolve,reject)=>{
  const id=++next;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));
 });
 await send('Page.enable');await send('Runtime.enable');
 const specs=[['desktop-top',1440,1000,false,''],['mobile-top',390,844,true,''],
              ['desktop-reader',1440,1000,false,'reader'],['mobile-materials',390,844,true,'materials']];
 for(const [name,width,height,mobile,anchor] of specs){
  const started=new Date().toISOString();
  await send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile,screenWidth:width,screenHeight:height});
  await send('Page.navigate',{url:base});
  for(let i=0;i<100;i++){
   const q=await send('Runtime.evaluate',{expression:'document.readyState === "complete" && !!document.getElementById("reader")',returnByValue:true});
   if(q.result.value)break;await delay(100);
  }
  await send('Runtime.evaluate',{expression:anchor?`document.getElementById(${JSON.stringify(anchor)}).scrollIntoView()`:'window.scrollTo(0,0)',returnByValue:true});
  await delay(500);
  const result=await send('Runtime.evaluate',{expression:`JSON.stringify({innerWidth:innerWidth,innerHeight:innerHeight,documentWidth:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,bodyWidth:document.body.getBoundingClientRect().width,mainLeft:document.querySelector('main').getBoundingClientRect().left,mainRight:document.querySelector('main').getBoundingClientRect().right,readerFrameWidth:document.querySelector('iframe').getBoundingClientRect().width,bodyTextCharacters:document.body.innerText.length,scrollY:scrollY,ready:document.readyState})`,returnByValue:true});
  const metrics=JSON.parse(result.result.value);
  if(metrics.innerWidth!==width||metrics.scrollWidth>width)throw Error('Unexpected viewport or horizontal overflow: '+JSON.stringify(metrics));
  const capture=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false,fromSurface:true});
  const bytes=Buffer.from(capture.data,'base64');const screenshot=path.join(P,'preview','cdp-'+name+'.png');
  fs.writeFileSync(screenshot,bytes,{flag:'wx'});
  receipts.push({started_UTC:started,completed_UTC:new Date().toISOString(),private_localhost_only:true,
   HTML_SHA256:sha(fs.readFileSync(path.join(P,'preview/index.html'))),window:[width,height],mobile,anchor,
   explicit_device_metrics_override:true,metrics,screenshot,screenshot_SHA256:sha(bytes),screenshot_bytes:bytes.length,
   production_or_native_verification:false});
 }
 await send('Browser.close').catch(()=>{});
}finally{
 if(socket)socket.close();child.kill('SIGTERM');
 await new Promise(resolve=>{if(child.exitCode!==null)resolve();else{child.once('exit',resolve);setTimeout(resolve,2000);}});
 await new Promise(resolve=>server.close(resolve));
 fs.rmSync(profile,{recursive:true,force:true});
}
fs.writeFileSync(receiptPath,JSON.stringify({receipts,chrome_arguments:chromeArgs,chrome_stderr:stderr,
 actual_local_access_log:access,earlier_CLI_capture_diagnostics:'Earlier CLI mobile capture clipped and fragment captures blank; retained as nonaccepted history. Explicit CDP metrics and accepted captures supersede them.',
 all_production_browser_native_canonical_gates_remain_false:true,temporary_profile_removed:true},null,2)+'\n',{flag:'wx'});
process.stdout.write(JSON.stringify({private_captures:receipts.length,metrics:receipts.map(x=>({window:x.window,metrics:x.metrics,bytes:x.screenshot_bytes})),production_browser_gate:false},null,2));

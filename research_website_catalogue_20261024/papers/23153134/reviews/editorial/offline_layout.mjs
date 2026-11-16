// New bounded offline screenshot utility; ordinary default is read-only.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const here=path.dirname(fileURLToPath(import.meta.url)),args=process.argv.slice(2),preview=path.join(here,'preview');
if(args.length===0){process.stdout.write(JSON.stringify({mode:'READ_ONLY_GUARD',explicit_render_required:true,preview_exists:fs.existsSync(path.join(preview,'index.html'))})+'\n');}
else{
 if(JSON.stringify(args)!=='["--render"]'||fs.existsSync(path.join(here,'FINAL.json')))throw new Error('Only one explicit pre-FINAL --render');
 const dir=path.join(here,'renders');if(fs.existsSync(dir))throw new Error('Fresh exclusive renders directory required');fs.mkdirSync(dir);
 const owned=['owned-profile','owned-temp','owned-downloads'].map(x=>path.join(dir,x));for(const q of owned)fs.mkdirSync(q);
 const receipt={kind:'One offline headless six-view HTML layout pass; no native/live/mobile/download certification',started_UTC:new Date().toISOString(),viewports:[],requests:[],request_failures:[],console_errors:[],page_errors:[],blocked_HTTP_requests:[],captures:[],measurements:[],cleanup:[],fatal_error:null,download_clicks:[],native_viewer_certification:false,scientific_program_executions:[]};
 let context=null;
 try{
  const require=createRequire(import.meta.url),{chromium}=require('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core');
  context=await chromium.launchPersistentContext(owned[0],{headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',downloadsPath:owned[2],env:{...process.env,TMPDIR:owned[1]},args:['--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run','--no-default-browser-check','--disable-features=MediaRouter,OptimizationHints']});
  receipt.browser_version=context.browser()?.version()??null;await context.setOffline(true);
  await context.route('**/*',async route=>{const u=route.request().url();const local=u.startsWith('file:')&&decodeURIComponent(new URL(u).pathname).startsWith(preview+'/');if(local||/^(data:|blob:|chrome:|chrome-extension:)/.test(u))await route.continue();else{receipt.blocked_HTTP_requests.push(u);await route.abort();}});
  const page=await context.newPage();page.on('request',q=>receipt.requests.push({url:q.url(),method:q.method(),resource_type:q.resourceType()}));page.on('requestfailed',q=>receipt.request_failures.push({url:q.url(),error:q.failure()?.errorText??null}));page.on('pageerror',e=>receipt.page_errors.push(e.message));page.on('console',m=>{if(m.type()==='error')receipt.console_errors.push(m.text());});
  const response=await page.goto(pathToFileURL(path.join(preview,'index.html')).href,{waitUntil:'load'});receipt.navigation_response=response?{url:response.url(),status:response.status()}:null;
  for(const [label,width,height] of [['desktop',1100,900],['mobile',390,844]]){
   await page.setViewportSize({width,height});receipt.viewports.push({label,width,height});await page.waitForTimeout(700);
   const measure=await page.evaluate(()=>({inner_width:innerWidth,document_scroll_width:document.documentElement.scrollWidth,body_font:getComputedStyle(document.body).fontFamily,body_background:getComputedStyle(document.body).backgroundColor,main_id:document.querySelector('main')?.id,h1_count:document.querySelectorAll('h1').length,iframe_title:document.querySelector('iframe')?.title,iframe_src:document.querySelector('iframe')?.getAttribute('src')}));receipt.measurements.push({label,...measure});
   if(measure.document_scroll_width!==width||measure.main_id!=='main'||measure.h1_count!==1||!measure.body_font.includes('Arial')||measure.body_background!=='rgb(255, 255, 255)')throw new Error('HTML layout mismatch '+label);
   for(const [name,selector] of [['full',null],['abstract','#abstract'],['result','#result']]){
    const q=path.join(dir,label+'-'+name+'.png');if(selector)await page.locator(selector).screenshot({path:q});else await page.screenshot({path:q,fullPage:true});receipt.captures.push({path:path.relative(here,q),selector,saved:true,error:null});
   }
  }
 }catch(e){receipt.fatal_error=String(e.stack??e);}
 finally{
  if(context)try{await context.close();}catch(e){receipt.console_errors.push('Context close: '+String(e));receipt.fatal_error??=String(e);}
  for(const q of owned){try{fs.rmSync(q,{recursive:true,force:false});receipt.cleanup.push({path:path.relative(here,q),removed:true,error:null});}catch(e){receipt.cleanup.push({path:path.relative(here,q),removed:false,error:String(e)});receipt.fatal_error??=String(e);}}
 }
 receipt.finished_UTC=new Date().toISOString();receipt.six_views_saved=receipt.captures.length===6;
 const raw=JSON.stringify(receipt,null,2)+'\n';fs.writeFileSync(path.join(dir,'LAYOUT_RECEIPT.json'),raw,{flag:'wx'});process.stdout.write(raw);if(receipt.fatal_error)process.exitCode=1;
}

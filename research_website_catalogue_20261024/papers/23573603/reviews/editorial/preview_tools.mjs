// Copyright (c) 2026 Alec Kriebel. MIT; see LICENSES.md.
// One read-only editorial data check, or one explicitly requested offline render.
// No source program, builder, scientific checker, live request or publication.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const own=p=>path.join(root,p), source=path.resolve(root,'../../sources');
const programme=path.resolve(root,'../../../..');
const read=p=>fs.readFileSync(p),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const pin=p=>{const b=read(p);return {bytes:b.length,SHA256:sha(b)};};
const need=(v,m)=>{if(!v)throw new Error(m);};
const norm=s=>s.trim().replace(/\s+/g,' ');
const decode=s=>s.replaceAll('&quot;','"').replaceAll('&#x27;',"'").replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&');
const plain=s=>norm(decode(s.replace(/<[^>]+>/g,'')));
const mode=process.argv.slice(2);need(mode.length===0||(mode.length===1&&mode[0]==='--render'),'Only read-only default or --render');
for(const p of ['OWNED_MANIFEST.json','FINAL.json']){
 const s=fs.lstatSync(own(p));need(s.isFile()&&!s.isSymbolicLink()&&read(own(p)).equals(Buffer.from('{}\n')),'Pre-final exact terminal '+p);
}
const html=read(own('preview/index.html')).toString();
const main=html.match(/<main id="main">[\s\S]*?<\/main>/g),head=html.match(/<head>[\s\S]*?<\/head>/g);
need(main?.length===1&&head?.length===1,'One complete MAIN and head');
const inputNames=['preview/index.html','preview/research.css','preview/citation.bib','MAIN.html','PAGE_MODEL.json','preview_tools.mjs'];
const inputs=()=>Object.fromEntries(inputNames.map(p=>[p,pin(own(p))]));
if(mode.length===0){
 const model=JSON.parse(read(own('PAGE_MODEL.json')));
 for(const row of [model.source_first.INITIAL,model.source_first.seal,model.source_first.source_pins,model.source_first.log]){
  need(JSON.stringify(pin(own(row.path)))===JSON.stringify({bytes:row.bytes,SHA256:row.SHA256}),'Frozen initial '+row.path);
 }
 for(const row of [model.root_scientific_clearance,model.root_report]){
  need(JSON.stringify(pin(path.join(programme,row.path)))===JSON.stringify({bytes:row.bytes,SHA256:row.SHA256}),'Actual opened root authority');
 }
 const tex=read(path.join(source,'published-source/container-001/tree/supercritical_nonuniqueness_source/main.tex')).toString();
 need(sha(tex)==='6b5a8b008f43d2cdd22641889b67d63b6c635e2997378ccca66246b7902666af','Original controlling TeX');
 const original=norm(tex.split('\\begin{abstract}')[1].split('\\end{abstract}')[0].replaceAll('$',''));
 const visible=html.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>[\s\S]*?<\/section>/)?.[1];
 const scholarly=JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
 const dc=decode(html.match(/<meta name="DC.description" content="([^"]*)">/)[1]);
 need(plain(visible)===original&&scholarly.abstract===original&&dc===original&&model.full_original_abstract===original,'Complete original abstract in all four representations');
 need(read(own('MAIN.html')).toString()===main[0]+'\n','Whole saved MAIN fragment');
 for(const row of [model.whole_page,model.MAIN_file,model.stylesheet,model.BibTeX]){
  need(JSON.stringify(pin(own(row.path)))===JSON.stringify({bytes:row.bytes,SHA256:row.SHA256}),'Whole authored input '+row.path);
 }
 const acquired=JSON.parse(read(path.join(source,'ACQUIRED.json'))).records[0];
 const files=JSON.parse(read(path.join(source,'files-23573603.response.body')));
 need(acquired.native_version_whole_field.original_value==='1.0.0'&&acquired.publication_date==='2026-10-22'&&acquired.created==='2026-10-22T17:57:59.433479+00:00','Native edition fields');
 need(acquired.native_is_published.present===false&&files.order.length===0,'Preserve native absence/order field');
 need(files.entries.map(f=>f.key).join('|')==='supercritical-nonuniqueness.pdf|supercritical-nonuniqueness-source-and-verification.zip','Literal native PDF then ZIP order');
 const assets=model.native_assets_in_order.map((row,i)=>{
  const b=read(own(row.path)),native=read(path.join(source,'assets',row.key)),f=files.entries[i];
  need(b.equals(native)&&b.length===row.bytes&&sha(b)===row.SHA256&&f.key===row.key&&f.size===b.length&&f.checksum==='md5:'+crypto.createHash('md5').update(b).digest('hex'),'Whole native asset '+row.key);
  return {path:row.path,...pin(own(row.path))};
 });
 const downloads=[...html.match(/<ol id="native-downloads">([\s\S]*?)<\/ol>/)[1].matchAll(/<li><a href="([^"]+)"/g)].map(m=>m[1]);
 need(downloads.join('|')===files.entries.map(f=>f.key).join('|'),'Visible native download order');
 need(html.includes('src="supercritical-nonuniqueness.pdf#view=FitH"')&&html.includes('title="Original five-page manuscript:'),'Unchanged local reader and title');
 need(html.includes('name="robots" content="noindex, nofollow, noarchive"')&&!/<link[^>]+rel="canonical"/.test(html),'Private noindex/no canonical');
 need(model.canonical_url===null&&model.AA===null&&model.follow_up===null&&model.publication_authority===false,'No public authority or question');
 need(!main[0].includes('Original Zenodo description')&&!main[0].includes('native-description')&&!main[0].includes('2048'),'No duplicated Description/internal count inventory');
 for(const text of ['explicitly declared interpretation','positive-probability nonuniqueness at one fixed parameter','sufficiently near one','2200741829/6461571200','27/107648','independent human or journal peer review','separately','MIT licensed','final-journal byte equivalence']){
  need(main[0].includes(text),'Required public scope/status '+text);
 }
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);need(new Set(ids).size===ids.length,'Unique HTML IDs');
 const hrefs=[...html.matchAll(/\bhref="([^"]+)"/g)].map(m=>m[1]);
 need(hrefs.filter(h=>h.startsWith('#')).every(h=>ids.includes(h.slice(1))),'Local fragments');
 for(const h of hrefs.filter(h=>!h.startsWith('/')&&!h.startsWith('#')&&!/^[a-z]+:/i.test(h))){
  const p=own('preview/'+h.split('#')[0]);need(fs.lstatSync(p).isFile(),'Existing local href '+h);
 }
 const bib=read(own('preview/citation.bib')).toString();
 need(bib.includes('doi = {10.5281/zenodo.23573603}')&&bib.includes('version = {1.0.0}')&&bib.includes('day = {22}'),'Native Bib metadata');
 console.log(JSON.stringify({status:'PRIVATE_EDITORIAL_DATA_PASS',mode:'read-only',writes:0,record_id:23573603,inputs:inputs(),whole_MAIN:{bytes:Buffer.byteLength(main[0]),SHA256:sha(main[0])},whole_head:{bytes:Buffer.byteLength(head[0]),SHA256:sha(head[0])},assets,full_abstract_equal:true,initial_four_unchanged:true,public_authority:false},null,2));
}else{
 need(!fs.existsSync(own('RENDER_RECEIPT.json'))&&!fs.existsSync(own('render-work'))&&!fs.existsSync(own('renders')),'One fresh render only');
 const before=inputs(),work=own('render-work'),remote=[],requests=[],failed=[],errors=[],consoleErrors=[],views=[],screenshots=[],cleanupErrors=[];
 fs.mkdirSync(work,{mode:0o700});fs.mkdirSync(path.join(work,'tmp'),{mode:0o700});fs.mkdirSync(own('renders'));
 let browser,fatal=null;
 try{
  const {chromium}=await import('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.mjs');
  browser=await chromium.launchPersistentContext(path.join(work,'profile'),{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,env:{...process.env,TMPDIR:path.join(work,'tmp')},args:['--disable-background-networking','--disable-component-update','--disable-default-apps','--disable-sync','--no-first-run','--no-default-browser-check','--disable-domain-reliability','--metrics-recording-only','--disable-features=OptimizationHints,MediaRouter,AutofillServerCommunication']});
  browser.on('request',r=>requests.push({url:r.url(),method:r.method(),resourceType:r.resourceType()}));
  browser.on('requestfailed',r=>failed.push({url:r.url(),failure:r.failure()}));
  await browser.route('**/*',r=>{
   const u=r.request().url();
   if(u.startsWith('file:')){need(fileURLToPath(u).startsWith(root+path.sep),'Owned local-file requests only');return r.continue();}
   if(/^(data:|about:|chrome-extension:|chrome:\/\/resources\/)/.test(u))return r.continue();
   remote.push(u);return r.abort();
  });
  const page=await browser.newPage();
  page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text());});
  for(const [name,width,height] of [['desktop',1100,900],['mobile',390,844]]){
   await page.setViewportSize({width,height});
   await page.goto(pathToFileURL(own('preview/index.html')).href,{waitUntil:'load'});
   await page.locator('iframe').scrollIntoViewIfNeeded();await page.waitForTimeout(750);await page.evaluate(()=>window.scrollTo(0,0));
   const state=await page.evaluate(()=>{
    const f=document.querySelector('iframe'),r=f.getBoundingClientRect();let observation;
    try{const d=f.contentDocument;observation=d?{accessible:true,readyState:d.readyState,bodyChildren:d.body?.children.length??null,bodyText:d.body?.innerText?.slice(0,300)??null}:{accessible:false,reason:'No accessible embedded document'};}catch(e){observation={accessible:false,error:String(e)};}
    return {viewport:innerWidth,scroll:document.documentElement.scrollWidth,mainCount:document.querySelectorAll('main#main').length,h1Count:document.querySelectorAll('h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor,iframeSrc:f.getAttribute('src'),iframeTitle:f.title,iframeBounds:{width:r.width,height:r.height},iframeObservation:observation};
   });
   await page.keyboard.press('Tab');state.firstFocus=await page.evaluate(()=>document.activeElement?.getAttribute('href'));
   state.layoutChecks={widthFits:state.viewport===width&&state.scroll===width,oneMainAndTitle:state.mainCount===1&&state.h1Count===1,whiteArial:state.font.startsWith('Arial')&&state.background==='rgb(255, 255, 255)',skipLinkFirst:state.firstFocus==='#main'};
   views.push({name,...state});
   for(const [suffix,locator] of [['full',null],['result','#result'],['abstract','#original-abstract']]){
    const p='renders/'+name+'-'+suffix+'.png';if(locator)await page.locator(locator).screenshot({path:own(p)});else await page.screenshot({path:own(p),fullPage:true});screenshots.push(p);
   }
  }
 }catch(e){fatal=String(e);process.exitCode=1;}
 finally{
  if(browser){try{await browser.close();}catch(e){cleanupErrors.push(String(e));process.exitCode=1;}}
  try{fs.rmSync(work,{recursive:true,force:true});}catch(e){cleanupErrors.push(String(e));process.exitCode=1;}
 }
 const sameInputs=JSON.stringify(before)===JSON.stringify(inputs());
 const receipt={UTC:new Date().toISOString(),render_invocations:1,method:'Installed headless Chrome local-file layout; no server or live requests',inputs:before,inputs_unchanged:sameInputs,views,screenshots,all_page_requests:requests,remote_page_requests:remote,failed_requests:failed,page_errors:errors,console_errors:consoleErrors,fatal_exception:fatal,cleanup_errors:cleanupErrors,PDF_viewer_limitations:['Headless local-file PDF frames may be blank, inaccessible or unsupported even with no page error.','The unchanged five-page native PDF was separately read visually during the source-first pass.','These captures do not certify native desktop or live PDF-reader behavior.'],publication_authority:false};
 fs.writeFileSync(own('RENDER_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt,null,2));if(!sameInputs)process.exitCode=1;
}

// Copyright (c) 2026 Alec Kriebel. CC BY 4.0; see LICENSES.md.
// One bounded read-only editorial data check, or one offline HTML render.
// No source program, scientific checker, old builder, live request or publication.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const own=p=>path.join(root,p),source=path.resolve(root,'../../sources'),programme=path.resolve(root,'../../../..');
const read=p=>fs.readFileSync(p),sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const pin=p=>{const b=read(p);return {bytes:b.length,SHA256:sha(b)};};
const need=(v,m)=>{if(!v)throw new Error(m);};
const norm=s=>s.trim().replace(/\s+/g,' ');
const decode=s=>s.replaceAll('&quot;','"').replaceAll('&#x27;',"'").replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&');
const plain=s=>norm(decode(s.replace(/<[^>]+>/g,'')));
const mode=process.argv.slice(2);need(mode.length===0||(mode.length===1&&mode[0]==='--render'),'Only default or --render');
for(const p of ['OWNED_MANIFEST.json','FINAL.json']){
 const s=fs.lstatSync(own(p));need(s.isFile()&&!s.isSymbolicLink()&&read(own(p)).equals(Buffer.from('{}\n')),'Pre-final exact terminal '+p);
}
const html=read(own('preview/index.html')).toString(),main=html.match(/<main id="main">[\s\S]*?<\/main>/g),head=html.match(/<head>[\s\S]*?<\/head>/g);
need(main?.length===1&&head?.length===1,'One complete MAIN and head');
const inputNames=['preview/index.html','preview/research.css','preview/citation.bib','MAIN.html','PAGE_MODEL.json','preview_tools.mjs','preview/focal_antipedal_sum.pdf','preview/focal_antipedal_sum_support.zip'];
const inputs=()=>Object.fromEntries(inputNames.map(p=>[p,pin(own(p))]));
if(mode.length===0){
 const model=JSON.parse(read(own('PAGE_MODEL.json')));
 for(const row of [model.source_first.INITIAL,model.source_first.seal,model.source_first.source_pins,model.source_first.log]){
  need(JSON.stringify(pin(own(row.path)))===JSON.stringify({bytes:row.bytes,SHA256:row.SHA256}),'Frozen initial '+row.path);
 }
 for(const row of [model.root_scientific_clearance,model.root_report]){
  need(JSON.stringify(pin(path.join(programme,row.path)))===JSON.stringify({bytes:row.bytes,SHA256:row.SHA256}),'Exact opened root authority');
 }
 const tex=read(path.join(source,'published-source/container-001/tree/focal_antipedal_sum.tex')).toString();
 need(sha(tex)==='c942322cf81a5083e0bc9a7c0ebe07b2604db75b68ef56b0258afbf28a149e64','Actual controlling TeX');
 const original=norm(tex.split('\\begin{abstract}')[1].split('\\end{abstract}')[0]);
 const visible=html.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>[\s\S]*?<\/section>/)?.[1];
 const scholarly=JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
 const dc=decode(html.match(/<meta name="DC.description" content="([^"]*)">/)[1]);
 need(plain(visible)===original&&scholarly.abstract===original&&dc===original&&model.full_original_abstract===original,'Whole original abstract in four representations');
 need(scholarly.name===model.native_title&&scholarly.version==='1.0'&&scholarly.datePublished==='2026-10-06'&&scholarly.license==='https://creativecommons.org/licenses/by/4.0/','Scholarly metadata');
 need(read(own('MAIN.html')).toString()===main[0]+'\n','Whole saved MAIN');
 for(const row of [model.whole_page,model.MAIN_file,model.stylesheet,model.BibTeX]){
  need(JSON.stringify(pin(own(row.path)))===JSON.stringify({bytes:row.bytes,SHA256:row.SHA256}),'Whole authored input '+row.path);
 }
 const rb=read(path.join(source,'record.response.body')),fb=read(path.join(source,'files-23191247.response.body'));
 need(sha(rb)==='5bedec67b8591dc42b39a10ed5c424d4958f43e58aa8d31ddf524971b595ee61'&&sha(fb)==='43173e80fe6b9591a6f91ac6992360e5cadfa618f51fb10d453c9b348efcb10e','Exact native API bytes');
 const record=JSON.parse(rb),files=JSON.parse(fb),meta=model.native_metadata;
 need(record.metadata.title===model.native_title&&record.metadata.version===meta.version&&record.metadata.publication_date===meta.publication_date&&record.created===meta.created&&record.updated===meta.updated&&record.state===meta.state,'Native title/edition/dates/state');
 need(!Object.hasOwn(record,'is_published')&&meta.is_published.present===false&&meta.is_published.original_value===null&&files.order.length===0&&files.default_preview===null,'Preserve native absence and literal file order field');
 need(JSON.stringify(record.metadata.creators[0])===JSON.stringify(meta.creator)&&JSON.stringify(record.metadata.resource_type)===JSON.stringify(meta.resource_type)&&record.metadata.license.id===meta.record_license,'Native author/type/rights');
 need(files.entries.map(f=>f.key).join('|')==='focal_antipedal_sum.pdf|focal_antipedal_sum_support.zip'&&record.files.map(f=>f.key).join('|')===files.entries.map(f=>f.key).join('|'),'Literal PDF then ZIP order');
 need(sha(read(path.join(source,'published-source/container-001/tree/LICENSE')))==='3556504678d5d85b82f57b70aaf40e16ee13461931a03c49d17c52d3868438e0','Actual CC BY 4.0 license');
 const assets=model.native_assets_in_order.map((row,i)=>{
  const b=read(own(row.path)),native=read(path.join(source,'assets',row.key)),f=files.entries[i],md5=crypto.createHash('md5').update(b).digest('hex');
  need(b.equals(native)&&b.length===row.bytes&&sha(b)===row.SHA256&&md5===row.native_MD5&&f.key===row.key&&f.size===b.length&&f.checksum==='md5:'+md5&&record.files[i].checksum===f.checksum,'Whole native asset '+row.key);
  return {path:row.path,...pin(own(row.path))};
 });
 const downloads=[...html.match(/<ol id="native-downloads">([\s\S]*?)<\/ol>/)[1].matchAll(/<li><a href="([^"]+)"/g)].map(m=>m[1]);
 need(downloads.join('|')===files.entries.map(f=>f.key).join('|'),'Visible native download order');
 need(html.includes('src="focal_antipedal_sum.pdf#view=FitH"')&&html.includes('title="Original four-page manuscript:'),'Original local reader target');
 need(html.includes('name="robots" content="noindex, nofollow, noarchive"')&&!/<link[^>]+rel="canonical"/.test(html),'Private noindex/no canonical');
 need(model.canonical_url===null&&model.base_url===null&&model.production_url===null&&model.AA===null&&model.follow_up===null&&model.publication_authority===false,'No public authority/question');
 need(!main[0].includes('native-description')&&!main[0].includes('Original Zenodo description')&&!/\bMIT\b/.test(html)&&!main[0].includes('358 exact'),'No duplicated Description, internal count narrative or MIT inference');
 for(const text of ['ordinary positive Euclidean norms','other caustic tangent','immediate retracing is excluded','odd primitive periods','neither individual sum is claimed constant','0 &lt; λ &lt; b²','original orbit polygon','final books and author sources','continued-open-status guarantee','including authored code','conventional independent human or journal peer review','actual scholarly contributions']){
  need(main[0].includes(text),'Required scope/status '+text);
 }
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);need(new Set(ids).size===ids.length,'Unique HTML IDs');
 const hrefs=[...html.matchAll(/\bhref="([^"]+)"/g)].map(m=>m[1]);
 need(hrefs.filter(h=>h.startsWith('#')).every(h=>ids.includes(h.slice(1))),'Local fragment targets');
 for(const h of hrefs.filter(h=>!h.startsWith('/')&&!h.startsWith('#')&&!/^[a-z]+:/i.test(h))){
  need(fs.lstatSync(own('preview/'+h.split('#')[0])).isFile(),'Existing local href '+h);
 }
 const bib=read(own('preview/citation.bib')).toString();need(bib.includes('doi = {10.5281/zenodo.23191247}')&&bib.includes('version = {1.0}')&&bib.includes('day = {6}'),'Native Bib metadata');
 console.log(JSON.stringify({status:'PRIVATE_EDITORIAL_DATA_PASS',mode:'read-only',writes:0,record_id:23191247,inputs:inputs(),whole_MAIN:{bytes:Buffer.byteLength(main[0]),SHA256:sha(main[0])},whole_head:{bytes:Buffer.byteLength(head[0]),SHA256:sha(head[0])},assets,full_abstract_equal:true,initial_four_unchanged:true,publication_authority:false},null,2));
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
   await page.setViewportSize({width,height});await page.goto(pathToFileURL(own('preview/index.html')).href,{waitUntil:'load'});
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
 const receipt={UTC:new Date().toISOString(),render_invocations:1,method:'Installed headless Chrome local-file layout; no server or live requests',inputs:before,inputs_unchanged:sameInputs,views,screenshots,all_page_requests:requests,remote_page_requests:remote,failed_requests:failed,page_errors:errors,console_errors:consoleErrors,fatal_exception:fatal,cleanup_errors:cleanupErrors,PDF_viewer_limitations:['Headless local-file PDF frames may be blank, inaccessible or unsupported even with no page error.','The unchanged four-page native PDF was separately read visually during the source-first pass.','These captures do not certify native desktop or live PDF-reader behavior.'],publication_authority:false};
 fs.writeFileSync(own('RENDER_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify(receipt,null,2));if(!sameInputs)process.exitCode=1;
}

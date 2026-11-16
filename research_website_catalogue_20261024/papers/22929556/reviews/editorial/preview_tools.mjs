// SPDX-License-Identifier: MIT
// Fixed private-page data check; --render explicitly creates six local-file views.
// No source/science programs, old helpers, HTTP fetch, server or publication action.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
import {fileURLToPath,pathToFileURL} from 'node:url';
const P='/Users/alec/Documents/Math/research_website_catalogue_20261024';
const O=path.join(P,'papers/22929556/reviews/editorial');
const V=path.join(O,'preview');
const SELF=fileURLToPath(import.meta.url);
const need=(ok,why)=>{if(!ok)throw new Error(why);};
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const pin=b=>({bytes:b.length,SHA256:hash(b)});
function read(p){
  need(path.isAbsolute(p),'Absolute read');
  for(let q=p;;q=path.dirname(q)){need(!fs.lstatSync(q).isSymbolicLink(),'No symlink input');if(path.dirname(q)===q)break;}
  need(fs.lstatSync(p).isFile(),'Regular input');return fs.readFileSync(p);
}
function bound(row){
  const p=path.isAbsolute(row.path)?row.path:path.join(P,row.path),b=read(p);
  need(b.length===row.bytes&&hash(b)===row.SHA256,'Whole bound input '+p);return b;
}
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const decode=s=>s.replace(/&#x([0-9a-f]+);/gi,(_,x)=>String.fromCodePoint(parseInt(x,16))).replace(/&#([0-9]+);/g,(_,x)=>String.fromCodePoint(+x)).replace(/&quot;/g,'"').replace(/&apos;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const text=s=>decode(s.replace(/<[^>]*>/g,'')).replace(/\s+/g,' ').trim();
function check(){
  need(SELF===path.join(O,'preview_tools.mjs'),'Fixed helper path');
  const initialRaw=read(path.join(O,'INITIAL.json'));
  need(hash(initialRaw)==='d673ec5e7400863af1fac3b8db1a4eb7eb98e9a9d6fe8e3caf571e218d52e634','Immutable source INITIAL');
  const initial=JSON.parse(initialRaw),model=JSON.parse(read(path.join(O,'PAGE_MODEL.json')));
  for(const row of initial.source_pins)bound(row);
  need(same(JSON.parse(bound(model.native_source_record_reference)).metadata,model.native_metadata_original),'Whole original native metadata');
  need(same(model.native_metadata_original,initial.native_metadata_original)&&!Object.hasOwn(model.native_metadata_original,'version'),'Native version ABSENT');
  need(model.native_version_field.present===false&&model.native_version_field.original_value===null&&model.printed_version==='1.0.1','Printed edition distinguished');
  need(same(JSON.parse(bound(model.native_source_files_reference)),model.native_files_response)&&same(model.native_record_files,initial.native_record_files_original),'Original file objects/response');
  const authority=JSON.parse(bound(model.authority_reference));
  need(model.authority_reference.bytes===1760&&model.authority_reference.SHA256==='e2caaafe00085906c4de7e50c3b6a80cafdeac5fc33463f1e59f4b323c28baef','Actual root clearance pin');
  bound(model.bound_ROOT_REVIEW_reference);
  need(authority.status==='ROOT_FULL_ORIGINAL_SCIENTIFIC_PASS'&&authority.original_claim_preserved&&authority.repair_or_narrowing===false&&authority.publication_authority===false,'Full-original private copy authority');
  const pageRaw=read(path.join(V,'index.html')),page=pageRaw.toString(),main=page.match(/<main\b[\s\S]*?<\/main>/)?.[0],head=page.match(/<head>[\s\S]*?<\/head>/)?.[0];
  need(main&&head&&same(pin(Buffer.from(main)),model.whole_MAIN)&&same(pin(Buffer.from(head)),model.whole_head)&&same(pin(pageRaw),model.whole_page),'Whole MAIN/head/page pins');
  const metas={};for(const tag of page.matchAll(/<meta\s+([^>]+)>/g)){
    const a=Object.fromEntries([...tag[1].matchAll(/([\w:-]+)="([^"]*)"/g)].map(m=>[m[1],decode(m[2])])),key=a.name??a.property;
    if(key){need(!Object.hasOwn(metas,key),'Unique meta key');metas[key]=a.content;}
  }
  const article=JSON.parse(page.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  const abstract=text(main.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>/)[1]);
  need(abstract===initial.complete_manuscript_abstract&&article.abstract===abstract&&metas['DC.description']===abstract&&model.abstract===abstract,'Complete source abstract visible/JSONLD/DC');
  need(metas.citation_title===initial.native_metadata_original.title&&article.name===metas.citation_title&&metas.citation_author_orcid==='https://orcid.org/0009-0001-9320-500X','Native identity/ORCID');
  need(metas.citation_publication_date==='2026/09/23'&&metas.citation_date==='2026/09/23'&&article.datePublished==='2026-09-23'&&metas.citation_version===article.version&&article.version==='1.0.1','Printed version/original date metadata');
  need(model.native_created==='2026-09-24T03:43:53.253905+00:00'&&main.includes('printed manuscript')&&main.includes('supplies no version field'),'Creation date/native absence distinction visible');
  need(metas.robots==='noindex, nofollow, noarchive'&&!/<link[^>]+rel="canonical"/.test(page),'Private noindex/canonical unset');
  for(const k of ['canonical_url','base_url','production_url','AA','follow_up'])need(model[k]===null,'Private unset '+k);
  need(model.publication_authority===false&&article.creativeWorkStatus==='Unrefereed preprint','Private unrefereed status');
  const ids=[...page.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
  need(new Set(ids).size===ids.length&&(page.match(/<h1>/g)||[]).length===1&&(page.match(/<main id="main">/g)||[]).length===1,'Unique IDs/main/H1');
  const plain=text(main);
  for(const s of ['a, b, c, d, cd, bd, ac.','P = {(d, cd), (c, bd), (b, ac)}.','VP = {(d, cd)}.','zero gradient paths from ac to b','bd → d → cd → c.','V′ = {(d, bd), (c, cd)}','ac → c → cd → d → bd → b','same example works over every field','No minimality claim','actual scholarly contributions'])need(plain.includes(s),'Faithful source/copy '+s);
  need(!main.includes('native-description')&&!main.includes('Original Zenodo description')&&!main.includes(initial.native_metadata_original.description),'No duplicate archive Description');
  need(!main.includes('ROOT_REVIEW')&&!main.includes('scientific review;')&&!main.includes('audit completed on'),'No dated internal review replay');
  const names=initial.native_assets_in_order.map(a=>a.original_native_file_object.key);
  need(same(article.encoding.map(a=>a.name),names)&&same(model.native_assets.map(a=>a.original_file_object),initial.native_record_files_original),'Original native asset order');
  const assets=[];for(let n=0;n<names.length;n++){
    const original=bound(initial.native_assets_in_order[n].source),copy=read(path.join(V,names[n])),row=initial.native_record_files_original[n];
    need(original.equals(copy)&&crypto.createHash('md5').update(copy).digest('hex')===row.checksum.slice(4),'Native asset whole bytes/MD5');assets.push({name:names[n],...pin(copy),native_MD5:row.checksum});
  }
  const sums=read(path.join(V,'SHA256SUMS')).toString().trim().split('\n');need(sums.length===2,'Two original checksum entries');
  for(const line of sums){const m=line.match(/^([0-9a-f]{64})  (paper\.pdf|source-and-verification\.zip)$/);need(m&&hash(read(path.join(V,m[2])))===m[1],'Original SHA256SUMS content');}
  need(metas.citation_pdf_url==='paper.pdf'&&page.includes('src="paper.pdf#view=FitH"'),'Local unchanged PDF citation/embed');
  const list=main.match(/<ol id="native-downloads">([\s\S]*?)<\/ol>/)[1];need(same([...list.matchAll(/<a href="([^"]+)" download>/g)].map(m=>m[1]),names),'Visible native order');
  for(const m of page.matchAll(/(?:href|src)="([^"]+)"/g)){
    const u=m[1];if(u.startsWith('https://')||u.startsWith('/'))continue;
    if(u.startsWith('#')){need(ids.includes(u.slice(1)),'Local fragment');continue;}
    const local=u.split('#')[0];need(!local.includes('..')&&fs.statSync(path.join(V,local)).isFile(),'Local resource');
  }
  const expected=['SHA256SUMS','citation.bib','index.html','paper.pdf','research.css','source-and-verification.zip'];
  need(same(fs.readdirSync(V).sort(),expected),'Exact six preview files');
  const css=read(path.join(V,'research.css'));need(css.length===1170&&hash(css)==='f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a','Unchanged1170BsharedCSS');
  const bib=read(path.join(V,'citation.bib')).toString();need(bib.includes(initial.native_metadata_original.title)&&bib.includes('native Zenodo version field absent')&&bib.includes('version = {1.0.1}')&&bib.includes('10.5281/zenodo.22929556'),'Printed-edition Bib identity');
  return {status:'PASS_PRIVATE_EDITORIAL_DATA_CHECK',record_id:22929556,whole_MAIN:pin(Buffer.from(main)),whole_head:pin(Buffer.from(head)),whole_page:pin(pageRaw),page_model:pin(read(path.join(O,'PAGE_MODEL.json'))),BibTeX:pin(Buffer.from(bib)),native_assets:assets,abstract_complete_visible_JSONLD_DC:true,native_version_field_present:false,printed_version:'1.0.1',private_noindex:true,canonical_url:null,AA:null,follow_up:null,publication_authority:false,source_programs_executed:0,helper:pin(read(SELF)),writes:0};
}
function exclusive(p,data){need(p.startsWith(O+path.sep),'Owned write');fs.writeFileSync(p,data,{flag:'wx',mode:0o644});}
async function render(checked){
  const renderDir=path.join(O,'renders'),tempRoot=path.join(O,'render-temp');
  need(!fs.existsSync(renderDir)&&!fs.existsSync(tempRoot)&&!fs.existsSync(path.join(O,'RENDER_RECEIPT.json')),'Single explicit fresh private render');
  fs.mkdirSync(renderDir,{mode:0o755});fs.mkdirSync(tempRoot,{mode:0o700});
  process.env.TMPDIR=tempRoot;
  const require=createRequire(import.meta.url),{chromium}=require('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core');
  let context;const remoteRequests=[],errors=[],views=[];
  try{
    context=await chromium.launchPersistentContext(path.join(tempRoot,'profile'),{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,acceptDownloads:false,downloadsPath:path.join(tempRoot,'downloads'),viewport:{width:1100,height:900},args:['--disable-background-networking','--disable-sync','--disable-component-update','--disable-default-apps','--disable-breakpad','--no-first-run','--metrics-recording-only','--no-proxy-server'],env:{...process.env,TMPDIR:tempRoot}});
    await context.setOffline(true);
    await context.route('**/*',async route=>{const u=route.request().url();if(/^(file:|data:|blob:|chrome-extension:)/.test(u))await route.continue();else{remoteRequests.push({method:route.request().method(),url:u});await route.abort();}});
    const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));
    for(const [name,width]of[['desktop',1100],['mobile',390]]){
      await page.setViewportSize({width,height:900});await page.goto(pathToFileURL(path.join(V,'index.html')).href,{waitUntil:'load',timeout:25000});
      await page.evaluate(async()=>{await document.fonts.ready;});await new Promise(r=>setTimeout(r,1500));
      const metrics=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth,main:document.querySelectorAll('main').length,h1:document.querySelectorAll('h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor,abstract:document.querySelector('#original-abstract p').textContent,iframe:document.querySelector('iframe').getAttribute('src'),iframeTitle:document.querySelector('iframe').title}));
      need(metrics.viewport===metrics.scroll&&metrics.main===1&&metrics.h1===1&&metrics.font.includes('Arial')&&metrics.background==='rgb(255, 255, 255)','Readable plain layout/no overflow');
      await page.screenshot({path:path.join(renderDir,name+'-full.png'),fullPage:true});
      await page.locator('#original-abstract').screenshot({path:path.join(renderDir,name+'-abstract.png')});
      await page.locator('#result').screenshot({path:path.join(renderDir,name+'-result.png')});
      await page.evaluate(()=>scrollTo(0,0));await page.keyboard.press('Tab');metrics.firstFocus=await page.locator(':focus').getAttribute('href');views.push({name,...metrics});
    }
    need(remoteRequests.length===0&&errors.length===0,'No remote page request or page error');
  }finally{
    if(context)await context.close();
    need(path.dirname(tempRoot)===O&&fs.lstatSync(tempRoot).isDirectory()&&!fs.lstatSync(tempRoot).isSymbolicLink(),'Owned temporary profile cleanup');fs.rmSync(tempRoot,{recursive:true});
  }
  const names=fs.readdirSync(renderDir).sort();need(names.length===6,'Six saved views');
  const images=names.map(name=>{const b=read(path.join(renderDir,name));need(b.subarray(1,4).toString()==='PNG','PNG view');return {path:'renders/'+name,...pin(b),width:b.readUInt32BE(16),height:b.readUInt32BE(20)};});
  const receipt={UTC:new Date().toISOString(),method:'Installed headless Chrome local-file layout; no live/native desktop PDF-viewer certification.',inputs:{'preview/index.html':checked.whole_page,'preview/research.css':pin(read(path.join(V,'research.css'))),'preview_tools.mjs':checked.helper},views,images,remote_page_requests:remoteRequests,page_errors:errors,native_assets_verified_whole_bytes:true,scientific_or_old_helper_execution:false,temporary_profile_removed:true,publication_authority:false};
  exclusive(path.join(O,'RENDER_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');return {status:'SIX_PRIVATE_LOCAL_FILE_VIEWS_SAVED',receipt:pin(read(path.join(O,'RENDER_RECEIPT.json'))),images,publication_authority:false};
}
const args=process.argv.slice(2);need(args.length===0||(args.length===1&&args[0]==='--render'),'Only read-only default or explicit private --render');
const checked=check();console.log(JSON.stringify(args.length?await render(checked):checked,null,2));

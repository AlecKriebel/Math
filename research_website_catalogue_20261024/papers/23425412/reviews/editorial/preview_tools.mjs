// Authored private utility, CC BY 4.0. Default is read-only; explicit render/seal only.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)), source=path.resolve(root,'../../sources'), programme=path.resolve(root,'../../../..');
const own=p=>path.join(root,p), read=p=>fs.readFileSync(p), sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const pin=p=>{const b=read(p);return {bytes:b.length,SHA256:sha(b)};};
const need=(v,m)=>{if(!v)throw new Error(m);}, same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const save=(p,v)=>fs.writeFileSync(own(p),JSON.stringify(v,null,2)+'\n');
const args=process.argv.slice(2); need(args.length<=1 && (!args.length || ['--render','--seal'].includes(args[0])),'Only default, --render, --seal');
const mode=args[0]||'read-only';
if(fs.existsSync(own('FINAL.json')))need(read(own('FINAL.json')).equals(Buffer.from('{}\n')),'Frozen: no further utility execution');
const html=read(own('preview/index.html')).toString(), main=html.match(/<main id="main">[\s\S]*?<\/main>/g), head=html.match(/<head>[\s\S]*?<\/head>/g);
need(main?.length===1 && head?.length===1,'One complete MAIN/head');
const record=JSON.parse(read(path.join(source,'record.response.body'))), files=JSON.parse(read(path.join(source,'files-23425412.response.body')));
const tex=read(path.join(source,'published-source/container-001/tree/paper/main.tex')).toString();
const abstract=tex.split('\\begin{abstract}')[1].split('\\end{abstract}')[0].trim().replace(/~/g,' ').replace(/\$/g,'').replaceAll('\\slie_n','sl_n').replaceAll("Poincar\\'e",'Poincaré').replaceAll('0,-6,-24','0,−6,−24').replace(/\s+/g,' ');
need(html.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>/)?.[1]===abstract,'Complete original abstract');
need(html.match(/<div id="native-description">([\s\S]*?)<\/div>/)?.[1]===record.metadata.description,'Whole four-paragraph native Description');
need(record.metadata.version==='1.0' && record.metadata.publication_date==='2026-10-16' && files.default_preview===null && files.order.length===0,'Literal native fields');
need(record.files.map(f=>f.key).join('|')==='habiro-rank-interpolation-v1.0.pdf|habiro-rank-interpolation-verification-v1.0.zip','Native order');
const assets=record.files.map(f=>{const p=own('preview/'+f.key),b=read(p);need(b.equals(read(path.join(source,'assets',f.key))) && b.length===f.size && 'md5:'+crypto.createHash('md5').update(b).digest('hex')===f.checksum,'Whole original asset '+f.key);return {path:'preview/'+f.key,...pin(p),original_file_object:f};});
need(html.includes('habiro-rank-interpolation-v1.0.pdf#view=FitH') && html.includes('name="robots" content="noindex, nofollow, noarchive"') && !/<link[^>]+rel="canonical"/.test(html) && !main[0].includes('Private preview'),'Private head and local PDF');
const initial=pin(own('INITIAL.md')), initialSeal=pin(own('INITIAL_SEAL.json'));need(initial.SHA256==='9a6f2bde6d5224358c1283cc1fb00b1301428a455043ca779aca97078ad87205' && initialSeal.SHA256==='c8f1fe70586ff6b2a6cceed03a11d0eefbffd245ab82b4b3ca3d95fd678d08e4','Frozen INITIAL');
const authority='verification/root-clearance-23425412-20261116.json';need(pin(path.join(programme,authority)).SHA256==='e59886b63d3b77fad6aebc56701b88b94e220ec6ba614d5a8fa40d9b8338505f','Opened authority');
const inputs=()=>Object.fromEntries(['preview/index.html','preview/research.css','preview_tools.mjs'].map(p=>[p,pin(own(p))]));
if(mode==='read-only'){
  console.log(JSON.stringify({mode,writes:0,record_id:23425412,whole_MAIN:{bytes:Buffer.byteLength(main[0]),SHA256:sha(main[0])},inputs:inputs(),native_assets:assets.map(({original_file_object,...a})=>a)},null,2));
}else if(mode==='--render'){
  need(!fs.existsSync(own('FINAL.json')) && !fs.existsSync(own('render-work')),'Fresh pre-final render');
  const before=inputs(),work=own('render-work');fs.mkdirSync(work);fs.mkdirSync(path.join(work,'tmp'));fs.mkdirSync(own('renders'),{recursive:true});let browser;
  try{
    const {chromium}=await import('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.mjs');
    browser=await chromium.launchPersistentContext(path.join(work,'profile'),{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,env:{...process.env,TMPDIR:path.join(work,'tmp')},args:['--disable-background-networking','--disable-component-update','--disable-default-apps','--disable-sync','--no-first-run','--no-default-browser-check','--disable-domain-reliability','--metrics-recording-only','--disable-features=OptimizationHints,MediaRouter,AutofillServerCommunication']});
    const remote=[],errors=[],views=[];await browser.route('**/*',r=>{const u=r.request().url();if(/^(file:|data:|about:|chrome-extension:|chrome:\/\/resources\/)/.test(u))return r.continue();remote.push(u);return r.abort();});
    const page=await browser.newPage();page.on('pageerror',e=>errors.push(String(e)));
    for(const [name,width,height] of [['desktop',1100,900],['mobile',390,844]]){
      await page.setViewportSize({width,height});await page.goto(pathToFileURL(own('preview/index.html')).href,{waitUntil:'load'});await page.waitForTimeout(750);
      const state=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth,main:document.querySelectorAll('main#main').length,h1:document.querySelectorAll('h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor,iframe:document.querySelector('iframe').getAttribute('src'),iframeTitle:document.querySelector('iframe').title,description:document.querySelector('#native-description').innerHTML}));
      need(state.viewport===state.scroll && state.scroll===width && state.main===1 && state.h1===1 && state.font.startsWith('Arial') && state.background==='rgb(255, 255, 255)' && state.description===record.metadata.description,'Layout/Description '+name);
      await page.keyboard.press('Tab');const focus=await page.evaluate(()=>document.activeElement?.getAttribute('href'));need(focus==='#main','Skip link first');
      await page.screenshot({path:own('renders/'+name+'-full.png'),fullPage:true});await page.locator('#result').screenshot({path:own('renders/'+name+'-result.png')});await page.locator('#original-abstract').screenshot({path:own('renders/'+name+'-abstract.png')});views.push({name,...state,firstFocus:focus});
    }
    need(remote.length===0 && errors.length===0 && same(before,inputs()),'No remote page requests/errors or changed render inputs');
    save('RENDER_RECEIPT.json',{UTC:new Date().toISOString(),inputs:before,views,remote_page_requests:remote,page_errors:errors,method:'Local-file headless Chrome layout only; no live/native desktop PDF-viewer certification.',native_assets_verified_whole_bytes:true});console.log(JSON.stringify({render:'completed',widths:views.map(v=>[v.name,v.viewport,v.scroll]),screenshots:6,remote_page_requests:remote.length,page_errors:errors.length}));
  }finally{if(browser)await browser.close();fs.rmSync(work,{recursive:true,force:true});}
}else{
  for(const p of ['OWNED_MANIFEST.json','FINAL.json']){const s=fs.lstatSync(own(p));need(s.isFile() && !s.isSymbolicLink() && read(own(p)).equals(Buffer.from('{}\n')),'Exact existing ordinary terminal '+p);}
  need(same(JSON.parse(read(own('RENDER_RECEIPT.json'))).inputs,inputs()),'Current whole page/CSS/helper bound to saved images');
  for(const p of JSON.parse(read(own('INITIAL_SEAL.json'))).finite_initial_payload){const b=read(own(p.path));need(sha(p.path==='RESEARCH_LOG.md'?b.subarray(0,p.bytes):b)===p.SHA256,'Initial payload '+p.path);}
  const model={record_id:23425412,sheet_row:146,native_metadata:record.metadata,native_record_files:record.files,native_files_response:files,native_created:record.created,native_modified:record.modified,native_updated:record.updated,native_record_status:record.status,native_is_published:{present:Object.hasOwn(record,'is_published'),original_value:record.is_published??null},printed_date:'16 October 2026',printed_version:'1.0',source_FINAL_reference:{path:'papers/23425412/sources/SOURCE_FINAL.json',...pin(path.join(source,'SOURCE_FINAL.json')),historical_unread_false_null_fields_unchanged:true},authority_reference:{path:authority,...pin(path.join(programme,authority))},source_first_INITIAL:initial,source_first_seal:initialSeal,proposed_slug:'habiro-rank-interpolation-obstruction',canonical_url:null,base_url:null,production_url:null,AA:null,follow_up:null,publication_authority:false,private_noindex:true,rights:{native_authored_work_including_code:'CC-BY-4.0',new_editorial_and_utility:'CC-BY-4.0',third_party_rights_retained:true},whole_MAIN:{bytes:Buffer.byteLength(main[0]),SHA256:sha(main[0])},whole_head:{bytes:Buffer.byteLength(head[0]),SHA256:sha(head[0])},whole_page:pin(own('preview/index.html')),native_assets:assets,render_receipt:pin(own('RENDER_RECEIPT.json'))};save('PAGE_MODEL.json',model);
  const manifest={UTC:new Date().toISOString(),root,directories:['.'],files:[],only_exact_already_existing_root_controls_excluded:['OWNED_MANIFEST.json','FINAL.json'],ignored_native_assets_rasters_and_images_included:true};
  const walk=r=>{for(const e of fs.readdirSync(own(r),{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))){const p=r?r+'/'+e.name:e.name;need(!e.isSymbolicLink(),'No symlink '+p);if(e.isDirectory()){manifest.directories.push(p);walk(p);}else{need(e.isFile(),'Ordinary file '+p);if(!['OWNED_MANIFEST.json','FINAL.json'].includes(p))manifest.files.push({path:p,...pin(own(p))});}}};walk('');save('OWNED_MANIFEST.json',manifest);
  save('FINAL.json',{UTC:new Date().toISOString(),status:'PRIVATE_EDITORIAL_CANDIDATE_FROZEN',record_id:23425412,editorial_completion_percent:100,publication_authority:false,canonical_url:null,AA:null,follow_up:null,manifest:{path:'OWNED_MANIFEST.json',...pin(own('OWNED_MANIFEST.json'))},actual_files:manifest.files.length+2,actual_directories_including_owned_root:manifest.directories.length,whole_MAIN:model.whole_MAIN,whole_head:model.whole_head,whole_page:model.whole_page,page_model:pin(own('PAGE_MODEL.json')),BibTeX:pin(own('preview/citation.bib')),current_helper:pin(own('preview_tools.mjs')),render_receipt:model.render_receipt,source_first_INITIAL:initial,source_first_seal:initialSeal,immutable_after_this_seal:true});
  console.log(JSON.stringify({FINAL:pin(own('FINAL.json')),manifest:pin(own('OWNED_MANIFEST.json')),whole_MAIN:model.whole_MAIN,files:manifest.files.length+2,directories_including_owned_root:manifest.directories.length},null,2));
}

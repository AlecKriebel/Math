// Authored private editorial utility. CC BY 4.0; see LICENSES.md.
// Default is read-only. Only explicit --render and --seal modes write this owned folder.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath, pathToFileURL} from 'node:url';
const owned = path.dirname(fileURLToPath(import.meta.url));
const source = path.resolve(owned, '../../sources');
const programme = path.resolve(owned, '../../../..');
const read = p => fs.readFileSync(p);
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const pin = p => ({bytes:read(p).length, SHA256:sha(read(p))});
const own = p => path.join(owned,p);
const requireThat = (v,m) => {if(!v) throw new Error(m);};
const writeJSON = (p,v) => fs.writeFileSync(own(p),JSON.stringify(v,null,2)+'\n');
const args = process.argv.slice(2);
requireThat(args.length<=1 && (!args.length || ['--render','--seal'].includes(args[0])),'Only default, --render or --seal is supported');
const mode = args[0] || 'read-only';
if(fs.existsSync(own('FINAL.json'))) requireThat(read(own('FINAL.json')).equals(Buffer.from('{}\n')),'Frozen packet: utility execution is closed');
const pagePath=own('preview/index.html'), html=read(pagePath).toString('utf8');
const main=html.match(/<main id="main">[\s\S]*?<\/main>/g), head=html.match(/<head>[\s\S]*?<\/head>/g);
requireThat(main?.length===1 && head?.length===1,'Exactly one complete MAIN and head');
const record=JSON.parse(read(path.join(source,'record.response.body'))), files=JSON.parse(read(path.join(source,'files.response.body')));
const tex=read(path.join(source,'published-source/asset-002/verification_kit/preprint.tex')).toString('utf8');
const abstract=tex.split('\\begin{abstract}')[1].split('\\end{abstract}')[0].trim().replace(/\$/g,'').replace(/\\geq/g,'≥').replace(/\\leq/g,'≤').replace(/--/g,'–').replace(/\s+/g,' ');
const abstractHTML=html.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>/)?.[1];
requireThat(abstractHTML===abstract,'Complete original abstract fidelity');
requireThat(html.match(/<div id="native-description"><p>([\s\S]*?)<\/p><\/div>/)?.[1]===record.metadata.description,'Whole native Description fidelity');
requireThat(record.metadata.version==='1.0' && record.metadata.publication_date==='2026-10-14','Native edition');
requireThat(record.files.map(x=>x.key).join('|')==='preprint.pdf|verification_kit.zip' && files.default_preview===null && files.order.length===0,'Original native order/nulls');
const assets=record.files.map(f=>{const p=own('preview/'+f.key), original=read(path.join(source,'assets',f.key)), b=read(p); requireThat(b.equals(original) && b.length===f.size && 'md5:'+crypto.createHash('md5').update(b).digest('hex')===f.checksum,'Unchanged native asset '+f.key); return {path:'preview/'+f.key,...pin(p),original_file_object:f};});
requireThat(html.includes('preprint.pdf#view=FitH') && html.includes('name="robots" content="noindex, nofollow, noarchive"') && !/<link[^>]+rel="canonical"/.test(html),'Private PDF/head contract');
requireThat(!main[0].includes('Private preview') && html.includes('including authored code') && html.includes('Creative Commons Attribution 4.0 International'),'Public body/rights');
const inputs=()=>Object.fromEntries(['preview/index.html','preview/research.css','preview_tools.mjs'].map(p=>[p,pin(own(p))]));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const initial=pin(own('INITIAL.md')), initialSeal=pin(own('INITIAL_SEAL.json'));
requireThat(initial.SHA256==='e5217641d6467223bfa9232b47326b9d11049f9b3970336230da08dd1b07f3b1' && initialSeal.SHA256==='d40888bfe00b478ef57abe7db53c18e488adfac89eaca5d11c5ed1f7302cd342','Frozen source-first INITIAL');
const authority='verification/root-clearance-23430927-20261116.json';
requireThat(pin(path.join(programme,authority)).SHA256==='ca1d6fdd4293e9135e1342c38cb42cb135cabe2f090c1c97f8c326b6b39c3c84','Actual opened authority');
if(mode==='read-only') {
  console.log(JSON.stringify({mode,writes:0,record_id:23430927,complete_MAIN:{bytes:Buffer.byteLength(main[0]),SHA256:sha(main[0])},inputs:inputs(),native_assets:assets.map(({original_file_object,...x})=>x)},null,2));
} else if(mode==='--render') {
  requireThat(!fs.existsSync(own('FINAL.json')) && !fs.existsSync(own('render-work')),'Fresh pre-final render');
  const before=inputs(), work=own('render-work'); fs.mkdirSync(work); fs.mkdirSync(path.join(work,'tmp')); fs.mkdirSync(own('renders'),{recursive:true});
  let browser;
  try {
    const {chromium}=await import('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.mjs');
    browser=await chromium.launchPersistentContext(path.join(work,'profile'),{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,env:{...process.env,TMPDIR:path.join(work,'tmp')},args:['--disable-background-networking','--disable-component-update','--disable-default-apps','--disable-sync','--no-first-run','--no-default-browser-check','--disable-domain-reliability','--metrics-recording-only','--disable-features=OptimizationHints,MediaRouter,AutofillServerCommunication']});
    const blocked=[],errors=[]; await browser.route('**/*',r=>{const u=r.request().url(); if(/^(file:|data:|about:|chrome-extension:|chrome:\/\/resources\/)/.test(u)) return r.continue(); blocked.push(u); return r.abort();});
    const page=await browser.newPage(); page.on('pageerror',e=>errors.push(String(e))); const views=[];
    for(const [name,width,height] of [['desktop',1100,900],['mobile',390,844]]) {
      await page.setViewportSize({width,height}); await page.goto(pathToFileURL(pagePath).href,{waitUntil:'load'}); await page.waitForTimeout(750);
      const state=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth,main:document.querySelectorAll('main#main').length,h1:document.querySelectorAll('h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor,iframe:document.querySelector('iframe').getAttribute('src'),iframeTitle:document.querySelector('iframe').title,description:document.querySelector('#native-description').textContent}));
      requireThat(state.scroll===width && state.main===1 && state.h1===1 && state.font.startsWith('Arial') && state.background==='rgb(255, 255, 255)' && state.description===record.metadata.description,'Layout and full Description '+name);
      await page.keyboard.press('Tab'); const firstFocus=await page.evaluate(()=>document.activeElement?.getAttribute('href')); requireThat(firstFocus==='#main','Keyboard skip link'); await page.keyboard.press('Escape');
      await page.screenshot({path:own('renders/'+name+'-full.png'),fullPage:true});
      await page.locator('#result').screenshot({path:own('renders/'+name+'-result.png')});
      await page.locator('#original-abstract').screenshot({path:own('renders/'+name+'-abstract.png')}); views.push({name,...state,firstFocus});
    }
    requireThat(blocked.length===0 && errors.length===0,'No blocked remote page request or page script error'); requireThat(equal(before,inputs()),'Render inputs unchanged');
    writeJSON('RENDER_RECEIPT.json',{UTC:new Date().toISOString(),inputs:before,views,blocked_remote_page_requests:blocked,page_errors:errors,method:'Installed headless Chrome with local file page; saved layout screenshots. Native PDF viewer pixels are not certified by these renders.',native_assets_whole_byte_verified:true});
    console.log(JSON.stringify({render:'completed',views:views.map(v=>({name:v.name,viewport:v.viewport,scroll:v.scroll})),screenshots:6,remote_page_requests:blocked.length,page_errors:errors.length}));
  } finally {if(browser) await browser.close(); fs.rmSync(work,{recursive:true,force:true});}
} else {
  for(const terminal of ['OWNED_MANIFEST.json','FINAL.json']) {const p=own(terminal); requireThat(fs.lstatSync(p).isFile() && !fs.lstatSync(p).isSymbolicLink() && read(p).equals(Buffer.from('{}\n')),'Exact existing ordinary terminal '+terminal);}
  const receipt=JSON.parse(read(own('RENDER_RECEIPT.json'))); requireThat(equal(receipt.inputs,inputs()),'Saved screenshots bind the current whole HTML/CSS/helper');
  for(const p of JSON.parse(read(own('INITIAL_SEAL.json'))).finite_initial_payload) {const b=read(own(p.path)); requireThat(sha(p.path==='RESEARCH_LOG.md'?b.subarray(0,p.bytes):b)===p.SHA256,'Initial payload preserved '+p.path);}
  const model={record_id:23430927,sheet_row:144,title:record.metadata.title,native_metadata:record.metadata,native_record_files:record.files,native_files_response:files,native_created:record.created,native_modified:record.modified,native_updated:record.updated,native_status:record.status,printed_designation:'Version 1.0 preparation candidate, 14 October 2026 UTC',historical_pending_review_text_preserved_in_unchanged_PDF:true,source_ready_seal_reference:{path:'papers/23430927/sources/SOURCE_READY_SEAL.json',...pin(path.join(source,'SOURCE_READY_SEAL.json')),historical_unread_flags_unchanged:true},authority_reference:{path:authority,...pin(path.join(programme,authority))},source_first_INITIAL:initial,source_first_seal:initialSeal,proposed_slug:'restricted-boundary-twist-factorizations',canonical_url:null,base_url:null,production_url:null,AA:null,follow_up:null,publication_authority:false,private_noindex:true,rights:{native_authored_note_and_kit_including_code:'CC-BY-4.0',new_editorial_and_utility:'CC-BY-4.0',third_party_rights_retained:true},whole_MAIN:{bytes:Buffer.byteLength(main[0]),SHA256:sha(main[0])},whole_head:{bytes:Buffer.byteLength(head[0]),SHA256:sha(head[0])},whole_page:pin(pagePath),native_assets:assets,render_receipt:pin(own('RENDER_RECEIPT.json'))};
  writeJSON('PAGE_MODEL.json',model);
  const manifest={UTC:new Date().toISOString(),root:owned,directories:['.'],files:[],only_exact_already_existing_root_controls_excluded:['OWNED_MANIFEST.json','FINAL.json'],ignored_assets_and_rasters_included:true};
  const walk=relative=>{for(const e of fs.readdirSync(own(relative),{withFileTypes:true}).sort((a,b)=>a.name.localeCompare(b.name))){const r=relative?relative+'/'+e.name:e.name; requireThat(!e.isSymbolicLink(),'No symlinks '+r); if(e.isDirectory()){manifest.directories.push(r);walk(r);} else {requireThat(e.isFile(),'Ordinary payload '+r); if(!['OWNED_MANIFEST.json','FINAL.json'].includes(r))manifest.files.push({path:r,...pin(own(r))});}}}; walk('');
  writeJSON('OWNED_MANIFEST.json',manifest);
  writeJSON('FINAL.json',{UTC:new Date().toISOString(),status:'PRIVATE_EDITORIAL_CANDIDATE_FROZEN',record_id:23430927,editorial_completion_percent:100,scientific_review_delegated_here:false,publication_authority:false,canonical_url:null,AA:null,follow_up:null,manifest:{path:'OWNED_MANIFEST.json',...pin(own('OWNED_MANIFEST.json'))},actual_files:manifest.files.length+2,actual_directories_including_owned_root:manifest.directories.length,whole_MAIN:model.whole_MAIN,whole_head:model.whole_head,whole_page:model.whole_page,page_model:pin(own('PAGE_MODEL.json')),BibTeX:pin(own('preview/citation.bib')),current_helper:pin(own('preview_tools.mjs')),source_first_INITIAL:initial,source_first_seal:initialSeal,render_receipt:model.render_receipt,immutable_after_this_seal:true});
  console.log(JSON.stringify({FINAL:pin(own('FINAL.json')),manifest:pin(own('OWNED_MANIFEST.json')),whole_MAIN:model.whole_MAIN,files:manifest.files.length+2,directories_including_owned_root:manifest.directories.length},null,2));
}

// Bounded private editorial data/layout utility; no scientific program imports.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const self=fileURLToPath(import.meta.url),here=path.dirname(self),project=path.resolve(here,'../../../..');
const args=process.argv.slice(2),read=n=>fs.readFileSync(path.join(here,n)),parse=n=>JSON.parse(read(n));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),pin=b=>({bytes:b.length,sha256:sha(b)});
const need=(v,m)=>{if(!v)throw new Error(m);},same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const decode=s=>s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#x27;/g,"'").replace(/&amp;/g,'&');
const text=s=>decode(s.replace(/<[^>]*>/g,'')).replace(/\s+/g,' ').trim();
function filePin(p){const st=fs.lstatSync(p);need(st.isFile()&&!st.isSymbolicLink(),'Regular file '+p);return {...pin(fs.readFileSync(p)),mode:'0o'+(st.mode&0o777).toString(8)};}
function matchPin(p,q){const x=filePin(p);need(x.bytes===q.bytes&&x.sha256===q.sha256&&(!q.mode||x.mode===q.mode),'Exact pin '+p);}
function walk(dir,prefix=''){
 const files=[],directories=[];
 for(const name of fs.readdirSync(dir).sort()){
  const p=path.join(dir,name),rel=prefix?prefix+'/'+name:name,st=fs.lstatSync(p);
  need(!st.isSymbolicLink(),'No source symlinks');
  if(st.isDirectory()){directories.push(rel);const r=walk(p,rel);files.push(...r.files);directories.push(...r.directories);}
  else{need(st.isFile(),'Regular source file');files.push(rel);}
 }
 return {files:files.sort(),directories:directories.sort()};
}
function check(){
 need(args.length===0||same(args,['--render']),'Only read-only default or explicit --render');
 matchPin(path.join(here,'INITIAL.json'),{bytes:15083,sha256:'352d38ea28827fe5dc410216f8d669c3ed0d9f2dd658af640fc8028cea27e666'});
 matchPin(path.join(here,'INITIAL_SEAL.json'),{bytes:3038,sha256:'ebf1ce78f3f7706d0aa928601562d220366c221d955a6f3792b79241b2a8d804'});
 const initial=parse('INITIAL.json'),seal=parse('INITIAL_SEAL.json'),custody=parse('SOURCE_CUSTODY.json'),model=parse('PAGE_MODEL.json');
 for(const q of seal.payload_pins)matchPin(path.join(here,q.path),q);
 for(const q of seal.reused_six_source_images_pins)matchPin(path.join(project,q.path),q);
 const source=path.join(project,custody.source_root),extent=walk(source);
 need(extent.files.length===206&&extent.directories.length===25&&same(extent.files,custody.files.map(x=>x.path).sort())&&same(extent.directories,custody.directories),'Entire source namespace unchanged');
 for(const q of custody.files)matchPin(path.join(source,q.path),q);
 const native=JSON.parse(fs.readFileSync(path.join(source,'record.response.body'))),files=JSON.parse(fs.readFileSync(path.join(source,'files-23398175.response.body')));
 const authored=JSON.parse(fs.readFileSync(path.join(source,'published-source/container-001/tree/k605a_outer_focal_pedal_product/metadata.json')));
 need(same(model.native_metadata_original,native.metadata)&&same(model.native_record_files,native.files)&&same(model.native_files_response,files)&&same(model.authored_metadata_original,authored),'Whole native/authored objects');
 need(native.metadata.version==='1.0'&&authored.version==='1.0'&&native.metadata.publication_date==='2026-10-15'&&native.created==='2026-10-15T14:26:52.483806+00:00','Original dates/version');
 need(!Object.hasOwn(native,'is_published')&&model.native_is_published_field==='ABSENT'&&model.printed_version===null,'No invented native boolean/printed version');
 const clearancePath=path.join(project,'verification/root-clearance-23398175-20261116.json');
 matchPin(clearancePath,{bytes:2033,sha256:'9fbb46f56dcfccc3cc61bea4ab19bca8938302aa6c50340c9e3d235a789af5e5'});
 const clearance=JSON.parse(fs.readFileSync(clearancePath));
 matchPin(path.join(project,clearance.root_review.path),{bytes:10709,sha256:'8289c40c9551f25e8a6f09accf9830177873e54885ac3d4994664342101e93d2'});
 need(clearance.status==='PASS_FULL_ORIGINAL_CLAIMS_NO_REPAIR_OR_NARROWING'&&clearance.follow_up===null&&clearance.central_proof_gap===null,'Actual full-original private clearance');
 const pageBytes=read('preview/index.html'),html=pageBytes.toString(),main=html.match(/<main\b[^>]*>[\s\S]*?<\/main>/)[0],head=html.match(/<head\b[^>]*>[\s\S]*?<\/head>/)[0];
 need(read('MAIN.html').equals(Buffer.from(main))&&same(pin(pageBytes),model.whole_page)&&same(pin(Buffer.from(main)),model.whole_MAIN)&&same(pin(Buffer.from(head)),model.whole_head),'Whole head/page/MAIN model binding');
 const meta=new Map([...head.matchAll(/<meta (?:name|property)="([^"]+)" content="([^"]*)">/g)].map(m=>[m[1],decode(m[2])]));
 const article=JSON.parse(head.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
 const tex=fs.readFileSync(path.join(source,'published-source/container-001/tree/k605a_outer_focal_pedal_product/manuscript.tex'),'utf8');
 const raw=tex.match(/\\begin\{abstract\}\s*([\s\S]*?)\s*\\end\{abstract\}/)[1];
 const abstract=raw.replace(/\s+/g,' ').replaceAll('$k_{605,a}$','k605,a').replaceAll('$k_{606}$','k606').trim();
 const visible=main.match(/<section id="original-abstract">[\s\S]*?<p>([\s\S]*?)<\/p>/)[1];
 need(raw===initial.whole_original_abstract_tex&&raw===model.abstract_tex&&abstract===model.abstract&&abstract===article.abstract&&abstract===meta.get('DC.description')&&abstract===text(visible),'Complete original abstract visible/schema/DC');
 need(visible.includes('k<sub>605,a</sub>')&&visible.includes('k<sub>606</sub>'),'Exact abstract index meaning');
 need(text(main.match(/<h1>([\s\S]*?)<\/h1>/)[1])===native.metadata.title&&article.name===native.metadata.title&&meta.get('citation_title')===native.metadata.title,'Full original title');
 need(article.datePublished==='2026-10-15'&&article.version==='1.0'&&meta.get('citation_publication_date')==='2026/10/15'&&meta.get('citation_version')==='1.0','Scholarly edition fields');
 need(article.author.identifier==='https://orcid.org/0009-0001-9320-500X'&&article.identifier.value===native.doi&&meta.get('citation_doi')===native.doi,'DOI/ORCID');
 for(const key of ['description','og:description','twitter:description'])need(meta.get(key)===model.meta_description,'Summary agreement '+key);
 need(decode(head.match(/<title>(.*?)<\/title>/)[1])===model.seo_title,'SEO title');
 need(meta.get('robots')==='noindex, nofollow, noarchive'&&!/<link\b[^>]*rel="canonical"/i.test(head)&&!/<base\b/i.test(head)&&!meta.has('og:url'),'Private URL/indexing state');
 for(const key of ['canonical_url','base_url','production_url','AA','follow_up'])need(model[key]===null,'Null '+key);
 need(model.publication_authority===false&&model.visible_duplicate_description===false&&!html.includes(native.metadata.description),'No publication authority/visible duplicate Description');
 need(native.metadata.license.id==='cc-by-4.0'&&authored.license==='cc-by-4.0'&&article.license==='https://creativecommons.org/licenses/by/4.0/'&&model.rights.no_invented_MIT_split&&!/\bMIT\b/.test(main),'Native rights without MIT split');
 need(!/Original Zenodo description|ROOT_REVIEW|root-clearance|2026-11-16|96 exact|internal audit/.test(main),'No internal verification narrative');
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 need(new Set(ids).size===ids.length&&(html.match(/<main\b/g)||[]).length===1&&(html.match(/<h1\b/g)||[]).length===1,'Unique IDs/one MAIN/H1');
 for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){
  const value=decode(m[1]);if(value.startsWith('https://'))continue;
  if(value.startsWith('#')){need(ids.includes(value.slice(1)),'Local fragment '+value);continue;}
  if(value.startsWith('/')){need(['/','/research/'].includes(value),'Existing site navigation');continue;}
  const leaf=value.split('#')[0];need(leaf&&!leaf.includes('/')&&fs.lstatSync(path.join(here,'preview',leaf)).isFile(),'Exact local resource '+value);
 }
 need(meta.get('citation_pdf_url')==='k605a-outer-focal-pedal-areas.pdf'&&main.includes('src="k605a-outer-focal-pedal-areas.pdf#view=FitH"')&&main.includes('href="k605a-outer-focal-pedal-areas.pdf" target="_blank"'),'PDF citation/open/embed');
 const downloads=main.match(/<ol id="native-downloads">([\s\S]*?)<\/ol>/)[1];
 const names=[...downloads.matchAll(/<li><a href="([^"]+)" download>/g)].map(x=>x[1]);
 need(same(names,['k605a-outer-focal-pedal-areas.pdf','k605a-source-verification.zip'])&&same(names,native.files.map(x=>x.key)),'PDF-first ZIP-second native order');
 const assets=[];
 for(let i=0;i<native.files.length;i++){
  const f=native.files[i],b=read('preview/'+f.key),original=fs.readFileSync(path.join(source,'assets',f.key));
  need(b.equals(original)&&b.length===f.size&&'md5:'+crypto.createHash('md5').update(b).digest('hex')===f.checksum,'Unchanged native asset '+f.key);
  need(article.encoding[i].contentUrl===f.key&&article.encoding[i].sameAs===f.links.self,'Encoding source order/link');assets.push({name:f.key,...pin(b),native_MD5:f.checksum});
 }
 need(same(fs.readdirSync(path.join(here,'preview')).sort(),['citation.bib','index.html','k605a-outer-focal-pedal-areas.pdf','k605a-source-verification.zip','research.css']),'Exact five preview leaves');
 need(same(pin(read('preview/research.css')),{bytes:1170,sha256:'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'}),'Unchanged shared style');
 const bib=read('preview/citation.bib');need(same(pin(bib),model.BibTeX)&&bib.toString().includes('version = {1.0}')&&bib.toString().includes(native.doi)&&bib.toString().includes('CC-BY-4.0'),'Bib native edition/rights');
 const explanation=[...main.matchAll(/<p data-explanation>([\s\S]*?)<\/p>/g)].map(x=>text(x[1])).join(' '),words=explanation.split(/\s+/).length;
 need(words===model.explanatory_words_excluding_full_abstract_metadata_resources_citation_references&&words>=600&&words<=900,'Light bounded explanation');
 for(const phrase of ['odd least period N ≥ 3','strictly nested, nondegenerate confocal elliptical caustic','original foci','signed shoelace area','s<sup>2</sup>','products are 16 and 25','Khare and Sukhatme','Ferudun','Historical priority of this particular application remains undetermined','No independent human peer review or formal proof-assistant verification','work actually contributed'])need(main.includes(phrase),'Scope/credit '+phrase);
 return {timestamp_utc:new Date().toISOString(),status:'PASS_PRIVATE_EDITORIAL_DATA_CHECK',record_id:23398175,whole_page:pin(pageBytes),whole_MAIN:pin(Buffer.from(main)),whole_head:pin(Buffer.from(head)),page_model:pin(read('PAGE_MODEL.json')),BibTeX:pin(bib),native_assets:assets,source_guards:206,source_directories:25,original_source_first_files_unchanged:7,abstract_visible_ScholarlyArticle_DC:true,explanation_words:words,private_noindex:true,canonical_url:null,AA:null,follow_up:null,publication_authority:false,scientific_program_executions:0,helper:pin(fs.readFileSync(self)),writes:0};
}
async function render(data){
 const dir=path.join(here,'renders'),temp=path.join(here,'render-temp');
 for(const q of [dir,temp,path.join(here,'RENDER_RECEIPT.json'),path.join(here,'CHECK_RECEIPT.json')])need(!fs.existsSync(q),'Exclusive one-pass output '+q);
 fs.writeFileSync(path.join(here,'CHECK_RECEIPT.json'),JSON.stringify(data,null,2)+'\n',{flag:'wx'});fs.mkdirSync(dir);fs.mkdirSync(temp);
 const require=createRequire(import.meta.url),{chromium}=require('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core');
 const diagnostics={nonlocal_page_routes_aborted:[],page_errors:[],console_errors:[],console_warnings:[],failed_requests:[]},captures=[],layouts=[];let context=null,failure=null;
 try{
  context=await chromium.launchPersistentContext(path.join(temp,'profile'),{headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',downloadsPath:path.join(temp,'downloads'),env:{...process.env,TMPDIR:temp},args:['--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run','--no-default-browser-check','--disable-features=MediaRouter,OptimizationHints']});
  await context.setOffline(true);
  await context.route('**/*',async route=>{const u=route.request().url();if(/^(file:|data:|blob:|chrome-extension:)/.test(u))await route.continue();else{diagnostics.nonlocal_page_routes_aborted.push(u);await route.abort();}});
  const page=await context.newPage();page.on('pageerror',e=>diagnostics.page_errors.push(e.message));
  page.on('console',m=>{if(m.type()==='error')diagnostics.console_errors.push(m.text());if(m.type()==='warning')diagnostics.console_warnings.push(m.text());});
  page.on('requestfailed',q=>diagnostics.failed_requests.push({url:q.url(),error:q.failure()?.errorText??null}));
  for(const [label,width] of [['desktop',1100],['mobile',390]]){
   await page.setViewportSize({width,height:900});await page.goto(pathToFileURL(path.join(here,'preview/index.html')).href,{waitUntil:'load'});await page.waitForTimeout(350);
   const layout=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth,MAINs:document.querySelectorAll('main').length,H1s:document.querySelectorAll('h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor}));
   need(layout.viewport===layout.scroll&&layout.MAINs===1&&layout.H1s===1&&layout.font.includes('Arial')&&layout.background==='rgb(255, 255, 255)','White Arial/no horizontal overflow '+label);layouts.push({label,...layout});
   for(const [name,selector] of [['full',null],['abstract','#original-abstract'],['result','#result']]){
    const target=path.join(dir,`${label}-${name}.png`);if(selector)await page.locator(selector).screenshot({path:target});else await page.screenshot({path:target,fullPage:true});
    const b=fs.readFileSync(target);captures.push({path:path.relative(here,target),...pin(b),width:b.readUInt32BE(16),height:b.readUInt32BE(20)});
   }
  }
 }catch(e){failure=String(e.stack??e);}
 finally{
  if(context)try{await context.close();}catch(e){diagnostics.console_errors.push('Context close: '+String(e));failure=failure??String(e);}
  fs.rmSync(temp,{recursive:true,force:false});
 }
 const receipt={timestamp_utc:new Date().toISOString(),status:failure?'RENDER_INCOMPLETE_FAILURE_RETAINED':'SIX_HTML_LAYOUT_VIEWS_SAVED',method:'One installed headless Chrome offline local-file pass; not a native desktop/live reader test.',explicit_render_invocations:1,inputs:{whole_page:data.whole_page,helper:data.helper},layouts,captures,diagnostics,failure,context_offline:true,temporary_owned_profile_removed:!fs.existsSync(temp),actual_embedded_PDF_display_certified:false,PDF_limitation:'The saved HTML iframe appearance does not certify actual native/live/mobile-hardware PDF display or a completed download. Direct-open/embed/download links and unchanged bytes are checked statically.',scientific_program_executions:0,publication_authority:false};
 fs.writeFileSync(path.join(here,'RENDER_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n',{flag:'wx'});
 if(failure)throw new Error(failure);return receipt;
}
const data=check();
if(args.length===0)process.stdout.write(JSON.stringify(data,null,2)+'\n');
else process.stdout.write(JSON.stringify({check:data,render:await render(data)},null,2)+'\n');

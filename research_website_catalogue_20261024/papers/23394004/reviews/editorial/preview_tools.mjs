// Bounded private editorial data/layout utility. CC BY 4.0. No scientific code is loaded.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const self=fileURLToPath(import.meta.url),here=path.dirname(self),project=path.resolve(here,'../../../..');
const mode=process.argv.slice(2),read=n=>fs.readFileSync(path.join(here,n)),parse=n=>JSON.parse(read(n));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const pin=b=>({bytes:b.length,sha256:sha(b)}),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const need=(v,m)=>{if(!v)throw new Error(m);};
const decode=s=>s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#x27;/g,"'").replace(/&amp;/g,'&');
const text=s=>decode(s.replace(/<[^>]*>/g,'')).replace(/\s+/g,' ').trim();

function check(){
  need(mode.length===0||same(mode,['--render']),'Only read-only default or explicit --render supported');
  const initialBytes=read('INITIAL.json');
  need(same(pin(initialBytes),{bytes:32803,sha256:'21a0ecc3e7155f47d33b538b1d3d683fe5a761cac66489c91ed7ead73832014d'}),'Immutable source-first INITIAL');
  const initial=JSON.parse(initialBytes),seal=parse('INITIAL_SEAL.json'),model=parse('PAGE_MODEL.json');
  need(same(pin(read('INITIAL_SEAL.json')),{bytes:1145,sha256:'1ecaa6c37d949c755178637832573a6c13a4b2d13b0f8e7a7025dd7e2435e379'}),'Immutable source-first seal');
  for(const q of seal.content_pins)need(same(pin(fs.readFileSync(path.join(project,q.path))),{bytes:q.bytes,sha256:q.sha256}),'Frozen source-first payload '+q.path);
  for(const q of initial.source_pins){
    const file=path.join(project,q.path);
    need(fs.lstatSync(file).isFile()&&!fs.lstatSync(file).isSymbolicLink()&&same(pin(fs.readFileSync(file)),{bytes:q.bytes,sha256:q.sha256}),'Unchanged source '+q.path);
  }
  const native=JSON.parse(fs.readFileSync(path.join(project,'papers/23394004/sources/record.response.body')));
  const files=JSON.parse(fs.readFileSync(path.join(project,'papers/23394004/sources/files-23394004.response.body')));
  const authored=JSON.parse(fs.readFileSync(path.join(project,'papers/23394004/sources/published-source/container-001/tree/k904a_outer_focal_inverse_product/metadata.json')));
  need(same(model.authored_metadata_original,authored)&&authored.license==='cc-by-4.0'&&authored.version==='1.0'&&model.rights.separate_LICENSE_present===false,'Actual authored metadata and rights');
  need(same(model.native_metadata_original,native.metadata)&&same(model.native_record_files,native.files)&&same(model.native_files_response,files),'Whole original native objects');
  need(native.metadata.version==='1.0'&&native.metadata.publication_date==='2026-10-15'&&native.created==='2026-10-15T11:39:15.137334+00:00','Native version/date/creation');
  need(!Object.hasOwn(native,'is_published')&&model.native_is_published_field==='ABSENT'&&model.printed_version===null,'Absent native boolean/printed version');
  const clearanceBytes=fs.readFileSync(path.join(project,'verification/root-clearance-23394004-20261116.json'));
  need(same(pin(clearanceBytes),{bytes:1627,sha256:'c3819ef78fa9fb2fc585d072d3a0822cfa91792711bd67e3ee748c5fb97dc4bf'}),'Actual clearance');
  const clearance=JSON.parse(clearanceBytes),review=fs.readFileSync(path.join(project,clearance.root_report.path));
  need(review.length===5802&&sha(review)==='2e1c30e4fcd90a1342d0aac43e0c6f5ac693839212238e52bc909593233a44a0'&&clearance.status==='FULL_ORIGINAL_SCIENTIFIC_PASS'&&clearance.follow_up===null&&!clearance.repair_or_narrowing,'Bound full-original disposition');
  const pageBytes=read('preview/index.html'),html=pageBytes.toString();
  const main=html.match(/<main\b[^>]*>[\s\S]*?<\/main>/)[0],head=html.match(/<head\b[^>]*>[\s\S]*?<\/head>/)[0];
  need(read('MAIN.html').equals(Buffer.from(main))&&same(pin(pageBytes),model.whole_page)&&same(pin(Buffer.from(main)),model.whole_MAIN)&&same(pin(Buffer.from(head)),model.whole_head),'Whole copy/head/MAIN bindings');
  const meta=new Map([...head.matchAll(/<meta (?:name|property)="([^"]+)" content="([^"]*)">/g)].map(m=>[m[1],decode(m[2])]));
  const article=JSON.parse(head.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  const tex=fs.readFileSync(path.join(project,'papers/23394004/sources/published-source/container-001/tree/k904a_outer_focal_inverse_product/manuscript.tex'),'utf8');
  const raw=tex.match(/\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}/)[1].trim();
  const abstract=raw.replace(/\s+/g,' ').trim();
  const section=main.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>[\s\S]*?<\/section>/)[1];
  const visibleAbstract=text(section);
  need(raw===model.abstract_tex&&abstract===model.abstract&&abstract===article.abstract&&abstract===meta.get('DC.description')&&abstract===visibleAbstract,'Complete source abstract visible/schema/DC with index meaning');
  need(article.name===native.metadata.title&&meta.get('citation_title')===native.metadata.title&&text(main.match(/<h1>(.*?)<\/h1>/)[1])===native.metadata.title,'Full native title');
  need(article.datePublished==='2026-10-15'&&article.version==='1.0'&&meta.get('citation_version')==='1.0'&&meta.get('citation_publication_date')==='2026/10/15','Scholarly date/version');
  need(article.author.identifier==='https://orcid.org/0009-0001-9320-500X'&&article.identifier.value===native.doi&&meta.get('citation_doi')===native.doi,'Author/DOI');
  for(const key of ['description','og:description','twitter:description'])need(meta.get(key)===model.meta_description,'Consistent unique summary '+key);
  need(meta.get('robots')==='noindex, nofollow, noarchive'&&!/<link\b[^>]*rel="canonical"/i.test(head)&&!/<base\b/i.test(head),'Private indexing state');
  for(const key of ['canonical_url','base_url','production_url','AA','follow_up'])need(model[key]===null,'Null '+key);
  need(model.publication_authority===false&&model.visible_duplicate_description===false,'No public authority/duplicate Description');
  need(native.metadata.license.id==='cc-by-4.0'&&article.license==='https://creativecommons.org/licenses/by/4.0/'&&model.rights.no_invented_MIT_split&&!/\bMIT\b/.test(main),'Exact rights without MIT inference');
  need(!/Original Zenodo description|ROOT_REVIEW|root-clearance|2026-11-16|FULL_ORIGINAL_SCIENTIFIC_PASS/.test(main),'No internal review replay');
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);need(new Set(ids).size===ids.length,'Unique IDs');
  need((html.match(/<main\b/g)||[]).length===1&&(html.match(/<h1\b/g)||[]).length===1,'One MAIN/H1');
  for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){
    const value=decode(m[1]);
    if(value.startsWith('https://'))continue;
    if(value.startsWith('#')){need(ids.includes(value.slice(1)),'Fragment '+value);continue;}
    if(value.startsWith('/')){need(['/','/research/'].includes(value),'Site navigation');continue;}
    const local=value.split('#')[0];need(local&&!local.includes('/')&&fs.lstatSync(path.join(here,'preview',local)).isFile(),'Local leaf '+value);
  }
  need(meta.get('citation_pdf_url')==='k904a-outer-focal-inverse-areas.pdf'&&main.includes('src="k904a-outer-focal-inverse-areas.pdf#view=FitH"')&&main.includes('href="k904a-outer-focal-inverse-areas.pdf" target="_blank"'),'PDF citation/open/embed');
  const downloads=main.match(/<ol id="native-downloads">([\s\S]*?)<\/ol>/)[1];
  const names=[...downloads.matchAll(/<li><a href="([^"]+)" download>/g)].map(m=>m[1]);
  need(same(names,['k904a-source-verification.zip','k904a-outer-focal-inverse-areas.pdf'])&&same(names,native.files.map(f=>f.key)),'Native ZIP then PDF order');
  const assets=[];
  for(let i=0;i<native.files.length;i++){
    const f=native.files[i],bytes=read('preview/'+f.key),source=fs.readFileSync(path.join(project,'papers/23394004/sources/assets',f.key));
    need(bytes.equals(source)&&bytes.length===f.size&&'md5:'+crypto.createHash('md5').update(bytes).digest('hex')===f.checksum,'Unchanged native asset '+f.key);
    need(article.encoding[i].contentUrl===f.key&&article.encoding[i].sameAs===f.links.self,'Original native encoding URL');
    assets.push({name:f.key,...pin(bytes),native_MD5:f.checksum});
  }
  need(same(fs.readdirSync(path.join(here,'preview')).sort(),['citation.bib','index.html','k904a-outer-focal-inverse-areas.pdf','k904a-source-verification.zip','research.css']),'Exact five preview leaves');
  need(same(pin(read('preview/research.css')),{bytes:1170,sha256:'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'}),'Unchanged shared style');
  const bib=read('preview/citation.bib');need(bib.toString().includes('version = {1.0}')&&bib.toString().includes(native.doi)&&bib.toString().includes('CC-BY-4.0'),'Bib edition/DOI/rights');
  for(const phrase of ['least odd period N ≥ 3','strictly nested, nondegenerate confocal elliptical caustic','original foci','unit circle','straight segments','signed shoelace areas','positive constant','every real outer vertex','critical triangular case','r<sup>2</sup>','s<sup>−4</sup>','ρ<sup>8</sup>','k904,a','k808,a','Chavez-Caliz','no first-proof, absolute-priority or current-worldwide-open claim','not independent human peer review or formal proof-assistant verification','actual scholarly contributions'])need(main.includes(phrase),'Scope/credit '+phrase);
  return {status:'PASS_PRIVATE_EDITORIAL_DATA_CHECK',record_id:23394004,whole_page:pin(pageBytes),whole_MAIN:pin(Buffer.from(main)),whole_head:pin(Buffer.from(head)),page_model:pin(read('PAGE_MODEL.json')),BibTeX:pin(bib),native_assets:assets,source_guards:initial.source_pins.length,source_first_packet_unchanged:true,full_abstract_visible_JSONLD_DC:true,private_noindex:true,canonical_url:null,AA:null,follow_up:null,publication_authority:false,scientific_program_executions:0,helper:pin(fs.readFileSync(self)),writes:0};
}

async function render(data){
  const dir=path.join(here,'renders'),temp=path.join(here,'render-temp');
  need(!fs.existsSync(dir)&&!fs.existsSync(temp)&&!fs.existsSync(path.join(here,'RENDER_RECEIPT.json')),'Exclusive one-pass outputs');
  fs.mkdirSync(dir);fs.mkdirSync(temp);
  const require=createRequire(import.meta.url),{chromium}=require('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core');
  const diagnostics={nonlocal_page_routes_aborted:[],page_errors:[],console_errors:[],failed_requests:[]};
  const captures=[],layouts=[];let context=null,failure=null;
  try{
    context=await chromium.launchPersistentContext(path.join(temp,'profile'),{headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',downloadsPath:path.join(temp,'downloads'),env:{...process.env,TMPDIR:temp},args:['--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run','--no-default-browser-check','--disable-features=MediaRouter,OptimizationHints']});
    await context.setOffline(true);
    await context.route('**/*',async route=>{const u=route.request().url();if(/^(file:|data:|blob:|chrome-extension:)/.test(u))await route.continue();else{diagnostics.nonlocal_page_routes_aborted.push(u);await route.abort();}});
    const page=await context.newPage();
    page.on('pageerror',e=>diagnostics.page_errors.push(e.message));
    page.on('console',m=>{if(m.type()==='error')diagnostics.console_errors.push(m.text());});
    page.on('requestfailed',q=>diagnostics.failed_requests.push({url:q.url(),error:q.failure()?.errorText??null}));
    for(const [label,width] of [['desktop',1100],['mobile',390]]){
      await page.setViewportSize({width,height:900});
      await page.goto(pathToFileURL(path.join(here,'preview/index.html')).href,{waitUntil:'load'});
      await page.waitForTimeout(350);
      const layout=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth,MAINs:document.querySelectorAll('main').length,H1s:document.querySelectorAll('h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor}));
      need(layout.viewport===layout.scroll&&layout.MAINs===1&&layout.H1s===1&&layout.font.includes('Arial')&&layout.background==='rgb(255, 255, 255)','White Arial layout/no horizontal overflow '+label);
      layouts.push({label,...layout});
      for(const [name,selector] of [['full',null],['abstract','#original-abstract'],['result','#result']]){
        const target=path.join(dir,`${label}-${name}.png`);
        if(selector)await page.locator(selector).screenshot({path:target});else await page.screenshot({path:target,fullPage:true});
        const b=fs.readFileSync(target);captures.push({path:path.relative(here,target),...pin(b),width:b.readUInt32BE(16),height:b.readUInt32BE(20)});
      }
    }
  }catch(e){failure=String(e.stack??e);}
  finally{if(context)await context.close();fs.rmSync(temp,{recursive:true,force:false});}
  const receipt={timestamp_utc:new Date().toISOString(),status:failure?'RENDER_INCOMPLETE_FAILURE_RETAINED':'SIX_HTML_LAYOUT_VIEWS_SAVED',method:'One offline installed headless Chrome local-file pass; no live or native desktop reader certification.',explicit_render_invocations:1,inputs:{whole_page:data.whole_page,helper:data.helper},layouts,captures,diagnostics,failure,context_offline:true,nonlocal_page_routes_aborted:true,temporary_owned_profile_removed:!fs.existsSync(temp),actual_embedded_PDF_display_certified:false,PDF_limitation:'Inspect the saved iframe appearance. No successful live/mobile-hardware/native-desktop PDF display or download is certified by this local HTML layout pass.',scientific_program_executions:0,publication_authority:false};
  fs.writeFileSync(path.join(here,'RENDER_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n',{flag:'wx'});
  if(failure)throw new Error(failure);
  return receipt;
}
const data=check();
if(mode.length===0)process.stdout.write(JSON.stringify(data,null,2)+'\n');
else process.stdout.write(JSON.stringify(await render(data),null,2)+'\n');

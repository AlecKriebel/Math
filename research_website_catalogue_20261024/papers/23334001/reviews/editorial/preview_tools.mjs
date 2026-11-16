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
  need(same(pin(initialBytes),{bytes:25411,sha256:'567777b32be34ce5e24eae412085b82bb469a836645255a0cca999fabb52eb61'}),'Immutable source-first INITIAL');
  const initial=JSON.parse(initialBytes),seal=parse('INITIAL_SEAL.json'),model=parse('PAGE_MODEL.json');
  need(same(pin(read('INITIAL_SEAL.json')),{bytes:1136,sha256:'0d2e4821d24c2ecda5d9d116a64d51e984070e121cb7169335884f91b4d41d25'}),'Immutable source-first seal');
  for(const q of seal.content_pins)need(same(pin(fs.readFileSync(path.join(project,q.path))),{bytes:q.bytes,sha256:q.sha256}),'Frozen source-first payload '+q.path);
  for(const q of initial.source_pins){
    const file=path.join(project,q.path);
    need(fs.lstatSync(file).isFile()&&!fs.lstatSync(file).isSymbolicLink()&&same(pin(fs.readFileSync(file)),{bytes:q.bytes,sha256:q.sha256}),'Unchanged source '+q.path);
  }
  const native=JSON.parse(fs.readFileSync(path.join(project,'papers/23334001/sources/record.response.body')));
  const files=JSON.parse(fs.readFileSync(path.join(project,'papers/23334001/sources/files-23334001.response.body')));
  need(same(model.native_metadata_original,native.metadata)&&same(model.native_record_files,native.files)&&same(model.native_files_response,files),'Whole original native objects');
  need(native.metadata.version==='1.0'&&native.metadata.publication_date==='2026-10-13'&&native.created==='2026-10-13T06:36:40.403085+00:00','Native version/date/creation');
  need(!Object.hasOwn(native,'is_published')&&model.native_is_published_field==='ABSENT'&&model.printed_version===null,'Absent native boolean/printed version');
  const clearanceBytes=fs.readFileSync(path.join(project,'verification/root-clearance-23334001-20261116.json'));
  need(same(pin(clearanceBytes),{bytes:1603,sha256:'43a4f0043c2cdb70ae1de5380c0cf08d6cb0f43797cf71ece0201e04a2ad6244'}),'Actual clearance');
  const clearance=JSON.parse(clearanceBytes),review=fs.readFileSync(path.join(project,clearance.root_report.path));
  need(review.length===6136&&sha(review)==='3da196edeffb1ff0d55ce76ebf4f15ce68dd872af579d36a99129875fa5dde77'&&clearance.status==='FULL_ORIGINAL_SCIENTIFIC_PASS'&&clearance.follow_up===null&&!clearance.repair_or_narrowing,'Bound full-original disposition');
  const pageBytes=read('preview/index.html'),html=pageBytes.toString();
  const main=html.match(/<main\b[^>]*>[\s\S]*?<\/main>/)[0],head=html.match(/<head\b[^>]*>[\s\S]*?<\/head>/)[0];
  need(read('MAIN.html').equals(Buffer.from(main))&&same(pin(pageBytes),model.whole_page)&&same(pin(Buffer.from(main)),model.whole_MAIN)&&same(pin(Buffer.from(head)),model.whole_head),'Whole copy/head/MAIN bindings');
  const meta=new Map([...head.matchAll(/<meta (?:name|property)="([^"]+)" content="([^"]*)">/g)].map(m=>[m[1],decode(m[2])]));
  const article=JSON.parse(head.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  const tex=fs.readFileSync(path.join(project,'papers/23334001/sources/published-source/container-001/tree/odd-origin-area-product-verification/paper/odd_origin_area_product.tex'),'utf8');
  const raw=tex.match(/\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}/)[1].trim();
  const abstract=raw.replace(/\$k_\{403,a\}\$/g,'k_{403,a}').replace(/\s+/g,' ').trim();
  const section=main.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>[\s\S]*?<\/section>/)[1];
  const visibleAbstract=text(section.replace('k<sub>403,a</sub>','k_{403,a}'));
  need(raw===model.abstract_tex&&abstract===model.abstract&&abstract===article.abstract&&abstract===meta.get('DC.description')&&abstract===visibleAbstract,'Complete source abstract visible/schema/DC with index meaning');
  need(article.name===native.metadata.title&&meta.get('citation_title')===native.metadata.title&&text(main.match(/<h1>(.*?)<\/h1>/)[1])===native.metadata.title,'Full native title');
  need(article.datePublished==='2026-10-13'&&article.version==='1.0'&&meta.get('citation_version')==='1.0'&&meta.get('citation_publication_date')==='2026/10/13','Scholarly date/version');
  need(article.author.identifier==='https://orcid.org/0009-0001-9320-500X'&&article.identifier.value===native.doi&&meta.get('citation_doi')===native.doi,'Author/DOI');
  for(const key of ['description','og:description','twitter:description'])need(meta.get(key)===model.meta_description,'Consistent unique summary '+key);
  need(meta.get('robots')==='noindex, nofollow, noarchive'&&!/<link\b[^>]*rel="canonical"/i.test(head)&&!/<base\b/i.test(head),'Private indexing state');
  for(const key of ['canonical_url','base_url','production_url','AA','follow_up'])need(model[key]===null,'Null '+key);
  need(model.publication_authority===false&&model.visible_duplicate_description===false,'No public authority/duplicate Description');
  need(native.metadata.license.id==='cc-by-4.0'&&article.license==='https://creativecommons.org/licenses/by/4.0/'&&model.rights.MIT_not_inferred&&!/\bMIT\b/.test(main),'Exact rights without MIT inference');
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
  need(meta.get('citation_pdf_url')==='odd_origin_area_product.pdf'&&main.includes('src="odd_origin_area_product.pdf#view=FitH"')&&main.includes('href="odd_origin_area_product.pdf" target="_blank"'),'PDF citation/open/embed');
  const downloads=main.match(/<ol id="native-downloads">([\s\S]*?)<\/ol>/)[1];
  const names=[...downloads.matchAll(/<li><a href="([^"]+)" download>/g)].map(m=>m[1]);
  need(same(names,['odd-origin-area-product-verification.zip','odd_origin_area_product.pdf'])&&same(names,native.files.map(f=>f.key)),'Native ZIP then PDF order');
  const assets=[];
  for(let i=0;i<native.files.length;i++){
    const f=native.files[i],bytes=read('preview/'+f.key),source=fs.readFileSync(path.join(project,'papers/23334001/sources/assets',f.key));
    need(bytes.equals(source)&&bytes.length===f.size&&'md5:'+crypto.createHash('md5').update(bytes).digest('hex')===f.checksum,'Unchanged native asset '+f.key);
    need(article.encoding[i].contentUrl===f.key&&article.encoding[i].sameAs===f.links.self,'Original native encoding URL');
    assets.push({name:f.key,...pin(bytes),native_MD5:f.checksum});
  }
  need(same(fs.readdirSync(path.join(here,'preview')).sort(),['citation.bib','index.html','odd-origin-area-product-verification.zip','odd_origin_area_product.pdf','research.css']),'Exact five preview leaves');
  need(same(pin(read('preview/research.css')),{bytes:1170,sha256:'f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a'}),'Unchanged shared style');
  const bib=read('preview/citation.bib');need(bib.toString().includes('version = {1.0}')&&bib.toString().includes(native.doi)&&bib.toString().includes('CC-BY-4.0'),'Bib edition/DOI/rights');
  for(const phrase of ['least odd period N ≥ 3','strictly nested, nondegenerate confocal elliptical caustic','signed shoelace area','all consecutive real antipedal intersections are finite','does not require either derived signed area to be nonzero','225/4 and 289/4','R<sup>4</sup>','r<sup>2</sup>','Reznik, Garcia and Koiller','earlier k<sub>203,b</sub>','No historical-firstness certification','without external human peer review or proof-assistant formalization','actual scholarly contributions'])need(main.includes(phrase),'Scope/credit '+phrase);
  return {status:'PASS_PRIVATE_EDITORIAL_DATA_CHECK',record_id:23334001,whole_page:pin(pageBytes),whole_MAIN:pin(Buffer.from(main)),whole_head:pin(Buffer.from(head)),page_model:pin(read('PAGE_MODEL.json')),BibTeX:pin(bib),native_assets:assets,source_guards:initial.source_pins.length,source_first_packet_unchanged:true,full_abstract_visible_JSONLD_DC:true,private_noindex:true,canonical_url:null,AA:null,follow_up:null,publication_authority:false,scientific_program_executions:0,helper:pin(fs.readFileSync(self)),writes:0};
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

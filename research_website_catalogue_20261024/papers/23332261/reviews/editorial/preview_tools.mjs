// Private editorial utility, CC BY 4.0. No source scientific programs are loaded.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';

const here=path.dirname(fileURLToPath(import.meta.url));
const project=path.resolve(here,'../../../..');
const mode=process.argv.slice(2);
const read=n=>fs.readFileSync(path.join(here,n));
const parse=n=>JSON.parse(read(n));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const need=(yes,message)=>{if(!yes)throw new Error(message);};
const pin=b=>({bytes:b.length,SHA256:sha(b)});
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const decode=s=>s.replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#x27;/g,"'").replace(/&amp;/g,'&');
const text=s=>decode(s.replace(/<[^>]*>/g,'')).replace(/\s+/g,' ').trim();
const mainText=html=>html.match(/<main\b[^>]*>[\s\S]*?<\/main>/)[0];
const headText=html=>html.match(/<head\b[^>]*>[\s\S]*?<\/head>/)[0];

function check(){
  need(mode.length===0||same(mode,['--render']),'Only read-only default or explicit --render supported');
  const initialBytes=read('INITIAL.json');
  need(initialBytes.length===20616&&sha(initialBytes)==='4067b4b66d75bb0ad86b2aeedca59238163331ff710d7350a0ba60d0197b113e','Fixed source-first INITIAL');
  const initial=JSON.parse(initialBytes), model=parse('PAGE_MODEL.json');
  for(const item of initial.source_pins){
    const file=path.join(project,item.path),bytes=fs.readFileSync(file);
    need(!fs.lstatSync(file).isSymbolicLink()&&same(pin(bytes),{bytes:item.bytes,SHA256:item.SHA256}),'Source pin '+item.path);
  }
  const native=JSON.parse(fs.readFileSync(path.join(project,'papers/23332261/sources/record.response.body')));
  const files=JSON.parse(fs.readFileSync(path.join(project,'papers/23332261/sources/files-23332261.response.body')));
  need(same(model.native_metadata_original,native.metadata)&&same(model.native_record_files,native.files)&&same(model.native_files_response,files),'Whole native objects preserved');
  need(native.metadata.version==='1.0.0'&&native.metadata.publication_date==='2026-10-12'&&native.created==='2026-10-13T05:12:09.360305+00:00','Version and two dates');
  need(!Object.hasOwn(native,'is_published')&&model.native_is_published_field==='ABSENT','No invented native boolean');
  const clearancePath=path.join(project,'verification/root-clearance-23332261-20261116.json');
  const clearanceBytes=fs.readFileSync(clearancePath),clearance=JSON.parse(clearanceBytes);
  need(clearanceBytes.length===1618&&sha(clearanceBytes)==='929f0ee55b446d67bb6835571fce44af8344d4ea6adce57110726bd4cdcd1406','Actual scientific clearance pin');
  const review=fs.readFileSync(path.join(project,clearance.root_report.path));
  need(same(pin(review),{bytes:clearance.root_report.bytes,SHA256:clearance.root_report.SHA256})&&clearance.status==='FULL_ORIGINAL_SCIENTIFIC_PASS'&&clearance.follow_up===null,'Bound actual disposition');
  const pageBytes=read('preview/index.html'),html=pageBytes.toString(),main=mainText(html),head=headText(html);
  need(same(pin(pageBytes),model.whole_page)&&same(pin(Buffer.from(main)),model.whole_MAIN)&&same(pin(Buffer.from(head)),model.whole_head),'Whole page, MAIN and head');
  const meta=new Map([...head.matchAll(/<meta (?:name|property)="([^"]+)" content="([^"]*)">/g)].map(m=>[m[1],decode(m[2])]));
  const article=JSON.parse(head.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
  const section=main.match(/<section id="original-abstract"[\s\S]*?<p>([\s\S]*?)<\/p>[\s\S]*?<\/section>/)[1];
  const tex=fs.readFileSync(path.join(project,'papers/23332261/sources/published-source/container-001/tree/preprint/note.tex'),'utf8');
  const abstract=tex.match(/\\begin\{abstract\}\n([\s\S]*?)\n\\end\{abstract\}/)[1].replace('$1<|z|<e$','1 < |z| < e');
  need(abstract===initial.complete_manuscript_abstract&&abstract===model.abstract&&abstract===article.abstract&&abstract===meta.get('DC.description')&&abstract===text(section),'Full original abstract visible, schema and DC');
  need(article.name===native.metadata.title&&meta.get('citation_title')===native.metadata.title&&text(main.match(/<h1>(.*?)<\/h1>/)[1])===native.metadata.title,'Full native title');
  need(article.version==='1.0.0'&&article.datePublished==='2026-10-12'&&meta.get('citation_version')==='1.0.0'&&meta.get('citation_publication_date')==='2026/10/12','Scholarly version/date');
  need(article.author.identifier==='https://orcid.org/0009-0001-9320-500X'&&article.identifier.value===native.doi&&meta.get('citation_doi')===native.doi,'Author ORCID and DOI');
  need(meta.get('description')===model.meta_description&&meta.get('og:description')===model.meta_description&&meta.get('twitter:description')===model.meta_description,'Unique consistent summary');
  need(meta.get('robots')==='noindex, nofollow, noarchive'&&!/<link\b[^>]*rel="canonical"/i.test(head)&&!/<base\b/i.test(head),'Private indexing/canonical state');
  for(const key of ['canonical_url','base_url','production_url','AA','follow_up'])need(model[key]===null,'Null '+key);
  need(model.publication_authority===false,'No public authority');
  need(native.metadata.license.id==='cc-by-4.0'&&article.license==='https://creativecommons.org/licenses/by/4.0/'&&model.rights.MIT_not_inferred&&!/\bMIT\b/.test(main),'Native rights without MIT inference');
  need(!/Original Zenodo description|ROOT_REVIEW|CHECK_RESULTS|root-clearance|2026-11-16/.test(main),'No duplicate Description or dated internal review replay');
  const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);need(new Set(ids).size===ids.length,'Unique IDs');
  need((html.match(/<main\b/g)||[]).length===1&&(html.match(/<h1\b/g)||[]).length===1,'One MAIN and H1');
  for(const m of html.matchAll(/(?:href|src)="([^"]+)"/g)){
    const value=decode(m[1]);
    if(value.startsWith('https://'))continue;
    if(value.startsWith('#')){need(ids.includes(value.slice(1)),'Fragment '+value);continue;}
    if(value.startsWith('/')){need(['/','/research/'].includes(value),'Allowed site navigation');continue;}
    const local=value.split('#')[0];need(local&&!local.includes('/')&&fs.lstatSync(path.join(here,'preview',local)).isFile(),'Local relative leaf '+value);
  }
  need(meta.get('citation_pdf_url')==='annular-martin-kernel-note.pdf'&&main.includes('src="annular-martin-kernel-note.pdf#view=FitH"')&&main.includes('href="annular-martin-kernel-note.pdf" target="_blank"'),'Local original PDF citations/open/embed');
  const downloadSection=main.match(/<ol id="native-downloads">([\s\S]*?)<\/ol>/)[1];
  const names=[...downloadSection.matchAll(/<li><a href="([^"]+)" download>/g)].map(m=>m[1]);
  need(same(names,native.files.map(f=>f.key)),'Native PDF then ZIP order');
  const assets=[];
  for(let i=0;i<native.files.length;i++){
    const f=native.files[i], bytes=read('preview/'+f.key),source=fs.readFileSync(path.join(project,`papers/23332261/sources/asset-23332261-${String(i+1).padStart(3,'0')}.response.body`));
    need(bytes.equals(source)&&bytes.length===f.size&&'md5:'+crypto.createHash('md5').update(bytes).digest('hex')===f.checksum,'Unchanged native '+f.key);
    need(article.encoding[i].contentUrl===f.key&&article.encoding[i].sameAs===f.links.self,'Encoding/native URL '+f.key);
    assets.push({name:f.key,...pin(bytes),native_MD5:f.checksum});
  }
  const expected=['annular-martin-kernel-note.pdf','annular-martin-kernel-verification.zip','citation.bib','index.html','research.css'].sort();
  need(same(fs.readdirSync(path.join(here,'preview')).sort(),expected),'Exact five preview leaves');
  const css=read('preview/research.css');need(css.length===1170&&sha(css)==='f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a','Unchanged established CSS');
  const bib=read('preview/citation.bib');need(bib.toString().includes('version = {1.0.0}')&&bib.toString().includes(native.doi)&&bib.toString().includes('CC-BY-4.0'),'Native edition/DOI/rights Bib');
  const visible=text(main);
  for(const phrase of ['1 &lt; |z| &lt; e','e<sup>1/2</sup>','ξ = −1','h(a) ≤ 1','U ∖ {a}','does not exclude isolated contact farther away','does not assume that the envelope is smooth','punctured-disc','No first historical resolution','no completed human peer review','actual scholarly contributions'])need(main.includes(phrase),'Scope/copy '+phrase);
  need(visible.includes('13 October 2026 UTC')&&visible.includes('OpenAI'),'Creation-date and AI disclosure');
  return {status:'PASS_PRIVATE_EDITORIAL_DATA_CHECK',record_id:23332261,whole_page:pin(pageBytes),whole_MAIN:pin(Buffer.from(main)),whole_head:pin(Buffer.from(head)),page_model:pin(read('PAGE_MODEL.json')),BibTeX:pin(bib),native_assets:assets,abstract_complete_visible_JSONLD_DC:true,native_version:'1.0.0',declared_date:'2026-10-12',native_created:native.created,private_noindex:true,canonical_url:null,AA:null,follow_up:null,publication_authority:false,scientific_program_executions:0,helper:pin(fs.readFileSync(fileURLToPath(import.meta.url))),writes:0};
}

async function render(data){
  const renderDir=path.join(here,'renders'),temp=path.join(here,'render-temp');
  need(!fs.existsSync(renderDir)&&!fs.existsSync(temp)&&!fs.existsSync(path.join(here,'RENDER_RECEIPT.json')),'Exclusive fresh render outputs');
  fs.mkdirSync(renderDir);fs.mkdirSync(temp);
  const require=createRequire(import.meta.url),{chromium}=require('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core');
  const diagnostics={nonlocal_page_routes_aborted:[],page_errors:[],console_errors:[],failed_requests:[]};
  const captures=[],layouts=[];let context=null,failure=null;
  try{
    context=await chromium.launchPersistentContext(path.join(temp,'profile'),{headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',downloadsPath:path.join(temp,'downloads'),env:{...process.env,TMPDIR:temp},args:['--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run','--no-default-browser-check','--disable-features=MediaRouter,OptimizationHints']});
    await context.setOffline(true);
    await context.route('**/*',async route=>{const url=route.request().url();if(/^(file:|data:|blob:|chrome-extension:)/.test(url))await route.continue();else{diagnostics.nonlocal_page_routes_aborted.push(url);await route.abort();}});
    const page=await context.newPage();
    page.on('pageerror',error=>diagnostics.page_errors.push(error.message));
    page.on('console',message=>{if(message.type()==='error')diagnostics.console_errors.push(message.text());});
    page.on('requestfailed',request=>diagnostics.failed_requests.push({url:request.url(),error:request.failure()?.errorText??null}));
    for(const [label,width] of [['desktop',1100],['mobile',390]]){
      await page.setViewportSize({width,height:900});
      await page.goto(pathToFileURL(path.join(here,'preview/index.html')).href,{waitUntil:'load'});
      await page.waitForTimeout(350);
      const layout=await page.evaluate(()=>({viewport:innerWidth,scroll:document.documentElement.scrollWidth,MAINs:document.querySelectorAll('main').length,H1s:document.querySelectorAll('h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor}));
      need(layout.viewport===layout.scroll&&layout.MAINs===1&&layout.H1s===1&&layout.font.includes('Arial')&&layout.background==='rgb(255, 255, 255)','Readable white/Arial single-column layout '+label);
      layouts.push({label,...layout});
      for(const [name,selector] of [['full',null],['abstract','#original-abstract'],['result','#result']]){
        const target=path.join(renderDir,`${label}-${name}.png`);
        if(selector)await page.locator(selector).screenshot({path:target});else await page.screenshot({path:target,fullPage:true});
        const bytes=fs.readFileSync(target);captures.push({path:path.relative(here,target),...pin(bytes),width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20)});
      }
    }
  }catch(error){failure=String(error.stack??error);}
  finally{if(context)await context.close();fs.rmSync(temp,{recursive:true,force:false});}
  const receipt={UTC:new Date().toISOString(),status:failure?'RENDER_INCOMPLETE_FAILURE_RETAINED':'SIX_HTML_LAYOUT_VIEWS_SAVED',method:'One offline installed headless Chrome local-file pass; not live or native desktop reader certification.',explicit_render_invocations:1,inputs:{whole_page:data.whole_page,helper:data.helper},layouts,captures,diagnostics,failure,context_offline:true,nonlocal_page_routes_aborted:true,temporary_owned_profile_removed:!fs.existsSync(temp),actual_embedded_PDF_display_certified:false,PDF_limitation:'Saved iframe appearance must be inspected. No successful live or native desktop PDF display is certified by this local layout pass.',native_asset_bytes_unchanged_by_data_check:true,scientific_program_executions:0,publication_authority:false};
  fs.writeFileSync(path.join(here,'RENDER_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n',{flag:'wx'});
  if(failure)throw new Error(failure);
  return receipt;
}

const data=check();
if(mode.length===0)process.stdout.write(JSON.stringify(data,null,2)+'\n');
else process.stdout.write(JSON.stringify(await render(data),null,2)+'\n');

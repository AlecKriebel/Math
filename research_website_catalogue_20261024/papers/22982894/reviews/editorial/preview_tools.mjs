// Copyright 2026 Alec Kriebel. MIT; see the full grant in LICENSES.md.
// One bounded local utility. Default reads only; --render and --seal are explicit.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const own=path.dirname(fileURLToPath(import.meta.url)),source=path.resolve(own,'../../sources'),P=path.resolve(own,'../../../..');
const args=process.argv.slice(2),hash=b=>({bytes:b.length,SHA256:crypto.createHash('sha256').update(b).digest('hex')});
const read=n=>fs.readFile(path.join(own,n)),pin=async n=>hash(await read(n)),json=async n=>JSON.parse(await read(n));
const need=(x,m)=>{if(!x)throw new Error(m);};
const save=async(n,obj)=>{need(path.basename(n)===n,'own-root file only');try{const s=await fs.lstat(path.join(own,n));need(s.isFile()&&!s.isSymbolicLink(),'ordinary output required');}catch(e){if(e.code!=='ENOENT')throw e;}await fs.writeFile(path.join(own,n),JSON.stringify(obj,null,2)+'\n');};
let final=null;try{final=await read('FINAL.json');}catch(e){if(e.code!=='ENOENT')throw e;}need(!final||final.toString()==='{}\n','frozen packet: no helper execution');
const inputs={};for(const n of ['preview/index.html','preview/research.css','preview_tools.mjs'])inputs[n]=await pin(n);
const html=(await read('preview/index.html')).toString(),main=html.match(/<main id="main">[\s\S]*?<\/main>/)?.[0],head=html.match(/<head>[\s\S]*?<\/head>/)?.[0];
need(main&&head&&html.match(/<main/g).length===1,'one complete actual MAIN required');
if(!args.length)console.log(JSON.stringify({status:'READ_ONLY_PREVIEW_GUARD',writes:0,inputs}));
else if(args.length===1&&args[0]==='--render'){
  need(!final,'no renderer during/after closure');
  const {chromium}=await import('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.mjs');
  const work=path.join(own,'render-work');await fs.mkdir(work,{recursive:true});await fs.mkdir(path.join(own,'renders'),{recursive:true});process.env.TMPDIR=work;
  let context;const external=[],errors=[],layouts=[];
  try{
    context=await chromium.launchPersistentContext(path.join(work,'profile'),{executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--disable-background-networking','--disable-component-update','--disable-sync','--no-first-run']});
    await context.route('**/*',async r=>{if(/^(file:|data:|about:|chrome-extension:|chrome:\/\/resources\/)/.test(r.request().url()))await r.continue();else{external.push(r.request().url());await r.abort();}});
    const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));
    for(const [name,width,height] of [['desktop',1100,900],['mobile',390,844]]){
      await page.setViewportSize({width,height});await page.goto(pathToFileURL(path.join(own,'preview/index.html')).href,{waitUntil:'load'});
      const a=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,main:document.querySelectorAll('main#main').length,h1:document.querySelectorAll('main h1').length,font:getComputedStyle(document.body).fontFamily,background:getComputedStyle(document.body).backgroundColor}));
      need(a.scroll===width&&a.main===1&&a.h1===1&&a.font.startsWith('Arial')&&a.background==='rgb(255, 255, 255)','layout mismatch '+JSON.stringify(a));
      await page.screenshot({path:path.join(own,'renders',name+'-full.png'),fullPage:true});
      for(const id of ['original-abstract','result'])await page.locator('#'+id).screenshot({path:path.join(own,'renders',name+'-'+id+'.png')});
      await page.keyboard.press('Tab');need(await page.evaluate(()=>document.activeElement?.getAttribute('href')==='#main'),'skip-link first focus');layouts.push({name,...a,skip_link_first_focus:true});
    }
    need(!external.length&&!errors.length,'unexpected external page request/error');
    for(const n of Object.keys(inputs))need(JSON.stringify(await pin(n))===JSON.stringify(inputs[n]),'changed render input');
    await save('RENDER_RECEIPT.json',{UTC:new Date().toISOString(),status:'PASS_LOCAL_LAYOUT',inputs,input_bytes_stable:true,layouts,external_page_requests:external,page_errors:errors,native_PDF_viewer_or_Mac_display_certified:false});
    console.log('PASS_LOCAL_LAYOUT desktop=1100 mobile=390 overflow=0 external_page_requests=0');
  }finally{if(context)await context.close();await fs.rm(work,{recursive:true,force:true});}
}else if(args.length===1&&args[0]==='--seal'){
  const terminals=['OWNED_MANIFEST.json','FINAL.json'];for(const n of terminals){const s=await fs.lstat(path.join(own,n));need(s.isFile()&&!s.isSymbolicLink()&&(await read(n)).toString()==='{}\n','exact precreated ordinary empty controls required');}
  const receipt=await json('RENDER_RECEIPT.json');need(receipt.status==='PASS_LOCAL_LAYOUT'&&receipt.input_bytes_stable&&JSON.stringify(receipt.inputs)===JSON.stringify(inputs),'current HTML/CSS/helper must match render');
  need(!main.includes('Private preview'),'administrative preview copy inside MAIN');
  const record=JSON.parse(await fs.readFile(path.join(source,'record.response.body'))),files=JSON.parse(await fs.readFile(path.join(source,'files.response.body')));
  need(JSON.stringify(record.files.map(x=>x.key))===JSON.stringify(['source-and-verification.zip','paper.pdf']),'native order');
  need(record.metadata.version==='1.0'&&record.metadata.publication_date==='2026-09-23','native date/version');
  need(html.match(/<div id="record-description">([\s\S]*?)<\/div>/)[1]===record.metadata.description,'complete original description');
  const assets=[];for(const row of record.files){const b=await read('preview/'+row.key),original=await fs.readFile(path.join(source,'assets',row.key));need(b.equals(original)&&b.length===row.size&&'md5:'+crypto.createHash('md5').update(b).digest('hex')===row.checksum,'native full bytes/MD5');assets.push({key:row.key,...hash(b)});}
  const authorityPath='verification/root-clearance-22982894-20261116.json',authority=hash(await fs.readFile(path.join(P,authorityPath)));need(authority.SHA256==='9566cc70a4d6d95e3d33f8b7ddd06170b01c61feaf4d2106b90c4e32680f67e8','root authority pin');
  need((await pin('INITIAL.md')).SHA256==='394bfa3e666c960eb51015f1c3ab8c35dd8b94ba856d3e2c6a50e3d384289215'&&(await pin('INITIAL_SEAL.json')).SHA256==='a823f34c4fcd90db3768826f1e3b12a93b612af5463bbf5def46ddaa2a45b76e','INITIAL freeze');
  const mainPin=hash(Buffer.from(main)),headPin=hash(Buffer.from(head)),now=new Date().toISOString();
  await save('PAGE_MODEL.json',{record_id:22982894,sheet_row:143,native_metadata_original:record.metadata,native_created_original:record.created,native_file_objects_original:record.files,native_files_response_original:files,printed_version:'1.0',printed_date:'2026-09-23',coefficient_convention:'canonical symmetric ordered polarization; multinomial factors for ordinary monomials',rights:{prose:'CC BY 4.0',code:'MIT',third_party_rights_retained:true,blanket_mixed_ZIP_license:false},root_authority:{path:authorityPath,...authority},proposed_slug:'positive-definite-coefficient-normalization',canonical_url:null,base_url:null,production_url:null,AA:null,follow_up:null,publication_authority:false,whole_actual_MAIN:mainPin,whole_head:headPin,assets});
  const payloads=[],dirs=[];async function walk(base,rel=''){for(const ent of (await fs.readdir(base,{withFileTypes:true})).sort((a,b)=>a.name.localeCompare(b.name))){const n=rel?rel+'/'+ent.name:ent.name;if(ent.isDirectory()){dirs.push(n);await walk(path.join(base,ent.name),n);}else{need(ent.isFile()&&!ent.isSymbolicLink(),'ordinary files only');if(!terminals.includes(n))payloads.push({path:n,...await pin(n)});}}}await walk(own);
  await save('OWNED_MANIFEST.json',{UTC:now,owned_root:own,files:payloads,directories:dirs,exact_existing_root_terminal_controls:terminals,subtree_basename_future_or_cache_exclusions:[],ignored_assets_and_rasters_included:true});
  await save('FINAL.json',{UTC:now,status:'PRIVATE_EDITORIAL_CANDIDATE_FROZEN',record_id:22982894,sheet_row:143,manifest:await pin('OWNED_MANIFEST.json'),payload_files:payloads.length,complete_owned_files:payloads.length+2,complete_directories:dirs.length,whole_actual_MAIN:mainPin,whole_head:headPin,whole_page:inputs['preview/index.html'],model:await pin('PAGE_MODEL.json'),BibTeX:await pin('preview/citation.bib'),helper:inputs['preview_tools.mjs'],exact_existing_root_terminal_controls:terminals,assigned_editorial_completion_percent:100,publication_authority:false,canonical_url:null,base_url:null,production_url:null,AA:null,follow_up:null,immutable_after_seal:true});
  console.log(JSON.stringify({status:'PRIVATE_EDITORIAL_CANDIDATE_FROZEN',FINAL:await pin('FINAL.json'),MAIN:mainPin,files:payloads.length+2,directories:dirs.length}));
}else throw new Error('Only read-only default, --render or --seal is permitted');

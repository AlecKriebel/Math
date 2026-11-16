// Copyright 2026 Alec Kriebel. CC BY 4.0. Own local editorial rendering only.
// Default: reads and reports; explicit --render is the only writing mode.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';

const own = path.dirname(fileURLToPath(import.meta.url));
const finalPath = path.join(own,'FINAL.json');
async function exists(p) { try { await fs.access(p); return true; } catch(e) { if(e.code==='ENOENT') return false; throw e; } }
if (await exists(finalPath)) throw new Error('Frozen or closing packet: renderer may not execute here');
const htmlPath = path.join(own,'preview/index.html');
const source = await fs.readFile(htmlPath);
const args = process.argv.slice(2);
if (!args.length) {
  console.log(JSON.stringify({status:'READ_ONLY_RENDER_GUARD',html_bytes:source.length,html_SHA256:crypto.createHash('sha256').update(source).digest('hex'),writes:0,browser_launched:false}));
} else {
  if (args.length!==1 || args[0]!=='--render') throw new Error('Only explicit --render is permitted');
  const {chromium} = await import('/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.mjs');
  const work = path.join(own,'render-work');
  const output = path.join(own,'renders');
  await fs.mkdir(work,{recursive:true});
  await fs.mkdir(output,{recursive:true});
  process.env.TMPDIR = work;
  let context;
  const external = [], errors = [], layouts = [];
  try {
    context = await chromium.launchPersistentContext(path.join(work,'profile'),{
      executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,
      args:['--disable-background-networking','--disable-component-update','--disable-default-apps','--disable-sync','--no-first-run','--metrics-recording-only'],
    });
    await context.route('**/*',async route=>{
      const u=route.request().url();
      if (/^(file:|data:|about:|chrome-extension:|chrome:\/\/resources\/)/.test(u)) await route.continue();
      else { external.push(u); await route.abort(); }
    });
    const page=await context.newPage();
    page.on('pageerror',e=>errors.push(String(e)));
    for (const spec of [{name:'desktop',width:1100,height:900},{name:'mobile',width:390,height:844}]) {
      await page.setViewportSize({width:spec.width,height:spec.height});
      await page.goto(pathToFileURL(htmlPath).href,{waitUntil:'load'});
      const audit=await page.evaluate(()=>({
        main_count:document.querySelectorAll('main#main').length,
        h1_count:document.querySelectorAll('main h1').length,
        font:getComputedStyle(document.body).fontFamily,
        background:getComputedStyle(document.body).backgroundColor,
        viewport:innerWidth,scroll_width:document.documentElement.scrollWidth,
        overflow:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left< -1);}).map(e=>e.tagName+(e.id?'#'+e.id:'')),
        original_abstract_text:document.querySelector('#original-abstract').innerText,
        iframe:{src:document.querySelector('iframe').getAttribute('src'),title:document.querySelector('iframe').title},
      }));
      if (audit.main_count!==1||audit.h1_count!==1||audit.scroll_width!==spec.width||audit.overflow.length||!audit.font.startsWith('Arial')||audit.background!=='rgb(255, 255, 255)') {
        await page.screenshot({path:path.join(output,spec.name+'-failed.png'),fullPage:true});
        throw new Error('Layout mismatch '+JSON.stringify({spec,audit}));
      }
      await page.screenshot({path:path.join(output,spec.name+'-full.png'),fullPage:true});
      await page.screenshot({path:path.join(output,spec.name+'-top.png')});
      await page.locator('#original-abstract').screenshot({path:path.join(output,spec.name+'-abstract.png')});
      await page.locator('#result').screenshot({path:path.join(output,spec.name+'-result.png')});
      await page.keyboard.press('Tab');
      const skip=await page.evaluate(()=>document.activeElement?.getAttribute('href')==='#main');
      if (!skip) throw new Error('First keyboard focus is not the skip link');
      layouts.push({...spec,audit,skip_link_first_focus:true});
    }
    if(external.length||errors.length) throw new Error('Unexpected external request/page error '+JSON.stringify({external,errors}));
    await fs.writeFile(path.join(own,'RENDER_RECEIPT.json'),JSON.stringify({UTC:new Date().toISOString(),status:'PASS_LOCAL_HEADLESS_LAYOUT',layouts,external_requests:external,page_errors:errors,local_file_and_builtin_Chrome_resources_only:true,native_Mac_or_desktop_display_claim:false,native_PDF_viewer_pixels_certified:false,PDF_reading:'Original complete text and four fresh individually viewed Poppler page rasters',temporary_work_removed_by_finally:true},null,2)+'\n');
    console.log('PASS_LOCAL_HEADLESS_LAYOUT desktop=1100 mobile=390 overflow=0 external_requests=0');
  } finally {
    if(context) await context.close();
    await fs.rm(work,{recursive:true,force:true});
  }
}

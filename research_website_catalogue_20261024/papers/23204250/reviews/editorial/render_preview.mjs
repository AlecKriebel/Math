// Bounded local HTML rendering only. No scientific code or remote URL is loaded.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { chromium } from '/opt/homebrew/lib/node_modules/openclaw/node_modules/playwright-core/index.mjs';

const owned = path.dirname(fileURLToPath(import.meta.url));
const output = path.join(owned, 'renders');
const profile = path.join(owned, '.render-profile');
const temp = path.join(owned, '.render-tmp');
await fs.mkdir(output, { recursive: true });
await fs.mkdir(temp, { recursive: true });
process.env.TMPDIR = temp;
const blocked = [];
const failures = [];
let context;
try {
  context = await chromium.launchPersistentContext(profile, {
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--disable-background-networking', '--disable-component-update', '--disable-default-apps', '--disable-sync', '--no-first-run', '--metrics-recording-only'],
  });
  await context.route('**/*', async route => {
    const url = route.request().url();
    if (url.startsWith('file:') || url.startsWith('data:') || url.startsWith('about:') || url.startsWith('chrome-extension:') || url.startsWith('chrome://resources/')) {
      await route.continue();
    } else {
      blocked.push(url);
      await route.abort();
    }
  });
  const page = await context.newPage();
  page.on('pageerror', error => failures.push(String(error)));
  const layouts = [];
  for (const spec of [{name:'desktop',width:1100,height:900}, {name:'mobile',width:390,height:844}]) {
    await page.setViewportSize({width:spec.width,height:spec.height});
    await page.goto(pathToFileURL(path.join(owned, 'preview/index.html')).href, {waitUntil:'load'});
    const audit = await page.evaluate(() => ({
      title: document.title,
      mainCount: document.querySelectorAll('main#main').length,
      h1Count: document.querySelectorAll('main h1').length,
      bodyFont: getComputedStyle(document.body).fontFamily,
      bodyBackground: getComputedStyle(document.body).backgroundColor,
      scrollWidth: document.documentElement.scrollWidth,
      viewportWidth: innerWidth,
      outerOverflow: [...document.querySelectorAll('body > *, header *, footer *')].filter(el => { const b = el.getBoundingClientRect(); return b.right > innerWidth + 1; }).map(el => ({tag:el.tagName,cls:el.className,right:el.getBoundingClientRect().right,width:el.getBoundingClientRect().width})),
      overflowElements: [...document.querySelectorAll('main *')].filter(el => {
        const b = el.getBoundingClientRect();
        return b.width > 0 && (b.right > innerWidth + 1 || b.left < -1);
      }).map(el => el.tagName + (el.id ? '#' + el.id : '')),
      iframe: {src:document.querySelector('iframe').getAttribute('src'), title:document.querySelector('iframe').title},
      mainTextLength: document.querySelector('main').innerText.length,
    }));
    if (audit.mainCount !== 1 || audit.h1Count !== 1 || audit.scrollWidth > spec.width || audit.overflowElements.length || !audit.bodyFont.startsWith('Arial') || audit.bodyBackground !== 'rgb(255, 255, 255)') {
      await page.screenshot({path:path.join(output,spec.name+'-failed.png'),fullPage:true});
      throw new Error('Layout audit failed: ' + JSON.stringify({spec,audit}));
    }
    await page.screenshot({path:path.join(output,spec.name+'-full.png'),fullPage:true});
    await page.screenshot({path:path.join(output,spec.name+'-top.png')});
    await page.locator('#result').screenshot({path:path.join(output,spec.name+'-result.png')});
    await page.locator('#review').screenshot({path:path.join(output,spec.name+'-review.png')});
    await page.keyboard.press('Tab');
    const skipFocus = await page.evaluate(() => document.activeElement?.getAttribute('href') === '#main');
    if (!skipFocus) throw new Error('Skip link was not first keyboard focus');
    layouts.push({...spec,audit,skip_link_first_keyboard_focus:true});
  }
  if (failures.length || blocked.length) throw new Error('Unexpected page errors or attempted external requests: '+JSON.stringify({failures,blocked}));
  const receipt = {
    UTC:new Date().toISOString(),
    status:'PASS_LOCAL_HEADLESS_LAYOUT',
    browser:'Installed Google Chrome, headless, persistent temporary profile inside owned namespace',
    source:'Local file URL and built-in Chrome resources only; external page requests blocked',
    blocked_external_requests:blocked,
    page_errors:failures,
    layouts,
    screenshots:['desktop-full.png','desktop-top.png','desktop-result.png','desktop-review.png','mobile-full.png','mobile-top.png','mobile-result.png','mobile-review.png'],
    native_desktop_or_Mac_display_claim:false,
    embedded_PDF_native_viewer_pixels_certified:false,
    PDF_reading:'Original PDF separately read in full by text extraction and six individually viewed fresh Poppler rasters',
  };
  await fs.writeFile(path.join(owned,'RENDER_RECEIPT.json'), JSON.stringify(receipt,null,2)+'\n');
  console.log('PASS_LOCAL_HEADLESS_LAYOUT desktop=1100 mobile=390 horizontal_overflow=0 external_requests=0');
} finally {
  if (context) await context.close();
  await fs.rm(profile,{recursive:true,force:true});
  await fs.rm(temp,{recursive:true,force:true});
}

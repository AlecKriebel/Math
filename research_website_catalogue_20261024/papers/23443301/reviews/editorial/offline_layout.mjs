// SPDX-License-Identifier: MIT
// One explicit offline six-view layout pass. Without --render this file only reports its guard.
import fs from "node:fs/promises";
import path from "node:path";
import {fileURLToPath, pathToFileURL} from "node:url";
import {chromium} from "/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/playwright/index.mjs";

const root = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
if (args.length !== 1 || args[0] !== "--render") {
  console.log(JSON.stringify({guard:"No rendering or filesystem writes without explicit --render",performed:false}));
  process.exit(0);
}
const output = path.join(root, "renders");
const profile = path.join(output, "owned-browser-profile");
const scratch = path.join(output, "owned-browser-temp");
const downloads = path.join(output, "owned-downloads");
const temporary = [profile, scratch, downloads];
const createdTemporary = [];
const receipt = {
  kind:"One offline headless layout pass, six saved views; no native Mac/mobile/live/download certification",
  started_UTC:new Date().toISOString(),
  page_URL:pathToFileURL(path.join(root,"preview/index.html")).href,
  requested_viewports:[{label:"desktop",width:1100,height:900},{label:"mobile",width:390,height:844}],
  requests:[], request_failures:[], console_errors:[], page_errors:[],
  blocked_HTTP_requests:[], captures:[], measurements:[], cleanup:[],
  navigation_response:null, fatal_error:null, browser_version:null,
  scientific_program_executions:[], external_GETs_permitted:false,
  download_clicks:[], native_viewer_certification:false
};
let context;
try {
  for (const target of temporary) {
    try { await fs.access(target); throw new Error("Refusing pre-existing temporary path: "+target); }
    catch (error) { if (error.code !== "ENOENT") throw error; }
  }
  for (const target of temporary) {
    await fs.mkdir(target);
    createdTemporary.push(target);
  }
  context = await chromium.launchPersistentContext(profile,{
    executablePath:"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    headless:true, offline:true, viewport:{width:1100,height:900},
    deviceScaleFactor:1, downloadsPath:downloads,
    env:{...process.env,TMPDIR:scratch,TMP:scratch,TEMP:scratch},
    args:["--disable-background-networking","--disable-component-update",
          "--disable-sync","--no-first-run","--no-default-browser-check",
          "--disable-crash-reporter","--disable-breakpad"]
  });
  receipt.browser_version=context.browser()?.version() ?? null;
  await context.route(/^https?:\/\//, async route => {
    receipt.blocked_HTTP_requests.push({url:route.request().url(),method:route.request().method()});
    await route.abort("internetdisconnected");
  });
  const page = context.pages()[0] ?? await context.newPage();
  page.on("request", request => receipt.requests.push({
    url:request.url(),method:request.method(),resource_type:request.resourceType()
  }));
  page.on("requestfailed", request => receipt.request_failures.push({
    url:request.url(),method:request.method(),resource_type:request.resourceType(),failure:request.failure()
  }));
  page.on("console", message => {
    if(message.type()==="error") receipt.console_errors.push({text:message.text(),location:message.location()});
  });
  page.on("pageerror", error => receipt.page_errors.push({name:error.name,message:error.message,stack:error.stack ?? null}));
  const response = await page.goto(receipt.page_URL,{waitUntil:"domcontentloaded",timeout:30000});
  receipt.navigation_response = response ? {url:response.url(),status:response.status()} : null;
  await page.waitForTimeout(1000);
  for (const viewport of receipt.requested_viewports) {
    await page.setViewportSize({width:viewport.width,height:viewport.height});
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.waitForTimeout(700);
    receipt.measurements.push(await page.evaluate(label=>{
      const main=document.querySelector("main");
      const frame=document.querySelector("iframe");
      const rect=main.getBoundingClientRect();
      return {label,inner_width:innerWidth,document_scroll_width:document.documentElement.scrollWidth,
        body_font:getComputedStyle(document.body).fontFamily,
        body_background:getComputedStyle(document.body).backgroundColor,
        main_id:main.id,main_width:rect.width,
        iframe_title:frame.title,iframe_src:frame.getAttribute("src"),
        iframe_box:{width:frame.getBoundingClientRect().width,height:frame.getBoundingClientRect().height},
        heading_count:document.querySelectorAll("h1").length};
    },viewport.label));
    for (const view of [{suffix:"full",selector:null},{suffix:"abstract",selector:"#abstract"},
                        {suffix:"result",selector:"#result"}]) {
      const filename=viewport.label+"-"+view.suffix+".png";
      const target=path.join(output,filename);
      try {
        if(view.selector) await page.locator(view.selector).screenshot({path:target,timeout:15000});
        else await page.screenshot({path:target,fullPage:true,timeout:15000});
        receipt.captures.push({path:"renders/"+filename,selector:view.selector,saved:true,error:null});
      } catch(error) {
        receipt.captures.push({path:"renders/"+filename,selector:view.selector,saved:false,
          error:{name:error.name,message:error.message}});
      }
    }
  }
} catch(error) {
  receipt.fatal_error={name:error.name,message:error.message,stack:error.stack ?? null};
} finally {
  if(context) {
    try { await context.close(); }
    catch(error) { receipt.cleanup.push({action:"browser-close",error:{name:error.name,message:error.message}}); }
  }
  for(const target of createdTemporary) {
    try { await fs.rm(target,{recursive:true,force:true}); receipt.cleanup.push({path:path.relative(root,target),removed:true,error:null}); }
    catch(error) { receipt.cleanup.push({path:path.relative(root,target),removed:false,error:{name:error.name,message:error.message}}); }
  }
  receipt.finished_UTC=new Date().toISOString();
  receipt.six_views_saved=receipt.captures.length===6 && receipt.captures.every(item=>item.saved);
  await fs.writeFile(path.join(output,"LAYOUT_RECEIPT.json"),JSON.stringify(receipt,null,2)+"\n");
  console.log(JSON.stringify(receipt,null,2));
}
process.exitCode=receipt.fatal_error===null && receipt.six_views_saved ? 0 : 1;


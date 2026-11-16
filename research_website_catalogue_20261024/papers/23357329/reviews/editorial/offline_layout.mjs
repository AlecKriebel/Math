// SPDX-License-Identifier: MIT
// One explicit offline six-view pass; the default guard does not render or write.
import fs from "node:fs/promises";
import path from "node:path";
import {fileURLToPath,pathToFileURL} from "node:url";
const root=path.dirname(fileURLToPath(import.meta.url));
if(process.argv.slice(2).join(" ")!=="--render") {
  console.log(JSON.stringify({performed:false,guard:"No render or writes without explicit --render"}));
  process.exit(0);
}
try {
  await fs.access(path.join(root,"FINAL.json"));
  console.error("Refusing to render a packet with an existing FINAL.json");
  process.exit(2);
} catch(error) {
  if(error.code!=="ENOENT") throw error;
}
const output=path.join(root,"renders");
const temporary=["owned-profile","owned-temp","owned-downloads"].map(x=>path.join(output,x));
const created=[];
const receipt={
  kind:"One offline headless six-view layout pass; no native Mac, physical mobile, live or download certification",
  started_UTC:new Date().toISOString(),page_URL:pathToFileURL(path.join(root,"preview/index.html")).href,
  viewports:[{label:"desktop",width:1100,height:900},{label:"mobile",width:390,height:844}],
  browser_version:null,navigation_response:null,requests:[],request_failures:[],
  console_errors:[],page_errors:[],blocked_HTTP_requests:[],captures:[],measurements:[],
  cleanup:[],fatal_error:null,download_clicks:[],native_viewer_certification:false,
  scientific_program_executions:[],external_GETs_permitted:false
};
let context;
try {
  for(const target of temporary) {
    try {await fs.access(target);throw new Error("Refusing pre-existing temporary path: "+target);}
    catch(error) {if(error.code!=="ENOENT")throw error;}
  }
  for(const target of temporary) {await fs.mkdir(target);created.push(target);}
  const {chromium}=await import("/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/playwright/index.mjs");
  context=await chromium.launchPersistentContext(temporary[0],{
    executablePath:"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    headless:true,offline:true,viewport:{width:1100,height:900},deviceScaleFactor:1,
    downloadsPath:temporary[2],env:{...process.env,TMPDIR:temporary[1],TMP:temporary[1],TEMP:temporary[1]},
    args:["--disable-background-networking","--disable-component-update","--disable-sync",
          "--no-first-run","--no-default-browser-check","--disable-crash-reporter","--disable-breakpad"]
  });
  receipt.browser_version=context.browser()?.version()??null;
  await context.route(/^https?:\/\//,async route=>{
    receipt.blocked_HTTP_requests.push({url:route.request().url(),method:route.request().method()});
    await route.abort("internetdisconnected");
  });
  const page=context.pages()[0]??await context.newPage();
  page.on("request",r=>receipt.requests.push({url:r.url(),method:r.method(),resource_type:r.resourceType()}));
  page.on("requestfailed",r=>receipt.request_failures.push({
    url:r.url(),method:r.method(),resource_type:r.resourceType(),failure:r.failure()}));
  page.on("console",m=>{if(m.type()==="error")receipt.console_errors.push({text:m.text(),location:m.location()});});
  page.on("pageerror",e=>receipt.page_errors.push({name:e.name,message:e.message,stack:e.stack??null}));
  const response=await page.goto(receipt.page_URL,{waitUntil:"domcontentloaded",timeout:30000});
  receipt.navigation_response=response?{url:response.url(),status:response.status()}:null;
  await page.waitForTimeout(1000);
  for(const viewport of receipt.viewports) {
    await page.setViewportSize({width:viewport.width,height:viewport.height});
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.waitForTimeout(700);
    receipt.measurements.push(await page.evaluate(label=>{
      const main=document.querySelector("main"),frame=document.querySelector("iframe");
      return {label,inner_width:innerWidth,document_scroll_width:document.documentElement.scrollWidth,
        body_font:getComputedStyle(document.body).fontFamily,
        body_background:getComputedStyle(document.body).backgroundColor,
        main_id:main.id,main_width:main.getBoundingClientRect().width,
        h1_count:document.querySelectorAll("h1").length,
        iframe_title:frame.title,iframe_src:frame.getAttribute("src"),
        iframe_box:{width:frame.getBoundingClientRect().width,height:frame.getBoundingClientRect().height}};
    },viewport.label));
    for(const view of [{name:"full",selector:null},{name:"abstract",selector:"#abstract"},{name:"result",selector:"#result"}]) {
      const filename=viewport.label+"-"+view.name+".png";
      try {
        if(view.selector)await page.locator(view.selector).screenshot({path:path.join(output,filename),timeout:15000});
        else await page.screenshot({path:path.join(output,filename),fullPage:true,timeout:15000});
        receipt.captures.push({path:"renders/"+filename,selector:view.selector,saved:true,error:null});
      } catch(error) {
        receipt.captures.push({path:"renders/"+filename,selector:view.selector,saved:false,
          error:{name:error.name,message:error.message}});
      }
    }
  }
} catch(error) {
  receipt.fatal_error={name:error.name,message:error.message,stack:error.stack??null};
} finally {
  if(context)try{await context.close();}catch(error){
    receipt.cleanup.push({action:"browser-close",error:{name:error.name,message:error.message}});
  }
  for(const target of created)try{
    await fs.rm(target,{recursive:true,force:true});
    receipt.cleanup.push({path:path.relative(root,target),removed:true,error:null});
  }catch(error){receipt.cleanup.push({path:path.relative(root,target),removed:false,
    error:{name:error.name,message:error.message}});}
  receipt.finished_UTC=new Date().toISOString();
  receipt.six_views_saved=receipt.captures.length===6&&receipt.captures.every(x=>x.saved);
  await fs.writeFile(path.join(output,"LAYOUT_RECEIPT.json"),JSON.stringify(receipt,null,2)+"\n");
  console.log(JSON.stringify(receipt,null,2));
}
process.exitCode=receipt.fatal_error===null&&receipt.six_views_saved?0:1;

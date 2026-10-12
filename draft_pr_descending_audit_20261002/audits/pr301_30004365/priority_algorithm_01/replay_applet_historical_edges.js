// Offline replay of pinned primary code. Two wrappers expose classes and set a public path;
// the invariant algorithms are unmodified. Every request is blocked.
const fs=require('fs'), path=require('path'), crypto=require('crypto');
const {chromium}=require('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=__dirname, sha=s=>crypto.createHash('sha256').update(s).digest('hex');
(async()=>{
 const main=fs.readFileSync(path.join(root,'sources/applet-2025-main.decoded.js'),'utf8'), vendors=fs.readFileSync(path.join(root,'sources/applet-2025-vendors.decoded.js'),'utf8');
 let mod=main;
 const exp='const rn=Vr;';
 if(mod.split(exp).length!==2)throw Error('export anchor differs');
 mod=mod.replace(exp,'globalThis.auditExports={Algebra:Vr,Quiver:le,examples:o};return;'+exp);
 const pub='if(!t)throw new Error("Automatic publicPath is not supported in this browser");';
 if(mod.split(pub).length!==2)throw Error('publicpath anchor differs');
 mod=mod.replace(pub,'if(!t)t="https://www.math.uni-bielefeld.de/~jgeuenich/string-applet/main.bundle.js";');
 fs.writeFileSync(path.join(root,'sources/applet-2025-main.replay.js'),mod);
 console.log(JSON.stringify({mainSHA256:sha(main),vendorsSHA256:sha(vendors),instrumentedSHA256:sha(mod),harnessSHA256:sha(fs.readFileSync(__filename)),node:process.version,utc:new Date().toISOString()}));
 const tmp=path.join(root,'tmp');fs.mkdirSync(tmp,{recursive:true});process.env.TMPDIR=tmp;
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',args:['--disable-breakpad','--disable-crash-reporter'],env:{...process.env,TMPDIR:tmp}});
 console.log(JSON.stringify({browser:await browser.version()}));
 const context=await browser.newContext();await context.route('**/*',r=>r.abort());
 const page=await context.newPage();page.on('pageerror',e=>console.log(JSON.stringify({pageerror:e.message})));
 let html=fs.readFileSync(path.join(root,'sources/string-applet.html'),'utf8').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'');
 await page.setContent(html);
 await page.evaluate(()=>{globalThis.MathJax={Hub:{Config(){},Queue(){},Register:{StartupHook(){}}}}});
 await page.addScriptTag({content:vendors});await page.addScriptTag({content:mod});
 const out=await page.evaluate(()=>{
  const {Algebra,Quiver,examples}=auditExports;
  examples['audit dual numbers']={quiver:{vertices:[{id:1}],arrows:[{id:'a',source:1,target:1}]},relations:'aa'};
  examples['audit k']={quiver:{vertices:[{id:1}],arrows:[]},relations:''};
  for(const [m,n] of [[3,5],[4,4]]){
   const vertices=Array.from({length:m+n},(_,i)=>({id:i+1})), arrows=[],relations=[];
   const names='abcdefghijklmnopqrstuvwxyz';
   for(let i=0;i<m+n;i++){
    const start=i<m?0:m, len=i<m?m:n;
    arrows.push({id:names[i],source:i+1,target:start+(i-start+1)%len+1});
    relations.push(names[i]+names[start+(i-start+1)%len]);
   }
   arrows.push({id:names[m+n],source:1,target:m+1});
   examples['audit A('+m+','+n+')']={quiver:{vertices,arrows},relations:relations.join(' ')};
  }
  const output={quiverStatic:Object.getOwnPropertyNames(Quiver),quiverPrototype:Object.getOwnPropertyNames(Quiver.prototype),examples:[]};
  for(const name of Object.keys(examples)){
   try{
    const ex=examples[name], q=new Quiver;
    ex.quiver.vertices.forEach(v=>q.addVertex(String(v.id),v.id));
    ex.quiver.arrows.forEach(a=>q.addArrow(a.source,a.target,a.id,a.id));
    const A=new Algebra(q,ex.relations||'');
    if(!A.isGentle())continue;
    const row={name,vertices:A.quiver.vertices.length,arrows:A.quiver.arrows.length,genus:A.genus(),ag:A.agInvariant(),boundary:A.boundaryWindingNumbers(),winding:A.windingNumbers(),intersection:A.intersectionNumbers(),gcd:A.windingNumberGCD(),parity:A.windingNumberParity(),arf:A.arfInvariant()};
    output.examples.push(row);
   }catch(e){output.examples.push({name,error:e.message,stack:e.stack});}
  }
  return output;
 });
 fs.writeFileSync(path.join(root,'APPLET_HISTORICAL_EDGE_RESULTS.json'),JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out));
 await browser.close();
})().catch(e=>{console.error(e.stack);process.exit(1)});

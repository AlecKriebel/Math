// Adversarial test of the unchanged primary Arf body against the independent Gauss-sum definition.
const fs=require('fs'),path=require('path'),zlib=require('zlib'),crypto=require('crypto');
const {chromium}=require('/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const R=__dirname,B=path.resolve('draft_pr_descending_audit_20261002/audits/pr301_30004365/priority_algorithm_01/sources');
const sha=d=>crypto.createHash('sha256').update(d).digest('hex');
let browser;
(async()=>{
 browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const page=await browser.newPage();await page.route('**/*',r=>r.abort());const results=[];
 await page.evaluate(()=>{
  // Babel finite-array iteration/destructuring adapters needed by the isolated primary function.
  globalThis.Cr=globalThis.Mr=(value)=>{let iterator;return{s(){iterator=value[Symbol.iterator]()},n(){return iterator.next()},e(error){throw error},f(){}}};
  globalThis.Tr=(value,length)=>Array.from(value).slice(0,length);
 });
 for(const edition of ['historical_20250321','current']){
  const primary=edition==='current'?fs.readFileSync(path.join(B,'string-main.js'),'utf8'):zlib.gunzipSync(fs.readFileSync(path.join(R,'sources/applet_2025.gz'))).toString('utf8');
  const start=primary.indexOf('arfInvariant:function(){'),end=primary.indexOf('},boundaryWindingNumbers:function',start);
  if(start<0||end<0)throw Error('Arf extraction anchors');
  const body=primary.slice(start+'arfInvariant:'.length,end+1);fs.writeFileSync(path.join(R,'sources/'+edition+'.arf_body.js'),body);
  const result=await page.evaluate((body)=>{
   const arf=new Function('return ('+body+')')();let forms=0,checks=0;
   const N=4, pairs=[];for(let i=0;i<N;i++)for(let j=i+1;j<N;j++)pairs.push([i,j]);
   function rank(M){M=M.map(r=>r.slice());let r=0;for(let c=0;c<N;c++){let p=M.findIndex((row,i)=>i>=r&&row[c]);if(p<0)continue;[M[p],M[r]]=[M[r],M[p]];for(let i=0;i<N;i++)if(i!==r&&M[i][c])for(let j=c;j<N;j++)M[i][j]^=M[r][j];r++;}return r;}
   for(let mask=0;mask<(1<<pairs.length);mask++){
    let B=Array.from({length:N},()=>Array(N).fill(0));for(let k=0;k<pairs.length;k++){const [i,j]=pairs[k];B[i][j]=B[j][i]=(mask>>k)&1;}
    if(rank(B)!==N)continue;forms++;
    for(let qmask=0;qmask<(1<<N);qmask++){
     const q=Array.from({length:N},(_,i)=>(qmask>>i)&1);let sum=0;
     for(let v=0;v<(1<<N);v++){let value=0;for(let i=0;i<N;i++)value^=q[i]&((v>>i)&1);for(const [i,j] of pairs)value^=B[i][j]&((v>>i)&1)&((v>>j)&1);sum+=value?-1:1;}
     if(Math.abs(sum)!==(1<<(N/2)))throw Error('independent Gauss sum not nondegenerate');
     const fake={genus:()=>2,boundaryWindingNumbers:()=>[-6],windingNumbers:()=>q.map(x=>2*(x-1)),intersectionNumbers:()=>B.map((row,i)=>row.slice(i+1)).slice(0,-1)};
     const actual=arf.call(fake),expected=sum<0?1:0;checks++;
     if(actual!==expected)throw Error(JSON.stringify({mask,qmask,actual,expected,B,q}));
    }
   }
   return {dimension:N,nondegenerate_forms:forms,gauss_sum_checks:checks};
  },body);
  results.push({edition,primary_sha256:sha(primary),body_sha256:sha(body),...result});
 }
 fs.writeFileSync(path.join(R,'ARF_CONTROLS.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results));await browser.close();
})().catch(e=>{console.error(e.stack);process.exitCode=1}).finally(async()=>{if(browser)await browser.close()});

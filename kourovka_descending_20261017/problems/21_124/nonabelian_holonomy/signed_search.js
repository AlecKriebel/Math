// Exact modular screening of every triple in B_n, first entry up to conjugacy.
// Positive modular candidates require separate rational verification.
const fs=require('fs');
const n=Number(process.argv[2]||3), unsigned=process.argv.includes('--unsigned'), prefix=unsigned?'permutation':'signed', P=65521, pp=[3,20,119], qq=[2,14,84];
function perms(a){if(a.length===0)return [[]];let out=[];for(let i=0;i<a.length;i++)for(const p of perms(a.slice(0,i).concat(a.slice(i+1))))out.push([a[i],...p]);return out;}
function key(g){const seen=Array(n).fill(false),cs=[];for(let i=0;i<n;i++)if(!seen[i]){let j=i,l=0,s=1;do{seen[j]=true;l++;s*=Math.sign(g[j]);j=Math.abs(g[j])-1;}while(j!==i);cs.push([l,s]);}cs.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);return JSON.stringify(cs);}
const gs=[],reps=[],keys=new Set();for(const p of perms([...Array(n).keys()]))for(let b=0;b<(unsigned?1:(1<<n));b++){const g=p.map((x,i)=>(x+1)*((b&(1<<i))?-1:1));const k=key(g);if(!keys.has(k)){keys.add(k);reps.push(g);}gs.push(g);}
const inverses=new Int32Array(P);inverses[1]=1;for(let i=2;i<P;i++)inverses[i]=(P-Math.floor(P/i)*inverses[P%i]%P)%P;
function rank(a,nr,nc){let r=0;for(let c=0;c<nc&&r<nr;c++){let k=r;while(k<nr&&!a[k*nc+c])k++;if(k===nr)continue;for(let j=c;j<nc;j++){const tmp=a[r*nc+j];a[r*nc+j]=a[k*nc+j];a[k*nc+j]=tmp;}const z=inverses[a[r*nc+c]];for(let j=c;j<nc;j++)a[r*nc+j]=a[r*nc+j]*z%P;for(let i=r+1;i<nr;i++){const v=a[i*nc+c];if(!v)continue;for(let j=c;j<nc;j++)a[i*nc+j]=(a[i*nc+j]-v*a[r*nc+j]%P+P)%P;}r++;}return r;}
function matrix(ss){const nc=3*n,a=new Int32Array(nc*nc);for(let k=0;k<3;k++)for(let c=0;c<n;c++){const s=Math.sign(ss[k][c]),r=Math.abs(ss[k][c])-1;a[(k*n+r)*nc+c]=(P+pp[k]*s)%P;a[(k*n+c)*nc+n+c]=P-qq[k];a[(k*n+r)*nc+2*n+c]=(a[(k*n+r)*nc+2*n+c]+P+s)%P;a[(k*n+c)*nc+2*n+c]=(a[(k*n+c)*nc+2*n+c]+P-1)%P;}return a;}
function fixedrank(ss){
  // Integer signed-graph computation: fixed-space dimension equals the number
  // of connected components whose edge-sign product is consistently +1.
  const adj=Array.from({length:n},()=>[]);
  for(const g of ss)for(let c=0;c<n;c++){const r=Math.abs(g[c])-1,s=Math.sign(g[c]);adj[c].push([r,s]);adj[r].push([c,s]);}
  const colors=Array(n).fill(0);let balanced=0;
  for(let start=0;start<n;start++)if(!colors[start]){let ok=true;colors[start]=1;const todo=[start];while(todo.length){const v=todo.pop();for(const [w,s] of adj[v]){if(!colors[w]){colors[w]=s*colors[v];todo.push(w);}else if(colors[w]!==s*colors[v])ok=false;}}if(ok)balanced++;}
  return n-balanced;
}
let tested=0,singular=0,extra=0;const start=Date.now(),fd=fs.openSync(`${prefix}_candidates_${n}.jsonl`,'w');for(const a of reps){for(const b of gs)for(const c of gs){tested++;const ss=[a,b,c],r=rank(matrix(ss),3*n,3*n);if(r===3*n)continue;singular++;const rt=fixedrank(ss);if(r<2*n+rt){extra++;fs.writeSync(fd,JSON.stringify({matrices:ss,mod_rank:r,fixed_rank:rt})+'\n');}}console.error(`n=${n}: tested ${tested}; modular candidates ${extra}`);}fs.closeSync(fd);console.log(JSON.stringify({dimension:n,unsigned,group_order:gs.length,first_conjugacy_classes:reps.length,tested_triples:tested,singular_mod:singular,extra_kernel_mod:extra,prime:P,seconds:(Date.now()-start)/1000}));

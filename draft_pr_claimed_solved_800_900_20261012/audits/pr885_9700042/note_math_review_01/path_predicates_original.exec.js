function auditPathPredicates(N) {
 const side=N+1,V=side*side,vertices=Array.from({length:V},(_,i)=>[Math.floor(i/side),i%side]);
 const adj=Array.from({length:V},()=>[]),out=Array.from({length:V},()=>[]);let edgeCount=0;
 const id=(x,y)=>x*side+y;
 for(let x=0;x<=N;x++)for(let y=0;y<=N;y++)for(const [dx,dy] of [[1,0],[0,1]])if(x+dx<=N&&y+dy<=N){
  const a=id(x,y),b=id(x+dx,y+dy),e=edgeCount++;adj[a].push([b,e,1]);adj[b].push([a,e,-1]);out[a].push(e);
 }
 const paths=[];
 function dfs(v,seen,vs,es) {if(v===V-1){paths.push({vs:[...vs],es:[...es]});return;}for(const [w,e,dir]of adj[v])if(!seen.has(w)){seen.add(w);vs.push(w);es.push([e,dir]);dfs(w,seen,vs,es);es.pop();vs.pop();seen.delete(w);}}
 dfs(0,new Set([0]),[0],[]);
 const boundary=vertices.map((v,i)=>(v[0]===N||v[1]===N)&&i!==V-1?i:-1).filter(i=>i>=0);
 const strict=(a,b)=>a[0]<b[0]&&a[1]<b[1],M=N+1;
 let checked=0,nonlast=0,extensionCases=0;
 for(let marks=0;marks<(1<<edgeCount);marks++){
  const rewards=paths.map(p=>{let k=0,b=0;for(const[e,dir]of p.es){if(dir<0)b++;else k+=(marks>>e)&1;}return{k,b,D:k-b};});
  const D=Math.max(...rewards.map(z=>z.D));
  for(let ext=0;ext<(1<<boundary.length);ext++){
   extensionCases++;
   const open=out.map(es=>es.some(e=>((marks>>e)&1)!==0));
   boundary.forEach((v,i)=>{if((ext>>i)&1)open[v]=true;});
   const dp=Array(V).fill(0);let A=0,lowerA=0;
   for(let v=0;v<V;v++)if(open[v]){
    dp[v]=1;for(let u=0;u<v;u++)if(strict(vertices[u],vertices[v]))dp[v]=Math.max(dp[v],dp[u]+1);
    A=Math.max(A,dp[v]);if(vertices[v][0]<N&&vertices[v][1]<N)lowerA=Math.max(lowerA,dp[v]);
   }
   if(D<lowerA)throw new Error("Lower chain comparison failed");
   for(let z=0;z<paths.length;z++)if(rewards[z].D===D){
    const path=paths[z],{k,b}=rewards[z];checked++;
    const list=[{xy:[0,0],pos:0}];
    path.vs.slice(1,-1).forEach((v,i)=>{if(open[v])list.push({xy:vertices[v],pos:i+1});});
    list.push({xy:[M,M],pos:Infinity});const p=list.length-2,I0=open[0]?1:0;
    const selected=[0];while(selected[selected.length-1]<p+1){const last=selected[selected.length-1];let j=last+1;while(!strict(list[last].xy,list[j].xy))j++;selected.push(j);}
    const a=selected.length-1,L=p-a+1;
    if(k>p+I0||A<a-1+I0||D-A>L-b)throw new Error("Cancellation failed");
    let X=0;
    for(let g=0;g<a;g++){
     const start=selected[g],end=selected[g+1],ell=end-start-1,anchor=list[start].xy,tail=list[end-1].xy,next=list[end].xy;
     const d=ell===0?0:(tail[0]<=anchor[0]?0:1),other=1-d;
     if(ell>0&&tail[d]>anchor[d])throw new Error("Distinguished coordinate failed");
     if(tail[other]-next[other]>2*(ell+1))throw new Error("Item 4 failed");
     if(g<a-1){let bj=0;for(let t=list[start].pos;t<list[end].pos;t++)if(path.es[t][1]<0)bj++;nonlast++;if(bj>ell)throw new Error("Local competitor inequality failed");}
     for(let i=start+1;i<end;i++){const u=list[i].xy.map((c,j)=>c-list[i-1].xy[j]);X+=Math.abs(u[d])+Math.max(-u[other],0);}
    }
    if(X>2*b)throw new Error("Variation bound failed");
   }
  }
 }
 return {N,forwardMarkConfigurations:1<<edgeCount,boundaryExtensionsPerConfiguration:1<<boundary.length,simplePaths:paths.length,extensionCases,optimalPathsChecked:checked,nonlastSegmentsChecked:nonlast,result:"All lower-chain, cancellation, local competitor, Item 4 and per-increment variation inequalities hold."};
}
text([1,2].map(auditPathPredicates));

function popcount(x) {let a=0;while(x){x&=x-1;a++;}return a;}
function checkFinite(n) {
  const N=n-2, side=N+1, V=side*side, edges=[], adj=Array.from({length:V},()=>[]);
  const id=(x,y)=>x*side+y;
  edges.push([[0,N],[0,N+1]],[[N,0],[N+1,0]]);
  for(let x=0;x<=N;x++)for(let y=0;y<=N;y++){
    if(x<N){const i=edges.length;edges.push([[x+1,N-y],[x+1,N+1-y]]);adj[id(x,y)].push([id(x+1,y),i]);adj[id(x+1,y)].push([id(x,y),-1]);}
    if(y<N){const i=edges.length;edges.push([[x,N-y],[x+1,N-y]]);adj[id(x,y)].push([id(x,y+1),i]);adj[id(x,y+1)].push([id(x,y),-1]);}
  }
  const free=[];for(let x=1;x<=N;x++)for(let y=1;y<=N;y++)free.push([x,y]);
  const cutmasks=[];
  for(let bits=0;bits<(1<<free.length);bits++){
    const src=new Set();
    for(let j=0;j<=N;j++){src.add(`0,${j}`);src.add(`${j},0`);}
    free.forEach((v,i)=>{if((bits>>i)&1)src.add(v.join(","));});
    let m=0;edges.forEach((e,i)=>{if(src.has(e[0].join(","))&&!src.has(e[1].join(",")))m|=1<<i;});cutmasks.push(m);
  }
  for(let mask=0;mask<(1<<edges.length);mask++){
    const primal=Math.min(...cutmasks.map(m=>popcount(m&mask)));
    const d=Array(V).fill(Infinity),used=Array(V).fill(false);d[0]=0;
    for(let iter=0;iter<V;iter++){
      let v=-1;for(let i=0;i<V;i++)if(!used[i]&&(v===-1||d[i]<d[v]))v=i;
      if(v===-1||v===V-1)break;used[v]=true;
      for(const [w,i]of adj[v])d[w]=Math.min(d[w],d[v]+(i<0?0:(mask>>i)&1));
    }
    const dual=((mask&1)!==0?1:0)+((mask&2)!==0?1:0)+d[V-1];
    if(primal!==dual)throw new Error(JSON.stringify({n,mask,primal,dual}));
  }
  return {n,relevantBinaryAssignments:1<<edges.length,sourceSideCuts:cutmasks.length,result:"All finite cut identities agree."};
}
text([2,3,4].map(checkFinite));

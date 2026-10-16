from pathlib import Path
BASE = Path(__file__).resolve().parent
import itertools,json

def comps(perm):
 n=len(perm); inv={p:s+1 for s,p in enumerate(perm)}
 edges=[]
 for p,q in itertools.combinations(range(1,n+1),2):
  a,b=2*inv[p]-1,2*(p-1); c,d=2*inv[q]-1,2*(q-1)
  m=2*n
  if (0<(c-a)%m<(b-a)%m)!=(0<(d-a)%m<(b-a)%m): edges.append((p,q))
 cs=[{p} for p in range(1,n+1)]
 for p,q in edges:
  a=next(c for c in cs if p in c); b=next(c for c in cs if q in c)
  if a is not b: a.update(b); cs.remove(b)
 return cs,edges
out={}
for n in range(3,9):
 byk={}; count=0; non=[]
 for p in itertools.permutations(range(1,n+1)):
  k=sum(x<=i for i,x in enumerate(p,1))
  cs,edges=comps(p)
  if len(cs)==1:
   count+=1;byk[k]=byk.get(k,0)+1
   if p != tuple((i+k-1)%n+1 for i in range(1,n+1)) and len(non)<10: non.append({'p':p,'k':k,'edges':edges})
 out[n]={'connected_count':count,'by_rank':byk,'first_nontop':non}
 print(n,out[n],flush=True)
open(BASE / 'strand_enumeration.json','w').write(json.dumps(out,indent=2))

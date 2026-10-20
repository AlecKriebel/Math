import itertools,json,time
from functools import lru_cache
from math import comb

def instance(d,n):
 p=list(itertools.product(range(1,n+1),repeat=d)); idx={x:i for i,x in enumerate(p)}; edges=set()
 for i,x in enumerate(p):
  for j in range(i,len(p)):
   z=tuple(a+b for a,b in zip(x,p[j]))
   if z in idx: edges.add((1<<i)|(1<<j)|(1<<idx[z]))
 return p,sorted(edges,key=lambda e:(e.bit_count(),e))

def run(d,n):
 p,edges=instance(d,n); full=(1<<len(p))-1
 slices=[(sum(t<=sum(x)<2*t for x in p),t) for t in range(1,d*n+1)]
 lower,t=max(slices); initial=sum(1<<i for i,x in enumerate(p) if not t<=sum(x)<2*t)
 best=initial.bit_count(); bestmask=initial; nodes=0
 # Exact branch-and-bound for the smallest deletion set meeting every edge.
 # Each recursive child deletes one vertex of a still-unmet forbidden edge.
 # Pairwise vertex-disjoint unmet edges each require an additional deletion.
 @lru_cache(None)
 def dfs(deleted):
  nonlocal best,bestmask,nodes
  nodes+=1; used=deleted.bit_count()
  if used>=best:return
  unmet=[e for e in edges if not e&deleted]
  if not unmet:best=used;bestmask=deleted;return
  pack=0; cnt=0
  for e in unmet:
   if not e&pack:
    pack|=e;cnt+=1
  if used+cnt>=best:return
  freq={}
  for e in unmet:
   for i in range(len(p)):
    if e>>i&1:freq[i]=freq.get(i,0)+1
  e=min(unmet,key=lambda e:(e.bit_count(),-sum(freq[i] for i in freq if e>>i&1)))
  for i in sorted((i for i in freq if e>>i&1),key=lambda i:-freq[i]):dfs(deleted|1<<i)
 dfs(0)
 chosen=[x for i,x in enumerate(p) if not bestmask>>i&1]
 assert all(tuple(a+b for a,b in zip(x,y)) not in set(chosen) for x in chosen for y in chosen)
 return dict(d=d,n=n,maximum=len(p)-best,slice_maximum=lower,slice_t=t,edges=len(edges),nodes=nodes,vertices=chosen)
if __name__=='__main__':
 import sys
 for spec in sys.argv[1:]:
  d,n=map(int,spec.split(',')); start=time.time(); r=run(d,n);r['seconds']=time.time()-start
  print(json.dumps(r),flush=True)

from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json
count=0
def ck(x):
 global count
 assert x
 count+=1
witnesses=0
for a in range(1,6):
 for b in range(1,6):
  P=[(i,j) for i in range(a) for j in range(b)];N=len(P);idx={p:i for i,p in enumerate(P)}
  edges=[(idx[p],idx[q]) for p in P for q in [(p[0]+1,p[1]),(p[0],p[1]+1)] if q in idx]
  order=[lambda x:x[0],lambda x:1-x[-1]]+[lambda x,u=u,v=v:x[v]-x[u] for u,v in edges]
  # Each order facet has a rational point satisfying only it at equality.
  pts=[[F(i,N) for i in range(N)],[F(i+1,N) for i in range(N)]]
  for u,v in edges:
   classes={i:(u if i==v else i) for i in range(N)};verts=set(classes.values());es={(classes[s],classes[t]) for s,t in edges if classes[s]!=classes[t]}
   topo=[];left=set(verts)
   while left:
    ready=sorted(t for t in left if not any(s in left and tt==t for s,tt in es));ck(bool(ready));topo.extend(ready);left-=set(ready)
   val={t:F(i+1,len(topo)+1) for i,t in enumerate(topo)};pts.append([val[classes[i]] for i in range(N)])
  ck(len(order)==(a-1)*b+a*(b-1)+2)
  for target,x in enumerate(pts):
   for j,f in enumerate(order):ck(f(x)==0 if j==target else f(x)>0)
   witnesses+=1
  # Enumerate lattice paths independently by choosing horizontal-step positions.
  h=a+b-1;paths=[]
  for horiz in combinations(range(h-1),a-1):
   H=set(horiz);i=j=0;path=[idx[i,j]]
   for t in range(h-1):
    if t in H:i+=1
    else:j+=1
    path.append(idx[i,j])
   paths.append(path)
  ck(len(paths)==comb(a+b-2,a-1))
  chain=[lambda x,i=i:x[i] for i in range(N)]+[lambda x,path=path:1-sum(x[i] for i in path) for path in paths]
  pts=[]
  for i in range(N):pts.append([F(0) if j==i else F(1,2*h) for j in range(N)])
  for path in paths:pts.append([F(1,h) if i in path else F(1,2*h) for i in range(N)])
  for target,x in enumerate(pts):
   for j,f in enumerate(chain):ck(f(x)==0 if j==target else f(x)>0)
   witnesses+=1
  if a==b==3:ck(len(order)==14 and len(chain)==15)
for n in range(2,25):
 X=set(range(n))
 for d in range(1,n):
  frozen={frozenset((s+t)%n for t in range(d)) for s in range(n)}
  comp={frozenset(X-set(I)) for I in frozen}
  expected={frozenset((s+d+t)%n for t in range(n-d)) for s in range(n)}
  ck(comp==expected);ck((comp==frozen)==(2*d==n))
  for I in frozen:ck(len(X-set(I))==n-d)
for r in range(1,20):
 for degree in range(1,20):
  for val in range(-9,10):ck(F(r*val,r*degree)==F(val,degree))
Path('independent_results.json').write_text(json.dumps({'assertions':count,'facet_witnesses':witnesses,'result':'PASS','scope':'Exact rational irredundancy witnesses for grids up to5x5, cyclic complements and degree scaling. No full plabic-flow theorem is computationally certified.'},indent=2)+'\n');print(count,witnesses)

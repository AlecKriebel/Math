#!/usr/bin/env python3
from itertools import product,combinations
import json
N=0;patterns=0;certified=0
def ck(v):
 global N
 assert v;N+=1
for n in range(3,7):
 G=set(range(n));subsets=[set(c) for d in range(n-1) for c in combinations(range(n),d)]
 # All patterns through n=4; deterministic structured control sample beyond.
 triples=product(subsets,repeat=3) if n<=4 else ((subsets[i],subsets[(3*i+j)%len(subsets)],subsets[(7*i+2*j)%len(subsets)]) for i in range(len(subsets)) for j in range(13))
 for DA,DB,DC in triples:
  ds=list(map(len,[DA,DB,DC]));ret=[G-DA,G-DB,G-DC];deleted=[DA,DB,DC]
  grid=[(a,b,(-a-b)%n) for a in G for b in G]
  kept=[t for t in grid if sum(t[i] in ret[i] for i in range(3))>=2]
  T=sum(a in DA and b in DB and c in DC for a,b,c in grid)
  P=ds[0]*ds[1]+ds[1]*ds[2]+ds[2]*ds[0]
  ck(len(kept)==n*n-P+2*T)
  good=False
  for i in range(3):
   j,k=(i+1)%3,(i+2)%3
   losses={a:sum((-a-b)%n in deleted[k] for b in deleted[j]) for a in ret[i]}
   for a,loss in losses.items():ck(sum(t[i]==a for t in kept)==n-loss)
   if any(x==0 for x in losses.values()):good=True
   if n-ds[i]>ds[j]*ds[k]:ck(any(x==0 for x in losses.values()))
  D=sum(ds)
  if D<=n-2 and D*D+3*D<9*n:ck(good);certified+=1
  patterns+=1
for n,expected in [(10,8),(100,28),(10000,298)]:
 largest=max(d for d in range(n-1) if d*d+3*d<9*n);ck(largest==expected)
for a,b,c in product(range(21),repeat=3):ck(3*(a*b+b*c+c*a)<=(a+b+c)**2)
print(json.dumps({'status':'PASS','assertions':N,'finite_deletion_patterns':patterns,'uniform_budget_controls':certified,'scope':'Exact cyclic incidence controls; the all-n deletion theorem is proved analytically.'},indent=2,sort_keys=True))

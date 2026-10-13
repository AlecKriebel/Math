from itertools import product
from collections import Counter
import json
X=range(4);pairs=list(product(X,repeat=2));triples=list(product(X,repeat=3))
row=lambda x:x//2;col=lambda x:x%2;mul=lambda x,y:2*row(x)+col(y)
stats=Counter();witness=None
# G depends only on the column of its first argument. Enumerate all such maps.
for g in product(range(2),repeat=8):
 G=lambda j,b:g[4*j+b]
 if not all(G(l,2*i+G(j,c))==G(l,c) for i,j,l,c in product(range(2),range(2),range(2),X)):continue
 stats['column_profiles']+=1
 fixed={}
 for i,l,j,c in product(range(2),range(2),range(2),X):fixed[(2*i+l,2*i+G(j,c))]=i
 free=[p for p in pairs if p not in fixed]
 for v in product(range(2),repeat=len(free)):
  F=fixed|dict(zip(free,v));add=lambda a,b:2*F[a,b]+G(col(a),b)
  if not all(add(add(a,b),c)==add(a,add(b,c)) for a,b,c in triples):continue
  stats['generalized_braces']+=1
  assert all(mul(a,add(b,c))==add(mul(a,b),mul(a,add(a,c))) for a,b,c in triples)
  r=lambda a,b:(mul(a,add(a,b)),mul(add(a,b),b))
  fails=[]
  for a,b,c in triples:
   u,v=r(a,b);w,z=r(v,c);x,y=r(u,w);L=(x,y,z)
   u,v=r(b,c);w,z=r(a,u);x,y=r(z,v);R=(w,x,y)
   if L!=R:fails.append({'input':[a,b,c],'left':L,'right':R})
  stats['YBE_pass' if not fails else 'YBE_fail']+=1
  if fails and witness is None:witness={'addition':[add(a,b) for a,b in pairs],'multiplication':[mul(a,b) for a,b in pairs],'first_failure':fails[0]}
print(json.dumps({'stats':dict(stats),'first_counterexample':witness},indent=2))

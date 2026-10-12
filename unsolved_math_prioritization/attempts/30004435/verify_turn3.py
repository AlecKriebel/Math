from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import random,json
checks=0;pairs=0;rng=random.Random(443503)
def check(x):
 global checks
 assert x;checks+=1
# Independent algebraic maximal coupling, including zero total discrepancy.
for size in range(2,8):
 for case in range(30):
  a=[rng.randrange(8) for _ in range(size)];b=[rng.randrange(8) for _ in range(size)]
  if not sum(a):a[0]=1
  if not sum(b):b[0]=1
  a=[F(x,sum(a)) for x in a];b=[F(x,sum(b)) for x in b];c=[min(x,y) for x,y in zip(a,b)];d=1-sum(c)
  C=[[F(0)]*size for _ in range(size)]
  for i in range(size):
   for j in range(size):C[i][j]=(c[i] if i==j else F(0))+((a[i]-c[i])*(b[j]-c[j])/d if d else 0)
  check([sum(row) for row in C]==a);check([sum(C[i][j] for i in range(size)) for j in range(size)]==b)
  check(sum(C[i][j] for i in range(size) for j in range(size) if i!=j)==sum(abs(x-y) for x,y in zip(a,b))/2)
# Truncated infinite-memory binary kernel. Histories ordered newest first.
for L in range(1,8):
 words=list(product(range(2),repeat=L));g={w:F(1,2)+sum(F(2*x-1,2**(j+3)) for j,x in enumerate(w)) for w in words}
 check(all(F(1,4)<=p<=F(3,4) for p in g.values()))
 for x in words:
  for y in words:
   k=next((i for i in range(L) if x[i]!=y[i]),L);check(abs(g[x]-g[y])<=F(1,2**(k+1)));pairs+=1
 for k in range(L):
  x=(0,)*L;y=(0,)*k+(1,)*(L-k)
  check(abs(g[x]-g[y])==F(1,2**(k+1))-F(1,2**(L+1)))
# Worst-case agreement run: increment with1-v_k, reset withv_k.
for kind in ['geometric','quadratic']:
 v=(lambda k:F(1,2**(k+1))) if kind=='geometric' else (lambda k:F(1,2*(k+1)*(k+2)))
 tail=(lambda l:F(1,2**l)) if kind=='geometric' else (lambda l:F(1,2*(l+1)))
 eps=1-v(0);dist={0:F(1)}
 for n in range(1,41):
  nxt=defaultdict(F)
  for k,p in dist.items():nxt[0]+=p*v(k);nxt[k+1]+=p*(1-v(k))
  dist=dict(nxt);check(sum(dist.values())==1)
  horizon=12;success=F(0)
  for k,p in dist.items():
   for j in range(k,k+horizon):p*=1-v(j)
   success+=p
  fail=1-success
  for l in range(1,min(n,10)+1):
   bound=(1-eps**l)**(n//l)+tail(l);check(fail<=bound)
   survival=F(1)
   for j in range(l,l+30):survival*=1-v(j)
   check(1-survival<=tail(l))
# Hitting a run of l by n compared to disjoint guaranteed-agreement blocks.
for eps in [F(1,4),F(1,2),F(3,4)]:
 for l in range(1,9):
  d={0:F(1)}
  for n in range(1,65):
   nd=defaultdict(F)
   for k,p in d.items():
    nd[0]+=p*(1-eps)
    if k+1<l:nd[k+1]+=p*eps
   d=nd;check(sum(d.values())<=(1-eps**l)**(n//l))
print(json.dumps(dict(assertions=checks,truncated_history_pairs=pairs,run_length_models=2,scope='Exact algebraic and finite-horizon controls for a proved infinite-memory coupling criterion; unrestricted original still unresolved.'),indent=2,sort_keys=True))

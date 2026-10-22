#!/usr/bin/env python3
"""Exact coefficient controls for the conditioned subdivision representation."""
from itertools import product,combinations
import json
H=list(combinations(range(4),2));m=len(H);assert m==6
checks=0;cases=0

def eq(a,b):
 global checks
 assert a==b,(a,b);checks+=1
for q in (3,4,5):
 a=q-2;r=q-1
 for W in range(16):
  cases+=1;J=[i for i,(u,v) in enumerate(H) if W>>u&1 and W>>v&1];jpos={e:k for k,e in enumerate(J)};k=len(J)
  direct=[0]*(1<<k)
  for g in product(range(q),repeat=4):
   if any(W>>v&1 and g[v]==0 for v in range(4)):continue
   outside=1
   for i,(u,v) in enumerate(H):
    if i not in jpos:outside*=a+(g[u]==g[v])
   for S in range(1<<k):
    w=outside
    for e,j in jpos.items():
     if not(S>>j&1):u,v=H[e];w*=a-1+(g[u]==g[v])
    direct[S]+=w
  predicted=[0]*(1<<k);RC=[]
  for eta in range(1<<m):
   parent=list(range(4))
   def root(x):
    while parent[x]!=x:x=parent[x]
    return x
   for e,(u,v) in enumerate(H):
    if eta>>e&1:parent[root(u)]=root(v)
   components={root(v) for v in range(4)};marked={root(v) for v in range(4) if W>>v&1}
   cluster=r**len(marked)*q**(len(components)-len(marked))
   RC.append(cluster*a**(m-eta.bit_count()))
   C=sum((not(eta>>e&1))<<j for e,j in jpos.items());outside_closed=m-eta.bit_count()-C.bit_count()
   for S in range(1<<k):
    if S&C==S:predicted[S]+=cluster*a**outside_closed*(a-1)**(C.bit_count()-S.bit_count())
  eq(direct,predicted);eq(sum(direct),sum(RC))
  for x in range(1<<m):
   for y in range(1<<m):
    assert RC[x&y]*RC[x|y]>=RC[x]*RC[y];checks+=1
  # Finite extra control: the resulting marginal also passes its lattice inequalities.
  for x in range(1<<k):
   for y in range(1<<k):
    assert direct[x&y]*direct[x|y]>=direct[x]*direct[y];checks+=1
# Adding a latent nonzero restriction need not increase an already observable zero.
from fractions import Fraction as F
triangle=[(0,1),(0,2),(1,2)];ratios=[]
for W in (3,7):
 z=0;numer=0
 for g in product(range(3),repeat=3):
  if any(W>>v&1 and g[v]==0 for v in range(3)):continue
  weights=[1+(g[u]==g[v]) for u,v in triangle]
  z+=weights[0]*weights[1]*weights[2]
  numer+=weights[1]*weights[2]
 ratios.append(F(numer,z))
eq(ratios,[F(11,17),F(9,14)]);assert ratios[0]>ratios[1];checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'latent_graph':'K4','q_values':[3,4,5],'all_boundary_subsets':16,'conditional_cases':cases,'triangle_conditioning_probabilities':[str(x) for x in ratios],'verified':'Direct conditional subdivision-coloring coefficients equal boundary-random-cluster closed-edge thinning; all finite boundary-RC and resulting marginal lattice inequalities checked.','scope':'Finite algebra controls; universal conditional representation and event theorem are proved separately.'},indent=2))

#!/usr/bin/env python3
"""Independent final-turn controls; no author code or solver is imported."""
from itertools import product,permutations
from fractions import Fraction as F
from collections import Counter
import json
C=Counter()
def check(v,k):
 assert v,k;C[k]+=1
P=[(1,2,12),(1,4,10),(1,6,8),(1,14),(2,4,9),(2,5,8),(2,13),(3,4,8),(3,12),(4,11),(5,10),(6,9),(7,8),(15,)]
h=dict(zip(P,[44,35,35,44,35,26,44,44,44,44,44,35,44,44]))
def part(word):
 blocks={}
 for i,c in enumerate(word):blocks[c]=blocks.get(c,0)+(1<<i)
 return tuple(sorted(blocks.values()))
words=list(product(range(3),repeat=4));weights=[]
for strict in [False,True]:
 w={c:(198*h[part(c)]+135*(3-len(part(c))) if strict else h[part(c)]) for c in words}
 Z=sum(w.values());check(Z==(648000 if strict else 3240),'word_totals')
 for c in words:
  check(w[c]>0,'full_support')
  for perm in permutations(range(3)):
   check(w[tuple(perm[x] for x in c)]==w[c],'color_symmetry')
 mu=[0]*16
 for c,v in w.items():mu[sum((x==0)<<i for i,x in enumerate(c))]+=v
 weights.append((mu,Z))
 for i in range(4):check(sum(mu[s] for s in range(16) if s>>i&1)*3==Z,'one_color_marginals')
 for e in range(1<<16):
  if not all(not(e>>s&1) or all(e>>(s|1<<i)&1 for i in range(4)) for s in range(16)):continue
  total=sum(mu[s] for s in range(16) if e>>s&1)
  for i in range(4):
   joint=sum(mu[s] for s in range(16) if e>>s&1 and s>>i&1)
   check(3*joint>=total,'singleton_regression')
 for fine in P:
  for coarse in P:
   if fine==coarse or not all(any(b&c==b for c in coarse) for b in fine):continue
   hf=198*h[fine]+135*(3-len(fine)) if strict else h[fine]
   hc=198*h[coarse]+135*(3-len(coarse)) if strict else h[coarse]
   check(hc>hf if strict else hc>=hf,'partition_coarsening')
 MF=sum(mu[s] for s in range(16) if s&3==3);MG=sum(mu[s] for s in range(16) if s&12==12)
 check(F(MF,Z)==(F(46,375) if strict else F(11,90)),'conjunction_F')
 check(F(MG,Z)==F(MF,Z),'conjunction_G')
 check(F(mu[15],Z)==(F(499,36000) if strict else F(11,810)),'joint_conjunction')
 check(F(mu[15],Z)-F(MF*MG,Z*Z)==(F(-593,500000) if strict else F(-11,8100)),'negative_covariance')
mu,Z=weights[0];check(mu[14]==2*mu[15],'base_monochromatic_equality')
check(F(sum(mu[s] for s in range(16) if s&3==3),Z)!=F(1,9),'base_component_independence_contradiction')

# Full proper-coloring enumeration for every labeled 3+3 bipartite graph.
# Every nonempty observed terminal subset is tested, hence hidden A vertices
# and disconnected components occur explicitly.
for mask in range(512):
 E=[(a,3+b) for a in range(3) for b in range(3) if mask>>(3*a+b)&1]
 colorings=[w for w in product(range(3),repeat=6) if all(w[a]!=w[b] for a,b in E)]
 parent=list(range(6))
 def root(x):
  while x!=parent[x]:x=parent[x]
  return x
 for a,b in E:parent[root(a)]=root(b)
 for Tmask in range(1,8):
  T=[i for i in range(3) if Tmask>>i&1];counts=Counter(tuple(w[i] for i in T) for w in colorings)
  mono=counts[(0,)*len(T)]
  for phi in product(range(3),repeat=len(T)):
   constant=all(phi[i]==phi[j] for i in range(len(T)) for j in range(len(T)) if root(T[i])==root(T[j]))
   check((counts[phi]==mono)==constant,'monochromatic_equality_characterization')
   for c,d in [(0,1),(0,2),(1,2)]:
    psi=tuple(c if x==d else x for x in phi)
    check(counts[psi]>=counts[phi],'terminal_coarsening_count')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'breakdown':dict(C),'scope':'Both exact auxiliary color laws and all 512 bipartite graphs on 3+3 labeled vertices, all nonempty terminal subsets and color prescriptions. This is a proof audit, not a graph-realization search.'},indent=2,sort_keys=True))

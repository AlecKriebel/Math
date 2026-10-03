from exact_linear import *
import random,json
rng=random.Random(62000044);checks=0;cats={};models=0
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
for d in range(2,9):
 for e in range(0,4):
  for trial in range(12):
   m=max(d,e+1);V=[rng.randrange(4) if k<=d else 0 for k in range(m+2)];E=[rng.randrange(4) if k<=e else 0 for k in range(m+2)];V[d]=rng.randrange(1,4);E[e]=rng.randrange(1,4)
   # Complexes V,E have zero internal differential; arbitrary degreewise delta gives a cochain map.
   delta=[[[rng.randrange(-2,3) for _ in range(V[k])] for _ in range(E[k])] for k in range(m+1)]
   rs=[rank(a) for a in delta];dims=[V[k]+(E[k-1] if k else 0) for k in range(m+2)]
   b=[dims[k]-(rs[k] if k<=m else 0)-(rs[k-1] if k else 0) for k in range(m+2)]
   ck(all(x>=0 for x in b),'cone_betti_nonnegative');ck(all(not b[k] for k in range(max(d,e+1)+1,m+2)),'cone_upper_bound')
   if d>e+1:ck(b[d]==V[d]>0,'top_vertex_degree_survives')
   models+=1
# Every admissible small-edge dimension profile of a candidate carries its failure at a vertex of maximal d.
for d1 in range(1,10):
 for q1 in range(1,d1+1):
  if q1==1 and d1!=1:continue
  for d2 in range(1,10):
   for q2 in range(1,d2+1):
    if q2==1 and d2!=1:continue
    d=max(d1,d2);q=max(q1,q2)
    if d<4:continue
    v=(q1,d1) if d1>=d2 else (q2,d2)
    ck(v[1]==d and v[0]<=q,'maximal_vertex_profile')
    if 3*q<2*d:ck(3*v[0]<2*v[1],'ratio_violation_descends')
for d in [3,4]:
 for q in range(3,d+1):ck(3*q>=2*d,'low_dim_fibering_exclusion')
print(json.dumps({'assertions':checks,'categories':cats,'mapping_cone_models':models,'scope':'Finite cochain and dimension-profile controls; no group existence, accessibility or subgroup theorem is computationally inferred.'},sort_keys=True,indent=2))

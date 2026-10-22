#!/usr/bin/env python3
from collections import Counter
from itertools import combinations
import json
counts=Counter();graphs=0
def ck(g,v):
 if not v:raise AssertionError(g)
 counts[g]+=1
# Exhaustive small bipartite cut choices in all labeled graphs through order six.
for n in range(2,7):
 es=list(combinations(range(n),2))
 for mask in range(1<<len(es)):
  adj=[0]*n
  for i,(u,v) in enumerate(es):
   if mask>>i&1:adj[u]|=1<<v;adj[v]|=1<<u
  deg=[v.bit_count() for v in adj]
  if 0 in deg:continue
  graphs+=1;w=len(set(deg));d=n-w
  for C in range(1,1<<n):
   if any(adj[v]&C for v in range(n) if C>>v&1):continue
   S=n-C.bit_count();B=((1<<n)-1)^C
   lhs=sum(deg[v] if B>>v&1 else -deg[v] for v in range(n))
   twice=sum((adj[v]&B).bit_count() for v in range(n) if B>>v&1)
   ck('exact_cut_identity',lhs==twice)
   if w>=S:ck('quadratic_degree_cut_bound',w*(w+1)//2-S*(S+1)-d*S<=twice)

# Independently minimize the signed representative sum over degree sets.
for n in range(2,12):
 for S in range(1,n):
  for w in range(S,n):
   actual=min(sum(-t if t<=S else t for t in D) for D in combinations(range(1,n),w))
   ck('representative_minimum',actual==w*(w+1)//2-S*(S+1))
for d in range(1,101):
 w=6*d;s=3*d;lower=w*(w+1)//2-s*(s+1)-d*s
 ck('geometric_relaxation_excluded',lower==6*d*d>4*d*d)
ck('twelve_vertex_first_shape_excluded',10*11//2-5*6-2*5>2*2*3)
ck('twelve_vertex_second_shape_survives',10*11//2-6*7-2*6<=2*2*4)
for a in range(1,8):
 for b in range(a,8):
  c=7-a-b
  if c<b:continue
  if a<=1 and b<=a+1 and c<=a+b+1:ck('seven_vertex_partition_unique',(a,b,c)==(1,2,4))
print(json.dumps({'problem_id':3242,'author_turn':2,'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'isolate_free_labelled_graphs_through_six':graphs,'scope':'Finite exact cut identities, degree-set minimization and partition controls. General analytic inequalities are proved in TURN_2.md; the full Melnikov target remains open in this work.'},indent=2,sort_keys=True))

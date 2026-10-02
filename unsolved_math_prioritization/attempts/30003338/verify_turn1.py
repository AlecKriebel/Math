#!/usr/bin/env python3
"""Exact small-graph controls, separate from the universal scoped proofs."""
from itertools import product
from fractions import Fraction as F
import json
from pathlib import Path
count=0;forest_cases=0

def eq(a,b):
 global count
 assert a==b,(a,b)
 count+=1
# All simple subgraphs of K_3,3 which are forests; full proper colorings at q=3,4.
for edge_mask in range(512):
 edges=[(i,3+j) for i in range(3) for j in range(3) if edge_mask>>(3*i+j)&1]
 parent=list(range(6))
 def root(v):
  while parent[v]!=v:v=parent[v]
  return v
 cyclic=False
 for a,b in edges:
  x,y=root(a),root(b)
  if x==y:cyclic=True;break
  parent[x]=y
 if cyclic:continue
 deg=[sum(v in e for e in edges) for v in range(6)]
 for q in (3,4):
  forest_cases+=1
  weights=[0]*64
  for colors in product(range(q),repeat=6):
   if any(colors[a]==colors[b] for a,b in edges):continue
   zero=sum((colors[v]==0)<<v for v in range(6));weights[zero]+=1
  const=(q-1)**(6-len(edges))*(q-2)**len(edges)
  lam=[F(q-1)**(d-1)/F(q-2)**d for d in deg]
  marginal=[0]*8
  for S,w in enumerate(weights):
   expected=F(const)
   if any(S>>a&1 and S>>b&1 for a,b in edges):expected=0
   else:
    for v in range(6):
     if S>>v&1:expected*=lam[v]
   eq(w,expected);marginal[S&7]+=w
  for S in range(8):
   expected=F(const)
   for a in range(3):
    if S>>a&1:expected*=lam[a]
   for b in range(3,6):
    if not any(v==b and S>>u&1 for u,v in edges):expected*=1+lam[b]
   eq(marginal[S],expected)
  for S in range(8):
   for T in range(8):
    assert marginal[S&T]*marginal[S|T]>=marginal[S]*marginal[T];count+=1
# Reconstruct the published dreidel graph directly and its conditional probabilities.
nb=[25,14,22,6];w=[0]*32
for c in product(range(3),repeat=5):
 ways=1
 for mask in nb:ways*=3-len({c[a] for a in range(5) if mask>>a&1})
 w[sum((c[a]==0)<<a for a in range(5))]+=ways
mass=lambda mask:sum(w[S] for S in range(32) if S&mask==mask)
eq(sum(w),336);eq(F(mass(3),mass(2)),F(23,56));eq(F(mass(7),mass(6)),F(9,22))
# The complete C++ event scan uses these same 32 independently generated weights.
saved=json.loads((Path(__file__).parent/'TURN_1_SEARCH.json').read_text());eq(w,saved['dreidel_zero_mask_weights'])
print(json.dumps({'status':'PASS','exact_assertions':count,'forest_graph_q_cases':forest_cases,'dreidel_total':336,'published_conditional_probabilities':['23/56','9/22'],'scope':'All labeled K3,3 forest subgraphs at q3,4 verify the exact hard-core reduction and FKG lattice condition. Dreidel calculations replay known stronger-condition failure; not a full-target counterexample.'},indent=2))

#!/usr/bin/env python3
from itertools import combinations
from math import comb
from fractions import Fraction as F
import json
checks=templates=obstructions=0
# Exact parameterized-family endpoint test.
for n in range(1,81):
 for r in range(1,n+1):
  for h in range(r,n+1):
   x=F(comb(h,r),comb(n,r));y=F(r,n)
   assert x<=F(h,n);checks+=1
   if r>=2:assert x<=F(h,n)**2;checks+=1
   for k in range(1,16):
    if h*k<n:
     assert not(x+k*y>1 and k*x+y>=1);checks+=1;obstructions+=1
   templates+=1
# Verify the union-size bound on every family of r-sets when |B|<=15.
for n in range(1,7):
 for r in range(1,n+1):
  bs=[sum(1<<i for i in c) for c in combinations(range(n),r)]
  if len(bs)>15:continue
  for mask in range(1,1<<len(bs)):
   u=0;s=0
   for i,b in enumerate(bs):
    if mask>>i&1:u|=b;s+=1
   assert s<=comb(u.bit_count(),r);checks+=1
# Full 396-vertex certificate, ordinary unweighted graph.
A=list(combinations(range(11),9));B=list(combinations(range(11),4));C=list(range(11))
AB=[[i for i,b in enumerate(B) if set(b)<=set(a)] for a in A]
reach=[set().union(*(set(B[i]) for i in row)) for row in AB]
for a,row,rr in zip(A,AB,reach):
 assert len(row)==126>=120;checks+=1
 assert rr==set(a);checks+=1
for b in B:assert len(b)==4;checks+=1
for c in C:
 assert sum(c in rr for rr in reach)==45;checks+=1
for c,d in combinations(C,2):
 missing=[i for i,rr in enumerate(reach) if c not in rr and d not in rr]
 assert len(missing)==1;checks+=1
 assert len([b for b in B if c not in b and d not in b])==126;checks+=1
assert F(4,11)*3>1;checks+=1
assert F(126,330)>F(4,11);checks+=1
assert F(45,55)==F(9,11);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'complete_uniform_templates':templates,'integer_k_no_counterexample_controls':obstructions,'explicit_graph_part_sizes':[55,330,11],'scope':'Exact finite controls; universal family proof and LP duality are in TURN_1.md. No unrestricted counterexample.'},indent=2))

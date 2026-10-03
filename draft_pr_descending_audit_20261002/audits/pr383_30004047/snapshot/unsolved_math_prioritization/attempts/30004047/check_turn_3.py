#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import json
checks=bounds=charges=0
for k in range(2,101):
 for n in range(k+1,8*k+1):
  r=(n-1)//k
  assert k*r<n;checks+=1
  if r>=2:
   for t in range(k):
    for u in {0,min(n,t*r),min(n,t*r)//2}:
     z=F(u,r)+F(n-u,r-1)
     assert z==F(r*n-u,r*(r-1));checks+=1
     assert z>=F(n-t,r-1)>=F(n-k+1,r-1);checks+=1;charges+=1
   if n<=4*k:
    assert F(r-1,n-k+1)<=F(1,k+1);checks+=1;bounds+=1
# Exact support-weight and compatibility control at n=9.
T=frozenset(range(4));D=set(range(4,9));triples=list(map(frozenset,combinations(D,3)))
S=[T]+triples;beta=[F(3,8)]+[F(1,16)]*10
assert sum(beta)==1;checks+=1
for a in range(9):
 assert sum(b for s,b in zip(S,beta) if a in s)==F(3,8);checks+=1
for s in S:
 assert sum(F(1,4) if a in T else F(1,3) for a in s)==1;checks+=1
for size in range(5):
 for cc in combinations(range(9),size):
  c=set(cc)
  assert sum(s<=c for s in triples)<=4;checks+=1
  if T<=c:assert sum(s<=c for s in triples)==0;checks+=1
assert F(4,14)==F(2,7)<F(1,3);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_size_threshold_controls':bounds,'charge_controls':charges,'scope':'Exact cardinality/charge checks and the nonrealizable nine-vertex first-incidence relaxation; proofs in TURN_3.md.'},indent=2))

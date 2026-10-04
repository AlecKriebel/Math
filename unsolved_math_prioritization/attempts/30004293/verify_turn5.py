#!/usr/bin/env python3
"""Finite exact controls for exponential tilting and pigeonhole inequalities."""
from fractions import Fraction as F
from itertools import combinations
from math import prod
import json
checks=0;sets=0;tilts=0;momentcases=0
for n in range(1,12):
 records=[]
 for mask in range(1<<(n-1)):
  A={1}|{i for i in range(2,n+1) if mask>>(i-2)&1}
  p=prod((F(1,i) if i in A else F(i-1,i)) for i in range(1,n+1))
  r={0:1}
  for a in sorted(A):
   for s,m in list(r.items()):r[s+a]=r.get(s+a,0)+m
  N=len(A);S=sum(A);M=max(r.values())
  assert sum(r.values())==2**N;assert M*(S+1)>=2**N;assert M<=2**N
  checks+=3;sets+=1;records.append((A,p,N,S,M))
 assert sum(p for A,p,N,S,M in records)==1;checks+=1
 for lam in [F(1,2),F(3,2),F(2),F(4),F(8)]:
  Z=prod(1+(lam-1)/i for i in range(1,n+1))
  total=F(0);meanN=F(0);meanS=F(0)
  for A,p,N,S,M in records:
   Q=prod((lam/F(i+lam-1) if i in A else F(i-1)/F(i+lam-1)) for i in range(1,n+1))
   assert Q==p*lam**N/Z;checks+=1;tilts+=1
   total+=Q;meanN+=Q*N;meanS+=Q*S
  assert total==1;assert meanN==sum(lam/(i+lam-1) for i in range(1,n+1));checks+=2
  if lam>=1:assert meanS<=lam*n;checks+=1
 for q in [1,2,3]:
  lam=F(2**q);Z=prod(1+(lam-1)/i for i in range(1,n+1))
  moment=sum(p*M**q for A,p,N,S,M in records)
  inverse=sum(p*lam**N/(S+1)**q for A,p,N,S,M in records)
  assert moment>=inverse>=Z/(lam*n+1)**q;checks+=1;momentcases+=1
  if q==2:
   exact=F((n+1)*(n+2)*(n+3),6)
   assert Z==exact;checks+=1
# Falling-factorial identity and factorial-moment upper bounds.
for n in range(1,10):
 for j in range(1,min(n,5)+1):
  mu=sum(F(1,i) for i in range(1,n+1))
  fact=sum(prod(F(1,i) for i in S) for S in combinations(range(1,n+1),j))
  fac=prod(range(1,j+1))
  assert fac*fact<=mu**j;checks+=1
# Exact product telescoping and a simple second-moment consequence.
for n in range(2,101):
 Z=prod(F(i+3,i) for i in range(1,n+1))
 assert Z==F((n+1)*(n+2)*(n+3),6);checks+=1
 assert Z/F((4*n+1)**2)>=F(n,150);checks+=1
print(json.dumps({'exact_assertions':checks,'finite_prefix_realizations':sets,'likelihood_ratio_cases':tilts,'raw_moment_cases':momentcases,'infinite_probabilistic_claims_tested':False},indent=2))

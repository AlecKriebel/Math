#!/usr/bin/env python3
from itertools import product
from fractions import Fraction as F
from math import factorial
from collections import defaultdict
import json
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
relcount=0;weighted=defaultdict(F);supports=[]
for m in range(2,13):
 H=sum((F(1,i)for i in range(1,m)),F(0))
 for es in product((-1,0,1),repeat=m-1):
  if sum((i+1)*e for i,e in enumerate(es))+m:continue
  supp=[i+1 for i,e in enumerate(es)if e]+[m];ell=len(supp);n=supp[-2]
  ck(ell>=3);ck(n*(ell-1)>=m)
  p=F(1)
  for a in supp:p/=a
  weighted[m,ell]+=p;relcount+=1;supports.append(frozenset(supp))
 for ell in range(3,m+1):
  bound=F(2**(ell-1)*(ell-1),factorial(ell-2)*m*m)*H**(ell-2)
  ck(weighted[m,ell]<=bound)
# The symmetric-difference core implication for every finite sample through 9.
finite_cases=0
for mask in range(1<<9):
 A=[i+1 for i in range(9)if mask>>i&1]
 for h in range(1,4):
  fibers=defaultdict(list)
  for bits in range(1<<len(A)):
   B=frozenset(a for j,a in enumerate(A)if bits>>j&1)
   if len(B)<=h:fibers[sum(B)].append(B)
  core=set()
  for Bs in fibers.values():
   for B in Bs[1:]:core.update(B^Bs[0])
  N=max(core,default=0)
  for Bs in fibers.values():
   outside={frozenset(a for a in B if a>N)for B in Bs};ck(len(outside)==1)
   ck(len(Bs)<=2**len([a for a in A if a<=N]))
  finite_cases+=1
print(json.dumps({'exact_assertions':checks,'signed_relations_enumerated':relcount,'largest_scale_checked':12,'fixed_cardinality_samples':finite_cases,'infinite_probabilistic_claims_tested':False},indent=2))

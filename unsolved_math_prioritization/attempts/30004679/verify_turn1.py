#!/usr/bin/env python3
"""Finite exact syntax and tail-fusion controls, not a test of infinite Ramsey existence."""
from itertools import combinations,product
import random,json
checks=0;families=0

def ok(x):
 global checks
 assert x
 checks+=1

def subword(a,b):
 it=iter(b)
 return all(any(x==y for y in it) for x in a)
def avoids(h,B):return not any(subword(t,h) for t in B)
def inverse_basis(U,i,B):
 out=[]
 for t in B:
  if not t:return [()]
  for a in combinations([u for u in U if u<t[0]],i):out.append(a+t)
 return out
rng=random.Random(30004679)
for size in range(2,10):
 U=tuple(range(size));words=[t for n in [1,2,3] for t in combinations(U,n)]
 for trial in range(13):
  B=[rng.sample(words,min(len(words),rng.randrange(1,5))) for _ in range(3)]
  Q=sum((inverse_basis(U,i,B[i]) for i in range(3)),[]);families+=1
  for n in range(size+1):
   for h in combinations(U,n):
    ok(avoids(h,Q)==all(avoids(h[i:],B[i]) for i in range(3)))
    for i in range(min(3,len(h))):
     for r in range(len(h)-i+1):
      for f in combinations(h[i:],r):
       g=h[:i]+f;ok(subword(g,h));ok(g[i:]==f)
# The first-coordinate union failure and its shifted repair.
for n in range(1,11):
 for h in combinations(range(14),n):
  ok(any(h[0]==i for i in range(14)))
  ok(any(x==i for i,x in enumerate(h))==(h[0]==0))
  if h[0]>0:
   for i in range(n):ok(all(x!=i for x in h[i:]))
# Finite nested reservoirs: the diagonal tails lie in every earlier reservoir.
for _ in range(101):
 R=sorted(rng.sample(range(200),80));Hs=[];Rs=[]
 for i in range(6):
  Rs.append(tuple(R));x=R[rng.randrange(min(3,len(R)))];Hs.append(x);R=[y for y in R if y>x]
 for i in range(6):ok(set(Hs[i:])<=set(Rs[i]))
print(json.dumps(dict(status='PASS',assertions=checks,finite_constraint_families=families,scope='finite exact checks of open-cylinder pullback and tail identities; infinite promise proof is analytic'),sort_keys=True,indent=2))

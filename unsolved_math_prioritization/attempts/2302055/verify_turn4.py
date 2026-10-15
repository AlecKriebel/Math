#!/usr/bin/env python3
from math import comb
import random,json
rng=random.Random(230205504);checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def clean(A):return {k:v for k,v in A.items()if v}
def plus(A,B):
 C=A.copy()
 for k,v in B.items():C[k]=C.get(k,0)+v
 return clean(C)
def shift(A,m):return {k+m:v for k,v in A.items()}
def prod(g,h):
 A,m=g;B,r=h;return (plus(A,shift(B,m)),m+r)
def inv(g):
 A,m=g;return ({k:-v for k,v in shift(A,-m).items()},-m)
def action(g,x):
 A,m=g;k,n=x;return (k+m,n+A.get(k+m,0))
def comm(g,h):return prod(prod(prod(g,h),inv(g)),inv(h))
I=({},0)
for _ in range(500):
 g=(clean({k:rng.randrange(-3,4)for k in range(-3,4)}),rng.randrange(-4,5));h=(clean({k:rng.randrange(-3,4)for k in range(-3,4)}),rng.randrange(-4,5))
 ck(prod(g,inv(g))==I);ck(prod(inv(g),g)==I)
 for k in range(-7,8):ck(action(prod(g,h),(k,2))==action(g,action(h,(k,2))))
finite_difference_cases=0
for r in range(1,9):
 for s in range(1,7):
  a=({},r);b=({0:s},0);c=b
  for k in range(1,25):
   c=comm(a,c);expected={r*j:s*(-1)**(k-j)*comb(k,j)for j in range(k+1)}
   ck(c==(expected,0));ck(c[0][r*k]==s);ck(c!=I);finite_difference_cases+=1
print(json.dumps({'exact_assertions':checks,'group_law_cases':500,'iterated_commutator_cases':finite_difference_cases,'analytic_counterexample_claimed':False},indent=2))

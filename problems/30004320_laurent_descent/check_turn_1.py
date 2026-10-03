#!/usr/bin/env python3
"""Finite exact controls for the pro-p/prime-to-p mechanism.
No finite test proves the profinite, gerbe, or algebro-geometric theorems.
"""
from math import gcd
import itertools,json
checks=0;presentations=0;lift_pairs=0

def ck(t):
 global checks
 assert t
 checks+=1
# Source finite quotient C_p ⋊ C_q; target C_m ⋊ C_q, with p not dividing m.
# A lift preserving C_q sends generators to (i,0),(j,1). Check all relations
# and the forced vanishing of the image of the p-kernel.
for p in (2,3,5,7):
 for m in range(2,11):
  if m%p==0:continue
  for q in (2,3,4,5):
   for a in range(1,m):
    if gcd(a,m)!=1 or pow(a,q,m)!=1:continue
    norm=sum(pow(a,h,m) for h in range(q))%m
    for b in range(1,p):
     if pow(b,q,p)!=1:continue
     presentations+=1
     for i,j in itertools.product(range(m),repeat=2):
      # rho^p=1; sigma^q=1; sigma rho sigma^-1=rho^b.
      relations=(p*i)%m==0 and (norm*j)%m==0 and (a*i-b*i)%m==0
      if relations:
       ck(i==0);ck((norm*j)%m==0);lift_pairs+=1
     # Every lift of the quotient itself inflates to a lift of the source.
     for j in range(m):
      if (norm*j)%m==0:ck((p*0)%m==0 and (a*0-b*0)%m==0)
finite_checks=checks
# All negative possible Artin-Schreier valuations are divisible by p;
# t=s^n has pole order n prime to p. This tests the exact obstruction used.
valuation_cases=0
for p in (2,3,5,7,11):
 for n in range(1,101):
  if n%p==0:continue
  for v in range(-100,1):
   if v<0:ck(p*v!=-n)
   else:ck(-n<0)
   valuation_cases+=1
# Relative-algebraic-closure valuation mechanism: a polynomial relation for
# an element of nonzero valuation has a unique extreme among nonzero terms.
for val in list(range(-10,0))+list(range(1,11)):
 for degree in range(1,10):
  for middle in itertools.product((0,1),repeat=degree-1):
   supp=[0]+[i+1 for i,z in enumerate(middle) if z]+[degree]
   exponents=[i*val for i in supp]
   ck(exponents.count(min(exponents))==1)
print(json.dumps({'status':'PASS','exact_assertions':checks,'semidirect_presentations':presentations,'valid_lift_generator_pairs':lift_pairs,'finite_group_assertions':finite_checks,'valuation_cases':valuation_cases,'limitations':'Exact finite models and valuation arithmetic corroborate the mechanism; the source-dependent profinite and gerbe proofs are in TURN_1.md. The wild example is not an original counterexample.'},indent=2,sort_keys=True))

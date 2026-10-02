#!/usr/bin/env python3
"""Exact controls for the heavy-interval and quantile-strip bounds."""
from fractions import Fraction as Q
from itertools import product
from math import factorial
import json
checks=0;trees=0
# Finite dyadic mass trees: recursively choosing the heavier closed-half model.
for leaves in product(range(3),repeat=8):
 total=sum(leaves)
 if not total:continue
 trees+=1
 indices=list(range(8));mass=total
 for depth in range(1,4):
  left=indices[:len(indices)//2];right=indices[len(indices)//2:]
  lm=sum(leaves[i] for i in left);rm=sum(leaves[i] for i in right)
  indices=left if lm>=rm else right;mass=max(lm,rm)
  assert mass*2**depth>=total;checks+=1
# Exact geometric and probability constants in the d=s=1 case.
for n in range(3,201):
 M=2*n-1;ell=Q(1,M);delta=ell*ell/4
 assert ell*ell-2*delta==ell*ell/2;checks+=1
 assert delta/M>=Q(1,32*n**3);checks+=1
 p=Q(factorial(n),1)*(delta/M)**n
 count=Q(1024*factorial(n)**3,128**n)
 assert count*p>=Q(1024*factorial(n)**4,4096**n*n**(3*n));checks+=1
# Threshold exponent d>2s/3, tested as exact rationals on a parameter grid.
for dd in range(1,41):
 for dn in range(1,dd+1):
  d=Q(dn,dd)
  for ss in range(21):
   s=Q(ss,20)
   assert (3-2*s/d>0)==(d>2*s/3);checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'dyadic_mass_trees':trees,
 'sample_sizes':[3,200],'scope':'Exact finite controls; the universal product-measure and line-nullness proofs are in TURN_3.md.'},indent=2,sort_keys=True))

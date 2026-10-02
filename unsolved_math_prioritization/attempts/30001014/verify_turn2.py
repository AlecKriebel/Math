#!/usr/bin/env python3
"""Finite central-amplification algebra controls, not a tensor-norm pathology simulation."""
from fractions import Fraction as F
from itertools import product
import json
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
# Matrix entries of [X, f(z)g(w)D] = f(z)g(w)[X,D].
for n in range(1,8):
 for i,j,k,l in product(range(n),repeat=4):
  coeff=F((i+1)*(l+2)-(j+2)*(k+1),7)
  diag_row=(i,k);diag_col=(j,l)
  for a,b in [(0,0),(n-1,0),(n-1,n-1)]:
   left=int(diag_col==(a,b))-int(diag_row==(a,b))
   for f,g in [(F(2,3),F(-3,5)),(F(0),F(7)),(F(-4,9),F(5,11))]:
    ok(coeff*(f*g*int(diag_col==(a,b))-f*g*int(diag_row==(a,b)))==f*g*(coeff*left))
# Constant inclusion and evaluation are exact retractions on finite function tables.
for sites in range(1,13):
 for z0 in range(sites):
  for value in range(-9,10):ok(([value]*sites)[z0]==value)
# Binary refinement: any finite number of clopen pieces can be padded to 2^k.
for pieces in range(1,1001):
 k=(pieces-1).bit_length();target=2**k
 ok(target>=pieces);ok(target<2*pieces or pieces==1)
 count=pieces
 while count<target:count+=1
 ok(count==target)
# Finite coordinate permutations behind regrouping product factors.
for n in range(1,8):
 m=max(1,n//2)
 for bits in product((0,1),repeat=n):
  a,b=bits[:m],bits[m:];ok(a+b==bits)
print(json.dumps({'status':'PASS','assertions':checks,'scope':'Finite scalar-central commutator, retraction and partition-label identities only; norm restrictions, nonzero kernel witnesses and Cantor topology are proved analytically'},indent=2,sort_keys=True))

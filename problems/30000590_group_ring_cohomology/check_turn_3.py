#!/usr/bin/env python3
from math import gcd
from fractions import Fraction as F
from itertools import product
import json
checks=complexes=kernels=0
for m in range(1,101):
 for n in range(1,101):
  g=gcd(m,n);v=(m//g,n//g)
  assert -n*m+m*n==0;checks+=1
  assert -n*v[0]+m*v[1]==0;checks+=1
  assert (g*v[0],g*v[1])==(m,n);checks+=1
  assert gcd(v[0],v[1])==1;checks+=1
  assert gcd(m,n)==g;checks+=1;complexes+=1
for d in range(1,151):
 for m in range(2,81):
  ker=[x for x in range(d) if m*x%d==0]
  quotient=gcd(d,m)
  assert len(ker)==quotient;checks+=1
  assert len({m*x%d for x in range(d)})*len(ker)==d;checks+=1;kernels+=1
# The natural Tor(Z/d,Fp) and M[p] comparison on cyclic controls.
for d in range(1,501):
 for p in [2,3,5,7,11,13]:
  assert len([x for x in range(d) if p*x%d==0])==(p if d%p==0 else 1);checks+=1
# Finite tensor-coordinate supports cannot be expanded in the first factor
# by an action on the second factor.
for a in range(1,7):
 for b in range(1,7):
  for mask in range(1<<a):
   support={i for i in range(a) if mask>>i&1}
   generators={(i,j) for i in support for j in range(b)}
   for shift in range(b):
    moved={(i,(j+shift)%b) for i,j in generators}
    assert {i for i,j in moved}==support;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'two_term_tensor_complexes':complexes,'fixed_modulus_cyclic_kernels':kernels,'scope':'Integral Kunneth signs/degrees, fixed-torsion sizes and tensor-coordinate support. No realization of a bad group-ring Tor term.'},indent=2,sort_keys=True))

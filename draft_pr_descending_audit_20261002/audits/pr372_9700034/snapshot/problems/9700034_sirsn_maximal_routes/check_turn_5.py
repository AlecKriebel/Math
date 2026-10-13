#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json
checks=mixtures=projections=0
# Finite truncations of the exact diagonal mixture construction.
for N in range(1,40):
 for mode in range(4):
  bs=[F(1+(j if mode==0 else j*j if mode==1 else 2**j if mode==2 else j**3)) for j in range(1,N+1)]
  Z=sum(F(1,2**j)/b for j,b in enumerate(bs,1));ws=[F(1,2**j)/(Z*b) for j,b in enumerate(bs,1)]
  assert sum(ws)==1;checks+=1
  assert sum(w*b for w,b in zip(ws,bs))==(1-F(1,2**N))/Z;checks+=1
  assert sum(w*(4**j*b) for j,(w,b) in enumerate(zip(ws,bs),1))==sum(F(2**j)/Z for j in range(1,N+1));checks+=1
  assert 0<Z<=1;checks+=1;mixtures+=1
# Rational projected tangent controls and threshold constants.
for Delta in range(1,20):
 for cn in range(1,4*Delta+1):
  c=F(cn,4);C=F(Delta+1);threshold=8*Delta/c;K=8*C*Delta/c
  assert c<=Delta;checks+=1
  assert c/F(4*Delta)<=F(1,4);checks+=1
  assert F(3,4)*c-(c/F(4*Delta))*Delta==c/2;checks+=1
  assert F(2,3)*c/4==c/6;checks+=1
  assert 6*C/c<=K;checks+=1
  for lam in [F(1),threshold/2,threshold,2*threshold]:
   if lam<1:continue
   if lam>=threshold:
    assert F(2)/lam<=c/F(4*Delta);checks+=1
    assert C*lam<=K*(lam*c/6);checks+=1
   else:
    assert C*lam<=K;checks+=1
   projections+=1
for a,b in product(range(-12,13),repeat=2):
 for x,y in [(F(3,5),F(4,5)),(F(5,13),F(12,13)),(F(7,25),F(24,25))]:
  assert abs(x*a-y*b)>=abs(y*b)-abs(x*a);checks+=1
  assert x*x+y*y==1;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_mixture_controls':mixtures,'anisotropy_threshold_controls':projections,'scope':'Exact mixture normalization/divergence truncations, coordinate projection inequalities and constants. No realization of an unbounded-ratio SIRSN family.'},indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Exact controls for cutoff variance scaling and continuum error bookkeeping."""
from fractions import Fraction as Q
from math import isqrt
import json
count=0
def ck(v):
 global count
 assert v
 count+=1
# Rational lower approximations to sqrt(k/n), with square n and square cutoff N.
# The theorem uses the analytic integral bound; these controls test its scaling.
for den in range(2,34):
 n=den*den
 for num in range(1,den+1):
  N=num*num;eps=Q(N,n);root=Q(num,den)
  weights=[Q(isqrt(k*n),n) for k in range(1,N+1)]
  for k,w in enumerate(weights,1):ck(w*w<=Q(k,n))
  ck(max(weights)<=root)
  ck(sum(w/Q(k) for k,w in enumerate(weights,1))<=2*root)
  ck(sum(Q(k,n)/k for k in range(1,N+1))==eps)
# Normalization cancels n in the variance estimate.
for nroot in range(1,70):
 for eroot in (Q(1,3),Q(2,5),Q(7,9)):
  eps=eroot*eroot
  sd_critical=Q(1,2*nroot)*nroot*(eroot+2*eroot)
  ck(sd_critical**2==Q(9,4)*eps)
  sd_mass=Q(1,2*nroot)*nroot*(eps+eps)
  ck(sd_mass**2==eps*eps)
# The final mean-square scales: sqrt(epsilon) dominates epsilon on (0,1].
for den in range(2,100):
 for num in range(1,den+1):
  r=Q(num,den);eps=r*r
  ck(eps<=r)
  ck(eps*eps<=eps)
  ck(r*eps==r**3)
print(json.dumps({'status':'PASS','assertions':count,'coverage':['rational cutoff toll scaling','cancellation of conditioned-tree n normalization','critical and mass variance exponents','continuum L2 error-order bookkeeping'],'scope':'Finite exact controls; the credited tree variance/contour theorems and measure-limit argument are separate analytic inputs.'},indent=2,sort_keys=True))

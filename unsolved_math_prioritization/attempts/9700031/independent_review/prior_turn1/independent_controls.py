#!/usr/bin/env python3
from fractions import Fraction as Q
from math import gcd
import json,random
n=0
# Derive rather than import the optimum: low exponent2-2a, high1+a(s-1).
for sd in range(1,17):
 for sn in range(sd,sd*9):
  s=Q(sn,sd);a=1/(s+1);low=2-2*a;high=1+a*(s-1)
  assert low==high;n+=1
  for bd in range(1,12):
   for bn in range(2*bd+1,4*bd):
    beta=Q(bn,bd)
    assert ((1-beta+low)>-1)==(s>(beta-2)/(4-beta));n+=1
# Exact endpoint tail integral in units log2 for discrete dyadic distributions.
r=random.Random(9700031)
for case in range(400):
 weights=[Q(r.randrange(0,20),19) for _ in range(12)]
 m=r.randrange(0,12); k=r.randrange(3,20);a=Q(1,k)
 # u dyadic intervals; tail integral du/u = log2 times its constant tail.
 integral=sum(sum(weights[j]*2**j for j in range(h+1,12)) for h in range(m,12))/a
 direct=sum(weights[j]*2**j*max(j-m,0) for j in range(12))/a
 assert integral==direct and 1-2*a>0;n+=1
# Far-endpoint constants and strict truncation compatibility at arbitrary rational R.
for i in range(1,100):
 R=1+Q(i,31);M=8*R;p=Q(i,17)
 intensity=(p/(M/2))*(2*R)**2
 assert intensity/R==8*p*R/M and M-2*R>M/2;n+=1
 # Dyadic sum is finite and exact (pi suppressed).
 total=16*p*R/M
 assert sum(8*p*R/(M*2**j) for j in range(20))==total*(1-Q(1,2**20));n+=1
print(json.dumps({'status':'PASS','independent_exact_assertions':n,'scope':'Exact exponent, discrete-log-tail and dyadic-constant controls; analytic geometry and measurability are reviewed in prose, not computationally certified.'},indent=2))

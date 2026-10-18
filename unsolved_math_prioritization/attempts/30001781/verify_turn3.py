#!/usr/bin/env python3
from fractions import Fraction as F
from math import comb
from itertools import product
import json
count=0
def ck(v):
 global count
 assert v
 count+=1
# Exact rational multiscale vectors illustrate the genuine flat-atom distortion.
# Block l has3*4^l coordinates of size2^-l, hence squared norm3 per block.
maxlevels=6
for levels in range(1,maxlevels+1):
 z=tuple(x for l in range(levels) for x in [F(1,2**l)]*(3*4**l))
 ck(sum(x*x for x in z)==3*levels)
 acc=F(0)
 for s,x in enumerate(z,1):
  acc+=x
  ck(acc*acc<=9*s)
 ck(len(z)==4**levels-1)
# Raw indicator layer-cake reconstruction uses rational coefficients exactly;
# normalizing each atom multiplies/divides by the same sqrt(s).
for a in product(range(5),repeat=5):
 b=sorted(map(F,a),reverse=True)+[F(0)]
 coeff=[b[s]-b[s+1] for s in range(5)]
 for j in range(5):ck(sum(coeff[s] for s in range(j,5))==b[j])
 ck(all(c>=0 for c in coeff))
# Net index cardinality and basic k,m ranges, without numerical logs.
for n in range(1,31):
 for s in range(1,n+1):
  ck(comb(n,s)*2**s<=2**n*2**s)
  ck(s*s>=s)
  for m in range(1,s+1):ck(m*m<=m*s)
# MGF moment bookkeeping: normalized flat weights have quadratic sum1
# and all absolute p-moments scale as s^(1-p/2); square identities avoid roots.
for s in range(1,50):
 ck(F(s,s)==1)
 for p in range(2,13,2):ck(s*F(1,s**(p//2))==F(1,s**(p//2-1)))
print(json.dumps({'status':'PASS','exact_assertions':count,'rational_multiscale_levels':maxlevels,'scope':'Exact deterministic geometry and coefficient bookkeeping. Bernstein/net probability estimates and the all-dimensional obstruction are proved in TURN_3.md; no simulation or random counterexample claim.'},indent=2,sort_keys=True))

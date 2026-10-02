#!/usr/bin/env python3
"""Exact localization-rate and interpolation controls, without stochastic simulation."""
from fractions import Fraction as F
from itertools import product
import json
checks=0

def ok(x):
 global checks
 assert x
 checks+=1
alpha=F(29,64);p=64
for i in range(1,101):
 C1=F(i,7);eta=alpha/(2*(1+C1));ok(C1*eta<=alpha/2);ok(alpha-C1*eta>=alpha/2)
 for R0 in [F(1),F(3),F(17)]:
  prev=None
  for n in range(1,71):
   bound=(R0+eta*(1+n))/4**n
   if prev is not None:ok(bound<=prev/2)
   prev=bound
  ok(F(25*3,16)**2*bound<1)
# Bilinear interpolation is a sup-norm contraction.
for s,t in product([F(i,8) for i in range(9)],repeat=2):
 w=[(1-s)*(1-t),s*(1-t),(1-s)*t,s*t];ok(sum(w)==1);ok(all(x>=0 for x in w))
 for es in [(-2,-1,0,3),(F(1,3),F(-2,7),F(5,9),F(-1,2)),(1,1,1,1)]:
  ok(abs(sum(a*b for a,b in zip(w,es)))<=max(map(abs,es)))
# Normalization of the high-moment event and cutoff agreement threshold.
for R in range(2,31):
 for k in range(R+1):
  exact=F(k,2)
  for sign in [-1,1]:
   err=sign*F(R,2);cutoff=max(F(0),exact+err)
   ok(exact<=F(R,2));ok(cutoff<=R)
# A bounded Lipschitz scalar test demonstrates the deterministic good/bad inequality.
clip=lambda x:max(F(-1),min(F(1),x))
for a,b in product([F(i,7) for i in range(-20,21)],repeat=2):
 ok(abs(clip(a)-clip(b))<=min(F(2),abs(a-b)))
ok(alpha*p/2==F(29,2))
print(json.dumps(dict(status='PASS',assertions=checks,scope='finite rate and interpolation algebra; coupling, exit estimates and path-law conclusions are analytical'),sort_keys=True,indent=2))

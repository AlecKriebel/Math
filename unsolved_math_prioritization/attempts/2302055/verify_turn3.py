#!/usr/bin/env python3
from fractions import Fraction as F
import random,json
rng=random.Random(230205503);checks=0
def ck(x):
 global checks
 assert x
 checks+=1
def clean(p):return {k:v for k,v in p.items()if v}
def add(p,q):
 r=p.copy()
 for k,v in q.items():r[k]=r.get(k,0)+v
 return clean(r)
def mul(p,q):
 r={}
 for i,x in p.items():
  for j,y in q.items():r[i+j]=r.get(i+j,0)+x*y
 return clean(r)
def deriv(p):return clean({k-1:k*v for k,v in p.items()})
def val(p,u):return sum(F(v)*u**k for k,v in p.items())
cases=0
for _ in range(400):
 R=clean({k:rng.randrange(-3,4)for k in range(rng.randrange(-5,1),rng.randrange(1,6))})
 if not R or all(k==0 for k in R):continue
 m=max(0,-min(R));P={k+m:v for k,v in R.items()};Q={m:1};d=max(max(P),m)
 ck(min(P)>=0);ck(d>=1)
 if m:ck(P.get(0,0)!=0)
 C=add(mul(deriv(P),Q),{k:-v for k,v in mul(P,deriv(Q)).items()})
 # R'=(P'Q-PQ')/Q^2 as an exact Laurent identity.
 ck(C==mul(deriv(R),mul(Q,Q)))
 for u in [F(1),F(-1),F(2),F(1,2)]:
  t=val(R,u);B=add(P,{m:-t});ck(val(B,u)==0)
  ck(val(C,u)==val(deriv(R),u)*val(Q,u)**2)
  ck(val(mul({1:1},deriv(R)),u)==u*val(deriv(R),u))
  ck(max(B,default=0)<=d)
 cases+=1
print(json.dumps({'laurent_maps':cases,'exact_assertions':checks,'sample_fibers_per_map':4,'analytic_claims_tested':False},indent=2))

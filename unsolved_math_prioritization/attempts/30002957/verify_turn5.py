#!/usr/bin/env python3
"""Exact finite cover, observable-shield, tail and confidence-interval controls."""
from fractions import Fraction as F
from itertools import product
from math import gcd
import random,json
checks=0;cover_cases=0;ci_cases=0

def ok(x):
 global checks
 assert x
 checks+=1

def norm(v):return sum(x*x for x in v)
rng=random.Random(300029575)
for d in range(1,13):
 m=4*d
 params=[tuple(F(rng.randrange(-20,21),rng.randrange(1,15)) for _ in range(d-1)) for __ in range(83)]
 for t in params:
  tt=norm(t);u=tuple([2*x/(1+tt) for x in t]+[(1-tt)/(1+tt)])
  q=tuple(round(m*x) for x in u);cover_cases+=1
  ok(norm(u)==1);ok(any(q));ok(max(map(abs,q))<=m)
  ok(norm(tuple(F(a,m)-b for a,b in zip(q,u)))<=F(d,4*m*m))
  dot=sum(a*b for a,b in zip(q,u));ok(dot>0);ok(4*dot*dot>=3*norm(q))
# Exact confidence coverage on a rational grid under the stated joint-mean event.
for den in (3,7,11):
 e=F(1,den)
 for bnum in range(1,25):
  b=F(bnum,den)
  for anum in range(bnum+1):
   a=F(anum,den)
   for da,db in product((-e,-e/2,F(0),e/2,e),repeat=2):
    aa=a+da;bb=b+db
    if not 0<=aa<=bb:continue
    ci_cases+=1
    if bb<=e:lo,hi=F(0),F(1)
    else:lo,hi=max(F(0),(aa-e)/(bb+e)),min(F(1),(aa+e)/(bb-e))
    ok(0<=lo<=hi<=1);ok(lo<=a/b<=hi)
# The polynomial portion of the series-tail ratio inequality is universal.
for d in range(1,7):
 for k in range(1,d+1):
  for j in range(5):
   for A in [F(1,100),F(1),F(37,3)]:
    x=A*2**(j*d)
    ok(((1+2**d*x)/(1+x))**(2*k)<=2**(2*k*d))
# A deterministic configuration verifies observable certificates and nonmonotonicity.
scale=10000
P=[(0,0)]+[(scale*i+rng.randrange(-100,101),scale*j+rng.randrange(-100,101)) for i in range(-6,7) for j in range(-6,7) if (i,j)!=(0,0)]
axes=sorted(set((a//gcd(abs(a),abs(b)),b//gcd(abs(a),abs(b))) for a,b in product(range(-8,9),repeat=2) if a or b))

def shielded(L):
 observed=[p for p in P if norm(p)<=L*L*scale*scale]
 queried=[p for p in observed if 16*norm(p)<=L*L*scale*scale]
 for x in queried:
  near=[(z[0]-x[0],z[1]-x[1]) for z in observed if z!=x and 64*norm((z[0]-x[0],z[1]-x[1]))<=L*L*scale*scale]
  for q in axes:
   if not any((w[0]*q[0]+w[1]*q[1])>0 and 4*(w[0]*q[0]+w[1]*q[1])**2>=3*norm(q)*norm(w) for w in near):return False
 return True
states={str(L):shielded(L) for L in [1,2,4,8,16,32]}
ok(states['16']);ok(not states['32']) # success need not persist at the next radius
ok(next(int(L) for L in states if states[L])==16)
print(json.dumps(dict(status='PASS',assertions=checks,rational_cover_cases=cover_cases,confidence_interval_cases=ci_cases,deterministic_shield_states=states,scope='finite exact controls; not stochastic simulation or an evaluated fraction'),sort_keys=True,indent=2))

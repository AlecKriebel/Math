#!/usr/bin/env python3
"""Elementary controls for the cited known lens-space witness; no WRT recomputation."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
from hashlib import sha256
import json
count=0
def check(x):
 global count
 assert x
 count+=1

def saw(x):return F(0) if x.denominator==1 else x-(x.numerator//x.denominator)-F(1,2)
def dedekind(q,p):return sum((saw(F(j,p))*saw(F(q*j,p)) for j in range(1,p)),F(0))

p=25
for q in (4,9):
 check(gcd(p,q)==1)
 for j in range(1,p):
  check((q*j)%p!=0)
  check(saw(F(q*j,p))==F((q*j)%p,p)-F(1,2))
 check(dedekind(q,p)==F(4,25))
 check(12*dedekind(q,p)==F(48,25))
orbit={4%25,(-4)%25,pow(4,-1,25),(-pow(4,-1,25))%25}
check(orbit=={4,21,19,6});check(9 not in orbit)
check(pow(9,-1,25)==14)

def negative_cf(a):
 out=F(a[-1])
 for x in reversed(a[:-1]):out=x-1/out
 return out

def leading_determinants(a):
 prev,now=1,0;out=[]
 for k,x in enumerate(a):
  if k==0:prev,now=1,x
  else:prev,now=now,x*now-prev
  out.append(now)
 return out
for q,chain in ((4,[7,2,2,2]),(9,[3,5,2])):
 check(negative_cf(chain)==F(25,q))
 minors=leading_determinants(chain)
 check(minors[-1]==25)
 check(all(x>0 for x in minors))
check(5-2==3)
D=Path(__file__).resolve().parent
print(json.dumps({'status':'PASS','assertions':count,'dedekind_sums':{'s(4,25)':'4/25','s(9,25)':'4/25'},'dedekind_symbols':'48/25','unoriented_homeomorphism_orbit_of_4_mod_25':sorted(orbit),'quantum_invariant_recomputed':False,'quantum_inequality_source':'Hansen–Takata remark immediately after Ohtsuki Problem7.2, printed p.472','artifact_sha256':sha256((D/'SOURCE_STATUS.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'limitations':'Only elementary finite controls; the full LMO formula and exact quantum separation are credited primary-source statements.'},indent=2,sort_keys=True))

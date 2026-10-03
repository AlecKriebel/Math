#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import random,json
rng=random.Random(300040474)
checks=cases=canonical=0

def verify(k,ts,fam):
 global checks,cases
 n=4*k+1;A=set(range(n));U=set().union(*ts);fam=list(set(map(frozenset,fam)))
 assert len(ts)==k-1 and all(len(t)==4 for t in ts);checks+=1
 assert all(len(s)==3 and not any(s<=t for t in ts) for s in fam);checks+=1
 assert all(len(s|t)<=4 for s,t in combinations(fam,2));checks+=1
 if not fam:
  u=[F(1,4) if i in U else F(1,2) for i in A]
 else:
  I=set.intersection(*map(set,fam))
  if len(I)>=2:
   P=set(sorted(I)[:2]);u=[F(1,4) if i in U|P else F(1,2) for i in A]
  else:
   D=set().union(*fam);assert len(D)==4;checks+=1
   u=[F(1,4) if i in U else F(1,3) if i in D else F(1,2) for i in A]
   if sum(u)<k+1:
    assert len(U)==4*k-4 and not D&U;checks+=1
    ws=A-U-D;assert len(ws)==1;checks+=1;w=next(iter(ws))
    if I:
     assert len(I)==1;checks+=1
     u=[F(1,4) if i in U else F(1) if i==w else F(0) if i in I else F(1,2) for i in A]
    else:u=[F(1,4) if i in U else F(1) if i==w else F(1,3) for i in A]
 assert sum(u)>=k+1;checks+=1
 used=list(ts)+fam+[frozenset([i]) for i in A]
 for t in ts:used += [frozenset(s) for s in combinations(t,3)]
 for s in combinations(A,2):
  ss=frozenset(s)
  if any(ss<=t for t in ts) or all(len(ss|f)<=4 for f in fam):used.append(ss)
 for s in used:assert sum(u[i] for i in s)<=1;checks+=1
 cases+=1
# All canonical pair-star and four-set families for n=9, relative to one T.
T=set(range(4));O=set(range(4,9))
for p in range(3):
 P=set(sorted(T)[:p]+sorted(O)[:2-p]);it=sorted(T-P);io=sorted(O-P)
 for a in range(len(it)+1):
  for b in range(len(io)+1):
   if a+b<2 or (p==2 and a):continue
   verify(2,[T],[P|{v} for v in it[:a]+io[:b]]);canonical+=1
for d in range(4):
 D=set(sorted(T)[:d]+sorted(O)[:4-d]);it=sorted(D&T);io=sorted(D-T)
 for a in range(len(it)+1):
  for b in range(len(io)+1):
   if a+b<2:continue
   fs=[D-{v} for v in it[:a]+io[:b]]
   if any(s<=T for s in fs):continue
   verify(2,[T],fs);canonical+=1
assert canonical==54;checks+=1
# Deterministic higher-k configurations, allowing overlapping maximal sets.
for k in range(2,13):
 n=4*k+1;A=set(range(n))
 for repeat in range(40):
  if repeat%2:ts=[set(range(4*i,4*i+4)) for i in range(k-1)]
  else:
   ts=[]
   while len(ts)<k-1:
    t=set(rng.sample(range(n),4))
    if t not in ts:ts.append(t)
  P=set(rng.sample(range(n),2))
  L=rng.sample(sorted(A-P),rng.randrange(0,min(10,n-2)+1))
  fs=[P|{v} for v in L if not any(P|{v}<=t for t in ts)]
  verify(k,ts,fs)
  D=set(rng.sample(range(n),4));fs=[D-{v} for v in D if rng.randrange(2) and not any(D-{v}<=t for t in ts)]
  verify(k,ts,fs)
# Scalar inequalities controlling all k in the proof.
for k in range(2,501):
 assert F(4*k+1,2)-F(4*k-2,4)==k+1;checks+=1
 assert F(4*k+1,2)-F(4*k-5,4)-F(4,6)==k+F(13,12)>k+1;checks+=1
 assert F(4*k+1,2)-F(4*k-4,4)-F(3,6)==k+1;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'canonical_nine_vertex_cases':canonical,'all_charge_configurations':cases,'scope':'Exact finite controls for the universal pairwise-union classification and explicit charges; no unrestricted source solution.'},indent=2))

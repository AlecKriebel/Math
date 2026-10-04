#!/usr/bin/env python3
from itertools import combinations,combinations_with_replacement
from fractions import Fraction as F
from math import comb
import json
checks=records=compositions=0
for m in range(8):
 for h in combinations_with_replacement(range(-1,m+1),m+1):
  good=all(h[j]>=j for j in range(m+1));patterns=[]
  for k in range(m+1):
   for interior in combinations(range(1,m+1),k):
    seq=(0,)+interior+(m+1,)
    ok=all(h[seq[i]]==seq[i+1]-1 for i in range(k)) and h[seq[k]]>=m
    if ok:patterns.append(seq)
  assert bool(patterns)==good;checks+=1
  assert len(patterns)<=1;checks+=1
  if good:
   records+=1;a=0;seq=[0]
   while h[a]<m:
    b=h[a]+1;assert a<b<=m;checks+=1;seq.append(b);a=b
   seq.append(m+1);assert tuple(seq)==patterns[0];checks+=1
   for i in range(1,len(seq)-1):
    assert seq[i+1]-1>=seq[i];checks+=1
for m in range(11):
 for g in range(2,7):
  q=F(1,2**g)
  for a in [F(1,8),F(1,2),F(1),F(3,2),F(4)]:
   lhs=F(0)
   for k in range(m+1):
    c=0
    for interior in combinations(range(1,m+1),k):
     seq=(0,)+interior+(m+1,);term=F(1)
     for i in range(k+1):term*=q**(seq[i+1]-seq[i])*a
     assert term==q**(m+1)*a**(k+1);checks+=1;compositions+=1;lhs+=term;c+=1
    assert c==comb(m,k);checks+=1
   assert lhs==q**(m+1)*a*(1+a)**m;checks+=1
   assert lhs<=(q*(1+a))**(m+1);checks+=1
for d in range(2,6):
 for G in range(2*d+1,2*d+17):
  gamma=F(G,2)
  assert gamma>d;checks+=1
  exp=(gamma-1)/(gamma-d)
  assert exp*(d-gamma)+(gamma-1)==0;checks+=1
  assert exp/(gamma-1)==1/(gamma-d);checks+=1
  for kn in range(1,int(4*(gamma-1))):
   kappa=F(kn,4)
   for n in range(15):
    m=int(F(n+1)/kappa)
    assert kappa*(m+1)>n+1;checks+=1
    q=kappa/F(2)
    assert q/kappa-1<0;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'record_profiles':records,'composition_terms':compositions,'record_depths':list(range(8)),'scope':'Finite record-event partition, exact composition sums and moment exponents; no geometric SIRSN simulation or unrestricted proof.'},indent=2,sort_keys=True))

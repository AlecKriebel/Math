#!/usr/bin/env python3
from itertools import combinations
from fractions import Fraction as F
import json
checks=blocks=stability=0
# Exact integer block-count inequalities.
for k in range(2,151):
 for m in range(k+2,k+102):
  assert F(k,m)+F(1,k)<=1;checks+=1;blocks+=1
# Pair-block argument on all positive integer block weights in this range.
def comps(total,n,prefix=()):
 if n==1:
  if total>0:yield prefix+(total,)
 else:
  for a in range(1,total-n+2):yield from comps(total-a,n-1,prefix+(a,))
for k in range(2,7):
 for den in range(k+1,19):
  for aa in comps(den,k+1):
   if all(k*a<den for a in aa):
    for i,j in combinations(range(k+1),2):
     assert k*(aa[i]+aa[j])>den;checks+=1
# Algebraic equivalence of the two deletion bounds, with strictness preserved.
for den in range(2,21):
 for a in range(1,den+1):
  x=F(a,den)
  for b in range(1,den+1):
   y=F(b,den)
   for e in range(a):
    eps=F(e,den);xx=(x-eps)/(1-eps)
    for k in range(2,8):
     assert (xx+k*y>1)==(eps<(x+k*y-1)/(k*y));checks+=1
     assert (k*xx+y>=1)==(eps<=(k*x+y-1)/(k+y-1));checks+=1;stability+=1
# Full ordinary graph and the exact local uncrossing failure.
A=list(map(frozenset,combinations(range(11),9)))
B=list(map(frozenset,combinations(range(11),4)))
b1=frozenset(range(4));b2=frozenset(range(4,8))
S1={i for i,a in enumerate(A) if b1<=a};S2={i for i,a in enumerate(A) if b2<=a}
assert (len(S1),len(S2),len(S1&S2),len(S1|S2))==(21,21,3,39);checks+=1
for i in range(55):
 assert int(i in S1)+int(i in S2)==int(i in S1|S2)+int(i in S1&S2);checks+=1
for c in range(11):
 old={i for i,a in enumerate(A) if c in a}
 remaining={i for i,a in enumerate(A) if any(c in b and b<=a for b in B if b not in [b1,b2])}
 assert remaining==old and len(old)==45;checks+=1
 expected=51 if c in b1|b2 else 55
 assert len(remaining|S1|S2)==expected>45;checks+=1
assert F(4,11)*3>1;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'block_count_controls':blocks,'deletion_equivalence_controls':stability,'uncrossing_graph_part_sizes':[55,330,11],'scope':'Exact finite endpoint and local-operation controls; structural theorem proved in TURN_5.md, original unresolved.'},indent=2))

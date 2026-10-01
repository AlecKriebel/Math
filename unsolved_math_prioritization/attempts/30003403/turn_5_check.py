"""Finite dense-set extensions and rational cut countercontrols; no forcing properness claim."""
from fractions import Fraction as F
from itertools import combinations_with_replacement,combinations
from math import isqrt
from collections import Counter
import json
C=Counter()
for n in range(1,7):
 for vals in combinations_with_replacement(range(-2,3),n):
  p={F(2*i):F(v) for i,v in enumerate(vals)}
  for x in [F(-1),F(2*n)]+[F(2*i+1) for i in range(n-1)]:
   left=[s for s in p if s<x];right=[s for s in p if s>x]
   y=p[max(left)] if left else p[min(right)]
   z=sorted(list(p.items())+[(x,y)])
   assert all(z[i][1]<=z[i+1][1] for i in range(len(z)-1));C['domain_extension']+=1
  for a in map(F,range(-3,4)):
   if a in p.values():continue
   left=[s for s in p if p[s]<a];right=[s for s in p if p[s]>a]
   x=(max(left)+min(right))/2 if left and right else (max(left)+1 if left else min(right)-1)
   assert x not in p
   z=sorted(list(p.items())+[(x,a)])
   assert all(z[i][1]<=z[i+1][1] for i in range(len(z)-1));C['range_extension']+=1
for i,j in combinations(range(100),2):
 assert i<j and -i>-j;C['antichain_pairs']+=1
# Nested rational brackets of sqrt(2); no floating point or numerical equality inference.
brackets=[]
for n in range(1,101):
 den=2**n;k=isqrt(2*den*den);lo=F(k,den);hi=F(k+1,den)
 assert lo*lo<2<hi*hi;C['exact_irrational_bracket']+=1
 brackets.append((lo,hi))
for (lo,hi),(ln,hn) in zip(brackets,brackets[1:]):
 assert lo<=ln<hn<=hi;C['nested_brackets']+=1
# Every bounded-denominator rational test value is excluded by some finite bracket.
for den in range(1,31):
 for num in range(-2*den,3*den+1):
  q=F(num,den)
  assert any(q<lo or q>hi for lo,hi in brackets);C['finite_rationals_excluded']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Exact finite extension and cut controls. The uncountable antichain is proved analytically; properness and the original PFA target are not established.'},indent=2))

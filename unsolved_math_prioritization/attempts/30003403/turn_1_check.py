"""Finite combinatorial controls for the finite-support gap argument.

These do not certify PFA or an uncountable normality theorem; see TURN_1.md.
"""
from itertools import product
from collections import Counter
import json
C=Counter();D=range(-2,3);small=range(-1,2)
for n in range(1,5):
 for x in product(D,repeat=n):
  if all(v in small for v in x):continue
  j=next(i for i,v in enumerate(x) if v not in small)
  xm=x+(-1,);xx=x+(0,);xp=x+(1,)
  assert xm<xx<xp;C['tail_points_on_both_sides']+=1
  # All small-alphabet words at the larger common padded length.
  for z in product(small,repeat=n+1):
   assert (z<xm)==(z<xx)==(z<xp);C['same_cut_against_small_alphabet']+=1
for n in range(1,4):
 W=list(product(D,repeat=n))
 for i,x in enumerate(W):
  for y in W[i+1:]:
   for c in [1,2]:
    assert x+(0,)<x+(c,)<y+(0,);C['interval_tail_insertions']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Finite-prefix comparison controls only. The uncountable structural theorem and the stationarity conclusion are proved analytically in TURN_1.md.'},indent=2))

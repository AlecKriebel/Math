"""Finite verification of the explicitly defined floor/ceiling retraction."""
from itertools import combinations,product
from collections import Counter
import json
C=Counter()
for n in range(1,11):
 A=list(range(n))
 for mask in range(1,1<<n):
  B=[x for x in A if mask>>x&1]
  def retraction(x):
   if x in B:return x
   left=[b for b in B if b<x]
   return max(left) if left else min(b for b in B if b>x)
  vals=[retraction(x) for x in A]
  assert all(vals[i]<=vals[i+1] for i in range(n-1));C['monotone']+=1
  assert set(vals)==set(B);C['onto']+=1
  assert all(retraction(b)==b for b in B);C['fixes_target']+=1
# Prefix insertion/removal preserves lexicographic order on finite padded inputs.
for n in range(1,5):
 W=list(product([-1,0,1],repeat=n))
 for i,x in enumerate(W):
  for y in W[i+1:]:assert (0,)+x < (0,)+y;C['prefix_order_embedding']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Finite retraction/prefix diagnostics. The infinite cut criterion and cylinder nonretraction are analytical arguments in TURN_2.md, not inferred from these tests.'},indent=2))

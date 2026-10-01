"""Exact finite quotient-gluing controls and explicit coordinate-projection countercontrols."""
from itertools import product,combinations
from collections import Counter
import json
C=Counter()
# For finite fibers use rank-clamping, not second-coordinate projection.
for dsize in range(2,7):
 for lsize in range(1,6):
  for isize in range(1,dsize+1):
   for cuts in combinations(range(1,dsize),isize-1):
    ends=(0,)+cuts+(dsize,)
    for sizes in product(range(1,min(lsize,3)+1),repeat=isize):
     out=[]
     for i in range(isize):
      domain=[(d,l) for d in range(ends[i],ends[i+1]) for l in range(lsize)]
      # Onto L by clipping the domain's full lexicographic rank, then onto A_i.
      vals=[(i,min(min(k,lsize-1),sizes[i]-1)) for k,_ in enumerate(domain)]
      assert all(vals[k]<=vals[k+1] for k in range(len(vals)-1));C['fiber_monotone']+=1
      assert {v[1] for v in vals}==set(range(sizes[i]));C['fiber_onto']+=1
      out+=vals
     assert all(out[k]<=out[k+1] for k in range(len(out)-1));C['glued_monotone']+=1
     assert set(out)=={(i,a) for i,size in enumerate(sizes) for a in range(size)};C['glued_onto']+=1
# The naive product projection is not monotone.
x=((0,),(1,));y=((1,),(0,))
assert x<y and x[1]>y[1];C['projection_reversal']+=1
# Interleaving is not lex-product order-preserving.
x=((0,-1),(1,0));y=((0,1),(-1,0))
interleave=lambda t:tuple(z for ab in zip(*t) for z in ab)
assert x<y and interleave(x)>interleave(y);C['interleaving_reversal']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Finite gluing controls and two false-formula countercontrols. Infinite short-product and normal-Countryman inputs are credited theorems, not inferred from enumeration.'},indent=2))

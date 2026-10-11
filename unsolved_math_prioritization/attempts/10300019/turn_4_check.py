"""Finite corner-return and face-pairing controls, not a compact-atlas existence proof."""
from itertools import permutations,product
from collections import Counter
import json
C=Counter()
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):return tuple(p.index(i) for i in range(len(p)))
for n in range(1,6):
 identity=tuple(range(n));P=list(permutations(range(n)))
 for p in P:
  ck=comp(inv(p),p);assert ck==identity;C['face_inverse']+=1
  for q in P:
   # Completing the third return map by the inverse gives identity on every label.
   r=inv(comp(q,p));assert comp(r,comp(q,p))==identity;C['closed_corner_return']+=1
   if comp(q,p)!=identity:
    assert any(comp(q,p)[i]!=i for i in range(n));C['nontrivial_return_detected']+=1
 # Same finite cardinality does not imply a compatible ordered matching.
 for p in P:
  order_ok=all(p[i]<p[i+1] for i in range(n-1))
  assert order_ok==(p==identity);C['order_not_cardinality']+=1
# Two colors may be reconnected without preserving global labels.
for n in range(1,30):
 left=[(0,i) for i in range(n)]+[(1,i) for i in range(n)]
 right=[(1,i) for i in range(n)]+[(0,i) for i in range(n)]
 pairing=dict(zip(left,right));assert len(pairing)==2*n and len(set(pairing.values()))==2*n;C['reconnection_bijection']+=1
 assert all(a[0]!=b[0] for a,b in pairing.items());C['colors_can_change']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Finite face/corner algebra only. Compactness, embedded normal disk packages and local product charts are explicit hypotheses of TURN_4.md, not consequences of these tests.'},indent=2))

"""Exhaust all 6^4 assignments of four generators to S3 for each central quotient."""
from itertools import permutations,product
from collections import Counter
from pathlib import Path
import json
from cover_homology import relators
I=(0,1,2);perms=list(permutations(range(3)))
def mul(p,q):return tuple(p[q[i]] for i in range(3))
def inv(p):return tuple(p.index(i) for i in range(3))
def word_value(w,t):
 z=I
 for x in w:z=mul(z,t[x-1] if x>0 else inv(t[-x-1]))
 return z

def generated(t):
 seen={I};todo=[I]
 for a in todo:
  for b in t:
   z=mul(a,b)
   if z not in seen:seen.add(z);todo.append(z)
 return seen
out={}
for name,l,k in [('F4',{(0,1):3,(1,2):4,(2,3):3},6),('H4',{(0,1):5,(1,2):3,(2,3):3},15)]:
 hist=Counter();witness=None
 for t in product(perms,repeat=4):
  if all(word_value(w,t)==I for w in relators(l,k)):
   size=len(generated(t));hist[size]+=1
   if size==6 and witness is None:witness=t
 out[name]={'assignments_tested':6**4,'image_order_counts':dict(sorted(hist.items())),'surjection_witness':witness}
assert out['H4']['image_order_counts'].get(6,0)==0
assert out['F4']['image_order_counts'].get(6,0)>0
print(json.dumps(out,indent=2));Path(__file__).with_name('small_quotients_results.json').write_text(json.dumps(out,indent=2)+'\n')

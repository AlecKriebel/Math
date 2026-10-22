#!/usr/bin/env python3
"""Exact structure of SL(2,3), a test case for the remaining extension gap."""
import itertools,json
from pathlib import Path
p=3;e=(1,0,0,1)
def mul(a,b):return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%p for i in range(2) for j in range(2))
G={a for a in itertools.product(range(p),repeat=4) if (a[0]*a[3]-a[1]*a[2])%p==1}
inv={a:next(b for b in G if mul(a,b)==e) for a in G}
def closure(xs):
 seen={e};todo=[e]
 while todo:
  a=todo.pop()
  for b in xs:
   c=mul(a,b)
   if c not in seen:seen.add(c);todo.append(c)
 return frozenset(seen)
Z={a for a in G if all(mul(a,b)==mul(b,a) for b in G)}
orders={a:len(closure([a])) for a in G}
subs={frozenset([e])};todo=list(subs)
while todo:
 H=todo.pop()
 for a in G-H:
  K=closure(list(H)+[a])
  if K not in subs:subs.add(K);todo.append(K)
normals=[H for H in subs if all(mul(mul(a,h),inv[a]) in H for a in G for h in H)]
nontriv=[H for H in normals if len(H)>1]
monolith=set.intersection(*map(set,nontriv))
assert len(G)==24 and len(Z)==2 and monolith==Z
assert sum(o==2 for o in orders.values())==1
assert not any(len(H)==12 and set(H)&Z=={e} for H in subs)
# Unique normal order-8 subgroup is Q8; quotient by center is V4, and it is
# the unique minimal nontrivial normal subgroup of G/Z.
Q8=next(H for H in normals if len(H)==8)
assert sorted(orders[x] for x in Q8)==[1,2,4,4,4,4,4,4]
assert all(len(H)>=8 for H in normals if not set(H)<=Z)
C={g for g in G if all(mul(mul(g,a),inv[g]) in {mul(a,z) for z in Z} for a in Q8)}
assert C==set(Q8)
out=dict(group='SL(2,3)',order=len(G),subgroup_count=len(subs),normal_subgroup_orders=sorted(map(len,normals)),center_order=len(Z),monolith_order=len(monolith),unique_involution=True,central_extension_has_complement=False,quotient_by_center_order=12,quotient_abelian_monolith_order=4,quotient_action_image_order=len(G)//len(C),bound_interval=[3,9],status='PASS',scope='The [3,9] asymptotic interval is supplied by the written bounds, not by finite enumeration. No counterexample is claimed.')
print(json.dumps(out,indent=2));Path(__file__).with_name('nonsplit_candidate_results.json').write_text(json.dumps(out,indent=2)+'\n')

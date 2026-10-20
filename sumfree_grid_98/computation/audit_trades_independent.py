"""Audit local exchange stability via every grid edge, not per-point blocker formulas."""
import json,itertools
from search_boundary_trades import search
results=[]
for d,n in [(2,8),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(4,4),(4,5),(5,4),(6,3)]:
 r=search(d,n);t=r['t'];P=set(itertools.product(range(1,n+1),repeat=d))
 B={x for x in P if t<=sum(x)<2*t or (max(x)==n and sum(x)<t) or (min(x)==1 and sum(x)>=2*t)}
 common={w:set(B) for w in P-B};counts={w:0 for w in P-B}
 for z in P:
  for x in itertools.product(*(range(1,a) for a in z)):
   y=tuple(a-b for a,b in zip(z,x));e={x,y,z};missing=e-B
   if not missing:raise ValueError('base is not sumfree')
   if len(missing)==1:
    w=next(iter(missing));common[w]&=e&B;counts[w]+=1
 if any(common.values()) or min(counts.values())==0:raise ValueError('local exchange found')
 results.append(dict(d=d,n=n,t=t,base=len(B),omitted_points=len(common),all_blocker_intersections_empty=True))
print(json.dumps(results,indent=2))

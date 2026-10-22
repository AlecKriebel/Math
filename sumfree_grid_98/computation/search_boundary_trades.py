"""Exact search for one-deletion/two-addition improvements of best B_t."""
from itertools import product
import json
from boundary_completion import best

def search(d,n):
 t=best(d,n)['t'];P=set(product(range(1,n+1),repeat=d));B={x for x in P if t<=sum(x)<2*t or (max(x)==n and sum(x)<t) or (min(x)==1 and sum(x)>=2*t)}
 outside=P-B;by={}
 for w in outside:
  blockers=[]
  # Every forbidden triple involving w and otherwise current B.
  twice=tuple(2*x for x in w)
  if twice in B:blockers.append({twice})
  for x in B:
   z=tuple(a+b for a,b in zip(w,x))
   if z in B:blockers.append({x,z})
  for x in product(*(range(1,a) for a in w)):
   y=tuple(a-b for a,b in zip(w,x))
   if x in B and y in B:blockers.append({x,y})
  if not blockers:
   raise ValueError('B was not inclusion maximal in tested central case')
  eligible=set.intersection(*blockers)
  for v in eligible:by.setdefault(v,[]).append(w)
 pairs=0
 for v,ws in by.items():
  for i,a in enumerate(ws):
   for b in ws[i+1:]:
    pairs+=1;R=B-{v}
    ab=tuple(x+y for x,y in zip(a,b));am=tuple(x-y for x,y in zip(a,b));bm=tuple(y-x for x,y in zip(a,b))
    if ab in R or am in R or bm in R:continue
    if tuple(2*x for x in a)==b or tuple(2*x for x in b)==a:continue
    C=R|{a,b}
    if any(tuple(x+y for x,y in zip(u,vv)) in C for u in C for vv in C):raise ValueError('Invalid witness')
    return {'d':d,'n':n,'t':t,'base':len(B),'found':True,'remove':v,'add':[a,b]}
 return {'d':d,'n':n,'t':t,'base':len(B),'found':False,'candidate_pairs_checked':pairs,'eligible_removals':len(by)}
if __name__=='__main__':
 for d,n in [(2,8),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(4,4),(4,5),(5,4),(6,3)]:
  print(json.dumps(search(d,n)),flush=True)

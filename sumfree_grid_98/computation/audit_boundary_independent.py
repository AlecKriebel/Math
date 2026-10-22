import itertools,json
from isolated_completion import calculate

def need(c,m):
 if not c:raise ValueError(m)
results=[]
for d in range(1,5):
 for n in range(2,7):
  P=list(itertools.product(range(1,n+1),repeat=d));edges=set()
  for z in P:
   for x in itertools.product(*(range(1,a) for a in z)):
    y=tuple(a-b for a,b in zip(z,x));edges.add(frozenset((x,y,z)))
  covered=set().union(*edges) if edges else set()
  iso={x for x in P if min(x)==1 and max(x)==n}
  need(set(P)-covered==iso,'isolated classification')
  calc=calculate(d,n)
  iso_best=max(len({x for x in P if t<=sum(x)<2*t}|iso) for t in range(1,d*n+1))
  need(iso_best==calc['completed_best']['completed'],'isolated formula')
  tested=[]
  for t in range(1,d*n+1):
   B={x for x in P if t<=sum(x)<2*t or (max(x)==n and sum(x)<t) or (min(x)==1 and sum(x)>=2*t)}
   need(not any(e<=B for e in edges),'boundary not sum-free')
   if d<=t and 2*t<=d*n+1 and d*n<=4*t-2:
    blocked={next(iter(e-B)) for e in edges if len(e-B)==1}
    need(set(P)-B<=blocked,'boundary not maximal')
    tested.append(t)
  results.append({'d':d,'n':n,'all_thresholds_sumfree':True,'maximality_thresholds':tested})
print(json.dumps(results,indent=2))

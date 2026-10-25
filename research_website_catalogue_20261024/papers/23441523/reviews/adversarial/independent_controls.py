"""Fresh exact finite checks; no imports from supplied verification or audit files."""
from itertools import combinations,product
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import random,json
rng=random.Random(23441523);counts=Counter()
def pairs(n):return list(combinations(range(n),2))
def edges(n,m):return {e for j,e in enumerate(pairs(n)) if m>>j&1}
def mask(n,E):return sum(1<<j for j,e in enumerate(pairs(n)) if e in E)
def colorable(n,E,k=3,omit=None):
 order=sorted((v for v in range(n) if v!=omit),key=lambda v:-sum(v in e for e in E));assignment={}
 def go(i):
  if i==len(order):return True
  v=order[i];bad={assignment[w] for w in assignment if tuple(sorted((v,w))) in E}
  for c in range(k):
   if c not in bad:
    assignment[v]=c
    if go(i+1):return True
  assignment.pop(v,None);return False
 return go(0)
def prop(n,E):
 if any(all(e in E for e in combinations(s,2)) for s in combinations(range(n),4)):return False
 return colorable(n,E) or any(colorable(n,E,omit=v) for v in range(n))
def triangle_sets(n,E):return [frozenset(combinations(s,2)) for s in combinations(range(n),3) if all(e in E for e in combinations(s,2))]
def tau(n,E):
 T=triangle_sets(n,E);hits={e:sum(1<<j for j,t in enumerate(T) if e in t) for e in E}
 @lru_cache(None)
 def solve(left):
  if not left:return 0
  j=(left&-left).bit_length()-1
  return 1+min(solve(left&~hits[e]) for e in T[j])
 return solve((1<<len(T))-1)
# Enumerate every possible repaired graph, allowing additions and deletions.
valid={}
for n in range(2,7):
 valid[n]=[m for m in range(1<<len(pairs(n))) if prop(n,edges(n,m))]
 counts['all_candidate_repairs_classified']+=1<<len(pairs(n))
for n in range(1,6):
 source=list(range(1<<len(pairs(n))))
 if n==5:source=rng.sample(source,48)
 for m in source:
  E=edges(n,m)
  if not colorable(n,E):continue
  J=E|{(v,n) for v in range(n)};jm=mask(n+1,J);tailmask=mask(n+1,set(pairs(n)));allmask=(1<<len(pairs(n+1)))-1;apexmask=allmask^tailmask
  best=min(((jm^f)&tailmask).bit_count()+n*((jm^f)&apexmask).bit_count() for f in valid[n+1])
  assert best==tau(n,E)
  counts['arbitrary_edit_heavy_apex_minima']+=1
# Exact cover deletion minima on all source graphs through four vertices.
for n in range(1,5):
 for m in range(1<<len(pairs(n))):
  E=edges(n,m);LE={tuple(sorted((i*n+u,j*n+v))) for i,j in combinations(range(3),2) for u in range(n) for v in range(n) if tuple(sorted((u,v))) in E}
  a=tau(n,E);b=tau(3*n,LE)
  assert b>=a and (a==0)==(b==0)
  assert colorable(3*n,LE)
  counts['exact_cover_minima']+=1
# Proper partial-coloring repair and list-potential inequalities.
examples=[(n,edges(n,m)) for n in range(1,5) for m in range(1<<len(pairs(n)))]
examples += [(6,edges(6,rng.randrange(1<<15))) for _ in range(50)]
for n,E in examples:
 assignments=product(range(4),repeat=n) if n<=4 else (tuple(rng.randrange(4) for _ in range(n)) for _ in range(80))
 for col in assignments:
  S={v for v,c in enumerate(col) if c}
  if any(col[u] and col[u]==col[v] for u,v in E):continue
  L={v:set(range(1,4))-{col[u] for u in S if tuple(sorted((u,v))) in E} for v in range(n) if v not in S};U={v for v in L if not L[v]};V=set(L)-U
  costs={v:{i:sum(tuple(sorted((u,v))) in E and i in L[u] for u in V) for i in L[v]} for v in V}
  delta={v:min(costs[v].values()) for v in V};full=list(col)
  for v in V:full[v]=min(costs[v],key=costs[v].get)
  for v in U:full[v]=1
  changed=sum(full[u]==full[v] for u,v in E);assert changed<=n*len(U)+sum(delta.values())
  for v in V:
   for i in L[v]:
    old=sum(map(len,L.values()));new=sum(len(L[u]-({i} if tuple(sorted((u,v))) in E else set())) for u in L if u!=v)
    assert old-new>=delta[v]
    counts['list_potential_decreases']+=1
  counts['partial_coloring_repairs']+=1
# Boundaries: hereditary/isolate closure are different from independent blowup closure.
C5={tuple(sorted((i,(i+1)%5))) for i in range(5)};wheel=C5|{(i,5) for i in range(5)}
assert prop(6,wheel) and not colorable(6,wheel)
blow={tuple(sorted((2*u+i,2*v+j))) for u,v in wheel for i,j in product(range(2),repeat=2)}
assert not prop(12,blow)
counts['blowup_nonclosure_witness']=1
for inside in range(64):
 E=blow|{(2*v,2*v+1) for v in range(6) if inside>>v&1}
 assert not prop(12,E)
 counts['all_internal_choices_of_wheel_blowup_rejected']+=1
# Without the 3-colorable-tail hypothesis, the heavy-apex identity is false.
myc=C5|{tuple(sorted((i,j+5))) for i,j in C5}|{tuple(sorted((j,i+5))) for i,j in C5}|{(i+5,10) for i in range(5)}
assert tau(11,myc)==0 and not colorable(11,myc)
J=myc|{(i,11) for i in range(11)};assert not prop(12,J)
counts['missing_3color_hypothesis_rejected']=1
# A light apex does not satisfy the stated exact factor: K4 can lose an apex edge.
assert F(1,100)*F(33,100)<F(33,100)**2
assert prop(4,set(pairs(4))-{(0,3)})
counts['light_apex_identity_rejected']=1
# Strict positivity/rationality and exact adjacency simulation on all small sources.
for n in range(1,5):
 for m in range(1<<len(pairs(n))):
  E=edges(n,m);labels=[None]+[(i,v) for i in range(3) for v in range(n)];D={x:F(1,2) if x is None else F(1,6*n) for x in labels};assert sum(D.values())==1 and all(x>0 for x in D.values())
  for x,y in product(labels,repeat=2):
   calls=0
   if x==y:a=False
   elif x is None or y is None:a=True
   elif x[0]==y[0] or x[1]==y[1]:a=False
   else:a=tuple(sorted((x[1],y[1]))) in E;calls=1
   expected=x!=y and (x is None or y is None or (x[0]!=y[0] and tuple(sorted((x[1],y[1]))) in E))
   assert a==expected and calls<=1;counts['oracle_endpoint_cases']+=1
  counts['positive_rational_distributions']+=1
out={'status':'PASS','seed':23441523,'counts':dict(counts),'scope':'Finite exhaustive arbitrary-edit minima for every 3-colorable tail through n=4 and 48 seeded n=5 candidates; exact triangle deletion cover minima through n=4; list-potential identities; oracle endpoint cases; explicit out-of-scope negative controls. No published code imported. Not an asymptotic lower-bound proof.'}
base=Path(__file__).parent;(base/'independent-controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

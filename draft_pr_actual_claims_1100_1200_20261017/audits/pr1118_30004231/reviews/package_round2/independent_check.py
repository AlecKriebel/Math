"""Fresh integer normal-grid census and finite-field/tree topology checks.
No imports from the distributed verification programs or earlier reviews.
"""
from itertools import product,combinations,permutations
from fractions import Fraction
from collections import Counter,deque
import json,pathlib,datetime
HERE=pathlib.Path(__file__).resolve().parent
N=0
def check(ok,msg):
 global N;N+=1
 if not ok:raise RuntimeError(msg)
def rank(rows,p=None):
 m=[[Fraction(x) for x in r] for r in rows] if p is None else [[x%p for x in r] for r in rows]
 if not m:return 0
 k=0
 for j in range(len(m[0])):
  pivot=next((i for i in range(k,len(m)) if m[i][j]),None)
  if pivot is None:continue
  m[k],m[pivot]=m[pivot],m[k];d=m[k][j]
  m[k]=[x/d for x in m[k]] if p is None else [x*pow(d,-1,p)%p for x in m[k]]
  for i in range(k+1,len(m)):
   t=m[i][j]
   m[i]=[x-t*y for x,y in zip(m[i],m[k])] if p is None else [(x-t*y)%p for x,y in zip(m[i],m[k])]
  k+=1
  if k==len(m):break
 return k
def dim(v):
 v=list(v);return rank([[x-y for x,y in zip(a,v[0])] for a in v[1:]])
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def exposed(verts,u):
 val=max(dot(u,v) for v in verts);return frozenset(v for v in verts if dot(u,v)==val)
def plus(a,b):return frozenset(tuple(x+y for x,y in zip(v,w)) for v in a for w in b)
def census(d,interval=True):
 base=[(0,)*d]+[tuple(int(i==j) for i in range(d)) for j in range(d)]
 if interval:
  p=frozenset(v+(t,) for v in base for t in (0,1));q=frozenset(tuple(-x for x in v)+(t,) for v in base for t in (0,1))
  normals=(u+(t,) for u in product(range(-2,3),repeat=d) for t in (-1,0,1))
 else:
  p=frozenset(base);q=frozenset(tuple(-x for x in v) for v in base);normals=product(range(-2,3),repeat=d)
 faces={}
 for u in normals:
  a,b=exposed(p,u),exposed(q,u);s=plus(a,b)
  if s in faces:check(faces[s]==(a,b),'unique canonical decomposition')
  else:faces[s]=(a,b)
 # '+' includes nonvertex points. Exposed-face coordinate sets can contain zero
 # only for the whole sum; inclusion remains exact because we use all generators.
 allsum=plus(p,q)
 qual=[];broad=[];vertical=0
 for s,(a,b) in faces.items():
  ds,da,db=dim(s),dim(a),dim(b)
  if da>0 and db>0 and ds==da+db:qual.append(s)
  if da>0 and db>0 and ds>=2:broad.append(s)
  if interval and len({v[-1] for v in s})==3:
   vertical+=1;check(ds<da+db,'vertical additivity exclusion')
 check(allsum in faces,'whole present');check(allsum not in qual,'whole rejected')
 def graph(vs):
  vs=list(vs);es=[(i,j) for i,a in enumerate(vs) for j,b in enumerate(vs) if a<b]
  # Every triple chain would have a vertex with both an incoming and outgoing edge.
  check(not(set(a for a,b in es)&set(b for a,b in es)),'no three-chain')
  adj=[set() for _ in vs]
  for a,b in es:adj[a].add(b);adj[b].add(a)
  remaining=set(range(len(vs)));comps=[];treeedges=[]
  while remaining:
   root=min(remaining);remaining.remove(root);queue=[root];c={root}
   for a in queue:
    for b in sorted(adj[a]):
     if b in remaining:remaining.remove(b);queue.append(b);c.add(b);treeedges.append((a,b))
   comps.append(c)
  matrix=[[int(i==b)-int(i==a) for a,b in es] for i in range(len(vs))]
  rs={str(p):rank(matrix,p) for p in (2,3,5,7,101)};rq=rank(matrix)
  check(all(x==len(vs)-len(comps) for x in rs.values()),'field independent rank')
  check(rq==len(treeedges)==len(vs)-len(comps),'rational/spanning forest rank')
  check(all(adj),'pure graph')
  # An incidence matrix forest minor has determinant +/-1 by successively
  # deleting a leaf row and its only forest edge. This proves integral
  # H0 is free, and H1 is free as a subgroup of free C1; no torsion hidden.
  for c in comps:
   check(sum(len(adj[i]) for i in c)//2-len(c)+1>=0,'cycle rank')
  return {'vertices':len(vs),'edges':len(es),'components':len(comps),'component_sizes':sorted(map(len,comps)),'boundary_rank_Q':rq,'boundary_ranks_Fp':rs,'integral_H0_rank':len(comps),'integral_H1_rank':len(es)-rq,'degrees':dict(sorted(Counter(map(len,adj)).items()))}
 g=graph(qual) if d>=4 else {'vertices':len(qual),'comparisons':sum(a<b for a in qual for b in qual)}
 return {'nonempty_faces':len(faces),'face_fvector':dict(sorted(Counter(dim(s) for s in faces).items())),'qualifying':g,'broad_criterion_faces':len(broad),'vertical_faces':vertical}
r5=census(4,True);r4=census(4,False);r3=census(3,False)
check(r5['nonempty_faces']==543,'all product faces')
check(r5['qualifying']['vertices']==100 and r5['qualifying']['edges']==120,'graph census')
check(r5['qualifying']['integral_H0_rank']==2 and r5['qualifying']['integral_H1_rank']==22,'homology')
check(r4['qualifying']['vertices']==50 and r4['qualifying']['edges']==60 and r4['qualifying']['components']==1,'base')
check(r3['qualifying']=={'vertices':6,'comparisons':0},'old six-point control')
# Shellability graph criterion: connected pure graphs can be shelled by first
# a spanning tree then remaining edges; disconnected edges fail every order.
def shelling(edges):
 seen=set()
 for i,e in enumerate(edges):
  hit=seen&set(e)
  if i and not hit:return False
  seen.update(e)
 return True
check(all(not shelling(o) for o in permutations([(0,1),(2,3)])),'disjoint adverse all orders')
check(shelling([(0,1),(1,2),(2,0)]),'cycle positive shelling')
check(not shelling([(0,1),(2,3),(1,2)]),'late bridge adverse')
# Adverse mutation: drop full additivity and vertical faces are falsely kept.
check(r5['broad_criterion_faces']>r5['qualifying']['vertices'],'criterion mutation detected')
# Same-direction summands and an artificial top both invalidate conclusion.
check(dim(plus({(0,0),(1,0)},{(0,0),(1,0)}))==1,'shared direction deficiency')
check(dim(plus({(0,0),(1,0)},{(0,0),(0,1)}))==2,'whole positive independent segments')
check(rank([[1,-1],[1,1]],2)==1 and rank([[1,-1],[1,1]],3)==2,'sign mutation detector')
check(not shelling([(0,1),(2,3)]) and shelling([(0,1),(1,2),(2,3)]),'cross-copy mutation detector')
result={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':N,'grid_coverage':'Every extremal/max/min/intermediate pattern has a ternary labeling; subtract its zeroth label yields a normal in [-2,2]^d. Interval sign covers all product faces.','R5':r5,'R4':r4,'R3':r3,'adverse_and_positive_controls':8,'integral_justification':'Spanning forests give unimodular incidence minors; H0 free, H1 subgroup of free C1. Graph has no higher chains.'}
print(json.dumps(result,indent=2,sort_keys=True))

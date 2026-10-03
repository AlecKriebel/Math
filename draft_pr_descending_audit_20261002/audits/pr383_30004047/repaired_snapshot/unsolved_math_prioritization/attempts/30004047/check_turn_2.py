#!/usr/bin/env python3
from itertools import combinations,permutations,product
from fractions import Fraction as F
import json
checks=graphs=weighted=0
E=list(combinations(range(5),2))
def mask(es):return sum(1<<E.index(tuple(sorted(e))) for e in es)
cycles=set()
for p in permutations(range(1,5)):
 v=(0,)+p;cycles.add(mask([(v[i],v[(i+1)%5]) for i in range(5)]))
tri_edge=[]
for tri in combinations(range(5),3):
 other=tuple(i for i in range(5) if i not in tri)
 tri_edge.append(mask(list(combinations(tri,2))+[other]))
# Enumerate all half-integral dual candidates on all labeled five-vertex graphs.
good=[]
for g in range(1<<10):
 es=[E[i] for i in range(10) if g>>i&1]
 opt=max(sum(u) for u in product(range(3),repeat=5) if all(u[a]+u[b]<=2 for a,b in es))
 assert opt>=5;checks+=1
 if opt<6:
  assert opt==5;checks+=1
  assert any(g&w==w for w in list(cycles)+tri_edge);checks+=1
  good.append(g)
 graphs+=1
def comps(total,n,prefix=()):
 if n==1:
  if total>=1:yield prefix+(total,)
 else:
  for a in range(1,total-n+2):yield from comps(total-a,n-1,prefix+(a,))
# Every weighted eligible five-vertex support with cover cost <3 contains
# four pairwise incompatible edge types, independently of the chosen witness.
for den in range(5,13):
 for aa in comps(den,5):
  if max(aa)*2>=den:continue
  allowed=sum(1<<i for i,(a,b) in enumerate(E) if 2*(aa[a]+aa[b])<den)
  for g in good:
   if g&allowed!=g:continue
   es=[set(E[i]) for i in range(10) if g>>i&1]
   found=False
   for inds in combinations(range(len(es)),4):
    if all(2*sum(aa[v] for v in es[i]|es[j])>=den for i,j in combinations(inds,2)):
     found=True;break
   assert found;checks+=1;weighted+=1
# Four-vertex structural classification and the exact charge bound.
E4=list(combinations(range(4),2))
for g in range(1<<6):
 es=[set(E4[i]) for i in range(6) if g>>i&1]
 if any(not e&f for e,f in combinations(es,2)):continue
 independent3=any(all(not e<=set(I) for e in es) for I in combinations(range(4),3))
 triangle=any(all(set(e) in es for e in combinations(T,2)) for T in combinations(range(4),3))
 assert independent3 or triangle;checks+=1
# Sharp 14-vertex graph.
S=[{0,1},{1,2},{2,0},{3,4},{3,4}];N=[{0},{1},{2},{3},{3}]
for a in range(5):assert sum(a in s for s in S)==2;checks+=1
for c in range(4):assert len(set().union(*(S[i] for i in range(5) if c in N[i])))==2;checks+=1
assert F(2,5)+2*F(1,4)==F(9,10)<1;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'labeled_five_vertex_graphs':graphs,'weighted_rank_two_supports_checked':weighted,'sharp_graph_part_sizes':[5,5,4],'scope':'Exact finite controls for the structural argument; no unrestricted source conclusion.'},indent=2))

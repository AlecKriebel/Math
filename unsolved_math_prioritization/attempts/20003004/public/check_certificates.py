#!/usr/bin/env python3
"""Exact finite controls for the stated conventions; not a proof by sampling."""
from itertools import product, combinations
from pathlib import Path
import json

V = (1,-1,2,-2,3,-3)
b = -1
adj = lambda x,y: x != -y
edges = [(x,y) for x in V for y in V if adj(x,y)]
def continuous(f): return all(adj(f[x],f[y]) for x,y in edges)
def strong(f,g): return continuous(f) and continuous(g) and all(adj(f[x],g[y]) for x,y in edges)
def box(f,g): return continuous(f) and continuous(g) and all(adj(f[x],g[x]) for x in V)
identity = {x:x for x in V}
h = {x:(2 if x==1 else b) for x in V}
c = {x:b for x in V}
assert box(identity,h) and box(h,c)
assert not strong(identity,h)
assert not adj(identity[1],h[-2]) and adj(1,-2)
based = []
for a in product(V,repeat=5):
 f={b:b}; f.update(dict(zip([x for x in V if x!=b],a)))
 if continuous(f): based.append(f)
strong_neighbors = [f for f in based if strong(identity,f)]
assert strong_neighbors == [identity]
faces = {k:[s for s in combinations(V,k+1) if all(adj(x,y) for x,y in combinations(s,2))] for k in range(6)}
assert [len(faces[k]) for k in range(4)] == [6,12,8,0]
# A general elementary hyperplane-duplication lemma is checked in finite dimensions.
def alpha(m,j,i): return i if i<=j else i-1
alpha_count=0
for m in range(1,81):
 for j in range(m):
  for u in range(m+2):
   for v in range(max(0,u-1),min(m+1,u+1)+1):
    assert abs(alpha(m,j,u)-alpha(m,j+1,v))<=1
    alpha_count+=1
# Independent exhaustive check that strong homotopy equals flag contiguity.
# The domain is the reflexive 3-path, whose nontrivial maximal cliques are its two edges.
comparisons=0
for q in range(1,5):
 pairs=list(combinations(range(q),2))
 for bits in product((False,True),repeat=len(pairs)):
  E={e for e,z in zip(pairs,bits) if z}
  A=lambda x,y: x==y or tuple(sorted((x,y))) in E
  maps=[f for f in product(range(q),repeat=3) if A(f[0],f[1]) and A(f[1],f[2])]
  for f in maps:
   for g in maps:
    left=all(A(f[u],g[v]) for u in range(3) for v in range(3) if abs(u-v)<=1)
    right=all(all(A(x,y) for x,y in combinations(set(f[u:u+2]+g[u:u+2]),2)) for u in (0,1))
    assert left==right
    comparisons+=1
out={
 'octahedral_clique_counts':[len(faces[k]) for k in range(4)],
 'based_continuous_endomorphisms':len(based),
 'based_strong_neighbors_of_identity':len(strong_neighbors),
 'two_step_box_contraction':{'identity':identity,'middle':h,'constant':c},
 'failed_strong_cross_pair':[1,-2],
 'duplication_cross_checks':alpha_count,
 'strong_contiguity_comparisons':comparisons,
 'result':'all exact checks passed',
 'scope':'Finite controls accompany general proofs and do not establish the literature comparison theorem by enumeration.'
}
print(json.dumps(out,indent=2))
Path(__file__).with_name('certificate_results.json').write_text(json.dumps(out,indent=2)+'\n')

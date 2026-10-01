#!/usr/bin/env python3
"""Independent exact check of endpoint graph distances under an edge-axis half-turn."""
from itertools import product,combinations
from collections import Counter,deque
import json
from check_certificate import K
phi=K(1,1)/2
ip=phi-1
zero=K()
verts=[tuple(K(s) for s in v) for v in product([-1,1],repeat=3)]
for a,b in product([-1,1],repeat=2):
    verts += [(zero,a*ip,b*phi),(a*ip,b*phi,zero),(a*phi,zero,b*ip)]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def mul(a,x):return tuple(a*b for b in x)
edge_squared=4*ip*ip
edges=[(i,j) for i,j in combinations(range(20),2) if dot(sub(verts[i],verts[j]),sub(verts[i],verts[j]))==edge_squared]
assert len(edges)==30
graph={i:set() for i in range(20)}
for a,b in edges:graph[a].add(b);graph[b].add(a)
assert all(len(s)==3 for s in graph.values())
dists={}
for a in range(20):
    ds={a:0};q=deque([a])
    while q:
        b=q.popleft()
        for c in graph[b]:
            if c not in ds:ds[c]=ds[b]+1;q.append(c)
    assert len(ds)==20
    dists[a]=ds
answers=[]
for a,b in edges:
    axis=add(verts[a],verts[b]);norm=dot(axis,axis)
    perm=[verts.index(sub(mul(2*dot(x,axis)/norm,axis),x)) for x in verts]
    assert sorted(perm)==list(range(20)) and all(perm[perm[i]]==i for i in range(20))
    assert all(perm[i]!=i for i in range(20))
    assert perm[a]==b and perm[b]==a
    assert all(perm[v] in graph[perm[u]] for u,v in edges)
    hist=Counter(dists[i][perm[i]] for i in range(20))
    assert hist.get(2,0)==0
    answers.append(dict(edge=[a,b],permutation=perm,vertex_distance_histogram=dict(sorted(hist.items()))))
assert all(x['vertex_distance_histogram']==answers[0]['vertex_distance_histogram'] for x in answers)
print(json.dumps(dict(vertices=[[repr(a) for a in v] for v in verts],edge_squared=repr(edge_squared),edge_count=len(edges),all_30_half_turns=answers),indent=2))

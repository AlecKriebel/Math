#!/usr/bin/env python3
"""Independent word-tree construction and exact arbitrary-order Kron checks.
No deposited generator/verifier or certificate is read.
"""
from fractions import Fraction as F
import json, random
from pathlib import Path
from datetime import datetime, timezone

def parent(w):
    return w + (0,) if all(t == 0 for t in w) else w[:-1]

def tree_neighbors(w):
    if not w: return [(0,), (1,), (2,)]
    return [w[:-1], w+(0,), w+(1,)]

def children(w):
    return [z for z in tree_neighbors(w) if z != parent(w)]

def descendants(w, depth):
    out={w}; layer={w}
    for _ in range(depth):
        layer={z for v in layer for z in children(v)}
        out |= layer
    return out

def edges(V):
    E=set()
    for w in V:
        for z in (parent(w),parent(parent(w))):
            if z in V: E.add(tuple(sorted((w,z))))
    return E

def kron(V,E,terminals,seed=4417):
    adj={v:{} for v in V}
    for v,w in E: adj[v][w]=adj[w][v]=F(1)
    interior=sorted(set(V)-set(terminals))
    random.Random(seed).shuffle(interior)
    for v in interior:
        nbs=list(adj[v].items()); total=sum(c for _,c in nbs)
        for i,(x,cx) in enumerate(nbs):
            for y,cy in nbs[i+1:]:
                val=adj[x].get(y,F(0))+cx*cy/total
                adj[x][y]=adj[y][x]=val
        for x,_ in nbs: del adj[x][v]
        del adj[v]
    return tuple(adj[x].get(y,F(0)) for x,y in
                 [(terminals[0],terminals[1]),(terminals[1],terminals[2]),(terminals[0],terminals[2])])

def c_sequence(m):
    c=[F(1)]
    for _ in range(m): c.append(1+2*c[-1]/(1+c[-1]))
    return c

def a(c,m): return 1+c[m-1]/(1+c[m-1])

def induced_expected(n):
    c=c_sequence(2*n)
    u=a(c,2*n-1)
    for j in range(n-2,0,-1): u=a(c,n+j)+u/(1+u)
    return (c[n],u,F(1))

def L_vertices_edges(m,n):
    spine=[(0,)*i for i in range(n+1)]
    V=set(spine)
    for i in range(n):
        for w in children(spine[i]):
            if i>0 and w==spine[i-1]: continue
            V|=descendants(w,m)
    # Here all induced edges on V coincide with the stated branch union:
    # the top vertex has no off-spine descendants in V, and cross-branch
    # grandparent edges can only hit the two included branch terminals.
    return V,edges(V)

def L_expected(m,n):
    k=F(1,2)
    for _ in range(m): k=(1+2*k)/(2+2*k)
    A=1+2*k; C=1+k; B=C
    for _ in range(n-2): B=C+B/(1+B)
    return (A,B,F(1))

results=[]
terms=[(),(0,),(0,0)]
for n in [2,3]:
    V=descendants((0,)*n,2*n); E=edges(V)
    observed=kron(V,E,terms); expected=induced_expected(n)
    assert observed==expected,(n,observed,expected)
    A,B,C=observed
    Rtree=1/(A+B/(1+B)); Rgp=1/(1+A*B/(A+B))
    results.append(dict(family='induced',n=n,vertices=len(V),edges=len(E),triangle=list(map(str,observed)),Rtree=str(Rtree),Rgp=str(Rgp)))
for m,n in [(0,2),(1,3),(2,4)]:
    V,E=L_vertices_edges(m,n)
    observed=kron(V,E,terms); expected=L_expected(m,n)
    assert observed==expected,(m,n,observed,expected)
    results.append(dict(family='diagonal',m=m,n=n,vertices=len(V),edges=len(E),triangle=list(map(str,observed))))

# Radius-ten tree ball, built by word length, independently of indexed formulas.
V={()}; layer={()}
for depth in range(10):
    new=set()
    for w in layer:
        for z in tree_neighbors(w):
            if len(z)==depth+1: new.add(z)
    V|=new; layer=new
E=edges(V)
adj={v:set() for v in V}
for v,w in E: adj[v].add(w);adj[w].add(v)
JE=set(E)
for v in V:
    for w in adj[v]:
        for z in adj[w]:
            if v!=z: JE.add(tuple(sorted((v,z))))
Jroot={w if v==() else v for v,w in JE if () in (v,w)}
assert len(V)==3070 and len(JE)==19931 and len(Jroot)==40
ordered=sorted(V,key=lambda w:(len(w),w))
indices={v:i for i,v in enumerate(ordered)}
root_indices=sorted(indices[v] for v in Jroot)
assert root_indices==list(range(1,23))+[24,25]+list(range(30,46))
results.append(dict(family='square_geometry',vertices=len(V),K_edges=len(E),J_edges=len(JE),root_degree=len(Jroot),root_indices=root_indices))

# Verify local triangle counts using interior edges, avoiding boundary artefacts.
for v,w in [((),(0,)),((),(0,0))]:
    common=adj[v]&adj[w]
    assert len(common)==(3 if len(w)==1 else 1)
results.append(dict(family='graph_structure',tree_edge_triangles=3,grandparent_edge_triangles=1))
output=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),method='word-tree construction, arbitrary-order exact rational Kron elimination',results=results)
Path(__file__).with_name('independent_finite_checks.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))

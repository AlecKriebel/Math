#!/usr/bin/env python3
"""Small independent local controls; no universal topological certification."""
from itertools import combinations
from fractions import Fraction
from collections import Counter
import json

def require(ok, message):
    if not ok: raise RuntimeError(message)

def simplex(v):
    v=sorted(v)
    return {frozenset(c) for k in range(len(v)+1) for c in combinations(v,k)}

def sphere_boundary(v):
    return simplex(v)-{frozenset(v)}

def join(a,b):
    return {x|y for x in a for y in b}

def vertex_set(c):
    return set().union(*c)

def missing(c):
    return {frozenset(t) for t in combinations(sorted(vertex_set(c)),3)
            if frozenset(t) not in c and all(frozenset(e) in c for e in combinations(t,2))}

def rank2(columns):
    basis={}
    for x in columns:
        while x:
            i=x.bit_length()-1
            if i in basis: x ^= basis[i]
            else:
                basis[i]=x
                break
    return len(basis)

def low_homology(c):
    verts=sorted(vertex_set(c)); vi={v:i for i,v in enumerate(verts)}
    edges=sorted((tuple(sorted(f)) for f in c if len(f)==2))
    ei={e:i for i,e in enumerate(edges)}
    r1=rank2([(1<<vi[a])^(1<<vi[b]) for a,b in edges])
    r2=rank2([sum(1<<ei[tuple(e)] for e in combinations(sorted(f),2)) for f in c if len(f)==3])
    return len(verts)-r1-1, len(edges)-r1-r2

moves=[]; complements=0
for p in range(5):
    q=4-p
    a=frozenset(range(p+1)); b=frozenset(range(p+1,6)); v=frozenset({6})
    old=join(simplex(a), sphere_boundary(b))
    new=join(sphere_boundary(a), simplex(b))
    boundary=join(sphere_boundary(a),sphere_boundary(b))
    exterior=join(simplex(v), boundary)
    Q=old|exterior; Qnew=new|exterior
    M=missing(Q); Mnew=missing(Qnew)
    require({f for f in Q if f<=vertex_set(old)} == old, 'old support not induced')
    for rho in boundary:
        if len(rho)>3: continue
        W=vertex_set(old)-set(rho)
        deletion={f for f in Q if not f & W}
        require(low_homology(deletion)==(0,0), f'complement homology {p,q,rho}')
        complements+=1
    new_missing=Mnew-M
    allowed=set()
    if p==2: allowed={a}
    if q==1: allowed={b|v}
    require(new_missing==allowed, f'new missing classification {p,q,new_missing}')
    if p==2:
        old_aug={f for f in Q if len(f)<=3}|{b}
        new_aug={f for f in Qnew if len(f)<=3}|{a}
        require(old_aug==new_aug,'middle-move identity')
    if q==1:
        require({f for f in Qnew if len(f)<=3}|{b|v} == {f for f in simplex(range(7)) if len(f)<=3},'Flores local example not full')
    moves.append({'p':p,'q':q,'old_vertices':len(vertex_set(Q)),'new_vertices':len(vertex_set(Qnew)),
                  'new_missing_triangles':[sorted(f) for f in sorted(new_missing,key=lambda f:tuple(sorted(f)))]})

# Explicit ordered coordinates in complementary R^3 and R^1 subspaces.
alpha=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(-1,-1,-1,0)]
beta=[(0,0,0,-1),(0,0,0,1)]
require(tuple(sum(Fraction(1,4)*x[j] for x in alpha) for j in range(4))==(0,0,0,0), 'alpha center')
require(tuple(sum(Fraction(1,2)*x[j] for x in beta) for j in range(4))==(0,0,0,0), 'beta center')
require(len({x[:3] for x in alpha})==4 and all(x[3]==0 for x in alpha), 'complementary support')

# Count each unordered deleted-product cell once and calculate its actual boundary.
triangles=list(combinations(range(7),3))
cells=[(a,b) for a,b in combinations(triangles,2) if not set(a)&set(b)]
def boundary4(chain):
    out=Counter()
    for a,b in chain:
        for small,other in [(a,b),(b,a)]:
            for edge in combinations(small,2):
                out[(edge,other)] ^= 1
    return {k for k,v in out.items() if v}
require(not boundary4(cells), 'Flores chain not closed')
require(bool(boundary4(cells[:-1])), 'deleted-cell negative control escaped')
m=(4,5,6)
partners={b if a==m else a for a,b in cells if a==m or b==m}
require(partners==set(combinations(range(4),3)), 'M partner chain not tetrahedron boundary')
# Exact affine moment-curve circuits: barycentric divided-difference identity.
crossings=0
for a,b in cells:
    union=sorted(a+b)
    weights={x:Fraction(1, __import__('math').prod(x-y for y in union if y!=x)) for x in union}
    require(all(sum(weights[x]*x**k for x in union)==0 for k in range(5)), 'affine circuit identity')
    positive={x for x,w in weights.items() if w>0}
    if set(a)==positive or set(b)==positive: crossings+=1
require(crossings==7 and crossings%2==1, 'intersection parity')
print(json.dumps({'passed':True,'local_bistellar_move_types':moves,'complement_low_homology_checks':complements,
                  'flores_cells':len(cells),'flores_nonzero_boundary_cells':0,'moment_curve_crossings':crossings,
                  'M_partners':[list(x) for x in sorted(partners)],'negative_controls':1,
                  'scope':'Five constructed standard local sphere examples and an exact finite chain/circuit witness; does not verify arbitrary sphere topology, contractibility, generic anisotropy, or Weber.'},indent=2))

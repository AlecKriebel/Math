#!/usr/bin/env python3
"""Exact finite controls for the four/five-choice extensional obstruction."""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1
def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def onseg(p,a,b):return orient(a,b,p)==0 and all(min(a[j],b[j])<=p[j]<=max(a[j],b[j]) for j in (0,1))
def intersects(a,b,c,d):
    o=[orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)]
    if o[0]*o[1]<0 and o[2]*o[3]<0:return True
    return any([o[0]==0 and onseg(c,a,b),o[1]==0 and onseg(d,a,b),o[2]==0 and onseg(a,c,d),o[3]==0 and onseg(b,c,d)])

V=[(F(1,8),F(1,8)),(F(7,8),F(1,8)),(F(1,2),F(7,8)),(F(1,2),F(3,8))]
E=list(combinations(range(4),2));sets=[frozenset(A) for k in range(1,5) for A in combinations(range(4),k)]
for i,p in enumerate(V):
    for a,b in E:
        if i not in (a,b):ck('no_nonincident_vertex_edge_contact',not onseg(p,V[a],V[b]))
for e,f in combinations(E,2):
    if not set(e)&set(f):ck('K4_independent_edges_disjoint',not intersects(V[e[0]],V[e[1]],V[f[0]],V[f[1]]))

def edges(A):return [e for e in E if set(e)<=A]
def cells_disjoint(A,B):
    if A&B:return False
    for i in A:
        for j,k in edges(B):
            if onseg(V[i],V[j],V[k]):return False
    for i in B:
        for j,k in edges(A):
            if onseg(V[i],V[j],V[k]):return False
    return not any(intersects(V[i],V[j],V[k],V[l]) for i,j in edges(A) for k,l in edges(B))

samples=0
for A in sets:
    ck('nonempty_induced_graph',len(A)>0)
    ck('complete_induced_graph_connected',len(A)==1 or all(tuple(sorted((i,j))) in edges(A) for i,j in combinations(A,2)))
    for B in sets:
        if A<=B:ck('finite_monotonicity',set(edges(A))<=set(edges(B)))
        if not A&B:ck('all_disjoint_subset_images',cells_disjoint(A,B))
    points=[V[i] for i in A]
    for i,j in edges(A):
        for n in range(1,10):
            lam=F(n,10);points.append(tuple((1-lam)*V[i][k]+lam*V[j][k] for k in (0,1)))
    for p in points:
        allowed=[]
        for i in range(4):
            in_forbidden=any(p==V[j] for j in range(4) if j!=i) or any(onseg(p,V[j],V[k]) for j,k in E if i not in (j,k))
            if not in_forbidden:allowed.append(i)
        ck('open_star_decoder_cover',bool(allowed))
        ck('all_decoder_choices_sound',set(allowed)<=A)
        samples+=1

# Classical K5 crossing parity: a concrete convex drawing and the finite
# independent-edge coordinate space for elementary vertex-edge switches.
P=[(0,0),(4,0),(6,3),(3,6),(-1,3)];EE=list(combinations(range(5),2))
independent=[(e,f) for e,f in combinations(EE,2) if not set(e)&set(f)]
ck('K5_independent_pair_count',len(independent)==15)
crossmask=0
for k,(e,f) in enumerate(independent):
    if intersects(P[e[0]],P[e[1]],P[f[0]],P[f[1]]):crossmask|=1<<k
ck('convex_K5_five_crossings',crossmask.bit_count()==5)
for e in EE:
    remaining=set(range(5))-set(e);others=[f for f in EE if set(f)<=remaining]
    ck('independent_edges_form_triangle',len(others)==3 and all(sum(v in f for f in others)==2 for v in remaining))
vectors=[]
for e in EE:
    for v in set(range(5))-set(e):
        mask=0
        for k,(f,g) in enumerate(independent):
            if (f==e and v in g) or (g==e and v in f):mask|=1<<k
        ck('vertex_edge_switch_even',mask.bit_count()==2)
        vectors.append(mask)
basis={}
for x in vectors:
    while x:
        bit=x.bit_length()-1
        if bit in basis:x^=basis[bit]
        else:basis[bit]=x;break
ck('switch_space_rank',len(basis)==14)
ck('all_switch_vectors_even',all(v.bit_count()%2==0 for v in vectors))
x=crossmask
while x and x.bit_length()-1 in basis:x^=basis[x.bit_length()-1]
ck('convex_mask_not_in_even_switch_space',x!=0)

print(json.dumps({'problem_id':30003661,'turn':2,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'K4_decoder_sample_points':samples,'K5_switch_space_dimension':len(basis),
    'arithmetic':'exact rational segment geometry and GF(2) elimination',
    'scope':'Finite controls for monotone/extensional preprocessing only. The classical planar parity argument and name-continuity proof are analytical; arbitrary name-dependent Weihrauch reductions remain outside the obstruction.'},indent=2,sort_keys=True))

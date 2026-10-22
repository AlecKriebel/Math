#!/usr/bin/env python3
"""Exact source-normalization diagnostics, not a finiteness proof."""
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json

C=Counter()
def ck(condition, category):
    assert condition,category
    C[category]+=1

def complex_from_facets(facets):
    return {frozenset(s) for t in facets for k in range(len(t)+1)
            for s in combinations(sorted(t),k)}

def boundary_faces(facets,D):
    incidences=Counter(frozenset(s) for t in facets for s in combinations(sorted(t),D))
    ck(all(c in (1,2) for c in incidences.values()),'ridge_incidence_one_or_two')
    return complex_from_facets([s for s,c in incidences.items() if c==1])

def fvector(K,D):
    return [sum(len(s)==j for s in K) for j in range(D+2)]

def hvector(f,D):
    return [sum((-1)**(i-j)*comb(D+1-j,D+1-i)*f[j]
                for j in range(i+1)) for i in range(D+2)]

def audit_manifold(facets,D):
    K=complex_from_facets(facets)
    B=boundary_faces(facets,D)
    f=fvector(K,D);h=hvector(f,D)
    vb=sum(len(s)==1 for s in B)
    vi=f[1]-vb
    q=f[2]-D*f[1]+comb(D+1,2)-vi
    ck(h[2]-vi==q,'h2_dimension_shift_on_complexes')
    ck(h[D]+(D+1)*h[D+1]==vi,'interior_vertex_h_identity')
    vstar=max(v for s in K for v in s)+1
    completed=K|{s|{vstar} for s in B}
    fc=fvector(completed,D)
    ck(fc[1]==f[1]+1,'completion_vertex_count')
    ck(fc[2]==f[2]+vb,'completion_edge_count')
    ck(fc[2]-(D+1)*fc[1]+comb(D+2,2)==q,'completion_g2_equals_q')
    link={s-{vstar} for s in completed if vstar in s}
    ck(link==B,'cone_vertex_link_is_boundary')
    return q,K,B

# Simplex balls followed by boundary facet stacking. Each step keeps all
# vertices on the boundary and preserves q despite unbounded vertex count.
for D in range(2,8):
    facets={frozenset(range(D+1))}
    q,K,B=audit_manifold(facets,D)
    ck(q==0,'simplex_ball_zero')
    for step in range(1,9):
        boundary=boundary_faces(facets,D)
        F=next(s for s in sorted(boundary,key=lambda s:tuple(sorted(s))) if len(s)==D)
        v=D+step
        oldf=fvector(K,D)
        facets.add(F|{v})
        q,K,B=audit_manifold(facets,D)
        newf=fvector(K,D)
        ck(q==0,'stacked_ball_zero')
        ck(newf[1]-oldf[1]==1 and newf[2]-oldf[2]==D,'stacking_face_increments')
        ck(all(frozenset({i}) in B for i in range(v+1)),'stacked_vertices_stay_boundary')

# Standard staircase triangulations of C_t x simplex^(D-1). Every edge of
# the cycle is a prism; its D maximal chains give a compatible triangulation.
# For D=3 these are solid tori and their boundaries are triangulated tori.
torus_diagnostics=[]
for D in range(2,6):
    for t in (3,4,5,6):
        facets=set()
        for a in range(t):
            a,b=sorted((a,(a+1)%t))
            for k in range(D):
                vertices=[a*D+j for j in range(k+1)]+[b*D+j for j in range(k,D)]
                facets.add(frozenset(vertices))
        q,K,B=audit_manifold(facets,D)
        ck(len(facets)==t*D,'product_prism_facet_count')
        ck(sum(len(s)==1 for s in K)==t*D,'product_vertex_count')
        euler=sum((-1)**(len(s)-1) for s in K if s)
        ck(euler==0,'circle_product_euler_characteristic')
        if D==3:
            boundary_euler=sum((-1)**(len(s)-1) for s in B if s)
            ck(boundary_euler==0 and boundary_euler!=2,'torus_link_not_two_sphere')
            torus_diagnostics.append({'cycle_vertices':t,'q':q,
                'f_vector':fvector(K,D)[1:],
                'boundary_f_vector':fvector(B,D-1)[1:],
                'boundary_euler':boundary_euler})

# Coefficient extraction from the h-polynomial, including arbitrary test
# vectors; only f_-1, f_0 and f_1 can contribute to h_2.
for D in range(2,17):
    for case in range(31):
        f=[1]+[(case+3)*(j+2)**2+case*j for j in range(D+1)]
        h=hvector(f,D)
        ck(h[2]==f[2]-D*f[1]+comb(D+1,2),'h2_polynomial_coefficient')
        for vi in (0,1,case+2):
            q=f[2]-D*f[1]+comb(D+1,2)-vi
            ck(h[2]-vi==q,'exact_report_dimension_rename')
            ck((f[2]+f[1]-vi)-(D+1)*(f[1]+1)+comb(D+2,2)==q,
               'symbolic_count_completion_formula')

for D in range(2,17):
    for r in range(1,21):
        v=r*(D+1);e=r*comb(D+1,2)
        ck(e-D*v+comb(D+1,2)==(1-r)*comb(D+1,2),
           'disconnected_union_constant_offset')
    v=D+2;e=comb(D+2,2)
    g2=e-(D+1)*v+comb(D+2,2)
    raw=e-D*v+comb(D+1,2)-v
    ck(g2==0 and raw==-(D+1),'closed_simplex_boundary_offset')

p=Path(__file__).resolve().parent
print(json.dumps({'status':'PASS','assertions':sum(C.values()),
    'categories':dict(sorted(C.items())),
    'solid_torus_diagnostics':torus_diagnostics,
    'artifact_sha256':hashlib.sha256((p/'SOURCE_STATUS.md').read_bytes()).hexdigest(),
    'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope':'Exact elementary normalization and category diagnostics. Does not prove the announced general boundary finiteness theorem.'},indent=2,sort_keys=True))

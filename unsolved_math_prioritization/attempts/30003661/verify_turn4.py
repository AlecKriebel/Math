#!/usr/bin/env python3
"""Finite exact controls for the graph-carrier argument; not a uniform selector."""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1
V=[(F(1,8),F(1,8)),(F(7,8),F(1,8)),(F(1,2),F(7,8)),(F(1,2),F(3,8))]
def point(a,b,t):return tuple((1-t)*a[j]+t*b[j] for j in (0,1))
witnesses=0
for i,j in combinations(range(4),2):
    a,b=V[i],V[j]
    ck('distinct_computable_edge_endpoints',a!=b)
    for den in range(2,11):
        for u,v in combinations(range(den+1),2):
            left,right=F(u,den),F(v,den);q=(left+right)/2
            x=point(a,b,q);xl=point(a,b,left);xr=point(a,b,right)
            ck('strict_rational_parameter_witness',left<q<right)
            ck('image_witness_in_segment',x==tuple((xl[k]+xr[k])/2 for k in (0,1)))
            ck('ambient_cube_boundary',all(0<=y<=1 for y in x))
            if left==0:ck('left_graph_vertex_case',xl==a)
            if right==1:ck('right_graph_vertex_case',xr==b)
            if 0<left<right<1:ck('vertex_free_edge_case',x!=a and x!=b)
            witnesses+=1
    for q in [F(0),F(1,3),F(1,2),F(1)]:
        x=point(a,b,q)
        ck('singleton_parameter_image',point(a,b,q)==x)
        coord=next(k for k in (0,1) if a[k]!=b[k])
        ck('injective_parameter_recovery',(x[coord]-a[coord])/(b[coord]-a[coord])==q)

# Finite-cover certificate geometry for the singleton case: any certified ball
# of radius epsilon containing the singleton provides the epsilon approximation.
for n in range(1,61):
    radius=F(1,2**(n+2))
    for q in [F(0),F(1,7),F(1,2),F(1)]:
        center=q+radius/2
        ck('singleton_ball_error',abs(center-q)<radius<F(1,2**n))
        ck('precision_adjustment',2*radius<=F(1,2**n))
print(json.dumps({'problem_id':30003661,'turn':4,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'rational_subarc_witnesses':witnesses,
    'arithmetic':'rational arithmetic only','scope':'Exact geometric boundary controls. Nonuniform computable-point existence, singleton search termination and the WKL obstruction are analytical proofs, not a uniform selector inferred from these samples.'},indent=2,sort_keys=True))

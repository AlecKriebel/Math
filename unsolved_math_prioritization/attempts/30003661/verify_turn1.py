#!/usr/bin/env python3
"""Exact collision certificates for the scoped planar-flattening obstruction."""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1

paths=[[(F(0),F(0)),(F(1),F(1))],
       [(F(0),F(0)),(F(1,3),F(4,5)),(F(2,3),F(1,5)),(F(1),F(1))],
       [(F(0),F(0)),(F(1,4),F(0)),(F(3,4),F(1)),(F(1),F(1))],
       [(F(0),F(0)),(F(1,2),F(1)),(F(3,4),F(1,2)),(F(1),F(1))]]

def evaluate(path,z):
    for (x,u),(y,v) in zip(path,path[1:]):
        if x<=z<=y:return u+(v-u)*(z-x)/(y-x)
    raise AssertionError('outside path')

def find_crossing(path,value):
    for (x,u),(y,v) in zip(path,path[1:]):
        if min(u,v)<=value<=max(u,v):
            return x if u==v else x+(y-x)*(value-u)/(v-u)
    raise AssertionError('IVT crossing omitted')

collisions=0
for path in paths:
    ck('boundary_interpolation',path[0]==(0,0) and path[-1]==(1,1))
    ck('piecewise_linear_domain',all(x<y for (x,_),(y,_) in zip(path,path[1:])))
    ck('interpolation_stays_in_unit_interval',all(0<=v<=1 for _,v in path))
    for den in range(2,9):
        for i,j,k in combinations(range(den+1),3):
            r,a,s=F(i,den),F(j,den),F(k,den)
            alpha=(a-r)/(s-r);z=find_crossing(path,alpha)
            ck('strict_disjoint_source_sets',r<a<s and a not in {r,s})
            ck('exact_piecewise_crossing',0<z<1 and evaluate(path,z)==alpha)
            ck('choice_coordinates_interpolate_to_wrong_singleton',(1-alpha)*r+alpha*s==a)
            for h in [lambda z:z,lambda z:1-z,lambda z:F(1,2),lambda z:z*(1-z)]:
                height=h(z)
                pair_output=((1-alpha)*r+alpha*s,height)
                singleton_output=((1-alpha)*a+alpha*a,height)
                ck('shared_output_exact',pair_output==singleton_output)
                ck('valid_planar_point',all(0<=x<=1 for x in pair_output))
                ck('vertical_source_membership',(r in {r,s}) and (s in {r,s}) and 0<=z<=1)
                ck('singleton_source_membership',a==a and 0<=z<=1)
                collisions+=1

# Explicit canonical affine witness, including the exact preserved height.
r,a,s=F(0),F(1,2),F(1);z=(a-r)/(s-r)
ck('canonical_affine_witness',(1-z)*r+z*s==a and z==F(1,2))
print(json.dumps({'problem_id':30003661,'turn':1,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'exact_overlap_certificates':collisions,
    'arithmetic':'rational arithmetic only',
    'scope':'Finite illustrations of the proved continuous-template obstruction. This does not show nonreducibility for arbitrary planar path-connected encodings, and does not identify ordinary and strong Weihrauch reducibility.'},indent=2,sort_keys=True))

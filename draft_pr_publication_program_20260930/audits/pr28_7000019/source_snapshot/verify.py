#!/usr/bin/env python3
"""Bounded exact controls for the strip note; not a rigidity-proof certificate."""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
import json

counts=Counter()
def check(ok,name):
    assert ok,name
    counts[name]+=1

# Spherical area uses 2*pi times the length in vertical coordinate.
# All factors of pi are removed, so this checks the half/full-width factors.
for a in [F(1,4),F(1,2),F(1),F(3,2)]:
    for scale in range(2,22):
        radius=a*scale
        length=2*a/radius
        h=2*a
        check(2*length == 4*a/radius, 'orientation_area_coefficient')
        check(length/2 == h/(2*radius), 'orientation_probability')
        R=radius
        C_over_pi=2*R*h
        U_over_pi=4*R
        check(U_over_pi==2*C_over_pi/h, 'sphere_potential_normalization')

vertices=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
for direction in product(range(-3,4),repeat=3):
    if direction==(0,0,0): continue
    projection=[sum(u*x for u,x in zip(direction,v)) for v in vertices]
    raw_width=max(projection)-min(projection)
    a,b,c=sorted(map(abs,direction),reverse=True)
    norm2=sum(x*x for x in direction)
    check(raw_width==2*(a+b), 'tetrahedron_support_formula')
    check(F(raw_width*raw_width,norm2)>=4, 'tetrahedron_minimum_width')
for face in combinations(range(4),3):
    omitted=next(i for i in range(4) if i not in face)
    normal=vertices[omitted]
    check(all(sum(normal[j]*vertices[i][j] for j in range(3))==-1
              for i in face), 'tetrahedron_face_distance')
check(F(3,2)**2>F(4,3), 'inradius_shortcut_negative_control')
check(F(3,2)<2, 'inradius_shortcut_negative_control')

# Disconnected warning only: all admissible slabs contain the inner sphere.
for R in [F(1),F(2),F(3)]:
    r=R/4; h=3*R/2
    constant=2*R*h+4*r*r # area divided by pi
    for k in range(21):
        t=-R+(2*R-h)*F(k,20)
        check(-R<=t<=R-h and t<=-r and t+h>=r,
              'nested_sphere_containment')
        outer_length=min(R,t+h)-max(-R,t)
        inner_length=min(r,t+h)-max(-r,t)
        area=2*R*outer_length+2*r*inner_length
        check(area==constant, 'nested_sphere_strip_area')

print(json.dumps({'status':'passed','arithmetic':'exact integers and fractions',
 'checks':dict(counts),'total_assertions':sum(counts.values()),
 'scope':'Finite normalization and counterexample-control checks only; no proof certificate for Reichel rigidity or the unresolved full strip problem'},indent=2))

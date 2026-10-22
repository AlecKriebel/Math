#!/usr/bin/env python3
"""Recover boundary walks for the 2020 V2 coordinate/face-set tables.

This is a source-credit control, not a new construction: enumerate incidence
isomorphisms to the already certified 2026 face walks, then independently
verify the 2020 coordinates by the exact triangle method. The 2020 table
order is never interpreted as a cyclic boundary order.
"""
from fractions import Fraction as F
from itertools import permutations
from collections import Counter
import json
from check_triangulation import C, verify

xyz='''
-212 0 -100;212 0 -100;-88 12 -76;88 -12 -76;
-70 -150/7 -40;70 150/7 -40;-2120/33 -1060/33 -940/33;2120/33 1060/33 -940/33;
-60 -40 -20;60 40 -20;-6360/163 -7420/163 -1460/163;6360/163 7420/163 -1460/163;
-7420/163 6360/163 1460/163;7420/163 -6360/163 1460/163;-40 60 20;40 -60 20;
1060/33 -2120/33 940/33;-1060/33 2120/33 940/33;-150/7 70 40;150/7 -70 40;
12 88 76;-12 -88 76;0 212 100;0 -212 100
'''
sets='''
1 3 5 6 7 9 11 14 17;
7 11 13 15 18 19 20 21 23;
4 6 8 10 14 16 21 23 24;
1 2 4 9 11 16 17 20 22;
8 12 14 16 17 19 20 22 24;
2 1 3 10 12 15 18 19 21;
3 5 7 9 13 15 22 24 23;
2 4 5 6 8 10 12 13 18
'''
vertices=[tuple(F(x) for x in r.split()) for r in xyz.split(';')]
faces=[{int(x)-1 for x in r.split()} for r in sets.split(';')]
old_triples=[frozenset(i for i,c in enumerate(faces) if v in c) for v in range(24)]
new_triples=[frozenset(i for i,c in enumerate(C) if v in c) for v in range(24)]
assert len(set(old_triples))==len(set(new_triples))==24
assert all(len(t)==3 for t in old_triples+new_triples)
new_index={t:i for i,t in enumerate(new_triples)}
isomorphisms=[]
for p in permutations(range(8)):
    transformed=[frozenset(p[i] for i in t) for t in old_triples]
    if set(transformed)==set(new_triples):
        vertex_map=[new_index[t] for t in transformed]
        isomorphisms.append((p,vertex_map))
assert len(isomorphisms)==8
certified=[]
for p,vertex_map in isomorphisms:
    inverse={new:old for old,new in enumerate(vertex_map)}
    try: verify([vertices[inverse[i]] for i in range(24)],C)
    except AssertionError: continue
    certified.append((p,vertex_map))
assert len(certified)==4
p,vertex_map=certified[0]
inverse={new:old for old,new in enumerate(vertex_map)}
new_coordinates=[vertices[inverse[i]] for i in range(24)]
result=verify(new_coordinates,C)
old_cycles=[None]*8
for old_face,new_face in enumerate(p):
    old_cycles[old_face]=[inverse[v] for v in C[new_face]]
    assert set(old_cycles[old_face])==faces[old_face]
# Verify again using the original vertex numbering and recovered face order.
original_numbering=verify(vertices,old_cycles)
assert original_numbering['absolute_volume']==result['absolute_volume']
print(json.dumps(dict(status='PASS',source='Mizhaev 2020, V2, Tables 5 and 6',
    face_vertex_incidence_isomorphisms=len(isomorphisms),
    geometrically_certified_boundary_isomorphisms=len(certified),
    old_face_to_new=[v+1 for v in p],
    old_vertex_to_new=[v+1 for v in vertex_map],
    recovered_2020_face_cycles=[[v+1 for v in c] for c in old_cycles],
    verification=original_numbering),indent=2))

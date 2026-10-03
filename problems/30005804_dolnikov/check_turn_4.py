"""Deterministic exact controls for TURN_4.md. Analytic theorem is in the text."""
from row_geometry import *
from random import Random
import json

rng = Random(30005804)
assertions = 0
branches = [0, 0]
cases = 0
incidences = 0

def ck(v):
    global assertions
    assertions += 1
    assert v

def verify(K, A, B, result, bound):
    global incidences
    i, Q = result
    branches[i] += 1
    ck(len(Q) <= bound)
    for t in (A, B)[i]:
        ck(any(inside(sub(q,t), K) for q in Q))
        incidences += 1

shapes = [[(0,0),(2,0),(0,2)], [(0,0),(3,0),(2,2),(0,1)],
          [(0,0),(2,0),(3,1),(1,3),(0,2)], [(0,0),(2,0),(2,2),(0,2)]]
for raw in shapes:
    K = list(map(pt, raw)); D = difference(K)
    U = [pt((F(x,2),F(y,2))) for x in range(-6,7) for y in range(-6,7)
         if inside(pt((F(x,2),F(y,2))),D)]
    V = [pt((x,y)) for x in range(-6,7) for y in range(-6,7)]
    ell = longest_horizontal(K)[0]
    for _ in range(160):
        ar = rng.sample(sorted(rows(U)), min(3,len(rows(U))))
        possible = [p for p in U if p[1] in ar]
        A = rng.sample(possible, rng.randrange(1,min(len(possible),12)+1))
        common = [b for b in V if all(inside(sub(a,b),D) for a in A)]
        ck(pt((0,0)) in common)
        br = rng.sample(sorted(rows(common)), min(3,len(rows(common))))
        B = [p for p in common if p[1] in br]
        for xs in rows(A).values():
            for ys in rows(B).values():
                ck(row_span(xs)+row_span(ys) <= 2*ell)
        verify(K,A,B,row_piercing(K,A,B),3)
        cases += 1

# Wide-spaced row systems for a continuum parameter sampled at exact rationals.
trapezoid_cases = 0
for m in map(F,[1,2,3,4,5,8,13]):
    K = list(map(pt,[(0,0),(m,0),(1,1),(0,1)])); D = difference(K)
    U = [pt((F(x,2),y)) for x in range(-2*int(m),2*int(m)+1)
         for y in [-1,0,1] if inside(pt((F(x,2),y)),D)]
    V = [pt((F(x,2),y)) for x in range(-4*int(m),4*int(m)+1)
         for y in range(-2,3)]
    for _ in range(35):
        A = rng.sample(U,rng.randrange(1,min(12,len(U))+1))
        B = [b for b in V if all(inside(sub(a,b),D) for a in A)]
        ck(bool(B))
        verify(K,A,B,row_system_piercing(K,A,B),2)
        trapezoid_cases += 1

K = list(map(pt,[(0,0),(1,0),(1,1),(0,1)])); D = difference(K)
A = list(map(pt,[(-1,0),(1,0)])); B = list(map(pt,[(0,-1),(0,1)]))
ck(all(inside(sub(a,b),D) for a in A for b in B))
ck(not inside(sub(A[0],A[1]),D)); ck(not inside(sub(B[0],B[1]),D))
verify(K,A,B,row_system_piercing(K,A,B),2)
ck(all(branches))
print(json.dumps({'assertions':assertions,'row_cases':cases,
                  'trapezoid_row_system_cases':trapezoid_cases,
                  'construction_branches':branches,'piercing_incidences':incidences,
                  'scope':'Exact finite controls of the all-size analytic row theorems; original unresolved'},
                 indent=2,sort_keys=True))

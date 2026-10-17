#!/usr/bin/env python3
"""Independent finite arithmetic and geometry checks; not a game solver."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

E = set(product((-1, 0, 1), repeat=2))
geometry_checks = []
for k in range(5):
    a = 2**k
    if len(E) != 9*a*a or max(max(abs(x), abs(y)) for x,y in E) != 2*a-1:
        raise RuntimeError("Geometry size/radius failure")
    geometry_checks.append({"scale": a, "size": len(E), "radius": 2*a-1})
    shifts = [(2*a*sx, 2*a*sy) for sx,sy in product((-1,1), repeat=2)]
    children = [{(x+sx,y+sy) for x,y in E} for sx,sy in shifts]
    if sum(map(len,children)) != len(set().union(*children)):
        raise RuntimeError("Children are not disjoint")
    E = set().union(*children)

max_A = (Q(0), None)
max_B = (Q(0), None)
for a in [2**k for k in range(11)]:
    for c in [2**k for k in range(11)]:
        Dc = 5*c*c+2*c
        Bc = Q(9*c*c,Dc)
        if a < c:
            Da = 5*a*a+2*a
            Ba = Q(9*a*a,Da)
            F = Q(4,9)*(1+(Ba-1)/a+Ba*(Bc-1)/c)
            if F >= Q(27,35):
                raise RuntimeError("Regime A bound failed")
            if F > max_A[0]: max_A = (F, [a,c])
        else:
            D = a*a*(5-4*(Bc-1)/c)+2*Bc*a
            lam = Q(25,9)-Q(6,9*c)+Q(8,9*c*c)
            if D/Bc != lam*a*a+2*a or not (Q(8,3)<=lam<=3):
                raise RuntimeError("Lambda identity/bounds failed")
            h = Bc/D
            F = Q(4,9)-Q(4,9*a)+4*a*h
            if F > Q(4,5):
                raise RuntimeError("Regime B bound failed")
            if F > max_B[0]: max_B = (F, [a,c])

result = {
    "status":"passed",
    "scope":"finite sanity checks accompanying the independently audited universal proof",
    "geometry_checks":geometry_checks,
    "scale_pairs_tested":121,
    "regime_A_largest_tested_bound":{"fraction":str(max_A[0]),"scales":max_A[1]},
    "regime_B_largest_tested_bound":{"fraction":str(max_B[0]),"scales":max_B[1]},
}
Path(__file__).with_name('three_deadline_constants_replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

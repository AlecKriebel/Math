#!/usr/bin/env python3
"""Independent exact local consistency checks; not a proof of the global theorem."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

edge_cases = 0
link_cases = 0
for weights in product(range(1,7), repeat=3):
    for baseheight in range(-12,13):
        for vertex in product((0,1), repeat=3):
            hv = baseheight + sum(m*x for m,x in zip(weights,vertex))
            if hv == 0:
                continue
            for numerators in ((1,0,0),(0,1,0),(0,0,1),(1,1,0),(2,1,3)):
                total = sum(numerators)
                ray = tuple(F(n,total*m) for n,m in zip(numerators,weights))
                target = tuple(F(x)-hv*d for x,d in zip(vertex,ray))
                assert F(baseheight) + sum(m*x for m,x in zip(weights,target)) == 0
                assert all(target[i] == vertex[i] for i,n in enumerate(numerators) if not n)
                link_cases += 1
        for axis in range(3):
            for face in product((0,1), repeat=2):
                start = [0,0,0]
                axes = [j for j in range(3) if j != axis]
                for j,x in zip(axes,face): start[j]=x
                end = start[:]; end[axis] = 1
                hs = baseheight + sum(m*x for m,x in zip(weights,start))
                he = hs + weights[axis]
                left = list(map(F,start)); left[axis] -= F(hs,weights[axis])
                right = list(map(F,end)); right[axis] -= F(he,weights[axis])
                assert left == right
                edge_cases += 1
result = {
    "status": "pass",
    "weights": "all ordered triples in {1,...,6}^3",
    "base_heights": [-12,12],
    "link_cases": link_cases,
    "edge_cases": edge_cases,
    "meaning": "Finite exact tests of coordinate formulas and edge compatibility only; global topology and quartic area bound require the mathematical proof."
}
Path(__file__).with_name('rectangle_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

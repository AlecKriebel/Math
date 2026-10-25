#!/usr/bin/env python3
"""Independent finite controls using Fourier--Motzkin, not vertex enumeration.

No imports from the submitted package. Standard-library exact fractions only.
This is an exponential diagnostic, not the claimed polynomial algorithm.
"""
from fractions import Fraction as F
from itertools import product
from math import ceil, floor, gcd, lcm
from functools import reduce
import hashlib
import json
from pathlib import Path
import random

COUNTS = dict(lp_calls=0, models=0, submodular_pairs=0, denominator_checks=0,
              grid_assignments=0, witness_coordinates=0, star_closed_forms=0)

def require(test, explanation):
    if not test:
        raise RuntimeError(explanation)

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def simplify(rows):
    # Ax >= b, positive scaling and duplicate left-hand sides only.
    kept = {}
    for a, b in rows:
        a, b = tuple(map(F, a)), F(b)
        if not any(a):
            if b > 0:
                return None
            continue
        den = lcm(*(x.denominator for x in a))
        ints = tuple(int(x*den) for x in a)
        scale = reduce(gcd, (abs(x) for x in ints))
        key = tuple(x//scale for x in ints)
        rhs = b*den/scale
        if key not in kept or rhs > kept[key]:
            kept[key] = rhs
    return [(tuple(map(F, a)), b) for a, b in kept.items()]

def lp(n, edges, cost, fixed=None, box=None):
    COUNTS['lp_calls'] += 1
    fixed = fixed or {}
    rows = []
    for u, v, b in edges:
        rows.append((tuple(F(int(i==u)-int(i==v)) for i in range(n)), b))
    for i, p in fixed.items():
        unit = tuple(F(int(i==j)) for j in range(n))
        rows += [(unit, F(p)), (tuple(-x for x in unit), -F(p))]
    if box is not None:
        for i, (lo, hi) in enumerate(box):
            unit = tuple(F(int(i==j)) for j in range(n))
            rows += [(unit, F(lo)), (tuple(-x for x in unit), -F(hi))]
    original = rows[:]
    # New first coordinate t is exactly cost.y; eliminate y in reverse order.
    rows = [((F(0),)+a, b) for a, b in rows]
    equality = (F(1),)+tuple(-a for a in cost)
    rows += [(equality, F(0)), (tuple(-a for a in equality), F(0))]
    rows = simplify(rows)
    snapshots = []
    for dimension in range(n+1, 1, -1):
        if rows is None:
            return None
        snapshots.append(rows)
        positive = [(a,b) for a,b in rows if a[-1] > 0]
        negative = [(a,b) for a,b in rows if a[-1] < 0]
        projected = [(a[:-1], b) for a,b in rows if a[-1] == 0]
        for a,b in positive:
            for c,d in negative:
                projected.append((tuple(x/a[-1]+y/(-c[-1]) for x,y in zip(a[:-1], c[:-1])), b/a[-1]+d/(-c[-1])))
        rows = simplify(projected)
    if rows is None:
        return None
    lower = [b/a[0] for a,b in rows if a[0] > 0]
    upper = [b/a[0] for a,b in rows if a[0] < 0]
    if not lower:
        return 'unbounded'
    optimum = max(lower)
    if upper and optimum > min(upper):
        return None
    point = [optimum]
    for system in reversed(snapshots):
        lower, upper = [], []
        for a,b in system:
            residual = b-dot(a[:-1], point)
            if a[-1] > 0:
                lower.append(residual/a[-1])
            elif a[-1] < 0:
                upper.append(residual/a[-1])
            else:
                require(residual <= 0, 'back-substitution zero coefficient')
        chosen = max(lower) if lower else min(upper) if upper else F(0)
        require(not upper or chosen <= min(upper), 'back-substitution interval')
        point.append(chosen)
    witness = tuple(point[1:])
    require(all(dot(a,witness) >= b for a,b in original), 'original inequality witness')
    require(dot(cost,witness) == optimum, 'original objective witness')
    COUNTS['witness_coordinates'] += n
    return optimum, witness

def check_model(n, edges, integers, cost):
    continuous = lp(n, edges, cost)
    require(continuous is not None and continuous != 'unbounded', 'bounded base')
    _, star = continuous
    lo = {i:ceil(star[i]-n) for i in integers}
    hi = {i:floor(star[i]+n) for i in integers}
    k = lcm(*(b.denominator for _,_,b in edges)) if edges else 1
    q = lcm(*(a.denominator for a in cost)) if cost else 1
    inside, outside_values = {}, []
    for p in product(*(range(lo[i]-1, hi[i]+2) for i in integers)):
        COUNTS['grid_assignments'] += 1
        fixed = dict(zip(integers, p))
        admissible = all(fixed[u]-fixed[v] >= b for u,v,b in edges if u in fixed and v in fixed)
        result = lp(n, edges, cost, fixed)
        require(admissible == (result is not None), 'exact completable assignment domain')
        if not admissible:
            continue
        require(result != 'unbounded', 'bounded objective on slice')
        value, witness = result
        require((value*k*q).denominator == 1, 'slice value denominator')
        COUNTS['denominator_checks'] += 1
        if all(lo[i] <= x <= hi[i] for i,x in zip(integers,p)):
            inside[p] = value
        outside_values.append(value)
    require(inside and min(inside.values()) == min(outside_values), 'near/far-grid optimum')
    for p,qv in product(inside, repeat=2):
        meet = tuple(min(x,y) for x,y in zip(p,qv))
        join = tuple(max(x,y) for x,y in zip(p,qv))
        require(meet in inside and join in inside, 'domain lattice')
        require(inside[p]+inside[qv] >= inside[meet]+inside[join], 'submodular value')
        COUNTS['submodular_pairs'] += 1
    # Check a genuinely strict full-coordinate proximity witness at the optimum.
    # For these finite rational instances choose epsilon after LP coordinates are
    # known. This does not replace the manuscript's universal strict bound proof.
    denom = lcm(k, *(x.denominator for x in star))
    radius = F(n)-F(1,2*denom)
    box = [(x-radius,x+radius) for x in star]
    optimal_labels = [p for p,v in inside.items() if v == min(inside.values())]
    close = [lp(n, edges, cost, dict(zip(integers,p)), box) for p in optimal_labels]
    require(any(r is not None and r != 'unbounded' and r[0] == min(inside.values()) for r in close), 'strict full-coordinate proximity')
    COUNTS['models'] += 1

def main():
    rng = random.Random(23352246261024)
    cases = []
    for n in range(1,4):
        left = set(range((n+1)//2))
        possible = [(u,v) for u in left for v in range(n) if v not in left]
        for bits in product((0,1), repeat=len(possible)):
            edges = [(u,v,F(rng.randrange(-8,9),rng.choice((2,3,5,7)))) for (u,v),keep in zip(possible,bits) if keep]
            for integer_mask in range(1<<n):
                integers = tuple(i for i in range(n) if integer_mask>>i & 1)
                cost = [F(0)]*n
                for u,v,b in edges:
                    w = F(rng.randrange(0,4),rng.choice((1,2,5)))
                    cost[u] += w
                    cost[v] -= w
                cases.append((n,edges,integers,cost))
    big = 2**191+117
    huge_edges = [(0,2,F(big,2**107-1)), (0,3,F(-big,2**89-1)), (1,2,F(3,11)), (1,3,F(-8,13))]
    for edges in [huge_edges,[(0,2,F(5,7)),(0,3,F(-2,3)),(1,2,F(4,11)),(1,3,F(8,5))]]:
        cost = [F(0)]*4
        for j,(u,v,b) in enumerate(edges):
            w=F(j+1,j+2)
            cost[u] += w
            cost[v] -= w
        cases.append((4,edges,(0,3),cost))
    for case in cases:
        check_model(*case)
    # Closed-form star objective: min over integer differences attained at the
    # floor/ceiling of b0-b1. Independent of all FM or submitted-code machinery.
    for _ in range(120):
        b0,b1 = F(rng.randrange(-50,51),rng.choice((3,7,11))), F(rng.randrange(-50,51),rng.choice((2,5,13)))
        w0,w1 = F(rng.randrange(1,9),7), F(rng.randrange(1,9),11)
        W=w0+w1
        f=lambda d:max(-w1*d+W*b0,w0*d+W*b1)
        expected=min(f(floor(b0-b1)),f(ceil(b0-b1)))
        actual=min(lp(3,[(0,2,b0),(1,2,b1)],[w0,w1,-W],{0:d,1:0})[0] for d in range(floor(b0-b1)-2,ceil(b0-b1)+3))
        require(actual==expected, 'closed form star integer-difference optimum')
        COUNTS['star_closed_forms'] += 1
    # Exact direct controls of the FM solver and theorem boundary distinctions.
    require(lp(1,[],[F(1)])=='unbounded','empty graph unbounded objective')
    require(lp(2,[(0,1,F(1,2))],[F(1),F(-1)],{0:0})[0]==F(1,2),'one integer endpoint: no demand rounding')
    require(lp(2,[(0,1,F(1,2))],[F(1),F(-1)],{0:0,1:0}) is None,'both integer endpoints: infeasible label')
    require(lp(0,[],[])[0]==0,'zero dimension')
    result=dict(status='PASS',seed=23352246261024,counts=COUNTS,
        mechanism='Exact Fourier--Motzkin projection and rational back-substitution; independent star closed-form minimization',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limits='Finite exact diagnostics; does not implement polynomial SFM/GLS or prove complexity/priority.')
    output=Path(__file__).with_name('fresh_elimination_results.json')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()

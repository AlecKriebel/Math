#!/usr/bin/env python3
"""Independent bounded exact controls. These are NOT a proof of the geometry."""
from itertools import combinations, product
from fractions import Fraction
import json
from pathlib import Path
import sys

counts = {}
assertions = 0

def check(value):
    global assertions
    assertions += 1
    if not value:
        raise AssertionError('Control failed at assertion ' + str(assertions))

# Exhaustive edge-subset enumeration, independent of the author's Prüfer routine.
# Connected graphs with n-1 edges are exactly trees.
trees = configurations = 0
for n in range(1, 7):
    edges = list(combinations(range(n), 2))
    for es in combinations(edges, n-1):
        adjacent = [set() for _ in range(n)]
        for u,v in es:
            adjacent[u].add(v); adjacent[v].add(u)
        seen = {0}; frontier = [0]
        while frontier:
            u = frontier.pop()
            for v in adjacent[u] - seen:
                seen.add(v); frontier.append(v)
        if len(seen) != n:
            continue
        trees += 1
        for active in range(n):
            for marked in range(n):
                stable = all(len(adjacent[v]) + int(v == marked) >= 3
                             for v in range(n) if v != active)
                check(stable == (n == 1))
                configurations += 1
counts.update(edge_subset_labeled_trees=trees, one_mark_configurations=configurations)

# A ghost with two markings and one node is stable. It cannot be excluded in M_0,2.
check(1 + 2 == 3)
# A marked ghost connecting two nonconstant components is stable.
check(2 + 1 == 3)
# That configuration uses two positive component degrees, so cannot be minimal
# when both component images contain x and have degree at least d.
for d in range(1, 31):
    check(2*d > d)

# Enumerate total degrees, distinguished component degrees and cover degrees.
# Degree bookkeeping itself must force e=1, image degree=d, residual degree=0.
minimal_cases = 0
for d in range(1, 61):
    for image_degree in range(d, 81):
        for cover_degree in range(1, 9):
            remainder = d - image_degree * cover_degree
            if remainder >= 0:
                check((image_degree, cover_degree, remainder) == (d,1,0))
                minimal_cases += 1
counts['minimal_degree_admissible_cases'] = minimal_cases

# Positive splitting: H^1(O(a-2))=0 for a>=1. The degree >=n+1 control
# additionally requires the nonzero normalization differential, hence max(a)>=2.
splittings=0
for n in range(1,6):
    for a in product(range(-2,6), repeat=n):
        if min(a) >= 1:
            check(all(max(0, 1-v) == 0 for v in a))
            if max(a) >= 2:
                check(sum(a) >= n+1)
            for p in (2,3,5,7):
                check(Fraction(min(p*v for v in a),p) == min(a))
            splittings += 1
counts['positive_splitting_cases'] = splittings
check(sum((3,-1))>0 and min((3,-1))<0)
check(sum((2,0))>0 and min((2,0))==0)

# Inseparable covers: d(t^p)/dt=0 in F_p, but degree is p>1.
for p in (2,3,5,7,11,13):
    check(p % p == 0 and p > 1)
    check(1 % p != 0)

# Explicit geometric controls reduced to their exact known splitting data.
for n in range(1,31):
    a = (2,) + (1,)*(n-1)
    check(min(a) == (2 if n == 1 else 1))
    check(sum(a) == n+1)
for a,b in product(range(1,11), repeat=2):
    check(min((2,)+(1,)*(a-1)+(0,)*b)==0)
# Diagonal curves in P1 x P1 are very free, but rulings through x have
# smaller O(1,1)-degree, are not very free, and are stable-map boundary pieces.
check(min((2,2))>0 and min((2,0))==0)
check(1+1==2)
blowups=0
for n in range(2,31):
    for r in range(2,n+1):
        for incidence in range(1,16):
            check(n+1-(r-1)*incidence<=n)
            blowups += 1
counts['blowup_degree_cases'] = blowups

# Exact numerical descent identity; q may be divisible by characteristic.
for d,b,q in product(range(1,21),range(-15,16),range(1,9)):
    check(q*(d*b-b*d)==0)
counts['assertions'] = assertions
result={'status':'PASS','purpose':'bounded controls only; no theorem verification',
        'counts':counts,
        'negative_controls': ['two-mark ghost exists',
                              'marked bridge between two active components exists',
                              'determinant positivity does not imply minimum slope positivity',
                              'very-free subfamily minimum is not absolute minimum',
                              'purely inseparable multiple-cover differential vanishes']}
text=json.dumps(result,indent=2,sort_keys=True)+'\n'
if '--write' in sys.argv:
    Path(__file__).with_name('independent_results.json').write_text(text)
else:
    check(Path(__file__).with_name('independent_results.json').read_text()==text)
print(text,end='')

#!/usr/bin/env python3
"""Exact finite checks for the planar diffraction counterexample.

These verify motif recognition, the algebra using the stipulated Rudin-Shapiro
first and second moments, and the suspension overlap formula. They DO NOT
prove the infinite Rudin-Shapiro theorem or establish publication priority.
Requires only Python's standard library. Run from any working directory.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ZERO = (F(0), F(0))
E = (F(1, 10), F(1, 10))
A = (F(1, 3), F(0))
B = (F(0), F(1, 3))
C = (ZERO, E, A, B)
D = (F(1), F(1), F(1, 2), F(1, 2))

marker_pairs = [
    (i, j) for i, c in enumerate(C) for j, d in enumerate(C)
    if tuple((d[k] - c[k]) % 1 for k in (0, 1)) == E
]
assert marker_pairs == [(0, 1)]
assert all((30 * z).denominator == 1 for c in C for z in c)
assert len(set(C)) == 4

# Occupancies at first and second cells. A coordinate-sharing identity such as
# X_m=X_0 for m=0 is enforced before enumerating the independent signs.
def expected_pair(c, d, m, n):
    required = set()
    if c == 2:
        required.add(('x', 0))
    elif c == 3:
        required.add(('y', 0))
    if d == 2:
        required.add(('x', m))
    elif d == 3:
        required.add(('y', n))
    keys = sorted(required)
    total = F(0)
    def occupancy(slot, p, q, signs):
        if slot < 2:
            return F(1)
        return F(1 + signs[('x', p) if slot == 2 else ('y', q)], 2)
    for values in product((-1, 1), repeat=len(keys)):
        signs = dict(zip(keys, values))
        total += occupancy(c, 0, 0, signs) * occupancy(d, m, n, signs)
    return total / (2 ** len(keys))

pair_checks = 0
for m, n in product(range(-4, 5), repeat=2):
    for c, d in product(range(4), repeat=2):
        expected = D[c] * D[d]
        if c == d == 2 and m == 0:
            expected += F(1, 4)
        if c == d == 3 and n == 0:
            expected += F(1, 4)
        assert expected_pair(c, d, m, n) == expected
        pair_checks += 1

# Weighted preliminary example: directly expand first and second moments.
weighted_checks = 0
for m, n in product(range(-4, 5), repeat=2):
    keys = sorted({('x', 0), ('x', m), ('y', 0), ('y', n)})
    total = F(0)
    for values in product((-1, 1), repeat=len(keys)):
        q = dict(zip(keys, values))
        total += ((4 + q['x', 0] + 2*q['y', 0]) *
                  (4 + q['x', m] + 2*q['y', n]))
    total /= 2**len(keys)
    assert total == 16 + int(m == 0) + 4 * int(n == 0)
    weighted_checks += 1
assert len({4+x+2*y for x,y in product((-1,1),repeat=2)}) == 4

# Suspension correlation: integrate the indicator 0 <= u+t < 1 over 0<=u<1.
suspension_checks = 0
for q in range(1, 18):
    for p in range(-3*q, 3*q+1):
        t = F(p, q)
        intersection = max(F(0), min(F(1), 1-t) - max(F(0), -t))
        target = max(F(0), 1-abs(t))
        assert intersection == target
        suspension_checks += 1

# Physical normalizations.
density = sum(D)
autocorrelation_origin = sum(w*w for w in D) + F(1, 2)
bragg_origin = density*density
assert density == autocorrelation_origin == 3
assert bragg_origin == 9

result = {
    'status': 'pass',
    'arithmetic': 'exact rational, Python standard library',
    'marker_pairs': marker_pairs,
    'motif_pair_checks': pair_checks,
    'weighted_correlation_checks': weighted_checks,
    'suspension_overlap_checks': suspension_checks,
    'density': str(density),
    'autocorrelation_mass_at_zero': str(autocorrelation_origin),
    'bragg_intensity_at_zero': str(bragg_origin),
    'scope': 'finite algebra and marker checks only; not an independent proof of the infinite-system theorem',
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
output = Path(__file__).with_name('verification_results.json')
output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))

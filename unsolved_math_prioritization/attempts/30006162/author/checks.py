#!/usr/bin/env python3
"""Finite supporting controls. This is not a GPP decision procedure."""
import itertools
import json
from fractions import Fraction as Q

counts = {}
def check(condition, section):
    counts[section] = counts.get(section, 0) + 1
    if not condition:
        raise RuntimeError('diagnostic failed: ' + section)

S3 = tuple(itertools.permutations(range(3)))
e = (0, 1, 2)
def mul(a, b):
    return tuple(a[b[i]] for i in range(3))
def inv(a):
    return tuple(a.index(i) for i in range(3))
def prod(A, B):
    return {mul(a, b) for a in A for b in B}
F = {(0, 1, 2), (1, 0, 2), (2, 0, 1)}
U = {(0, 1, 2), (0, 2, 1)}
check(e in U, 'factor_order')
check({inv(u) for u in U} == U, 'factor_order')
check(prod(U, U) == U, 'factor_order')
check(prod(F, U) == set(S3), 'factor_order')
check(len(prod(U, F)) == 4, 'factor_order')
check(prod(F, U) != prod(U, F), 'factor_order')
# This is a fixed-F diagnostic only: every subgroup of a finite group is
# presyndetic and co-precompact. It does not separate the two properties.

# Exact checks of the two-defect estimate used in Proposition 4.
# These finite functions need not be homogeneous. They check the inequality,
# not the existence of a nonzero homogeneous quasimorphism on a finite group.
for seed in range(1, 8):
    q = {g: Q(((seed + 2) * i * i + seed * i) % 17 - 8, seed + 1)
         for i, g in enumerate(S3)}
    q[e] = Q(0)
    defect = max(abs(q[mul(a, b)] - q[a] - q[b]) for a in S3 for b in S3)
    for f, u, h in itertools.product(S3, repeat=3):
        g = mul(mul(f, u), h)
        bound = abs(q[f]) + abs(q[u]) + abs(q[h]) + 2 * defect
        check(abs(q[g]) <= bound, 'two_defect_bound')

# Rational one-dimensional displacement controls for the triangle inequality
# in Proposition 2. Compactness and surface two-transitivity are proved in prose.
for delta in (Q(1, 7), Q(1, 3), Q(1), Q(5, 2), Q(9)):
    for j, k in itertools.product(range(-4, 5), repeat=2):
        dx, dy = delta * Q(j, 20), delta * Q(k, 20)
        check(abs((delta + dy) - dx) > delta / 2, 'separation_estimate')

# Integer torsion-to-Z and rational cohomology controls. Bounds in this finite
# loop are diagnostic; the universal torsion argument is 2a=0 => a=0 in Z.
for a in range(-30, 31):
    check((2 * a == 0) == (a == 0), 'torsion_to_Z')
# Cellular cochains in degrees 0,1,2: RP2 has d^0=0 and d^1=[2];
# S2 has C^1=0. Thus their integral H^1 is zero, not the RP2 H_1=Z/2.
check(Q(2) != 0, 'cohomology_controls')
check(1 - 1 + 1 == 1, 'cohomology_controls')
check(1 - 0 + 1 == 2, 'cohomology_controls')
check(2 > 0 and 1 > 0, 'cohomology_controls')

# Exact arithmetic for the homogeneity squeeze, without a false finite
# certification of an all-n statement.
for numerator in range(1, 14):
    for denominator in range(1, 10):
        a, C = Q(numerator, denominator), Q(37, 5)
        n = C // a + 1
        check(n * a > C, 'homogeneity_squeeze')

# Orientation degree: the antipodal map on S2 has degree (-1)^3=-1;
# exactly one of a lift and its antipodal companion has positive degree.
for degree in (-1, 1):
    check(sum(x == 1 for x in (degree, -degree)) == 1, 'lift_sign')
check((-1) ** 3 == -1, 'lift_sign')

result = {
    'problem_id': 30006162,
    'status': 'PASS',
    'exact_assertions': sum(counts.values()),
    'sections': counts,
    'fixed_factor_example': {'FU_cardinality': 6, 'UF_cardinality': 4},
    'scope': 'Finite exact supporting diagnostics only; no proof of GPP, Baire-category claims, cited theorems, or subgroup existence.',
}
print(json.dumps(result, sort_keys=True))

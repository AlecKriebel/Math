#!/usr/bin/env python3
"""Exact finite controls for an analytic proof; no numeric experiment proves it.
Run: python3 controls.py > validation.json
Only Python's standard library is required. All tested arithmetic is rational.
"""
import itertools
import json
from fractions import Fraction as F

counts = {}
def check(family, condition):
    if not condition:
        raise AssertionError(family)
    counts[family] = counts.get(family, 0) + 1

def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)

# A rational circle of circumference 1 models the exact grid covering lemma.
for n in range(1, 65):
    for excess in (F(0), F(1, 1000), F(1, 10)):
        length = F(1, n) + excess
        for numerator in range(-80, 81):
            left = F(numerator, 37)
            first_grid_point = F(ceil_fraction(n * left), n)
            check('all_rotation_grid_representatives',
                  left <= first_grid_point <= left + length)
            check('grid_point_has_integral_index',
                  (n * first_grid_point).denominator == 1)

# Direct rational denominator control with c standing for cos(t) in [-1,1].
# This certifies the algebra used in the compact-disk Poisson bound.
for denominator in range(2, 65):
    for numerator in range(denominator):
        r = F(numerator, denominator)
        for c in (F(-1), F(-1,2), F(0), F(1,2), F(1)):
            kernel = (1-r*r)/(1-2*r*c+r*r)
            check('compact_disk_kernel_bound',
                  F(0) < kernel <= (1+r)/(1-r))

# pi<22/7 gives a strict rationally checked upper bound pi/16<1/4.
pi_upper = F(22, 7)
m = 16
check('local_sign_constant', pi_upper/m < F(1,4))
check('local_sign_constant', 1-2*pi_upper/m > F(1,2))
for j in range(1, 101):
    exact_infinite_tail = F(1, 2**(j+3))
    finite_tail = 2*sum((F(1,2**(k+4)) for k in range(j+1,j+101)), F(0))
    check('geometric_tail', finite_tail < exact_infinite_tail <= F(1,16))
    check('oscillation_margin', F(1,2)-exact_infinite_tail > F(1,4))

# Exhaustive overwriting controls on four boundary atoms and four stages.
# Every subset mask at every stage is tested, including empty/full/overlap.
for masks in itertools.product(range(16), repeat=4):
    values = [0]*4
    history = [values.copy()]
    for j, mask in enumerate(masks, start=1):
        sign = (-1)**j
        old = values.copy()
        values = [sign if mask & (1<<atom) else old[atom] for atom in range(4)]
        for atom in range(4):
            indicator = int(bool(mask & (1<<atom)))
            check('overwrite_support', abs(values[atom]-old[atom]) <= 2*indicator)
            check('real_boundary_range', values[atom] in (-1,0,1))
            if indicator:
                check('latest_overwrite_sign', values[atom] == sign)
        history.append(values.copy())
    for atom in range(4):
        changes = sum(abs(history[k+1][atom]-history[k][atom]) for k in range(4))
        check('overwrite_telescoping', abs(values[atom]) <= changes)

# Affine normalization preserves strict positivity and an oscillation gap.
for i in range(-100,101):
    h = F(i,100)
    v = (h+2)/4
    check('positive_affine_normalization', F(1,4) <= v <= F(3,4))
check('positive_oscillation_gap', (F(1,4)+2)/4 == F(9,16))
check('positive_oscillation_gap', (-F(1,4)+2)/4 == F(7,16))
check('positive_oscillation_gap', F(9,16)-F(7,16) == F(1,8))

print(json.dumps({
    'result': 'PASS',
    'arithmetic': 'exact fractions and integers; Python standard library',
    'checks': counts,
    'total_assertions': sum(counts.values()),
    'limits': [
        'Finite controls are regression checks, not a proof for every path.',
        'The analytic proof supplies arbitrary-curve selection, all rotations, and infinite convergence.',
        'No floating-point quadrature, sampled path, or numerical limit is used to certify the theorem.'
    ]
}, indent=2, sort_keys=True))

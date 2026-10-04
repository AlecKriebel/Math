#!/usr/bin/env python3
"""Reproducible arithmetic audit of a literature specialization, not proof search."""
from fractions import Fraction
import json
from math import comb

# Coefficient check valid for every n: C(n,2)+C(n,3)=(n^3-n)/6.
# Expand C(n,2)=(n^2-n)/2 and C(n,3)=(n^3-3n^2+2n)/6.
coefficients = {3: Fraction(1, 6),
                2: Fraction(1, 2)-Fraction(3, 6),
                1: -Fraction(1, 2)+Fraction(2, 6),
                0: Fraction(0)}
assert coefficients == {3:Fraction(1,6), 2:0, 1:Fraction(-1,6), 0:0}
cases = []
for n in range(101):
    binomial = comb(n, 2) if n >= 2 else 0
    binomial += comb(n, 3) if n >= 3 else 0
    bound = Fraction(binomial, 4)
    target = Fraction(n*(n*n-1), 24)
    assert bound == target
    if n <= 12:
        cases.append({'n':n, 'source_bound_after_division_by_4':str(bound),
                      'target_floor':target.numerator//target.denominator})
print(json.dumps({'universal_coefficient_identity_checked':True,
                  'finite_boundary_checks':101,
                  'assumptions_from_source_not_computationally_proved':
                  ['universal source inequality |vt3| <= C(n,2)+C(n,3)',
                   'source normalization vt3=4v3', 'v3 integer valued'],
                  'cases':cases}, indent=2))

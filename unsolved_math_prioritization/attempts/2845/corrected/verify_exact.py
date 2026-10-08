#!/usr/bin/env python3
"""Exact algebra checks for REPORT.md; not a proof of K3 Problem 3.47."""
from fractions import Fraction as F
import json


def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def power(a, n):
    r = [[F(1), F(0)], [F(0), F(1)]]
    for _ in range(n):
        r = mul(r, a)
    return r


def det(a):
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]


def trace(a):
    return a[0][0]+a[1][1]


def q(a):
    return [[F(0), -1/a], [a, F(0)]]


def check(condition, message):
    # Deliberately not Python assert: checks also run under python -O.
    if not condition:
        raise RuntimeError(message)


def divisors(n):
    return [d for d in range(1, n+1) if n % d == 0]


def is_power_two(n):
    return n > 0 and n & (n-1) == 0


def lef(n, positive, negative):
    return sum(d*(-positive.get(d, 0) + (1 if (n//d) % 2 else -1)*negative.get(d, 0)) for d in divisors(n))


def run():
    p = mul(q(F(1)), q(F(2)))
    check(p == [[F(-2), F(0)], [F(0), F(-1, 2)]], 'quarter-turn product')
    check(det(p) == 1 and trace(p) == F(-5, 2), 'symplectic negative hyperbolic endpoint')
    identity = [[F(1), F(0)], [F(0), F(1)]]
    orbit_indices = []
    for m in range(1, 65):
        pm = power(p, m)
        ip = [[identity[i][j]-pm[i][j] for j in range(2)] for i in range(2)]
        d = det(ip)
        sign = 1 if d > 0 else -1 if d < 0 else 0
        check(d != 0, 'hyperbolic iterates remain nondegenerate')
        check(sign == (1 if m % 2 else -1), 'negative hyperbolic index alternation')
        orbit_indices.append(sign)
    b = {d: 1 for d in range(1, 513) if is_power_two(d)}
    for n in range(1, 513):
        check(lef(n, {}, b) == 1, 'all-iterate formal Lefschetz model')
    # A non-minimal dyadic model tests the recurrence with nonzero a values.
    a2 = {2**k: (k*k+3) % 5 for k in range(10)}
    b2 = {1: a2[1]+1}
    for k in range(1, 10):
        b2[2**k] = a2[2**k] + b2[2**(k-1)]
    for k in range(10):
        check(lef(2**k, a2, b2) == 1, 'dyadic recurrence')
    for k in range(2, 513):
        check(3*k < 4*k-1, 'index-three iterate misses stronger threshold')
    # Trace thresholds checked at exact matrices of all relevant types.
    controls = [
        ('elliptic', [[F(0),F(-1)],[F(1),F(0)]], 0),
        ('positive_parabolic', [[F(1),F(1)],[F(0),F(1)]], 2),
        ('negative_parabolic', [[F(-1),F(1)],[F(0),F(-1)]], -2),
        ('positive_hyperbolic', [[F(2),F(0)],[F(0),F(1,2)]], F(5,2)),
        ('negative_hyperbolic', p, F(-5,2)),
    ]
    for name, matrix, t in controls:
        check(det(matrix) == 1 and trace(matrix) == t, name)
    return {
        'status': 'pass',
        'arithmetic': 'fractions.Fraction, exact',
        'negative_hyperbolic_product': [['-2','0'],['0','-1/2']],
        'negative_hyperbolic_iterates_checked': 64,
        'formal_lefschetz_identities_checked_n': [1, 512],
        'dyadic_recurrences_checked_k': [0, 9],
        'index_gap_checks_k': [2, 512],
        'trace_type_controls': len(controls),
        'limits': [
            'No realization of the formal cycle model is asserted.',
            'No convex hypersurface realization of the linear system is asserted.',
            'No infinite-dimensional theorem or universal ellipticity claim is proved by this script.',
            'The report supplies the proofs for all n and all k; finite tests only check formulas.'
        ]
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

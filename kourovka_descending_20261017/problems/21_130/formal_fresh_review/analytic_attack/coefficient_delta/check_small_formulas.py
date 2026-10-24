#!/usr/bin/env python3
"""Small independent tests of new compressed formulas by the full grid identity.

Only writes when caller redirects stdout; no coefficient-data files are changed.
"""
from fractions import Fraction
from itertools import product
from math import factorial
from pathlib import Path
import json

SOURCE = Path(__file__).resolve().parents[3] / 'algebraic'

def load_function(filename, function):
    scope = {'__name__': 'audit_dependency'}
    exec(compile((SOURCE / filename).read_text(), str(SOURCE / filename), 'exec'), scope)
    return scope[function]

fixed = load_function('fixed_zero_coefficients.py', 'coefficients')
low = load_function('low_exponent_coefficients.py', 'probe')

def q_value(a):
    n = len(a)
    v = 1
    for i in range(n):
        for j in range(i + 1, n):
            v *= a[j] - a[i]
    if not v:
        return 0
    for i in range(n):
        edge_i = {i, (i + 1) % n}
        for j in range(i + 1, n):
            if edge_i.isdisjoint({j, (j + 1) % n}):
                v *= a[j] + a[(j + 1) % n] - a[i] - a[(i + 1) % n]
    return v

def coefficient_general_grid(t):
    total = Fraction(0)
    checked = contributing = 0
    for a in product(*(range(u + 1) for u in t)):
        checked += 1
        value = q_value(a)
        if not value:
            continue
        contributing += 1
        denominator = 1
        for ai, ti in zip(a, t):
            denominator *= (-1) ** (ti - ai) * factorial(ai) * factorial(ti - ai)
        total += Fraction(value, denominator)
    assert total.denominator == 1
    return {'coefficient': total.numerator, 'grid_tuples': checked,
            'nonzero_grid_values': contributing}

results = []
for n in range(3, 7):
    fixed_values = fixed(n)['coefficients']
    for j in range(1, n):
        t = [n-1] * n
        t[0] = 0
        t[j] -= 1
        direct = coefficient_general_grid(t)
        assert direct['coefficient'] == fixed_values[j-1], (n, t, direct, fixed_values[j-1])
        results.append({'family': 'fixed_zero', 'n': n, 'exponents': t,
                        'compressed_coefficient': fixed_values[j-1], **direct})
    low_values = {tuple(w['exponents']): w['coefficient']
                  for w in low(n)['coefficients']}
    # All small cases include repeated/distinct deficits and zero/nonzero signs.
    for j, k in ((j, k) for j in range(1, n) for k in range(j, n)):
        t = [n-1] * n
        t[0] = 1
        t[j] -= 1
        t[k] -= 1
        direct = coefficient_general_grid(t)
        compressed = low_values[tuple(t)]
        assert direct['coefficient'] == compressed, (n, t, direct, compressed)
        results.append({'family': 'low_exponent', 'n': n, 'exponents': t,
                        'compressed_coefficient': compressed, **direct})
print(json.dumps({'status': 'all_equal', 'checked_coefficients': len(results),
                  'results': results}, indent=2))

#!/usr/bin/env python3
"""Recheck the finite characteristic-two coefficient behind Karpenko (2023), Thm 4.1.

This checks a polynomial calculation only, not the referenced geometric theorems.
No source bodies or downloaded data are inputs. Variables are x,x5,x6,x7,x8.
Run from this folder: python3 CHECK_MOD2.py
"""
import json
from pathlib import Path

ZERO = (0, 0, 0, 0, 0)

def add(a, b):
    return a ^ b

def mul(a, b):
    out = set()
    for s in a:
        for t in b:
            u = tuple(i + j for i, j in zip(s, t))
            if u in out:
                out.remove(u)
            else:
                out.add(u)
    return out

def var(i):
    e = list(ZERO)
    e[i] = 1
    return {tuple(e)}

def square(a):
    return {tuple(2 * i for i in t) for t in a}

def substitute_x(a, i):
    out = set()
    for t in a:
        u = list(t)
        u[i] += u[0]
        u[0] = 0
        u = tuple(u)
        if u in out:
            out.remove(u)
        else:
            out.add(u)
    return out

# Mechanism A: multiply all sixteen linear factors independently.
direct = {ZERO}
for mask in range(16):
    factor = var(0)
    for j in range(4):
        if mask & (1 << j):
            factor = add(factor, var(j + 1))
    direct = mul(direct, factor)

# Mechanism B: additive-polynomial recurrence, with variables adjoined one at a time.
recursive = var(0)
for i in (4, 3, 2, 1):
    recursive = add(square(recursive), mul(recursive, substitute_x(recursive, i)))
if direct != recursive:
    raise RuntimeError('Independent polynomial mechanisms disagree')
if (8, 0, 0, 4, 4) not in direct:
    raise RuntimeError('Expected decisive coefficient is not one')
if {a[0] for a in direct} != {1, 2, 4, 8, 16}:
    raise RuntimeError('The polynomial is not linearized in x as expected')

# In mod-2 CH(flag), x^8 becomes e8; x_i^8=0. For x^8 terms the remaining
# nonzero exponents are at most four and obey a_i<i (i=5,6,7,8), so no
# reduction can cancel the decisive basis coefficient x7^4 x8^4 e8.
coefficient = sorted(t[1:] for t in direct if t[0] == 8)
surviving = [t for t in coefficient if all(i < 8 for i in t)]
if not all(all(a < i for a, i in zip(t, (5, 6, 7, 8))) for t in surviving):
    raise RuntimeError('A surviving term is outside the stated basis bounds')
result = {
    'scope': 'finite polynomial coefficient, not a standalone geometry proof',
    'field': 'F2',
    'variables': ['x', 'x5', 'x6', 'x7', 'x8'],
    'direct_and_recursive_products_equal': True,
    'monomial_count': len(direct),
    'x_degrees': sorted({t[0] for t in direct}),
    'coefficient_x8_x7_4_x8_4': 1,
    'x8_coefficient_monomials_before_xi8_vanishing': coefficient,
    'x8_coefficient_survivors_in_flag_basis': surviving,
    'decisive_basis_term': 'x7^4*x8^4*e8',
    'decisive_term_nonzero_in_stated_basis': True,
}
Path('CHECK_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('direct_and_recursive_products_equal', 'monomial_count', 'coefficient_x8_x7_4_x8_4', 'decisive_term_nonzero_in_stated_basis')}, indent=2))

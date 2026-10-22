#!/usr/bin/env python3
"""Exact finite checks for the partial note; not an analytic proof checker.
Python 3 standard library only. Run: python3 verify.py
"""
from fractions import Fraction as F
import json

checks = []

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

# Sparse rational polynomials in three formal variables, with no evaluation.
def const(c):
    c = F(c)
    return {} if c == 0 else {(0, 0, 0): c}

def var(k):
    e = [0, 0, 0]
    e[k] = 1
    return {tuple(e): F(1)}

def add(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return {e: c for e, c in out.items() if c}

def mul(*ps):
    out = const(1)
    for p in ps:
        q = {}
        for e, c in out.items():
            for f, d in p.items():
                g = tuple(e[i] + f[i] for i in range(3))
                q[g] = q.get(g, F(0)) + c*d
        out = {e: c for e, c in q.items() if c}
    return out

def neg(p):
    return mul(const(-1), p)

def power(p, n):
    out = const(1)
    for _ in range(n):
        out = mul(out, p)
    return out

one = const(1)
z, a, w = (var(i) for i in range(3))
plus = add(one, z)
minus = add(one, neg(z))
num = mul(const(2), z, plus)
check('Cayley composition numerator',
      add(power(plus, 2), neg(mul(plus, minus))) == num)
check('exceptional half-slope factorization',
      add(num, mul(const(F(1, 2)), plus, power(minus, 2)))
      == mul(const(F(1, 2)), power(plus, 3)))
check('target minus-a factorization',
      add(num, mul(a, plus, power(minus, 2)))
      == mul(plus, add(mul(a, power(z, 2)),
                       mul(add(const(2), mul(const(-2), a)), z), a)))
# z now denotes the formal half-plane variable t.
check('half-plane cubic clearing denominator',
      add(mul(add(power(z, 2), neg(z), neg(w)), plus),
          mul(a, add(z, const(-1))))
      == add(power(z, 3), mul(add(a, neg(w), const(-1)), z), neg(a), neg(w)))
# z now denotes y, a denotes the real cusp parameter s.
check('cusp repeated-root cubic identity',
      mul(power(add(z, neg(a)), 2), add(z, mul(const(2), a)))
      == add(power(z, 3), mul(const(-3), power(a, 2), z),
             mul(const(2), power(a, 3))))
# z now denotes the real part of t; a denotes the imaginary part.
check('Cayley half-plane modulus difference',
      add(power(add(z, one), 2), power(a, 2),
          neg(power(add(z, const(-1)), 2)), neg(power(a, 2)))
      == mul(const(4), z))
check('small-cluster contour lies in half-plane', F(1, 2)-F(3, 8) > 0)
check('small-cluster contour contains both roots', F(1, 4) < F(3, 8))
check('small-cluster boundary margin', F(3, 8)**2-F(1, 4)**2 == F(5, 64))
check('large-cluster contour lies in half-plane', F(1, 2)-F(1, 8) > 0)
check('large-cluster boundary margin', F(1, 8)*(2*F(1, 4)-F(1, 8)) == F(3, 64))
check('chosen uniform margin below other margin', F(3, 64) < F(5, 64))
check('critical disk preimage', (F(1, 2)-1)/(F(1, 2)+1) == F(-1, 3))
check('critical value', F(1, 2)**2-F(1, 2) == F(-1, 4))

# Exact boundary, exterior and interior controls. These are finite sanity checks,
# not computational substitutes for the all-parameter classification proof.
for k in range(-20, 21):
    s = F(k, 4)
    alpha = (1+3*s*s)/2
    beta = s**3
    p = 2*alpha-1
    check(f'cusp boundary {k}', p**3-27*beta**2 == 0)
    check(f'cusp repeated roots sum {k}', s+s-2*s == 0)
    check(f'cusp repeated roots product {k}', s*s*(-2*s) == -2*beta)
    check(f'cusp exterior {k}', (2*(alpha-F(1, 10))-1)**3-27*beta**2 < 0)
    check(f'cusp interior {k}', (2*(alpha+F(1, 10))-1)**3-27*beta**2 > 0)

examples = [
    ('zero', F(0), F(0), False),
    ('small positive', F(1, 100), F(0), False),
    ('negative', F(-10), F(0), False),
    ('imaginary', F(0), F(10), False),
    ('endpoint', F(1, 2), F(0), True),
    ('positive ray', F(1), F(0), True),
    ('upper boundary', F(2), F(1), True),
    ('lower boundary', F(2), F(-1), True),
    ('outside cusp', F(2), F(2), False),
]
for name, alpha, beta, omitted in examples:
    check('slope classification '+name,
          ((2*alpha-1)**3 >= 27*beta**2) == omitted)

for j in range(-15, 16):
    for k in range(-15, 16):
        alpha, beta = F(j, 32), F(k, 32)
        if alpha*alpha+beta*beta < F(1, 4):
            check(f'open half-radius disk {j},{k}', (2*alpha-1)**3 < 27*beta**2)

result = {
    'status': 'PASS',
    'exact_assertions': len(checks),
    'polynomial_identities': 6,
    'uniform_bounded_perturbation_margin': '3/64 (strict norm bound)',
    'bad_affine_locus': '(2*Re(a)-1)^3 >= 27*Im(a)^2',
    'omitted_value_on_bad_locus': '-conjugate(a)',
    'scope': 'Exact finite algebra and rational controls only; not formal verification of complex analysis or the original universal problem.'
}
print(json.dumps(result, indent=2, sort_keys=True))

#!/usr/bin/env python3
"""Small exact certificates for the restricted Macaulay-quartic obstructions.

This uses sparse polynomial arithmetic over fractions.Fraction, no CAS or
network. The geometric and all-ideal arguments are in PARTIAL_RESULTS.md;
finite checks here do not decide the full set-theoretic CM question.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json

checks = 0


def clean(p):
    return {e: F(c) for e, c in p.items() if c}


def plus(a, b):
    c = dict(a)
    for e, v in b.items():
        c[e] = c.get(e, F(0)) + v
    return clean(c)


def times(a, b):
    c = {}
    for e, u in a.items():
        for f, v in b.items():
            g = tuple(x+y for x, y in zip(e, f))
            c[g] = c.get(g, F(0)) + u*v
    return clean(c)


def scale(c, p):
    return clean({e: c*v for e, v in p.items()})


def minus(a, b):
    return plus(a, scale(-1, b))


def mono(exponents, c=1):
    return clean({tuple(exponents): F(c)})


def power(p, n):
    if not p:
        return {} if n else {(0, 0): F(1)}
    unit = mono([0]*len(next(iter(p))))
    for _ in range(n):
        unit = times(unit, p)
    return unit


def variables(n):
    return [mono([int(j == i) for j in range(n)]) for i in range(n)]


def total(ps):
    a = {}
    for p in ps:
        a = plus(a, p)
    return a


def assert_equal(a, b):
    global checks
    assert a == b, (a, b)
    checks += 1


def vadd(a, b):
    return [plus(x, y) for x, y in zip(a, b)]


def vmul(p, a):
    return [times(p, x) for x in a]


def vsub(a, b):
    return [minus(x, y) for x, y in zip(a, b)]


def det2(a, b, c, d):
    return minus(times(a, d), times(b, c))


def derivative(p, j):
    out = {}
    for e, c in p.items():
        if e[j]:
            f = list(e)
            f[j] -= 1
            out[tuple(f)] = c*e[j]
    return clean(out)


def rank(columns):
    a = [[F(x) for x in row] for row in zip(*columns)]
    r = 0
    for j in range(len(columns)):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        d = a[r][j]
        a[r] = [x/d for x in a[r]]
        for i in range(r+1, len(a)):
            d = a[i][j]
            a[i] = [x-d*y for x, y in zip(a[i], a[r])]
        r += 1
    return r


# Missing monomial and its annihilator.
s, t = variables(2)
w0, x0, y0, z0 = [mono(e) for e in [(4, 0), (3, 1), (1, 3), (0, 4)]]
u = mono((2, 2))
assert_equal(power(u, 2), times(w0, z0))
assert_equal(power(u, 3), times(power(x0, 2), z0))
for left, right in zip([w0, x0, y0, z0], [power(x0, 2), times(w0, y0), times(x0, z0), power(y0, 2)]):
    assert_equal(times(left, u), right)
assert_equal(times(w0, z0), times(x0, y0))
assert_equal(power(x0, 3), times(power(w0, 2), y0))
assert_equal(power(y0, 3), times(x0, power(z0, 2)))
assert_equal(times(w0, power(y0, 2)), times(power(x0, 2), z0))

reachable = {0}
semigroup_checks = []
for degree in range(1, 21):
    reachable = {a+b for a in reachable for b in [0, 1, 3, 4]}
    expected = {0, 1, 3, 4} if degree == 1 else set(range(4*degree+1))
    assert_equal(reachable, expected)
    semigroup_checks.append({"degree": degree, "dimension": len(reachable)})

# Explicit conormal frame, with no reliance on a normal-bundle classification.
f = [w0, x0, y0, z0]
jac = [[derivative(a, i) for a in f] for i in range(2)]
v1 = [mono((0, 3), 2), mono((1, 2), -3), mono((3, 0)), {}]
v2 = [{}, mono((0, 3)), mono((2, 1), -3), mono((3, 0), 2)]
for v in [v1, v2]:
    for row in jac:
        assert_equal(total(times(a, b) for a, b in zip(row, v)), {})
assert_equal(det2(v1[0], v2[0], v1[1], v2[1]), mono((0, 6), 2))
assert_equal(det2(v1[2], v2[2], v1[3], v2[3]), mono((6, 0), 2))
assert_equal(det2(jac[0][0], jac[0][1], jac[1][0], jac[1][1]), mono((6, 0), 4))
assert_equal(det2(jac[0][2], jac[0][3], jac[1][2], jac[1][3]), mono((0, 6), 4))

# The linked skew-line ideal's Koszul H_1 has an explicit nonzero socle.
w, x, y, z = variables(4)
g = [times(w, y), times(w, z), times(x, y), times(x, z)]
boundaries = {}
for i, j in combinations(range(4), 2):
    v = [{} for _ in range(4)]
    v[i], v[j] = scale(-1, g[j]), g[i]
    boundaries[(i+1, j+1)] = v
c = [scale(-1, times(x, z)), times(x, y), {}, {}]
assert_equal(total(times(a, b) for a, b in zip(g, c)), {})
d = boundaries
certs = [vmul(x, d[1, 2]),
         vsub(vsub(vmul(x, d[1, 4]), vmul(w, d[3, 4])), vmul(x, d[2, 3])),
         vsub(vmul(z, d[1, 3]), vmul(y, d[2, 3])),
         vsub(vmul(z, d[1, 4]), vmul(y, d[2, 4]))]
for variable, cert in zip([w, x, y, z], certs):
    assert_equal(vmul(variable, c), cert)
monomials = sorted({e for v in list(d.values())+[c] for p in v for e in p})
def flatten(v):
    return [p.get(e, F(0)) for p in v for e in monomials]
cols = [flatten(v) for v in d.values()]
assert_equal(rank(cols), 6)
assert_equal(rank(cols+[flatten(c)]), 7)

# Exact Segre factorization for the linkage description.
a, b, cc, dd = variables(4)
ww, xx, yy, zz = times(a, cc), times(a, dd), times(b, cc), times(b, dd)
assert_equal(minus(times(ww, zz), times(xx, yy)), {})
assert_equal(minus(times(ww, power(yy, 2)), times(power(xx, 2), zz)),
             times(times(a, b), minus(times(b, power(cc, 3)), times(a, power(dd, 3)))))

# Regression checks of the elementary cohomology formulas used in the proof.
h0 = lambda d: max(d+1, 0)
h1 = lambda d: max(-d-1, 0)
for r in range(1, 33):
    assert_equal(h0(0)*h1(-2*r)+h1(0)*h0(-2*r), 2*r-1)
for ell in range(-7, 21):
    assert_equal(h1(ell+8), 0)
    assert 9+h0(ell+8) >= 11 > comb(5, 3)
    checks += 1

receipt = {"status": "passed", "arithmetic": "fractions.Fraction and integer arithmetic",
           "assertions": checks, "scope": "Restricted-obstruction polynomial certificates, not a full solution",
           "koszul_boundary_rank": 6, "with_socle_cycle_rank": 7,
           "semigroup": semigroup_checks,
           "conormal_frame": "two cubic columns; Jacobian product zero; endpoint minors 2*s^6,2*t^6",
           "double_structure_bound": "h^0(O_Y(2)) >= 11 > 10",
           "quadric_thickening_defect": "h^1(I_(rC)(r)) = 2*r-1 (formula proved separately)"}
Path(__file__).with_name('verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'semigroup'}, indent=2))

#!/usr/bin/env python3
"""Discovery-only Bernstein search for the adjacent-mass merge inequality.

This script deliberately uses binary floating point.  Its purpose is to find a
small rational certificate format; it is not a verifier.
"""

from __future__ import annotations

from collections import defaultdict
from math import comb, factorial, pi

import numpy as np


# Sparse polynomials in (s,t,r,u).
NVAR = 4
ZERO = (0,) * NVAR


def clean(p, tol=1e-13):
    return {m: c for m, c in p.items() if abs(c) > tol}


def add(p, q, scale=1.0):
    out = defaultdict(float)
    out.update(p)
    for m, c in q.items():
        out[m] += scale * c
    return clean(out)


def scale(p, a):
    return clean({m: a * c for m, c in p.items()})


def mul(p, q):
    out = defaultdict(float)
    for a, ca in p.items():
        for b, cb in q.items():
            out[tuple(a[i] + b[i] for i in range(NVAR))] += ca * cb
    return clean(out)


def power(p, n):
    out = {ZERO: 1.0}
    base = p
    while n:
        if n & 1:
            out = mul(out, base)
        n >>= 1
        if n:
            base = mul(base, base)
    return out


one = {ZERO: 1.0}
s = {(1, 0, 0, 0): 1.0}
t = {(0, 1, 0, 0): 1.0}
r = {(0, 0, 1, 0): 1.0}
u = {(0, 0, 0, 1): 1.0}


def sub(p, q):
    return add(p, q, -1.0)


def compose(coeffs, x):
    out = {}
    xp = one
    for c in coeffs:
        out = add(out, scale(xp, c))
        xp = mul(xp, x)
    return out


def f_coeffs(degree=18):
    """Maclaurin polynomial for F using the machine value of pi."""
    k = 2.0 * pi / 3.0
    out = np.zeros(degree + 1)
    out[0] = 0.25
    for harmonic, weight in ((k, 3.0 / 8.0), (2.0 * k, 1.0 / 8.0)):
        for j in range(degree // 2 + 1):
            out[2 * j] += weight * ((-1.0) ** j) * harmonic ** (2 * j) / factorial(2 * j)
    return out


FC = f_coeffs()


def F(x):
    return compose(FC, x)


def P(x):
    return add(add(F(x), F(sub(one, x))), {ZERO: -0.75})


x = mul(s, t)
y = sub(s, x)
a = mul(r, u)
c = sub(r, a)


def Phi(X):
    Y = sub(s, X)
    return add(
        add(
            add(F(add(X, r)), F(add(Y, r))),
            add(F(sub(sub(one, X), a)), F(sub(sub(one, Y), c))),
        ),
        add(P(X), P(Y)),
        -1.0,
    )


D = sub(add(mul(sub(one, t), Phi({})), mul(t, Phi(s))), Phi(x))


def divide_monomial(p, powers):
    out = {}
    for m, coeff in p.items():
        if any(m[i] < powers[i] for i in range(NVAR)):
            if abs(coeff) > 5e-9:
                raise AssertionError(("nondivisible monomial", m, coeff))
            continue
        out[tuple(m[i] - powers[i] for i in range(NVAR))] = coeff
    return clean(out)


def divide_one_minus_t(p):
    """Divide by 1-t, grouping the other exponents."""
    groups = defaultdict(dict)
    for m, coeff in p.items():
        groups[(m[0], m[2], m[3])][m[1]] = coeff
    out = {}
    max_residual = 0.0
    for fixed, cs in groups.items():
        degree = max(cs)
        cumulative = 0.0
        for j in range(degree + 1):
            cumulative += cs.get(j, 0.0)
            if j < degree:
                out[(fixed[0], j, fixed[1], fixed[2])] = cumulative
        max_residual = max(max_residual, abs(cumulative))
    print("division residual", max_residual)
    return clean(out, 1e-10)


# D/(s^2 t(1-t)r).
Q = divide_one_minus_t(divide_monomial(D, (2, 1, 1, 0)))
Q = add(Q, {ZERO: -2.0})  # Search for Q-2 >= 0.


def substitute_r_one_minus_s_v(p):
    """Return p(s,t,(1-s)v,u), now using variable 2 as v."""
    out = {}
    rv = mul(sub(one, s), r)
    for m, coeff in p.items():
        term = {ZERO: coeff}
        term = mul(term, power(s, m[0]))
        term = mul(term, power(t, m[1]))
        term = mul(term, power(rv, m[2]))
        term = mul(term, power(u, m[3]))
        out = add(out, term)
    return clean(out)


QCUBE = substitute_r_one_minus_s_v(Q)
DEG = tuple(max(m[i] for m in QCUBE) for i in range(NVAR))
print("terms", len(QCUBE), "multidegree", DEG)


def power_to_bernstein(p, degrees):
    """Tensor-product power to Bernstein coefficients on [0,1]^4."""
    shape = tuple(d + 1 for d in degrees)
    coeff = np.zeros(shape)
    for m, value in p.items():
        coeff[m] = value
    for axis, degree in enumerate(degrees):
        transform = np.zeros((degree + 1, degree + 1))
        for i in range(degree + 1):
            for j in range(i + 1):
                transform[i, j] = comb(i, j) / comb(degree, j)
        coeff = np.moveaxis(coeff, axis, 0)
        coeff = np.tensordot(transform, coeff, axes=(1, 0))
        coeff = np.moveaxis(coeff, 0, axis)
    return coeff


B = power_to_bernstein(QCUBE, DEG)
print("whole-cube Bernstein range", float(B.min()), float(B.max()))
print("power samples", [
    sum(c * np.prod(np.asarray(point) ** np.asarray(m)) for m, c in QCUBE.items())
    for point in (
        (0.2, 0.3, 0.4, 0.5),
        (0.9, 0.9, 0.1, 1.0),
        (1.0, 1.0, 0.0, 1.0),
    )
])

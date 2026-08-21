#!/usr/bin/env python3
"""Derive E6 contact kernel for h=pq, R=pq(Ap+Bq)."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, B = sp.symbols("A B")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


P, Q = p**3 * q, p * q**3
R = p * q * (A * p + B * q)
N1 = (5 * p**2, -q**2, 3 * A * p)
N2 = (-p**2, 5 * q**2, 3 * B * q)
N = tuple(sp.expand(s * N1[i] + t * N2[i]) for i in range(3))
H4 = sp.Matrix([P, Q, 0])
H3 = sp.Matrix([r * N[0], r * N[1], R])
H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * N[2]])
weighted = sp.Poly(
    sp.expand(
        (
            z * H2.jacobian(variables)
            + z**2 * H3.jacobian(variables)
            + z**3 * H4.jacobian(variables)
        ).det()
    ),
    z,
)
assert sp.expand(weighted.coeff_monomial(z**7)) == 0
E6r = sp.Poly(
    sp.expand(weighted.coeff_monomial(z**6)), r
).coeff_monomial(r)
lifted = []
for equation in coefficients(E6r, 5):
    poly = sp.Poly(equation, s, t)
    lifted.append(
        sp.expand(
            poly.coeff_monomial(s**2) * X
            + poly.coeff_monomial(s * t) * Y
            + poly.coeff_monomial(t**2) * Z
            + poly.coeff_monomial(1)
        )
    )
M = sp.Matrix(
    [
        [
            equation.coeff(variable)
            for variable in (X, Y, Z, x5, y5)
        ]
        for equation in lifted
    ]
)
print("rank", M.rank())
print("kernel", [[sp.factor(v) for v in K] for K in M.nullspace()])
for rows in itertools.combinations(range(6), 4):
    found = False
    for cols in itertools.combinations(range(5), 4):
        minor = sp.factor(M.extract(rows, cols).det())
        if minor:
            print("decisive", rows, cols, minor)
            found = True
            break
    if found:
        break

alpha = (
    sp.diff(Q, p) * sp.diff(R, q)
    - sp.diff(Q, q) * sp.diff(R, p)
)
beta = -(
    sp.diff(P, p) * sp.diff(R, q)
    - sp.diff(P, q) * sp.diff(R, p)
)
gamma = sp.diff(P, p) * sp.diff(Q, q) - sp.diff(P, q) * sp.diff(Q, p)
a0, a1, b0, b1, l33 = sp.symbols("a0 a1 b0 b1 l33")
constant = alpha * (a0 * p + a1 * q) + beta * (b0 * p + b1 * q) + gamma * l33
Mc = sp.Matrix(
    [
        [eq.coeff(v) for v in (a0, a1, b0, b1, l33)]
        for eq in coefficients(constant, 6)
    ]
)
print("constant rank", Mc.rank())
for rows in itertools.combinations(range(7), 5):
    det = sp.factor(Mc.extract(rows, range(5)).det())
    if det:
        print("constant decisive", rows, det)
        break

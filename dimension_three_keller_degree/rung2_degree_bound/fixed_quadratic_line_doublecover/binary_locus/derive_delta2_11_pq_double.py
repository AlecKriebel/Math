#!/usr/bin/env python3
"""Derive the lifted E6 contact matrix for h=pq, R=p^2(Ap+Bq)."""

from __future__ import annotations

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
R = p**2 * (A * p + B * q)
N1 = (5 * B * p**2, 15 * B * q**2, 5 * B**2 * p)
N2 = (-p * (9 * A * p - 8 * B * q), -27 * A * q**2, 5 * B**2 * q)
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
for omitted in range(6):
    rows = [index for index in range(6) if index != omitted]
    print("omit", omitted, sp.factor(M.extract(rows, range(5)).det()))

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
constant_eq = coefficients(constant, 6)
Mc = sp.Matrix(
    [
        [equation.coeff(variable) for variable in (a0, a1, b0, b1, l33)]
        for equation in constant_eq
    ]
)
print("constant rank", Mc.rank())
for rows in __import__("itertools").combinations(range(7), 5):
    determinant = sp.factor(Mc.extract(rows, range(5)).det())
    if determinant:
        print("constant decisive", rows, determinant)
        break

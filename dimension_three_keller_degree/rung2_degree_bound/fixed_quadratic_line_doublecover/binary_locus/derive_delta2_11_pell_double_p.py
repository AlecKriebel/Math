#!/usr/bin/env python3
"""Derive E6 contact data for h=p(p+q), R=p^2(Ap+Bq)."""

from __future__ import annotations

import itertools
import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, B = sp.symbols("A B")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def jac(first, second):
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), p, q)
    return [
        poly.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


h = p * (p + q)
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
R = p**2 * (A * p + B * q)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
uu = sp.symbols("u0:3")
vv = sp.symbols("v0:3")
tt = sp.symbols("t0:2")
uform = uu[0] * p**2 + uu[1] * p * q + uu[2] * q**2
vform = vv[0] * p**2 + vv[1] * p * q + vv[2] * q**2
tform = tt[0] * p + tt[1] * q
unknowns = (*uu, *vv, *tt)
M7 = sp.Matrix(
    [
        [equation.coeff(variable) for variable in unknowns]
        for equation in coefficients(
            alpha * uform + beta * vform + gamma * tform, 7
        )
    ]
)
print("E7 rank", M7.rank())
basis = M7.nullspace()
print("basis", [[sp.factor(value) for value in K] for K in basis])
tangents = []
for vector in basis:
    substitution = dict(zip(unknowns, vector))
    tangents.append(
        (
            sp.factor(uform.subs(substitution)),
            sp.factor(vform.subs(substitution)),
            sp.factor(tform.subs(substitution)),
        )
    )
N1 = tuple(sp.factor(B * value) for value in tangents[0])
N2 = tuple(sp.factor(5 * B**2 * value) for value in tangents[1])
print("polynomial basis", N1, N2)
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
print("contact rank", M.rank())
print("contact kernel", [[sp.factor(v) for v in K] for K in M.nullspace()])
rank = M.rank()
for rows in itertools.combinations(range(6), rank):
    found = False
    for cols in itertools.combinations(range(5), rank):
        minor = sp.factor(M.extract(rows, cols).det())
        if minor:
            print("decisive", rows, cols, minor)
            found = True
            break
    if found:
        break

a0, a1, b0, b1, l33 = sp.symbols("a0 a1 b0 b1 l33")
constant = (
    alpha * (a0 * p + a1 * q)
    + beta * (b0 * p + b1 * q)
    + gamma * l33
)
Mc = sp.Matrix(
    [
        [equation.coeff(variable) for variable in (a0, a1, b0, b1, l33)]
        for equation in coefficients(constant, 6)
    ]
)
print("constant rank", Mc.rank())
for rows in itertools.combinations(range(7), 5):
    determinant = sp.factor(Mc.extract(rows, range(5)).det())
    if determinant:
        print("constant decisive", rows, determinant)
        break

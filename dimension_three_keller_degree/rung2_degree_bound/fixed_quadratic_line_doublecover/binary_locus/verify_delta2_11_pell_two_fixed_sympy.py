#!/usr/bin/env python3
"""Exact E6 exclusion of h=p(p+q), R=p(p+q)(Ap+Bq)."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
A, B = sp.symbols("A B")
s, t, x5, y5 = sp.symbols("s t x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)


def zero(value):
    return sp.cancel(sp.expand(value)) == 0


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


ell = p + q
P, Q = p**3 * ell, p * ell * q**2
R = p * ell * (A * p + B * q)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == p * ell

boundaries = (
    ({A: 1, B: 0}, p**2 * ell),
    ({A: 1, B: 1}, p * ell**2),
    ({A: -4, B: 1}, p * q * ell),
)
for substitution, expected in boundaries:
    specialized = (
        alpha.subs(substitution),
        beta.subs(substitution),
        gamma,
    )
    assert zero(
        sp.factor(sp.gcd(sp.gcd(specialized[0], specialized[1]),
                        specialized[2]))
        - expected
    )

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
assert zero(
    M7.extract(range(6), range(6)).det()
    - 24 * B**3 * (A - B) ** 2 * (A + 4 * B)
)
for substitution, _ in boundaries:
    assert M7.subs(substitution).rank() == 5

N1 = (
    5 * B * p**2,
    -B * q * (6 * p + q),
    3 * B * p * (A - B),
)
N2 = (
    -(A + 4 * B) * p**2,
    q * (6 * A * p + 5 * A * q - 4 * B * q),
    3 * B * q * (A - B),
)
for tangent in (N1, N2):
    assert zero(
        alpha * tangent[0]
        + beta * tangent[1]
        + gamma * tangent[2]
    )
print("PASS exact boundaries and complete two-tangent E7 basis")

N = tuple(
    sp.expand(s * N1[index] + t * N2[index])
    for index in range(3)
)
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
assert zero(weighted.coeff_monomial(z**7))
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
contact = sp.Matrix(
    [
        [
            equation.coeff(variable)
            for variable in (X, Y, Z, x5, y5)
        ]
        for equation in lifted
    ]
)
kernel = sp.Matrix(
    [
        -(5 * A**2 + 4 * A * B - 4 * B**2),
        -B * (7 * A - 2 * B),
        -5 * B**2,
        0,
        36 * B**2 * (A - B) ** 2,
    ]
)
assert all(zero(value) for value in contact * kernel)
assert zero(
    contact.extract((0, 1, 2, 3), (0, 1, 2, 3)).det()
    + 41472 * B**5 * (A - B) ** 4 * (A + 4 * B)
)
assert zero(
    kernel[1] ** 2 - kernel[0] * kernel[2]
    - 24 * B**2 * (A - B) ** 2
)
print("PASS rank-four contact kernel misses the Veronese cone")

a0, a1, b0, b1, l33 = sp.symbols("a0 a1 b0 b1 l33")
constant_E6 = (
    alpha * (a0 * p + a1 * q)
    + beta * (b0 * p + b1 * q)
    + gamma * l33
)
constant_matrix = sp.Matrix(
    [
        [
            equation.coeff(variable)
            for variable in (a0, a1, b0, b1, l33)
        ]
        for equation in coefficients(constant_E6, 6)
    ]
)
assert zero(
    constant_matrix.extract((1, 2, 3, 4, 5), range(5)).det()
    - 8 * B**2 * (A - B) * (A + 4 * B)
)
print("PASS constant E6 full rank and all-binary exit")
print("ALL PELL TWO-FIXED {1,1} EXCLUSION CHECKS PASSED")

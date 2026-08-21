#!/usr/bin/env python3
"""Exact E6 exclusion of h=pq, R=p^2(Ap+Bq), AB!=0."""

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


P, Q = p**3 * q, p * q**3
R = p**2 * (A * p + B * q)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == p**2
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(A, 0), beta.subs(A, 0)), gamma
    )
) == p**2 * q
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(B, 0), beta.subs(B, 0)), gamma
    )
) == p**3

N1 = (5 * B * p**2, 15 * B * q**2, 5 * B**2 * p)
N2 = (
    -p * (9 * A * p - 8 * B * q),
    -27 * A * q**2,
    5 * B**2 * q,
)
for tangent in (N1, N2):
    assert zero(
        alpha * tangent[0]
        + beta * tangent[1]
        + gamma * tangent[2]
    )
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
assert zero(
    contact.extract((0, 1, 2, 3, 4), range(5)).det()
    + 2332800000 * A**3 * B**8
)
print("PASS exact-open lifted E6 contact injectivity")

# Once the contact variables vanish, every H3/H2 term is binary except
# for the possible linear-in-r A,B terms.  Constant E6 is exactly the
# full-rank M1 block below.
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
    constant_matrix.extract((0, 1, 2, 3, 4), range(5)).det()
    + 3240 * A**3 * B
)
print("PASS constant E6 full rank and all-binary exit")
print("ALL PQ DOUBLED-CONTRIBUTION {1,1} EXCLUSION CHECKS PASSED")

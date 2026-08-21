#!/usr/bin/env python3
"""Exact E6 exclusion of h=pq, R=pq(Ap+Bq), AB!=0."""

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
R = p * q * (A * p + B * q)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == p * q
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(A, 0), beta.subs(A, 0)), gamma
    )
) == p * q**2
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(B, 0), beta.subs(B, 0)), gamma
    )
) == p**2 * q

N1 = (5 * p**2, -q**2, 3 * A * p)
N2 = (-p**2, 5 * q**2, 3 * B * q)
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
kernel = sp.Matrix([1, sp.Rational(7, 5), 1, 0, 0])
assert all(zero(value) for value in contact * kernel)
assert zero(
    contact.extract((1, 2, 3, 4), (0, 1, 3, 4)).det()
    - 5760 * A**2 * B**2
)
assert zero(
    kernel[1] ** 2 - kernel[0] * kernel[2]
    - sp.Rational(24, 25)
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
    - 8 * A**2 * B**2
)
print("PASS constant E6 full rank and all-binary exit")
print("ALL PQ TWO-SIMPLE {1,1} EXCLUSION CHECKS PASSED")

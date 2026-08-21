#!/usr/bin/env python3
"""Exact E6 exclusion for h=p(p+q), R=p^2(Ap+Bq)."""

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


h = p * (p + q)
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
R = p**2 * (A * p + B * q)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == p**2
assert sp.factor(
    sp.gcd(sp.gcd(alpha.subs(B, 0), beta.subs(B, 0)), gamma)
) == p**3
assert sp.factor(
    sp.gcd(sp.gcd(alpha.subs(A, B), beta.subs(A, B)), gamma)
) == p**2 * (p + q)
assert sp.factor(
    sp.gcd(
        sp.gcd(
            alpha.subs(A, sp.Rational(4, 3) * B),
            beta.subs(A, sp.Rational(4, 3) * B),
        ),
        gamma,
    )
) == p**2 * q
assert sp.factor(
    sp.gcd(sp.gcd(alpha.subs(A, 0), beta.subs(A, 0)), gamma)
) == p**2

N1 = (p**2, q * (2 * p + 3 * q), B * p)
N2 = (
    -p * (9 * A * p - 12 * B * p - 8 * B * q),
    -q * (18 * A * p + 27 * A * q - 4 * B * q),
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
    + 6220800 * B**5 * (A - B) ** 2 * (3 * A - 4 * B)
)
print("PASS exact-open lifted contact injectivity and boundary routing")

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
    + 1080 * B * (A - B) ** 2 * (3 * A - 4 * B)
)
print("PASS constant E6 full rank and all-binary exit")
print("ALL PELL DOUBLED-P {1,1} EXCLUSION CHECKS PASSED")

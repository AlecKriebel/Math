#!/usr/bin/env python3
"""Exact E6 exclusion for h=p(p+q), R=(p+q)^2(Ap+Bq)."""

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


def contact_matrix(P, Q, R, N1, N2):
    alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
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
    determinant = sp.Poly(
        sp.expand(
            (
                z * H2.jacobian(variables)
                + z**2 * H3.jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    assert zero(determinant.coeff_monomial(z**7))
    E6r = sp.Poly(
        sp.expand(determinant.coeff_monomial(z**6)), r
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
    return sp.Matrix(
        [
            [
                equation.coeff(variable)
                for variable in (X, Y, Z, x5, y5)
            ]
            for equation in lifted
        ]
    )


ell = p + q
h = p * ell
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
R = ell**2 * (A * p + B * q)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == ell**2
assert sp.factor(
    sp.gcd(sp.gcd(alpha.subs(B, 0), beta.subs(B, 0)), gamma)
) == p * ell**2
assert sp.factor(
    sp.gcd(
        sp.gcd(
            alpha.subs(A, -sp.Rational(4, 5) * B),
            beta.subs(A, -sp.Rational(4, 5) * B),
        ),
        gamma,
    )
) == q * ell**2
assert sp.factor(
    sp.gcd(sp.gcd(alpha.subs(A, B), beta.subs(A, B)), gamma)
) == ell**2

# Polynomial tangent basis away from the internal pivot A=B.
N1 = (
    -27 * B * p**2,
    q * (8 * A * p + 10 * B * p - 9 * B * q),
    5 * p * (A - B) ** 2,
)
N2 = (
    3 * p**2 * (5 * A + 4 * B),
    -q * (18 * A * p - 5 * A * q - 4 * B * q),
    5 * q * (A - B) ** 2,
)
contact = contact_matrix(P, Q, R, N1, N2)
minor0 = sp.factor(
    contact.extract((1, 2, 3, 4, 5), range(5)).det()
)
minor1 = sp.factor(
    contact.extract((0, 2, 3, 4, 5), range(5)).det()
)
assert zero(
    minor0
    + 466560000
    * B**3
    * (A - B) ** 6
    * (5 * A**2 + 26 * A * B + 23 * B**2)
)
assert zero(
    minor1
    + 311040000
    * B**3
    * (A - B) ** 6
    * (2 * A + 7 * B)
    * (5 * A + 4 * B)
)
assert zero(
    (5 * A**2 + 26 * A * B + 23 * B**2).subs(
        A, -sp.Rational(7, 2) * B
    )
    + sp.Rational(27, 4) * B**2
)

# A=B is exact delta=2 and gets a fresh basis rather than division.
R_equal = ell**3
N1_equal = (3 * p**2, -q * (2 * p - q), 0)
N2_equal = (0, sp.Rational(8, 9) * p * q, ell)
contact_equal = contact_matrix(
    P, Q, R_equal, N1_equal, N2_equal
)
assert zero(
    contact_equal.extract((1, 2, 3, 4, 5), range(5)).det()
    - 276480
)
print("PASS two-minor contact cover and fresh A=B pivot chart")

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
    + 648 * B**3 * (5 * A + 4 * B)
)
print("PASS exact boundaries, constant E6 rank, and all-binary exit")
print("ALL PELL DOUBLED-L {1,1} EXCLUSION CHECKS PASSED")

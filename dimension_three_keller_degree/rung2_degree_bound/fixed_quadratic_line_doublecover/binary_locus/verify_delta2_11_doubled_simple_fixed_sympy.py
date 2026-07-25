#!/usr/bin/env python3
"""Exact exclusion of h=(p+q)^2 with one simple fixed root."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
A, B, C = sp.symbols("A B C")
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
    polynomial = sp.Poly(sp.expand(value), p, q)
    return [
        polynomial.coeff_monomial(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


def contact_matrix(P, Q, R, first, second):
    tangent = tuple(
        sp.expand(s * first[index] + t * second[index])
        for index in range(3)
    )
    H4 = sp.Matrix([P, Q, 0])
    H3 = sp.Matrix([r * tangent[0], r * tangent[1], R])
    H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * tangent[2]])
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
        polynomial = sp.Poly(equation, s, t)
        lifted.append(
            sp.expand(
                polynomial.coeff_monomial(s**2) * X
                + polynomial.coeff_monomial(s * t) * Y
                + polynomial.coeff_monomial(t**2) * Z
                + polynomial.coeff_monomial(1)
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


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand((p + q) * (A * p**2 + B * p * q + C * q**2))
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == 2 * h

e1 = A - 2 * B
e2 = 2 * B - C
e3 = A - B + C
assert sp.factor(
    sp.gcd(sp.gcd(alpha.subs(A, 2 * B), beta.subs(A, 2 * B)), gamma)
) == 2 * q * h
assert sp.factor(
    sp.gcd(sp.gcd(alpha.subs(C, 2 * B), beta.subs(C, 2 * B)), gamma)
) == 2 * p * h
assert sp.factor(
    sp.gcd(
        sp.gcd(alpha.subs(A, B - C), beta.subs(A, B - C)),
        gamma,
    )
) == 2 * (p + q) ** 3

# The only projective stabilizer is p <-> q, which swaps A and C.
assert zero(
    R.subs({p: q, q: p}, simultaneous=True)
    - R.subs({A: C, C: A}, simultaneous=True)
)
print("PASS exact-open gcd mutations and residual stabilizer")

Delta = 4 * A * C - B**2
N1 = (
    -2 * (B - 8 * C) * p**2 + 12 * C * p * q,
    -6 * B * p * q - 4 * (2 * B - C) * q**2,
    3 * Delta * p,
)
N2 = (
    4 * (A - 2 * B) * p**2 - 6 * B * p * q,
    12 * A * p * q + 2 * (8 * A - B) * q**2,
    3 * Delta * q,
)
for tangent in (N1, N2):
    assert zero(
        alpha * tangent[0] + beta * tangent[1] + gamma * tangent[2]
    )
e7_monomials = (p**2, p * q, q**2, p**2, p * q, q**2, p, q)
e7_columns = tuple(
    alpha * e7_monomials[index]
    if index < 3
    else beta * e7_monomials[index]
    if index < 6
    else gamma * e7_monomials[index]
    for index in range(8)
)
e7_matrix = sp.Matrix.hstack(
    *(sp.Matrix(coefficients(column, 7)) for column in e7_columns)
)
assert zero(
    e7_matrix.extract(range(6), range(6)).det()
    + 768 * e1 * e2 * Delta * e3**2
)

generic_contact = contact_matrix(P, Q, R, N1, N2)
expected_generic = (
    26542080 * e1 * e2 * Delta**3 * e3**3
)
assert zero(
    generic_contact.extract(range(5), range(5)).det()
    - expected_generic
)
print("PASS generic Delta-nonzero contact determinant")

# Delta=0 is an internal pivot, not an incidence boundary.
A_delta = B**2 / (4 * C)
R_delta = sp.expand(R.subs(A, A_delta))
alpha_delta = sp.cancel(alpha.subs(A, A_delta))
beta_delta = sp.cancel(beta.subs(A, A_delta))
N1_delta = (
    (B - 8 * C) * p**2 - 6 * C * p * q,
    3 * B * p * q + 2 * (2 * B - C) * q**2,
    0,
)
N2_delta = (
    10 * C * p**2 + 8 * C * p * q,
    -2 * C * p * q,
    (2 * B - C) * (B * p + 2 * C * q),
)
for tangent in (N1_delta, N2_delta):
    assert zero(
        alpha_delta * tangent[0]
        + beta_delta * tangent[1]
        + gamma * tangent[2]
    )
e7_delta = e7_matrix.applyfunc(
    lambda value: sp.cancel(value.subs(A, A_delta))
)
assert zero(
    e7_delta.extract(range(6), (0, 1, 2, 3, 4, 6)).det()
    + 16
    * B
    * (B - 8 * C)
    * (B - 2 * C) ** 4
    * (2 * B - C) ** 2
    / C**3
)

delta_contact = contact_matrix(
    P, Q, R_delta, N1_delta, N2_delta
)
expected_delta = (
    -3840
    * B
    * (B - 8 * C)
    * (B - 2 * C) ** 6
    * (2 * B - C) ** 4
    / C
)
assert zero(
    delta_contact.extract(range(5), range(5)).det()
    - expected_delta
)
assert zero(e1.subs(A, A_delta) - B * (B - 8 * C) / (4 * C))
assert zero(e3.subs(A, A_delta) - (B - 2 * C) ** 2 / (4 * C))
print("PASS fresh Delta-zero contact determinant and exact-open cover")

# With the contact tangent killed, the remaining E6 constant block is
# uniformly full rank on the same exact open.
constant_columns = (
    alpha * p,
    alpha * q,
    beta * p,
    beta * q,
    gamma,
)
constant_matrix = sp.Matrix.hstack(
    *(
        sp.Matrix(coefficients(column, 6))
        for column in constant_columns
    )
)
assert zero(
    constant_matrix.extract(range(5), range(5)).det()
    + 512 * e1 * e2 * e3**2
)
print("PASS uniform constant E6 determinant and all-binary exit")
print("ALL DOUBLED-NONBRANCH SIMPLE-FIXED {1,1} CHECKS PASSED")

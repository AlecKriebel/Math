#!/usr/bin/env python3
"""Exact E6 exclusion for the fixed-(p+q) plus contact leaf."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
B, C = sp.symbols("B C")
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


def contact_matrix(P_case, Q_case, R_case, first, second):
    tangent = tuple(
        sp.expand(s * first[index] + t * second[index])
        for index in range(3)
    )
    H4 = sp.Matrix([P_case, Q_case, 0])
    H3 = sp.Matrix([r * tangent[0], r * tangent[1], R_case])
    H2 = sp.Matrix([x5 * r**2, y5 * r**2, r * tangent[2]])
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
    e6r = sp.Poly(
        sp.expand(weighted.coeff_monomial(z**6)), r
    ).coeff_monomial(r)
    lifted = []
    for equation in coefficients(e6r, 5):
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
P, Q = p**3 * ell, p * ell * q**2
R = ell * (-4 * B * p**2 + B * p * q + C * q**2)
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) == q * ell

boundary_data = (
    ({C: 0, B: 1}, p * q * ell),
    ({C: 5, B: 1}, q * ell**2),
)
for substitution, expected in boundary_data:
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
for substitution, _ in boundary_data:
    assert M7.subs(substitution).rank() == 5
assert zero(
    M7.extract((1, 2, 3, 4, 5, 6), range(6)).det()
    - 216 * C**3 * (B + 16 * C) * (5 * B - C) ** 2
)
print("PASS fresh C=0 and C=5B delta-three boundary reruns")

N1 = (
    -27 * C * p**2,
    8 * B * p**2
    + 8 * B * p * q
    - 16 * C * p**2
    + 2 * C * p * q
    - 9 * C * q**2,
    p * (B + 16 * C) * (5 * B - C),
)
N2 = (
    3 * p**2 * (5 * B + 8 * C),
    72 * B * p**2
    + 62 * B * p * q
    + 5 * B * q**2
    - 16 * C * p * q
    + 8 * C * q**2,
    q * (B + 16 * C) * (5 * B - C),
)
for tangent in (N1, N2):
    assert zero(
        alpha * tangent[0]
        + beta * tangent[1]
        + gamma * tangent[2]
    )
generic_contact = contact_matrix(P, Q, R, N1, N2)
assert zero(
    generic_contact.extract(range(5), range(5)).det()
    + 746496
    * C**3
    * (B + 16 * C) ** 3
    * (5 * B - 4 * C)
    * (5 * B - C) ** 4
)
print("PASS generic lifted contact determinant")

pivot_substitution = {B: -16, C: 1}
pivot_R = R.subs(pivot_substitution)
pivot_alpha = alpha.subs(pivot_substitution)
pivot_beta = beta.subs(pivot_substitution)
pivot_M7 = M7.subs(pivot_substitution)
assert zero(
    pivot_M7.extract(
        (1, 2, 3, 4, 5, 6), (0, 1, 2, 3, 4, 6)
    ).det()
    + 157464
)
pivot_N1 = (3 * p**2, 16 * p**2 + 14 * p * q + q**2, 0)
pivot_N2 = (0, sp.Rational(8, 9) * p * ell, -8 * p + q)
for tangent in (pivot_N1, pivot_N2):
    assert zero(
        pivot_alpha * tangent[0]
        + pivot_beta * tangent[1]
        + gamma * tangent[2]
    )
pivot_contact = contact_matrix(P, Q, pivot_R, pivot_N1, pivot_N2)
assert zero(
    pivot_contact.extract(range(5), range(5)).det() - 6967296
)
print("PASS fresh B=-16C pivot chart has full contact rank")

special_substitution = {B: 4, C: 5}
special_R = R.subs(special_substitution)
special_alpha = alpha.subs(special_substitution)
special_beta = beta.subs(special_substitution)
special_M7 = M7.subs(special_substitution)
assert zero(
    special_M7.extract((1, 2, 3, 4, 5, 6), range(6)).det()
    - 510300000
)
special_N1 = (
    -sp.Rational(3, 28) * p**2,
    -(16 * p**2 - 14 * p * q + 15 * q**2) / 420,
    p,
)
special_N2 = (
    p**2 / 7,
    (24 * p**2 + 14 * p * q + 5 * q**2) / 105,
    q,
)
for tangent in (special_N1, special_N2):
    assert zero(
        special_alpha * tangent[0]
        + special_beta * tangent[1]
        + gamma * tangent[2]
    )
special_contact = contact_matrix(P, Q, special_R, special_N1, special_N2)
special_kernel = sp.Matrix(
    [-840, -sp.Rational(945, 2), -sp.Rational(945, 4), 0, 1]
)
assert all(zero(value) for value in special_contact * special_kernel)
assert zero(
    special_contact.extract((1, 2, 3, 4), range(4)).det()
    - sp.Rational(120, 343)
)
assert zero(
    special_kernel[1] ** 2
    - special_kernel[0] * special_kernel[2]
    - sp.Rational(99225, 4)
)
print("PASS fresh 5B=4C kernel misses the Veronese cone")

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
    constant_matrix.extract((2, 3, 4, 5, 6), range(5)).det()
    + 648 * C**3 * (5 * B - C)
)
print("PASS constant E6 full rank and all-binary exit")
print("ALL PELL FIXED-L CONTACT {1,1} EXCLUSION CHECKS PASSED")

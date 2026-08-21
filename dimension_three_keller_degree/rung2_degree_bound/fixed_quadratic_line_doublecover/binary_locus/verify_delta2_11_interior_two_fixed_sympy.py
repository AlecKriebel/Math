#!/usr/bin/env python3
"""Exact E6 exclusion for the squarefree-interior two-fixed-root leaf."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
w, A, B = sp.symbols("w A B")
c1, c2, x5, y5 = sp.symbols("c1 c2 x5 y5")
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
        sp.expand(c1 * first[index] + c2 * second[index])
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
        poly = sp.Poly(equation, c1, c2)
        lifted.append(
            sp.expand(
                poly.coeff_monomial(c1**2) * X
                + poly.coeff_monomial(c1 * c2) * Y
                + poly.coeff_monomial(c2**2) * Z
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


L = p - w * q
Mfixed = w * p - q
h = sp.expand(L * Mfixed)
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
R = sp.expand(h * (A * p + B * q))
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert zero(sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) - h)

boundary_data = (
    ({A: -w, B: 1}, L * Mfixed**2),
    ({A: 1, B: -w}, L**2 * Mfixed),
    ({A: 4 * w, B: w**2 + 1}, q * h),
    ({A: w**2 + 1, B: 4 * w}, p * h),
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
print("PASS four deeper-incidence boundary gcd reruns")

eval_M = A + B * w
eval_L = A * w + B
left_contact = A * w**2 + A - 4 * B * w
right_contact = -4 * A * w + B * w**2 + B

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
    - 24
    * w**6
    * eval_M**2
    * (w - 1) ** 2
    * (w + 1) ** 2
    * eval_L**2
    * right_contact
    * left_contact
)

N1 = (
    p * (4 * A * p * w + 5 * B * p * w**2 + 5 * B * p - 6 * B * q * w),
    q * (4 * A * q * w + 6 * B * p * w - B * q * w**2 - B * q),
    3 * p * eval_M * eval_L,
)
N2 = (
    -p * (A * p * w**2 + A * p - 6 * A * q * w - 4 * B * p * w),
    -q * (6 * A * p * w - 5 * A * q * w**2 - 5 * A * q - 4 * B * q * w),
    3 * q * eval_M * eval_L,
)
for tangent in (N1, N2):
    assert zero(
        alpha * tangent[0]
        + beta * tangent[1]
        + gamma * tangent[2]
    )
contact = contact_matrix(P, Q, R, N1, N2)
assert zero(
    contact.extract((0, 1, 2, 3), (0, 1, 2, 3)).det()
    + 41472
    * w**5
    * eval_M**4
    * eval_L**4
    * right_contact
    * left_contact
)
kernel = sp.Matrix(
    [
        5 * A**2 * w**4
        - 14 * A**2 * w**2
        + 5 * A**2
        - 4 * A * B * w**3
        - 4 * A * B * w
        - 4 * B**2 * w**2,
        2 * A**2 * w**3
        + 2 * A**2 * w
        + 7 * A * B * w**4
        - 6 * A * B * w**2
        + 7 * A * B
        + 2 * B**2 * w**3
        + 2 * B**2 * w,
        -4 * A**2 * w**2
        - 4 * A * B * w**3
        - 4 * A * B * w
        + 5 * B**2 * w**4
        - 14 * B**2 * w**2
        + 5 * B**2,
        -36 * w * eval_M**2 * eval_L**2,
        -36 * w * eval_M**2 * eval_L**2,
    ]
)
assert all(zero(value) for value in contact * kernel)
assert zero(
    kernel[1] ** 2
    - kernel[0] * kernel[2]
    - 24
    * eval_M**2
    * (w - 1) ** 2
    * (w + 1) ** 2
    * eval_L**2
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
    constant_matrix.extract(range(5), range(5)).det()
    + 8
    * w**5
    * eval_M
    * (w - 1) ** 2
    * (w + 1) ** 2
    * eval_L
    * right_contact
    * left_contact
)
print("PASS constant E6 full rank and all-binary exit")
print("ALL INTERIOR TWO-FIXED {1,1} EXCLUSION CHECKS PASSED")

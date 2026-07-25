#!/usr/bin/env python3
"""Exact raw-determinant certificate for the a=0, W_0 != 0 exclusion.

The weighted coefficient E_6 is built directly from row multilinearity.
An exterior expansion is built separately and compared to the raw result.
The binary E_5 classification formulas and the six decisive coefficients
of the scaled E_6 factor are then checked symbolically.
"""

from __future__ import annotations

from itertools import product
import os
import sys

import sympy as s


if not __debug__:
    raise SystemExit("FAIL: optimized Python disables fail-closed assertions")


def check(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


x, y, z = s.symbols("x y z")
kappa, gamma = s.symbols("kappa gamma")
alpha, beta, chi, delta, epsilon, phi = s.symbols(
    "alpha beta chi delta epsilon phi"
)
u, v, omega = s.symbols("u v omega")
a20, a11, a02, a10, a01, a00 = s.symbols(
    "a20 a11 a02 a10 a01 a00"
)
b20, b11, b02, b10, b01, b00 = s.symbols(
    "b20 b11 b02 b10 b01 b00"
)
v30, v21, v12, v03, v20, v11, v02, v10, v01 = s.symbols(
    "v30 v21 v12 v03 v20 v11 v02 v10 v01"
)
l11, l12, l13, l21, l22, l23, l31, l32, l33 = s.symbols(
    "l11 l12 l13 l21 l22 l23 l31 l32 l33"
)
t = s.symbols("t")

q = (
    kappa * x**3
    + z * (alpha * x**2 + beta * x * y + chi * y**2)
    + z**2 * (delta * x + epsilon * y)
    + phi * z**3
)
W = gamma * x**2 + z * (u * x + v * y) + omega * z**2
A = (
    a20 * x**2
    + a11 * x * y
    + a02 * y**2
    + z * (a10 * x + a01 * y)
    + a00 * z**2
)
B = (
    b20 * x**2
    + b11 * x * y
    + b02 * y**2
    + z * (b10 * x + b01 * y)
    + b00 * z**2
)
V = (
    v30 * x**3
    + v21 * x**2 * y
    + v12 * x * y**2
    + v03 * y**3
    + z * (v20 * x**2 + v11 * x * y + v02 * y**2)
    + z**2 * (v10 * x + v01 * y)
)
linear_forms = (
    l11 * x + l12 * y + l13 * z,
    l21 * x + l22 * y + l23 * z,
    l31 * x + l32 * y + l33 * z,
)
h2 = (A, B, W)
h3 = (s.Rational(4, 3) * z * W, V, z**3)
h4 = (z**4, z * q, s.Integer(0))


def gradient(form):
    return (s.diff(form, x), s.diff(form, y), s.diff(form, z))


def jac(first, second, third):
    return s.det(s.Matrix((gradient(first), gradient(second), gradient(third))))


def bracket(first, second):
    return s.diff(first, x) * s.diff(second, y) - s.diff(
        first, y
    ) * s.diff(second, x)


def weighted_coefficient(weight):
    jets = tuple(
        tuple(gradient(forms[row]) for forms in (linear_forms, h2, h3, h4))
        for row in range(3)
    )
    result = 0
    for choices in product(range(4), repeat=3):
        if sum(choices) != weight:
            continue
        result += s.det(s.Matrix(tuple(jets[row][choices[row]] for row in range(3))))
    return s.expand(result)


raw_e8 = weighted_coefficient(8)
raw_e7 = weighted_coefficient(7)
raw_e6 = weighted_coefficient(6)
check(raw_e8 == 0, "E8 did not vanish")
check(raw_e7 == 0, "E7 did not vanish")

exterior_e6 = s.expand(
    jac(h4[0], h4[1], linear_forms[2])
    + jac(h3[0], h4[1], h2[2])
    + jac(h4[0], h3[1], h2[2])
    + jac(h2[0], h4[1], h3[2])
    + jac(h3[0], h3[1], h3[2])
    + jac(h4[0], h2[1], h3[2])
)
check(raw_e6 == exterior_e6, "raw and exterior E6 differ")

Phi = s.expand(
    4 * W * bracket(q, W)
    + 9 * z**2 * bracket(A, q)
    + 12 * z**3 * bracket(q, linear_forms[2])
)
check(s.expand(3 * raw_e6 - z * Phi) == 0, "3 E6 != z Phi")

phi_poly = s.Poly(Phi, x, y, z)


def coefficient(monomial):
    return s.factor(phi_poly.coeff_monomial(monomial))


expected_coefficients = {
    x**3 * y * z: -16 * chi * gamma**2,
    x**4 * z: 4 * gamma * (-2 * beta * gamma + 3 * kappa * v),
    x**2 * y * z**2: -2
    * (
        27 * a02 * kappa
        + 2 * beta * gamma * v
        + 12 * chi * gamma * u
        - 6 * kappa * v**2
    ),
    y**2 * z**3: -2
    * (
        9 * a02 * beta
        - 9 * a11 * chi
        - 2 * beta * v**2
        + 4 * chi * u * v
    ),
    x**3 * z**2: (
        -27 * a11 * kappa
        + 8 * alpha * gamma * v
        - 12 * beta * gamma * u
        - 8 * epsilon * gamma**2
        + 12 * kappa * u * v
    ),
    y * z**4: (
        -9 * a01 * beta
        - 18 * a02 * delta
        + 18 * a10 * chi
        + 9 * a11 * epsilon
        + 12 * beta * l32
        + 4 * beta * v * omega
        - 24 * chi * l31
        - 8 * chi * u * omega
        + 4 * delta * v**2
        - 4 * epsilon * u * v
    ),
}
for monomial, expected in expected_coefficients.items():
    check(
        s.expand(coefficient(monomial) - expected) == 0,
        f"wrong Phi coefficient at {monomial}",
    )

# Exact ideal-combination checks used by the division-free proof.
r = 2 * beta * gamma - 3 * kappa * v
f = 27 * kappa * a02 + 2 * beta * gamma * v - 6 * kappa * v**2
g = 9 * a02 - v**2
h = 9 * a02 * beta - 2 * beta * v**2
check(s.expand(f - v * r - 3 * kappa * g) == 0, "first ideal identity failed")
check(s.expand(h - beta * g + beta * v**2) == 0, "second ideal identity failed")
j = 27 * kappa * a11 + 8 * gamma**2 * epsilon
k = 9 * a11 * epsilon
check(
    s.expand(epsilon * j - 3 * kappa * k - 8 * gamma**2 * epsilon**2)
    == 0,
    "epsilon ideal identity failed",
)

# Reconstruct the plane E5 identity and the two complete binary solution
# tables in coefficient form.
q30, q21, q12, q03 = s.symbols("q30 q21 q12 q03")
aa, ab, ac = s.symbols("aa ab ac")
d30, d21, d12, d03 = s.symbols("d30 d21 d12 d03")
q0 = q30 * x**3 + q21 * x**2 * y + q12 * x * y**2 + q03 * y**3
A0 = aa * x**2 + ab * x * y + ac * y**2
V0 = d30 * x**3 + d21 * x**2 * y + d12 * x * y**2 + d03 * y**3

identity_xy = s.Poly(
    s.expand(4 * x * y * bracket(V0, x * y) + 3 * q0 * bracket(x * y, A0)),
    x,
    y,
)
xy_expected = {
    x**5: -6 * aa * q30,
    x**4 * y: 12 * d30 - 6 * aa * q21,
    x**3 * y**2: 4 * d21 + 6 * (ac * q30 - aa * q12),
    x**2 * y**3: -4 * d12 + 6 * (ac * q21 - aa * q03),
    x * y**4: -12 * d03 + 6 * ac * q12,
    y**5: 6 * ac * q03,
}
for monomial, expected in xy_expected.items():
    check(
        s.expand(identity_xy.coeff_monomial(monomial) - expected) == 0,
        f"W0=xy table failed at {monomial}",
    )

identity_x2 = s.expand(
    4 * x**2 * bracket(V0, x**2) + 3 * q0 * bracket(x**2, A0)
)
check(
    s.expand(identity_x2 - 2 * x * (-4 * x**2 * s.diff(V0, y) + 3 * q0 * s.diff(A0, y)))
    == 0,
    "W0=x^2 factorization failed",
)

# Sharp nonminimal boundary witness: it survives E8 through E4 but not the
# lower determinant identities.
boundary_substitution = {
    kappa: 1,
    gamma: 1,
    alpha: 0,
    beta: 0,
    chi: 0,
    delta: 0,
    epsilon: 0,
    phi: 0,
    u: 0,
    v: 0,
    omega: 0,
    a20: 0,
    a11: 0,
    a02: 0,
    a10: 0,
    a01: 0,
    a00: 0,
    b20: 0,
    b11: 0,
    b02: 0,
    b10: 0,
    b01: 0,
    b00: 0,
    v30: 0,
    v21: 0,
    v12: 0,
    v03: 0,
    v20: 0,
    v11: 0,
    v02: 0,
    v10: 0,
    v01: 0,
    l11: 1,
    l12: 0,
    l13: 0,
    l21: 0,
    l22: 1,
    l23: 0,
    l31: 0,
    l32: 0,
    l33: 1,
}
boundary_coefficients = [
    s.expand(weighted_coefficient(weight).subs(boundary_substitution))
    for weight in range(9)
]
check(
    all(boundary_coefficients[weight] == 0 for weight in range(4, 9)),
    "nonminimal boundary witness does not survive E8 through E4",
)
check(boundary_coefficients[3] == -s.Rational(8, 3) * x**3, "wrong boundary E3")
check(
    s.expand(boundary_coefficients[2] - z * (8 * x + 9 * z) / 3) == 0,
    "wrong boundary E2",
)
check(boundary_coefficients[1] == 0, "wrong boundary E1")
check(boundary_coefficients[0] == 1, "wrong boundary E0")

# Negative controls must change the exact raw factorization.
mutation = os.environ.get("A0_W0_MUTATION", "")
if mutation:
    if mutation == "wrong_U":
        mutated_h3 = (s.Rational(5, 3) * z * W, V, z**3)
        original = h3
        h3 = mutated_h3
        mutated_e6 = weighted_coefficient(6)
        h3 = original
        check(
            s.expand(3 * mutated_e6 - z * Phi) == 0,
            "wrong_U mutation unexpectedly survived",
        )
    elif mutation == "drop_chi":
        check(
            coefficient(x**3 * y * z) == 0,
            "drop_chi mutation unexpectedly survived",
        )
    elif mutation == "flip_bracket":
        wrong_phi = s.expand(
            4 * W * bracket(W, q)
            + 9 * z**2 * bracket(A, q)
            + 12 * z**3 * bracket(q, linear_forms[2])
        )
        check(
            s.expand(3 * raw_e6 - z * wrong_phi) == 0,
            "flip_bracket mutation unexpectedly survived",
        )
    else:
        raise SystemExit(f"FAIL: unknown mutation {mutation}")

print("PASS: A0_W0_NONZERO_SYMPY_E6_6E2A91")

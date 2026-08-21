#!/usr/bin/env python3
"""Exact SymPy replay of the squarefree interior fixed/contact leaf."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp


p, q, r, z = sp.symbols("p q r z")
w, A, T = sp.symbols("w A T")
c1, c2, x5, y5 = sp.symbols("c1 c2 x5 y5")
X, Y, Z = sp.symbols("X Y Z")
variables = (p, q, r)
u = w**2


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
    H4_case = sp.Matrix([P_case, Q_case, 0])
    H3_case = sp.Matrix(
        [r * tangent[0], r * tangent[1], R_case]
    )
    H2_case = sp.Matrix(
        [x5 * r**2, y5 * r**2, r * tangent[2]]
    )
    weighted = sp.Poly(
        sp.expand(
            (
                z * H2_case.jacobian(variables)
                + z**2 * H3_case.jacobian(variables)
                + z**3 * H4_case.jacobian(variables)
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
M = w * p - q
h = sp.expand(L * M)
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(
    L
    * (
        A * p**2
        + (1 - 3 * u) * T * p * q
        + 4 * w * T * q**2
    )
)
alpha = jac(Q, R)
beta = -jac(P, R)
gamma = jac(P, Q)
E = A + T * (w**3 + w)
F = -A * w + 3 * T * u - 5 * T
G = A * u - 3 * A + 12 * T * w**3 - 4 * T * w
D = -16 * A * w + T * (9 * u**2 - 6 * u + 1)
H = (
    12 * A * w**3
    - 4 * A * w
    + T * (7 * u**3 + 9 * u**2 - 3 * u - 5)
)

assert zero(sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) - p * L)
boundary_data = (
    ({A: -w * (u + 1), T: 1}, p * L * M),
    ({A: 3 * u - 5, T: w}, p * L**2),
    ({A: 4 * w * (3 * u - 1), T: 3 - u}, p * q * L),
)
for substitution, expected in boundary_data:
    specialized = (
        alpha.subs(substitution),
        beta.subs(substitution),
        gamma,
    )
    assert zero(
        sp.factor(
            sp.gcd(sp.gcd(specialized[0], specialized[1]), specialized[2])
        )
        - expected
    )
print("PASS three deeper-incidence boundary gcd reruns")

N1 = (
    24 * A * p**2 * w**3
    - 8 * A * p**2 * w
    - 16 * A * p * q * w**2
    - 15 * T * p**2 * w**6
    - 9 * T * p**2 * w**4
    + 75 * T * p**2 * w**2
    + 5 * T * p**2
    + 42 * T * p * q * w**5
    - 84 * T * p * q * w**3
    - 62 * T * p * q * w
    - 24 * T * q**2 * w**4
    + 72 * T * q**2 * w**2,
    -q
    * (
        -16 * A * p * w**2
        - 8 * A * q * w**3
        + 24 * A * q * w
        + 18 * T * p * w**5
        - 36 * T * p * w**3
        + 10 * T * p * w
        - 3 * T * q * w**6
        + 3 * T * q * w**4
        + 23 * T * q * w**2
        - 15 * T * q
    ),
    p * F * D,
)
N2 = (
    -A * p**2 * w**4
    + 6 * A * p**2 * w**2
    - 9 * A * p**2
    + 22 * A * p * q * w**3
    - 2 * A * p * q * w
    - 16 * A * q**2 * w**2
    - 12 * T * p**2 * w**5
    + 40 * T * p**2 * w**3
    - 12 * T * p**2 * w
    - 24 * T * p * q * w**4
    - 16 * T * p * q * w**2
    + 8 * T * p * q
    + 24 * T * q**2 * w**3
    - 8 * T * q**2 * w,
    -q
    * (
        6 * A * p * w**3
        - 18 * A * p * w
        - 5 * A * q * w**4
        - 10 * A * q * w**2
        + 27 * A * q
        + 12 * T * q * w**5
        - 16 * T * q * w**3
        + 4 * T * q * w
    ),
    q * F * D,
)
for tangent in (N1, N2):
    assert zero(
        alpha * tangent[0] + beta * tangent[1] + gamma * tangent[2]
    )

uu = sp.symbols("u0:3")
vv = sp.symbols("v0:3")
tt = sp.symbols("t0:2")
unknown7 = (*uu, *vv, *tt)
E7 = (
    alpha * (uu[0] * p**2 + uu[1] * p * q + uu[2] * q**2)
    + beta * (vv[0] * p**2 + vv[1] * p * q + vv[2] * q**2)
    + gamma * (tt[0] * p + tt[1] * q)
)
M7 = sp.Matrix(
    [
        [equation.coeff(variable) for variable in unknown7]
        for equation in coefficients(E7, 7)
    ]
)
expected_e7_minor = (
    -72
    * (w - 1) ** 2
    * (w + 1) ** 2
    * E**2
    * F**2
    * D
    * G
)
assert zero(
    M7.extract(range(6), range(6)).det(method="domain-ge")
    - expected_e7_minor
)

contact = contact_matrix(P, Q, R, N1, N2)
expected_contact_minor = (
    27648
    * w**5
    * (w - 1) ** 2
    * (w + 1) ** 2
    * (u - 3) ** 2
    * E**2
    * F**4
    * D**3
    * G
    * H
)
assert zero(
    contact.extract(range(1, 6), range(5)).det(method="domain-ge")
    - expected_contact_minor
)
print("PASS generic D*H contact chart")

# Fresh D=0 chart.
S = 9 * u**2 - 6 * u + 1
RD = sp.expand(
    L * (S * p**2 + 16 * w * (1 - 3 * u) * p * q + 64 * u * q**2)
)
N1D = (
    -24
    * w
    * (u - 3)
    * (
        p**2 * w**4
        + 18 * p**2 * u
        + p**2
        - 22 * p * q * w**3
        - 14 * p * q * w
        + 16 * q**2 * u
    ),
    -24
    * q
    * w
    * (u - 3)
    * (
        6 * p * w**3
        - 2 * p * w
        - 5 * q * w**4
        - 2 * q * u
        + 3 * q
    ),
    0,
)
N2D = (
    -8
    * (
        p**2 * w**5
        + p**2 * w**3
        - 4 * p**2 * w
        - 2 * p * q * w**4
        + 3 * p * q * u
        + 3 * p * q
        + q**2 * w**3
        - 3 * q**2 * w
    ),
    -8 * p * q * u * (w - 1) * (w + 1),
    -3
    * (u - 3)
    * (u + 1)
    * (5 * u - 3)
    * (3 * p * u - p - 8 * q * w),
)
contactD = contact_matrix(P, Q, RD, N1D, N2D)
Jpoly = 55 * u**3 + 9 * u**2 - 3 * u - 21
expected_D = (
    41278242816
    * w**5
    * (w - 1) ** 2
    * (w + 1) ** 2
    * (u - 3) ** 7
    * (u + 1) ** 3
    * (3 * u - 1)
    * (5 * u - 3) ** 3
    * (5 * u + 1) ** 4
    * (u**2 + 18 * u + 1)
    * Jpoly
)
assert zero(
    contactD.extract(range(5), range(5)).det(method="domain-ge")
    - expected_D
)

# Fresh H=0 chart.
Kpoly = 7 * u**3 + 9 * u**2 - 3 * u - 5
AH = -Kpoly
TH = 4 * w * (3 * u - 1)
RH = sp.expand(
    L
    * (
        AH * p**2
        + (1 - 3 * u) * TH * p * q
        + 4 * w * TH * q**2
    )
)
F0 = 7 * u**3 + 45 * u**2 - 75 * u + 15
N1H = (
    -4
    * w
    * (
        87 * p**2 * w**8
        + 52 * p**2 * w**6
        - 270 * p**2 * w**4
        + 36 * p**2 * u
        + 15 * p**2
        - 154 * p * q * w**7
        + 258 * p * q * w**5
        + 114 * p * q * w**3
        - 42 * p * q * w
        + 72 * q**2 * w**6
        - 240 * q**2 * w**4
        + 72 * q**2 * u
    ),
    -4
    * q
    * w
    * (
        82 * p * w**7
        - 90 * p * w**5
        + 54 * p * w**3
        - 30 * p * w
        + 5 * q * w**8
        - 12 * q * w**6
        + 6 * q * w**4
        - 60 * q * u
        + 45 * q
    ),
    4 * p * u * F0 * Jpoly,
)
N2H = (
    7 * p**2 * w**10
    - 177 * p**2 * w**8
    + 534 * p**2 * w**6
    - 210 * p**2 * w**4
    + 51 * p**2 * u
    - 45 * p**2
    - 154 * p * q * w**9
    - 472 * p * q * w**7
    - 12 * p * q * w**5
    + 264 * p * q * w**3
    - 42 * p * q * w
    + 112 * q**2 * w**8
    + 432 * q**2 * w**6
    - 240 * q**2 * w**4
    - 48 * q**2 * u,
    q
    * (
        42 * p * w**9
        - 72 * p * w**7
        - 180 * p * w**5
        + 24 * p * w**3
        + 90 * p * w
        - 35 * q * w**10
        - 259 * q * w**8
        + 354 * q * w**6
        + 186 * q * w**4
        - 15 * q * u
        - 135 * q
    ),
    4 * q * u * F0 * Jpoly,
)
contactH = contact_matrix(P, Q, RH, N1H, N2H)
Gpositive = 7 * u**4 - 156 * u**3 + 66 * u**2 - 12 * u + 15
expected_H_minor = (
    294912
    * w**8
    * (w - 1) ** 2
    * (w + 1) ** 2
    * (u + 1) ** 4
    * (11 * u - 9)
    * (5 * u**2 - 6 * u + 5) ** 2
    * F0**4
    * Jpoly**3
    * Gpositive
)
assert zero(
    contactH.extract(range(4), range(4)).det(method="domain-ge")
    - expected_H_minor
)
NX = 49 * u**5 - 987 * u**4 - 3126 * u**3 + 4650 * u**2 + 405 * u - 1215
NY = 343 * u**5 - 165 * u**4 + 1734 * u**3 + 150 * u**2 - 2925 * u + 1215
NZ = 107 * u**4 - 90 * u**3 + 120 * u**2 - 150 * u + 45
kernelH = sp.Matrix(
    [
        -NX / (64 * w**5 * (11 * u - 9) * F0**2 * Jpoly),
        -NY / (32 * w**4 * (u + 1) * (11 * u - 9) * F0**2 * Jpoly),
        -(u - 3)
        * NZ
        / (2 * w**3 * (u + 1) ** 2 * (11 * u - 9) * F0**2 * Jpoly),
        (5 * u - 3)
        * (12 * u**3 - 5 * u**2 + 6 * u - 9)
        / (u * (u + 1) ** 2 * (11 * u - 9)),
        1,
    ]
)
assert all(zero(value) for value in contactH * kernelH)
V = 515 * u**4 - 548 * u**3 + 162 * u**2 - 324 * u + 243
expected_obstruction = (
    3
    * V
    / (
        1024
        * w**8
        * (u + 1) ** 2
        * (11 * u - 9) ** 2
        * F0**2
        * Jpoly**2
    )
)
assert zero(kernelH[1] ** 2 - kernelH[0] * kernelH[2] - expected_obstruction)
print("PASS fresh D=0 and H=0 contact charts")

# The uniform constant E6 block.
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
expected_constant = (
    72
    * (w - 1) ** 2
    * (w + 1) ** 2
    * (u - 3)
    * E**2
    * F
    * G
)
assert zero(
    constant_matrix.extract(range(5), range(5)).det(method="domain-ge")
    - expected_constant
)
print("PASS uniform constant E6 full rank")

# Primitive/content, irreducibility, and exact survivor disjointness.
u_symbol = sp.symbols("U")
V_u = 515 * u_symbol**4 - 548 * u_symbol**3 + 162 * u_symbol**2 - 324 * u_symbol + 243
C_u = (
    47705 * u_symbol**8
    - 413356 * u_symbol**7
    + 546080 * u_symbol**6
    + 294804 * u_symbol**5
    - 623574 * u_symbol**4
    + 87132 * u_symbol**3
    - 152280 * u_symbol**2
    + 362556 * u_symbol
    - 142155
)
assert sp.Poly(V_u, u_symbol).content() == 1
assert sp.Poly(C_u, u_symbol).content() == 1
assert sp.Poly(V_u, u_symbol).is_irreducible
W = sp.expand(V)
assert sp.Poly(W, w).content() == 1
assert sp.Poly(W, w).is_irreducible
assert sp.resultant(V_u, C_u, u_symbol) == 272095271176488581477730636079615180800
assert sp.resultant(
    V_u,
    NX.subs(u, u_symbol),
    u_symbol,
) == 46746446734136993390788608
for denominator_factor in (
    u_symbol,
    u_symbol + 1,
    11 * u_symbol - 9,
    F0.subs(u, u_symbol),
    Jpoly.subs(u, u_symbol),
    Gpositive.subs(u, u_symbol),
):
    assert sp.resultant(V_u, denominator_factor, u_symbol) != 0

# Denominator-cleared Veronese lift on V=0.
lift_c1 = (u + 1) * NX
lift_c2 = 2 * w * NY
lift_lambda = -64 * w**5 * (u + 1) ** 2 * NX * (11 * u - 9) * F0**2 * Jpoly
lift_x5 = (
    -64
    * w**3
    * NX
    * F0**2
    * Jpoly
    * (5 * u - 3)
    * (12 * u**3 - 5 * u**2 + 6 * u - 9)
)
lift_y5 = lift_lambda
lifted_vector = sp.Matrix(
    [lift_c1**2, lift_c1 * lift_c2, lift_c2**2, lift_x5, lift_y5]
)
for value in contactH * lifted_vector:
    assert sp.rem(sp.Poly(sp.expand(value), w), sp.Poly(W, w)) == 0

tangentH = tuple(
    sp.expand(lift_c1 * N1H[index] + lift_c2 * N2H[index])
    for index in range(3)
)
H4_lift = sp.Matrix([P, Q, 0])
H3_lift = sp.Matrix([r * tangentH[0], r * tangentH[1], RH])
H2_lift = sp.Matrix([lift_x5 * r**2, lift_y5 * r**2, r * tangentH[2]])
weighted_lift = sp.Poly(
    sp.expand(
        (
            z * H2_lift.jacobian(variables)
            + z**2 * H3_lift.jacobian(variables)
            + z**3 * H4_lift.jacobian(variables)
        ).det()
    ),
    z,
    r,
    p,
    q,
)
e5_certificate = weighted_lift.coeff_monomial(z**5 * r**2 * p**3)
expected_e5 = (
    -96
    * w**5
    * (u + 1) ** 2
    * F0**3
    * Jpoly
    * Gpositive
    * NX
    * C_u.subs(u_symbol, u)
)
assert zero(e5_certificate - expected_e5)

# Why omitted lower jets cannot change [r^2]E5.  In the (3,1,1)
# partition the r-leading H2 Jacobian has arbitrary lower jets only in
# its upper-left 2x2 block; the mixed determinant with JH4 is
# independent of that block.  In the (2,2,1) partition the r-leading
# JH3 Jacobian is supported in the upper-left 2x2 block, so the mixed
# determinant sees only the fixed (3,3) entry of JH2.  The (3,2,0)
# partition has r-degree at most one.
s = sp.symbols("s")
aa, bb, cc, dd, ee, ff, xx, yy = sp.symbols("aa bb cc dd ee ff xx yy")
top_left_H4 = sp.Matrix(
    [
        [sp.diff(P, p), sp.diff(P, q), 0],
        [sp.diff(Q, p), sp.diff(Q, q), 0],
        [0, 0, 0],
    ]
)
leading_H2 = sp.Matrix(
    [[aa, bb, 2 * xx], [cc, dd, 2 * yy], [ee, ff, 0]]
)
mixed_311 = sp.Poly(
    sp.expand((leading_H2 + s * top_left_H4).det()), s
).coeff_monomial(s)
assert all(sp.diff(mixed_311, variable) == 0 for variable in (aa, bb, cc, dd))

arbitrary = sp.symbols("b00:09")
arbitrary_H2 = sp.Matrix(3, 3, arbitrary)
leading_H3 = sp.Matrix(
    [
        [sp.diff(tangentH[0], p), sp.diff(tangentH[0], q), 0],
        [sp.diff(tangentH[1], p), sp.diff(tangentH[1], q), 0],
        [0, 0, 0],
    ]
)
mixed_221 = sp.Poly(
    sp.expand((arbitrary_H2 + s * leading_H3).det()), s
).coeff_monomial(s**2)
assert all(
    sp.diff(mixed_221, arbitrary[index]) == 0
    for index in range(9)
    if index != 8
)
print("PASS primitive quartic survivor and top-only E5 obstruction")
print("ALL INTERIOR FIXED/CONTACT {1,1} EXCLUSION CHECKS PASSED")

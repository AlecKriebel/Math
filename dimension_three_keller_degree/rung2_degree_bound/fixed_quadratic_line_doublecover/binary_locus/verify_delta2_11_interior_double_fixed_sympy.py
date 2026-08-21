#!/usr/bin/env python3
"""Exact E6 exclusion for the squarefree-interior doubled fixed root."""

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
R = sp.expand(L**2 * (A * p + B * q))
alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
assert zero(sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)) - L**2)

boundary_data = (
    ({A: -w, B: 1}, L**2 * Mfixed),
    ({A: 4 * w, B: 5 * w**2 - 3}, q * L**2),
    ({A: 5 - 3 * w**2, B: 4 * w}, p * L**2),
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
print("PASS three deeper-incidence boundary gcd reruns")

other_root = A + B * w
pivot = A * w + B
left_contact = 5 * A * w**2 - 3 * A - 4 * B * w
right_contact = 4 * A * w + 3 * B * w**2 - 5 * B

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
    - 360
    * other_root**2
    * (w - 1) ** 2
    * (w + 1) ** 2
    * pivot**2
    * right_contact
    * left_contact
)

N1 = (
    p
    * (
        4 * A * p * w
        + 27 * B * p * w**2
        - 5 * B * p
        - 18 * B * q * w
    ),
    -q
    * (
        8 * A * p * w**2
        - 12 * A * q * w
        - 10 * B * p * w
        - 9 * B * q * w**2
        + 15 * B * q
    ),
    5 * p * pivot**2,
)
N2 = (
    -p
    * (
        15 * A * p * w**2
        - 9 * A * p
        - 10 * A * q * w
        - 12 * B * p * w
        + 8 * B * q
    ),
    -q
    * (
        18 * A * p * w
        + 5 * A * q * w**2
        - 27 * A * q
        - 4 * B * q * w
    ),
    5 * q * pivot**2,
)
for tangent in (N1, N2):
    assert zero(
        alpha * tangent[0]
        + beta * tangent[1]
        + gamma * tangent[2]
    )
contact = contact_matrix(P, Q, R, N1, N2)

Q1 = (
    108 * A**3 * w**5
    - 266 * A**3 * w**3
    + 216 * A**2 * B * w**6
    - 855 * A**2 * B * w**4
    + 165 * A**2 * B * w**2
    + 108 * A * B**2 * w**7
    - 972 * A * B**2 * w**5
    + 450 * A * B**2 * w**3
    - 60 * A * B**2 * w
    - 378 * B**3 * w**6
    + 270 * B**3 * w**4
    - 45 * B**3 * w**2
    - 5 * B**3
)
Q2 = (
    127 * A**3 * w**4
    - 285 * A**3 * w**2
    + 294 * A**2 * B * w**5
    - 954 * A**2 * B * w**3
    + 186 * A**2 * B * w
    + 162 * A * B**2 * w**6
    - 978 * A * B**2 * w**4
    + 357 * A * B**2 * w**2
    - 15 * A * B**2
    - 324 * B**3 * w**5
    + 186 * B**3 * w**3
    - 20 * B**3 * w
)
Q3 = (
    20 * A**3 * w**5
    - 186 * A**3 * w**3
    + 324 * A**3 * w
    + 15 * A**2 * B * w**6
    - 357 * A**2 * B * w**4
    + 978 * A**2 * B * w**2
    - 162 * A**2 * B
    - 186 * A * B**2 * w**5
    + 954 * A * B**2 * w**3
    - 294 * A * B**2 * w
    + 285 * B**3 * w**4
    - 127 * B**3 * w**2
)
Q4 = (
    5 * A**3 * w**7
    + 45 * A**3 * w**5
    - 270 * A**3 * w**3
    + 378 * A**3 * w
    + 60 * A**2 * B * w**6
    - 450 * A**2 * B * w**4
    + 972 * A**2 * B * w**2
    - 108 * A**2 * B
    - 165 * A * B**2 * w**5
    + 855 * A * B**2 * w**3
    - 216 * A * B**2 * w
    + 266 * B**3 * w**4
    - 108 * B**3 * w**2
)
base = (
    1920000
    * (w - 1) ** 3
    * (w + 1) ** 3
    * pivot**6
    * right_contact
    * left_contact
)
expected_minors = (
    (1, base * w**2 * Q1),
    (2, -base * w**2 * Q2),
    (3, -base * w**2 * Q3),
    (4, base * w * Q4),
)
for omitted, expected in expected_minors:
    rows = [index for index in range(6) if index != omitted]
    assert zero(contact.extract(rows, range(5)).det() - expected)
print("PASS four residual contact-minor identities")

q1 = sp.expand(Q1.subs(B, 1))
q2 = sp.expand(Q2.subs(B, 1))
q3 = sp.expand(Q3.subs(B, 1))
q4 = sp.expand(Q4.subs(B, 1))
resultants = (
    sp.resultant(q1, q2, A),
    sp.resultant(q1, q3, A),
    sp.resultant(q1, q4, A),
    sp.resultant(q2, q3, A),
)
expected_resultants = (
    637729200
    * w**6
    * (w - 1) ** 12
    * (w + 1) ** 12
    * (12 * w**4 + 28 * w**2 - 57),
    -318864600
    * w**3
    * (w - 1) ** 12
    * (w + 1) ** 12
    * (w**2 + 3) ** 2
    * (18 * w**4 - 27 * w**2 - 8),
    1434890700
    * w**3
    * (w - 1) ** 12
    * (w + 1) ** 12
    * (
        14 * w**12
        + 28 * w**10
        + 77 * w**8
        - 34 * w**6
        + 77 * w**4
        + 28 * w**2
        + 14
    ),
    -159432300
    * w**4
    * (w - 1) ** 12
    * (w + 1) ** 12
    * (23 * w**4 - 114 * w**2 + 23),
)
for actual, expected in zip(resultants, expected_resultants):
    assert zero(actual - expected)
resultant_gcd = sp.Poly(sp.gcd_list(resultants), w).monic().as_expr()
assert zero(
    resultant_gcd - w**3 * (w - 1) ** 12 * (w + 1) ** 12
)
endpoint_gcd = sp.Poly(
    sp.gcd(Q1.subs({A: 1, B: 0}), Q2.subs({A: 1, B: 0})),
    w,
).monic().as_expr()
assert zero(endpoint_gcd - w**2)
print("PASS projective contact-rank cover by resultants and endpoint gcd")

pivot_substitution = {A: 1, B: -w}
pivot_R = sp.expand(R.subs(pivot_substitution))
pivot_alpha = sp.expand(alpha.subs(pivot_substitution))
pivot_beta = sp.expand(beta.subs(pivot_substitution))
pivot_M7 = M7.subs(pivot_substitution)
assert zero(
    pivot_M7.extract(range(6), (0, 1, 2, 3, 4, 6)).det()
    + 5832
    * w**2
    * (w - 1) ** 4
    * (w + 1) ** 4
    * (w**2 - 3) ** 2
    * (3 * w**2 - 1)
)
pivot_N1 = (
    9 * p * w * (3 * p * w**2 - p - 2 * q * w),
    9 * q * w * (2 * p * w + q * w**2 - 3 * q),
    0,
)
pivot_N2 = (
    8 * p * (4 * p * w - 3 * q),
    8 * p * q * w**2,
    -9 * L * (w**2 - 3),
)
for tangent in (pivot_N1, pivot_N2):
    assert zero(
        pivot_alpha * tangent[0]
        + pivot_beta * tangent[1]
        + gamma * tangent[2]
    )
pivot_contact = contact_matrix(P, Q, pivot_R, pivot_N1, pivot_N2)
assert zero(
    pivot_contact.extract(range(5), range(5)).det()
    - 48977602560
    * w**5
    * (w - 1) ** 6
    * (w + 1) ** 6
    * (w**2 - 3) ** 4
    * (3 * w**2 - 1)
)
print("PASS fresh triple-fixed pivot chart has full contact rank")

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
    + 216
    * other_root**2
    * (w - 1) ** 2
    * (w + 1) ** 2
    * right_contact
    * left_contact
)
print("PASS constant E6 full rank and all-binary exit")
print("ALL INTERIOR DOUBLE-FIXED {1,1} EXCLUSION CHECKS PASSED")

#!/usr/bin/env python3
"""Exact full-lower E6 elimination for canonical family D4-DN-3.

This verifier never specializes the eleven binary coefficients of U0,V0,T0
to zero.  It first computes the contact elimination ideal and its radical.
It then reconstructs all thirteen E6 coefficient equations with all eighteen
lower variables and certifies a specialization-safe rank atlas over the two
geometric contact planes.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, weight = sp.symbols("p q r weight")
coords = (p, q, r)
sqrt2 = sp.sqrt(2)


def jac2(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def weighted_determinant(P, Q, R, U, V, T, A, B, linear):
    H2 = sp.Matrix([A, B, T])
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    return sp.Poly(
        sp.expand(
            (
                linear
                + weight * H2.jacobian(coords)
                + weight**2 * H3.jacobian(coords)
                + weight**3 * H4.jacobian(coords)
            ).det()
        ),
        weight,
    )


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = (p + q) ** 3
alpha = jac2(Q, R)
beta = -jac2(P, R)
gamma = jac2(P, Q)
assert sp.factor(alpha) == -6 * q * (p + q) ** 4
assert sp.factor(beta) == -6 * p * (p + q) ** 4
assert sp.factor(gamma) == 8 * p * q * (p + q) ** 4

# Complete E7 contact coordinates.  The r^3 coefficients of U,V vanish;
# the r^2 and r^1 blocks have nullities two and four.
d, z, x, y, a, b = sp.symbols("d z x y a b")
U2 = (4 * z - 3 * d) * p / 3
V2 = d * q
T2 = z
U1 = (4 * a - 3 * x) * p**2 / 3 + (4 * b - 3 * y) * p * q / 3
V1 = x * p * q + y * q**2
T1 = a * p + b * q
assert sp.expand(alpha * U2 + beta * V2 + gamma * T2) == 0
assert sp.expand(alpha * U1 + beta * V1 + gamma * T1) == 0

u3, v3 = sp.symbols("u3 v3")
e7_r2_matrix, _ = sp.linear_eq_to_matrix(
    sp.Poly(alpha * u3 + beta * v3, p, q).coeffs(), (u3, v3)
)
assert e7_r2_matrix.rank() == 2
u20, u21, v20, v21, t20 = sp.symbols("u20 u21 v20 v21 t20")
e7_r1_matrix, _ = sp.linear_eq_to_matrix(
    sp.Poly(
        alpha * (u20 * p + u21 * q)
        + beta * (v20 * p + v21 * q)
        + gamma * t20,
        p,
        q,
    ).coeffs(),
    (u20, u21, v20, v21, t20),
)
assert e7_r1_matrix.rank() == 3
u10, u11, u12, v10, v11, v12, t10, t11 = sp.symbols(
    "u10 u11 u12 v10 v11 v12 t10 t11"
)
e7_r0_matrix, _ = sp.linear_eq_to_matrix(
    sp.Poly(
        alpha * (u10 * p**2 + u11 * p * q + u12 * q**2)
        + beta * (v10 * p**2 + v11 * p * q + v12 * q**2)
        + gamma * (t10 * p + t11 * q),
        p,
        q,
    ).coeffs(),
    (u10, u11, u12, v10, v11, v12, t10, t11),
)
assert e7_r0_matrix.rank() == 4
assert (2 - 2) + (5 - 3) + (8 - 4) == 6

# E6 at r-degree three is lower-variable-free and forces d=z=0.
contact_det = weighted_determinant(
    P,
    Q,
    R,
    r * U1 + r**2 * U2,
    r * V1 + r**2 * V2,
    r * T1 + r**2 * T2,
    0,
    0,
    sp.zeros(3),
)
contact_e6 = sp.Poly(contact_det.coeff_monomial(weight**6), p, q, r)
expected_r3 = {
    p**0 * q**3 * r**3: sp.Rational(2, 3) * (-3 * d + 4 * z) ** 2,
    p * q**2 * r**3: 2 * (9 * d**2 - 16 * d * z + 8 * z**2),
    p**2 * q * r**3: sp.Rational(2, 3) * (27 * d**2 - 24 * d * z + 8 * z**2),
    p**3 * r**3: 6 * d**2,
}
for monomial, expected in expected_r3.items():
    assert sp.factor(contact_e6.coeff_monomial(monomial) - expected) == 0
assert sp.solve((d, -3 * d + 4 * z), (d, z), dict=True) == [{d: 0, z: 0}]

# Eliminate the only lower variables that occur in E6 at r-degree one:
# the r^2 coefficients ar,br of A,B.
ar, br = sp.symbols("ar br")
line_det = weighted_determinant(
    P,
    Q,
    R,
    r * U1,
    r * V1,
    r * T1,
    ar * r**2,
    br * r**2,
    sp.zeros(3),
)
line_e6 = sp.Poly(line_det.coeff_monomial(weight**6), p, q, r)
line_equations = [
    line_e6.coeff_monomial(p**i * q ** (5 - i) * r) for i in range(6)
]
elimination_groebner = sp.groebner(
    line_equations, ar, br, a, b, x, y, order="lex", domain=sp.QQ
)
elimination_generators = tuple(
    polynomial.as_expr()
    for polynomial in elimination_groebner.polys
    if not ({ar, br} & polynomial.as_expr().free_symbols)
)
assert len(elimination_generators) == 6

# Set-theoretic radical certificate.  J is the elimination ideal.  Every
# generator of J lies in I=(a-b,f), while (a-b)^2 and f^2 lie in J.
wxy = x - y
plane_product = 8 * a**2 + 24 * a * wxy + 9 * wxy**2
candidate_ideal = sp.groebner(
    (a - b, plane_product), a, b, x, y, order="grevlex", domain=sp.QQ
)
assert all(
    candidate_ideal.reduce(generator)[1] == 0
    for generator in elimination_generators
)
elimination_ideal = sp.groebner(
    elimination_generators, a, b, x, y, order="grevlex", domain=sp.QQ
)
assert elimination_ideal.reduce((a - b) ** 2)[1] == 0
assert elimination_ideal.reduce(plane_product**2)[1] == 0
assert sp.expand(
    plane_product
    - (3 * wxy + (4 + 2 * sqrt2) * a)
    * (3 * wxy + (4 - 2 * sqrt2) * a)
) == 0

# Restore all 18 lower variables:
#   six nonbinary A,B coefficients, L_33, and all 11 binary U0,V0,T0
# coefficients.  No binary coefficient is specialized.
mon3_binary = (p**3, p**2 * q, p * q**2, q**3)
mon2_binary = (p**2, p * q, q**2)
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
uc = sp.symbols("uc0:4")
vc = sp.symbols("vc0:4")
tc = sp.symbols("tc0:3")
ac = sp.symbols("ac0:6")
bc = sp.symbols("bc0:6")
ell = sp.symbols("ell0:9")
U0 = sum(value * monomial for value, monomial in zip(uc, mon3_binary))
V0 = sum(value * monomial for value, monomial in zip(vc, mon3_binary))
T0 = sum(value * monomial for value, monomial in zip(tc, mon2_binary))
Afull = sum(value * monomial for value, monomial in zip(ac, mon2))
Bfull = sum(value * monomial for value, monomial in zip(bc, mon2))
L = sp.Matrix(3, 3, ell)
lower18 = (
    ac[2],
    ac[4],
    ac[5],
    bc[2],
    bc[4],
    bc[5],
    ell[8],
) + uc + vc + tc
assert len(lower18) == 18

s, k = sp.symbols("s k")
cplus = (-4 + 2 * sqrt2) / 3
Uplus = sp.expand((4 * k - 3 * (s + cplus * k)) * p**2 / 3 + (4 * k - 3 * s) * p * q / 3)
Vplus = sp.expand((s + cplus * k) * p * q + s * q**2)
Tplus = k * (p + q)
full_det = weighted_determinant(
    P,
    Q,
    R,
    U0 + r * Uplus,
    V0 + r * Vplus,
    T0 + r * Tplus,
    Afull,
    Bfull,
    L,
)
assert all(full_det.coeff_monomial(weight**degree) == 0 for degree in (9, 8, 7))
full_e6 = sp.Poly(full_det.coeff_monomial(weight**6), p, q, r)
expected_monomials = (
    (6, 0, 0),
    (5, 1, 0),
    (5, 0, 1),
    (4, 2, 0),
    (4, 1, 1),
    (3, 3, 0),
    (3, 2, 1),
    (2, 4, 0),
    (2, 3, 1),
    (1, 5, 0),
    (1, 4, 1),
    (0, 6, 0),
    (0, 5, 1),
)
assert tuple(full_e6.monoms()) == expected_monomials
full_matrix, full_rhs = sp.linear_eq_to_matrix(full_e6.coeffs(), lower18)
assert full_matrix.shape == (13, 18)

# Specialization-safe pivot atlas.  The first pivot is independent of s,
# so it covers the whole k != 0 part of the plus plane, including the line
# missed by the earlier denominator.  The minus plane is its Galois
# conjugate.
rows7 = (0, 1, 2, 3, 4, 5, 7)
cols7 = (0, 1, 2, 3, 5, 7, 8)
pivot7 = sp.factor(
    full_matrix[list(rows7), list(cols7)].det(), extension=sqrt2
)
assert sp.expand(pivot7 - 373248 * (7 - 5 * sqrt2) * k**2) == 0
assert full_matrix.rank() == 7
assert full_matrix.row_join(full_rhs).rank() == 7

# The two planes meet at k=0.  Recompute, rather than specialize a
# k-pivoted solution.  The nonzero intersection and the origin have ranks
# six and five, respectively.
intersection_matrix = full_matrix.subs(k, 0)
intersection_rhs = full_rhs.subs(k, 0)
rows6 = (0, 1, 2, 3, 4, 5)
cols6 = (0, 1, 2, 3, 5, 7)
pivot6 = sp.factor(
    intersection_matrix[list(rows6), list(cols6)].det(), extension=sqrt2
)
assert sp.expand(pivot6 + 279936 * s) == 0
assert intersection_matrix.rank() == 6
assert intersection_matrix.row_join(intersection_rhs).rank() == 6

origin_matrix = intersection_matrix.subs(s, 0)
origin_rhs = intersection_rhs.subs(s, 0)
rows5 = (0, 1, 2, 3, 4)
cols5 = (0, 1, 2, 3, 5)
pivot5 = origin_matrix[list(rows5), list(cols5)].det()
assert pivot5 == 31104
assert origin_matrix.rank() == 5
assert origin_matrix.row_join(origin_rhs).rank() == 5

# Galois conjugation gives the identical atlas on the second plane.
assert sp.factor(
    pivot7.xreplace({sqrt2: -sqrt2})
    - 373248 * (7 + 5 * sqrt2) * k**2
) == 0
assert 7 + 5 * sqrt2 != 0

print("D4_DN3_FULL_E6_ELIMINATION_PASS_TWO_PLANES_18_LOWER")

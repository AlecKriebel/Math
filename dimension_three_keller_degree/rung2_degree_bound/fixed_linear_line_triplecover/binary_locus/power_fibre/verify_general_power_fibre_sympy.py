#!/usr/bin/env python3
"""Exact primary certificate for the fixed-linear binary power fibre."""

from __future__ import annotations

import sympy as sp

import explore_general_power_fibre as D


if not __debug__:
    raise RuntimeError("assertions must remain enabled")

p, q, r = D.p, D.q, D.r
c, u, v, d, x, l = D.c, D.u, D.v, D.d, D.x, D.l
w = sp.symbols("w")


def coefficient(degree: int, r_power: int, substitutions) -> sp.Expr:
    return sp.factor(
        sp.Poly(D.E[degree].as_expr(), r)
        .coeff_monomial(r**r_power)
        .subs(substitutions)
    )


def assert_same(left, right) -> None:
    assert sp.factor(sp.together(left - right)) == 0


def exact_zero(value) -> bool:
    numerator = sp.together(value).as_numer_denom()[0]
    return sp.Poly(sp.expand(numerator), p, q, r).is_zero


# A shear in q and a target scaling normalize the coprime companion to
# C3=d0*p^3+d1*p^2*q+q^3.  Coprimality with p^3 is exactly d3!=0.
normal = {d[2]: 0, d[3]: 1}
Dq = d[1] * p**2 + 3 * q**2

assert D.E[8].is_zero and D.E[7].is_zero
assert_same(
    coefficient(6, 3, normal),
    sp.Rational(8, 3) * p * D.tt**2 * Dq,
)

# ---------------------------------------------------------------------------
# v9 != 0.
# ---------------------------------------------------------------------------

v9_top = {
    **normal,
    D.tt: 0,
    D.tq: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: sp.Rational(4, 3) * c[2],
    u[3]: 0,
    D.aa: sp.Rational(2, 9) * D.tp**2,
}
assert exact_zero(coefficient(6, 2, v9_top))
assert exact_zero(coefficient(6, 1, v9_top))
assert exact_zero(coefficient(5, 4, v9_top))

e6_r0_v9 = coefficient(6, 0, v9_top)
bracket = (
    -9 * D.ap * p**2
    - 9 * D.aq * p * q
    - 8 * c[0] * p**2 * D.tp
    + 4 * c[1] * p * q * D.tp
    + 4 * c[2] * q**2 * D.tp
    + 12 * l[8] * p**2
    + 9 * p**2 * D.tp * u[0]
)
assert_same(e6_r0_v9, p**2 * Dq * bracket / 3)

v9_e6 = {
    **v9_top,
    D.ap: (12 * l[8] + D.tp * (9 * u[0] - 8 * c[0])) / 9,
    D.aq: sp.Rational(4, 9) * c[1] * D.tp,
}
e5_r2_v9 = sp.Poly(coefficient(5, 2, v9_e6), p, q)
assert_same(
    e5_r2_v9.coeff_monomial(q**3),
    -8 * c[2] ** 2 * v[9],
)

v9_c2_zero = {**v9_e6, c[2]: 0, u[2]: 0}
e5_r2_c20 = sp.Poly(coefficient(5, 2, v9_c2_zero), p, q)
assert_same(
    e5_r2_c20.coeff_monomial(p * q**2),
    -sp.Rational(4, 3) * D.tp**3,
)

v9_tp_zero = {
    **normal,
    D.tt: 0,
    D.tq: 0,
    D.tp: 0,
    D.aa: 0,
    c[2]: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: 0,
    u[3]: 0,
    D.ap: sp.Rational(4, 3) * l[8],
    D.aq: 0,
    x[1]: (
        sp.Rational(4, 3) * l[7]
        - c[1] * (8 * c[0] - 9 * u[0]) / 9
    ),
    x[2]: sp.Rational(2, 9) * c[1] ** 2,
}
assert exact_zero(coefficient(6, 0, v9_tp_zero))
assert exact_zero(coefficient(5, 3, v9_tp_zero))
assert exact_zero(coefficient(5, 2, v9_tp_zero))
assert exact_zero(coefficient(5, 1, v9_tp_zero))
assert_same(
    coefficient(5, 0, v9_tp_zero),
    p**2
    * Dq
    * (
        -8 * c[0] * l[8] * p
        + 4 * c[1] * l[8] * q
        - 9 * l[2] * p
        + 9 * l[8] * u[0] * p
    )
    / 3,
)

e4_r2_v9 = sp.Poly(coefficient(4, 2, v9_tp_zero), p, q)
assert_same(
    e4_r2_v9.coeff_monomial(q**2),
    sp.Rational(4, 3) * c[1] ** 3 * v[9],
)

v9_c1_zero = {
    **v9_tp_zero,
    c[1]: 0,
    u[1]: 0,
    x[1]: sp.Rational(4, 3) * l[7],
    x[2]: 0,
    l[2]: l[8] * (u[0] - sp.Rational(8, 9) * c[0]),
    l[1]: l[7] * (u[0] - sp.Rational(8, 9) * c[0]),
}
assert_same(
    coefficient(4, 1, v9_c1_zero),
    sp.Rational(4, 3) * l[8] ** 2 * p * Dq,
)

v9_singular = {
    **v9_c1_zero,
    l[8]: 0,
    D.ap: 0,
    l[2]: 0,
}
e3_r2_v9 = sp.Poly(coefficient(3, 2, v9_singular), p, q)
assert_same(
    e3_r2_v9.coeff_monomial(q), -4 * l[7] ** 2 * v[9]
)

# ---------------------------------------------------------------------------
# v9=0 and ell=v7*p+v8*q != 0.
# ---------------------------------------------------------------------------

ell_top = {
    **normal,
    D.tt: 0,
    D.tq: 0,
    v[9]: 0,
    D.aa: sp.Rational(2, 9) * D.tp**2,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: sp.Rational(4, 3) * c[2],
    u[3]: 0,
}
assert exact_zero(coefficient(6, 1, ell_top))
assert exact_zero(coefficient(5, 3, ell_top))
assert_same(
    coefficient(6, 0, ell_top), p**2 * Dq * bracket / 3
)

ell_e6 = {
    **ell_top,
    D.ap: (12 * l[8] + D.tp * (9 * u[0] - 8 * c[0])) / 9,
    D.aq: sp.Rational(4, 9) * c[1] * D.tp,
}
e5_r2_ell = sp.Poly(coefficient(5, 2, ell_e6), p, q)
assert_same(
    e5_r2_ell.coeff_monomial(p * q**2),
    -sp.Rational(4, 3) * D.tp * (3 * c[2] * v[8] + D.tp**2),
)
# E6 has c2*tp=0, so the preceding coefficient forces tp=0.

ell_tp_zero = {
    **normal,
    D.tt: 0,
    D.tq: 0,
    D.tp: 0,
    D.aa: 0,
    v[9]: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: sp.Rational(4, 3) * c[2],
    u[3]: 0,
    D.ap: sp.Rational(4, 3) * l[8],
    D.aq: 0,
}
e5_r1_ell = coefficient(5, 1, ell_tp_zero)
K = (
    8 * c[0] * c[1] * p**3
    + 16 * c[0] * c[2] * p**2 * q
    - 4 * c[1] ** 2 * p**2 * q
    - 12 * c[1] * c[2] * p * q**2
    - 9 * c[1] * u[0] * p**3
    - 8 * c[2] ** 2 * q**3
    - 18 * c[2] * u[0] * p**2 * q
    - 12 * l[7] * p**3
    + 9 * x[1] * p**3
    + 18 * x[2] * p**2 * q
)
assert_same(e5_r1_ell, sp.Rational(2, 3) * (p * v[7] + q * v[8]) * K)

ell_e5 = {
    **ell_tp_zero,
    c[2]: 0,
    u[2]: 0,
    x[1]: (
        sp.Rational(4, 3) * l[7]
        - c[1] * (8 * c[0] - 9 * u[0]) / 9
    ),
    x[2]: sp.Rational(2, 9) * c[1] ** 2,
}
assert exact_zero(coefficient(5, 1, ell_e5))
assert_same(
    coefficient(5, 0, ell_e5),
    p**2
    * Dq
    * (
        -8 * c[0] * l[8] * p
        + 4 * c[1] * l[8] * q
        - 9 * l[2] * p
        + 9 * l[8] * u[0] * p
    )
    / 3,
)

# v8!=0: E4 first forces c1=0, then l33=0.
e4_r1_ell = sp.Poly(coefficient(4, 1, ell_e5), p, q)
assert_same(
    e4_r1_ell.coeff_monomial(q**3),
    sp.Rational(8, 9) * c[1] ** 3 * v[8],
)
ell_c1_zero = {
    **ell_e5,
    c[1]: 0,
    u[1]: 0,
    x[1]: sp.Rational(4, 3) * l[7],
    x[2]: 0,
    l[2]: l[8] * (u[0] - sp.Rational(8, 9) * c[0]),
}
e4_r1_c10 = sp.Poly(coefficient(4, 1, ell_c1_zero), p, q)
assert_same(e4_r1_c10.coeff_monomial(p * q**2), 4 * l[8] ** 2)

# v8=0,v7!=0: E5 gives c1*l33=0, while E4 has the
# displayed expression; its middle term therefore vanishes.
assert_same(
    e4_r1_ell.coeff_monomial(p * q**2).subs({v[8]: 0}),
    sp.Rational(4, 9)
    * (
        2 * c[1] ** 3 * v[7]
        + 3 * c[1] * l[8] * v[6]
        + 9 * l[8] ** 2
    ),
)

ell_singular = {
    **ell_c1_zero,
    l[8]: 0,
    D.ap: 0,
    l[2]: 0,
    l[1]: l[7] * (u[0] - sp.Rational(8, 9) * c[0]),
}
e3_r1_ell = sp.Poly(coefficient(3, 1, ell_singular), p, q)
assert_same(
    e3_r1_ell.coeff_monomial(q**2),
    -sp.Rational(8, 3) * l[7] ** 2 * v[8],
)
assert_same(
    e3_r1_ell.coeff_monomial(p * q).subs({v[8]: 0}),
    -sp.Rational(8, 3) * l[7] ** 2 * v[7],
)

# ---------------------------------------------------------------------------
# v9=0 and ell=0.
# ---------------------------------------------------------------------------

ell_zero = {
    **normal,
    D.tt: 0,
    D.tq: 0,
    v[9]: 0,
    v[7]: 0,
    v[8]: 0,
    D.aa: sp.Rational(2, 9) * D.tp**2,
}
assert exact_zero(coefficient(6, 1, ell_zero))
assert_same(
    coefficient(5, 2, ell_zero),
    -sp.Rational(4, 9) * p * D.tp**3 * Dq,
)

zero_leaf = {
    **normal,
    D.tt: 0,
    D.tq: 0,
    D.tp: 0,
    D.aa: 0,
    v[9]: 0,
    v[7]: 0,
    v[8]: 0,
}
source = sp.Matrix((p, q, r))
F = sp.expand(D.L * source + D.H2 + D.H3 + D.H4)
F0 = sp.Matrix([sp.expand(component.subs(zero_leaf)) for component in F])
G = sp.expand(F0[2].subs({r: 0}))
assert sp.expand(F0[2] - (l[8] * r + G)) == 0

r_from_w = (w - G) / l[8]
plane_l33 = [
    sp.together(F0[index].subs({r: r_from_w})) for index in (0, 1)
]
degrees_l33 = [
    sp.Poly(expression.as_numer_denom()[0], p, q).total_degree()
    for expression in plane_l33
]
assert max(degrees_l33) <= 6

coordinate_leaf = {
    **zero_leaf,
    l[8]: 0,
    c[1]: 0,
    c[2]: 0,
}
F_coordinate = sp.Matrix(
    [sp.expand(component.subs(coordinate_leaf)) for component in F]
)
q_from_w = (w - p**3 - c[0] * p**2 - l[6] * p) / l[7]
plane_l32 = [
    sp.together(F_coordinate[index].subs({q: q_from_w}))
    for index in (0, 1)
]
degrees_l32 = [
    sp.Poly(expression.as_numer_denom()[0], p, r).total_degree()
    for expression in plane_l32
]
assert max(degrees_l32) <= 10
assert sp.expand(F_coordinate[2].subs({q: q_from_w}) - w) == 0

print("PASS general fixed-linear power fibre: v9!=0 excluded")
print("PASS general fixed-linear power fibre: v9=0, ell!=0 excluded")
print(f"PASS ell=0 coordinate exits have plane degrees {max(degrees_l33)} and {max(degrees_l32)}")
print("ALL GENERAL FIXED-LINEAR POWER-FIBRE CHECKS PASSED")

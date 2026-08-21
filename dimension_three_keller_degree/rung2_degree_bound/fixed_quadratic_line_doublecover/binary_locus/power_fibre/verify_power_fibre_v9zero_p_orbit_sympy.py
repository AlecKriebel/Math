#!/usr/bin/env python3
"""Exact exclusion of the ell=p orbit on the v9=0 power fibre."""

from __future__ import annotations

import sympy as sp

import explore_power_fibre_v9zero as D


if not __debug__:
    raise RuntimeError("assertions must remain enabled")

p, q, r = D.p, D.q, D.r
c, u, v, x, y, l = D.c, D.u, D.v, D.x, D.y, D.l


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


orbit = {v[9]: 0, v[7]: 1, v[8]: 0, D.tt: 0}

# E5[r^3] forces tq=0.
assert_same(
    coefficient(5, 3, orbit),
    -sp.Rational(8, 3) * p * D.tq * (p * D.tp + q * D.tq),
)

# E6[r] then gives u1=4c1/3, u3=0 and the displayed u2 relation.
top = {
    **orbit,
    D.tq: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: D.aa + sp.Rational(4, 3) * c[2] - sp.Rational(2, 9) * D.tp**2,
    u[3]: 0,
}
assert exact_zero(coefficient(6, 1, top))

e6_r0 = sp.Poly(coefficient(6, 0, top), p, q)
e5_r2 = sp.Poly(coefficient(5, 2, top), p, q)
e6_last = sp.factor(e6_r0.coeff_monomial(p**3 * q**3))
e5_last = sp.factor(e5_r2.coeff_monomial(p**2 * q))
assert_same(
    e5_last + 2 * e6_last,
    -2 * D.tp * (27 * D.aa - 2 * D.tp**2) / 9,
)

# ---------------------------------------------------------------------------
# tp != 0.
# ---------------------------------------------------------------------------

tp_nonzero = {
    **orbit,
    D.tq: 0,
    c[0]: 0,
    c[1]: 0,
    D.aa: sp.Rational(2, 27) * D.tp**2,
    c[2]: -D.tp**2 / 9 + D.tp * v[6] / 3,
    u[1]: 0,
    u[2]: sp.Rational(4, 9) * D.tp * v[6] - sp.Rational(8, 27) * D.tp**2,
    u[3]: 0,
    D.ap: (
        sp.Rational(4, 3) * l[8]
        - sp.Rational(4, 27) * D.tp**2 * v[4]
        + D.tp * u[0]
    ),
    D.aq: -sp.Rational(4, 27) * D.tp**2 * v[5],
}
assert exact_zero(coefficient(6, 1, tp_nonzero))
assert exact_zero(coefficient(6, 0, tp_nonzero))
assert exact_zero(coefficient(5, 2, tp_nonzero))

e5_r1_tp = sp.Poly(coefficient(5, 1, tp_nonzero), p, q)
assert_same(
    e5_r1_tp.coeff_monomial(p * q**3),
    -sp.Rational(16, 81)
    * D.tp**2
    * (D.tp**2 - D.tp * v[6] + 3 * v[6] ** 2),
)
e4_r3_tp = sp.Poly(coefficient(4, 3, tp_nonzero), p, q)
assert_same(
    e4_r3_tp.coeff_monomial(p),
    -sp.Rational(8, 27) * D.tp**3 * v[5],
)
assert_same(
    e4_r3_tp.coeff_monomial(q),
    -sp.Rational(8, 243) * D.tp**3 * (D.tp + 6 * v[6]),
)
assert_same(
    e5_r1_tp.coeff_monomial(p * q**3).subs({v[6]: -D.tp / 6}),
    -sp.Rational(20, 81) * D.tp**4,
)

# ---------------------------------------------------------------------------
# tp = 0.  The last E6/E5 equations say aa*v6=0.
# ---------------------------------------------------------------------------

tp_zero_top = {
    **orbit,
    D.tq: 0,
    D.tp: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: D.aa + sp.Rational(4, 3) * c[2],
    u[3]: 0,
    D.ap: D.aa * v[4] + sp.Rational(4, 3) * l[8],
    D.aq: D.aa * v[5],
}
assert_same(
    sp.Poly(coefficient(6, 0, tp_zero_top), p, q).coeff_monomial(
        p**3 * q**3
    ),
    6 * D.aa * v[6],
)

# aa != 0, hence v6=0.  E4[r^3] first forces c1=c2=0.
aa_nonzero = {**tp_zero_top, v[6]: 0}
e4_r3_aa = sp.Poly(coefficient(4, 3, aa_nonzero), p, q)
assert_same(e4_r3_aa.coeff_monomial(p), 2 * D.aa * c[1])
assert_same(e4_r3_aa.coeff_monomial(q), 4 * D.aa * c[2])

aa_e5 = {
    **aa_nonzero,
    c[1]: 0,
    c[2]: 0,
    u[1]: 0,
    u[2]: D.aa,
    x[1]: D.aa * v[1] + sp.Rational(4, 3) * l[7],
    x[2]: D.aa * (v[2] - D.bb),
    v[3]: 0,
}
assert exact_zero(coefficient(5, 1, aa_e5))
e4_r2_aa = sp.Poly(coefficient(4, 2, aa_e5), p, q)
assert_same(
    e4_r2_aa.coeff_monomial(p * q), -2 * D.aa * l[8]
)
assert_same(
    e4_r2_aa.coeff_monomial(p**2),
    6 * D.aa * (D.bb * v[5] - D.bq),
)

aa_lower = {
    **aa_e5,
    l[8]: 0,
    D.ap: D.aa * v[4],
    D.bq: D.bb * v[5],
    l[2]: D.aa * (D.bp - D.bb * v[4]),
}
assert exact_zero(coefficient(5, 0, aa_lower))
e4_r1_aa = sp.Poly(coefficient(4, 1, aa_lower), p, q)
assert_same(e4_r1_aa.coeff_monomial(p * q**2), 2 * D.aa * l[7])

aa_e4 = {
    **aa_lower,
    l[7]: 0,
    x[1]: D.aa * v[1],
    y[2]: D.bb * (v[2] - D.bb),
    l[1]: D.aa * (y[1] - D.bb * v[1]),
}
assert exact_zero(coefficient(4, 1, aa_e4))
e4_r0_aa = sp.Poly(coefficient(4, 0, aa_e4), p, q)
assert_same(
    e4_r0_aa.coeff_monomial(p**3 * q),
    6 * D.aa * (D.bb**2 * v[4] - D.bb * D.bp + l[5]),
)

aa_e3 = {
    **aa_e4,
    l[5]: D.bb * (D.bp - D.bb * v[4]),
}
e3_r1_aa = sp.Poly(coefficient(3, 1, aa_e3), p, q)
assert_same(
    e3_r1_aa.coeff_monomial(p**2),
    6 * D.aa * (D.bb * (y[1] - D.bb * v[1]) - l[4]),
)

aa_final = {
    **aa_e3,
    l[4]: D.bb * (y[1] - D.bb * v[1]),
}
det_aa = sp.factor(D.L.det().subs(aa_final))
assert det_aa == 0

# aa=0.  E5[r] forces c2=0 and fixes x1,x2.
aa_zero_pre = {
    **orbit,
    D.tq: 0,
    D.tp: 0,
    D.aa: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: sp.Rational(4, 3) * c[2],
    u[3]: 0,
    D.ap: sp.Rational(4, 3) * l[8],
    D.aq: 0,
}
e5_r1_aa0 = sp.Poly(coefficient(5, 1, aa_zero_pre), p, q)
assert_same(
    e5_r1_aa0.coeff_monomial(p * q**3),
    -sp.Rational(16, 3) * c[2] ** 2,
)

aa_zero = {
    **aa_zero_pre,
    c[2]: 0,
    u[2]: 0,
    x[1]: (
        sp.Rational(4, 3) * l[7]
        - c[1] * (8 * c[0] - 9 * u[0]) / 9
    ),
    x[2]: sp.Rational(2, 9) * c[1] ** 2,
}
assert exact_zero(coefficient(5, 1, aa_zero))
e5_r0_aa0 = sp.Poly(coefficient(5, 0, aa_zero), p, q)
assert_same(
    e5_r0_aa0.coeff_monomial(p**3 * q**2),
    sp.Rational(8, 3) * c[1] * l[8],
)

# If c1!=0, E5 makes l33=l13=0 and E4 has 8c1^3/9.
c1_nonzero = {**aa_zero, l[8]: 0, D.ap: 0, l[2]: 0}
e4_r1_c1 = sp.Poly(coefficient(4, 1, c1_nonzero), p, q)
assert_same(
    e4_r1_c1.coeff_monomial(p * q**2),
    sp.Rational(8, 9) * c[1] ** 3,
)

# If c1=0, E4 makes l33=0 and E3 then makes l32=0.
c1_zero = {
    **aa_zero,
    c[1]: 0,
    u[1]: 0,
    x[1]: sp.Rational(4, 3) * l[7],
    x[2]: 0,
    l[2]: l[8] * (u[0] - sp.Rational(8, 9) * c[0]),
}
e4_r1_c10 = sp.Poly(coefficient(4, 1, c1_zero), p, q)
assert_same(
    e4_r1_c10.coeff_monomial(p**2 * q),
    sp.Rational(8, 3) * l[8] ** 2,
)
singular = {
    **c1_zero,
    l[8]: 0,
    D.ap: 0,
    l[2]: 0,
    l[1]: l[7] * (u[0] - sp.Rational(8, 9) * c[0]),
}
e3_r1_singular = sp.Poly(coefficient(3, 1, singular), p, q)
assert_same(
    e3_r1_singular.coeff_monomial(p * q),
    -sp.Rational(8, 3) * l[7] ** 2,
)

print("PASS v9=0, ell=p, tp!=0 branch excluded")
print("PASS v9=0, ell=p, tp=0, aa!=0 branch forces det(L)=0")
print("PASS v9=0, ell=p, tp=aa=0 branches excluded")
print("ALL v9=0 ell=p CHECKS PASSED")

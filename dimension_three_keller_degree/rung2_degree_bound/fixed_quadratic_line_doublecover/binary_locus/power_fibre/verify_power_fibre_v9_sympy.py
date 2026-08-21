#!/usr/bin/env python3
"""Exact certificate excluding the r^3 branch on the power fibre."""

from __future__ import annotations

import sympy as sp


if not __debug__:
    raise RuntimeError("assertions must remain enabled")

p, q, r, tau = sp.symbols("p q r tau")
variables = (p, q, r)


def binary_form(prefix: str, degree: int):
    coefficients = sp.symbols(f"{prefix}0:{degree + 1}")
    return (
        sum(
            coefficients[index] * p ** (degree - index) * q**index
            for index in range(degree + 1)
        ),
        coefficients,
    )


def exact_zero(value) -> bool:
    return sp.Poly(sp.together(value).as_numer_denom()[0], p, q, r).is_zero


U0, u = binary_form("u", 3)
T0, c = binary_form("c", 2)
A0, x = binary_form("x", 2)
B0, y = binary_form("y", 2)
tp, tq, tt = sp.symbols("tp tq tt")
ap, aq, aa = sp.symbols("ap aq aa")
bp, bq, bb = sp.symbols("bp bq bb")

T = T0 + r * (tp * p + tq * q) + tt * r**2
U = (
    U0
    + sp.Rational(4, 3) * r * p * (tp * p + tq * q)
    + sp.Rational(4, 3) * tt * p * r**2
)
v = sp.symbols("v0:10")
monomials3 = (
    p**3,
    p**2 * q,
    p * q**2,
    q**3,
    p**2 * r,
    p * q * r,
    q**2 * r,
    p * r**2,
    q * r**2,
    r**3,
)
V = sum(coefficient * monomial for coefficient, monomial in zip(v, monomials3))
A = A0 + r * (ap * p + aq * q) + aa * r**2
B = B0 + r * (bp * p + bq * q) + bb * r**2

H4 = sp.Matrix((p**4, p**2 * q**2, 0))
H3 = sp.Matrix((U, V, p**3))
H2 = sp.Matrix((A, B, T))
l = sp.symbols("l11 l12 l13 l21 l22 l23 l31 l32 l33")
L = sp.Matrix(3, 3, l)
weighted = sp.Poly(
    sp.expand(
        (
            L
            + tau * H2.jacobian(variables)
            + tau**2 * H3.jacobian(variables)
            + tau**3 * H4.jacobian(variables)
        ).det()
    ),
    tau,
)
E = {
    degree: sp.Poly(sp.expand(weighted.coeff_monomial(tau**degree)), p, q, r)
    for degree in (7, 6, 5, 4, 3)
}

assert E[7].is_zero
assert sp.factor(sp.Poly(E[6].as_expr(), r).coeff_monomial(r**3)) == (
    sp.Rational(16, 3) * p**2 * q * tt**2
)

# On v9 != 0, E6[r^2] gives the three displayed linear relations.
e6_r2_tt0 = sp.Poly(
    sp.Poly(E[6].as_expr(), r).coeff_monomial(r**2).subs({tt: 0}),
    p,
    q,
)
assert sp.factor(e6_r2_tt0.coeff_monomial(p**4)) == (
    3 * v[9] * (3 * u[1] - 4 * c[1])
)
assert sp.factor(e6_r2_tt0.coeff_monomial(p**3 * q)) == (
    6 * v[9] * (3 * u[2] - 4 * c[2])
)
assert sp.factor(e6_r2_tt0.coeff_monomial(p**2 * q**2)) == 27 * v[9] * u[3]

v9_top = {
    tt: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: sp.Rational(4, 3) * c[2],
    u[3]: 0,
}

# E5[r^4] then forces tq=0: its p and q coefficients are
# -4*tq*v9*tp and -4*tq^2*v9.
e5_r4_top = sp.factor(
    sp.Poly(E[5].as_expr(), r).coeff_monomial(r**4).subs(v9_top)
)
assert e5_r4_top == -4 * tq * v[9] * (p * tp + q * tq)

e6_r1 = sp.factor(
    sp.Poly(E[6].as_expr(), r)
    .coeff_monomial(r)
    .subs(v9_top)
    .subs({tq: 0})
)
assert e6_r1 == -sp.Rational(4, 3) * p**4 * q * (
    9 * aa - 2 * tp**2
)

# With aa=2tp^2/9, E6[r^0] has exactly three coefficient equations.
e6_r0_pre = sp.factor(
    sp.Poly(E[6].as_expr(), r)
    .coeff_monomial(1)
    .subs(v9_top)
    .subs({tq: 0, aa: sp.Rational(2, 9) * tp**2})
)
assert sp.expand(
    e6_r0_pre
    - sp.Rational(2, 3)
    * p**2
    * q
    * (
        p**3 * (-9 * ap - 8 * c[0] * tp + 12 * l[8] + 9 * tp * u[0])
        + p**2 * q * (-9 * aq + 4 * c[1] * tp)
        + 4 * c[2] * p * q**2 * tp
    )
) == 0

# Thus c2*tp=0.  On tp=0, the q^3 coefficient of E5[r^2] is
# -8*c2^2*v9, so c2=0 in both branches.  The remaining E5[r^2]
# coefficients give x1 and x2.
pre_c2 = {
    **v9_top,
    tq: 0,
    aa: sp.Rational(2, 9) * tp**2,
    aq: sp.Rational(4, 9) * c[1] * tp,
    ap: (12 * l[8] + tp * (9 * u[0] - 8 * c[0])) / 9,
}
e5_r2_tp0 = sp.Poly(
    sp.Poly(E[5].as_expr(), r)
    .coeff_monomial(r**2)
    .subs(pre_c2)
    .subs({tp: 0}),
    p,
    q,
)
assert sp.factor(e5_r2_tp0.coeff_monomial(q**3)) == -8 * c[2] ** 2 * v[9]

base = {
    **pre_c2,
    c[2]: 0,
    u[2]: 0,
    x[1]: (
        sp.Rational(4, 3) * l[7]
        - c[1] * (8 * c[0] - 9 * u[0]) / 9
    ),
    x[2]: (
        sp.Rational(2, 9) * c[1] ** 2
        + 4 * tp**3 / (81 * v[9])
    ),
}
assert exact_zero(
    sp.Poly(E[5].as_expr(), r).coeff_monomial(r**2).subs(base)
)

# If tp != 0, the legal source shear in r kills c0 and c1.  The complete
# E5 solution then has the following form, but E4[r^3] is nonzero.
tp_nonzero = {
    **base,
    c[0]: 0,
    c[1]: 0,
    u[1]: 0,
    v[7]: -9 * l[8] * v[9] / tp**2,
    v[8]: 0,
    v[6]: sp.Rational(2, 3) * tp,
    v[5]: -9 * l[7] * v[9] / tp**2,
    l[2]: (
        -sp.Rational(4, 9) * l[6] * tp
        + l[8] * u[0]
        + 4 * tp**3 * v[4] / (81 * v[9])
        + sp.Rational(2, 3) * tp * x[0]
    ),
}
for degree in (6, 5):
    assert exact_zero(E[degree].as_expr().subs(tp_nonzero).subs({c[0]: 0, c[1]: 0}))
e4_r3 = sp.factor(
    sp.Poly(E[4].as_expr(), r)
    .coeff_monomial(r**3)
    .subs(tp_nonzero)
    .subs({c[0]: 0, c[1]: 0})
)
assert e4_r3 == -sp.Rational(8, 27) * q * tp**4

# It remains to take tp=0.  If c1 != 0, E5 makes l33=l13=0 and
# the q^2 coefficient of E4[r^2] is a nonzero multiple of c1^3*v9.
tp_zero_base = {
    **pre_c2,
    tp: 0,
    c[2]: 0,
    u[2]: 0,
    aa: 0,
    aq: 0,
    ap: sp.Rational(4, 3) * l[8],
    x[1]: (
        sp.Rational(4, 3) * l[7]
        - c[1] * (8 * c[0] - 9 * u[0]) / 9
    ),
    x[2]: sp.Rational(2, 9) * c[1] ** 2,
}

# The constant-r part of E5 says c1*l33=0 and fixes l13.
e5_r0_tp0 = sp.factor(
    sp.Poly(E[5].as_expr(), r).coeff_monomial(1).subs(tp_zero_base)
)
assert sp.expand(
    e5_r0_tp0
    - sp.Rational(2, 3)
    * p**3
    * q
    * (
        p * (-8 * c[0] * l[8] - 9 * l[2] + 9 * l[8] * u[0])
        + 4 * c[1] * l[8] * q
    )
) == 0
c1_nonzero = {**tp_zero_base, l[8]: 0, ap: 0, l[2]: 0}
for degree in (6, 5):
    assert exact_zero(E[degree].as_expr().subs(c1_nonzero))
e4_r2_c1 = sp.Poly(
    sp.Poly(E[4].as_expr(), r)
    .coeff_monomial(r**2)
    .subs(c1_nonzero),
    p,
    q,
)
assert sp.factor(e4_r2_c1.coeff_monomial(q**2)) == (
    sp.Rational(4, 3) * c[1] ** 3 * v[9]
)

# If c1=0, E4 first fixes l12, then forces l33=0.  E3 either makes
# l32=0 (so two rows of L are supported in column one) or contradicts
# the q coefficient of the displayed linear factor.
c1_zero = {
    **tp_zero_base,
    c[1]: 0,
    u[1]: 0,
    x[1]: sp.Rational(4, 3) * l[7],
    x[2]: 0,
    l[2]: l[8] * (u[0] - sp.Rational(8, 9) * c[0]),
    l[1]: l[7] * (u[0] - sp.Rational(8, 9) * c[0]),
}
for degree in (6, 5):
    assert exact_zero(E[degree].as_expr().subs(c1_zero).subs({c[1]: 0}))
e4_r2_c10 = sp.factor(
    sp.Poly(E[4].as_expr(), r)
    .coeff_monomial(r**2)
    .subs(c1_zero)
    .subs({c[1]: 0})
)
assert e4_r2_c10 == 0
e4_r1_c10 = sp.factor(
    sp.Poly(E[4].as_expr(), r)
    .coeff_monomial(r)
    .subs(c1_zero)
    .subs({c[1]: 0})
)
assert e4_r1_c10 == sp.Rational(8, 3) * p**2 * q * l[8] ** 2

final_branch = {
    **c1_zero,
    l[8]: 0,
    ap: 0,
    l[2]: 0,
}
e3_r2 = sp.factor(
    sp.Poly(E[3].as_expr(), r)
    .coeff_monomial(r**2)
    .subs(final_branch)
    .subs({c[1]: 0})
)
expected_linear = (
    8 * c[0] ** 2 * p
    - 9 * c[0] * p * u[0]
    - 6 * l[6] * p
    + 6 * l[7] * q
    + 9 * p * x[0]
)
assert e3_r2 == -sp.Rational(2, 3) * l[7] * v[9] * expected_linear
assert sp.Poly(expected_linear, p, q).coeff_monomial(q) == 6 * l[7]

print("PASS E7 parameterization and E6 top branch split")
print("PASS v9*tp branch obstructed by E4[r^3] = -(8/27)q tp^4")
print("PASS v9, tp=0, c1!=0 branch obstructed by (4/3)c1^3 v9")
print("PASS sole remaining branch forces det(L)=0 or a nonzero E3 coefficient")
print("ALL POWER-FIBRE v9!=0 CHECKS PASSED")

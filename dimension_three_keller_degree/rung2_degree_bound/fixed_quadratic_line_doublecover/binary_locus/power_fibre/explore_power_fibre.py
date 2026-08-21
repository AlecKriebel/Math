#!/usr/bin/env python3
"""Exact full-coefficient expansion on the exceptional power fibre."""

from __future__ import annotations

import sympy as sp


p, q, r, tau = sp.symbols("p q r tau")
variables = (p, q, r)


def binary_form(prefix: str, degree: int) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    coefficients = sp.symbols(f"{prefix}0:{degree + 1}")
    value = sum(
        coefficients[index] * p ** (degree - index) * q**index
        for index in range(degree + 1)
    )
    return value, coefficients


U0, u = binary_form("u", 3)
T0, c = binary_form("c", 2)
A0, x = binary_form("x", 2)
B0, y = binary_form("y", 2)

tp, tq, tt = sp.symbols("tp tq tt")
T = T0 + r * (tp * p + tq * q) + tt * r**2
U = (
    U0
    + sp.Rational(4, 3) * r * p * (tp * p + tq * q)
    + sp.Rational(4, 3) * tt * p * r**2
)

v = sp.symbols("v0:10")
degree_three_monomials = (
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
V = sum(coefficient * monomial for coefficient, monomial in zip(v, degree_three_monomials))

ap, aq, aa = sp.symbols("ap aq aa")
bp, bq, bb = sp.symbols("bp bq bb")
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

E7 = sp.Poly(sp.expand(weighted.coeff_monomial(tau**7)), p, q, r)
assert E7.is_zero
print("PASS full E7 parameterization")

E6 = sp.Poly(sp.expand(weighted.coeff_monomial(tau**6)), p, q, r)
for r_power in range(E6.degree(r), -1, -1):
    coefficient = sp.Poly(E6.as_expr(), r).coeff_monomial(r**r_power)
    if coefficient != 0:
        print(f"E6[r^{r_power}] =", sp.factor(coefficient))

branch_v9 = {
    tt: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: sp.Rational(4, 3) * c[2],
    u[3]: 0,
}
print("\nBRANCH v9 != 0")
for r_power in (1, 0):
    coefficient = sp.expand(
        sp.Poly(E6.as_expr(), r)
        .coeff_monomial(r**r_power)
        .subs(branch_v9)
    )
    print(f"E6_v9[r^{r_power}] =", sp.factor(coefficient))

E5 = sp.Poly(sp.expand(weighted.coeff_monomial(tau**5)), p, q, r)
for r_power in range(E5.degree(r), -1, -1):
    coefficient = sp.expand(
        sp.Poly(E5.as_expr(), r)
        .coeff_monomial(r**r_power)
        .subs(branch_v9)
    )
    if coefficient != 0:
        print(f"E5_v9[r^{r_power}] =", sp.factor(coefficient))

common_v9_e6 = {
    tt: 0,
    tq: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: sp.Rational(4, 3) * c[2],
    u[3]: 0,
    aa: sp.Rational(2, 9) * tp**2,
    aq: sp.Rational(4, 9) * c[1] * tp,
    ap: (
        12 * l[8] + tp * (9 * u[0] - 8 * c[0])
    ) / 9,
}
for label, extra in (
    ("tp_zero", {tp: 0, aa: 0, aq: 0, ap: sp.Rational(4, 3) * l[8]}),
    ("tp_nonzero_c2_zero", {c[2]: 0, u[2]: 0}),
):
    substitutions = {**common_v9_e6, **extra}
    print(f"\nBRANCH v9 != 0, {label}, AFTER E6")
    for r_power in range(E5.degree(r), -1, -1):
        coefficient = sp.expand(
            sp.Poly(E5.as_expr(), r)
            .coeff_monomial(r**r_power)
            .subs(substitutions)
        )
        if coefficient != 0:
            print(
                f"E5_v9_{label}[r^{r_power}] =",
                sp.factor(coefficient),
            )

common_v9_e5_r2 = {
    **common_v9_e6,
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
print("\nBRANCH v9 != 0 AFTER E6 AND E5[r^2]")
for r_power in (1, 0):
    coefficient = sp.factor(
        sp.together(
            sp.Poly(E5.as_expr(), r)
            .coeff_monomial(r**r_power)
            .subs(common_v9_e5_r2)
        )
    )
    print(f"E5_v9_common[r^{r_power}] =", coefficient)

E4 = sp.Poly(sp.expand(weighted.coeff_monomial(tau**4)), p, q, r)
v9_tp_normalized = {
    **common_v9_e5_r2,
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
print("\nBRANCH v9*tp != 0, SOURCE-SHEAR NORMALIZED, THROUGH E5")
for r_power in range(E4.degree(r), -1, -1):
    coefficient = sp.factor(
        sp.together(
            sp.Poly(E4.as_expr(), r)
            .coeff_monomial(r**r_power)
            .subs(v9_tp_normalized)
            .subs({c[0]: 0, c[1]: 0})
        )
    )
    if coefficient != 0:
        print(f"E4_v9_tp[r^{r_power}] =", coefficient)

v9_tp_zero_base = {
    tt: 0,
    tq: 0,
    tp: 0,
    c[2]: 0,
    u[1]: sp.Rational(4, 3) * c[1],
    u[2]: 0,
    u[3]: 0,
    aa: 0,
    aq: 0,
    ap: sp.Rational(4, 3) * l[8],
    x[1]: (
        sp.Rational(4, 3) * l[7]
        - c[1] * (8 * c[0] - 9 * u[0]) / 9
    ),
    x[2]: sp.Rational(2, 9) * c[1] ** 2,
}
for label, extra in (
    (
        "c1_nonzero",
        {l[8]: 0, ap: 0, l[2]: 0},
    ),
    (
        "c1_zero",
        {
            c[1]: 0,
            u[1]: 0,
            x[1]: sp.Rational(4, 3) * l[7],
            x[2]: 0,
            l[2]: l[8] * (u[0] - sp.Rational(8, 9) * c[0]),
        },
    ),
):
    substitutions = {**v9_tp_zero_base, **extra}
    print(f"\nBRANCH v9 != 0, tp = 0, {label}, THROUGH E5")
    for r_power in range(E4.degree(r), -1, -1):
        coefficient = sp.factor(
            sp.together(
                sp.Poly(E4.as_expr(), r)
                .coeff_monomial(r**r_power)
                .subs(substitutions)
            )
        )
        if coefficient != 0:
            print(f"E4_v9_tp0_{label}[r^{r_power}] =", coefficient)

E3 = sp.Poly(sp.expand(weighted.coeff_monomial(tau**3)), p, q, r)
v9_final_e4 = {
    **v9_tp_zero_base,
    c[1]: 0,
    u[1]: 0,
    x[1]: sp.Rational(4, 3) * l[7],
    x[2]: 0,
    l[8]: 0,
    ap: 0,
    l[2]: 0,
    l[1]: l[7] * (u[0] - sp.Rational(8, 9) * c[0]),
}
print("\nBRANCH v9 != 0, SOLE E4 SURVIVOR")
for r_power in range(E3.degree(r), -1, -1):
    coefficient = sp.factor(
        sp.together(
            sp.Poly(E3.as_expr(), r)
            .coeff_monomial(r**r_power)
            .subs(v9_final_e4)
            .subs({c[1]: 0})
        )
    )
    if coefficient != 0:
        print(f"E3_v9_final[r^{r_power}] =", coefficient)

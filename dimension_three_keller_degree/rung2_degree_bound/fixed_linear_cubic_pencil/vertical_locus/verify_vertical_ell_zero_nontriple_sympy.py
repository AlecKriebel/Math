#!/usr/bin/env python3
"""Exact checks for the zero-ell nontriple vertical-companion lemma."""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


x, y, z = sp.symbols("x y z")
source_variables = (x, y, z)
s, w, k = sp.symbols("s w k", nonzero=True)
r20, r11, r02, r10, r01 = sp.symbols("r20 r11 r02 r10 r01")
moduli = (r20, r11, r02, r10, r01)

a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
v = sp.symbols("v0:9")
ell = sp.symbols("l0:9")

quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
cubic_monomials_no_z3 = (
    x**3,
    x**2 * y,
    x * y**2,
    y**3,
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
)

A = sum(c * m for c, m in zip(a, quadratic_monomials))
B = sum(c * m for c, m in zip(b, quadratic_monomials))
W = w * z**2
V_general = sum(c * m for c, m in zip(v, cubic_monomials_no_z3))
L = sp.Matrix(3, 3, ell)


def determinant_polynomial(q: sp.Expr, V: sp.Expr) -> sp.Poly:
    H2 = sp.Matrix((A, B, W))
    H3 = sp.Matrix((sp.Rational(4, 3) * z * W + s * q, V, z**3))
    H4 = sp.Matrix((z**4, z * q, 0))
    determinant = sp.expand(
        (L + H2.jacobian(source_variables)
         + H3.jacobian(source_variables)
         + H4.jacobian(source_variables)).det()
    )
    return sp.Poly(determinant - 1, x, y, z)


root_types = {
    "squarefree": x * y * (x - y),
    "double": x**2 * y,
}

expected_e6_minors = {
    "squarefree": (
        (0, 2, 3, 4, 5, 6, 7, 8),
        (0, 1, 3, 4, 5, 6, 7, 8),
    ),
    "double": (
        (0, 1, 2, 3, 4, 5, 6, 7),
        (0, 2, 3, 4, 5, 6, 7, 8),
    ),
}

for label, q0 in root_types.items():
    q = (
        q0
        + z * (r20 * x**2 + r11 * x * y + r02 * y**2)
        + z**2 * (r10 * x + r01 * y)
    )

    raw = determinant_polynomial(q, V_general)
    degree_six = [
        sp.expand(coefficient)
        for monomial, coefficient in raw.terms()
        if sum(monomial) == 6
    ]
    e6_unknowns = v + (ell[6], ell[7])
    e6_matrix, e6_rhs = sp.linear_eq_to_matrix(degree_six, e6_unknowns)
    rows, columns = expected_e6_minors[label]
    minor = sp.factor(e6_matrix[list(rows), list(columns)].det())
    check(
        minor == 5668704 * s**8,
        f"{label}: literal E6 minor",
    )
    check(e6_matrix.rank() == 8, f"{label}: E6 rank eight")
    check(
        e6_matrix.row_join(e6_rhs).rank() == 8,
        f"{label}: E6 consistency",
    )

    V_solution = (
        k * q
        + z * (A - a[5] * z**2) / s
        - sp.Rational(4, 3) * z**2 * (ell[6] * x + ell[7] * y) / s
    )
    solved = determinant_polynomial(q, V_solution)
    check(
        all(
            sp.expand(coefficient) == 0
            for monomial, coefficient in solved.terms()
            if sum(monomial) == 6
        ),
        f"{label}: displayed three-parameter E6 family",
    )

    if label == "squarefree":
        transverse_coefficients = (
            solved.coeff_monomial(x**4 * y),
            solved.coeff_monomial(x * y**4),
        )
        expected_transverse = (s * ell[6], -s * ell[7])
    else:
        transverse_coefficients = (
            solved.coeff_monomial(x**4 * y),
            solved.coeff_monomial(x**3 * y**2),
        )
        expected_transverse = (s * ell[6], -2 * s * ell[7])
    check(
        tuple(map(sp.factor, transverse_coefficients))
        == expected_transverse,
        f"{label}: E5 kills third-row x,y entries",
    )

    zero_transverse = {ell[6]: 0, ell[7]: 0}
    degree_five = [
        sp.expand(coefficient.subs(zero_transverse))
        for monomial, coefficient in solved.terms()
        if sum(monomial) == 5
        and coefficient.subs(zero_transverse) != 0
    ]
    e5_matrix, e5_rhs = sp.linear_eq_to_matrix(degree_five, b[:5])
    e5_rows = (0, 1, 2, 3, 4)
    check(
        sp.factor(e5_matrix[list(e5_rows), :].det()) == -3888 * s**5,
        f"{label}: literal E5 minor",
    )

    b_solution = {
        b[0]: a[0] * k / s,
        b[1]: a[1] * k / s,
        b[2]: a[2] * k / s,
        b[3]: (a[3] * k + ell[0]) / s,
        b[4]: (a[4] * k + ell[1]) / s,
    }
    check(
        all(sp.factor(e.subs(b_solution)) == 0 for e in degree_five),
        f"{label}: complete E5 solution",
    )

    reduced = {
        **zero_transverse,
        **b_solution,
        ell[3]: k * ell[0] / s,
        ell[4]: k * ell[1] / s,
    }
    if label == "squarefree":
        e4_pair = (
            solved.coeff_monomial(x**2 * z**2),
            solved.coeff_monomial(y**2 * z**2),
        )
        expected_e4 = (
            3 * (k * ell[0] - s * ell[3]),
            3 * (k * ell[1] - s * ell[4]),
        )
    else:
        e4_pair = (
            solved.coeff_monomial(x**2 * z**2),
            solved.coeff_monomial(x * y * z**2),
        )
        expected_e4 = (
            3 * (k * ell[0] - s * ell[3]),
            -6 * (k * ell[1] - s * ell[4]),
        )
    e4_pair = tuple(sp.factor(e.subs(zero_transverse).subs(b_solution))
                    for e in e4_pair)
    check(
        all(sp.expand(left - right) == 0
            for left, right in zip(e4_pair, expected_e4)),
        f"{label}: E4 proportionality pair",
    )
    check(
        sp.factor(L.det().subs(reduced)) == 0,
        f"{label}: singular linear part",
    )

print("VERTICAL_ELL_ZERO_NONTRIPLE_SYMPY_PASS_91C4D7")

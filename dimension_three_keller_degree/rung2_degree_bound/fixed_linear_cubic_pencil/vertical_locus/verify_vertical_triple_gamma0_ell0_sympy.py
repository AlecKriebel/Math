#!/usr/bin/env python3
"""Exact unified certificate for W=w*z^2 on all triple-root q charts."""

from __future__ import annotations

import sympy as sp


if not __debug__:
    raise SystemExit("refusing optimized Python: fail-closed checks required")


def check(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


x, y, z = sp.symbols("x y z")
source_variables = (x, y, z)
s = sp.symbols("s", nonzero=True)
w, k, alpha = sp.symbols("w k alpha")
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
A = sum(coefficient * monomial for coefficient, monomial
        in zip(a, quadratic_monomials))
B = sum(coefficient * monomial for coefficient, monomial
        in zip(b, quadratic_monomials))
W = w * z**2
V_general = sum(coefficient * monomial for coefficient, monomial
                in zip(v, cubic_monomials_no_z3))
L = sp.Matrix(3, 3, ell)

charts = {
    "quadratic_y": {
        "q": x**3 + y**2 * z + alpha * x * z**2,
        "e6_rows": (0, 1, 2, 3, 4, 5, 7, 11),
        "e6_columns": (0, 1, 2, 3, 4, 5, 7, 8),
        "e6_minor": -459165024,
        "e5_rows": (0, 1, 2, 4, 5, 6, 10),
        "e5_minor": 629856,
        "e4": {
            (2, 0, 2): 9 * (-k * ell[1] + s * ell[4]),
            (0, 1, 3): -6 * (-k * ell[0] + s * ell[3]),
            (0, 0, 4): 3 * alpha * (-k * ell[1] + s * ell[4]),
        },
        "e4_rows": ((2, 0, 2), (0, 1, 3)),
        "e4_minor": 54,
    },
    "mixed_xy": {
        "q": x**3 + x * y * z,
        "e6_rows": (0, 1, 2, 3, 4, 5, 7, 10),
        "e6_columns": (0, 1, 2, 3, 4, 6, 7, 8),
        "e6_minor": 38263752,
        "e5_rows": (0, 1, 3, 4, 5, 7, 9),
        "e5_minor": 26244,
        "e4": {
            (2, 0, 2): 9 * (-k * ell[1] + s * ell[4]),
            (1, 0, 3): -3 * (-k * ell[0] + s * ell[3]),
            (0, 1, 3): 3 * (-k * ell[1] + s * ell[4]),
        },
        "e4_rows": ((2, 0, 2), (1, 0, 3)),
        "e4_minor": 27,
    },
    "linear_y": {
        "q": x**3 + y * z**2,
        "e6_rows": (0, 1, 2, 3, 4, 5, 7, 10),
        "e6_columns": (0, 1, 2, 3, 4, 5, 6, 7),
        "e6_minor": -114791256,
        "e5_rows": (0, 1, 2, 3, 4, 5, 6),
        "e5_minor": 104976,
        "e4": {
            (2, 0, 2): 9 * (-k * ell[1] + s * ell[4]),
            (0, 0, 4): -3 * (-k * ell[0] + s * ell[3]),
        },
        "e4_rows": ((2, 0, 2), (0, 0, 4)),
        "e4_minor": 27,
    },
}


def determinant_polynomial(q: sp.Expr, V: sp.Expr, B_form: sp.Expr = B) -> sp.Poly:
    H2 = sp.Matrix((A, B_form, W))
    H3 = sp.Matrix((sp.Rational(4, 3) * z * W + s * q, V, z**3))
    H4 = sp.Matrix((z**4, z * q, 0))
    return sp.Poly(
        sp.expand(
            (
                L
                + H2.jacobian(source_variables)
                + H3.jacobian(source_variables)
                + H4.jacobian(source_variables)
            ).det()
        ),
        x,
        y,
        z,
    )


for label, data in charts.items():
    q = data["q"]
    raw = determinant_polynomial(q, V_general)
    check(
        all(sum(monomial) <= 6 for monomial, _ in raw.terms()),
        f"{label}: E8 or E7 survives",
    )

    degree_six = [
        sp.expand(coefficient)
        for monomial, coefficient in raw.terms()
        if sum(monomial) == 6
    ]
    e6_unknowns = v + (ell[6], ell[7])
    e6_matrix, _ = sp.linear_eq_to_matrix(degree_six, e6_unknowns)
    e6_minor = e6_matrix.extract(
        data["e6_rows"],
        data["e6_columns"],
    ).det()
    check(
        sp.factor(e6_minor) == data["e6_minor"] * s**8,
        f"{label}: literal E6 minor",
    )

    V_solution = (
        k * q
        + z * (A - a[5] * z**2) / s
        - sp.Rational(4, 3) * z**2
        * (ell[6] * x + ell[7] * y) / s
    )
    after_e6 = determinant_polynomial(q, V_solution)
    check(
        all(
            sp.factor(coefficient) == 0
            for monomial, coefficient in after_e6.terms()
            if sum(monomial) == 6
        ),
        f"{label}: displayed complete E6 family",
    )

    degree_five = [
        sp.expand(coefficient)
        for monomial, coefficient in after_e6.terms()
        if sum(monomial) == 5
    ]
    e5_unknowns = b[:5] + (ell[6], ell[7])
    e5_matrix, e5_rhs = sp.linear_eq_to_matrix(degree_five, e5_unknowns)
    e5_minor = e5_matrix.extract(data["e5_rows"], tuple(range(7))).det()
    check(
        sp.factor(e5_minor) == data["e5_minor"] * s**7,
        f"{label}: literal E5 minor",
    )

    e5_solution = {
        b[0]: a[0] * k / s,
        b[1]: a[1] * k / s,
        b[2]: a[2] * k / s,
        b[3]: (a[3] * k + ell[0]) / s,
        b[4]: (a[4] * k + ell[1]) / s,
        ell[6]: 0,
        ell[7]: 0,
    }
    selected_matrix = e5_matrix.extract(data["e5_rows"], tuple(range(7)))
    selected_rhs = e5_rhs.extract(data["e5_rows"], (0,))
    selected_solution = selected_matrix.inv() * selected_rhs
    check(
        {
            unknown: sp.factor(value)
            for unknown, value in zip(e5_unknowns, selected_solution)
        } == e5_solution,
        f"{label}: unique E5 solution",
    )
    check(
        all(sp.factor(equation.subs(e5_solution)) == 0
            for equation in degree_five),
        f"{label}: residual E5 equation",
    )

    degree_four = {}
    for monomial, coefficient in after_e6.terms():
        if sum(monomial) != 4:
            continue
        reduced = sp.factor(coefficient.subs(e5_solution))
        if reduced != 0:
            degree_four[monomial] = reduced
    check(
        set(degree_four) == set(data["e4"])
        and all(
            sp.expand(degree_four[monomial] - expected) == 0
            for monomial, expected in data["e4"].items()
        ),
        f"{label}: complete E4 residual",
    )
    e4_equations = [degree_four[monomial] for monomial in data["e4_rows"]]
    e4_matrix, _ = sp.linear_eq_to_matrix(
        e4_equations,
        (ell[3], ell[4]),
    )
    check(
        abs(sp.factor(e4_matrix.det())) == data["e4_minor"] * s**2,
        f"{label}: literal E4 minor",
    )

    final_solution = {
        **e5_solution,
        ell[3]: k * ell[0] / s,
        ell[4]: k * ell[1] / s,
    }
    check(
        all(
            sp.factor(coefficient.subs(final_solution)) == 0
            for monomial, coefficient in after_e6.terms()
            if sum(monomial) in (6, 5, 4)
        ),
        f"{label}: final E6--E4 residual",
    )
    check(
        sp.factor(L.det().subs(final_solution)) == 0,
        f"{label}: singular linear part",
    )
    print(
        f"{label}: E6={sp.factor(e6_minor)}, "
        f"E5={sp.factor(e5_minor)}, "
        f"E4={sp.factor(e4_matrix.det())}"
    )

print("VERTICAL_TRIPLE_GAMMA0_ELL0_SYMPY_PASS_83A4E1")

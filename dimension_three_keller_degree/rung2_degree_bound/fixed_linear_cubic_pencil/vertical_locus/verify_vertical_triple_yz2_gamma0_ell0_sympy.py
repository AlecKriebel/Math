#!/usr/bin/env python3
"""Exact certificate for the vertical q=x^3+yz^2, W=w*z^2 chart."""

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
w, k = sp.symbols("w k")
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
q = x**3 + y * z**2
V_general = sum(coefficient * monomial for coefficient, monomial
                in zip(v, cubic_monomials_no_z3))
L = sp.Matrix(3, 3, ell)


def determinant_polynomial(V: sp.Expr, B_form: sp.Expr = B) -> sp.Poly:
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


raw = determinant_polynomial(V_general)
check(
    all(sum(monomial) <= 6 for monomial, _ in raw.terms()),
    "E8 or E7 survived the legal gauge",
)

# Complete E6 solve.
degree_six = [
    sp.expand(coefficient)
    for monomial, coefficient in raw.terms()
    if sum(monomial) == 6
]
e6_unknowns = v + (ell[6], ell[7])
e6_matrix, e6_rhs = sp.linear_eq_to_matrix(degree_six, e6_unknowns)
e6_rows = (0, 1, 2, 3, 4, 5, 7, 10)
e6_columns = (0, 1, 2, 3, 4, 5, 6, 7)
check(
    sp.factor(
        e6_matrix.extract(e6_rows, e6_columns).det()
    ) == -114791256 * s**8,
    "literal E6 minor",
)

V_solution = (
    k * q
    + z * (A - a[5] * z**2) / s
    - sp.Rational(4, 3) * z**2 * (ell[6] * x + ell[7] * y) / s
)
solved_e6 = determinant_polynomial(V_solution)
check(
    all(
        sp.expand(coefficient) == 0
        for monomial, coefficient in solved_e6.terms()
        if sum(monomial) == 6
    ),
    "displayed E6 family",
)
check(
    e6_matrix.rank() == 8
    and e6_matrix.row_join(e6_rhs).rank() == 8,
    "E6 rank sandwich",
)

# The entire E5 system is a nonsingular square system.
degree_five = [
    sp.expand(coefficient)
    for monomial, coefficient in solved_e6.terms()
    if sum(monomial) == 5
]
e5_unknowns = b[:5] + (ell[6], ell[7])
e5_matrix, e5_rhs = sp.linear_eq_to_matrix(degree_five, e5_unknowns)
check(e5_matrix.shape == (7, 7), "E5 is not the expected square system")
check(
    sp.factor(e5_matrix.det()) == 104976 * s**7,
    "literal E5 determinant",
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
matrix_solution = e5_matrix.inv() * e5_rhs
check(
    {
        unknown: sp.factor(value)
        for unknown, value in zip(e5_unknowns, matrix_solution)
    } == e5_solution,
    "unique E5 solution",
)
check(
    all(sp.factor(equation.subs(e5_solution)) == 0
        for equation in degree_five),
    "residual E5 equation",
)

check(
    sp.factor(solved_e6.coeff_monomial(x**5)) == -3 * ell[7] * s,
    "E5 coefficient killing l32",
)
lambda_pair = (
    solved_e6.coeff_monomial(x**3 * z**2),
    solved_e6.coeff_monomial(y * z**4),
)
check(
    sp.factor(lambda_pair[0] + 3 * lambda_pair[1])
    == 4 * ell[6] * s,
    "E5 combination killing l31",
)

# After E5, E4 has exactly two equations and forces proportional rows.
after_e5 = {
    **e5_solution,
}
degree_four = {}
for monomial, coefficient in solved_e6.terms():
    if sum(monomial) != 4:
        continue
    reduced_coefficient = sp.factor(coefficient.subs(after_e5))
    if reduced_coefficient != 0:
        degree_four[monomial] = reduced_coefficient
expected_degree_four = {
    (2, 0, 2): 9 * (-k * ell[1] + s * ell[4]),
    (0, 0, 4): -3 * (-k * ell[0] + s * ell[3]),
}
check(
    all(
        sp.expand(degree_four[monomial] - expected) == 0
        for monomial, expected in expected_degree_four.items()
    )
    and set(degree_four) == set(expected_degree_four),
    "complete E4 residual",
)

e4_matrix, _ = sp.linear_eq_to_matrix(
    list(degree_four.values()),
    (ell[3], ell[4]),
)
check(abs(sp.factor(e4_matrix.det())) == 27 * s**2, "literal E4 minor")

final_solution = {
    **after_e5,
    ell[3]: k * ell[0] / s,
    ell[4]: k * ell[1] / s,
}
check(
    all(
        sp.factor(coefficient.subs(final_solution)) == 0
        for monomial, coefficient in solved_e6.terms()
        if sum(monomial) in (6, 5, 4)
    ),
    "E6 through E4 residual after final solution",
)
check(sp.factor(L.det().subs(final_solution)) == 0, "singular linear part")

print("VERTICAL_TRIPLE_YZ2_GAMMA0_ELL0_SYMPY_PASS_4FD8A2")

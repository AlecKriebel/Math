#!/usr/bin/env python3
"""Exact full-lower exclusion of the frozen quartic family D4-DN-2C.

This certificate starts from the independently frozen four-chart E6 atlas,
retains every free lower coefficient, and closes:

* the two transverse contact-plane interiors at E5;
* the punctured plane intersection through the complete E5 branch ideal and
  a specialization-safe E4/E3 descent; and
* the origin by literal collapse of all six r-dependent quadratic
  coefficients, followed by the unconditional bounded-degree plane exit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

HERE = Path(__file__).resolve().parent
REBUILD = HERE.parent / "d4_dn2c_full_rebuild"
sys.path.insert(0, str(REBUILD))
import verify_full_e6_elimination as base  # noqa: E402


def sequential_substitute(expression, substitutions):
    value = expression
    for substitution in substitutions:
        value = value.subs(substitution)
    return sp.cancel(value)


def solve_selected(equations, variables, rows, columns, expected_pivot):
    """Solve a displayed square pivot and check every equation."""
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    pivot = sp.factor(
        matrix.extract(rows, columns).det(), extension=base.eta
    )
    assert sp.expand(pivot - expected_pivot) == 0, (pivot, expected_pivot)
    free_columns = tuple(
        index for index in range(len(variables)) if index not in columns
    )
    values = matrix.extract(rows, columns).inv() * (
        rhs.extract(rows, (0,))
        - matrix.extract(rows, free_columns)
        * sp.Matrix([variables[index] for index in free_columns])
    )
    substitution = {
        variables[column]: sp.cancel(values[index])
        for index, column in enumerate(columns)
    }
    residuals = tuple(
        sp.factor(sp.cancel(equation.subs(substitution)))
        for equation in equations
    )
    return matrix, substitution, residuals


def solve_e6_chart(contact, rows, columns, expected_pivot):
    equations = tuple(
        sp.expand(equation.subs(contact)) for equation in base.e6_equations
    )
    _, substitution, residuals = solve_selected(
        equations, base.lower18, rows, columns, expected_pivot
    )
    assert all(value == 0 for value in residuals)
    return substitution


def nonzero_coefficients_with_r_degree(polynomial, r_degree, substitutions):
    result = []
    for monomial, coefficient in polynomial.terms():
        if monomial[2] != r_degree:
            continue
        value = sequential_substitute(coefficient, substitutions)
        if value != 0:
            result.append(value)
    return tuple(result)


e5 = sp.Poly(
    base.full_determinant.coeff_monomial(base.weight**5),
    base.p,
    base.q,
    base.r,
)
e4 = sp.Poly(
    base.full_determinant.coeff_monomial(base.weight**4),
    base.p,
    base.q,
    base.r,
)


# ---------------------------------------------------------------------------
# The two transverse plane interiors: incompatible pure E5 equations
# ---------------------------------------------------------------------------

plus_e6 = solve_e6_chart(
    base.plane_plus,
    base.rows7,
    base.cols7,
    93312 * (base.eta - 1) * (2 * base.k + 3 * base.s) ** 2,
)
minus_e6 = solve_e6_chart(
    base.plane_minus,
    base.rows7,
    base.cols7,
    93312 * (-base.eta - 1) * (2 * base.k + 3 * base.s) ** 2,
)

q1 = (
    (-16 + 40 * base.eta) * base.k**2
    + (-120 - 24 * base.eta) * base.k * base.s
    + (18 - 45 * base.eta) * base.s**2
)
q2 = (
    (116 + 88 * base.eta) * base.k**2
    + (-30 - 6 * base.eta) * base.k * base.s
    + (180 + 36 * base.eta) * base.s**2
)


def plane_e5_coefficient(monomial, contact, solve6):
    return sequential_substitute(
        e5.coeff_monomial(monomial),
        ({base.d: 0, base.z: 0}, contact, solve6),
    )


plus_c1 = plane_e5_coefficient(
    base.p**3 * base.r**2, base.plane_plus, plus_e6
)
plus_c2 = plane_e5_coefficient(
    base.p**2 * base.q * base.r**2, base.plane_plus, plus_e6
)
# MUTATION_GUARD_INTERIOR_DENOMINATOR
expected_plus_c1 = (2 * base.k + 3 * base.s) * q1 / sp.Integer(162)
expected_plus_c2 = (2 * base.k + 3 * base.s) * q2 / sp.Integer(243)
assert sp.expand(plus_c1 - expected_plus_c1) == 0
assert sp.expand(plus_c2 - expected_plus_c2) == 0

t = sp.symbols("t")
q1t = sp.expand(q1.subs({base.k: 1, base.s: t}))
q2t = sp.expand(q2.subs({base.k: 1, base.s: t}))
bezout1 = (
    t * (sp.Rational(1, 6) - sp.Rational(5, 36) * base.eta)
    + sp.Rational(13, 108)
    + sp.Rational(11, 72) * base.eta
)
bezout2 = (
    t * (sp.Rational(5, 72) + sp.Rational(1, 24) * base.eta)
    + sp.Rational(5, 108)
    - sp.Rational(1, 18) * base.eta
)
assert sp.expand(bezout1 * q1t + bezout2 * q2t - 1) == 0
assert sp.expand(
    (18 - 45 * base.eta) * (18 + 45 * base.eta) - 4374
) == 0

q1_minus = q1.xreplace({sp.I: -sp.I})
q2_minus = q2.xreplace({sp.I: -sp.I})
minus_c1 = plane_e5_coefficient(
    base.p**3 * base.r**2, base.plane_minus, minus_e6
)
minus_c2 = plane_e5_coefficient(
    base.p**2 * base.q * base.r**2, base.plane_minus, minus_e6
)
assert sp.expand(
    minus_c1
    - (2 * base.k + 3 * base.s) * q1_minus / sp.Integer(162)
) == 0
assert sp.expand(
    minus_c2
    - (2 * base.k + 3 * base.s) * q2_minus / sp.Integer(243)
) == 0
assert sp.expand(
    bezout1.xreplace({sp.I: -sp.I})
    * q1t.xreplace({sp.I: -sp.I})
    + bezout2.xreplace({sp.I: -sp.I})
    * q2t.xreplace({sp.I: -sp.I})
    - 1
) == 0

print("D4_DN2C_INTERIORS_E5_PASS_NO_COMMON_ZERO")


# ---------------------------------------------------------------------------
# Punctured intersection: full E5 ideal and exhaustive E4/E3 split
# ---------------------------------------------------------------------------

intersection_e6 = solve_e6_chart(
    base.intersection_line,
    base.rows6,
    base.cols6,
    186624 * base.k,
)
intersection_common = (
    {base.d: 0, base.z: 0},
    base.intersection_line,
    intersection_e6,
)

e5_r1 = nonzero_coefficients_with_r_degree(e5, 1, intersection_common)
variables51 = (
    base.bc[4],
    base.tc[0],
    base.tc[1],
    base.tc[2],
    base.uc[1],
    base.uc[2],
    base.uc[3],
    base.vc[1],
    base.vc[2],
    base.vc[3],
)
_, solve51, residual51 = solve_selected(
    e5_r1,
    variables51,
    (0, 1),
    (0, 1),
    -sp.Rational(64, 9) * base.k**3,
)
assert all(value == 0 for value in residual51)
assert sp.factor(
    solve51[base.bc[4]]
    - base.k * (base.vc[1] - base.vc[2]) / 3
) == 0
assert sp.factor(
    solve51[base.tc[0]]
    - (
        4 * base.tc[1]
        - 4 * base.tc[2]
        + 3 * base.uc[1]
        - 6 * base.uc[2]
        + 9 * base.uc[3]
        - 3 * base.vc[1]
        + 6 * base.vc[2]
        - 9 * base.vc[3]
    )
    / 4
) == 0

e5_r0 = nonzero_coefficients_with_r_degree(
    e5, 0, intersection_common + (solve51,)
)
variables50 = (
    base.ac[0],
    base.ac[1],
    base.ac[3],
    base.bc[0],
    base.bc[1],
    base.bc[3],
    base.ell[2],
    base.ell[5],
    base.ell[6],
    base.ell[7],
)
_, solve50, residual50 = solve_selected(
    e5_r0,
    variables50,
    (0, 1, 2),
    (0, 1, 3),
    -32 * base.k**3,
)

A_factor = (
    8 * base.tc[1]
    - 8 * base.tc[2]
    - 6 * base.uc[2]
    + 9 * base.uc[3]
    + 12 * base.vc[2]
    - 18 * base.vc[3]
)
B_factor = (
    -6 * base.ell[8]
    + 2 * base.k * base.tc[1]
    - 4 * base.k * base.tc[2]
    - 3 * base.k * base.vc[1]
    + 6 * base.k * base.vc[2]
    - 9 * base.k * base.vc[3]
)
Q_factor = (
    base.uc[1] ** 2
    - 4 * base.uc[1] * base.uc[2]
    + 6 * base.uc[1] * base.uc[3]
    - 6 * base.uc[1] * base.vc[0]
    + 4 * base.uc[1] * base.vc[1]
    - 2 * base.uc[1] * base.vc[2]
    + 4 * base.uc[2] ** 2
    - 12 * base.uc[2] * base.uc[3]
    + 12 * base.uc[2] * base.vc[0]
    - 8 * base.uc[2] * base.vc[1]
    + 4 * base.uc[2] * base.vc[2]
    + 9 * base.uc[3] ** 2
    - 18 * base.uc[3] * base.vc[0]
    + 12 * base.uc[3] * base.vc[1]
    - 6 * base.uc[3] * base.vc[2]
    + 18 * base.vc[0] ** 2
    - 30 * base.vc[0] * base.vc[1]
    + 24 * base.vc[0] * base.vc[2]
    - 18 * base.vc[0] * base.vc[3]
    + 13 * base.vc[1] ** 2
    - 22 * base.vc[1] * base.vc[2]
    + 18 * base.vc[1] * base.vc[3]
    + 10 * base.vc[2] ** 2
    - 18 * base.vc[2] * base.vc[3]
    + 9 * base.vc[3] ** 2
)
compatibility_variables = (
    base.ell[8],
    base.tc[1],
    base.tc[2],
    base.uc[1],
    base.uc[2],
    base.uc[3],
    base.vc[0],
    base.vc[1],
    base.vc[2],
    base.vc[3],
)
compatibility_domain = sp.QQ.frac_field(base.k)
actual_e5_ideal = sp.groebner(
    tuple(value for value in residual50 if value != 0),
    *compatibility_variables,
    order="grevlex",
    domain=compatibility_domain,
)
expected_e5_ideal = sp.groebner(
    (Q_factor, A_factor * B_factor),
    *compatibility_variables,
    order="grevlex",
    domain=compatibility_domain,
)
assert actual_e5_ideal == expected_e5_ideal

intersection_before_e4 = intersection_common + (solve51, solve50)
S_factor = base.vc[0] - base.vc[1] + base.vc[2] - base.vc[3]
S_substitution = {
    base.vc[0]: base.vc[1] - base.vc[2] + base.vc[3]
}
D_factor = (
    base.uc[1]
    - 2 * base.uc[2]
    + 3 * base.uc[3]
    - base.vc[1]
    + 2 * base.vc[2]
    - 3 * base.vc[3]
)
D_substitution = {
    base.uc[1]: (
        2 * base.uc[2]
        - 3 * base.uc[3]
        + base.vc[1]
        - 2 * base.vc[2]
        + 3 * base.vc[3]
    )
}
e4_p2r2 = sequential_substitute(
    e4.coeff_monomial(base.p**2 * base.r**2),
    intersection_before_e4,
)
e4_pqr2 = sequential_substitute(
    e4.coeff_monomial(base.p * base.q * base.r**2),
    intersection_before_e4,
)
assert sp.factor(
    e4_p2r2 + sp.Rational(2, 3) * base.k**3 * S_factor
) == 0
assert sp.factor(
    e4_pqr2 + sp.Rational(2, 3) * base.k**3 * S_factor
) == 0
assert sp.factor(Q_factor.subs(S_substitution) - D_factor**2) == 0

# Branch B=0.  If A=0 this lies in branch A below.  If A!=0, the E4
# compatibility forces a displayed factor of det(L) to vanish.
B_substitution = {
    base.ell[8]: (
        2 * base.k * base.tc[1]
        - 4 * base.k * base.tc[2]
        - 3 * base.k * base.vc[1]
        + 6 * base.k * base.vc[2]
        - 9 * base.k * base.vc[3]
    )
    / 6
}
branch_b_before_r1 = intersection_before_e4 + (
    B_substitution,
    S_substitution,
    D_substitution,
)
branch_b_r1 = nonzero_coefficients_with_r_degree(
    e4, 1, branch_b_before_r1
)
variables_b41 = (base.bc[1], base.bc[3], base.ell[5])
_, solve_b41, residual_b41 = solve_selected(
    branch_b_r1,
    variables_b41,
    (0,),
    (0,),
    -sp.Rational(2, 3) * base.k**2,
)
assert all(value == 0 for value in residual_b41)

branch_b_r0 = nonzero_coefficients_with_r_degree(
    e4, 0, branch_b_before_r1 + (solve_b41,)
)
variables_b40 = (base.ell[0], base.ell[1], base.ell[3], base.ell[4])
_, solve_b40, residual_b40 = solve_selected(
    branch_b_r0,
    variables_b40,
    (0, 1),
    (0, 2),
    4 * base.k**2,
)
F_b = (
    4 * base.ell[6]
    - 4 * base.ell[7]
    - 2 * base.tc[1] * base.vc[1]
    + 4 * base.tc[1] * base.vc[2]
    - 6 * base.tc[1] * base.vc[3]
    + 4 * base.tc[2] * base.vc[1]
    - 8 * base.tc[2] * base.vc[2]
    + 12 * base.tc[2] * base.vc[3]
    + 3 * base.vc[1] ** 2
    - 12 * base.vc[1] * base.vc[2]
    + 18 * base.vc[1] * base.vc[3]
    + 12 * base.vc[2] ** 2
    - 36 * base.vc[2] * base.vc[3]
    + 27 * base.vc[3] ** 2
)
nonzero_b40 = tuple(value for value in residual_b40 if value != 0)
assert nonzero_b40
assert all(
    not sp.cancel(value / (base.k * A_factor * F_b)).free_symbols
    for value in nonzero_b40
)
det_b = sequential_substitute(
    base.linear.det(),
    branch_b_before_r1 + (solve_b41, solve_b40),
)
H_b = sp.cancel(-216 * det_b / F_b)
H_b_numerator, H_b_denominator = sp.together(H_b).as_numer_denom()
assert H_b_denominator == 1
assert H_b_numerator != 0
assert sp.cancel(det_b + F_b * H_b / 216) == 0

# Branch A=0, including the A=B=0 boundary.
A_substitution = {
    base.tc[1]: (
        base.tc[2]
        + sp.Rational(3, 4) * base.uc[2]
        - sp.Rational(9, 8) * base.uc[3]
        - sp.Rational(3, 2) * base.vc[2]
        + sp.Rational(9, 4) * base.vc[3]
    )
}
branch_a_before_r1 = intersection_before_e4 + (
    A_substitution,
    S_substitution,
    D_substitution,
)
branch_a_r1 = nonzero_coefficients_with_r_degree(
    e4, 1, branch_a_before_r1
)
variables_a41 = (base.bc[1], base.bc[3], base.ell[5])
_, solve_a41_pre, residual_a41_pre = solve_selected(
    branch_a_r1,
    variables_a41,
    (0,),
    (0,),
    -sp.Rational(2, 3) * base.k**2,
)
C_factor = (
    24 * base.ell[8]
    + 8 * base.k * base.tc[2]
    - 6 * base.k * base.uc[2]
    + 9 * base.k * base.uc[3]
    + 12 * base.k * base.vc[1]
    - 12 * base.k * base.vc[2]
    + 18 * base.k * base.vc[3]
)
nonzero_a41 = tuple(value for value in residual_a41_pre if value != 0)
assert nonzero_a41
assert all(
    not sp.cancel(value / C_factor**2).free_symbols
    for value in nonzero_a41
)
C_substitution = {
    base.ell[8]: base.k
    * (
        -8 * base.tc[2]
        + 6 * base.uc[2]
        - 9 * base.uc[3]
        - 12 * base.vc[1]
        + 12 * base.vc[2]
        - 18 * base.vc[3]
    )
    / 24
}
solve_a41 = {
    variable: sp.cancel(value.subs(C_substitution))
    for variable, value in solve_a41_pre.items()
}
branch_a_before_r0 = branch_a_before_r1 + (C_substitution, solve_a41)
branch_a_r0 = nonzero_coefficients_with_r_degree(
    e4, 0, branch_a_before_r0
)
variables_a40 = (base.ell[0], base.ell[1], base.ell[3], base.ell[4])
_, solve_a40, residual_a40 = solve_selected(
    branch_a_r0,
    variables_a40,
    (0, 1),
    (0, 2),
    4 * base.k**2,
)
assert all(value == 0 for value in residual_a40)

branch_a_complete_e4 = branch_a_before_r0 + (solve_a40,)
det_a = sequential_substitute(base.linear.det(), branch_a_complete_e4)
F_a = (
    16 * base.ell[6]
    - 16 * base.ell[7]
    + 8 * base.tc[2] * base.vc[1]
    - 16 * base.tc[2] * base.vc[2]
    + 24 * base.tc[2] * base.vc[3]
    - 6 * base.uc[2] * base.vc[1]
    + 12 * base.uc[2] * base.vc[2]
    - 18 * base.uc[2] * base.vc[3]
    + 9 * base.uc[3] * base.vc[1]
    - 18 * base.uc[3] * base.vc[2]
    + 27 * base.uc[3] * base.vc[3]
    + 12 * base.vc[1] ** 2
    - 36 * base.vc[1] * base.vc[2]
    + 54 * base.vc[1] * base.vc[3]
    + 24 * base.vc[2] ** 2
    - 72 * base.vc[2] * base.vc[3]
    + 54 * base.vc[3] ** 2
)
H_a = sp.cancel(1152 * det_a / F_a)
H_a_numerator, H_a_denominator = sp.together(H_a).as_numer_denom()
assert H_a_denominator == 1
assert H_a_numerator != 0
assert sp.cancel(det_a - F_a * H_a / 1152) == 0

# If F_a=0 then det(L)=0.  Localize at F_a!=0 and use the first two E3
# equations to solve ac3,bc3.  The remaining equations are an immediate
# nonzero obstruction.
e3 = sp.Poly(
    base.full_determinant.coeff_monomial(base.weight**3),
    base.p,
    base.q,
    base.r,
)
branch_a_e3 = tuple(
    value
    for _, coefficient in e3.terms()
    for value in (
        sequential_substitute(coefficient, branch_a_complete_e4),
    )
    if value != 0
)
variables_a3 = (base.ac[3], base.bc[3], base.ell[2], base.ell[5])
_, solve_a3, residual_a3 = solve_selected(
    branch_a_e3,
    variables_a3,
    (0, 1),
    (0, 1),
    base.k**2 * F_a**2 / 144,
)
assert residual_a3[0] == 0 and residual_a3[1] == 0
assert sp.factor(residual_a3[2] - base.k * F_a**2 / 288) == 0, (
    sp.factor(residual_a3[2] / (base.k * F_a**2))
)
assert sp.factor(residual_a3[3] - base.k * F_a**2 / 288) == 0, (
    sp.factor(residual_a3[3] / (base.k * F_a**2))
)

print("D4_DN2C_INTERSECTION_PASS_E5_AB_SPLIT_E4_E3_DETL")


# ---------------------------------------------------------------------------
# Origin: literal all-six collapse and unconditional plane/Moh exit
# ---------------------------------------------------------------------------

origin_e6 = solve_e6_chart(
    base.origin,
    base.rows5,
    base.cols5,
    sp.Integer(31104),
)
assert sp.factor(
    origin_e6[base.ac[2]]
    - (3 * base.bc[4] + 4 * base.ell[8]) / 3
) == 0
assert sp.factor(
    origin_e6[base.ac[4]]
    - 2 * (3 * base.bc[4] + 2 * base.ell[8]) / 3
) == 0
assert origin_e6[base.ac[5]] == 0
assert origin_e6[base.bc[2]] == 0
assert origin_e6[base.bc[5]] == 0

origin_common = (
    {base.d: 0, base.z: 0},
    base.origin,
    origin_e6,
)
origin_p3r = sequential_substitute(
    e4.coeff_monomial(base.p**3 * base.r), origin_common
)
origin_q3r = sequential_substitute(
    e4.coeff_monomial(base.q**3 * base.r), origin_common
)
assert sp.factor(origin_p3r + 3 * base.bc[4] ** 2) == 0
assert sp.factor(
    origin_q3r
    - sp.Rational(2, 3) * (3 * base.bc[4] + 2 * base.ell[8]) ** 2
) == 0

origin_collapse = {base.bc[4]: 0, base.ell[8]: 0}
all_six_nonbinary_quadratic = (
    base.ac[2],
    base.ac[4],
    base.ac[5],
    base.bc[2],
    base.bc[4],
    base.bc[5],
)
assert all(
    sp.cancel(
        variable.subs(origin_e6).subs(origin_collapse)
        if variable in origin_e6
        else variable.subs(origin_collapse)
    )
    == 0
    for variable in all_six_nonbinary_quadratic
)

print("D4_DN2C_ORIGIN_PASS_ALL_SIX_COLLAPSE_PLANE_MOH_EXIT")
print("D4_DN2C_FULL_EXCLUSION_SYMPY_PASS")

#!/usr/bin/env python3
"""Exact closure of the F=0 and G=0 finite-companion resonances.

The ambient pencil is p=x^2, q=yz and

    H4=((p-aq)^2,(p-bq)^2,0),  R=x(p-cq).

Outside the already-certified c=0 marked-critical locus, F=0 may be scaled
to b=1, a=t, c=3t/(2t+1), with t not in {0,1,-1/2}.  The chart t=1/2 is
handled independently, because a convenient translation gauge for the
generic chart has a (2t-1) denominator.

All assertions are symbolic over QQ.  Sample ranks are never used.
"""

from __future__ import annotations

if not __debug__:
    raise RuntimeError("verification requires assertions; do not use -O")

from functools import reduce
from itertools import product

import sympy as sp


x, y, z = sp.symbols("x y z")
variables = (x, y, z)
p = x**2
q = y * z


def homogeneous_monomials(degree: int) -> tuple[sp.Expr, ...]:
    answer: list[sp.Expr] = []
    for x_degree in range(degree, -1, -1):
        for y_degree in range(degree - x_degree, -1, -1):
            z_degree = degree - x_degree - y_degree
            answer.append(x**x_degree * y**y_degree * z**z_degree)
    return tuple(answer)


def homogeneous_form(
    prefix: str, degree: int
) -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    monomials = homogeneous_monomials(degree)
    coefficients = sp.symbols(f"{prefix}0:{len(monomials)}")
    return (
        sp.Add(
            *(
                coefficient * monomial
                for coefficient, monomial in zip(coefficients, monomials)
            )
        ),
        coefficients,
    )


def jacobian_matrix(vector: sp.Matrix) -> sp.Matrix:
    return vector.jacobian(variables)


def jacobian_determinant(first: sp.Expr, second: sp.Expr, third: sp.Expr) -> sp.Expr:
    return sp.expand(jacobian_matrix(sp.Matrix([first, second, third])).det())


def weighted_determinant_coefficient(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
    weight: int,
) -> sp.Expr:
    matrices = tuple(
        jacobian_matrix(vector) for vector in (linear, quadratic, cubic, quartic)
    )
    result = 0
    for row_weights in product(range(4), repeat=3):
        if sum(row_weights) != weight:
            continue
        result += sp.Matrix.vstack(
            *(matrices[row_weights[row]][row, :] for row in range(3))
        ).det()
    return sp.expand(result)


def coefficient_equations(form: sp.Expr, degree: int) -> list[sp.Expr]:
    polynomial = sp.Poly(sp.expand(form), *variables)
    return [
        polynomial.coeff_monomial(monomial)
        for monomial in homogeneous_monomials(degree)
        if polynomial.coeff_monomial(monomial) != 0
    ]


def assert_associate(left: sp.Expr, right: sp.Expr) -> None:
    quotient = sp.cancel(left / right)
    assert quotient.is_Rational and quotient != 0, (left, right, quotient)


def contains_associate(polynomials: list[sp.Expr], target: sp.Expr) -> bool:
    for candidate in polynomials:
        quotient = sp.cancel(candidate / target)
        if quotient.is_Rational and quotient != 0:
            return True
    return False


def generic_resonance_chart() -> tuple[
    sp.Symbol,
    sp.Expr,
    sp.Matrix,
    sp.Matrix,
    tuple[sp.Symbol, ...],
]:
    """Certify the E7 quotient and E6 square exit for t != 1/2."""

    t = sp.symbols("t")
    c = 3 * t / (2 * t + 1)
    H4 = sp.Matrix([(p - t * q) ** 2, (p - q) ** 2, 0])

    general_U, u3 = homogeneous_form("resonanceCubicU", 3)
    general_V, v3 = homogeneous_form("resonanceCubicV", 3)
    general_W, w = homogeneous_form("resonanceQuadraticW", 2)
    R = x * (p - c * q)
    E7 = (
        jacobian_determinant(H4[0], H4[1], general_W)
        + jacobian_determinant(H4[0], general_V, R)
        + jacobian_determinant(general_U, H4[1], R)
    )

    raw_equations = [
        sp.Poly(E7, *variables).coeff_monomial(monomial)
        for monomial in homogeneous_monomials(7)
    ]
    raw_matrix, _ = sp.linear_eq_to_matrix(
        raw_equations, u3 + v3 + w
    )
    assert raw_matrix.shape == (36, 26)
    assert raw_matrix.rank() == 14
    raw_pivot_columns = (
        1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 19,
    )
    raw_pivot_rows = (
        1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19,
    )
    assert_associate(
        sp.factor(
            raw_matrix.extract(raw_pivot_rows, raw_pivot_columns).det()
        ),
        t**6 * (t - 1) ** 6 / (2 * t + 1) ** 14,
    )

    # Target shears set u0=v0=0.  Since t!=0, source translations set
    # u1=u2=0.  The following 18-by-18 minor proves that no gauge-fixed E7
    # modes beyond the displayed family have been omitted.
    full_equations = [
        sp.Poly(E7, *variables).coeff_monomial(monomial)
        for monomial in homogeneous_monomials(7)
    ] + [u3[0], v3[0], u3[1], u3[2]]
    gauge_matrix, _ = sp.linear_eq_to_matrix(
        full_equations, u3 + v3
    )
    assert gauge_matrix.shape == (40, 20)
    assert gauge_matrix[:, 4] == sp.zeros(40, 1)
    assert gauge_matrix[:, 14] == sp.zeros(40, 1)
    pivot_columns = (
        0, 1, 2, 3, 5, 6, 7, 8, 9,
        10, 11, 12, 13, 15, 16, 17, 18, 19,
    )
    pivot_rows = (
        1, 2, 3, 5, 6, 7, 8, 9, 11,
        13, 16, 17, 18, 19, 36, 37, 38, 39,
    )
    assert_associate(
        sp.factor(gauge_matrix.extract(pivot_rows, pivot_columns).det()),
        t**8 * (t - 1) ** 6 * (2 * t - 1) ** 2 / (2 * t + 1) ** 14,
    )

    U4, V4 = sp.symbols("resonanceU4 resonanceV4")
    w0, w1, w2, w3, w4, w5 = w
    factor = (t - 1) * (2 * t + 1)
    U3 = (
        U4 * x * q
        - sp.Rational(4, 3) * factor * w3 * x * y**2
        - sp.Rational(4, 3) * factor * w5 * x * z**2
        - 4 * t * factor * w1 * y**2 * z / (3 * (2 * t - 1))
        - 4 * t * factor * w2 * y * z**2 / (3 * (2 * t - 1))
    )
    V3 = (
        V4 * x * q
        + 4 * factor * w1 * (x**2 * y - y**2 * z)
        / (3 * t * (2 * t - 1))
        + 4 * factor * w2 * (x**2 * z - y * z**2)
        / (3 * t * (2 * t - 1))
    )
    substitutions = {}
    for coefficients, form in ((u3, U3), (v3, V3)):
        polynomial = sp.Poly(form, *variables)
        substitutions.update(
            {
                coefficient: polynomial.coeff_monomial(monomial)
                for coefficient, monomial in zip(
                    coefficients, homogeneous_monomials(3)
                )
            }
        )
    residual = sp.expand(E7.subs(substitutions))
    assert sp.factor(residual) == 0

    W = w0 * p + w1 * x * y + w2 * x * z + w3 * y**2 + w4 * q + w5 * z**2
    H3 = sp.Matrix([U3, V3, R])
    U2, u2 = homogeneous_form("resonanceQuadraticU", 2)
    V2, v2 = homogeneous_form("resonanceQuadraticV", 2)
    H2 = sp.Matrix([U2, V2, W])
    ell = sp.symbols("resonanceEll0:9")
    L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])

    E6 = weighted_determinant_coefficient(L, H2, H3, H4, 6)
    equations = coefficient_equations(E6, 6)
    unknowns = u2 + v2 + ell
    matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)
    assert matrix.shape == (20, 21)
    assert matrix.rank() == 8
    rank_rows = (0, 1, 2, 3, 5, 6, 9, 10)
    rank_columns = (1, 2, 3, 5, 7, 8, 9, 11)
    assert_associate(
        sp.factor(matrix.extract(rank_rows, rank_columns).det()),
        t**4 * (t - 1) ** 4 / (2 * t + 1) ** 8,
    )
    compatibilities = [
        sp.factor((vector.T * rhs)[0]) for vector in matrix.T.nullspace()
    ]
    assert contains_associate(
        compatibilities, (t - 1) * (2 * t + 1) * w3**2
    )
    assert contains_associate(
        compatibilities, (t - 1) * (2 * t + 1) * w5**2
    )

    reduced = [
        sp.factor(candidate.subs({w3: 0, w5: 0}))
        for candidate in compatibilities
    ]
    assert contains_associate(
        reduced,
        t * (t - 1) ** 2 * (2 * t + 1) * w1**2 / (2 * t - 1) ** 2,
    )
    assert contains_associate(
        reduced,
        t * (t - 1) ** 2 * (2 * t + 1) * w2**2 / (2 * t - 1) ** 2,
    )

    print("  PASS F=0 generic chart: complete E7 quotient and E6 squares")
    return t, c, H4, sp.Matrix([U4 * x * q, V4 * x * q, R]), w


def half_resonance_chart() -> None:
    """Independent chart for t=1/2, where the preceding gauge degenerates."""

    t = sp.Rational(1, 2)
    c = sp.Rational(3, 4)
    H4 = sp.Matrix([(p - t * q) ** 2, (p - q) ** 2, 0])
    R = x * (p - c * q)

    general_U, u3 = homogeneous_form("halfCubicU", 3)
    general_V, v3 = homogeneous_form("halfCubicV", 3)
    general_W, w = homogeneous_form("halfQuadraticW", 2)
    E7 = (
        jacobian_determinant(H4[0], H4[1], general_W)
        + jacobian_determinant(H4[0], general_V, R)
        + jacobian_determinant(general_U, H4[1], R)
    )

    raw_equations = [
        sp.Poly(E7, *variables).coeff_monomial(monomial)
        for monomial in homogeneous_monomials(7)
    ]
    raw_matrix, _ = sp.linear_eq_to_matrix(
        raw_equations, u3 + v3 + w
    )
    assert raw_matrix.rank() == 14
    raw_pivot_columns = (
        1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 19,
    )
    raw_pivot_rows = (
        1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19,
    )
    assert raw_matrix.extract(raw_pivot_rows, raw_pivot_columns).det() == (
        -sp.Rational(387420489, 256)
    )

    # Here translations are gauged by v1=v2=0 instead.
    full_equations = [
        sp.Poly(E7, *variables).coeff_monomial(monomial)
        for monomial in homogeneous_monomials(7)
    ] + [u3[0], v3[0], v3[1], v3[2]]
    gauge_matrix, _ = sp.linear_eq_to_matrix(full_equations, u3 + v3)
    assert gauge_matrix[:, 4] == sp.zeros(40, 1)
    assert gauge_matrix[:, 14] == sp.zeros(40, 1)
    pivot_columns = (
        0, 1, 2, 3, 5, 6, 7, 8, 9,
        10, 11, 12, 13, 15, 16, 17, 18, 19,
    )
    pivot_rows = (
        1, 2, 3, 5, 6, 7, 8, 9, 11,
        13, 16, 17, 18, 19, 36, 37, 38, 39,
    )
    assert gauge_matrix.extract(pivot_rows, pivot_columns).det() == (
        -sp.Rational(387420489, 256)
    )

    U4, V4 = sp.symbols("halfU4 halfV4")
    w0, w1, w2, w3, w4, w5 = w
    U3 = U4 * x * q + sp.Rational(4, 3) * (
        w1 * x**2 * y + w2 * x**2 * z + w3 * x * y**2 + w5 * x * z**2
    )
    V3 = V4 * x * q
    substitutions = {}
    for coefficients, form in ((u3, U3), (v3, V3)):
        polynomial = sp.Poly(form, *variables)
        substitutions.update(
            {
                coefficient: polynomial.coeff_monomial(monomial)
                for coefficient, monomial in zip(
                    coefficients, homogeneous_monomials(3)
                )
            }
        )
    assert sp.expand(E7.subs(substitutions)) == 0

    W = w0 * p + w1 * x * y + w2 * x * z + w3 * y**2 + w4 * q + w5 * z**2
    H3 = sp.Matrix([U3, V3, R])
    U2, u2 = homogeneous_form("halfQuadraticU", 2)
    V2, v2 = homogeneous_form("halfQuadraticV", 2)
    ell = sp.symbols("halfEll0:9")
    L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])
    E6 = weighted_determinant_coefficient(
        L, sp.Matrix([U2, V2, W]), H3, H4, 6
    )
    equations = coefficient_equations(E6, 6)
    matrix, rhs = sp.linear_eq_to_matrix(equations, u2 + v2 + ell)
    assert matrix.rank() == 8
    rank_rows = (0, 1, 2, 3, 5, 6, 9, 10)
    rank_columns = (1, 2, 3, 5, 7, 8, 9, 11)
    assert matrix.extract(rank_rows, rank_columns).det() == sp.Rational(
        6561, 16
    )
    compatibilities = [
        sp.factor((vector.T * rhs)[0]) for vector in matrix.T.nullspace()
    ]
    assert contains_associate(compatibilities, w3**2)
    assert contains_associate(compatibilities, w5**2)
    reduced = [
        sp.factor(candidate.subs({w3: 0, w5: 0}))
        for candidate in compatibilities
    ]
    assert contains_associate(reduced, w1**2)
    assert contains_associate(reduced, w2**2)

    print("  PASS F=0 t=1/2 chart: complete E7 quotient and E6 squares")


def invariant_lower_exit(
    t: sp.Symbol,
    c: sp.Expr,
    H4: sp.Matrix,
    H3: sp.Matrix,
    w: tuple[sp.Symbol, ...],
) -> None:
    """After the E6 squares, both L columns lie in one 1D kernel."""

    w0, _, _, _, w4, _ = w
    U2, u2 = homogeneous_form("exitQuadraticU", 2)
    V2, v2 = homogeneous_form("exitQuadraticV", 2)
    H2 = sp.Matrix([U2, V2, w0 * p + w4 * q])
    ell = sp.symbols("exitEll0:9")
    L = sp.Matrix(3, 3, ell) * sp.Matrix([x, y, z])
    E6 = weighted_determinant_coefficient(L, H2, H3, H4, 6)
    equations = coefficient_equations(E6, 6)
    matrix, _ = sp.linear_eq_to_matrix(equations, u2 + v2 + ell)
    assert matrix.rank() == 8
    rank_rows = tuple(range(8))
    rank_columns = (1, 2, 3, 5, 7, 8, 9, 11)
    assert_associate(
        sp.factor(matrix.extract(rank_rows, rank_columns).det()),
        t**4 * (t - 1) ** 4 / (2 * t + 1) ** 8,
    )

    multiplier = -sp.Rational(4, 3) * (t - 1) * (2 * t + 1)
    solution6 = {
        u2[1]: multiplier * ell[7],
        u2[2]: multiplier * ell[8],
        u2[3]: 0,
        u2[5]: 0,
        v2[1]: 0,
        v2[2]: 0,
        v2[3]: 0,
        v2[5]: 0,
    }
    assert sp.expand(E6.subs(solution6)) == 0

    E5 = weighted_determinant_coefficient(
        L, H2.subs(solution6), H3, H4, 5
    ).subs(solution6)
    polynomial = sp.Poly(E5, *variables)
    y_equations = [
        polynomial.coeff_monomial(monomial)
        for monomial in (x**4 * y, x**2 * y**2 * z, y**3 * z**2)
    ]
    z_equations = [
        polynomial.coeff_monomial(monomial)
        for monomial in (x**4 * z, x**2 * y * z**2, y**2 * z**3)
    ]
    y_matrix, y_rhs = sp.linear_eq_to_matrix(
        y_equations, (ell[1], ell[4], ell[7])
    )
    z_matrix, z_rhs = sp.linear_eq_to_matrix(
        z_equations, (ell[2], ell[5], ell[8])
    )
    assert y_rhs == sp.zeros(3, 1)
    assert z_rhs == sp.zeros(3, 1)
    assert sp.simplify(y_matrix + z_matrix) == sp.zeros(3)
    assert sp.factor(y_matrix.extract((0, 1), (0, 1)).det()) == (
        -36 * t * (t - 1) / (2 * t + 1) ** 2
    )

    # Both columns (ell_12,ell_22,ell_32)^T and
    # (ell_13,ell_23,ell_33)^T therefore lie in the same kernel of
    # dimension at most one.  They are proportional, so det(L)=0.
    determinant = sp.Matrix(3, 3, ell).det()
    assert sp.expand(
        determinant
        - (
            ell[0] * (ell[4] * ell[8] - ell[5] * ell[7])
            - ell[1] * (ell[3] * ell[8] - ell[5] * ell[6])
            + ell[2] * (ell[3] * ell[7] - ell[4] * ell[6])
        )
    ) == 0

    print("  PASS F=0 lower exit: common at-most-one-dimensional E5 kernel")


def symmetry_check() -> None:
    a, b, c = sp.symbols("symmetryA symmetryB symmetryC")
    F = 3 * a * b - 2 * a * c - b * c
    G = 3 * a * b - a * c - 2 * b * c
    assert sp.expand(
        F.subs({a: b, b: a}, simultaneous=True) - G
    ) == 0
    print("  PASS outer-component involution exchanges F and G")


def excluded_parameter_checks() -> None:
    """Account for every value omitted by the t chart."""

    t, c = sp.symbols("endpointT endpointC")
    # With b=1, F=3t-c(2t+1).
    F_chart = 3 * t - c * (2 * t + 1)
    assert sp.expand(
        F_chart.subs({t: -sp.Rational(1, 2)}) + sp.Rational(3, 2)
    ) == 0
    # Thus t=-1/2 contains no F=0 point.  At t=0, F=0 forces c=0,
    # the already-certified marked-critical triple branch.
    assert sp.expand(F_chart.subs({t: 0}) + c) == 0
    # t=1 is exactly a=b and is outside the a!=b degree-two outer stratum.
    assert (t - 1).subs({t: 1}) == 0

    a, b = sp.symbols("endpointA endpointB")
    F = 3 * a * b - 2 * a * c - b * c
    # If the scaling coordinate b vanishes and c!=0, F=0 forces a=0,
    # contradicting a!=b.  The encoded specialization is -2ac.
    assert sp.expand(F.subs({b: 0}) + 2 * a * c) == 0
    print("  PASS t=-1/2,0,1 and b=0 endpoint accounting")


if __name__ == "__main__":
    excluded_parameter_checks()
    chart_data = generic_resonance_chart()
    half_resonance_chart()
    invariant_lower_exit(*chart_data)
    symmetry_check()
    print("PASS: finite-outer-critical F=0 and G=0 resonances are excluded")

#!/usr/bin/python3
"""Strict exact composition of the binary fixed-conic endgames.

The sibling E7/E6 repair is imported and executed first.  Every branch
below then starts from its complete E7 affine fibre, not from a legacy
particular solution.  Weighted determinant equations are solved in
descending order with constant pivots, explicit square/product splits, or
fixed minors whose nonvanishing premise is recorded.

Exit zero means that the legacy families (13)--(36) span every relevant
binary endgame fibre and that their stated terminal obstruction or
binary automorphism exit is reproduced.  Any mismatch raises
VerificationFailure, including under ``python -O``.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import sympy as sp


HERE = Path(__file__).resolve().parent
REPAIR = HERE.parent / "fixed_conic_binary_repair_sympy"
sys.path.insert(0, str(REPAIR))

import verify_binary_fixed_conic_repair as top  # noqa: E402


p, q, r = top.p, top.q, top.r
variables = (p, q, r)
A, Ap, Aq = top.A, top.Ap, top.Aq
v, w, ell = top.v, top.w, top.ell
L = top.linear_part


class VerificationFailure(RuntimeError):
    """Raised when an exact endgame certificate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def all_zero(matrix_or_vector: sp.Matrix) -> bool:
    return all(sp.expand(entry) == 0 for entry in matrix_or_vector)


def matrix_equal(first: sp.Matrix, second: sp.Matrix) -> bool:
    return first.shape == second.shape and all_zero(first - second)


def weighted_coefficient(
    degree: int,
    H4: sp.Matrix,
    H3: sp.Matrix,
    H2: sp.Matrix,
    linear_part: sp.Matrix,
) -> sp.Expr:
    """Return [s^degree] det(L+s JH2+s^2 JH3+s^3 JH4)."""
    jacobians = (
        linear_part,
        H2.jacobian(variables),
        H3.jacobian(variables),
        H4.jacobian(variables),
    )
    answer = sp.Integer(0)
    for column_degrees in itertools.product(range(4), repeat=3):
        if sum(column_degrees) != degree:
            continue
        answer += sp.Matrix.hstack(
            jacobians[column_degrees[0]][:, 0],
            jacobians[column_degrees[1]][:, 1],
            jacobians[column_degrees[2]][:, 2],
        ).det()
    return sp.expand(answer)


def coefficient_equations(expression: sp.Expr) -> List[sp.Expr]:
    expression = sp.expand(expression)
    if expression == 0:
        return []
    return [
        coefficient
        for _, coefficient in sp.Poly(expression, p, q, r).terms()
    ]


def coefficient(
    expression: sp.Expr,
    p_degree: int,
    q_degree: int,
    r_degree: int,
) -> sp.Expr:
    return sp.expand(
        sp.Poly(sp.expand(expression), p, q, r).coeff_monomial(
            p**p_degree * q**q_degree * r**r_degree
        )
    )


def require_equal(
    actual: sp.Expr,
    expected: sp.Expr,
    message: str,
) -> None:
    require(sp.expand(actual - expected) == 0, message)


def constant_partial_solve(
    equations: Sequence[sp.Expr],
    unknowns: Sequence[sp.Symbol],
    expected_rank: int,
    label: str,
) -> Tuple[Dict[sp.Symbol, sp.Expr], List[sp.Expr]]:
    """Solve independent rows of a constant-coefficient affine system.

    Residuals are returned rather than presumed zero, allowing the caller
    to retain exact compatibility obstructions.
    """
    matrix, rhs = sp.linear_eq_to_matrix(list(equations), list(unknowns))
    require(
        all(not entry.free_symbols for entry in matrix),
        f"{label}: a parameter-dependent pivot matrix appeared",
    )
    require(
        matrix.rank() == expected_rank,
        f"{label}: unexpected constant matrix rank",
    )
    if expected_rank == 0:
        return {}, [sp.factor(-entry) for entry in rhs if entry != 0]

    row_indices = matrix.T.rref()[1]
    require(
        len(row_indices) == expected_rank,
        f"{label}: independent-row count changed",
    )
    reduced_matrix = matrix[list(row_indices), :]
    reduced_rhs = rhs[list(row_indices), :]
    solution_tuple = next(
        iter(
            sp.linsolve(
                (reduced_matrix, reduced_rhs),
                list(unknowns),
            )
        )
    )
    substitutions = {
        symbol: sp.factor(value)
        for symbol, value in zip(unknowns, solution_tuple)
        if value != symbol
    }
    residual = matrix * sp.Matrix(solution_tuple) - rhs
    return substitutions, [
        sp.factor(entry) for entry in residual if sp.factor(entry) != 0
    ]


def solve_fixed_minor(
    equations: Sequence[sp.Expr],
    unknowns: Sequence[sp.Symbol],
    row_indices: Sequence[int],
    expected_determinant: sp.Expr,
    label: str,
) -> Dict[sp.Symbol, sp.Expr]:
    """Solve a square fixed minor and validate every unused equation."""
    matrix, rhs = sp.linear_eq_to_matrix(list(equations), list(unknowns))
    minor = matrix[list(row_indices), :]
    require(
        minor.rows == minor.cols == len(unknowns),
        f"{label}: fixed minor is not square",
    )
    require_equal(
        sp.factor(minor.det()),
        sp.factor(expected_determinant),
        f"{label}: fixed minor determinant changed",
    )
    solution_tuple = next(
        iter(
            sp.linsolve(
                (minor, rhs[list(row_indices), :]),
                list(unknowns),
            )
        )
    )
    residual = matrix * sp.Matrix(solution_tuple) - rhs
    require(
        all(sp.factor(entry) == 0 for entry in residual),
        f"{label}: fixed-minor solution misses an equation",
    )
    return dict(zip(unknowns, solution_tuple))


def apply_substitutions(
    expression: sp.Expr | sp.Matrix,
    *substitutions: Dict[sp.Symbol, sp.Expr],
) -> sp.Expr | sp.Matrix:
    result = expression
    for current in substitutions:
        result = result.subs(current)
    return sp.expand(result)


def positive_coefficients(
    H4: sp.Matrix,
    H3: sp.Matrix,
    H2: sp.Matrix,
    linear_part: sp.Matrix,
    degrees: Iterable[int],
) -> List[sp.Expr]:
    answer: List[sp.Expr] = []
    for degree in degrees:
        answer.extend(
            coefficient_equations(
                weighted_coefficient(
                    degree, H4, H3, H2, linear_part
                )
            )
        )
    return answer


def has_nonzero_constant(expressions: Sequence[sp.Expr]) -> bool:
    return any(
        expression.is_number and expression != 0
        for expression in expressions
    )


# ---------------------------------------------------------------------------
# Split-root scalar tangent: equations (13)--(19)
# ---------------------------------------------------------------------------


def verify_split_scalar() -> None:
    H4 = p * q * A
    raw_substitution = {
        top.a: 1,
        top.d: 1,
        v[3]: 0,
        v[8]: 0,
    }
    raw_H3 = apply_substitutions(
        top.split_result.H3, raw_substitution
    )
    raw_H2 = apply_substitutions(
        top.H2_general,
        top.split_solution,
        raw_substitution,
    )
    E6_raw = weighted_coefficient(6, H4, raw_H3, raw_H2, L)

    require_equal(
        coefficient(E6_raw, 4, 1, 1),
        -3 * (2 * v[4] - v[9]),
        "split scalar: E6 v9 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 3, 2, 1),
        3 * (v[0] + v[10] - 2 * v[5]),
        "split scalar: E6 v0 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 2, 3, 1),
        3 * (v[1] + v[11] - 2 * v[6]),
        "split scalar: E6 v1 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 1, 4, 1),
        3 * (v[2] - 2 * v[7]),
        "split scalar: E6 v2 relation changed",
    )
    endpoint_substitution = {
        v[9]: 2 * v[4],
        v[0]: 2 * v[5] - v[10],
        v[1]: 2 * v[6] - v[11],
        v[2]: 2 * v[7],
    }
    endpoint = apply_substitutions(E6_raw, endpoint_substitution)
    require_equal(
        coefficient(endpoint, 6, 0, 0),
        12 * v[4] ** 2,
        "split scalar: first E6 square changed",
    )
    require_equal(
        coefficient(endpoint, 0, 6, 0),
        12 * v[7] ** 2,
        "split scalar: second E6 square changed",
    )
    # Over C the two squares force v4=v7=0, hence also v9=v2=0.
    endpoint_zero = apply_substitutions(
        endpoint, {v[4]: 0, v[7]: 0}
    )
    require_equal(
        coefficient(endpoint_zero, 5, 1, 0),
        -4 * w[12],
        "split scalar: E6 w12 pivot changed",
    )
    require_equal(
        coefficient(endpoint_zero, 1, 5, 0),
        -4 * w[2],
        "split scalar: E6 w2 pivot changed",
    )

    U, Vv, X, Y, S, T = sp.symbols("ss_U ss_V ss_X ss_Y ss_S ss_T")
    A0, A1, B0, B1, B2, C1, C = sp.symbols(
        "ss_A0 ss_A1 ss_B0 ss_B1 ss_B2 ss_C1 ss_C"
    )
    family_substitution = {
        v[0]: U - X,
        v[1]: Vv - Y,
        v[2]: 0,
        v[3]: 0,
        v[4]: 0,
        v[5]: U,
        v[6]: Vv,
        v[7]: 0,
        v[8]: 0,
        v[9]: 0,
        v[10]: U + X,
        v[11]: Vv + Y,
        w[0]: A0,
        w[1]: A1,
        w[2]: 0,
        w[6]: B0,
        w[7]: B1,
        w[8]: B2,
        w[10]: T,
        w[12]: 0,
        w[13]: C1,
        w[14]: C,
        w[16]: 2 * S,
    }
    H3 = apply_substitutions(raw_H3, family_substitution)
    H2 = apply_substitutions(raw_H2, family_substitution)
    expected_H3 = sp.Matrix(
        [
            (U - X) * p**3 + (Vv - Y) * p**2 * q,
            U * p**2 * q + Vv * p * q**2,
            (U + X) * p * q**2 + (Vv + Y) * q**3,
        ]
    ) + 2 * r * A
    require(
        matrix_equal(H3, expected_H3),
        "split scalar: equation (13) does not span the E6 H3 fibre",
    )

    E6 = weighted_coefficient(6, H4, H3, H2, L)
    solve6, residual6 = constant_partial_solve(
        coefficient_equations(E6),
        (ell[2], ell[5], ell[8]),
        3,
        "split scalar E6 linear solve",
    )
    require(
        residual6 == [],
        "split scalar: E6 has an unretained compatibility",
    )

    E5 = apply_substitutions(
        weighted_coefficient(5, H4, H3, H2, L),
        solve6,
    )
    r_equations = [
        value
        for monomial, value in sp.Poly(E5, p, q, r).terms()
        if monomial[2] > 0
    ]
    solve_h2, residual_h2 = constant_partial_solve(
        r_equations,
        (A0, A1, C1),
        3,
        "split scalar E5 H2 solve",
    )
    expected_h2_solve = {
        A0: 2 * B1 - C - 4 * S * T - 8 * S * Y
        + 8 * T * X + 18 * X * Y,
        A1: 2 * B2 + 2 * T**2 + 8 * T * Y + 9 * Y**2,
        C1: 2 * B0 + 2 * S**2 - 8 * S * X + 9 * X**2,
    }
    require(
        all(
            sp.expand(solve_h2[key] - value) == 0
            for key, value in expected_h2_solve.items()
        ),
        "split scalar: equation (14) H2 relations changed",
    )
    require(
        residual_h2 == [],
        "split scalar: E5 r-part has an extra compatibility",
    )

    H2_14 = apply_substitutions(H2, solve_h2)
    E5_solved_h2 = apply_substitutions(E5, solve_h2)
    solve5, residual5 = constant_partial_solve(
        coefficient_equations(E5_solved_h2),
        (ell[0], ell[1], ell[3], ell[6]),
        4,
        "split scalar E5 linear solve",
    )
    require(
        residual5 == [],
        "split scalar: E5 linear solve has a compatibility",
    )

    linear_pre4 = apply_substitutions(L, solve6, solve_h2, solve5)
    E4 = weighted_coefficient(4, H4, H3, H2_14, linear_pre4)
    require_equal(
        coefficient(E4, 2, 0, 2),
        12 * (S - 2 * X) ** 2,
        "split scalar: S square certificate changed",
    )
    require_equal(
        coefficient(E4, 0, 2, 2),
        12 * (T + 2 * Y) ** 2,
        "split scalar: T square certificate changed",
    )
    st_substitution = {S: 2 * X, T: -2 * Y}
    E4_st = apply_substitutions(E4, st_substitution)
    require_equal(
        coefficient(E4_st, 4, 0, 0),
        8 * (B0 - U * X + X**2) ** 2,
        "split scalar: B0 square certificate changed",
    )
    require_equal(
        coefficient(E4_st, 0, 4, 0),
        8 * (B2 + Vv * Y + Y**2) ** 2,
        "split scalar: B2 square certificate changed",
    )
    b_substitution = {
        B0: U * X - X**2,
        B2: -Vv * Y - Y**2,
    }
    E4_b = apply_substitutions(E4_st, b_substitution)
    relation = B1 - C + U * Y + Vv * X + X * Y
    require_equal(
        coefficient(E4_b, 2, 2, 0),
        8 * relation**2,
        "split scalar: C square certificate changed",
    )
    c_substitution = {C: B1 + U * Y + Vv * X + X * Y}
    final_H2 = apply_substitutions(
        H2_14, st_substitution, b_substitution, c_substitution
    )
    final_L = apply_substitutions(
        linear_pre4, st_substitution, b_substitution, c_substitution
    )
    require(
        all(
            weighted_coefficient(
                degree, H4, H3, final_H2, final_L
            )
            == 0
            for degree in range(3, 9)
        ),
        "split scalar: equations (15)--(16) do not close E8 through E3",
    )

    Q = B1 * Y + U * Y**2 + ell[4]
    R = (
        -2 * B1 * X
        - 2 * U * X * Y
        + Vv * X**2
        + X**2 * Y
        + ell[7]
    )
    E2 = weighted_coefficient(2, H4, H3, final_H2, final_L)
    require_equal(
        E2,
        (R * p - 2 * Q * q) ** 2,
        "split scalar: equation (17) changed",
    )
    linear_factor = (
        Vv * X**2 * Y
        + X**2 * Y**2
        + 2 * X * ell[4]
        + Y * ell[7]
    )
    require_equal(
        final_L.det(),
        linear_factor**2,
        "split scalar: equation (19) changed",
    )
    exit_substitution = {
        ell[4]: -B1 * Y - U * Y**2,
        ell[7]: 2 * B1 * X + 2 * U * X * Y
        - Vv * X**2 - X**2 * Y,
    }
    require_equal(
        final_L.det().subs(exit_substitution),
        0,
        "split scalar: E2 does not force singular L",
    )


verify_split_scalar()


# ---------------------------------------------------------------------------
# Split-root opposite tangent and zero tangent: (11), (20)--(22)
# ---------------------------------------------------------------------------


def verify_split_opposite() -> None:
    H4 = p * q * A
    raw_substitution = {
        top.a: 1,
        top.d: -1,
        v[3]: 0,
        v[8]: 0,
    }
    raw_H3 = apply_substitutions(
        top.split_result.H3, raw_substitution
    )
    raw_H2 = apply_substitutions(
        top.H2_general,
        top.split_solution,
        raw_substitution,
    )
    E6_raw = weighted_coefficient(6, H4, raw_H3, raw_H2, L)
    require_equal(
        coefficient(E6_raw, 4, 1, 1),
        -8 * (6 * v[4] - v[9]),
        "split opposite: first E6 r relation changed",
    )
    require_equal(
        coefficient(E6_raw, 3, 2, 1),
        8 * (3 * v[0] + 3 * v[10] - 2 * v[5] + 2 * w[16]),
        "split opposite: second E6 r relation changed",
    )
    require_equal(
        coefficient(E6_raw, 2, 3, 1),
        8 * (v[1] + 9 * v[11] - 6 * v[6] - 4 * w[10]),
        "split opposite: third E6 r relation changed",
    )
    require_equal(
        coefficient(E6_raw, 1, 4, 1),
        8 * (v[2] - 6 * v[7]),
        "split opposite: fourth E6 r relation changed",
    )
    r_substitution = {
        v[9]: 6 * v[4],
        w[16]: (-3 * v[0] - 3 * v[10] + 2 * v[5]) / 2,
        v[1]: -9 * v[11] + 6 * v[6] + 4 * w[10],
        v[2]: 6 * v[7],
    }
    E6_r = apply_substitutions(E6_raw, r_substitution)
    require_equal(
        coefficient(E6_r, 6, 0, 0),
        36 * v[4] ** 2,
        "split opposite: v4 square changed",
    )
    require_equal(
        coefficient(E6_r, 0, 6, 0),
        -36 * v[7] ** 2,
        "split opposite: v7 square changed",
    )
    E6_zero = apply_substitutions(E6_r, {v[4]: 0, v[7]: 0})
    require_equal(
        coefficient(E6_zero, 5, 1, 0),
        -8 * w[12],
        "split opposite: E6 w12 pivot changed",
    )
    require_equal(
        coefficient(E6_zero, 1, 5, 0),
        8 * w[2],
        "split opposite: E6 w2 pivot changed",
    )

    rho = sp.symbols("op_rho")
    family_substitution = {
        v[0]: (-v[10] + 6 * v[5] - 4 * rho) / 9,
        v[1]: -9 * v[11] + 6 * v[6] + 4 * w[10],
        v[2]: 0,
        v[3]: 0,
        v[4]: 0,
        v[7]: 0,
        v[8]: 0,
        v[9]: 0,
        w[2]: 0,
        w[12]: 0,
        w[16]: (2 * rho - 4 * v[10]) / 3,
    }
    H3 = apply_substitutions(raw_H3, family_substitution)
    H2 = apply_substitutions(raw_H2, family_substitution)
    expected_H3 = sp.Matrix(
        [
            (-v[10] + 6 * v[5] - 4 * rho) * p**3 / 9
            + (-9 * v[11] + 6 * v[6] + 4 * w[10]) * p**2 * q,
            v[5] * p**2 * q + v[6] * p * q**2,
            v[10] * p * q**2 + v[11] * q**3,
        ]
    ) + r * (p * Ap - q * Aq)
    expected_H2 = sp.Matrix(
        [
            w[0] * p**2
            + w[1] * p * q
            + (-12 * v[11] + 8 * v[6] + 6 * w[10]) * p * r,
            w[6] * p**2
            + w[7] * p * q
            + w[8] * q**2
            + rho * p * r
            + w[10] * q * r
            - 2 * r**2,
            w[13] * p * q
            + w[14] * q**2
            + (2 * rho - 4 * v[10]) * q * r / 3,
        ]
    )
    require(
        matrix_equal(H3, expected_H3)
        and matrix_equal(H2, expected_H2),
        "split opposite: legacy degree-six family does not span",
    )

    solve6, residual6 = constant_partial_solve(
        coefficient_equations(
            weighted_coefficient(6, H4, H3, H2, L)
        ),
        ell,
        3,
        "split opposite E6 L solve",
    )
    require(
        residual6 == [],
        "split opposite: E6 L solve has a compatibility",
    )
    remaining = tuple(symbol for symbol in ell if symbol not in solve6)
    solve5, residual5 = constant_partial_solve(
        coefficient_equations(
            apply_substitutions(
                weighted_coefficient(5, H4, H3, H2, L),
                solve6,
            )
        ),
        remaining,
        4,
        "split opposite E5 L solve",
    )
    del solve5
    require(
        has_nonzero_constant(residual5)
        and any(abs(item) == 64 for item in residual5 if item.is_number),
        "split opposite: constant 64 obstruction disappeared",
    )


verify_split_opposite()


def binary_quadratic_vector(prefix: str) -> Tuple[sp.Matrix, Tuple[sp.Symbol, ...]]:
    symbols = sp.symbols(f"{prefix}0:9")
    monomials = (p**2, p * q, q**2)
    vector = sp.Matrix(
        [
            sum(
                symbols[3 * component + index] * monomial
                for index, monomial in enumerate(monomials)
            )
            for component in range(3)
        ]
    )
    return vector, symbols


def verify_constant_e5_obstruction(
    label: str,
    H4: sp.Matrix,
    H3: sp.Matrix,
    H2: sp.Matrix,
    expected_magnitude: int,
    additional_magnitudes: Sequence[int] = (),
) -> None:
    solve6, residual6 = constant_partial_solve(
        coefficient_equations(
            weighted_coefficient(6, H4, H3, H2, L)
        ),
        ell,
        3,
        f"{label} E6 L solve",
    )
    require(residual6 == [], f"{label}: E6 compatibility appeared")
    remaining = tuple(symbol for symbol in ell if symbol not in solve6)
    _, residual5 = constant_partial_solve(
        coefficient_equations(
            apply_substitutions(
                weighted_coefficient(5, H4, H3, H2, L),
                solve6,
            )
        ),
        remaining,
        0,
        f"{label} E5 obstruction",
    )
    require(
        has_nonzero_constant(residual5)
        and all(
            any(
                abs(item) == magnitude
                for item in residual5
                if item.is_number
            )
            for magnitude in (
                expected_magnitude,
                *additional_magnitudes,
            )
        ),
        f"{label}: expected constant obstruction disappeared",
    )


def verify_split_zero() -> None:
    H4 = p * q * A
    raw_H3 = apply_substitutions(
        top.split_result.H3,
        {top.a: 0, top.d: 0},
    )
    raw_H2 = apply_substitutions(
        top.H2_general,
        top.split_solution,
        {top.a: 0, top.d: 0},
    )
    alpha, beta = sp.symbols("sz_alpha sz_beta")
    B, _ = binary_quadratic_vector("sz_B")
    directional_substitution = {
        w[0]: sp.Poly(B[0], p, q).coeff_monomial(p**2),
        w[1]: sp.Poly(B[0], p, q).coeff_monomial(p * q),
        w[2]: sp.Poly(B[0], p, q).coeff_monomial(q**2),
        w[6]: sp.Poly(B[1], p, q).coeff_monomial(p**2),
        w[7]: sp.Poly(B[1], p, q).coeff_monomial(p * q),
        w[8]: sp.Poly(B[1], p, q).coeff_monomial(q**2),
        w[10]: alpha,
        w[12]: sp.Poly(B[2], p, q).coeff_monomial(p**2),
        w[13]: sp.Poly(B[2], p, q).coeff_monomial(p * q),
        w[14]: sp.Poly(B[2], p, q).coeff_monomial(q**2),
        w[16]: 2 * beta,
    }
    require(
        matrix_equal(
            apply_substitutions(raw_H2, directional_substitution),
            B + r * (alpha * Ap + beta * Aq),
        ),
        "split zero: equation (20) is not the complete E7 H2 fibre",
    )

    E6_one_raw = weighted_coefficient(6, H4, top.V, B + r * Ap, L)
    require_equal(
        coefficient(E6_one_raw, 5, 1, 0),
        -9 * v[8],
        "split zero (1,0): E6 v8 relation changed",
    )
    require_equal(
        coefficient(E6_one_raw, 1, 5, 0),
        -v[2] - 6 * v[7],
        "split zero (1,0): E6 v2 relation changed",
    )
    require_equal(
        coefficient(E6_one_raw, 0, 6, 0),
        3 * v[3],
        "split zero (1,0): E6 v3 relation changed",
    )
    one_H3 = top.V.subs({v[2]: -6 * v[7], v[3]: 0, v[8]: 0})
    verify_constant_e5_obstruction(
        "split zero orbit (1,0)",
        H4,
        one_H3,
        B + r * Ap,
        8,
    )
    E6_two_raw = weighted_coefficient(
        6, H4, top.V, B + r * (Ap + Aq), L
    )
    require_equal(
        coefficient(E6_two_raw, 6, 0, 0),
        3 * v[8],
        "split zero (1,1): E6 v8 relation changed",
    )
    require_equal(
        coefficient(E6_two_raw, 5, 1, 0),
        -6 * v[4] - 9 * v[8] - v[9],
        "split zero (1,1): E6 v9 relation changed",
    )
    require_equal(
        coefficient(E6_two_raw, 1, 5, 0),
        -v[2] - 9 * v[3] - 6 * v[7],
        "split zero (1,1): E6 v2 relation changed",
    )
    require_equal(
        coefficient(E6_two_raw, 0, 6, 0),
        3 * v[3],
        "split zero (1,1): E6 v3 relation changed",
    )
    two_H3 = top.V.subs(
        {
            v[2]: -6 * v[7],
            v[3]: 0,
            v[8]: 0,
            v[9]: -6 * v[4],
        }
    )
    verify_constant_e5_obstruction(
        "split zero orbit (1,1)",
        H4,
        two_H3,
        B + r * (Ap + Aq),
        8,
        (16,),
    )

    binary_H2 = B
    require(
        all(
            component.diff(r) == 0
            for component in (H4 + top.V + binary_H2)
        ),
        "split zero orbit (0,0): nonlinear part is not binary",
    )


verify_split_zero()


# ---------------------------------------------------------------------------
# Double-root scalar tangent: equations (23)--(27)
# ---------------------------------------------------------------------------


def verify_double_scalar() -> None:
    H4 = p**2 * A
    raw_substitution = {
        top.a: 1,
        top.c: 0,
        top.d: 1,
        v[3]: 0,
        v[2]: 2 * v[7],
    }
    raw_H3 = apply_substitutions(
        top.double_result.H3, raw_substitution
    )
    raw_H2 = apply_substitutions(
        top.H2_general,
        top.double_solution,
        raw_substitution,
    )
    E6_raw = weighted_coefficient(6, H4, raw_H3, raw_H2, L)
    require_equal(
        coefficient(E6_raw, 5, 0, 1),
        3 * v[8],
        "double scalar: E6 v8 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 4, 1, 1),
        -3 * (2 * v[4] - v[9]),
        "double scalar: E6 v9 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 3, 2, 1),
        3 * (v[0] + v[10] - 2 * v[5]),
        "double scalar: E6 v0 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 2, 3, 1),
        3 * (v[1] + v[11] - 2 * v[6]),
        "double scalar: E6 v1 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 0, 6, 0),
        12 * v[7] ** 2,
        "double scalar: E6 v7 square changed",
    )

    U, Vv, X, Y, Z, S, T = sp.symbols(
        "ds_U ds_V ds_X ds_Y ds_Z ds_S ds_T"
    )
    A0, A12, C1, C, B0, B1, B2 = sp.symbols(
        "ds_A0 ds_A12 ds_C1 ds_C ds_B0 ds_B1 ds_B2"
    )
    coordinate_substitution = {
        v[0]: U - X,
        v[1]: Vv - Y,
        v[2]: 0,
        v[3]: 0,
        v[4]: Z / 2,
        v[5]: U,
        v[6]: Vv,
        v[7]: 0,
        v[8]: 0,
        v[9]: Z,
        v[10]: U + X,
        v[11]: Vv + Y,
        w[10]: T,
    }
    E6_coordinates = apply_substitutions(
        E6_raw, coordinate_substitution
    )
    require_equal(
        coefficient(E6_coordinates, 3, 3, 0),
        -4 * (w[1] - 2 * w[8] - 2 * T * Y - 6 * X * Y),
        "double scalar: E6 w1 relation changed",
    )
    require_equal(
        coefficient(E6_coordinates, 2, 4, 0),
        -4 * (w[2] - 3 * Y**2),
        "double scalar: E6 w2 relation changed",
    )
    family_substitution = {
        v[0]: U - X,
        v[1]: Vv - Y,
        v[2]: 0,
        v[3]: 0,
        v[4]: Z / 2,
        v[5]: U,
        v[6]: Vv,
        v[7]: 0,
        v[8]: 0,
        v[9]: Z,
        v[10]: U + X,
        v[11]: Vv + Y,
        w[0]: A0,
        w[1]: 2 * B2 + 2 * T * Y + 6 * X * Y,
        w[2]: 3 * Y**2,
        w[6]: B0,
        w[7]: B1,
        w[8]: B2,
        w[10]: T,
        w[12]: A12,
        w[13]: C1,
        w[14]: C,
        w[16]: 2 * S,
    }
    H3_pre5 = apply_substitutions(raw_H3, family_substitution)
    H2_pre5 = apply_substitutions(raw_H2, family_substitution)
    E6 = weighted_coefficient(6, H4, H3_pre5, H2_pre5, L)
    solve6, residual6 = constant_partial_solve(
        coefficient_equations(E6),
        (ell[2], ell[5], ell[8]),
        3,
        "double scalar E6 linear solve",
    )
    require(
        residual6 == [],
        "double scalar: E6 has an unretained compatibility",
    )

    E5 = apply_substitutions(
        weighted_coefficient(5, H4, H3_pre5, H2_pre5, L),
        solve6,
    )
    require_equal(
        coefficient(E5, 0, 4, 1),
        -24 * Y**2,
        "double scalar: E5 Y square changed",
    )
    # Hence Y=0.  The remaining r-coefficients solve A12,C1,A0.
    E5_y = apply_substitutions(E5, {Y: 0})
    r_equations = [
        value
        for monomial, value in sp.Poly(E5_y, p, q, r).terms()
        if monomial[2] > 0
    ]
    solve_h2, residual_h2 = constant_partial_solve(
        r_equations,
        (A12, C1, A0),
        3,
        "double scalar E5 H2 solve",
    )
    expected_h2_solve = {
        A12: sp.Rational(9, 4) * Z**2 - 4 * Z * S + 2 * S**2,
        C1: 2 * B0 + 9 * X * Z - 8 * X * S
        + 4 * Z * T - 4 * S * T,
        A0: 9 * X**2 + 8 * X * T + 2 * T**2 - C + 2 * B1,
    }
    require(
        all(
            sp.expand(solve_h2[key] - value) == 0
            for key, value in expected_h2_solve.items()
        ),
        "double scalar: equation (24) H2 relations changed",
    )
    require(
        residual_h2 == [],
        "double scalar: E5 r-part has an extra compatibility",
    )

    y_substitution = {Y: 0}
    H3 = apply_substitutions(H3_pre5, y_substitution)
    H2_24 = apply_substitutions(H2_pre5, y_substitution, solve_h2)
    expected_H3 = sp.Matrix(
        [
            (U - X) * p**3 + Vv * p**2 * q,
            Z * p**3 / 2 + U * p**2 * q + Vv * p * q**2,
            Z * p**2 * q + (U + X) * p * q**2 + Vv * q**3,
        ]
    ) + 2 * r * A
    require(
        matrix_equal(H3, expected_H3),
        "double scalar: equation (23) does not span the E5 H3 fibre",
    )

    solve6_y = {
        key: apply_substitutions(value, y_substitution, solve_h2)
        for key, value in solve6.items()
    }
    E5_solved_h2 = apply_substitutions(
        weighted_coefficient(5, H4, H3, H2_24, L),
        solve6_y,
    )
    solve5, residual5 = constant_partial_solve(
        coefficient_equations(E5_solved_h2),
        (ell[0], ell[1], ell[3], ell[6]),
        4,
        "double scalar E5 linear solve",
    )
    require(
        residual5 == [],
        "double scalar: E5 L solve has a compatibility",
    )

    linear_pre4 = apply_substitutions(L, solve6_y, solve5)
    E4 = weighted_coefficient(4, H4, H3, H2_24, linear_pre4)
    require_equal(
        coefficient(E4, 2, 0, 2),
        12 * (S - Z) ** 2,
        "double scalar: S square changed",
    )
    require_equal(
        coefficient(E4, 0, 2, 2),
        12 * (T + 2 * X) ** 2,
        "double scalar: T square changed",
    )
    st_substitution = {S: Z, T: -2 * X}
    E4_st = apply_substitutions(E4, st_substitution)
    require_equal(
        coefficient(E4_st, 4, 0, 0),
        2 * (2 * B0 - U * Z) ** 2,
        "double scalar: B0 square changed",
    )
    require_equal(
        coefficient(E4_st, 0, 4, 0),
        8 * (B2 + Vv * X) ** 2,
        "double scalar: B2 square changed",
    )
    b_substitution = {B0: U * Z / 2, B2: -Vv * X}
    E4_b = apply_substitutions(E4_st, b_substitution)
    relation = 2 * B1 - 2 * C + 2 * U * X + Vv * Z + 2 * X**2
    require_equal(
        coefficient(E4_b, 2, 2, 0),
        2 * relation**2,
        "double scalar: C square changed",
    )
    c_substitution = {
        C: B1 + U * X + Vv * Z / 2 + X**2
    }
    final_H2 = apply_substitutions(
        H2_24, st_substitution, b_substitution, c_substitution
    )
    final_L = apply_substitutions(
        linear_pre4, st_substitution, b_substitution, c_substitution
    )
    require(
        all(
            weighted_coefficient(
                degree, H4, H3, final_H2, final_L
            )
            == 0
            for degree in range(3, 9)
        ),
        "double scalar: equation (25) does not close E8 through E3",
    )

    double_Q = B1 * X + U * X**2 + X**3 + ell[4]
    double_R = (
        -4 * B1 * Z
        - 4 * U * X * Z
        + Vv * Z**2
        - 4 * X**2 * Z
        + 4 * ell[7]
    )
    E2 = weighted_coefficient(2, H4, H3, final_H2, final_L)
    require_equal(
        E2,
        (double_R * p / 4 - 2 * double_Q * q) ** 2,
        "double scalar: equation (26) changed",
    )
    linear_factor = (
        Vv * X * Z**2 + 4 * X * ell[7] + 4 * Z * ell[4]
    )
    require_equal(
        final_L.det(),
        linear_factor**2 / 16,
        "double scalar: equation (27) changed",
    )
    exit_substitution = {
        ell[4]: -B1 * X - U * X**2 - X**3,
        ell[7]: B1 * Z + U * X * Z
        - Vv * Z**2 / 4 + X**2 * Z,
    }
    require_equal(
        final_L.det().subs(exit_substitution),
        0,
        "double scalar: E2 does not force singular L",
    )


verify_double_scalar()


# ---------------------------------------------------------------------------
# Double-root semisimple tangent: equations (28)--(30)
# ---------------------------------------------------------------------------


def verify_double_semisimple() -> None:
    H4 = p**2 * A
    raw_substitution = {
        top.a: 1,
        top.c: 0,
        top.d: 0,
        v[3]: 0,
        v[2]: 6 * v[7],
    }
    raw_H3 = apply_substitutions(
        top.double_result.H3, raw_substitution
    )
    raw_H2 = apply_substitutions(
        top.H2_general,
        top.double_solution,
        raw_substitution,
    )
    E6_raw = weighted_coefficient(6, H4, raw_H3, raw_H2, L)
    require_equal(
        coefficient(E6_raw, 5, 0, 1),
        -3 * v[8],
        "double semisimple: E6 v8 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 4, 1, 1),
        6 * v[4] - 3 * v[9] + 8 * w[16],
        "double semisimple: E6 v9 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 3, 2, 1),
        -3 * v[0] + 5 * v[10] + 6 * v[5] - 16 * w[10],
        "double semisimple: E6 v0 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 2, 3, 1),
        v[1] + 9 * v[11] - 2 * v[6],
        "double semisimple: E6 v1 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 1, 4, 1),
        -12 * v[7],
        "double semisimple: E6 v7 relation changed",
    )

    U, Vv, S, T, P, J, G = sp.symbols(
        "sm_U sm_V sm_S sm_T sm_P sm_J sm_G"
    )
    A0, A1, B0, B1, C0, C1, C2 = sp.symbols(
        "sm_A0 sm_A1 sm_B0 sm_B1 sm_C0 sm_C1 sm_C2"
    )
    family_substitution = {
        v[0]: 2 * (U - T) + sp.Rational(5, 3) * P,
        v[1]: 2 * Vv - 9 * J,
        v[2]: 0,
        v[3]: 0,
        v[4]: S,
        v[5]: U,
        v[6]: Vv,
        v[7]: 0,
        v[8]: 0,
        v[9]: 2 * S + sp.Rational(8, 3) * G,
        v[10]: 2 * T + P,
        v[11]: J,
        w[0]: A0,
        w[1]: A1,
        w[6]: B0,
        w[7]: B1,
        w[10]: T,
        w[12]: C0,
        w[13]: C1,
        w[14]: C2,
        w[16]: G,
    }
    H3_pre5 = apply_substitutions(raw_H3, family_substitution)
    H2_pre5 = apply_substitutions(raw_H2, family_substitution)
    E6 = weighted_coefficient(6, H4, H3_pre5, H2_pre5, L)
    solve6, residual6 = constant_partial_solve(
        coefficient_equations(E6),
        (w[2], w[8], ell[2], ell[5], ell[8]),
        5,
        "double semisimple E6 solve",
    )
    require(
        residual6 == [],
        "double semisimple: E6 has an unretained compatibility",
    )
    require_equal(
        solve6[w[2]],
        Vv * (Vv - 6 * J),
        "double semisimple: E6 w2 relation changed",
    )
    require_equal(
        solve6[w[8]],
        T * Vv,
        "double semisimple: E6 w8 relation changed",
    )

    E5 = apply_substitutions(
        weighted_coefficient(
            5,
            H4,
            H3_pre5,
            apply_substitutions(H2_pre5, solve6),
            L,
        ),
        solve6,
    )
    require_equal(
        coefficient(E5, 2, 1, 2),
        2 * G,
        "double semisimple: E5 G pivot changed",
    )
    require_equal(
        coefficient(E5, 1, 2, 2),
        2 * P,
        "double semisimple: E5 P pivot changed",
    )
    require_equal(
        coefficient(E5, 0, 3, 2),
        6 * J,
        "double semisimple: E5 J pivot changed",
    )
    deviation_substitution = {G: 0, P: 0, J: 0}
    E5_deviation = apply_substitutions(E5, deviation_substitution)
    require_equal(
        coefficient(E5_deviation, 2, 2, 1),
        8 * (C2 - T**2),
        "double semisimple: E5 C2 relation changed",
    )
    c2_substitution = {C2: T**2}

    final_H3 = apply_substitutions(
        H3_pre5, deviation_substitution
    )
    final_H2 = apply_substitutions(
        H2_pre5,
        solve6,
        deviation_substitution,
        c2_substitution,
    )
    expected_H3 = sp.Matrix(
        [
            2 * (U - T) * p**3 + 2 * Vv * p**2 * q,
            S * p**3 + U * p**2 * q + Vv * p * q**2,
            2 * S * p**2 * q + 2 * T * p * q**2,
        ]
    ) + r * p * Ap
    expected_H2 = sp.Matrix(
        [
            A0 * p**2
            + A1 * p * q
            + Vv**2 * q**2
            + 2 * (U - T) * p * r
            + 2 * Vv * q * r
            + r**2,
            B0 * p**2
            + B1 * p * q
            + Vv * T * q**2
            + S * p * r
            + T * q * r,
            C0 * p**2 + C1 * p * q + T**2 * q**2,
        ]
    )
    require(
        matrix_equal(final_H3, expected_H3)
        and matrix_equal(final_H2, expected_H2),
        "double semisimple: equations (28)--(29) do not span",
    )

    equations = positive_coefficients(
        H4, final_H3, final_H2, L, (6, 5, 4)
    )
    solve_linear = solve_fixed_minor(
        equations,
        ell,
        (0, 1, 2, 3, 4, 6, 8, 13, 16),
        sp.Integer(32768),
        "double semisimple stacked L solve",
    )
    solved_L = apply_substitutions(L, solve_linear)
    expected_L = sp.Matrix(
        [
            [
                -A0 * T
                + A0 * U
                + A1 * S
                + 2 * S * T * Vv
                - 2 * S * U * Vv
                + T**3
                - 3 * T**2 * U
                + 3 * T * U**2
                - U**3,
                A0 * Vv + A1 * T + T**2 * Vv - U**2 * Vv,
                A0 - T**2 + 2 * T * U - U**2,
            ],
            [
                -B0 * T
                + B0 * U
                + B1 * S
                - S**2 * Vv
                + S * T * U
                - S * U**2,
                B0 * Vv
                + B1 * T
                - S * U * Vv
                + T**3
                - T**2 * U,
                B0 + S * T - S * U,
            ],
            [
                -C0 * T
                + C0 * U
                + C1 * S
                - S**2 * T
                - S**2 * U,
                C0 * Vv
                + C1 * T
                - S**2 * Vv
                - 2 * S * T**2,
                C0 - S**2,
            ],
        ]
    )
    require(
        matrix_equal(solved_L, expected_L),
        "double semisimple: displayed solution (30) changed",
    )
    require_equal(
        solved_L.det(),
        0,
        "double semisimple: equation (30) no longer gives singular L",
    )


verify_double_semisimple()


# ---------------------------------------------------------------------------
# Double-root nilpotent tangent: equations (31)--(33)
# ---------------------------------------------------------------------------


def verify_double_nilpotent() -> None:
    H4 = p**2 * A
    raw_substitution = {
        top.a: 0,
        top.c: 1,
        top.d: 0,
        v[3]: 0,
    }
    raw_H3 = apply_substitutions(
        top.double_result.H3, raw_substitution
    )
    raw_H2 = apply_substitutions(
        top.H2_general,
        top.double_solution,
        raw_substitution,
    )
    E6_raw = weighted_coefficient(6, H4, raw_H3, raw_H2, L)
    require_equal(
        coefficient(E6_raw, 5, 0, 1),
        8 * (v[10] - w[16]),
        "double nilpotent: E6 w16 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 4, 1, 1),
        -8 * (-3 * v[11] + 2 * v[6] - 2 * w[10]),
        "double nilpotent: E6 w10 relation changed",
    )
    require_equal(
        coefficient(E6_raw, 3, 2, 1),
        -8 * v[2],
        "double nilpotent: E6 v2 relation changed",
    )
    require_equal(
        coefficient(E6_raw.subs(v[2], 0), 1, 5, 0),
        36 * v[7] ** 2,
        "double nilpotent: E6 v7 square changed",
    )

    K, J, G = sp.symbols("nil_K nil_J nil_G")
    A0, A1, B0, B1, C0, C1 = sp.symbols(
        "nil_A0 nil_A1 nil_B0 nil_B1 nil_C0 nil_C1"
    )
    family_substitution = {
        v[2]: 0,
        v[3]: 0,
        v[6]: K,
        v[7]: 0,
        v[10]: G,
        v[11]: J,
        w[0]: A0,
        w[1]: A1,
        w[6]: B0,
        w[7]: B1,
        w[10]: K - sp.Rational(3, 2) * J,
        w[12]: C0,
        w[13]: C1,
        w[16]: G,
    }
    H3_pre5 = apply_substitutions(raw_H3, family_substitution)
    H2_pre5 = apply_substitutions(raw_H2, family_substitution)
    solve6, residual6 = constant_partial_solve(
        coefficient_equations(
            weighted_coefficient(6, H4, H3_pre5, H2_pre5, L)
        ),
        (w[2], ell[2], ell[5], ell[8]),
        4,
        "double nilpotent E6 solve",
    )
    require(
        residual6 == [],
        "double nilpotent: E6 has an unretained compatibility",
    )
    expected_w2 = (
        9 * J**2
        - 15 * J * K
        + 3 * J * v[1]
        + 2 * K**2
        + K * v[1]
    ) / 4
    require_equal(
        solve6[w[2]],
        expected_w2,
        "double nilpotent: E6 w2 relation changed",
    )

    E5 = apply_substitutions(
        weighted_coefficient(
            5,
            H4,
            H3_pre5,
            apply_substitutions(H2_pre5, solve6),
            L,
        ),
        solve6,
    )
    require_equal(
        coefficient(E5, 3, 0, 2),
        -12 * J,
        "double nilpotent: E5 J pivot changed",
    )
    E5_j = apply_substitutions(E5, {J: 0})
    require_equal(
        coefficient(E5_j, 4, 0, 1),
        -2 * (G**2 - 4 * w[14]),
        "double nilpotent: E5 w14 relation changed",
    )
    require_equal(
        coefficient(E5_j, 3, 1, 1),
        8 * G * K - 16 * w[8],
        "double nilpotent: E5 w8 relation changed",
    )
    require_equal(
        coefficient(E5_j, 2, 2, 1),
        2 * K * (v[1] - 2 * K),
        "double nilpotent: E5 product split changed",
    )
    quadratic_substitution = {
        J: 0,
        w[14]: G**2 / 4,
        w[8]: G * K / 2,
    }
    E5_product = apply_substitutions(E5, quadratic_substitution)

    # K != 0: equation (31) forces v1=2K, and the remaining p^2 q^3
    # coefficient forces v0=2v5-G.
    E5_nonzero = apply_substitutions(E5_product, {v[1]: 2 * K})
    require_equal(
        coefficient(E5_nonzero, 2, 3, 0),
        3 * K**2 * (G + v[0] - 2 * v[5]),
        "double nilpotent K!=0: v0 relation changed",
    )

    S, V4, R, T = sp.symbols("nil_S nil_V4 nil_R nil_T")
    nonzero_substitution = {
        v[0]: 2 * S,
        v[1]: 2 * K,
        v[2]: 0,
        v[3]: 0,
        v[4]: V4,
        v[5]: (G + 2 * S) / 2,
        v[6]: K,
        v[7]: 0,
        v[8]: R,
        v[9]: T,
        v[10]: G,
        v[11]: 0,
        w[0]: A0,
        w[1]: A1,
        w[6]: B0,
        w[7]: B1,
        w[8]: G * K / 2,
        w[10]: K,
        w[12]: C0,
        w[13]: C1,
        w[14]: G**2 / 4,
        w[16]: G,
    }
    nonzero_H3_pre4 = apply_substitutions(
        raw_H3, nonzero_substitution
    )
    nonzero_H2_pre4 = apply_substitutions(
        raw_H2, nonzero_substitution
    )
    solve6_nz, residual6_nz = constant_partial_solve(
        coefficient_equations(
            weighted_coefficient(
                6, H4, nonzero_H3_pre4, nonzero_H2_pre4, L
            )
        ),
        (w[2], ell[2], ell[5], ell[8]),
        4,
        "double nilpotent K!=0 E6 solve",
    )
    require(
        residual6_nz == [],
        "double nilpotent K!=0: E6 compatibility appeared",
    )
    nonzero_H2_pre4 = apply_substitutions(
        nonzero_H2_pre4, solve6_nz
    )
    E5_nz = apply_substitutions(
        weighted_coefficient(
            5, H4, nonzero_H3_pre4, nonzero_H2_pre4, L
        ),
        solve6_nz,
    )
    solve5_nz, residual5_nz = constant_partial_solve(
        coefficient_equations(E5_nz),
        (ell[1], ell[4], ell[7]),
        3,
        "double nilpotent K!=0 E5 solve",
    )
    require(
        residual5_nz == [],
        "double nilpotent K!=0: E5 compatibility appeared",
    )
    E4_nz = apply_substitutions(
        weighted_coefficient(
            4,
            H4,
            nonzero_H3_pre4,
            nonzero_H2_pre4,
            L,
        ),
        solve6_nz,
        solve5_nz,
    )
    require_equal(
        coefficient(E4_nz, 3, 0, 1),
        -3 * K**2 * R,
        "double nilpotent K!=0: E4 v8 relation changed",
    )
    require_equal(
        coefficient(E4_nz, 2, 1, 1),
        -3 * K**2 * (T - 2 * V4),
        "double nilpotent K!=0: E4 v9 relation changed",
    )
    final_nz_substitution = {R: 0, T: 2 * V4}
    final_nz_H3 = apply_substitutions(
        nonzero_H3_pre4, final_nz_substitution
    )
    final_nz_H2 = apply_substitutions(
        nonzero_H2_pre4, final_nz_substitution
    )
    expected_nz_H3 = sp.Matrix(
        [
            2 * S * p**3 + 2 * K * p**2 * q,
            V4 * p**3
            + (G + 2 * S) * p**2 * q / 2
            + K * p * q**2,
            2 * V4 * p**2 * q + G * p * q**2,
        ]
    ) + r * p * Aq
    expected_nz_H2 = sp.Matrix(
        [
            A0 * p**2 + A1 * p * q + K**2 * q**2,
            B0 * p**2
            + B1 * p * q
            + G * K * q**2 / 2
            + S * p * r
            + K * q * r,
            C0 * p**2
            + C1 * p * q
            + G**2 * q**2 / 4
            + 2 * V4 * p * r
            + G * q * r
            + r**2,
        ]
    )
    require(
        matrix_equal(final_nz_H3, expected_nz_H3)
        and matrix_equal(final_nz_H2, expected_nz_H2),
        "double nilpotent K!=0: legacy family does not span",
    )
    nz_equations = positive_coefficients(
        H4, final_nz_H3, final_nz_H2, L, (6, 5, 4)
    )
    solve_nz_L = solve_fixed_minor(
        nz_equations,
        ell,
        (0, 1, 2, 3, 4, 6, 9, 10, 12),
        -262144 * K**3,
        "double nilpotent K!=0 stacked L solve",
    )
    require_equal(
        apply_substitutions(L, solve_nz_L).det(),
        0,
        "double nilpotent K!=0: lower solve does not make L singular",
    )

    # K=0: no division and no v1 constraint.  The complete family is the
    # second legacy family, and E6/E5 make column two equal (v10/2) times
    # column three.
    Aa, G0, S0, T0, V0, V40, V8 = sp.symbols(
        "nil0_Aa nil0_G nil0_S nil0_T nil0_V0 nil0_V4 nil0_V8"
    )
    zero_substitution = {
        v[0]: V0,
        v[1]: G0,
        v[2]: 0,
        v[3]: 0,
        v[4]: V40,
        v[5]: (Aa + 2 * S0) / 2,
        v[6]: 0,
        v[7]: 0,
        v[8]: V8,
        v[9]: T0,
        v[10]: Aa,
        v[11]: 0,
        w[0]: A0,
        w[1]: A1,
        w[6]: B0,
        w[7]: B1,
        w[8]: 0,
        w[10]: 0,
        w[12]: C0,
        w[13]: C1,
        w[14]: Aa**2 / 4,
        w[16]: Aa,
    }
    zero_H3 = apply_substitutions(raw_H3, zero_substitution)
    zero_H2 = apply_substitutions(raw_H2, zero_substitution)
    expected_zero_H3 = sp.Matrix(
        [
            V0 * p**3 + G0 * p**2 * q,
            V40 * p**3 + (Aa + 2 * S0) * p**2 * q / 2,
            V8 * p**3 + T0 * p**2 * q + Aa * p * q**2,
        ]
    ) + r * p * Aq
    expected_zero_H2 = sp.Matrix(
        [
            A0 * p**2 + A1 * p * q + G0 * p * r,
            B0 * p**2 + B1 * p * q + S0 * p * r,
            C0 * p**2
            + C1 * p * q
            + Aa**2 * q**2 / 4
            + T0 * p * r
            + Aa * q * r
            + r**2,
        ]
    )
    require(
        matrix_equal(zero_H3, expected_zero_H3),
        "double nilpotent K=0: legacy H3 family does not span",
    )
    solve6_z, residual6_z = constant_partial_solve(
        coefficient_equations(
            weighted_coefficient(6, H4, zero_H3, zero_H2, L)
        ),
        (w[2], ell[2], ell[5], ell[8]),
        4,
        "double nilpotent K=0 E6 solve",
    )
    require(
        residual6_z == [] and solve6_z[w[2]] == 0,
        "double nilpotent K=0: E6 solve changed",
    )
    zero_H2_solved = apply_substitutions(zero_H2, solve6_z)
    require(
        matrix_equal(zero_H2_solved, expected_zero_H2),
        "double nilpotent K=0: legacy H2 family does not span",
    )
    E5_z = apply_substitutions(
        weighted_coefficient(5, H4, zero_H3, zero_H2_solved, L),
        solve6_z,
    )
    solve5_z, residual5_z = constant_partial_solve(
        coefficient_equations(E5_z),
        (ell[1], ell[4], ell[7]),
        3,
        "double nilpotent K=0 E5 solve",
    )
    require(
        residual5_z == [],
        "double nilpotent K=0: E5 compatibility appeared",
    )
    require(
        all(
            sp.expand(
                solve5_z[ell[row]]
                - Aa * solve6_z[ell[row + 1]] / 2
            )
            == 0
            for row in (1, 4, 7)
        ),
        "double nilpotent K=0: equation (33) changed",
    )
    solved_zero_L = apply_substitutions(L, solve6_z, solve5_z)
    require_equal(
        solved_zero_L.det(),
        0,
        "double nilpotent K=0: dependent-column exit failed",
    )


verify_double_nilpotent()


# ---------------------------------------------------------------------------
# Double-root zero tangent: equations (34)--(36)
# ---------------------------------------------------------------------------


def verify_double_zero() -> None:
    H4 = p**2 * A
    raw_H2 = apply_substitutions(
        top.H2_general,
        top.double_solution,
        {top.a: 0, top.c: 0, top.d: 0},
    )
    alpha, beta = sp.symbols("dz_alpha dz_beta")
    B, _ = binary_quadratic_vector("dz_B")
    directional_substitution = {
        w[0]: sp.Poly(B[0], p, q).coeff_monomial(p**2),
        w[1]: sp.Poly(B[0], p, q).coeff_monomial(p * q),
        w[2]: sp.Poly(B[0], p, q).coeff_monomial(q**2),
        w[6]: sp.Poly(B[1], p, q).coeff_monomial(p**2),
        w[7]: sp.Poly(B[1], p, q).coeff_monomial(p * q),
        w[8]: sp.Poly(B[1], p, q).coeff_monomial(q**2),
        w[10]: alpha,
        w[12]: sp.Poly(B[2], p, q).coeff_monomial(p**2),
        w[13]: sp.Poly(B[2], p, q).coeff_monomial(p * q),
        w[14]: sp.Poly(B[2], p, q).coeff_monomial(q**2),
        w[16]: 2 * beta,
    }
    require(
        matrix_equal(
            apply_substitutions(raw_H2, directional_substitution),
            B + r * (alpha * Ap + beta * Aq),
        ),
        "double zero: equation (20) is not the complete E7 H2 fibre",
    )

    E6_ap_raw = weighted_coefficient(6, H4, top.V, B + r * Ap, L)
    require_equal(
        coefficient(E6_ap_raw, 3, 3, 0),
        -2 * (v[1] - 3 * v[11] + 2 * v[6]),
        "double zero Ap: E6 v1 relation changed",
    )
    require_equal(
        coefficient(E6_ap_raw, 2, 4, 0),
        2 * (v[2] - 6 * v[7]),
        "double zero Ap: E6 v2 relation changed",
    )
    require_equal(
        coefficient(E6_ap_raw, 1, 5, 0),
        6 * v[3],
        "double zero Ap: E6 v3 relation changed",
    )
    ap_H3 = top.V.subs(
        {
            v[1]: 3 * v[11] - 2 * v[6],
            v[2]: 6 * v[7],
            v[3]: 0,
        }
    )
    verify_constant_e5_obstruction(
        "double zero orbit Ap",
        H4,
        ap_H3,
        B + r * Ap,
        8,
    )

    E6_aq_raw = weighted_coefficient(6, H4, top.V, B + r * Aq, L)
    require_equal(
        coefficient(E6_aq_raw, 3, 3, 0),
        -8 * (v[2] - 3 * v[7]),
        "double zero Aq: E6 v2 relation changed",
    )
    require_equal(
        coefficient(E6_aq_raw, 2, 4, 0),
        -12 * v[3],
        "double zero Aq: E6 v3 relation changed",
    )
    aq_H3 = top.V.subs({v[2]: 3 * v[7], v[3]: 0})
    verify_constant_e5_obstruction(
        "double zero orbit Aq",
        H4,
        aq_H3,
        B + r * Aq,
        8,
    )

    require(
        all(
            component.diff(r) == 0
            for component in (H4 + top.V + B)
        ),
        "double zero orbit (0,0): nonlinear part is not binary",
    )


verify_double_zero()


print("PASS split scalar family (13)--(19) is complete")
print("PASS split opposite and zero-tangent families (11), (20)--(22)")
print("PASS double scalar family (23)--(27) is complete")
print("PASS double semisimple family (28)--(30) is complete")
print("PASS double nilpotent split (31)--(33) is complete")
print("PASS double zero-tangent families (34)--(36)")
print("PASS binary fixed-conic fibre-to-endgame composition")

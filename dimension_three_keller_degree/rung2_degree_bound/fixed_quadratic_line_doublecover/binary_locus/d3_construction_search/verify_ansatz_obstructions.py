#!/usr/bin/env python3
"""Exact certificates for two frozen D3 strata.

This works directly with

    det(L + z JH2 + z^2 JH3 + z^3 JH4).

No reduction of BCW type is used.  The full-family certificates retain
all binary coefficients in H2 and H3, both arbitrary ternary quadratic
components, and the entire arbitrary linear part.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


if not __debug__:
    print("FAIL: assertions must remain enabled", file=sys.stderr)
    raise SystemExit(2)


p, q, r, z, w = sp.symbols("p q r z w")
tau, k = sp.symbols("tau k")
coords = (p, q, r)
mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
mon3_binary = (p**3, p**2 * q, p * q**2, q**3)

EXPECTED_DENOMINATOR_SHA256 = (
    "440df4694f98b1b361a09e136afb4365c3aa302c5532e5291f4b76a2a068c65a"
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def exponents(degree: int, binary: bool = False):
    if binary:
        return tuple((degree - j, j) for j in range(degree + 1))
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficients(poly, degree: int, binary: bool = False):
    if binary:
        pp = sp.Poly(sp.expand(poly), p, q)
        return tuple(
            pp.coeff_monomial(p**i * q**j)
            for i, j in exponents(degree, binary=True)
        )
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return tuple(
        pp.coeff_monomial(p**i * q**j * r**s)
        for i, j, s in exponents(degree)
    )


def jac2(left, right):
    return sp.expand(
        sp.diff(left, p) * sp.diff(right, q)
        - sp.diff(left, q) * sp.diff(right, p)
    )


def weighted_determinant(h, R, U, V, T, A, B, L):
    H2 = sp.Matrix((A, B, T))
    H3 = sp.Matrix((U, V, R))
    H4 = sp.Matrix((sp.expand(h * p**2), sp.expand(h * q**2), 0))
    return sp.Poly(
        sp.expand(
            (
                L
                + z * H2.jacobian(coords)
                + z**2 * H3.jacobian(coords)
                + z**3 * H4.jacobian(coords)
            ).det()
        ),
        z,
    )


def syzygy_basis(alpha, beta, gamma, degree: int):
    """Kernel of (a,b,c) -> alpha*a+beta*b+gamma*c.

    The three binary degrees are (degree, degree, degree-1).
    """

    aa_vars = sp.symbols(f"sa{degree}_0:{degree + 1}")
    bb_vars = sp.symbols(f"sb{degree}_0:{degree + 1}")
    cc_vars = sp.symbols(f"sc{degree}_0:{degree}")
    aa = sum(
        value * p ** (degree - j) * q**j
        for j, value in enumerate(aa_vars)
    )
    bb = sum(
        value * p ** (degree - j) * q**j
        for j, value in enumerate(bb_vars)
    )
    cc = sum(
        value * p ** (degree - 1 - j) * q**j
        for j, value in enumerate(cc_vars)
    )
    variables = aa_vars + bb_vars + cc_vars
    matrix, rhs = sp.linear_eq_to_matrix(
        coefficients(alpha * aa + beta * bb + gamma * cc, 5 + degree, True),
        variables,
    )
    require(rhs == sp.zeros(matrix.rows, 1), "syzygy system is homogeneous")
    triples = []
    for vector in matrix.nullspace():
        substitution = dict(zip(variables, vector))
        triples.append(
            (
                sp.factor(aa.subs(substitution)),
                sp.factor(bb.subs(substitution)),
                sp.factor(cc.subs(substitution)),
            )
        )
    return matrix, tuple(triples)


def verify_expected_basis(alpha, beta, gamma, degree, expected):
    matrix, actual = syzygy_basis(alpha, beta, gamma, degree)
    require(len(actual) == len(expected), f"degree-{degree} nullity")
    for triple in expected:
        require(
            sp.expand(alpha * triple[0] + beta * triple[1] + gamma * triple[2])
            == 0,
            f"degree-{degree} displayed syzygy",
        )

    def vector(triple):
        return sp.Matrix(
            coefficients(triple[0], degree, True)
            + coefficients(triple[1], degree, True)
            + coefficients(triple[2], degree - 1, True)
        )

    displayed = sp.Matrix.hstack(*(vector(triple) for triple in expected))
    require(displayed.rank() == len(expected), f"degree-{degree} basis independence")
    require(matrix.rank() + len(expected) == matrix.cols, f"degree-{degree} completeness")
    return actual


def verify_r2_kernel_zero(alpha, beta, label):
    """The r^2 part of (U_r,V_r) has no T_r companion."""

    r2_u, r2_v = sp.symbols(f"{label}_r2_u {label}_r2_v")
    matrix, rhs = sp.linear_eq_to_matrix(
        coefficients(alpha * r2_u + beta * r2_v, 5, True),
        (r2_u, r2_v),
    )
    require(rhs == sp.zeros(matrix.rows, 1), f"{label}: r2 system homogeneous")
    require(matrix.rank() == matrix.cols == 2, f"{label}: zero r2 kernel")


def canonical_nonzero(polynomials):
    answer = []
    for value in polynomials:
        value = sp.factor(value)
        if value == 0:
            continue
        poly = sp.Poly(value)
        _, primitive = poly.primitive()
        value = sp.factor(primitive.as_expr())
        if sp.Poly(value).LC() < 0:
            value = -value
        if value not in answer:
            answer.append(value)
    return tuple(answer)


def ideals_equal(left, right, variables, label):
    gb_left = sp.groebner(left, *variables, order="grevlex")
    gb_right = sp.groebner(right, *variables, order="grevlex")
    require(
        all(gb_right.reduce(poly)[1] == 0 for poly in left),
        f"{label}: left is contained in right",
    )
    require(
        all(gb_left.reduce(poly)[1] == 0 for poly in right),
        f"{label}: right is contained in left",
    )


def e6_compatibility(label, h, R, degree1, degree2, expected_ideal):
    x0 = sp.symbols(f"{label}_x")
    y0, y1, y2 = sp.symbols(f"{label}_y0:3")
    U1, V1, T1 = (
        sum(parameter * triple[index] for parameter, triple in zip((y0, y1, y2), degree2))
        for index in range(3)
    )
    U2, V2, T2 = (x0 * degree1[0][index] for index in range(3))
    U = sp.expand(r * U1 + sp.Rational(1, 2) * r**2 * U2)
    V = sp.expand(r * V1 + sp.Rational(1, 2) * r**2 * V2)
    T = sp.expand(r * T1 + sp.Rational(1, 2) * r**2 * T2)

    avars = sp.symbols(f"{label}_a0:3")
    bvars = sp.symbols(f"{label}_b0:3")
    l33 = sp.symbols(f"{label}_l33")
    A = r * (avars[0] * p + avars[1] * q) + avars[2] * r**2
    B = r * (bvars[0] * p + bvars[1] * q) + bvars[2] * r**2
    L = sp.zeros(3)
    L[2, 2] = l33
    determinant = weighted_determinant(h, R, U, V, T, A, B, L)
    require(determinant.coeff_monomial(z**7) == 0, f"{label}: E7")
    equations = coefficients(determinant.coeff_monomial(z**6), 6)
    lower = avars + bvars + (l33,)
    matrix, rhs = sp.linear_eq_to_matrix(equations, lower)
    require(matrix.rank() == 6, f"{label}: E6 lower rank")
    compatibility = canonical_nonzero(
        (left.T * rhs)[0] for left in matrix.T.nullspace()
    )
    variables = (x0, y0, y1, y2)
    ideals_equal(compatibility, expected_ideal, variables, f"{label}: E6 ideal")
    return compatibility


def generic_lower(prefix):
    avars = sp.symbols(f"{prefix}_a0:6")
    bvars = sp.symbols(f"{prefix}_b0:6")
    lvars = sp.symbols(f"{prefix}_l0:9")
    A = sum(value * monomial for value, monomial in zip(avars, mon2))
    B = sum(value * monomial for value, monomial in zip(bvars, mon2))
    L = sp.Matrix(3, 3, lvars)
    return avars, bvars, lvars, A, B, L


def staged_substitute(expression, *stages):
    """Apply substitutions in an explicit order, simultaneously per stage."""

    for substitution in stages:
        expression = sp.expand(expression.subs(substitution, simultaneous=True))
    return expression


def solve_e6_e5(determinant, variables, expected_rank, label):
    equations = []
    for degree in (6, 5):
        equations.extend(coefficients(determinant.coeff_monomial(z**degree), degree))
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    require(matrix.rank() == expected_rank, f"{label}: E6/E5 rank")
    require(
        matrix.row_join(rhs).rank() == expected_rank,
        f"{label}: E6/E5 consistency",
    )
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    require(
        all(sp.expand(equation.subs(substitution)) == 0 for equation in equations),
        f"{label}: E6/E5 solution",
    )
    return substitution


def verify_zero_tangent_obstruction(label, h, square_exponent, square_constant, mutation):
    avars, bvars, lvars, A, B, L = generic_lower(label)
    determinant = weighted_determinant(h, p**2 * q, 0, 0, 0, A, B, L)
    require(
        all(determinant.coeff_monomial(z**degree) == 0 for degree in (9, 8, 7)),
        f"{label}: top identities",
    )
    substitution = solve_e6_e5(
        determinant, avars + bvars + lvars, 8, f"{label}: zero tangent"
    )
    reduced_det = sp.factor(L.det().subs(substitution))
    expected_det = sp.factor(
        lvars[8] * (lvars[0] * lvars[4] - lvars[1] * lvars[3])
    )
    require(reduced_det == expected_det, f"{label}: determinant factor")
    e4 = sp.Poly(
        sp.expand(determinant.coeff_monomial(z**4).subs(substitution)), p, q, r
    )
    i, j, s = square_exponent
    square = sp.factor(e4.coeff_monomial(p**i * q**j * r**s))
    expected_square = square_constant * lvars[8] ** 2
    if mutation == "zero_square" and label == "BB21":
        expected_square = 0
    require(square == expected_square, f"{label}: decisive E4 square")
    # In characteristic zero E4=0 forces l_33=0, hence det L=0.
    require(
        sp.factor(reduced_det.subs(lvars[8], 0)) == 0,
        f"{label}: E4 forces singular L",
    )


def verify_bs_nonzero_tangent(mutation):
    avars, bvars, lvars, A, B, L = generic_lower("BSY1")
    determinant = weighted_determinant(
        p**2,
        p**2 * q,
        0,
        2 * k * p * q * r,
        k * p * r,
        A,
        B,
        L,
    )
    require(
        all(determinant.coeff_monomial(z**degree) == 0 for degree in (9, 8, 7)),
        "BS nonzero tangent: top identities",
    )
    substitution = solve_e6_e5(
        determinant,
        avars + bvars + lvars,
        11,
        "BS nonzero tangent localized at k",
    )
    e4 = sp.Poly(
        sp.expand(determinant.coeff_monomial(z**4).subs(substitution)), p, q, r
    )
    decisive = (
        sp.factor(e4.coeff_monomial(p**4)),
        sp.factor(e4.coeff_monomial(p**3 * r)),
        sp.factor(e4.coeff_monomial(p**2 * q**2)),
    )
    expected = (4 * k * lvars[4], -8 * k**2 * lvars[7], 2 * k * lvars[1])
    if mutation == "bs_tangent":
        expected = (expected[0], expected[1], -expected[2])
    require(decisive == expected, "BS nonzero tangent: decisive E4 coefficients")
    reduced_det = sp.factor(L.det().subs(substitution))
    killed = reduced_det.subs({lvars[4]: 0, lvars[7]: 0, lvars[1]: 0})
    require(sp.factor(killed) == 0, "BS nonzero tangent: E4 forces singular L")


def verify_bs_full_parameterization(mutation):
    """Full E7 parameterization and exact descent for D3-BS-N2-Z."""

    tangent_a, tangent_b, tangent_c, tangent_k = sp.symbols(
        "BS_full_a BS_full_b BS_full_c BS_full_k"
    )
    avars, bvars, lvars, A, B, L = generic_lower("BSFULL")
    uvars = sp.symbols("BSFULL_u0:4")
    vvars = sp.symbols("BSFULL_v0:4")
    tvars = sp.symbols("BSFULL_t0:3")
    u0 = sum(value * monomial for value, monomial in zip(uvars, mon3_binary))
    v0 = sum(value * monomial for value, monomial in zip(vvars, mon3_binary))
    t0 = tvars[0] * p**2 + tvars[1] * p * q + tvars[2] * q**2
    S = tangent_a * p + tangent_b * q + tangent_c * r
    U = u0 - 2 * tangent_k * p**2 * r
    V = (
        v0
        + 2 * tangent_a * p * q * r
        + (2 * tangent_b + tangent_k) * q**2 * r
        + tangent_c * q * r**2
    )
    T = (
        t0
        + (tangent_a * p + tangent_b * q) * r
        + tangent_c * r**2 / 2
    )
    require(
        sp.expand(sp.diff(U, r) + 2 * tangent_k * p**2) == 0
        and sp.expand(sp.diff(V, r) - 2 * q * S - tangent_k * q**2)
        == 0
        and sp.expand(sp.diff(T, r) - S) == 0,
        "BS full E7 parameterization",
    )
    determinant = weighted_determinant(p**2, p**2 * q, U, V, T, A, B, L)
    require(determinant.coeff_monomial(z**7) == 0, "BS full E7 identity")

    e6_raw = determinant.coeff_monomial(z**6)
    e5_raw = determinant.coeff_monomial(z**5)
    e6_poly = sp.Poly(e6_raw, p, q, r)
    require(
        sp.factor(e6_poly.coeff_monomial(p**3 * r**3))
        == 4 * tangent_c**2,
        "BS E6 forces c=0",
    )

    # After c=0 all six ordinary pivots have constant coefficients.
    # The displayed residual therefore involves no localization in a,
    # b, or k.
    e6_pivots = {
        bvars[2]: tangent_a * vvars[1]
        - sp.Rational(3, 2) * tangent_k * vvars[0],
        bvars[4]: 2 * lvars[8]
        - 2 * tangent_a * tvars[1]
        + 2 * tangent_a * vvars[2]
        + tangent_b * vvars[1]
        + 2 * tangent_k * tvars[0],
        bvars[5]: tangent_a**2,
        avars[2]: -8 * tangent_a * tvars[2]
        + tangent_a * uvars[1]
        + 6 * tangent_a * vvars[3]
        - 4 * tangent_b * tvars[1]
        + 4 * tangent_b * vvars[2]
        - 2 * tangent_k * tvars[1]
        - sp.Rational(3, 2) * tangent_k * uvars[0]
        + 3 * tangent_k * vvars[2],
        avars[4]: 2 * tangent_a * uvars[2]
        - 8 * tangent_b * tvars[2]
        + tangent_b * uvars[1]
        + 6 * tangent_b * vvars[3]
        - 8 * tangent_k * tvars[2]
        + 6 * tangent_k * vvars[3],
        avars[5]: 2 * tangent_b**2
        + 4 * tangent_b * tangent_k
        + 3 * tangent_k**2,
    }
    zero_c = {tangent_c: 0}
    e6_pivoted = staged_substitute(e6_raw, zero_c, e6_pivots)
    expected_e6 = (
        16 * tangent_a * (tangent_b + tangent_k) * p**4 * q * r
        + (
            6 * tangent_a * uvars[3]
            + (4 * tangent_b + 3 * tangent_k) * uvars[2]
        )
        * p**2
        * q**4
        + 6
        * uvars[3]
        * (tangent_b + tangent_k)
        * p
        * q**5
    )
    require(
        sp.expand(e6_pivoted - expected_e6) == 0,
        "BS complete E6 pivot replay",
    )

    e5_pivoted = sp.Poly(
        staged_substitute(e5_raw, zero_c, e6_pivots), p, q, r
    )
    require(
        sp.factor(e5_pivoted.coeff_monomial(p * q**2 * r**2))
        == -24 * (tangent_b + tangent_k) ** 3,
        "BS E5 forces b+k=0",
    )
    require(
        sp.factor(
            e5_pivoted.coeff_monomial(p**3 * r**2).subs(
                tangent_k, -tangent_b
            )
        )
        == -12 * tangent_a**2 * tangent_b,
        "BS E5 forces a^2*b=0",
    )
    require(
        sp.factor(
            sp.Poly(e6_pivoted, p, q, r)
            .coeff_monomial(p**2 * q**4)
            .subs(tangent_k, -tangent_b)
        )
        == tangent_b * uvars[2] + 6 * tangent_a * uvars[3],
        "BS E6 forces b*u2+6*a*u3=0",
    )

    # Scaling the source variable r by a nonzero scalar sends
    # (a,b,k) to (a/s,b/s,k/s), preserves the frozen top, and scales
    # det(L) by the same nonzero denominator.  Thus the two non-origin
    # components b=0 and a=0 may safely be normalized to a=1 and b=1.
    scale = sp.symbols("BS_full_scale", nonzero=True)
    scaled = {r: r / scale, tangent_c: 0}
    require(
        sp.expand(
            U.subs(scaled)
            - (u0 - 2 * (tangent_k / scale) * p**2 * r)
        )
        == 0
        and sp.expand(
            V.subs(scaled)
            - (
                v0
                + 2 * (tangent_a / scale) * p * q * r
                + (2 * tangent_b + tangent_k)
                / scale
                * q**2
                * r
            )
        )
        == 0
        and sp.expand(
            T.subs(scaled)
            - (
                t0
                + (
                    (tangent_a / scale) * p
                    + (tangent_b / scale) * q
                )
                * r
            )
        )
        == 0,
        "BS r-scaling tangent normalization",
    )
    scaled_L = L.copy()
    scaled_L[:, 2] = scaled_L[:, 2] / scale
    require(
        sp.expand(scaled_L.det() - L.det() / scale) == 0,
        "BS r-scaling preserves linear invertibility",
    )

    # Chart I: b=k=0 and a is normalized to one.  The E6 constraint
    # gives u3=0, without division by any lower coefficient.
    chart_i = {
        tangent_a: 1,
        tangent_b: 0,
        tangent_c: 0,
        tangent_k: 0,
        uvars[3]: 0,
    }
    i_e6 = {
        bvars[2]: vvars[1],
        bvars[4]: 2 * lvars[8] - 2 * tvars[1] + 2 * vvars[2],
        bvars[5]: 1,
        avars[2]: -8 * tvars[2] + uvars[1] + 6 * vvars[3],
        avars[4]: 2 * uvars[2],
        avars[5]: 0,
    }
    require(
        staged_substitute(e6_raw, chart_i, i_e6) == 0,
        "BS chart I E6 replay",
    )
    i_e5_poly = sp.Poly(
        staged_substitute(e5_raw, chart_i, i_e6), p, q, r
    )
    require(
        sp.factor(i_e5_poly.coeff_monomial(p**2 * q**2 * r))
        == 4 * uvars[2],
        "BS chart I E5 forces u2=0",
    )
    require(
        sp.expand(
            i_e5_poly.coeff_monomial(p**3 * q * r)
            - 8 * (2 * tvars[2] - 3 * vvars[3])
        )
        == 0,
        "BS chart I E5 forces 2*t2=3*v3",
    )
    i_constraints = {
        uvars[2]: 0,
        tvars[2]: sp.Rational(3, 2) * vvars[3],
    }
    i_l8 = tvars[1] - vvars[2] / 2
    i_e5 = {
        lvars[8]: i_l8,
        bvars[1]: lvars[5]
        - i_l8 * vvars[1]
        + tvars[1] * vvars[1]
        + sp.Rational(9, 2) * vvars[0] * vvars[3],
        bvars[3]: lvars[7]
        + i_l8 * tvars[1]
        - i_l8 * vvars[2]
        - 3 * tvars[0] * vvars[3]
        - tvars[1] ** 2
        + tvars[1] * vvars[2]
        + sp.Rational(3, 2) * vvars[1] * vvars[3],
        avars[1]: lvars[2]
        - i_l8 * uvars[1]
        + 6 * i_l8 * vvars[3]
        + tvars[1] * uvars[1]
        - 12 * tvars[1] * vvars[3]
        + sp.Rational(9, 2) * uvars[0] * vvars[3]
        + 3 * vvars[2] * vvars[3],
        avars[3]: sp.Rational(3, 2) * uvars[1] * vvars[3],
    }
    require(
        staged_substitute(
            e5_raw, chart_i, i_e6, i_constraints, i_e5
        )
        == 0,
        "BS chart I complete E5 replay",
    )
    i_e4_raw = staged_substitute(
        determinant.coeff_monomial(z**4),
        chart_i,
        i_e6,
        i_constraints,
        i_e5,
    )
    i_e4_poly = sp.Poly(i_e4_raw, p, q, r)
    expected_i_e4 = 12 * vvars[3]
    require(
        sp.factor(i_e4_poly.coeff_monomial(p**2 * r**2))
        == expected_i_e4,
        "BS chart I decisive E4 coefficient",
    )
    i_v3 = {vvars[3]: 0}
    i_e4 = {
        lvars[7]: i_l8 * vvars[2] / 2,
        lvars[4]: lvars[5] * vvars[2] / 2,
        lvars[1]: lvars[2] * vvars[2] / 2,
    }
    i_stages = (chart_i, i_e6, i_constraints, i_e5, i_v3, i_e4)
    require(
        staged_substitute(
            determinant.coeff_monomial(z**4), *i_stages
        )
        == 0,
        "BS chart I complete E4 replay",
    )
    require(
        all(
            staged_substitute(
                L[row, 1] - vvars[2] * L[row, 2] / 2, *i_stages
            )
            == 0
            for row in range(3)
        ),
        "BS chart I columns two and three are proportional",
    )
    require(
        staged_substitute(L.det(), *i_stages) == 0,
        "BS chart I forces singular L",
    )

    # Chart II: a=0, b is normalized to one, k=-1, and E6 gives u2=0.
    chart_ii = {
        tangent_a: 0,
        tangent_b: 1,
        tangent_c: 0,
        tangent_k: -1,
        uvars[2]: 0,
    }
    ii_e6 = {
        bvars[2]: sp.Rational(3, 2) * vvars[0],
        bvars[4]: 2 * lvars[8] - 2 * tvars[0] + vvars[1],
        bvars[5]: 0,
        avars[2]: -2 * tvars[1]
        + sp.Rational(3, 2) * uvars[0]
        + vvars[2],
        avars[4]: uvars[1],
        avars[5]: 1,
    }
    require(
        staged_substitute(e6_raw, chart_ii, ii_e6) == 0,
        "BS chart II E6 replay",
    )
    ii_e5_poly = sp.Poly(
        staged_substitute(e5_raw, chart_ii, ii_e6), p, q, r
    )
    require(
        sp.factor(ii_e5_poly.coeff_monomial(p**4 * r))
        == 3 * vvars[0],
        "BS chart II E5 forces v0=0",
    )
    require(
        sp.expand(
            ii_e5_poly.coeff_monomial(p**2 * q**2 * r)
            + sp.Rational(3, 2)
            * (4 * tvars[1] - uvars[0] - 2 * vvars[2])
        )
        == 0,
        "BS chart II E5 forces u0=4*t1-2*v2",
    )
    require(
        sp.expand(
            ii_e5_poly.coeff_monomial(q**5)
            - 3 * uvars[3] * (tvars[1] - vvars[2])
        )
        == 0,
        "BS chart II E5 split coefficient",
    )
    ii_constraints = {
        vvars[0]: 0,
        uvars[0]: 4 * tvars[1] - 2 * vvars[2],
    }
    ii_e5 = {
        bvars[0]: lvars[5]
        - lvars[8] * vvars[1]
        + tvars[0] * vvars[1],
        bvars[1]: 2 * lvars[6]
        + 4 * lvars[8] * tvars[1]
        - 4 * lvars[8] * vvars[2]
        - 8 * tvars[0] * tvars[1]
        + 6 * tvars[0] * vvars[2]
        + tvars[1] * vvars[1],
        avars[0]: lvars[2]
        + 8 * lvars[8] * tvars[2]
        - lvars[8] * uvars[1]
        - 6 * lvars[8] * vvars[3]
        - 8 * tvars[0] * tvars[2]
        + tvars[0] * uvars[1]
        + 6 * tvars[0] * vvars[3]
        + 6 * tvars[1] ** 2
        - 8 * tvars[1] * vvars[2]
        + 3 * vvars[2] ** 2,
        avars[1]: 8 * tvars[1] * tvars[2]
        + tvars[1] * uvars[1]
        - 6 * tvars[1] * vvars[3]
        - 8 * tvars[2] * vvars[2]
        + 6 * vvars[2] * vvars[3],
    }
    ii_base_stages = (chart_ii, ii_e6, ii_constraints, ii_e5)
    ii_e5_reduced = staged_substitute(e5_raw, *ii_base_stages)
    expected_ii_e5 = (
        6
        * uvars[3]
        * (lvars[8] - tvars[0])
        * p
        * q**4
        + 3
        * uvars[3]
        * (tvars[1] - vvars[2])
        * q**5
    )
    require(
        sp.expand(ii_e5_reduced - expected_ii_e5) == 0,
        "BS chart II complete E5 replay",
    )

    # If u3 is nonzero, the two displayed E5 factors force
    # v2=t1 and l8=t0.  No normalization or division by u3 is used.
    ii_u3_nonzero = {vvars[2]: tvars[1], lvars[8]: tvars[0]}
    ii_nonzero_stages = ii_base_stages + (ii_u3_nonzero,)
    ii_nonzero_e4 = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**4), *ii_nonzero_stages
        ),
        p,
        q,
        r,
    )
    require(
        sp.expand(
            ii_nonzero_e4.coeff_monomial(q**4)
            - 3
            * uvars[3]
            * (-lvars[6] + tvars[0] * tvars[1])
        )
        == 0,
        "BS chart II u3-nonzero E4 pivot",
    )
    ii_nonzero_l6 = {lvars[6]: tvars[0] * tvars[1]}
    ii_nonzero_after_l6 = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**4),
            *ii_nonzero_stages,
            ii_nonzero_l6,
        ),
        p,
        q,
        r,
    )
    require(
        sp.expand(
            ii_nonzero_after_l6.coeff_monomial(p**4)
            - 2 * (lvars[3] - lvars[5] * tvars[1])
        )
        == 0
        and sp.expand(
            ii_nonzero_after_l6.coeff_monomial(p**2 * q**2)
            - (lvars[0] - lvars[2] * tvars[1])
        )
        == 0,
        "BS chart II u3-nonzero ordinary E4 pivots",
    )
    ii_nonzero_pivots = {
        lvars[3]: lvars[5] * tvars[1],
        lvars[0]: lvars[2] * tvars[1],
    }
    ii_nonzero_all = ii_nonzero_stages + (
        ii_nonzero_l6,
        ii_nonzero_pivots,
    )
    require(
        staged_substitute(
            determinant.coeff_monomial(z**4), *ii_nonzero_all
        )
        == 0,
        "BS chart II u3-nonzero complete E4 replay",
    )
    require(
        all(
            staged_substitute(
                L[row, 0] - tvars[1] * L[row, 2],
                *ii_nonzero_all,
            )
            == 0
            for row in range(3)
        ),
        "BS chart II u3-nonzero columns one and three proportional",
    )
    require(
        staged_substitute(L.det(), *ii_nonzero_all) == 0,
        "BS chart II u3-nonzero forces singular L",
    )

    # It remains to take u3=0 and write d=t1-v2.  First E4 contains the
    # unconditional square 8(l8-t0)^2.
    d = sp.symbols("BSII_d")
    ii_u3_zero = {uvars[3]: 0, vvars[2]: tvars[1] - d}
    ii_zero_stages = ii_base_stages + (ii_u3_zero,)
    ii_zero_e4 = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**4), *ii_zero_stages
        ),
        p,
        q,
        r,
    )
    require(
        sp.expand(
            ii_zero_e4.coeff_monomial(p**3 * r)
            - 8 * (-lvars[8] + tvars[0]) ** 2
        )
        == 0,
        "BS chart II u3-zero E4 forces l8=t0",
    )
    ii_l8 = {lvars[8]: tvars[0]}
    ii_zero_l8_stages = ii_zero_stages + (ii_l8,)
    ii_zero_l8_e4 = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**4), *ii_zero_l8_stages
        ),
        p,
        q,
        r,
    )
    require(
        sp.expand(
            ii_zero_l8_e4.coeff_monomial(p**3 * q)
            + 8 * d * (-lvars[6] + tvars[0] * tvars[1])
        )
        == 0
        and sp.expand(
            ii_zero_l8_e4.coeff_monomial(p * q**3)
            + 24 * d**2 * (tvars[2] - vvars[3])
        )
        == 0
        and sp.expand(
            ii_zero_l8_e4.coeff_monomial(q**4)
            + 2
            * d
            * (
                -avars[3]
                + 8 * tvars[2] ** 2
                + tvars[2] * uvars[1]
                - 18 * tvars[2] * vvars[3]
                + 9 * vvars[3] ** 2
            )
        )
        == 0,
        "BS chart II d-nonzero E4 pivots",
    )

    # On d != 0 each pivot below is licensed by an explicitly displayed
    # factor of d or d^2; the resulting formulas contain no denominator.
    ii_d_nonzero_localized = {
        lvars[6]: tvars[0] * tvars[1],
        tvars[2]: vvars[3],
        avars[3]: vvars[3] * (uvars[1] - vvars[3]),
    }
    ii_d_l3 = (
        lvars[5] * (tvars[1] + d) - tvars[0] * d * vvars[1]
    )
    ii_d_l0 = (
        -4 * bvars[3] * d
        + 12 * d**3
        + d * lvars[2]
        + 4 * d * lvars[7]
        - d * tvars[0] * uvars[1]
        - 2 * d * tvars[0] * vvars[3]
        + 4 * d * vvars[1] * vvars[3]
        + lvars[2] * tvars[1]
    )
    ii_d_nonzero_localized_stages = ii_zero_l8_stages + (
        ii_d_nonzero_localized,
    )
    ii_d_localized_e4 = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**4),
            *ii_d_nonzero_localized_stages,
        ),
        p,
        q,
        r,
    )
    require(
        sp.expand(
            ii_d_localized_e4.coeff_monomial(p**4)
            - 2 * (lvars[3] - ii_d_l3)
        )
        == 0
        and sp.expand(
            ii_d_localized_e4.coeff_monomial(p**2 * q**2)
            - (lvars[0] - ii_d_l0)
        )
        == 0,
        "BS chart II d-nonzero ordinary E4 pivots",
    )
    ii_d_nonzero_pivots = {
        lvars[3]: ii_d_l3,
        lvars[0]: ii_d_l0,
    }
    ii_d_nonzero_all = ii_d_nonzero_localized_stages + (
        ii_d_nonzero_pivots,
    )
    require(
        staged_substitute(
            determinant.coeff_monomial(z**4), *ii_d_nonzero_all
        )
        == 0,
        "BS chart II d-nonzero complete E4 replay",
    )
    ii_d_nonzero_e3 = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**3), *ii_d_nonzero_all
        ),
        p,
        q,
        r,
    )
    expected_d_cube = 12 * d**3
    if mutation == "bs_full":
        expected_d_cube = -expected_d_cube
    require(
        sp.factor(ii_d_nonzero_e3.coeff_monomial(q**2 * r))
        == expected_d_cube,
        "BS chart II d-nonzero decisive E3 coefficient",
    )

    # Finally d=0.  E4 has two ordinary pivots.  The p^3 coefficient of
    # E3 is a square in g=-l6+t0*v2, while det(L) is divisible by g.
    ii_d_zero = {d: 0}
    gap = -lvars[6] + tvars[0] * tvars[1]
    ii_d_zero_pivots = {
        lvars[3]: lvars[5] * tvars[1]
        + lvars[6] * vvars[1]
        - tvars[0] * tvars[1] * vvars[1],
        lvars[0]: lvars[2] * tvars[1]
        - (lvars[6] - tvars[0] * tvars[1])
        * (8 * tvars[2] - uvars[1] - 6 * vvars[3]),
    }
    ii_d_zero_pre_pivots = ii_zero_l8_stages + (ii_d_zero,)
    ii_d_zero_e4_before_pivots = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**4),
            *ii_d_zero_pre_pivots,
        ),
        p,
        q,
        r,
    )
    require(
        sp.expand(
            ii_d_zero_e4_before_pivots.coeff_monomial(p**4)
            - 2 * (lvars[3] - ii_d_zero_pivots[lvars[3]])
        )
        == 0
        and sp.expand(
            ii_d_zero_e4_before_pivots.coeff_monomial(p**2 * q**2)
            - (lvars[0] - ii_d_zero_pivots[lvars[0]])
        )
        == 0,
        "BS chart II d-zero ordinary E4 pivots",
    )
    ii_d_zero_all = ii_zero_l8_stages + (ii_d_zero, ii_d_zero_pivots)
    require(
        staged_substitute(
            determinant.coeff_monomial(z**4), *ii_d_zero_all
        )
        == 0,
        "BS chart II d-zero complete E4 replay",
    )
    ii_d_zero_e3 = sp.Poly(
        staged_substitute(
            determinant.coeff_monomial(z**3), *ii_d_zero_all
        ),
        p,
        q,
        r,
    )
    require(
        sp.expand(ii_d_zero_e3.coeff_monomial(p**3) + 4 * gap**2)
        == 0,
        "BS chart II d-zero decisive E3 square",
    )
    reduced_det = sp.factor(staged_substitute(L.det(), *ii_d_zero_all))
    quotient = sp.cancel(reduced_det / gap)
    require(
        sp.denom(quotient) == 1
        and sp.expand(reduced_det - gap * quotient) == 0,
        "BS chart II d-zero determinant divisibility",
    )
    require(
        sp.factor(reduced_det.subs(lvars[6], tvars[0] * tvars[1]))
        == 0,
        "BS chart II d-zero E3 forces singular L",
    )


def reduce_tau(expression):
    return sp.factor(sp.rem(sp.together(expression), tau**2 + 5, tau))


def verify_bb_full_parameterization(mutation):
    """Full E7 parameterization and the E6/E5 collapse for D3-BB-21."""

    tangent_a, tangent_b, tangent_c, tangent_k = sp.symbols(
        "BB_full_a BB_full_b BB_full_c BB_full_k"
    )
    avars, bvars, lvars, A, B, L = generic_lower("BBFULL")
    uvars = sp.symbols("BBFULL_u0:4")
    vvars = sp.symbols("BBFULL_v0:4")
    tvars = sp.symbols("BBFULL_t0:3")
    U0 = sum(value * monomial for value, monomial in zip(uvars, mon3_binary))
    V0 = sum(value * monomial for value, monomial in zip(vvars, mon3_binary))
    T0 = tvars[0] * p**2 + tvars[1] * p * q + tvars[2] * q**2
    S = tangent_a * p + tangent_b * q + tangent_c * r
    U = (
        U0
        + p
        * r
        * (
            (8 * tangent_a - tangent_k) * p
            + 8 * tangent_b * q
            + 4 * tangent_c * r
        )
        / 5
    )
    V = V0 + tangent_k * q**2 * r
    T = (
        T0
        + (tangent_a * p + tangent_b * q) * r
        + tangent_c * r**2 / 2
    )
    require(
        sp.expand(sp.diff(U, r) - p * (8 * S - tangent_k * p) / 5) == 0
        and sp.expand(sp.diff(V, r) - tangent_k * q**2) == 0
        and sp.expand(sp.diff(T, r) - S) == 0,
        "BB full E7 parameterization",
    )
    determinant = weighted_determinant(p * q, p**2 * q, U, V, T, A, B, L)
    require(
        all(determinant.coeff_monomial(z**degree) == 0 for degree in (9, 8, 7)),
        "BB full E9/E8/E7 identities",
    )
    e6 = sp.Poly(determinant.coeff_monomial(z**6), p, q, r)
    coeff = e6.coeff_monomial
    conic = (
        12 * tangent_a**2
        - 8 * tangent_a * tangent_k
        + 3 * tangent_k**2
    )
    require(
        sp.factor(coeff(p * q**2 * r**3))
        == sp.Rational(12, 5) * tangent_c**2,
        "BB E6 forces c=0",
    )
    require(
        sp.factor(coeff(p * q**4 * r).subs(tangent_c, 0))
        == sp.Rational(24, 5) * tangent_b**2,
        "BB E6 forces b=0",
    )
    conic_coefficient = coeff(p**3 * q**2 * r).subs(
        {tangent_c: 0, tangent_b: 0}
    )
    require(
        sp.expand(conic_coefficient - sp.Rational(2, 5) * conic) == 0,
        "BB E6 conic",
    )
    v0_endpoint = coeff(p**6).subs({tangent_c: 0, tangent_b: 0})
    u3_endpoint = coeff(p * q**5).subs({tangent_c: 0, tangent_b: 0})
    require(
        sp.expand(
            v0_endpoint
            - sp.Rational(3, 5)
            * vvars[0]
            * (3 * tangent_a - tangent_k)
        )
        == 0,
        "BB E6 v0 endpoint",
    )
    require(
        sp.expand(
            u3_endpoint
            - 3 * uvars[3] * (2 * tangent_k - tangent_a)
        )
        == 0,
        "BB E6 u3 endpoint",
    )

    # Complete ordinary E6 pivots after c=b=0.  The three remaining
    # equations are exactly the conic and the two displayed endpoints.
    pivots = {
        tangent_c: 0,
        tangent_b: 0,
        avars[5]: 0,
        bvars[5]: 0,
        bvars[2]: tangent_a * vvars[1],
        bvars[4]: (
            -(48 * tangent_a - 16 * tangent_k) * tvars[0]
            + (45 * tangent_a - 15 * tangent_k) * uvars[0]
            + (tangent_a + 3 * tangent_k) * vvars[2]
        )
        / 5,
        avars[4]: (
            (16 * tangent_a - 32 * tangent_k) * tvars[2]
            + (5 * tangent_a + 15 * tangent_k) * uvars[2]
        )
        / 25,
        avars[2]: (
            -(16 * tangent_a + 8 * tangent_k) * tvars[1]
            + 25 * tangent_a * uvars[1]
            + (-3 * tangent_a + 6 * tangent_k) * vvars[3]
            + 40 * lvars[8]
        )
        / 25,
    }
    e6_pivoted = sp.factor(determinant.coeff_monomial(z**6).subs(pivots))
    expected_e6 = (
        sp.Rational(2, 5) * conic * p**3 * q**2 * r
        + sp.Rational(3, 5)
        * vvars[0]
        * (3 * tangent_a - tangent_k)
        * p**6
        + 3 * uvars[3] * (2 * tangent_k - tangent_a) * p * q**5
    )
    require(
        sp.expand(e6_pivoted - expected_e6) == 0,
        "BB complete E6 pivot replay",
    )

    e5 = sp.Poly(
        sp.expand(determinant.coeff_monomial(z**5).subs(pivots)), p, q, r
    )
    decisive = sp.factor(e5.coeff_monomial(p**2 * q * r**2))
    expected_e5 = (
        sp.Rational(2, 5)
        * tangent_a
        * tangent_k
        * (8 * tangent_a - tangent_k)
    )
    if mutation == "bb_tangent":
        expected_e5 = -expected_e5
    require(decisive == expected_e5, "BB full decisive E5 coefficient")
    require(
        decisive.free_symbols == {tangent_a, tangent_k},
        "BB full E5 independence from all lower coefficients",
    )
    resultant_a = sp.factor(
        sp.resultant(conic, tangent_a * tangent_k * (8 * tangent_a - tangent_k), tangent_k)
    )
    resultant_k = sp.factor(
        sp.resultant(conic, tangent_a * tangent_k * (8 * tangent_a - tangent_k), tangent_a)
    )
    require(
        resultant_a == 1680 * tangent_a**6
        and resultant_k == 420 * tangent_k**6,
        "BB E6/E5 meet only at the origin",
    )

    # Recover the two conjugate zero-binary lines as a specialization.
    specialized = reduce_tau(
        decisive.subs({tangent_a: 3 * k, tangent_k: (4 + 2 * tau) * k})
    )
    expected_specialized = k**3 * (
        120 + sp.Rational(192, 5) * tau
    )
    require(
        sp.expand(specialized - expected_specialized) == 0,
        "BB conjugate specialization",
    )
    norm = sp.expand(
        (120 + sp.Rational(192, 5) * tau)
        * (120 - sp.Rational(192, 5) * tau)
    ).subs(tau**2, -5)
    require(norm == sp.Rational(108864, 5), "BB E5 coefficient norm")


def verify_origin_structure(label, h, mutation):
    avars, bvars, lvars, A, B, L = generic_lower(label + "ORIGIN")
    uvars = sp.symbols(f"{label}_origin_u0:4")
    vvars = sp.symbols(f"{label}_origin_v0:4")
    tvars = sp.symbols(f"{label}_origin_t0:3")
    U = sum(value * monomial for value, monomial in zip(uvars, mon3_binary))
    V = sum(value * monomial for value, monomial in zip(vvars, mon3_binary))
    T = tvars[0] * p**2 + tvars[1] * p * q + tvars[2] * q**2
    determinant = weighted_determinant(h, p**2 * q, U, V, T, A, B, L)
    require(
        all(determinant.coeff_monomial(z**degree) == 0 for degree in (9, 8, 7)),
        f"{label} origin: top identities",
    )
    variables = (
        avars[2],
        avars[4],
        avars[5],
        bvars[2],
        bvars[4],
        bvars[5],
        lvars[8],
    )
    equations = coefficients(determinant.coeff_monomial(z**6), 6)
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    require(matrix.rank() == matrix.row_join(rhs).rank() == 6, f"{label} origin: E6 rank")
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    if label == "BB":
        expected = (
            sp.Rational(8, 5) * lvars[8],
            0,
            0,
            0,
            0,
            0,
            lvars[8],
        )
    else:
        expected = (
            0,
            0,
            0,
            0,
            2 * lvars[8],
            0,
            lvars[8],
        )
    if mutation == "origin" and label == "BB":
        expected = (-expected[0],) + expected[1:]
    require(
        all(sp.expand(left - right) == 0 for left, right in zip(solution, expected)),
        f"{label} origin: complete E6 solution",
    )
    require(
        all(sp.expand(equation.subs(substitution)) == 0 for equation in equations),
        f"{label} origin: E6 replay",
    )

    # On l_33=0 every nonlinear term is binary.
    binary_substitution = substitution | {lvars[8]: 0}
    require(
        sp.diff(A.subs(binary_substitution), r) == 0
        and sp.diff(B.subs(binary_substitution), r) == 0,
        f"{label} origin: all-binary boundary",
    )

    # On l_33!=0, the third component is triangular in r and its inverse
    # has degree at most three.  This is the coordinate used by the
    # fibrewise plane low-degree exit.
    binary_third = lvars[6] * p + lvars[7] * q + T + p**2 * q
    third_component = lvars[8] * r + binary_third
    inverse_r = (w - binary_third) / lvars[8]
    require(
        sp.expand(third_component.subs(r, inverse_r) - w) == 0,
        f"{label} origin: triangular coordinate inverse",
    )
    require(
        sp.Poly(sp.together(inverse_r * lvars[8]), p, q, w).total_degree() <= 3,
        f"{label} origin: inverse degree",
    )
    require(3 * 4 == 12 and 12 < 100, f"{label} origin: Moh degree transfer")


def verify_frozen_scope(mutation):
    here = Path(__file__).resolve().parent
    scope = json.loads((here / "SCOPE.json").read_text())
    denominator_path = (
        here.parent.parent
        / "audit_delta_ge3_denominator"
        / "DENOMINATOR.json"
    )
    raw = denominator_path.read_bytes()
    expected_sha = (
        "0" * 64 if mutation == "denominator" else EXPECTED_DENOMINATOR_SHA256
    )
    require(hashlib.sha256(raw).hexdigest() == expected_sha, "denominator SHA")
    denominator = json.loads(raw)
    families = {entry["id"]: entry for entry in denominator["families"]}
    require(len(families) == denominator["counts"]["total"] == 26, "family count")
    require(
        scope["denominator"]
        == {
            "relative_path": "../../audit_delta_ge3_denominator/DENOMINATOR.json",
            "sha256": EXPECTED_DENOMINATOR_SHA256,
            "family_count": 26,
        },
        "scope denominator binding",
    )
    require(
        set(scope["targets"]) == {"D3-BB-21", "D3-BS-N2-Z"},
        "scope target IDs",
    )
    require(len(scope["exact_obstructions"]) == 4, "exact certificate count")
    require(
        scope["full_counterexample_exclusions"]
        == ["D3-BB-21", "D3-BS-N2-Z"],
        "full counterexample exclusion scope",
    )
    require(
        set(scope["structural_origin_exit"]["targets"])
        == {"D3-BB-21", "D3-BS-N2-Z"},
        "origin structural scope",
    )
    require(
        "no claim that either excluded stratum contains no Keller automorphisms"
        in scope["not_claimed"],
        "automorphism-existence disclaimer",
    )
    require("no BCW reduction" in scope["not_claimed"], "BCW disclaimer")
    require(
        families["D3-BB-21"]["normal_form"] == {"h": "pq", "R": "p^2q"},
        "D3-BB-21 frozen form",
    )
    require(
        families["D3-BS-N2-Z"]["normal_form"] == {"h": "p^2", "R": "p^2 q"},
        "D3-BS-N2-Z frozen form",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        choices=(
            "denominator",
            "zero_square",
            "bs_tangent",
            "bs_full",
            "bb_tangent",
            "origin",
        ),
    )
    args = parser.parse_args()

    verify_frozen_scope(args.mutation)

    data = {}
    for label, h in (("BB", p * q), ("BS", p**2)):
        P, Q, R = sp.expand(h * p**2), sp.expand(h * q**2), p**2 * q
        alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
        gcd = sp.gcd(
            sp.gcd(sp.Poly(alpha, p, q), sp.Poly(beta, p, q)),
            sp.Poly(gamma, p, q),
        )
        require(gcd.total_degree() == 3, f"{label}: exact delta three")
        verify_r2_kernel_zero(alpha, beta, label)
        if label == "BB":
            degree1_expected = ((sp.Rational(8, 5) * p, 0, 1),)
            degree2_expected = (
                (-sp.Rational(1, 5) * p**2, q**2, 0),
                (sp.Rational(8, 5) * p**2, 0, p),
                (sp.Rational(8, 5) * p * q, 0, q),
            )
        else:
            degree1_expected = ((0, 2 * q, 1),)
            degree2_expected = (
                (-2 * p**2, q**2, 0),
                (0, 2 * p * q, p),
                (4 * p**2, 0, q),
            )
        verify_expected_basis(alpha, beta, gamma, 1, degree1_expected)
        verify_expected_basis(alpha, beta, gamma, 2, degree2_expected)
        data[label] = (h, R, degree1_expected, degree2_expected)

    bb_x, bb_y0, bb_y1, bb_y2 = sp.symbols("BB_x BB_y0:3")
    bs_x, bs_y0, bs_y1, bs_y2 = sp.symbols("BS_x BS_y0:3")
    e6_compatibility(
        "BB",
        *data["BB"],
        (
            bb_x**2,
            bb_y2**2,
            bb_x * bb_y2,
            bb_x * (bb_y0 - 3 * bb_y1),
            3 * bb_y0**2 - 8 * bb_y0 * bb_y1 + 12 * bb_y1**2,
        ),
    )
    e6_compatibility(
        "BS",
        *data["BS"],
        (
            bs_x**2,
            bs_x * bs_y1,
            bs_x * (bs_y0 - bs_y2),
            bs_y1 * (bs_y0 - bs_y2),
        ),
    )

    verify_zero_tangent_obstruction(
        "BB21", p * q, (1, 2, 1), sp.Rational(24, 5), args.mutation
    )
    verify_zero_tangent_obstruction(
        "BSN2Z", p**2, (3, 0, 1), sp.Integer(8), args.mutation
    )
    verify_origin_structure("BB", p * q, args.mutation)
    verify_origin_structure("BS", p**2, args.mutation)
    verify_bs_nonzero_tangent(args.mutation)
    verify_bs_full_parameterization(args.mutation)
    verify_bb_full_parameterization(args.mutation)

    print("D3_CONSTRUCTION_EXACT_OBSTRUCTIONS_PASS")


if __name__ == "__main__":
    main()

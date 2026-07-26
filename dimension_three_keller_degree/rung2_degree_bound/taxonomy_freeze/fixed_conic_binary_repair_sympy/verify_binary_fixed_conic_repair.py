#!/usr/bin/python3
"""Fail-closed exact repair for the binary fixed-conic E7/E6 gap.

This checker starts from equation (4) of WORKING_FIXED_CONIC_ROW.md:

    H3 = V(p,q)
         + r ((a p+b q) A_p + (c p+d q) A_q)
         + r^2/2 (e A_p+f A_q),

with all 12 coefficients of V, all 18 coefficients of H2, and an
arbitrary 3-by-3 linear part.  It treats h=pq and h=p^2 separately.

The E7 coefficient matrix in the H2 variables has constant rational rank
seven.  All solves below use constant pivots.  The checker retains:

* the complete reduced E7 compatibility locus over C;
* an explicit 11-parameter affine H2 fibre on that locus;
* the universal E6 r^2 remainder and its exact coefficient ideal;
* polynomial sections proving that these are the full tangent-elimination
  ideals, not merely necessary conditions; and
* every rank jump that meets the E6 tangent locus.

Exit zero certifies only this binary E7/E6 repair and the tangent-orbit
reduction.  It does not certify the later branch endgames or the global
taxonomy row.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

import sympy as sp


p, q, r, book = sp.symbols("p q r book")
source_variables = (p, q, r)

A = sp.Matrix([p**2, p * q, q**2])
Ap = A.diff(p)
Aq = A.diff(q)

v = sp.symbols("v0:12")
w = sp.symbols("w0:18")
ell = sp.symbols("ell0:9")
a, b, c, d, e, f = sp.symbols("a b c d e f")

binary_cubic_monomials = (p**3, p**2 * q, p * q**2, q**3)
ternary_quadratic_monomials = (
    p**2,
    p * q,
    q**2,
    p * r,
    q * r,
    r**2,
)

V = sp.Matrix(
    [
        sum(
            v[4 * component + index] * monomial
            for index, monomial in enumerate(binary_cubic_monomials)
        )
        for component in range(3)
    ]
)
H2_general = sp.Matrix(
    [
        sum(
            w[6 * component + index] * monomial
            for index, monomial in enumerate(ternary_quadratic_monomials)
        )
        for component in range(3)
    ]
)
H3_full = (
    V
    + r * ((a * p + b * q) * Ap + (c * p + d * q) * Aq)
    + sp.Rational(1, 2) * r**2 * (e * Ap + f * Aq)
)
linear_part = sp.Matrix(3, 3, ell)


class VerificationFailure(RuntimeError):
    """Raised on a failed certificate, including under python -O."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationFailure(message)


def coefficients(
    expression: sp.Expr,
    variables: Sequence[sp.Symbol],
) -> List[sp.Expr]:
    expression = sp.expand(expression)
    if expression == 0:
        return []
    return [
        coefficient
        for _, coefficient in sp.Poly(expression, *variables).terms()
    ]


def nonzero(expressions: Iterable[sp.Expr]) -> List[sp.Expr]:
    return [
        sp.factor(expression)
        for expression in expressions
        if sp.factor(expression) != 0
    ]


def constant_multiple(expression: sp.Expr, target: sp.Expr) -> bool:
    quotient = sp.cancel(expression / target)
    return bool(quotient.is_number and quotient != 0)


def contains_constant_multiple(
    expressions: Iterable[sp.Expr],
    target: sp.Expr,
) -> bool:
    return any(
        constant_multiple(expression, target)
        for expression in expressions
    )


def ideal_contains_all(
    generators: Sequence[sp.Expr],
    expressions: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol],
) -> bool:
    basis = sp.groebner(
        [sp.expand(generator) for generator in generators],
        *variables,
        order="lex",
    )
    return all(
        sp.expand(basis.reduce(sp.expand(expression))[1]) == 0
        for expression in expressions
    )


def same_ideal(
    first: Sequence[sp.Expr],
    second: Sequence[sp.Expr],
    variables: Sequence[sp.Symbol],
) -> bool:
    first = [sp.expand(item) for item in first if sp.expand(item) != 0]
    second = [sp.expand(item) for item in second if sp.expand(item) != 0]
    return ideal_contains_all(
        first, second, variables
    ) and ideal_contains_all(
        second, first, variables
    )


def all_zero(vector_or_matrix: sp.Matrix) -> bool:
    return all(sp.expand(entry) == 0 for entry in vector_or_matrix)


def e7_expression(h: sp.Expr, H3: sp.Matrix, H2: sp.Matrix) -> sp.Expr:
    """Coefficient of weight seven in det(JH4,JH3,JH2,L)."""
    J4 = (h * A).jacobian(source_variables)
    J3 = H3.jacobian(source_variables)
    J2 = H2.jacobian(source_variables)
    return sp.expand(
        sp.trace(J4.adjugate() * J2)
        + sp.trace(J3.adjugate() * J4)
    )


def e6_expression(
    h: sp.Expr,
    H3: sp.Matrix,
    H2: sp.Matrix,
) -> sp.Expr:
    J4 = (h * A).jacobian(source_variables)
    J3 = H3.jacobian(source_variables)
    J2 = H2.jacobian(source_variables)

    # Weight six consists only of the column-degree patterns (3,3,0),
    # (3,2,1), and (2,2,2).  Expanding just those ten determinants is much
    # smaller than constructing irrelevant weights zero through nine.
    two_top_one_linear = sp.trace(J4.adjugate() * linear_part)
    all_distinct = sum(
        sp.Matrix.hstack(
            (J4, J3, J2)[assignment[0]][:, 0],
            (J4, J3, J2)[assignment[1]][:, 1],
            (J4, J3, J2)[assignment[2]][:, 2],
        ).det()
        for assignment in (
            (0, 1, 2),
            (0, 2, 1),
            (1, 0, 2),
            (1, 2, 0),
            (2, 0, 1),
            (2, 1, 0),
        )
    )
    return sp.expand(two_top_one_linear + all_distinct + J3.det())


def left_compatibilities(
    matrix: sp.Matrix,
    right_hand_side: sp.Matrix,
) -> List[sp.Expr]:
    return nonzero(
        (left.T * right_hand_side)[0]
        for left in matrix.T.nullspace()
    )


def constant_denominators(substitutions: Dict[sp.Symbol, sp.Expr]) -> bool:
    return all(
        sp.denom(sp.cancel(expression)).is_number
        for expression in substitutions.values()
    )


@dataclass
class E7Result:
    name: str
    h: sp.Expr
    H3: sp.Matrix
    forced_zero: Dict[sp.Symbol, int]
    compatibility: Tuple[sp.Expr, ...]
    compatibility_variables: Tuple[sp.Symbol, ...]
    solution: Dict[sp.Symbol, sp.Expr]
    free_h2: Tuple[sp.Symbol, ...]
    raw_equation_count: int
    raw_compatibility_count: int


split_solution = {
    w[3]: (
        5 * a * v[1]
        - 3 * a * v[11]
        - 2 * a * v[6]
        + d * v[1]
        + 9 * d * v[11]
        - 10 * d * v[6]
        + 8 * w[10]
    )
    / 4,
    w[4]: (
        a * v[2]
        + 6 * a * v[7]
        + 5 * d * v[2]
        - 18 * d * v[7]
    )
    / 4,
    w[5]: sp.Integer(0),
    w[9]: -(
        9 * a * v[0]
        + a * v[10]
        - 10 * a * v[5]
        - 3 * d * v[0]
        + 5 * d * v[10]
        - 2 * d * v[5]
        - 4 * w[16]
    )
    / 8,
    w[11]: -(a - d) ** 2 / 2,
    w[15]: -(
        18 * a * v[4]
        - 5 * a * v[9]
        - 6 * d * v[4]
        - d * v[9]
    )
    / 4,
    w[17]: sp.Integer(0),
}

double_solution = {
    w[3]: (
        3 * a * v[0]
        - a * v[10]
        - 2 * a * v[5]
        + 2 * c * v[1]
        + 6 * c * v[11]
        - 8 * c * v[6]
        + 4 * d * v[10]
        - 4 * d * v[5]
        + 4 * w[10]
    )
    / 2,
    w[4]: (
        a * v[1]
        - 3 * a * v[11]
        + 2 * a * v[6]
        + 4 * c * v[2]
        - 12 * c * v[7]
        + 2 * d * v[1]
        + 6 * d * v[11]
        - 8 * d * v[6]
    )
    / 2,
    w[5]: (a - d) ** 2,
    w[9]: (
        6 * a * v[4]
        - a * v[9]
        - 4 * c * v[10]
        + 4 * c * v[5]
        - 2 * d * v[9]
        + 2 * w[16]
    )
    / 4,
    w[11]: c * (a - d),
    w[15]: (3 * a * v[8] + 2 * c * v[9]) / 2,
    w[17]: c**2,
}

free_h2 = tuple(symbol for symbol in w if symbol not in split_solution)
require(
    free_h2
    == (
        w[0],
        w[1],
        w[2],
        w[6],
        w[7],
        w[8],
        w[10],
        w[12],
        w[13],
        w[14],
        w[16],
    ),
    "the intended eleven free H2 coefficients changed",
)
require(
    tuple(symbol for symbol in w if symbol not in double_solution)
    == free_h2,
    "the split and double-root H2 free sets no longer agree",
)

split_result = E7Result(
    name="h=pq",
    h=p * q,
    H3=V + r * (a * p * Ap + d * q * Aq),
    forced_zero={e: 0, f: 0, b: 0, c: 0},
    compatibility=(
        (3 * a - d) * v[8],
        (a - 3 * d) * v[3],
    ),
    compatibility_variables=(a, d, v[3], v[8]),
    solution=split_solution,
    free_h2=free_h2,
    raw_equation_count=22,
    raw_compatibility_count=15,
)

double_first_compatibility = (
    (a - 4 * d) * v[2]
    + 6 * (2 * d - a) * v[7]
    - 6 * c * v[3]
)
double_result = E7Result(
    name="h=p^2",
    h=p**2,
    H3=V + r * (a * p * Ap + (c * p + d * q) * Aq),
    forced_zero={e: 0, f: 0, b: 0},
    compatibility=(
        double_first_compatibility,
        (a - 2 * d) * v[3],
    ),
    compatibility_variables=(a, c, d, v[2], v[3], v[7]),
    solution=double_solution,
    free_h2=free_h2,
    raw_equation_count=20,
    raw_compatibility_count=13,
)


def verify_complete_e7(result: E7Result) -> None:
    raw = e7_expression(result.h, H3_full, H2_general)
    raw_equations = coefficients(raw, source_variables)
    matrix, rhs = sp.linear_eq_to_matrix(raw_equations, w)
    raw_compatibility = left_compatibilities(matrix, rhs)

    require(
        len(raw_equations) == result.raw_equation_count,
        f"{result.name}: raw E7 equation count changed",
    )
    require(
        matrix.rank() == 7,
        f"{result.name}: E7 H2 matrix does not have constant rank seven",
    )
    require(
        len(raw_compatibility) == result.raw_compatibility_count,
        f"{result.name}: raw E7 compatibility count changed",
    )

    # These square generators prove the forced zero parameters for actual
    # C-points.  No division or generic-rank premise is used.
    require(
        contains_constant_multiple(raw_compatibility, e**2),
        f"{result.name}: E7 no longer forces e=0",
    )
    require(
        contains_constant_multiple(raw_compatibility, f**2),
        f"{result.name}: E7 no longer forces f=0",
    )
    after_ef = nonzero(
        expression.subs({e: 0, f: 0})
        for expression in raw_compatibility
    )
    require(
        contains_constant_multiple(after_ef, b**2),
        f"{result.name}: E7 no longer forces b=0",
    )
    if result.name == "h=pq":
        require(
            contains_constant_multiple(after_ef, c**2),
            "h=pq: E7 no longer forces c=0",
        )

    final_compatibility = nonzero(
        expression.subs(result.forced_zero)
        for expression in raw_compatibility
    )
    require(
        same_ideal(
            final_compatibility,
            result.compatibility,
            result.compatibility_variables,
        ),
        f"{result.name}: reduced raw E7 compatibility ideal changed",
    )

    reduced = sp.expand(raw.subs(result.forced_zero))
    reduced_equations = coefficients(reduced, source_variables)
    reduced_matrix, _ = sp.linear_eq_to_matrix(reduced_equations, w)
    require(
        reduced_matrix.rank() == 7,
        f"{result.name}: reduced E7 rank changed",
    )
    require(
        reduced_matrix.rref()[1] == (3, 4, 5, 9, 11, 15, 17),
        f"{result.name}: the constant E7 pivot columns changed",
    )
    require(
        constant_denominators(result.solution),
        f"{result.name}: a parameter-dependent E7 denominator appeared",
    )

    solved = sp.expand(reduced.subs(result.solution))
    solved_coefficients = coefficients(solved, source_variables)
    require(
        same_ideal(
            solved_coefficients,
            result.compatibility,
            result.compatibility_variables,
        ),
        f"{result.name}: displayed H2 fibre is not complete",
    )

    # Every displayed pivot variable occurs with a constant nonzero pivot,
    # and rank seven leaves exactly the listed eleven free variables.
    require(
        len(result.solution) == 7 and len(result.free_h2) == 11,
        f"{result.name}: E7 affine-fibre dimension changed",
    )


verify_complete_e7(split_result)
verify_complete_e7(double_result)


def verify_e6_split() -> None:
    H2 = sp.expand(H2_general.subs(split_result.solution))
    E6 = e6_expression(split_result.h, split_result.H3, H2)
    require(
        sp.Poly(E6, r).degree() == 2,
        "h=pq: E6 acquired an unexpected r-degree",
    )
    remainder = sp.factor(
        sp.Poly(E6, r).coeff_monomial(r**2)
    )
    expected = 12 * p**2 * q**2 * (a - d) ** 2 * (a + d)
    require(
        sp.expand(remainder - expected) == 0,
        "h=pq: universal E6 remainder is not equation (7)",
    )
    require(
        not (set(v) | set(w) | set(ell)).intersection(
            remainder.free_symbols
        ),
        "h=pq: E6 r^2 remainder still depends on lower data",
    )

    raw_ideal = coefficients(remainder, (p, q))
    expected_ideal = [(a - d) ** 2 * (a + d)]
    require(
        same_ideal(raw_ideal, expected_ideal, (a, d)),
        "h=pq: raw universal E6 coefficient ideal changed",
    )
    require(
        sp.factor(sp.sqf_part(expected_ideal[0]))
        == (a - d) * (a + d),
        "h=pq: reduced E6 locus is not the two claimed lines",
    )

    # This polynomial section proves equality, not just containment, for
    # the tangent-elimination ideal: V=free H2=L=0 gives precisely the raw
    # ideal above and satisfies every other E7/E6 coefficient modulo it.
    section = {
        **{symbol: 0 for symbol in v},
        **{symbol: 0 for symbol in split_result.free_h2},
        **{symbol: 0 for symbol in ell},
    }
    require(
        sp.expand(E6.subs(section) - r**2 * expected) == 0,
        "h=pq: tangent-elimination section failed",
    )
    require(
        sp.expand(
            e7_expression(
                split_result.h,
                split_result.H3,
                H2,
            ).subs(section)
        )
        == 0,
        "h=pq: E7 section failed",
    )


def verify_e6_double() -> None:
    H2 = sp.expand(H2_general.subs(double_result.solution))
    E6 = e6_expression(double_result.h, double_result.H3, H2)
    require(
        sp.Poly(E6, r).degree() == 2,
        "h=p^2: E6 acquired an unexpected r-degree",
    )
    remainder = sp.factor(
        sp.Poly(E6, r).coeff_monomial(r**2)
    )
    expected = (
        24
        * d
        * p**2
        * (c * p + (d - a) * q) ** 2
    )
    require(
        sp.expand(remainder - expected) == 0,
        "h=p^2: universal E6 remainder is not equation (8)",
    )
    require(
        not (set(v) | set(w) | set(ell)).intersection(
            remainder.free_symbols
        ),
        "h=p^2: E6 r^2 remainder still depends on lower data",
    )

    raw_ideal = coefficients(remainder, (p, q))
    expected_ideal = [
        d * c**2,
        d * c * (d - a),
        d * (d - a) ** 2,
    ]
    require(
        same_ideal(raw_ideal, expected_ideal, (a, c, d)),
        "h=p^2: raw universal E6 coefficient ideal changed",
    )

    # The reduced ideal is
    # <d c, d(d-a)> = <d> intersection <c,d-a>.  The exact inclusions
    # I subset J and J^2 subset I certify equality of radicals.
    reduced_ideal = [d * c, d * (d - a)]
    require(
        ideal_contains_all(
            reduced_ideal,
            expected_ideal,
            (a, c, d),
        ),
        "h=p^2: raw E6 ideal is not contained in claimed radical",
    )
    require(
        ideal_contains_all(
            expected_ideal,
            [
                first * second
                for first in reduced_ideal
                for second in reduced_ideal
            ],
            (a, c, d),
        ),
        "h=p^2: square of claimed radical is not in raw E6 ideal",
    )

    section = {
        **{symbol: 0 for symbol in v},
        **{symbol: 0 for symbol in double_result.free_h2},
        **{symbol: 0 for symbol in ell},
    }
    require(
        sp.expand(E6.subs(section) - r**2 * expected) == 0,
        "h=p^2: tangent-elimination section failed",
    )
    require(
        sp.expand(
            e7_expression(
                double_result.h,
                double_result.H3,
                H2,
            ).subs(section)
        )
        == 0,
        "h=p^2: E7 section failed",
    )


verify_e6_split()
verify_e6_double()


def tangent_field(matrix: sp.Matrix) -> sp.Matrix:
    return (
        (matrix[0, 0] * p + matrix[0, 1] * q) * Ap
        + (matrix[1, 0] * p + matrix[1, 1] * q) * Aq
    )


def verify_orbits_and_rank_jumps() -> None:
    require(
        all_zero(p * Ap + q * Aq - 2 * A),
        "Euler identity for A changed",
    )

    # h=pq.  The reduced E6 equation has the scalar line d=a and the
    # opposite-weight line d=-a.  They meet only at the zero tangent.
    split_rank_matrix = sp.Matrix(
        [
            [3 * a - d, 0],
            [0, a - 3 * d],
        ]
    )
    require(
        sp.factor(split_rank_matrix.det())
        == (a - 3 * d) * (3 * a - d),
        "h=pq: E7 rank determinant changed",
    )
    require(
        split_rank_matrix.subs(d, a).rank(iszerofunc=lambda x: x == 0)
        == 2,
        "h=pq: scalar nonzero branch rank certificate changed",
    )
    require(
        split_rank_matrix.subs(d, -a).rank(iszerofunc=lambda x: x == 0)
        == 2,
        "h=pq: opposite nonzero branch rank certificate changed",
    )
    require(
        all_zero(split_rank_matrix.subs({a: 0, d: 0})),
        "h=pq: zero-tangent E7 rank jump disappeared",
    )
    require(
        all_zero(
            tangent_field(sp.eye(2)) - 2 * A
        ),
        "h=pq: scalar tangent representative changed",
    )
    require(
        all_zero(
            tangent_field(sp.diag(1, -1))
            - (p * Ap - q * Aq)
        ),
        "h=pq: opposite tangent representative changed",
    )

    # h=p^2.  On d=0, M=[[a,0],[c,0]].  For a != 0 the lower-triangular
    # stabilizer matrix g has det(g)=a and conjugates M to diag(a,0).
    M = sp.Matrix([[a, 0], [c, 0]])
    semisimple_g = sp.Matrix([[a, 0], [c, 1]])
    semisimple_normal = sp.diag(a, 0)
    require(
        all_zero(M * semisimple_g - semisimple_g * semisimple_normal),
        "h=p^2: semisimple orbit conjugacy certificate failed",
    )
    require(
        sp.expand(semisimple_g.det() - a) == 0,
        "h=p^2: semisimple chart determinant changed",
    )

    # At a=0,c!=0 the rank drops to the nilpotent orbit.  The following
    # stabilizer certificate has determinant c.
    nilpotent_M = M.subs(a, 0)
    nilpotent_g = sp.diag(1, c)
    nilpotent_normal = sp.Matrix([[0, 0], [1, 0]])
    require(
        all_zero(
            nilpotent_M * nilpotent_g
            - nilpotent_g * nilpotent_normal
        ),
        "h=p^2: nilpotent orbit conjugacy certificate failed",
    )
    require(
        sp.expand(nilpotent_g.det() - c) == 0,
        "h=p^2: nilpotent chart determinant changed",
    )

    # Retain the complete E7 compatibility-rank stratification.
    double_rank_matrix = sp.Matrix(
        [
            [a - 4 * d, -6 * c, 6 * (2 * d - a)],
            [0, a - 2 * d, 0],
        ]
    )
    x = a - 2 * d
    require(
        sp.factor(
            double_rank_matrix[:, [1, 2]].det()
        )
        == 6 * x**2,
        "h=p^2: generic E7 rank-two minor changed",
    )
    on_resonance = sp.simplify(
        double_rank_matrix.subs(a, 2 * d)
    )
    require(
        on_resonance
        == sp.Matrix([[-2 * d, -6 * c, 0], [0, 0, 0]]),
        "h=p^2: resonant E7 rank-one matrix changed",
    )
    require(
        all_zero(
            double_rank_matrix.subs({a: 0, c: 0, d: 0})
        ),
        "h=p^2: zero-tangent E7 rank-zero boundary changed",
    )

    # Ranks on the four E6 tangent orbits.  Nonzero hypotheses are retained
    # by the displayed nonzero minors a^2 or c; no generic division occurs.
    scalar_matrix = sp.simplify(
        double_rank_matrix.subs({c: 0, d: a})
    )
    require(
        sp.factor(scalar_matrix[:, [0, 1]].det()) == 3 * a**2,
        "h=p^2: scalar branch E7 rank-two certificate changed",
    )
    semisimple_matrix = sp.simplify(
        double_rank_matrix.subs(d, 0)
    )
    require(
        sp.factor(semisimple_matrix[:, [0, 1]].det()) == a**2,
        "h=p^2: semisimple branch E7 rank-two certificate changed",
    )
    nilpotent_matrix = sp.simplify(
        double_rank_matrix.subs({a: 0, d: 0})
    )
    require(
        nilpotent_matrix
        == sp.Matrix([[0, -6 * c, 0], [0, 0, 0]]),
        "h=p^2: nilpotent branch E7 rank-one certificate changed",
    )

    require(
        all_zero(
            tangent_field(sp.eye(2)) - 2 * A
        ),
        "h=p^2: scalar representative changed",
    )
    require(
        all_zero(
            tangent_field(sp.diag(1, 0)) - p * Ap
        ),
        "h=p^2: semisimple representative changed",
    )
    require(
        all_zero(
            tangent_field(nilpotent_normal) - p * Aq
        ),
        "h=p^2: nilpotent representative changed",
    )


verify_orbits_and_rank_jumps()

print("PASS full binary degree-eight normal retained (12 V, 18 H2, 9 L)")
print("PASS h=pq complete E7 locus and 11-parameter H2 fibre")
print("PASS h=p^2 complete E7 locus and 11-parameter H2 fibre")
print("PASS universal E6 tangent-elimination ideals and polynomial sections")
print("PASS equations (7), (8), and tangent list (9), including rank jumps")
print("SCOPE binary E7/E6 repair only; later endgames are not certified here")

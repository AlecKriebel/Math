#!/usr/bin/python3
"""Exact regressions for WORKING_FIXED_CONIC_ROW.md.

The script retains raw lower-Jacobian solves for every decisive branch.  It
does not replace the geometric orbit classification or the independent
mathematical audit.
"""

from __future__ import annotations

import sympy as sp

p, q, r, book = sp.symbols("p q r book")
source_variables = (p, q, r)
A = sp.Matrix([p**2, p * q, q**2])
Ap = A.diff(p)
Aq = A.diff(q)
Delta = Ap.cross(Aq)


def jacobian_map(H: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            [sp.diff(H[i], variable) for variable in source_variables]
            for i in range(3)
        ]
    )


def coefficient_equations(expression: sp.Expr) -> list[sp.Expr]:
    if sp.expand(expression) == 0:
        return []
    return [
        coefficient
        for _, coefficient in sp.Poly(
            sp.expand(expression), p, q, r
        ).terms()
    ]


def linear_step(
    determinant: sp.Expr,
    degree: int,
    unknowns: list[sp.Symbol],
) -> tuple[dict[sp.Symbol, sp.Expr], list[sp.Expr]]:
    coefficient = sp.Poly(sp.expand(determinant), book).coeff_monomial(
        book**degree
    )
    equations = coefficient_equations(coefficient)
    if not equations:
        return {}, []
    matrix, rhs = sp.linear_eq_to_matrix(equations, unknowns)
    compatibility = [
        sp.factor((vector.T * rhs)[0])
        for vector in matrix.T.nullspace()
        if sp.factor((vector.T * rhs)[0]) != 0
    ]
    reduced, pivots = matrix.row_join(rhs).rref()
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    for row, column in enumerate(pivots):
        if column < len(unknowns):
            substitutions[unknowns[column]] = sp.factor(
                reduced[row, -1]
                - sum(
                    reduced[row, j] * unknowns[j]
                    for j in range(column + 1, len(unknowns))
                )
            )
    return substitutions, compatibility


def weighted_determinant(
    H4: sp.Matrix,
    H3: sp.Matrix,
    H2: sp.Matrix,
    linear_part: sp.Matrix,
) -> sp.Expr:
    return sp.expand(
        (
            linear_part
            + book * jacobian_map(H2)
            + book**2 * jacobian_map(H3)
            + book**3 * jacobian_map(H4)
        ).det()
    )


def e5_has_constant_obstruction(
    H4: sp.Matrix, H3: sp.Matrix, H2: sp.Matrix
) -> list[sp.Expr]:
    linear_symbols = list(sp.symbols("ell0:9"))
    linear_part = sp.Matrix(3, 3, linear_symbols)
    determinant = weighted_determinant(H4, H3, H2, linear_part)
    assert (
        sp.Poly(determinant, book).coeff_monomial(book**7) == 0
    )
    degree_six_solution, degree_six_compatibility = linear_step(
        determinant, 6, linear_symbols
    )
    assert degree_six_compatibility == []
    determinant = sp.expand(determinant.subs(degree_six_solution))
    remaining = [
        symbol for symbol in linear_symbols
        if symbol not in degree_six_solution
    ]
    _, degree_five_compatibility = linear_step(
        determinant, 5, remaining
    )
    assert any(
        item.is_number and item != 0
        for item in degree_five_compatibility
    )
    return degree_five_compatibility


# The top normal and the two degree-six branch polynomials.
for h in (p * q, p**2):
    H4 = h * A
    expected_normal = 2 * h**2 * Delta
    assert all(
        sp.expand(value) == 0
        for value in (
            H4.diff(p).cross(H4.diff(q)) - expected_normal
        )
    )

a, c, d = sp.symbols("a c d")
split_H4 = p * q * A
split_W = a * p * Ap + d * q * Aq
split_Z = sp.Matrix([0, -(a - d) ** 2 / 2, 0])
split_weighted = weighted_determinant(
    split_H4, r * split_W, r**2 * split_Z, sp.zeros(3)
)
split_degree_six = sp.Poly(
    split_weighted, book
).coeff_monomial(book**6)
assert sp.expand(
    sp.Poly(split_degree_six, r).coeff_monomial(r**2)
    - 12 * p**2 * q**2 * (a - d) ** 2 * (a + d)
) == 0

double_H4 = p**2 * A
double_W = a * p * Ap + (c * p + d * q) * Aq
double_Z = sp.Matrix([(a - d) ** 2, c * (a - d), c**2])
double_weighted = weighted_determinant(
    double_H4, r * double_W, r**2 * double_Z, sp.zeros(3)
)
double_degree_six = sp.Poly(
    double_weighted, book
).coeff_monomial(book**6)
assert sp.expand(
    sp.Poly(double_degree_six, r).coeff_monomial(r**2)
    - 24 * d * p**2 * (c * p + (d - a) * q) ** 2
) == 0


# Shared general binary cubic and quadratic vectors.
v = sp.symbols("v0:12")
w = sp.symbols("w0:18")
binary_cubic_monomials = (p**3, p**2 * q, p * q**2, q**3)
quadratic_monomials = (p**2, p * q, q**2, p * r, q * r, r**2)
V_general = sp.Matrix(
    [
        sum(v[4 * i + j] * binary_cubic_monomials[j] for j in range(4))
        for i in range(3)
    ]
)
H2_general = sp.Matrix(
    [
        sum(w[6 * i + j] * quadratic_monomials[j] for j in range(6))
        for i in range(3)
    ]
)


# Split-root, opposite-weight tangent: degree five contains 64=0.
opposite_H3 = sp.Matrix(
    [
        (-v[10] + 6 * v[5] - 4 * w[9]) * p**3 / 9
        + (-9 * v[11] + 6 * v[6] + 4 * w[10]) * p**2 * q,
        v[5] * p**2 * q + v[6] * p * q**2,
        v[10] * p * q**2 + v[11] * q**3,
    ]
) + r * (p * Ap - q * Aq)
opposite_H2 = sp.Matrix(
    [
        w[0] * p**2
        + w[1] * p * q
        + (-12 * v[11] + 8 * v[6] + 6 * w[10]) * p * r,
        w[6] * p**2
        + w[7] * p * q
        + w[8] * q**2
        + w[9] * p * r
        + w[10] * q * r
        - 2 * r**2,
        w[13] * p * q
        + w[14] * q**2
        + (2 * w[9] - 4 * v[10]) * q * r / 3,
    ]
)
opposite_compatibility = e5_has_constant_obstruction(
    split_H4, opposite_H3, opposite_H2
)
assert any(sp.expand(item - 64) == 0 for item in opposite_compatibility)


# Split-root, tangent zero: the two nonzero support orbits both have a
# constant degree-five obstruction.
B_symbols = sp.symbols("b0:9")
binary_quadratic_monomials = (p**2, p * q, q**2)
B_general = sp.Matrix(
    [
        sum(
            B_symbols[3 * i + j] * binary_quadratic_monomials[j]
            for j in range(3)
        )
        for i in range(3)
    ]
)
one_direction_H3 = V_general.subs(
    {v[2]: -6 * v[7], v[3]: 0, v[8]: 0}
)
one_direction_compatibility = e5_has_constant_obstruction(
    split_H4, one_direction_H3, B_general + r * Ap
)
assert any(
    item.is_number and item != 0
    for item in one_direction_compatibility
)

two_direction_H3 = V_general.subs(
    {v[2]: -6 * v[7], v[3]: 0, v[8]: 0, v[9]: -6 * v[4]}
)
two_direction_compatibility = e5_has_constant_obstruction(
    split_H4, two_direction_H3, B_general + r * (Ap + Aq)
)
assert any(
    item.is_number and item != 0
    for item in two_direction_compatibility
)


# Split-root scalar tangent: compact endgame.
U, Vv, X, Y, B, C = sp.symbols("U V X Y B C")
ell4, ell7 = sp.symbols("ell4 ell7")
C_relation = B + U * Y + Vv * X + X * Y
split_scalar_H3 = sp.Matrix(
    [
        (U - X) * p**3 + (Vv - Y) * p**2 * q,
        U * p**2 * q + Vv * p * q**2,
        (U + X) * p * q**2 + (Vv + Y) * q**3,
    ]
) + 2 * r * A
split_scalar_H2 = sp.Matrix(
    [
        (2 * X * Y - C_relation + 2 * B) * p**2
        + (-2 * Vv * Y - Y**2) * p * q
        - 4 * Y * p * r,
        (U * X - X**2) * p**2
        + B * p * q
        + (-Vv * Y - Y**2) * q**2
        + 2 * X * p * r
        - 2 * Y * q * r,
        (2 * U * X - X**2) * p * q
        + C_relation * q**2
        + 4 * X * q * r,
    ]
)
split_scalar_L = sp.Matrix(
    [
        [
            -2 * B * Y
            + 2 * C_relation * Y
            - U * Y**2
            - X * Y**2
            + 2 * ell4,
            Y**2 * (Vv + Y),
            2 * Y**2,
        ],
        [
            (
                2 * B * X
                - 2 * C_relation * X
                + Vv * X**2
                + 3 * X**2 * Y
                + ell7
            )
            / 2,
            ell4,
            -2 * X * Y,
        ],
        [X**2 * (U - X), ell7, 2 * X**2],
    ]
)
split_scalar_det = weighted_determinant(
    split_H4, split_scalar_H3, split_scalar_H2, split_scalar_L
)
for degree in range(3, 9):
    assert (
        sp.Poly(split_scalar_det, book).coeff_monomial(book**degree)
        == 0
    )
Q = B * Y + U * Y**2 + ell4
R = -2 * B * X - 2 * U * X * Y + Vv * X**2 + X**2 * Y + ell7
assert sp.expand(
    sp.Poly(split_scalar_det, book).coeff_monomial(book**2)
    - (R * p - 2 * Q * q) ** 2
) == 0
split_scalar_linear_factor = (
    Vv * X**2 * Y + X**2 * Y**2 + 2 * X * ell4 + Y * ell7
)
assert sp.expand(
    split_scalar_L.det() - split_scalar_linear_factor**2
) == 0
split_scalar_exit = {
    ell4: -B * Y - U * Y**2,
    ell7: 2 * B * X + 2 * U * X * Y - Vv * X**2 - X**2 * Y,
}
assert sp.expand(split_scalar_L.det().subs(split_scalar_exit)) == 0


# Double-root scalar tangent: compact endgame.
Z = sp.symbols("Z")
double_scalar_B0 = U * Z / 2
double_scalar_C = B + U * X + Vv * Z / 2 + X**2
double_scalar_H3 = sp.Matrix(
    [
        (U - X) * p**3 + Vv * p**2 * q,
        Z * p**3 / 2 + U * p**2 * q + Vv * p * q**2,
        Z * p**2 * q + (U + X) * p * q**2 + Vv * q**3,
    ]
) + 2 * r * A
double_scalar_H2 = sp.Matrix(
    [
        (2 * B - double_scalar_C + X**2) * p**2
        - 2 * Vv * X * p * q
        - 4 * X * p * r,
        double_scalar_B0 * p**2
        + B * p * q
        - Vv * X * q**2
        + Z * p * r
        - 2 * X * q * r,
        Z**2 * p**2 / 4
        + (2 * double_scalar_B0 + X * Z) * p * q
        + double_scalar_C * q**2
        + 2 * Z * q * r,
    ]
)
double_scalar_L = sp.Matrix(
    [
        [
            -2 * B * X
            + 2 * double_scalar_C * X
            - U * X**2
            - X**3
            + 2 * ell4,
            Vv * X**2,
            2 * X**2,
        ],
        [
            (
                -8 * double_scalar_B0 * X
                + 4 * B * Z
                - 4 * double_scalar_C * Z
                + 4 * U * X * Z
                + Vv * Z**2
                + 4 * ell7
            )
            / 8,
            ell4,
            -X * Z,
        ],
        [
            Z * (4 * double_scalar_B0 - U * Z + X * Z) / 4,
            ell7,
            Z**2 / 2,
        ],
    ]
)
double_scalar_det = weighted_determinant(
    double_H4, double_scalar_H3, double_scalar_H2, double_scalar_L
)
for degree in range(3, 9):
    assert (
        sp.Poly(double_scalar_det, book).coeff_monomial(book**degree)
        == 0
    )
double_Q = B * X + U * X**2 + X**3 + ell4
double_R = (
    -4 * B * Z
    - 4 * U * X * Z
    + Vv * Z**2
    - 4 * X**2 * Z
    + 4 * ell7
)
assert sp.expand(
    sp.Poly(double_scalar_det, book).coeff_monomial(book**2)
    - (double_R * p / 4 - 2 * double_Q * q) ** 2
) == 0
double_scalar_linear_factor = (
    Vv * X * Z**2 + 4 * X * ell7 + 4 * Z * ell4
)
assert sp.expand(
    double_scalar_L.det() - double_scalar_linear_factor**2 / 16
) == 0
double_scalar_exit = {
    ell4: -B * X - U * X**2 - X**3,
    ell7: B * Z + U * X * Z - Vv * Z**2 / 4 + X**2 * Z,
}
assert sp.expand(double_scalar_L.det().subs(double_scalar_exit)) == 0


def solve_to_linear_singularity(
    H4: sp.Matrix,
    H3: sp.Matrix,
    H2: sp.Matrix,
    degrees: tuple[int, ...],
) -> sp.Matrix:
    linear_symbols = list(sp.symbols("m0:9"))
    linear_part = sp.Matrix(3, 3, linear_symbols)
    determinant = weighted_determinant(H4, H3, H2, linear_part)
    substitutions: dict[sp.Symbol, sp.Expr] = {}
    remaining = linear_symbols[:]
    for degree in degrees:
        current = sp.expand(determinant.subs(substitutions))
        solution, compatibility = linear_step(
            current, degree, remaining
        )
        assert compatibility == []
        substitutions.update(solution)
        remaining = [
            symbol for symbol in remaining if symbol not in solution
        ]
    result = linear_part.subs(substitutions)
    assert sp.expand(result.det()) == 0
    return result


# Double-root one-zero semisimple tangent.
S, T = sp.symbols("S T")
A0, A1, B0, B1, C0, C1 = sp.symbols("A0 A1 B0 B1 C0 C1")
Q0 = U - T
double_semisimple_H3 = sp.Matrix(
    [
        2 * Q0 * p**3 + 2 * Vv * p**2 * q,
        S * p**3 + U * p**2 * q + Vv * p * q**2,
        2 * S * p**2 * q + 2 * T * p * q**2,
    ]
) + r * p * Ap
double_semisimple_H2 = sp.Matrix(
    [
        A0 * p**2
        + A1 * p * q
        + Vv**2 * q**2
        + 2 * Q0 * p * r
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
solve_to_linear_singularity(
    double_H4,
    double_semisimple_H3,
    double_semisimple_H2,
    (6, 5, 4),
)


# Double-root nilpotent tangent, first subbranch.
K, Aa, V4 = sp.symbols("K Aa V4")
W0, W1 = sp.symbols("W0 W1")
double_nilpotent_nonzero_H3 = sp.Matrix(
    [
        2 * S * p**3 + 2 * K * p**2 * q,
        V4 * p**3 + (Aa + 2 * S) * p**2 * q / 2 + K * p * q**2,
        2 * V4 * p**2 * q + Aa * p * q**2,
    ]
) + r * p * Aq
double_nilpotent_nonzero_H2 = sp.Matrix(
    [
        W0 * p**2 + W1 * p * q + K**2 * q**2,
        B0 * p**2
        + B1 * p * q
        + Aa * K * q**2 / 2
        + S * p * r
        + K * q * r,
        C0 * p**2
        + C1 * p * q
        + Aa**2 * q**2 / 4
        + 2 * V4 * p * r
        + Aa * q * r
        + r**2,
    ]
)
solve_to_linear_singularity(
    double_H4,
    double_nilpotent_nonzero_H3,
    double_nilpotent_nonzero_H2,
    (6, 5, 4),
)

# Double-root nilpotent tangent, second subbranch.
V0, V8, G = sp.symbols("V0 V8 G")
double_nilpotent_zero_H3 = sp.Matrix(
    [
        V0 * p**3 + G * p**2 * q,
        V4 * p**3 + (Aa + 2 * S) * p**2 * q / 2,
        V8 * p**3 + T * p**2 * q + Aa * p * q**2,
    ]
) + r * p * Aq
double_nilpotent_zero_H2 = sp.Matrix(
    [
        W0 * p**2 + W1 * p * q + G * p * r,
        B0 * p**2 + B1 * p * q + S * p * r,
        C0 * p**2
        + C1 * p * q
        + Aa**2 * q**2 / 4
        + T * p * r
        + Aa * q * r
        + r**2,
    ]
)
solve_to_linear_singularity(
    double_H4,
    double_nilpotent_zero_H3,
    double_nilpotent_zero_H2,
    (6, 5),
)


# Double-root tangent zero: its two nonzero Borel orbits have constant
# degree-five obstructions.
double_normal_H3 = V_general.subs(
    {v[1]: 3 * v[11] - 2 * v[6], v[2]: 6 * v[7], v[3]: 0}
)
double_normal_compatibility = e5_has_constant_obstruction(
    double_H4, double_normal_H3, B_general + r * Ap
)
assert any(
    item.is_number and item != 0
    for item in double_normal_compatibility
)

double_tangent_H3 = V_general.subs({v[2]: 3 * v[7], v[3]: 0})
double_tangent_compatibility = e5_has_constant_obstruction(
    double_H4, double_tangent_H3, B_general + r * Aq
)
assert any(
    item.is_number and item != 0
    for item in double_tangent_compatibility
)

print("fixed-divisor conic-row SymPy checks passed")

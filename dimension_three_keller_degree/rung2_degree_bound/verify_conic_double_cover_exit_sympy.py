#!/usr/bin/python3
"""Exact checks for the conic double-cover quartic stratum.

The leading form is

    H4 = (x^4, x^2 y^2, y^4).

This script starts with a completely general cubic and quadratic part.  It
checks the full degree-eight kernel, the degree-seven solution and its two
compatibilities, and then independently follows every affine normal-form
branch through the first decisive lower homogeneous identity.
"""

from __future__ import annotations

import sympy as sp

if not __debug__:
    raise RuntimeError("verification requires Python assertions")


x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)


def jacobian(vector: sp.Matrix) -> sp.Matrix:
    return vector.jacobian(variables)


def weighted_determinant(
    linear: sp.Matrix,
    quadratic: sp.Matrix,
    cubic: sp.Matrix,
    quartic: sp.Matrix,
) -> sp.Expr:
    return sp.expand(
        (
            linear
            + scale * jacobian(quadratic)
            + scale**2 * jacobian(cubic)
            + scale**3 * jacobian(quartic)
        ).det()
    )


def homogeneous_coefficient(determinant: sp.Expr, degree: int) -> sp.Expr:
    return sp.expand(
        sp.Poly(determinant, scale).coeff_monomial(scale**degree)
    )


def coefficient_dictionary(polynomial: sp.Expr) -> dict[tuple[int, int, int], sp.Expr]:
    return {
        monomial: sp.expand(coefficient)
        for monomial, coefficient in sp.Poly(
            sp.expand(polynomial), x, y, z
        ).terms()
        if coefficient != 0
    }


def assert_zero(expression: sp.Expr) -> None:
    assert sp.expand(expression) == 0


H4 = sp.Matrix([x**4, x**2 * y**2, y**4])
JH4 = jacobian(H4)
normal = JH4[:, 0].cross(JH4[:, 1])
expected_normal = 8 * x * y * sp.Matrix(
    [y**4, -2 * x**2 * y**2, x**4]
)
assert JH4[:, 2] == sp.zeros(3, 1)
assert JH4.adjugate() == sp.Matrix([0, 0, 1]) * normal.T
assert normal == expected_normal


# ---------------------------------------------------------------------------
# E8: the full cubic kernel has dimension 14.
# ---------------------------------------------------------------------------

cubic_monomials = (
    x**3,
    x**2 * y,
    x * y**2,
    y**3,
    x**2 * z,
    x * y * z,
    y**2 * z,
    x * z**2,
    y * z**2,
    z**3,
)
raw_cubic_symbols = sp.symbols("raw_cubic0:30")
raw_H3 = sp.Matrix(
    [
        sum(
            raw_cubic_symbols[10 * component + index] * monomial
            for index, monomial in enumerate(cubic_monomials)
        )
        for component in range(3)
    ]
)
raw_E8 = sp.expand(normal.dot(raw_H3.diff(z)))
raw_E8_from_determinant = homogeneous_coefficient(
    weighted_determinant(
        sp.zeros(3), sp.zeros(3, 1), raw_H3, H4
    ),
    8,
)
assert_zero(raw_E8_from_determinant - raw_E8)
raw_E8_equations = list(coefficient_dictionary(raw_E8).values())
raw_E8_matrix, raw_E8_rhs = sp.linear_eq_to_matrix(
    raw_E8_equations, list(raw_cubic_symbols)
)
assert raw_E8_rhs == sp.zeros(raw_E8_matrix.rows, 1)
assert raw_E8_matrix.rank() == 16

c = sp.symbols("c0:12")
a, b = sp.symbols("a b")
binary_cubic_monomials = (x**3, x**2 * y, x * y**2, y**3)
C3 = sp.Matrix(
    [
        sum(c[4 * component + index] * monomial for index, monomial in enumerate(binary_cubic_monomials))
        for component in range(3)
    ]
)
T2 = sp.Matrix([2 * a * x**2, a * y**2 + b * x**2, 2 * b * y**2])
E8_H3 = C3 + z * T2
assert_zero(normal.dot(E8_H3.diff(z)))

candidate_parameters = list(c) + [a, b]
candidate_coefficients = []
for component in E8_H3:
    polynomial = sp.Poly(component, x, y, z)
    candidate_coefficients.extend(
        polynomial.coeff_monomial(monomial)
        for monomial in cubic_monomials
    )
candidate_matrix = sp.Matrix(
    [
        [sp.diff(entry, parameter) for parameter in candidate_parameters]
        for entry in candidate_coefficients
    ]
)
assert candidate_matrix.rank() == 14
assert raw_E8_matrix.cols - raw_E8_matrix.rank() == 14
assert raw_E8_matrix * candidate_matrix == sp.zeros(
    raw_E8_matrix.rows, candidate_matrix.cols
)


# ---------------------------------------------------------------------------
# E7: rank nine, two endpoint compatibilities, and the complete H2 solution.
# ---------------------------------------------------------------------------

quadratic_monomials = (x**2, x * y, y**2, x * z, y * z, z**2)
w = sp.symbols("w0:18")
raw_H2 = sp.Matrix(
    [
        sum(
            w[6 * component + index] * monomial
            for index, monomial in enumerate(quadratic_monomials)
        )
        for component in range(3)
    ]
)
zero_linear = sp.zeros(3)
E7_determinant = weighted_determinant(
    zero_linear, raw_H2, E8_H3, H4
)
raw_E7 = homogeneous_coefficient(E7_determinant, 7)
expected_E7_coefficients = {
    (7, 0, 0): -4 * b * c[9],
    (6, 1, 0): 4 * (-3 * a * c[8] - 2 * b * c[10] + 2 * w[15]),
    (5, 2, 0): 4
    * (-2 * a * c[9] - 3 * b * c[11] + 2 * b * c[5] + 2 * w[16]),
    (5, 1, 1): 16 * (-b**2 + w[17]),
    (4, 3, 0): -4
    * (a * c[10] - 6 * a * c[4] - 4 * b * c[6] + 4 * w[9]),
    (3, 4, 0): -4
    * (-4 * a * c[5] + b * c[1] - 6 * b * c[7] + 4 * w[10]),
    (3, 3, 1): -32 * (-a * b + w[11]),
    (2, 5, 0): 4
    * (-3 * a * c[0] + 2 * a * c[6] - 2 * b * c[2] + 2 * w[3]),
    (1, 6, 0): 4 * (-2 * a * c[1] - 3 * b * c[3] + 2 * w[4]),
    (1, 5, 1): 16 * (-a**2 + w[5]),
    (0, 7, 0): -4 * a * c[2],
}
assert coefficient_dictionary(raw_E7) == {
    monomial: sp.expand(value)
    for monomial, value in expected_E7_coefficients.items()
}
E7_matrix, _ = sp.linear_eq_to_matrix(
    list(expected_E7_coefficients.values()), list(w)
)
assert E7_matrix.rank() == 9

binary_quadratic_symbols = sp.symbols("q0:9")
binary_H2 = sp.Matrix(
    [
        binary_quadratic_symbols[3 * component] * x**2
        + binary_quadratic_symbols[3 * component + 1] * x * y
        + binary_quadratic_symbols[3 * component + 2] * y**2
        for component in range(3)
    ]
)
z_coefficients = (
    (3 * a * c[0] - 2 * a * c[6] + 2 * b * c[2]) / 2,
    (2 * a * c[1] + 3 * b * c[3]) / 2,
    a**2,
    (-a * c[10] + 6 * a * c[4] + 4 * b * c[6]) / 4,
    (4 * a * c[5] - b * c[1] + 6 * b * c[7]) / 4,
    a * b,
    (3 * a * c[8] + 2 * b * c[10]) / 2,
    (2 * a * c[9] + 3 * b * c[11] - 2 * b * c[5]) / 2,
    b**2,
)
solved_H2 = binary_H2 + sp.Matrix(
    [
        z_coefficients[3 * component] * x * z
        + z_coefficients[3 * component + 1] * y * z
        + z_coefficients[3 * component + 2] * z**2
        for component in range(3)
    ]
)
solved_E7 = homogeneous_coefficient(
    weighted_determinant(zero_linear, solved_H2, E8_H3, H4), 7
)
assert_zero(solved_E7 + 4 * b * c[9] * x**7 + 4 * a * c[2] * y**7)


# ---------------------------------------------------------------------------
# The two-nonzero orbit: E6 has six essential compatibilities.  They are
# precisely the affine-gauge directions, and E5 then kills two L0 columns.
# ---------------------------------------------------------------------------

ell = sp.symbols("ell0:9")
linear_part = sp.Matrix(3, 3, ell)
generic_substitution = {a: 1, b: 1, c[2]: 0, c[9]: 0}
generic_H3 = sp.expand(E8_H3.subs(generic_substitution))
generic_H2 = sp.expand(solved_H2.subs(generic_substitution))
generic_E6 = homogeneous_coefficient(
    weighted_determinant(linear_part, generic_H2, generic_H3, H4), 6
)
generic_unknowns = list(binary_quadratic_symbols) + list(ell)
generic_E6_equations = list(coefficient_dictionary(generic_E6).values())
generic_E6_matrix, generic_E6_rhs = sp.linear_eq_to_matrix(
    generic_E6_equations, generic_unknowns
)
assert generic_E6_matrix.shape == (13, 18)
assert generic_E6_matrix.rank() == 6

generic_relations = (
    c[11] - 2 * c[5],
    c[8],
    c[1] - 2 * c[7],
    c[10] - 2 * c[4],
    c[3],
    c[0] - 2 * c[6],
)
generic_left_compatibilities = [
    sp.factor((vector.T * generic_E6_rhs)[0])
    for vector in generic_E6_matrix.T.nullspace()
]
generic_relation_substitution = {
    c[11]: 2 * c[5],
    c[8]: 0,
    c[1]: 2 * c[7],
    c[10]: 2 * c[4],
    c[3]: 0,
    c[0]: 2 * c[6],
}
assert all(
    sp.expand(item.subs(generic_relation_substitution)) == 0
    for item in generic_left_compatibilities
)
for relation in generic_relations:
    assert any(
        sp.cancel(item / relation).is_number
        and sp.cancel(item / relation) != 0
        for item in generic_left_compatibilities
    )

redundant_compatibility = (
    c[0] * c[1]
    + 2 * c[1] * c[4]
    - 2 * c[1] * c[6]
    + c[1] * c[8]
    - c[10] * c[11]
    - c[10] * c[3]
    + 2 * c[10] * c[5]
    - 2 * c[10] * c[7]
)
redundant_certificate = (
    c[1] * (c[0] - 2 * c[6])
    - c[1] * (c[10] - 2 * c[4])
    + c[1] * c[8]
    - c[10] * (c[11] - 2 * c[5])
    - c[10] * c[3]
    + c[10] * (c[1] - 2 * c[7])
)
assert_zero(redundant_compatibility - redundant_certificate)
assert any(
    sp.cancel(item / redundant_compatibility).is_number
    and sp.cancel(item / redundant_compatibility) != 0
    for item in generic_left_compatibilities
)

generic_C3_on_relations = sp.expand(
    C3.subs({c[2]: 0, c[9]: 0}).subs(generic_relation_substitution)
)
generic_T2 = T2.subs({a: 1, b: 1})
mu = -c[4]
nu = -c[7]
xi = (c[4] - c[6]) / 2
eta = (c[7] - c[5]) / 2
gauge_correction = (
    xi * H4.diff(x)
    + eta * H4.diff(y)
    + (mu * x + nu * y) * generic_T2
)
assert all(
    sp.expand(entry) == 0
    for entry in generic_C3_on_relations + gauge_correction
)

canonical_generic_H3 = z * generic_T2
canonical_generic_H2 = binary_H2 + z**2 * sp.ones(3, 1)
canonical_generic_E6 = homogeneous_coefficient(
    weighted_determinant(
        linear_part, canonical_generic_H2, canonical_generic_H3, H4
    ),
    6,
)
canonical_generic_solution = {
    binary_quadratic_symbols[1]: 0,
    binary_quadratic_symbols[4]: 0,
    binary_quadratic_symbols[7]: 0,
    ell[2]: binary_quadratic_symbols[0] + binary_quadratic_symbols[2],
    ell[5]: binary_quadratic_symbols[3] + binary_quadratic_symbols[5],
    ell[8]: binary_quadratic_symbols[6] + binary_quadratic_symbols[8],
}
assert_zero(canonical_generic_E6.subs(canonical_generic_solution))
canonical_generic_matrix, _ = sp.linear_eq_to_matrix(
    list(coefficient_dictionary(canonical_generic_E6).values()),
    generic_unknowns,
)
assert canonical_generic_matrix.rank() == 6

generic_E5_after_E6 = homogeneous_coefficient(
    weighted_determinant(
        linear_part,
        canonical_generic_H2,
        canonical_generic_H3,
        H4,
    ),
    5,
).subs(canonical_generic_solution)
expected_generic_E5 = (
    -4 * ell[7] * x**5
    - 4 * ell[6] * x**4 * y
    + 8 * ell[4] * x**3 * y**2
    + 8 * ell[3] * x**2 * y**3
    - 4 * ell[1] * x * y**4
    - 4 * ell[0] * y**5
)
assert_zero(generic_E5_after_E6 - expected_generic_E5)


# ---------------------------------------------------------------------------
# The one-nonzero orbit.  Its affine normal slice has five parameters
# (S,D,P,M,N) with the complete equation P*M=0.
# ---------------------------------------------------------------------------

one_nonzero_substitution = {a: 1, b: 0, c[2]: 0}
one_H3 = sp.expand(E8_H3.subs(one_nonzero_substitution))
one_H2 = sp.expand(solved_H2.subs(one_nonzero_substitution))
one_E6 = homogeneous_coefficient(
    weighted_determinant(linear_part, one_H2, one_H3, H4), 6
)
one_E6_equations = list(coefficient_dictionary(one_E6).values())
one_E6_matrix, one_E6_rhs = sp.linear_eq_to_matrix(
    one_E6_equations, generic_unknowns
)
assert one_E6_matrix.shape == (10, 18)
assert one_E6_matrix.rank() == 6
one_compatibilities = [
    sp.factor((vector.T * one_E6_rhs)[0])
    for vector in one_E6_matrix.T.nullspace()
]
expected_one_relations = (
    c[8],
    c[10] - 2 * c[4],
    c[0] - 2 * c[6],
    c[10] * c[9],
)
for relation in expected_one_relations:
    assert any(
        sp.cancel(item / relation).is_number
        and sp.cancel(item / relation) != 0
        for item in one_compatibilities
    )

S, D, P, M, N = sp.symbols("S D P M N")
one_C3_on_relations = sp.expand(
    C3.subs(c[2], 0).subs(
        {c[8]: 0, c[10]: 2 * c[4], c[0]: 2 * c[6]}
    )
)
one_T2 = T2.subs({a: 1, b: 0})
one_gauge_correction = (
    -c[6] * H4.diff(x) / 2
    - c[5] * H4.diff(y) / 2
    - c[7] * y * one_T2
)
one_normal_substitution = {
    S: c[1] - 2 * c[7],
    D: c[3],
    P: c[4],
    M: c[9],
    N: c[11] - 2 * c[5],
}
normal_C3 = sp.Matrix(
    [
        S * x**2 * y + D * y**3,
        P * x**3,
        M * x**2 * y + 2 * P * x * y**2 + N * y**3,
    ]
)
assert all(
    sp.expand(entry) == 0
    for entry in (
        one_C3_on_relations
        + one_gauge_correction
        - normal_C3.subs(one_normal_substitution)
    )
)
assert_zero(
    (c[10] * c[9]).subs(c[10], 2 * c[4])
    - 2 * (P * M).subs(one_normal_substitution)
)
normal_H3 = normal_C3 + z * sp.Matrix([2 * x**2, y**2, 0])
q0, q2, q3, q5, q6, q8 = sp.symbols("q0 q2 q3 q5 q6 q8")
normal_H2 = sp.Matrix(
    [
        q0 * x**2 + sp.Rational(3, 2) * D * P * x * y + q2 * y**2,
        q3 * x**2 - sp.Rational(1, 4) * P * S * x * y + q5 * y**2,
        q6 * x**2 + sp.Rational(3, 2) * N * P * x * y + q8 * y**2,
    ]
) + z * sp.Matrix([S * y, P * x, M * y]) + z**2 * sp.Matrix([1, 0, 0])
normal_linear = sp.Matrix(
    [
        [ell[0], ell[1], q0],
        [ell[3], ell[4], q3],
        [ell[6], ell[7], q6 - P**2],
    ]
)
normal_E6 = homogeneous_coefficient(
    weighted_determinant(normal_linear, normal_H2, normal_H3, H4), 6
)
assert_zero(normal_E6 - 2 * M * P * x**6)

normal_E5 = homogeneous_coefficient(
    weighted_determinant(normal_linear, normal_H2, normal_H3, H4), 5
)
expected_normal_E5 = (
    3 * N * P**2 * x**5
    + (-M * P * S + 8 * P * q8 - 8 * ell[6]) * x**4 * y / 2
    + 6 * M * P * x**4 * z
    + 3 * P**2 * S * x**3 * y**2
    - (3 * D * M * P + 16 * P * q5 - 16 * ell[3])
    * x**2
    * y**3
    / 2
    + 3 * D * P**2 * x * y**4
    + (-P * S**2 + 4 * P * q2 - 4 * ell[0]) * y**5
)
assert_zero(normal_E5 - expected_normal_E5)

nonzero_P_solution = {
    M: 0,
    N: 0,
    S: 0,
    D: 0,
    ell[0]: P * q2,
    ell[3]: P * q5,
    ell[6]: P * q8,
}
assert_zero(normal_E5.subs(nonzero_P_solution))
normal_E4_after_E5 = homogeneous_coefficient(
    weighted_determinant(normal_linear, normal_H2, normal_H3, H4), 4
).subs(nonzero_P_solution)
expected_normal_E4 = (
    2 * P * ell[7] * x**4
    - 4 * P * ell[4] * x**2 * y**2
    + 2 * P * ell[1] * y**4
)
assert_zero(normal_E4_after_E5 - expected_normal_E4)


# On P=0, the polynomial coordinate U=z+x^2 exposes a plane-plus-shear
# map.  This identity retains all four remaining normal moduli.
U = sp.symbols("U")
P_zero_map = sp.expand(
    (
        normal_linear * sp.Matrix([x, y, z])
        + normal_H2
        + normal_H3
        + H4
    ).subs(P, 0)
)
P_zero_in_U = sp.expand(P_zero_map.subs(z, U - x**2))
first_column = sp.Matrix([ell[0], ell[3], ell[6]])
second_column = sp.Matrix([ell[1], ell[4], ell[7]])
U_column = sp.Matrix([q0, q3, q6])
expected_P_zero_map = (
    first_column * x
    + second_column * y
    + U_column * U
    + sp.Matrix(
        [
            U**2 + S * y * U + D * y**3 + q2 * y**2,
            U * y**2 + q5 * y**2,
            y**4 + M * y * U + N * y**3 + q8 * y**2,
        ]
    )
)
assert P_zero_in_U == expected_P_zero_map


# The remaining one-nonzero orbit is obtained by the exact source/target
# involution x<->y and output 1<->3.
swap_target = sp.Matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
swapped_H4 = swap_target * H4.subs({x: y, y: x}, simultaneous=True)
assert swapped_H4 == H4
swapped_T2 = swap_target * T2.subs(
    {x: y, y: x, a: b, b: a}, simultaneous=True
)
assert swapped_T2 == T2


if __name__ == "__main__":
    print(
        "PASS: exact conic double-cover E8--E4 branch classification "
        "and plane-exit factorization"
    )

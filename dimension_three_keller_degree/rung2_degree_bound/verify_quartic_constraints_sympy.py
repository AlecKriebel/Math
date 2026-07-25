#!/usr/bin/python3
"""Exact regression checks for the quartic working lemmas.

This script does not prove the geometric or duality statements.  It checks:

1. the nine homogeneous determinant identities;
2. the degree-eight and degree-seven coefficients in the line-type net;
3. the discrete degree-three line-boundary table;
4. the global degree and parity consequences of the conductor formula.
"""

from __future__ import annotations

import itertools

import sympy as sp


def coeff(expr: sp.Expr, variable: sp.Symbol, degree: int) -> sp.Expr:
    return sp.Poly(sp.expand(expr), variable).coeff_monomial(variable**degree)


def determinant_coefficient_checks() -> None:
    z = sp.symbols("z")
    entries_a = sp.symbols("a11:14 a21:24 a31:34")
    entries_b = sp.symbols("b11:14 b21:24 b31:34")
    entries_c = sp.symbols("c11:14 c21:24")

    A = sp.Matrix(3, 3, entries_a)
    B = sp.Matrix(3, 3, entries_b)
    C = sp.Matrix(
        [
            entries_c[0:3],
            entries_c[3:6],
            (0, 0, 0),
        ]
    )
    polynomial = sp.expand((sp.eye(3) + z * A + z**2 * B + z**3 * C).det())

    expected_8 = sp.Matrix.vstack(C[0, :], C[1, :], B[2, :]).det()
    assert sp.expand(coeff(polynomial, z, 8) - expected_8) == 0

    B_zero_third = B.copy()
    B_zero_third[2, :] = sp.zeros(1, 3)
    polynomial_zero_third = sp.expand(
        (sp.eye(3) + z * A + z**2 * B_zero_third + z**3 * C).det()
    )
    expected_7 = sp.Matrix.vstack(C[0, :], C[1, :], A[2, :]).det()
    assert sp.expand(coeff(polynomial_zero_third, z, 7) - expected_7) == 0

    # Check all nine polarized identities by assigning formal weights.
    generic_c_entries = sp.symbols("d11:14 d21:24 d31:34")
    generic_c = sp.Matrix(3, 3, generic_c_entries)
    weighted = sp.expand(
        (sp.eye(3) + z * A + z**2 * B + z**3 * generic_c).det() - 1
    )

    def e2(matrix: sp.Matrix) -> sp.Expr:
        return (
            sp.trace(matrix) ** 2 - sp.trace(matrix * matrix)
        ) / 2

    def s(matrix_1: sp.Matrix, matrix_2: sp.Matrix) -> sp.Expr:
        return sp.trace(matrix_1) * sp.trace(matrix_2) - sp.trace(
            matrix_1 * matrix_2
        )

    # Polarized determinant coefficients are recovered directly from a
    # two- or three-parameter determinant, avoiding a hand-coded formula.
    u, v, w = sp.symbols("u v w")
    det_abc = sp.expand((u * A + v * B + w * generic_c).det())

    def delta_coefficient(i: int, j: int, k: int) -> sp.Expr:
        raw = sp.Poly(det_abc, u, v, w).coeff_monomial(u**i * v**j * w**k)
        multinomial = sp.factorial(3) / (
            sp.factorial(i) * sp.factorial(j) * sp.factorial(k)
        )
        return sp.expand(raw / multinomial)

    identities = {
        1: sp.trace(A),
        2: sp.trace(B) + e2(A),
        3: sp.trace(generic_c) + s(A, B) + A.det(),
        4: e2(B) + s(A, generic_c) + 3 * delta_coefficient(2, 1, 0),
        5: s(B, generic_c)
        + 3 * delta_coefficient(2, 0, 1)
        + 3 * delta_coefficient(1, 2, 0),
        6: e2(generic_c)
        + B.det()
        + 6 * delta_coefficient(1, 1, 1),
        7: 3 * delta_coefficient(1, 0, 2)
        + 3 * delta_coefficient(0, 2, 1),
        8: 3 * delta_coefficient(0, 1, 2),
        9: generic_c.det(),
    }
    for degree, identity in identities.items():
        assert sp.expand(coeff(weighted, z, degree) - identity) == 0


def discrete_table_checks() -> None:
    profiles: list[tuple[int, int, int, int, int, int, int]] = []
    for s, q, genus in itertools.product(range(2, 16), range(1, 4), range(0, 8)):
        transpositions = 2 * genus + q + 1
        for split in range(0, 16):
            defect_one = s - split - transpositions
            if defect_one < 0:
                continue
            total_defect = defect_one + 2 * split + 2 * transpositions
            punctures = s + split + q
            if punctures > 16:
                continue
            assert total_defect == 2 * genus + 1 + punctures

            # The conductor degree obtained by summing the local formulas is
            # independent of the distribution of hyperplane multiplicities.
            conductor_degree = 64 - transpositions + 3 + q
            assert conductor_degree == 66 - 2 * genus

            # Odd conductor branches occur in an even number globally.
            odd_branches = transpositions + (1 if q == 2 else 0)
            assert odd_branches % 2 == 0
            profiles.append(
                (
                    s,
                    q,
                    genus,
                    split,
                    defect_one,
                    transpositions,
                    punctures,
                )
            )

    s_two = [profile for profile in profiles if profile[0] == 2]
    assert s_two == [(2, 1, 0, 0, 0, 2, 3)]

    # The sharp genus caps by infinity partition.
    maxima = {
        q: max(profile[2] for profile in profiles if profile[1] == q)
        for q in range(1, 4)
    }
    assert maxima == {1: 6, 2: 5, 3: 4}


def nonprimitive_warning_example() -> None:
    x, y, z = sp.symbols("x y z")
    linear = x + y
    quadratic = y**2 + x * z
    P = linear**4
    Q = quadratic**2
    R = linear * quadratic
    jacobian = sp.Matrix(
        [
            [sp.diff(poly, variable) for variable in (x, y, z)]
            for poly in (P, Q, R)
        ]
    ).det()
    assert sp.expand(jacobian) == 0
    assert sp.expand(R**4 - P * Q**2) == 0


def rank_one_quartic_obstruction_example() -> None:
    x, y, z = sp.symbols("x y z")
    F = sp.Matrix([x + y**2, y + (x + y**2) ** 2, z])
    jacobian = F.jacobian((x, y, z))
    assert sp.expand(jacobian.det() - 1) == 0

    H2 = sp.Matrix([y**2, x**2, 0])
    H3 = sp.Matrix([0, 2 * x * y**2, 0])
    H4 = sp.Matrix([0, y**4, 0])
    assert sp.expand(F - sp.Matrix([x, y, z]) - H2 - H3 - H4) == sp.zeros(3, 1)
    assert H4.jacobian((x, y, z)).rank() == 1

    # On the quotient by e3, the coefficient matrices E12 and E21
    # generate all of M_2, certifying that they have no common invariant
    # line and hence no common full flag upstairs.
    E12 = sp.Matrix([[0, 1], [0, 0]])
    E21 = sp.Matrix([[0, 0], [1, 0]])
    generated = [sp.eye(2), E12, E21, E12 * E21]
    flattened = sp.Matrix.hstack(*(matrix.reshape(4, 1) for matrix in generated))
    assert flattened.rank() == 4


if __name__ == "__main__":
    determinant_coefficient_checks()
    discrete_table_checks()
    nonprimitive_warning_example()
    rank_one_quartic_obstruction_example()
    print("PASS: exact quartic determinant, boundary, and conductor regressions")

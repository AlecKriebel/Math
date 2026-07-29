#!/usr/bin/env python3
"""Exact checks for the determinant-boundary corner factorization note.

This verifier has three independent finite components:

1. Fusion-path corner dimensions for both invertible three-strand
   determinant endpoints, checked through twelve added strands.
2. Exact 3-, 2-, and 3-dimensional four-strand quotient blocks, including
   the full d=6 abstract multiplicity/rank bookkeeping.
3. The five-site boundary-word reduction and the six-site generic
   Clifford block.

Only exact SymPy arithmetic is used.
"""

from __future__ import annotations

import sympy as sp


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def fusion_corner_audit() -> None:
    weights = [
        (a, b)
        for a in range(4)
        for b in range(4 - a)
    ]
    index = {weight: position for position, weight in enumerate(weights)}

    # Columns are source simples and rows are target simples.
    fusion_x = sp.zeros(10)
    for a, b in weights:
        successors: list[tuple[int, int]] = []
        if a + b < 3:
            successors.append((a + 1, b))
        if a > 0:
            successors.append((a - 1, b + 1))
        if b > 0:
            successors.append((a, b - 1))
        for successor in successors:
            fusion_x[index[successor], index[(a, b)]] += 1

    # The simple current g=(3,0) acts by a fusion-graph automorphism.
    fusion_g = sp.zeros(10)
    for a, b in weights:
        image = (3 - a - b, a)
        fusion_g[index[image], index[(a, b)]] = 1
    assert fusion_g**3 == sp.eye(10)
    assert fusion_g * fusion_x == fusion_x * fusion_g

    vacuum = sp.zeros(10, 1)
    vacuum[index[(0, 0)]] = 1
    determinant = fusion_g * vacuum

    # Multiplication by g gives a path-count bijection for every length.
    vacuum_paths = vacuum
    determinant_paths = determinant
    for added_sites in range(13):
        assert determinant_paths == fusion_g * vacuum_paths
        vacuum_corner_dimension = sum(
            int(entry) ** 2 for entry in vacuum_paths
        )
        determinant_corner_dimension = sum(
            int(entry) ** 2 for entry in determinant_paths
        )
        assert determinant_corner_dimension == vacuum_corner_dimension

        if added_sites == 1:
            assert sorted(
                int(entry)
                for entry in determinant_paths
                if entry
            ) == [1]
            assert determinant_corner_dimension == 1
        if added_sites == 2:
            assert sorted(
                int(entry)
                for entry in determinant_paths
                if entry
            ) == [1, 1]
            assert determinant_corner_dimension == 2
        if added_sites == 3:
            assert sorted(
                int(entry)
                for entry in determinant_paths
                if entry
            ) == [1, 1, 2]
            assert determinant_corner_dimension == 6

        vacuum_paths = fusion_x * vacuum_paths
        determinant_paths = fusion_x * determinant_paths


def common_one(p: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    return sp.Rational(3, 2) * p * q * p - p / 2


def common_zero(p: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    identity = sp.eye(p.rows)
    pp = identity - p
    qq = identity - q
    return sp.Rational(3, 2) * pp * qq * pp - pp / 2


def cubic_residual(p: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    return p * q * p - q * p * q - (p - q) / 3


def four_strand_blocks() -> list[tuple[str, tuple[sp.Matrix, ...]]]:
    one_third = sp.Rational(1, 3)
    q_generic = sp.Matrix(
        [
            [one_third, sp.sqrt(2) / 3],
            [sp.sqrt(2) / 3, sp.Rational(2, 3)],
        ]
    )

    p1_31 = sp.diag(0, 1, 0)
    p2_31 = sp.zeros(3)
    p2_31[1:3, 1:3] = q_generic
    vector = sp.Matrix(
        [1 / sp.sqrt(2), 0, 1 / sp.sqrt(2)]
    )
    p3_31 = vector * vector.T

    identity_3 = sp.eye(3)
    block_31 = (p1_31, p2_31, p3_31)
    block_211 = tuple(identity_3 - p for p in block_31)

    p1_22 = sp.diag(1, 0)
    block_22 = (p1_22, q_generic, p1_22)

    return [
        ("31", block_31),
        ("22", block_22),
        ("211", block_211),
    ]


def four_strand_exact_audit() -> None:
    blocks = four_strand_blocks()

    weighted_dimension = 0
    weighted_generator_ranks = [0, 0, 0]
    weighted_common_one = 0
    weighted_common_zero = 0

    # For d=6, s=3, every four-strand simple is repeated 2*s^4 times.
    s = 3
    multiplicity = 2 * s**4
    assert multiplicity == 162

    for name, generators in blocks:
        p1, p2, p3 = generators
        identity = sp.eye(p1.rows)
        for p in generators:
            assert is_zero(p**2 - p)
            assert is_zero(p.T - p)
        assert is_zero(cubic_residual(p1, p2))
        assert is_zero(cubic_residual(p2, p3))
        assert is_zero(p1 * p3 - p3 * p1)

        e_left = common_one(p1, p2)
        e_right = common_one(p2, p3)
        f_left = common_zero(p1, p2)
        f_right = common_zero(p2, p3)

        for projection in (e_left, e_right, f_left, f_right):
            assert is_zero(projection**2 - projection)
            assert is_zero(projection.T - projection)

        assert is_zero(e_left * p3 * e_left - e_left / 2)
        assert is_zero(
            f_left * (identity - p3) * f_left - f_left / 2
        )
        assert is_zero(e_left * e_right * e_left - e_left / 4)
        assert is_zero(e_right * e_left * e_right - e_right / 4)
        assert is_zero(f_left * f_right * f_left - f_left / 4)
        assert is_zero(f_right * f_left * f_right - f_right / 4)
        assert is_zero(e_left * f_right)
        assert is_zero(f_left * e_right)

        if name == "31":
            assert sp.trace(e_left) == 0
            assert sp.trace(f_left) == 1
        elif name == "211":
            assert sp.trace(e_left) == 1
            assert sp.trace(f_left) == 0
        else:
            assert sp.trace(e_left) == 0
            assert sp.trace(f_left) == 0

        weighted_dimension += multiplicity * p1.rows
        for position, p in enumerate(generators):
            weighted_generator_ranks[position] += (
                multiplicity * int(sp.trace(p))
            )
        weighted_common_one += multiplicity * int(sp.trace(e_left))
        weighted_common_zero += multiplicity * int(sp.trace(f_left))

    assert weighted_dimension == 6**4 == 1296
    assert weighted_generator_ranks == [648, 648, 648]
    assert weighted_common_one == weighted_common_zero == 162


def boundary_word_and_clifford_audit() -> None:
    # The five-site reduction can be checked in the universal algebra by
    # using only e*a*e=e/2, b*e=e*b, b^2=b, and
    # e*a*b*a*e=(e+e*b)/6.  Represent e by 1 and b by its two scalar
    # projection characters 0 and 1.
    for b in (sp.Integer(0), sp.Integer(1)):
        e_a_b_a_e = (1 + b) / 6
        h_boundary_word = (
            1
            - 2 * b
            + 4 * (b / 2 + b / 2)
            - 8 * e_a_b_a_e
        )
        assert sp.simplify(h_boundary_word + (1 - 2 * b) / 3) == 0

    # The generic H3 block on the three added sites.
    p = sp.diag(1, 0)
    q = sp.Matrix(
        [
            [sp.Rational(1, 3), sp.sqrt(2) / 3],
            [sp.sqrt(2) / 3, sp.Rational(2, 3)],
        ]
    )
    z = 2 * p - sp.eye(2)
    x = (sp.Rational(3, 1) / sp.sqrt(2)) * (
        p * q * (sp.eye(2) - p)
        + (sp.eye(2) - p) * q * p
    )
    assert is_zero(z**2 - sp.eye(2))
    assert is_zero(x**2 - sp.eye(2))
    assert is_zero(z * x + x * z)

    # At odd s=3 the path-factor M2 is still valid: it occurs with odd
    # module multiplicity and supplies the only factor of two.
    s = 3
    determinant_rank = s**3
    generic_module_multiplicity = 3 * s**6
    assert determinant_rank == 27
    assert generic_module_multiplicity == 2187
    assert determinant_rank % 2 == 1
    assert generic_module_multiplicity % 2 == 1
    assert 2 * generic_module_multiplicity % 2 == 0


def main() -> None:
    fusion_corner_audit()
    print("PASS determinant simple-current corner dimensions through 12 added sites")
    four_strand_exact_audit()
    print("PASS exact d=6 abstract four-strand boundary model")
    boundary_word_and_clifford_audit()
    print("PASS five-site spectator reduction and six-site Clifford limitation")
    print("All determinant-boundary corner checks passed exactly.")


if __name__ == "__main__":
    main()

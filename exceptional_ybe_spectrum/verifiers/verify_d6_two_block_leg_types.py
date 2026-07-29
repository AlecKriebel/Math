#!/usr/bin/env python3
"""Exact checks for the dimension-six two-block leg-algebra audit.

The human proof is in notes/d6_two_block_leg_types.md.  This verifier
checks only finite algebra and block calculations; the established empty
rank-two d=2 class remains an explicit external dependency.
"""

from __future__ import annotations

import itertools

import sympy as sp


def vec(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.reshape(matrix.rows * matrix.cols, 1)


def permutation_matrix(permutation: tuple[int, ...]) -> sp.Matrix:
    out = sp.zeros(len(permutation))
    for column, row in enumerate(permutation):
        out[row, column] = 1
    return out


def algebra_4_plus_2() -> list[sp.Matrix]:
    z = sp.diag(0, 0, 0, 0, 1, 1)
    return [sp.eye(6) - z, z]


def algebra_m2_i2_plus_2() -> list[sp.Matrix]:
    basis: list[sp.Matrix] = []
    for i, j in itertools.product(range(2), repeat=2):
        matrix = sp.zeros(6)
        for multiplicity in range(2):
            matrix[2 * i + multiplicity, 2 * j + multiplicity] = 1
        basis.append(matrix)
    last = sp.zeros(6)
    last[4, 4] = last[5, 5] = 1
    basis.append(last)
    return basis


def intersection_dimension(
    first: list[sp.Matrix],
    second: list[sp.Matrix],
) -> int:
    joined = sp.Matrix.hstack(
        *(list(map(vec, first)) + list(map(vec, second)))
    )
    return len(first) + len(second) - joined.rank()


def check_relative_positions() -> None:
    a41 = algebra_4_plus_2()
    a221 = algebra_m2_i2_plus_2()
    p_simple = permutation_matrix((0, 1, 2, 4, 3, 5))
    p_factor = permutation_matrix((0, 2, 1, 4, 3, 5))

    for first, second, unitary in (
        (a41, a41, p_simple),
        (a41, a221, p_simple),
        (a221, a41, p_simple),
        (a221, a221, p_factor),
    ):
        conjugated = [unitary * x * unitary.T for x in second]
        assert intersection_dimension(first, conjugated) == 1


def generic_pair() -> tuple[sp.Matrix, sp.Matrix]:
    p = sp.diag(1, 0)
    q = sp.Matrix(
        [
            [sp.Rational(1, 3), sp.sqrt(2) / 3],
            [sp.sqrt(2) / 3, sp.Rational(2, 3)],
        ]
    )
    return p, q


def endpoint_block(a: int, b: int) -> tuple[sp.Matrix, sp.Matrix]:
    """The exact 24ab-dimensional endpoint pair from the note."""

    common = 3 * a * b
    generic = 9 * a * b
    p_pieces: list[sp.Matrix] = [sp.ones(1, 1) for _ in range(common)]
    q_pieces: list[sp.Matrix] = [sp.ones(1, 1) for _ in range(common)]
    for _ in range(generic):
        p, q = generic_pair()
        p_pieces.append(p)
        q_pieces.append(q)
    p_pieces.extend(sp.zeros(1, 1) for _ in range(common))
    q_pieces.extend(sp.zeros(1, 1) for _ in range(common))
    return sp.diag(*p_pieces), sp.diag(*q_pieces)


def check_endpoint_blocks() -> None:
    for a, b in itertools.product((1, 2), repeat=2):
        p, q = endpoint_block(a, b)
        size = 24 * a * b
        assert p.shape == q.shape == (size, size)
        assert p**2 == p and q**2 == q
        assert p.T == p and q.T == q
        assert sp.trace(p) == sp.trace(q) == 12 * a * b
        assert p * q * p - q * p * q == (p - q) / 3
        assert sp.trace(p * q) == 6 * a * b

    # (m,a) parameters for C I4 + C I2 and
    # (M2 tensor I2) + C I2.
    types = {
        "4+2": ((1, 2), (1, 1)),
        "m2i2+2": ((2, 1), (1, 1)),
    }
    for left in types.values():
        for right in types.values():
            dimension = rank_p = common = overlap = 0
            for m, a in left:
                for n, b in right:
                    multiplicity = m * n
                    dimension += multiplicity * 24 * a * b
                    rank_p += multiplicity * 12 * a * b
                    common += multiplicity * 3 * a * b
                    overlap += multiplicity * 6 * a * b
            assert dimension == 216
            assert rank_p == 108
            assert common == 27
            assert overlap == 54


def check_shared_atom_steps() -> None:
    # Rank-one cell determinant gap.
    assert sp.Rational(1, 16) < sp.Rational(1, 9)
    bell = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
    q = bell * bell.T
    q12 = sp.kronecker_product(q, sp.eye(2))
    q23 = sp.kronecker_product(sp.eye(2), q)
    assert q12 * q23 * q12 == q12 / 4

    # If the W x W cell is scalar, the cubic forces the entire W row
    # to have the same scalar.  A non-scalar involution guards the sign.
    y = sp.kronecker_product(sp.eye(2), sp.kronecker_product(
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    ))
    identity = sp.eye(8)
    for sign in (-1, 1):
        x = sign * identity
        residual = x * y * x - y * x * y - (x - y) / 3
        assert residual == sp.Rational(4, 3) * (y - x)
        assert residual != sp.zeros(8)
        assert 6 * sign * sp.eye(2) != sp.zeros(2)


def main() -> None:
    check_shared_atom_steps()
    check_relative_positions()
    check_endpoint_blocks()
    print("rank-one cell determinant gap: exact")
    print("shared scalar cell propagation: exact")
    print("d=2 rank-two emptiness: explicit external dependency")
    print("two-block relative intersections: scalar in all four pairs")
    print("endpoint cubic blocks for ab=1,2,4: exact")
    print("all four ordered algebra pairs: D=216, rank=108, common=27")
    print("PASS")


if __name__ == "__main__":
    main()

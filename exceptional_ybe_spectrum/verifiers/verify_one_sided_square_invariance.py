#!/usr/bin/env python3
"""Exact verifier for the one-sided square-invariance audit.

This script constructs a rank-18 projection on C^6 tensor C^6.  It has
scalar partial traces 3 I_6 and contains the published balanced
exceptional d=4 projection on W tensor W, but U tensor U is not
invariant.  The construction deliberately fails the ambient cubic
relation; an explicit nonzero coefficient is checked exactly.

No floating-point arithmetic is used.
"""

from __future__ import annotations

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def partial_trace_two(
    matrix: sp.Matrix, dimension: int, traced_leg: int
) -> sp.Matrix:
    """Trace one leg of a two-site operator."""

    if traced_leg == 1:
        return sp.Matrix(
            dimension,
            dimension,
            lambda row, column: sum(
                matrix[
                    row * dimension + index,
                    column * dimension + index,
                ]
                for index in range(dimension)
            ),
        )
    if traced_leg == 0:
        return sp.Matrix(
            dimension,
            dimension,
            lambda row, column: sum(
                matrix[
                    index * dimension + row,
                    index * dimension + column,
                ]
                for index in range(dimension)
            ),
        )
    raise ValueError("traced_leg must be 0 or 1")


def published_projection() -> sp.Matrix:
    identity_2 = sp.eye(2)
    x = sp.Matrix([[0, 1], [1, 0]])
    z = sp.diag(1, -1)
    j = sp.Matrix([[0, -1], [1, 0]])
    h = (
        -tensor(z, identity_2, z, z) / sp.sqrt(6)
        - tensor(z, identity_2, j, j) / sp.sqrt(6)
        - tensor(j, identity_2, z, j) / sp.sqrt(6)
        + tensor(j, identity_2, j, z) / sp.sqrt(6)
        - tensor(x, identity_2, x, x) / sp.sqrt(3)
    )
    assert is_zero(h.conjugate().T - h)
    assert is_zero(h**2 - sp.eye(16))
    assert sp.trace(h) == 0
    return (sp.eye(16) - h) / 2


def cubic_residual(projection: sp.Matrix, dimension: int) -> sp.Matrix:
    identity = sp.eye(dimension)
    first = tensor(projection, identity)
    second = tensor(identity, projection)
    return (
        first * second * first
        - second * first * second
        - sp.Rational(1, 3) * (first - second)
    )


def embed_d4_and_rectangle_mix() -> tuple[sp.Matrix, sp.Matrix]:
    """Return the d=6 projection and its d=4 diagonal restriction."""

    p4 = published_projection()
    dimension = 6
    projection = sp.MutableSparseMatrix(dimension**2, dimension**2, {})

    # Embed P_4 into the W tensor W cell, W = span(v_0,...,v_3).
    for row in range(16):
        first_row, second_row = divmod(row, 4)
        ambient_row = dimension * first_row + second_row
        for column in range(16):
            entry = p4[row, column]
            if entry != 0:
                first_column, second_column = divmod(column, 4)
                ambient_column = dimension * first_column + second_column
                projection[ambient_row, ambient_column] = entry

    # Eight untouched coordinate vectors in (W tensor W)^perp.
    coordinate_vectors = (
        (0, 4),
        (1, 4),
        (3, 5),
        (4, 0),
        (4, 1),
        (5, 2),
        (5, 3),
        (5, 5),
    )
    for first, second in coordinate_vectors:
        index = dimension * first + second
        projection[index, index] = 1

    # Two orthonormal rectangle superpositions.
    pairs = (
        ((4, 4), (2, 5)),
        ((4, 5), (2, 4)),
    )
    for left, right in pairs:
        left_index = dimension * left[0] + left[1]
        right_index = dimension * right[0] + right[1]
        for row, column in (
            (left_index, left_index),
            (left_index, right_index),
            (right_index, left_index),
            (right_index, right_index),
        ):
            projection[row, column] += sp.Rational(1, 2)

    return sp.SparseMatrix(projection), p4


def check_universal_defect_arithmetic() -> None:
    d, r = sp.symbols("d r", integer=True, positive=True)
    u = d - r

    ambient_rank = d**2 / 2
    restricted_rank = r**2 / 2
    mixed_trace = r * u
    complementary_trace = sp.simplify(
        ambient_rank - restricted_rank - mixed_trace
    )
    assert sp.simplify(complementary_trace - u**2 / 2) == 0

    # The corner identity of a block projection
    # [[A,C],[C*,K]] is K^2+C*C=K.  The displayed scalar example
    # exercises all equalities in the variance formula.
    k = sp.diag(sp.Rational(1, 2), sp.Rational(1, 2), 0, 1)
    assert sp.trace(k) == 2
    assert sp.trace(k**2) == sp.Rational(3, 2)
    assert sp.trace(k - k**2) == sp.Rational(1, 2)


def check_exact_limitation_model() -> None:
    projection, p4 = embed_d4_and_rectangle_mix()
    dimension = 6
    identity_36 = sp.eye(dimension**2)

    assert is_zero(p4.conjugate().T - p4)
    assert is_zero(p4**2 - p4)
    assert sp.trace(p4) == 8
    assert p4.rank() == 8
    assert is_zero(partial_trace_two(p4, 4, 0) - 2 * sp.eye(4))
    assert is_zero(partial_trace_two(p4, 4, 1) - 2 * sp.eye(4))
    assert is_zero(cubic_residual(p4, 4))

    assert is_zero(projection.conjugate().T - projection)
    assert is_zero(projection**2 - projection)
    assert sp.trace(projection) == 18
    assert projection.rank() == 18
    assert is_zero(
        partial_trace_two(projection, dimension, 0) - 3 * sp.eye(6)
    )
    assert is_zero(
        partial_trace_two(projection, dimension, 1) - 3 * sp.eye(6)
    )

    e = sp.diag(1, 1, 1, 1, 0, 0)
    f = sp.eye(6) - e
    square_w = tensor(e, e)
    square_u = tensor(f, f)
    mixed = sp.eye(36) - square_w - square_u

    assert is_zero(projection * square_w - square_w * projection)
    assert not is_zero(projection * square_u - square_u * projection)

    compression = square_u * projection * square_u
    coupling = mixed * projection * square_u
    delta_first = sp.simplify(
        2 - sp.trace(compression * compression)
    )
    delta_corner = sp.simplify(
        sp.trace(compression - compression * compression)
    )
    delta_coupling = sp.simplify(
        sp.trace(coupling.conjugate().T * coupling)
    )
    commutator = projection * square_u - square_u * projection
    delta_commutator = sp.simplify(
        sp.trace(commutator.conjugate().T * commutator) / 2
    )

    assert sp.trace(compression) == 2
    assert sp.trace(compression * compression) == sp.Rational(3, 2)
    assert (
        delta_first
        == delta_corner
        == delta_coupling
        == delta_commutator
        == sp.Rational(1, 2)
    )

    # The Hecke and unitarity checks use q^2-q+1=0 exactly.
    q = (1 + sp.I * sp.sqrt(3)) / 2
    r_matrix = q * identity_36 - (1 + q) * projection
    assert is_zero(
        (r_matrix + identity_36) * (r_matrix - q * identity_36)
    )
    assert is_zero(r_matrix.conjugate().T * r_matrix - identity_36)

    # One exact matrix coefficient certifies failure of the ambient
    # spatial cubic without constructing its full 216-by-216 residual.
    identity_6 = sp.eye(6)
    first = tensor(projection, identity_6)
    second = tensor(identity_6, projection)
    input_vector = sp.zeros(216, 1)
    input_vector[4] = 1  # |0,0,4>
    residual_vector = (
        first * (second * (first * input_vector))
        - second * (first * (second * input_vector))
        - sp.Rational(1, 3)
        * (first * input_vector - second * input_vector)
    )
    assert sp.simplify(residual_vector[10] + sp.sqrt(2) / 48) == 0
    assert sp.simplify(residual_vector[10]) != 0  # <0,1,4| residual


def main() -> None:
    check_universal_defect_arithmetic()
    check_exact_limitation_model()
    print("PASS complement-invariance variance reduction")
    print("PASS exact d=6 two-site model with exceptional d=4 restriction")
    print("PASS delta = 1/2 and ambient cubic coefficient = -sqrt(2)/48")


if __name__ == "__main__":
    main()

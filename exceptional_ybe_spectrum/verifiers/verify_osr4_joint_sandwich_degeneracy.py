#!/usr/bin/env python3
"""Exact replay for the OSR-four joint-sandwich degeneracy audit.

The script uses SymPy exact arithmetic throughout.  It verifies finite
calibrations and rank certificates; the all-dimension quotient and
C*-algebra arguments are human proofs in the accompanying note.
"""

from __future__ import annotations

from collections import Counter
from itertools import product

import sympy as sp


def tensor(*matrices: sp.Matrix) -> sp.Matrix:
    result = sp.Matrix([[1]])
    for matrix in matrices:
        result = sp.kronecker_product(result, matrix)
    return result


def dagger(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.conjugate().T


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def vectorize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(matrix).reshape(matrix.rows * matrix.cols, 1)


def span_rank(matrices: list[sp.Matrix]) -> int:
    return sp.Matrix.hstack(*(vectorize(matrix) for matrix in matrices)).rank()


def hs_gram(matrices: list[sp.Matrix]) -> sp.Matrix:
    return sp.Matrix(
        len(matrices),
        len(matrices),
        lambda i, j: sp.simplify(
            sp.trace(dagger(matrices[i]) * matrices[j])
        ),
    )


def partial_trace_second(matrix: sp.Matrix, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda a, c: sp.simplify(
            sum(matrix[a * d + b, c * d + b] for b in range(d))
        ),
    )


def partial_trace_first(matrix: sp.Matrix, d: int) -> sp.Matrix:
    return sp.Matrix(
        d,
        d,
        lambda b, e: sp.simplify(
            sum(matrix[a * d + b, a * d + e] for a in range(d))
        ),
    )


def sandwich_matrix(
    outer_support: list[sp.Matrix],
    input_space: list[sp.Matrix],
) -> sp.Matrix:
    """Matrix of c_ik -> (sum c_ik B_i x B_k)_x.

    Inputs x are stacked vertically.  Columns use row-major (i,k) order.
    """
    columns = []
    for left in outer_support:
        for right in outer_support:
            columns.append(
                sp.Matrix.vstack(
                    *(
                        vectorize(left * middle * right)
                        for middle in input_space
                    )
                )
            )
    return sp.Matrix.hstack(*columns)


def sandwich_statistics(
    outer_support: list[sp.Matrix],
    support_inputs: list[sp.Matrix],
    identity: sp.Matrix,
) -> tuple[list[int], int, int]:
    individual = [
        span_rank(
            [
                left * middle * right
                for left in outer_support
                for right in outer_support
            ]
        )
        for middle in support_inputs
    ]
    support_rank = sandwich_matrix(outer_support, support_inputs).rank()
    operator_system_rank = sandwich_matrix(
        outer_support, [identity] + support_inputs
    ).rank()
    return individual, support_rank, operator_system_rank


def first_closure_rank(
    support: list[sp.Matrix], identity: sp.Matrix
) -> int:
    return span_rank(
        [identity]
        + support
        + [left * right for left in support for right in support]
    )


def finite_dimensional_cstar_check() -> tuple[tuple[int, ...], ...]:
    """Enumerate multisets (n_a) with sum n_a^2 = 5."""
    types = set()
    for length in range(1, 6):
        for sizes in product((1, 2), repeat=length):
            if tuple(sorted(sizes, reverse=True)) != sizes:
                continue
            if sum(size * size for size in sizes) == 5:
                types.add(sizes)
    result = tuple(sorted(types))
    assert set(result) == {(1, 1, 1, 1, 1), (2, 1)}

    # The rank-one C17 consequence is exactly divisibility by four.
    for d in range(1, 129):
        assert ((d * d) % 8 == 0) == (d % 4 == 0)
    return result


I2 = sp.eye(2)
I3 = sp.eye(3)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
J = sp.Matrix([[0, -1], [1, 0]])


def published_d4_rank_calibration() -> dict[str, object]:
    """Supports of the exact published d=4, OSR-three witness."""
    i4 = sp.eye(4)
    left = [
        tensor(Z, I2),
        sp.I * tensor(J, I2),
        tensor(X, I2),
    ]
    right = [
        -(tensor(Z, Z) + tensor(J, J)),
        -sp.I * (-tensor(Z, J) + tensor(J, Z)),
        -tensor(X, X),
    ]
    assert all(dagger(matrix) == matrix for matrix in left + right)
    assert span_rank(left) == span_rank(right) == 3

    right_on_left = sandwich_statistics(right, left, i4)
    left_on_right = sandwich_statistics(left, right, i4)
    assert right_on_left == ([7, 7, 4], 9, 9)
    assert left_on_right == ([7, 7, 4], 9, 9)
    assert first_closure_rank(left, i4) == 4
    assert first_closure_rank(right, i4) == 4
    return {
        "right_on_left": right_on_left,
        "left_on_right": left_on_right,
        "closure": (4, 4),
    }


def c61_d4_rank_calibration() -> dict[str, object]:
    """The exact balanced Clifford calibration retained with C61."""
    i4 = sp.eye(4)
    left = [
        tensor(X, I2),
        tensor(I2, X),
        tensor(Z, I2),
        tensor(X, Z),
    ]
    right = [
        tensor(X, I2),
        tensor(Z, I2),
        tensor(X, Z),
        tensor(Z, Y),
    ]
    assert span_rank(left) == span_rank(right) == 4

    right_on_left = sandwich_statistics(right, left, i4)
    left_on_right = sandwich_statistics(left, right, i4)
    assert right_on_left == ([7, 7, 7, 7], 14, 16)
    assert left_on_right == ([7, 7, 7, 7], 14, 16)
    assert first_closure_rank(left, i4) == 11
    assert first_closure_rank(right, i4) == 11
    return {
        "right_on_left": right_on_left,
        "left_on_right": left_on_right,
        "closure": (11, 11),
    }


def d6_controlled_calibration() -> dict[str, object]:
    """A standard OSR-four d=6 reflection with full joint-sandwich rank."""
    d = 6
    i6 = sp.eye(d)
    color_sign = sp.diag(1, 1, -1)
    orthogonal = sp.Rational(1, 17) * sp.Matrix(
        [
            [-1, 0, -12, 0, 0, -12],
            [0, 17, 0, 0, 0, 0],
            [-12, 0, 9, 0, 0, -8],
            [0, 0, 0, 17, 0, 0],
            [0, 0, 0, 0, 17, 0],
            [-12, 0, -8, 0, 0, 9],
        ]
    )
    assert orthogonal.T * orthogonal == i6

    raw_right = [
        tensor(X, color_sign),
        tensor(X, I3),
        tensor(Y, I3),
        tensor(Z, I3),
    ]
    right = [
        orthogonal * matrix * orthogonal.T for matrix in raw_right
    ]
    for matrix in right:
        assert dagger(matrix) == matrix
        assert matrix * matrix == i6
        assert sp.trace(matrix) == 0

    left = [
        sp.diag(1, -1, 0, 0, 0, 0),
        sp.diag(0, 0, 1, 1, -1, -1),
        sp.diag(0, 0, 1, -1, 1, -1),
        sp.diag(0, 0, 1, -1, -1, 1),
    ]
    assert all(sp.trace(matrix) == 0 for matrix in left)
    assert hs_gram(left) == sp.diag(2, 4, 4, 4)
    expected_right_gram = sp.Matrix(
        [
            [6, 2, 0, 0],
            [2, 6, 0, 0],
            [0, 0, 6, 0],
            [0, 0, 0, 6],
        ]
    )
    assert hs_gram(right) == expected_right_gram
    assert span_rank(left) == span_rank(right) == 4

    tetrahedral_blocks = [
        right[0],
        -right[0],
        (right[1] + right[2] + right[3]) / sp.sqrt(3),
        (right[1] - right[2] - right[3]) / sp.sqrt(3),
        (-right[1] + right[2] - right[3]) / sp.sqrt(3),
        (-right[1] - right[2] + right[3]) / sp.sqrt(3),
    ]
    for block in tetrahedral_blocks:
        assert dagger(block) == block
        assert is_zero(block * block - i6)

    h_factorized = tensor(left[0], right[0]) + sum(
        (
            tensor(left[index], right[index]) / sp.sqrt(3)
            for index in range(1, 4)
        ),
        sp.zeros(d * d),
    )
    h_controlled = sp.diag(*tetrahedral_blocks)
    assert is_zero(h_factorized - h_controlled)
    assert dagger(h_controlled) == h_controlled
    assert is_zero(h_controlled * h_controlled - sp.eye(d * d))
    assert sp.trace(h_controlled) == 0
    assert is_zero(partial_trace_first(h_controlled, d))
    assert is_zero(partial_trace_second(h_controlled, d))

    right_on_left = sandwich_statistics(right, left, i6)
    left_on_right = sandwich_statistics(left, right, i6)
    assert right_on_left == ([16, 14, 14, 16], 16, 16)
    assert left_on_right == ([15, 15, 12, 11], 16, 16)
    closures = (
        first_closure_rank(left, i6),
        first_closure_rank(right, i6),
    )
    assert closures == (6, 8)

    # Direct exact three-site falsification, compressed to a fixed first
    # control value.  This does not invoke the quotient theorem.
    h23 = h_controlled
    nonzero_certificate = None
    nonzero_block_index = None
    for control, block in enumerate(tetrahedral_blocks):
        h12_on_control = tensor(block, i6)
        residual = (
            h12_on_control * h23 * h12_on_control
            - h23 * h12_on_control * h23
            - sp.Rational(1, 3) * (h12_on_control - h23)
        )
        for row in range(residual.rows):
            for column in range(residual.cols):
                value = sp.simplify(residual[row, column])
                if value != 0:
                    nonzero_block_index = control
                    nonzero_certificate = (
                        row,
                        column,
                        sp.factor(sp.together(value)),
                    )
                    break
            if nonzero_certificate is not None:
                break
        if nonzero_certificate is not None:
            break
    assert nonzero_certificate is not None

    return {
        "right_on_left": right_on_left,
        "left_on_right": left_on_right,
        "closure": closures,
        "residual_control": nonzero_block_index,
        "residual_entry": nonzero_certificate,
    }


def d6_color_calibration() -> dict[str, object]:
    """An exact standard OSR-four d=6 involution with no odd leg atom."""
    d = 6
    i6 = sp.eye(d)
    color_sign = sp.diag(1, 1, -1)
    support = [
        tensor(X, I3),
        tensor(Z, I3),
        tensor(X, color_sign),
        tensor(Z, color_sign),
    ]
    coefficients = [
        -sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
    ]
    h = sum(
        (
            coefficient * tensor(matrix, matrix)
            for coefficient, matrix in zip(coefficients, support)
        ),
        sp.zeros(d * d),
    )
    assert dagger(h) == h
    assert is_zero(h * h - sp.eye(d * d))
    assert sp.trace(h) == 0
    assert is_zero(partial_trace_first(h, d))
    assert is_zero(partial_trace_second(h, d))
    assert span_rank(support) == 4

    expected_gram = sp.Matrix(
        [
            [6, 0, 2, 0],
            [0, 6, 0, 2],
            [2, 0, 6, 0],
            [0, 2, 0, 6],
        ]
    )
    gram = hs_gram(support)
    assert gram == expected_gram

    stats = sandwich_statistics(support, support, i6)
    assert stats == ([4, 4, 4, 4], 4, 8)
    assert first_closure_rank(support, i6) == 8

    # The nonzero singular values of realignment are the absolute
    # eigenvalues of C G for this real symmetric factorization L C L^T.
    coefficient_matrix = sp.diag(*coefficients)
    eigenvalues = coefficient_matrix * gram
    eigenvalue_counter = Counter()
    for eigenvalue, multiplicity in eigenvalues.eigenvals().items():
        eigenvalue_counter[sp.simplify(eigenvalue**2)] += multiplicity
    assert eigenvalue_counter == Counter({sp.Integer(8): 2, 16: 1, 4: 1})

    # Independently assemble every color-sector cubic residual on the
    # three qubits and sum its exact Hilbert--Schmidt norm.
    signs = (1, 1, -1)
    norm_counter: Counter[sp.Rational] = Counter()
    total_norm = sp.Integer(0)
    for first, middle, last in product(range(3), repeat=3):
        if signs[first] == signs[middle]:
            h12 = tensor(Z, Z, I2)
        else:
            h12 = -tensor(X, X, I2)
        if signs[middle] == signs[last]:
            h23 = tensor(I2, Z, Z)
        else:
            h23 = -tensor(I2, X, X)
        residual = (
            h12 * h23 * h12
            - h23 * h12 * h23
            - sp.Rational(1, 3) * (h12 - h23)
        )
        norm = sp.simplify(sp.trace(dagger(residual) * residual))
        norm_counter[norm] += 1
        total_norm += norm
    assert norm_counter == Counter(
        {sp.Rational(256, 9): 15, sp.Rational(64, 9): 12}
    )
    assert total_norm == 512

    return {
        "sandwich": stats,
        "closure": 8,
        "schmidt_squared": dict(eigenvalue_counter),
        "residual_sector_norms": dict(norm_counter),
        "residual_norm_squared": total_norm,
    }


def four_reflection_limitation() -> dict[str, object]:
    """Four orthogonal balanced d=6 reflections outside a Clifford frame."""
    d = 6
    i6 = sp.eye(d)
    first_three = [tensor(X, I3), tensor(Y, I3), tensor(Z, I3)]

    vectors = []
    for color in range(3):
        vector = sp.zeros(d, 1)
        vector[color, 0] = 1 / sp.sqrt(2)
        vector[3 + ((color + 1) % 3), 0] = 1 / sp.sqrt(2)
        vectors.append(vector)
    assert hs_gram(vectors) == sp.eye(3)
    projection = sum(
        (vector * dagger(vector) for vector in vectors), sp.zeros(d)
    )
    assert projection * projection == projection
    assert sp.trace(projection) == 3
    fourth = i6 - 2 * projection
    reflections = first_three + [fourth]

    for reflection in reflections:
        assert dagger(reflection) == reflection
        assert reflection * reflection == i6
        assert sp.trace(reflection) == 0
    assert hs_gram(reflections) == 6 * sp.eye(4)

    pair_status = []
    for reflection in first_three:
        commutes = is_zero(reflection * fourth - fourth * reflection)
        anticommutes = is_zero(reflection * fourth + fourth * reflection)
        pair_status.append((commutes, anticommutes))
    assert any(not commutes and not anticommutes for commutes, anticommutes in pair_status)
    return {"fourth_pair_status": pair_status}


def main() -> None:
    cstar_types = finite_dimensional_cstar_check()
    published = published_d4_rank_calibration()
    c61 = c61_d4_rank_calibration()
    controlled = d6_controlled_calibration()
    color = d6_color_calibration()
    reflections = four_reflection_limitation()

    print("PASS dimension-five C*-types:", cstar_types)
    print(
        "PASS published d4 OSR3 sandwiches:",
        published["right_on_left"],
        published["left_on_right"],
        "closure",
        published["closure"],
    )
    print(
        "PASS C61 d4 OSR4 sandwiches:",
        c61["right_on_left"],
        c61["left_on_right"],
        "closure",
        c61["closure"],
    )
    print(
        "PASS d6 controlled reflection: H*=H, H^2=I, trace and partial traces zero"
    )
    print(
        "PASS d6 controlled sandwiches:",
        controlled["right_on_left"],
        controlled["left_on_right"],
        "closure",
        controlled["closure"],
    )
    print(
        "PASS d6 controlled direct cubic nonzero entry:",
        "control",
        controlled["residual_control"],
        controlled["residual_entry"],
    )
    print(
        "PASS d6 color reflection: H*=H, H^2=I, trace and partial traces zero"
    )
    print(
        "PASS d6 color sandwiches:",
        color["sandwich"],
        "closure",
        color["closure"],
    )
    print(
        "PASS d6 color Schmidt singular values squared:",
        color["schmidt_squared"],
    )
    print(
        "PASS d6 color cubic residual sectors:",
        color["residual_sector_norms"],
        "total",
        color["residual_norm_squared"],
    )
    print(
        "PASS four orthogonal balanced d6 reflections; statuses with U4:",
        reflections["fourth_pair_status"],
    )
    print(
        "THEOREM if either OSR4 joint sandwich map on CI+support is injective, 4|d"
    )
    print(
        "NECESSARY d=2 mod 4 OSR4 candidates have nonzero common annihilators on both legs"
    )
    print("SCOPE unrestricted OSR4 exceptional divisibility remains open")


if __name__ == "__main__":
    main()

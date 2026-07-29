#!/usr/bin/env python3
"""Exact checks for the two-qubit support second-kernel gap."""

from __future__ import annotations

from fractions import Fraction as F


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def frobenius_squared(matrix):
    return sum(value * value for row in matrix for value in row)


def kronecker(left, right):
    return [
        [
            left[i // len(right)][j // len(right[0])]
            * right[i % len(right)][j % len(right[0])]
            for j in range(len(left[0]) * len(right[0]))
        ]
        for i in range(len(left) * len(right))
    ]


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def main() -> None:
    epsilon = [[F(0), F(1)], [F(-1), F(0)]]
    j = [
        [
            epsilon[i // 2][k // 2] * epsilon[i % 2][k % 2]
            for k in range(4)
        ]
        for i in range(4)
    ]
    assert transpose(j) == j
    assert matmul(j, j) == [
        [F(i == k) for k in range(4)] for i in range(4)
    ]
    assert frobenius_squared(j) == 4

    # Verify the skew-plus-scalar identity (12a) on a basis of M_2.
    identity = [[F(1), F(0)], [F(0), F(1)]]
    for row in range(2):
        for column in range(2):
            matrix = [[F(0), F(0)], [F(0), F(0)]]
            matrix[row][column] = F(1)
            left = matmul(kronecker(identity, matrix), j)
            symmetrized = add(left, transpose(left))
            trace = matrix[0][0] + matrix[1][1]
            assert symmetrized == scale(trace, j)

            left = matmul(kronecker(matrix, identity), j)
            symmetrized = add(left, transpose(left))
            assert symmetrized == scale(trace, j)

    # Standard annihilator Lambda=(e1,e2).  A skew matrix is encoded by
    # its six upper-triangular coordinates.  Verify the exact norm
    # ratio in (20).
    for coordinate in range(6):
        pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        skew = [[F(0) for _ in range(4)] for _ in range(4)]
        row, column = pairs[coordinate]
        skew[row][column] = F(1)
        skew[column][row] = F(-1)
        first_two_rows = skew[:2]
        full_norm = frobenius_squared(skew)
        row_norm = frobenius_squared(first_two_rows)
        if (row, column) == (2, 3):
            assert row_norm == 0  # the one-dimensional kernel
        else:
            assert row_norm >= F(1, 2) * full_norm

    # Constants in the two-case estimate.
    assert F(1, 8) >= F(1, 20)
    assert F(1, 20) == F(1, (2 * 2 * 5))
    # The outside-column estimate is
    # lambda_min(T*T) = marginal_min/2 >= mu^2/8.
    assert F(1, 2) * F(1, 4) == F(1, 8)
    # Two-by-two entrywise defect B gives ||K|| <= 2B; combining
    # with lambda_2 >= mu^2/20 gives the constants 40 and 10.
    assert 20 * 2 == 40
    assert F(40, 4) == 10

    print(
        "verified: full qubit-support skew identities, "
        "outside-sector and two-slice constants"
    )


if __name__ == "__main__":
    main()

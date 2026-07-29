#!/usr/bin/env python3
"""Exact checks for the shifted-concurrence bridge.

The checker verifies:

1. the determinant/spin-flip identity used in the Kraus argument;
2. the final quantitative square identity;
3. the exact computational-basis equality Gram matrix.
"""

from fractions import Fraction as F
from itertools import product


def zeros(rows, columns):
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def index(word):
    value = 0
    for digit in word:
        value = 3 * value + digit
    return value


def matrix_unit(row, column):
    out = zeros(3, 3)
    out[row][column] = F(1)
    return out


def kron(left, right):
    out = zeros(
        len(left) * len(right),
        len(left[0]) * len(right[0]),
    )
    for i, j, k, ell in product(
        range(len(left)),
        range(len(left[0])),
        range(len(right)),
        range(len(right[0])),
    ):
        out[i * len(right) + k][j * len(right[0]) + ell] = (
            left[i][j] * right[k][ell]
        )
    return out


def partial_trace(matrix, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(3) if i not in traced)
    remaining_words = list(product(range(3), repeat=len(remaining)))
    traced_words = list(product(range(3), repeat=len(traced)))
    out = zeros(3 ** len(remaining), 3 ** len(remaining))
    for row_index, row_remaining in enumerate(remaining_words):
        for column_index, column_remaining in enumerate(remaining_words):
            value = F(0)
            for trace_word in traced_words:
                row = [0, 0, 0]
                column = [0, 0, 0]
                for position, site in enumerate(remaining):
                    row[site] = row_remaining[position]
                    column[site] = column_remaining[position]
                for position, site in enumerate(traced):
                    row[site] = trace_word[position]
                    column[site] = trace_word[position]
                value += matrix[index(row)][index(column)]
            out[row_index][column_index] = value
    return out


def hs_inner(left, right):
    return sum(
        left[i][j] * right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    )


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def pair_inner(left, right):
    value = F(0)
    for site in range(3):
        value += F(1, 3) * hs_inner(
            partial_trace(left, (site,)),
            partial_trace(right, (site,)),
        )
        complement = tuple(i for i in range(3) if i != site)
        value -= F(2, 9) * hs_inner(
            partial_trace(left, complement),
            partial_trace(right, complement),
        )
    value += F(1, 9) * trace(left) * trace(right)
    return value


def dyad(row_word, column_word):
    out = zeros(27, 27)
    out[index(row_word)][index(column_word)] = F(1)
    return out


def main():
    # z^T (epsilon tensor epsilon) z = 2 det(M), in row-major
    # vectorization z=(m00,m01,m10,m11).
    m00, m01, m10, m11 = F(2), F(3), F(5), F(7)
    epsilon = [[F(0), F(1)], [F(-1), F(0)]]
    spin_flip = [
        [
            epsilon[i // 2][j // 2] * epsilon[i % 2][j % 2]
            for j in range(4)
        ]
        for i in range(4)
    ]
    z = [m00, m01, m10, m11]
    bilinear = sum(
        z[i] * spin_flip[i][j] * z[j]
        for i in range(4)
        for j in range(4)
    )
    determinant = m00 * m11 - m01 * m10
    assert bilinear == 2 * determinant
    assert m01 * m10 == m00 * m11 - determinant

    # If p=a^2 and q=b^2, inserting the shifted Gram bound into
    # the rank-two quadratic form leaves exactly one square.
    s1, s2, a, b = F(7), F(4), F(3), F(2)
    mu = F(4, 9)
    g11 = mu - a * a
    g22 = mu - b * b
    cross_bound = F(2, 9) + a * b
    pair_value = (
        s1 * s1 * g11
        + s2 * s2 * g22
        + 2 * s1 * s2 * cross_bound
    )
    target = mu * (s1 * s1 + s2 * s2 + s1 * s2)
    assert target - pair_value == (s1 * a - s2 * b) ** 2

    # Exact product-saturation equality from the note.
    e1 = dyad((0, 0, 0), (1, 0, 0))
    e2 = dyad((0, 1, 1), (1, 1, 1))
    gram = [
        [pair_inner(e1, e1), pair_inner(e1, e2)],
        [pair_inner(e2, e1), pair_inner(e2, e2)],
    ]
    assert gram == [
        [F(4, 9), F(-2, 9)],
        [F(-2, 9), F(4, 9)],
    ]

    # The older sharp feature state is the unequal-slack equality:
    # p=q=1/9 and |G12|=1/3=2/9+sqrt(pq).
    p = q = F(1, 9)
    assert F(1, 3) == F(2, 9) + p

    print(
        "verified: determinant bridge, quantitative square, and "
        "exact shifted-Gram boundary equality"
    )


if __name__ == "__main__":
    main()

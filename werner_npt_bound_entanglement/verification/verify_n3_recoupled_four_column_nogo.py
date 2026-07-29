#!/usr/bin/env python3
"""Exact dependency-free check of the four-column rank-two no-go."""

from fractions import Fraction as Q
from itertools import product


D = 3
N = D**3
OP = N * N


def digits(number):
    out = []
    for _ in range(3):
        out.append(number % D)
        number //= D
    return tuple(out)


def index(word):
    return word[0] + D * word[1] + D * D * word[2]


def zero_operator():
    return [[Q(0) for _ in range(N)] for _ in range(N)]


def basis_operator(row, column, sign=1):
    out = zero_operator()
    out[row][column] = Q(sign)
    return out


def add(first, second, scale=Q(1)):
    return [
        [
            first[row][column] + scale * second[row][column]
            for column in range(len(first[0]))
        ]
        for row in range(len(first))
    ]


def scalar_part(matrix, site):
    out = zero_operator()
    place = D**site
    for row in range(N):
        row_digit = (row // place) % D
        base_row = row - row_digit * place
        for column in range(N):
            if (column // place) % D != row_digit:
                continue
            base_column = column - row_digit * place
            out[row][column] = sum(
                matrix[base_row + value * place][
                    base_column + value * place
                ]
                for value in range(D)
            ) / D
    return out


def exact_sector(matrix, traceless_mask):
    out = matrix
    for site in range(3):
        scalar = scalar_part(out, site)
        out = (
            add(out, scalar, Q(-1))
            if (traceless_mask >> site) & 1
            else scalar
        )
    return out


def apply_z(matrix):
    out = [[Q(2) * value for value in row] for row in matrix]
    for mask in (3, 5, 6):
        out = add(out, exact_sector(matrix, mask), Q(-3))
    return out


def inner(first, second):
    return sum(
        first[row][column] * second[row][column]
        for row in range(N)
        for column in range(N)
    )


def gram(left, right):
    images = [apply_z(vector) for vector in right]
    return [
        [inner(vector, image) for image in images]
        for vector in left
    ]


def matrix_product(first, second):
    size = len(first)
    return [
        [
            sum(first[i][k] * second[k][j] for k in range(size))
            for j in range(size)
        ]
        for i in range(size)
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def norm_squared(matrix):
    return sum(value * value for row in matrix for value in row)


def rational_rank(matrix):
    work = [[Q(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    work[row][j] - scale * work[pivot_row][j]
                    for j in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def kron(first, second):
    return [
        [
            first[i][j] * second[k][l]
            for j in range(len(first[0]))
            for l in range(len(second[0]))
        ]
        for i in range(len(first))
        for k in range(len(second))
    ]


def swap(word, first, second):
    out = list(word)
    out[first], out[second] = out[second], out[first]
    return tuple(out)


def move(word, first_vertical, second_vertical, crossed):
    if crossed:
        word = swap(word, 2, 3)
    if second_vertical:
        word = swap(word, 1, 3)
    if first_vertical:
        word = swap(word, 0, 2)
    if crossed:
        word = swap(word, 0, 1)
    return word


def local_table(left, right, crossed):
    state = {
        (a, b, c, d): x * y
        for (a, b), x in left.items()
        for (c, d), y in right.items()
    }
    norm = sum(value * value for value in state.values())
    return {
        (first, second): sum(
            value * state.get(
                move(word, first, second, crossed), Q(0)
            )
            for word, value in state.items()
        )
        / norm
        for first, second in product((0, 1), repeat=2)
    }


COEFFICIENT = (Q(2), Q(-1), Q(2, 3), Q(-1, 3))


def contraction(tables):
    value = Q(0)
    for first_mask in range(8):
        for second_mask in range(8):
            term = (
                COEFFICIENT[bin(first_mask).count("1")]
                * COEFFICIENT[bin(second_mask).count("1")]
            )
            for site in range(3):
                term *= tables[site][
                    (
                        (first_mask >> site) & 1,
                        (second_mask >> site) & 1,
                    )
                ]
            value += term
    return value


def main():
    # The four singular-frame columns.  Signs realize
    # A=E01 x E00 x diag(-1,1,0), B=E01 x E11 x diag(1,1,0).
    x = [
        (index((0, 0, 0)), 1),
        (index((0, 0, 1)), -1),
    ]
    y = [
        (index((1, 0, 0)), -1),
        (index((1, 0, 1)), -1),
    ]
    u = [
        (index((0, 1, 0)), -1),
        (index((0, 1, 1)), -1),
    ]
    v = [
        (index((1, 1, 0)), -1),
        (index((1, 1, 1)), -1),
    ]
    e_columns = []
    f_columns = []
    for i, j in product(range(2), repeat=2):
        e_columns.append(
            basis_operator(x[i][0], u[j][0], x[i][1] * u[j][1])
        )
        f_columns.append(
            basis_operator(y[i][0], v[j][0], y[i][1] * v[j][1])
        )

    ge = gram(e_columns, e_columns)
    gf = gram(f_columns, f_columns)
    h = gram(e_columns, f_columns)
    expected_ge = [
        [Q(2, 3), 0, 0, Q(1, 3)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [Q(1, 3), 0, 0, Q(2, 3)],
    ]
    expected_gf = [
        [Q(2, 3), 0, 0, Q(-1, 3)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [Q(-1, 3), 0, 0, Q(2, 3)],
    ]
    expected_h = [
        [Q(1, 3), 0, 0, Q(-2, 3)],
        [0, 1, 0, 0],
        [0, 0, -1, 0],
        [Q(2, 3), 0, 0, Q(-1, 3)],
    ]
    assert ge == expected_ge
    assert gf == expected_gf
    assert h == expected_h

    gram_term = trace(matrix_product(ge, gf))
    cross_norm = norm_squared(h)
    difference = add(h, transpose(h), Q(-1))
    antisymmetric_compensation = norm_squared(difference) / 2
    assert gram_term == Q(8, 3)
    assert cross_norm == Q(28, 9)
    assert gram_term - cross_norm == Q(-4, 9)
    assert antisymmetric_compensation == Q(16, 9)
    assert gram_term - cross_norm + antisymmetric_compensation == Q(4, 3)

    zero = Q(0)
    e01 = [[zero for _ in range(3)] for _ in range(3)]
    e00 = [[zero for _ in range(3)] for _ in range(3)]
    e11 = [[zero for _ in range(3)] for _ in range(3)]
    diagonal_minus = [[zero for _ in range(3)] for _ in range(3)]
    projection_two = [[zero for _ in range(3)] for _ in range(3)]
    e01[0][1] = 1
    e00[0][0] = 1
    e11[1][1] = 1
    diagonal_minus[0][0] = -1
    diagonal_minus[1][1] = 1
    projection_two[0][0] = projection_two[1][1] = 1
    matrix_a = kron(kron(e01, e00), diagonal_minus)
    matrix_b = kron(kron(e01, e11), projection_two)
    assert rational_rank(matrix_a) == 2
    assert rational_rank(matrix_b) == 2
    assert norm_squared(matrix_a) == norm_squared(matrix_b) == 2

    left = (
        {(0, 1): Q(1)},
        {(0, 0): Q(1)},
        {(0, 0): Q(-1), (1, 1): Q(1)},
    )
    right = (
        {(0, 1): Q(1)},
        {(1, 1): Q(1)},
        {(0, 0): Q(1), (1, 1): Q(1)},
    )
    direct = [
        local_table(a, b, False) for a, b in zip(left, right)
    ]
    crossed = [
        local_table(a, b, True) for a, b in zip(left, right)
    ]
    normalized_direct_check = contraction(direct) - contraction(crossed)
    assert normalized_direct_check == Q(1, 3)
    assert Q(4) * normalized_direct_check == Q(4, 3)

    print(
        "verified: ranks=(2,2), stronger Gram residual=-4/9, "
        "antisymmetric compensation=16/9, recoupled value=4/3"
    )


if __name__ == "__main__":
    main()

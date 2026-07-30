#!/usr/bin/env python3
"""Exact checker for the rank-two nilpotent exterior counterexample."""

from itertools import product


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def neg(value):
    return -value[0], -value[1]


def mul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value):
    return value[0], -value[1]


def norm_squared(value):
    return value[0] ** 2 + value[1] ** 2


ZERO = (0, 0)


def inner(left, right, first, second):
    value = ZERO
    for row in range(len(left)):
        value = add(
            value,
            mul(conjugate(left[row][first]), right[row][second]),
        )
    return value


def matrix_product(left, right):
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    assert len(left[0]) == middle
    answer = [[ZERO for _ in range(columns)] for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            value = ZERO
            for index in range(middle):
                value = add(
                    value, mul(left[row][index], right[index][column])
                )
            answer[row][column] = value
    return answer


def determinant_two(matrix):
    return add(
        mul(matrix[0][0], matrix[1][1]),
        neg(mul(matrix[0][1], matrix[1][0])),
    )


def gram_determinant(matrix):
    diagonal_zero = inner(matrix, matrix, 0, 0)
    diagonal_one = inner(matrix, matrix, 1, 1)
    off_diagonal = inner(matrix, matrix, 0, 1)
    assert diagonal_zero[1] == diagonal_one[1] == 0
    return (
        diagonal_zero[0] * diagonal_one[0]
        - norm_squared(off_diagonal)
    )


Y = [
    [(1, 7), (8, -4)],
    [(-2, -6), (1, -1)],
    [(4, 6), (0, 1)],
    [(-4, -4), (1, -2)],
    [(1, -7), (1, 0)],
    [(0, 6), (-3, 1)],
    [(-2, -5), (2, -1)],
    [(1, 3), (0, -1)],
]

X_ZERO = [
    [(5, 4), (1, -1)],
    [(-2, 0), (0, 1)],
    [(2, 0), (-1, -1)],
    [(5, 0), (-1, -4)],
    [(-1, -1), (0, 1)],
    [(-3, -4), (-2, 3)],
    [(4, 3), (1, -4)],
    [(-13, -4), (0, -6)],
]

G = [
    [(-40, 20), (10, 20)],
    [(40, 80), (40, -20)],
]

H = [[(299, 0), (-1, 0)], [(-1, 0), (105, 0)]]
ADJUGATE_H = [[(105, 0), (1, 0)], [(1, 0), (299, 0)]]
DET_H = 31394

computed_h = [
    [inner(Y, Y, row, column) for column in range(2)]
    for row in range(2)
]
computed_k = [
    [inner(Y, X_ZERO, row, column) for column in range(2)]
    for row in range(2)
]
assert computed_h == H
assert computed_k == [
    [(-41, 24), (9, 24)],
    [(40, 69), (38, -21)],
]
assert add(G[0][0], G[1][1]) == ZERO
assert determinant_two(G) == ZERO
assert matrix_product(G, G) == [[ZERO, ZERO], [ZERO, ZERO]]

delta = [
    [add(G[row][column], neg(computed_k[row][column]))
     for column in range(2)]
    for row in range(2)
]
correction = matrix_product(Y, matrix_product(ADJUGATE_H, delta))
X = [
    [
        add(
            (DET_H * X_ZERO[row][column][0],
             DET_H * X_ZERO[row][column][1]),
            correction[row][column],
        )
        for column in range(2)
    ]
    for row in range(8)
]

logical_overlap = [
    [inner(Y, X, row, column) for column in range(2)]
    for row in range(2)
]
assert logical_overlap == [
    [
        (DET_H * G[row][column][0],
         DET_H * G[row][column][1])
        for column in range(2)
    ]
    for row in range(2)
]
assert logical_overlap != [[ZERO, ZERO], [ZERO, ZERO]]
assert add(logical_overlap[0][0], logical_overlap[1][1]) == ZERO
assert determinant_two(logical_overlap) == ZERO
assert matrix_product(logical_overlap, logical_overlap) == [
    [ZERO, ZERO],
    [ZERO, ZERO],
]

det_x = gram_determinant(X)
det_y = gram_determinant(Y)
assert det_x == 28330741506297369413120
assert det_y == 31394
assert det_x > 0 and det_y > 0

BINARY_INDICES = (0, 1, 3, 4, 9, 10, 12, 13)
full_x = [[ZERO, ZERO] for _ in range(27)]
full_y = [[ZERO, ZERO] for _ in range(27)]
for row, index in enumerate(BINARY_INDICES):
    full_x[index] = X[row]
    full_y[index] = Y[row]

C = [[ZERO for _ in range(27)] for _ in range(27)]
for row in range(27):
    for column in range(27):
        C[row][column] = add(
            mul(full_x[row][0], conjugate(full_y[column][0])),
            mul(full_x[row][1], conjugate(full_y[column][1])),
        )


def tensor_index(digits):
    return 9 * digits[0] + 3 * digits[1] + digits[2]


def partial_trace_norm_squared(traced):
    remaining = tuple(site for site in range(3) if site not in traced)
    total = 0
    for row_remaining in product(range(3), repeat=len(remaining)):
        for column_remaining in product(range(3), repeat=len(remaining)):
            value = ZERO
            for common in product(range(3), repeat=len(traced)):
                row = [0, 0, 0]
                column = [0, 0, 0]
                for offset, site in enumerate(remaining):
                    row[site] = row_remaining[offset]
                    column[site] = column_remaining[offset]
                for offset, site in enumerate(traced):
                    row[site] = common[offset]
                    column[site] = common[offset]
                value = add(
                    value, C[tensor_index(row)][tensor_index(column)]
                )
            total += norm_squared(value)
    return total


normal = sum(norm_squared(value) for row in C for value in row)
single = sum(partial_trace_norm_squared((site,)) for site in range(3))
pair = sum(
    partial_trace_norm_squared(sites)
    for sites in ((0, 1), (0, 2), (1, 2))
)
trace = partial_trace_norm_squared((0, 1, 2))

assert normal == 105262033353136
assert single == 230674647423880
assert pair == 84535625654192
assert trace == 0

linear_part = 3 * normal - 2 * single + pair
singular_product_squared = det_x * det_y
assert linear_part == -61027569134160
assert singular_product_squared == 889415298848699615355489280
assert (
    linear_part * linear_part - 4 * singular_product_squared
    == 166702999029879870656948480
)
assert linear_part < 0
assert linear_part * linear_part > 4 * singular_product_squared

eight_q = 8 * normal - 4 * single + 2 * pair - trace
assert eight_q == 88468928437952
assert eight_q > 0

print("verified: rank-two nilpotent exterior counterexample")
print("verified: C^3=0, C^2!=0 through the nonzero square-zero overlap")
print("verified: endpoint value remains positive")

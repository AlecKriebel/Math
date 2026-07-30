#!/usr/bin/env python3
"""Exact checker for the hard-region radical-free counterexample.

Only Gaussian-integer arithmetic from the Python standard library is
used.  The binary support is canonically embedded in three qutrits.
"""

from __future__ import annotations

from itertools import combinations

GI = tuple[int, int]
Matrix = list[list[GI]]


def add(left: GI, right: GI) -> GI:
    return left[0] + right[0], left[1] + right[1]


def sub(left: GI, right: GI) -> GI:
    return left[0] - right[0], left[1] - right[1]


def mul(left: GI, right: GI) -> GI:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conjugate(value: GI) -> GI:
    return value[0], -value[1]


def zeros(rows: int, columns: int) -> Matrix:
    return [[(0, 0) for _ in range(columns)] for _ in range(rows)]


def dagger(matrix: Matrix) -> Matrix:
    return [
        [conjugate(matrix[column][row]) for column in range(len(matrix))]
        for row in range(len(matrix[0]))
    ]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    out = zeros(len(left), len(right[0]))
    for row in range(len(left)):
        for column in range(len(right[0])):
            for middle in range(len(right)):
                out[row][column] = add(
                    out[row][column],
                    mul(left[row][middle], right[middle][column]),
                )
    return out


def determinant_2(matrix: Matrix) -> GI:
    return sub(
        mul(matrix[0][0], matrix[1][1]),
        mul(matrix[0][1], matrix[1][0]),
    )


def norm_squared(value: GI) -> int:
    return value[0] * value[0] + value[1] * value[1]


def hs_norm_squared(matrix: Matrix) -> int:
    return sum(norm_squared(value) for row in matrix for value in row)


def trace(matrix: Matrix) -> GI:
    out = (0, 0)
    for index in range(len(matrix)):
        out = add(out, matrix[index][index])
    return out


def digits(index: int, sites: tuple[int, ...]) -> list[int]:
    out = [0, 0, 0]
    for site in reversed(sites):
        out[site] = index % 2
        index //= 2
    return out


def partial_trace(matrix: Matrix, traced: tuple[int, ...]) -> Matrix:
    remaining = tuple(site for site in range(3) if site not in traced)
    size = 2 ** len(remaining)
    out = zeros(size, size)
    for output_row in range(size):
        row = digits(output_row, remaining)
        for output_column in range(size):
            column = digits(output_column, remaining)
            for trace_index in range(2 ** len(traced)):
                traced_digits = digits(trace_index, traced)
                full_row = row.copy()
                full_column = column.copy()
                for site in traced:
                    full_row[site] = traced_digits[site]
                    full_column[site] = traced_digits[site]
                matrix_row = (
                    4 * full_row[0] + 2 * full_row[1] + full_row[2]
                )
                matrix_column = (
                    4 * full_column[0]
                    + 2 * full_column[1]
                    + full_column[2]
                )
                out[output_row][output_column] = add(
                    out[output_row][output_column],
                    matrix[matrix_row][matrix_column],
                )
    return out


X: Matrix = [
    [(30, -68), (20, 0)],
    [(-4, -4), (-29, 15)],
    [(18, 59), (60, -27)],
    [(21, 6), (-7, 17)],
    [(28, -108), (12, -33)],
    [(54, 100), (61, 54)],
    [(37, 99), (61, -60)],
    [(-104, -73), (29, 74)],
]

Y: Matrix = [
    [(62, -80), (47, -67)],
    [(-74, 20), (-28, -36)],
    [(-49, 106), (42, -61)],
    [(34, -30), (-63, -24)],
    [(66, 47), (27, 12)],
    [(73, -74), (29, 1)],
    [(-84, -9), (25, 33)],
    [(-16, 84), (66, -13)],
]

gram_x = matmul(dagger(X), X)
gram_y = matmul(dagger(Y), Y)

assert gram_x == [
    [(62517, 0), (591, -19093)],
    [(591, 19093), (27641, 0)],
]
assert gram_y == [
    [(63632, 0), (-476, -7480)],
    [(-476, 7480), (26762, 0)],
]

det_x = determinant_2(gram_x)
det_y = determinant_2(gram_y)
assert det_x == (1363140467, 0)
assert det_y == (1646742608, 0)
assert det_x[0] > 0 and det_y[0] > 0

C = matmul(X, dagger(Y))
N = hs_norm_squared(C)
S = sum(hs_norm_squared(partial_trace(C, (site,))) for site in range(3))
P = sum(
    hs_norm_squared(partial_trace(C, pair))
    for pair in combinations(range(3), 2)
)
A = 3 * N - 2 * S + P

assert N == 5002878834
assert S == 11103088421
assert P == 4142165753
assert A == -3055374587

D_squared = det_x[0] * det_y[0]
T_squared = hs_norm_squared(matmul(C, C))
assert D_squared == 2244741487697917936
assert T_squared == 88764941278788546

numerator = A * A - 4 * D_squared
certificate = numerator - 4 * T_squared
assert numerator == 356347916093748825
assert certificate == 1288150978594641
assert certificate > 0

trace_squared = norm_squared(trace(C))
eight_q3 = 8 * N - 4 * S + 2 * P - trace_squared
assert trace_squared == 42710042
assert eight_q3 == 3852298452
assert eight_q3 > 0

print("verified exact hard-region counterexample to A^2 <= 4D^2+4T^2")
print("A =", A)
print("D^2 =", D_squared)
print("T^2 =", T_squared)
print("A^2-4D^2-4T^2 =", certificate)
print("8 Q3 =", eight_q3)

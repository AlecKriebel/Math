#!/usr/bin/env python3
"""Exact replay of the nilpotent principal-overlap counterexample.

Only Gaussian-integer arithmetic is used until the final rational
principal-angle quotient.  No third-party package is required.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

GI = tuple[int, int]
Matrix = list[list[GI]]


def add(x: GI, y: GI) -> GI:
    return x[0] + y[0], x[1] + y[1]


def neg(x: GI) -> GI:
    return -x[0], -x[1]


def sub(x: GI, y: GI) -> GI:
    return add(x, neg(y))


def mul(x: GI, y: GI) -> GI:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def conj(x: GI) -> GI:
    return x[0], -x[1]


def scale(k: int, x: GI) -> GI:
    return k * x[0], k * x[1]


def zeros(rows: int, columns: int) -> Matrix:
    return [[(0, 0) for _ in range(columns)] for _ in range(rows)]


def dagger(a: Matrix) -> Matrix:
    return [[conj(a[j][i]) for j in range(len(a))] for i in range(len(a[0]))]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    out = zeros(len(a), len(b[0]))
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                out[i][j] = add(out[i][j], mul(a[i][k], b[k][j]))
    return out


def matrix_sum(*matrices: Matrix) -> Matrix:
    out = zeros(len(matrices[0]), len(matrices[0][0]))
    for matrix in matrices:
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                out[i][j] = add(out[i][j], matrix[i][j])
    return out


def matrix_scale(k: int, matrix: Matrix) -> Matrix:
    return [[scale(k, entry) for entry in row] for row in matrix]


def determinant_2(matrix: Matrix) -> GI:
    return sub(
        mul(matrix[0][0], matrix[1][1]),
        mul(matrix[0][1], matrix[1][0]),
    )


def adjugate_2(matrix: Matrix) -> Matrix:
    return [
        [matrix[1][1], neg(matrix[0][1])],
        [neg(matrix[1][0]), matrix[0][0]],
    ]


def trace(matrix: Matrix) -> GI:
    answer = (0, 0)
    for i in range(len(matrix)):
        answer = add(answer, matrix[i][i])
    return answer


def norm_squared(x: GI) -> int:
    return x[0] * x[0] + x[1] * x[1]


def hs_norm_squared(matrix: Matrix) -> int:
    return sum(norm_squared(entry) for row in matrix for entry in row)


def digits(index: int, sites: tuple[int, ...]) -> list[int]:
    answer = [0, 0, 0]
    for site in reversed(sites):
        answer[site] = index % 2
        index //= 2
    return answer


def partial_trace(matrix: Matrix, traced: tuple[int, ...]) -> Matrix:
    remaining = tuple(i for i in range(3) if i not in traced)
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
                matrix_row = 4 * full_row[0] + 2 * full_row[1] + full_row[2]
                matrix_column = (
                    4 * full_column[0] + 2 * full_column[1] + full_column[2]
                )
                out[output_row][output_column] = add(
                    out[output_row][output_column],
                    matrix[matrix_row][matrix_column],
                )
    return out


X: Matrix = [
    [(15, 11), (1, 2)],
    [(-5, -1), (0, 5)],
    [(5, 0), (-2, -5)],
    [(12, 1), (-3, -10)],
    [(-4, -3), (-2, 5)],
    [(-7, -9), (-5, 10)],
    [(10, 6), (2, -11)],
    [(-30, -10), (-2, -15)],
]

Z: Matrix = [
    [(2, 19), (20, -11)],
    [(-6, -16), (4, -4)],
    [(10, 13), (-2, 5)],
    [(-9, -9), (3, -4)],
    [(2, -16), (5, -2)],
    [(0, 13), (-5, 1)],
    [(-4, -12), (4, -2)],
    [(3, 9), (4, -7)],
]

a = (8, 5)
b = (8, -15)
G0: Matrix = [
    [neg(mul(a, b)), mul(a, a)],
    [neg(mul(b, b)), mul(a, b)],
]

assert trace(G0) == (0, 0)
assert determinant_2(G0) == (0, 0)
assert G0 != zeros(2, 2)

A = matmul(dagger(X), X)
det_a = determinant_2(A)
assert det_a == (1232663, 0)
delta = det_a[0]
adj_a = adjugate_2(A)
cross = matmul(dagger(X), Z)

Y = matrix_sum(
    matmul(matmul(X, adj_a), dagger(G0)),
    matrix_scale(delta, Z),
    matrix_scale(-1, matmul(matmul(X, adj_a), cross)),
)

expected_Y: Matrix = [
    [(2796130, 23291231), (24762449, -13947340)],
    [(-7440040, -19477708), (5034703, -4730775)],
    [(12287826, 15775869), (-2625444, 6002621)],
    [(-11107921, -11621731), (3394987, -5316298)],
    [(2327306, -19505990), (6181213, -2235678)],
    [(-355208, 16421493), (-6215262, 1717644)],
    [(-4707786, -15290448), (4823441, -2953433)],
    [(3234015, 11074667), (4790609, -8176340)],
]
assert Y == expected_Y

G = matmul(dagger(Y), X)
assert G == matrix_scale(delta, G0)
assert trace(G) == (0, 0)
assert determinant_2(G) == (0, 0)
assert G != zeros(2, 2)

B = matmul(dagger(Y), Y)
det_b = determinant_2(B)
assert det_b == (3069052087197770664967749903517, 0)
assert det_b[0] > 0

C = matmul(X, dagger(Y))
N = hs_norm_squared(C)
S = sum(hs_norm_squared(partial_trace(C, (i,))) for i in range(3))
P = sum(
    hs_norm_squared(partial_trace(C, pair))
    for pair in combinations(range(3), 2)
)

assert N == 5687218642840734153
assert S == 11750875477966803914
assert P == 2477784354164963891

rational_part = 3 * N - 2 * S + P
assert rational_part == -3962310673246441478

D_squared = delta * det_b[0]
assert D_squared == 3783106952961465581191141499318975771

# kappa = Tr(A^{-1} G^* B^{-1} G).  Keep inverses cleared.
adj_b = adjugate_2(B)
kappa_cleared = trace(
    matmul(matmul(matmul(adj_a, dagger(G)), adj_b), G)
)
assert kappa_cleared[1] == 0
kappa_numerator = kappa_cleared[0]
kappa_denominator = D_squared
kappa = Fraction(kappa_numerator, kappa_denominator)
assert kappa == Fraction(
    491280799491106687496457081302285190,
    3783106952961465581191141499318975771,
)
assert kappa > 0

# The corrected expression is
#   rational_part + sqrt(D_squared) * (2 + kappa/4).
# Since rational_part < 0, it is negative exactly when the following
# cleared square difference is positive.
coefficient = 2 + kappa / 4
certificate = (
    rational_part * rational_part * coefficient.denominator**2
    - D_squared * coefficient.numerator**2
)
assert certificate == int(
    "1178385817096270686310864285696206375051688931213891192722859855833435685"
)
assert certificate > 0

print(
    "verified exact rank-two nilpotent-overlap counterexample: "
    "Tr G = det G = 0, G != 0, and the D*kappa/4 correction fails"
)

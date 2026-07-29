#!/usr/bin/env python3
"""Exact replay of the positive-definite crossed-Hodge counterexample."""

from fractions import Fraction as Q


def zeros(rows: int, columns: int) -> list[list[Q]]:
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def transpose(a: list[list[Q]]) -> list[list[Q]]:
    return [list(row) for row in zip(*a)]


def multiply(a: list[list[Q]], b: list[list[Q]]) -> list[list[Q]]:
    bt = transpose(b)
    return [
        [sum(x * y for x, y in zip(row, column)) for column in bt]
        for row in a
    ]


def determinant(a: list[list[Q]]) -> Q:
    work = [row[:] for row in a]
    value = Q(1)
    for column in range(len(work)):
        pivot = next(
            row
            for row in range(column, len(work))
            if work[row][column]
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        diagonal = work[column][column]
        value *= diagonal
        for row in range(column + 1, len(work)):
            ratio = work[row][column] / diagonal
            for entry in range(column, len(work)):
                work[row][entry] -= ratio * work[column][entry]
    return value


def state_index(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


left = zeros(27, 2)
right = zeros(27, 2)
left[state_index(2, 1, 1)][0] = 1
left[state_index(2, 1, 2)][0] = -1
left[state_index(0, 1, 2)][1] = -1
left[state_index(1, 0, 0)][1] = -1
left[state_index(2, 0, 1)][1] = Q(1, 2)
right[state_index(0, 1, 1)][0] = -1
right[state_index(2, 1, 1)][0] = -1
right[state_index(0, 1, 1)][1] = -1
right[state_index(1, 0, 0)][1] = 1
right[state_index(2, 2, 1)][1] = Q(-1, 4)

# Both factor pairs are visibly independent.  The nonzero 2 by 2
# minors below make this an exact mechanical check.
assert determinant(
    [
        [left[state_index(2, 1, 1)][0], left[state_index(2, 1, 1)][1]],
        [left[state_index(0, 1, 2)][0], left[state_index(0, 1, 2)][1]],
    ]
) == -1
assert determinant(
    [
        [right[state_index(2, 1, 1)][0], right[state_index(2, 1, 1)][1]],
        [right[state_index(1, 0, 0)][0], right[state_index(1, 0, 0)][1]],
    ]
) == -1

coefficient = multiply(left, transpose(right))


def block(a: int, p: int) -> list[list[Q]]:
    return [
        [coefficient[9 * a + row][9 * p + column] for column in range(9)]
        for row in range(9)
    ]


def partial_trace(a: list[list[Q]], site: int) -> list[list[Q]]:
    out = zeros(3, 3)
    if site == 0:
        for j in range(3):
            for ell in range(3):
                out[j][ell] = sum(
                    a[3 * i + j][3 * i + ell] for i in range(3)
                )
    else:
        for i in range(3):
            for k in range(3):
                out[i][k] = sum(
                    a[3 * i + j][3 * k + j] for j in range(3)
                )
    return out


def hs(a: list[list[Q]], b: list[list[Q]]) -> Q:
    return sum(
        a[row][column] * b[row][column]
        for row in range(len(a))
        for column in range(len(a[0]))
    )


def trace(a: list[list[Q]]) -> Q:
    return sum(a[i][i] for i in range(len(a)))


def b2(a: list[list[Q]], b: list[list[Q]]) -> Q:
    return (
        hs(a, b)
        - (
            hs(partial_trace(a, 0), partial_trace(b, 0))
            + hs(partial_trace(a, 1), partial_trace(b, 1))
        )
        / 2
        + trace(a) * trace(b) / 4
    )


blocks = [block(a, p) for a in range(3) for p in range(3)]
beta = [
    [b2(blocks[row], blocks[column]) for column in range(9)]
    for row in range(9)
]

expected_scaled_beta = [
    [64, 0, 0, 0, 0, 0, 64, 0, 64],
    [0, 128, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 128, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 32, 0, 32, 0, 32],
    [0, 0, 0, 0, 0, 8, 0, 0, 0],
    [64, 0, 0, 0, 32, 0, 112, 0, 96],
    [0, 0, 0, 0, 0, 0, 0, 16, 0],
    [64, 0, 0, 0, 32, 0, 96, 0, 97],
]
assert [[128 * x for x in row] for row in beta] == expected_scaled_beta

leading_minors = [
    determinant([row[:size] for row in beta[:size]])
    for size in range(1, 10)
]
assert leading_minors == [
    Q(1, 2),
    Q(1, 2),
    Q(1, 32),
    Q(1, 32),
    Q(1, 128),
    Q(1, 2048),
    Q(1, 16384),
    Q(1, 131072),
    Q(1, 16777216),
]
assert all(value > 0 for value in leading_minors)


def partial_transpose_beta(a: list[list[Q]]) -> list[list[Q]]:
    out = zeros(9, 9)
    for left_a in range(3):
        for right_p in range(3):
            for left_b in range(3):
                for right_q in range(3):
                    out[3 * left_a + right_p][3 * left_b + right_q] = (
                        a[3 * left_a + right_q][3 * left_b + right_p]
                    )
    return out


pt_beta = partial_transpose_beta(beta)
hodge = zeros(9, 3)
for column, (a, p) in enumerate(((0, 1), (0, 2), (1, 2))):
    # We omit 1/sqrt(2) here and divide the compression by two.
    hodge[3 * a + p][column] = 1
    hodge[3 * p + a][column] = -1
hodge_compression = multiply(transpose(hodge), multiply(pt_beta, hodge))
hodge_compression = [
    [entry / 2 for entry in row] for row in hodge_compression
]
assert hodge_compression == [
    [1, 0, Q(1, 8)],
    [0, Q(-1, 32), 0],
    [Q(1, 8), 0, Q(-5, 32)],
]

# One negative eigenvalue is explicit.  The complementary 2 by 2 block
# has negative determinant and hence exactly one further negative root.
assert hodge_compression[1][1] < 0
corner = [
    [hodge_compression[0][0], hodge_compression[0][2]],
    [hodge_compression[2][0], hodge_compression[2][2]],
]
assert determinant(corner) == Q(-11, 64)

# Exact minimal-polynomial replay:
#   (32 K + I)(64 K^2 - 54 K - 11 I) = 0.
identity3 = zeros(3, 3)
for i in range(3):
    identity3[i][i] = 1
k_squared = multiply(hodge_compression, hodge_compression)
linear_factor = [
    [
        32 * hodge_compression[i][j] + identity3[i][j]
        for j in range(3)
    ]
    for i in range(3)
]
quadratic_factor = [
    [
        64 * k_squared[i][j]
        - 54 * hodge_compression[i][j]
        - 11 * identity3[i][j]
        for j in range(3)
    ]
    for i in range(3)
]
assert multiply(linear_factor, quadratic_factor) == zeros(3, 3)
assert linear_factor != zeros(3, 3)
assert quadratic_factor != zeros(3, 3)

beta_trace = trace(beta)
identity = [Q(1) if i in (0, 4, 8) else Q(0) for i in range(9)]
identity_overlap = sum(
    identity[i] * beta[i][j] * identity[j]
    for i in range(9)
    for j in range(9)
)
q3 = beta_trace - identity_overlap / 2
assert beta_trace == Q(593, 128)
assert identity_overlap == Q(385, 128)
assert q3 == Q(801, 256) > 0

print("verified rank(C)=2 from independent thin factors")
print("verified beta is positive definite by nine exact leading minors")
print("verified crossed Hodge compression has exactly two negative directions")
print("verified exact cubic minimal-polynomial identity for the compression")
print("verified Q3(C)=801/256>0, so this is only an intermediate obstruction")

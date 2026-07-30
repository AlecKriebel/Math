#!/usr/bin/env python3
"""Dependency-free exact checker for the full-dual two-pair theorem."""

from fractions import Fraction as F


def zero(rows, columns):
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def outer(left, right):
    return [[x * y for y in right] for x in left]


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def hs_inner(left, right):
    return sum(
        left[i][j] * right[i][j]
        for i in range(len(left))
        for j in range(len(left[0]))
    )


def hs_squared(matrix):
    return hs_inner(matrix, matrix)


def digits(index, dims):
    answer = [0] * len(dims)
    for site in range(len(dims) - 1, -1, -1):
        answer[site] = index % dims[site]
        index //= dims[site]
    return tuple(answer)


def flat_index(values, dims):
    answer = 0
    for value, dimension in zip(values, dims):
        answer = dimension * answer + value
    return answer


def partial_trace(matrix, dims, traced_sites):
    traced_sites = tuple(sorted(traced_sites))
    kept_sites = tuple(
        site for site in range(len(dims)) if site not in traced_sites
    )
    kept_dims = tuple(dims[site] for site in kept_sites)
    out_dimension = 1
    for dimension in kept_dims:
        out_dimension *= dimension
    answer = zero(out_dimension, out_dimension)
    for row in range(len(matrix)):
        row_digits = digits(row, dims)
        for column in range(len(matrix)):
            column_digits = digits(column, dims)
            if any(
                row_digits[site] != column_digits[site]
                for site in traced_sites
            ):
                continue
            out_row = flat_index(
                tuple(row_digits[site] for site in kept_sites), kept_dims
            )
            out_column = flat_index(
                tuple(column_digits[site] for site in kept_sites), kept_dims
            )
            answer[out_row][out_column] += matrix[row][column]
    return answer


def q2(matrix, dims=(3, 3)):
    first = partial_trace(matrix, dims, (0,))
    second = partial_trace(matrix, dims, (1,))
    return (
        hs_squared(matrix)
        - F(1, 2) * (hs_squared(first) + hs_squared(second))
        + F(1, 4) * trace(matrix) ** 2
    )


def q3(matrix):
    dims = (3, 3, 3)
    value = hs_squared(matrix)
    for site in range(3):
        value -= F(1, 2) * hs_squared(
            partial_trace(matrix, dims, (site,))
        )
    for first in range(3):
        for second in range(first + 1, 3):
            value += F(1, 4) * hs_squared(
                partial_trace(matrix, dims, (first, second))
            )
    value -= F(1, 8) * trace(matrix) ** 2
    return value


def matrix_rank(matrix):
    work = [row[:] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    x - multiplier * y
                    for x, y in zip(work[row], work[rank])
                ]
        rank += 1
    return rank


# A rank-two 27 by 27 example whose first partial trace has rank six.
u0 = [F(0)] * 27
u1 = [F(0)] * 27
for site_value in range(3):
    u0[9 * site_value + site_value] = F(1)
    u1[9 * site_value + 3 + site_value] = F(1)
C = add(outer(u0, u0), outer(u1, u1))
assert matrix_rank(C) == 2

T = partial_trace(C, (3, 3, 3), (0,))
assert matrix_rank(T) == 6
q = (
    hs_squared(C)
    - F(1, 2)
    * (
        hs_squared(partial_trace(C, (3, 3, 3), (1,)))
        + hs_squared(partial_trace(C, (3, 3, 3), (2,)))
    )
    + F(1, 4)
    * hs_squared(partial_trace(C, (3, 3, 3), (1, 2)))
)
t = q2(T)

trace_t = trace(T)
w0 = trace_t**2 / 9
trace_first = partial_trace(T, (3, 3), (0,))
trace_second = partial_trace(T, (3, 3), (1,))
w1 = (
    (hs_squared(trace_first) + hs_squared(trace_second)) / 3
    - F(2, 9) * trace_t**2
)
w2 = hs_squared(T) - w0 - w1
assert t == F(1, 4) * w0 - F(1, 2) * w1 + w2
assert w0 <= 2 * w1 + 2 * w2
assert t <= F(3, 2) * w2

# Audit the recursion and exact sector normalization.
fully_traceless_t = w2
w011 = fully_traceless_t / 3
assert 2 * q3(C) + 3 * w011 == 2 * q - t + w2

# Audit the d=3 fourth-moment block identity.  The polarized block
# Gram is evaluated directly for this exact rank-two matrix.
blocks = [[zero(9, 9) for _ in range(3)] for _ in range(3)]
for a in range(3):
    for b in range(3):
        for row in range(9):
            for column in range(9):
                blocks[a][b][row][column] = C[9 * a + row][9 * b + column]


def b2(left, right):
    return (
        hs_inner(left, right)
        - F(1, 2)
        * (
            hs_inner(
                partial_trace(left, (3, 3), (0,)),
                partial_trace(right, (3, 3), (0,)),
            )
            + hs_inner(
                partial_trace(left, (3, 3), (1,)),
                partial_trace(right, (3, 3), (1,)),
            )
        )
        + F(1, 4) * trace(left) * trace(right)
    )


block_total = sum(
    b2(blocks[a][b], blocks[a][b])
    for a in range(3)
    for b in range(3)
)
assert block_total == q

one_diagonal_average = F(0)
for a in range(3):
    for b in range(3):
        for c in range(3):
            for d in range(3):
                moment = F(
                    (1 if a == b and d == c else 0)
                    + (1 if a == c and d == b else 0),
                    12,
                )
                one_diagonal_average += moment * b2(
                    blocks[a][b], blocks[c][d]
                )
assert one_diagonal_average == (q + t) / 12
assert 3 * one_diagonal_average == (q + t) / 4
assert q - 3 * one_diagonal_average == (3 * q - t) / 4

print(
    "verified exact two-pair recursion, rank-six trace bound, "
    "and d=3 block fourth-moment normalization"
)

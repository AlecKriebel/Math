#!/usr/bin/env python3
"""Exact checker for the sitewise n=3 sharp-trace reduction."""

from fractions import Fraction as F


def zero(dimension):
    return [[F(0) for _ in range(dimension)] for _ in range(dimension)]


def digits(index, number):
    answer = [0] * number
    for site in range(number - 1, -1, -1):
        answer[site] = index % 3
        index //= 3
    return tuple(answer)


def flat(values):
    answer = 0
    for value in values:
        answer = 3 * answer + value
    return answer


def partial_trace(matrix, number, traced):
    traced = tuple(sorted(traced))
    kept = tuple(site for site in range(number) if site not in traced)
    answer = zero(3 ** len(kept))
    for row in range(3**number):
        row_digits = digits(row, number)
        for column in range(3**number):
            column_digits = digits(column, number)
            if any(
                row_digits[site] != column_digits[site] for site in traced
            ):
                continue
            answer[flat(tuple(row_digits[site] for site in kept))][
                flat(tuple(column_digits[site] for site in kept))
            ] += matrix[row][column]
    return answer


def trace(matrix):
    return sum(matrix[index][index] for index in range(len(matrix)))


def hs_squared(matrix):
    return sum(
        entry * entry
        for row in matrix
        for entry in row
    )


def q2(matrix):
    return (
        hs_squared(matrix)
        - F(1, 2)
        * (
            hs_squared(partial_trace(matrix, 2, (0,)))
            + hs_squared(partial_trace(matrix, 2, (1,)))
        )
        + F(1, 4) * trace(matrix) ** 2
    )


def q3(matrix):
    value = hs_squared(matrix)
    for site in range(3):
        value -= F(1, 2) * hs_squared(
            partial_trace(matrix, 3, (site,))
        )
    for first in range(3):
        for second in range(first + 1, 3):
            value += F(1, 4) * hs_squared(
                partial_trace(matrix, 3, (first, second))
            )
    value -= F(1, 8) * trace(matrix) ** 2
    return value


def q_retaining_site(matrix, site):
    others = tuple(index for index in range(3) if index != site)
    return (
        hs_squared(matrix)
        - F(1, 2)
        * sum(
            hs_squared(partial_trace(matrix, 3, (other,)))
            for other in others
        )
        + F(1, 4)
        * hs_squared(partial_trace(matrix, 3, others))
    )


def doubly_traceless_mass(matrix):
    total = hs_squared(matrix)
    first = hs_squared(partial_trace(matrix, 2, (0,)))
    second = hs_squared(partial_trace(matrix, 2, (1,)))
    scalar = trace(matrix) ** 2
    return total - F(1, 3) * (first + second) + F(1, 9) * scalar


def blocks(matrix, site):
    others = tuple(index for index in range(3) if index != site)
    answer = [[zero(9) for _ in range(3)] for _ in range(3)]
    for row in range(27):
        row_digits = digits(row, 3)
        for column in range(27):
            column_digits = digits(column, 3)
            block_row = row_digits[site]
            block_column = column_digits[site]
            inside_row = flat(tuple(row_digits[index] for index in others))
            inside_column = flat(
                tuple(column_digits[index] for index in others)
            )
            answer[block_row][block_column][inside_row][inside_column] = (
                matrix[row][column]
            )
    return answer


# Formal sitewise identity.
q_symbol = F(17, 13)
t_symbol = F(11, 7)
c_symbol = F(5, 19)
w_symbol = 3 * c_symbol
r_symbol = F(3, 2) * w_symbol - t_symbol
s_symbol = 3 * q_symbol - t_symbol
assert (
    2 * r_symbol + 4 * s_symbol - 9 * c_symbol
    == 12 * (q_symbol - t_symbol / 2)
)


# Exact GHZ projection.
ghz = zero(27)
ghz[flat((0, 0, 0))][flat((0, 0, 0))] = F(1)
ghz[flat((1, 1, 1))][flat((1, 1, 1))] = F(1)
assert q3(ghz) == 0

for site in range(3):
    reduced = partial_trace(ghz, 3, (site,))
    q_value = q_retaining_site(ghz, site)
    t_value = q2(reduced)
    w_value = doubly_traceless_mass(reduced)
    c_value = w_value / 3
    r_value = F(3, 2) * w_value - t_value
    s_value = 3 * q_value - t_value
    assert q_value == F(1, 2)
    assert t_value == 1
    assert w_value == F(10, 9)
    assert c_value == F(10, 27)
    assert r_value == F(2, 3)
    assert s_value == F(1, 2)
    assert 2 * r_value + 4 * s_value == 9 * c_value

    site_blocks = blocks(ghz, site)
    assert sum(
        q2(site_blocks[row][column])
        for row in range(3)
        for column in range(3)
    ) == q_value
    diagonal_sum = zero(9)
    for diagonal in range(3):
        for row in range(9):
            for column in range(9):
                diagonal_sum[row][column] += site_blocks[diagonal][
                    diagonal
                ][row][column]
    assert diagonal_sum == reduced
    assert q2(diagonal_sum) == 2 * q_value


# Exact algebraic nonnormal equality without square roots: scale the
# vectors in (19) by sqrt(2), which only changes the overall norm.
a = [F(0)] * 9
b = [F(0)] * 9
a[flat((0, 0))] = a[flat((1, 1))] = F(1)
b[flat((0, 0))] = b[flat((1, 2))] = F(1)
rank_one = [
    [a[row] * b[column] for column in range(9)] for row in range(9)
]
p = zero(3)
p[0][0] = p[1][1] = F(1)
nonnormal = zero(27)
for row12 in range(9):
    for column12 in range(9):
        for row3 in range(3):
            for column3 in range(3):
                nonnormal[3 * row12 + row3][3 * column12 + column3] = (
                    rank_one[row12][column12] * p[row3][column3]
                )
assert q3(nonnormal) == 0

print(
    "verified sitewise slack identity, sharp GHZ block trace equality, "
    "and exact nonnormal tensor equality"
)

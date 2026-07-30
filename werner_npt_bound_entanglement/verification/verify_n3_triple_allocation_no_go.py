#!/usr/bin/env python3
"""Exact checker for the triple-Hodge allocation no-go."""

from fractions import Fraction as F


def kron(first, second):
    rows_first = len(first)
    columns_first = len(first[0])
    rows_second = len(second)
    columns_second = len(second[0])
    return [
        [
            first[row // rows_second][column // columns_second]
            * second[row % rows_second][column % columns_second]
            for column in range(columns_first * columns_second)
        ]
        for row in range(rows_first * rows_second)
    ]


def digits(index, number):
    result = [0] * number
    for position in range(number - 1, -1, -1):
        result[position] = index % 3
        index //= 3
    return tuple(result)


def flatten(values):
    result = 0
    for value in values:
        result = 3 * result + value
    return result


def partial_trace(matrix, traced):
    traced = tuple(sorted(traced))
    kept = tuple(site for site in range(3) if site not in traced)
    dimension = 3 ** len(kept)
    result = [[F(0) for _ in range(dimension)] for _ in range(dimension)]
    for row in range(27):
        row_digits = digits(row, 3)
        for column in range(27):
            column_digits = digits(column, 3)
            if any(
                row_digits[site] != column_digits[site]
                for site in traced
            ):
                continue
            kept_row = flatten(tuple(row_digits[site] for site in kept))
            kept_column = flatten(
                tuple(column_digits[site] for site in kept)
            )
            result[kept_row][kept_column] += matrix[row][column]
    return result


def norm_squared(matrix):
    return sum(entry * entry for row in matrix for entry in row)


def trace(matrix):
    return sum(matrix[index][index] for index in range(len(matrix)))


p0 = [
    [F(1), F(0), F(0)],
    [F(0), F(0), F(0)],
    [F(0), F(0), F(0)],
]
e01 = [
    [F(0), F(1), F(0)],
    [F(0), F(0), F(0)],
    [F(0), F(0), F(0)],
]
p2 = [
    [F(1), F(0), F(0)],
    [F(0), F(1), F(0)],
    [F(0), F(0), F(0)],
]

matrix = kron(kron(p0, e01), p2)

normal = norm_squared(matrix)
single = sum(
    norm_squared(partial_trace(matrix, (site,)))
    for site in range(3)
)
double = sum(
    norm_squared(partial_trace(matrix, pair))
    for pair in ((0, 1), (0, 2), (1, 2))
)
scalar = trace(matrix) ** 2

assert (normal, single, double, scalar) == (2, 6, 4, 0)

j2 = F(3, 4) * normal - F(1, 2) * single + F(1, 4) * double
j3 = F(1, 8) * (normal - single + double - scalar)
assert j2 == F(-1, 2)
assert j3 == 0

# The expectation of every T_lambda^Gamma is independent of lambda.
for parameter in (F(-7, 3), F(0), F(4, 3), F(19, 5)):
    expectation = F(4, 9) * j2 + (F(8, 9) - parameter) * j3
    assert expectation == F(-2, 9)

# Direct degree-two mass from the exact projection formula.
degree_two = F(1, 3) * single - F(2, 9) * double + F(1, 9) * scalar
assert degree_two == F(10, 9)

# The two nonzero singular values are both one, by the explicit tensor
# factors.  Thus the desired shifted inequality has exact slack 2/9.
shifted_slack = F(4, 9) * (normal + 1) - degree_two
assert shifted_slack == F(2, 9)

print(
    "verified rank two, J2=-1/2, J3=0, allocation expectation=-2/9, "
    "and positive shifted slack 2/9"
)

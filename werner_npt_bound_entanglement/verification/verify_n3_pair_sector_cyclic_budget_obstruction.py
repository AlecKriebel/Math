#!/usr/bin/env python3
"""Exact checker for the cyclic pair-budget obstruction.

Only integer sparse vectors are used.
"""

from __future__ import annotations


def basis_index(a: int, b: int, c: int) -> int:
    return 9 * a + 3 * b + c


def squared_norm(columns: list[dict[int, int]]) -> int:
    return sum(value * value for column in columns for value in column.values())


def inner(
    first: list[dict[int, int]], second: list[dict[int, int]]
) -> int:
    return sum(
        sum(value * second_column.get(index, 0) for index, value in first_column.items())
        for first_column, second_column in zip(first, second)
    )


# V has columns |000> and |001>.
# D_hat1 has amplitude 1 on both and D_hat3 has amplitude 4 on both.
d1_columns = [
    {basis_index(0, 1, 0): 1},
    {basis_index(0, 1, 1): 1},
]
d3_columns = [
    {basis_index(0, 1, 0): 4},
    {basis_index(0, 1, 1): 4},
]

# Pair coefficient norms:
# ||E_10 tensor diag(1,1,-2)||^2 = 6,
# ||diag(4,-2,-2) tensor E_10||^2 = 24.
b1_squared = 6
b2_squared = 0
b3_squared = 24

a1 = squared_norm(d1_columns)
a2 = 0
a3 = squared_norm(d3_columns)
c13 = inner(d1_columns, d3_columns)

assert (a1, a2, a3, c13) == (2, 0, 32, 8)

d1 = 2 * b1_squared - a1
d2 = 2 * b2_squared - a2
d3 = 2 * b3_squared - a3
assert (d1, d2, d3) == (10, 0, 16)

# Twice q_ij avoids fractions.
twice_q12 = d1 + d2
twice_q23 = d2 + d3
twice_q13 = d1 + d3 - 4 * c13
assert (twice_q12, twice_q23, twice_q13) == (10, 16, -6)

full_columns = [
    {
        index: d1_columns[column].get(index, 0)
        + d3_columns[column].get(index, 0)
        for index in set(d1_columns[column]) | set(d3_columns[column])
    }
    for column in range(2)
]
full_output_squared = squared_norm(full_columns)
full_budget = 2 * (b1_squared + b2_squared + b3_squared)
assert (full_output_squared, full_budget, full_budget - full_output_squared) == (
    50,
    60,
    10,
)

assert (twice_q12 + twice_q23 + twice_q13) // 2 == 10

print("exact n=3 cyclic pair-budget obstruction passed")

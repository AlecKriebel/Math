#!/usr/bin/env python3
"""Exact certificate that the proposed cyclic even-reduction bound is false.

The witness is

    C = diag(1,1,0) tensor |0><1| tensor |0><0|.

All arithmetic is integral/rational and the implementation is independent
of the floating-point discovery optimizer.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


D = 3
N = 3
SIZE = D**N


def digits(index: int) -> tuple[int, ...]:
    out = []
    for _ in range(N):
        out.append(index % D)
        index //= D
    return tuple(out)


def index(values: tuple[int, ...]) -> int:
    answer = 0
    multiplier = 1
    for value in values:
        answer += multiplier * value
        multiplier *= D
    return answer


ALL_DIGITS = [digits(k) for k in range(SIZE)]


def coefficient(row: tuple[int, ...], column: tuple[int, ...]) -> int:
    p2 = int(row[0] == column[0] and row[0] in (0, 1))
    e01 = int(row[1] == 0 and column[1] == 1)
    e00 = int(row[2] == 0 and column[2] == 0)
    return p2 * e01 * e00


C = [
    [coefficient(row, column) for column in ALL_DIGITS]
    for row in ALL_DIGITS
]


def partial_trace(matrix: list[list[int]], traced: tuple[int, ...]):
    kept = tuple(site for site in range(N) if site not in traced)
    kept_digits = list(product(range(D), repeat=len(kept)))
    traced_digits = list(product(range(D), repeat=len(traced)))
    output = [
        [0 for _ in range(len(kept_digits))]
        for _ in range(len(kept_digits))
    ]
    for row_number, row_kept in enumerate(kept_digits):
        for column_number, column_kept in enumerate(kept_digits):
            value = 0
            for common in traced_digits:
                row = [0] * N
                column = [0] * N
                for position, site in enumerate(kept):
                    row[site] = row_kept[position]
                    column[site] = column_kept[position]
                for position, site in enumerate(traced):
                    row[site] = common[position]
                    column[site] = common[position]
                value += matrix[index(tuple(row))][index(tuple(column))]
            output[row_number][column_number] = value
    return output


def norm_squared(matrix) -> int:
    return sum(value * value for row in matrix for value in row)


norm = norm_squared(C)
singletons = [
    norm_squared(partial_trace(C, (site,))) for site in range(N)
]
pairs = [
    norm_squared(partial_trace(C, sites))
    for sites in combinations(range(N), 2)
]
trace = partial_trace(C, tuple(range(N)))[0][0]

even_reduction = 3 * norm - 2 * sum(singletons) + sum(pairs)
q3 = Fraction(0)
for size in range(N + 1):
    for sites in combinations(range(N), size):
        q3 += Fraction(-1, 2) ** size * norm_squared(
            partial_trace(C, sites)
        )

# Rank is exactly rank(P2) rank(E01) rank(E00) = 2.  Both nonzero singular
# values are one, since each factor is a partial isometry on its support.
assert norm == 2
assert singletons == [4, 0, 2]
assert pairs == [0, 4, 0]
assert trace == 0
assert even_reduction == -2
assert q3 == 0

# Check the corrected sharp identity:
#   8 Q3 = 2 ||C||_2^2 - |Tr C|^2 + 2 E(C).
assert 8 * q3 == 2 * norm - trace * trace + 2 * even_reduction

# Exact obstruction to routing the live shifted minor through the ordinary
# matched Gram entry.  For basis strings, N = tensor_i(2I-F_i) factorizes
# into the following integer local matrix element.
u1 = (0, 0, 0)
u2 = (0, 0, 1)
v1 = (1, 1, 0)
v2 = (1, 1, 1)


def n_element(x, y, z, w):
    value = 1
    for a, b, c, d in zip(x, y, z, w):
        value *= 2 * int(a == c) * int(b == d) - int(a == d) * int(b == c)
    return value


def n_diagonal(x, y):
    return n_element(x, y, x, y)


g1 = n_diagonal(u1, v1) - 1
g2 = n_diagonal(u2, v2) - 1
h = n_element(u1, v2, u2, v1)
matched = n_element(u1, v1, u2, v2)
assert (g1, g2, h, matched) == (3, 3, -4, 0)
assert abs(h) == 1 + 3  # 1 + sqrt(g1*g2)

print("verified exact n=3 even-reduction obstruction")
print("rank=2, singular values=(1,1)")
print("||C||^2 =", norm)
print("singleton norms =", singletons)
print("pair norms =", pairs)
print("E(C) =", even_reduction)
print("Q3(C) =", q3)
print("shifted-minor obstruction (g1,g2,h,d) =", (g1, g2, h, matched))

#!/usr/bin/env python3
"""Exact checker for the common-plane plus square-zero midpoint zero."""

from fractions import Fraction as F
from itertools import combinations, product


# Every stored matrix coefficient q represents the real number q*sqrt(2).
# All matrices in the exact example have this form, so Hilbert--Schmidt
# products are twice the corresponding rational dot products.
d = 3
n = 3


def add(A, B, scale=F(1)):
    out = dict(A)
    for key, value in B.items():
        out[key] = out.get(key, F(0)) + scale * value
        if out[key] == 0:
            del out[key]
    return out


def scale(A, value):
    return {key: value * entry for key, entry in A.items() if value * entry}


def inner(A, B):
    return 2 * sum(value * B.get(key, F(0)) for key, value in A.items())


def partial_trace(A, traced):
    traced = tuple(sorted(traced))
    remaining = tuple(i for i in range(n) if i not in traced)
    out = {}
    for row_rem in product(range(d), repeat=len(remaining)):
        for col_rem in product(range(d), repeat=len(remaining)):
            value = F(0)
            for trace_values in product(range(d), repeat=len(traced)):
                row = [0] * n
                col = [0] * n
                for pos, site in enumerate(remaining):
                    row[site] = row_rem[pos]
                    col[site] = col_rem[pos]
                for pos, site in enumerate(traced):
                    row[site] = trace_values[pos]
                    col[site] = trace_values[pos]
                value += A.get((tuple(row), tuple(col)), F(0))
            if value:
                out[(row_rem, col_rem)] = value
    return out


def endpoint_pairing(A, B):
    value = F(0)
    for size in range(n + 1):
        for traced in combinations(range(n), size):
            value += F(-1, 2) ** size * inner(
                partial_trace(A, traced),
                partial_trace(B, traced),
            )
    return value


def scalar_projection_at_site(A, site):
    reduced = partial_trace(A, (site,))
    remaining = tuple(i for i in range(n) if i != site)
    out = {}
    for (row_rem, col_rem), value in reduced.items():
        for symbol in range(d):
            row = [0] * n
            col = [0] * n
            row[site] = symbol
            col[site] = symbol
            for pos, other_site in enumerate(remaining):
                row[other_site] = row_rem[pos]
                col[other_site] = col_rem[pos]
            out[(tuple(row), tuple(col))] = value / d
    return out


def sector(A, traceless_sites):
    out = A
    traceless_sites = frozenset(traceless_sites)
    for site in range(n):
        scalar = scalar_projection_at_site(out, site)
        out = add(out, scalar, F(-1)) if site in traceless_sites else scalar
    return out


def matrix_rank(A):
    strings = list(product(range(d), repeat=n))
    matrix = [[A.get((row, col), F(0)) for col in strings] for row in strings]
    rank = 0
    column = 0
    while rank < len(matrix) and column < len(matrix[0]):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            column += 1
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                a - multiplier * b for a, b in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        column += 1
    return rank


def product_actual(A, B):
    """Multiply two stored sqrt(2)-scaled matrices, returning rationals."""
    out = {}
    strings = list(product(range(d), repeat=n))
    for row in strings:
        for col in strings:
            value = 2 * sum(
                A.get((row, middle), F(0)) * B.get((middle, col), F(0))
                for middle in strings
            )
            if value:
                out[(row, col)] = value
    return out


# N=(1/sqrt(2))UU^dagger.  Coefficients below are recorded after
# extracting the common sqrt(2).
N = {
    ((0, 0, 0), (0, 0, 0)): F(1, 2),
    ((1, 1, 1), (1, 1, 1)): F(1, 4),
    ((1, 1, 1), (0, 0, 1)): F(1, 4),
    ((0, 0, 1), (1, 1, 1)): F(1, 4),
    ((0, 0, 1), (0, 0, 1)): F(1, 4),
}

# S=(1/sqrt(2))UW^dagger.
S = {
    ((0, 0, 0), (1, 1, 0)): F(1, 2),
    ((1, 1, 1), (1, 1, 1)): F(1, 4),
    ((1, 1, 1), (0, 0, 1)): F(-1, 4),
    ((0, 0, 1), (1, 1, 1)): F(1, 4),
    ((0, 0, 1), (0, 0, 1)): F(-1, 4),
}

C = add(N, S)

assert matrix_rank(N) == 2
assert matrix_rank(S) == 2
assert matrix_rank(C) == 2
assert inner(N, S) == 0
assert partial_trace(S, (0, 1, 2)) == {}
assert product_actual(S, S) == {}

expected = {
    0: (F(2, 27), F(0), F(0)),
    1: (F(1, 6), F(1, 18), F(-1, 18)),
    2: (F(4, 9), F(5, 9), F(1, 9)),
    3: (F(17, 54), F(7, 18), F(-1, 18)),
}

sector_data = {}
for size in range(n + 1):
    mass_N = F(0)
    mass_S = F(0)
    cross = F(0)
    for sites in combinations(range(n), size):
        N_part = sector(N, sites)
        S_part = sector(S, sites)
        mass_N += inner(N_part, N_part)
        mass_S += inner(S_part, S_part)
        cross += inner(N_part, S_part)
    sector_data[size] = (mass_N, mass_S, cross)

assert sector_data == expected
assert sum(values[0] for values in sector_data.values()) == inner(N, N) == 1
assert sum(values[1] for values in sector_data.values()) == inner(S, S) == 1
assert sum(values[2] for values in sector_data.values()) == inner(N, S) == 0

q_N = endpoint_pairing(N, N)
q_S = endpoint_pairing(S, S)
z = endpoint_pairing(N, S)
q_C = endpoint_pairing(C, C)

assert (q_N, q_S, z, q_C) == (F(1, 8), F(1, 8), F(-1, 8), F(0))

z_from_sectors = F(3, 4) * (
    sector_data[3][2] - sector_data[2][2]
)
assert z_from_sectors == z

z_from_partial_traces = (
    F(-1, 2)
    * sum(
        inner(partial_trace(N, (site,)), partial_trace(S, (site,)))
        for site in range(n)
    )
    + F(1, 4)
    * sum(
        inner(partial_trace(N, sites), partial_trace(S, sites))
        for sites in combinations(range(n), 2)
    )
)
assert z_from_partial_traces == z
assert q_N * q_S - z * z == 0
assert q_N + q_S - 2 * abs(z) == 0

# Degree-two Cauchy alone already exceeds the entire available phase
# budget: sqrt(5)/6 > 1/8.  Verify this without irrational arithmetic.
assert F(5, 36) > F(1, 64)

print(
    "verified: the canonical midpoint zero has "
    "Q(N)=Q(S)=1/8, B(N,S)=-1/8, the exact four-sector table, "
    "and saturates the common/square-zero 2x2 determinant"
)

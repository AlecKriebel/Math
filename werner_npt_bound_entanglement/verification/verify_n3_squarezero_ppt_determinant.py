#!/usr/bin/env python3
"""Exact checks for the square-zero PPT/determinant reduction.

Only Python's standard library is used.  All arithmetic is rational.
"""

from fractions import Fraction as F
from itertools import combinations, product


D = 27


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def basis(word):
    out = [F(0)] * D
    out[index(word)] = F(1)
    return out


def outer(u, v):
    return [[u[i] * v[j] for j in range(D)] for i in range(D)]


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def partial_trace(c, sites):
    sites = tuple(sorted(sites))
    remaining = tuple(i for i in range(3) if i not in sites)
    out = []
    for row_remaining in product(range(3), repeat=len(remaining)):
        row = []
        for col_remaining in product(range(3), repeat=len(remaining)):
            value = F(0)
            for traced_values in product(range(3), repeat=len(sites)):
                rr = [0, 0, 0]
                cc = [0, 0, 0]
                for pos, site in enumerate(remaining):
                    rr[site] = row_remaining[pos]
                    cc[site] = col_remaining[pos]
                for pos, site in enumerate(sites):
                    rr[site] = traced_values[pos]
                    cc[site] = traced_values[pos]
                value += c[index(rr)][index(cc)]
            row.append(value)
        out.append(row)
    return out


def inner(a, b):
    return sum(
        a[i][j] * b[i][j]
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def endpoint_bilinear(a, b):
    value = inner(a, b)
    for site in range(3):
        value -= F(1, 2) * inner(
            partial_trace(a, (site,)), partial_trace(b, (site,))
        )
    for sites in ((0, 1), (0, 2), (1, 2)):
        value += F(1, 4) * inner(
            partial_trace(a, sites), partial_trace(b, sites)
        )
    value -= F(1, 8) * inner(
        partial_trace(a, (0, 1, 2)),
        partial_trace(b, (0, 1, 2)),
    )
    return value


def determinant(a):
    a = [row[:] for row in a]
    answer = F(1)
    for col in range(len(a)):
        pivot = next((row for row in range(col, len(a)) if a[row][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            answer = -answer
        p = a[col][col]
        answer *= p
        for row in range(col + 1, len(a)):
            factor = a[row][col] / p
            for j in range(col + 1, len(a)):
                a[row][j] -= factor * a[col][j]
    return answer


def rank(a):
    a = [row[:] for row in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((r for r in range(row, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        p = a[row][col]
        for r in range(len(a)):
            if r != row and a[r][col]:
                factor = a[r][col] / p
                for j in range(col, len(a[0])):
                    a[r][j] -= factor * a[row][j]
        row += 1
    return row


def partial_transpose_second(h):
    out = [[F(0)] * 4 for _ in range(4)]
    for a, b, c, d in product(range(2), repeat=4):
        out[2 * a + b][2 * c + d] = h[2 * a + d][2 * c + b]
    return out


def all_principal_minors_nonnegative(a):
    for size in range(1, len(a) + 1):
        for subset in combinations(range(len(a)), size):
            minor = [[a[i][j] for j in subset] for i in subset]
            assert determinant(minor) >= 0


# The commuting-swap sector identity behind the sharp orthogonal
# rank-one bound:
# 3^r/8 - 1/4 + (-1)^r/8 is 0,0,1,3.
rank_one_remainders = [
    F(3**r, 8) - F(1, 4) + F((-1) ** r, 8) for r in range(4)
]
assert rank_one_remainders == [F(0), F(0), F(1), F(3)]


# Dynamically construct the canonical physical square-zero equality.
u = (basis((0, 0, 0)), basis((1, 0, 0)))
w = (basis((0, 1, 0)), basis((1, 1, 0)))
units = tuple(outer(u[a], w[b]) for a in range(2) for b in range(2))
h = [[endpoint_bilinear(e, f) for f in units] for e in units]

expected_h = [
    [F(1, 4), 0, 0, F(-1, 4)],
    [0, F(1, 2), 0, 0],
    [0, 0, F(1, 2), 0],
    [F(-1, 4), 0, 0, F(1, 4)],
]
assert h == expected_h
assert determinant(h) == 0

kernel = [F(1), F(0), F(0), F(1)]
assert all(sum(h[i][j] * kernel[j] for j in range(4)) == 0 for i in range(4))

c = [[units[0][i][j] + units[3][i][j] for j in range(D)] for i in range(D)]
assert rank(c) == 2
assert matmul(c, c) == [[F(0)] * D for _ in range(D)]
assert endpoint_bilinear(c, c) == 0

h_pt = partial_transpose_second(h)
expected_h_pt = [
    [F(1, 4), 0, 0, 0],
    [0, F(1, 2), F(-1, 4), 0],
    [0, F(-1, 4), F(1, 2), 0],
    [0, 0, 0, F(1, 4)],
]
assert h_pt == expected_h_pt
all_principal_minors_nonnegative(h_pt)


# The sector-compensation identity modulo the two parity balances.
# For each k, the coefficient difference is
# (-1)^(k+1)/8 times (1,-1,1,-1).
for k in range(2):
    for r in range(4):
        endpoint_coefficient = F(((-1) ** k) * 3**r, 8)
        compensated_coefficient = F((-1) ** k, 4)
        if r == 2:
            compensated_coefficient += (-1) ** k
        if r == 3:
            compensated_coefficient += 3 * ((-1) ** k)
        expected_difference = F((-1) ** (k + 1 + r), 8)
        assert endpoint_coefficient - compensated_coefficient == expected_difference


# Exact abstract obstruction: strict 1/4 product margin and positive
# partial transpose do not force the missing determinant.
h_abs = [
    [F(1, 4), 0, 0, F(-3, 4)],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [F(-3, 4), 0, 0, F(1, 4)],
]
assert determinant(h_abs) == F(-1, 2)
h_abs_pt = partial_transpose_second(h_abs)
expected_abs_pt = [
    [F(1, 4), 0, 0, 0],
    [0, 1, F(-3, 4), 0],
    [0, F(-3, 4), 1, 0],
    [0, 0, 0, F(1, 4)],
]
assert h_abs_pt == expected_abs_pt
all_principal_minors_nonnegative(h_abs_pt)

print("verified: sharp orthogonal rank-one sector identity")
print("verified: exact physical square-zero equality and crossed Gram")
print("verified: positive logical partial transpose")
print("verified: auxiliary-parity compensation coefficients")
print("verified: abstract determinant obstruction")

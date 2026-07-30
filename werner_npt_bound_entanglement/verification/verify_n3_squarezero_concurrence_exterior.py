#!/usr/bin/env python3
"""Exact checks for agent_n3_squarezero_concurrence_exterior.md.

Only the Python standard library and rational arithmetic are used.
"""

from fractions import Fraction as F
from itertools import combinations, product


WORDS = list(product(range(3), repeat=3))
INDEX = {word: index for index, word in enumerate(WORDS)}
D = 27


def basis(word):
    out = [F(0)] * D
    out[INDEX[word]] = F(1)
    return out


def outer(left, right, coefficient=F(1)):
    return [
        [coefficient * left[row] * right[column] for column in range(D)]
        for row in range(D)
    ]


def add(*matrices):
    return [
        [
            sum((matrix[row][column] for matrix in matrices), F(0))
            for column in range(len(matrices[0][0]))
        ]
        for row in range(len(matrices[0]))
    ]


def partial_trace(matrix, traced):
    traced = tuple(sorted(traced))
    kept = tuple(site for site in range(3) if site not in traced)
    kept_words = list(product(range(3), repeat=len(kept)))
    traced_words = list(product(range(3), repeat=len(traced)))
    out = [[F(0) for _ in kept_words] for _ in kept_words]
    for row_index, row_kept in enumerate(kept_words):
        for column_index, column_kept in enumerate(kept_words):
            value = F(0)
            for common in traced_words:
                row = [0, 0, 0]
                column = [0, 0, 0]
                for position, site in enumerate(kept):
                    row[site] = row_kept[position]
                    column[site] = column_kept[position]
                for position, site in enumerate(traced):
                    row[site] = common[position]
                    column[site] = common[position]
                value += matrix[INDEX[tuple(row)]][INDEX[tuple(column)]]
            out[row_index][column_index] = value
    return out


def hs_norm_squared(matrix):
    return sum(
        (entry * entry for row in matrix for entry in row),
        F(0),
    )


def invariants(matrix):
    n = hs_norm_squared(matrix)
    s = sum(
        (hs_norm_squared(partial_trace(matrix, (site,)))
         for site in range(3)),
        F(0),
    )
    p = sum(
        (hs_norm_squared(partial_trace(matrix, sites))
         for sites in combinations(range(3), 2)),
        F(0),
    )
    t = hs_norm_squared(partial_trace(matrix, (0, 1, 2)))
    q = n - F(1, 2) * s + F(1, 4) * p - F(1, 8) * t
    j = F(3, 4) * n - F(1, 2) * s + F(1, 4) * p
    return n, s, p, t, q, j


def matmul(left, right):
    return [
        [
            sum(
                (left[row][middle] * right[middle][column]
                 for middle in range(len(right))),
                F(0),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def matvec(matrix, vector):
    return [
        sum((entry * value for entry, value in zip(row, vector)), F(0))
        for row in matrix
    ]


def partial_transpose_second(matrix):
    out = [[F(0)] * 4 for _ in range(4)]
    for a, b, c, d in product(range(2), repeat=4):
        out[2 * a + b][2 * c + d] = matrix[2 * a + d][2 * c + b]
    return out


# The simultaneous-swap polynomial identity:
# y(r)-1/4+(-1)^r/8 = choose(r,2), with triple occupancy counted
# three times by sum_{i<j} A_i A_j.
for antisymmetric_sites in range(4):
    y_eigenvalue = F(3**antisymmetric_sites, 8)
    left = (
        y_eigenvalue
        - F(1, 4)
        + F((-1) ** antisymmetric_sites, 8)
    )
    right = F(combinations_count := (
        0 if antisymmetric_sites < 2
        else antisymmetric_sites * (antisymmetric_sites - 1) // 2
    ))
    assert left == right


# Exact sharp orthogonal frame.
u = (basis((0, 0, 0)), basis((0, 0, 1)))
w = (basis((1, 1, 0)), basis((1, 1, 1)))

R = [
    [F(1, 4), 0, 0, 0],
    [0, F(3, 4), F(-1, 2), 0],
    [0, F(-1, 2), F(3, 4), 0],
    [0, 0, 0, F(1, 4)],
]
quarter_identity = [
    [F(row == column, 4) for column in range(4)]
    for row in range(4)
]
H = add(quarter_identity, partial_transpose_second(R))

# R has Takagi/eigenvalues 5/4,1/4,1/4,1/4 and concurrence 1/2.
e00 = [F(1), F(0), F(0), F(0)]
e01 = [F(0), F(1), F(0), F(0)]
e10 = [F(0), F(0), F(1), F(0)]
e11 = [F(0), F(0), F(0), F(1)]
singlet = [a - b for a, b in zip(e01, e10)]
triplet = [a + b for a, b in zip(e01, e10)]
assert matvec(R, singlet) == [F(5, 4) * x for x in singlet]
assert matvec(R, triplet) == [F(1, 4) * x for x in triplet]
assert matvec(R, e00) == [F(1, 4) * x for x in e00]
assert matvec(R, e11) == [F(1, 4) * x for x in e11]
assert F(5, 4) - 3 * F(1, 4) == F(1, 2)
assert F(5, 4) > F(1, 2)  # exact failure of R <= I/2


# The equal-singular-value square-zero matrix is an endpoint zero.
c_equal = add(outer(u[0], w[0]), outer(u[1], w[1]))
zero = [[F(0)] * D for _ in range(D)]
assert matmul(c_equal, c_equal) == zero
n, s, p, t, q, j = invariants(c_equal)
assert (n, t, q, j) == (F(2), F(0), F(0), F(-1, 2))
assert 3 * n - 2 * s + p + 2 == 0
assert q == F(1, 4) * (1 - 1) ** 2


# A determinant-one diagonal logical filter gives singular values
# t and 1/t.  Check the quantitative identity at t=2.
filter_parameter = F(2)
c_filtered = add(
    outer(u[0], w[0], filter_parameter),
    outer(u[1], w[1], 1 / filter_parameter),
)
assert matmul(c_filtered, c_filtered) == zero
n, s, p, t, q, j = invariants(c_filtered)
s1 = filter_parameter
s2 = 1 / filter_parameter
assert s1 * s2 == 1
assert j + F(1, 2) == F(1, 4) * (s1 - s2) ** 2
assert q == F(1, 2) * (s1 - s2) ** 2
assert q >= F(1, 4) * (s1 - s2) ** 2
assert 3 * n - 2 * s + p + 2 * s1 * s2 >= 0


# The endpoint Gram has the maximally entangled kernel at equality.
omega = [F(1), F(0), F(0), F(1)]
assert matvec(H, omega) == [F(0)] * 4

print("verified: swap-sector feature identity")
print("verified: exact sharp feature concurrence and Loewner obstruction")
print("verified: square-zero exterior equality")
print("verified: determinant-one filtered quantitative identity")

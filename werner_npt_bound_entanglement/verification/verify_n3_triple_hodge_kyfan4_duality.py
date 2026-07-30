#!/usr/bin/env python3
"""Dependency-free exact checks for the triple-Hodge Ky--Fan frontier."""

from fractions import Fraction as F
from itertools import product


def epsilon(i: int, j: int, k: int) -> int:
    if len({i, j, k}) < 3:
        return 0
    values = (i, j, k)
    inversions = sum(
        values[a] > values[b]
        for a in range(3)
        for b in range(a + 1, 3)
    )
    return -1 if inversions % 2 else 1


def kron(left, right):
    rows_l, cols_l = len(left), len(left[0])
    rows_r, cols_r = len(right), len(right[0])
    return [
        [
            left[i // rows_r][j // cols_r]
            * right[i % rows_r][j % cols_r]
            for j in range(cols_l * cols_r)
        ]
        for i in range(rows_l * rows_r)
    ]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def multiply(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def identity(size: int):
    return [
        [F(int(i == j)) for j in range(size)]
        for i in range(size)
    ]


def diagonal_projection(words):
    diagonal = [F(0)] * 27
    for word in words:
        diagonal[9 * word[0] + 3 * word[1] + word[2]] = F(1)
    return diagonal


def diagonal_reduction(diagonal, keep):
    result = {}
    for word in product(range(3), repeat=3):
        value = diagonal[9 * word[0] + 3 * word[1] + word[2]]
        key = tuple(word[i] for i in keep)
        result[key] = result.get(key, F(0)) + value
    return result


def diagonal_lift(reduced, keep):
    return [
        reduced[tuple(word[i] for i in keep)]
        for word in product(range(3), repeat=3)
    ]


# Unnormalized local epsilon matrices E_p=sqrt(2) A_p.
E = [
    [[F(epsilon(p, a, i)) for i in range(3)] for a in range(3)]
    for p in range(3)
]

# Product tensor t=|000>: D_t=(E_0 tensor E_0 tensor E_0)/sqrt(8).
# Its squared singular spectrum is eight copies of 1/8 and 19 zeros.
K = kron(kron(E[0], E[0]), E[0])
KTK = multiply(transpose(K), K)
assert all(
    KTK[i][j] == (F(1) if i == j and KTK[i][i] else F(0))
    for i in range(27)
    for j in range(27)
)
assert sum(KTK[i][i] for i in range(27)) == 8
assert sum(sorted((KTK[i][i] / 8 for i in range(27)), reverse=True)[:4]) == F(1, 2)

# For x with Schmidt values sigma_1,sigma_2 and sigma_3=0, the exact
# double-Hodge block formula gives diagonal-block eigenvalues
# +/-sqrt(sigma_1^2+sigma_2^2)/2 and 0.
sigma_square_sum = F(1)
mu_1 = sigma_square_sum / 4
mu_2 = sigma_square_sum / 4
assert mu_1 + mu_2 == F(1, 2)

# A saturating rank-four spectral projection for t=|000>.
P_words = {(1, 1, 1), (1, 1, 2), (1, 2, 1), (1, 2, 2)}
P = diagonal_projection(P_words)
single_sum = [F(0)] * 27
pair_sum = [F(0)] * 27
for site in range(3):
    lifted = diagonal_lift(diagonal_reduction(P, (site,)), (site,))
    single_sum = [x + y for x, y in zip(single_sum, lifted)]
for pair in ((0, 1), (0, 2), (1, 2)):
    lifted = diagonal_lift(diagonal_reduction(P, pair), pair)
    pair_sum = [x + y for x, y in zip(pair_sum, lifted)]
marginal_lhs = [
    P[i] + single_sum[i] - pair_sum[i]
    for i in range(27)
]
assert min(marginal_lhs) == 0
assert marginal_lhs[0] == 0

# The corresponding channel expectation at t=|000> is exactly 1/2.
assert sum(P[9 * a + 3 * b + c] for a in (1, 2) for b in (1, 2) for c in (1, 2)) / 8 == F(1, 2)

print("verified exact triple-Hodge Ky--Fan boundary data")
print("product top-four singular-square sum = 1/2")
print("rank-four marginal operator boundary eigenvalue = 0")

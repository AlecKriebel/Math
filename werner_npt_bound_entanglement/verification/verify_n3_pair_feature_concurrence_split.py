#!/usr/bin/env python3
"""Exact checks for agent_n3_pair_feature_concurrence_split.md.

Only Python's standard library and rational arithmetic are used.
"""

from fractions import Fraction as F
from itertools import combinations


WORDS = [(a, b, c) for a in range(3) for b in range(3) for c in range(3)]
INDEX = {w: i for i, w in enumerate(WORDS)}
ORDER = [(0, 0), (0, 1), (1, 0), (1, 1)]


def basis(word, coefficient=1):
    return {word: F(coefficient)}


def phi_last(last, sign=1):
    """sqrt(3) times sign*|Phi> tensor |last>."""
    return {(j, j, last): F(sign) for j in range(3)}


def tensor_two(x, y):
    return {(a, b): xa * yb for a, xa in x.items() for b, yb in y.items()}


def swapped_key(key, sites):
    a, b = list(key[0]), list(key[1])
    for i in sites:
        a[i], b[i] = b[i], a[i]
    return tuple(a), tuple(b)


def inner(x, y):
    return sum(x.get(k, F(0)) * value for k, value in y.items())


def product_i_minus_f_entry(left, right, sites):
    total = F(0)
    sites = tuple(sites)
    for r in range(len(sites) + 1):
        for subset in combinations(sites, r):
            moved = {swapped_key(k, subset): value for k, value in right.items()}
            total += (-1) ** r * inner(left, moved)
    return total


def feature_groups(u, v, logical_norm_factor=F(1)):
    """Return compressions of S_(2), S_(3).

    S_(2)=(1/9) sum_(i<j) (I-F_i)(I-F_j),
    S_(3)=(1/9) product_i (I-F_i).
    """
    w = {(a, c): tensor_two(u[a], v[c]) for a, c in ORDER}
    q2 = [[F(0) for _ in range(4)] for _ in range(4)]
    q3 = [[F(0) for _ in range(4)] for _ in range(4)]
    for row, ac in enumerate(ORDER):
        for col, bd in enumerate(ORDER):
            pair_sum = sum(
                (
                    product_i_minus_f_entry(w[ac], w[bd], sites)
                    for sites in combinations(range(3), 2)
                ),
                F(0),
            )
            q2[row][col] = logical_norm_factor * F(pair_sum, 9)
            triple = product_i_minus_f_entry(w[ac], w[bd], range(3))
            q3[row][col] = logical_norm_factor * F(triple, 9)
    return q2, q3


def matmul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matvec(a, x):
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0))
            for i in range(len(a))]


def scale_matrix(c, a):
    return [[c * x for x in row] for row in a]


def assert_eigenbasis(a, vectors, values):
    assert len(vectors) == len(values) == len(a)
    for vector, value in zip(vectors, values):
        assert matvec(a, vector) == [value * x for x in vector]


J = [
    [F(0), F(0), F(0), F(1)],
    [F(0), F(0), F(-1), F(0)],
    [F(0), F(-1), F(0), F(0)],
    [F(1), F(0), F(0), F(0)],
]

e00 = [F(1), F(0), F(0), F(0)]
e01 = [F(0), F(1), F(0), F(0)]
e10 = [F(0), F(0), F(1), F(0)]
e11 = [F(0), F(0), F(0), F(1)]


def addv(x, y, sign=1):
    return [a + sign * b for a, b in zip(x, y)]


# Canonical sharp code.
u_can = [basis((0, 0, 0)), basis((0, 0, 1))]
v_can = [basis((1, 1, 0)), basis((1, 1, 1))]
q2_can, q3_can = feature_groups(u_can, v_can)

expected_q3_can = [
    [F(0), F(0), F(0), F(0)],
    [F(0), F(1, 9), F(-1, 9), F(0)],
    [F(0), F(-1, 9), F(1, 9), F(0)],
    [F(0), F(0), F(0), F(0)],
]
expected_q2_can = [
    [F(1, 9), F(0), F(0), F(0)],
    [F(0), F(1, 3), F(-2, 9), F(0)],
    [F(0), F(-2, 9), F(1, 3), F(0)],
    [F(0), F(0), F(0), F(1, 9)],
]
assert q3_can == expected_q3_can
assert q2_can == expected_q2_can
assert matmul(matmul(J, q3_can), J) == q3_can
assert matmul(matmul(J, q2_can), J) == q2_can
assert_eigenbasis(
    q3_can,
    [addv(e01, e10, -1), addv(e01, e10), e00, e11],
    [F(2, 9), F(0), F(0), F(0)],
)
assert_eigenbasis(
    q2_can,
    [addv(e01, e10, -1), addv(e01, e10), e00, e11],
    [F(5, 9), F(1, 9), F(1, 9), F(1, 9)],
)
assert F(2, 9) - 0 == F(2, 9)
assert F(5, 9) - 3 * F(1, 9) == F(2, 9)


# Exact code disproving separate 2/9 component budgets.
# These vectors are sqrt(3) times the normalized logical frames, hence a
# logical matrix element has the extra normalization factor 1/9.
u_bad = [phi_last(0, -1), phi_last(2, -1)]
v_bad = [phi_last(2, 1), phi_last(0, -1)]
q2_bad, q3_bad = feature_groups(u_bad, v_bad, F(1, 9))

expected_q3_bad = scale_matrix(
    F(4, 27),
    [
        [1, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 0, 0, 1],
    ],
)
expected_q2_bad = scale_matrix(
    F(4, 27),
    [
        [2, 0, 0, 1],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 2],
    ],
)
assert q3_bad == expected_q3_bad
assert q2_bad == expected_q2_bad
assert matmul(matmul(J, q3_bad), J) == q3_bad
assert matmul(matmul(J, q2_bad), J) == q2_bad
assert_eigenbasis(
    q3_bad,
    [addv(e00, e11), addv(e00, e11, -1), e01, e10],
    [F(8, 27), F(0), F(0), F(0)],
)
assert_eigenbasis(
    q2_bad,
    [addv(e00, e11), addv(e00, e11, -1), e01, e10],
    [F(4, 9), F(4, 27), F(4, 27), F(4, 27)],
)
assert F(8, 27) > F(2, 9)
assert F(4, 9) - 3 * F(4, 27) == 0


# Integer skew basis B_p=sqrt(2) A_p.
B = [
    [[0, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[0, 0, -1], [0, 0, 0], [1, 0, 0]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 0]],
]


def apply_local_triple(mats, vector):
    out = {}
    for word, coefficient in vector.items():
        for row in WORDS:
            value = coefficient
            for site in range(3):
                value *= mats[site][row[site]][word[site]]
            if value:
                out[row] = out.get(row, F(0)) + value
    return out


def compressed_scaled(p, q, r):
    """tilde U^T (B_p tensor B_q tensor B_r) tilde V."""
    moved = [apply_local_triple((B[p], B[q], B[r]), vector)
             for vector in v_bad]
    return [[inner(u_bad[i], moved[j]) for j in range(2)]
            for i in range(2)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


nonzero = {}
det_numerator = F(0)
for p in range(3):
    for q in range(3):
        for r in range(3):
            matrix = compressed_scaled(p, q, r)
            determinant = det2(matrix)
            if determinant:
                nonzero[(p, q, r)] = matrix
                det_numerator += abs(determinant)

assert set(nonzero) == {(0, 0, 1), (1, 1, 1), (2, 2, 1)}
assert all(abs(det2(matrix)) == 4 for matrix in nonzero.values())
assert det_numerator == 12
assert det_numerator / 72 == F(1, 6)
assert F(16, 9) * F(1, 6) == F(8, 27)


# Verify sum A_p tensor A_p=(3P_Phi-F)/2 exactly as 9x9 matrices.
def kron(a, b):
    return [
        [a[i // len(b)][j // len(b[0])] * b[i % len(b)][j % len(b[0])]
         for j in range(len(a[0]) * len(b[0]))]
        for i in range(len(a) * len(b))
    ]


k = [[F(0) for _ in range(9)] for _ in range(9)]
for p in range(3):
    bp_tensor = kron(B[p], B[p])
    for i in range(9):
        for j in range(9):
            k[i][j] += F(bp_tensor[i][j], 2)

rhs = [[F(0) for _ in range(9)] for _ in range(9)]
for i, (a, b) in enumerate([(a, b) for a in range(3) for b in range(3)]):
    for j, (c, d) in enumerate([(a, b) for a in range(3) for b in range(3)]):
        three_p_phi = 1 if a == b and c == d else 0
        flip = 1 if a == d and b == c else 0
        rhs[i][j] = F(three_p_phi - flip, 2)
assert k == rhs

hs_k_squared = sum((entry * entry for row in k for entry in row), F(0))
assert hs_k_squared == 3

# K has eigenvalues 1 on Phi, -1/2 on symmetric Phi-perp, and 1/2
# on the antisymmetric sector.  A_1 has squared operator norm 1/2 and
# Hilbert--Schmidt norm one.  Tensor-product multiplicativity gives:
op_d_squared = F(1, 2)
hs_d_squared = hs_k_squared
assert op_d_squared / hs_d_squared == F(1, 6)
assert F(1, 6) > F(1, 8)

print("exact symmetric feature-concurrence split checks passed")

#!/usr/bin/env python3
"""Dependency-free exact audit of the DTH support lift."""

from fractions import Fraction as F
from itertools import combinations, permutations


def add(left, right, scale=F(1)):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, F(0)) + scale * value
        if out[key] == 0:
            del out[key]
    return out


def scale(vector, scalar):
    return {key: scalar * value for key, value in vector.items() if value}


def dot(left, right):
    # All certificate vectors in this checker are rational and real.
    return sum(value * right.get(key, F(0)) for key, value in left.items())


def tensor(*vectors):
    out = {(): F(1)}
    for vector in vectors:
        new = {}
        for prefix, x in out.items():
            for suffix, y in vector.items():
                suffix_tuple = suffix if isinstance(suffix, tuple) else (suffix,)
                new[prefix + suffix_tuple] = x * y
        out = new
    return out


def position_permute(vector, permutation):
    """Move old tensor position i to new position permutation[i]."""
    out = {}
    for word, value in vector.items():
        new_word = [None] * len(word)
        for old, new in enumerate(permutation):
            new_word[new] = word[old]
        new_word = tuple(new_word)
        out[new_word] = out.get(new_word, F(0)) + value
    return {key: value for key, value in out.items() if value}


def transposition(size, first, second):
    result = list(range(size))
    result[first], result[second] = result[second], result[first]
    return tuple(result)


def jucys_on_tensor(vector):
    out = {}
    for index in range(4):
        out = add(out, position_permute(vector, transposition(5, index, 4)))
    return out


def antisymmetrize_first_four(vector):
    out = {}
    for perm4 in permutations(range(4)):
        inversions = sum(
            perm4[i] > perm4[j]
            for i in range(4)
            for j in range(i + 1, 4)
        )
        sign = F(-1 if inversions % 2 else 1, 24)
        out = add(out, position_permute(vector, tuple(perm4) + (4,)), sign)
    return out


# Unnormalized decomposable bivector e0 wedge e1. Its coefficient
# matrix has W_01=1, W_10=-1, and ||w||^2=2.
w01 = {(0, 1): F(1), (1, 0): F(-1)}


def eta(w, z):
    return tensor(w, w, z)


z_support = {(2,): F(1)}
eta_support = eta(w01, z_support)
assert dot(eta_support, eta_support) == 4
assert antisymmetrize_first_four(eta_support) == {}

j_eta_support = jucys_on_tensor(eta_support)
assert dot(eta_support, j_eta_support) == 0
assert jucys_on_tensor(j_eta_support) == scale(eta_support, 4)

p_plus = scale(add(scale(eta_support, 2), j_eta_support), F(1, 4))
p_minus = scale(add(scale(eta_support, 2), j_eta_support, F(-1)), F(1, 4))
assert dot(p_plus, p_plus) == 2
assert dot(p_minus, p_minus) == 2
assert dot(p_plus, p_minus) == 0

# A non-support vector z=e0 has ||W^dagger z||^2=1. Formula (3)
# predicts 4*||w||^2*1=8.
z_nonsupport = {(0,): F(1)}
eta_nonsupport = eta(w01, z_nonsupport)
assert dot(eta_nonsupport, jucys_on_tensor(eta_nonsupport)) == 8

# Exact phase mismatch: eta(iw,z) has factor i^2=-1, while
# (iw) tensor ((iW)^dagger z) has factor i*(-i)=+1.
assert 1j * 1j == -1
assert 1j * (-1j) == 1


# Direct exact support identity for a general skew matrix.
W = [
    [F(0), F(2), F(-1)],
    [F(-2), F(0), F(3)],
    [F(1), F(-3), F(0)],
]
z = [F(4), F(-2), F(5)]
w_general = {
    (i, j): W[i][j]
    for i in range(3)
    for j in range(3)
    if W[i][j]
}
z_general = {(i,): value for i, value in enumerate(z) if value}
eta_general = eta(w_general, z_general)

norm_w = sum(W[i][j] ** 2 for i in range(3) for j in range(3))
h = [sum(W[i][j] * z[i] for i in range(3)) for j in range(3)]
norm_h = sum(value * value for value in h)
assert dot(eta_general, jucys_on_tensor(eta_general)) == 4 * norm_w * norm_h

# Mixed-conjugate contraction. With real coefficients bar(W)=W, so
# contracting the first barred bivector index with z leaves h=W^dagger z.
mixed_output = tensor(
    w_general,
    {(j,): value for j, value in enumerate(h) if value},
)
assert dot(mixed_output, mixed_output) == norm_w * norm_h


# ---------------------------------------------------------------------------
# S5 group-algebra check of J^2=4 on the first-Pluecker source.


def compose(left, right):
    """Composition left after right."""
    return tuple(left[right[i]] for i in range(5))


identity_perm = tuple(range(5))


def ga_add(left, right, scalar=F(1)):
    out = dict(left)
    for perm, value in right.items():
        out[perm] = out.get(perm, F(0)) + scalar * value
        if out[perm] == 0:
            del out[perm]
    return out


def ga_scale(element, scalar):
    return {perm: scalar * value for perm, value in element.items() if value}


def ga_mul(left, right):
    out = {}
    for p, x in left.items():
        for q, y in right.items():
            pq = compose(p, q)
            out[pq] = out.get(pq, F(0)) + x * y
    return {perm: value for perm, value in out.items() if value}


GA_I = {identity_perm: F(1)}


def ga_perm(perm):
    return {tuple(perm): F(1)}


def ga_trans(first, second):
    return ga_perm(transposition(5, first, second))


A12 = ga_scale(ga_add(GA_I, ga_trans(0, 1), F(-1)), F(1, 2))
A34 = ga_scale(ga_add(GA_I, ga_trans(2, 3), F(-1)), F(1, 2))
pair_exchange_perm = (2, 3, 0, 1, 4)
PAIR_SYM = ga_scale(ga_add(GA_I, ga_perm(pair_exchange_perm)), F(1, 2))
P_X = ga_mul(PAIR_SYM, ga_mul(A12, A34))

A4 = {}
for perm4 in permutations(range(4)):
    inversions = sum(
        perm4[i] > perm4[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    sign = F(-1 if inversions % 2 else 1, 24)
    A4 = ga_add(A4, ga_perm(tuple(perm4) + (4,)), sign)

P_K = ga_add(P_X, A4, F(-1))
J = {}
for index in range(4):
    J = ga_add(J, ga_trans(index, 4))

assert ga_mul(P_K, P_K) == P_K
assert ga_mul(P_K, J) == ga_mul(J, P_K)
J2_MINUS_4 = ga_add(ga_mul(J, J), GA_I, F(-4))
assert ga_mul(P_K, ga_mul(J2_MINUS_4, P_K)) == {}


# ---------------------------------------------------------------------------
# Exact point x point x edge audit of the cloud obstruction xi.


POINTS = tuple(range(5))
EDGES = tuple(combinations(POINTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def point_f(index):
    return {index: F(1), 4: F(-1)}


def edge_r(a, b, c, d):
    out = {}
    for edge, sign in (
        ((a, c), 1),
        ((a, d), -1),
        ((b, c), -1),
        ((b, d), 1),
    ):
        key = EDGE_INDEX[tuple(sorted(edge))]
        out[key] = out.get(key, F(0)) + sign
    return {key: value for key, value in out.items() if value}


def add_rank_one(out, first, second, third, scalar):
    for i, x in first.items():
        for j, y in second.items():
            for k, q in third.items():
                key = (i, j, k)
                out[key] = out.get(key, F(0)) + scalar * x * y * q
                if out[key] == 0:
                    del out[key]


xi = {}
for index in (1, 3):
    add_rank_one(
        xi, point_f(index), point_f(index), edge_r(0, 1, 2, 3), F(-1)
    )
add_rank_one(xi, point_f(3), point_f(3), edge_r(0, 1, 2, 4), F(1))
add_rank_one(xi, point_f(2), point_f(2), edge_r(0, 1, 2, 4), F(-1))
add_rank_one(xi, point_f(1), point_f(1), edge_r(0, 4, 2, 3), F(1))
add_rank_one(xi, point_f(0), point_f(0), edge_r(0, 4, 2, 3), F(-1))


def local_block_permute(vector, permutation):
    out = {}
    for (i, j, edge_index), value in vector.items():
        a, b = EDGES[edge_index]
        new_edge = tuple(sorted((permutation[a], permutation[b])))
        key = (permutation[i], permutation[j], EDGE_INDEX[new_edge])
        out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def block_jucys(vector):
    out = {}
    for index in range(4):
        out = add(
            out,
            local_block_permute(vector, transposition(5, index, 4)),
        )
    return out


j_xi = block_jucys(xi)
assert dot(xi, xi) == 64
assert dot(xi, j_xi) == -40
assert block_jucys(j_xi) == scale(xi, 4)

xi_plus = scale(add(scale(xi, 2), j_xi), F(1, 4))
xi_minus = scale(add(scale(xi, 2), j_xi, F(-1)), F(1, 4))
assert dot(xi_plus, xi_plus) == 22
assert dot(xi_minus, xi_minus) == 42
assert dot(xi_plus, xi_minus) == 0


print("verified exact DTH support-lift audit")
print("literal holomorphic linear map: phase-obstructed")
print("support identity: <eta,J5 eta> = 4||w||^2||W^dagger z||^2")
print("first-Pluecker J5 branches: +2 and -2")
print("cloud xi: norm^2=64, <J5>=-40, branch masses=(22,42)")

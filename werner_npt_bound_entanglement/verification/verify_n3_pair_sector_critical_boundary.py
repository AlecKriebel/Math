#!/usr/bin/env python3
"""Exact checker for the pair-sector critical boundary equality.

Uses only the Python standard library and Fraction arithmetic.
"""

from fractions import Fraction as F
from itertools import product


d = 3
n = 3
N = d**n


def digits(k):
    out = [0] * n
    for i in range(n - 1, -1, -1):
        out[i] = k % d
        k //= d
    return tuple(out)


TUPLES = [digits(k) for k in range(N)]
INDEX = {t: k for k, t in enumerate(TUPLES)}


def zero(rows=N, cols=N):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def adjoint(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def hs2(a):
    return sum((x * x for row in a for x in row), F(0))


def partial_trace_site(c, site):
    rem = [i for i in range(n) if i != site]
    rem_tuples = list(product(range(d), repeat=n - 1))
    out = zero(d ** (n - 1), d ** (n - 1))
    for ir, rr in enumerate(rem_tuples):
        for ic, cc in enumerate(rem_tuples):
            val = F(0)
            for a in range(d):
                row = [0] * n
                col = [0] * n
                row[site] = col[site] = a
                for p, j in enumerate(rem):
                    row[j] = rr[p]
                    col[j] = cc[p]
                val += c[INDEX[tuple(row)]][INDEX[tuple(col)]]
            out[ir][ic] = val
    return out


def embed_identity(x, site):
    rem = [i for i in range(n) if i != site]
    rem_tuples = list(product(range(d), repeat=n - 1))
    rem_index = {t: k for k, t in enumerate(rem_tuples)}
    out = zero()
    for r, rt in enumerate(TUPLES):
        for c, ct in enumerate(TUPLES):
            if rt[site] != ct[site]:
                continue
            rr = tuple(rt[j] for j in rem)
            cc = tuple(ct[j] for j in rem)
            out[r][c] = x[rem_index[rr]][rem_index[cc]]
    return out


def identity_part(c, site):
    return scale(F(1, 3), embed_identity(partial_trace_site(c, site), site))


def pair_sector(c):
    out = zero()
    for identity_site in range(n):
        x = identity_part(c, identity_site)
        for j in range(n):
            if j != identity_site:
                x = add(x, scale(F(-1), identity_part(x, j)))
        out = add(out, x)
    return out


def matrix_rank(a):
    x = [row[:] for row in a]
    rows, cols = len(x), len(x[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if x[r][col]), None)
        if pivot is None:
            continue
        x[rank], x[pivot] = x[pivot], x[rank]
        p = x[rank][col]
        x[rank] = [z / p for z in x[rank]]
        for r in range(rows):
            if r != rank and x[r][col]:
                q = x[r][col]
                x[r] = [x[r][j] - q * x[rank][j] for j in range(cols)]
        rank += 1
    return rank


def local_reduction_of_plane(columns, site):
    p = zero()
    for col in columns:
        for i in range(N):
            for j in range(N):
                p[i][j] += col[i] * col[j]
    # Trace the two complementary sites.
    keep = site
    out = zero(d, d)
    others = [i for i in range(n) if i != keep]
    for a in range(d):
        for b in range(d):
            val = F(0)
            for rest in product(range(d), repeat=2):
                row = [0] * n
                col = [0] * n
                row[keep], col[keep] = a, b
                for q, j in enumerate(others):
                    row[j] = col[j] = rest[q]
                val += p[INDEX[tuple(row)]][INDEX[tuple(col)]]
            out[a][b] = val
    return out


def basis_vector(t):
    v = [F(0)] * N
    v[INDEX[t]] = F(1)
    return v


# C = E01 tensor E01 tensor (P0 + P1).
c = zero()
for k in (0, 1):
    c[INDEX[(0, 0, k)]][INDEX[(1, 1, k)]] = F(1)

assert matrix_rank(c) == 2
dmat = pair_sector(c)

expected = zero()
for k in range(3):
    expected[INDEX[(0, 0, k)]][INDEX[(1, 1, k)]] = F(2, 3)
assert dmat == expected
assert hs2(dmat) / hs2(c) == F(2, 3)

u = [basis_vector((0, 0, 0)), basis_vector((0, 0, 1))]
v = [basis_vector((1, 1, 0)), basis_vector((1, 1, 1))]
assert [matrix_rank(local_reduction_of_plane(u, i)) for i in range(3)] == [1, 1, 2]
assert [matrix_rank(local_reduction_of_plane(v, i)) for i in range(3)] == [1, 1, 2]

# Euler equations D V = (2/3) C V and D^* U = (2/3) C^* U.
for col in v:
    lhs = [sum((dmat[i][j] * col[j] for j in range(N)), F(0)) for i in range(N)]
    rhs0 = [sum((c[i][j] * col[j] for j in range(N)), F(0)) for i in range(N)]
    assert lhs == [F(2, 3) * z for z in rhs0]
for col in u:
    da = adjoint(dmat)
    ca = adjoint(c)
    lhs = [sum((da[i][j] * col[j] for j in range(N)), F(0)) for i in range(N)]
    rhs0 = [sum((ca[i][j] * col[j] for j in range(N)), F(0)) for i in range(N)]
    assert lhs == [F(2, 3) * z for z in rhs0]

print("verified exact pair-sector critical boundary equality")

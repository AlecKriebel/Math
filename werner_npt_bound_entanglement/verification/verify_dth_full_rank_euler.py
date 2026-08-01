#!/usr/bin/env python3
"""Dependency-free exact audit of the DTH Euler/marginal identities."""

from fractions import Fraction as F
from itertools import product


N = 27


def eps(p, a, i):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in positive) - int((p, a, i) in negative)


def zeros(n=N, m=N):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def add(*matrices):
    return [[sum(m[i][j] for m in matrices)
             for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def hodge_hat(z):
    """Dhat=(2 sqrt(2))D, so D^*D=Dhat^T Dhat/8."""
    out = zeros()
    for p, q, r in product(range(3), repeat=3):
        c0 = z[9 * p + 3 * q + r]
        if not c0:
            continue
        for a, b, c in product(range(3), repeat=3):
            row = 9 * a + 3 * b + c
            for i, j, k in product(range(3), repeat=3):
                value = c0 * eps(p, a, i) * eps(q, b, j) * eps(r, c, k)
                if value:
                    out[row][9 * i + 3 * j + k] += value
    return out


def reduced_one(vector):
    out = []
    for site in range(3):
        rho = zeros(3, 3)
        for row in product(range(3), repeat=3):
            for col_value in range(3):
                col = list(row)
                col[site] = col_value
                i = 9 * row[0] + 3 * row[1] + row[2]
                j = 9 * col[0] + 3 * col[1] + col[2]
                rho[row[site]][col_value] += vector[i] * vector[j]
        out.append(rho)
    return out


def partial_trace_operator(matrix, site):
    out = zeros(3, 3)
    other = [k for k in range(3) if k != site]
    for a, b in product(range(3), repeat=2):
        total = F(0)
        for tail in product(range(3), repeat=2):
            row = [0, 0, 0]
            col = [0, 0, 0]
            row[site], col[site] = a, b
            for k, value in zip(other, tail):
                row[k] = col[k] = value
            ir = 9 * row[0] + 3 * row[1] + row[2]
            ic = 9 * col[0] + 3 * col[1] + col[2]
            total += matrix[ir][ic]
        out[a][b] = total
    return out


def local_action(h, site):
    out = zeros()
    for row in product(range(3), repeat=3):
        for col in product(range(3), repeat=3):
            if all(row[k] == col[k] for k in range(3) if k != site):
                i = 9 * row[0] + 3 * row[1] + row[2]
                j = 9 * col[0] + 3 * col[1] + col[2]
                out[i][j] = h[row[site]][col[site]]
    return out


def apply(matrix, vector):
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


def outer(x, y):
    return [[a * b for b in y] for a in x]


def main():
    # Unconditional local output identity on a nonsymmetric rational tensor.
    z = [F(((17 * i + 11) % 23) - 11, 7) for i in range(N)]
    dh = hodge_hat(z)
    s_out = scale(F(1, 8), matmul(transpose(dh), dh))
    norm2 = sum(x * x for x in z)
    rhos = reduced_one(z)
    for site in range(3):
        expected = [[(norm2 * F(a == b) - rhos[site][a][b]) / 2
                     for b in range(3)] for a in range(3)]
        assert partial_trace_operator(s_out, site) == expected

    # Infinitesimal Hodge covariance (6), with the same generic z.
    h = [[F(2), F(-1), F(3)], [F(-1), F(4), F(2)], [F(3), F(2), F(-5)]]
    for site in range(3):
        local = local_action(h, site)
        hz = apply(local, z)
        left = hodge_hat(hz)
        right = add(
            scale(sum(h[i][i] for i in range(3)), dh),
            scale(-1, matmul(transpose(local), dh)),
            scale(-1, matmul(dh, local)),
        )
        assert left == right

    # Smooth factor equality z0=e0 tensor (3E00+4E11)/5.
    z0 = [F(0)] * N
    z0[0], z0[4] = F(3, 5), F(4, 5)
    d0 = hodge_hat(z0)
    s0 = scale(F(1, 8), matmul(transpose(d0), d0))

    # Top P=e0-perp tensor span{q,E22}, q=(4E00+3E11)/5.
    q = [F(0)] * 9
    q[0], q[4] = F(4, 5), F(3, 5)
    r = [F(0)] * 9
    r[8] = F(1)
    prest = add(outer(q, q), outer(r, r))
    ptop = zeros()
    for local_site in (1, 2):
        for i, j in product(range(9), repeat=2):
            ptop[9 * local_site + i][9 * local_site + j] = prest[i][j]
    mtop = matmul(ptop, s0)
    f_value = sum(mtop[i][i] for i in range(N))
    assert f_value == F(1, 2)

    rho0 = reduced_one(z0)
    for site in range(3):
        expected = [[f_value * (F(a == b) - rho0[site][a][b]) / 2
                     for b in range(3)] for a in range(3)]
        assert partial_trace_operator(mtop, site) == expected

    # Euler equation via the exact Fierz form (10).
    gp8 = scale(4, [[F(i == j) for j in range(N)] for i in range(N)])
    gp8 = add(gp8, scale(-1, ptop))
    # Construct the two operator embeddings in (10) directly.
    for site in range(3):
        pi = partial_trace_operator(ptop, site)
        # Complementary marginal is obtained by explicit trace over site.
        phat_dim = 9
        phat = zeros(phat_dim, phat_dim)
        others = [k for k in range(3) if k != site]
        for rr, cc in product(product(range(3), repeat=2), repeat=2):
            total = F(0)
            for value in range(3):
                row = [0, 0, 0]
                col = [0, 0, 0]
                row[site] = col[site] = value
                for k, x in zip(others, rr):
                    row[k] = x
                for k, x in zip(others, cc):
                    col[k] = x
                total += ptop[9 * row[0] + 3 * row[1] + row[2]][
                    9 * col[0] + 3 * col[1] + col[2]]
            ir = 3 * rr[0] + rr[1]
            ic = 3 * cc[0] + cc[1]
            phat[ir][ic] = total

        op_i = zeros()
        op_hat = zeros()
        for row, col in product(product(range(3), repeat=3), repeat=2):
            ir = 9 * row[0] + 3 * row[1] + row[2]
            ic = 9 * col[0] + 3 * col[1] + col[2]
            if all(row[k] == col[k] for k in others):
                op_i[ir][ic] = pi[row[site]][col[site]]
            if row[site] == col[site]:
                rr = tuple(row[k] for k in others)
                cc = tuple(col[k] for k in others)
                # Transpose in the fixed product basis.
                op_hat[ir][ic] = phat[3 * cc[0] + cc[1]][3 * rr[0] + rr[1]]
        gp8 = add(gp8, scale(-1, op_i), op_hat)

    assert apply(gp8, z0) == [8 * f_value * x for x in z0]

    print("exact DTH full-rank Euler identities passed")
    print("output marginal complement identity passed")
    print("factor critical normalization F=1/2 passed")


if __name__ == "__main__":
    main()

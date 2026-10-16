#!/usr/bin/env python3
"""Independent exact C4 controls; Python standard library only.

No candidate verifier or inherited review is imported or executed.
The analytic proof and the measure-zero argument are in REPORT.md.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]


def rank(a):
    a = [[F(x) for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        p = a[r][j]
        a[r] = [v / p for v in a[r]]
        for k in range(len(a)):
            if k != r:
                q = a[k][j]
                a[k] = [u - q * v for u, v in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def det(a):
    a = [[F(x) for x in row] for row in a]
    out = F(1)
    for j in range(len(a)):
        k = next((k for k in range(j, len(a)) if a[k][j]), None)
        if k is None:
            return F(0)
        if k != j:
            a[k], a[j] = a[j], a[k]
            out *= -1
        p = a[j][j]
        out *= p
        for k in range(j + 1, len(a)):
            q = a[k][j] / p
            a[k] = [u - q * v for u, v in zip(a[k], a[j])]
    return out


def stats(s, edge_factor=2):
    return [sum(s[i][i] for i in range(4))] + [
        edge_factor * s[i][j] for i, j in EDGES
    ]


def gram(x):
    return [[sum(a * b for a, b in zip(u, v)) for v in x] for u in x]


def jacobian(x, edge_factor=2):
    n = len(x[0])
    rows = [[2 * x[i][j] for i in range(4) for j in range(n)]]
    for a, b in EDGES:
        rows.append([
            edge_factor * ((x[b][j] if i == a else 0)
                           + (x[a][j] if i == b else 0))
            for i in range(4) for j in range(n)
        ])
    return rows


# Tiny exact polynomial algebra, used only to check the alternating identity.
N = 9  # x1..x4, lambda, edge12,edge23,edge34,edge41


def var(i):
    e = [0] * N
    e[i] = 1
    return {tuple(e): F(1)}


def add(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return {e: c for e, c in out.items() if c}


def mul(p, q):
    out = {}
    for e, c in p.items():
        for f, d in q.items():
            g = tuple(a + b for a, b in zip(e, f))
            out[g] = out.get(g, F(0)) + c * d
    return {e: c for e, c in out.items() if c}


def scale(c, p):
    return {e: c * v for e, v in p.items() if c * v}


def main():
    checks = {}
    x = [[1, 0], [0, 0], [0, 1], [0, 0]]
    j = jacobian(x)
    # Columns x11,x21,x22,x42,x41, in statistic edge order.
    cols = [0, 2, 3, 7, 6]
    minor = [[row[c] for c in cols] for row in j]
    checks['rank_two_X_rank'] = rank(x)
    checks['five_output_jacobian_rank'] = rank(j)
    checks['selected_minor_determinant'] = str(det(minor))
    assert rank(x) == 2 and rank(j) == 5 and det(minor) == 32
    j_old = jacobian(x, edge_factor=1)
    old_minor = [[row[c] for c in cols] for row in j_old]
    checks['OWR_unscaled_edge_minor_determinant'] = str(det(old_minor))
    assert det(old_minor) == 2

    e1 = [[1], [0], [0], [0]]
    s = gram(e1)
    q = [[F(i == j, 4) for j in range(4)] for i in range(4)]
    checks['rank_one_and_PD_statistics_equal'] = stats(s) == stats(q)
    checks['PD_witness_leading_principal_minors'] = [
        str(det([row[:k] for row in q[:k]])) for k in range(1, 5)
    ]
    assert stats(s) == stats(q)
    assert all(det([row[:k] for row in q[:k]]) > 0 for k in range(1, 5))
    assert stats(s, 1) == stats(q, 1)

    # f=t12*t34-t23*t41 is four times an exact rank-one 2-minor.
    checks['rank_one_ideal_witness'] = 't12*t34-t23*t41 = 4*(s12*s34-s23*s14)'
    test_vectors = [[1, 2, 3, 4], [0, 1, 2, 3], [1, 0, 0, 0]]
    for v in test_vectors:
        t = stats(gram([[a] for a in v]))
        assert t[1] * t[3] - t[2] * t[4] == 0
    assert 1 * 1 - 0 * 0 == 1  # the polynomial is not identically zero.

    xv = [var(i) for i in range(4)]
    lam = var(4)
    kx = [mul(lam, xv[i]) for i in range(4)]
    for e, (a, b) in enumerate(EDGES):
        kx[a] = add(kx[a], mul(var(5 + e), xv[b]))
        kx[b] = add(kx[b], mul(var(5 + e), xv[a]))
    lhs = add(*(scale((-1) ** i, mul(xv[i], kx[i])) for i in range(4)))
    rhs = mul(lam, add(*(scale((-1) ** i, mul(xv[i], xv[i])) for i in range(4))))
    residual = add(lhs, scale(-1, rhs))
    checks['alternating_identity_residual_monomials'] = len(residual)
    assert not residual

    lap = [[0] * 4 for _ in range(4)]
    for a, b in EDGES:
        lap[a][a] += 1
        lap[b][b] += 1
        lap[a][b] -= 1
        lap[b][a] -= 1
    assert all(sum(row) == 0 for row in lap)
    checks['balanced_exception_laplacian_rank'] = rank(lap)
    assert rank(lap) == 3
    # PSD is certified analytically by z^T lap z=sum_edges(za-zb)^2.
    for v in test_vectors:
        assert sum(v[i] * lap[i][j] * v[j] for i in range(4) for j in range(4)) == sum(
            (v[a] - v[b]) ** 2 for a, b in EDGES
        )

    eps = F(1, 100)
    # Equal diagonal completion near e1: Qii=||x||^2/4 and Qij=xi*xj on edges.
    lower_diag = (1 - eps) ** 2 / 4
    upper_offdiag_sum = 2 * (1 + eps) * eps
    checks['explicit_rank_one_open_box_PD_margin'] = str(lower_diag - upper_offdiag_sum)
    assert lower_diag - upper_offdiag_sum > 0

    result = {
        'status': 'PASS',
        'method': 'exact rational linear algebra and exact polynomial identity; no sampling proof',
        'checks': checks,
        'limits': 'Does not prove the Gaussian null-set argument automatically; see REPORT.md. Does not certify the TDA experiments or exact K4,4 priority.',
        'source_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

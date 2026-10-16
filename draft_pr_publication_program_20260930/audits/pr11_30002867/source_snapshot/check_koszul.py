#!/usr/bin/env python3
"""Small exact checks of the multiplication-matrix CI criterion.

Python standard library only. All ranks are computed over Q by Fraction-based
Gaussian elimination. This is validation of examples, not a proof by search.
"""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def zero(rows, cols):
    return [[0] * cols for _ in range(rows)]


def rank(matrix, ncols=None):
    if not matrix:
        return 0
    a = [[Fraction(x) for x in row] for row in matrix]
    cols = len(a[0]) if ncols is None else ncols
    assert all(len(row) == cols for row in a)
    pivot = 0
    for col in range(cols):
        found = next((r for r in range(pivot, len(a)) if a[r][col]), None)
        if found is None:
            continue
        a[pivot], a[found] = a[found], a[pivot]
        p = a[pivot][col]
        a[pivot] = [v / p for v in a[pivot]]
        for r in range(pivot + 1, len(a)):
            if a[r][col]:
                scale = a[r][col]
                a[r] = [v - scale * w for v, w in zip(a[r], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def matmul(a, b):
    if not b:
        return [[] for _ in a]
    cols = len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(cols)] for i in range(len(a))]


def shifted(m, value):
    return [[v - (value if i == j else 0) for j, v in enumerate(row)]
            for i, row in enumerate(m)]


def koszul(mats, lam):
    d, n = len(mats), len(mats[0])
    t = [shifted(m, v) for m, v in zip(mats, lam)]
    d1 = [sum((m[row] for m in t), []) for row in range(n)]
    pairs = list(combinations(range(d), 2))
    d2 = zero(d * n, len(pairs) * n)
    for col, (i, j) in enumerate(pairs):
        for a in range(n):
            for b in range(n):
                d2[i*n+a][col*n+b] = -t[j][a][b]
                d2[j*n+a][col*n+b] = t[i][a][b]
    return d1, d2


def monomial_algebra(basis):
    """Multiplication matrices of the quotient with this monomial order ideal."""
    d = len(basis[0])
    n = len(basis)
    indices = {b: i for i, b in enumerate(basis)}
    mats = [zero(n, n) for _ in range(d)]
    for col, exp in enumerate(basis):
        for var in range(d):
            target = tuple(e + (i == var) for i, e in enumerate(exp))
            if target in indices:
                mats[var][indices[target]][col] = 1
    return mats


def point(lam):
    return [[[v]] for v in lam]


def direct_product(*tuples):
    d = len(tuples[0])
    n = sum(len(ms[0]) for ms in tuples)
    result = [zero(n, n) for _ in range(d)]
    off = 0
    for ms in tuples:
        size = len(ms[0])
        assert len(ms) == d
        for j, m in enumerate(ms):
            for a in range(size):
                for b in range(size):
                    result[j][off+a][off+b] = m[a][b]
        off += size
    return result


def gorenstein_non_ci():
    # Basis 1,x,y,z,t, where xy=z^2=t, and the remaining positive products vanish.
    n = 5
    x, y, z = [zero(n, n) for _ in range(3)]
    x[1][0], y[2][0], z[3][0] = 1, 1, 1
    x[4][2], y[4][1], z[4][3] = 1, 1, 1
    return [x, y, z]


def power(m, exponent):
    n = len(m)
    result = [[int(i == j) for j in range(n)] for i in range(n)]
    for _ in range(exponent):
        result = matmul(result, m)
    return result


def monomial_generator_count(basis):
    """Independent count of minimal monomial generators of the complementary ideal."""
    basis = set(basis)
    d = len(next(iter(basis)))
    border = set()
    for exp in basis:
        for j in range(d):
            new = tuple(v + (i == j) for i, v in enumerate(exp))
            if new not in basis:
                border.add(new)
    return sum(not any(other != m and all(a <= b for a, b in zip(other, m))
                       for other in border) for m in border)


def run_case(name, mats, expectations, global_mu, monomial_basis=None):
    d, n = len(mats), len(mats[0])
    assert d > 0 and n > 0
    for a, b in combinations(mats, 2):
        assert matmul(a, b) == matmul(b, a), (name, 'noncommuting')
    results = []
    mus = []
    for lam, expected_mu in expectations:
        d1, d2 = koszul(mats, lam)
        assert all(x == 0 for row in matmul(d1, d2) for x in row)
        r1, r2 = rank(d1), rank(d2)
        assert r1 == n - 1, (name, lam, r1)
        mu = d*n-r1-r2
        assert mu == expected_mu, (name, lam, mu, expected_mu)
        mus.append(mu)
        results.append({'lambda': list(lam), 'rank_D1': r1, 'rank_D2': r2,
                        'local_generators': mu, 'CI_rank_target': (d-1)*(n-1),
                        'is_local_CI': mu == d})
    assert max(mus) == global_mu
    if monomial_basis is not None:
        assert monomial_generator_count(monomial_basis) == global_mu
    # An unrelated point must have full D1 rank and zero first Koszul homology.
    external = (101,) * d
    d1, d2 = koszul(mats, external)
    assert rank(d1) == n
    assert d*n-rank(d1)-rank(d2) == 0
    return {'name': name, 'variables': d, 'length': n,
            'global_generators': global_mu, 'complete_intersection': global_mu == d,
            'points': results, 'outside_support_homology': 0}


def main():
    cases = []
    def add(name, basis, mu):
        cases.append(run_case(name, monomial_algebra(basis),
                              [((0,)*len(basis[0]), mu)], mu, basis))
    add('one reduced point in three variables', [(0, 0, 0)], 3)
    add('univariate length four', [(i,) for i in range(4)], 1)
    add('monomial CI x^2,y^3', list(product(range(2), range(3))), 2)
    add('monomial CI x^2,y^2,z^2', list(product(range(2), repeat=3)), 3)
    add('square-zero plane algebra', [(0,0), (1,0), (0,1)], 3)
    add('square-zero three-variable algebra', [(0,0,0), (1,0,0), (0,1,0), (0,0,1)], 6)
    add('mixed monomial non-CI x^3,xy,y^2', [(0,0), (1,0), (2,0), (0,1)], 3)
    add('four-variable monomial CI', list(product(range(2), repeat=4)), 4)
    cases.append(run_case('three reduced points', direct_product(point((0,0)),
                        point((1,0)), point((0,1))),
                        [((0,0),2), ((1,0),2), ((0,1),2)], 2))
    ci = monomial_algebra(list(product(range(2), repeat=2)))
    cases.append(run_case('nonreduced CI plus reduced point',
                        direct_product(ci, point((2,3))), [((0,0),2), ((2,3),2)], 2))
    nonci = monomial_algebra([(0,0), (1,0), (0,1)])
    cases.append(run_case('non-CI plus reduced point',
                        direct_product(nonci, point((2,3))), [((0,0),3), ((2,3),2)], 3))
    g = gorenstein_non_ci()
    cases.append(run_case('Gorenstein length-five non-CI', g, [((0,0,0),5)], 5))
    # Its common kernel (socle) is one-dimensional: this does not imply CI in d=3.
    assert len(g[0]) - rank(sum(g, [])) == 1
    t = monomial_algebra([(i,) for i in range(4)])[0]
    cases.append(run_case('curvilinear nonlinear embedding (t,t^2,t^3)',
                        [t, power(t,2), power(t,3)], [((0,0,0),3)], 3))
    report = {'arithmetic': 'exact rational, Python Fraction', 'case_count': len(cases),
              'passed': True, 'cases': cases}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

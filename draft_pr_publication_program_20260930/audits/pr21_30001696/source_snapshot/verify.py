#!/usr/bin/env python3
"""Exact finite sanity checks for the cross-polytope flow proof.

No floating-point exponentials, large search, or nonstandard dependencies.
The homeomorphism and PL conclusion require the written proof, not these tests.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def K(N, k, j):
    return sum((-1) ** ell * choose(j, ell) * choose(N - j, k - ell)
               for ell in range(k + 1))


def det(A):
    A = [list(map(F, row)) for row in A]
    result = F(1)
    for k in range(len(A)):
        row = next((i for i in range(k, len(A)) if A[i][k]), None)
        if row is None:
            return F(0)
        if row != k:
            A[row], A[k] = A[k], A[row]
            result = -result
        pivot = A[k][k]
        result *= pivot
        for i in range(k + 1, len(A)):
            q = A[i][k] / pivot
            for j in range(k + 1, len(A)):
                A[i][j] -= q * A[k][j]
            A[i][k] = F(0)
    return result


def minus(v):
    signs = [1 if x > 0 else -1 for x in v if x]
    return sum(x != y for x, y in zip(signs, signs[1:]))


def extrema(v):
    states = {}
    for x in v:
        allowed = [1 if x > 0 else -1] if x else [-1, 1]
        new = {}
        for s in allowed:
            if not states:
                new[s] = (0, 0)
            else:
                new[s] = (min(lo + (s != t) for t, (lo, hi) in states.items()),
                          max(hi + (s != t) for t, (lo, hi) in states.items()))
        states = new
    return min(lo for lo, hi in states.values()), max(hi for lo, hi in states.values())


def flow_matrix(N, a):
    return [[sum(F(K(N, k, j) * comb(N, h) * K(N, k, h),
                   2 ** N * comb(N, k)) * a ** k for k in range(N + 1))
             for h in range(N + 1)] for j in range(N + 1)]


def main():
    counts = {}
    eigens = orthogonal = 0
    for N in range(1, 10):
        for k in range(N + 1):
            v = [K(N, k, j) for j in range(N + 1)]
            for j in range(N + 1):
                lhs = ((N-j)*v[j+1] if j < N else 0) + (j*v[j-1] if j else 0)
                assert lhs == (N - 2 * k) * v[j]
                eigens += 1
            for ell in range(N + 1):
                dot = sum(comb(N, j) * v[j] * K(N, ell, j) for j in range(N + 1))
                assert dot == (2 ** N * comb(N, k) if k == ell else 0)
                orthogonal += 1
    counts['integer_eigen_equations'] = eigens
    counts['weighted_orthogonality_equations'] = orthogonal

    minors = 0
    for d in range(2, 7):
        for a in (F(1, 2), F(1, 3)):
            A = flow_matrix(d - 1, a)
            assert all(sum(row) == 1 for row in A)
            for k in range(1, d + 1):
                for rows in combinations(range(d), k):
                    for cols in combinations(range(d), k):
                        assert det([[A[i][j] for j in cols] for i in rows]) > 0
                        minors += 1
    counts['strictly_positive_rational_minors'] = minors

    variations = face_patterns = 0
    for d in range(2, 8):
        A = flow_matrix(d - 1, F(1, 2))
        for v in product((-1, 0, 1), repeat=d):
            if not any(v):
                continue
            lo, hi = extrema(v)
            assert lo == minus(v)
            y = [sum(x * a for x, a in zip(v, row)) for row in A]
            assert extrema(y)[1] <= minus(v)
            variations += 1
            face_patterns += 1
    counts['zero_sensitive_variation_tests'] = variations
    counts['face_completion_tests'] = face_patterns

    spectral = 0
    for d in range(2, 8):
        N = d - 1
        for r in range(1, d):
            for coeff in product((-1, 0, 1), repeat=r):
                if any(coeff):
                    v = [sum(coeff[k] * K(N, k, j) for k in range(r)) for j in range(d)]
                    assert extrema(v)[1] <= r - 1
                    spectral += 1
            for coeff in product((-1, 0, 1), repeat=d - r):
                if any(coeff):
                    v = [sum(coeff[k-r] * K(N, k, j) for k in range(r, d))
                         for j in range(d)]
                    assert minus(v) >= r
                    spectral += 1
    counts['spectral_sign_separation_tests'] = spectral

    graphs = edges = 0
    for d in range(2, 10):
        for k in range(1, d):
            states = list(combinations(range(d), k))
            adjacent = {s: [] for s in states}
            for s in states:
                for pos, j in enumerate(s):
                    for new in (j-1, j+1):
                        if not 0 <= new < d or new in s:
                            continue
                        raw = list(s)
                        raw[pos] = new
                        inversions = sum(raw[u] > raw[v] for u in range(k) for v in range(u+1, k))
                        assert inversions % 2 == 0
                        adjacent[s].append(tuple(sorted(raw)))
                        edges += 1
            seen = {states[0]}
            stack = [states[0]]
            while stack:
                for t in adjacent[stack.pop()]:
                    if t not in seen:
                        seen.add(t)
                        stack.append(t)
            assert len(seen) == len(states)
            graphs += 1
    counts['connected_compound_graphs'] = graphs
    counts['positive_wedge_moves'] = edges

    ratios = 0
    for d in range(2, 10):
        N = d - 1
        for r in range(1, d):
            y = {0: F(1)} if r == 1 else {0: F(3, 5), r-1: F(4, 5)}
            z = {r: F(1)} if d-r == 1 else {r: F(5, 13), N: F(12, 13)}
            previous = F(0)
            for a in (F(1, 4), F(1, 2), F(1), F(2), F(4)):
                R2 = sum(c*c*a**(2*k) for k,c in z.items()) / sum(c*c*a**(2*k) for k,c in y.items())
                assert R2 > previous
                if a <= 1:
                    assert a**(2*N) <= R2 <= a*a
                else:
                    assert a*a <= R2 <= a**(2*N)
                previous = R2
                ratios += 1
    counts['spectral_ratio_bounds'] = ratios

    cutoff = 0
    epsilon = F(1, 8)
    for beta in (F(1, 4), F(1, 2), F(1), F(2), F(4)):
        def h(a):
            return a if a <= epsilon else epsilon+(1-epsilon)*(a-epsilon)/(beta-epsilon)
        def inv(b):
            return b if b <= epsilon else epsilon+(beta-epsilon)*(b-epsilon)/(1-epsilon)
        assert h(beta) == 1
        for a in sorted({epsilon/2, epsilon} | {beta * F(j, 20) for j in range(1, 21)}):
            assert inv(h(a)) == a
            assert 0 < h(a) <= 1
            if a <= epsilon:
                assert h(a) == a
            cutoff += 1
    counts['identity_cutoff_inverse_tests'] = cutoff

    print(json.dumps({'status': 'passed', 'arithmetic': 'exact Python integers and fractions',
                      'checks': counts,
                      'scope': 'Bounded finite checks; not a proof certificate for the homeomorphism or PL theorem'}, indent=2))


if __name__ == '__main__':
    main()

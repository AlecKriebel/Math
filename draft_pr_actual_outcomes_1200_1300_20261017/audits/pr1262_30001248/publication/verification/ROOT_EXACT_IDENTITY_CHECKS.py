#!/usr/bin/env python3
"""Independent graphwise rational identities; not an asymptotic LLT test."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run():
    rng = random.Random(126230001248)
    cases = 0
    overlaps = 0
    variance_cases = 0
    ps = (F(1, 7), F(1, 2), F(6, 7))
    for n in range(3, 11):
        edges = list(combinations(range(n), 2))
        N = len(edges)
        idx = {e: i for i, e in enumerate(edges)}
        wedges = [(i, j) for i, j in combinations(range(N), 2)
                  if len(set(edges[i]) | set(edges[j])) == 3]
        disjoint = [(i, j) for i, j in combinations(range(N), 2)
                    if len(set(edges[i]) | set(edges[j])) == 4]
        triples = [tuple(idx[e] for e in combinations(v, 2))
                   for v in combinations(range(n), 3)]
        A = len(wedges)
        B = sum(len(set(a) & set(b)) == 1
                for a in wedges for b in wedges if a != b)
        require(A == N * (n - 2), 'wedge count')
        require(B == A * (4 * n - 10), 'ordered overlap count')
        require(F(B) - F(4 * A * A, N) == -2 * A, 'conditional cancellation')
        require(len(disjoint) == 3 * comb(n, 4), 'disjoint pair count')
        overlaps += 1
        masks = {0, (1 << N) - 1,
                 sum(1 << i for i, e in enumerate(edges) if 0 in e),
                 sum(1 << i for i, e in enumerate(edges) if e[0] < n // 2 <= e[1])}
        masks.update(rng.getrandbits(N) for _ in range(18))
        for mask in sorted(masks):
            x = [(mask >> i) & 1 for i in range(N)]
            M = sum(x)
            T = sum(x[a] * x[b] * x[c] for a, b, c in triples)
            W = sum(x[a] * x[b] for a, b in wedges)
            Y = sum(x[a] * x[b] for a, b in disjoint)
            require(Y == comb(M, 2) - W, 'graphwise pair partition')
            for p in ps:
                z = [F(v) - p for v in x]
                triangle_expansion = (
                    p ** 2 * (n - 2) * sum(z)
                    + p * sum(z[a] * z[b] for a, b in wedges)
                    + sum(z[a] * z[b] * z[c] for a, b, c in triples))
                require(F(T) - comb(n, 3) * p ** 3 == triangle_expansion,
                        'graphwise triangle chaos expansion')
                pair_expansion = (p * comb(n - 2, 2) * sum(z)
                                  + sum(z[a] * z[b] for a, b in disjoint))
                require(F(Y) - 3 * comb(n, 4) * p ** 2 == pair_expansion,
                        'graphwise 2K2 chaos expansion')
                cases += 1
    for n in range(3, 101):
        N = comb(n, 2)
        for p in ps:
            leading = N * (n - 2) ** 2 * p ** 5 * (1 - p)
            residual = (3 * comb(n, 3) * p ** 4 * (1 - p) ** 2
                        + comb(n, 3) * p ** 3 * (1 - p) ** 3)
            covariance = (comb(n, 3) * p ** 3 * (1 - p ** 3)
                          + 12 * comb(n, 4) * p ** 5 * (1 - p))
            require(leading + residual == covariance, 'variance identity')
            ratio = ((1 - p) / p + (1 - p) ** 2 / (3 * p ** 2)) / (n - 2)
            require(residual / leading == ratio, 'exact CLT variance ratio')
            variance_cases += 1
    return {
        'schema': 'pr1262-root-graphwise-identities-v1',
        'result': 'PASS',
        'graph_probability_cases': cases,
        'ordered_wedge_incidence_sizes': overlaps,
        'closed_variance_and_exact_ratio_cases': variance_cases,
        'graph_n_range': [3, 10],
        'variance_n_range': [3, 100],
        'p_values': [str(p) for p in ps],
        'arithmetic': 'exact fractions; explicit exceptions survive optimization',
        'scope': 'finite identity diagnostics, not an asymptotic or imported-LLT proof',
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))

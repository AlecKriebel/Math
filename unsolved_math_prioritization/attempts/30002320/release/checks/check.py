#!/usr/bin/env python3
"""Small exact controls for the report; no asymptotic theorem is proved here.
Standard library only. Prints a JSON receipt; no file or network writes.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb, factorial
import json


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for rest in compositions(n - a, k - 1):
                yield (a,) + rest


def proper_count(n, edges, k):
    # Direct vertex-by-vertex enumeration, independent of class-size formula.
    previous = [[] for _ in range(n)]
    for u, v in edges:
        if u > v:
            u, v = v, u
        previous[v].append(u)
    colors = [-1] * n

    def visit(v):
        if v == n:
            return 1
        used = {colors[u] for u in previous[v]}
        total = 0
        for c in range(k):
            if c not in used:
                colors[v] = c
                total += visit(v + 1)
        return total
    return visit(0)


def type_sum(n, m, k):
    result = 0
    for ns in compositions(n, k):
        multiplicity = factorial(n)
        for a in ns:
            multiplicity //= factorial(a)
        allowed = (n*n - sum(a*a for a in ns)) // 2
        if allowed >= m:
            result += multiplicity * comb(allowed, m)
    return result


def main():
    total_graphs = 0
    first_moment_checks = 0
    balanced_checks = 0
    component_checks = 0
    annihilation_checks = 0
    details = []
    for n in range(1, 6):
        all_edges = list(combinations(range(n), 2))
        N = len(all_edges)
        sums = {k: defaultdict(int) for k in (3, 4)}
        for mask in range(1 << N):
            edges = [e for i, e in enumerate(all_edges) if mask >> i & 1]
            total_graphs += 1
            for k in (3, 4):
                sums[k][len(edges)] += proper_count(n, edges, k)
        for k in (3, 4):
            for m in range(N + 1):
                # Both sides count pairs (graph, labeled proper coloring).
                assert sums[k][m] == type_sum(n, m, k)
                first_moment_checks += 1
            details.append({'n': n, 'k': k, 'edge_counts_checked': N+1})
    for n in range(1, 11):
        for k in range(2, 6):
            ns = [n//k + (i < n % k) for i in range(k)]
            T = (n*n-sum(a*a for a in ns))//2
            max_T = max((n*n-sum(a*a for a in cs))//2 for cs in compositions(n,k))
            C = factorial(n)
            for a in ns:
                C //= factorial(a)
            assert T == max_T
            assert C * (n+1)**k >= k**n
            balanced_checks += 1
    for k in (3, 4):
        for n in range(1, 8):
            path = [(i, i+1) for i in range(n-1)]
            assert proper_count(n, path, k) == k*(k-1)**(n-1)
            component_checks += 1
        for ell in range(3, 8):
            cycle = [(i, (i+1) % ell) for i in range(ell)]
            assert proper_count(ell, cycle, k) == (k-1)**ell + (-1)**ell*(k-1)
            component_checks += 1
    for k in range(2, 5):
        n = k+1
        clique = list(combinations(range(n), 2))
        missing = clique[1:]
        assert proper_count(n, clique, k) == 0
        assert proper_count(n, missing, k) == factorial(k)
        # Attach two isolated vertices: exact factor k^2.
        assert proper_count(n+2, missing, k) == factorial(k)*k**2
        assert max(1, proper_count(n+2, clique, k)) == 1
        assert max(1, proper_count(n, clique, k))*k**2 != 1
        annihilation_checks += 1
    assert Fraction(3)*Fraction(2,3)**3 == Fraction(8,9)
    assert Fraction(8,9) < 1
    # At n=6,k=3,m=6, enumerate the annealed expectation exactly via types.
    example = Fraction(type_sum(6,6,3), comb(15,6))
    return {
        'passed': True,
        'scope': 'finite exact identities and counterexamples to generic inferences only',
        'graphs_enumerated': total_graphs,
        'first_moment_parameter_checks': first_moment_checks,
        'balanced_type_checks': balanced_checks,
        'component_count_checks': component_checks,
        'one_edge_annihilation_and_clamp_checks': annihilation_checks,
        'literal_rate_at_k3_d6': '8/9',
        'finite_example_E_Z_n6_k3_m6': str(example),
        'first_moment_details': details,
        'asymptotic_conjecture_verified': False,
    }


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))

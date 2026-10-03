#!/usr/bin/env python3
"""Independent finite controls; no asymptotic claim. Python standard library only.
Counts colorings by edge-subset inclusion-exclusion, independently of the
reviewed author's vertex-color recursion. Prints JSON; no writes or network.
"""
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, factorial, log, exp


def subset_sums(a, N):
    a = a[:]
    for i in range(N):
        bit = 1 << i
        for mask in range(1 << N):
            if mask & bit:
                a[mask] += a[mask ^ bit]
    return a


def components(n, edges, mask):
    p = list(range(n))
    def root(x):
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x
    for i, (u,v) in enumerate(edges):
        if mask >> i & 1:
            p[root(u)] = root(v)
    verts = Counter(root(v) for v in range(n))
    counts = Counter()
    for i, (u,v) in enumerate(edges):
        if mask >> i & 1:
            counts[root(u)] += 1
    return [(s, counts[r]) for r, s in verts.items()]


def assignment_pair_sum(n, m, k):
    # No multinomial/type enumeration: enumerate all k^n assignments directly.
    edges = list(combinations(range(n), 2))
    return sum(comb(sum(cs[u] != cs[v] for u,v in edges), m)
               for cs in product(range(k), repeat=n))


def rooted_cycle_path_templates(n, edges):
    # A cycle with distinguished attachment vertex is represented in both
    # directions; retain a[1] < a[ell-1] to remove that factor of two.
    idx = {e: i for i,e in enumerate(edges)}
    hist = [0] * (1 << len(edges))
    by_size = Counter()
    for ell in range(3, n+1):
        for r in range(n-ell+1):
            total = 0
            for a in permutations(range(n), ell+r):
                if a[1] > a[ell-1]:
                    continue
                pairs = [(a[j], a[(j+1)%ell]) for j in range(ell)]
                if r:
                    pairs += [(a[0], a[ell])]
                    pairs += [(a[j],a[j+1]) for j in range(ell,ell+r-1)]
                mask = sum(1 << idx[tuple(sorted(e))] for e in pairs)
                assert mask.bit_count() == ell+r
                hist[mask] += 1
                total += 1
            assert total == factorial(n)//factorial(n-ell-r)//2
            by_size[(ell,r)] = total
    return hist, by_size


def main():
    graphs = params = roots = witness_graphs = witness_expectations = forest_checks = 0
    detail = []
    example = None
    for n in range(1,7):
        edges = list(combinations(range(n),2))
        N = len(edges)
        sizes = [mask.bit_count() for mask in range(1 << N)]
        comps = [components(n, edges, mask) for mask in range(1 << N)]
        graphs += 1 << N
        w_base, templates = rooted_cycle_path_templates(n, edges)
        witnesses = subset_sums(w_base, N)
        wsums = [0] * (N+1)
        for mask, c in enumerate(comps):
            R = sum(s for s,t in c if t >= s)
            assert R <= witnesses[mask]
            if any(t >= s+1 for s,t in c):
                assert R > 0
            wsums[sizes[mask]] += witnesses[mask]
            witness_graphs += 1
        for m in range(N+1):
            lhs = Fraction(wsums[m], comb(N,m))
            rhs = sum((Fraction(num * comb(N-ell-r,m-ell-r), comb(N,m))
                       for (ell,r),num in templates.items() if ell+r <= m), Fraction())
            assert lhs == rhs
            witness_expectations += 1
        for k in (2,3,4):
            base = [(-1)**sizes[mask] * k**len(comps[mask]) for mask in range(1 << N)]
            counts = subset_sums(base, N)
            sums = [0] * (N+1)
            colorables = [0] * (N+1)
            f_sums = [0.] * (N+1)
            for mask,z in enumerate(counts):
                assert 0 <= z <= k**n
                m = sizes[mask]
                sums[m] += z
                colorables[m] += bool(z)
                f_sums[m] += z**(1/n)
                assert bool(z) <= z**(1/n) + 1e-12
                assert z**(1/n) <= k*bool(z) + 1e-12
                roots += 1
                if all(t == s-1 for s,t in comps[mask]):
                    assert z == k**(n-m)*(k-1)**m
                    forest_checks += 1
                for i in range(N):
                    if not mask >> i & 1:
                        assert counts[mask | (1 << i)] <= z
            ns = [n//k + (i < n%k) for i in range(k)]
            T = (n*n-sum(x*x for x in ns))//2
            C = factorial(n)
            for x in ns:
                C //= factorial(x)
            for m in range(N+1):
                assert sums[m] == assignment_pair_sum(n,m,k)
                assert C*comb(T,m) <= sums[m] <= k**n*comb(T,m)
                denom = comb(N,m)
                F = f_sums[m]/denom
                prob = colorables[m]/denom
                A = (sums[m]/denom)**(1/n)
                assert prob-1e-10 <= F <= k*prob+1e-10
                assert F <= A+1e-10
                params += 1
                if (n,k,m) == (6,3,6):
                    example = str(Fraction(sums[m],denom))
            # Exact binomial-model annealed identity with p=1/4.
            lhs = sum(Fraction(sums[m]*3**(N-m),4**N) for m in range(N+1))
            rhs = sum(Fraction(3,4)**sum(cs[u] == cs[v] for u,v in edges)
                      for cs in product(range(k),repeat=n))
            assert lhs == rhs
        detail.append({'n':n, 'graphs':1 << N, 'colors':[2,3,4], 'edge_counts':N+1})
    assert example == '7560/143'
    # Exact clique-minus-edge annihilation and soft/hard limit controls.
    annihilation = []
    for k in range(2,6):
        n=k+1
        edges=list(combinations(range(n),2))
        def weighted_missing(weight, omit=False):
            es=edges[1:] if omit else edges
            return sum(weight**sum(cs[u] == cs[v] for u,v in es)
                       for cs in product(range(k),repeat=n))
        z0=weighted_missing(Fraction(0))
        zminus=weighted_missing(Fraction(0),True)
        soft=weighted_missing(Fraction(1,2))
        assert z0 == 0 and zminus == factorial(k) and soft > 0
        assert zminus*k**2 == factorial(k)*k**2
        annihilation.append({'k':k,'K_k_plus_1':int(z0),'K_k_plus_1_minus_edge':int(zminus), 'soft_weight_half':str(soft)})
    # d=0 and strict first-moment-region numerical/exact controls.
    assert Fraction(3)*Fraction(2,3)**3 == Fraction(8,9)
    assert 6 > -2*log(3)/log(Fraction(2,3))
    assert 3*exp(-1) > Fraction(8,9)
    return {'passed':True,'scope':'finite exact identities and adversarial model controls; not an asymptotic proof',
            'independent_method':'edge-subset inclusion-exclusion with subset zeta transform',
            'graphs':graphs,'graph_color_cases':roots,'first_moment_parameter_cases':params,
            'cycle_path_graph_domination_cases':witness_graphs,
            'cycle_path_exact_expectation_cases':witness_expectations,
            'forest_formula_cases':forest_checks,'binomial_annealed_parameter_cases':18,
            'clique_annihilation':annihilation,'finite_example_E_Z_n6_k3_m6':example,
            'literal_rate_k3_d6':'8/9','root_limit_k3_d6':'0 (proved analytically in reviewed packet)',
            'low_density_k2_excluded':'triangle is uncolorable; k>=3 hypothesis is essential',
            'asymptotic_conjecture_verified':False,'details':detail}

if __name__ == '__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))

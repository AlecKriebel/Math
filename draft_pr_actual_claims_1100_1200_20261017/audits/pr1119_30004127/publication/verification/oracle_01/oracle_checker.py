"""Exact, independently authored finite adversarial controls. No third-party packages."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product, combinations
from math import comb
from pathlib import Path
import json, hashlib

def check(condition, message='finite invariant failed'):
    if not condition:
        raise RuntimeError(message)
N = 6
TRIANGLES = ((0, 1, 2), (0, 3, 4))
PAIRS = tuple(combinations(range(N), 2))
IDX = {e: i for i, e in enumerate(PAIRS)}
GOOD = (0, 3, 5, 6)
BAD = (7, 1, 2, 4)

def graph_distribution(patterns, hidden=True):
    out = Counter()
    for perm in permutations(range(N)) if hidden else [tuple(range(N))]:
        for pat in product(patterns, repeat=len(TRIANGLES)):
            mask = 0
            for tri, bits in zip(TRIANGLES, pat):
                for i, (u, v) in enumerate(combinations(tri, 2)):
                    if bits >> i & 1:
                        mask |= 1 << IDX[tuple(sorted((perm[u], perm[v])))]
            out[mask] += 1
    return out

def tv(a, b):
    za = sum(a.values())
    zb = sum(b.values())
    return sum((abs(Fraction(a.get(v, 0), za) - Fraction(b.get(v, 0), zb)) for v in a.keys() | b.keys()), Fraction()) / 2

def project(dist, k):
    inds = [i for i, (u, v) in enumerate(PAIRS) if u < k and v < k]
    out = Counter()
    for g, c in dist.items():
        out[sum(((g >> i & 1) << j for j, i in enumerate(inds)))] += c
    return out

def optimum_query_tv(good, bad, maxq):
    """Bellman over all deterministic adaptive edge-query trees, arbitrary names.
    Signed masses suffice: each depth-q leaf contributes absolute signed mass.
    Taking max over next edges includes every adaptive policy by backward induction.
    """
    total = sum(good.values())
    check(total == sum(bad.values()))
    signed = tuple(((g, good.get(g, 0) - bad.get(g, 0)) for g in good.keys() | bad.keys() if good.get(g, 0) != bad.get(g, 0)))

    @lru_cache(None)
    def mass(mask, value):
        return sum((c for g, c in signed if g & mask == value))

    @lru_cache(None)
    def solve(mask, value, q):
        if q == 0:
            return abs(mass(mask, value))
        return max((solve(mask | 1 << i, value, q - 1) + solve(mask | 1 << i, value | 1 << i, q - 1) for i in range(len(PAIRS)) if not mask >> i & 1))
    ans = [str(Fraction(solve(0, 0, q), 2 * total)) for q in range(maxq + 1)]

    def witness(mask, value, q):
        if q == 0:
            return {'decision': 'GOOD' if mass(mask, value) >= 0 else 'BAD', 'signed_mass': mass(mask, value)}
        candidates = [i for i in range(len(PAIRS)) if not mask >> i & 1]
        i = max(candidates, key=lambda i: solve(mask | 1 << i, value, q - 1) + solve(mask | 1 << i, value | 1 << i, q - 1))
        return {'query': PAIRS[i], 'absent': witness(mask | 1 << i, value, q - 1), 'present': witness(mask | 1 << i, value | 1 << i, q - 1)}
    nonadaptive = []
    for q in range(maxq + 1):
        val = max((sum((abs(mass(sum((1 << i for i in coords)), sum(((bits >> j & 1) << i for j, i in enumerate(coords))))) for bits in range(1 << q))) for coords in combinations(range(len(PAIRS)), q)))
        nonadaptive.append(str(Fraction(val, 2 * total)))
    check(Fraction(ans[-1]) > Fraction(nonadaptive[-1]), 'adaptive negative control should help at q=4')
    return {'tv_by_worst_case_query_budget': ans, 'optimal_nonadaptive_tv': nonadaptive, 'bellman_states': solve.cache_info().currsize, 'marginal_states': mass.cache_info().currsize, 'optimal_adaptive_four_query_tree': witness(0, 0, maxq)}

def conditional_permutation_check():
    """Condition on exact exposed host images AND all bits among exposed labels.
    Verify unused named labels retain uniform remaining host image. Uses k=2,3,
    including full-triangle posteriors, so this is stronger than pre-failure only.
    """
    checked = 0
    for patterns in (GOOD, BAD):
        for k in (2, 3):
            groups = {}
            for perm in permutations(range(N)):
                for pats in product(patterns, repeat=len(TRIANGLES)):
                    edges = set()
                    for tri, bits in zip(TRIANGLES, pats):
                        for i, e in enumerate(combinations(tri, 2)):
                            if bits >> i & 1:
                                edges.add(tuple(sorted(e)))
                    observation = tuple((int(tuple(sorted((perm[u], perm[v]))) in edges) for u, v in combinations(range(k), 2)))
                    key = (perm[:k], observation)
                    counters = groups.setdefault(key, [Counter() for _ in range(k, N)])
                    for label in range(k, N):
                        counters[label - k][perm[label]] += 1
            for (images, obs), counters in groups.items():
                remaining = set(range(N)) - set(images)
                for counts in counters:
                    check(set(counts) == remaining and len(set(counts.values())) == 1)
                    checked += 1
    return checked

def sample_distinct_counts(s):
    state = {0: Fraction(1)}
    for _ in range(s):
        new = {}
        for j, p in state.items():
            new[j] = new.get(j, Fraction()) + p * Fraction(6 + j, 12)
            if j < N:
                new[j + 1] = new.get(j + 1, Fraction()) + p * Fraction(N - j, 12)
        state = new
    return state

def parity_control():
    out = []
    for k in range(4):
        for coords in combinations(range(3), k):
            a = Counter((tuple((p >> i & 1 for i in coords)) for p in GOOD))
            b = Counter((tuple((p >> i & 1 for i in coords)) for p in BAD))
            t = tv(a, b)
            check(t == (0 if k < 3 else 1))
            out.append({'coordinates': coords, 'tv': str(t)})
    return out

def parameter_checks():
    for d in range(4, 129):
        m = 1 << d * (d + 1)
        K = (1 << d * d - 2 * d) // d
        n = 6 * m
        T = m * K
        eps = Fraction(T, 32 * n * n)
        check(K > 0 and T > 64)
        check(Fraction(1, 2304 * d * (1 << 3 * d)) <= eps <= Fraction(1, 1152 * d * (1 << 3 * d)))
        check(n * (n - 1) * (n - 2) >= Fraction(n ** 3, 2))
        check(Fraction(n ** 3, 96 * T) >= m)
        check(Fraction(n ** 3, 12 * T) >= m)
    return {'actual_parameter_d_range': [4, 128], 'cases': 125, 'integer_rational_inequalities': 'all pass'}

def main():
    g = graph_distribution(GOOD)
    b = graph_distribution(BAD)
    total = sum(g.values())
    check(total == 11520)
    induced = []
    tvs = {}
    for k in range(N + 1):
        subsets = list(combinations(range(N), k))
        fail = Fraction(sum((any((set(tri) <= set(s) for tri in TRIANGLES)) for s in subsets)), len(subsets))
        bound = Fraction(len(TRIANGLES) * comb(k, 3), comb(N, 3)) if k >= 3 else Fraction(0)
        t = tv(project(g, k), project(b, k))
        check(t <= fail <= bound)
        tvs[k] = t
        induced.append({'k_distinct_tail_names': k, 'exact_tv': str(t), 'exact_triangle_exposure_probability': str(fail), 'union_bound': str(bound)})

    def stopped(d):
        out = Counter()
        for mask, c in d.items():
            e = mask & 1
            key = (2, e) if e else (3, next(iter(project(Counter({mask: c}), 3))))
            out[key] += c
        return out
    stopping_tv = tv(stopped(g), stopped(b))
    check(stopping_tv <= Fraction(1, 10))
    repeat = []
    for s in (1, 2, 3, 4, 6, 10):
        occupancy = sample_distinct_counts(s)
        exact = sum((p * tvs[k] for k, p in occupancy.items()), Fraction())
        exposure = sum((p * Fraction(len(TRIANGLES) * comb(k, 3), comb(N, 3)) for k, p in occupancy.items() if k >= 3), Fraction())
        check(exact <= exposure)
        repeat.append({'sample_calls': s, 'exact_tv_with_induced_graph_and_sample_names': str(exact), 'expected_union_bound': str(exposure), 'occupancy': {str(k): str(p) for k, p in occupancy.items()}})
    known_g = graph_distribution(GOOD, False)
    known_b = graph_distribution(BAD, False)
    t = tv(project(known_g, 3), project(known_b, 3))
    check(t == 1)
    results = {'host': {'n': N, 'triangles': TRIANGLES, 'per_world_latent_assignments': total, 'distinct_good_graphs': len(g), 'distinct_bad_graphs': len(b)}, 'parity_marginals': parity_control(), 'induced_exposure': induced, 'all_adaptive_edge_queries': optimum_query_tv(g, b, 4), 'adaptive_stopping_tv': str(stopping_tv), 'posterior_uniformity_counterchecks': conditional_permutation_check(), 'repeated_samples': repeat, 'negative_control_known_map_tv_after_3_triangle_queries': str(t), 'parameter_checks': parameter_checks(), 'verdict': 'All exact controls passed. Finite evidence supports, but does not replace, the general coupling proof.'}
    out = Path(__file__).with_name('oracle_checker_results.json')
    out.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
if __name__ == '__main__':
    main()

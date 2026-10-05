#!/usr/bin/env python3
"""Independent exact checks; no author-code imports or external dependencies.
Finite calculations supplement the analytic audit, not the asymptotic theorem.
"""
import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction as R
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path


def geometry(n):
    edges = list(combinations(range(n), 2))
    index = {e: j for j, e in enumerate(edges)}
    triples = list(combinations(range(n), 3))
    covers = [frozenset(index[e] for e in combinations(t, 2)) for t in triples]
    return edges, triples, covers


def backwards_terminal(n):
    """Memoized backward transition law on AVAILABLE TRIANGLES, not chosen sets."""
    edges, triples, covers = geometry(n)
    conflicts = [sum(1 << j for j, b in enumerate(covers) if a & b) for a in covers]
    distinguished = [triples.index((0, 1, 2))]
    if n >= 5:
        distinguished.append(triples.index((0, 3, 4)))
    tags = {j: 1 << i for i, j in enumerate(distinguished)}

    @lru_cache(None)
    def future(available):
        if not available:
            return {(0, 0): R(1)}
        result = defaultdict(R)
        count = available.bit_count()
        for j in range(len(triples)):
            if available >> j & 1:
                for (size, tag), probability in future(available & ~conflicts[j]).items():
                    result[(size + 1, tag | tags.get(j, 0))] += probability / count
        return dict(result)

    law = future((1 << len(triples)) - 1)
    assert sum(law.values()) == 1
    sizes = defaultdict(R)
    for (size, tag), probability in law.items():
        sizes[size] += probability
    marginal = sum(prob for (size, tag), prob in law.items() if tag & 1)
    expected = sum(size * prob for size, prob in sizes.items())
    assert expected == comb(n, 3) * marginal
    joint = sum(prob for (size, tag), prob in law.items() if tag == 3) if n >= 5 else None
    if n == 5:
        assert joint == R(1, 15) and marginal == R(1, 5)
    return {'n': n, 'backward_states': future.cache_info().currsize,
            'size_distribution': {str(k): str(v) for k, v in sorted(sizes.items())},
            'expected_size': str(expected), 'marginal': str(marginal),
            'selected_joint': None if joint is None else str(joint)}


def hazard_exhaustive(n=6):
    """Enumerate target packings first, then every graph containing their edges."""
    edges, triples, covers = geometry(n)
    full = (1 << len(edges)) - 1
    masks = [sum(1 << e for e in t) for t in covers]
    families = []

    def pack(start, chosen, shadow):
        if chosen:
            families.append((chosen, shadow))
        for j in range(start, len(triples)):
            if not shadow & masks[j]:
                pack(j + 1, chosen + (j,), shadow | masks[j])
    pack(0, (), 0)
    checks = 0
    by_size = Counter()
    min_slack = [None, None]
    for chosen, shadow in families:
        protected = [j for j in range(len(edges)) if shadow >> j & 1]
        degrees = Counter(v for j in protected for v in edges[j])
        delta = max(degrees.values())
        free = full ^ shadow
        sub = free
        while True:
            graph = shadow | sub
            adjacency = [set() for _ in range(n)]
            for j, (u, v) in enumerate(edges):
                if graph >> j & 1:
                    adjacency[u].add(v); adjacency[v].add(u)
            d = min(len(adjacency[u] & adjacency[v]) for j in protected for u, v in [edges[j]])
            available = [j for j, t in enumerate(triples)
                         if t[1] in adjacency[t[0]] and t[2] in adjacency[t[0]]
                         and t[2] in adjacency[t[1]]]
            bad = [j for j in available if j not in chosen and masks[j] & shadow]
            r = len(chosen)
            incidences = sum((masks[j] & shadow).bit_count() for j in bad)
            collisions = sum(comb((masks[j] & shadow).bit_count(), 2) for j in bad)
            assert incidences >= 3 * r * (d - 1)
            assert collisions <= sum(comb(x, 2) for x in degrees.values())
            assert len(bad) >= incidences - collisions
            slack = [len(bad) - r*(d-1), len(bad) - 3*r*(d-delta)]
            assert min(slack) >= 0
            for j in range(2):
                min_slack[j] = slack[j] if min_slack[j] is None else min(slack[j], min_slack[j])
            checks += 1; by_size[r] += 1
            if sub == 0:
                break
            sub = (sub - 1) & free
    assert checks == sum(2**(len(edges)-3*len(f)) for f, _ in families)
    return {'n': n, 'target_packings': len(families), 'graph_family_pairs': checks,
            'pairs_by_family_size': dict(sorted(by_size.items())),
            'minimum_slacks': min_slack, 'all_pass': True}


def exact_algebra():
    checks = 0
    bernoulli = 0
    # Direct expanded margin, preserving the separate final density p_star.
    for n in (400, 1000, 10000):
        h = R(6, n*n)
        for p in (R(1), R(4,5), R(1,2), R(1,10)):
            for p_star in (p, p/2, p/10):
                a = ((p-h)/p)**2
                hazard = 3*(R(99,100)*n*p*p-R(1,10)*n*p_star*p_star)
                direct = 1+hazard-n*(p-h)**2/2-R(101,600)*n**3*p**3*(1-a)
                expanded = 1+R(9,20)*n*p*p-R(3,10)*n*p_star*p_star+R(201,100)*n*p*h-n*h*h/2
                assert direct == expanded
                assert direct > R(3,20)*n*p*p
                checks += 1
                max_r = n*n*p_star*p_star//60
                assert max_r*(1-a) <= R(1,5)
                for r in set([0, 1, 2, min(100, int(max_r)), min(1000, int(max_r))]):
                    assert a**r >= 1-r*(1-a)
                    bernoulli += 1
    # Arbitrarily huge valid n with exact integer stopping rule, no float powers.
    stopping = []
    for base in (7, 10, 100):
        n = base**100
        m = n*n//6-base**199
        p = 1-R(6*m,n*n)
        assert m > 0 and 0 < p < 1
        assert R(6,base) <= p < R(6,base)+R(6,n*n)
        assert R(199,100)+R(1,100) == 2
        assert p**6*n >= 1  # p >= n^(-1/6), the BFL M=3 range
        assert 2/(R(99,100)*n*p*p) <= R(50,891)*R(base**2,n)
        stopping.append({'base': base, 'n_decimal_digits': len(str(n)),
                         'm_positive': True, 'floor_error_exact': str(p-R(6,base)),
                         'bfl_range_verified': True})
    return {'scalar_identity_cases': checks, 'bernoulli_spot_checks': bernoulli,
            'uniform_margin': '3/20', 'max_linear_loss': '1/5',
            'exact_large_n_stopping_checks': stopping,
            'all_k_argument': 'Analytic Bernoulli inequality, not the finite spot checks.'}


def affine_steiner_witness(dimension=5):
    """Use affine lines over F_3, independently of the author's Bose system."""
    s = 3**dimension
    coordinates = [tuple((x//3**j)%3 for j in range(dimension)) for x in range(s)]
    def third(a, b):
        return sum(((-coordinates[a][j]-coordinates[b][j])%3)*3**j for j in range(dimension))
    blocks = set()
    for a, b in combinations(range(s), 2):
        c = third(a, b)
        assert c not in (a, b)
        blocks.add(tuple(sorted((a, b, c))))
    pairs = Counter(e for t in blocks for e in combinations(t, 2))
    assert len(pairs) == comb(s,2) and set(pairs.values()) == {1}
    n = 2*s; r = len(blocks); q = comb(n,3)
    bad = comb(s,3)+comb(s,2)*(n-s)-r
    assert bad == r*(3*n-2*s-3)
    p_next = 1-R(6,n*n)
    bracket = 1-R(r+bad,q)+R(r*n,2*q)*p_next**2
    ratio = bracket/p_next**(2*r)
    assert ratio > 1
    assert n-2 >= R(99,100)*n
    assert R(99,600)*n**3 <= q <= R(101,600)*n**3
    assert n-4 >= R(99,100)*n*p_next**2
    assert R(99,600)*n**3*p_next**3 <= q-(3*n-8) <= R(101,600)*n**3*p_next**3
    assert R(5,8)*(1+R(1,2)+R(1,8)) == R(65,64) > 1
    return {'construction': 'Affine lines over F_3^5', 'n': n, 'subsystem_vertices': s,
            'targets': r, 'protected_pairs': len(pairs), 'bad_triangles': bad,
            'positive_drift_exact': True, 'first_step_survives_trajectory_tests': True,
            'ratio_decimal_diagnostic_only': float(ratio),
            'limit': '(5/8)*exp(1/2)', 'strict_rational_limit_lower_bound': '65/64',
            'not_a_counterexample_to_original_problem': True}


def run():
    return {'status': 'PASS', 'independence': 'No author verifier import; different enumeration and design construction.',
            'terminal_laws': [backwards_terminal(n) for n in range(3,8)],
            'hazards': hazard_exhaustive(), 'algebra': exact_algebra(),
            'dense_potential': affine_steiner_witness(),
            'limitations': ['Not a proof of the imported BFL concentration theorem.',
                'Finite n witness is a potential counterexample, not the asymptotic stopping-time experiment.',
                'The full conditional C/n spread question remains unresolved.']}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output'); args=parser.parse_args()
    result=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    if args.output: Path(args.output).write_text(result)
    print(result,end='')

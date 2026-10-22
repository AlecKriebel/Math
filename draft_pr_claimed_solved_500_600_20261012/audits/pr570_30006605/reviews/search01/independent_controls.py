#!/usr/bin/env python3
"""Independent exact adversaries, no fast general median-graph oracle claimed.

Run with standard-library Python 3; JSON on stdout, no file writes. No imports
from author controls. Distances use Floyd-Warshall; threshold bounds use a direct
scan; row pruning uses bisect on explicitly materialized reference rows. These
choices deliberately differ from the author's BFS/binary-bound implementation.
The n^2 materializations here are tests, not the claimed fast algorithm.
"""
from bisect import bisect_left, bisect_right
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
import random


SEED = 2026101557030006605


def floyd(adj):
    n = len(adj)
    d = [[0 if i == j else (1 if j in adj[i] else n + 1)
          for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d if all(x <= n-1 for row in d for x in row) else None


def is_median(d):
    n = len(d)
    intervals = [[sum((1 << x) for x in range(n)
                     if d[i][x] + d[x][j] == d[i][j])
                  for j in range(n)] for i in range(n)]
    for i, j, k in combinations(range(n), 3):
        mask = intervals[i][j] & intervals[j][k] & intervals[k][i]
        if mask == 0 or mask & (mask - 1):
            return False
    return True


def transformed_sets(d, weights, radius):
    """Return feasible set via additive transform, plus all additive labels."""
    n = len(weights)
    if radius < 0:
        return [], None
    D = n - 1
    # Scan all bounded integer radii; handles zero without division or floor.
    b = [max(k for k in range(n) if k*w <= radius) for w in weights]
    a = [D - bound for bound in b]
    assert all(0 <= x <= D for x in a)
    e = [max(d[x][u] + a[u] for u in range(n)) for x in range(n)]
    return [x for x in range(n) if e[x] <= D], e


def raw_radii(d, weights):
    # Different nesting from threshold oracle: accumulate vertex maxima by u.
    values = [0] * len(weights)
    for u, w in enumerate(weights):
        for x in range(len(weights)):
            values[x] = max(values[x], w*d[x][u])
    return values


def median_pivots(rows, low, stop):
    active = [(rows[i][(low[i]+stop[i]-1)//2], stop[i]-low[i])
              for i in range(len(rows)) if low[i] < stop[i]]
    M = sum(length for _, length in active)
    eligible = sorted({q for q, _ in active
                       if 2*sum(L for a, L in active if a <= q) >= M
                       and 2*sum(L for a, L in active if a >= q) >= M})
    assert bool(eligible) == bool(M)
    return eligible, M


def row_search(rows, threshold_oracle, optimum, mode="high"):
    """Reference version; asserts invariant at every state, returns witness."""
    assert rows and all(row for row in rows)
    B = max(row[-1] for row in rows)
    ok, witness = threshold_oracle(B)
    assert ok
    low = [0] * len(rows)
    stop = list(map(len, rows))
    trace = []
    # Unlike the author, keep zero rows active and run the full generic search
    # even at B=0. This exercises the generic proof independently of shortcuts.
    while any(l < h for l, h in zip(low, stop)):
        assert B == optimum or any(optimum in row[l:h]
                                   for row, l, h in zip(rows, low, stop))
        choices, M = median_pivots(rows, low, stop)
        q = choices[0] if mode == "low" else choices[-1]
        feasible, vertex = threshold_oracle(q)
        if feasible:
            if q < B:
                B, witness = q, vertex
            stop = [bisect_left(row, q, l, h)
                    for row, l, h in zip(rows, low, stop)]
        else:
            low = [bisect_right(row, q, l, h)
                   for row, l, h in zip(rows, low, stop)]
        next_M = sum(h-l for l, h in zip(low, stop))
        assert 4*next_M <= 3*M, (rows, low, stop, q, M, next_M)
        assert next_M < M
        assert B == optimum or any(optimum in row[l:h]
                                   for row, l, h in zip(rows, low, stop))
        trace.append([str(q), feasible, M, next_M])
    assert B == optimum
    return B, witness, trace


def graph_from_edges(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def box(lengths):
    coords = list(product(*(range(n) for n in lengths)))
    edges = [(i, j) for i in range(len(coords)) for j in range(i)
             if sum(abs(a-b) for a, b in zip(coords[i], coords[j])) == 1]
    return graph_from_edges(len(coords), edges)


def gated_cubes():
    """Three squares/cubes sharing gated faces and a pendant path."""
    # Use union of boxes in Z^3; check medianity below rather than assume it.
    coords = sorted(set(product(range(3), range(2), range(2))) |
                    set(product(range(2), range(3), range(2))) |
                    {(0, 0, 2), (0, 0, 3)})
    return graph_from_edges(len(coords), [
        (i, j) for i in range(len(coords)) for j in range(i)
        if sum(abs(a-b) for a, b in zip(coords[i], coords[j])) == 1])


def run():
    counts = Counter()
    graph_digest = sha256()
    row_digest = sha256()
    rng = random.Random(SEED)
    examples = []

    def check_graph(adj, weights, full_thresholds, family, median=None):
        d = floyd(adj)
        assert d is not None
        if median is None:
            median = is_median(d)
        actual = raw_radii(d, weights)
        optimum = min(actual)
        all_centers = [x for x, r in enumerate(actual) if r == optimum]
        rows = [tuple(k*w for k in range(len(weights))) for w in weights]
        calls = 0

        def oracle(R):
            nonlocal calls
            calls += 1
            feasible, labels = transformed_sets(d, weights, R)
            want = [x for x, r in enumerate(actual) if r <= R]
            assert feasible == want
            counts['search_complete_feasible_sets_compared'] += 1
            return bool(feasible), feasible[-1] if feasible else None

        # Highest valid weighted median and last feasible vertex give choices
        # distinct from the author's first cumulative median/first vertex.
        found, witness, trace = row_search(rows, oracle, optimum, "high")
        assert found == optimum and witness in all_centers
        final_set, _ = transformed_sets(d, weights, found)
        assert final_set == all_centers
        counts['optimization_cases'] += 1
        counts['median_optimization_cases'] += int(median)
        counts['zero_optimum_cases'] += int(optimum == 0)
        counts['multiple_center_cases'] += int(len(all_centers) > 1)
        counts['pruning_iterations'] += len(trace)
        counts['max_graph_iterations'] = max(counts['max_graph_iterations'], len(trace))
        # Quantitative termination bound: if 4^t > M0*3^t, M_t=0.
        upper = 0
        while 4**upper <= len(weights)**2 * 3**upper:
            upper += 1
        assert len(trace) <= upper
        values = sorted(set(x for row in rows for x in row))
        tests = {-1, 0, optimum, values[-1] + 1}
        if full_thresholds:
            tests.update(values)
            tests.update(Fraction(a+b, 2) for a, b in zip(values, values[1:]))
        else:
            i = bisect_left(values, optimum)
            if i:
                tests.add(Fraction(values[i-1]+optimum, 2))
                tests.add(values[i-1])
            if i+1 < len(values):
                tests.add(Fraction(values[i+1]+optimum, 2))
            tests.add(values[-1])
        for R in sorted(tests):
            got, _ = transformed_sets(d, weights, R)
            assert got == [x for x, r in enumerate(actual) if r <= R]
            counts['boundary_complete_feasible_sets_compared'] += 1
        graph_digest.update(json.dumps([family, adj, [str(w) for w in weights],
                                       str(found), all_centers, trace],
                                      separators=(',', ':')).encode())
        if family in ('explicit-boundary', 'gated-glue'):
            examples.append({'family': family, 'n': len(weights),
                             'weights': list(map(str, weights)),
                             'radii': list(map(str, actual)),
                             'optimum': str(found), 'centers': all_centers,
                             'saved_witness': witness, 'trace': trace})

    # All connected labelled simple graphs through n=5, and every median graph
    # among them with EVERY profile in {0,1,3}^n. This exceeds the author's
    # exhaustive median coverage n<=4 and uses a different alphabet.
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = graph_from_edges(n, [p for j, p in enumerate(pairs) if mask >> j & 1])
            d = floyd(adj)
            if d is None:
                continue
            counts['connected_graphs_enumerated'] += 1
            median = is_median(d)
            counts['median_graphs_enumerated'] += int(median)
            profiles = product((0, 1, 3), repeat=n) if median else [
                (1,)*n, tuple(3 if i == n-1 else 0 for i in range(n)),
                tuple(rng.randrange(4) for _ in range(n))]
            for weights in profiles:
                check_graph(adj, weights, n <= 4, 'all-labelled-through-five', median)

    # Exact rational and huge-scale boundary profiles, hypercubes, products,
    # glued median pieces, and varied connected nonmedian examples.
    boundary_graphs = [graph_from_edges(1, []), graph_from_edges(2, [(0, 1)]),
                       graph_from_edges(3, [(0, 1), (1, 2)]), box((2, 2)),
                       graph_from_edges(7, [(0, j) for j in range(1, 7)])]
    for adj in boundary_graphs:
        n = len(adj)
        profiles = [[0]*n, [1]*n,
                    [Fraction(0)]*(n-1)+[Fraction(1, 2**1024+1)],
                    [Fraction(2**2048+7, 3) if i % 2 else Fraction(1, 2**2048+9)
                     for i in range(n)],
                    [Fraction(i, 7) for i in range(n)]]
        for weights in profiles:
            check_graph(adj, weights, True, 'explicit-boundary')

    families = [box((2,)*d) for d in range(1, 7)] + [
        box((3, 4)), box((3, 3, 2)), box((4, 4, 3)), gated_cubes()]
    for j, adj in enumerate(families):
        assert is_median(floyd(adj)), j
        counts['larger_median_families'] += 1
        n = len(adj)
        profiles = [[Fraction(rng.randrange(0, 23), rng.randrange(1, 24))
                     for _ in adj] for _ in range(20)]
        profiles.extend([[1]*n, [0]*n,
                         [Fraction(2**(i % 17), 2**4096+17) for i in range(n)],
                         [0]*(n-1)+[Fraction(2**4096+17, 2**2048+9)]])
        for weights in profiles:
            check_graph(adj, weights, False,
                        'gated-glue' if j == len(families)-1 else 'larger-median')

    for _ in range(100):
        n = rng.randrange(6, 19)
        edges = [(i, rng.randrange(i)) for i in range(1, n)]
        edges.extend((i, j) for i, j in combinations(range(n), 2)
                     if (i, j) not in edges and (j, i) not in edges
                     and rng.randrange(7) == 0)
        adj = graph_from_edges(n, edges)
        weights = [Fraction(rng.randrange(31), rng.randrange(1, 31)) for _ in adj]
        check_graph(adj, weights, False, 'generic-connected')

    # A local adversary for the contraction lemma in greater generality than
    # the problem: arbitrary nondecreasing, repeated-entry rows with lengths
    # 0..4 over {0,1,2}. Check EVERY eligible midpoint pivot and BOTH outcomes.
    catalogue = [tuple()] + [row for length in range(1, 5)
                            for row in combinations_with_replacement(range(3), length)]
    for nrows in range(1, 4):
        for rows in product(catalogue, repeat=nrows):
            low = [0]*nrows
            stop = list(map(len, rows))
            pivots, M = median_pivots(rows, low, stop)
            if not M:
                continue
            counts['abstract_row_states'] += 1
            for q in pivots:
                small = sum(bisect_left(row, q) for row in rows)
                large = sum(len(row)-bisect_right(row, q) for row in rows)
                assert 4*small <= 3*M and 4*large <= 3*M
                counts['abstract_outcome_contractions'] += 2
            # End-to-end optimize all possible optimum values. Empty rows are
            # removed before search, as already permitted by the active state.
            active = [row for row in rows if row]
            for optimum in sorted({x for row in active for x in row}):
                def oracle(q):
                    return q >= optimum, 0 if q >= optimum else None
                for mode in ('low', 'high'):
                    B, witness, trace = row_search(active, oracle, optimum, mode)
                    assert B == optimum and witness == 0
                    counts['abstract_optimization_runs'] += 1
                    counts['abstract_search_iterations'] += len(trace)
                    row_digest.update(json.dumps([rows, optimum, mode, trace],
                                                 separators=(',', ':')).encode())

    # Structural edge-read bound: for every subset of Q_4 check the general
    # induced-cube edge inequality m <= n log_2(n)/2 without floating point.
    # Equivalently 2^(2m) <= n^n. Median graphs are isometric cube subgraphs.
    for mask in range(1, 1 << 16):
        n = mask.bit_count()
        m = sum(1 for u in range(16) if mask >> u & 1
                for j in range(4) if (u ^ (1 << j)) < u
                and mask >> (u ^ (1 << j)) & 1)
        assert 2**(2*m) <= n**n
        counts['cube_subset_edge_bound_checks'] += 1

    return {'status': 'PASS', 'seed': SEED,
            'statistics': dict(sorted(counts.items())),
            'graph_cases_sha256': graph_digest.hexdigest(),
            'abstract_cases_sha256': row_digest.hexdigest(),
            'explicit_boundary_results': examples,
            'limits': [
                'Finite controls do not prove a universal theorem.',
                'No fast general median-graph additive oracle is implemented.',
                'The reference rows and Floyd-Warshall tables are quadratic or worse.',
                'No runtime benchmark, human peer review, or proof-assistant certification.'
            ]}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

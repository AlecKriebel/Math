#!/usr/bin/env python3
"""Independent exact falsification tests. This is NOT an implementation of BDH.

No functions are imported from the frozen author controls. Explicit row
enumeration and quadratic graph distances are intentionally used only as small
reference controls, never as evidence for the claimed asymptotic runtime.
"""
from bisect import bisect_left, bisect_right
from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
import hashlib
import json


def row_search(rows, optimum, stats):
    """Use an independent monotone cutoff oracle; exhaust strict tie pruning."""
    active = [(0, len(row)) for row in rows]
    incumbent = max(max(row) for row in rows if row)
    total_initial = sum(len(row) for row in rows)
    steps = 0
    while True:
        mids = sorted((row[(lo + hi - 1) // 2], hi - lo)
                      for row, (lo, hi) in zip(rows, active) if lo < hi)
        total = sum(length for _, length in mids)
        if not total:
            break
        cumulative = 0
        for pivot, length in mids:
            cumulative += length
            if 2 * cumulative >= total:
                break
        assert 2 * sum(length for value, length in mids if value <= pivot) >= total
        assert 2 * sum(length for value, length in mids if value >= pivot) >= total
        feasible = pivot >= optimum
        if feasible:
            incumbent = min(incumbent, pivot)
        new_active = []
        for row, (lo, hi) in zip(rows, active):
            if feasible:
                hi = bisect_left(row, pivot, lo, hi)
            else:
                lo = bisect_right(row, pivot, lo, hi)
            new_active.append((lo, hi))
        new_total = sum(hi - lo for lo, hi in new_active)
        assert 4 * new_total <= 3 * total
        active = new_active
        assert incumbent == optimum or any(
            optimum in row[lo:hi] for row, (lo, hi) in zip(rows, active))
        steps += 1
    assert incumbent == optimum
    # Exact integer version of the logarithmic stopping argument.
    assert (4 ** (steps - 1) <= total_initial * 3 ** (steps - 1)) if steps else True
    stats['implicit_search_cases'] += 1
    stats['contraction_steps'] += steps
    stats['maximum_steps'] = max(stats['maximum_steps'], steps)


def all_distances(adj):
    matrix = []
    for source in range(len(adj)):
        distance = [-1] * len(adj)
        distance[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if distance[v] == -1:
                    distance[v] = distance[u] + 1
                    queue.append(v)
        if -1 in distance:
            return None
        matrix.append(distance)
    return matrix


def main():
    stats = Counter()
    digest = hashlib.sha256()
    # Every triple of nondecreasing rows of length 0..4 over {0,1,2}.
    # This tests arbitrary ties and unequal active-row lengths, beyond rows kw.
    options = [row for length in range(5)
               for row in combinations_with_replacement(range(3), length)]
    for rows in product(options, repeat=3):
        candidates = sorted(set(value for row in rows for value in row))
        if not candidates:
            continue
        stats['arbitrary_sorted_row_families'] += 1
        for optimum in candidates:
            row_search(rows, optimum, stats)

    # All connected labelled graphs through n=5, all 0/1/2 profiles. Both the
    # reduction and the candidate-search argument are graph-independent.
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            adj = [[] for _ in range(n)]
            for index, (u, v) in enumerate(pairs):
                if mask & (1 << index):
                    adj[u].append(v)
                    adj[v].append(u)
            distances = all_distances(adj)
            if distances is None:
                continue
            stats['connected_labelled_graphs'] += 1
            for weights in product(range(3), repeat=n):
                radius = [max(w * d for w, d in zip(weights, row))
                          for row in distances]
                optimum = min(radius)
                rows = [tuple(k * w for k in range(n)) for w in weights]
                row_search(rows, optimum, stats)
                stats['graph_profiles'] += 1
                candidates = sorted(set(value for row in rows for value in row))
                thresholds = [Fraction(-1)] + [Fraction(c) for c in candidates]
                thresholds += [Fraction(a + b, 2)
                               for a, b in zip(candidates, candidates[1:])]
                thresholds += [Fraction(candidates[-1] + 1)]
                for threshold in thresholds:
                    direct = tuple(x for x, value in enumerate(radius) if value <= threshold)
                    if threshold < 0:
                        reduced = ()
                    else:
                        # Deliberately use literal enumeration rather than the
                        # author's binary search or floor formula.
                        bounds = [max(k for k in range(n) if k * w <= threshold)
                                  for w in weights]
                        offsets = [n - 1 - b for b in bounds]
                        reduced = tuple(x for x, row in enumerate(distances)
                                        if max(d + a for d, a in zip(row, offsets)) <= n - 1)
                    assert direct == reduced
                    stats['full_feasible_set_checks'] += 1
                digest.update(json.dumps([n, mask, weights, radius]).encode())
    return {'status': 'PASS', 'statistics': dict(sorted(stats.items())),
            'graph_case_digest_sha256': digest.hexdigest(),
            'limitations': ['Finite controls are not proof of the universal theorem.',
                            'No BDH implementation or performance benchmark.',
                            'Reference graph calculations deliberately use quadratic storage.']}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))

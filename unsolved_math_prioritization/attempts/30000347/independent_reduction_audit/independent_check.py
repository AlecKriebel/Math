#!/usr/bin/env python3
"""Independent finite checks; no code or imports from the author's checker.

These checks do not establish a universal complexity theorem.
"""
from itertools import combinations, product
from functools import cache
from pathlib import Path
from collections import Counter
import hashlib
import json
import time


def graph(parts, hedges, backup=False):
    n = len(parts)
    edges = list(hedges) + [(v, n + parts[v]) for v in range(n)]
    total = n + 3
    if backup:
        for a, b in combinations(range(n, n + 3), 2):
            path = [a, total, total + 1, total + 2, b]
            edges += list(zip(path, path[1:]))
            total += 3
    assert len(set(map(frozenset, edges))) == len(edges)
    assert all(a != b for a, b in edges)
    return total, edges, tuple(range(n, n + 3))


def distances(total, edges, deleted, terminals):
    neighbors = [set() for _ in range(total)]
    for i, (a, b) in enumerate(edges):
        if deleted & (1 << i) == 0:
            neighbors[a].add(b)
            neighbors[b].add(a)
    result = []
    for a, b in combinations(terminals, 2):
        frontier, visited, length = {a}, {a}, 0
        while frontier and b not in frontier:
            frontier = set().union(*(neighbors[v] for v in frontier)) - visited
            visited |= frontier
            length += 1
        result.append(length if frontier else None)
    return tuple(result)


def is_cover(selected, edges):
    return all(selected & (1 << a | 1 << b) for a, b in edges)


def cover_by_subsets(n, edges):
    for size in range(n + 1):
        for chosen in combinations(range(n), size):
            mask = sum(1 << v for v in chosen)
            if is_cover(mask, edges):
                return size
    raise AssertionError


def cover_by_independent_set(n, edges):
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a

    @cache
    def independent(remaining):
        if not remaining:
            return 0
        candidates = [v for v in range(n) if remaining & 1 << v]
        v = max(candidates, key=lambda v: (adj[v] & remaining).bit_count())
        if not adj[v] & remaining:
            return remaining.bit_count()
        removed = remaining & ~(1 << v)
        return max(independent(removed), 1 + independent(removed & ~adj[v]))

    return n - independent((1 << n) - 1)


def subdivision(n, oriented):
    parts = [0] * n
    edges = []
    for a, b in oriented:
        x = len(parts)
        parts += [1, 2]
        edges += [(a, x), (x, x + 1), (x + 1, b)]
    return parts, edges


def small_exhaustive(counts):
    for sizes in ((1, 1, 1), (2, 1, 1), (2, 2, 1)):
        parts = [p for p, size in enumerate(sizes) for _ in range(size)]
        possible = [(a, b) for a, b in combinations(range(len(parts)), 2)
                    if parts[a] != parts[b]]
        for presence in product((False, True), repeat=len(possible)):
            hedges = [e for e, yes in zip(possible, presence) if yes]
            kinds = {frozenset((parts[a], parts[b])) for a, b in hedges}
            if len(kinds) != 3:
                continue
            total, edges, terminals = graph(parts, hedges)
            assert distances(total, edges, 0, terminals) == (3, 3, 3)
            best = len(edges)
            for deleted in range(1 << len(edges)):
                after = distances(total, edges, deleted, terminals)
                feasible = all(d is None or d > 3 for d in after)
                extracted = 0
                for i, (a, b) in enumerate(edges):
                    if deleted & 1 << i:
                        # Select the other endpoint from the author's convention.
                        v = max(a, b) if i < len(hedges) else a
                        extracted |= 1 << v
                covered = is_cover(extracted, hedges)
                if feasible:
                    assert covered
                    assert extracted.bit_count() <= deleted.bit_count()
                    best = min(best, deleted.bit_count())
                    counts['feasible_deletions_mapped'] += 1
                # Check the full hitting criterion independently of BFS.
                hit = all(deleted & ((1 << i) |
                                    (1 << (len(hedges) + a)) |
                                    (1 << (len(hedges) + b)))
                          for i, (a, b) in enumerate(hedges))
                assert feasible == hit
                counts['deletion_sets'] += 1
            assert best == cover_by_subsets(len(parts), hedges)
            btotal, bedges, bterminals = graph(parts, hedges, backup=True)
            assert distances(btotal, bedges, 0, bterminals) == (3, 3, 3)
            for cover in range(1 << len(parts)):
                if is_cover(cover, hedges):
                    deleted = cover << len(hedges)
                    assert distances(btotal, bedges, deleted, bterminals) == (4, 4, 4)
                    counts['backup_cover_sets'] += 1
            counts['tripartite_graphs'] += 1


def composed(counts):
    for n in range(2, 6):
        possible = list(combinations(range(n), 2))
        for flags in product((False, True), repeat=len(possible)):
            base = [e for e, yes in zip(possible, flags) if yes]
            if not base:
                continue
            parts, hedges = subdivision(n, base)
            qtau = cover_by_subsets(n, base)
            htau = cover_by_independent_set(len(parts), hedges)
            assert htau == len(base) + qtau
            total, edges, terminals = graph(parts, hedges)
            assert len(edges) == n + 5 * len(base)
            assert total == n + 2 * len(base) + 3
            assert distances(total, edges, 0, terminals) == (3, 3, 3)
            for k in [0, 1, n - 1, n, n + 1, 2 ** 100]:
                assert (qtau <= k) == (htau <= len(base) + k)
                counts['budget_checks_including_huge_binary_budget'] += 1
            counts['base_graphs'] += 1
    for n in range(2, 5):
        possible = list(combinations(range(n), 2))
        for states in product((0, 1, 2), repeat=len(possible)):
            oriented = [e if flag == 1 else e[::-1]
                        for e, flag in zip(possible, states) if flag]
            if not oriented:
                continue
            parts, hedges = subdivision(n, oriented)
            assert cover_by_independent_set(len(parts), hedges) == (
                len(oriented) + cover_by_subsets(n, oriented))
            assert distances(*graph(parts, hedges)[:2], 0,
                             graph(parts, hedges)[2]) == (3, 3, 3)
            counts['all_endpoint_orderings_through_4_vertices'] += 1


def main():
    started = time.monotonic()
    counts = Counter()
    small_exhaustive(counts)
    composed(counts)
    result = {
        'result': 'PASS',
        'checks': dict(counts),
        'seconds': round(time.monotonic() - started, 3),
        'independent_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limitations': 'Finite tests are supplementary; the written reduction supplies the universal proof.'
    }
    Path(__file__).with_name('independent_check_results.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

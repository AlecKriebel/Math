#!/usr/bin/env python3
"""Fresh finite checks: no import/read of the submitted or earlier checkers.

Distances and all geodesics are discovered from adjacency lists. Exact optima
use a generic hitting-set recurrence, not either claimed optimum identity.
Exhaustive deletions separately compare geodesic hitting with deleted-graph BFS.
"""

from collections import deque
from datetime import datetime, timezone
from functools import lru_cache
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import time


class Graph:
    def __init__(self, n, edges):
        self.n = n
        self.edges = tuple(tuple(sorted(e)) for e in edges)
        assert all(0 <= u < v < n for u, v in self.edges)
        assert len(set(self.edges)) == len(self.edges)
        self.adj = [[] for _ in range(n)]
        for i, (u, v) in enumerate(self.edges):
            self.adj[u].append((v, i))
            self.adj[v].append((u, i))

    def distances(self, source, removed=0):
        ds = [None] * self.n
        ds[source] = 0
        todo = deque([source])
        while todo:
            u = todo.popleft()
            for v, i in self.adj[u]:
                if not (removed >> i & 1) and ds[v] is None:
                    ds[v] = ds[u] + 1
                    todo.append(v)
        return ds

    def geodesics(self, source, target):
        a = self.distances(source)
        b = self.distances(target)
        d = a[target]
        assert d is not None
        found = set()

        def walk(u, mask):
            if u == target:
                found.add(mask)
                return
            for v, i in self.adj[u]:
                if a[v] == a[u] + 1 and b[v] is not None and a[v] + b[v] == d:
                    walk(v, mask | (1 << i))

        walk(source, 0)
        return d, frozenset(found)


def exact_hitting_optimum(constraints):
    constraints = tuple(dict.fromkeys(constraints))
    if not constraints:
        return 0
    incidence = {}
    for j, constraint in enumerate(constraints):
        assert constraint
        bits = constraint
        while bits:
            e = bits & -bits
            bits -= e
            incidence[e] = incidence.get(e, 0) | (1 << j)

    @lru_cache(None)
    def solve(unhit):
        if not unhit:
            return 0
        j = (unhit & -unhit).bit_length() - 1
        bits = constraints[j]
        costs = []
        while bits:
            e = bits & -bits
            bits -= e
            costs.append(1 + solve(unhit & ~incidence[e]))
        return min(costs)

    return solve((1 << len(constraints)) - 1)


def cover_optimum(graph):
    return exact_hitting_optimum([(1 << u) | (1 << v) for u, v in graph.edges])


def is_cover(graph, mask):
    return all(mask & ((1 << u) | (1 << v)) for u, v in graph.edges)


def make_spokes(graph, parts):
    assert len(parts) == graph.n
    terms = tuple(range(graph.n, graph.n + 3))
    spokes = [(v, terms[parts[v]]) for v in range(graph.n)]
    return Graph(graph.n + 3, graph.edges + tuple(spokes)), terms


def add_backups(graph, terms):
    edges = list(graph.edges)
    n = graph.n
    for a, b in combinations(terms, 2):
        internal = [n, n + 1, n + 2]
        n += 3
        chain = [a] + internal + [b]
        edges.extend(zip(chain, chain[1:]))
    return Graph(n, edges)


def terminal_data(graph, terms):
    ds = []
    paths = set()
    for a, b in combinations(terms, 2):
        d, ps = graph.geodesics(a, b)
        ds.append(d)
        paths.update(ps)
    return tuple(ds), frozenset(paths)


def residual_distances(graph, terms, removed):
    result = []
    for a, b in combinations(terms, 2):
        result.append(graph.distances(a, removed)[b])
    return tuple(result)


def blocked_distances(ds, original):
    return all(d is None or d > old for d, old in zip(ds, original))


def extracted_cover(h, removed, high):
    x = 0
    m = len(h.edges)
    for i, (u, v) in enumerate(h.edges):
        if removed >> i & 1:
            x |= 1 << (v if high else u)
    for v in range(h.n):
        if removed >> (m + v) & 1:
            x |= 1 << v
    return x


def tripartite_instances(sizes):
    parts = tuple(p for p, size in enumerate(sizes) for _ in range(size))
    possible = tuple((u, v) for u, v in combinations(range(sum(sizes)), 2)
                     if parts[u] != parts[v])
    for mask in range(1 << len(possible)):
        edges = tuple(e for i, e in enumerate(possible) if mask >> i & 1)
        types = {tuple(sorted((parts[u], parts[v]))) for u, v in edges}
        if types == {(0, 1), (0, 2), (1, 2)}:
            yield Graph(sum(sizes), edges), parts


def subdivision(q, orientations):
    edges = []
    m = len(q.edges)
    # Distinct contiguous B and C blocks deliberately differ from many
    # alternating-index encodings and test order independence.
    for j, ((x, y), direction) in enumerate(zip(q.edges, orientations)):
        u, v = (y, x) if direction else (x, y)
        b, c = q.n + j, q.n + m + j
        edges.extend(((u, b), (b, c), (c, v)))
    parts = (0,) * q.n + (1,) * m + (2,) * m
    return Graph(q.n + 2 * m, edges), parts


def check_subdivision_maps(q, h, orientations, counts):
    m = len(q.edges)
    for s in range(1 << q.n):
        if not is_cover(q, s):
            continue
        x = s
        for j, ((a, b), direction) in enumerate(zip(q.edges, orientations)):
            u, v = (b, a) if direction else (a, b)
            # If the initial endpoint belongs to the source cover, choose C;
            # otherwise choose B. This also handles both endpoints selected.
            selected = q.n + m + j if s >> u & 1 else q.n + j
            x |= 1 << selected
        assert is_cover(h, x)
        assert x.bit_count() == s.bit_count() + m
        counts['subdivision_forward_cover_maps'] += 1
    if q.n <= 3:
        for x in range(1 << h.n):
            if not is_cover(h, x):
                continue
            s = x & ((1 << q.n) - 1)
            sprime = s
            uncovered = 0
            for u, v in q.edges:
                if not s & ((1 << u) | (1 << v)):
                    uncovered += 1
                    sprime |= 1 << u
            assert x.bit_count() >= s.bit_count() + m + uncovered
            assert is_cover(q, sprime)
            assert sprime.bit_count() <= x.bit_count() - m
            counts['subdivision_reverse_cover_maps'] += 1


def main():
    start = time.monotonic()
    counts = {
        'arbitrary_deletion_graphs': 0, 'arbitrary_deletion_subsets': 0,
        'feasible_blockers': 0, 'endpoint_extraction_checks': 0,
        'tripartite_optimum_graphs': 0, 'subdivision_orientation_instances': 0,
        'subdivision_forward_cover_maps': 0, 'subdivision_reverse_cover_maps': 0,
        'composed_budget_comparisons': 0, 'finite_cover_checks': 0,
        'finite_arbitrary_subsets': 0, 'finite_feasible_blockers': 0,
        'finite_terminal_blockers': 0, 'exact_four_blockers': 0,
    }

    for sizes in ((1, 1, 1), (1, 1, 2), (1, 2, 2)):
        for h, parts in tripartite_instances(sizes):
            g, terms = make_spokes(h, parts)
            original, paths = terminal_data(g, terms)
            assert original == (3, 3, 3)
            expected = frozenset((1 << j) | (1 << (len(h.edges) + u)) |
                                 (1 << (len(h.edges) + v))
                                 for j, (u, v) in enumerate(h.edges))
            assert paths == expected
            counts['arbitrary_deletion_graphs'] += 1
            best = len(g.edges)
            for f in range(1 << len(g.edges)):
                ds = residual_distances(g, terms, f)
                bfs_ok = blocked_distances(ds, original)
                hit_ok = all(f & p for p in paths)
                assert bfs_ok == hit_ok
                counts['arbitrary_deletion_subsets'] += 1
                if bfs_ok:
                    counts['feasible_blockers'] += 1
                    best = min(best, f.bit_count())
                    for high in (False, True):
                        x = extracted_cover(h, f, high)
                        assert is_cover(h, x) and x.bit_count() <= f.bit_count()
                        counts['endpoint_extraction_checks'] += 1
            assert best == cover_optimum(h) == exact_hitting_optimum(paths)

            augmented = add_backups(g, terms)
            assert terminal_data(augmented, terms) == (original, paths)
            for x in range(1 << h.n):
                if is_cover(h, x):
                    f = x << len(h.edges)
                    assert residual_distances(augmented, terms, f) == (4, 4, 4)
                    counts['finite_cover_checks'] += 1

    for h, parts in tripartite_instances((2, 2, 2)):
        g, terms = make_spokes(h, parts)
        original, paths = terminal_data(g, terms)
        assert original == (3, 3, 3)
        expected = frozenset((1 << j) | (1 << (len(h.edges) + u)) |
                             (1 << (len(h.edges) + v))
                             for j, (u, v) in enumerate(h.edges))
        assert paths == expected
        assert exact_hitting_optimum(paths) == cover_optimum(h)
        counts['tripartite_optimum_graphs'] += 1

    for n in range(6):
        possible = tuple(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            q = Graph(n, [e for j, e in enumerate(possible) if mask >> j & 1])
            m = len(q.edges)
            # All orientations through order four; two opposite orientations
            # for every order-five graph. Includes isolated and edgeless graphs.
            directions = product((0, 1), repeat=m) if n <= 4 else (
                [(0,) * m, (1,) * m] if m else [()])
            qopt = cover_optimum(q)
            for orient in directions:
                h, parts = subdivision(q, orient)
                assert cover_optimum(h) == m + qopt
                check_subdivision_maps(q, h, orient, counts)
                counts['subdivision_orientation_instances'] += 1
                if not m:
                    continue
                g, terms = make_spokes(h, parts)
                assert len(g.edges) == n + 5 * m
                assert g.n == n + 2 * m + 3
                original, paths = terminal_data(g, terms)
                assert original == (3, 3, 3)
                opt = exact_hitting_optimum(paths)
                assert opt == m + qopt
                for k in list(range(n + 2)) + [1 << 512]:
                    assert (qopt <= k) == (opt <= m + k)
                    counts['composed_budget_comparisons'] += 1

    h = Graph(3, ((0, 1), (0, 2), (1, 2)))
    g, terms = make_spokes(h, (0, 1, 2))
    augmented = add_backups(g, terms)
    original, paths = terminal_data(augmented, terms)
    assert original == (3, 3, 3)
    opt_all = opt_finite = opt_exact = len(augmented.edges)
    for f in range(1 << len(augmented.edges)):
        ds = residual_distances(augmented, terms, f)
        bfs_ok = blocked_distances(ds, original)
        assert bfs_ok == all(f & p for p in paths)
        counts['finite_arbitrary_subsets'] += 1
        if bfs_ok:
            counts['finite_feasible_blockers'] += 1
            opt_all = min(opt_all, f.bit_count())
            for high in (False, True):
                x = extracted_cover(h, f, high)
                assert is_cover(h, x) and x.bit_count() <= f.bit_count()
            if all(d is not None for d in ds):
                counts['finite_terminal_blockers'] += 1
                opt_finite = min(opt_finite, f.bit_count())
            if ds == (4, 4, 4):
                counts['exact_four_blockers'] += 1
                opt_exact = min(opt_exact, f.bit_count())
    assert opt_all == opt_finite == opt_exact == 2

    # Total-reduction fixed yes-instance for every source m=0 and k>=0.
    assert exact_hitting_optimum(terminal_data(g, terms)[1]) <= 2

    # Falsification controls: omitted hypotheses must cause known failures.
    missing_type = Graph(3, ((0, 1), (0, 2)))
    mg, mt = make_spokes(missing_type, (0, 1, 2))
    md, mp = terminal_data(mg, mt)
    assert md == (3, 3, 4)
    assert cover_optimum(missing_type) == 1
    assert exact_hitting_optimum(mp) == 2
    # Cross-part triangle plus a disjoint triangle internal to A.
    nontripartite = Graph(6, ((0, 1), (1, 2), (0, 2),
                            (3, 4), (3, 5), (4, 5)))
    ng, nt = make_spokes(nontripartite, (0, 0, 0, 0, 1, 2))
    nd, np = terminal_data(ng, nt)
    assert nd == (3, 3, 3)
    assert cover_optimum(nontripartite) == 4
    assert exact_hitting_optimum(np) == 2

    results = {
        'status': 'PASS', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'seconds': round(time.monotonic() - start, 3), 'counts': counts,
        'finite_optima': {'unrestricted': opt_all, 'finite': opt_finite,
                          'exact_3_to_4': opt_exact},
        'negative_controls': {
            'omitted_cross_type': {'distances': md, 'cover_optimum': 1,
                                  'blocker_optimum': 2},
            'intra_part_edges': {'distances': nd, 'cover_optimum': 4,
                                'blocker_optimum': 2},
        },
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limitations': 'Finite checks supplement the universal proof; no priority claim audited.'
    }
    output = Path(__file__).with_name('independent_results.json')
    output.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

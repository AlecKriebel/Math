#!/usr/bin/env python3
"""Fresh reviewer tests; no imports from the submitted verification code."""
from collections import deque
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def distance(vertices, edges, start, finish, deleted=frozenset()):
    neighbors = [[] for _ in range(vertices)]
    for i, (u, v) in enumerate(edges):
        if i not in deleted:
            neighbors[u].append(v)
            neighbors[v].append(u)
    d = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == finish:
            return d[u]
        for v in neighbors[u]:
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return float('inf')


def cover_number(vertices, edges):
    for size in range(vertices + 1):
        for choice in combinations(range(vertices), size):
            s = set(choice)
            if all(u in s or v in s for u, v in edges):
                return size
    raise RuntimeError('missing vertex cover')


def main():
    subdivision_instances = 0
    for n in range(5):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            q = [e for i, e in enumerate(possible) if mask >> i & 1]
            h = []
            for i, (u, v) in enumerate(q):
                b, c = n + 2 * i, n + 2 * i + 1
                h.extend([(u, b), (b, c), (c, v)])
            require(cover_number(n + 2 * len(q), h) == len(q) + cover_number(n, q),
                    'subdivision identity')
            subdivision_instances += 1

    tripartite_instances = deletion_subsets = feasible_subsets = backup_subsets = 0
    for sizes in [(1, 1, 1), (1, 1, 2), (1, 2, 2)]:
        w = sum(sizes)
        parts = [0] * sizes[0] + [1] * sizes[1] + [2] * sizes[2]
        possible = [(u, v) for u, v in combinations(range(w), 2) if parts[u] != parts[v]]
        for mask in range(1 << len(possible)):
            h = [e for i, e in enumerate(possible) if mask >> i & 1]
            types = {tuple(sorted((parts[u], parts[v]))) for u, v in h}
            if len(types) != 3:
                continue
            tau = cover_number(w, h)
            edges = [(w + parts[v], v) for v in range(w)] + h
            pairs = list(combinations(range(w, w + 3), 2))
            require(all(distance(w + 3, edges, a, b) == 3 for a, b in pairs), 'initial distances')
            triple_masks = [(1 << u) | (1 << v) | (1 << (w + i))
                            for i, (u, v) in enumerate(h)]
            optimum = len(edges)
            for fmask in range(1 << len(edges)):
                deletion_subsets += 1
                hit = all(fmask & triple for triple in triple_masks)
                # Independently check every deletion with BFS for the smaller partitions,
                # and all size <= tau+1 masks for the larger partition.
                if w <= 4 or fmask.bit_count() <= tau + 1:
                    deleted = {i for i in range(len(edges)) if fmask >> i & 1}
                    bfs_hit = all(distance(w + 3, edges, a, b, deleted) >= 4 for a, b in pairs)
                    require(hit == bfs_hit, 'path family not exact')
                if hit:
                    feasible_subsets += 1
                    optimum = min(optimum, fmask.bit_count())
                    extracted = {v for v in range(w) if fmask >> v & 1}
                    extracted.update(u for i, (u, v) in enumerate(h) if fmask >> (w + i) & 1)
                    require(len(extracted) <= fmask.bit_count(), 'cover extraction size')
                    require(all(u in extracted or v in extracted for u, v in h), 'cover extraction coverage')
            require(optimum == tau, 'blocker optimum')
            # Entire binary-budget semantics, including an input independent huge integer.
            for budget in [0, tau - 1, tau, tau + 1, len(edges), 2 ** 1000]:
                require((optimum <= budget) == (tau <= budget), 'budget classification')

            if w <= 4:
                backed = list(edges)
                nv = w + 3
                for a, b in pairs:
                    backed.extend([(a, nv), (nv, nv + 1), (nv + 1, nv + 2), (nv + 2, b)])
                    nv += 3
                require(all(distance(nv, backed, a, b) == 3 for a, b in pairs), 'backup shortens initial path')
                opt_finite = opt_exact = None
                # Enumerate all subsets through tau: proves no smaller feasible solution
                # and finds both strengthened optima, including arbitrary backup deletions.
                for size in range(tau + 1):
                    for choice in combinations(range(len(backed)), size):
                        backup_subsets += 1
                        ds = [distance(nv, backed, a, b, set(choice)) for a, b in pairs]
                        if all(4 <= d < float('inf') for d in ds):
                            opt_finite = size if opt_finite is None else min(opt_finite, size)
                        if all(d == 4 for d in ds):
                            opt_exact = size if opt_exact is None else min(opt_exact, size)
                require(opt_finite == tau and opt_exact == tau, 'strengthened optima')
            tripartite_instances += 1

    # Meaningful negative control: retaining just two demand pairs is not enough.
    # For a triangle H, blocking two demands needs one spoke, while VC(H)=2.
    h = [(0, 1), (0, 2), (1, 2)]
    edges = [(3, 0), (4, 1), (5, 2)] + h
    require(distance(6, edges, 3, 4, {0}) >= 4, 'negative control pair1')
    require(distance(6, edges, 3, 5, {0}) >= 4, 'negative control pair2')
    require(distance(6, edges, 4, 5, {0}) == 3, 'negative control detects missing third demand')
    result = dict(status='PASS', subdivision_instances=subdivision_instances,
                  tripartite_instances=tripartite_instances, deletion_subsets=deletion_subsets,
                  feasible_subsets=feasible_subsets, backup_subsets=backup_subsets,
                  negative_control='third-demand omission detected',
                  optimization_safe=True, imports_from_submission=False)
    Path(__file__).with_name('independent_full_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

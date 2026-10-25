"""Independent finite diagnostics; no supplied package code is imported.

Only --write writes, solely to CONTROL_RESULTS.json beside this file.
The exhaustive masks are diagnostics, not a proof for arbitrary graphs.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def cover_number(n, edges):
    for size in range(n + 1):
        for vertices in itertools.combinations(range(n), size):
            chosen = set(vertices)
            if all(u in chosen or v in chosen for u, v in edges):
                return size
    raise AssertionError("no cover")


def construct(n, qedges):
    hedges = []
    for j, (u, v) in enumerate(qedges):
        b, c = n + 2 * j, n + 2 * j + 1
        hedges.extend(((u, b), (b, c), (c, v)))
    hn = n + 2 * len(qedges)
    terminals = (hn, hn + 1, hn + 2)
    spoke_term = [terminals[0]] * n
    for _ in qedges:
        spoke_term.extend((terminals[1], terminals[2]))
    edges = list(hedges) + [(v, spoke_term[v]) for v in range(hn)]
    return hn, hedges, terminals, edges


def distances(n, edges, terminals, removed):
    adjacency = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        if not (removed >> i) & 1:
            adjacency[u].append(v)
            adjacency[v].append(u)
    answer = []
    for j, root in enumerate(terminals[:2]):
        dist = {root: 0}
        queue = collections.deque([root])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        answer.extend(dist.get(target, 10**6) for target in terminals[j + 1:])
    return answer


def run():
    rows = []
    mask_count = feasible_count = backup_covers = 0
    digest = hashlib.sha256()
    for n in (2, 3):
        complete = list(itertools.combinations(range(n), 2))
        for qmask in range(1, 1 << len(complete)):
            qedges = [e for j, e in enumerate(complete) if (qmask >> j) & 1]
            hn, hedges, terminals, edges = construct(n, qedges)
            tauq = cover_number(n, qedges)
            tauh = cover_number(hn, hedges)
            assert tauh == len(qedges) + tauq
            assert distances(hn + 3, edges, terminals, 0) == [3, 3, 3]
            opt = len(edges) + 1
            feasible = 0
            middle_only = False
            for removed in range(1 << len(edges)):
                mask_count += 1
                ds = distances(hn + 3, edges, terminals, removed)
                valid = all(d >= 4 for d in ds)
                # An independent exact hyperedge hitting predicate.
                hit = all(
                    ((removed >> j) & 1)
                    or ((removed >> (len(hedges) + u)) & 1)
                    or ((removed >> (len(hedges) + v)) & 1)
                    for j, (u, v) in enumerate(hedges)
                )
                assert valid == hit
                if not valid:
                    continue
                feasible += 1
                feasible_count += 1
                opt = min(opt, removed.bit_count())
                selected = set()
                for j, (u, v) in enumerate(edges):
                    if (removed >> j) & 1:
                        selected.add(u)  # H endpoint for spokes and H edges.
                assert len(selected) <= removed.bit_count()
                assert all(u in selected or v in selected for u, v in hedges)
                middle_only |= not (removed >> len(hedges))
            assert opt == tauh
            assert middle_only  # Removing all H edges is valid with no spokes.
            augmented = list(edges)
            next_node = hn + 3
            for a, b in itertools.combinations(terminals, 2):
                path = [a, next_node, next_node + 1, next_node + 2, b]
                next_node += 3
                augmented.extend(zip(path, path[1:]))
            for xmask in range(1 << hn):
                if not all(((xmask >> u) | (xmask >> v)) & 1 for u, v in hedges):
                    continue
                removed = xmask << len(hedges)
                assert distances(next_node, augmented, terminals, removed) == [4, 4, 4]
                backup_covers += 1
            row = dict(n=n, qmask=qmask, m=len(qedges), tau_q=tauq,
                       tau_h=tauh, optimum_blocker=opt,
                       deletion_masks=1 << len(edges), feasible_masks=feasible,
                       all_h_edges_no_spokes_control=True)
            rows.append(row)
            digest.update(json.dumps(row, sort_keys=True).encode())
    # Boundary: edgeless original maps to the fixed H triangle, budget two.
    tri_edges = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 4), (2, 5)]
    assert distances(6, tri_edges, (3, 4, 5), 0) == [3, 3, 3]
    assert all(d >= 4 for d in distances(6, tri_edges, (3, 4, 5), (1 << 3) | (1 << 4)))
    assert not all(d >= 4 for d in distances(6, tri_edges, (3, 4, 5), 1 << 3))
    return dict(scope="finite exact diagnostic only; universal proof separate",
                original_graphs=len(rows), arbitrary_deletion_masks=mask_count,
                feasible_masks_with_cover_extraction=feasible_count,
                backup_cover_checks=backup_covers, rows=rows,
                boundary_fixed_yes_and_budget_one_no=True,
                deterministic_rows_sha256=digest.hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run()
    target = Path(__file__).with_name("CONTROL_RESULTS.json")
    if args.write:
        target.write_text(json.dumps(result, indent=2) + "\n")
    else:
        assert result == json.loads(target.read_text())
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, sort_keys=True))

#!/usr/bin/env python3
"""Independent stdlib replay: reconstruct the graph using tree geodesics.

No imports from the candidate verifier, constructor, or numeric graph generator.
The integer labels are breadth-first labels in a degree-three rooted tree.
The end direction is determined by distance to a point beyond the audited ball.
"""
import gzip
import hashlib
import json
import sys
from collections import deque
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def replay(path):
    raw = Path(path).read_bytes()
    c = json.loads(gzip.decompress(raw))
    need(c['q'] == 2 and c['radius'] == 10, 'wrong graph parameters')
    # Work in a larger TREE, first without any directed parent relation.
    tree = [[]]
    depth = [0]
    for u in range(3 * 2**14 - 2):
        if depth[u] == 14:
            continue
        for _ in range(3 if u == 0 else 2):
            v = len(tree)
            tree.append([u])
            tree[u].append(v)
            depth.append(depth[u] + 1)
    end_point = 0
    for _ in range(14):
        end_point = next(v for v in tree[end_point] if depth[v] > depth[end_point])
    distance = [-1] * len(tree)
    distance[end_point] = 0
    queue = deque([end_point])
    while queue:
        u = queue.popleft()
        for v in tree[u]:
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                queue.append(v)
    parent = [None] * len(tree)
    for u in range(len(tree)):
        if u != end_point:
            toward = [v for v in tree[u] if distance[v] < distance[u]]
            need(len(toward) == 1, 'tree geodesic not unique')
            parent[u] = toward[0]
    full_edges = set()
    for u, p in enumerate(parent):
        if p is not None:
            full_edges.add(tuple(sorted((u, p))))
            if parent[p] is not None:
                full_edges.add(tuple(sorted((u, parent[p]))))
    inner = {u for u, d in enumerate(depth) if d <= 10}
    n = len(inner)
    need(inner == set(range(n)) and n == 3070, 'inner vertex labels')
    original = {e for e in full_edges if set(e) <= inner}
    full_adj = [set() for _ in tree]
    small_adj = [set() for _ in range(n)]
    for a, b in full_edges:
        full_adj[a].add(b)
        full_adj[b].add(a)
    for a, b in original:
        small_adj[a].add(b)
        small_adj[b].add(a)
    expected_edges = set(original)
    for a in range(n):
        for middle in small_adj[a]:
            for b in small_adj[middle]:
                if a != b:
                    expected_edges.add(tuple(sorted((a, b))))
    full_neighborhood = set(full_adj[0])
    for middle in full_adj[0]:
        full_neighborhood.update(full_adj[middle])
    full_neighborhood.discard(0)
    local_neighborhood = {b if a == 0 else a for a, b in expected_edges if 0 in (a, b)}
    need(full_neighborhood == local_neighborhood, 'omitted square-root neighbor')
    need(len(full_neighborhood) == 40, 'unexpected full root degree')
    need(max(depth[v] for v in full_neighborhood) == 4, 'root radius')
    need(c['vertices'] == n, 'vertex count')
    need(c['edge_order'] == [list(e) for e in sorted(expected_edges)], 'edge set mismatch')
    need(c['root_neighbors'] == sorted(full_neighborhood), 'neighbor order mismatch')
    need(len(c['flows']) == 40, 'flow count')
    need(type(c['denominator']) is int and c['denominator'] > 0, 'bad denominator')
    D = c['denominator']
    energies = []
    for sink, flow in zip(c['root_neighbors'], c['flows']):
        need(len(flow) == len(expected_edges), 'flow length')
        net_in = [0] * n
        energy = 0
        for edge, value in zip(c['edge_order'], flow):
            need(type(value) is int, 'noninteger flow')
            low, high = edge
            net_in[low] -= value
            net_in[high] += value
            energy += value * value
        need(net_in[0] == D and net_in[sink] == -D, 'terminal flow mismatch')
        need(all(balance == 0 for u, balance in enumerate(net_in) if u not in (0, sink)), 'interior flow imbalance')
        energies.append(energy)
    total = sum(energies)
    need(c['energy_numerators'] == energies, 'per-flow energy mismatch')
    need(c['total_energy_numerator'] == total, 'total numerator mismatch')
    need(c['total_energy_denominator'] == D * D, 'total denominator mismatch')
    need(total == 3208526010913748780 and D * D == 10**18, 'unexpected exact bound')
    need(100 * total < 321 * D * D, 'strict square upper bound failed')
    # Pure integer check of the lower-bound radical comparison.
    need(2 * 50**2 < 73**2, 'sqrt(2) < 73/50 failed')
    need(50 * 24 - 73 == 7 * 161, 'original lower-bound arithmetic failed')
    return {
        'verdict': 'PASS',
        'certificate_sha256': hashlib.sha256(raw).hexdigest(),
        'certificate_bytes': len(raw),
        'vertices': n,
        'original_edges': len(original),
        'square_edges': len(expected_edges),
        'complete_square_root_degree': len(full_neighborhood),
        'root_neighbor_max_tree_distance': 4,
        'flow_entries_checked': len(expected_edges) * len(c['flows']),
        'exact_energy_numerator': total,
        'exact_energy_denominator': D * D,
        'strict_expected_degree_bounds': 'G^2 < 321/100 < 161/50 < G',
    }


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'analysis_graph_square_1893/square_flow_certificate.json.gz'
    print(json.dumps(replay(path), indent=2))

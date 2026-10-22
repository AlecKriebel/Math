"""Independent subset-DP cycle oracle. Standard library; checks survive -O.
Finite tests support the separate analytic audit and do not prove EP-642.
"""
import collections
import sys
sys.dont_write_bytecode = True
import importlib.util
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    spec = importlib.util.spec_from_file_location('candidate', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def oracle(n, edges):
    """Count unoriented simple cycles by vertex subset using Held-Karp paths.
    Every path starts at its least vertex. Closing paths are paired by reversal.
    This does not call or reproduce the author's DFS cycle generator.
    """
    neighbors = [0] * n
    edge_set = set()
    for u, v in edges:
        require(0 <= u < n and 0 <= v < n and u != v, 'invalid oracle edge')
        edge_set.add(tuple(sorted((u, v))))
        neighbors[u] |= 1 << v
        neighbors[v] |= 1 << u
    counts = {}
    for start in range(n):
        dp = {(1 << start, start): 1}
        for mask in range(1 << start, 1 << n):
            if not mask & (1 << start) or mask & ((1 << start) - 1):
                continue
            size = mask.bit_count()
            closed = 0
            for last in range(start, n):
                ways = dp.get((mask, last), 0)
                if not ways:
                    continue
                if size >= 3 and neighbors[last] & (1 << start):
                    closed += ways
                available = neighbors[last] & ~mask & ~((1 << (start + 1)) - 1)
                while available:
                    bit = available & -available
                    available -= bit
                    nxt = bit.bit_length() - 1
                    key = (mask | bit, nxt)
                    dp[key] = dp.get(key, 0) + ways
            if closed:
                require(closed % 2 == 0, 'cycle orientation parity')
                counts[mask] = closed // 2
    cycle_count = sum(counts.values())
    margin = None
    violating = 0
    max_length = 0
    boundary_rows = []
    for mask, count in counts.items():
        length = mask.bit_count()
        induced = sum(bool(mask & (1 << u) and mask & (1 << v)) for u, v in edge_set)
        q = induced - length
        boundary = sum(bool(mask & (1 << u)) != bool(mask & (1 << v)) for u, v in edge_set)
        surplus = sum(neighbors[v].bit_count() - 4 for v in range(n) if mask & (1 << v))
        require(2 * (q - length) == surplus - boundary, 'independent boundary identity')
        boundary_rows.append((length, q, boundary))
        max_length = max(max_length, length)
        margin = q - length if margin is None else max(margin, q - length)
        if q >= length:
            violating += count
    summary = {'vertices': n, 'edges': len(edge_set), 'cycles': cycle_count,
               'max_cycle_length': max_length, 'max_chords_minus_length': margin,
               'violating_cycles': violating}
    # Independent component classification, using union-find rather than DFS.
    parent = list(range(n))
    def find(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for u, v in edge_set:
        parent[find(u)] = find(v)
    component_masks = {}
    for v in range(n):
        component_masks[find(v)] = component_masks.get(find(v), 0) | (1 << v)
    if max((x.bit_count() for x in neighbors), default=0) <= 4:
        classified = any(counts.get(mask, 0) > 0 and
                         all(neighbors[v].bit_count() == 4 for v in range(n) if mask & (1 << v))
                         for mask in component_masks.values())
        require(bool(violating) == classified, 'independent component classification')
    return summary, counts, boundary_rows


def compare(module, n, edges):
    expected, counts, rows = oracle(n, edges)
    actual_graph = module.graph(n, edges)
    actual = module.check(actual_graph)
    require(actual == expected, f'candidate summary differs for order {n}')
    emitted = list(module.cycles(actual_graph))
    require(len(emitted) == len(set(emitted)), 'duplicate cycle tuple')
    actual_counts = collections.Counter(sum(1 << v for v in c) for c in emitted)
    require(actual_counts == counts, 'candidate cycle subset counts differ')
    for c in emitted:
        require(len(c) >= 3 and len(set(c)) == len(c), 'not a simple cycle')
        require(c[0] == min(c) and c[1] < c[-1], 'cycle is not canonical')
        require(all(c[(i+1) % len(c)] in actual_graph[c[i]] for i in range(len(c))), 'non-edge in cycle')
    return expected, rows


def run(path):
    module = load(path)
    tested = 0
    for n in range(6):
        possible = list(itertools.combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [e for i, e in enumerate(possible) if mask & (1 << i)]
            compare(module, n, edges)
            tested += 1
    require(tested == 1100, 'wrong finite graph count')
    edges = []
    for offset in (0, 5):
        edges += [(u+offset, v+offset) for u, v in itertools.combinations(range(5), 2) if (u, v) != (0, 1)]
        edges += [(10, offset), (10, offset+1)]
    example, rows = compare(module, 11, edges)
    require(example == {'vertices':11,'edges':22,'cycles':74,'max_cycle_length':6,'max_chords_minus_length':-1,'violating_cycles':0}, 'example expected counts')
    require(all(boundary > 0 for _, _, boundary in rows), 'example has cycle with no boundary')
    require(all(q == 5 and boundary == 2 for length, q, boundary in rows if length == 6), 'longest-cycle exact margin')
    families = []
    for n in range(6, 12):
        result, _ = compare(module, n, [(u,v) for u in range(3) for v in range(3,n)])
        b = n - 3
        expected_cycles = 3 * (b*(b-1)//2) + 6 * (b*(b-1)*(b-2)//6)
        require(result['edges'] == 3*n-9 and result['cycles'] == expected_cycles and result['violating_cycles'] == 0, 'family formula')
        families.append(result)
    # K5 is the equality witness; K5 plus an isolated vertex tests component scope.
    k5, _ = compare(module, 5, list(itertools.combinations(range(5), 2)))
    isolated, _ = compare(module, 6, list(itertools.combinations(range(5), 2)))
    require(k5['violating_cycles'] == 12 and isolated['violating_cycles'] == 12, 'density equality witness')
    return {'passed':True, 'all_labeled_graphs_orders_0_through_5':tested,
            'eleven_vertex_example':example, 'complete_bipartite_family':families,
            'equality_witnesses':{'K5':12,'K5_plus_isolated_vertex':12},
            'independent_oracle':'subset dynamic programming with orientation pairing',
            'scope':'Finite checks only; no solution or asymptotic improvement.'}


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('candidate', type=Path)
    args = p.parse_args()
    print(json.dumps(run(args.candidate.resolve()), indent=2))

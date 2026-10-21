"""Finite checks for the authored cover/apex bridge. No external dependencies."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
HERE = Path(__file__).resolve().parent

def pairs(n):
    return list(combinations(range(n), 2))

def graph_edges(n, mask):
    return {p for i, p in enumerate(pairs(n)) if mask >> i & 1}

def colorable(n, edges, removed=None):
    verts = [v for v in range(n) if v != removed]
    for cs in product(range(3), repeat=len(verts)):
        c = dict(zip(verts, cs))
        if all((u == removed or v == removed or c[u] != c[v] for u, v in edges)):
            return True
    return False

def in_property(n, edges):
    if any((all((tuple(sorted(e)) in edges for e in combinations(vs, 2))) for vs in combinations(range(n), 4))):
        return False
    return colorable(n, edges) or any((colorable(n, edges, a) for a in range(n)))

def triangle_deletions(n, edges):
    es = sorted(edges)
    idx = {p: i for i, p in enumerate(es)}
    tris = []
    for vs in combinations(range(n), 3):
        te = [tuple(sorted(e)) for e in combinations(vs, 2)]
        if all((e in idx for e in te)):
            tris.append(sum((1 << idx[e] for e in te)))
    if not tris:
        return 0
    covers = [sum((1 << t for t, tri in enumerate(tris) if tri >> e & 1)) for e in range(len(es))]
    tri_vars = [[i for i in range(len(es)) if tri >> i & 1] for tri in tris]

    @lru_cache(None)
    def solve(state):
        if not state:
            return 0
        alive = [t for t in range(len(tris)) if state >> t & 1]
        t = max(alive, key=lambda t: sum(((state & covers[e]).bit_count() for e in tri_vars[t])))
        return 1 + min((solve(state & ~covers[e]) for e in tri_vars[t]))
    return solve((1 << len(tris)) - 1)

def cover(n, edges):
    out = set()
    for i, j in combinations(range(3), 2):
        for u, v in edges:
            out.add(tuple(sorted((i * n + u, j * n + v))))
            out.add(tuple(sorted((i * n + v, j * n + u))))
    return out
checks = []
for n in range(1, 5):
    ps = pairs(n + 1)
    valid = [mask for mask in range(1 << len(ps)) if in_property(n + 1, graph_edges(n + 1, mask))]
    weights = [n if 0 in e else 1 for e in ps]

    def weighted_cost(xor):
        return sum((w for i, w in enumerate(weights) if xor >> i & 1))
    for mask in range(1 << len(pairs(n))):
        es = graph_edges(n, mask)
        tau = triangle_deletions(n, es)
        ces = cover(n, es)
        ctau = triangle_deletions(3 * n, ces)
        if not ctau >= tau:
            raise AssertionError('verification failed at original line 77')
        if not (ctau == 0) == (tau == 0):
            raise AssertionError('verification failed at original line 78')
        jes = {(0, i + 1) for i in range(n)} | {(u + 1, v + 1) for u, v in es}
        jmask = sum((1 << i for i, e in enumerate(ps) if e in jes))
        cost = min((weighted_cost(jmask ^ f) for f in valid))
        if colorable(n, es):
            if not cost == tau:
                raise AssertionError((n, mask, tau, cost))
        checks.append(dict(n=n, graph_mask=mask, tail_tau=tau, cover_tau=ctau, apex_min_cost_units=cost, apex_cost_unit_denominator=4 * n * n))
k3 = next((x for x in checks if x['n'] == 3 and x['graph_mask'] == 7))
if not (k3['tail_tau'] == 1 and k3['apex_min_cost_units'] == 1):
    raise AssertionError('verification failed at original line 89')
result = {'status': 'PASS', 'scope': 'All 75 labeled simple tail graphs with 1 <= n <= 4. Apex minimum ranges over every target graph in P on n+1 vertices, allowing arbitrary additions and deletions.', 'graphs_checked': len(checks), 'source_code': Path(__file__).name, 'normalization_control': {'K3_tail_uniform_distance': '1/9', 'heavy_apex_K4_distance': '1/36', 'single_apex_edge_cost': '1/12'}, 'limitations': 'Finite checks do not establish the general theorem, its asymptotics, or literature priority.', 'checks': checks}
HERE.joinpath('bridge_check_results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))

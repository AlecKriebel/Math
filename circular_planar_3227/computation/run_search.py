"""Small exact finite-domain search. Search status is not a formal UNSAT certificate."""
import collections
import json
import os
import sys
import time
import networkx as nx
from verify_certificate import verify


def solve(g, p, q, limit=30):
    start = time.monotonic()
    vertices = sorted(g.nodes())
    adj = [list(g.neighbors(v)) for v in vertices]
    assert vertices == list(range(len(vertices)))
    n = len(vertices)
    masks = [sum(1 << ((c+d) % p) for d in range(q, p-q+1)) for c in range(p)]
    domains = [(1 << p)-1]*n
    domains[0] = 1  # rotation symmetry
    if adj[0]:
        domains[adj[0][0]] &= sum(1 << c for c in range(q, p//2+1))  # reflection
    stats = {'nodes': 0, 'propagations': 0}

    def recurse(ds):
        if time.monotonic()-start > limit:
            raise TimeoutError
        stats['nodes'] += 1
        queue = collections.deque((u, v) for u in vertices for v in adj[u])
        while queue:
            u, v = queue.popleft()
            stats['propagations'] += 1
            new = 0
            bits = ds[u]
            while bits:
                bit = bits & -bits
                c = bit.bit_length()-1
                if masks[c] & ds[v]:
                    new |= bit
                bits -= bit
            if new != ds[u]:
                if not new:
                    return None
                ds[u] = new
                queue.extend((w, u) for w in adj[u] if w != v)
        candidates = [v for v in vertices if ds[v].bit_count() > 1]
        if not candidates:
            return [d.bit_length()-1 for d in ds]
        v = min(candidates, key=lambda v: (ds[v].bit_count(), -len(adj[v]), v))
        bits = ds[v]
        while bits:
            bit = bits & -bits
            bits -= bit
            next_ds = ds.copy()
            next_ds[v] = bit
            result = recurse(next_ds)
            if result is not None:
                return result
        return None

    try:
        solution = recurse(domains)
        status = 'SAT' if solution is not None else 'EXHAUSTED_SEARCH_NOT_FORMAL_CERTIFICATE'
    except TimeoutError:
        solution, status = None, 'UNKNOWN_TIMEOUT'
    return solution, dict(stats, status=status, seconds=round(time.monotonic()-start, 6))


def main():
    out = os.path.dirname(os.path.abspath(__file__))
    cases = [('cycle5', nx.cycle_graph(5)), ('cycle7', nx.cycle_graph(7)),
             ('cube', nx.cubical_graph()), ('pentagonal_prism', nx.circular_ladder_graph(5)),
             ('heptagonal_prism', nx.circular_ladder_graph(7)),
             ('hexagonal_patch_3x3', nx.hexagonal_lattice_graph(3, 3)),
             ('dodecahedron', nx.dodecahedral_graph())]
    results = []
    for name, g in cases:
        g = nx.convert_node_labels_to_integers(g)
        properties = {'n': len(g), 'm': g.number_of_edges(), 'planar': nx.check_planarity(g)[0],
                      'max_degree': max(dict(g.degree()).values()), 'triangle_count': sum(nx.triangles(g).values())//3}
        assert properties['planar'] and properties['max_degree'] <= 3 and properties['triangle_count'] == 0
        sol, stats = solve(g, 20, 7)
        result = dict(name=name, p=20, q=7, graph_properties=properties, **stats)
        if sol is not None:
            cert = {'name': name, 'p': 20, 'q': 7, 'vertices': list(g.nodes()),
                    'edges': [list(e) for e in sorted(g.edges())], 'colors': {str(v): sol[v] for v in g}}
            result['verification'] = verify(cert)
            with open(os.path.join(out, name+'_20_7.json'), 'w') as f:
                json.dump(cert, f, indent=2, sort_keys=True)
                f.write('\n')
        results.append(result)
        print(json.dumps(result), flush=True)
    sol, stats = solve(nx.dodecahedral_graph(), 17, 6, 30)
    result = dict(name='dodecahedron', p=17, q=6, **stats)
    results.append(result)
    print(json.dumps(result), flush=True)
    with open(os.path.join(out, 'results.json'), 'w') as f:
        json.dump({'networkx_version': nx.__version__, 'results': results}, f, indent=2, sort_keys=True)
        f.write('\n')

if __name__ == '__main__':
    main()

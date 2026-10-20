"""Independent set-based, standard-library verifier of exhaustive branch trees.

The producer uses bitsets and queued revisions; this checker uses sets and full
edge sweeps. No producer code is imported. Diagnostic rejected_domains are not
trusted: contradictions are recomputed from the original graph and branch path.
"""
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(data):
    require(data['format'] == 'circular-unsat-branch-tree-v1', 'Unknown format')
    p,q = data['p'],data['q']
    require(type(p) is int and type(q) is int and q > 0 and p >= 2*q, 'Invalid target')
    vertices = data['vertices']
    require(vertices == list(range(len(vertices))), 'Expected integer vertex indices')
    n = len(vertices)
    edges = data['edges']
    seen = set()
    for u,v in edges:
        require(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n and u != v, 'Invalid edge')
        edge = frozenset((u,v))
        require(edge not in seen, 'Duplicate edge')
        seen.add(edge)
    r,s = data['symmetry']['root'],data['symmetry']['neighbor']
    require(type(r) is int and type(s) is int and 0 <= r < n and 0 <= s < n, 'Invalid symmetry vertices')
    require(frozenset((r,s)) in seen, 'Reflection restriction requires an edge')
    domains = [set(range(p)) for _ in vertices]
    domains[r] = {0}
    domains[s] = set(range(q, p//2+1))
    counts = {'nodes': 0, 'leaves': 0}

    def propagate(ds):
        changed = True
        while changed:
            changed = False
            for a,b in edges:
                for u,v in ((a,b),(b,a)):
                    new = {c for c in ds[u] if any(q <= (c-d) % p <= p-q for d in ds[v])}
                    if new != ds[u]:
                        ds[u] = new
                        changed = True
                    if not new:
                        return False
        return True

    def walk(node, ds):
        counts['nodes'] += 1
        consistent = propagate(ds)
        if 'leaf' in node:
            require(node['leaf'] == 'contradiction' and not consistent, 'False contradiction leaf')
            # Leaf domain snapshots are diagnostics only. Require a syntactically
            # valid snapshot with the claimed empty domain, but never use it to
            # establish contradiction: independent propagation above does that.
            snapshot = node['rejected_domains']
            v = node['rejected_vertex']
            require(type(v) is int and 0 <= v < n and len(snapshot) == n, 'Malformed leaf snapshot')
            require(snapshot[v] == [], 'Missing diagnostic empty domain')
            require(all(isinstance(xs, list) and len(xs) == len(set(xs)) and all(type(c) is int and 0 <= c < p for c in xs) for xs in snapshot), 'Malformed diagnostic colors')
            counts['leaves'] += 1
            return
        require(consistent, 'Unexpected branch at contradiction')
        v = node['branch']
        require(type(v) is int and 0 <= v < n and len(ds[v]) > 1, 'Invalid branch variable')
        require(node['remaining_domain'] == sorted(ds[v]), 'Wrong remaining domain')
        children = node['children']
        colors = [child['color'] for child in children]
        require(all(type(c) is int for c in colors), 'Invalid branch color')
        require(len(colors) == len(set(colors)) and set(colors) == ds[v], 'Branches do not exactly cover remaining domain')
        for child in children:
            next_ds = [set(xs) for xs in ds]
            next_ds[v] = {child['color']}
            walk(child['tree'], next_ds)

    walk(data['tree'], domains)
    require(counts == data['counts'], 'Incorrect counts')
    return dict(verified_exhaustive_unsat=True, p=p, q=q, vertices=n, edges=len(edges), **counts)

if __name__ == '__main__':
    for path in sys.argv[1:]:
        with open(path) as f:
            data = json.load(f)
        print(path, json.dumps(verify(data), sort_keys=True))

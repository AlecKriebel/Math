"""Produce a finite exhaustive branching certificate, with diagnostic leaf domains."""
import collections
import json
import os
import time

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, 'dodecahedron_20_7.json')) as f:
    graph = json.load(f)
p, q = 17, 6
n = len(graph['vertices'])
adj = [[] for _ in range(n)]
for u, v in graph['edges']:
    adj[u].append(v)
    adj[v].append(u)
allowed = [sum(1 << ((c+d) % p) for d in range(q, p-q+1)) for c in range(p)]
root, neighbor = 0, adj[0][0]
ds = [(1 << p)-1]*n
ds[root] = 1
ds[neighbor] = sum(1 << c for c in range(q, p//2+1))
start = time.monotonic()
counts = {'nodes': 0, 'leaves': 0}

def unpack(ds):
    return [[c for c in range(p) if mask & (1 << c)] for mask in ds]

def build(ds):
    if time.monotonic()-start > 30:
        raise TimeoutError('UNKNOWN: generation exceeded budget')
    counts['nodes'] += 1
    queue = collections.deque((u,v) for u in range(n) for v in adj[u])
    while queue:
        u,v = queue.popleft()
        new = sum(1 << c for c in range(p) if ds[u] & (1 << c) and allowed[c] & ds[v])
        if new != ds[u]:
            ds[u] = new
            if not new:
                counts['leaves'] += 1
                return {'leaf': 'contradiction', 'rejected_vertex': u, 'rejected_domains': unpack(ds)}
            queue.extend((w,u) for w in adj[u] if w != v)
    candidates = [v for v in range(n) if ds[v].bit_count() > 1]
    if not candidates:
        raise ValueError('SAT leaf encountered; not an UNSAT certificate')
    v = min(candidates, key=lambda v: (ds[v].bit_count(), -len(adj[v]), v))
    children = []
    for c in range(p):
        if ds[v] & (1 << c):
            child_ds = ds.copy()
            child_ds[v] = 1 << c
            children.append({'color': c, 'tree': build(child_ds)})
    return {'branch': v, 'remaining_domain': unpack([ds[v]])[0], 'children': children}

cert = {'format': 'circular-unsat-branch-tree-v1', 'p': p, 'q': q,
        'vertices': graph['vertices'], 'edges': graph['edges'],
        'symmetry': {'root': root, 'neighbor': neighbor}, 'tree': build(ds), 'counts': counts}
with open(os.path.join(base, 'dodecahedron_17_6_unsat.json'), 'w') as f:
    json.dump(cert, f, separators=(',', ':'), sort_keys=True)
    f.write('\n')
print(counts)

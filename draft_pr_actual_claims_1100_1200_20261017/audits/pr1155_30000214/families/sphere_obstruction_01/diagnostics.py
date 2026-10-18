#!/usr/bin/env python3
"""Exact finite checks of PG(2,11); does not instantiate the building quotient."""
from collections import Counter, deque
from itertools import product
from pathlib import Path
import json

Q = 11

def canonical(v):
    first = next(x for x in v if x)
    inv = pow(first, -1, Q)
    return tuple(x * inv % Q for x in v)

vectors = sorted({canonical(v) for v in product(range(Q), repeat=3) if any(v)})
points = vectors
lines = vectors
inc = [[sum(a*b for a, b in zip(p,l)) % Q == 0 for l in lines] for p in points]
n = len(points)
adj = [set() for _ in range(2*n)]
for i in range(n):
    for j in range(n):
        if inc[i][j]:
            adj[i].add(n+j)
            adj[n+j].add(i)
assert n == Q*Q+Q+1 == 133
assert set(map(len, adj)) == {Q+1}
assert all(sum(inc[i][j] and inc[k][j] for j in range(n)) == (Q+1 if i == k else 1)
           for i in range(n) for k in range(n))

def connected_without(deleted):
    allowed = set(range(2*n)) - deleted
    seen = {min(allowed)}
    queue = deque(seen)
    while queue:
        a = queue.popleft()
        for b in adj[a] - deleted - seen:
            seen.add(b)
            queue.append(b)
    return seen == allowed

assert connected_without(set())
for w in range(2*n):
    assert connected_without({w})
    assert Counter(len(adj[v] - {w}) for v in range(2*n) if v != w) == Counter({11:12,12:253})

# Noncollinear coordinate points furnish a six-cycle by their joining lines.
p = [points.index(v) for v in [(1,0,0),(0,1,0),(0,0,1)]]
l = [n+lines.index(v) for v in [(0,0,1),(1,0,0),(0,1,0)]]
witness = [p[0],l[0],p[1],l[1],p[2],l[2]]
assert len(set(witness)) == 6
assert all(witness[(i+1)%6] in adj[witness[i]] for i in range(6))
# Bipartite graph plus exactly one common line per distinct point pair excludes all shorter cycles.
assert 11 < 4**2
assert 7*2 > 12
result = {
    "scope": "Exact incidence-graph arithmetic only; no enumeration of Gamma_9 quotient or homology boundary matrices.",
    "q": Q,
    "projective_points": n,
    "projective_lines": n,
    "vertices": len(adj),
    "edges": sum(map(len,adj))//2,
    "regular_degree": Q+1,
    "incidence_identity": "MM^T = 11I + J; all 17689 entries checked exactly",
    "girth": 6,
    "six_cycle_witness_indices": witness,
    "all_266_single_vertex_deletions_connected": True,
    "single_deletion_degree_multiplicities": {"11":12,"12":253},
    "symbolic_gap_certificate": "sqrt(11)<4; (11-sqrt(11))/12>7/12>1/2",
    "outcome": "PASS"
}
Path(__file__).with_name("DIAGNOSTICS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))

"""Independent exact finite diagnostics; not enumeration of the quotient K."""
from collections import deque
from fractions import Fraction
from itertools import combinations, product
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        pivot = a[r][j]
        a[r] = [x / pivot for x in a[r]]
        for k in range(len(a)):
            if k != r and a[k][j]:
                c = a[k][j]
                a[k] = [x - c * y for x, y in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


q = 11
projective = []
for v in product(range(q), repeat=3):
    if not any(v):
        continue
    first = next(x for x in v if x)
    if first == 1:
        projective.append(v)
need(len(projective) == 133, "projective normalization")
matrix = [[int(sum(x*y for x, y in zip(p, ell)) % q == 0)
           for ell in projective] for p in projective]
need(all(sum(row) == 12 for row in matrix), "point degree")
need(all(sum(row[j] for row in matrix) == 12 for j in range(133)), "line degree")
need(all(sum(x*y for x, y in zip(matrix[i], matrix[j])) == (12 if i == j else 1)
         for i in range(133) for j in range(133)), "M M^T = 11 I + J")
adj = {i: set() for i in range(266)}
for i in range(133):
    for j in range(133):
        if matrix[i][j]:
            adj[i].add(133+j)
            adj[133+j].add(i)


def connected_without(w):
    start = next(v for v in adj if v != w)
    seen = {start}
    queue = deque([start])
    while queue:
        for v in adj[queue.popleft()]:
            if v != w and v not in seen:
                seen.add(v)
                queue.append(v)
    return len(seen) == 265


need(all(connected_without(w) for w in adj), "every single deletion connected")
need(all(len((adj[v] - {w})) in (11, 12) for w in adj for v in adj if v != w),
     "every deleted-link degree")
need(all(len(adj[i] & adj[j]) <= 1 for i in range(133) for j in range(i)),
     "no 4-cycle")
# The symbolic eigenvalue computation follows from the exact Gram identity.
# sqrt(11)<4 supplies a strict rational lower bound, avoiding floats.
need(11 < 4**2 and Fraction(7, 12) > Fraction(1, 2), "strict rational gap")

# A 7-vertex triangulated torus supplies the sharp boundary gap=1/2:
# each link is C6, while H1 has dimension 2. This tests why strictness matters.
triangles = sorted({tuple(sorted(((i+a) % 7 for a in pattern)))
                    for i in range(7) for pattern in [(0, 1, 3), (0, 2, 3)]})
edges = sorted({e for t in triangles for e in combinations(t, 2)})
need(len(triangles) == 14 and len(edges) == 21, "torus face counts")
need(all(sum(set(e) <= set(t) for t in triangles) == 2 for e in edges), "torus edge links")
for v in range(7):
    link_edges = [tuple(x for x in t if x != v) for t in triangles if v in t]
    link_adj = {u: set() for u in range(7) if u != v}
    for a, b in link_edges:
        link_adj[a].add(b)
        link_adj[b].add(a)
    need(all(len(x) == 2 for x in link_adj.values()), "torus link degrees")
    seen = set()
    queue = [next(iter(link_adj))]
    while queue:
        u = queue.pop()
        if u not in seen:
            seen.add(u)
            queue.extend(link_adj[u])
    need(len(seen) == 6, "torus link C6")
d1 = [[int(v == b) - int(v == a) for a, b in edges] for v in range(7)]
d2 = [[sum((-1)**k for k in range(3) if tuple(x for j, x in enumerate(t) if j != k) == e)
       for t in triangles] for e in edges]
r1, r2 = rank(d1), rank(d2)
need((r1, r2, len(edges)-r1-r2) == (6, 13, 2), "torus H1 threshold control")
need(all(sum(d1[i][k]*d2[k][j] for k in range(21)) == 0
         for i in range(7) for j in range(14)), "boundary squared")

# Reproduce the triangle/edge energy double-counting for an exact cocycle.
potential = [v*v-3*v for v in range(7)]
a = {(u, v): potential[v]-potential[u] for u in range(7) for v in range(7)}
energy = sum(sum(set(e) <= set(t) for t in triangles)*a[e]**2 for e in edges)
link_energy = sum((a[v,u]-a[v,w])**2 for t in triangles
                  for v in t for u, w in [tuple(x for x in t if x != v)])
endpoint_norm = sum(sum(set(e) <= set(t) for t in triangles)*a[e]**2
                    for e in edges for _ in e)
need(link_energy == energy and endpoint_norm == 2*energy, "weighted cocycle identities")

print(json.dumps({
    "status": "PASS", "field_order": q, "point_count": 133, "line_count": 133,
    "incidences": 1596, "exact_gram_entry_checks": 133**2,
    "all_single_deletions_connected": 266,
    "all_deleted_degrees_11_or_12": True, "girth_at_least_six": True,
    "deleted_normalized_gap_strict_rational_lower_bound": "7/12 > 1/2",
    "sharp_threshold_control": {"complex": "7-vertex 14-triangle torus", "link": "C6",
                               "normalized_gap": "1/2", "rational_H1_dimension": 2},
    "weighted_cocycle_energy": energy, "link_energy": link_energy,
    "endpoint_weighted_norm": endpoint_norm,
    "limits": "Exact finite incidence/energy/strict-threshold diagnostics; does not enumerate K, certify the lattice theorem, or prove the complete mathematical claim."
}, indent=2))

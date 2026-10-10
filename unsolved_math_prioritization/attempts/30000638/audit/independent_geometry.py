"""Independent exact finite audit. Standard library only; no author imports.

Supporting planes are enumerated, but facet areas use all-pairs supporting
edges and the divergence formula, not the author's projected monotone chain
and origin-tetrahedron fan. This is finite evidence, not a general proof.
"""
from fractions import Fraction
from itertools import combinations, product, permutations
from math import gcd, comb


def need(ok, label):
    if not ok:
        raise ValueError(label)


def determinant(a):
    n = len(a)
    result = 0
    for p in permutations(range(n)):
        sign = (-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i+1, n))
        term = sign
        for i in range(n):
            term *= a[i][p[i]]
        result += term
    return result


def plane_through(vs):
    a = tuple((-1)**j * determinant([[1]+[v[k] for k in range(3) if k != j]
                                   for v in vs]) for j in range(3))
    b = sum(a[j]*vs[0][j] for j in range(3))
    if not b:
        return None
    if b < 0:
        a, b = tuple(-x for x in a), -b
    g = gcd(*a, b)
    return tuple(x//g for x in a)+(b//g,)


def dot(a, v):
    return sum(x*y for x, y in zip(a, v))


def area_twice(points):
    pts = sorted(set(points))
    edges = []
    for p, q in permutations(pts, 2):
        dx, dy = q[0]-p[0], q[1]-p[1]
        orient = [(dx*(r[1]-p[1])-dy*(r[0]-p[0])) for r in pts]
        if min(orient) < 0 or max(orient) == 0:
            continue
        length2 = dx*dx+dy*dy
        if any(s == 0 and not (0 <= dx*(r[0]-p[0])+dy*(r[1]-p[1]) <= length2)
               for r, s in zip(pts, orient)):
            continue
        edges.append((p, q))
    need(len(edges) >= 3, 'facet supporting edges')
    need({p for p, q in edges} == {q for p, q in edges}, 'closed facet boundary')
    need(len({p for p, q in edges}) == len(edges), 'unique outgoing edge')
    area2 = sum(p[0]*q[1]-p[1]*q[0] for p, q in edges)
    need(area2 > 0, 'positive facet area')
    return area2


def independent_case(raw):
    vs = [tuple(p) for p in raw]
    planes = set()
    for triple in combinations(vs, 3):
        plane = plane_through(triple)
        if plane and all(dot(plane[:3], v) <= plane[3] for v in vs):
            planes.add(plane)
    need(len(planes) >= 4, 'support facets')
    volume = Fraction(0)
    for a, b, c, d in planes:
        normal = (a, b, c)
        drop = max(range(3), key=lambda j: abs(normal[j]))
        face = [tuple(v[j] for j in range(3) if j != drop)
                for v in vs if dot(normal, v) == d]
        volume += Fraction(d*area_twice(face), abs(normal[drop]))
    need(volume.denominator == 1, 'integer normalized volume')
    radii = [max(abs(v[j]) for v in vs) for j in range(3)]
    counts = [1]
    interior = 0
    for k in range(1, 4):
        closed = 0
        for x in product(*(range(-k*r, k*r+1) for r in radii)):
            values = [dot(p[:3], x)-k*p[3] for p in planes]
            closed += max(values) <= 0
            if k == 1:
                interior += max(values) < 0
        counts.append(closed)
    h = [sum((-1)**j*comb(4, j)*counts[i-j] for j in range(i+1)) for i in range(4)]
    return {'volume_normalized': int(volume), 'interior_count': interior,
            'closed_counts_k0_to_k3': counts, 'hstar': h, 'facet_count': len(planes)}


def verify_cases(results):
    rows = []
    for name, author in results['cases'].items():
        actual = independent_case(author['vertices'])
        need(all(author[key] == val for key, val in actual.items()), 'independent mismatch: '+name)
        rows.append({'case': name, **actual, 'match': True})
    return rows

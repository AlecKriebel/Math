#!/usr/bin/env python3
"""Exact local-patch checks for the radius-sqrt(10) layered triangulation.

The all-vertex reduction and non-cocompactness proof are in CANDIDATE.md.
This checks all eight neighboring-layer choices at both central row types,
including closed-ball boundary points. Only the Python standard library is used.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from collections import Counter
from math import gcd, lcm
from pathlib import Path
import json

R2 = Q(10)


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def scale(t, a):
    return t*a[0], t*a[1]


def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]


def norm2(a):
    return dot(a, a)


def edge(a, b):
    return tuple(sorted([a, b]))


def segment_minimum(e):
    a, b = e
    v = sub(b, a)
    t = max(Q(0), min(Q(1), -dot(a, v)/norm2(v)))
    p = add(a, scale(t, v))
    return norm2(p), p


def make_patch(signs):
    # The radius is <4. For the two root types at y=0 and y=1, only
    # T_-1,I_-1,T_0,I_0,T_1 can meet the disk. Extra guard rows are included.
    delta = {j: Q(1)+Q(signs.get(j, 1), 2) for j in range(-3, 4)}
    offsets = {0: Q(0)}
    for j in range(0, 3):
        offsets[j+1] = offsets[j]+delta[j]+1
    for j in range(-1, -4, -1):
        offsets[j] = offsets[j+1]-delta[j]-1
    rows = []
    for j in range(-3, 4):
        rows.append((Q(4*j), offsets[j]))
        rows.append((Q(4*j+1), offsets[j]+delta[j]))
    vertices, edges, triangles = set(), set(), []
    for (yl, al), (yu, au) in zip(rows, rows[1:]):
        # Shift is delta_j for a short band and exactly1 for a tall band.
        for k in range(-10, 11):
            lo = (Q(2*k)+al, yl)
            lonext = (Q(2*k+2)+al, yl)
            up = (Q(2*k)+au, yu)
            upprev = (Q(2*k-2)+au, yu)
            for triangle in [(lo, lonext, up), (upprev, up, lo)]:
                triangles.append(triangle)
                vertices.update(triangle)
                edges.update(edge(a, b) for a, b in combinations(triangle, 2))
    return delta[0], vertices, edges, triangles


def canonical_transform(p, delta, upper):
    x, y = p
    if upper:
        x, y = delta-x, 1-y  # half-turn centered at(delta/2,1/2)
    if delta == Q(3, 2):
        x = -x               # vertical reflection;1.5 becomes0.5 modulo2
    return x, y


def oriented_line(a, b, third):
    dx, dy = sub(b, a)
    coeff = (-dy, dx, dy*a[0]-dx*a[1])
    if coeff[0]*third[0]+coeff[1]*third[1]+coeff[2] < 0:
        coeff = tuple(-v for v in coeff)
    denominator = lcm(*(v.denominator for v in coeff))
    integers = [int(v*denominator) for v in coeff]
    divisor = gcd(*integers)
    return tuple(v//divisor for v in integers)


def face_data(triangle, radius2):
    inequalities, minima, visible = [], [], []
    for i in range(3):
        a, b, third = triangle[i], triangle[(i+1)%3], triangle[(i+2)%3]
        line = oriented_line(a, b, third)
        inequalities.append(line)
        minimum = segment_minimum(edge(a, b))
        minima.append(minimum)
        if minimum[0] < radius2:
            visible.append(line)
    minimum = (Q(0), (Q(0), Q(0))) if all(line[2] >= 0 for line in inequalities) else min(minima)
    if minimum[0] < radius2:
        # For a positive-area convex clipped face, the inequalities whose
        # actual edges meet the open disk determine the face inside the disk.
        return "area", tuple(sorted(visible))
    if minimum[0] == radius2:
        return "point", minimum[1]
    return "empty", None


def signature(signs, upper=False, radius2=R2):
    delta, vv, ee, tt = make_patch(signs)
    transform = lambda p: canonical_transform(p, delta, upper)
    visible_vertices = {transform(v) for v in vv if norm2(transform(v)) <= radius2}
    visible_edges, boundary_edges = set(), Counter()
    for e in ee:
        transformed = edge(*(transform(p) for p in e))
        d, p = segment_minimum(transformed)
        if d < radius2:
            visible_edges.add(transformed)
        elif d == radius2:
            boundary_edges[p] += 1
    area_faces, boundary_faces = Counter(), Counter()
    for triangle in set(tuple(sorted(t)) for t in tt):
        kind, value = face_data(tuple(transform(p) for p in triangle), radius2)
        if kind == "area":
            area_faces[value] += 1
        elif kind == "point":
            boundary_faces[value] += 1
    return (frozenset(visible_vertices), frozenset(visible_edges),
            tuple(sorted(boundary_edges.items())), tuple(sorted(area_faces.items())),
            tuple(sorted(boundary_faces.items())))


def main():
    baseline = signature({-1: -1, 0: -1, 1: -1})
    cases = []
    triangle_lengths, areas = set(), set()
    for word in product([-1, 1], repeat=3):
        signs = dict(zip([-1, 0, 1], word))
        delta, vertices, edges, triangles = make_patch(signs)
        for t in triangles:
            lengths = tuple(sorted(norm2(sub(a, b)) for a, b in combinations(t, 2)))
            triangle_lengths.add(lengths)
            assert max(lengths) <= R2
            a, b, c = t
            u, v = sub(b, a), sub(c, a)
            area = abs(u[0]*v[1]-u[1]*v[0])/2
            assert area in [1, 3]
            areas.add(area)
        for upper in [False, True]:
            sig = signature(signs, upper)
            assert sig == baseline, (word, upper)
            cases.append({"neighbor_signs": list(word), "root": "upper" if upper else "lower",
                          "vertices_in_closed_disk": len(sig[0]),
                          "edges_with_positive_length_in_disk": len(sig[1]),
                          "boundary_edge_point_locations": len(sig[2]),
                          "positive_area_faces": sum(v for k,v in sig[3]),
                          "point_only_faces": sum(v for k,v in sig[4]), "status": "passed"})
    assert triangle_lengths == {(Q(5, 4), Q(13, 4), Q(4)), (Q(4), Q(10), Q(10))}
    assert areas == {1, 3}

    # Exact shielding inequality for each nearest far-row endpoint.
    for px in [-1, 1]:
        for dx in [Q(-3, 2), Q(-1, 2), Q(1, 2), Q(3, 2)]:
            assert dot((Q(px), Q(-3)), (dx, Q(-1))) >= Q(3, 2)
    assert Q(3, 2)**2+9 > 10  # all farther endpoints/edges stay outside

    # A negative control: adding radius beyond the threshold reveals a
    # previously shielded choice in the canonically normalized patch.
    s1 = signature({-1: -1, 0: -1, 1: -1}, radius2=Q(1001, 100))
    s2 = signature({-1: 1, 0: -1, 1: -1}, radius2=Q(1001, 100))
    assert s1 != s2

    receipt = {"status": "passed", "arithmetic": "fractions.Fraction",
               "radius_squared": 10, "local_configurations": 8, "rooted_cases": len(cases),
               "triangle_squared_sides": [[str(x) for x in v] for v in sorted(triangle_lengths)],
               "triangle_areas": [1, 3],
               "closed_disk_vertices": len(baseline[0]), "positive_length_edges": len(baseline[1]),
               "boundary_edge_points": {str(k):v for k,v in baseline[2]},
               "positive_area_faces": sum(v for k,v in baseline[3]),
               "point_only_face_traces": {str(k):v for k,v in baseline[4]},
               "negative_control": "canonical neighboring-layer patches differ at radius_squared1001/100",
               "scope": "finite exhaustive local certificate after the analytic locality reduction; no global-periodicity conclusion from finite testing",
               "cases": cases}
    Path(__file__).with_name('verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Independent exact finite controls. Not a formal proof of the analytic theorems."""
from fractions import Fraction as Q
from itertools import combinations, product
import json


def rank(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        d = a[r][c]
        a[r] = [x / d for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                d = a[i][c]
                a[i] = [x - d * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def sphere_complex(n):
    faces = sorted({tuple(sorted((pole, i, (i + 1) % n)))
                    for pole in (n, n + 1) for i in range(n)})
    vertices = list(range(n + 2))
    edges = sorted({e for f in faces for e in combinations(f, 2)})
    return vertices, edges, faces


def homology(vertices, edges, faces):
    vi = {v: i for i, v in enumerate(vertices)}
    ei = {e: i for i, e in enumerate(edges)}
    d1 = [[0] * len(edges) for _ in vertices]
    d2 = [[0] * len(faces) for _ in edges]
    for j, (u, v) in enumerate(edges):
        d1[vi[u]][j], d1[vi[v]][j] = -1, 1
    for j, face in enumerate(faces):
        for k in range(3):
            edge = face[:k] + face[k + 1:]
            d2[ei[edge]][j] = (-1) ** k
    assert all(sum(d1[i][k] * d2[k][j] for k in range(len(edges))) == 0
               for i in range(len(vertices)) for j in range(len(faces)))
    r1, r2 = rank(d1), rank(d2)
    return [len(vertices) - r1, len(edges) - r1 - r2, len(faces) - r2]


def circular_link(v, faces):
    edges = [tuple(x for x in f if x != v) for f in faces if v in f]
    nodes = set().union(*(set(e) for e in edges))
    adjacency = {w: set() for w in nodes}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen, todo = set(), [next(iter(nodes))]
    while todo:
        w = todo.pop()
        if w not in seen:
            seen.add(w)
            todo.extend(adjacency[w] - seen)
    return seen == nodes and all(len(a) == 2 for a in adjacency.values())


def run():
    output = {}
    # This model uses C7, independently of the author's C5 model.
    n = 7
    poles = {('pole', -1), ('pole', 1)}
    points = poles | {(i, r) for i in range(n) for r in (Q(-1, 2), Q(0), Q(1, 2))}

    def action(pair, p):
        a, k = pair
        return p if p in poles else ((a + pow(5, k, n) * p[0]) % n, p[1])

    def multiply(u, v):
        a, k = u
        b, m = v
        return ((a + pow(5, k, n) * b) % n, k + m)

    elements = list(product(range(n), range(-3, 4)))
    checks = 0
    for u, v, p in product(elements, elements, points):
        assert action(u, action(v, p)) == action(multiply(u, v), p)
        checks += 1
    for p in points:
        assert action((0, -1), action((1, 0), action((0, 1), p))) == action((3, 0), p)
    fixed = {p for p in points if all(action(g, p) == p for g in ((1, 0), (0, 1)))}
    assert fixed == poles
    output['semidirect_C7'] = {'composition_checks': checks, 'relation_points': len(points),
                              'global_fixed_points': 2, 'stable_letter_multiplier': 5,
                              'automorphism_multiplier': 3}

    # An honest C6 x Z action: t fixes both endpoints but g swaps them.
    # Thus checking t alone is insufficient, even when the group relation holds.
    def bad_g(p):
        return ('pole', -p[1]) if p in poles else ((p[0] + 1) % 6, -p[1])
    bad_points = poles | {(i, Q(1, 2)) for i in range(6)} | {(i, Q(-1, 2)) for i in range(6)}
    for p in bad_points:
        x = p
        for _ in range(6):
            x = bad_g(x)
        assert x == p
    assert all(bad_g(p) != p for p in poles)
    output['stable_letter_only_false_positive_rejected'] = True

    rows = []
    for n in range(3, 17):
        v, e, f = sphere_complex(n)
        b = homology(v, e, f)
        assert b == [1, 0, 1]
        assert len(v) - len(e) + len(f) == 2
        assert all(circular_link(x, f) for x in v)
        assert all(sum(set(edge) <= set(face) for face in f) == 2 for edge in e)
        rows.append({'polygon_vertices': n, 'simplex_counts': [len(v), len(e), len(f)],
                     'rational_betti_numbers': b, 'all_vertex_links_circles': True})
    v, e, f = sphere_complex(7)
    mutant = f[:-1]
    assert homology(v, e, mutant) == [1, 0, 0]
    assert not all(circular_link(x, mutant) for x in v)
    output['suspension_spheres'] = rows
    output['deleted_face_mutation_rejected'] = True

    # Rational points in the explicit sphere homeomorphism from the suspension.
    circle = {(Q(1) - u * u, 2 * u, Q(1) + u * u) for u in map(Q, range(-5, 6))}
    heights_radii = [(Q(0), Q(1)), (Q(3, 5), Q(4, 5)), (Q(-3, 5), Q(4, 5)),
                     (Q(5, 13), Q(12, 13)), (Q(-5, 13), Q(12, 13)),
                     (Q(1), Q(0)), (Q(-1), Q(0))]
    for s, rho in heights_radii:
        images = {(rho * x / d, rho * y / d, s) for x, y, d in circle}
        assert all(sum(c * c for c in xyz) == 1 for xyz in images)
        assert len(images) == (1 if abs(s) == 1 else len(circle))
    output['exact_sphere_coordinate_checks'] = len(circle) * len(heights_radii)
    return {'result': 'pass', 'scope': 'Exact finite algebra and simplicial controls only; '
            'the theorem application, compactification, nullity, and dimension proof are not machine verified.',
            'checks': output}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

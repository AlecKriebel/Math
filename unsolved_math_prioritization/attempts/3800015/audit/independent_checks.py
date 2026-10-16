#!/usr/bin/env python3
"""Independent exact geometry and adversarial checks; finite evidence only.

Usage: python3 -I -B independent_checks.py /path/to/frozen/verify.py
No third-party packages, floating point arithmetic, or writes are used.
"""
import itertools
import json
import math
from pathlib import Path
import random
import runpy
import sys
from fractions import Fraction as Q


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def normalized(raw):
    a, b, c = map(Q, raw)
    need(a or b, 'zero line')
    pivot = a if a else b
    return a / pivot, b / pivot, c / pivot


def contains(line, p):
    return line[0] * p[0] + line[1] * p[1] == line[2]


def crossing(first, second):
    # Substitution, rather than the tested implementation's Cramer formula.
    a, b, c = first
    d, e, f = second
    if b:
        coefficient = d - e * a / b
        if coefficient == 0:
            return None
        x = (f - e * c / b) / coefficient
        return x, (c - a * x) / b
    if not e:
        return None
    x = c / a
    return x, (f - d * x) / e


def length(p, q):
    x, y = p[0] - q[0], p[1] - q[1]
    squared = x*x + y*y
    numerator = math.isqrt(squared.numerator)
    denominator = math.isqrt(squared.denominator)
    need(numerator*numerator == squared.numerator and denominator*denominator == squared.denominator,
         'nonrational test length')
    return Q(numerator, denominator)


def interior(p, r, q):
    px, py = r[0] - p[0], r[1] - p[1]
    qx, qy = q[0] - p[0], q[1] - p[1]
    return px*qy == py*qx and 0 < px*qx + py*qy < qx*qx + qy*qy


def graph(raw):
    lines = set(map(normalized, raw))
    points = {p for l, m in itertools.combinations(lines, 2)
              if (p := crossing(l, m)) is not None}
    adjacency = {p: {} for p in points}
    for p, q in itertools.combinations(points, 2):
        if any(contains(l, p) and contains(l, q) for l in lines):
            if not any(interior(p, r, q) for r in points - {p, q}):
                adjacency[p][q] = adjacency[q][p] = length(p, q)
    return lines, adjacency


def bellman_ford(adjacency, source):
    # Layered dynamic programming with a separate previous layer, no heap.
    distances = {source: Q(0)}
    for _ in range(max(0, len(adjacency) - 1)):
        newer = dict(distances)
        for p, dp in distances.items():
            for q, w in adjacency[p].items():
                if q not in newer or dp + w < newer[q]:
                    newer[q] = dp + w
        if newer == distances:
            break
        distances = newer
    return distances


def all_geodesics(adjacency, source, distances):
    stack = [[source]]
    while stack:
        path = stack.pop()
        yield path
        p = path[-1]
        for q, w in adjacency[p].items():
            if distances[p] + w == distances[q]:
                stack.append(path + [q])


def check_geodesic(lines, path):
    if len(path) > 1:
        incidence_s = sum(contains(l, path[0]) for l in lines)
        incidence_t = sum(contains(l, path[-1]) for l in lines)
        need(len(path)-1 <= len(lines)-incidence_s-incidence_t+2, 'sharp edge bound')
    for line in lines:
        hits = [i for i, p in enumerate(path) if contains(line, p)]
        need(not hits or hits == list(range(min(hits), max(hits)+1)), 'disconnected line hits')
        a, b, c = line
        fs = a*path[0][0]+b*path[0][1]-c
        ft = a*path[-1][0]+b*path[-1][1]-c
        if fs >= 0 and ft >= 0:
            need(all(a*x+b*y-c >= 0 for x, y in path), 'positive corridor')
        if fs <= 0 and ft <= 0:
            need(all(a*x+b*y-c <= 0 for x, y in path), 'negative corridor')


def compare(raw, tested, enumerate_ties=False):
    lines, adjacency = graph(raw)
    original = tested['Arrangement'](raw)
    need(set(adjacency) == set(original.points), 'independent vertex mismatch')
    for p, neighbors in adjacency.items():
        i = original.ids[p]
        original_neighbors = {original.points[j]: w for j, w in original.adj[i].items()}
        need(neighbors == original_neighbors, 'independent edge or length mismatch')
    pairs = paths = 0
    for source in adjacency:
        independent = bellman_ford(adjacency, source)
        actual = original.dijkstra(original.ids[source])[0]
        need({original.points[i]: d for i, d in actual.items()} == independent,
             'independent shortest-distance mismatch')
        pairs += len(independent)
        if enumerate_ties:
            for path in all_geodesics(adjacency, source, independent):
                check_geodesic(lines, path)
                paths += 1
    return pairs, paths


def expect_rejection(fn, exact_message):
    try:
        fn()
    except RuntimeError as error:
        need(str(error) == exact_message, 'unexpected adversarial rejection: ' + str(error))
    else:
        raise RuntimeError('adversarial path accepted: ' + exact_message)


def adversarial(tested):
    # Both chains have actual graph edges and truthful total lengths, but are
    # nongeodesics. Extra remote line allows the first to pass the edge bound.
    raw = [(4, 3, 0), (5, -12, 15), (5, -12, -63), (4, 3, 75), (0, 1, 0)]
    results = []
    for extra, message in [([], 'incidence-sensitive edge bound failed'),
                           ([(0, 1, 100)], 'a line has disconnected intersection with a geodesic')]:
        arrangement = tested['Arrangement'](raw + extra)
        vertices = [(-3, 4), (0, 0), (Q(5, 7), Q(-20, 21)), (3, 0), (15, 5)]
        chain = [arrangement.index(x, y) for x, y in vertices]
        predecessors = {j: i for i, j in zip(chain, chain[1:])}
        total = sum(arrangement.adj[i][j] for i, j in zip(chain, chain[1:]))
        expect_rejection(lambda: tested['check_path'](arrangement, chain[0], chain[-1], total, predecessors), message)
        results.append(message)
    return results


def main():
    need(len(sys.argv) == 2, 'provide frozen verifier path')
    tested = runpy.run_path(str(Path(sys.argv[1]).resolve()), run_name='independent_import')
    five = [(4, 3, 0), (5, -12, 15), (5, -12, -63), (4, 3, 75), (0, 1, 0)]
    profile = [(0, 1, 0), (3, 4, 12), (3, -4, -12), (5, -12, 0)]
    fixed = [five, profile,
             [(0, 1, 0), (1, 0, 0), (3, 4, 0), (5, 12, 0)],
             [(0, 1, j) for j in range(4)] + [(1, 0, i) for i in range(4)],
             [(0, 1, 0), (0, -2, 0), (1, 0, 0), (3, 4, 12), (3, 4, 0)],
             [(1, 0, 0), (1, 0, 4), (0, 1, 0), (0, 1, 3), (3, 4, 12)]]
    pairs = paths = 0
    for raw in fixed:
        p, q = compare(raw, tested, enumerate_ties=True)
        pairs += p
        paths += q
    rng = random.Random(71063800015)
    normals = [(0, 1), (1, 0), (3, 4), (3, -4), (4, 3), (4, -3), (5, 12), (5, -12)]
    for k in range(24):
        raw = [(*v, rng.randrange(-9, 10)) for v in rng.sample(normals, 4 + k % 5)]
        if k % 3 == 0:
            raw.append(tuple(-2*x for x in raw[0]))
        p, _ = compare(raw, tested)
        pairs += p
    # Check isometric and scaled versions via independent geometry.
    transforms = [(1, 7, -11, False), (3, 0, 0, False), (2, -4, 5, True)]
    transformed_queries = 0
    for raw in (five, profile):
        _, original_graph = graph(raw)
        for scale, tx, ty, rotate in transforms:
            def transform(p):
                x, y = p
                if rotate:
                    x, y = -y, x
                return scale*x+tx, scale*y+ty
            transformed = []
            for a, b, c in raw:
                if rotate:
                    a, b = -b, a
                transformed.append((a, b, scale*c+a*tx+b*ty))
            _, moved_graph = graph(transformed)
            need(set(moved_graph) == {transform(p) for p in original_graph}, 'transformed vertices')
            for source in original_graph:
                old = bellman_ford(original_graph, source)
                new = bellman_ford(moved_graph, transform(source))
                need(new == {transform(p): scale*d for p, d in old.items()}, 'transformed distances')
                transformed_queries += len(old)
            p, _ = compare(transformed, tested)
            pairs += p
    # Exact hand certificates not using the tested verifier's hard-coded output.
    _, adjacency = graph(five)
    source, target = (Q(-3), Q(4)), (Q(15), Q(5))
    need(bellman_ford(adjacency, source)[target] == 21, 'five-line optimum')
    one_bend_lengths = []
    for first in set(map(normalized, five)):
        for last in set(map(normalized, five)):
            if contains(first, source) and contains(last, target):
                corner = crossing(first, last)
                if corner is not None:
                    one_bend_lengths.append(length(source, corner)+length(corner, target))
    need(sorted(one_bend_lengths) == [Q(65,3), Q(65,3)], 'one-bend costs')
    z = (Q(1), Q(1,5))
    directions = [(Q(1), Q(0)), (Q(3,5), Q(-4,5)), (Q(12,13), Q(5,13))]
    need(all(abs(z[0]*u[0]+z[1]*u[1]) <= 1 for u in directions), 'dual infeasibility')
    need(z[0]*18 + z[1] == Q(91,5) == Q(78,5)+Q(13,5), 'primal-dual mismatch')
    need((Q(78,5)+Q(12,5), Q(1)) == (Q(18), Q(1)), 'primal displacement')
    _, adjacency = graph(profile)
    dp = bellman_ford(adjacency, (Q(0), Q(3)))
    need([dp[(Q(x), Q(0))] for x in [-4, 0, 4]] == [5, 6, 5], 'profile values')
    print(json.dumps({'status':'passed', 'optimization':sys.flags.optimize,
                      'independent_arrangements':36, 'independent_ordered_distance_queries':pairs,
                      'all_tied_geodesic_paths_checked':paths, 'metamorphic_distance_queries':transformed_queries,
                      'adversarial_rejections':adversarial(tested),
                      'independent_algorithms':['substitution intersection', 'pairwise no-interior-vertex adjacency',
                                                'layered Bellman-Ford', 'all shortest-path DAG enumeration'],
                      'scope':'Finite rational checks and targeted negative tests, not a general proof or algorithm.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

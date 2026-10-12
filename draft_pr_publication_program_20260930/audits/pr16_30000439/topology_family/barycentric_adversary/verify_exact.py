#!/usr/bin/env python3
"""Exact triangle-intersection stress check for the moment-curve construction.

This is a finite illustration, not the general proof. All geometry uses Fraction.
The Fano-plane hypergraph has seven triples, any two meeting in one vertex,
and a cyclic incidence graph. Each intersection polytope is bounded; its basic
feasible solutions suffice to check every possible intersection point.
"""

from fractions import Fraction as Q
from itertools import combinations, permutations
import json
import sys


def p(t):
    return (Q(t), Q(t * t), Q(t * t * t))


def unique_solution(columns, rhs):
    """Solve an overdetermined system, requiring full column rank."""
    width = len(columns)
    a = [[columns[j][i] for j in range(width)] + [rhs[i]]
         for i in range(len(rhs))]
    row = 0
    for col in range(width):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            return None
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [v - scale * w for v, w in zip(a[i], a[row])]
        row += 1
    if any(all(not v for v in r[:-1]) and r[-1] for r in a):
        return None
    return tuple(a[i][-1] for i in range(width))


SUPPORTS = [s for k in range(1, 6) for s in combinations(range(6), k)]


def intersection_vertices(a, b):
    columns = [tuple(v) + (Q(1), Q(0)) for v in a]
    columns += [tuple(-c for c in v) + (Q(0), Q(1)) for v in b]
    rhs = (Q(0), Q(0), Q(0), Q(1), Q(1))
    seen = set()
    for support in SUPPORTS:
        sol = unique_solution([columns[j] for j in support], rhs)
        if sol is None or any(c < 0 for c in sol):
            continue
        coeff = [Q(0)] * 6
        for j, c in zip(support, sol):
            coeff[j] = c
        x = tuple(sum(coeff[j] * a[j][i] for j in range(3)) for i in range(3))
        if x not in seen:
            seen.add(x)
            yield x


def in_expected_hull(x, expected):
    if not expected:
        return False
    if len(expected) == 1:
        return x == expected[0]
    a, b = expected
    i = next(i for i in range(3) if a[i] != b[i])
    t = (x[i] - a[i]) / (b[i] - a[i])
    return 0 <= t <= 1 and all(x[j] == a[j] + t * (b[j] - a[j])
                              for j in range(3))


def main(denominator=10**10):
    facets = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
              (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    assert all(len(set(f) & set(g)) == 1 for f, g in combinations(facets, 2))
    eps = Q(1, denominator)
    positions = {("v", i): p(i + 1) for i in range(7)}
    incidence_adjacency = {("v", i): set() for i in range(7)}
    for fi, facet in enumerate(facets):
        incidence_adjacency[("f", fi)] = {("v", i) for i in facet}
        for i in facet:
            incidence_adjacency[("v", i)].add(("f", fi))
    unseen = set(incidence_adjacency)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            v = stack.pop()
            for w in incidence_adjacency[v] & unseen:
                unseen.remove(w)
                stack.append(w)
    incidence_edges = sum(len(v) for v in incidence_adjacency.values()) // 2
    cycle_rank = incidence_edges - len(incidence_adjacency) + components
    assert cycle_rank > 0
    triangles = []
    for fi, facet in enumerate(facets):
        fkey = ("f", fi)
        f = positions[fkey] = p(fi + 8)
        for i, j in combinations(facet, 2):
            ekey = ("e", tuple(sorted((i, j))))
            positions[ekey] = tuple(f[k] + eps * (positions[("v", i)][k]
                                                  + positions[("v", j)][k]
                                                  - 2 * f[k]) for k in range(3))
        for i, j in permutations(facet, 2):
            keys = (fkey, ("v", i), ("e", tuple(sorted((i, j)))))
            triangles.append((keys, tuple(positions[k] for k in keys)))

    checked = 0
    feasible_vertices = 0
    for (ka, a), (kb, b) in combinations(triangles, 2):
        expected = [positions[k] for k in ka if k in kb]
        for x in intersection_vertices(a, b):
            feasible_vertices += 1
            if not in_expected_hull(x, expected):
                result = {"status": "FAIL", "epsilon": str(eps),
                          "triangles": [str(ka), str(kb)],
                          "unexpected_intersection": [str(c) for c in x],
                          "pairs_checked_before_failure": checked}
                print(json.dumps(result, indent=2), flush=True)
                return 1
        checked += 1
    isolated_checks = 0
    isolated_points = [p(0), p(15)]
    for isolated in isolated_points:
        for keys, triangle in triangles:
            # A repeated-point "triangle" only tests point containment.
            if next(intersection_vertices(triangle, (isolated,) * 3), None) is not None:
                print(json.dumps({"status": "FAIL", "epsilon": str(eps),
                                  "triangle": str(keys), "isolated_point": str(isolated)},
                                 indent=2), flush=True)
                return 1
            isolated_checks += 1
    print(json.dumps({"status": "PASS", "epsilon": str(eps),
                      "hypergraph": "Fano plane", "facets": len(facets),
                      "triangles": len(triangles), "pairs_checked": checked,
                      "exact_intersection_vertices_checked": feasible_vertices,
                      "incidence_graph_cycle_rank": cycle_rank,
                      "isolated_original_vertices": len(isolated_points),
                      "isolated_point_triangle_checks": isolated_checks},
                     indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10**10))

#!/usr/bin/env python3
"""Exact coordinate/facet audit; Python standard library only, no asserts.

Run: python3 verifier.py; python3 -O verifier.py.
Facets are reconstructed from coordinates, NOT supplied from index-pair formulas.
The index-pair formulas are compared only after the geometric face lattice exists.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import gcd
import json


class CheckFailure(RuntimeError):
    pass


def check(condition, message):
    if not condition:
        raise CheckFailure(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def determinant(rows):
    """Bareiss exact integer determinant, including row swaps."""
    a = [list(row) for row in rows]
    n = len(a)
    if n == 0:
        return 1
    sign, previous = 1, 1
    for k in range(n-1):
        pivotrow = next((i for i in range(k, n) if a[i][k]), None)
        if pivotrow is None:
            return 0
        if pivotrow != k:
            a[k], a[pivotrow] = a[pivotrow], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = a[i][j]*pivot - a[i][k]*a[k][j]
                check(numerator % previous == 0, "nonexact Bareiss division")
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    if not a:
        return 0
    r, n = 0, len(a[0])
    for col in range(n):
        pivotrow = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivotrow is None:
            continue
        a[r], a[pivotrow] = a[pivotrow], a[r]
        pivot = a[r][col]
        a[r] = [x/pivot for x in a[r]]
        for i in range(r+1, len(a)):
            if a[i][col]:
                scalar = a[i][col]
                a[i] = [x-scalar*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def affine_dimension(points):
    points = list(points)
    if not points:
        return -1
    p = points[0]
    return rank([[x-y for x, y in zip(q, p)] for q in points[1:]])


def facet_hull(points):
    """All supporting facets via all d-point candidates of a full-dimensional hull."""
    points = tuple(sorted(set(points)))
    d = len(points[0])
    check(affine_dimension(points) == d, "facet_hull requires full dimension")
    facets = {}
    for ids in combinations(range(len(points)), d):
        p = points[ids[0]]
        rows = [[x-y for x, y in zip(points[i], p)] for i in ids[1:]]
        normal = tuple(((-1)**j)*determinant([row[:j]+row[j+1:] for row in rows])
                       for j in range(d))
        if not any(normal):
            continue
        h = dot(normal, p)
        values = [dot(normal, q)-h for q in points]
        if all(v <= 0 for v in values):
            pass
        elif all(v >= 0 for v in values):
            normal, h = neg(normal), -h
            values = [-v for v in values]
        else:
            continue
        check(any(v < 0 for v in values), "support unexpectedly contains full hull")
        scale = 0
        for x in normal+(h,):
            scale = gcd(scale, abs(x))
        normal, h = tuple(x//scale for x in normal), h//scale
        face = frozenset(i for i, v in enumerate(values) if v == 0)
        check(affine_dimension(points[i] for i in face) == d-1, "bad facet rank")
        facets[(normal, h)] = face
    facets = tuple((n, h, facets[(n, h)]) for n, h in sorted(facets))
    check(facets, "no facets")
    return points, facets


def face_lattice(points, facets):
    """Closure under intersection, including whole and empty faces."""
    faces = {frozenset(range(len(points)))}
    for _, _, facet in facets:
        faces.update(f & facet for f in tuple(faces))
    check(frozenset() in faces, "empty face absent")
    return tuple(sorted(faces, key=lambda f: (len(f), tuple(sorted(f)))))


def expose(points, normal):
    values = [dot(p, normal) for p in points]
    top = max(values)
    return frozenset(i for i, v in enumerate(values) if v == top)


def simplex(m):
    return ((0,)*m,)+tuple(tuple(int(i == j) for j in range(m)) for i in range(m))


def sum_vertex_points(p1, a, p2, b):
    return {add(p1[i], p2[j]) for i in a for j in b}


def audit_exposures(points, facets, faces, p1, p2):
    """Recover canonical summands by a positive sum of all containing normals."""
    records = {}
    for face in faces:
        if not face:
            continue
        containing = [n for n, _, v in facets if face <= v]
        normal = tuple(sum(n[j] for n in containing) for j in range(len(points[0])))
        check(expose(points, normal) == face, "facet-normal sum exposes wrong face")
        a, b = expose(p1, normal), expose(p2, normal)
        da, db = affine_dimension(p1[i] for i in a), affine_dimension(p2[i] for i in b)
        df = affine_dimension(points[i] for i in face)
        # Face vertices must be among pair sums; all pair sums lie on exposed support.
        sums = sum_vertex_points(p1, a, p2, b)
        check({points[i] for i in face} <= sums, "sum missing hull-face vertex")
        h = max(dot(q, normal) for q in points)
        check(all(dot(q, normal) == h for q in sums), "summand sum outside face support")
        # A second normal lies in the same relative normal-cone interior.
        weights = list(range(1, len(containing)+1))
        other = tuple(sum(w*n[j] for w, n in zip(weights, containing))
                      for j in range(len(points[0])))
        check(expose(points, other) == face, "weighted normals expose wrong face")
        check(expose(p1, other) == a and expose(p2, other) == b,
              "canonical summands depend on exposing normal")
        records[face] = {"a": a, "b": b, "dims": (df, da, db), "normal": normal,
                         "mixed": da > 0 and db > 0 and df == da+db}
    return records


def all_facepair_uniqueness(points, facets, faces, p1, p2, f1, f2, records):
    """Check all summand face pairs, including pairs without a common normal.

    Their sum lies in its minimal sum face. It equals that face iff it contains
    every extreme vertex of that face. Thus no floating point convex-hull test
    or unproved arbitrary-decomposition assumption is used here.
    """
    nonempty = [f for f in faces if f]
    canonical_facet1 = [expose(p1, n) for n, _, _ in facets]
    canonical_facet2 = [expose(p2, n) for n, _, _ in facets]
    masks1 = {a: {k for k, c in enumerate(canonical_facet1) if a <= c} for a in f1 if a}
    masks2 = {b: {k for k, c in enumerate(canonical_facet2) if b <= c} for b in f2 if b}
    counts = Counter()
    not_faces = 0
    checked = 0
    full = frozenset(range(len(points)))
    for a, maska in masks1.items():
        for b, maskb in masks2.items():
            checked += 1
            candidate = full
            for k in maska & maskb:
                candidate = candidate & facets[k][2]
            check(candidate in records, "minimal containing face absent")
            sums = sum_vertex_points(p1, a, p2, b)
            if all(points[i] in sums for i in candidate):
                counts[candidate] += 1
                check(records[candidate]["a"] == a and records[candidate]["b"] == b,
                      "noncanonical decomposition reproduces sum face")
            else:
                not_faces += 1
    check(set(counts) == set(nonempty), "some sum faces have no decomposition")
    check(all(counts[f] == 1 for f in nonempty), "decomposition not unique")
    return {"face_pairs_checked": checked, "pairs_equal_to_sum_faces": sum(counts.values()),
            "pairs_not_sum_faces": not_faces, "unique_for_all_nonempty_faces": True}


def compare_index_classification(m, points, records, endpoints=None):
    """POST-HOC comparison with claimed A,B indexing, not construction of lattice."""
    s = simplex(m)
    candidates = {}
    for labels in product(range(3), repeat=m+1):
        a = frozenset(i for i, x in enumerate(labels) if x == 1)
        b = frozenset(i for i, x in enumerate(labels) if x == 2)
        if not a or not b:
            continue
        base = {tuple(x-y for x, y in zip(s[i], s[j])) for i in a for j in b}
        heights = [None] if endpoints is None else endpoints
        for height in heights:
            vertices = base if height is None else {v+(height,) for v in base}
            ids = frozenset(i for i, p in enumerate(points) if p in vertices)
            check(ids in records, "index-pair candidate not geometrically reconstructed")
            check(len(ids) == len(vertices), "unexpected nonvertex in A,B product")
            check(ids not in candidates, "index-pair duplicate face")
            candidates[ids] = (a, b, height)
            check(records[ids]["dims"] == (len(a)+len(b)-2, len(a)-1, len(b)-1),
                  "index dimension or canonical dimensions disagree")
    mixed = {f for f, r in records.items() if r["mixed"]}
    predicted_mixed = {f for f, (a, b, _) in candidates.items() if len(a) >= 2 and len(b) >= 2}
    check(mixed == predicted_mixed, "mixed face classification mismatch")
    # All ordered face-pair inclusions, not only covers or predicted mixed faces.
    inclusion_checks = 0
    for f, (a, b, h) in candidates.items():
        for g, (c, d, k) in candidates.items():
            check((f <= g) == (h == k and a <= c and b <= d), "index inclusion mismatch")
            inclusion_checks += 1
    return candidates, inclusion_checks


def graph_summary(records):
    mixed = sorted((f for f, r in records.items() if r["mixed"]), key=lambda f: tuple(sorted(f)))
    adjacent = {f: set() for f in mixed}
    for a, b in combinations(mixed, 2):
        if a < b or b < a:
            adjacent[a].add(b)
            adjacent[b].add(a)
    check(all(not (a < b < c) for a in mixed for b in adjacent[a]
              for c in adjacent[b]), "chain length three: complex not a graph")
    check(all(adjacent[f] for f in mixed) or not mixed, "isolated vertex: graph not pure")
    unseen, components = set(mixed), []
    while unseen:
        seed = min(unseen, key=lambda f: tuple(sorted(f)))
        stack, reached = [seed], {seed}
        while stack:
            for b in adjacent[stack.pop()]:
                if b not in reached:
                    reached.add(b)
                    stack.append(b)
        unseen -= reached
        edges = sum(len(adjacent[f]) for f in reached)//2
        components.append({"vertices": len(reached), "edges": edges,
                           "cycle_rank": edges-len(reached)+1})
    return {"vertices": len(mixed), "edges": sum(len(a) for a in adjacent.values())//2,
            "components": sorted(components, key=lambda d: (d["vertices"], d["edges"])),
            "degree_histogram": dict(sorted(Counter(len(a) for a in adjacent.values()).items())),
            "mixed_face_dimensions": dict(sorted(Counter(records[f]["dims"][0] for f in mixed).items()))}


def control_rejected(function, label):
    try:
        function()
    except CheckFailure:
        return label
    raise CheckFailure("adverse control was not rejected: "+label)


def main():
    # Sanity checks deliberately survive Python -O.
    check(determinant([[0, 1], [1, 0]]) == -1, "determinant row-swap control")
    check(determinant([[2, 4], [1, 2]]) == 0, "determinant singular control")
    check(rank([[Fraction(1, 3), Fraction(1, 7)], [Fraction(2, 3), Fraction(2, 7)]]) == 1,
          "rational rank control")
    s = simplex(4)
    p1 = tuple(sorted(v+(h,) for v in s for h in (0, 1)))
    p2 = tuple(sorted(neg(v)+(h,) for v in s for h in (0, 1)))
    base_input = {tuple(x-y for x, y in zip(a, b)) for a in s for b in s}
    # The origin is an input sum but not a hull vertex; remove it only after
    # checking it is the exact average of opposite root vertices.
    zero = (0,)*4
    check(zero in base_input, "sum interior point absent")
    root_points = base_input-{zero}
    check(all(neg(v) in root_points for v in root_points), "central-symmetry control")
    q, qfacets = facet_hull(root_points)
    qfaces = face_lattice(q, qfacets)
    qrecords = audit_exposures(q, qfacets, qfaces, s, tuple(neg(v) for v in s))
    qclasses, qincl = compare_index_classification(4, q, qrecords)
    # All facets of a Cartesian product Q x [0,2] are either vertical lifts
    # of Q facets or the two horizontal endpoints. Proved in REPORT.md.
    total = tuple(sorted(v+(h,) for v in q for h in (0, 2)))
    sfacets = []
    for n, h, _ in qfacets:
        normal = n+(0,)
        sfacets.append((normal, h, expose(total, normal)))
    for t in (-1, 1):
        normal = (0, 0, 0, 0, t)
        h = max(dot(p, normal) for p in total)
        sfacets.append((normal, h, expose(total, normal)))
    sfacets = tuple(sorted(sfacets))
    sfaces = face_lattice(total, sfacets)
    records = audit_exposures(total, sfacets, sfaces, p1, p2)
    classes, sincl = compare_index_classification(4, total, records, endpoints=(0, 2))
    # Product structure is checked AFTER facet-intersection enumeration.
    product_types = Counter()
    all_inclusion_checks = 0
    classification = {}
    for f, r in records.items():
        base = frozenset(q.index(total[i][:4]) for i in f)
        heights = frozenset(total[i][4] for i in f)
        check(base in qrecords, "projection not a base face")
        check(heights in (frozenset({0}), frozenset({2}), frozenset({0, 2})), "bad interval face")
        expected_vertices = {q[i]+(h,) for i in base for h in heights}
        check({total[i] for i in f} == expected_vertices, "nonproduct exposed face")
        df, da, db = r["dims"]
        bdf, bda, bdb = qrecords[base]["dims"]
        full_interval = len(heights) == 2
        shift = int(full_interval)
        check((df, da, db) == (bdf+shift, bda+shift, bdb+shift), "product dimension mismatch")
        if full_interval:
            check(df < da+db, "full interval direction erroneously additive")
        else:
            check(r["mixed"] == qrecords[base]["mixed"], "endpoint positivity/additivity mismatch")
        product_types["full_interval" if full_interval else "lower" if 0 in heights else "upper"] += 1
        classification[f] = (base, heights)
    for f, (a, h) in classification.items():
        for g, (b, k) in classification.items():
            check((f <= g) == (a <= b and h <= k), "full product inclusion mismatch")
            all_inclusion_checks += 1
    pp1, p1facets = facet_hull(p1)
    pp2, p2facets = facet_hull(p2)
    check(pp1 == p1 and pp2 == p2, "summand coordinate ordering mismatch")
    p1faces, p2faces = face_lattice(p1, p1facets), face_lattice(p2, p2facets)
    uniqueness = all_facepair_uniqueness(total, sfacets, sfaces, p1, p2, p1faces, p2faces, records)
    graph = graph_summary(records)
    basegraph = graph_summary(qrecords)
    check(len(qfacets) == 30 and len(qfaces) == 182, "base face count mismatch")
    check(len(sfacets) == 32 and len(sfaces) == 544, "sum face count mismatch")
    check(graph["vertices"] == 100 and graph["edges"] == 120, "mixed graph count mismatch")
    check(graph["components"] == [{"vertices": 50, "edges": 60, "cycle_rank": 11}]*2,
          "component count mismatch")
    check(basegraph["components"] == [{"vertices": 50, "edges": 60, "cycle_rank": 11}],
          "base graph mismatch")
    # Controls intentionally imitate the most plausible wrong implementations.
    rejected = []
    rejected.append(control_rejected(lambda: check(len(records) == 542, "whole sum omitted"),
                                      "omit whole face from all-face census"))
    full = frozenset(range(len(total)))
    check(records[full]["dims"] == (5, 5, 5) and not records[full]["mixed"], "whole-face control")
    for h in (0, 2):
        f = frozenset(i for i, p in enumerate(total) if p[4] == h)
        check(records[f]["dims"] == (4, 4, 4) and not records[f]["mixed"], "end-face control")
    false_vertical = next(f for f, r in records.items() if
                          len({total[i][4] for i in f}) == 2 and r["dims"] == (3, 2, 2))
    rejected.append(control_rejected(lambda: check(records[false_vertical]["mixed"], "shared interval ignored"),
                                      "count shared interval direction only once in summands"))
    false_positive = next(f for f, r in records.items() if r["dims"] == (1, 0, 1))
    rejected.append(control_rejected(lambda: check(records[false_positive]["mixed"], "zero summand allowed"),
                                      "drop positive dimension requirement"))
    reversed_pair = next((f, g) for f, x in classes.items() for g, y in classes.items()
                         if x[0] < y[0] and x[1] == y[1] and x[2] == y[2])
    rejected.append(control_rejected(lambda: check(reversed_pair[1] <= reversed_pair[0], "order reversed"),
                                      "reverse face inclusion"))
    # Remove a facet to ensure the closure census detects an incomplete hull.
    missing_faces = face_lattice(q, qfacets[:-1])
    rejected.append(control_rejected(lambda: check(set(missing_faces) == set(qfaces), "facet missing"),
                                      "remove one supporting facet"))
    check(frozenset() not in records, "empty face improperly given summands")
    # Dimension-three control: reconstruction again starts from coordinates.
    t = simplex(3)
    roots3 = {tuple(x-y for x, y in zip(a, b)) for a in t for b in t if a != b}
    q3, facets3 = facet_hull(roots3)
    faces3 = face_lattice(q3, facets3)
    r3 = audit_exposures(q3, facets3, faces3, t, tuple(neg(v) for v in t))
    mixed3 = [f for f, r in r3.items() if r["mixed"]]
    check(len(mixed3) == 6 and all(not (a < b or b < a) for a, b in combinations(mixed3, 2)),
          "tetrahedron difference control")
    output = {
        "status": "PASS", "arithmetic": "integer Bareiss determinants; Fraction Gaussian ranks; no asserts",
        "base_input_distinct_points_including_interior_origin": len(base_input),
        "base": {"vertices": len(q), "facets": len(qfacets), "faces_including_empty_whole": len(qfaces),
                 "nonempty_faces_by_dimension": dict(sorted(Counter(r["dims"][0] for r in qrecords.values()).items())),
                 "posthoc_index_inclusion_checks": qincl, "mixed_graph": basegraph},
        "summands": {"vertices_each": len(p1), "facets_each": len(p1facets),
                     "nonempty_faces_each": len(p1faces)-1},
        "sum": {"vertices": len(total), "facets": len(sfacets), "faces_including_empty_whole": len(sfaces),
                "nonempty_faces_by_dimension": dict(sorted(Counter(r["dims"][0] for r in records.values()).items())),
                "product_face_types": dict(sorted(product_types.items())),
                "all_nonempty_product_inclusion_checks": all_inclusion_checks,
                "endpoint_index_inclusion_checks": sincl, "mixed_graph": graph},
        "canonical_decomposition": uniqueness,
        "whole_face_dimensions_sum_P1_P2": records[full]["dims"],
        "tetrahedron_control": {"vertices": len(q3), "facets": len(facets3),
                                "faces_including_empty_whole": len(faces3), "mixed_antichain_size": len(mixed3)},
        "adverse_controls_rejected": rejected,
        "boundary_cases": "empty excluded; whole and both end faces tested; vertical faces exhaustively rejected"
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact supplemental checks; the infinite-family proof is in PROOF.md.

Uses Python standard library only. All geometric predicates use integers;
intersection coordinates use fractions. Random checks use a fixed seed and
are explicitly supplemental, never evidence for the universal quantifier.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random


def drawing(m, n):
    a, h = m // 2, n // 2
    pts = [(-i, 0) for i in range(1, a + 1)]
    pts += [(i, 0) for i in range(1, m - a + 1)]
    pts += [(0, -j) for j in range(1, h + 1)]
    pts += [(0, j) for j in range(1, n - h + 1)]
    edges = [(x, y) for x in range(m) for y in range(m, m + n)]
    return pts, edges


def orientation(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def proper_cross(a, b, c, d):
    return orientation(a, b, c)*orientation(a, b, d) < 0 and \
           orientation(c, d, a)*orientation(c, d, b) < 0


def intersection(a, b, c, d):
    dx, dy = b[0]-a[0], b[1]-a[1]
    ex, ey = d[0]-c[0], d[1]-c[1]
    determinant = dx*ey-dy*ex
    t = Fraction((c[0]-a[0])*ey-(c[1]-a[1])*ex, determinant)
    return (a[0]+t*dx, a[1]+t*dy)


def instance(m, n):
    pts, edges = drawing(m, n)
    pairs, bits, locations = [], [], defaultdict(list)
    assert len(pts) == len(set(pts)) == m+n
    for e in edges:
        a, b = [pts[v] for v in e]
        for v, c in enumerate(pts):
            if v not in e:
                assert not (orientation(a, b, c) == 0 and
                            min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
                            min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))
    for i, j in combinations(range(len(edges)), 2):
        e, f = edges[i], edges[j]
        a, b = [pts[v] for v in e]
        c, d = [pts[v] for v in f]
        hit = proper_cross(a, b, c, d)
        if set(e) & set(f):
            assert not hit
            continue
        pairs.append((i, j))
        bits.append(int(hit))
        expected = (pts[e[0]][0]*pts[f[0]][0] > 0 and
                    pts[e[1]][1]*pts[f[1]][1] > 0 and
                    (abs(pts[e[0]][0])-abs(pts[f[0]][0])) *
                    (abs(pts[e[1]][1])-abs(pts[f[1]][1])) < 0)
        assert hit == expected
        if hit:
            locations[intersection(a, b, c, d)].append((i, j))
    q = (n//2)*((n-1)//2)
    assert len(pairs) == m*(m-1)*n*(n-1)//2
    assert sum(bits) == (m-2)*q
    assert all(len(es) == 1 for es in locations.values())
    return pts, edges, pairs, bits


def local_identity_checks(m, n, edges, pairs, bits):
    count = 0
    for xs in combinations(range(m), 3):
        for ys in combinations(range(m, m+n), 3):
            vertices = set(xs+ys)
            local = [k for k, (i, j) in enumerate(pairs)
                     if set(edges[i]+edges[j]) <= vertices]
            assert len(local) == 18
            assert sum(bits[k] for k in local) in (1, 3)
            coefficients = Counter()
            for k in local:
                i, j = pairs[k]
                for v in edges[j]:
                    coefficients[(i, v)] += 1
                for v in edges[i]:
                    coefficients[(j, v)] += 1
            assert len(coefficients) == 36
            assert set(coefficients.values()) == {2}
            count += 1
    return count


def exhaustive_k33_image():
    _, edges, pairs, c = instance(3, 3)
    columns = []
    for i, e in enumerate(edges):
        for v in range(6):
            if v in e:
                continue
            vector = 0
            for k, (a, b) in enumerate(pairs):
                if (a == i and v in edges[b]) or (b == i and v in edges[a]):
                    vector ^= 1 << k
            columns.append(vector)
    basis = {}
    for column in columns:
        v = column
        while v:
            pivot = v.bit_length()-1
            if pivot in basis:
                v ^= basis[pivot]
            else:
                basis[pivot] = v
                break
    vectors = list(basis.values())
    baseline = sum(bit << k for k, bit in enumerate(c))
    histogram = Counter()
    value = baseline
    previous = 0
    for i in range(1 << len(vectors)):
        gray = i ^ (i >> 1)
        if i:
            change = gray ^ previous
            value ^= vectors[change.bit_length()-1]
        histogram[value.bit_count()] += 1
        previous = gray
    assert len(columns) == 36 and len(pairs) == 18
    assert len(vectors) == 17 and min(histogram) == 1
    assert all(weight % 2 for weight in histogram)
    return {"incidence_variables": len(columns), "independent_pairs": len(pairs),
            "switch_image_rank": len(vectors), "distinct_switched_vectors": 1 << len(vectors),
            "minimum_weight": min(histogram),
            "weight_histogram": dict(sorted(histogram.items()))}


def main():
    rng = random.Random(1782)
    rows = []
    for m in (3, 4):
        for n in range(3, 33):
            _, edges, pairs, c = instance(m, n)
            local_count = local_identity_checks(m, n, edges, pairs, c) if n <= 10 else None
            sample_count = 64 if n <= 16 else 0
            endpoint_masks = [(1 << u) | (1 << v) for u, v in edges]
            for _ in range(sample_count):
                assignments = [rng.getrandbits(m+n) & ~mask for mask in endpoint_masks]
                b = [bit ^ (((assignments[i] & endpoint_masks[j]).bit_count() +
                             (assignments[j] & endpoint_masks[i]).bit_count()) & 1)
                     for (i, j), bit in zip(pairs, c)]
                assert sum(b) >= sum(c)
                for xs in combinations(range(m), 3):
                    weights = Counter()
                    for (i, j), bit in zip(pairs, b):
                        if edges[i][0] in xs and edges[j][0] in xs:
                            weights[tuple(sorted((edges[i][1], edges[j][1])))] += bit
                    y0 = m
                    labels = {y0: 0}
                    labels.update({y: 1 ^ (weights[(y0, y)] & 1)
                                   for y in range(m+1, m+n)})
                    for y, z in combinations(range(m, m+n), 2):
                        assert (weights[(y, z)] & 1) == (1 ^ labels[y] ^ labels[z])
            rows.append({"m": m, "n": n, "independent_pairs": len(pairs),
                         "crossings": sum(c), "nice_exact_geometry": True,
                         "local_k33_identities_checked": local_count,
                         "supplemental_seeded_assignments_checked": sample_count})
    result = {"status": "PASS", "role": "supplemental only; infinite-family proof is PROOF.md",
              "arithmetic": "integer orientation, rational intersection, GF(2) switch identity",
              "cases": rows, "exhaustive_k33_switch_image": exhaustive_k33_image()}
    out = Path(__file__).with_name("exact_checks.json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "geometry_cases": len(rows),
                      "local_k33_subgraphs": sum(r["local_k33_identities_checked"] or 0 for r in rows),
                      "seeded_assignments": sum(r["supplemental_seeded_assignments_checked"] for r in rows),
                      "k33_image_rank": result["exhaustive_k33_switch_image"]["switch_image_rank"],
                      "k33_minimum_weight": result["exhaustive_k33_switch_image"]["minimum_weight"]}))


if __name__ == "__main__":
    main()

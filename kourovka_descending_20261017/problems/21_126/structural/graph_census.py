#!/usr/bin/env python3
"""Exact finite census of the sufficient ambient exclusion class in FORESTS_AND_CLOSURE.
No group computations and no assertion that graphs outside the class are viable.
Run with Python3 standard library only; deterministic certificate output.
"""
from functools import lru_cache
from itertools import combinations, permutations
import json
from pathlib import Path


def adjacency(n, mask):
    rows = [0] * n
    for k, (i, j) in enumerate(combinations(range(n), 2)):
        if mask >> k & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return tuple(rows)


def induce(rows, verts):
    return tuple(sum(1 << j for j, w in enumerate(verts) if rows[v] >> w & 1)
                 for v in verts)


def components(rows, complement=False):
    left = set(range(len(rows)))
    result = []
    while left:
        first = min(left)
        left.remove(first)
        reached, todo = [first], [first]
        while todo:
            v = todo.pop()
            found = [w for w in sorted(left)
                     if bool(rows[v] >> w & 1) != complement]
            for w in found:
                left.remove(w)
                reached.append(w)
                todo.append(w)
        result.append(tuple(sorted(reached)))
    return tuple(result)


@lru_cache(None)
def sufficient(rows):
    n = len(rows)
    if not n:
        return True
    comps = components(rows)
    edge_count = sum(x.bit_count() for x in rows) // 2
    if edge_count == n - len(comps):
        return True  # graph is a forest
    anti = components(rows, complement=True)
    if len(anti) <= 3 and all(
        all(not (rows[v] >> w & 1) for v, w in combinations(part, 2))
        for part in anti
    ):
        return True  # complete multipartite, at most 3 parts
    if len(comps) > 1:
        return all(sufficient(induce(rows, part)) for part in comps)
    universals = [v for v in range(n) if rows[v].bit_count() == n - 1]
    if universals:
        remaining = tuple(v for v in range(n) if v not in universals)
        return sufficient(induce(rows, remaining))
    return False


def canonical(n, mask):
    rows = adjacency(n, mask)
    pairs = tuple(combinations(range(n), 2))
    return min(sum(1 << k for k, (i, j) in enumerate(pairs)
                   if rows[p[i]] >> p[j] & 1)
               for p in permutations(range(n)))


def main():
    result = {"meaning": "sufficient exclusion class only; not a search for actual subgroup witnesses",
              "definition": "forests and complete multipartite <=3 parts; disjoint union and universal-vertex closure",
              "labelled_counts": [], "isomorphism_counts": []}
    for n in range(7):
        masks = range(1 << (n * (n - 1) // 2))
        inside, outside = [], []
        for mask in masks:
            (inside if sufficient(adjacency(n, mask)) else outside).append(mask)
        result["labelled_counts"].append({"vertices": n, "inside": len(inside), "outside": len(outside)})
        if n <= 5:
            yes = {canonical(n, mask) for mask in inside}
            no = {canonical(n, mask) for mask in outside}
            assert not yes & no
            result["isomorphism_counts"].append({"vertices": n, "inside": len(yes), "outside": len(no),
                                                   "outside_canonical_masks": sorted(no)})
    assert all(row["outside"] == 0 for row in result["labelled_counts"] if row["vertices"] <= 4)
    # F2^4 lies outside this class: four independent parts of size2.
    k = 0
    mask = 0
    for v, w in combinations(range(8), 2):
        if v // 2 != w // 2:
            mask |= 1 << k
        k += 1
    assert not sufficient(adjacency(8, mask))
    result["boundary_checks"] = {"all_graphs_at_most4_inside": True, "F2_power4_outside": True}
    out = Path(__file__).with_name('graph_census.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

"""Exhaustive atomic sanity checks for the compression construction.

This checks equal-weight finite atomic spaces through five points. It does
not certify the Borel/infinite-class part of the theorem. All arithmetic is
integer arithmetic in units of one atom's measure.
"""

import itertools
import json
from collections import deque
from pathlib import Path


def partitions(n):
    """Restricted-growth strings enumerate each set partition once."""
    def extend(prefix, maximum):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        for value in range(maximum + 2):
            yield from extend(prefix + [value], max(maximum, value))
    if n == 0:
        yield ()
    else:
        yield from extend([0], 0)


def join(partition, edges):
    n = len(partition)
    parents = list(range(n))
    def root(x):
        while parents[x] != x:
            parents[x] = parents[parents[x]]
            x = parents[x]
        return x
    def unite(x, y):
        parents[root(x)] = root(y)
    for x in range(n):
        for y in range(x):
            if partition[x] == partition[y]:
                unite(x, y)
    for x, y in edges:
        unite(x, y)
    return tuple(root(x) for x in range(n))


def refines(smaller, larger):
    return all(smaller[x] != smaller[y] or larger[x] == larger[y]
               for x in range(len(smaller)) for y in range(x))


def equivalent(left, right):
    return refines(left, right) and refines(right, left)


def check(s, t, edges):
    n = len(s)
    blocks = sorted(set(s))
    roots = {min(x for x in range(n) if t[x] == block) for block in set(t)}
    retained = {s[x] for x in roots}
    y = {x for x in range(n) if s[x] in retained}
    distance = {block: 0 for block in retained}
    queue = deque(retained)
    while queue:
        block = queue.popleft()
        for x, z in edges:
            for origin, target in ((x, z), (z, x)):
                if s[target] == block and s[origin] not in distance:
                    distance[s[origin]] = distance[block] + 1
                    queue.append(s[origin])
    assert set(distance) == set(blocks)
    selected = {}
    for block in blocks:
        if block in retained:
            continue
        for index, (x, z) in enumerate(edges):
            eligible = [(origin, target) for origin, target in ((x, z), (z, x))
                        if s[origin] == block
                        and distance[s[target]] == distance[block] - 1]
            if eligible:
                selected[block] = (index, *min(eligible))
                break
    deleted = {data[0] for data in selected.values()}
    assert len(deleted) == len(selected), "Two classes selected one edge instance"
    f = {x: x for x in y}
    for block in sorted(selected, key=distance.get):
        target = selected[block][2]
        for x in range(n):
            if s[x] == block:
                f[x] = f[target]
    for index, x, z in selected.values():
        assert f[x] == f[z]
    pushed = [(f[x], f[z]) for index, (x, z) in enumerate(edges)
              if index not in deleted]
    assert equivalent(join(s, edges), join(t, pushed))
    assert len(pushed) == len(edges) - len(set(s)) + len(set(t))


def main():
    rows = []
    for n in range(1, 6):
        parts = list(partitions(n))
        possible_edges = list(itertools.combinations(range(n), 2))
        count = 0
        for mask in range(1 << len(possible_edges)):
            edges = [edge for index, edge in enumerate(possible_edges)
                     if mask & (1 << index)]
            for s in parts:
                q = join(s, edges)
                for t in parts:
                    if refines(s, t) and refines(t, q):
                        check(s, t, edges)
                        count += 1
        rows.append({"atoms": n, "partitions": len(parts),
                     "simple_graphs": 1 << len(possible_edges),
                     "admissible_triples_checked": count})
    # Edge repetitions, loops, and a noninjective f require separate cases.
    special = [((0, 1, 2, 3), (0, 0, 0, 0),
                [(0, 1), (0, 1), (1, 2), (2, 3), (3, 0), (2, 2)]),
               ((0, 0, 1, 1, 2), (0, 0, 0, 0, 0),
                [(1, 2), (3, 4), (0, 4), (0, 0)])]
    for s, t, edges in special:
        check(s, t, edges)
    result = {"status": "PASS", "scope": "finite equal-weight atomic spaces",
              "rows": rows, "special_cases": len(special),
              "total": sum(row["admissible_triples_checked"] for row in rows)
              + len(special)}
    Path(__file__).with_name("finite_boundary_results.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

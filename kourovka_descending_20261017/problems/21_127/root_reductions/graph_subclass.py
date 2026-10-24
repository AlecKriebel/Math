"""Exact finite graph census for a credited known rational-scl subclass.

No scl computation or full rationality theorem is claimed.
"""
from itertools import combinations, permutations
from pathlib import Path
import json


def components(vertices, edges, complement=False):
    todo = set(vertices)
    answer = []
    while todo:
        seed = min(todo)
        found, stack = set(), [seed]
        while stack:
            v = stack.pop()
            if v in found:
                continue
            found.add(v)
            stack.extend(w for w in todo - found
                         if ((tuple(sorted((v, w))) in edges) != complement))
        todo -= found
        answer.append(sorted(found))
    return answer


def in_subclass(n, edges):
    # Join factors are complement components; every factor must be a cluster.
    for block in components(range(n), edges, complement=True):
        for piece in components(block, edges):
            if any(pair not in edges for pair in combinations(piece, 2)):
                return False
    return True


def canonical(n, edges):
    return min(tuple(int(tuple(sorted((p[i], p[j]))) in edges)
                     for i, j in combinations(range(n), 2))
               for p in permutations(range(n)))


def main():
    rows = []
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        classes = {}
        yes = 0
        for mask in range(1 << len(pairs)):
            edges = {pair for j, pair in enumerate(pairs) if (mask >> j) & 1}
            value = in_subclass(n, edges)
            yes += value
            key = canonical(n, edges)
            if key in classes:
                assert classes[key] == value
            classes[key] = value
        assert len(classes) == [1, 2, 4, 11, 34][n - 1]
        assert n > 3 or all(classes.values())
        outside = [list(k) for k, v in classes.items() if not v]
        if n == 4:
            p4 = {(0, 1), (1, 2), (2, 3)}
            p3_isolated = {(0, 1), (1, 2)}
            assert {tuple(x) for x in outside} == {
                canonical(n, p4), canonical(n, p3_isolated)}
        rows.append({"vertices": n, "labelled_total": 1 << len(pairs),
                     "labelled_inside": yes, "isomorphism_classes": len(classes),
                     "classes_inside": sum(classes.values()),
                     "classes_outside_reduction_canonical_bits": outside})
    output = Path(__file__).with_name("graph_subclass.json")
    output.write_text(json.dumps({"scope": "join of cluster graphs only; not all rational cases",
                                  "rows": rows}, indent=2) + "\n")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()

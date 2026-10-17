#!/usr/bin/env python3
"""Source-free reconstruction of the supplied finite L(2,1) instance.

Python standard library only. Normal replay: `python3 -B replay.py`.
To write a neutral current output: `python3 reconstruct.py --output current.json`.
No external files, network, source-author implementation, or candidate proof read.
"""

import argparse
from collections import deque
from itertools import combinations, product
from functools import lru_cache
import json
from random import Random


VERTICES = ("a", "b", "c", "d", "e", "a1", "a2", "b1", "d1", "e1", "e2")
EDGES = (("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"),
         ("a", "a1"), ("a", "a2"), ("b", "b1"), ("d", "d1"),
         ("e", "e1"), ("e", "e2"))
A = (1, 2, 3, 4, 5)
B = (1, 3, 4, 5, 6)
B_VERTICES = frozenset(("a1", "a2", "e1", "e2"))
SUPPLIED = {v: B if v in B_VERTICES else A for v in VERTICES}


def adjacency(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        assert u in adj and v in adj and u != v
        adj[u].add(v)
        adj[v].add(u)
    return adj


def valid_by_bfs(vertices, edges, lists, labeling):
    """Independent checker: compute graph distances directly by BFS."""
    if set(labeling) != set(vertices):
        return False
    if any(labeling[v] not in lists[v] for v in vertices):
        return False
    adj = adjacency(vertices, edges)
    for u in vertices:
        distance = {u: 0}
        todo = deque([u])
        while todo:
            v = todo.popleft()
            if distance[v] == 2:
                continue
            for w in adj[v]:
                if w not in distance:
                    distance[w] = distance[v] + 1
                    todo.append(w)
        for v, d in distance.items():
            if d == 1 and abs(labeling[u] - labeling[v]) < 2:
                return False
            if d == 2 and labeling[u] == labeling[v]:
                return False
    return True


def constraints(vertices, edges):
    """Build binary constraints using edges and common neighbors, not BFS."""
    adj = adjacency(vertices, edges)
    need = {v: {} for v in vertices}
    for u, v in edges:
        need[u][v] = need[v][u] = 2
    for center in vertices:
        for u, v in combinations(sorted(adj[center]), 2):
            need[u][v] = max(need[u].get(v, 0), 1)
            need[v][u] = max(need[v].get(u, 0), 1)
    return need


def exact_solutions(vertices, edges, lists):
    """Complete search, deterministic MRV, forward checking, exact count."""
    vertices = tuple(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    need = constraints(vertices, edges)
    domains = {v: tuple(sorted(set(lists[v]))) for v in vertices}
    assert all(domains[v] and all(isinstance(x, int) and x > 0
                                 for x in domains[v]) for v in vertices)
    nodes = 0
    count = 0
    first = None

    def search(assigned, remaining):
        nonlocal nodes, count, first
        nodes += 1
        if not remaining:
            count += 1
            if first is None:
                first = {v: assigned[v] for v in vertices}
            return
        v = min(remaining, key=lambda u: (len(remaining[u]),
                                         -len(need[u]), index[u]))
        for x in remaining[v]:
            updated = {}
            possible = True
            for u, domain in remaining.items():
                if u == v:
                    continue
                gap = need[v].get(u)
                if gap is None:
                    updated[u] = domain
                else:
                    reduced = tuple(y for y in domain if abs(x - y) >= gap)
                    if not reduced:
                        possible = False
                        break
                    updated[u] = reduced
            if possible:
                assigned[v] = x
                search(assigned, updated)
                del assigned[v]

    search({}, domains)
    if first is not None:
        assert valid_by_bfs(vertices, edges, lists, first)
    return {"count": count, "first": first, "search_nodes": nodes}


def naive_count(vertices, edges, lists):
    """Cartesian enumeration for independently checking small controls."""
    return sum(valid_by_bfs(vertices, edges, lists, dict(zip(vertices, values)))
               for values in product(*(lists[v] for v in vertices)))


def tree_dp_count(vertices, edges, lists, root):
    """Second exact method: sum child-star assignments bottom-up on the tree."""
    adj = adjacency(vertices, edges)
    parent = {root: None}
    children = {v: [] for v in vertices}
    order = [root]
    for v in order:
        for w in sorted(adj[v]):
            if w == parent[v]:
                continue
            assert w not in parent
            parent[w] = v
            children[v].append(w)
            order.append(w)
    assert len(order) == len(vertices)

    @lru_cache(None)
    def below(v, parent_label, label):
        child_domains = [tuple(x for x in lists[w]
                               if abs(x - label) >= 2 and x != parent_label)
                         for w in children[v]]
        total = 0
        for labels in product(*child_domains):
            if len(set(labels)) != len(labels):
                continue
            ways = 1
            for w, x in zip(children[v], labels):
                ways *= below(w, label, x)
            total += ways
        return total

    return sum(below(root, None, x) for x in lists[root])


def greedy_tree_lists(vertices, edges, lists, root):
    """Constructive Delta+3 list bound, parent-before-child BFS order."""
    adj = adjacency(vertices, edges)
    parent = {root: None}
    order = [root]
    for v in order:
        for w in sorted(adj[v]):
            if w == parent[v]:
                continue
            assert w not in parent, "Input must be a tree."
            parent[w] = v
            order.append(w)
    assert len(order) == len(vertices)
    delta = max(map(len, adj.values()), default=0)
    required = 1 if delta == 0 else delta + 3
    assert all(len(set(lists[v])) >= required for v in vertices)
    labeling = {}
    steps = []
    for v in order:
        forbidden = set()
        p = parent[v]
        if p is not None:
            forbidden.update((labeling[p] - 1, labeling[p], labeling[p] + 1))
            for w in adj[p]:
                if w != v and w in labeling:
                    forbidden.add(labeling[w])
        choices = sorted(set(lists[v]) - forbidden)
        assert choices
        labeling[v] = choices[0]
        steps.append({"vertex": v, "forbidden": sorted(forbidden),
                      "chosen": choices[0]})
    assert valid_by_bfs(vertices, edges, lists, labeling)
    return {"labeling": labeling, "steps": steps, "delta": delta}


def extended_instance(lengths):
    """At most one outward path at each original leaf, lengths in edges."""
    vertices = list(VERTICES)
    edges = list(EDGES)
    for leaf, length in sorted(lengths.items()):
        assert leaf in ("a1", "a2", "b1", "d1", "e1", "e2")
        assert isinstance(length, int) and length >= 0
        previous = leaf
        for i in range(1, length + 1):
            v = f"{leaf}_path_{i}"
            vertices.append(v)
            edges.append((previous, v))
            previous = v
    return tuple(vertices), tuple(edges)


def ordinary_extension(labeling, lengths):
    """Extend a valid five-palette witness independently on each path."""
    adj = adjacency(VERTICES, EDGES)
    answer = dict(labeling)
    for leaf, length in sorted(lengths.items()):
        previous_label = labeling[next(iter(adj[leaf]))]
        current_label = labeling[leaf]
        for i in range(1, length + 1):
            choices = [x for x in A
                       if abs(x - current_label) >= 2 and x != previous_label]
            assert choices
            following = choices[0]
            answer[f"{leaf}_path_{i}"] = following
            previous_label, current_label = current_label, following
    vertices, edges = extended_instance(lengths)
    assert valid_by_bfs(vertices, edges, {v: A for v in vertices}, answer)
    return answer


def controls():
    results = []
    edge_v, edge_e = ("x", "y"), (("x", "y"),)
    cases = [
        ("adjacent_equal_rejected", edge_v, edge_e, {"x": (1,), "y": (1,)}, 0),
        ("adjacent_gap_one_rejected", edge_v, edge_e, {"x": (1,), "y": (2,)}, 0),
        ("adjacent_gap_two_accepted", edge_v, edge_e, {"x": (1,), "y": (3,)}, 1),
        ("distance_two_equality_rejected", ("x", "y", "z"),
         (("x", "y"), ("y", "z")), {"x": (1,), "y": (3,), "z": (1,)}, 0),
        ("distance_two_gap_one_accepted", ("x", "y", "z"),
         (("x", "y"), ("y", "z")), {"x": (1,), "y": (4,), "z": (2,)}, 1),
    ]
    for name, vertices, edges, lists, expected in cases:
        actual = exact_solutions(vertices, edges, lists)["count"]
        assert actual == expected == naive_count(vertices, edges, lists)
        results.append({"name": name, "expected": expected, "actual": actual})
    star_v = ("s", "u", "v", "w")
    star_e = (("s", "u"), ("s", "v"), ("s", "w"))
    for k, expected in ((4, 0), (5, 12)):
        lists = {v: tuple(range(1, k + 1)) for v in star_v}
        actual = exact_solutions(star_v, star_e, lists)["count"]
        assert actual == expected == naive_count(star_v, star_e, lists)
        results.append({"name": f"degree_three_star_palette_{k}",
                        "expected": expected, "actual": actual})
    rng = Random(121130000418)
    for trial in range(80):
        n = rng.randrange(1, 6)
        vertices = tuple(str(i) for i in range(n))
        edges = tuple((vertices[i], vertices[rng.randrange(i)]) for i in range(1, n))
        lists = {v: tuple(sorted(rng.sample(range(1, 8), rng.randrange(1, 5))))
                 for v in vertices}
        actual = exact_solutions(vertices, edges, lists)["count"]
        expected = naive_count(vertices, edges, lists)
        dp = tree_dp_count(vertices, edges, lists, vertices[0])
        assert actual == expected == dp, (trial, vertices, edges, lists, actual, expected, dp)
    results.append({"name": "seeded_small_tree_cartesian_crosschecks", "cases": 80,
                    "passed": True})
    # A positive gap may collapse during rank compression.
    original = {"x": (1,), "y": (3,)}
    compressed = {"x": (1,), "y": (2,)}
    assert exact_solutions(edge_v, edge_e, original)["count"] == 1
    assert exact_solutions(edge_v, edge_e, compressed)["count"] == 0
    results.append({"name": "rank_compression_forward_failure", "passed": True,
                    "original_lists": original, "compressed_lists": compressed})
    return results


def run():
    result = {"input": {"vertices": VERTICES, "edges": EDGES,
                         "A": A, "B": B, "B_vertices": sorted(B_VERTICES)}}
    result["ordinary"] = {
        str(k): exact_solutions(VERTICES, EDGES, {v: tuple(range(1, k + 1))
                                                 for v in VERTICES})
        for k in range(1, 6)}
    assert [result["ordinary"][str(k)]["count"] for k in range(1, 6)] == [0, 0, 0, 0, 8]
    result["supplied_lists"] = exact_solutions(VERTICES, EDGES, SUPPLIED)
    assert result["supplied_lists"]["count"] == 0
    result["tree_dynamic_program_counts"] = {
        "ordinary": {str(k): tree_dp_count(VERTICES, EDGES,
                                           {v: tuple(range(1, k + 1)) for v in VERTICES}, "c")
                     for k in range(1, 6)},
        "supplied_lists": tree_dp_count(VERTICES, EDGES, SUPPLIED, "c")}
    assert all(result["tree_dynamic_program_counts"]["ordinary"][str(k)]
               == result["ordinary"][str(k)]["count"] for k in range(1, 6))
    assert result["tree_dynamic_program_counts"]["supplied_lists"] == 0
    result["endpoint_controls"] = {}
    for end in ("a", "e"):
        lists = dict(SUPPLIED)
        lists[end + "1"] = lists[end + "2"] = A
        outcome = exact_solutions(VERTICES, EDGES, lists)
        assert outcome["count"] > 0
        result["endpoint_controls"][f"restore_{end}_leaf_pair_to_A"] = outcome
    shifted = {v: tuple(x + 19 for x in SUPPLIED[v]) for v in VERTICES}
    assert exact_solutions(VERTICES, EDGES, shifted)["count"] == 0
    reversed_vertices = tuple(reversed(VERTICES))
    assert exact_solutions(reversed_vertices, tuple(reversed(EDGES)), SUPPLIED)["count"] == 0
    result["controls"] = controls()
    result["controls"].append({"name": "supplied_translation_and_order_invariance", "passed": True})
    result["local_infeasibility_certificate"] = {
        "degree_three_centers_with_all_A_neighbors": {
            str(x): [y for y in A if abs(x - y) >= 2] for x in A},
        "forced_b_d_orientations": [(1, 5), (5, 1)],
        "forced_c": 3,
        "endpoint_next_to_center_one": {
            str(x): [y for y in B if abs(x - y) >= 2 and y != 1]
            for x in (4, 5)}}
    six_lists = {v: tuple(range(1, 7)) for v in VERTICES}
    result["six_list_greedy_example"] = greedy_tree_lists(VERTICES, EDGES, six_lists, "c")
    witness = result["ordinary"]["5"]["first"]
    lengths = {"a1": 3, "a2": 7, "b1": 1, "d1": 8, "e1": 0, "e2": 12}
    extension = ordinary_extension(witness, lengths)
    result["pendant_path_example"] = {"lengths": lengths, "labeling": extension}
    for trial in range(100):
        lengths = {leaf: rng_length for leaf, rng_length in
                   zip(("a1", "a2", "b1", "d1", "e1", "e2"),
                       (Random(1200 + trial * 17 + j).randrange(41) for j in range(6)))}
        ordinary_extension(witness, lengths)
        vertices, edges = extended_instance(lengths)
        rng = Random(1300 + trial)
        lists = {v: tuple(sorted(rng.sample(range(1, 41), 6))) for v in vertices}
        greedy_tree_lists(vertices, edges, lists, "c")
    result["controls"].append({"name": "pendant_paths_and_six_list_greedy", "cases": 100,
                                "passed": True})
    result["conclusions"] = {"ordinary_palette_minimum": 5,
                              "supplied_lists_feasible": False,
                              "arbitrary_list_number": 6}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Write deterministic JSON to this file.")
    args = parser.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "x", encoding="utf-8") as output:
            output.write(payload)
    else:
        print(payload, end="")

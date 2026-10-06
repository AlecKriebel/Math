#!/usr/bin/env python3
"""Finite checks of the exact colored-tree -> destination-table translation.

Uses only stdlib; does not read any external sources or mutate queue state.
"""
from itertools import combinations, product
import json
from pathlib import Path


def build(edges):
    h = len(edges)
    vertices = sorted(set().union(*map(set, edges)))
    assert len(vertices) == h
    assert all(len(e) == 3 for e in edges)
    assert all(sum(v in e for e in edges) == 3 for v in vertices)
    pairs = [(i, j) for i, j in combinations(range(h), 2) if set(edges[i]) & set(edges[j])]
    root = "r"
    layer = {root: 0}
    arcs = []
    incoming = {}
    for i in range(h):
        for tag in ("b", "g"):
            node = f"{tag}{i}"
            layer[node] = 1
            arcs += [(root, node), (node, f"u{i}")]
            incoming[node] = [root]
        layer[f"u{i}"] = 2
        incoming[f"u{i}"] = [f"b{i}", f"g{i}"]
    kind = {}
    for v in vertices:
        node = f"v{v}"
        layer[node] = 3
        kind[node] = "b"
        incoming[node] = [f"u{i}" for i, e in enumerate(edges) if v in e]
        arcs += [(u, node) for u in incoming[node]]
    for i, j in pairs:
        node = f"w{i}_{j}"
        layer[node] = 3
        kind[node] = "g"
        incoming[node] = [f"u{i}", f"u{j}"]
        arcs += [(u, node) for u in incoming[node]]
    assert len(arcs) == len(set(arcs))
    assert all(layer[v] == layer[u] + 1 for u, v in arcs)
    assert all(1 <= len(ps) <= 3 for ps in incoming.values())
    reached = {root}
    for _ in range(3):
        reached |= {v for u, v in arcs if u in reached}
    assert reached == set(layer)
    table = {dest: {arc: 0 for arc in arcs} for dest in incoming}
    for dest, correct in kind.items():
        incorrect = "g" if correct == "b" else "b"
        for i in range(h):
            table[dest][(root, f"{incorrect}{i}")] = 1
    assert set(x for row in table.values() for x in row.values()) <= {0, 1}
    return dict(h=h, root=root, layer=layer, arcs=arcs, incoming=incoming,
                kind=kind, table=table, edges=edges, pairs=pairs)


def path(model, parents, dest):
    result = []
    node = dest
    while node != model["root"]:
        parent = parents[node]
        result.append((parent, node))
        node = parent
    return result[::-1]


def evaluate(model, labels, targets, corrupt=False):
    parents = {node: ps[0] for node, ps in model["incoming"].items() if model["layer"][node] == 1}
    parents.update({f"u{i}": f"{label}{i}" for i, label in enumerate(labels)})
    parents.update(targets)
    objective = 0
    positive = 0
    for dest in model["incoming"]:
        p = path(model, parents, dest)
        row = model["table"][dest]
        value = sum(row[a] for a in p)
        if corrupt and dest == next(iter(model["kind"])):
            value = 1 - value
        objective += value
        positive += value + len(p)
    violations = sum(labels[int(parent[1:])] != model["kind"][dest]
                     for dest, parent in targets.items())
    offset = 4 * model["h"] + 3 * len(model["kind"])
    assert objective == violations
    assert positive == objective + offset
    return objective


def exact_cover(edges, labels):
    selected = [set(e) for e, label in zip(edges, labels) if label == "b"]
    vertices = set().union(*map(set, edges))
    return all(sum(v in e for e in selected) == 1 for v in vertices)


def check_model(name, edges, exhaustive):
    model = build(edges)
    sinks = list(model["kind"])
    checks = 0
    minimum = len(sinks)
    zero_labels = 0
    for labels in product("bg", repeat=model["h"]):
        optimal_parents = {dest: min(model["incoming"][dest],
                                    key=lambda parent: labels[int(parent[1:])] != model["kind"][dest])
                           for dest in sinks}
        best = evaluate(model, labels, optimal_parents)
        assert (best == 0) == exact_cover(edges, labels)
        minimum = min(minimum, best)
        zero_labels += best == 0
        if exhaustive:
            choices = product(*(model["incoming"][dest] for dest in sinks))
            for choice in choices:
                evaluate(model, labels, dict(zip(sinks, choice)))
                checks += 1
        else:
            # Every local parent possibility is checked under every root assignment.
            # The universal all-tree equivalence is established by the written proof.
            for dest in sinks:
                for parent in model["incoming"][dest]:
                    changed = optimal_parents | {dest: parent}
                    evaluate(model, labels, changed)
                    checks += 1
    caught = False
    labels = tuple("b" for _ in range(model["h"]))
    parents = {dest: model["incoming"][dest][0] for dest in sinks}
    try:
        evaluate(model, labels, parents, corrupt=True)
    except AssertionError:
        caught = True
    assert caught, "reversing one destination test was not detected"
    return dict(instance=name, hyperedges=edges, vertices=len(model["layer"]), arcs=len(model["arcs"]),
                root_assignments=2 ** model["h"], explicit_tree_or_local_parent_checks=checks,
                full_tree_enumeration=exhaustive, optimum_binary=minimum,
                exact_cover_root_assignments=zero_labels, positive_offset=4 * model["h"] + 3 * len(sinks),
                graph_restrictions_pass=True, corrupted_cost_negative_control_detected=caught)


def main():
    cases = [
        check_model("complete_3_uniform_on_4_vertices_no_cover", list(combinations(range(4), 3)), True),
        check_model("six_edge_3_regular_yes_cover",
                    [(0, 1, 2), (0, 1, 3), (0, 2, 4), (1, 3, 5), (2, 4, 5), (3, 4, 5)], False),
        check_model("six_edge_3_regular_no_cover",
                    [(0, 1, 2), (0, 1, 3), (0, 4, 5), (1, 4, 5), (2, 3, 4), (2, 3, 5)], False),
    ]
    out = dict(status="pass", checks=cases,
               limitation="Finite checks support the translation; PRIOR_COROLLARY.md proves it for the whole prior reduction family.")
    destination = Path(__file__).with_name("VALIDATION.json")
    destination.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

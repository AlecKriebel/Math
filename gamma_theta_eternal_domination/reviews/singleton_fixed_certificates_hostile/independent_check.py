#!/usr/bin/env python3
"""Clean-room hostile checker for the singleton fixed-certificate note.

This file deliberately imports no campaign or candidate module.  Graphs,
states, transitions, complements, components, and exact parameters are
reconstructed with ordinary Python sets.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import deque
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "math/working/singleton_fixed_certificates"

CASES = {
    "FCpbO": {
        "reference": frozenset({0, 5, 6}),
        "order": 7,
        "size": 8,
        "parameters": (3, 3, 3, 3, 3),
        "family_size": 12,
        "obligations": 48,
        "lists": {
            1: frozenset({6}),
            2: frozenset({5}),
            3: frozenset({0}),
            4: frozenset({6}),
        },
        "fixed_singletons": 8,
        "exact_two": 0,
        "cross_edges": 0,
        "colorings": 1,
    },
    "LFzJbZYhdrDZdM": {
        "reference": frozenset({0, 1, 2}),
        "order": 13,
        "size": 43,
        "parameters": (3, 3, 3, 3, 3),
        "family_size": 142,
        "obligations": 1420,
        "lists": {
            3: frozenset({0, 1}),
            4: frozenset({1, 2}),
            5: frozenset({0, 1}),
            6: frozenset({1, 2}),
            7: frozenset({1, 2}),
            8: frozenset({0, 1}),
            9: frozenset({0, 2}),
            10: frozenset({0, 2}),
            11: frozenset({2}),
            12: frozenset({0}),
        },
        "fixed_singletons": 4,
        "exact_two": 8,
        "cross_edges": 10,
        "colorings": 2,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> tuple[frozenset[int], frozenset[frozenset[int]]]:
    raw = [ord(char) - 63 for char in record.strip()]
    assert raw and 0 <= raw[0] <= 62
    n = raw[0]
    stream = [
        (word >> bit) & 1
        for word in raw[1:]
        for bit in range(5, -1, -1)
    ]
    edges: set[frozenset[int]] = set()
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            assert cursor < len(stream)
            if stream[cursor]:
                edges.add(frozenset({low, high}))
            cursor += 1
    return frozenset(range(n)), frozenset(edges)


def edge(edges: frozenset[frozenset[int]], u: int, v: int) -> bool:
    return u != v and frozenset({u, v}) in edges


def complement_edges(
    vertices: frozenset[int], edges: frozenset[frozenset[int]]
) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset({u, v})
        for u, v in itertools.combinations(sorted(vertices), 2)
        if not edge(edges, u, v)
    )


def dominates(
    state: frozenset[int],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> bool:
    return all(
        vertex in state
        or any(edge(edges, guard, vertex) for guard in state)
        for vertex in vertices
    )


def independent(state: frozenset[int], edges: frozenset[frozenset[int]]) -> bool:
    return not any(edge(edges, u, v) for u, v in itertools.combinations(state, 2))


def subsets(vertices: frozenset[int], size: int):
    for group in itertools.combinations(sorted(vertices), size):
        yield frozenset(group)


def legal_successors(
    state: frozenset[int],
    attacked: int,
    edges: frozenset[frozenset[int]],
) -> list[tuple[int, frozenset[int]]]:
    assert attacked not in state
    return [
        (guard, frozenset((state - {guard}) | {attacked}))
        for guard in sorted(state)
        if edge(edges, guard, attacked)
    ]


def is_eternal_family(
    family: frozenset[frozenset[int]],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> bool:
    if not family:
        return False
    for state in family:
        if not dominates(state, vertices, edges):
            return False
        for attacked in vertices - state:
            if not any(
                successor in family
                for _, successor in legal_successors(state, attacked, edges)
            ):
                return False
    return True


def greatest_family(
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
    size: int,
) -> frozenset[frozenset[int]]:
    family = frozenset(
        state
        for state in subsets(vertices, size)
        if dominates(state, vertices, edges)
    )
    while True:
        retained = frozenset(
            state
            for state in family
            if all(
                any(
                    successor in family
                    for _, successor in legal_successors(state, attacked, edges)
                )
                for attacked in vertices - state
            )
        )
        if retained == family:
            assert not family or is_eternal_family(family, vertices, edges)
            return family
        family = retained


def minimum_size(predicate, vertices: frozenset[int]) -> int:
    for size in range(1, len(vertices) + 1):
        if any(predicate(state) for state in subsets(vertices, size)):
            return size
    raise AssertionError("no witness")


def parameters(
    vertices: frozenset[int], edges: frozenset[frozenset[int]]
) -> tuple[int, int, int, int, int]:
    gamma = minimum_size(lambda state: dominates(state, vertices, edges), vertices)
    independent_sets = [
        state
        for size in range(1, len(vertices) + 1)
        for state in subsets(vertices, size)
        if independent(state, edges)
    ]
    alpha = max(map(len, independent_sets))
    independent_domination = min(
        len(state)
        for state in independent_sets
        if dominates(state, vertices, edges)
    )
    eternal = next(
        size
        for size in range(1, len(vertices) + 1)
        if greatest_family(vertices, edges, size)
    )

    cliques = [
        state
        for size in range(1, len(vertices) + 1)
        for state in subsets(vertices, size)
        if all(edge(edges, u, v) for u, v in itertools.combinations(state, 2))
    ]

    @lru_cache(maxsize=None)
    def clique_partition_number(remaining: frozenset[int]) -> int:
        if not remaining:
            return 0
        first = min(remaining)
        choices = [
            clique
            for clique in cliques
            if first in clique and clique <= remaining
        ]
        return 1 + min(
            clique_partition_number(remaining - clique) for clique in choices
        )

    theta = clique_partition_number(vertices)
    return gamma, independent_domination, alpha, eternal, theta


def bipartition(
    vertices: frozenset[int], h_edges: frozenset[frozenset[int]]
) -> tuple[dict[int, int], dict[int, int], list[frozenset[int]]]:
    side: dict[int, int] = {}
    component: dict[int, int] = {}
    components: list[frozenset[int]] = []
    for root in sorted(vertices):
        if root in side:
            continue
        index = len(components)
        side[root] = 0
        component[root] = index
        queue = deque([root])
        found = set()
        while queue:
            current = queue.popleft()
            found.add(current)
            for neighbor in vertices - {current}:
                if not edge(h_edges, current, neighbor):
                    continue
                if neighbor not in side:
                    side[neighbor] = side[current] ^ 1
                    component[neighbor] = index
                    queue.append(neighbor)
                else:
                    assert side[neighbor] != side[current], "complement is not bipartite"
        components.append(frozenset(found))
    return side, component, components


def response_lists(
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
    family: frozenset[frozenset[int]],
    reference: frozenset[int],
) -> dict[int, frozenset[int]]:
    lists = {}
    for attacked in sorted(vertices - reference):
        responders = frozenset(
            anchor
            for anchor in reference
            if edge(edges, anchor, attacked)
            and frozenset((reference - {anchor}) | {attacked}) in family
        )
        assert responders
        lists[attacked] = responders
    return lists


def count_response_colorings(
    vertices: frozenset[int],
    h_edges: frozenset[frozenset[int]],
    reference: frozenset[int],
    lists: dict[int, frozenset[int]],
) -> int:
    assigned = {anchor: anchor for anchor in reference}
    outside = sorted(vertices - reference, key=lambda x: (len(lists[x]), x))

    def recurse(position: int) -> int:
        if position == len(outside):
            return 1
        vertex = outside[position]
        total = 0
        for color in lists[vertex]:
            if any(
                assigned[other] == color and edge(h_edges, vertex, other)
                for other in assigned
            ):
                continue
            assigned[vertex] = color
            total += recurse(position + 1)
            del assigned[vertex]
        return total

    return recurse(0)


def audit_projection(
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
    family: frozenset[frozenset[int]],
    reference: frozenset[int],
    lists: dict[int, frozenset[int]],
    frozen: int,
) -> dict[str, object]:
    remaining_anchors = reference - {frozen}
    omission = frozenset(
        vertex for vertex in vertices - reference if frozen not in lists[vertex]
    )
    q_vertices = remaining_anchors | omission
    q_edges = frozenset(pair for pair in edges if pair <= q_vertices)
    h_edges = complement_edges(q_vertices, q_edges)
    projected_family = frozenset(
        state - {frozen}
        for state in family
        if frozen in state and state - {frozen} <= q_vertices
    )
    assert remaining_anchors in projected_family

    obligations = 0
    for pair in projected_family:
        assert len(pair) == 2
        assert dominates(pair, q_vertices, q_edges)
        original = pair | {frozen}
        assert original in family
        for attacked in q_vertices - pair:
            obligations += 1
            original_legal = [
                (guard, successor)
                for guard, successor in legal_successors(original, attacked, edges)
                if successor in family
            ]
            assert original_legal
            assert all(
                guard != frozen for guard, _ in original_legal
            ), "frozen guard has a retained successor"
            projected_legal = [
                (guard, successor)
                for guard, successor in legal_successors(pair, attacked, q_edges)
                if successor in projected_family
            ]
            assert projected_legal

    side, component, components = bipartition(q_vertices, h_edges)
    anchors = sorted(remaining_anchors)
    assert edge(h_edges, anchors[0], anchors[1])
    assert component[anchors[0]] == component[anchors[1]]
    assert side[anchors[0]] != side[anchors[1]]

    for pair in projected_family:
        x, y = sorted(pair)
        if component[x] == component[y]:
            assert side[x] != side[y], "retained same-side projected pair"

    return {
        "vertices": q_vertices,
        "edges": q_edges,
        "h_edges": h_edges,
        "family": projected_family,
        "side": side,
        "component": component,
        "components": components,
        "anchor_component": component[anchors[0]],
        "obligations": obligations,
    }


def audit_case(record: str, expected: dict[str, object]) -> dict[str, object]:
    vertices, edges = decode_graph6(record)
    h_edges = complement_edges(vertices, edges)
    assert len(vertices) == expected["order"]
    assert len(edges) == expected["size"]
    assert parameters(vertices, edges) == expected["parameters"]

    family = greatest_family(vertices, edges, 3)
    assert len(family) == expected["family_size"]
    reference = expected["reference"]
    assert reference in family and independent(reference, edges)
    obligations = sum(len(vertices - state) for state in family)
    assert obligations == expected["obligations"]
    assert is_eternal_family(family, vertices, edges)
    lists = response_lists(vertices, edges, family, reference)
    assert lists == expected["lists"]
    assert all(0 < len(response) < 3 for response in lists.values())

    projections = {
        frozen: audit_projection(vertices, edges, family, reference, lists, frozen)
        for frozen in reference
    }

    fixed_singletons = []
    free_singletons = []
    exact_two = []
    for vertex, response in lists.items():
        if len(response) == 1:
            demanded = next(iter(response))
            for frozen in reference - {demanded}:
                projection = projections[frozen]
                assert vertex in projection["component"]
                anchor_component = projection["anchor_component"]
                if projection["component"][vertex] == anchor_component:
                    assert projection["side"][vertex] == projection["side"][demanded]
                    fixed_singletons.append((vertex, frozen, demanded))
                else:
                    free_singletons.append((vertex, frozen, demanded))
        elif len(response) == 2:
            omitted = next(iter(reference - response))
            projection = projections[omitted]
            assert projection["component"][vertex] != projection["anchor_component"]
            exact_two.append((vertex, omitted, projection["component"][vertex]))
        else:
            raise AssertionError("control has a full response list")

    cross_edges = []
    for x, y in itertools.combinations(sorted(vertices - reference), 2):
        if not edge(h_edges, x, y):
            continue
        if len(lists[x]) != 2 or len(lists[y]) != 2:
            continue
        omitted_x = next(iter(reference - lists[x]))
        omitted_y = next(iter(reference - lists[y]))
        if omitted_x == omitted_y:
            continue
        projection_x = projections[omitted_x]
        projection_y = projections[omitted_y]
        variable_x = (omitted_x, projection_x["component"][x])
        variable_y = (omitted_y, projection_y["component"][y])
        assert projection_x["component"][x] != projection_x["anchor_component"]
        assert projection_y["component"][y] != projection_y["anchor_component"]
        assert variable_x != variable_y
        assert len(lists[x] & lists[y]) == 1
        cross_edges.append((x, y, next(iter(lists[x] & lists[y]))))

    assert len(fixed_singletons) == expected["fixed_singletons"]
    assert len(exact_two) == expected["exact_two"]
    assert len(cross_edges) == expected["cross_edges"]
    colorings = count_response_colorings(vertices, h_edges, reference, lists)
    assert colorings == expected["colorings"]

    return {
        "order": len(vertices),
        "size": len(edges),
        "parameters": list(expected["parameters"]),
        "family_size": len(family),
        "obligations": obligations,
        "projected_family_sizes": {
            str(u): len(projections[u]["family"]) for u in sorted(reference)
        },
        "projected_obligations": {
            str(u): projections[u]["obligations"] for u in sorted(reference)
        },
        "fixed_singleton_incidences": len(fixed_singletons),
        "free_singleton_incidences": len(free_singletons),
        "exact_two_free_vertices": len(exact_two),
        "cross_type_free_free_edges": len(cross_edges),
        "response_coloring_count": colorings,
    }


def graph_from_edge_mask(
    n: int, mask: int
) -> tuple[frozenset[int], frozenset[frozenset[int]]]:
    vertices = frozenset(range(n))
    possible = [
        frozenset({u, v}) for u, v in itertools.combinations(range(n), 2)
    ]
    edges = frozenset(
        possible[index] for index in range(len(possible)) if (mask >> index) & 1
    )
    return vertices, edges


def same_side_bad_pairs(
    family: frozenset[frozenset[int]],
    side: dict[int, int],
    component: dict[int, int],
) -> list[frozenset[int]]:
    result = []
    for pair in family:
        x, y = sorted(pair)
        if component[x] == component[y] and side[x] == side[y]:
            result.append(pair)
    return result


def stress_pair_lemma() -> dict[str, int]:
    counts = {
        "labeled_graphs_through_6": 0,
        "bipartite_complements_through_6": 0,
        "greatest_pair_families": 0,
        "retained_pairs": 0,
        "direct_arbitrary_families_through_4": 0,
        "direct_eternal_families_through_4": 0,
    }
    for n in range(2, 7):
        edge_count = n * (n - 1) // 2
        for mask in range(1 << edge_count):
            counts["labeled_graphs_through_6"] += 1
            vertices, edges = graph_from_edge_mask(n, mask)
            h_edges = complement_edges(vertices, edges)
            try:
                side, component, _ = bipartition(vertices, h_edges)
            except AssertionError:
                continue
            counts["bipartite_complements_through_6"] += 1
            greatest = greatest_family(vertices, edges, 2)
            if greatest:
                counts["greatest_pair_families"] += 1
                counts["retained_pairs"] += len(greatest)
                assert not same_side_bad_pairs(greatest, side, component)

            if n <= 4:
                dominating_pairs = [
                    pair
                    for pair in subsets(vertices, 2)
                    if dominates(pair, vertices, edges)
                ]
                for family_mask in range(1, 1 << len(dominating_pairs)):
                    family = frozenset(
                        dominating_pairs[index]
                        for index in range(len(dominating_pairs))
                        if (family_mask >> index) & 1
                    )
                    counts["direct_arbitrary_families_through_4"] += 1
                    if not is_eternal_family(family, vertices, edges):
                        continue
                    counts["direct_eternal_families_through_4"] += 1
                    assert not same_side_bad_pairs(family, side, component)
    return counts


def verify_candidate_manifest() -> dict[str, object]:
    manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    checked = {}
    for relative, expected_hash in manifest["files"].items():
        actual = sha256(ROOT / relative)
        assert actual == expected_hash
        checked[relative] = actual
    for relative, expected_hash in manifest["accepted_dependencies"].items():
        actual = sha256(ROOT / relative)
        assert actual == expected_hash
        checked[relative] = actual
    assert manifest["reproduction"]["stdout_sha256"] == (
        "a06c8a764635a8fed0ec6f5b55a3fc9a95f7f420746f666eee38764647b5a4e5"
    )
    return {
        "manifest_sha256": sha256(CANDIDATE / "MANIFEST.json"),
        "checked_file_count": len(checked),
        "candidate_stdout_sha256": manifest["reproduction"]["stdout_sha256"],
    }


def main() -> None:
    results = {
        "schema": "singleton-fixed-certificates-hostile-check-v1",
        "model": (
            "attacks only at unoccupied vertices; exactly one guard moves "
            "along one G-edge; successor must be in the retained family"
        ),
        "candidate_manifest": verify_candidate_manifest(),
        "controls": {
            record: audit_case(record, expected)
            for record, expected in CASES.items()
        },
        "pair_lemma_stress": stress_pair_lemma(),
        "logical_scope": {
            "fixed_singleton_demands_checked_aligned": True,
            "exact_two_omitted_projection_components_checked_free": True,
            "cross_type_clause_variables_checked_distinct_and_free": True,
            "initial_false_constant_branch_empty": True,
            "unit_propagation_branch_closed": False,
            "unit_free_bicycle_branch_closed": False,
            "k3_resolved": False,
            "universal_resolved": False,
        },
        "verdict": "PASS",
    }
    sys.stdout.write(json.dumps(results, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()

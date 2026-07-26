#!/usr/bin/env python3
"""Independent bounded probe for the frozen-color projection theorem.

This review probe deliberately uses verifier B's ordinary ``frozenset``
graph representation and literal eternal-family checker.  It does not import
the working-note probe or any response-list helper from the theorem author.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path

from verifier_b.eternal import (
    eternal_domination_number,
    find_eternal_family,
    verify_eternal_family,
)
from verifier_b.graph import Graph
from verifier_b.invariants import (
    clique_cover_number,
    domination_number,
    independence_number,
    is_dominating,
    is_independent,
    minimum_clique_partition,
)


CAMPAIGN = Path(__file__).resolve().parents[2]
GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
CATALOG = CAMPAIGN / "instances" / "mmv2022_table9.csv"
NOTE = CAMPAIGN / "math" / "working" / "k3_cross_state_attack.md"
OUTPUT = Path(__file__).with_name("probe_result.json")

State = frozenset[int]
Family = frozenset[State]


def cycle(order: int) -> Graph:
    return Graph.from_edges(
        order, ((vertex, (vertex + 1) % order) for vertex in range(order))
    )


def induced_graph(
    graph: Graph, vertices: set[int]
) -> tuple[Graph, tuple[int, ...]]:
    original = tuple(sorted(vertices))
    local = {vertex: index for index, vertex in enumerate(original)}
    edges = (
        (local[first], local[second])
        for first, second in itertools.combinations(original, 2)
        if second in graph.adjacency[first]
    )
    return Graph.from_edges(len(original), edges), original


def response_lists(
    graph: Graph,
    reference: State,
    family: Family,
    *,
    static: bool,
) -> dict[int, State]:
    lists: dict[int, State] = {}
    for attacked in graph.vertices:
        if attacked in reference:
            continue
        viable: set[int] = set()
        for guard in reference:
            if attacked not in graph.adjacency[guard]:
                continue
            successor = frozenset((reference - {guard}) | {attacked})
            if static:
                accepted = is_dominating(graph, successor)
            else:
                accepted = successor in family
            if accepted:
                viable.add(guard)
        lists[attacked] = frozenset(viable)
    return lists


def projected_family(
    family: Family,
    frozen: int,
    projected_vertices: set[int],
    local_vertices: tuple[int, ...],
    guard_count: int,
) -> Family:
    local = {vertex: index for index, vertex in enumerate(local_vertices)}
    states: set[State] = set()
    for outside_tuple in itertools.combinations(
        sorted(projected_vertices), guard_count - 1
    ):
        outside = frozenset(outside_tuple)
        if frozenset({frozen}) | outside in family:
            states.add(frozenset(local[vertex] for vertex in outside))
    return frozenset(states)


def check_one_projection(
    graph: Graph,
    family: Family,
    reference: State,
    frozen: int,
    *,
    static: bool,
) -> dict[str, int]:
    guard_count = len(reference)
    lists = response_lists(graph, reference, family, static=static)
    omitted = {
        vertex
        for vertex in graph.vertices
        if vertex not in reference and frozen not in lists[vertex]
    }
    projected_vertices = (set(reference) - {frozen}) | omitted
    projected, original = induced_graph(graph, projected_vertices)
    projection = projected_family(
        family, frozen, projected_vertices, original, guard_count
    )

    assert projection
    assert verify_eternal_family(projected, guard_count - 1, projection)
    assert independence_number(projected) == guard_count - 1

    if domination_number(graph) == guard_count:
        assert domination_number(projected) == guard_count - 1

    static_assignments = 0
    if guard_count == 3:
        # This is checked directly, rather than inferred from the alpha=2
        # theorem used in the note.
        assert clique_cover_number(projected) == 2

    if static and clique_cover_number(projected) == guard_count - 1:
        parts = minimum_clique_partition(projected)
        assert len(parts) == guard_count - 1
        for part in parts:
            anchors = [
                local_vertex
                for local_vertex in part
                if original[local_vertex] in reference - {frozen}
            ]
            assert len(anchors) == 1
            anchor = original[anchors[0]]
            for local_vertex in part:
                vertex = original[local_vertex]
                if vertex in omitted:
                    assert anchor in lists[vertex]
                    static_assignments += 1

    obligations = sum(
        projected.order - len(state) for state in projection
    )
    return {
        "projected_states": len(projection),
        "attack_obligations": obligations,
        "static_color_assignments": static_assignments,
    }


def check_family(
    graph: Graph,
    family: Family,
) -> Counter[str]:
    guard_count = len(next(iter(family)))
    counts: Counter[str] = Counter()
    for reference_tuple in itertools.combinations(
        graph.vertices, guard_count
    ):
        reference = frozenset(reference_tuple)
        if not is_independent(graph, reference):
            continue
        assert reference in family
        counts["independent_reference_states"] += 1
        for static in (False, True):
            for frozen in reference:
                result = check_one_projection(
                    graph,
                    family,
                    reference,
                    frozen,
                    static=static,
                )
                counts["projections"] += 1
                counts.update(result)
    return counts


def connected_small_graph_scan() -> dict[str, object]:
    totals: Counter[str] = Counter()
    per_order: dict[str, dict[str, int]] = {}
    for order in range(2, 8):
        completed = subprocess.run(
            [str(GENG), "-cq", str(order)],
            check=True,
            capture_output=True,
            text=True,
        )
        order_counts: Counter[str] = Counter()
        for record in completed.stdout.splitlines():
            graph = Graph.from_graph6(record)
            order_counts["connected_graphs"] += 1
            guard_count = independence_number(graph)
            if guard_count < 2:
                continue
            family = find_eternal_family(graph, guard_count)
            if not family:
                continue
            order_counts["eligible_alpha_equals_eternal_graphs"] += 1
            order_counts.update(check_family(graph, family))
        per_order[str(order)] = dict(order_counts)
        totals.update(order_counts)
    return {"per_order": per_order, "totals": dict(totals)}


def catalog_scan() -> dict[str, int]:
    totals: Counter[str] = Counter()
    with CATALOG.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            totals["catalog_graphs"] += 1
            graph = Graph.from_graph6(row["graph6"])
            guard_count = independence_number(graph)
            family = find_eternal_family(graph, guard_count)
            if not family:
                continue
            totals["eligible_alpha_equals_eternal_graphs"] += 1
            totals.update(check_family(graph, family))
    return dict(totals)


def every_subfamily_scan(name: str, graph: Graph) -> dict[str, object]:
    guard_count = independence_number(graph)
    greatest = tuple(
        sorted(
            find_eternal_family(graph, guard_count) or (),
            key=lambda state: tuple(sorted(state)),
        )
    )
    family_histogram: Counter[int] = Counter()
    totals: Counter[str] = Counter()
    for mask in range(1, 1 << len(greatest)):
        family = frozenset(
            greatest[index]
            for index in range(len(greatest))
            if mask & (1 << index)
        )
        if not verify_eternal_family(graph, guard_count, family):
            continue
        totals["eternal_subfamilies"] += 1
        family_histogram[len(family)] += 1
        totals.update(check_family(graph, family))
    return {
        "name": name,
        "graph6": graph.to_graph6(),
        "greatest_family_states": len(greatest),
        "eternal_family_size_histogram": {
            str(size): count for size, count in sorted(family_histogram.items())
        },
        **dict(totals),
    }


def is_bipartite(graph: Graph) -> bool:
    colors: dict[int, int] = {}
    for start in graph.vertices:
        if start in colors:
            continue
        colors[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in graph.adjacency[vertex]:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    stack.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def control_record(
    name: str, graph: Graph, reference: State
) -> dict[str, object]:
    guard_count = len(reference)
    family = find_eternal_family(graph, guard_count)
    static_lists = response_lists(
        graph, reference, family or frozenset(), static=True
    )
    static_projection_bipartite: dict[str, bool] = {}
    for frozen in sorted(reference):
        omitted = {
            vertex
            for vertex in graph.vertices
            if vertex not in reference
            and frozen not in static_lists[vertex]
        }
        projected, _ = induced_graph(
            graph, (set(reference) - {frozen}) | omitted
        )
        static_projection_bipartite[str(frozen)] = is_bipartite(
            projected.complement()
        )
    return {
        "name": name,
        "graph6": graph.to_graph6(),
        "gamma": domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity": eternal_domination_number(graph),
        "theta": clique_cover_number(graph),
        "eternal_family_at_reference_size": 0 if family is None else len(family),
        "reference": sorted(reference),
        "static_lists": {
            str(vertex): sorted(response)
            for vertex, response in sorted(static_lists.items())
        },
        "static_projection_bipartite": static_projection_bipartite,
    }


def non_greatest_projection_witness() -> dict[str, object]:
    """Recompute the FCZbg witness with no theorem-note helper."""

    graph = Graph.from_graph6("FCZbg")
    reference = frozenset({0, 4, 6})
    frozen = 4
    family = find_eternal_family(graph, 3)
    assert family is not None and reference in family
    lists = response_lists(graph, reference, family, static=False)
    omitted = {
        vertex
        for vertex in graph.vertices
        if vertex not in reference and frozen not in lists[vertex]
    }
    projected_vertices = (set(reference) - {frozen}) | omitted
    projected, original = induced_graph(graph, projected_vertices)
    projection = projected_family(
        family, frozen, projected_vertices, original, 3
    )
    greatest_projected = find_eternal_family(projected, 2)
    assert greatest_projected is not None
    assert verify_eternal_family(projected, 2, projection)
    assert verify_eternal_family(projected, 2, greatest_projected)
    assert projection < greatest_projected

    def original_states(states: Family) -> list[list[int]]:
        return sorted(
            sorted(original[vertex] for vertex in state)
            for state in states
        )

    return {
        "graph6": graph.to_graph6(),
        "reference": sorted(reference),
        "frozen": frozen,
        "family_response_lists": {
            str(vertex): sorted(response)
            for vertex, response in sorted(lists.items())
        },
        "omission_set": sorted(omitted),
        "projected_vertices": list(original),
        "projected_graph6": projected.to_graph6(),
        "projected_family_states": original_states(projection),
        "greatest_projected_family_states": original_states(greatest_projected),
        "missing_from_projection": original_states(
            greatest_projected - projection
        ),
        "projected_family_size": len(projection),
        "greatest_projected_family_size": len(greatest_projected),
        "projection_is_proper_subfamily": True,
    }


def main() -> None:
    note_bytes = NOTE.read_bytes()
    result = {
        "format": "gamma-theta-frozen-color-hostile-probe-v1",
        "note": {
            "path": str(NOTE.relative_to(CAMPAIGN)),
            "sha256": hashlib.sha256(note_bytes).hexdigest(),
        },
        "implementation": {
            "graph_representation": "verifier_b ordinary frozensets",
            "family_validation": "literal verify_eternal_family",
            "theorem_note_helpers_imported": False,
            "orders": [2, 7],
            "order_14_used": False,
        },
        "connected_small_graph_scan": connected_small_graph_scan(),
        "mmv2022_catalog_scan": catalog_scan(),
        "all_eternal_subfamilies": [
            every_subfamily_scan("C4", cycle(4)),
            every_subfamily_scan("FCpbO", Graph.from_graph6("FCpbO")),
        ],
        "non_greatest_projection_boundary": non_greatest_projection_witness(),
        "controls": [
            control_record("C4", cycle(4), frozenset({0, 2})),
            control_record("C7", cycle(7), frozenset({0, 2, 4})),
            control_record(
                "J@l|bfNuVK_",
                Graph.from_graph6("J@l|bfNuVK_"),
                frozenset({0, 1, 2}),
            ),
        ],
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(OUTPUT)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

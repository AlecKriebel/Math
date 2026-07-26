#!/usr/bin/env python3
"""Independent small-graph audit for the FDzro mixed-P4 witness."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from verifier_a.core import (
    BitGraph,
    alpha as alpha_a,
    domination_number as domination_number_a,
    eternal_domination_number as eternal_number_a,
    eternal_fixed_point as eternal_fixed_point_a,
    theta as theta_a,
)
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
    minimum_clique_partition,
    minimum_dominating_set,
)


CAMPAIGN = Path(__file__).resolve().parents[2]
NOTE = CAMPAIGN / "math" / "working" / "k3_mixed_p4_attack.md"
EVIDENCE = CAMPAIGN / "results" / "k3_mixed_p4_probe.json"
OUTPUT = Path(__file__).with_name("probe_result.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def family_lists(
    graph: Graph,
    reference: frozenset[int],
    family: frozenset[frozenset[int]],
) -> dict[str, list[int]]:
    lists: dict[str, list[int]] = {}
    for attacked in graph.vertices:
        if attacked in reference:
            continue
        lists[str(attacked)] = sorted(
            guard
            for guard in reference
            if attacked in graph.adjacency[guard]
            and frozenset((reference - {guard}) | {attacked}) in family
        )
    return lists


def canonical_states(
    family: frozenset[frozenset[int]],
) -> list[list[int]]:
    return sorted(sorted(state) for state in family)


def main() -> None:
    recorded = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    near = recorded["exact_near_realization"]
    graph = Graph.from_graph6(near["graph6"])
    graph_a = BitGraph.from_graph6(near["graph6"])
    reference = frozenset({0, 1, 2})
    explicit = frozenset(
        frozenset(state) for state in near["explicit_family"]
    )

    expected_edges = {
        (0, 3),
        (0, 4),
        (0, 5),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 5),
        (3, 6),
        (4, 6),
    }
    assert set(graph.edges()) == expected_edges

    core = (3, 4, 5, 6)
    complement_core_edges = {
        (left, right)
        for index, left in enumerate(core)
        for right in core[index + 1 :]
        if right not in graph.adjacency[left]
    }
    assert complement_core_edges == {(3, 4), (4, 5), (5, 6)}

    assert len(explicit) == 21
    assert verify_eternal_family(graph, 3, explicit)
    obligations = 0
    responses: list[dict[str, object]] = []
    for source in sorted(explicit, key=lambda state: tuple(sorted(state))):
        for attacked in graph.vertices:
            if attacked in source:
                continue
            obligations += 1
            legal = []
            for guard in sorted(source):
                if attacked not in graph.adjacency[guard]:
                    continue
                target = frozenset((source - {guard}) | {attacked})
                if target in explicit:
                    legal.append(
                        {
                            "guard": guard,
                            "target": sorted(target),
                        }
                    )
            assert legal
            responses.append(
                {
                    "source": sorted(source),
                    "attack": attacked,
                    "responses": legal,
                }
            )
    assert obligations == 84

    greatest = find_eternal_family(graph, 3)
    assert greatest is not None
    greatest_a = eternal_fixed_point_a(graph_a, 3).family
    greatest_a_states = frozenset(
        frozenset(
            vertex
            for vertex in graph.vertices
            if mask & (1 << vertex)
        )
        for mask in greatest_a
    )
    assert greatest_a_states == greatest
    assert explicit < greatest
    assert len(greatest) == 33

    explicit_lists = family_lists(graph, reference, explicit)
    greatest_lists = family_lists(graph, reference, greatest)
    assert explicit_lists == {
        "3": [0],
        "4": [0, 2],
        "5": [1, 2],
        "6": [1],
    }
    assert greatest_lists == {
        "3": [0, 2],
        "4": [0, 1, 2],
        "5": [0, 1, 2],
        "6": [1, 2],
    }

    parameters_b = {
        "gamma": domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity": eternal_domination_number(graph),
        "theta": clique_cover_number(graph),
    }
    parameters_a = {
        "gamma": domination_number_a(graph_a),
        "alpha": alpha_a(graph_a),
        "gamma_infinity": eternal_number_a(graph_a),
        "theta": theta_a(graph_a),
    }
    expected_parameters = {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert parameters_a == expected_parameters
    assert parameters_b == expected_parameters
    assert parameters_b == near["parameters"]

    required_tight_states = {
        frozenset({1, 3, 4}),
        frozenset({0, 5, 6}),
    }
    assert required_tight_states <= explicit

    result = {
        "format": "gamma-theta-k3-mixed-p4-hostile-probe-v1",
        "reviewed": {
            "note_path": str(NOTE.relative_to(CAMPAIGN)),
            "note_sha256": sha256(NOTE),
            "evidence_path": str(EVIDENCE.relative_to(CAMPAIGN)),
            "evidence_sha256": sha256(EVIDENCE),
        },
        "graph": {
            "graph6": graph.to_graph6(),
            "order": graph.order,
            "size": graph.size,
            "edges": [list(edge) for edge in graph.edges()],
            "complement_core_vertices": list(core),
            "complement_core_edges": [
                list(edge) for edge in sorted(complement_core_edges)
            ],
        },
        "parameters": {
            "verifier_a": parameters_a,
            "verifier_b": parameters_b,
            "dominating_witness": sorted(minimum_dominating_set(graph)),
            "clique_partition": [
                sorted(part) for part in minimum_clique_partition(graph)
            ],
        },
        "displayed_family": {
            "size": len(explicit),
            "literal_checker_accepts": True,
            "attack_obligations_checked": obligations,
            "states": canonical_states(explicit),
            "response_table_sha256": hashlib.sha256(
                json.dumps(
                    responses,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest(),
            "family_lists_at_012": explicit_lists,
            "hall_tight_forced_states_present": [
                sorted(state) for state in sorted(
                    required_tight_states,
                    key=lambda state: tuple(sorted(state)),
                )
            ],
        },
        "greatest_family_scope": {
            "size": len(greatest),
            "verifier_a_and_b_agree": True,
            "displayed_family_is_proper_subfamily": True,
            "states_missing_from_displayed_family": canonical_states(
                greatest - explicit
            ),
            "family_lists_at_012": greatest_lists,
        },
        "census_scope_read_from_evidence": {
            "claim_status": recorded["claim_status"],
            "warning": recorded["connected_unlabeled_census"]["warning"],
            "aggregate_graphs": recorded["connected_unlabeled_census"][
                "aggregate_graphs"
            ],
            "aggregate_pattern_realizations": recorded[
                "connected_unlabeled_census"
            ]["aggregate_pattern_realizations"],
            "pattern_list_scope": "greatest family",
            "rerun_by_hostile_reviewer": False,
        },
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

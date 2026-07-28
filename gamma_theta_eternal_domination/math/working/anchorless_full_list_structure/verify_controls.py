#!/usr/bin/env python3
"""Deterministic candidate replay for component-palette controls.

This checker reuses verifier A and is therefore not an independent hostile
review.  It recomputes the named graphs, greatest families, full roots,
physical links, spokes, retained palettes, and component-side uniformity.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
)


def mask(vertices: tuple[int, ...] | list[int]) -> int:
    return sum(1 << vertex for vertex in vertices)


def vertex_list(bits: int, order: int) -> list[int]:
    return [vertex for vertex in range(order) if bits >> vertex & 1]


def link_components(
    complement: BitGraph, physical: int
) -> list[tuple[list[int], list[int]]]:
    remaining = physical
    components = []
    while remaining:
        seed = remaining & -remaining
        frontier = seed
        seen = 0
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            vertex = bit.bit_length() - 1
            seen |= bit
            frontier |= complement.adj[vertex] & physical & ~seen
        remaining &= ~seen

        root = (seen & -seen).bit_length() - 1
        side = {root: 0}
        queue = [root]
        while queue:
            vertex = queue.pop(0)
            neighbors = complement.adj[vertex] & seen
            for neighbor in vertex_list(neighbors, complement.n):
                expected = 1 - side[vertex]
                if neighbor in side:
                    if side[neighbor] != expected:
                        raise AssertionError("physical link is not bipartite")
                else:
                    side[neighbor] = expected
                    queue.append(neighbor)
        components.append(
            (
                sorted(vertex for vertex, value in side.items() if value == 0),
                sorted(vertex for vertex, value in side.items() if value == 1),
            )
        )
    return components


def parameters(graph: BitGraph) -> dict[str, int]:
    return {
        "gamma": domination_number(graph),
        "i": independent_domination_number(graph),
        "alpha": alpha(graph),
        "gamma_infinity": eternal_domination_number(graph),
        "theta": theta(graph),
    }


def analyze(record: str, root_vertices: tuple[int, int, int], target: int):
    graph = BitGraph.from_graph6(record)
    complement = graph.complement()
    family_result = eternal_fixed_point(graph, 3)
    family = set(family_result.family)
    root = mask(root_vertices)
    target_bit = 1 << target
    assert graph.is_independent(root)
    assert root in family
    assert all(
        root ^ (1 << anchor) ^ target_bit in family
        for anchor in root_vertices
    )

    physical = complement.adj[target]
    spokes = {
        anchor: physical & complement.adj[anchor] for anchor in root_vertices
    }
    anchorless = physical
    for spoke in spokes.values():
        anchorless &= ~spoke
    palettes = {
        vertex: tuple(
            anchor
            for anchor in root_vertices
            if target_bit | (1 << anchor) | (1 << vertex) in family
        )
        for vertex in vertex_list(physical, graph.n)
    }

    component_records = []
    for first, second in link_components(complement, physical):
        first_palettes = {palettes[vertex] for vertex in first}
        second_palettes = {palettes[vertex] for vertex in second}
        assert len(first_palettes) == len(second_palettes) == 1
        assert len(next(iter(first_palettes))) >= 2
        assert len(next(iter(second_palettes))) >= 2
        component_records.append(
            {
                "sides": [first, second],
                "side_palettes": [
                    list(next(iter(first_palettes))),
                    list(next(iter(second_palettes))),
                ],
                "spoke_signatures": [
                    [
                        anchor
                        for anchor, spoke in spokes.items()
                        if any(spoke >> vertex & 1 for vertex in first)
                    ],
                    [
                        anchor
                        for anchor, spoke in spokes.items()
                        if any(spoke >> vertex & 1 for vertex in second)
                    ],
                ],
            }
        )

    for u, v in combinations(vertex_list(physical, graph.n), 2):
        if not (complement.adj[u] >> v & 1):
            continue
        for anchor in root_vertices:
            if anchor in palettes[u]:
                assert not any(
                    complement.adj[u] >> spoke_vertex & 1
                    for spoke_vertex in vertex_list(spokes[anchor], graph.n)
                )
            if anchor in palettes[v]:
                assert not any(
                    complement.adj[v] >> spoke_vertex & 1
                    for spoke_vertex in vertex_list(spokes[anchor], graph.n)
                )

    return {
        "graph6": record,
        "parameters": parameters(graph),
        "greatest_family_size": len(family),
        "attack_obligations": len(family) * (graph.n - 3),
        "root": list(root_vertices),
        "target": target,
        "physical_link": vertex_list(physical, graph.n),
        "spokes": {
            str(anchor): vertex_list(spoke, graph.n)
            for anchor, spoke in spokes.items()
        },
        "anchorless": vertex_list(anchorless, graph.n),
        "palettes": {
            str(vertex): list(palette) for vertex, palette in palettes.items()
        },
        "components": component_records,
    }


def main() -> None:
    equality = analyze("Ksv`f\\knJVis", (1, 2, 3), 0)
    assert equality["parameters"] == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert equality["anchorless"] == []
    assert equality["palettes"] == {
        "6": [1, 2],
        "8": [2, 3],
        "10": [1, 3],
        "11": [1, 2],
    }

    one_spoke = analyze("EEz_", (0, 1, 2), 4)
    assert one_spoke["parameters"] == {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert one_spoke["spokes"] == {"0": [], "1": [], "2": [3]}
    assert one_spoke["anchorless"] == [5]
    assert one_spoke["palettes"] == {"3": [0, 1, 2], "5": [0, 1]}

    anchorless_only = analyze("EFz_", (0, 1, 2), 3)
    assert anchorless_only["parameters"] == {
        "gamma": 2,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    assert anchorless_only["anchorless"] == [4, 5]
    assert anchorless_only["palettes"] == {
        "4": [0, 1, 2],
        "5": [0, 1, 2],
    }

    print(
        json.dumps(
            {
                "schema": "anchorless-full-list-control-replay-v1",
                "theorem_checks": {
                    "component_side_palette_uniformity": True,
                    "spoke_opposite_palette_rule": True,
                    "two_attack_anticompleteness": True,
                },
                "controls": {
                    "equality_two_spoke": equality,
                    "gamma_two_one_spoke_anchorless": one_spoke,
                    "gamma_two_anchorless_only": anchorless_only,
                },
                "scope": {
                    "independent_hostile_review": False,
                    "anchorless_eliminated": False,
                    "full_list_branch_closed": False,
                    "complete_k3": False,
                    "universal_conjecture_resolved": False,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

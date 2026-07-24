#!/usr/bin/env python3
"""Exact finite-graph comparison for the block-reinsertion experiment.

The graphs themselves are defined from stored binary64 coordinates, so the
geometric conclusions remain numerical.  Once those graphs are formed,
degree, component, triangle, and graph-isomorphism calculations below are
finite and exact.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "block_reinsertion.json"
OUTPUT = HERE / "results" / "block_topology.json"


def tight_graph(
    coordinates: list[list[float]], tolerance: float
) -> tuple[float, float, list[int], list[tuple[int, int]]]:
    array = np.asarray(coordinates, dtype=float)
    gram = array @ array.T
    first, second = np.triu_indices(len(array), 1)
    products = gram[first, second]
    maximum = float(np.max(products))
    cutoff = maximum - tolerance
    edges = [
        (int(left), int(right))
        for left, right, product in zip(first, second, products)
        if product >= cutoff
    ]
    clearance = float(np.min(np.abs(products - cutoff)))
    adjacency = [0] * len(array)
    for left, right in edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    return maximum, clearance, adjacency, edges


def graph_invariants(adjacency: list[int]) -> dict[str, object]:
    cardinality = len(adjacency)
    degrees = sorted(mask.bit_count() for mask in adjacency)
    triangle_sum = 0
    for left in range(cardinality):
        neighbors = adjacency[left]
        while neighbors:
            bit = neighbors & -neighbors
            right = bit.bit_length() - 1
            if right > left:
                triangle_sum += (
                    adjacency[left] & adjacency[right]
                ).bit_count()
            neighbors ^= bit
    # Each triangle is counted once for each of its three edges.
    triangle_count = triangle_sum // 3

    unseen = (1 << cardinality) - 1
    component_sizes = []
    while unseen:
        seed = unseen & -unseen
        frontier = seed
        component = 0
        while frontier:
            component |= frontier
            unseen &= ~frontier
            next_frontier = 0
            remaining = frontier
            while remaining:
                bit = remaining & -remaining
                vertex = bit.bit_length() - 1
                next_frontier |= adjacency[vertex]
                remaining ^= bit
            frontier = next_frontier & unseen
        component_sizes.append(component.bit_count())
    return {
        "edge_count": sum(degrees) // 2,
        "degree_sequence": degrees,
        "triangle_count": triangle_count,
        "component_sizes": sorted(component_sizes),
    }


def isomorphism(
    first_adjacency: list[int], second_adjacency: list[int]
) -> tuple[list[int] | None, int]:
    """Exact individualization/refinement graph-isomorphism search."""

    cardinality = len(first_adjacency)
    if len(second_adjacency) != cardinality:
        return None, 0
    visited = 0

    def refine(
        first_colors: list[int], second_colors: list[int]
    ) -> tuple[list[int], list[int]] | None:
        while True:
            keys: list[tuple[object, ...]] = []
            for adjacency, colors in (
                (first_adjacency, first_colors),
                (second_adjacency, second_colors),
            ):
                for vertex in range(cardinality):
                    counts: dict[int, int] = {}
                    neighbors = adjacency[vertex]
                    while neighbors:
                        bit = neighbors & -neighbors
                        neighbor = bit.bit_length() - 1
                        counts[colors[neighbor]] = (
                            counts.get(colors[neighbor], 0) + 1
                        )
                        neighbors ^= bit
                    keys.append(
                        (
                            colors[vertex],
                            tuple(sorted(counts.items())),
                        )
                    )
            palette = {
                key: color
                for color, key in enumerate(sorted(set(keys)))
            }
            new_first = [
                palette[key] for key in keys[:cardinality]
            ]
            new_second = [
                palette[key] for key in keys[cardinality:]
            ]
            if sorted(new_first) != sorted(new_second):
                return None
            if (
                new_first == first_colors
                and new_second == second_colors
            ):
                return new_first, new_second
            first_colors, second_colors = new_first, new_second

    def search(
        first_colors: list[int], second_colors: list[int]
    ) -> list[int] | None:
        nonlocal visited
        visited += 1
        refined = refine(first_colors, second_colors)
        if refined is None:
            return None
        first_colors, second_colors = refined
        classes: dict[int, list[int]] = {}
        for vertex, color in enumerate(first_colors):
            classes.setdefault(color, []).append(vertex)
        nonsingletons = [
            (color, vertices)
            for color, vertices in classes.items()
            if len(vertices) > 1
        ]
        if not nonsingletons:
            inverse_second = {
                color: vertex
                for vertex, color in enumerate(second_colors)
            }
            mapping = [
                inverse_second[color] for color in first_colors
            ]
            for left in range(cardinality):
                for right in range(cardinality):
                    first_edge = (
                        first_adjacency[left] >> right
                    ) & 1
                    second_edge = (
                        second_adjacency[mapping[left]]
                        >> mapping[right]
                    ) & 1
                    if first_edge != second_edge:
                        return None
            return mapping

        color, vertices = min(
            nonsingletons, key=lambda item: len(item[1])
        )
        first_vertex = vertices[0]
        marker = max(first_colors + second_colors) + 1
        for second_vertex, second_color in enumerate(second_colors):
            if second_color != color:
                continue
            next_first = first_colors.copy()
            next_second = second_colors.copy()
            next_first[first_vertex] = marker
            next_second[second_vertex] = marker
            mapping = search(next_first, next_second)
            if mapping is not None:
                return mapping
        return None

    initial_first = [
        neighbors.bit_count() for neighbors in first_adjacency
    ]
    initial_second = [
        neighbors.bit_count() for neighbors in second_adjacency
    ]
    return search(initial_first, initial_second), visited


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    artifact = json.loads(source_bytes)
    tolerance = float(artifact["parameters"]["tight_tolerance"])
    reports = []
    for analysis in artifact["analyses"]:
        cardinality = int(analysis["cardinality"])
        (
            source_maximum,
            source_clearance,
            source_adjacency,
            source_edges,
        ) = tight_graph(
            analysis["source"]["coordinates_float64"], tolerance
        )
        source_invariants = graph_invariants(source_adjacency)
        for run in artifact["runs"]:
            if run["cardinality"] != cardinality:
                continue
            (
                retained_maximum,
                retained_clearance,
                retained_adjacency,
                _retained_edges,
            ) = tight_graph(
                run["retained"]["coordinates_float64"], tolerance
            )
            retained_invariants = graph_invariants(
                retained_adjacency
            )
            mapping, visited = isomorphism(
                source_adjacency, retained_adjacency
            )
            gram_difference = None
            if mapping is not None:
                source_array = np.asarray(
                    analysis["source"]["coordinates_float64"],
                    dtype=float,
                )
                retained_array = np.asarray(
                    run["retained"]["coordinates_float64"],
                    dtype=float,
                )
                source_gram = source_array @ source_array.T
                retained_gram = retained_array @ retained_array.T
                permuted = retained_gram[np.ix_(mapping, mapping)]
                gram_difference = float(
                    np.max(np.abs(source_gram - permuted))
                )
            reports.append(
                {
                    "cardinality": cardinality,
                    "restart": run["restart"],
                    "source_maximum": source_maximum,
                    "retained_maximum": retained_maximum,
                    "maximum_change": (
                        retained_maximum - source_maximum
                    ),
                    "source_cutoff_clearance": source_clearance,
                    "retained_cutoff_clearance": retained_clearance,
                    "source_graph": source_invariants,
                    "retained_graph": retained_invariants,
                    "isomorphic_to_source": mapping is not None,
                    "isomorphism_search_nodes": visited,
                    "source_to_retained_isomorphism": mapping,
                    "mapped_gram_maximum_difference": gram_difference,
                    "topology_changed_up_to_isomorphism": (
                        mapping is None
                    ),
                    "strictly_beats_source_at_1e-12": (
                        retained_maximum
                        < source_maximum - 1.0e-12
                    ),
                }
            )
    output = {
        "schema": "kissing5.block_reinsertion_topology.v1",
        "evidence_status": (
            "FINITE GRAPH RESULTS EXACT FOR GRAPHS FORMED FROM "
            "BINARY64 COORDINATES; GEOMETRIC INTERPRETATION IS "
            "NUMERICAL EVIDENCE ONLY"
        ),
        "source": str(SOURCE.relative_to(HERE.parents[1])),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "tight_tolerance": tolerance,
        "reports": reports,
        "summary": {
            "run_count": len(reports),
            "nonisomorphic_to_source_count": sum(
                report["topology_changed_up_to_isomorphism"]
                for report in reports
            ),
            "strict_improvement_count": sum(
                report["strictly_beats_source_at_1e-12"]
                for report in reports
            ),
        },
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output["summary"], sort_keys=True))


if __name__ == "__main__":
    main()

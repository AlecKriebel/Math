#!/usr/bin/env python3
"""Exhaustive small-case audit of the odd triangle-free deficit lemma.

For a=2 and a=3, every labeled graph on 2a+1 vertices is inspected.
For a=4, a counterexample would have 18 edges and hence be 4-regular.
After fixing one vertex neighborhood by relabeling, the remaining finite
4-by-4 incidence problem is exhaustively inspected.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "results" / "small_case_audit.json"


def edge_data(cardinality: int):
    edges = list(combinations(range(cardinality), 2))
    edge_index = {
        edge: index for index, edge in enumerate(edges)
    }
    return edges, edge_index


def induced_edge_mask(
    vertices: tuple[int, ...], edge_index: dict[tuple[int, int], int]
) -> int:
    return sum(
        1 << edge_index[edge]
        for edge in combinations(vertices, 2)
    )


def decode_edges(
    graph_mask: int, edges: list[tuple[int, int]]
) -> list[list[int]]:
    return [
        [first, second]
        for index, (first, second) in enumerate(edges)
        if (graph_mask >> index) & 1
    ]


def enumerate_all_labeled(a: int) -> dict[str, object]:
    cardinality = 2 * a + 1
    edges, edge_index = edge_data(cardinality)
    triangle_masks = [
        induced_edge_mask(vertices, edge_index)
        for vertices in combinations(range(cardinality), 3)
    ]
    forbidden_independent_masks = [
        induced_edge_mask(vertices, edge_index)
        for vertices in combinations(
            range(cardinality), a + 1
        )
    ]
    histogram: dict[int, int] = {}
    maximum = -1
    maximum_example = -1
    feasible = 0
    for graph in range(1 << len(edges)):
        if any(
            graph & triangle == triangle
            for triangle in triangle_masks
        ):
            continue
        if any(
            graph & subset_edges == 0
            for subset_edges in forbidden_independent_masks
        ):
            continue
        edge_count = graph.bit_count()
        feasible += 1
        histogram[edge_count] = histogram.get(edge_count, 0) + 1
        if edge_count > maximum:
            maximum = edge_count
            maximum_example = graph
    return {
        "a": a,
        "cardinality": cardinality,
        "total_labeled_graphs": 1 << len(edges),
        "feasible_labeled_graphs": feasible,
        "edge_count_histogram": {
            str(edge_count): histogram[edge_count]
            for edge_count in sorted(histogram)
        },
        "maximum_edge_count": maximum,
        "lemma_bound": a * a + 1,
        "maximum_example_edge_mask": maximum_example,
        "maximum_example_edges": decode_edges(
            maximum_example, edges
        ),
    }


def audit_a4_only_possible_violation() -> dict[str, object]:
    """Enumerate the normalized 4-regular nine-vertex case."""

    # A counterexample has maximum degree at most four and at least 18
    # edges.  Handshake forces exactly 18 edges and every degree four.
    # Relabel a chosen vertex as 0 and its neighborhood as A={1,...,4}.
    # Triangle-freeness makes A independent.  Put B={5,...,8}.  The
    # degree equations force exactly two edges in B, row sum 3 for the
    # A-B incidence matrix, and column sum 4-q_b.
    b_edges = list(combinations(range(4), 2))
    internal_edge_sets = 0
    incidence_matrices_checked = 0
    degree_feasible = 0
    triangle_free_survivors = 0
    by_internal_shape = {
        "matching": {
            "internal_edge_sets": 0,
            "degree_feasible_incidence_matrices": 0,
            "triangle_free_survivors": 0,
        },
        "adjacent": {
            "internal_edge_sets": 0,
            "degree_feasible_incidence_matrices": 0,
            "triangle_free_survivors": 0,
        },
    }
    for chosen_indices in combinations(range(len(b_edges)), 2):
        chosen_edges = [b_edges[index] for index in chosen_indices]
        internal_degrees = [0] * 4
        for first, second in chosen_edges:
            internal_degrees[first] += 1
            internal_degrees[second] += 1
        shape = (
            "matching"
            if max(internal_degrees) == 1
            else "adjacent"
        )
        internal_edge_sets += 1
        by_internal_shape[shape]["internal_edge_sets"] += 1
        for incidence in range(1 << 16):
            incidence_matrices_checked += 1
            row_degrees = [
                (
                    (incidence >> (4 * row))
                    & 0b1111
                ).bit_count()
                for row in range(4)
            ]
            if row_degrees != [3, 3, 3, 3]:
                continue
            column_masks = [
                sum(
                    ((incidence >> (4 * row + column)) & 1)
                    << row
                    for row in range(4)
                )
                for column in range(4)
            ]
            if any(
                column_masks[column].bit_count()
                + internal_degrees[column]
                != 4
                for column in range(4)
            ):
                continue
            degree_feasible += 1
            by_internal_shape[shape][
                "degree_feasible_incidence_matrices"
            ] += 1
            # For an edge yz inside B, a common A-neighbor completes a
            # triangle.  There are no other possible triangles.
            if any(
                column_masks[first] & column_masks[second]
                for first, second in chosen_edges
            ):
                continue
            triangle_free_survivors += 1
            by_internal_shape[shape][
                "triangle_free_survivors"
            ] += 1
    return {
        "a": 4,
        "cardinality": 9,
        "lemma_bound": 17,
        "only_possible_violating_edge_count": 18,
        "normalization": (
            "fix v=0 and N(v)={1,2,3,4}; "
            "B={5,6,7,8}"
        ),
        "internal_B_edge_sets": internal_edge_sets,
        "incidence_matrices_per_internal_edge_set": 1 << 16,
        "incidence_matrices_checked": incidence_matrices_checked,
        "degree_feasible_incidence_matrices": degree_feasible,
        "triangle_free_survivors": triangle_free_survivors,
        "violating_graphs_up_to_the_safe_normalization": (
            triangle_free_survivors
        ),
        "by_internal_B_shape": by_internal_shape,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = {
        "schema": "kissing5.odd_triangle_free_deficit_small_a.v1",
        "claim": (
            "If F is triangle-free on 2a+1 vertices and "
            "alpha(F)<=a, then e(F)<=a^2+1."
        ),
        "evidence_status": (
            "COMPUTATIONALLY CERTIFIED SMALL-CASE AUDIT; "
            "THE GENERAL LEMMA HAS A SEPARATE HUMAN PROOF"
        ),
        "full_labeled_enumerations": [
            enumerate_all_labeled(2),
            enumerate_all_labeled(3),
        ],
        "a4_violation_enumeration": (
            audit_a4_only_possible_violation()
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(
        "a=2,3 maxima:",
        [
            record["maximum_edge_count"]
            for record in result["full_labeled_enumerations"]
        ],
    )
    print(
        "a=4 violating survivors:",
        result["a4_violation_enumeration"][
            "triangle_free_survivors"
        ],
    )


if __name__ == "__main__":
    main()

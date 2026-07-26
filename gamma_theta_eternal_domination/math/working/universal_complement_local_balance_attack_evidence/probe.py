#!/usr/bin/env python3
"""Light exact diagnostics for the complement/local-balance proof attack.

This is a falsification probe, not a certificate-producing computation.  It
uses the accepted bitset evaluator only on graphs of order at most eleven and
streams the 853 connected unlabeled graphs of order seven.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys


CAMPAIGN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CAMPAIGN))

from src.verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha,
    dominating_masks,
    domination_number,
    eternal_domination_number,
    eternal_fixed_point,
    independent_domination_number,
    theta,
)


def mask(vertices: tuple[int, ...] | list[int]) -> int:
    value = 0
    for vertex in vertices:
        value |= 1 << vertex
    return value


def parameters(graph: BitGraph) -> dict[str, int]:
    return {
        "n": graph.n,
        "m": graph.size,
        "gamma": domination_number(graph),
        "i": independent_domination_number(graph),
        "alpha": alpha(graph),
        "gamma_infinity": eternal_domination_number(graph),
        "theta": theta(graph),
    }


def legal_labelled_loop(
    graph: BitGraph,
    initial: tuple[int, ...],
    steps: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    state = mask(initial)
    labels = {vertex: label for label, vertex in enumerate(initial)}
    states = [list(initial)]
    for attacked, moved in steps:
        assert not state & (1 << attacked)
        assert state & (1 << moved)
        assert graph.adj[attacked] & (1 << moved)
        successor = state ^ (1 << moved) ^ (1 << attacked)
        assert graph.is_dominating(successor)
        label = labels.pop(moved)
        labels[attacked] = label
        state = successor
        states.append(
            [vertex for vertex in range(graph.n) if state & (1 << vertex)]
        )
    assert state == mask(initial)
    return {
        "states": states,
        "final_label_at_vertex": {
            str(vertex): labels[vertex] for vertex in sorted(labels)
        },
    }


def is_clique(graph: BitGraph, state: int) -> bool:
    vertices = [v for v in range(graph.n) if state & (1 << v)]
    return all(
        graph.adj[left] & (1 << right)
        for left, right in combinations(vertices, 2)
    )


def maximal_clique_sizes(graph: BitGraph) -> list[int]:
    answer: list[int] = []
    for state in range(1, 1 << graph.n):
        if not is_clique(graph, state):
            continue
        if any(
            not state & (1 << x)
            and all(
                graph.adj[x] & (1 << y)
                for y in range(graph.n)
                if state & (1 << y)
            )
            for x in range(graph.n)
        ):
            continue
        answer.append(state.bit_count())
    return sorted(answer)


def bipartite_on(graph: BitGraph, vertices: int) -> bool:
    colors: dict[int, int] = {}
    for root in range(graph.n):
        if not vertices & (1 << root) or root in colors:
            continue
        colors[root] = 0
        stack = [root]
        while stack:
            left = stack.pop()
            for right in range(graph.n):
                if not vertices & (1 << right):
                    continue
                if not graph.adj[left] & (1 << right):
                    continue
                if right in colors:
                    if colors[right] == colors[left]:
                        return False
                else:
                    colors[right] = 1 - colors[left]
                    stack.append(right)
    return True


def all_pairs_have_common_neighbor(graph: BitGraph) -> bool:
    return all(
        bool(graph.adj[left] & graph.adj[right])
        for left, right in combinations(range(graph.n), 2)
    )


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def flag_h1_dimension_mod2(graph: BitGraph) -> int:
    edges = [
        (left, right)
        for left in range(graph.n)
        for right in range(left + 1, graph.n)
        if graph.adj[left] & (1 << right)
    ]
    edge_index = {edge: index for index, edge in enumerate(edges)}
    triangle_boundaries: list[int] = []
    for a, b, c in combinations(range(graph.n), 3):
        if not all(
            graph.adj[left] & (1 << right)
            for left, right in ((a, b), (a, c), (b, c))
        ):
            continue
        triangle_boundaries.append(
            (1 << edge_index[(a, b)])
            | (1 << edge_index[(a, c)])
            | (1 << edge_index[(b, c)])
        )

    unseen = set(range(graph.n))
    component_count = 0
    while unseen:
        component_count += 1
        stack = [unseen.pop()]
        while stack:
            left = stack.pop()
            neighbors = [
                right
                for right in tuple(unseen)
                if graph.adj[left] & (1 << right)
            ]
            for right in neighbors:
                unseen.remove(right)
                stack.append(right)

    cycle_space_dimension = len(edges) - graph.n + component_count
    return cycle_space_dimension - gf2_rank(triangle_boundaries)


def simultaneous_kernel_profile(graph: BitGraph, guard_count: int) -> dict[str, object]:
    configurations = set(dominating_masks(graph, guard_count))
    kernels = [configurations]
    while kernels[-1]:
        previous = kernels[-1]
        current: set[int] = set()
        for state in configurations:
            survives = True
            for attacked in range(graph.n):
                if state & (1 << attacked):
                    continue
                if not any(
                    state & (1 << guard)
                    and graph.adj[attacked] & (1 << guard)
                    and (
                        state ^ (1 << guard) ^ (1 << attacked)
                    )
                    in previous
                    for guard in range(graph.n)
                ):
                    survives = False
                    break
            if survives:
                current.add(state)
        if current == previous:
            break
        kernels.append(current)

    maximum_independent = {
        state
        for state in configurations
        if graph.is_independent(state)
    }
    return {
        "kernel_sizes": [len(kernel) for kernel in kernels],
        "maximum_independent_state_counts": [
            len(kernel & maximum_independent) for kernel in kernels
        ],
        "maximum_independent_state_total": len(maximum_independent),
    }


def family_response_hall_checks(graph: BitGraph, guard_count: int) -> tuple[int, int]:
    family = set(eternal_fixed_point(graph, guard_count).family)
    references = [
        state
        for state in family
        if graph.is_independent(state)
    ]
    checked_independent_sets = 0
    for reference in references:
        outside = graph.full ^ reference
        response_lists: dict[int, int] = {}
        for attacked in range(graph.n):
            if reference & (1 << attacked):
                continue
            colors = 0
            for guard in range(graph.n):
                if not reference & (1 << guard):
                    continue
                if not graph.adj[attacked] & (1 << guard):
                    continue
                successor = reference ^ (1 << guard) ^ (1 << attacked)
                if successor in family:
                    colors |= 1 << guard
            assert colors
            response_lists[attacked] = colors

        subset = outside
        while True:
            if graph.is_independent(subset):
                checked_independent_sets += 1
                union = 0
                remaining = subset
                while remaining:
                    bit = remaining & -remaining
                    union |= response_lists[bit.bit_length() - 1]
                    remaining ^= bit
                assert union.bit_count() >= subset.bit_count()
            if subset == 0:
                break
            subset = (subset - 1) & outside
    return len(references), checked_independent_sets


def order_seven_homology_scan() -> dict[str, object]:
    geng = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
    completed = subprocess.run(
        [str(geng), "-q", "-c", "7"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    records = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    assert len(records) == 853

    equality_records: list[str] = []
    nonzero_h1: list[dict[str, object]] = []
    hall_references = 0
    hall_independent_sets = 0
    for record in records:
        graph = BitGraph.from_graph6(record)
        if parameters(graph) != {
            "n": 7,
            "m": graph.size,
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        }:
            continue
        equality_records.append(record)
        reference_count, independent_set_count = family_response_hall_checks(
            graph, 3
        )
        hall_references += reference_count
        hall_independent_sets += independent_set_count
        complement = graph.complement()
        dimension = flag_h1_dimension_mod2(complement)
        if dimension:
            nonzero_h1.append(
                {
                    "G_graph6": record,
                    "H_graph6": complement.to_graph6(),
                    "H1_dimension_mod2": dimension,
                }
            )
    return {
        "connected_unlabeled_graphs": len(records),
        "equality_k3_graphs": len(equality_records),
        "family_response_hall": {
            "maximum_independent_references": hall_references,
            "independent_outside_sets_checked": hall_independent_sets,
            "violations": 0,
        },
        "nonzero_complement_flag_H1": nonzero_h1,
    }


def main() -> None:
    c4 = BitGraph.cycle(4)
    c4_loop = legal_labelled_loop(
        c4,
        (0, 2),
        ((1, 0), (3, 2), (0, 3), (2, 1)),
    )

    c7 = BitGraph.cycle(7)
    c7_loop = legal_labelled_loop(
        c7,
        (0, 2, 4),
        (
            (5, 4),
            (3, 2),
            (1, 0),
            (6, 5),
            (4, 3),
            (2, 1),
            (0, 6),
        ),
    )
    c7_complement = c7.complement()

    deep_near_miss = BitGraph.from_graph6("J@l|bfNuVK_")
    deep_complement = deep_near_miss.complement()

    payload = {
        "model": "one guard; unoccupied attacks; one edge per response",
        "C4_label_exchange": {
            "parameters": parameters(c4),
            "loop": c4_loop,
        },
        "C7_facet_holonomy": {
            "parameters": parameters(c7),
            "H_graph6": c7_complement.to_graph6(),
            "all_pairs_common_neighbor_in_H": all_pairs_have_common_neighbor(
                c7_complement
            ),
            "maximal_clique_sizes_in_H": maximal_clique_sizes(c7_complement),
            "all_vertex_links_bipartite": all(
                bipartite_on(c7_complement, c7_complement.adj[vertex])
                for vertex in range(7)
            ),
            "loop": c7_loop,
        },
        "deep_near_miss_J": {
            "G_graph6": deep_near_miss.to_graph6(),
            "H_graph6": deep_complement.to_graph6(),
            "parameters": parameters(deep_near_miss),
            "all_pairs_common_neighbor_in_H": all_pairs_have_common_neighbor(
                deep_complement
            ),
            "maximal_clique_sizes_in_H": maximal_clique_sizes(deep_complement),
            "all_vertex_links_bipartite": all(
                bipartite_on(deep_complement, deep_complement.adj[vertex])
                for vertex in range(deep_complement.n)
            ),
            "simultaneous_k3_kernel": simultaneous_kernel_profile(
                deep_near_miss, 3
            ),
        },
        "order7_topology_scan": order_seven_homology_scan(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

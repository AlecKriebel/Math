#!/usr/bin/env python3
"""Light exact audit for the line-graph holonomy referee note.

This script constructs only named graphs of order at most 15.  Parameter
values are evaluated independently by verifier A and verifier B.  It imports
no synthesis or production-search code and launches no SAT solver.
"""

from __future__ import annotations

from itertools import combinations
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha as alpha_a,
    domination_number as gamma_a,
    eternal_fixed_point,
    eternal_domination_number as eternal_a,
    independent_domination_number as independent_gamma_a,
    theta as theta_a,
)
from verifier_b import (  # noqa: E402
    Graph,
    chromatic_number,
    clique_cover_number,
    domination_number as gamma_b,
    eternal_domination_number as eternal_b,
    find_eternal_family,
    independence_number as alpha_b,
    independent_domination_number as independent_gamma_b,
    is_dominating,
)


PETERSEN_EDGES = (
    (0, 3),
    (1, 4),
    (2, 5),
    (0, 6),
    (1, 6),
    (2, 6),
    (2, 7),
    (3, 7),
    (4, 7),
    (1, 8),
    (3, 8),
    (5, 8),
    (0, 9),
    (4, 9),
    (5, 9),
)


def edges_a(graph: BitGraph) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for second in range(graph.n)
        for first in range(second)
        if graph.adj[first] & (1 << second)
    )


def line_edges(
    host_edges: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for second in range(len(host_edges))
        for first in range(second)
        if set(host_edges[first]).intersection(host_edges[second])
    )


def graph_pair(
    host_order: int,
    host_edges: tuple[tuple[int, int], ...],
) -> tuple[BitGraph, Graph, BitGraph, Graph]:
    host_a = BitGraph.from_edges(host_order, host_edges)
    host_b = Graph.from_edges(host_order, host_edges)
    line = line_edges(host_edges)
    line_a = BitGraph.from_edges(len(host_edges), line)
    line_b = Graph.from_edges(len(host_edges), line)
    return host_a, host_b, line_a, line_b


def parameters_a(graph: BitGraph) -> dict[str, int]:
    return {
        "alpha": alpha_a(graph),
        "gamma": gamma_a(graph),
        "gamma_infinity_one_guard": eternal_a(graph),
        "i": independent_gamma_a(graph),
        "theta": theta_a(graph),
    }


def parameters_b(graph: Graph) -> dict[str, int]:
    return {
        "alpha": alpha_b(graph),
        "gamma": gamma_b(graph),
        "gamma_infinity_one_guard": eternal_b(graph),
        "i": independent_gamma_b(graph),
        "theta": clique_cover_number(graph),
    }


def induced_a(graph: BitGraph, chosen: tuple[int, ...]) -> BitGraph:
    position = {old: new for new, old in enumerate(chosen)}
    return BitGraph.from_edges(
        len(chosen),
        (
            (position[first], position[second])
            for later, second in enumerate(chosen)
            for first in chosen[:later]
            if graph.adj[first] & (1 << second)
        ),
    )


def induced_b(graph: Graph, chosen: tuple[int, ...]) -> Graph:
    position = {old: new for new, old in enumerate(chosen)}
    return Graph.from_edges(
        len(chosen),
        (
            (position[first], position[second])
            for later, second in enumerate(chosen)
            for first in chosen[:later]
            if graph.has_edge(first, second)
        ),
    )


def clique_number_b(graph: Graph) -> int:
    return alpha_b(graph.complement())


def clique_masks_b(graph: Graph) -> tuple[int, ...]:
    found: list[int] = []
    for mask in range(1, 1 << graph.order):
        vertices = tuple(
            vertex for vertex in graph.vertices if mask & (1 << vertex)
        )
        if all(
            graph.has_edge(first, second)
            for second_index, second in enumerate(vertices)
            for first in vertices[:second_index]
        ):
            found.append(mask)
    return tuple(found)


def local_profile(graph: Graph, parameter: int) -> dict[str, object]:
    clique_masks = clique_masks_b(graph)
    maximal_sizes: list[int] = []
    link_rows: dict[int, list[tuple[int, int, int]]] = {
        size: [] for size in range(1, parameter)
    }
    for mask in clique_masks:
        vertices = tuple(
            vertex for vertex in graph.vertices if mask & (1 << vertex)
        )
        maximal = not any(
            not (mask & (1 << outside))
            and all(graph.has_edge(outside, vertex) for vertex in vertices)
            for outside in graph.vertices
        )
        if maximal:
            maximal_sizes.append(len(vertices))
        if len(vertices) >= parameter:
            continue
        common = tuple(
            outside
            for outside in graph.vertices
            if not (mask & (1 << outside))
            and all(graph.has_edge(outside, vertex) for vertex in vertices)
        )
        link = induced_b(graph, common)
        link_rows[len(vertices)].append(
            (link.order, clique_number_b(link), chromatic_number(link))
        )
    profiles: dict[str, object] = {}
    for size, rows in link_rows.items():
        census: dict[str, int] = {}
        for row in rows:
            key = ",".join(map(str, row))
            census[key] = census.get(key, 0) + 1
        profiles[str(size)] = {
            "common_link_order_omega_chi_census": census,
            "expected_omega_chi": parameter - size,
            "links_checked": len(rows),
        }
    return {
        "all_maximal_cliques_have_size_parameter":
            set(maximal_sizes) == {parameter},
        "maximal_clique_count": len(maximal_sizes),
        "maximal_clique_sizes": sorted(set(maximal_sizes)),
        "profiles_by_clique_size": profiles,
    }


def distance_at_most_two(graph: Graph) -> bool:
    for first in graph.vertices:
        closed_two = {first} | set(graph.adjacency[first])
        for neighbor in graph.adjacency[first]:
            closed_two.update(graph.adjacency[neighbor])
        if len(closed_two) != graph.order:
            return False
    return True


def odd_cycle_case(order: int) -> dict[str, object]:
    host_a = BitGraph.cycle(order)
    host_b = Graph.from_edges(
        order, ((vertex, (vertex + 1) % order) for vertex in range(order))
    )
    host_edges = edges_a(host_a)
    line_a = BitGraph.from_edges(order, line_edges(host_edges))
    line_b = Graph.from_edges(order, line_edges(host_edges))
    target_a = line_a.complement()
    target_b = line_b.complement()
    values_a = parameters_a(target_a)
    values_b = parameters_b(target_b)
    if values_a != values_b:
        raise AssertionError("odd-cycle evaluator disagreement")
    return {
        "complement_line_graph_graph6": target_a.to_graph6(),
        "host": f"C{order}",
        "host_is_class_II": theta_a(target_a) == 3,
        "line_graph_graph6": line_a.to_graph6(),
        "local_profile": local_profile(line_b, 2),
        "parameters": values_a,
    }


def petersen_case() -> dict[str, object]:
    host_a, host_b, line_a, line_b = graph_pair(10, PETERSEN_EDGES)
    target_a = line_a.complement()
    target_b = line_b.complement()
    values_a = parameters_a(target_a)
    values_b = parameters_b(target_b)
    if values_a != values_b:
        raise AssertionError("Petersen evaluator disagreement")

    family_a = eternal_fixed_point(target_a, 3)
    family_b = find_eternal_family(target_b, 3)
    if family_b is None:
        raise AssertionError("verifier B found no three-guard family")
    dominating_triples = tuple(
        frozenset(candidate)
        for candidate in combinations(target_b.vertices, 3)
        if is_dominating(target_b, candidate)
    )
    all_dominating = frozenset(dominating_triples)
    if set(family_a.family) != {
        sum(1 << vertex for vertex in configuration)
        for configuration in all_dominating
    }:
        raise AssertionError("verifier A family is not all dominating triples")
    if family_b != all_dominating:
        raise AssertionError("verifier B family is not all dominating triples")

    dominating_pairs = tuple(
        candidate
        for candidate in combinations(target_b.vertices, 2)
        if is_dominating(target_b, candidate)
    )
    first_pair = dominating_pairs[0]
    connector_exists = any(
        line_b.has_edge(first_pair[0], candidate)
        and line_b.has_edge(first_pair[1], candidate)
        for candidate in line_b.vertices
        if candidate not in first_pair
    )
    if connector_exists:
        raise AssertionError("reported dominating pair has a line-graph connector")

    return {
        "complement_line_graph_graph6": target_a.to_graph6(),
        "dominating_pair": {
            "host_edge_ids": list(first_pair),
            "host_edges": [list(PETERSEN_EDGES[index]) for index in first_pair],
            "line_graph_common_neighbor_exists": connector_exists,
        },
        "dominating_triples": len(dominating_triples),
        "eternal_family_a_size": len(family_a.family),
        "eternal_family_b_size": len(family_b),
        "host": {
            "degrees": sorted(
                host_a.adj[vertex].bit_count() for vertex in range(host_a.n)
            ),
            "edge_count": host_a.size,
            "edges": [list(edge) for edge in PETERSEN_EDGES],
            "graph6": host_a.to_graph6(),
            "triangle_free": all(
                not (
                    host_b.has_edge(first, second)
                    and host_b.has_edge(first, third)
                    and host_b.has_edge(second, third)
                )
                for first, second, third in combinations(host_b.vertices, 3)
            ),
        },
        "line_graph_diameter_at_most_two": distance_at_most_two(line_b),
        "line_graph_graph6": line_a.to_graph6(),
        "local_profile": local_profile(line_b, 3),
        "parameters": values_a,
    }


def k33_case() -> dict[str, object]:
    host_edges = tuple(
        (left, 3 + right) for left in range(3) for right in range(3)
    )
    _host_a, _host_b, line_a, line_b = graph_pair(6, host_edges)
    target_a = line_a.complement()
    target_b = line_b.complement()
    values_a = parameters_a(target_a)
    values_b = parameters_b(target_b)
    if values_a != values_b:
        raise AssertionError("K3,3 evaluator disagreement")
    return {
        "complement_line_graph_graph6": target_a.to_graph6(),
        "host": "K3,3",
        "line_graph_diameter_at_most_two": distance_at_most_two(line_b),
        "line_graph_graph6": line_a.to_graph6(),
        "local_profile": local_profile(line_b, 3),
        "parameters": values_a,
    }


def critical_core_scan() -> dict[str, object]:
    _host_a, _host_b, line_a, line_b = graph_pair(10, PETERSEN_EDGES)
    minimum_order: int | None = None
    critical: list[dict[str, object]] = []
    chromatic_four_counts: dict[str, int] = {}
    for order in range(4, line_a.n + 1):
        count = 0
        for chosen in combinations(range(line_a.n), order):
            induced = induced_a(line_a, chosen)
            if theta_a(induced.complement()) != 4:
                continue
            count += 1
            vertex_critical = all(
                theta_a(
                    induced_a(
                        induced,
                        tuple(
                            vertex
                            for vertex in range(induced.n)
                            if vertex != removed
                        ),
                    ).complement()
                )
                <= 3
                for removed in range(induced.n)
            )
            if not vertex_critical:
                continue
            profile = local_profile(induced_b(line_b, chosen), 3)
            critical.append(
                {
                    "chosen_line_vertices": list(chosen),
                    "graph6": induced.to_graph6(),
                    "local_profile_passes":
                        profile["all_maximal_cliques_have_size_parameter"]
                        and all(
                            all(
                                tuple(map(int, key.split(",")))[1:] == (
                                    row["expected_omega_chi"],
                                    row["expected_omega_chi"],
                                )
                                for key in row[
                                    "common_link_order_omega_chi_census"
                                ]
                            )
                            for row in profile[
                                "profiles_by_clique_size"
                            ].values()
                        ),
                    "pure_clique_complex":
                        profile["all_maximal_cliques_have_size_parameter"],
                }
            )
        chromatic_four_counts[str(order)] = count
        if critical:
            minimum_order = order
            break
    if minimum_order is None:
        raise AssertionError("no critical four-chromatic induced core found")
    return {
        "chromatic_four_counts_through_first_critical_order":
            chromatic_four_counts,
        "critical_core_count_at_minimum_order": len(critical),
        "critical_cores": critical,
        "minimum_critical_order": minimum_order,
        "none_preserves_both_purity_and_local_profiles": all(
            not row["pure_clique_complex"]
            and not row["local_profile_passes"]
            for row in critical
        ),
        "status": "OBSERVED_EXHAUSTIVE_SUBSET_SCAN_PENDING_HOSTILE_REVIEW",
        "subsets_covered": sum(
            len(tuple(combinations(range(line_a.n), order)))
            for order in range(4, minimum_order + 1)
        ),
    }


def main() -> None:
    petersen = petersen_case()
    k33 = k33_case()
    odd_cycles = [odd_cycle_case(order) for order in (5, 7)]
    critical = critical_core_scan()
    source = Path(__file__).read_bytes()
    evidence = {
        "claim_boundary":
            "Light exact named-graph and induced-subset audit only. "
            "The general line-graph exclusion is proved in the accompanying "
            "mathematical note; this computation launches no SAT solver and "
            "makes no universal conjecture-resolution claim.",
        "critical_core_scan": critical,
        "k33_control": k33,
        "odd_cycle_critical_controls": odd_cycles,
        "petersen_near_miss": petersen,
        "schema": "gamma-theta-universal-holonomy-critical-referee-v1",
        "schema_version": 1,
        "source": {
            "path":
                "reviews/universal_holonomy_critical_graph_referee/audit.py",
            "sha256": hashlib.sha256(source).hexdigest(),
            "size_bytes": len(source),
        },
        "status_labels": {
            "general_family_theorems": "PROVED_IN_COMPANION_NOTE",
            "named_graph_parameters": "EXACT_TWO_EVALUATOR_AGREEMENT",
            "petersen_eternal_family":
                "EXACT_TWO_EVALUATOR_AGREEMENT_ALL_395_DOMINATING_TRIPLES",
            "critical_core_scan":
                "OBSERVED_EXHAUSTIVE_SUBSET_SCAN_PENDING_HOSTILE_REVIEW",
        },
    }
    print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

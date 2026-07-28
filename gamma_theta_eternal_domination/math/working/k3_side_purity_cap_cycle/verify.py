#!/usr/bin/env python3
"""Independent exact verifier for the k=3 side-purity cap-cycle control."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


GRAPH6 = "GCXfVG"
VERTICES = tuple(range(8))
NAMES = {
    0: "a",
    1: "b",
    2: "c",
    3: "z",
    4: "x0",
    5: "x1",
    6: "x2",
    7: "x3",
}
S = frozenset({0, 1, 2})


def edge(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


EXPECTED_G = {
    edge(0, 3),
    edge(0, 6),
    edge(0, 7),
    *(edge(1, x) for x in range(4, 8)),
    *(edge(2, x) for x in range(4, 8)),
    edge(4, 6),
    edge(5, 7),
}

EXPECTED_H = {
    edge(0, 1),
    edge(0, 2),
    edge(1, 2),
    edge(1, 3),
    edge(2, 3),
    *(edge(3, x) for x in range(4, 8)),
    edge(0, 4),
    edge(0, 5),
    edge(4, 5),
    edge(5, 6),
    edge(6, 7),
    edge(4, 7),
}

RIM = (4, 5, 6, 7)
RIM_EDGES = {
    edge(4, 5),
    edge(5, 6),
    edge(6, 7),
    edge(4, 7),
}


def pairs(vertices):
    return itertools.combinations(vertices, 2)


def graph6_decode(record: str) -> tuple[tuple[int, ...], set[tuple[int, int]]]:
    raw = record.encode("ascii")
    assert raw and 63 <= raw[0] <= 125
    n = raw[0] - 63
    assert n <= 62
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    assert len(bits) >= needed
    graph_edges: set[tuple[int, int]] = set()
    position = 0
    for high in range(1, n):
        for low in range(high):
            if bits[position]:
                graph_edges.add((low, high))
            position += 1
    return tuple(range(n)), graph_edges


def graph6_encode(
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> str:
    n = len(vertices)
    assert vertices == tuple(range(n))
    bits = [
        int((low, high) in graph_edges)
        for high in range(1, n)
        for low in range(high)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = sum(bits[start + offset] << (5 - offset) for offset in range(6))
        payload.append(chr(63 + value))
    return chr(63 + n) + "".join(payload)


def complement_edges(
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    return {edge(u, v) for u, v in pairs(vertices) if edge(u, v) not in graph_edges}


def neighbors(
    vertex: int,
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> set[int]:
    return {
        other
        for other in vertices
        if other != vertex and edge(vertex, other) in graph_edges
    }


def connected(
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> bool:
    reached = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        u = stack.pop()
        for v in neighbors(u, vertices, graph_edges) - reached:
            reached.add(v)
            stack.append(v)
    return reached == set(vertices)


def dominates(
    state,
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> bool:
    state = frozenset(state)
    return all(
        vertex in state
        or any(edge(vertex, guard) in graph_edges for guard in state)
        for vertex in vertices
    )


def independent(state, graph_edges: set[tuple[int, int]]) -> bool:
    return all(edge(u, v) not in graph_edges for u, v in pairs(state))


def domination_number(
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> int:
    for size in range(1, len(vertices) + 1):
        if any(
            dominates(state, vertices, graph_edges)
            for state in itertools.combinations(vertices, size)
        ):
            return size
    raise AssertionError("finite graph has no dominating set")


def independence_number(
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> int:
    for size in range(len(vertices), 0, -1):
        if any(
            independent(state, graph_edges)
            for state in itertools.combinations(vertices, size)
        ):
            return size
    return 0


def chromatic_number(
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
) -> int:
    adjacency = {
        vertex: neighbors(vertex, vertices, graph_edges) for vertex in vertices
    }
    order = sorted(vertices, key=lambda vertex: (-len(adjacency[vertex]), vertex))
    for color_count in range(1, len(vertices) + 1):
        assignment: dict[int, int] = {}

        def visit(position: int) -> bool:
            if position == len(order):
                return True
            vertex = order[position]
            forbidden = {
                assignment[other]
                for other in adjacency[vertex]
                if other in assignment
            }
            for color in range(color_count):
                if color in forbidden:
                    continue
                assignment[vertex] = color
                if visit(position + 1):
                    return True
                del assignment[vertex]
            return False

        if visit(0):
            return color_count
    raise AssertionError("unreachable")


def successors(
    state: frozenset[int],
    attack: int,
    graph_edges: set[tuple[int, int]],
) -> set[frozenset[int]]:
    return {
        frozenset((set(state) - {guard}) | {attack})
        for guard in state
        if edge(guard, attack) in graph_edges
    }


def greatest_safe_family(
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
    guard_count: int,
) -> tuple[set[frozenset[int]], list[int], int]:
    family = {
        frozenset(state)
        for state in itertools.combinations(vertices, guard_count)
        if dominates(state, vertices, graph_edges)
    }
    initial_size = len(family)
    deletion_round_sizes: list[int] = []
    while True:
        removed = {
            state
            for state in family
            if any(
                not any(
                    successor in family
                    for successor in successors(state, attack, graph_edges)
                )
                for attack in set(vertices) - set(state)
            )
        }
        if not removed:
            return family, deletion_round_sizes, initial_size
        deletion_round_sizes.append(len(removed))
        family -= removed


def response_lists(
    reference: frozenset[int],
    vertices: tuple[int, ...],
    graph_edges: set[tuple[int, int]],
    family: set[frozenset[int]],
) -> dict[int, set[int]]:
    return {
        outside: {
            anchor
            for anchor in reference
            if edge(anchor, outside) in graph_edges
            and frozenset((set(reference) - {anchor}) | {outside}) in family
        }
        for outside in set(vertices) - set(reference)
    }


def direct_list_colorings(
    outside: tuple[int, ...],
    h_edges: set[tuple[int, int]],
    lists: dict[int, set[int]],
) -> list[dict[int, int]]:
    colorings: list[dict[int, int]] = []
    assignment: dict[int, int] = {}

    def visit(position: int) -> None:
        if position == len(outside):
            colorings.append(dict(assignment))
            return
        vertex = outside[position]
        for color in sorted(lists[vertex]):
            if any(
                edge(vertex, other) in h_edges and assignment[other] == color
                for other in assignment
            ):
                continue
            assignment[vertex] = color
            visit(position + 1)
            del assignment[vertex]

    visit(0)
    return colorings


def components_with_bipartition(
    induced_vertices: set[int],
    h_edges: set[tuple[int, int]],
) -> tuple[dict[int, int], dict[int, int]]:
    adjacency = {vertex: set() for vertex in induced_vertices}
    for u, v in h_edges:
        if u in adjacency and v in adjacency:
            adjacency[u].add(v)
            adjacency[v].add(u)
    component: dict[int, int] = {}
    color: dict[int, int] = {}
    component_index = 0
    for start in sorted(induced_vertices):
        if start in color:
            continue
        component[start] = component_index
        color[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in color:
                    component[v] = component_index
                    color[v] = color[u] ^ 1
                    stack.append(v)
                else:
                    assert color[v] != color[u]
        component_index += 1
    return component, color


def side_purity_checks(
    vertices: tuple[int, ...],
    reference: frozenset[int],
    h_edges: set[tuple[int, int]],
    lists: dict[int, set[int]],
) -> dict[str, dict]:
    outside = set(vertices) - set(reference)
    report: dict[str, dict] = {}
    for anchor in sorted(reference):
        positive = {vertex for vertex in outside if anchor in lists[vertex]}
        omitting = outside - positive
        component, color = components_with_bipartition(omitting, h_edges)
        exposed_hubs = []
        checks = 0
        for hub in sorted(outside):
            if not any(
                edge(hub, p) in h_edges for p in positive if p != hub
            ):
                continue
            exposed_hubs.append(hub)
            by_component: dict[int, set[int]] = {}
            for neighbor in omitting:
                if neighbor != hub and edge(hub, neighbor) in h_edges:
                    by_component.setdefault(component[neighbor], set()).add(
                        color[neighbor]
                    )
            for sides in by_component.values():
                checks += 1
                assert len(sides) <= 1
        report[str(anchor)] = {
            "exposed_hubs": exposed_hubs,
            "omitting_vertices": sorted(omitting),
            "positive_vertices": sorted(positive),
            "side_purity_component_checks": checks,
        }
    return report


def c079_embeddings(
    vertices: tuple[int, ...],
    reference: frozenset[int],
    h_edges: set[tuple[int, int]],
    lists: dict[int, set[int]],
) -> dict[str, int]:
    outside = set(vertices) - set(reference)
    counts: dict[str, int] = {}
    for anchor in sorted(reference):
        positive = [vertex for vertex in outside if anchor in lists[vertex]]
        omitting = [vertex for vertex in outside if anchor not in lists[vertex]]
        count = 0
        for vertex_count in range(2, len(omitting) + 1):
            path_length = vertex_count - 1
            if path_length % 2 == 0:
                continue
            for path in itertools.permutations(omitting, vertex_count):
                if not all(
                    edge(path[index], path[index + 1]) in h_edges
                    for index in range(path_length)
                ):
                    continue
                for p in positive:
                    for q in outside:
                        if len({p, q, *path}) != vertex_count + 2:
                            continue
                        if (
                            edge(p, q) in h_edges
                            and edge(q, path[0]) in h_edges
                            and edge(q, path[-1]) in h_edges
                        ):
                            count += 1
        counts[str(anchor)] = count
    return counts


def state_name(state: frozenset[int]) -> str:
    return "".join(str(vertex) for vertex in sorted(state))


def pair_list(edge_set: set[tuple[int, int]]) -> list[list[int]]:
    return [list(item) for item in sorted(edge_set)]


def build_result() -> dict:
    vertices, graph_edges = graph6_decode(GRAPH6)
    assert vertices == VERTICES
    assert graph_edges == EXPECTED_G
    assert len(graph_edges) == 13
    assert graph6_encode(vertices, graph_edges) == GRAPH6

    h_edges = complement_edges(vertices, graph_edges)
    assert h_edges == EXPECTED_H
    assert len(h_edges) == 15
    assert connected(vertices, graph_edges)

    kernels = {}
    kernel_families: dict[int, set[frozenset[int]]] = {}
    for guard_count in (1, 2, 3):
        family, rounds, initial_size = greatest_safe_family(
            vertices, graph_edges, guard_count
        )
        kernel_families[guard_count] = family
        kernels[str(guard_count)] = {
            "deletion_round_sizes": rounds,
            "dominating_states_initially": initial_size,
            "greatest_safe_family_states": len(family),
        }

    family = kernel_families[3]
    expected_d_pairs = {
        frozenset(pair)
        for pair in itertools.combinations({1, 2, 4, 5, 6, 7}, 2)
        if frozenset(pair) not in {frozenset({4, 6}), frozenset({5, 7})}
    }
    expected_family = {
        frozenset({t}) | d_pair for t in (0, 3) for d_pair in expected_d_pairs
    }
    assert len(expected_family) == 26
    assert family == expected_family

    obligations = 0
    successor_minimum = 3
    successor_maximum = 0
    for state in sorted(family, key=lambda item: tuple(sorted(item))):
        assert dominates(state, vertices, graph_edges)
        for attack in sorted(set(vertices) - set(state)):
            obligations += 1
            retained = successors(state, attack, graph_edges) & family
            assert retained
            successor_minimum = min(successor_minimum, len(retained))
            successor_maximum = max(successor_maximum, len(retained))
    assert obligations == 26 * 5 == 130

    lists = response_lists(S, vertices, graph_edges, family)
    expected_lists = {
        3: {0},
        4: {1, 2},
        5: {1, 2},
        6: {1, 2},
        7: {1, 2},
    }
    assert lists == expected_lists

    colorings = direct_list_colorings((3, 4, 5, 6, 7), h_edges, lists)
    expected_colorings = [
        {3: 0, 4: 1, 5: 2, 6: 1, 7: 2},
        {3: 0, 4: 2, 5: 1, 6: 2, 7: 1},
    ]
    assert colorings == expected_colorings

    gamma = domination_number(vertices, graph_edges)
    alpha = independence_number(vertices, graph_edges)
    gamma_infinity = next(
        guard_count
        for guard_count in (1, 2, 3)
        if kernel_families[guard_count]
    )
    theta = chromatic_number(vertices, h_edges)
    assert (gamma, alpha, gamma_infinity, theta) == (3, 3, 3, 3)

    clique_partition = [{0, 3}, {1, 4, 6}, {2, 5, 7}]
    assert set().union(*clique_partition) == set(vertices)
    assert sum(len(part) for part in clique_partition) == len(vertices)
    assert all(
        all(edge(u, v) in graph_edges for u, v in pairs(part))
        for part in clique_partition
    )

    k4s = [
        clique
        for clique in itertools.combinations(vertices, 4)
        if all(edge(u, v) in h_edges for u, v in pairs(clique))
    ]
    dominating_pairs = [
        pair
        for pair in itertools.combinations(vertices, 2)
        if dominates(pair, vertices, graph_edges)
    ]
    common_h_neighbor_counts = {
        f"{u}{v}": len(
            neighbors(u, vertices, h_edges) & neighbors(v, vertices, h_edges)
        )
        for u, v in itertools.combinations(vertices, 2)
    }
    assert not k4s
    assert not dominating_pairs
    assert all(count >= 1 for count in common_h_neighbor_counts.values())

    rim_induced_edges = {
        edge(u, v) for u, v in pairs(RIM) if edge(u, v) in h_edges
    }
    assert rim_induced_edges == RIM_EDGES
    cap_common_neighborhoods = {
        f"{u}{v}": sorted(
            neighbors(u, vertices, h_edges) & neighbors(v, vertices, h_edges)
        )
        for u, v in sorted(RIM_EDGES)
    }
    assert all(3 in common for common in cap_common_neighborhoods.values())
    assert cap_common_neighborhoods["67"] == [3]
    assert edge(0, 6) in graph_edges and edge(0, 7) in graph_edges

    side_purity = side_purity_checks(vertices, S, h_edges, lists)
    fan_counts = c079_embeddings(vertices, S, h_edges, lists)
    assert fan_counts == {"0": 0, "1": 0, "2": 0}

    result = {
        "classification": {
            "colorable_positive_control": True,
            "gamma_theta_counterexample": False,
            "response_list_colorings": len(colorings),
            "scope": (
                "Refutes only repeated-cap/finiteness recurrence without "
                "cross-port or terminal-unit data."
            ),
        },
        "eternal_family": {
            "all_dominating_triples_are_retained": True,
            "dominating_triple_count": 26,
            "greatest_eternal_triple_family_count": 26,
            "greatest_safe_kernels": kernels,
            "retained_successors_per_obligation_maximum": successor_maximum,
            "retained_successors_per_obligation_minimum": successor_minimum,
            "states": [
                state_name(state)
                for state in sorted(family, key=lambda item: tuple(sorted(item)))
            ],
            "unoccupied_attack_obligations": obligations,
        },
        "graph": {
            "connected": True,
            "g_edge_count": len(graph_edges),
            "g_edges": pair_list(graph_edges),
            "graph6": GRAPH6,
            "h_edge_count": len(h_edges),
            "h_edges": pair_list(h_edges),
            "vertex_count": len(vertices),
            "vertex_names": {str(key): value for key, value in NAMES.items()},
        },
        "parameters": {
            "alpha": alpha,
            "gamma": gamma,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "reference": {
            "direct_list_colorings": [
                {str(key): value for key, value in coloring.items()}
                for coloring in colorings
            ],
            "lists": {
                str(vertex): sorted(response)
                for vertex, response in sorted(lists.items())
            },
            "state": sorted(S),
        },
        "repeated_cap_cycle": {
            "all_rim_edges_capped_by_z": True,
            "cap_common_h_neighborhoods": cap_common_neighborhoods,
            "cap_vertex": 3,
            "fully_dynamic_edge": [6, 7],
            "fully_dynamic_edge_unique_cap": 3,
            "rim_bipartition": [[4, 6], [5, 7]],
            "rim_edges": pair_list(RIM_EDGES),
        },
        "safety_exits": {
            "c079_embedding_counts_by_anchor": fan_counts,
            "complement_k4_count": len(k4s),
            "dominating_pair_count": len(dominating_pairs),
            "every_pair_has_common_h_neighbor": True,
            "side_purity_checks": side_purity,
        },
        "schema": "k3-side-purity-cap-cycle-v1",
        "status": "PASS",
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        type=Path,
        help="compare the deterministic result with an existing JSON artifact",
    )
    args = parser.parse_args()

    result = build_result()
    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        assert result == expected
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

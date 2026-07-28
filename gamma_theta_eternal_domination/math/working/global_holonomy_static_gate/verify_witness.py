#!/usr/bin/env python3
"""Independent exact verifier for the seven-vertex static-gate control.

Only the Python standard library is used.  In particular, this checker does
not import either campaign eternal-domination implementation or the SAT
discovery code.  It checks:

* both graph encodings and complementarity;
* all static link/common-neighbor/K4 conditions;
* exact gamma, i, alpha, theta, and one-guard gamma-infinity for G;
* the explicit two-attack failure tree from a forced independent triple;
* two independently represented greatest-fixed-point computations;
* absence of any smaller static countermodel by exhaustive labeled
  enumeration through order six;
* canonical graph6 identifiers using a caller-supplied ``labelg`` binary.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path
from typing import Iterable


VertexSet = frozenset[int]


def normalized_edges(edges: Iterable[Iterable[int]], order: int) -> tuple[tuple[int, int], ...]:
    found: set[tuple[int, int]] = set()
    for raw in edges:
        pair = tuple(raw)
        if len(pair) != 2:
            raise ValueError("an edge must have two endpoints")
        u, v = pair
        if type(u) is not int or type(v) is not int:
            raise ValueError("edge endpoints must be integers")
        if not (0 <= u < order and 0 <= v < order) or u == v:
            raise ValueError("invalid edge")
        found.add((u, v) if u < v else (v, u))
    if len(found) != len(tuple(tuple(edge) for edge in edges)):
        raise ValueError("duplicate edge")
    return tuple(sorted(found))


def adjacency(order: int, edges: Iterable[tuple[int, int]]) -> tuple[int, ...]:
    answer = [0] * order
    for u, v in edges:
        answer[u] |= 1 << v
        answer[v] |= 1 << u
    return tuple(answer)


def graph6_decode(text: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    raw = text.encode("ascii")
    if not raw or raw[0] < 63 or raw[0] > 125:
        raise ValueError("only compact graph6 records are accepted")
    order = raw[0] - 63
    needed = order * (order - 1) // 2
    values = [byte - 63 for byte in raw[1:]]
    if len(values) != (needed + 5) // 6 or any(not 0 <= x <= 63 for x in values):
        raise ValueError("malformed graph6 payload")
    bits = [
        (value >> shift) & 1
        for value in values
        for shift in range(5, -1, -1)
    ]
    if any(bits[needed:]):
        raise ValueError("nonzero graph6 padding")
    found: list[tuple[int, int]] = []
    position = 0
    for v in range(1, order):
        for u in range(v):
            if bits[position]:
                found.append((u, v))
            position += 1
    return order, tuple(sorted(found))


def graph6_encode(order: int, edges: Iterable[tuple[int, int]]) -> str:
    edge_set = set(edges)
    bits = [
        int((u, v) in edge_set)
        for v in range(1, order)
        for u in range(v)
    ]
    while len(bits) % 6:
        bits.append(0)
    return chr(order + 63) + "".join(
        chr(
            63
            + sum(
                bits[start + offset] << (5 - offset)
                for offset in range(6)
            )
        )
        for start in range(0, len(bits), 6)
    )


def canonicalize(labelg: Path, record: str) -> str:
    completed = subprocess.run(
        [str(labelg.resolve()), "-q"],
        input=record + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    lines = completed.stdout.splitlines()
    if len(lines) != 1:
        raise ValueError("labelg did not return exactly one record")
    return lines[0]


def subsets(order: int, cardinality: int) -> Iterable[VertexSet]:
    return map(frozenset, itertools.combinations(range(order), cardinality))


def is_independent(adj: tuple[int, ...], chosen: VertexSet) -> bool:
    return all(not (adj[u] >> v & 1) for u, v in itertools.combinations(chosen, 2))


def is_dominating(adj: tuple[int, ...], chosen: VertexSet) -> bool:
    covered = set(chosen)
    for vertex in chosen:
        covered.update(v for v in range(len(adj)) if adj[vertex] >> v & 1)
    return len(covered) == len(adj)


def exact_gamma(adj: tuple[int, ...]) -> int:
    for cardinality in range(len(adj) + 1):
        if any(is_dominating(adj, chosen) for chosen in subsets(len(adj), cardinality)):
            return cardinality
    raise AssertionError


def exact_alpha(adj: tuple[int, ...]) -> int:
    for cardinality in range(len(adj), -1, -1):
        if any(is_independent(adj, chosen) for chosen in subsets(len(adj), cardinality)):
            return cardinality
    raise AssertionError


def exact_i(adj: tuple[int, ...]) -> int:
    for cardinality in range(len(adj) + 1):
        if any(
            is_independent(adj, chosen) and is_dominating(adj, chosen)
            for chosen in subsets(len(adj), cardinality)
        ):
            return cardinality
    raise AssertionError


def coloring(adj: tuple[int, ...], color_count: int) -> tuple[int, ...] | None:
    order = len(adj)
    assigned = [-1] * order

    def extend(done: int) -> bool:
        if done == order:
            return True
        vertex = max(
            (v for v in range(order) if assigned[v] < 0),
            key=lambda v: (
                len(
                    {
                        assigned[w]
                        for w in range(order)
                        if adj[v] >> w & 1 and assigned[w] >= 0
                    }
                ),
                adj[v].bit_count(),
                -v,
            ),
        )
        forbidden = {
            assigned[w]
            for w in range(order)
            if adj[vertex] >> w & 1 and assigned[w] >= 0
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if extend(done + 1):
                return True
            assigned[vertex] = -1
        return False

    return tuple(assigned) if extend(0) else None


def exact_chromatic(adj: tuple[int, ...]) -> int:
    for count in range(1, len(adj) + 1):
        if coloring(adj, count) is not None:
            return count
    raise AssertionError


def dominating_configurations(adj: tuple[int, ...], guards: int) -> set[VertexSet]:
    return {
        chosen
        for chosen in subsets(len(adj), guards)
        if is_dominating(adj, chosen)
    }


def successors(
    adj: tuple[int, ...],
    source: VertexSet,
    attack: int,
    universe: set[VertexSet],
) -> set[VertexSet]:
    return {
        frozenset((source - {guard}) | {attack})
        for guard in source
        if adj[guard] >> attack & 1
        and frozenset((source - {guard}) | {attack}) in universe
    }


def kernel_sets(
    adj: tuple[int, ...], guards: int
) -> tuple[set[VertexSet], dict[VertexSet, int]]:
    """Synchronous set/frozenset greatest-fixed-point deletion."""

    all_configurations = dominating_configurations(adj, guards)
    surviving = set(all_configurations)
    ranks: dict[VertexSet, int] = {}
    round_number = 1
    while surviving:
        doomed = {
            source
            for source in surviving
            if any(
                not successors(adj, source, attack, surviving)
                for attack in range(len(adj))
                if attack not in source
            )
        }
        if not doomed:
            break
        for source in doomed:
            ranks[source] = round_number
        surviving -= doomed
        round_number += 1
    return surviving, ranks


def kernel_bitmasks(adj: tuple[int, ...], guards: int) -> set[int]:
    """Independent bit-mask fixed point with precomputed colored arcs."""

    order = len(adj)
    configs = [
        sum(1 << v for v in chosen)
        for chosen in subsets(order, guards)
        if is_dominating(adj, chosen)
    ]
    config_set = set(configs)
    attacks: dict[tuple[int, int], int] = {}
    for source in configs:
        for attack in range(order):
            if source >> attack & 1:
                continue
            target_mask = 0
            for guard in range(order):
                if source >> guard & 1 and adj[guard] >> attack & 1:
                    target = source ^ (1 << guard) ^ (1 << attack)
                    if target in config_set:
                        target_mask |= 1 << configs.index(target)
            attacks[source, attack] = target_mask
    active = (1 << len(configs)) - 1
    while True:
        doomed = 0
        for position, source in enumerate(configs):
            if not (active >> position & 1):
                continue
            if any(
                not (targets & active)
                for (state, _), targets in attacks.items()
                if state == source
            ):
                doomed |= 1 << position
        if not doomed:
            break
        active &= ~doomed
    return {
        source
        for position, source in enumerate(configs)
        if active >> position & 1
    }


def bipartite_link(adj: tuple[int, ...], root: int) -> tuple[bool, bool, bool]:
    vertices = {v for v in range(len(adj)) if adj[root] >> v & 1}
    colors: dict[int, int] = {}
    components = 0
    for start in sorted(vertices):
        if start in colors:
            continue
        components += 1
        colors[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in vertices:
                if not (adj[vertex] >> neighbor & 1):
                    continue
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    stack.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False, False, False
    isolate_free = all(adj[v] & sum(1 << x for x in vertices) for v in vertices)
    return True, isolate_free, components == 1


def static_conditions(adj: tuple[int, ...], require_nonthree: bool) -> bool:
    order = len(adj)
    if not any(
        all(adj[u] >> v & 1 for u, v in itertools.combinations(triple, 2))
        for triple in itertools.combinations(range(order), 3)
    ):
        return False
    if any(
        all(adj[u] >> v & 1 for u, v in itertools.combinations(four, 2))
        for four in itertools.combinations(range(order), 4)
    ):
        return False
    if any(
        not (adj[u] & adj[v])
        for u, v in itertools.combinations(range(order), 2)
    ):
        return False
    if any(bipartite_link(adj, root)[:2] != (True, True) for root in range(order)):
        return False
    return not require_nonthree or coloring(adj, 3) is None


def exhaustive_smaller_orders() -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for order in range(1, 7):
        pairs = tuple(itertools.combinations(range(order), 2))
        static_count = 0
        nonthree_count = 0
        for graph_mask in range(1 << len(pairs)):
            edges = [
                pair
                for position, pair in enumerate(pairs)
                if graph_mask >> position & 1
            ]
            adj = adjacency(order, edges)
            if static_conditions(adj, require_nonthree=False):
                static_count += 1
                if coloring(adj, 3) is None:
                    nonthree_count += 1
        if nonthree_count:
            raise AssertionError("a smaller static countermodel exists")
        result[str(order)] = {
            "labeled_graphs": 1 << len(pairs),
            "static_graphs": static_count,
            "non_three_colorable_static_graphs": nonthree_count,
        }
    return result


def missed(adj: tuple[int, ...], source: VertexSet) -> list[int]:
    return [
        vertex
        for vertex in range(len(adj))
        if vertex not in source
        and not any(adj[guard] >> vertex & 1 for guard in source)
    ]


def verify_dynamic_tree(
    adj: tuple[int, ...], record: dict[str, object]
) -> None:
    source = frozenset(record["forced_independent_state"])
    if not is_independent(adj, source) or len(source) != 3:
        raise AssertionError("root state is not an independent triple")
    attack = record["first_attack"]
    first = record["first_responses"]
    eligible = {guard for guard in source if adj[guard] >> attack & 1}
    if {branch["guard"] for branch in first} != eligible:
        raise AssertionError("first-response list is incomplete")
    for branch in first:
        guard = branch["guard"]
        target = frozenset((source - {guard}) | {attack})
        if sorted(target) != branch["successor"]:
            raise AssertionError("wrong first successor")
        if "second_attack" not in branch:
            if missed(adj, target) != branch["missed_vertices"]:
                raise AssertionError("wrong first-level domination failure")
            continue
        if not is_dominating(adj, target):
            raise AssertionError("second-level state should dominate")
        second_attack = branch["second_attack"]
        second = branch["second_responses"]
        second_eligible = {
            vertex for vertex in target if adj[vertex] >> second_attack & 1
        }
        if {item["guard"] for item in second} != second_eligible:
            raise AssertionError("second-response list is incomplete")
        for item in second:
            successor = frozenset(
                (target - {item["guard"]}) | {second_attack}
            )
            if sorted(successor) != item["successor"]:
                raise AssertionError("wrong second successor")
            if missed(adj, successor) != item["missed_vertices"]:
                raise AssertionError("wrong second-level domination failure")


def explicit_four_family() -> set[VertexSet]:
    return {
        frozenset((a, b, c, 6))
        for a in (0, 1)
        for b in (2, 3)
        for c in (4, 5)
    }


def verify_family(adj: tuple[int, ...], family: set[VertexSet]) -> bool:
    return bool(family) and all(
        len(source) == 4
        and is_dominating(adj, source)
        and all(
            successors(adj, source, attack, family)
            for attack in range(len(adj))
            if attack not in source
        )
        for source in family
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--labelg", type=Path, required=True)
    arguments = parser.parse_args()

    raw = arguments.witness.read_bytes()
    data = json.loads(raw)
    if data["schema"] != "gamma-theta-global-holonomy-static-control-v1":
        raise ValueError("wrong witness schema")
    order = 7
    g_edges = normalized_edges(data["G"]["edges"], order)
    h_edges = normalized_edges(data["H"]["edges"], order)
    all_pairs = set(itertools.combinations(range(order), 2))
    if set(g_edges) | set(h_edges) != all_pairs or set(g_edges) & set(h_edges):
        raise AssertionError("G and H are not complements")
    if graph6_decode(data["G"]["labeled_graph6"]) != (order, g_edges):
        raise AssertionError("G graph6 mismatch")
    if graph6_decode(data["H"]["labeled_graph6"]) != (order, h_edges):
        raise AssertionError("H graph6 mismatch")
    if graph6_encode(order, g_edges) != data["G"]["labeled_graph6"]:
        raise AssertionError("independent G graph6 encoding mismatch")
    if graph6_encode(order, h_edges) != data["H"]["labeled_graph6"]:
        raise AssertionError("independent H graph6 encoding mismatch")
    for name in ("G", "H"):
        if canonicalize(arguments.labelg, data[name]["labeled_graph6"]) != data[name]["canonical_graph6"]:
            raise AssertionError(f"{name} canonical graph6 mismatch")

    g_adj = adjacency(order, g_edges)
    h_adj = adjacency(order, h_edges)
    if not static_conditions(h_adj, require_nonthree=True):
        raise AssertionError("H does not meet the static gate")
    link_records = {}
    for root in range(order):
        bipartite, isolate_free, connected = bipartite_link(h_adj, root)
        if (bipartite, isolate_free, connected) != (True, True, True):
            raise AssertionError("every link should be a connected P4")
        link_vertices = [v for v in range(order) if h_adj[root] >> v & 1]
        link_edges = [
            [u, v]
            for u, v in itertools.combinations(link_vertices, 2)
            if h_adj[u] >> v & 1
        ]
        if len(link_vertices) != 4 or len(link_edges) != 3:
            raise AssertionError("link is not P4-sized")
        link_degrees = sorted(
            sum(vertex in edge for edge in link_edges)
            for vertex in link_vertices
        )
        if link_degrees != [1, 1, 2, 2]:
            raise AssertionError("connected link is not a P4")
        link_records[str(root)] = {
            "vertices": link_vertices,
            "edges": link_edges,
            "connected": connected,
        }

    parameters = {
        "gamma": exact_gamma(g_adj),
        "independent_domination": exact_i(g_adj),
        "alpha": exact_alpha(g_adj),
        "theta": exact_chromatic(h_adj),
    }
    set_kernel_three, ranks = kernel_sets(g_adj, 3)
    set_kernel_four, _ = kernel_sets(g_adj, 4)
    bit_kernel_three = kernel_bitmasks(g_adj, 3)
    bit_kernel_four = kernel_bitmasks(g_adj, 4)
    if set_kernel_three or bit_kernel_three:
        raise AssertionError("three guards unexpectedly survive")
    if {
        sum(1 << vertex for vertex in source) for source in set_kernel_four
    } != bit_kernel_four:
        raise AssertionError("independent four-guard kernels disagree")
    if not set_kernel_four:
        raise AssertionError("four guards unexpectedly fail")
    parameters["eternal_domination"] = 4
    if parameters != data["expected_parameters_G"]:
        raise AssertionError("parameter tuple mismatch")
    if not verify_family(g_adj, explicit_four_family()):
        raise AssertionError("explicit four-guard family fails")
    verify_dynamic_tree(g_adj, data["dynamic_failure"])

    dominating_three = dominating_configurations(g_adj, 3)
    rank_histogram: dict[str, int] = {}
    for rank in ranks.values():
        rank_histogram[str(rank)] = rank_histogram.get(str(rank), 0) + 1
    if len(dominating_three) != 14 or rank_histogram != {"1": 7, "2": 7}:
        raise AssertionError("unexpected three-configuration rank census")

    common_neighbor_table = {
        f"{u},{v}": [
            w for w in range(order) if h_adj[u] >> w & 1 and h_adj[v] >> w & 1
        ]
        for u, v in itertools.combinations(range(order), 2)
    }
    smaller = exhaustive_smaller_orders()

    # The clique complex is pure flag dimension two.  Its seven facets are
    # exactly the cyclic triples {i,i+2,i+4}; its boundary is one 7-cycle.
    facets = sorted(
        sorted(triple)
        for triple in itertools.combinations(range(order), 3)
        if all(h_adj[u] >> v & 1 for u, v in itertools.combinations(triple, 2))
    )
    expected_facets = sorted(
        sorted({i, (i + 2) % 7, (i + 4) % 7}) for i in range(7)
    )
    if facets != expected_facets:
        raise AssertionError("unexpected clique-complex facets")
    incidence: dict[tuple[int, int], int] = {}
    for facet in facets:
        for edge in itertools.combinations(facet, 2):
            incidence[edge] = incidence.get(edge, 0) + 1
    boundary = sorted([list(edge) for edge, count in incidence.items() if count == 1])
    if len(boundary) != 7 or sorted(incidence.values()) != [1] * 7 + [2] * 7:
        raise AssertionError("unexpected manifold edge incidence")
    boundary_adjacency = {vertex: set() for vertex in range(order)}
    for u, v in boundary:
        boundary_adjacency[u].add(v)
        boundary_adjacency[v].add(u)
    if any(len(neighbors) != 2 for neighbors in boundary_adjacency.values()):
        raise AssertionError("the boundary is not two-regular")
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in boundary_adjacency[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    if reached != set(range(order)):
        raise AssertionError("the boundary is not one connected 7-cycle")

    edge_deletion_survivors = []
    for deleted in h_edges:
        reduced = adjacency(order, (edge for edge in h_edges if edge != deleted))
        if static_conditions(reduced, require_nonthree=True):
            edge_deletion_survivors.append(list(deleted))
    output = {
        "schema": "gamma-theta-global-holonomy-static-control-verification-v1",
        "status": "PASS",
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "order": order,
        "sizes": {"G": len(g_edges), "H": len(h_edges)},
        "canonical_graph6": {
            "G": data["G"]["canonical_graph6"],
            "H": data["H"]["canonical_graph6"],
        },
        "parameters_G": parameters,
        "static_H": {
            "omega": exact_alpha(g_adj),
            "chi": exact_chromatic(h_adj),
            "every_pair_has_common_neighbor": all(common_neighbor_table.values()),
            "all_links_connected_bipartite_isolate_free": True,
            "link_records": link_records,
            "common_neighbor_table": common_neighbor_table,
        },
        "eternal_kernel": {
            "dominating_triples": len(dominating_three),
            "surviving_triples_set_core": len(set_kernel_three),
            "surviving_triples_bit_core": len(bit_kernel_three),
            "synchronous_rank_histogram": rank_histogram,
            "surviving_four_sets": len(set_kernel_four),
            "explicit_four_family_size": len(explicit_four_family()),
        },
        "clique_complex": {
            "flag": True,
            "pure_dimension": 2,
            "f_vector": [7, 14, 7],
            "euler_characteristic": 0,
            "facets": facets,
            "boundary_edges": boundary,
            "boundary_components": 1,
            "surface": "Moebius band",
        },
        "minimality": {
            "all_labeled_graphs_through_order_six": smaller,
            "order_minimal": True,
            "edge_minimal": not edge_deletion_survivors,
            "single_edge_deletions_still_passing_full_gate": edge_deletion_survivors,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

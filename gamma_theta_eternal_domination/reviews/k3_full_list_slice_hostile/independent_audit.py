#!/usr/bin/env python3
"""Clean-room audit of the k=3 full family-response-list slice.

No function from the target probe or campaign evaluators is imported.
The order-nine coverage replay uses integer masks.  The order-twelve
control is checked again with ordinary frozenset configurations.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import subprocess
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
TARGET = CAMPAIGN / "math" / "working" / "k3_full_list_slice"
GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> tuple[int, ...]:
    raw = record.strip().encode("ascii")
    if not raw or not 63 <= raw[0] <= 125:
        raise ValueError(record)
    order = raw[0] - 63
    required = order * (order - 1) // 2
    bits = []
    for byte in raw[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < required:
        raise ValueError("truncated graph6")
    rows = [0] * order
    position = 0
    for high in range(1, order):
        for low in range(high):
            if bits[position]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            position += 1
    return tuple(rows)


def bit_vertices(mask: int):
    while mask:
        final = mask & -mask
        yield final.bit_length() - 1
        mask ^= final


def choose_masks(order: int, size: int):
    for chosen in itertools.combinations(range(order), size):
        mask = 0
        for vertex in chosen:
            mask |= 1 << vertex
        yield mask


def independent_mask(graph: tuple[int, ...], state: int) -> bool:
    for vertex in bit_vertices(state):
        if graph[vertex] & (state ^ (1 << vertex)):
            return False
    return True


def closed_rows(graph: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(row | (1 << vertex) for vertex, row in enumerate(graph))


def dominates_mask(closed: tuple[int, ...], state: int, universe: int) -> bool:
    reached = 0
    for vertex in bit_vertices(state):
        reached |= closed[vertex]
    return reached == universe


def static_full_incidences(graph: tuple[int, ...]) -> list[tuple[int, int]]:
    order = len(graph)
    universe = (1 << order) - 1
    closed = closed_rows(graph)
    answer = []
    for reference in choose_masks(order, 3):
        if not independent_mask(graph, reference):
            continue
        for target in range(order):
            target_bit = 1 << target
            if reference & target_bit:
                continue
            if graph[target] & reference != reference:
                continue
            if all(
                dominates_mask(
                    closed,
                    (reference ^ (1 << guard)) | target_bit,
                    universe,
                )
                for guard in bit_vertices(reference)
            ):
                answer.append((reference, target))
    return answer


def alpha_is_three(graph: tuple[int, ...], known_independent_triple: bool) -> bool:
    if not known_independent_triple:
        return False
    return not any(
        independent_mask(graph, state)
        for state in choose_masks(len(graph), 4)
    )


def gamma_is_three(graph: tuple[int, ...]) -> bool:
    order = len(graph)
    universe = (1 << order) - 1
    closed = closed_rows(graph)
    if any(row == universe for row in closed):
        return False
    if any(
        closed[left] | closed[right] == universe
        for left, right in itertools.combinations(range(order), 2)
    ):
        return False
    return any(
        dominates_mask(closed, state, universe)
        for state in choose_masks(order, 3)
    )


def greatest_triple_kernel(graph: tuple[int, ...]) -> set[int]:
    order = len(graph)
    universe = (1 << order) - 1
    closed = closed_rows(graph)
    current = {
        state
        for state in choose_masks(order, 3)
        if dominates_mask(closed, state, universe)
    }
    while True:
        removed = set()
        for state in current:
            for attack in bit_vertices(universe ^ state):
                if not any(
                    ((state ^ (1 << guard)) | (1 << attack)) in current
                    for guard in bit_vertices(state & graph[attack])
                ):
                    removed.add(state)
                    break
        if not removed:
            return current
        current -= removed


def response_guards(
    graph: tuple[int, ...],
    family: set[int],
    reference: int,
    target: int,
) -> tuple[int, ...]:
    return tuple(
        guard
        for guard in bit_vertices(reference & graph[target])
        if ((reference ^ (1 << guard)) | (1 << target)) in family
    )


def scan_through_nine() -> dict:
    rows = []
    for order in range(1, 10):
        completed = subprocess.run(
            (str(GENG), "-cq", str(order)),
            text=True,
            capture_output=True,
            check=True,
        )
        if completed.stderr:
            raise AssertionError(completed.stderr)
        records = [line for line in completed.stdout.splitlines() if line]
        stream = hashlib.sha256(
            "".join(record + "\n" for record in records).encode("ascii")
        ).hexdigest()
        raw_static = 0
        gamma_alpha_graphs = 0
        gamma_alpha_pairs = 0
        eternal_candidate_graphs = 0
        equality_pairs = 0
        histogram = {str(size): 0 for size in range(4)}
        full_pairs = 0
        for record in records:
            graph = decode_graph6(record)
            incidences = static_full_incidences(graph)
            raw_static += len(incidences)
            if not incidences:
                continue
            if not alpha_is_three(graph, known_independent_triple=True):
                continue
            if not gamma_is_three(graph):
                continue
            gamma_alpha_graphs += 1
            gamma_alpha_pairs += len(incidences)
            family = greatest_triple_kernel(graph)
            if not family:
                continue
            eternal_candidate_graphs += 1
            equality_pairs += len(incidences)
            for reference, target in incidences:
                response = response_guards(graph, family, reference, target)
                histogram[str(len(response))] += 1
                if response == tuple(bit_vertices(reference)):
                    full_pairs += 1
        rows.append(
            {
                "order": order,
                "connected_graphs": len(records),
                "graph6_stream_sha256": stream,
                "raw_static_full_pairs": raw_static,
                "gamma_alpha_three_graphs_with_static_full_pair": gamma_alpha_graphs,
                "gamma_alpha_three_static_full_pairs": gamma_alpha_pairs,
                "eternal_three_graphs_among_those_candidates": eternal_candidate_graphs,
                "equality_static_pairs_in_eternal_graphs": equality_pairs,
                "equality_static_pair_family_list_size_histogram": histogram,
                "greatest_family_full_pairs": full_pairs,
            }
        )
    totals = {
        key: sum(row[key] for row in rows)
        for key in (
            "connected_graphs",
            "raw_static_full_pairs",
            "gamma_alpha_three_graphs_with_static_full_pair",
            "gamma_alpha_three_static_full_pairs",
            "eternal_three_graphs_among_those_candidates",
            "equality_static_pairs_in_eternal_graphs",
            "greatest_family_full_pairs",
        )
    }
    histogram = {
        str(size): sum(
            row["equality_static_pair_family_list_size_histogram"][str(size)]
            for row in rows
        )
        for size in range(4)
    }
    expected_totals = {
        "connected_graphs": 273193,
        "raw_static_full_pairs": 623732,
        "gamma_alpha_three_graphs_with_static_full_pair": 51,
        "gamma_alpha_three_static_full_pairs": 61,
        "eternal_three_graphs_among_those_candidates": 15,
        "equality_static_pairs_in_eternal_graphs": 24,
        "greatest_family_full_pairs": 0,
    }
    if totals != expected_totals or histogram != {"0": 0, "1": 24, "2": 0, "3": 0}:
        raise AssertionError({"totals": totals, "histogram": histogram})
    return {
        "orders": rows,
        "totals": totals,
        "family_list_size_histogram": histogram,
        "accepted": True,
    }


# The following ordinary-set implementation is separate from the scan core.

Edge = tuple[int, int]
State = frozenset[int]


def edge(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def edge_set(graph: tuple[int, ...]) -> set[Edge]:
    return {
        (left, right)
        for left, right in itertools.combinations(range(len(graph)), 2)
        if graph[left] & (1 << right)
    }


def set_dominates(
    state,
    vertices: tuple[int, ...],
    graph_edges: set[Edge],
) -> bool:
    return all(
        vertex in state
        or any(edge(vertex, guard) in graph_edges for guard in state)
        for vertex in vertices
    )


def set_independent(state, graph_edges: set[Edge]) -> bool:
    return all(edge(left, right) not in graph_edges for left, right in itertools.combinations(state, 2))


def set_successors(state: State, attack: int, graph_edges: set[Edge]) -> set[State]:
    if attack in state:
        raise AssertionError("occupied attack")
    return {
        frozenset((set(state) - {guard}) | {attack})
        for guard in state
        if edge(guard, attack) in graph_edges
    }


def set_greatest_family(
    vertices: tuple[int, ...],
    graph_edges: set[Edge],
) -> set[State]:
    current = {
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if set_dominates(state, vertices, graph_edges)
    }
    while True:
        removed = {
            state
            for state in current
            if any(
                not (set_successors(state, attack, graph_edges) & current)
                for attack in set(vertices) - set(state)
            )
        }
        if not removed:
            return current
        current -= removed


def set_response_lists(
    reference: State,
    vertices: tuple[int, ...],
    graph_edges: set[Edge],
    family: set[State],
) -> dict[int, set[int]]:
    return {
        target: {
            guard
            for guard in reference
            if edge(guard, target) in graph_edges
            and frozenset((set(reference) - {guard}) | {target}) in family
        }
        for target in set(vertices) - set(reference)
    }


def compatible_list_colorings(
    vertices: tuple[int, ...],
    graph_edges: set[Edge],
    reference: State,
    lists: dict[int, set[int]],
) -> list[dict[int, int]]:
    outside = sorted(set(vertices) - set(reference), key=lambda item: (len(lists[item]), item))
    assignment = {anchor: anchor for anchor in reference}
    found = []

    def extend(position: int):
        if position == len(outside):
            found.append(dict(assignment))
            return
        vertex = outside[position]
        for color in sorted(lists[vertex]):
            if any(
                color == assignment[other]
                and edge(vertex, other) not in graph_edges
                for other in assignment
            ):
                continue
            assignment[vertex] = color
            extend(position + 1)
            del assignment[vertex]

    extend(0)
    return found


def order12_control() -> dict:
    labeled = "Ksv`f\\knJVis"
    graph = decode_graph6(labeled)
    vertices = tuple(range(len(graph)))
    graph_edges = edge_set(graph)
    family = set_greatest_family(vertices, graph_edges)
    dominating_triples = {
        frozenset(state)
        for state in itertools.combinations(vertices, 3)
        if set_dominates(state, vertices, graph_edges)
    }
    if family != dominating_triples or len(family) != 127:
        raise AssertionError("order-12 family mismatch")
    obligations = 0
    for state in family:
        for attack in set(vertices) - set(state):
            obligations += 1
            if not (set_successors(state, attack, graph_edges) & family):
                raise AssertionError((state, attack))
    if obligations != 1143:
        raise AssertionError(obligations)

    reference = frozenset({1, 2, 3})
    lists = set_response_lists(reference, vertices, graph_edges, family)
    if lists[0] != set(reference):
        raise AssertionError("target zero is not full")
    expected_lists = {
        0: {1, 2, 3},
        4: {1, 3},
        5: {1, 2},
        6: {2, 3},
        7: {1, 2},
        8: {1, 2},
        9: {2, 3},
        10: {1, 2},
        11: {1, 3},
    }
    if lists != expected_lists:
        raise AssertionError(lists)
    colorings = compatible_list_colorings(
        vertices, graph_edges, reference, lists
    )
    if len(colorings) != 1 or colorings[0][0] != 3:
        raise AssertionError(colorings)
    partition = ({1, 5, 8, 11}, {2, 6, 7, 10}, {0, 3, 4, 9})
    if not all(
        edge(left, right) in graph_edges
        for part in partition
        for left, right in itertools.combinations(part, 2)
    ):
        raise AssertionError("partition failure")

    gamma = next(
        size
        for size in range(1, 4)
        if any(
            set_dominates(state, vertices, graph_edges)
            for state in itertools.combinations(vertices, size)
        )
    )
    alpha = next(
        size
        for size in range(len(vertices), 0, -1)
        if any(
            set_independent(state, graph_edges)
            for state in itertools.combinations(vertices, size)
        )
    )
    if (gamma, alpha) != (3, 3):
        raise AssertionError((gamma, alpha))

    canonical = subprocess.run(
        (str(LABELG), "-q"),
        input=labeled + "\n",
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    if canonical != "K{eYptMJynEn":
        raise AssertionError(canonical)

    link = {
        vertex
        for vertex in vertices
        if vertex != 0 and edge(0, vertex) not in graph_edges
    }
    link_edges = {
        edge(left, right)
        for left, right in itertools.combinations(link, 2)
        if edge(left, right) not in graph_edges
    }
    if link != {6, 8, 10, 11} or link_edges != {(6, 8), (10, 11)}:
        raise AssertionError((link, link_edges))
    spokes = {
        anchor: {
            vertex
            for vertex in link
            if edge(anchor, vertex) not in graph_edges
        }
        for anchor in reference
    }
    if spokes != {1: {6}, 2: {11}, 3: {8, 10}}:
        raise AssertionError(spokes)
    witnesses = {}
    for anchor, spoke in spokes.items():
        for spoke_vertex in spoke:
            witnesses[(anchor, spoke_vertex)] = {
                vertex
                for vertex in vertices
                if vertex not in {anchor, spoke_vertex}
                and edge(anchor, vertex) not in graph_edges
                and edge(spoke_vertex, vertex) not in graph_edges
            }
    expected_witnesses = {
        (1, 6): {9},
        (2, 11): {4},
        (3, 8): {7},
        (3, 10): {5},
    }
    if witnesses != expected_witnesses:
        raise AssertionError(witnesses)
    for (anchor, spoke_vertex), witness_set in witnesses.items():
        if frozenset({0, anchor, spoke_vertex}) not in family:
            raise AssertionError("missing spoke state")
        for witness in witness_set:
            if edge(0, witness) not in graph_edges:
                raise AssertionError("external witness misses full target")
            if frozenset({anchor, spoke_vertex, witness}) not in family:
                raise AssertionError("missing independent witness state")

    local_vertices = tuple(sorted(set(reference) | {0} | link))
    local_counts = {}
    for target_color in sorted(reference):
        allowed = {
            vertex: (
                {target_color}
                if vertex == 0
                else {vertex}
                if vertex in reference
                else set(reference) - {target_color}
            )
            for vertex in local_vertices
        }
        local_assignments = 0
        for values in itertools.product(*(sorted(allowed[vertex]) for vertex in local_vertices)):
            coloring = dict(zip(local_vertices, values))
            if all(
                coloring[left] != coloring[right]
                for left, right in itertools.combinations(local_vertices, 2)
                if edge(left, right) not in graph_edges
            ):
                local_assignments += 1
        local_counts[str(target_color)] = local_assignments
    if local_counts != {"1": 1, "2": 1, "3": 1}:
        raise AssertionError(local_counts)

    return {
        "accepted": True,
        "labeled_graph6": labeled,
        "canonical_graph6": canonical,
        "order": 12,
        "parameters": {
            "gamma": gamma,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "greatest_family_states": len(family),
        "unoccupied_attack_obligations": obligations,
        "full_target": 0,
        "compatible_anchored_colorings": len(colorings),
        "unique_full_target_color": colorings[0][0],
        "local_link_colorings_by_full_target_color": local_counts,
        "link_edges": [list(item) for item in sorted(link_edges)],
        "spokes": {str(key): sorted(value) for key, value in spokes.items()},
        "witnesses": {
            f"{key[0]},{key[1]}": sorted(value)
            for key, value in witnesses.items()
        },
    }


def smaller_controls() -> dict:
    proper_graph = decode_graph6("FDzro")
    proper_vertices = tuple(range(len(proper_graph)))
    proper_edges = edge_set(proper_graph)
    proper_family = {
        frozenset(state)
        for state in (
            (0, 1, 2), (0, 1, 4), (0, 2, 4), (0, 2, 6), (0, 4, 6),
            (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 4, 5),
            (2, 3, 4), (2, 3, 6), (2, 4, 5), (2, 4, 6), (2, 5, 6),
            (3, 4, 6), (4, 5, 6),
        )
    }
    proper_obligations = 0
    for state in proper_family:
        if not set_dominates(state, proper_vertices, proper_edges):
            raise AssertionError("proper control contains a nondominating state")
        for attack in set(proper_vertices) - set(state):
            proper_obligations += 1
            if not (set_successors(state, attack, proper_edges) & proper_family):
                raise AssertionError((state, attack))
    proper_lists = set_response_lists(
        frozenset({0, 1, 2}),
        proper_vertices,
        proper_edges,
        proper_family,
    )
    proper_greatest = set_greatest_family(proper_vertices, proper_edges)
    if (
        proper_obligations != 68
        or proper_lists[4] != {0, 1, 2}
        or len(proper_greatest) != 33
        or not proper_family < proper_greatest
    ):
        raise AssertionError("proper-family control mismatch")

    static_graph = decode_graph6("HCQebjw")
    static_vertices = tuple(range(len(static_graph)))
    static_edges = edge_set(static_graph)
    static_family = set_greatest_family(static_vertices, static_edges)
    static_reference = frozenset({0, 1, 2})
    static_lists = set_response_lists(
        static_reference,
        static_vertices,
        static_edges,
        static_family,
    )
    static_swaps = {
        guard: set_dominates(
            frozenset((set(static_reference) - {guard}) | {8}),
            static_vertices,
            static_edges,
        )
        for guard in static_reference
    }
    static_partition = ({0, 3, 6}, {1, 4, 8}, {2, 5, 7})
    if (
        not all(static_swaps.values())
        or static_lists[8] != {1}
        or len(static_family) != 27
        or not all(
            edge(left, right) in static_edges
            for part in static_partition
            for left, right in itertools.combinations(part, 2)
        )
    ):
        raise AssertionError("static/full-family control mismatch")

    exchange_states = {
        (0, 0), (1, 1), (1, 2), (2, 1), (2, 4), (3, 3),
        (3, 5), (3, 6), (4, 1), (5, 5), (6, 3), (7, 7),
    }
    for removed, inserted in exchange_states:
        for target in range(3):
            if inserted & (1 << target):
                continue
            if not any(
                not (removed & (1 << source))
                and (
                    removed | (1 << source),
                    inserted | (1 << target),
                )
                in exchange_states
                for source in range(3)
            ):
                raise AssertionError("target expansion failure")
        for source in range(3):
            if not (removed & (1 << source)):
                continue
            if not any(
                inserted & (1 << target)
                and (
                    removed & ~(1 << source),
                    inserted & ~(1 << target),
                )
                in exchange_states
                for target in range(3)
            ):
                raise AssertionError("source restoration failure")
    base_orders = []
    for permutation in itertools.permutations(range(3)):
        if all(
            (
                removed,
                sum(
                    1 << permutation[source]
                    for source in range(3)
                    if removed & (1 << source)
                ),
            )
            in exchange_states
            for removed in range(8)
        ):
            base_orders.append(permutation)
    if base_orders or not all((1 << source, 1) in exchange_states for source in range(3)):
        raise AssertionError("abstract full-column control mismatch")

    return {
        "proper_FDzro": {
            "states": len(proper_family),
            "unoccupied_attack_obligations": proper_obligations,
            "greatest_family_states": len(proper_greatest),
            "full_target": 4,
            "accepted": True,
        },
        "static_HCQebjw": {
            "all_static_swaps_dominate": static_swaps,
            "greatest_family_states": len(static_family),
            "greatest_family_target8_list": sorted(static_lists[8]),
            "accepted": True,
        },
        "abstract_full_column": {
            "states": len(exchange_states),
            "full_first_column": True,
            "base_orderings": [],
            "accepted": True,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "independent_result.json")
    parser.add_argument("--skip-scan", action="store_true")
    args = parser.parse_args()
    started = time.time()
    result = {
        "schema": "k3-full-list-slice-hostile-v1",
        "target_hashes": {
            name: sha256(TARGET / name)
            for name in ("NOTE.md", "probe.py", "probe_result.json", "RESEARCH_LOG.md")
        },
        "order12_control": order12_control(),
        "smaller_controls": smaller_controls(),
        "scan_through_order9": (
            {"status": "SKIPPED"} if args.skip_scan else scan_through_nine()
        ),
        "environment": {
            "python": platform.python_version(),
            "geng_sha256": sha256(GENG),
            "labelg_sha256": sha256(LABELG),
        },
    }
    result["elapsed_seconds"] = time.time() - started
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "sha256": sha256(args.output),
                "elapsed_seconds": result["elapsed_seconds"],
                "order12": result["order12_control"]["accepted"],
                "scan_full_pairs": result["scan_through_order9"].get(
                    "totals", {}
                ).get("greatest_family_full_pairs"),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

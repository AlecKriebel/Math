#!/usr/bin/env python3
"""Clean-room audit of the original-edge incidence equality controls.

This file deliberately imports no campaign evaluator, search module, or
source verifier.  Graphs are decoded from their graph6 strings.  All graph
parameters, the simultaneous greatest one-guard triple fixed point,
response lists, frozen projections, representatives, caps, and compatible
list colorings are recomputed with integer bit masks.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


S_VERTICES = (0, 1, 2)
S_MASK = sum(1 << vertex for vertex in S_VERTICES)


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    raw = record.encode("ascii")
    assert raw and raw[0] != ord(":")
    order = raw[0] - 63
    assert 0 <= order <= 62
    bits: list[int] = []
    for char in raw[1:]:
        value = char - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    assert len(bits) >= needed
    assert all(bit == 0 for bit in bits[needed:])
    adjacency = [0] * order
    position = 0
    for high in range(1, order):
        for low in range(high):
            if bits[position]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    return order, tuple(adjacency)


def is_g_edge(adjacency: tuple[int, ...], first: int, second: int) -> bool:
    return first != second and bool(adjacency[first] & (1 << second))


def is_h_edge(adjacency: tuple[int, ...], first: int, second: int) -> bool:
    return first != second and not is_g_edge(adjacency, first, second)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def is_independent(adjacency: tuple[int, ...], mask: int) -> bool:
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if adjacency[vertex] & remaining:
            return False
    return True


def is_dominating(adjacency: tuple[int, ...], mask: int) -> bool:
    covered = mask
    for vertex in vertices(mask):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def is_connected(adjacency: tuple[int, ...]) -> bool:
    seen = 1
    frontier = 1
    while frontier:
        next_frontier = 0
        for vertex in vertices(frontier):
            next_frontier |= adjacency[vertex]
        next_frontier &= ~seen
        seen |= next_frontier
        frontier = next_frontier
    return seen == (1 << len(adjacency)) - 1


def exact_static_parameters(adjacency: tuple[int, ...]) -> dict[str, int]:
    order = len(adjacency)
    gamma = order + 1
    alpha = 0
    independent_domination = order + 1
    for mask in range(1, 1 << order):
        size = mask.bit_count()
        independent = is_independent(adjacency, mask)
        dominating = is_dominating(adjacency, mask)
        if dominating:
            gamma = min(gamma, size)
        if independent:
            alpha = max(alpha, size)
            if dominating:
                independent_domination = min(independent_domination, size)
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
    }


def h_coloring(
    adjacency: tuple[int, ...],
    color_count: int,
    allowed: dict[int, int] | None = None,
    enumerate_all: bool = False,
) -> list[tuple[int, ...]]:
    order = len(adjacency)
    full_colors = (1 << color_count) - 1
    domains = [
        allowed.get(vertex, full_colors) if allowed is not None else full_colors
        for vertex in range(order)
    ]
    assigned = [-1] * order
    answers: list[tuple[int, ...]] = []

    def visit() -> bool:
        if all(color >= 0 for color in assigned):
            answers.append(tuple(assigned))
            return not enumerate_all
        candidate = -1
        candidate_options = 0
        candidate_key = None
        for vertex in range(order):
            if assigned[vertex] >= 0:
                continue
            forbidden = 0
            saturation = set()
            h_degree = 0
            for other in range(order):
                if not is_h_edge(adjacency, vertex, other):
                    continue
                h_degree += 1
                if assigned[other] >= 0:
                    forbidden |= 1 << assigned[other]
                    saturation.add(assigned[other])
            options = domains[vertex] & ~forbidden
            if options == 0:
                return False
            key = (options.bit_count(), -len(saturation), -h_degree, vertex)
            if candidate_key is None or key < candidate_key:
                candidate_key = key
                candidate = vertex
                candidate_options = options
        for color in range(color_count):
            if candidate_options & (1 << color):
                assigned[candidate] = color
                stop = visit()
                assigned[candidate] = -1
                if stop:
                    return True
        return False

    visit()
    return answers


def greatest_triple_kernel(
    adjacency: tuple[int, ...],
) -> tuple[frozenset[int], list[int]]:
    order = len(adjacency)
    family = {
        sum(1 << vertex for vertex in triple)
        for triple in combinations(range(order), 3)
        if is_dominating(
            adjacency, sum(1 << vertex for vertex in triple)
        )
    }
    deletion_round_sizes: list[int] = []
    while True:
        rejected: set[int] = set()
        for state in family:
            for attack in range(order):
                attack_bit = 1 << attack
                if state & attack_bit:
                    continue
                defended = False
                for guard in vertices(state):
                    if not is_g_edge(adjacency, guard, attack):
                        continue
                    successor = (state ^ (1 << guard)) | attack_bit
                    if successor in family:
                        defended = True
                        break
                if not defended:
                    rejected.add(state)
                    break
        if not rejected:
            return frozenset(family), deletion_round_sizes
        deletion_round_sizes.append(len(rejected))
        family.difference_update(rejected)


def family_hash(family: frozenset[int]) -> str:
    payload = "".join(
        ",".join(str(vertex) for vertex in vertices(state)) + "\n"
        for state in sorted(family, key=lambda item: tuple(vertices(item)))
    ).encode("ascii")
    return sha256(payload).hexdigest()


def audit_obligations(
    adjacency: tuple[int, ...], family: frozenset[int]
) -> int:
    obligations = 0
    for state in family:
        assert state.bit_count() == 3
        assert is_dominating(adjacency, state)
        for attack in range(len(adjacency)):
            if state & (1 << attack):
                continue
            obligations += 1
            assert any(
                is_g_edge(adjacency, guard, attack)
                and ((state ^ (1 << guard)) | (1 << attack)) in family
                for guard in vertices(state)
            )
    return obligations


def response_lists(
    adjacency: tuple[int, ...], family: frozenset[int]
) -> dict[int, int]:
    assert S_MASK in family
    answer: dict[int, int] = {}
    for target in range(3, len(adjacency)):
        colors = 0
        for anchor in S_VERTICES:
            successor = (S_MASK ^ (1 << anchor)) | (1 << target)
            if is_g_edge(adjacency, anchor, target) and successor in family:
                colors |= 1 << anchor
        answer[target] = colors
    return answer


def bipartition_projection(
    adjacency: tuple[int, ...],
    lists: dict[int, int],
    omitted: int,
) -> tuple[dict[int, int], dict[int, int], list[tuple[int, int]]]:
    projection = {
        anchor for anchor in S_VERTICES if anchor != omitted
    } | {
        vertex
        for vertex, colors in lists.items()
        if not (colors & (1 << omitted))
    }
    component: dict[int, int] = {}
    parity: dict[int, int] = {}
    edges = [
        (first, second)
        for first, second in combinations(sorted(projection), 2)
        if is_h_edge(adjacency, first, second)
    ]
    h_neighbors = {vertex: set() for vertex in projection}
    for first, second in edges:
        h_neighbors[first].add(second)
        h_neighbors[second].add(first)
    component_number = 0
    for root in sorted(projection):
        if root in parity:
            continue
        parity[root] = 0
        component[root] = component_number
        stack = [root]
        while stack:
            first = stack.pop()
            for second in sorted(h_neighbors[first]):
                if second not in parity:
                    parity[second] = parity[first] ^ 1
                    component[second] = component_number
                    stack.append(second)
                else:
                    assert parity[second] == (parity[first] ^ 1)
        component_number += 1
    return component, parity, edges


def same_sign_physical_representatives(
    adjacency: tuple[int, ...], lists: dict[int, int], port: int
) -> tuple[list[int], dict[str, object]]:
    colors = lists[port]
    omitted_colors = [
        color for color in S_VERTICES if not (colors & (1 << color))
    ]
    assert len(omitted_colors) == 1
    omitted = omitted_colors[0]
    component, parity, edges = bipartition_projection(
        adjacency, lists, omitted
    )
    candidates = [
        vertex
        for vertex, vertex_colors in lists.items()
        if vertex_colors == colors
        and is_h_edge(adjacency, omitted, vertex)
        and component[vertex] == component[port]
        and parity[vertex] == parity[port]
    ]
    return candidates, {
        "omitted": omitted,
        "component": component[port],
        "port_parity": parity[port],
        "projection_edges": [list(edge) for edge in edges],
    }


def caps(
    adjacency: tuple[int, ...],
    lists: dict[int, int],
    first: int,
    second: int,
) -> list[dict[str, object]]:
    answer = []
    for cap in range(len(adjacency)):
        if cap in (first, second):
            continue
        if not (
            is_h_edge(adjacency, first, cap)
            and is_h_edge(adjacency, second, cap)
        ):
            continue
        signature = [
            anchor
            for anchor in S_VERTICES
            if is_h_edge(adjacency, anchor, cap)
        ]
        answer.append(
            {
                "vertex": cap,
                "list": [
                    color
                    for color in S_VERTICES
                    if lists[cap] & (1 << color)
                ]
                if cap in lists
                else None,
                "anchor_signature": signature,
            }
        )
    return answer


def enumerate_response_list_colorings(
    adjacency: tuple[int, ...], lists: dict[int, int]
) -> list[dict[str, int]]:
    outside = sorted(lists)
    allowed = {vertex: lists[vertex] for vertex in outside}
    assignment: dict[int, int] = {}
    answers: list[dict[str, int]] = []

    def visit() -> None:
        if len(assignment) == len(outside):
            full_assignment = {anchor: anchor for anchor in S_VERTICES}
            full_assignment.update(assignment)
            assert all(
                full_assignment[first] != full_assignment[second]
                for first, second in combinations(
                    range(len(adjacency)), 2
                )
                if is_h_edge(adjacency, first, second)
            )
            answers.append(
                {str(vertex): assignment[vertex] for vertex in outside}
            )
            return
        best = None
        best_options = None
        for vertex in outside:
            if vertex in assignment:
                continue
            forbidden = {
                assignment[other]
                for other in assignment
                if is_h_edge(adjacency, vertex, other)
            }
            options = [
                color
                for color in S_VERTICES
                if allowed[vertex] & (1 << color)
                and color not in forbidden
            ]
            key = (len(options), vertex)
            if best is None or key < best:
                best = key
                best_options = (vertex, options)
        assert best_options is not None
        vertex, options = best_options
        for color in options:
            assignment[vertex] = color
            visit()
            del assignment[vertex]

    visit()
    return answers


def common_h_neighbor_counts(adjacency: tuple[int, ...]) -> list[int]:
    counts = []
    for first, second in combinations(range(len(adjacency)), 2):
        count = sum(
            vertex not in (first, second)
            and is_h_edge(adjacency, first, vertex)
            and is_h_edge(adjacency, second, vertex)
            for vertex in range(len(adjacency))
        )
        counts.append(count)
    return counts


def audit_local_gate_table() -> dict[str, object]:
    """Enumerate the three literal-edge constraints without source code."""
    x_domain = (0, 1)
    y_domain = (1, 2)
    rows: dict[str, object] = {}
    sole_unit_free = []
    for z_mask in range(1, 0b111):
        z_domain = tuple(
            color for color in S_VERTICES if z_mask & (1 << color)
        )
        solutions = [
            [x_color, y_color, z_color]
            for x_color in x_domain
            for y_color in y_domain
            for z_color in z_domain
            if len({x_color, y_color, z_color}) == 3
        ]
        assert solutions
        fixed = {}
        for position, name in enumerate(("X", "Y", "Z")):
            values = sorted({solution[position] for solution in solutions})
            if len(values) == 1:
                fixed[name] = values[0]
        key = "".join(str(color) for color in z_domain)
        rows[key] = {"solutions": solutions, "fixed_colors": fixed}
        if not fixed:
            sole_unit_free.append(list(z_domain))
    assert sole_unit_free == [[0, 2]]
    assert rows == {
        "0": {
            "solutions": [[1, 2, 0]],
            "fixed_colors": {"X": 1, "Y": 2, "Z": 0},
        },
        "1": {
            "solutions": [[0, 2, 1]],
            "fixed_colors": {"X": 0, "Y": 2, "Z": 1},
        },
        "2": {
            "solutions": [[0, 1, 2]],
            "fixed_colors": {"X": 0, "Y": 1, "Z": 2},
        },
        "01": {
            "solutions": [[0, 2, 1], [1, 2, 0]],
            "fixed_colors": {"Y": 2},
        },
        "02": {
            "solutions": [[0, 1, 2], [1, 2, 0]],
            "fixed_colors": {},
        },
        "12": {
            "solutions": [[0, 1, 2], [0, 2, 1]],
            "fixed_colors": {"X": 0},
        },
    }
    return {
        "rows": rows,
        "sole_locally_unit_free_cap_list": [0, 2],
    }


def audit_graph(
    record: str,
    expected_size: int,
    expected_family_size: int,
    expected_family_hash: str,
) -> tuple[dict[str, object], tuple[int, ...], dict[int, int]]:
    order, adjacency = decode_graph6(record)
    size = sum(row.bit_count() for row in adjacency) // 2
    assert size == expected_size
    assert is_connected(adjacency)
    static = exact_static_parameters(adjacency)
    assert static == {"gamma": 3, "i": 3, "alpha": 3}
    assert is_independent(adjacency, S_MASK)
    assert is_dominating(adjacency, S_MASK)
    common_counts = common_h_neighbor_counts(adjacency)
    assert min(common_counts) >= 1
    full_colorings = h_coloring(adjacency, 3)
    assert len(full_colorings) == 1
    coloring = full_colorings[0]
    assert all(
        coloring[first] != coloring[second]
        for first, second in combinations(range(order), 2)
        if is_h_edge(adjacency, first, second)
    )
    family, deletion_round_sizes = greatest_triple_kernel(adjacency)
    assert len(family) == expected_family_size
    assert family_hash(family) == expected_family_hash
    obligations = audit_obligations(adjacency, family)
    lists = response_lists(adjacency, family)
    assert all(colors not in (0, 0b111) for colors in lists.values())
    list_colorings = enumerate_response_list_colorings(adjacency, lists)
    assert len(list_colorings) == 2
    return (
        {
            "graph6": record,
            "order": order,
            "size": size,
            "parameters": {
                **static,
                "gamma_infinity": 3,
                "theta": 3,
            },
            "common_H_neighbor_count_minimum": min(common_counts),
            "dominating_triples_initial": expected_family_size
            + sum(deletion_round_sizes),
            "kernel_deletion_round_sizes": deletion_round_sizes,
            "greatest_triple_family_size": len(family),
            "greatest_triple_family_sha256": family_hash(family),
            "one_guard_obligations": obligations,
            "lists_at_S": {
                str(vertex): [
                    color
                    for color in S_VERTICES
                    if colors & (1 << color)
                ]
                for vertex, colors in lists.items()
            },
            "one_complement_3_coloring": list(coloring),
            "compatible_response_list_coloring_count": len(list_colorings),
            "compatible_response_list_colorings": list_colorings,
        },
        adjacency,
        lists,
    )


def build_evidence() -> dict[str, object]:
    first, adjacency14, lists14 = audit_graph(
        "MFzJbZYhlrDZdMhd_",
        51,
        177,
        "43318de751e7f8f80617bde59f5f16948ef41d38dc3fa13a7201ce3e107955ad",
    )
    reps14, projection14 = same_sign_physical_representatives(
        adjacency14, lists14, 3
    )
    assert reps14 == [8]
    assert is_h_edge(adjacency14, 3, 4)
    assert is_h_edge(adjacency14, 3, 9)
    assert is_g_edge(adjacency14, 8, 4)
    assert is_g_edge(adjacency14, 8, 9)
    caps_84 = caps(adjacency14, lists14, 8, 4)
    caps_89 = caps(adjacency14, lists14, 8, 9)
    assert caps_84 == [
        {"vertex": 13, "list": [0, 2], "anchor_signature": [1]}
    ]
    assert caps_89 == [
        {"vertex": 7, "list": [1, 2], "anchor_signature": [0]}
    ]
    first["refutation"] = {
        "port": 3,
        "same_sign_physical_representatives": reps14,
        "specified_original_H_edges": [[3, 4], [3, 9]],
        "corresponding_representative_G_edges": [[8, 4], [8, 9]],
        "caps": {"8,4": caps_84, "8,9": caps_89},
        "projection": projection14,
    }

    second, adjacency15, lists15 = audit_graph(
        "NFzJbZZhlrDZdMhd|h_",
        60,
        216,
        "66b8ac6f738dc501ce5f541ecbad4e782fa449b17ffa0cc2ef77e73d3a3e8580",
    )
    reps_q, projection_q = same_sign_physical_representatives(
        adjacency15, lists15, 3
    )
    reps_v, projection_v = same_sign_physical_representatives(
        adjacency15, lists15, 4
    )
    assert reps_q == [8]
    assert reps_v == [7]
    assert is_h_edge(adjacency15, 3, 4)
    assert is_g_edge(adjacency15, 8, 7)
    caps_87 = caps(adjacency15, lists15, 8, 7)
    assert caps_87 == [
        {"vertex": 13, "list": [0, 2], "anchor_signature": [1]}
    ]
    second["refutation"] = {
        "original_H_edge": [3, 4],
        "port_3_same_sign_physical_representatives": reps_q,
        "port_4_same_sign_physical_representatives": reps_v,
        "representative_pair_is_G_edge": [8, 7],
        "common_H_caps": caps_87,
        "projection_port_3": projection_q,
        "projection_port_4": projection_v,
    }

    return {
        "schema": "gamma-theta-original-edge-incidence-hostile-v1",
        "verdict": "PASS",
        "local_gate_table": audit_local_gate_table(),
        "controls": [first, second],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    evidence = build_evidence()
    if args.check is not None:
        assert evidence == json.loads(args.check.read_text())
        print("PASS")
    else:
        print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

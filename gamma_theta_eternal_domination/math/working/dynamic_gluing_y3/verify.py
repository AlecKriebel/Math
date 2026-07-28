#!/usr/bin/env python3
"""Clean finite checks for the dynamic Y_3 gluing note.

This checker has no dependency on the campaign search code.  It verifies:

1. among all 64 completions of the seven named vertices and all nine
   nonempty family-list subpatterns beneath the static Y_3 lists, local
   one-guard closure can retain the reference state and every listed direct
   swap only when both internal lists are full;
2. the eight-vertex "double static defect" core has no retained reference
   state for any of its 16 remaining adjacency completions; and
3. FDzro is a sharp gamma-two control with a literal 21-state eternal
   family-response Y_3, while its static lists are strictly larger.
4. IzM]XTR`W is a sharp graph-specific negative control: it satisfies the
   static complement conditions, but every dominating-triple state is
   deleted by the one-guard kernel.

The local kernels deliberately overapproximate an actual eternal family:
they contain every core-dominating triple that satisfies restoration.
Deleting the reference state from this greatest overapproximate kernel is
therefore a sound obstruction even when arbitrary vertices exist outside
the displayed core.
"""

from __future__ import annotations

import hashlib
import itertools
import json


S = 0b111


def adjacency(order: int, edges: set[tuple[int, int]]) -> tuple[int, ...]:
    rows = [0] * order
    for left, right in edges:
        if not 0 <= left < right < order:
            raise AssertionError((left, right))
        rows[left] |= 1 << right
        rows[right] |= 1 << left
    return tuple(rows)


def decode_graph6(record: str) -> tuple[int, ...]:
    values = [ord(character) - 63 for character in record.strip()]
    if not values or not 0 <= values[0] <= 62:
        raise AssertionError("only ordinary graph6 records are supported")
    order = values[0]
    bits: list[int] = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges: set[tuple[int, int]] = set()
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                edges.add((left, right))
            cursor += 1
    return adjacency(order, edges)


def masks_of_size(order: int, size: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in subset)
        for subset in itertools.combinations(range(order), size)
    )


def dominates(state: int, graph: tuple[int, ...]) -> bool:
    return all(
        state & (1 << vertex) or state & graph[vertex]
        for vertex in range(len(graph))
    )


def independent(state: int, graph: tuple[int, ...]) -> bool:
    occupied = [vertex for vertex in range(len(graph)) if state & (1 << vertex)]
    return all(
        not (graph[left] & (1 << right))
        for left, right in itertools.combinations(occupied, 2)
    )


def restoration_ok(state: int, lists: dict[int, frozenset[int]]) -> bool:
    missing = {0, 1, 2} - {
        anchor for anchor in range(3) if state & (1 << anchor)
    }
    restored: set[int] = set()
    for vertex, response_list in lists.items():
        if state & (1 << vertex):
            restored.update(response_list)
    return missing <= restored


def local_kernel(
    graph: tuple[int, ...],
    lists: dict[int, frozenset[int]],
) -> tuple[set[int], list[dict[int, int]], int]:
    """Greatest core-closed restoration overapproximation.

    Each deletion-round map records one fatal unoccupied attack per deleted
    state.  Rounds are synchronous, so their ranks are directly replayable.
    """

    order = len(graph)
    active = {
        state
        for state in masks_of_size(order, 3)
        if dominates(state, graph) and restoration_ok(state, lists)
    }
    initial_size = len(active)
    rounds: list[dict[int, int]] = []
    while True:
        doomed: dict[int, int] = {}
        for state in sorted(active):
            for attacked in range(order):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                retained = False
                for guard in range(order):
                    guard_bit = 1 << guard
                    if not (state & guard_bit and graph[attacked] & guard_bit):
                        continue
                    successor = state ^ guard_bit ^ attacked_bit
                    if successor in active:
                        retained = True
                        break
                if not retained:
                    doomed[state] = attacked
                    break
        if not doomed:
            return active, rounds, initial_size
        rounds.append(doomed)
        active.difference_update(doomed)


def unrestricted_kernel(graph: tuple[int, ...], size: int) -> set[int]:
    order = len(graph)
    active = {
        state
        for state in masks_of_size(order, size)
        if dominates(state, graph)
    }
    while True:
        doomed: set[int] = set()
        for state in active:
            for attacked in range(order):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                if not any(
                    state & (1 << guard)
                    and graph[attacked] & (1 << guard)
                    and state ^ (1 << guard) ^ attacked_bit in active
                    for guard in range(order)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return active
        active.difference_update(doomed)


def unrestricted_kernel_trace(
    graph: tuple[int, ...], size: int
) -> tuple[set[int], list[dict[int, int]], int]:
    active = {
        state
        for state in masks_of_size(len(graph), size)
        if dominates(state, graph)
    }
    initial_size = len(active)
    rounds: list[dict[int, int]] = []
    while True:
        doomed: dict[int, int] = {}
        for state in sorted(active):
            for attacked in range(len(graph)):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                if not any(
                    state & (1 << guard)
                    and graph[attacked] & (1 << guard)
                    and state ^ (1 << guard) ^ attacked_bit in active
                    for guard in range(len(graph))
                ):
                    doomed[state] = attacked
                    break
        if not doomed:
            return active, rounds, initial_size
        rounds.append(doomed)
        active.difference_update(doomed)


def direct_states(lists: dict[int, frozenset[int]]) -> set[int]:
    return {
        S ^ (1 << anchor) ^ (1 << vertex)
        for vertex, response_list in lists.items()
        for anchor in response_list
    }


def response_lists(
    graph: tuple[int, ...], family: set[int]
) -> dict[int, frozenset[int]]:
    return {
        vertex: frozenset(
            anchor
            for anchor in range(3)
            if graph[vertex] & (1 << anchor)
            and S ^ (1 << anchor) ^ (1 << vertex) in family
        )
        for vertex in range(3, len(graph))
    }


def static_lists(graph: tuple[int, ...]) -> dict[int, frozenset[int]]:
    return {
        vertex: frozenset(
            anchor
            for anchor in range(3)
            if graph[vertex] & (1 << anchor)
            and dominates(S ^ (1 << anchor) ^ (1 << vertex), graph)
        )
        for vertex in range(3, len(graph))
    }


def domination_number(graph: tuple[int, ...]) -> int:
    for size in range(len(graph) + 1):
        if any(dominates(state, graph) for state in masks_of_size(len(graph), size)):
            return size
    raise AssertionError


def independence_number(graph: tuple[int, ...]) -> int:
    for size in range(len(graph), -1, -1):
        if any(
            independent(state, graph)
            for state in masks_of_size(len(graph), size)
        ):
            return size
    raise AssertionError


def clique_cover_number(graph: tuple[int, ...]) -> int:
    order = len(graph)
    full = (1 << order) - 1
    is_clique = [False] * (1 << order)
    is_clique[0] = True
    for state in range(1, 1 << order):
        bit = state & -state
        vertex = bit.bit_length() - 1
        rest = state ^ bit
        is_clique[state] = is_clique[rest] and not (
            rest & (full ^ bit ^ graph[vertex])
        )
    values = [order + 1] * (1 << order)
    values[0] = 0
    for state in range(1, 1 << order):
        pivot = state & -state
        part = state
        while part:
            if part & pivot and is_clique[part]:
                values[state] = min(values[state], 1 + values[state ^ part])
            part = (part - 1) & state
    return values[full]


def verify_static_to_family_rigidity() -> dict[str, object]:
    # a,b,c,x0,x1,x2,x3 = 0,...,6.
    fixed_edges = {
        (0, 3),
        (0, 4),
        (2, 4),
        (1, 5),
        (2, 5),
        (1, 6),
        (3, 5),
        (3, 6),
        (4, 6),
    }
    optional_edges = (
        (1, 3),
        (2, 3),
        (1, 4),
        (0, 5),
        (0, 6),
        (2, 6),
    )
    left_middle_lists = (
        frozenset({0}),
        frozenset({2}),
        frozenset({0, 2}),
    )
    right_middle_lists = (
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2}),
    )

    survivors: list[dict[str, object]] = []
    cases = 0
    for edge_mask in range(1 << len(optional_edges)):
        edges = set(fixed_edges)
        edges.update(
            edge
            for index, edge in enumerate(optional_edges)
            if edge_mask & (1 << index)
        )
        graph = adjacency(7, edges)
        for left_middle in left_middle_lists:
            for right_middle in right_middle_lists:
                cases += 1
                lists = {
                    3: frozenset({0}),
                    4: left_middle,
                    5: right_middle,
                    6: frozenset({1}),
                }
                family, _, _ = local_kernel(graph, lists)
                if S in family and direct_states(lists) <= family:
                    survivors.append(
                        {
                            "edge_mask": edge_mask,
                            "left_middle": sorted(left_middle),
                            "right_middle": sorted(right_middle),
                            "kernel_size": len(family),
                        }
                    )

    expected = [
        {
            "edge_mask": mask,
            "left_middle": [0, 2],
            "right_middle": [1, 2],
            "kernel_size": size,
        }
        for mask, size in ((46, 21), (47, 22), (62, 22), (63, 23))
    ]
    if survivors != expected:
        raise AssertionError(("static-to-family survivor mismatch", survivors))
    return {
        "cases": cases,
        "survivors": survivors,
        "conclusion": "every survivor has the exact full internal lists",
    }


def verify_double_defect_exclusion() -> dict[str, object]:
    # Add z=7.  The accepted mixed-path theorem fixes cx0 and cx3.
    # A double defect fixes za,zb,zx0,zx3 as nonedges and zc,zx1,zx2
    # as edges.  Only bx0,bx1,ax2,ax3 remain undecided.
    fixed_edges = {
        (0, 3),
        (0, 4),
        (2, 4),
        (1, 5),
        (2, 5),
        (1, 6),
        (2, 3),
        (2, 6),
        (3, 5),
        (3, 6),
        (4, 6),
        (2, 7),
        (4, 7),
        (5, 7),
    }
    optional_edges = ((1, 3), (1, 4), (0, 5), (0, 6))
    lists = {
        3: frozenset({0}),
        4: frozenset({0, 2}),
        5: frozenset({1, 2}),
        6: frozenset({1}),
        7: frozenset({2}),
    }
    required = direct_states(lists)
    rows: list[dict[str, object]] = []
    for edge_mask in range(16):
        edges = set(fixed_edges)
        edges.update(
            edge
            for index, edge in enumerate(optional_edges)
            if edge_mask & (1 << index)
        )
        graph = adjacency(8, edges)
        family, rounds, initial_size = local_kernel(graph, lists)
        initial = {
            state
            for state in masks_of_size(8, 3)
            if dominates(state, graph) and restoration_ok(state, lists)
        }
        if not required <= initial:
            raise AssertionError(("required direct state not initially allowed", edge_mask))
        if S in family:
            raise AssertionError(("double defect retained S", edge_mask))
        reference_rank = next(
            index + 1 for index, round_map in enumerate(rounds) if S in round_map
        )
        rows.append(
            {
                "edge_mask": edge_mask,
                "initial_size": initial_size,
                "round_sizes": [len(round_map) for round_map in rounds],
                "reference_rank": reference_rank,
                "fatal_attack": rounds[reference_rank - 1][S],
            }
        )

    expected_rows = [
        (0, 28, [13, 13, 2], 2, 4),
        (1, 29, [11, 15, 3], 3, 4),
        (2, 29, [11, 12, 6], 2, 4),
        (3, 30, [10, 12, 8], 3, 4),
        (4, 29, [11, 12, 6], 2, 5),
        (5, 30, [9, 12, 9], 3, 5),
        (6, 30, [9, 7, 8, 6], 3, 4),
        (7, 31, [8, 7, 8, 8], 4, 4),
        (8, 29, [11, 15, 3], 3, 4),
        (9, 30, [9, 17, 4], 3, 4),
        (10, 30, [9, 12, 9], 3, 4),
        (11, 31, [8, 14, 9], 3, 4),
        (12, 30, [10, 12, 8], 3, 5),
        (13, 31, [8, 14, 9], 3, 5),
        (14, 31, [8, 7, 8, 8], 4, 4),
        (15, 32, [7, 9, 8, 8], 4, 4),
    ]
    compact = [
        (
            row["edge_mask"],
            row["initial_size"],
            row["round_sizes"],
            row["reference_rank"],
            row["fatal_attack"],
        )
        for row in rows
    ]
    if compact != expected_rows:
        raise AssertionError(("double-defect table mismatch", compact))
    trace_sha256 = hashlib.sha256(
        json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "cases": len(rows),
        "optional_edges": [list(edge) for edge in optional_edges],
        "rows": rows,
        "trace_sha256": trace_sha256,
        "conclusion": "the reference state is deleted in every completion",
    }


def verify_fdzro_control() -> dict[str, object]:
    graph = decode_graph6("FDzro")
    lists = {
        3: frozenset({0}),
        4: frozenset({0, 2}),
        5: frozenset({1, 2}),
        6: frozenset({1}),
    }
    family, _, _ = local_kernel(graph, lists)
    if len(family) != 21 or S not in family:
        raise AssertionError(("FDzro constrained kernel", len(family)))
    if response_lists(graph, family) != lists:
        raise AssertionError(("FDzro family lists", response_lists(graph, family)))

    obligations = 0
    for state in family:
        if not dominates(state, graph):
            raise AssertionError(("nondominating FDzro state", state))
        for attacked in range(7):
            if state & (1 << attacked):
                continue
            obligations += 1
            if not any(
                state & (1 << guard)
                and graph[attacked] & (1 << guard)
                and state ^ (1 << guard) ^ (1 << attacked) in family
                for guard in range(7)
            ):
                raise AssertionError(("failed FDzro obligation", state, attacked))
    if obligations != 84:
        raise AssertionError(obligations)

    parameters = {
        "gamma": domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity": next(
            size for size in range(8) if unrestricted_kernel(graph, size)
        ),
        "theta": clique_cover_number(graph),
    }
    if parameters != {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(("FDzro parameters", parameters))
    expected_static = {
        3: frozenset({0, 2}),
        4: frozenset({0, 1, 2}),
        5: frozenset({0, 1, 2}),
        6: frozenset({1, 2}),
    }
    actual_static = static_lists(graph)
    if actual_static != expected_static:
        raise AssertionError(("FDzro static lists", actual_static))
    family_sha256 = hashlib.sha256(
        ",".join(str(state) for state in sorted(family)).encode()
    ).hexdigest()
    return {
        "graph6": "FDzro",
        "parameters": parameters,
        "family_size": len(family),
        "obligations": obligations,
        "family_sha256": family_sha256,
        "family_lists": {
            str(vertex): sorted(response_list)
            for vertex, response_list in lists.items()
        },
        "static_lists": {
            str(vertex): sorted(response_list)
            for vertex, response_list in actual_static.items()
        },
    }


def complement(graph: tuple[int, ...]) -> tuple[int, ...]:
    full = (1 << len(graph)) - 1
    return tuple(
        full ^ (1 << vertex) ^ graph[vertex]
        for vertex in range(len(graph))
    )


def bipartite_induced(
    graph: tuple[int, ...], vertices: set[int]
) -> bool:
    colors: dict[int, int] = {}
    for start in sorted(vertices):
        if start in colors:
            continue
        colors[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in sorted(vertices):
                if not (graph[vertex] & (1 << neighbor)):
                    continue
                if neighbor not in colors:
                    colors[neighbor] = colors[vertex] ^ 1
                    stack.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def verify_static_negative_control() -> dict[str, object]:
    graph6 = "IzM]XTR`W"
    complement_graph6 = "ICp`eik]_"
    graph = decode_graph6(graph6)
    h_graph = decode_graph6(complement_graph6)
    if complement(graph) != h_graph:
        raise AssertionError("negative-control complement mismatch")

    parameters = {
        "gamma": domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity": next(
            size for size in range(11) if unrestricted_kernel(graph, size)
        ),
        "theta": clique_cover_number(graph),
    }
    if parameters != {
        "gamma": 3,
        "alpha": 3,
        "gamma_infinity": 4,
        "theta": 4,
    }:
        raise AssertionError(("negative-control parameters", parameters))

    k4_count = sum(
        all(h_graph[left] & (1 << right) for left, right in itertools.combinations(vertices, 2))
        for vertices in itertools.combinations(range(10), 4)
    )
    if k4_count:
        raise AssertionError(("negative-control H has K4", k4_count))
    if not all(
        bipartite_induced(
            h_graph,
            {
                neighbor
                for neighbor in range(10)
                if h_graph[vertex] & (1 << neighbor)
            },
        )
        for vertex in range(10)
    ):
        raise AssertionError("negative-control H has nonbipartite link")
    if not all(
        h_graph[left] & h_graph[right]
        for left, right in itertools.combinations(range(10), 2)
    ):
        raise AssertionError("negative-control H pair lacks common neighbor")

    family, rounds, initial_size = unrestricted_kernel_trace(graph, 3)
    if family or initial_size != 77 or [len(row) for row in rounds] != [
        10,
        20,
        40,
        7,
    ]:
        raise AssertionError(
            (
                "negative-control kernel",
                len(family),
                initial_size,
                [len(row) for row in rounds],
            )
        )
    independent_states = {
        state
        for state in masks_of_size(10, 3)
        if independent(state, graph)
    }
    deletion_rank = {
        state: next(
            index + 1
            for index, round_map in enumerate(rounds)
            if state in round_map
        )
        for state in independent_states
    }
    rank_counts = {
        str(rank): sum(value == rank for value in deletion_rank.values())
        for rank in sorted(set(deletion_rank.values()))
    }
    if len(independent_states) != 7 or rank_counts != {"3": 2, "4": 5}:
        raise AssertionError(("negative-control independent ranks", rank_counts))
    return {
        "graph6": graph6,
        "complement_graph6": complement_graph6,
        "parameters": parameters,
        "H_K4_count": k4_count,
        "H_all_links_bipartite": True,
        "H_every_pair_has_common_neighbor": True,
        "dominating_triples": initial_size,
        "deletion_round_sizes": [len(row) for row in rounds],
        "independent_triples": len(independent_states),
        "independent_deletion_rank_counts": rank_counts,
        "terminal_family_size": len(family),
        "greatest_eternal_four_family_size": len(
            unrestricted_kernel(graph, 4)
        ),
    }


def main() -> int:
    result = {
        "schema": "dynamic-gluing-y3-check-v1",
        "static_to_family": verify_static_to_family_rigidity(),
        "double_defect": verify_double_defect_exclusion(),
        "gamma_two_control": verify_fdzro_control(),
        "static_negative_control": verify_static_negative_control(),
    }
    digest = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("PASS: dynamic Y_3 rigidity and double-defect exclusion")
    print(f"result_sha256={digest}")
    print(
        "static_to_family_cases="
        f"{result['static_to_family']['cases']}; "
        "double_defect_cases="
        f"{result['double_defect']['cases']}; "
        "FDzro_obligations="
        f"{result['gamma_two_control']['obligations']}; "
        "negative_control_rounds="
        f"{result['static_negative_control']['deletion_round_sizes']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

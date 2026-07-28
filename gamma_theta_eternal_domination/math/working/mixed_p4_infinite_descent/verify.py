#!/usr/bin/env python3
"""Independent finite-core verifier for the one-defect mixed-P4 theorem.

The decisive check uses ordinary Python ``frozenset`` configurations and
adjacency sets.  It imports no campaign evaluator or predecessor checker.
It exhausts the five genuinely undecided graph edges of the displayed
eight-vertex core, starts from every core-dominating,
restoration-compatible triple, and applies synchronous greatest-fixed-point
deletion for attacks at displayed unoccupied vertices.

Two exact controls are reconstructed as scope checks:

* ``FDzro`` realizes the exact *family* mixed P4 at gamma two, but its
  static lists are larger.
* ``HCOceRy`` is a full equality graph containing two adjacent pure
  singleton vertices of the same response color.  Thus singleton cliques
  alone do not support an infinite-descent claim.
"""

from __future__ import annotations

from itertools import combinations
import hashlib
import json


Vertex = int
State = frozenset[Vertex]
Edge = frozenset[Vertex]

NAMES = ("a", "b", "c", "x0", "x1", "x2", "x3", "d")
ORDER = 8
REFERENCE = frozenset((0, 1, 2))

# Graph edges forced by the exact family mixed P4, endpoint saturation, and
# one left endpoint defect d.
FIXED_GRAPH_EDGES = frozenset(
    Edge(pair)
    for pair in (
        (0, 3),  # a-x0
        (0, 4),  # a-x1
        (2, 4),  # c-x1
        (1, 5),  # b-x2
        (2, 5),  # c-x2
        (1, 6),  # b-x3
        (2, 3),  # c-x0: accepted endpoint saturation
        (2, 6),  # c-x3: accepted endpoint saturation
        (3, 5),  # induced complement-P4 chord x0-x2
        (3, 6),  # induced complement-P4 chord x0-x3
        (4, 6),  # induced complement-P4 chord x1-x3
        (2, 7),  # c-d
        (4, 7),  # x1-d
        (5, 7),  # x2-d
    )
)

FIXED_GRAPH_NONEDGES = frozenset(
    Edge(pair)
    for pair in (
        (0, 1),
        (0, 2),
        (1, 2),  # independent reference triple
        (3, 4),
        (4, 5),
        (5, 6),  # complement P4
        (0, 7),
        (1, 7),
        (3, 7),  # d misses a,b,x0
    )
)

OPTIONAL_GRAPH_EDGES = (
    Edge((1, 3)),  # b-x0
    Edge((1, 4)),  # b-x1
    Edge((0, 5)),  # a-x2
    Edge((0, 6)),  # a-x3
    Edge((6, 7)),  # x3-d
)

RESPONSE_LISTS = {
    3: frozenset((0,)),
    4: frozenset((0, 2)),
    5: frozenset((1, 2)),
    6: frozenset((1,)),
    7: frozenset((2,)),
}


def all_edges(order: int) -> frozenset[Edge]:
    return frozenset(Edge(pair) for pair in combinations(range(order), 2))


def neighborhoods(order: int, edges: frozenset[Edge]) -> tuple[frozenset[int], ...]:
    rows = [set() for _ in range(order)]
    for edge in edges:
        if len(edge) != 2:
            raise AssertionError(f"not a two-vertex edge: {edge}")
        first, second = tuple(edge)
        rows[first].add(second)
        rows[second].add(first)
    return tuple(frozenset(row) for row in rows)


def dominates(state: State, adjacency: tuple[frozenset[int], ...]) -> bool:
    return all(vertex in state or bool(state & adjacency[vertex])
               for vertex in range(len(adjacency)))


def independent(state: State, adjacency: tuple[frozenset[int], ...]) -> bool:
    return all(second not in adjacency[first]
               for first, second in combinations(sorted(state), 2))


def restoration_ok(state: State) -> bool:
    missing = REFERENCE - state
    restored = set()
    for vertex in state - REFERENCE:
        restored.update(RESPONSE_LISTS[vertex])
    return missing <= restored


def direct_states() -> frozenset[State]:
    states = {REFERENCE}
    for vertex, response_list in RESPONSE_LISTS.items():
        for omitted in response_list:
            states.add(frozenset((REFERENCE - {omitted}) | {vertex}))
    return frozenset(states)


def local_kernel(
    adjacency: tuple[frozenset[int], ...],
) -> tuple[frozenset[State], tuple[dict[State, int], ...], int]:
    active = {
        frozenset(state)
        for state in combinations(range(len(adjacency)), 3)
        if dominates(frozenset(state), adjacency)
        and restoration_ok(frozenset(state))
    }
    initial_size = len(active)
    rounds: list[dict[State, int]] = []

    while True:
        doomed: dict[State, int] = {}
        for state in sorted(active, key=lambda item: tuple(sorted(item))):
            for attacked in range(len(adjacency)):
                if attacked in state:
                    continue
                has_response = False
                for guard in sorted(state):
                    if attacked not in adjacency[guard]:
                        continue
                    successor = frozenset((state - {guard}) | {attacked})
                    if successor in active:
                        has_response = True
                        break
                if not has_response:
                    doomed[state] = attacked
                    break
        if not doomed:
            return frozenset(active), tuple(rounds), initial_size
        rounds.append(doomed)
        active.difference_update(doomed)


def state_text(state: State) -> str:
    return "{" + ",".join(NAMES[vertex] for vertex in sorted(state)) + "}"


def verify_core() -> dict[str, object]:
    complete_pairs = all_edges(ORDER)
    decided = (
        FIXED_GRAPH_EDGES
        | FIXED_GRAPH_NONEDGES
        | frozenset(OPTIONAL_GRAPH_EDGES)
    )
    if decided != complete_pairs:
        raise AssertionError(
            {
                "missing_pairs": sorted(
                    sorted(edge) for edge in complete_pairs - decided
                ),
                "overlap_edges_nonedges": sorted(
                    sorted(edge)
                    for edge in FIXED_GRAPH_EDGES & FIXED_GRAPH_NONEDGES
                ),
            }
        )
    if len(FIXED_GRAPH_EDGES) != 14:
        raise AssertionError(len(FIXED_GRAPH_EDGES))
    if len(FIXED_GRAPH_NONEDGES) != 9:
        raise AssertionError(len(FIXED_GRAPH_NONEDGES))
    if len(OPTIONAL_GRAPH_EDGES) != 5:
        raise AssertionError(len(OPTIONAL_GRAPH_EDGES))

    required = direct_states()
    rows: list[dict[str, object]] = []
    for mask in range(1 << len(OPTIONAL_GRAPH_EDGES)):
        edges = set(FIXED_GRAPH_EDGES)
        edges.update(
            edge
            for index, edge in enumerate(OPTIONAL_GRAPH_EDGES)
            if mask & (1 << index)
        )
        adjacency = neighborhoods(ORDER, frozenset(edges))
        initial = {
            frozenset(state)
            for state in combinations(range(ORDER), 3)
            if dominates(frozenset(state), adjacency)
            and restoration_ok(frozenset(state))
        }
        if not required <= initial:
            raise AssertionError(
                (
                    mask,
                    "required state absent initially",
                    sorted(state_text(state) for state in required - initial),
                )
            )

        terminal, rounds, initial_size = local_kernel(adjacency)
        if terminal:
            raise AssertionError(
                (
                    mask,
                    "nonempty terminal local kernel",
                    sorted(state_text(state) for state in terminal),
                )
            )
        reference_round = next(
            index + 1
            for index, round_map in enumerate(rounds)
            if REFERENCE in round_map
        )
        rows.append(
            {
                "mask": mask,
                "mask_binary": format(mask, "05b"),
                "optional_edge_flags_in_list_order": [
                    int(bool(mask & (1 << index)))
                    for index in range(len(OPTIONAL_GRAPH_EDGES))
                ],
                "present_optional_edges": [
                    sorted(edge)
                    for index, edge in enumerate(OPTIONAL_GRAPH_EDGES)
                    if mask & (1 << index)
                ],
                "initial_size": initial_size,
                "round_sizes": [len(round_map) for round_map in rounds],
                "reference_deletion_round": reference_round,
                "reference_fatal_attack": NAMES[
                    rounds[reference_round - 1][REFERENCE]
                ],
                "terminal_size": 0,
            }
        )

    compact = [
        (
            row["mask"],
            row["initial_size"],
            row["round_sizes"],
            row["reference_deletion_round"],
            row["reference_fatal_attack"],
        )
        for row in rows
    ]
    expected = [
        (0, 28, [13, 13, 2], 2, "x1"),
        (1, 29, [11, 15, 3], 3, "x1"),
        (2, 29, [11, 12, 6], 2, "x1"),
        (3, 30, [10, 12, 8], 3, "x1"),
        (4, 29, [11, 12, 6], 2, "x2"),
        (5, 30, [9, 12, 9], 3, "x2"),
        (6, 30, [9, 7, 8, 6], 3, "x1"),
        (7, 31, [8, 7, 8, 8], 4, "x1"),
        (8, 29, [11, 15, 3], 3, "x1"),
        (9, 30, [9, 17, 4], 3, "x1"),
        (10, 30, [9, 12, 9], 3, "x1"),
        (11, 31, [8, 14, 9], 3, "x1"),
        (12, 30, [10, 12, 8], 3, "x2"),
        (13, 31, [8, 14, 9], 3, "x2"),
        (14, 31, [8, 7, 8, 8], 4, "x1"),
        (15, 32, [7, 9, 8, 8], 4, "x1"),
        (16, 29, [10, 13, 6], 2, "x1"),
        (17, 30, [8, 15, 7], 3, "x1"),
        (18, 30, [8, 9, 6, 5, 2], 2, "x1"),
        (19, 31, [7, 10, 6, 6, 2], 3, "x1"),
        (20, 30, [8, 8, 10, 4], 4, "x0"),
        (21, 31, [6, 11, 10, 4], 4, "x0"),
        (22, 31, [6, 3, 2, 6, 4, 6, 4], 5, "x1"),
        (23, 32, [5, 5, 2, 6, 4, 6, 4], 5, "x1"),
        (24, 29, [9, 11, 9], 3, "x1"),
        (25, 30, [6, 13, 10, 1], 4, "x0"),
        (26, 30, [7, 8, 5, 6, 4], 3, "x1"),
        (27, 31, [5, 9, 6, 6, 5], 4, "x0"),
        (28, 30, [8, 8, 10, 4], 4, "x0"),
        (29, 31, [5, 12, 10, 4], 4, "x0"),
        (30, 31, [6, 3, 2, 6, 4, 6, 4], 5, "x1"),
        (31, 32, [4, 6, 2, 6, 4, 6, 4], 5, "x1"),
    ]
    if compact != expected:
        raise AssertionError(("core trace mismatch", compact))

    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return {
        "order": ORDER,
        "fixed_graph_edges": sorted(sorted(edge) for edge in FIXED_GRAPH_EDGES),
        "fixed_graph_nonedges": sorted(
            sorted(edge) for edge in FIXED_GRAPH_NONEDGES
        ),
        "optional_graph_edges_in_bit_order": [
            sorted(edge) for edge in OPTIONAL_GRAPH_EDGES
        ],
        "pair_partition": {
            "fixed_edges": len(FIXED_GRAPH_EDGES),
            "fixed_nonedges": len(FIXED_GRAPH_NONEDGES),
            "optional": len(OPTIONAL_GRAPH_EDGES),
            "total": len(decided),
        },
        "completion_count": len(rows),
        "all_terminal_kernels_empty": True,
        "rows_sha256": hashlib.sha256(encoded).hexdigest(),
        "rows": rows,
    }


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(character) - 63 for character in record.strip()]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only short graph6 records are supported")
    order = values[0]
    slots = order * (order - 1) // 2
    bits: list[int] = []
    for value in values[1:]:
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < slots:
        raise ValueError("truncated graph6 record")
    edges = []
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.append(Edge((low, high)))
            cursor += 1
    return neighborhoods(order, frozenset(edges))


def all_states(order: int, size: int) -> tuple[State, ...]:
    return tuple(frozenset(state) for state in combinations(range(order), size))


def greatest_family(
    adjacency: tuple[frozenset[int], ...],
    size: int,
    banned: frozenset[State] = frozenset(),
) -> frozenset[State]:
    active = {
        state
        for state in all_states(len(adjacency), size)
        if state not in banned and dominates(state, adjacency)
    }
    while True:
        doomed = set()
        for state in active:
            for attacked in range(len(adjacency)):
                if attacked in state:
                    continue
                if not any(
                    attacked in adjacency[guard]
                    and frozenset((state - {guard}) | {attacked}) in active
                    for guard in state
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return frozenset(active)
        active.difference_update(doomed)


def response_lists(
    adjacency: tuple[frozenset[int], ...],
    family: frozenset[State],
    reference: State,
) -> dict[int, frozenset[int]]:
    result = {}
    for vertex in range(len(adjacency)):
        if vertex in reference:
            continue
        result[vertex] = frozenset(
            anchor
            for anchor in reference
            if vertex in adjacency[anchor]
            and frozenset((reference - {anchor}) | {vertex}) in family
        )
    return result


def static_lists(
    adjacency: tuple[frozenset[int], ...],
    reference: State,
) -> dict[int, frozenset[int]]:
    result = {}
    for vertex in range(len(adjacency)):
        if vertex in reference:
            continue
        result[vertex] = frozenset(
            anchor
            for anchor in reference
            if vertex in adjacency[anchor]
            and dominates(
                frozenset((reference - {anchor}) | {vertex}),
                adjacency,
            )
        )
    return result


def domination_number(adjacency: tuple[frozenset[int], ...]) -> int:
    for size in range(len(adjacency) + 1):
        if any(dominates(state, adjacency)
               for state in all_states(len(adjacency), size)):
            return size
    raise AssertionError


def independence_number(adjacency: tuple[frozenset[int], ...]) -> int:
    for size in range(len(adjacency), -1, -1):
        if any(independent(state, adjacency)
               for state in all_states(len(adjacency), size)):
            return size
    raise AssertionError


def independent_domination_number(
    adjacency: tuple[frozenset[int], ...],
) -> int:
    for size in range(len(adjacency) + 1):
        if any(
            independent(state, adjacency) and dominates(state, adjacency)
            for state in all_states(len(adjacency), size)
        ):
            return size
    raise AssertionError


def eternal_domination_number(
    adjacency: tuple[frozenset[int], ...],
) -> int:
    for size in range(1, len(adjacency) + 1):
        if greatest_family(adjacency, size):
            return size
    raise AssertionError


def clique_cover_number(adjacency: tuple[frozenset[int], ...]) -> int:
    vertices = frozenset(range(len(adjacency)))
    cliques = {
        state
        for size in range(1, len(adjacency) + 1)
        for state in all_states(len(adjacency), size)
        if all(second in adjacency[first]
               for first, second in combinations(sorted(state), 2))
    }
    memo: dict[frozenset[int], int] = {frozenset(): 0}

    def cover(remaining: frozenset[int]) -> int:
        if remaining in memo:
            return memo[remaining]
        pivot = min(remaining)
        value = len(remaining)
        for clique in cliques:
            if pivot in clique and clique <= remaining:
                value = min(value, 1 + cover(remaining - clique))
        memo[remaining] = value
        return value

    return cover(vertices)


def parameters(adjacency: tuple[frozenset[int], ...]) -> dict[str, int]:
    return {
        "gamma": domination_number(adjacency),
        "i": independent_domination_number(adjacency),
        "alpha": independence_number(adjacency),
        "gamma_infinity": eternal_domination_number(adjacency),
        "theta": clique_cover_number(adjacency),
    }


def verify_fdzro() -> dict[str, object]:
    adjacency = decode_graph6("FDzro")
    reference = frozenset((0, 1, 2))
    target_lists = {
        3: frozenset((0,)),
        4: frozenset((0, 2)),
        5: frozenset((1, 2)),
        6: frozenset((1,)),
    }
    banned = frozenset(
        frozenset((reference - {anchor}) | {vertex})
        for vertex, allowed in target_lists.items()
        for anchor in reference - allowed
    )
    family = greatest_family(adjacency, 3, banned)
    lists = response_lists(adjacency, family, reference)
    stat = static_lists(adjacency, reference)
    expected_static = {
        3: frozenset((0, 2)),
        4: frozenset((0, 1, 2)),
        5: frozenset((0, 1, 2)),
        6: frozenset((1, 2)),
    }
    if len(family) != 21 or lists != target_lists or stat != expected_static:
        raise AssertionError(
            ("FDzro control mismatch", len(family), lists, stat)
        )
    exact_parameters = parameters(adjacency)
    if exact_parameters != {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(exact_parameters)
    return {
        "graph6": "FDzro",
        "parameters": exact_parameters,
        "constrained_family_size": len(family),
        "family_lists": {
            str(vertex): sorted(values) for vertex, values in lists.items()
        },
        "static_lists": {
            str(vertex): sorted(values) for vertex, values in stat.items()
        },
        "interpretation": (
            "Exact family mixed-P4 is possible at gamma two, but the "
            "endpoint and internal static lists are strictly larger."
        ),
    }


def verify_hcoce_ry() -> dict[str, object]:
    adjacency = decode_graph6("HCOceRy")
    reference = frozenset((0, 1, 2))
    family = greatest_family(adjacency, 3)
    lists = response_lists(adjacency, family, reference)
    exact_parameters = parameters(adjacency)
    if exact_parameters != {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(exact_parameters)
    if len(family) != 24:
        raise AssertionError(len(family))
    for defect in (3, 6):
        if lists[defect] != frozenset((0,)):
            raise AssertionError((defect, lists[defect]))
        if {
            anchor
            for anchor in reference
            if anchor not in adjacency[defect]
        } != {1, 2}:
            raise AssertionError(("anchor signature", defect))
    if 6 not in adjacency[3]:
        raise AssertionError("the two pure singleton vertices are not adjacent")
    return {
        "graph6": "HCOceRy",
        "parameters": exact_parameters,
        "greatest_family_size": len(family),
        "reference": sorted(reference),
        "pure_same_color_singletons": [3, 6],
        "singleton_list": [0],
        "missed_anchors": [1, 2],
        "singletons_adjacent_in_G": True,
        "interpretation": (
            "A same-color pure singleton clique is compatible with full "
            "equality; the mixed-P4 incidences are essential."
        ),
    }


def main() -> None:
    result = {
        "schema": "mixed-p4-one-defect-local-kernel-v1",
        "model": (
            "one guard moves along one graph edge to an unoccupied "
            "attacked vertex"
        ),
        "core": verify_core(),
        "gamma2_family_static_boundary": verify_fdzro(),
        "equality_singleton_boundary": verify_hcoce_ry(),
        "verdict": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()

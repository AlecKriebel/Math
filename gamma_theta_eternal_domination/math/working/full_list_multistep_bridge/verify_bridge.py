#!/usr/bin/env python3
"""Exact replay for the two-step full-target spoke theorem and controls.

This checker is deliberately self-contained.  It uses ordinary Python sets
and imports no campaign search or game implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


Graph = tuple[frozenset[int], ...]
State = frozenset[int]


CONTROLS = (
    {
        "name": "C123_static_control",
        "graph6": "IxU[ISrXW",
        "target": 9,
        "root": (1, 5, 8),
        "expected_B": (0, 3, 4, 6),
        "expected_kernel_size": 0,
        "expected_root_rank": 2,
    },
    {
        "name": "C128_gamma3_static_control",
        "graph6": "KxU[ISrR}NP^",
        "target": 11,
        "root": (0, 4, 8),
        "expected_B": (1, 2, 3, 5),
        "expected_kernel_size": 0,
        "expected_root_rank": 3,
    },
    {
        "name": "exact_equality_control",
        "graph6": r"Ksv`f\knJVis",
        "target": 0,
        "root": (1, 2, 3),
        "expected_B": (6, 8, 10, 11),
        "expected_kernel_size": 127,
        "expected_root_rank": None,
    },
)


def decode_graph6(record: str) -> Graph:
    raw = record.encode("ascii")
    if not raw or raw[0] == 126:
        raise AssertionError("checker expects short graph6")
    order = raw[0] - 63
    bit_count = order * (order - 1) // 2
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise AssertionError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(raw) != 1 + (bit_count + 5) // 6 or any(bits[bit_count:]):
        raise AssertionError("noncanonical short graph6 payload")
    rows = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low].add(high)
                rows[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in rows)


def complement(graph: Graph) -> Graph:
    universe = set(range(len(graph)))
    return tuple(
        frozenset(universe - {vertex} - set(graph[vertex]))
        for vertex in range(len(graph))
    )


def subsets(order: int, size: int):
    yield from (
        frozenset(group)
        for group in itertools.combinations(range(order), size)
    )


def independent(graph: Graph, state: State) -> bool:
    return all(graph[v].isdisjoint(state - {v}) for v in state)


def dominates(graph: Graph, state: State) -> bool:
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def greatest_family(
    graph: Graph, size: int
) -> tuple[frozenset[State], dict[State, int], list[int]]:
    family = {
        state
        for state in subsets(len(graph), size)
        if dominates(graph, state)
    }
    ranks: dict[State, int] = {}
    removed_per_round: list[int] = []
    round_number = 0
    while True:
        deleted: list[State] = []
        for state in family:
            for attack in range(len(graph)):
                if attack in state:
                    continue
                if not any(
                    attack in graph[guard]
                    and (state - {guard}) | {attack} in family
                    for guard in state
                ):
                    deleted.append(state)
                    break
        if not deleted:
            return frozenset(family), ranks, removed_per_round
        round_number += 1
        removed_per_round.append(len(deleted))
        for state in deleted:
            family.remove(state)
            ranks[state] = round_number


def components(graph: Graph, vertices: frozenset[int]) -> list[frozenset[int]]:
    unseen = set(vertices)
    answer: list[frozenset[int]] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        found = {start}
        queue = deque((start,))
        while queue:
            vertex = queue.popleft()
            for other in sorted(graph[vertex] & unseen):
                unseen.remove(other)
                found.add(other)
                queue.append(other)
        answer.append(frozenset(found))
    return sorted(answer, key=lambda part: tuple(sorted(part)))


def legal_dominating_successors(
    graph: Graph, state: State, attack: int
) -> list[dict[str, object]]:
    answer = []
    for guard in sorted(state):
        successor = (state - {guard}) | {attack}
        if attack in graph[guard] and dominates(graph, successor):
            answer.append(
                {"guard": guard, "successor": sorted(successor)}
            )
    return answer


def response_truth_table() -> list[dict[str, object]]:
    """Exhaust the abstract second-attack response choices."""

    rows = []
    anchors = frozenset(range(3))
    incidence_types = (frozenset(),) + tuple(
        frozenset((index,)) for index in range(3)
    )
    for blocked in incidence_types:
        accepted = []
        for palette_size in range(4):
            for palette in itertools.combinations(range(3), palette_size):
                retained = frozenset(palette)
                closes = True
                for removed in range(3):
                    present = anchors - {removed}
                    possible = False
                    for moving in present:
                        stationary = next(iter(present - {moving}))
                        if moving not in blocked and stationary in retained:
                            possible = True
                    if not possible:
                        closes = False
                        break
                predicted = (
                    len(retained) >= 2
                    and (not blocked or blocked <= retained)
                )
                if closes != predicted:
                    raise AssertionError("truth-table characterization failed")
                if closes:
                    accepted.append(sorted(retained))
        rows.append(
            {
                "blocked_anchor_indices": sorted(blocked),
                "accepted_retained_palettes": accepted,
            }
        )
    return rows


def analyze_control(specification: dict[str, object]) -> dict[str, object]:
    graph = decode_graph6(str(specification["graph6"]))
    h = complement(graph)
    target = int(specification["target"])
    root = frozenset(int(v) for v in specification["root"])
    assert independent(graph, root)
    assert target not in root
    assert all(target in graph[anchor] for anchor in root)

    target_successors = {
        anchor: (root - {anchor}) | {target}
        for anchor in root
    }
    assert all(dominates(graph, state) for state in target_successors.values())

    deletion = frozenset(range(len(graph))) - {target}
    physical = frozenset(
        vertex for vertex in deletion if target not in graph[vertex]
    )
    assert tuple(sorted(physical)) == tuple(specification["expected_B"])

    spokes = {
        anchor: frozenset(physical & h[anchor])
        for anchor in sorted(root)
    }
    assert all(
        len([anchor for anchor in root if vertex in spokes[anchor]]) <= 1
        for vertex in physical
    )
    anchorless = physical - frozenset().union(*spokes.values())

    dominating_palettes: dict[int, frozenset[int]] = {}
    for vertex in sorted(physical):
        palette = frozenset(
            anchor
            for anchor in root
            if dominates(graph, frozenset((target, anchor, vertex)))
        )
        dominating_palettes[vertex] = palette
        for anchor in root:
            no_spoke_neighbor = not (h[vertex] & spokes[anchor])
            state_dominates = anchor in palette
            if no_spoke_neighbor != state_dominates:
                raise AssertionError("domination/spoke equivalence failed")

    second_attack_failures = []
    for removed, state in sorted(target_successors.items()):
        for attack in sorted(physical):
            replies = legal_dominating_successors(graph, state, attack)
            if not replies:
                second_attack_failures.append(
                    {
                        "first_move_guard_to_target": removed,
                        "state": sorted(state),
                        "second_attack": attack,
                    }
                )

    family, ranks, removed_per_round = greatest_family(graph, 3)
    assert len(family) == int(specification["expected_kernel_size"])
    expected_root_rank = specification["expected_root_rank"]
    if expected_root_rank is None:
        assert root in family
    else:
        assert ranks[root] == int(expected_root_rank)

    retained_palettes = {
        vertex: frozenset(
            anchor
            for anchor in root
            if frozenset((target, anchor, vertex)) in family
        )
        for vertex in physical
    }

    component_records = []
    for component in components(h, physical):
        signature = sorted(
            anchor
            for anchor in root
            if component & spokes[anchor]
        )
        component_records.append(
            {
                "vertices": sorted(component),
                "spoke_signature": signature,
                "edges": [
                    [u, v]
                    for u, v in itertools.combinations(sorted(component), 2)
                    if v in h[u]
                ],
            }
        )

    if family:
        assert not second_attack_failures
        for vertex in physical:
            palette = retained_palettes[vertex]
            own = frozenset(
                anchor for anchor in root if vertex in spokes[anchor]
            )
            assert len(palette) >= 2
            assert own <= palette <= dominating_palettes[vertex]
            for anchor in palette:
                assert not (h[vertex] & spokes[anchor])

    return {
        "name": specification["name"],
        "graph6": specification["graph6"],
        "order": len(graph),
        "target": target,
        "root": sorted(root),
        "physical_inactive_B": sorted(physical),
        "spokes": {
            str(anchor): sorted(spokes[anchor]) for anchor in sorted(root)
        },
        "anchorless_B_star": sorted(anchorless),
        "H_B_edges": [
            [u, v]
            for u, v in itertools.combinations(sorted(physical), 2)
            if v in h[u]
        ],
        "dominating_palettes_Q": {
            str(vertex): sorted(dominating_palettes[vertex])
            for vertex in sorted(physical)
        },
        "retained_palettes_P": {
            str(vertex): sorted(retained_palettes[vertex])
            for vertex in sorted(physical)
        },
        "second_attack_failures_from_full_root": second_attack_failures,
        "kernel_size_k3": len(family),
        "kernel_removed_per_round": removed_per_round,
        "root_deletion_rank": ranks.get(root),
        "H_B_components": component_records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    controls = [analyze_control(specification) for specification in CONTROLS]
    by_name = {record["name"]: record for record in controls}

    c123 = by_name["C123_static_control"]
    assert c123["spokes"] == {
        "1": [3, 6],
        "5": [],
        "8": [0, 4],
    }
    assert [3, 6] in c123["H_B_edges"]
    assert [0, 4] in c123["H_B_edges"]

    c128 = by_name["C128_gamma3_static_control"]
    assert c128["spokes"] == {
        "0": [3],
        "4": [2],
        "8": [1, 5],
    }
    assert c128["dominating_palettes_Q"]["1"] == [4]
    assert c128["dominating_palettes_Q"]["5"] == [0]
    assert c128["second_attack_failures_from_full_root"] == [
        {
            "first_move_guard_to_target": 0,
            "state": [4, 8, 11],
            "second_attack": 1,
        },
        {
            "first_move_guard_to_target": 0,
            "state": [4, 8, 11],
            "second_attack": 5,
        },
        {
            "first_move_guard_to_target": 4,
            "state": [0, 8, 11],
            "second_attack": 1,
        },
        {
            "first_move_guard_to_target": 4,
            "state": [0, 8, 11],
            "second_attack": 5,
        },
    ]

    equality = by_name["exact_equality_control"]
    assert equality["spokes"] == {
        "1": [6],
        "2": [11],
        "3": [8, 10],
    }
    assert equality["retained_palettes_P"] == {
        "6": [1, 2],
        "8": [2, 3],
        "10": [1, 3],
        "11": [1, 2],
    }
    assert equality["H_B_components"] == [
        {
            "vertices": [6, 8],
            "spoke_signature": [1, 3],
            "edges": [[6, 8]],
        },
        {
            "vertices": [10, 11],
            "spoke_signature": [2, 3],
            "edges": [[10, 11]],
        },
    ]

    result = {
        "schema": "full-list-multistep-bridge-verification-v1",
        "verdict": "PASS",
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one G-edge",
            "retained_states": "every retained state dominates G",
        },
        "abstract_response_truth_table": response_truth_table(),
        "controls": controls,
        "claim_boundary": {
            "two_step_spoke_theorem_verified": True,
            "C123_rejected_by_the_new_condition": True,
            "C128_rejected_by_the_new_condition": True,
            "exact_equality_control_satisfies_the_new_condition": True,
            "full_list_branch_resolved": False,
            "gamma_theta_conjecture_resolved": False,
        },
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()


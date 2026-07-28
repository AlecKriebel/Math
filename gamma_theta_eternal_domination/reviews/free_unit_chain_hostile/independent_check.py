#!/usr/bin/env python3
"""Clean-room audit of the FCZbg free-singleton control.

This file intentionally imports no campaign code and reads no candidate
control file.  It uses explicit edge data, set-based graph operations,
complete subset/partition searches, and a separately written greatest
fixed-point computation.
"""

from __future__ import annotations

from collections import deque
from itertools import combinations
import hashlib
import json


VERTICES = frozenset(range(7))
EDGES = frozenset(
    frozenset(edge)
    for edge in (
        (0, 3),
        (1, 4),
        (2, 4),
        (0, 5),
        (1, 5),
        (2, 5),
        (1, 6),
        (2, 6),
        (3, 6),
        (5, 6),
    )
)
REFERENCE = frozenset((3, 4, 5))


def edge(left: int, right: int) -> bool:
    return left != right and frozenset((left, right)) in EDGES


def graph6_from_explicit_edges() -> str:
    """Encode the explicit graph using the short graph6 specification."""
    bits = []
    for high in range(1, len(VERTICES)):
        for low in range(high):
            bits.append(1 if edge(low, high) else 0)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(len(VERTICES) + 63) + "".join(payload)


def subsets(size: int):
    return (
        frozenset(choice)
        for choice in combinations(sorted(VERTICES), size)
    )


def dominates(state: frozenset[int], universe=VERTICES) -> bool:
    return all(
        vertex in state or any(edge(guard, vertex) for guard in state)
        for vertex in universe
    )


def independent(state: frozenset[int]) -> bool:
    return all(not edge(left, right) for left, right in combinations(state, 2))


def maximal_independent(state: frozenset[int]) -> bool:
    return independent(state) and all(
        any(edge(vertex, member) for member in state)
        for vertex in VERTICES - state
    )


def minimum_size(predicate) -> tuple[int, tuple[int, ...]]:
    for size in range(1, len(VERTICES) + 1):
        for state in subsets(size):
            if predicate(state):
                return size, tuple(sorted(state))
    raise AssertionError("predicate has no witness")


def maximum_independent() -> tuple[int, tuple[int, ...]]:
    for size in range(len(VERTICES), 0, -1):
        for state in subsets(size):
            if independent(state):
                return size, tuple(sorted(state))
    raise AssertionError("independent set search failed")


def minimum_clique_partition() -> tuple[int, tuple[tuple[int, ...], ...]]:
    """Complete canonical set-partition search, independent of coloring code."""
    best_count = len(VERTICES) + 1
    best_partition: tuple[tuple[int, ...], ...] | None = None
    blocks: list[list[int]] = []

    def extend(vertex: int) -> None:
        nonlocal best_count, best_partition
        if vertex == len(VERTICES):
            if len(blocks) < best_count:
                best_count = len(blocks)
                best_partition = tuple(tuple(block) for block in blocks)
            return
        if len(blocks) >= best_count:
            return
        for block in blocks:
            if all(edge(vertex, member) for member in block):
                block.append(vertex)
                extend(vertex + 1)
                block.pop()
        blocks.append([vertex])
        extend(vertex + 1)
        blocks.pop()

    extend(0)
    if best_partition is None:
        raise AssertionError("partition search failed")
    return best_count, best_partition


def successor(
    state: frozenset[int], guard: int, attacked: int
) -> frozenset[int]:
    return frozenset((state - {guard}) | {attacked})


def greatest_triple_family() -> tuple[frozenset[frozenset[int]], list[int]]:
    current = frozenset(state for state in subsets(3) if dominates(state))
    stage_sizes = [len(current)]
    while True:
        kept = []
        for state in current:
            survives = True
            for attacked in sorted(VERTICES - state):
                responses = [
                    successor(state, guard, attacked)
                    for guard in sorted(state)
                    if edge(guard, attacked)
                ]
                if not any(response in current for response in responses):
                    survives = False
                    break
            if survives:
                kept.append(state)
        updated = frozenset(kept)
        if updated == current:
            return current, stage_sizes
        current = updated
        stage_sizes.append(len(current))


def family_obligations(
    family: frozenset[frozenset[int]],
) -> tuple[int, str]:
    rows = []
    for state in sorted(family, key=lambda item: tuple(sorted(item))):
        assert dominates(state)
        for attacked in sorted(VERTICES - state):
            legal = []
            for guard in sorted(state):
                if not edge(guard, attacked):
                    continue
                target = successor(state, guard, attacked)
                if target in family:
                    assert dominates(target)
                    legal.append(guard)
            assert legal, (state, attacked)
            rows.append([sorted(state), attacked, legal])
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return len(rows), hashlib.sha256(encoded).hexdigest()


def response_lists(
    family: frozenset[frozenset[int]],
) -> dict[int, tuple[int, ...]]:
    answer = {}
    for outside in sorted(VERTICES - REFERENCE):
        retained = []
        for removed in sorted(REFERENCE):
            target = frozenset((REFERENCE - {removed}) | {outside})
            if target in family:
                retained.append(removed)
        assert retained
        answer[outside] = tuple(retained)
    return answer


def static_response_lists() -> dict[int, tuple[int, ...]]:
    """Responses legal and dominating before family membership is imposed."""
    answer = {}
    for outside in sorted(VERTICES - REFERENCE):
        legal = []
        for removed in sorted(REFERENCE):
            target = frozenset((REFERENCE - {removed}) | {outside})
            if edge(removed, outside) and dominates(target):
                legal.append(removed)
        answer[outside] = tuple(legal)
    return answer


def complement_neighbors(vertex: int, universe: frozenset[int]) -> set[int]:
    return {
        other
        for other in universe
        if other != vertex and not edge(vertex, other)
    }


def complement_components(
    universe: frozenset[int],
) -> tuple[list[tuple[int, ...]], dict[int, int], dict[int, int]]:
    unseen = set(universe)
    components = []
    component_of: dict[int, int] = {}
    side: dict[int, int] = {}
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = deque([root])
        side[root] = 0
        members = []
        component_index = len(components)
        while queue:
            vertex = queue.popleft()
            members.append(vertex)
            component_of[vertex] = component_index
            for neighbor in sorted(complement_neighbors(vertex, universe)):
                if neighbor not in side:
                    side[neighbor] = side[vertex] ^ 1
                    unseen.remove(neighbor)
                    queue.append(neighbor)
                else:
                    assert side[neighbor] != side[vertex]
        components.append(tuple(sorted(members)))
    return components, component_of, side


def projected_family_audit(
    frozen: int,
    family: frozenset[frozenset[int]],
    lists: dict[int, tuple[int, ...]],
) -> dict[str, object]:
    anchors = REFERENCE - {frozen}
    universe = frozenset(
        set(anchors)
        | {
            vertex
            for vertex in VERTICES - REFERENCE
            if frozen not in lists[vertex]
        }
    )
    pairs = frozenset(
        state - {frozen}
        for state in family
        if frozen in state and state - {frozen} <= universe
    )
    for pair in pairs:
        assert len(pair) == 2
        assert dominates(pair, universe)
        for attacked in sorted(universe - pair):
            retained_responses = [
                successor(pair, guard, attacked)
                for guard in sorted(pair)
                if edge(guard, attacked)
                and successor(pair, guard, attacked) in pairs
            ]
            assert retained_responses, (frozen, pair, attacked)

    components, component_of, side = complement_components(universe)
    anchor_list = sorted(anchors)
    assert not edge(anchor_list[0], anchor_list[1])
    anchor_component = component_of[anchor_list[0]]
    assert component_of[anchor_list[1]] == anchor_component

    return {
        "universe": universe,
        "pairs": pairs,
        "components": components,
        "component_of": component_of,
        "side": side,
        "anchor_component": anchor_component,
    }


def free_singleton_audit(
    family: frozenset[frozenset[int]],
    lists: dict[int, tuple[int, ...]],
    projections: dict[int, dict[str, object]],
) -> tuple[list[dict[str, object]], set[tuple[int, int, int]]]:
    incidences = []
    lifted = set()
    for marker, marker_list in sorted(lists.items()):
        if len(marker_list) != 1:
            continue
        demanded = marker_list[0]
        for frozen in sorted(REFERENCE - {demanded}):
            projection = projections[frozen]
            component_of = projection["component_of"]
            component_index = component_of[marker]
            if component_index == projection["anchor_component"]:
                continue
            members = projection["components"][component_index]
            marker_side = projection["side"][marker]
            other_anchor = next(
                anchor
                for anchor in REFERENCE
                if anchor not in {frozen, demanded}
            )

            for vertex in members:
                required = (
                    demanded
                    if projection["side"][vertex] == marker_side
                    else other_anchor
                )
                assert required in lists[vertex]
                if len(lists[vertex]) == 1:
                    assert lists[vertex] == (required,)

            for left, right in combinations(members, 2):
                if edge(left, right):
                    continue
                target = frozenset((frozen, left, right))
                assert target in family
                lifted.add(tuple(sorted(target)))

            incidences.append(
                {
                    "marker": marker,
                    "frozen": frozen,
                    "demanded": demanded,
                    "other_anchor": other_anchor,
                    "component": list(members),
                }
            )
    return incidences, lifted


def connected() -> bool:
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in sorted(VERTICES - reached):
            if edge(vertex, neighbor):
                reached.add(neighbor)
                queue.append(neighbor)
    return reached == set(VERTICES)


def main() -> None:
    assert all(len(item) == 2 for item in EDGES)
    assert graph6_from_explicit_edges() == "FCZbg"
    assert connected()

    gamma, gamma_witness = minimum_size(dominates)
    independent_domination, i_witness = minimum_size(maximal_independent)
    alpha, alpha_witness = maximum_independent()
    theta, theta_witness = minimum_clique_partition()
    family, stage_sizes = greatest_triple_family()
    obligations, obligation_hash = family_obligations(family)
    lists = response_lists(family)
    static_lists = static_response_lists()
    projections = {
        frozen: projected_family_audit(frozen, family, lists)
        for frozen in sorted(REFERENCE)
    }
    incidences, lifted = free_singleton_audit(
        family, lists, projections
    )

    assert (gamma, independent_domination, alpha, theta) == (3, 3, 3, 3)
    assert stage_sizes == [22, 19, 18]
    assert len(family) == 18
    assert obligations == 72
    assert lists == {
        0: (3,),
        1: (4, 5),
        2: (4, 5),
        6: (5,),
    }
    # These strict containments actively test the family/static distinction.
    assert static_lists == {
        0: (3, 5),
        1: (4, 5),
        2: (4, 5),
        6: (3, 5),
    }
    assert incidences == [
        {
            "marker": 0,
            "frozen": 4,
            "demanded": 3,
            "other_anchor": 5,
            "component": [0, 6],
        },
        {
            "marker": 6,
            "frozen": 4,
            "demanded": 5,
            "other_anchor": 3,
            "component": [0, 6],
        },
    ]
    assert lifted == {(0, 4, 6)}

    serialized_family = [
        list(sorted(state))
        for state in sorted(family, key=lambda item: tuple(sorted(item)))
    ]
    result = {
        "schema": "free-unit-chain-hostile-clean-room-v1",
        "graph": {
            "graph6": graph6_from_explicit_edges(),
            "order": len(VERTICES),
            "size": len(EDGES),
            "connected": True,
            "edges": [
                list(sorted(item))
                for item in sorted(EDGES, key=lambda item: tuple(sorted(item)))
            ],
        },
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": gamma,
            "theta": theta,
        },
        "witnesses": {
            "dominating": list(gamma_witness),
            "maximal_independent": list(i_witness),
            "maximum_independent": list(alpha_witness),
            "clique_partition": [list(block) for block in theta_witness],
        },
        "greatest_family": {
            "stage_sizes": stage_sizes,
            "states": serialized_family,
            "state_count": len(family),
            "unoccupied_attack_obligations": obligations,
            "obligation_sha256": obligation_hash,
        },
        "family_response_lists": {
            str(vertex): list(value) for vertex, value in lists.items()
        },
        "static_response_lists": {
            str(vertex): list(value)
            for vertex, value in static_lists.items()
        },
        "projection_summaries": {
            str(frozen): {
                "universe": sorted(projection["universe"]),
                "pair_count": len(projection["pairs"]),
                "components": [
                    list(component) for component in projection["components"]
                ],
            }
            for frozen, projection in projections.items()
        },
        "free_singleton_incidences": incidences,
        "lifted_component_edges": [list(item) for item in sorted(lifted)],
        "verdict": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()

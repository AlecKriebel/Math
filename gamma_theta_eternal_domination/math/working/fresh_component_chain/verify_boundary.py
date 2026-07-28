#!/usr/bin/env python3
"""Standalone checker for the separated no-full singleton lollipop control."""

from __future__ import annotations

import hashlib
import itertools
import json


N = 9
ANCHORS = frozenset((0, 1, 2))
X, P0, MID, P1, Q0, Q1 = 3, 4, 5, 6, 7, 8
H_EDGES = frozenset(
    {
        (0, 1),
        (0, 2),
        (1, 2),
        (X, P0),
        (P0, MID),
        (MID, P1),
        (P1, Q1),
        (Q0, Q1),
        (P0, Q0),
    }
)
EXPECTED_LISTS = {
    X: frozenset((0,)),
    P0: frozenset((0, 1)),
    MID: frozenset((0,)),
    P1: frozenset((0, 1)),
    Q0: frozenset((1, 2)),
    Q1: frozenset((1, 2)),
}


def edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def g_adjacent(u: int, v: int) -> bool:
    return u != v and edge(u, v) not in H_EDGES


def dominates(state: frozenset[int]) -> bool:
    return all(
        x in state or any(g_adjacent(x, guard) for guard in state)
        for x in range(N)
    )


def independent(state: frozenset[int]) -> bool:
    return all(
        not g_adjacent(u, v)
        for u, v in itertools.combinations(state, 2)
    )


def maximal_independent(state: frozenset[int]) -> bool:
    return independent(state) and all(
        any(g_adjacent(x, guard) for guard in state)
        for x in set(range(N)) - state
    )


def swap(anchor: int, target: int) -> frozenset[int]:
    return (ANCHORS - {anchor}) | {target}


def restricted_kernel():
    banned = {
        swap(anchor, target)
        for target, allowed in EXPECTED_LISTS.items()
        for anchor in ANCHORS
        if anchor not in allowed
    }
    family = {
        frozenset(choice)
        for choice in itertools.combinations(range(N), 3)
        if frozenset(choice) not in banned
        and dominates(frozenset(choice))
    }
    rounds = []
    while True:
        removed = set()
        for state in family:
            for attack in set(range(N)) - state:
                if not any(
                    g_adjacent(guard, attack)
                    and (state - {guard}) | {attack} in family
                    for guard in state
                ):
                    removed.add(state)
                    break
        if not removed:
            return frozenset(family), tuple(rounds)
        rounds.append(len(removed))
        family.difference_update(removed)


def audit_family(family: frozenset[frozenset[int]]) -> int:
    obligations = 0
    for state in family:
        assert dominates(state)
        for attack in set(range(N)) - state:
            obligations += 1
            assert any(
                g_adjacent(guard, attack)
                and (state - {guard}) | {attack} in family
                for guard in state
            )
    return obligations


def response_lists(family: frozenset[frozenset[int]]):
    return {
        target: frozenset(
            anchor
            for anchor in ANCHORS
            if g_adjacent(anchor, target)
            and swap(anchor, target) in family
        )
        for target in set(range(N)) - ANCHORS
    }


def minimum_size(predicate) -> int:
    for size in range(1, N + 1):
        if any(
            predicate(frozenset(choice))
            for choice in itertools.combinations(range(N), size)
        ):
            return size
    raise AssertionError("finite search exhausted")


def alpha() -> int:
    for size in range(N, 0, -1):
        if any(
            independent(frozenset(choice))
            for choice in itertools.combinations(range(N), size)
        ):
            return size
    raise AssertionError("empty graph universe")


def theta() -> int:
    neighbors = {
        x: {y for y in range(N) if edge(x, y) in H_EDGES}
        for x in range(N)
    }
    order = sorted(range(N), key=lambda x: (-len(neighbors[x]), x))
    for color_count in range(1, N + 1):
        assigned: dict[int, int] = {}

        def visit(index: int) -> bool:
            if index == N:
                return True
            x = order[index]
            used = {
                assigned[y] for y in neighbors[x] if y in assigned
            }
            for color in range(color_count):
                if color in used:
                    continue
                assigned[x] = color
                if visit(index + 1):
                    return True
                del assigned[x]
            return False

        if visit(0):
            return color_count
    raise AssertionError("color search exhausted")


def encode_graph6() -> str:
    bits = [
        int(g_adjacent(low, high))
        for high in range(1, N)
        for low in range(high)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(N + 63) + "".join(payload)


def family_hash(family: frozenset[frozenset[int]]) -> str:
    serialized = "\n".join(
        " ".join(map(str, sorted(state)))
        for state in sorted(family, key=lambda state: tuple(sorted(state)))
    ) + "\n"
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def main() -> None:
    assert encode_graph6() == "HFzvvn{"
    family, rounds = restricted_kernel()
    assert ANCHORS in family
    assert len(family) == 52
    assert rounds == (15, 4, 4)
    obligations = audit_family(family)
    assert obligations == 52 * (N - 3) == 312
    lists = response_lists(family)
    assert lists == EXPECTED_LISTS

    gamma = minimum_size(dominates)
    independent_domination = minimum_size(maximal_independent)
    independence = alpha()
    clique_cover = theta()
    assert (gamma, independent_domination, independence, clique_cover) == (
        2,
        2,
        3,
        3,
    )
    # The displayed eternal triple-family proves gamma_infinity <= 3, and
    # alpha <= gamma_infinity gives the reverse inequality.
    gamma_infinity = 3

    # Exact physical two-component lollipop.
    assert all(edge(*item) in H_EDGES for item in ((3, 4), (4, 5), (5, 6)))
    assert all(edge(*item) in H_EDGES for item in ((7, 8), (4, 7), (6, 8)))
    assert edge(4, 6) not in H_EDGES
    assert lists[3] == lists[5] == frozenset((0,))
    assert lists[4] == lists[6] == frozenset((0, 1))
    assert lists[7] == lists[8] == frozenset((1, 2))

    # The singleton pins force ports 4 and 6 to color 1.  The first cross
    # edge then forces 7 to color 2, the edge 7-8 forces 8 to color 1,
    # and the returning edge 6-8 is monochromatic.  Enumerate all allowed
    # colorings to check the contradiction without trusting that trace.
    allowed = dict(lists)
    assigned = {anchor: anchor for anchor in ANCHORS}
    coloring_count = 0

    def extend(index: int) -> None:
        nonlocal coloring_count
        outside = tuple(sorted(set(range(N)) - ANCHORS))
        if index == len(outside):
            coloring_count += 1
            return
        x = outside[index]
        for color in allowed[x]:
            if any(
                edge(x, y) in H_EDGES and assigned[y] == color
                for y in assigned
            ):
                continue
            assigned[x] = color
            extend(index + 1)
            del assigned[x]

    extend(0)
    assert coloring_count == 0

    # Each separated source is individually C-079-exposed for frozen color
    # 0, yet the two sources see opposite sides of the target component.
    exposed_mates = {
        P0: tuple(
            p
            for p, values in lists.items()
            if p != P0 and 0 in values and edge(p, P0) in H_EDGES
        ),
        P1: tuple(
            p
            for p, values in lists.items()
            if p != P1 and 0 in values and edge(p, P1) in H_EDGES
        ),
    }
    assert exposed_mates[P0] == (3, 5)
    assert exposed_mates[P1] == (5,)
    assert edge(P0, Q0) in H_EDGES and edge(P0, Q1) not in H_EDGES
    assert edge(P1, Q1) in H_EDGES and edge(P1, Q0) not in H_EDGES

    dominating_pairs = [
        list(choice)
        for choice in itertools.combinations(range(N), 2)
        if dominates(frozenset(choice))
    ]
    result = {
        "schema": "fresh-component-chain-boundary-v1",
        "status": "PASS",
        "classification": "EXACT_GAMMA_TWO_BOUNDARY",
        "graph6": "HFzvvn{",
        "order": N,
        "size": sum(
            g_adjacent(u, v)
            for u, v in itertools.combinations(range(N), 2)
        ),
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": independence,
            "gamma_infinity": gamma_infinity,
            "theta": clique_cover,
        },
        "family_size": len(family),
        "family_sha256": family_hash(family),
        "kernel_deletion_rounds": list(rounds),
        "attack_obligations": obligations,
        "response_lists": {
            str(x): sorted(values) for x, values in sorted(lists.items())
        },
        "unit_component_path": [3, 4, 5, 6],
        "target_component_path": [7, 8],
        "cross_clause_edges": [[4, 7], [6, 8]],
        "forced_color_trace": {
            "3": 0,
            "4": 1,
            "7": 2,
            "8": 1,
            "6": 1,
            "terminal_collision_edge": [6, 8],
        },
        "compatible_response_colorings": coloring_count,
        "exposed_positive_mates": {
            str(x): list(values) for x, values in exposed_mates.items()
        },
        "dominating_pair_count": len(dominating_pairs),
        "first_dominating_pairs": dominating_pairs[:10],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Standalone checker for the equality cross-hub side-choice control."""

from __future__ import annotations

import itertools
import json


GRAPH6 = "HEhbtjK"
REFERENCE = frozenset((0, 1, 2))


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    values = [ord(char) - 63 for char in record]
    n = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return n, tuple(adjacency)


N, ADJACENCY = decode_graph6(GRAPH6)
ALL = (1 << N) - 1


def mask(choice) -> int:
    return sum(1 << x for x in choice)


def vertices(state: int):
    return tuple(x for x in range(N) if state >> x & 1)


def dominates(state: int) -> bool:
    covered = state
    for x in vertices(state):
        covered |= ADJACENCY[x]
    return covered == ALL


def independent(state: int) -> bool:
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        if ADJACENCY[bit.bit_length() - 1] & scan:
            return False
    return True


def greatest_family() -> set[int]:
    family = {
        mask(choice)
        for choice in itertools.combinations(range(N), 3)
        if dominates(mask(choice))
    }
    while True:
        removed = set()
        for state in family:
            for attack in range(N):
                if state >> attack & 1:
                    continue
                if not any(
                    ADJACENCY[guard] >> attack & 1
                    and ((state ^ (1 << guard)) | (1 << attack)) in family
                    for guard in vertices(state)
                ):
                    removed.add(state)
                    break
        if not removed:
            return family
        family.difference_update(removed)


def family_audit(family: set[int]) -> int:
    obligations = 0
    for state in family:
        assert dominates(state)
        for attack in range(N):
            if state >> attack & 1:
                continue
            obligations += 1
            assert any(
                ADJACENCY[guard] >> attack & 1
                and ((state ^ (1 << guard)) | (1 << attack)) in family
                for guard in vertices(state)
            )
    return obligations


def response_lists(family: set[int]):
    reference = mask(REFERENCE)
    return {
        x: frozenset(
            a
            for a in REFERENCE
            if ADJACENCY[x] >> a & 1
            and ((reference ^ (1 << a)) | (1 << x)) in family
        )
        for x in set(range(N)) - REFERENCE
    }


def minimum_size(predicate) -> int:
    for size in range(1, N + 1):
        if any(
            predicate(mask(choice))
            for choice in itertools.combinations(range(N), size)
        ):
            return size
    raise AssertionError("search exhausted")


def alpha() -> int:
    for size in range(N, 0, -1):
        if any(
            independent(mask(choice))
            for choice in itertools.combinations(range(N), size)
        ):
            return size
    raise AssertionError("search exhausted")


def maximal_independent(state: int) -> bool:
    return independent(state) and dominates(state)


def theta() -> int:
    h_neighbors = {
        x: {
            y
            for y in range(N)
            if y != x and not (ADJACENCY[x] >> y & 1)
        }
        for x in range(N)
    }
    order = sorted(range(N), key=lambda x: (-len(h_neighbors[x]), x))
    for count in range(1, N + 1):
        assigned: dict[int, int] = {}

        def visit(index: int) -> bool:
            if index == N:
                return True
            x = order[index]
            blocked = {
                assigned[y] for y in h_neighbors[x] if y in assigned
            }
            for color in range(count):
                if color in blocked:
                    continue
                assigned[x] = color
                if visit(index + 1):
                    return True
                del assigned[x]
            return False

        if visit(0):
            return count
    raise AssertionError("color search exhausted")


def h_edge(u: int, v: int) -> bool:
    return u != v and not (ADJACENCY[u] >> v & 1)


def main() -> None:
    assert N == 9
    family = greatest_family()
    assert len(family) == 48
    obligations = family_audit(family)
    assert obligations == 288
    lists = response_lists(family)
    assert lists == {
        3: frozenset((0, 1)),
        4: frozenset((0, 2)),
        5: frozenset((1, 2)),
        6: frozenset((1, 2)),
        7: frozenset((0, 2)),
        8: frozenset((0, 1)),
    }

    parameters = {
        "gamma": minimum_size(dominates),
        "i": minimum_size(maximal_independent),
        "alpha": alpha(),
        "gamma_infinity": 3,
        "theta": theta(),
    }
    assert parameters == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }

    # Frozen color 0 target component: 5--6.  Same-list sources 3 and 8
    # see opposite sides through the two cross clauses 3--5 and 8--6.
    assert h_edge(5, 6)
    assert h_edge(3, 5) and not h_edge(3, 6)
    assert h_edge(8, 6) and not h_edge(8, 5)
    assert lists[3] == lists[8] == frozenset((0, 1))
    assert h_edge(3, 8)

    exposed = {
        source: [
            p
            for p, values in sorted(lists.items())
            if p != source and 0 in values and h_edge(p, source)
        ]
        for source in (3, 8)
    }
    assert exposed == {3: [4, 8], 8: [3, 7]}

    result = {
        "schema": "fresh-component-cross-hub-equality-control-v1",
        "status": "PASS",
        "classification": "EXACT_EQUALITY_CONTROL_STRICT_SCOPE",
        "graph6": GRAPH6,
        "parameters": parameters,
        "family_size": len(family),
        "attack_obligations": obligations,
        "reference": sorted(REFERENCE),
        "response_lists": {
            str(x): sorted(values) for x, values in sorted(lists.items())
        },
        "frozen_color": 0,
        "target_component_edge": [5, 6],
        "same_list_sources": [3, 8],
        "source_to_opposite_side_edges": [[3, 5], [8, 6]],
        "source_component_edge": [3, 8],
        "exposed_positive_mates": {
            str(x): values for x, values in exposed.items()
        },
        "scope": (
            "refutes cross-hub side synchronization only; the source edge "
            "forces opposite source colors, so this is not an active "
            "same-color lollipop return"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

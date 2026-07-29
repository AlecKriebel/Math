#!/usr/bin/env python3
"""Standalone exact audit for the global completion transport lemma."""

from __future__ import annotations

import itertools
import json
from collections import Counter


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def mask(items) -> int:
    value = 0
    for item in items:
        value |= 1 << item
    return value


def members(state: int):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def subsets(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield mask(choice)


def adjacency_from_code(order: int, code: int) -> tuple[int, ...]:
    adjacency = [0] * order
    for index, (left, right) in enumerate(
        itertools.combinations(range(order), 2)
    ):
        if code & (1 << index):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return tuple(adjacency)


def decode_graph6(record: str) -> tuple[int, ...]:
    values = [ord(character) - 63 for character in record]
    require(values and 0 <= values[0] <= 62, "short graph6 only")
    order = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return tuple(adjacency)


def adjacent(adjacency: tuple[int, ...], left: int, right: int) -> bool:
    return bool(adjacency[left] & (1 << right))


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(
        not adjacency[vertex] & (state ^ (1 << vertex))
        for vertex in members(state)
    )


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in members(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def greatest_family(adjacency: tuple[int, ...], size: int) -> set[int]:
    family = {
        state
        for state in subsets(len(adjacency), size)
        if dominates(adjacency, state)
    }
    while True:
        removed = set()
        for state in family:
            for target in range(len(adjacency)):
                if state & (1 << target):
                    continue
                if not retained_movers(adjacency, family, state, target):
                    removed.add(state)
                    break
        if not removed:
            return family
        family.difference_update(removed)


def retained_movers(
    adjacency: tuple[int, ...],
    family: set[int],
    state: int,
    target: int,
) -> tuple[int, ...]:
    target_bit = 1 << target
    return tuple(
        guard
        for guard in members(state)
        if adjacency[guard] & target_bit
        and ((state ^ (1 << guard)) | target_bit) in family
    )


def common_nonneighbors(
    adjacency: tuple[int, ...], left: int, right: int
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (left, right)
        and not adjacent(adjacency, left, vertex)
        and not adjacent(adjacency, right, vertex)
    )


def clique(adjacency: tuple[int, ...], vertices) -> bool:
    return all(
        adjacent(adjacency, left, right)
        for left, right in itertools.combinations(vertices, 2)
    )


def exact_static_three(adjacency: tuple[int, ...]) -> bool:
    order = len(adjacency)
    return (
        not any(dominates(adjacency, state) for state in subsets(order, 2))
        and any(dominates(adjacency, state) for state in subsets(order, 3))
        and any(independent(adjacency, state) for state in subsets(order, 3))
        and not any(
            independent(adjacency, state) for state in subsets(order, 4)
        )
    )


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in subsets(order, size)):
            return size
    raise AssertionError("minimum absent")


def independence_number(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency), 0, -1):
        if any(
            independent(adjacency, state)
            for state in subsets(len(adjacency), size)
        ):
            return size
    return 0


def clique_cover_number(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    for count in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(count)]

        def extend(vertex: int, used: int) -> bool:
            if vertex == order:
                return True
            for part in range(min(used + 1, count)):
                if all(
                    adjacent(adjacency, vertex, other)
                    for other in parts[part]
                ):
                    parts[part].append(vertex)
                    if extend(vertex + 1, max(used, part + 1)):
                        return True
                    parts[part].pop()
            return False

        if extend(0, 0):
            return count
    raise AssertionError("clique cover absent")


def parameter_vector(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    order = len(adjacency)
    gamma = minimum_size(order, lambda state: dominates(adjacency, state))
    independent_domination = minimum_size(
        order,
        lambda state: independent(adjacency, state)
        and dominates(adjacency, state),
    )
    eternal_number = next(
        size
        for size in range(1, order + 1)
        if greatest_family(adjacency, size)
    )
    return (
        gamma,
        independent_domination,
        independence_number(adjacency),
        eternal_number,
        clique_cover_number(adjacency),
    )


def audit_instance(
    adjacency: tuple[int, ...],
    family: set[int],
    u: int,
    x: int,
    r: int,
    completion: tuple[int, ...],
    layers: dict[int, tuple[int, ...]],
) -> Counter:
    counts = Counter()
    hot = set().union(*(set(layer) for layer in layers.values()))
    require(hot, "empty global hot set")

    for left, right in itertools.combinations(completion, 2):
        require(adjacent(adjacency, left, right), "completion not clique")
        require(
            x in common_nonneighbors(adjacency, left, right)
            and r in common_nonneighbors(adjacency, left, right),
            "missing two support blockers",
        )
        require(not adjacent(adjacency, x, r), "blockers adjacent")
        pair = (1 << left) | (1 << right)
        require(
            not any(state & pair == pair for state in family),
            "forbidden completion pair is supported",
        )
        counts["forbidden_completion_pairs"] += 1

    for d in completion:
        for w in hot:
            state = mask((u, d, w))
            require(state in family, ("missing product state", u, d, w))
            counts["product_incidences"] += 1
            for target in completion:
                if target == d:
                    continue
                require(
                    retained_movers(adjacency, family, state, target) == (d,),
                    ("nonunique completion transport", state, target),
                )
                counts["unique_transport_attacks"] += 1

    require(clique(adjacency, tuple(hot)), "global hot set is not a clique")
    counts["instances"] += 1
    counts["multi_C"] += len(completion) >= 2
    counts["multi_H"] += len(hot) >= 2

    central = common_nonneighbors(adjacency, u, x)
    if (
        central
        and all(mask((u, x, d)) in family for d in completion)
        and all(
            mask((u, w, z)) in family
            for w in hot
            for z in central
        )
    ):
        require(
            clique(adjacency, tuple(set(completion) | set(central))),
            "completion-central union not a clique",
        )
        counts["bridge_applications"] += 1
        counts["bridge_multi_C"] += len(completion) >= 2
        counts["bridge_multi_H"] += len(hot) >= 2
        counts["bridge_multi_Z"] += len(central) >= 2
        for w in hot:
            for z in central:
                require(
                    mask((u, w, z)) in family,
                    "missing hot-central bridge",
                )
                counts["HZ_cells"] += 1
                if adjacent(adjacency, w, z):
                    witnesses = common_nonneighbors(adjacency, w, z)
                    require(u in witnesses, "u absent from supported fan")
                    require(clique(adjacency, witnesses), "bad supported fan")
                    require(
                        all(mask((w, z, e)) in family for e in witnesses),
                        "supported fan not retained",
                    )
                    counts["HZ_edges"] += 1
                else:
                    counts["HZ_nonedges"] += 1
    return counts


def census() -> dict[str, object]:
    totals = Counter()
    by_order: dict[str, dict[str, int]] = {}
    for order in range(3, 7):
        counts = Counter()
        for code in range(1 << (order * (order - 1) // 2)):
            counts["labeled_graphs"] += 1
            adjacency = adjacency_from_code(order, code)
            if not exact_static_three(adjacency):
                continue
            family = greatest_family(adjacency, 3)
            if not family:
                continue
            counts["equality_graphs"] += 1
            for x in range(order):
                for r in range(order):
                    if x == r or adjacent(adjacency, x, r):
                        continue
                    completion = common_nonneighbors(adjacency, x, r)
                    if not completion or not clique(adjacency, completion):
                        continue
                    for u in range(order):
                        if (
                            u in (x, r)
                            or not adjacent(adjacency, u, x)
                            or not adjacent(adjacency, u, r)
                        ):
                            continue
                        layers = {
                            d: common_nonneighbors(adjacency, u, d)
                            for d in completion
                        }
                        if not all(layers.values()):
                            continue
                        if not all(
                            mask((u, d, w)) in family
                            for d in completion
                            for w in layers[d]
                        ):
                            continue
                        counts.update(
                            audit_instance(
                                adjacency,
                                family,
                                u,
                                x,
                                r,
                                completion,
                                layers,
                            )
                        )
        by_order[str(order)] = dict(sorted(counts.items()))
        totals.update(counts)
    return {
        "by_order": by_order,
        "totals": dict(sorted(totals.items())),
    }


def transport_control() -> dict[str, object]:
    record = "FCQe_"
    adjacency = decode_graph6(record)
    family = greatest_family(adjacency, 3)
    require(
        parameter_vector(adjacency) == (3, 3, 3, 3, 3),
        "wrong control parameters",
    )
    require(len(family) == 12, "wrong control family size")
    u, x, r = 5, 0, 2
    completion = common_nonneighbors(adjacency, x, r)
    layers = {
        d: common_nonneighbors(adjacency, u, d)
        for d in completion
    }
    require(completion == (1, 4), "wrong completion set")
    require(layers == {1: (3,), 4: (3, 6)}, "wrong hot fibers")
    counts = audit_instance(
        adjacency, family, u, x, r, completion, layers
    )
    require(mask((5, 1, 6)) in family, "transported cross state absent")
    return {
        "graph6": record,
        "parameters": [3, 3, 3, 3, 3],
        "greatest_triple_family_size": len(family),
        "u_x_r": [u, x, r],
        "C": list(completion),
        "fibers": {str(key): list(value) for key, value in layers.items()},
        "transported_nonseed_state": [5, 1, 6],
        "audit_counts": dict(sorted(counts.items())),
    }


def main() -> None:
    print(
        json.dumps(
            {
                "schema": "qq1-bowtie-global-coupling-audit-v1",
                "status": "VERIFIED",
                "model": (
                    "one guard moves; attacks only at unoccupied vertices"
                ),
                "census": census(),
                "transport_control": transport_control(),
                "scope": (
                    "The audit verifies the global C-by-H transport and "
                    "H-by-Z cell normal form; it does not eliminate QQ1."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

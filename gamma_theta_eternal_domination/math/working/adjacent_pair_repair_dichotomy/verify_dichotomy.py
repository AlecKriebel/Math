#!/usr/bin/env python3
"""Independent finite audit for the adjacent-pair repair dichotomy.

This checker uses only integer bitsets and exhaustive enumeration.  It
does not import a campaign evaluator or the QQ1 search code.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mask(vertices) -> int:
    result = 0
    for vertex in vertices:
        result |= 1 << vertex
    return result


def vertices(state: int):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def subsets(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield mask(choice)


def adjacency_from_code(order: int, code: int) -> tuple[int, ...]:
    adjacency = [0] * order
    for index, (left, right) in enumerate(itertools.combinations(range(order), 2)):
        if code & (1 << index):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return tuple(adjacency)


def decode_graph6(record: str) -> tuple[int, ...]:
    values = tuple(ord(character) - 63 for character in record)
    require(values and 0 <= values[0] <= 62, "only short graph6 is supported")
    order = values[0]
    bits = tuple(
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    )
    needed = order * (order - 1) // 2
    require(len(bits) >= needed and not any(bits[needed:]), "invalid graph6 payload")
    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return tuple(adjacency)


def encode_graph6(adjacency: tuple[int, ...]) -> str:
    order = len(adjacency)
    bits = [
        int(bool(adjacency[left] & (1 << right)))
        for right in range(1, order)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(
        not adjacency[vertex] & (state ^ (1 << vertex))
        for vertex in vertices(state)
    )


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def eternal(adjacency: tuple[int, ...], family: set[int]) -> bool:
    order = len(adjacency)
    if not family or not all(dominates(adjacency, state) for state in family):
        return False
    for state in family:
        for target in range(order):
            target_bit = 1 << target
            if state & target_bit:
                continue
            if not any(
                adjacency[guard] & target_bit
                and ((state ^ (1 << guard)) | target_bit) in family
                for guard in vertices(state)
            ):
                return False
    return True


def greatest_family(adjacency: tuple[int, ...]) -> set[int]:
    order = len(adjacency)
    family = {
        state
        for state in subsets(order, 3)
        if dominates(adjacency, state)
    }
    while True:
        removed = set()
        for state in family:
            for target in range(order):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                if not any(
                    adjacency[guard] & target_bit
                    and ((state ^ (1 << guard)) | target_bit) in family
                    for guard in vertices(state)
                ):
                    removed.add(state)
                    break
        if not removed:
            return family
        family.difference_update(removed)


def exact_static_three(adjacency: tuple[int, ...]) -> bool:
    order = len(adjacency)
    if any(dominates(adjacency, state) for state in subsets(order, 1)):
        return False
    if any(dominates(adjacency, state) for state in subsets(order, 2)):
        return False
    if not any(dominates(adjacency, state) for state in subsets(order, 3)):
        return False
    if not any(independent(adjacency, state) for state in subsets(order, 3)):
        return False
    return not any(independent(adjacency, state) for state in subsets(order, 4))


def active(
    adjacency: tuple[int, ...],
    family: set[int],
    source: int,
    target: int,
) -> bool:
    order = len(adjacency)
    if not adjacency[source] & (1 << target):
        return False
    for state in subsets(order, 3):
        if (
            state in family
            and state & (1 << source)
            and not state & (1 << target)
            and independent(adjacency, state)
            and ((state ^ (1 << source)) | (1 << target)) in family
        ):
            return True
    return False


def common_nonneighbors(
    adjacency: tuple[int, ...],
    left: int,
    right: int,
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (left, right)
        and not adjacency[left] & (1 << vertex)
        and not adjacency[right] & (1 << vertex)
    )


def audit_family(
    adjacency: tuple[int, ...],
    family: set[int],
) -> Counter:
    require(exact_static_three(adjacency), "family audit lacks gamma=alpha=3")
    require(eternal(adjacency, family), "family audit lacks eternal closure")
    counts = Counter()
    order = len(adjacency)
    for left in range(order):
        for right in range(left + 1, order):
            if not adjacency[left] & (1 << right):
                continue
            witnesses = common_nonneighbors(adjacency, left, right)
            require(witnesses, "gamma=3 edge has no common nonneighbor")
            centers = {
                witness: mask((left, right, witness)) in family
                for witness in witnesses
            }
            if any(centers.values()):
                require(all(centers.values()), "mixed central-fan membership")
                for witness in witnesses:
                    for target in witnesses:
                        if witness == target:
                            continue
                        require(
                            adjacency[witness] & (1 << target),
                            "retained central fan is not a clique",
                        )
                        source_state = mask((left, right, witness))
                        target_state = mask((left, right, target))
                        require(target_state in family, "central target is absent")
                        responders = tuple(
                            guard
                            for guard in vertices(source_state)
                            if adjacency[guard] & (1 << target)
                            and ((source_state ^ (1 << guard)) | (1 << target))
                            in family
                        )
                        require(
                            responders == (witness,),
                            "central witness exchange is not unique",
                        )
                if active(adjacency, family, left, right) and active(
                    adjacency, family, right, left
                ):
                    counts["retained_fan_reciprocal"] += 1
                else:
                    counts["retained_fan_nonreciprocal"] += 1
            else:
                require(
                    active(adjacency, family, left, right),
                    "omitted fan lacks forward activity",
                )
                require(
                    active(adjacency, family, right, left),
                    "omitted fan lacks reverse activity",
                )
                counts["omitted_fan_reciprocal"] += 1
    return counts


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in subsets(order, size)):
            return size
    raise AssertionError("no finite minimum")


def independence_number(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency), 0, -1):
        if any(independent(adjacency, state) for state in subsets(len(adjacency), size)):
            return size
    return 0


def clique_cover_number(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    for part_count in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(part_count)]

        def extend(vertex: int, used: int) -> bool:
            if vertex == order:
                return True
            for part in range(min(used + 1, part_count)):
                if part == used and used == part_count:
                    continue
                if all(adjacency[vertex] & (1 << member) for member in parts[part]):
                    parts[part].append(vertex)
                    if extend(vertex + 1, max(used, part + 1)):
                        return True
                    parts[part].pop()
            return False

        if extend(0, 0):
            return part_count
    raise AssertionError("singleton clique cover must exist")


def parameter_vector(adjacency: tuple[int, ...]) -> tuple[int, int, int, int, int]:
    order = len(adjacency)
    gamma = minimum_size(order, lambda state: dominates(adjacency, state))
    i_value = minimum_size(
        order,
        lambda state: independent(adjacency, state) and dominates(adjacency, state),
    )
    alpha = independence_number(adjacency)
    gamma_infinity = next(
        count
        for count in range(1, order + 1)
        if (
            greatest_family(adjacency)
            if count == 3
            else greatest_family_for_count(adjacency, count)
        )
    )
    theta = clique_cover_number(adjacency)
    return gamma, i_value, alpha, gamma_infinity, theta


def greatest_family_for_count(
    adjacency: tuple[int, ...],
    guard_count: int,
) -> set[int]:
    order = len(adjacency)
    family = {
        state
        for state in subsets(order, guard_count)
        if dominates(adjacency, state)
    }
    while True:
        removed = set()
        for state in family:
            for target in range(order):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                if not any(
                    adjacency[guard] & target_bit
                    and ((state ^ (1 << guard)) | target_bit) in family
                    for guard in vertices(state)
                ):
                    removed.add(state)
                    break
        if not removed:
            return family
        family.difference_update(removed)


def connected(adjacency: tuple[int, ...]) -> bool:
    if not adjacency:
        return False
    seen = 1
    previous = 0
    while seen != previous:
        previous = seen
        for vertex in vertices(seen):
            seen |= adjacency[vertex]
    return seen == (1 << len(adjacency)) - 1


def fixed_control(record: str) -> dict:
    adjacency = decode_graph6(record)
    require(encode_graph6(adjacency) == record, "control graph6 round trip failed")
    family = greatest_family(adjacency)
    counts = audit_family(adjacency, family)
    return {
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(adjacency),
        "size": sum(mask.bit_count() for mask in adjacency) // 2,
        "connected": connected(adjacency),
        "parameters": parameter_vector(adjacency),
        "greatest_triple_family_size": len(family),
        "branch_counts": dict(sorted(counts.items())),
    }


def main() -> None:
    greatest_graphs = 0
    greatest_families = 0
    greatest_obligations = Counter()
    labeled_graph_count = 0
    for order in range(1, 7):
        edge_count = order * (order - 1) // 2
        for code in range(1 << edge_count):
            labeled_graph_count += 1
            adjacency = adjacency_from_code(order, code)
            if order < 3 or not exact_static_three(adjacency):
                continue
            family = greatest_family(adjacency)
            if not family:
                continue
            greatest_graphs += 1
            greatest_families += 1
            greatest_obligations.update(audit_family(adjacency, family))

    arbitrary_families = 0
    arbitrary_graphs = 0
    arbitrary_obligations = Counter()
    for order in range(3, 6):
        edge_count = order * (order - 1) // 2
        for code in range(1 << edge_count):
            adjacency = adjacency_from_code(order, code)
            if not exact_static_three(adjacency):
                continue
            dominating_triples = tuple(
                state for state in subsets(order, 3) if dominates(adjacency, state)
            )
            graph_has_family = False
            for family_code in range(1, 1 << len(dominating_triples)):
                family = {
                    state
                    for index, state in enumerate(dominating_triples)
                    if family_code & (1 << index)
                }
                if not eternal(adjacency, family):
                    continue
                graph_has_family = True
                arbitrary_families += 1
                arbitrary_obligations.update(audit_family(adjacency, family))
            arbitrary_graphs += int(graph_has_family)

    controls = {
        "connected_two_branch_control": fixed_control("EpQ?"),
        "retained_fan_reciprocal_control": fixed_control("D]?"),
    }
    require(
        controls["connected_two_branch_control"]["parameters"] == (3, 3, 3, 3, 3),
        "wrong connected control parameter vector",
    )
    require(
        controls["retained_fan_reciprocal_control"]["parameters"]
        == (3, 3, 3, 3, 3),
        "wrong reciprocal-fan control parameter vector",
    )
    first_counts = controls["connected_two_branch_control"]["branch_counts"]
    require(
        first_counts.get("retained_fan_nonreciprocal", 0) > 0
        and first_counts.get("omitted_fan_reciprocal", 0) > 0,
        "connected control does not realize both sharp branches",
    )
    require(
        controls["retained_fan_reciprocal_control"]["branch_counts"].get(
            "retained_fan_reciprocal", 0
        )
        > 0,
        "second control lacks a reciprocal retained fan",
    )

    result = {
        "schema": "adjacent-pair-repair-dichotomy-audit-v1",
        "status": "VERIFIED",
        "model": "one-guard-moves; attacks only at unoccupied vertices",
        "greatest_family_census_through_order_6": {
            "labeled_graphs_examined": labeled_graph_count,
            "applicable_graphs": greatest_graphs,
            "applicable_families": greatest_families,
            "edge_obligations": dict(sorted(greatest_obligations.items())),
        },
        "arbitrary_eternal_subfamily_census_through_order_5": {
            "applicable_graphs": arbitrary_graphs,
            "applicable_families": arbitrary_families,
            "edge_obligations": dict(sorted(arbitrary_obligations.items())),
        },
        "controls": controls,
        "scope": (
            "The audit checks the theorem and sharp branches. It does not "
            "eliminate QQ1, prove complete k=3, or resolve gamma-theta."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

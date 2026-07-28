#!/usr/bin/env python3
"""Standalone exact checker for the first-cross-clause controls."""

from __future__ import annotations

import hashlib
import itertools
import json


FD_FAMILY = (
    (0, 1, 2),
    (1, 2, 3),
    (0, 1, 4),
    (1, 2, 4),
    (1, 3, 4),
    (0, 1, 5),
    (0, 2, 5),
    (1, 3, 5),
    (2, 3, 5),
    (0, 4, 5),
    (1, 4, 5),
    (2, 4, 5),
    (3, 4, 5),
    (0, 2, 6),
    (2, 3, 6),
    (0, 4, 6),
    (2, 4, 6),
    (3, 4, 6),
    (0, 5, 6),
    (3, 5, 6),
    (4, 5, 6),
)


def decode_graph6(record: str) -> tuple[int, list[int]]:
    data = record.encode("ascii")
    if not data or not 63 <= data[0] < 126:
        raise ValueError("only short graph6 records are supported")
    n = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("bad graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < n * (n - 1) // 2:
        raise ValueError("truncated graph6")
    adjacency = [0] * n
    index = 0
    for high in range(1, n):
        for low in range(high):
            if bits[index]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            index += 1
    return n, adjacency


def mask(items) -> int:
    return sum(1 << item for item in items)


def members(state: int) -> tuple[int, ...]:
    return tuple(index for index in range(state.bit_length()) if state >> index & 1)


def subsets(n: int, size: int):
    for values in itertools.combinations(range(n), size):
        yield mask(values)


def dominates(state: int, adjacency: list[int], full: int) -> bool:
    covered = state
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        covered |= adjacency[bit.bit_length() - 1]
    return covered == full


def independent(state: int, adjacency: list[int]) -> bool:
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & scan:
            return False
    return True


def minimum_parameter(n: int, predicate) -> int:
    for size in range(1, n + 1):
        if any(predicate(state) for state in subsets(n, size)):
            return size
    raise AssertionError("parameter search failed")


def greatest_family(
    n: int, adjacency: list[int], size: int
) -> tuple[set[int], tuple[int, ...]]:
    full = (1 << n) - 1
    family = {
        state for state in subsets(n, size) if dominates(state, adjacency, full)
    }
    round_sizes = []
    while True:
        bad = set()
        for state in family:
            for attacked in range(n):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                guards = state & adjacency[attacked]
                if not any(
                    ((state ^ bit) | attacked_bit) in family
                    for bit in (
                        1 << guard
                        for guard in range(n)
                        if guards >> guard & 1
                    )
                ):
                    bad.add(state)
                    break
        if not bad:
            return family, tuple(round_sizes)
        round_sizes.append(len(bad))
        family -= bad


def eternal_number(n: int, adjacency: list[int]) -> int:
    for size in range(1, n + 1):
        family, _ = greatest_family(n, adjacency, size)
        if family:
            return size
    raise AssertionError("eternal parameter search failed")


def theta_number(n: int, adjacency: list[int]) -> int:
    full = (1 << n) - 1
    h_neighbors = [
        full ^ adjacency[vertex] ^ (1 << vertex) for vertex in range(n)
    ]

    def colorable(count: int) -> bool:
        colors = [-1] * n

        def visit() -> bool:
            uncolored = [vertex for vertex in range(n) if colors[vertex] < 0]
            if not uncolored:
                return True
            vertex = max(
                uncolored,
                key=lambda item: (
                    len(
                        {
                            colors[other]
                            for other in members(h_neighbors[item])
                            if colors[other] >= 0
                        }
                    ),
                    h_neighbors[item].bit_count(),
                    -item,
                ),
            )
            forbidden = {
                colors[other]
                for other in members(h_neighbors[vertex])
                if colors[other] >= 0
            }
            for color in range(count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                if visit():
                    return True
                colors[vertex] = -1
            return False

        return visit()

    for count in range(1, n + 1):
        if colorable(count):
            return count
    raise AssertionError("coloring search failed")


def parameters(n: int, adjacency: list[int]) -> dict[str, int]:
    full = (1 << n) - 1
    gamma = minimum_parameter(
        n, lambda state: dominates(state, adjacency, full)
    )
    alpha = max(
        size
        for size in range(1, n + 1)
        if any(independent(state, adjacency) for state in subsets(n, size))
    )
    independent_domination = minimum_parameter(
        n,
        lambda state: independent(state, adjacency)
        and dominates(state, adjacency, full),
    )
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": eternal_number(n, adjacency),
        "theta": theta_number(n, adjacency),
    }


def check_family(
    n: int, adjacency: list[int], family: set[int]
) -> tuple[int, str]:
    full = (1 << n) - 1
    rows = []
    for state in sorted(family):
        if state.bit_count() != 3 or not dominates(state, adjacency, full):
            raise AssertionError("bad retained state")
        for attacked in range(n):
            attacked_bit = 1 << attacked
            if state & attacked_bit:
                continue
            legal = []
            guards = state & adjacency[attacked]
            for guard in range(n):
                guard_bit = 1 << guard
                if not guards & guard_bit:
                    continue
                successor = (state ^ guard_bit) | attacked_bit
                if successor in family:
                    legal.append(guard)
            if not legal:
                raise AssertionError(
                    f"unanswered attack {members(state)} -> {attacked}"
                )
            rows.append([state, attacked, legal])
    digest = hashlib.sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    return len(rows), digest


def response_lists(
    n: int, family: set[int], reference: tuple[int, int, int]
) -> dict[int, tuple[int, ...]]:
    reference_mask = mask(reference)
    result = {}
    for vertex in range(n):
        if vertex in reference:
            continue
        result[vertex] = tuple(
            anchor
            for anchor in reference
            if ((reference_mask ^ (1 << anchor)) | (1 << vertex)) in family
        )
        if not result[vertex]:
            raise AssertionError("empty response list")
    return result


def h_neighbors(n: int, adjacency: list[int]) -> list[int]:
    full = (1 << n) - 1
    return [
        full ^ adjacency[vertex] ^ (1 << vertex) for vertex in range(n)
    ]


def projection_components(
    n: int,
    adjacency: list[int],
    reference: tuple[int, int, int],
    lists: dict[int, tuple[int, ...]],
    frozen: int,
) -> list[tuple[int, ...]]:
    retained = (set(reference) - {frozen}) | {
        vertex for vertex, values in lists.items() if frozen not in values
    }
    unseen = set(retained)
    components = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        component = {root}
        queue = [root]
        while queue:
            left = queue.pop()
            for right in sorted(tuple(unseen)):
                if adjacency[left] >> right & 1:
                    continue
                unseen.remove(right)
                component.add(right)
                queue.append(right)
        components.append(tuple(sorted(component)))
    return sorted(components)


def fd_control() -> dict[str, object]:
    record = "FDzro"
    n, adjacency = decode_graph6(record)
    family = {mask(state) for state in FD_FAMILY}
    obligations, digest = check_family(n, adjacency, family)
    reference = (0, 1, 2)
    lists = response_lists(n, family, reference)
    expected_lists = {
        3: (0,),
        4: (0, 2),
        5: (1, 2),
        6: (1,),
    }
    if lists != expected_lists:
        raise AssertionError(f"FDzro list mismatch {lists}")
    h = h_neighbors(n, adjacency)
    path = (3, 4, 5, 6)
    for left, right in zip(path[:-1], path[1:], strict=True):
        if not h[left] >> right & 1:
            raise AssertionError("missing complement path edge")
    for left, right in ((3, 5), (3, 6), (4, 6)):
        if h[left] >> right & 1:
            raise AssertionError("complement path chord")
    projection_b = projection_components(n, adjacency, reference, lists, 1)
    projection_a = projection_components(n, adjacency, reference, lists, 0)
    if (3, 4) not in projection_b or (5, 6) not in projection_a:
        raise AssertionError("wrong free components")
    defects_left = members(h[2] & h[3])
    defects_right = members(h[2] & h[6])
    if defects_left != (1,) or defects_right != (0,):
        raise AssertionError("wrong anchor-only defects")
    greatest, rounds = greatest_family(n, adjacency, 3)
    return {
        "graph6": record,
        "parameters": parameters(n, adjacency),
        "specified_family_size": len(family),
        "specified_obligations": obligations,
        "obligation_digest": digest,
        "greatest_triple_family_size": len(greatest),
        "greatest_kernel_rounds": list(rounds),
        "response_lists": {str(k): list(v) for k, v in lists.items()},
        "free_components": {
            "frozen_1": [list(value) for value in projection_b],
            "frozen_0": [list(value) for value in projection_a],
        },
        "defect_ridges": {
            "pin_3_color_2": list(defects_left),
            "pin_6_color_2": list(defects_right),
        },
    }


def fc_control() -> dict[str, object]:
    record = "FCZbg"
    n, adjacency = decode_graph6(record)
    family, rounds = greatest_family(n, adjacency, 3)
    obligations, digest = check_family(n, adjacency, family)
    reference = (3, 4, 5)
    lists = response_lists(n, family, reference)
    expected_lists = {0: (3,), 1: (4, 5), 2: (4, 5), 6: (5,)}
    if lists != expected_lists:
        raise AssertionError(f"FCZbg list mismatch {lists}")
    h = h_neighbors(n, adjacency)
    left = members(h[4] & h[0])
    right = members(h[4] & h[6])
    if left != (6,) or right != (0,):
        raise AssertionError("wrong equality defect ridges")
    exchange = mask((0, 4, 6))
    if exchange not in family:
        raise AssertionError("missing ridge exchange state")
    if 5 not in lists[6] or 3 not in lists[0]:
        raise AssertionError("wrong forced defect response")
    return {
        "graph6": record,
        "parameters": parameters(n, adjacency),
        "greatest_triple_family_size": len(family),
        "greatest_kernel_rounds": list(rounds),
        "obligations": obligations,
        "obligation_digest": digest,
        "response_lists": {str(k): list(v) for k, v in lists.items()},
        "defect_ridges_at_color_4": {
            "pin_0": list(left),
            "pin_6": list(right),
        },
        "exchange_state": list(members(exchange)),
    }


def main() -> None:
    result = {
        "status": "PASS",
        "model": "standard one-guard-moves eternal domination",
        "fdzro_literal_one_clause": fd_control(),
        "fczbg_equality_ridge": fc_control(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

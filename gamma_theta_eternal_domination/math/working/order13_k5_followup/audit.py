#!/usr/bin/env python3
"""Small solver-free checks for the order-13 k=5 follow-up.

This is not a coverage certificate.  It checks finite arithmetic, the
order-five residual classification used in Lemma 9, the exact domination
case count, and the set-theoretic split used in Theorem 10.  All graph
invariants below are implemented directly in this file.
"""

from __future__ import annotations

from itertools import combinations
import json


def subsets(mask: int):
    current = mask
    while True:
        yield current
        if current == 0:
            return
        current = (current - 1) & mask


def is_independent(adjacency: tuple[int, ...], chosen: int) -> bool:
    scan = chosen
    while scan:
        bit = scan & -scan
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & chosen:
            return False
        scan ^= bit
    return True


def is_dominating(adjacency: tuple[int, ...], chosen: int) -> bool:
    covered = chosen
    scan = chosen
    while scan:
        bit = scan & -scan
        vertex = bit.bit_length() - 1
        covered |= adjacency[vertex]
        scan ^= bit
    return covered == (1 << len(adjacency)) - 1


def alpha(adjacency: tuple[int, ...]) -> int:
    full = (1 << len(adjacency)) - 1
    return max(mask.bit_count() for mask in subsets(full)
               if is_independent(adjacency, mask))


def gamma(adjacency: tuple[int, ...]) -> int:
    full = (1 << len(adjacency)) - 1
    return min(mask.bit_count() for mask in subsets(full)
               if is_dominating(adjacency, mask))


def theta(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    full = (1 << n) - 1
    clique = [False] * (1 << n)
    clique[0] = True
    for mask in range(1, 1 << n):
        bit = mask & -mask
        vertex = bit.bit_length() - 1
        rest = mask ^ bit
        clique[mask] = clique[rest] and not (rest & ~adjacency[vertex])
    value = [n + 1] * (1 << n)
    value[0] = 0
    for mask in range(1, 1 << n):
        pivot = mask & -mask
        part = mask
        while part:
            if part & pivot and clique[part]:
                value[mask] = min(value[mask], 1 + value[mask ^ part])
            part = (part - 1) & mask
    return value[full]


def graph_from_edge_mask(n: int, edge_mask: int) -> tuple[int, ...]:
    adjacency = [0] * n
    position = 0
    for high in range(1, n):
        for low in range(high):
            if edge_mask & (1 << position):
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    return tuple(adjacency)


def check_order_five_classification() -> int:
    qualifying = 0
    for edge_mask in range(1 << 10):
        adjacency = graph_from_edge_mask(5, edge_mask)
        if (gamma(adjacency), alpha(adjacency), theta(adjacency)) == (4, 4, 4):
            qualifying += 1
            if edge_mask.bit_count() != 1:
                raise AssertionError("Lemma 9 residual is not a one-edge graph")
    if qualifying != 10:
        raise AssertionError("unexpected number of labeled one-edge graphs")
    return qualifying


def check_domination_count() -> int:
    total = (
        3 * sum(len(tuple(combinations(range(10), size)))
                for size in range(4))
        + 3 * sum(len(tuple(combinations(range(10), size)))
                  for size in range(3))
        + sum(len(tuple(combinations(range(10), size)))
              for size in range(2))
    )
    if total != 707:
        raise AssertionError("domination obligation count changed")
    return total


def check_raw_mask_count() -> tuple[int, int]:
    ordered = 0
    diagonal = 0
    full = (1 << 10) - 1
    masks = [mask for mask in range(1, 1 << 10) if mask.bit_count() <= 6]
    for first in masks:
        for second in masks:
            if (full ^ (first | second)).bit_count() < 3:
                continue
            ordered += 1
            if first == second:
                diagonal += 1
    if (ordered, diagonal) != (465157, 847):
        raise AssertionError("raw attachment-mask count changed")
    return ordered, (ordered + diagonal) // 2


def check_two_six_mask_split() -> tuple[int, int]:
    masks = [sum(1 << vertex for vertex in chosen)
             for chosen in combinations(range(10), 6)]
    equal = 0
    unequal = 0
    full = (1 << 10) - 1
    for first in masks:
        for second in masks:
            residual = full ^ (first | second)
            if residual.bit_count() < 3:
                continue
            intersection = (first & second).bit_count()
            if first == second:
                equal += 1
                if residual.bit_count() != 4 or intersection != 6:
                    raise AssertionError("bad equal-mask branch")
            else:
                unequal += 1
                if (
                    residual.bit_count() != 3
                    or intersection != 5
                    or (first ^ second).bit_count() != 2
                ):
                    raise AssertionError("bad unequal-mask branch")
    if (equal, unequal) != (210, 5040):
        raise AssertionError("unexpected six-mask split")
    return equal, unequal


def main() -> None:
    labeled_residuals = check_order_five_classification()
    domination_tests = check_domination_count()
    ordered_masks, unordered_masks = check_raw_mask_count()
    equal_six, unequal_six = check_two_six_mask_split()
    print(json.dumps({
        "schema": "gamma-theta-order13-k5-followup-small-audit-v1",
        "broad_enumeration_performed": False,
        "order_five_labeled_graphs_checked": 1 << 10,
        "order_five_qualifying_one_edge_graphs": labeled_residuals,
        "domination_tests": domination_tests,
        "raw_ordered_mask_pairs": ordered_masks,
        "raw_unordered_mask_pairs": unordered_masks,
        "equal_six_mask_pairs": equal_six,
        "unequal_six_mask_pairs_rejected_by_theorem": unequal_six,
        "claim_boundary": "structural_reduction_not_slice_exclusion",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

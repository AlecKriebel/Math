#!/usr/bin/env python3
"""Independent ordinary-set audit of the critical bounded conclusion.

This file intentionally does not import the search implementation.  It
re-enumerates the 512 extensions and the 27*512 complement-edge-addition
cases, reconstructs the family predicate with frozensets, and checks directly
that every predicate-positive graph has a dominating singleton or pair.
"""

from __future__ import annotations

import itertools
import json


BASE_N = 9
N = 10
VERTICES = frozenset(range(N))
S = frozenset((0, 1, 2))
X = 3
BASE_H = frozenset(
    {
        frozenset((0, 1)),
        frozenset((0, 2)),
        frozenset((1, 2)),
        frozenset((3, 4)),
        frozenset((4, 5)),
        frozenset((5, 6)),
        frozenset((6, 8)),
        frozenset((7, 8)),
        frozenset((4, 7)),
    }
)
OLD_LISTS = {
    3: frozenset((0, 1, 2)),
    4: frozenset((0, 1)),
    5: frozenset((0, 1)),
    6: frozenset((0, 1)),
    7: frozenset((1, 2)),
    8: frozenset((1, 2)),
}
ADDABLE_OLD_H_EDGES = tuple(
    frozenset((u, v))
    for u in range(BASE_N)
    for v in range(u + 1, BASE_N)
    if frozenset((u, v)) not in BASE_H
)


def h_edges(extension: int, extra: frozenset[int] | None):
    result = set(BASE_H)
    result.update(
        frozenset((old, 9))
        for old in range(BASE_N)
        if extension & (1 << old)
    )
    if extra is not None:
        result.add(extra)
    return frozenset(result)


def adjacent_g(u: int, v: int, h: frozenset[frozenset[int]]) -> bool:
    return u != v and frozenset((u, v)) not in h


def dominates(state: frozenset[int], h: frozenset[frozenset[int]]) -> bool:
    return all(
        vertex in state
        or any(adjacent_g(vertex, guard, h) for guard in state)
        for vertex in VERTICES
    )


def swap(guard: int, target: int) -> frozenset[int]:
    return (S - {guard}) | {target}


def safe_kernel(
    h: frozenset[frozenset[int]], banned: frozenset[frozenset[int]]
) -> frozenset[frozenset[int]]:
    family = {
        frozenset(state)
        for state in itertools.combinations(range(N), 3)
        if frozenset(state) not in banned and dominates(frozenset(state), h)
    }
    while True:
        dead = set()
        for state in family:
            for attack in VERTICES - state:
                if not any(
                    adjacent_g(guard, attack, h)
                    and (state - {guard}) | {attack} in family
                    for guard in state
                ):
                    dead.add(state)
                    break
        if not dead:
            return frozenset(family)
        family.difference_update(dead)


def list_colorable(
    h: frozenset[frozenset[int]],
    lists: dict[int, frozenset[int]],
    *,
    include_x: bool,
) -> bool:
    assigned = {0: 0, 1: 1, 2: 2}
    vertices = tuple(
        vertex
        for vertex in range(3, N)
        if include_x or vertex != X
    )
    effective = dict(lists)
    if include_x:
        effective[X] = frozenset((0,))

    def visit(remaining: tuple[int, ...]) -> bool:
        if not remaining:
            return True
        options = {}
        for vertex in remaining:
            colors = tuple(
                color
                for color in effective[vertex]
                if all(
                    color != other_color
                    for other, other_color in assigned.items()
                    if frozenset((vertex, other)) in h
                )
            )
            if not colors:
                return False
            options[vertex] = colors
        vertex = min(options, key=lambda item: (len(options[item]), item))
        rest = tuple(item for item in remaining if item != vertex)
        for color in options[vertex]:
            assigned[vertex] = color
            if visit(rest):
                del assigned[vertex]
                return True
            del assigned[vertex]
        return False

    return visit(vertices)


def predicate(h: frozenset[frozenset[int]]) -> bool:
    eligible = frozenset(
        guard for guard in S if adjacent_g(guard, 9, h)
    )
    for size in (1, 2):
        for new_list_tuple in itertools.combinations(sorted(eligible), size):
            new_list = frozenset(new_list_tuple)
            lists = dict(OLD_LISTS)
            lists[9] = new_list
            banned = frozenset(
                swap(guard, target)
                for target, allowed in lists.items()
                for guard in S
                if guard not in allowed
            )
            family = safe_kernel(h, banned)
            required = {S} | {
                swap(guard, target)
                for target, allowed in lists.items()
                for guard in allowed
            }
            if not required <= family:
                continue
            if list_colorable(h, lists, include_x=False) and not list_colorable(
                h, lists, include_x=True
            ):
                return True
    return False


def minimum_domination_at_most_two(
    h: frozenset[frozenset[int]],
) -> tuple[int, tuple[int, ...]]:
    for size in (1, 2):
        for state in itertools.combinations(range(N), size):
            if dominates(frozenset(state), h):
                return size, state
    return 3, ()


def audit_scope(extras: tuple[frozenset[int] | None, ...]) -> dict:
    cases = positives = gamma1 = gamma2 = gamma_at_least3 = 0
    for extra in extras:
        for extension in range(1 << BASE_N):
            cases += 1
            h = h_edges(extension, extra)
            if not predicate(h):
                continue
            positives += 1
            size, _ = minimum_domination_at_most_two(h)
            if size == 1:
                gamma1 += 1
            elif size == 2:
                gamma2 += 1
            else:
                gamma_at_least3 += 1
    return {
        "cases": cases,
        "predicate_positive": positives,
        "positive_with_gamma_1": gamma1,
        "positive_with_gamma_2": gamma2,
        "positive_with_gamma_at_least_3": gamma_at_least3,
    }


def main() -> None:
    assert len(BASE_H) == 9
    assert len(ADDABLE_OLD_H_EDGES) == 27
    extensions = audit_scope((None,))
    edge_additions = audit_scope(ADDABLE_OLD_H_EDGES)
    print(
        json.dumps(
            {
                "computed_extensions": extensions,
                "computed_edge_additions": edge_additions,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    assert extensions == {
        "cases": 512,
        "predicate_positive": 99,
        "positive_with_gamma_1": 1,
        "positive_with_gamma_2": 98,
        "positive_with_gamma_at_least_3": 0,
    }
    assert edge_additions == {
        "cases": 13824,
        "predicate_positive": 718,
        "positive_with_gamma_1": 8,
        "positive_with_gamma_2": 710,
        "positive_with_gamma_at_least_3": 0,
    }
    result = {
        "status": "PASS",
        "implementation": "independent frozenset ordinary-set replay",
        "extensions": extensions,
        "edge_additions": edge_additions,
        "conclusion": (
            "No predicate-positive case in either bounded scope has gamma=3."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

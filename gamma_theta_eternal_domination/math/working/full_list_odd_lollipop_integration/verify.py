#!/usr/bin/env python3
"""Ordinary-set verifier for the separated-port lollipop control."""

from __future__ import annotations

import itertools
import json


N = 9
S = frozenset((0, 1, 2))
X, R, T, Q, V0, V1 = 3, 4, 5, 6, 7, 8
H_EDGES = frozenset(
    {
        (0, 1),
        (0, 2),
        (1, 2),
        (X, R),
        (R, T),
        (T, Q),
        (Q, V1),
        (V0, V1),
        (R, V0),
    }
)
DESIRED_LISTS = {
    X: frozenset((0, 1, 2)),
    R: frozenset((0, 1)),
    T: frozenset((0, 1)),
    Q: frozenset((0, 1)),
    V0: frozenset((1, 2)),
    V1: frozenset((1, 2)),
}


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def g_edge(u: int, v: int) -> bool:
    return u != v and pair(u, v) not in H_EDGES


def dominates(state: frozenset[int]) -> bool:
    return all(
        vertex in state or any(g_edge(vertex, guard) for guard in state)
        for vertex in range(N)
    )


def independent(state: frozenset[int]) -> bool:
    return all(not g_edge(u, v) for u, v in itertools.combinations(state, 2))


def direct_swap(guard: int, target: int) -> frozenset[int]:
    return (S - {guard}) | {target}


def restricted_kernel() -> tuple[frozenset[frozenset[int]], tuple[int, ...]]:
    banned = {
        direct_swap(guard, target)
        for target, allowed in DESIRED_LISTS.items()
        for guard in S
        if guard not in allowed
    }
    family = {
        frozenset(state)
        for state in itertools.combinations(range(N), 3)
        if frozenset(state) not in banned and dominates(frozenset(state))
    }
    rounds: list[int] = []
    while True:
        dead = set()
        for state in family:
            for attack in set(range(N)) - state:
                if not any(
                    g_edge(guard, attack)
                    and (state - {guard}) | {attack} in family
                    for guard in state
                ):
                    dead.add(state)
                    break
        if not dead:
            return frozenset(family), tuple(rounds)
        rounds.append(len(dead))
        family.difference_update(dead)


def family_audit(family: frozenset[frozenset[int]]) -> int:
    obligations = 0
    for state in family:
        assert dominates(state)
        for attack in set(range(N)) - state:
            obligations += 1
            assert any(
                g_edge(guard, attack)
                and (state - {guard}) | {attack} in family
                for guard in state
            )
    return obligations


def response_lists(
    family: frozenset[frozenset[int]],
) -> dict[int, frozenset[int]]:
    return {
        target: frozenset(
            guard
            for guard in S
            if g_edge(guard, target)
            and direct_swap(guard, target) in family
        )
        for target in set(range(N)) - S
    }


def exact_parameter(kind: str) -> int:
    for size in range(1, N + 1):
        states = map(frozenset, itertools.combinations(range(N), size))
        if kind == "gamma" and any(dominates(state) for state in states):
            return size
        if kind == "alpha":
            reverse_size = N + 1 - size
            states = map(
                frozenset, itertools.combinations(range(N), reverse_size)
            )
            if any(independent(state) for state in states):
                return reverse_size
    raise AssertionError(kind)


def proper_h_coloring_count(
    lists: dict[int, frozenset[int]], *, include_x: bool
) -> int:
    vertices = [v for v in range(N) if v not in S and (include_x or v != X)]
    assigned = {anchor: anchor for anchor in S}
    count = 0

    def visit(index: int) -> None:
        nonlocal count
        if index == len(vertices):
            count += 1
            return
        vertex = vertices[index]
        for color in lists[vertex]:
            if all(
                color != other_color
                for other, other_color in assigned.items()
                if pair(vertex, other) in H_EDGES
            ):
                assigned[vertex] = color
                visit(index + 1)
                del assigned[vertex]

    visit(0)
    return count


def fan_embeddings(lists: dict[int, frozenset[int]]) -> list[tuple]:
    outside = set(range(N)) - S
    found = []
    for omitted in S:
        for p, q in itertools.permutations(outside, 2):
            if omitted not in lists[p] or pair(p, q) not in H_EDGES:
                continue
            remaining = outside - {p, q}
            for path_order in range(2, len(remaining) + 1, 2):
                for path in itertools.permutations(remaining, path_order):
                    if any(omitted in lists[v] for v in path):
                        continue
                    if (
                        pair(q, path[0]) in H_EDGES
                        and pair(q, path[-1]) in H_EDGES
                        and all(
                            pair(path[i], path[i + 1]) in H_EDGES
                            for i in range(len(path) - 1)
                        )
                    ):
                        found.append((omitted, p, q, path))
    return found


def main() -> None:
    family, rounds = restricted_kernel()
    obligations = family_audit(family)
    lists = response_lists(family)
    assert lists == DESIRED_LISTS
    assert len(family) == 65
    assert rounds == (8, 1, 4)
    assert obligations == 390

    # X=1 is the lollipop variable for the component R-T-Q, and Y is the
    # variable for V0-V1.  The two cross edges give these clauses.
    base_assignments = [
        (x_value, y_value)
        for x_value, y_value in itertools.product((0, 1), repeat=2)
        if (x_value == 0 or y_value == 1)
        and (x_value == 0 or y_value == 0)
    ]
    augmented_assignments = [
        assignment for assignment in base_assignments if assignment[0] == 1
    ]
    assert base_assignments == [(0, 0), (0, 1)]
    assert not augmented_assignments

    # Direct list-color enumeration is an independent semantic check.
    assert proper_h_coloring_count(lists, include_x=False) == 2
    lists_with_x_fixed = dict(lists)
    lists_with_x_fixed[X] = frozenset((0,))
    assert proper_h_coloring_count(lists_with_x_fixed, include_x=True) == 0

    embeddings = fan_embeddings(lists)
    assert not embeddings
    result = {
        "status": "PASS",
        "labeled_graph6": "HFzvvn{",
        "canonical_graph6": "Hvzax|~",
        "H_edges": [list(edge) for edge in sorted(H_EDGES)],
        "family_states": len(family),
        "attack_obligations": obligations,
        "restricted_kernel_deletion_rounds": list(rounds),
        "parameters": {
            "gamma": exact_parameter("gamma"),
            "alpha": exact_parameter("alpha"),
            "gamma_infinity": 3,
            "theta": 3,
        },
        "response_lists": {
            str(vertex): sorted(colors) for vertex, colors in lists.items()
        },
        "base_boolean_assignments": [list(item) for item in base_assignments],
        "augmented_boolean_assignments": augmented_assignments,
        "odd_fan_path_embeddings": embeddings,
    }
    assert result["parameters"] == {
        "gamma": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

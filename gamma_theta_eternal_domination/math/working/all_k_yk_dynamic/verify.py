#!/usr/bin/env python3
"""Independent finite control for the all-k Y_k dynamic note.

This script reconstructs the seven-vertex clean-singleton example from its
edge list.  It uses exhaustive subsets, a greatest-fixed-point eternal
kernel, and a separate backtracking complement-coloring routine.
"""

from itertools import combinations


N = 7
VERTICES = frozenset(range(N))
EDGES = frozenset(
    {
        (0, 5),
        (2, 5),
        (2, 6),
        (3, 4),
        (4, 6),
    }
)
S = frozenset({0, 1, 2, 3})
T = frozenset({0, 1, 2, 4})
Z = 4
X = 5


def edge(u, v):
    return tuple(sorted((u, v))) in EDGES


def dominates(state, vertices=VERTICES):
    state = frozenset(state)
    return all(v in state or any(edge(v, u) for u in state) for v in vertices)


def independent(state):
    return all(not edge(u, v) for u, v in combinations(state, 2))


def domination_number(vertices=VERTICES):
    vertices = frozenset(vertices)
    for size in range(len(vertices) + 1):
        for state in combinations(sorted(vertices), size):
            if all(
                v in state or any(edge(v, u) for u in state)
                for v in vertices
            ):
                return size
    raise AssertionError("finite domination search failed")


def independence_number(vertices=VERTICES):
    vertices = tuple(sorted(vertices))
    return max(
        len(state)
        for size in range(len(vertices) + 1)
        for state in combinations(vertices, size)
        if independent(state)
    )


def greatest_kernel(k, vertices=VERTICES):
    vertices = frozenset(vertices)
    states = {
        frozenset(state)
        for state in combinations(sorted(vertices), k)
        if all(
            v in state or any(edge(v, u) for u in state)
            for v in vertices
        )
    }
    rounds = []
    while True:
        doomed = set()
        for state in states:
            for attack in vertices - state:
                if not any(
                    frozenset((state - {guard}) | {attack}) in states
                    for guard in state
                    if edge(guard, attack)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return states, rounds
        states -= doomed
        rounds.append(len(doomed))


def eternal_number(vertices=VERTICES):
    for k in range(1, len(vertices) + 1):
        kernel, _ = greatest_kernel(k, vertices)
        if kernel:
            return k
    raise AssertionError("finite eternal search failed")


def complement_colorable(k, vertices=VERTICES):
    vertices = tuple(sorted(vertices))
    order = sorted(
        vertices,
        key=lambda v: -sum(v != w and not edge(v, w) for w in vertices),
    )
    colors = {}

    def visit(pos):
        if pos == len(order):
            return True
        v = order[pos]
        for color in range(k):
            if all(
                colors.get(w) != color
                for w in vertices
                if w != v and not edge(v, w)
            ):
                colors[v] = color
                if visit(pos + 1):
                    return True
                del colors[v]
        return False

    return visit(0)


def theta(vertices=VERTICES):
    for k in range(1, len(vertices) + 1):
        if complement_colorable(k, vertices):
            return k
    raise AssertionError("finite coloring search failed")


def static_list(reference, target, vertices=VERTICES):
    reference = frozenset(reference)
    vertices = frozenset(vertices)
    result = set()
    for guard in reference:
        successor = (reference - {guard}) | {target}
        if edge(guard, target) and all(
            v in successor or any(edge(v, u) for u in successor)
            for v in vertices
        ):
            result.add(guard)
    return frozenset(result)


def family_list(reference, target, family):
    reference = frozenset(reference)
    return frozenset(
        guard
        for guard in reference
        if edge(guard, target)
        and frozenset((reference - {guard}) | {target}) in family
    )


def assert_closed(family, vertices=VERTICES):
    vertices = frozenset(vertices)
    obligations = 0
    for state in family:
        assert all(
            v in state or any(edge(v, u) for u in state)
            for v in vertices
        )
        for attack in vertices - state:
            obligations += 1
            assert any(
                frozenset((state - {guard}) | {attack}) in family
                for guard in state
                if edge(guard, attack)
            )
    return obligations


def main():
    kernel, rounds = greatest_kernel(4)
    expected = {
        frozenset(state)
        for state in (
            (0, 1, 2, 3),
            (0, 1, 2, 4),
            (0, 1, 3, 6),
            (0, 1, 4, 6),
            (1, 2, 3, 5),
            (1, 2, 4, 5),
            (1, 3, 5, 6),
            (1, 4, 5, 6),
        )
    }
    assert kernel == expected
    assert rounds == [2]
    obligations = assert_closed(kernel)
    assert obligations == 24

    assert independent(S)
    assert independent(T)
    assert S in kernel and T in kernel
    assert not edge(Z, X)

    assert static_list(S, Z) == frozenset({3})
    assert family_list(S, Z, kernel) == frozenset({3})
    assert static_list(S, X) == frozenset({0})
    assert family_list(S, X, kernel) == frozenset({0})
    assert static_list(T, X) == frozenset({0, 2})
    assert family_list(T, X, kernel) == frozenset({0})

    # Vertex 6 is the old defect for the 2-swap, and z=4 repairs it.
    old_swap = frozenset((S - {2}) | {X})
    new_swap = frozenset((T - {2}) | {X})
    assert not dominates(old_swap)
    assert 6 not in old_swap
    assert not any(edge(6, u) for u in old_swap)
    assert edge(6, Z)
    assert dominates(new_swap)

    full_parameters = (
        domination_number(),
        independence_number(),
        eternal_number(),
        theta(),
    )
    assert full_parameters == (3, 4, 4, 4)

    projected_vertices = frozenset(
        v for v in VERTICES - {Z} if not edge(v, Z)
    )
    assert projected_vertices == frozenset({0, 1, 2, 5})
    projected_parameters = (
        domination_number(projected_vertices),
        independence_number(projected_vertices),
        eternal_number(projected_vertices),
        theta(projected_vertices),
    )
    assert projected_parameters == (2, 3, 3, 3)

    projected_family = {
        state - {Z}
        for state in kernel
        if Z in state and state - {Z} <= projected_vertices
    }
    assert projected_family == {
        frozenset({0, 1, 2}),
        frozenset({1, 2, 5}),
    }
    projected_obligations = assert_closed(
        projected_family, projected_vertices
    )
    assert projected_obligations == 2

    print("PASS: clean singleton static-repair control")
    print(f"full_parameters={full_parameters}")
    print(f"projected_parameters={projected_parameters}")
    print(f"kernel_states={len(kernel)} obligations={obligations}")
    print(
        "lists="
        f"S:z{sorted(static_list(S, Z))},"
        f"S:x{sorted(static_list(S, X))},"
        f"T:x_static{sorted(static_list(T, X))},"
        f"T:x_family{sorted(family_list(T, X, kernel))}"
    )
    print(
        f"projected_states={len(projected_family)} "
        f"projected_obligations={projected_obligations}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent finite audit of the inactive-path induction.

This is not used as a substitute for the proof in NOTE.md.  It checks the
blocked-or-absent response calculus behind the leaf-extension proof, the
closed form of the local greatest kernel on paths through a user-selected
length, and the even-parity product-family controls.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections.abc import Iterable


State = tuple[int, int, int]
Edge = tuple[int, int]


def state(vertices: Iterable[int]) -> State:
    answer = tuple(sorted(vertices))
    if len(answer) != 3 or len(set(answer)) != 3:
        raise ValueError(f"not a three-set: {answer}")
    return answer


def edge(first: int, second: int) -> Edge:
    if first == second:
        raise ValueError("loop")
    return tuple(sorted((first, second)))


def response_is_blocked_or_dead(
    current: State,
    attacked: int,
    guard: int,
    forced_nonedges: set[Edge],
    dead: set[State],
) -> bool:
    if edge(guard, attacked) in forced_nonedges:
        return True
    successor = state((set(current) - {guard}) | {attacked})
    return successor in dead


def valid_death_step(
    current: State,
    attacked: int,
    forced_nonedges: set[Edge],
    dead: set[State],
) -> bool:
    return attacked not in current and all(
        response_is_blocked_or_dead(
            current, attacked, guard, forced_nonedges, dead
        )
        for guard in current
    )


def saturate(
    vertices: tuple[int, ...],
    forced_nonedges: set[Edge],
    initial_dead: set[State],
) -> tuple[set[State], int]:
    all_states = tuple(itertools.combinations(vertices, 3))
    dead = set(initial_dead)
    rounds = 0
    while True:
        new_dead: set[State] = set()
        for current in all_states:
            if current in dead:
                continue
            for attacked in vertices:
                if valid_death_step(
                    current, attacked, forced_nonedges, dead
                ):
                    new_dead.add(current)
                    break
        if not new_dead:
            return dead, rounds
        dead.update(new_dead)
        rounds += 1


def path_instance(
    path_length: int,
) -> tuple[
    tuple[int, ...],
    set[int],
    set[int],
    set[int],
    int,
    set[Edge],
    set[State],
]:
    rim = tuple(range(path_length + 1))
    witness_start = path_length + 1
    witnesses = tuple(
        range(witness_start, witness_start + path_length)
    )
    target = witness_start + path_length
    vertices = tuple(range(target + 1))
    even_rim = set(rim[0::2])
    odd_rim = set(rim[1::2])
    neutral = set(witnesses) | {target}
    forced_nonedges: set[Edge] = set()
    inactive_successors: set[State] = set()
    for index, witness in enumerate(witnesses):
        left = rim[index]
        right = rim[index + 1]
        forced_nonedges.update(
            {
                edge(left, right),
                edge(left, witness),
                edge(right, witness),
            }
        )
        inactive_successors.update(
            {
                state((left, witness, target)),
                state((right, witness, target)),
            }
        )
    return (
        vertices,
        even_rim,
        odd_rim,
        neutral,
        target,
        forced_nonedges,
        inactive_successors,
    )


def audit_path_kernels(max_path_length: int) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for length in range(1, max_path_length + 1):
        (
            vertices,
            even_rim,
            odd_rim,
            _neutral,
            target,
            forced_nonedges,
            inactive_successors,
        ) = path_instance(length)
        all_states = set(itertools.combinations(vertices, 3))
        expected_dead = {
            current
            for current in all_states
            if not (
                set(current) & even_rim and set(current) & odd_rim
            )
        }
        dead, support_rounds = saturate(
            vertices, forced_nonedges, inactive_successors
        )
        assert dead == expected_dead

        endpoint = state((0, length, target))
        endpoint_dead, endpoint_rounds = saturate(
            vertices,
            forced_nonedges,
            inactive_successors | {endpoint},
        )
        named_states = {
            state((index, index + 1, length + 1 + index))
            for index in range(length)
        }
        if length % 2:
            assert endpoint_dead == all_states
            assert named_states <= endpoint_dead
        else:
            assert endpoint_dead == expected_dead
            assert not (named_states & endpoint_dead)
        results.append(
            {
                "path_length": length,
                "order": len(vertices),
                "state_count": len(all_states),
                "support_dead_count": len(dead),
                "support_rounds": support_rounds,
                "endpoint_dead_count": len(endpoint_dead),
                "endpoint_rounds": endpoint_rounds,
                "parity": "odd" if length % 2 else "even",
            }
        )
    return results


def audit_leaf_extension() -> dict[str, object]:
    """Check the exact five-layer schematic leaf argument.

    Three generic vertices per old class suffice: a state and one attack
    mention at most four vertices, while the proof treats the named
    endpoint/witness/target vertices separately.
    """

    w, z, h, y, p, x = range(6)
    generic_a = set(range(6, 9))
    generic_b = set(range(9, 12))
    generic_n = set(range(12, 15))
    old_a = {z} | generic_a
    old_b = {w} | generic_b
    old_n = {h, x} | generic_n
    old_vertices = old_a | old_b | old_n
    new_a = set(old_a)
    new_b = set(old_b) | {y}
    vertices = tuple(range(15))
    all_states = set(itertools.combinations(vertices, 3))
    forced_nonedges = {
        edge(w, z),
        edge(w, h),
        edge(z, h),
        edge(z, y),
        edge(z, p),
        edge(y, p),
    }

    old_support_dead = {
        current
        for current in itertools.combinations(sorted(old_vertices), 3)
        if not (
            set(current) & old_a and set(current) & old_b
        )
    }
    dead = set(old_support_dead)
    new_boundaries = {state((z, p, x)), state((y, p, x))}
    dead.update(new_boundaries)

    layer_counts: list[int] = []

    # Layer 1: every three-set in the private star of z is blocked.
    layer = set(itertools.combinations(sorted((w, h, y, p)), 3))
    for current in layer:
        assert valid_death_step(
            current, z, forced_nonedges, dead
        )
    dead.update(layer)
    layer_counts.append(len(layer))

    # Layer 2: four bridge forms for every old vertex lacking old A.
    old_no_a = old_b | old_n
    layer = set()
    for item in old_no_a:
        for current, attacked in (
            ((item, h, p), w),
            ((item, h, y), w),
            ((item, w, p), h),
            ((item, w, y), h),
        ):
            if len(set(current)) == 3:
                normalized = state(current)
                if normalized not in dead:
                    assert valid_death_step(
                        normalized, attacked, forced_nonedges, dead
                    )
                    layer.add(normalized)
    dead.update(layer)
    layer_counts.append(len(layer))

    # Layer 3: all new three-sets lacking A.
    layer = {
        current
        for current in all_states
        if set(current) <= old_no_a | {p, y}
        and (p in current or y in current)
        and current not in dead
    }
    for current in layer:
        assert w not in current
        assert valid_death_step(
            current, w, forced_nonedges, dead
        )
    dead.update(layer)
    layer_counts.append(len(layer))

    # Layer 4: the seed {z,h,p}, then all {z,p,d}.
    layer = set()
    seed = state((z, h, p))
    assert valid_death_step(seed, x, forced_nonedges, dead)
    dead.add(seed)
    layer.add(seed)
    old_no_b = old_a | old_n
    for item in old_no_b - {z}:
        current = state((z, p, item))
        if current in dead:
            continue
        attacked = h
        assert valid_death_step(
            current, attacked, forced_nonedges, dead
        )
        dead.add(current)
        layer.add(current)
    layer_counts.append(len(layer))

    # Layer 5: every remaining new three-set lacking B.
    layer = {
        current
        for current in all_states
        if set(current) <= old_no_b | {p}
        and p in current
        and current not in dead
    }
    for current in layer:
        assert z not in current
        assert valid_death_step(
            current, z, forced_nonedges, dead
        )
    dead.update(layer)
    layer_counts.append(len(layer))

    required = {
        current
        for current in all_states
        if not (set(current) & new_a and set(current) & new_b)
        and (
            set(current) <= old_vertices
            or p in current
            or y in current
        )
    }
    assert required <= dead
    return {
        "abstract_order": len(vertices),
        "abstract_state_count": len(all_states),
        "old_support_dead_count": len(old_support_dead),
        "new_boundary_count": len(new_boundaries),
        "layer_counts": layer_counts,
        "required_dead_count": len(required),
        "verified_dead_count": len(dead & required),
    }


def product_family_control(path_length: int) -> dict[str, object]:
    (
        vertices,
        even_rim,
        odd_rim,
        neutral,
        target,
        forced_nonedges,
        inactive_successors,
    ) = path_instance(path_length)
    graph_edges = {
        edge(first, second)
        for first, second in itertools.combinations(vertices, 2)
        if edge(first, second) not in forced_nonedges
    }
    family = {
        state((first, second, third))
        for first in even_rim
        for second in odd_rim
        for third in neutral
    }
    assert family
    for current in family:
        for vertex in vertices:
            assert vertex in current or any(
                edge(guard, vertex) in graph_edges
                for guard in current
            )
        for attacked in vertices:
            if attacked in current:
                continue
            responses = []
            for guard in current:
                if edge(guard, attacked) not in graph_edges:
                    continue
                successor = state(
                    (set(current) - {guard}) | {attacked}
                )
                if successor in family:
                    responses.append((guard, successor))
            assert responses
    assert not (family & inactive_successors)
    named_states = {
        state((index, index + 1, path_length + 1 + index))
        for index in range(path_length)
    }
    assert named_states <= family
    endpoint = state((0, path_length, target))
    assert (endpoint in family) == bool(path_length % 2)
    return {
        "path_length": path_length,
        "order": len(vertices),
        "family_size": len(family),
        "endpoint_in_family": endpoint in family,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-path-length", type=int, default=25)
    arguments = parser.parse_args()
    if arguments.max_path_length < 2:
        raise SystemExit("--max-path-length must be at least 2")
    path_results = audit_path_kernels(arguments.max_path_length)
    leaf_result = audit_leaf_extension()
    controls = [
        product_family_control(length)
        for length in range(1, min(arguments.max_path_length, 12) + 1)
    ]
    payload = {
        "schema": "inactive-odd-path-induction-audit-v1",
        "classification": "INDEPENDENT-CHECK-OF-HUMAN-PROOF",
        "max_path_length": arguments.max_path_length,
        "path_results": path_results,
        "leaf_extension": leaf_result,
        "product_family_controls": controls,
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()
    payload["result_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

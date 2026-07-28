#!/usr/bin/env python3
"""Standalone exact checker for the bridge-turning-ridge controls.

The checker imports no campaign evaluator.  It uses ordinary frozensets,
explicit one-guard successors, greatest-fixed-point deletion, exhaustive
subset predicates, and a direct clique-partition recursion.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "result.json"


def decode_graph6(record: str) -> tuple[frozenset[int], frozenset[frozenset[int]]]:
    raw = record.encode("ascii")
    if not raw or not 63 <= raw[0] <= 125:
        raise ValueError(record)
    order = raw[0] - 63
    bits = [
        ((byte - 63) >> shift) & 1
        for byte in raw[1:]
        for shift in range(5, -1, -1)
    ]
    need = order * (order - 1) // 2
    if len(bits) < need or any(bits[need:]):
        raise ValueError("bad graph6 payload")
    edges: set[frozenset[int]] = set()
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.add(frozenset((low, high)))
            cursor += 1
    return frozenset(range(order)), frozenset(edges)


def adjacent(edges: frozenset[frozenset[int]], left: int, right: int) -> bool:
    return left != right and frozenset((left, right)) in edges


def subsets(vertices: frozenset[int], size: int):
    for choice in itertools.combinations(sorted(vertices), size):
        yield frozenset(choice)


def independent(state: frozenset[int], edges: frozenset[frozenset[int]]) -> bool:
    return all(
        not adjacent(edges, left, right)
        for left, right in itertools.combinations(sorted(state), 2)
    )


def dominates(
    state: frozenset[int],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> bool:
    return all(
        target in state
        or any(adjacent(edges, guard, target) for guard in state)
        for target in vertices
    )


def maximal_independent(
    state: frozenset[int],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> bool:
    return independent(state, edges) and all(
        any(adjacent(edges, inside, outside) for inside in state)
        for outside in vertices - state
    )


def minimum_size(vertices: frozenset[int], predicate) -> int:
    for size in range(1, len(vertices) + 1):
        if any(predicate(state) for state in subsets(vertices, size)):
            return size
    raise AssertionError("minimum not found")


def maximum_size(vertices: frozenset[int], predicate) -> int:
    for size in range(len(vertices), 0, -1):
        if any(predicate(state) for state in subsets(vertices, size)):
            return size
    raise AssertionError("maximum not found")


def clique_partition_number(
    vertices: frozenset[int], edges: frozenset[frozenset[int]]
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    ordered = sorted(vertices)
    best = len(vertices) + 1
    witness: tuple[tuple[int, ...], ...] | None = None
    blocks: list[list[int]] = []

    def visit(position: int) -> None:
        nonlocal best, witness
        if len(blocks) >= best:
            return
        if position == len(ordered):
            best = len(blocks)
            witness = tuple(tuple(block) for block in blocks)
            return
        vertex = ordered[position]
        for block in blocks:
            if all(adjacent(edges, vertex, member) for member in block):
                block.append(vertex)
                visit(position + 1)
                block.pop()
        blocks.append([vertex])
        visit(position + 1)
        blocks.pop()

    visit(0)
    assert witness is not None
    return best, witness


def legal_successors(
    state: frozenset[int],
    attack: int,
    edges: frozenset[frozenset[int]],
) -> tuple[tuple[int, frozenset[int]], ...]:
    return tuple(
        (guard, frozenset((state - {guard}) | {attack}))
        for guard in sorted(state)
        if adjacent(edges, guard, attack)
    )


def greatest_family(
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
    size: int,
) -> tuple[frozenset[frozenset[int]], tuple[int, ...]]:
    family = frozenset(
        state
        for state in subsets(vertices, size)
        if dominates(state, vertices, edges)
    )
    stages = [len(family)]
    while True:
        kept = frozenset(
            state
            for state in family
            if all(
                any(
                    successor in family
                    for _, successor in legal_successors(state, attack, edges)
                )
                for attack in vertices - state
            )
        )
        if kept == family:
            return family, tuple(stages)
        family = kept
        stages.append(len(family))


def family_response_list(
    reference: frozenset[int],
    target: int,
    family: frozenset[frozenset[int]],
    edges: frozenset[frozenset[int]],
) -> frozenset[int]:
    return frozenset(
        guard
        for guard in reference
        if adjacent(edges, guard, target)
        and frozenset((reference - {guard}) | {target}) in family
    )


def obligation_digest(
    family: frozenset[frozenset[int]],
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> tuple[int, str]:
    rows = []
    for state in sorted(family, key=lambda value: tuple(sorted(value))):
        assert dominates(state, vertices, edges)
        for attack in sorted(vertices - state):
            successors = tuple(
                (guard, tuple(sorted(successor)))
                for guard, successor in legal_successors(state, attack, edges)
                if successor in family
            )
            assert successors
            rows.append(
                json.dumps(
                    {
                        "state": tuple(sorted(state)),
                        "attack": attack,
                        "successors": successors,
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                )
            )
    payload = ("\n".join(rows) + "\n").encode()
    return len(rows), hashlib.sha256(payload).hexdigest()


def parameter_summary(
    vertices: frozenset[int],
    edges: frozenset[frozenset[int]],
) -> dict[str, object]:
    gamma = minimum_size(
        vertices, lambda state: dominates(state, vertices, edges)
    )
    alpha = maximum_size(vertices, lambda state: independent(state, edges))
    independent_domination = minimum_size(
        vertices,
        lambda state: maximal_independent(state, vertices, edges),
    )
    eternal = next(
        size
        for size in range(1, len(vertices) + 1)
        if greatest_family(vertices, edges, size)[0]
    )
    theta, partition = clique_partition_number(vertices, edges)
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": eternal,
        "theta": theta,
        "clique_partition": partition,
    }


def check_control(
    record: str,
    expected_order: int,
    expected_family_size: int,
    z: int,
    q: int,
    q_list: frozenset[int],
) -> dict[str, object]:
    vertices, edges = decode_graph6(record)
    assert len(vertices) == expected_order
    reference = frozenset((0, 1, 2))
    u, v, w = 1, 0, 2
    family, stages = greatest_family(vertices, edges, 3)
    assert len(family) == expected_family_size
    lists = {
        target: family_response_list(reference, target, family, edges)
        for target in sorted(vertices - reference)
    }
    assert lists[z] == frozenset((u, w))
    assert lists[q] == q_list

    def h_edge(left: int, right: int) -> bool:
        return left != right and not adjacent(edges, left, right)

    ridge = frozenset(
        target
        for target in vertices
        if h_edge(w, target) and h_edge(z, target)
    )
    assert ridge == frozenset((v, q))
    assert all(
        adjacent(edges, left, right)
        for left, right in itertools.combinations(sorted(ridge), 2)
    )
    ridge_states = {
        target: frozenset((w, z, target)) for target in ridge
    }
    assert all(state in family for state in ridge_states.values())
    for left, right in itertools.permutations(ridge, 2):
        state = ridge_states[left]
        successors = {
            guard: successor
            for guard, successor in legal_successors(state, right, edges)
            if successor in family
        }
        assert successors == {left: ridge_states[right]}

    obligations, obligation_hash = obligation_digest(family, vertices, edges)
    parameters = parameter_summary(vertices, edges)
    assert {
        key: parameters[key]
        for key in ("gamma", "i", "alpha", "gamma_infinity", "theta")
    } == {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    return {
        "graph6": record,
        "order": len(vertices),
        "size": len(edges),
        "edges": tuple(tuple(sorted(edge)) for edge in sorted(edges, key=sorted)),
        "parameters": parameters,
        "reference": tuple(sorted(reference)),
        "response_lists": {
            str(target): tuple(sorted(values)) for target, values in lists.items()
        },
        "turning_data": {
            "u_v_w_z_q": (u, v, w, z, q),
            "ridge": tuple(sorted(ridge)),
            "ridge_states": {
                str(target): tuple(sorted(state))
                for target, state in ridge_states.items()
            },
        },
        "greatest_family": {
            "stage_sizes": stages,
            "state_count": len(family),
            "attack_obligations": obligations,
            "obligation_sha256": obligation_hash,
        },
    }


def main() -> None:
    result = {
        "schema": "bridge-turning-ridge-controls-v1",
        "model": (
            "attacks only at unoccupied vertices; exactly one adjacent guard "
            "moves; every retained state dominates"
        ),
        "controls": {
            "external_singleton": check_control(
                "FCXfO", 7, 18, z=4, q=3, q_list=frozenset((0,))
            ),
            "external_two_list": check_control(
                "HEhbtjK", 9, 48, z=5, q=3, q_list=frozenset((0, 1))
            ),
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(payload, encoding="utf-8")
    print(payload, end="")
    print("result_sha256", hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()

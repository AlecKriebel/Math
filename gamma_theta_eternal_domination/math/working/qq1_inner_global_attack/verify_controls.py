#!/usr/bin/env python3
"""Standalone exact audit for the QQ1 simultaneous-witness controls.

This verifier deliberately does not import the SAT search code or either
campaign evaluator.  It uses ordinary Python sets, exhaustive subset
checks, an explicit greatest-fixed-point deletion, and a small exact
complement-coloring search.
"""

from __future__ import annotations

import hashlib
import itertools
import json


CONTROLS = {
    "two-witness": "OslallyN]z~r|^{~|^|~^",
    "repaired-pw": "OslallyN]fv|y~v^}n}{n",
}

LABELS = {
    "u": 0,
    "x": 1,
    "p": 2,
    "q": 3,
    "r": 4,
    "b": 5,
    "c": 6,
    "d": 7,
    "w": 8,
    "z": 9,
}


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(char) - 63 for char in record]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only short graph6 records are supported")
    order = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    needed = order * (order - 1) // 2
    if len(bits) < needed or any(bits[needed:]):
        raise ValueError("truncated or nonzero-padded graph6 record")
    graph = [set() for _ in range(order)]
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                graph[left].add(right)
                graph[right].add(left)
            cursor += 1
    return tuple(frozenset(row) for row in graph)


def encode_graph6(graph: tuple[frozenset[int], ...]) -> str:
    order = len(graph)
    if order > 62:
        raise ValueError("only short graph6 records are supported")
    bits = []
    for right in range(1, order):
        for left in range(right):
            bits.append(int(right in graph[left]))
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def independent(graph, state) -> bool:
    return all(
        right not in graph[left]
        for left, right in itertools.combinations(state, 2)
    )


def dominates(graph, state) -> bool:
    occupied = frozenset(state)
    return all(
        vertex in occupied or bool(graph[vertex] & occupied)
        for vertex in range(len(graph))
    )


def domination_number(graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            dominates(graph, state)
            for state in itertools.combinations(range(len(graph)), size)
        ):
            return size
    raise AssertionError("finite graph has no dominating set")


def independence_number(graph) -> int:
    for size in range(len(graph), 0, -1):
        if any(
            independent(graph, state)
            for state in itertools.combinations(range(len(graph)), size)
        ):
            return size
    return 0


def independent_domination_number(graph) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            independent(graph, state) and dominates(graph, state)
            for state in itertools.combinations(range(len(graph)), size)
        ):
            return size
    raise AssertionError("a maximal independent set must exist")


def kernel_with_ranks(graph, guard_count: int):
    configurations = {
        frozenset(state)
        for state in itertools.combinations(range(len(graph)), guard_count)
        if dominates(graph, state)
    }
    ranks: dict[frozenset[int], int] = {}
    round_number = 1
    while True:
        removed = set()
        for state in configurations:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and state - {guard} | {target} in configurations
                    for guard in state
                ):
                    removed.add(state)
                    break
        if not removed:
            return configurations, ranks
        for state in removed:
            ranks[state] = round_number
        configurations -= removed
        round_number += 1


def eternal_domination_number(graph) -> int:
    for guard_count in range(1, len(graph) + 1):
        family, _ = kernel_with_ranks(graph, guard_count)
        if family:
            return guard_count
    raise AssertionError("the all-vertex state is eternal")


def complement_coloring(graph, color_count: int):
    order = len(graph)
    complement = [
        set(range(order)) - {vertex} - set(graph[vertex])
        for vertex in range(order)
    ]
    colors = [-1] * order

    def recurse(colored: int) -> bool:
        if colored == order:
            return True
        uncolored = [vertex for vertex in range(order) if colors[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in complement[item]
                        if colors[neighbor] >= 0
                    }
                ),
                len(complement[item]),
                -item,
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in complement[vertex]
            if colors[neighbor] >= 0
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if recurse(colored + 1):
                return True
        colors[vertex] = -1
        return False

    if not recurse(0):
        return None
    return tuple(
        tuple(vertex for vertex in range(order) if colors[vertex] == color)
        for color in range(color_count)
    )


def clique_cover_number(graph) -> tuple[int, tuple[tuple[int, ...], ...]]:
    for count in range(1, len(graph) + 1):
        coloring = complement_coloring(graph, count)
        if coloring is not None:
            return count, coloring
    raise AssertionError("singleton cliques always cover a finite graph")


def common_nonneighbors(graph, left: int, right: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (left, right)
        and vertex not in graph[left]
        and vertex not in graph[right]
    )


def dominating_pairs(graph) -> tuple[tuple[int, int], ...]:
    return tuple(
        pair
        for pair in itertools.combinations(range(len(graph)), 2)
        if dominates(graph, pair)
    )


def move(state, guard, target):
    state = frozenset(state)
    if guard not in state or target in state:
        raise AssertionError("displayed attack is occupied or mover absent")
    return state - {guard} | {target}


def audit_bridge_bookkeeping():
    U = frozenset(("u", "b", "c"))
    side_b = move(U, "b", "d")
    side_c = move(U, "c", "d")
    A = frozenset(("u", "x", "d"))
    if move(side_b, "c", "x") != A:
        raise AssertionError("first side route does not reach A")
    if move(side_c, "b", "x") != A:
        raise AssertionError("second side route does not reach A")
    K = move(A, "x", "w")
    bridge = move(K, "d", "z")
    losing_side = move(K, "w", "z")
    omitted = move(losing_side, "z", "r")
    nondominating = move(losing_side, "u", "r")
    if K != frozenset(("u", "d", "w")):
        raise AssertionError("wrong hot state")
    if bridge != frozenset(("u", "w", "z")):
        raise AssertionError("wrong bridge state")
    if losing_side != frozenset(("u", "d", "z")):
        raise AssertionError("wrong alternate z-successor")
    if omitted != frozenset(("u", "d", "r")):
        raise AssertionError("wrong omitted successor")
    if nondominating != frozenset(("r", "d", "z")):
        raise AssertionError("wrong successor missing x")
    return {
        "retained_target": sorted(bridge),
        "alternate_if_target_omitted": sorted(losing_side),
        "alternate_attack": "r",
        "alternate_successors": {
            "z_to_r_omitted": sorted(omitted),
            "u_to_r_misses_x": sorted(nondominating),
        },
        "exactly_one_guard_moves": True,
        "all_attacks_unoccupied": True,
    }


def audit_control(label: str, record: str):
    graph = decode_graph6(record)
    if encode_graph6(graph) != record:
        raise AssertionError("graph6 round trip failed")
    u, x, p, q, r, b, c, d, w, z = range(10)
    required_edges = (
        (u, x),
        (u, p),
        (u, q),
        (u, r),
        (u, d),
        (p, r),
        (q, r),
        (p, b),
        (q, c),
        (x, b),
        (x, c),
        (b, c),
        (d, p),
        (d, q),
        (d, b),
        (d, c),
        (w, x),
        (w, r),
        (z, d),
        (z, w),
    )
    required_nonedges = (
        (x, p),
        (x, q),
        (p, q),
        (x, r),
        (u, b),
        (b, r),
        (b, q),
        (u, c),
        (c, r),
        (c, p),
        (x, d),
        (r, d),
        (u, w),
        (d, w),
        (u, z),
        (x, z),
    )
    if any(right not in graph[left] for left, right in required_edges):
        raise AssertionError(f"{label}: missing named edge")
    if any(right in graph[left] for left, right in required_nonedges):
        raise AssertionError(f"{label}: forbidden named edge")

    family, ranks = kernel_with_ranks(graph, 3)
    named_states = {
        "T": frozenset((x, p, q)),
        "U": frozenset((u, b, c)),
        "R": frozenset((r, b, c)),
        "I": frozenset((x, r, d)),
        "A": frozenset((u, x, d)),
        "K": frozenset((u, d, w)),
        "E": frozenset((x, d, w)),
        "F": frozenset((r, d, w)),
        "bridge": frozenset((u, w, z)),
        "ux_ridge": frozenset((u, x, z)),
    }
    if not all(state in family for state in named_states.values()):
        raise AssertionError(f"{label}: missing retained named state")
    B = frozenset((u, p, q))
    O = frozenset((u, r, d))
    if ranks.get(B) != 1 or ranks.get(O) != 3:
        raise AssertionError(f"{label}: wrong B/O deletion ranks")

    completions_u_w = common_nonneighbors(graph, u, w)
    completions_d_w = common_nonneighbors(graph, d, w)
    outer = {
        f"{left},{right}": frozenset((left, w, right)) in family
        for left in completions_u_w
        for right in completions_d_w
    }
    if not outer or not all(outer.values()):
        raise AssertionError(f"{label}: unsaturated outer bow tie")

    gamma = domination_number(graph)
    i_value = independent_domination_number(graph)
    alpha = independence_number(graph)
    eternal = eternal_domination_number(graph)
    theta, partition = clique_cover_number(graph)
    vector = [gamma, i_value, alpha, eternal, theta]
    if vector != [2, 3, 3, 3, 3]:
        raise AssertionError(f"{label}: wrong parameter vector {vector}")

    pairs = dominating_pairs(graph)
    expected_pair = (p, w) if label == "two-witness" else (q, 14)
    if expected_pair not in pairs:
        raise AssertionError(f"{label}: missing expected gamma-two pair")
    pw_witnesses = common_nonneighbors(graph, p, w)
    if label == "two-witness" and pw_witnesses:
        raise AssertionError("first control unexpectedly repairs {p,w}")
    if label == "repaired-pw" and pw_witnesses != (15,):
        raise AssertionError("second control has wrong {p,w} witness")

    named_or_auxiliary_pairs = tuple(
        pair for pair in pairs if pair[0] < 10 or pair[1] < 10
    )
    return {
        "label": label,
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(graph),
        "size": sum(map(len, graph)) // 2,
        "parameter_vector_gamma_i_alpha_ginf_theta": vector,
        "greatest_triple_family_size": len(family),
        "rank_B_O": [ranks[B], ranks[O]],
        "common_nonneighbors_ux": list(common_nonneighbors(graph, u, x)),
        "common_nonneighbors_ud": list(common_nonneighbors(graph, u, d)),
        "common_nonneighbors_pw": list(pw_witnesses),
        "completion_set_u_w": list(completions_u_w),
        "completion_set_d_w": list(completions_d_w),
        "outer_mixed_retention": outer,
        "retained_named_states": {
            name: sorted(state) for name, state in named_states.items()
        },
        "dominating_pair_count": len(pairs),
        "dominating_pairs_with_named_endpoint": [
            list(pair) for pair in named_or_auxiliary_pairs
        ],
        "displayed_dominating_pair": list(expected_pair),
        "theta_clique_partition": [list(part) for part in partition],
        "classification": "FIXED_GAMMA2_BOUNDARY_CONTROL",
    }


def evaluate():
    return {
        "schema": "QQ1-inner-global-control-audit-v1",
        "status": "VERIFIED",
        "bridge_bookkeeping": audit_bridge_bookkeeping(),
        "controls": {
            label: audit_control(label, record)
            for label, record in CONTROLS.items()
        },
        "scope": (
            "Exact fixed-graph and symbolic bookkeeping audit only. "
            "The controls refute a proposed local proof shortcut; they "
            "are not counterexamples and no finite UNSAT claim is certified."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))

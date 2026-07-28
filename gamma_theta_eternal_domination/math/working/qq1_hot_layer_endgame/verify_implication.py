#!/usr/bin/env python3
"""Standalone finite audit for the QQ1 hot-layer normal form.

This checker verifies finite response-tree bookkeeping and independently
decodes the fixed boundary controls.  It does not re-prove the accepted
symbolic dependencies C-010, C-108, C-143, C-145, or C-158.
"""

from __future__ import annotations

import hashlib
import itertools
import json


CONTROLS = {
    "dominating-ux": "Mslamztl~fnny~]~_",
    "nondominating-ux": "NslalntvXzn^{~n||^w",
}
HOT_EDGE_CONTROL = "Oslally^v{zn{~y~nn~j~"


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    values = [ord(char) - 63 for char in record]
    if not values or not (0 <= values[0] <= 62):
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


def independent(graph, state) -> bool:
    return all(
        right not in graph[left]
        for left, right in itertools.combinations(state, 2)
    )


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
    raise AssertionError("maximal independent set must exist")


def kernel(graph, size: int):
    family = {
        frozenset(state)
        for state in itertools.combinations(range(len(graph)), size)
        if dominates(graph, state)
    }
    while True:
        removed = set()
        for state in family:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and state - {guard} | {target} in family
                    for guard in state
                ):
                    removed.add(state)
                    break
        if not removed:
            return family
        family.difference_update(removed)


def kernel_with_ranks(graph, size: int):
    family = {
        frozenset(state)
        for state in itertools.combinations(range(len(graph)), size)
        if dominates(graph, state)
    }
    ranks = {}
    round_number = 0
    while True:
        removed = set()
        for state in family:
            for target in range(len(graph)):
                if target in state:
                    continue
                if not any(
                    target in graph[guard]
                    and state - {guard} | {target} in family
                    for guard in state
                ):
                    removed.add(state)
                    break
        if not removed:
            return family, ranks
        round_number += 1
        for state in removed:
            ranks[state] = round_number
        family.difference_update(removed)


def eternal_domination_number(graph) -> int:
    lower = domination_number(graph)
    for size in range(lower, len(graph) + 1):
        if kernel(graph, size):
            return size
    raise AssertionError("all-occupied state is eternal")


def colorable(graph, colors: int) -> bool:
    order = len(graph)
    assignment = [-1] * order
    saturation = [set() for _ in range(order)]
    degrees = [len(graph[v]) for v in range(order)]

    def search(colored: int) -> bool:
        if colored == order:
            return True
        vertex = max(
            (v for v in range(order) if assignment[v] < 0),
            key=lambda v: (len(saturation[v]), degrees[v], -v),
        )
        forbidden = saturation[vertex]
        for color in range(colors):
            if color in forbidden:
                continue
            assignment[vertex] = color
            changed = []
            for neighbor in graph[vertex]:
                if assignment[neighbor] < 0 and color not in saturation[neighbor]:
                    saturation[neighbor].add(color)
                    changed.append(neighbor)
            if search(colored + 1):
                return True
            for neighbor in changed:
                saturation[neighbor].remove(color)
            assignment[vertex] = -1
        return False

    return search(0)


def clique_cover_number(graph) -> int:
    complement = tuple(
        frozenset(
            w
            for w in range(len(graph))
            if w != v and w not in graph[v]
        )
        for v in range(len(graph))
    )
    lower = independence_number(graph)
    for colors in range(lower, len(graph) + 1):
        if colorable(complement, colors):
            return colors
    raise AssertionError("singleton coloring must exist")


def audit_control(label: str, record: str):
    graph = decode_graph6(record)
    u, x, p, q, r, b, c = range(7)
    completions = [
        vertex
        for vertex in range(len(graph))
        if vertex not in (x, r)
        and vertex not in graph[x]
        and vertex not in graph[r]
    ]
    if len(completions) != 1:
        raise AssertionError("C-159 control must have one x,r completion")
    d = completions[0]
    if not all(vertex in graph[d] for vertex in (p, q, b, c)):
        raise AssertionError("completion is not four-hit")
    hot = [
        vertex
        for vertex in range(len(graph))
        if vertex not in (u, d)
        and vertex not in graph[u]
        and vertex not in graph[d]
    ]
    if hot:
        raise AssertionError("C-159 control unexpectedly enters hot layer")
    vector = [
        domination_number(graph),
        independent_domination_number(graph),
        independence_number(graph),
        eternal_domination_number(graph),
        clique_cover_number(graph),
    ]
    if vector != [2, 3, 3, 3, 3]:
        raise AssertionError(f"wrong control parameter vector: {vector}")
    return {
        "label": label,
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(graph),
        "completion_d": d,
        "parameter_vector_gamma_i_alpha_ginf_theta": vector,
        "u_d_pair_dominates": dominates(graph, (u, d)),
        "hot_set": hot,
    }


def audit_hot_edge_control(record: str):
    graph = decode_graph6(record)
    u, x, p, q, r, b, c, d, w, s, t = range(11)
    vector = [
        domination_number(graph),
        independent_domination_number(graph),
        independence_number(graph),
        eternal_domination_number(graph),
        clique_cover_number(graph),
    ]
    if vector != [2, 3, 3, 3, 3]:
        raise AssertionError(f"wrong hot control vector: {vector}")
    family, ranks = kernel_with_ranks(graph, 3)
    hot = [
        vertex
        for vertex in range(len(graph))
        if vertex not in (u, d)
        and vertex not in graph[u]
        and vertex not in graph[d]
    ]
    completions_u_w = [
        vertex
        for vertex in range(len(graph))
        if vertex not in (u, w)
        and vertex not in graph[u]
        and vertex not in graph[w]
    ]
    completions_d_w = [
        vertex
        for vertex in range(len(graph))
        if vertex not in (d, w)
        and vertex not in graph[d]
        and vertex not in graph[w]
    ]
    if hot != [w] or completions_u_w != [b, s] or completions_d_w != [t]:
        raise AssertionError("wrong hot/completion sets in edge control")
    mixed = {
        (left, right): frozenset((left, w, right)) in family
        for left in completions_u_w
        for right in completions_d_w
    }
    if not mixed or not all(mixed.values()):
        raise AssertionError("edge control does not saturate bow-ties")
    named_retained = (
        (x, p, q),
        (u, b, c),
        (r, b, c),
        (x, r, d),
        (u, x, d),
        (u, d, w),
        (x, d, w),
        (r, d, w),
        (u, w, s),
        (d, w, t),
        (s, w, t),
        (b, w, t),
    )
    if not all(frozenset(state) in family for state in named_retained):
        raise AssertionError("edge control is missing a named retained state")
    B = frozenset((u, p, q))
    O = frozenset((u, r, d))
    if [ranks.get(B), ranks.get(O)] != [1, 3]:
        raise AssertionError("wrong B/O ranks in edge control")
    dominating_pairs = sum(
        dominates(graph, pair)
        for pair in itertools.combinations(range(len(graph)), 2)
    )
    if dominating_pairs != 34:
        raise AssertionError("wrong number of dominating pairs")
    return {
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(graph),
        "size": sum(map(len, graph)) // 2,
        "parameter_vector_gamma_i_alpha_ginf_theta": vector,
        "greatest_triple_family_size": len(family),
        "rank_B_O": [ranks[B], ranks[O]],
        "hot_set": hot,
        "completion_set_u_w": completions_u_w,
        "completion_set_d_w": completions_d_w,
        "mixed_retention": {
            f"{left},{right}": retained
            for (left, right), retained in sorted(mixed.items())
        },
        "dominating_pair_count": dominating_pairs,
        "u_d_edge": d in graph[u],
        "classification": "FIXED_GAMMA2_BOUNDARY_CONTROL",
    }


def audit_side_polarization():
    sides = ("b", "c")
    cases = []
    total_assignments = 0
    for response_size in (1, 2):
        for response in itertools.combinations(sides, response_size):
            allowed = []
            for hits in itertools.product((False, True), repeat=2):
                hit = dict(zip(sides, hits))
                if "b" in response and not hit["c"]:
                    continue
                if "c" in response and not hit["b"]:
                    continue
                if not (hit["b"] or hit["c"]):
                    continue
                allowed.append(hit)
            paired = list(itertools.product(allowed, repeat=2))
            total_assignments += len(paired)
            common = {
                side
                for side in sides
                if all(pattern[side] for pair in paired for pattern in pair)
            }
            required_common = {
                "c" if mover == "b" else "b"
                for mover in response
            }
            if not required_common <= common:
                raise AssertionError("side response did not polarize hot layer")
            cases.append(
                {
                    "response_list": list(response),
                    "single_witness_patterns": len(allowed),
                    "two_witness_assignments": len(paired),
                    "forced_common_sides": sorted(required_common),
                }
            )
    if total_assignments != 9:
        raise AssertionError("unexpected polarization assignment count")
    return {
        "response_cases": cases,
        "two_witness_assignments_total": total_assignments,
        "at_least_one_uniform_side": True,
    }


def audit_omitted_attack_tree():
    U = frozenset(("u", "b", "c"))

    def move(state, guard, target):
        if guard not in state or target in state:
            raise AssertionError("invalid one-guard move")
        return state - {guard} | {target}

    R = move(U, "u", "r")
    if R != frozenset(("r", "b", "c")):
        raise AssertionError("wrong U-to-R transition")
    terminal_branches = []
    for side_guard in ("b", "c"):
        X = move(R, side_guard, "w")
        other = "c" if side_guard == "b" else "b"
        # Noncollision branch: s is external to {b,c}.
        bad_at_s = move(X, "r", "s")
        if "u" in bad_at_s or bad_at_s != frozenset(("s", "w", other)):
            raise AssertionError("wrong non-dominating r-successor")
        Y = move(X, other, "s")
        if Y != frozenset(("r", "w", "s")):
            raise AssertionError("side branches do not merge")
        omitted_Q = move(Y, "r", "t")
        bad_at_d = move(Y, "s", "t")
        if omitted_Q != frozenset(("s", "w", "t")):
            raise AssertionError("wrong omitted bow-tie successor")
        if bad_at_d != frozenset(("r", "w", "t")):
            raise AssertionError("wrong final non-dominating successor")
        terminal_branches.append(
            {
                "mover_at_w": side_guard,
                "state_after_w": sorted(X),
                "bad_r_successor_at_s": sorted(bad_at_s),
                "merged_state": sorted(Y),
                "omitted_successor_at_t": sorted(omitted_Q),
                "successor_missing_d": sorted(bad_at_d),
            }
        )
        # Collision branch: s is the side guard left in X.  The state X
        # is already Y, so the attack at s is skipped.
        collision_Y = X
        collision_Q = move(collision_Y, "r", "t")
        collision_bad = move(collision_Y, other, "t")
        if collision_Q != frozenset((other, "w", "t")):
            raise AssertionError("wrong collision omitted successor")
        if collision_bad != frozenset(("r", "w", "t")):
            raise AssertionError("wrong collision terminal successor")
        terminal_branches[-1]["collision_case"] = {
            "s_equals": other,
            "attack_at_s_skipped": True,
            "merged_state": sorted(collision_Y),
            "omitted_successor_at_t": sorted(collision_Q),
            "successor_missing_d": sorted(collision_bad),
        }
    return {
        "initial_state": sorted(U),
        "unique_r_successor": sorted(R),
        "side_branches_checked": terminal_branches,
        "forced_nonedges_used": [
            "ub",
            "uc",
            "uw",
            "us",
            "ws",
            "wt",
            "rd",
            "wd",
            "td",
        ],
        "every_omitted_Q_branch_contradicts_closure": True,
    }


def audit_named_transitions():
    # States use names rather than graph search: this is an exact audit of
    # the one-guard set replacements displayed in Theorems 2.1 and 3.1.
    U = frozenset(("u", "b", "c"))
    A = frozenset(("u", "x", "d"))
    I = frozenset(("x", "r", "d"))
    O = frozenset(("u", "r", "d"))
    w = "w"

    def move(state, guard, target):
        if guard not in state or target in state:
            raise AssertionError("invalid one-guard move")
        return state - {guard} | {target}

    side_b = move(U, "b", "d")
    side_c = move(U, "c", "d")
    if move(side_b, "c", "x") != A:
        raise AssertionError("b-side route does not reach A")
    if move(side_c, "b", "x") != A:
        raise AssertionError("c-side route does not reach A")
    K = move(A, "x", w)
    F = move(K, "u", "r")
    if move(K, w, "r") != O:
        raise AssertionError("wrong omitted K corner")
    if move(F, w, "x") != I:
        raise AssertionError("four-state loop does not close")
    E_from_K = move(K, "u", "x")
    E_from_I = move(I, "r", w)
    if E_from_K != E_from_I:
        raise AssertionError("two constructions of E differ")
    return {
        "side_routes_to_A": 2,
        "retained_loop": [
            sorted(A),
            sorted(K),
            sorted(F),
            sorted(I),
            sorted(A),
        ],
        "shared_E": sorted(E_from_K),
        "omitted_O": sorted(O),
        "exactly_one_guard_per_displayed_move": True,
    }


def evaluate():
    return {
        "schema": "QQ1-hot-layer-endgame-audit-v2",
        "status": "VERIFIED",
        "named_transition_audit": audit_named_transitions(),
        "side_polarization": audit_side_polarization(),
        "omitted_bowtie_attack_tree": audit_omitted_attack_tree(),
        "controls": {
            label: audit_control(label, record)
            for label, record in CONTROLS.items()
        },
        "hot_edge_control": audit_hot_edge_control(HOT_EDGE_CONTROL),
        "scope": (
            "Finite bookkeeping and fixed-control audit only; the all-order "
            "proof is the symbolic argument in NOTE.md."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))

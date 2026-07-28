#!/usr/bin/env python3
"""Finite bookkeeping audit for the canonical QQ1 completion theorem.

This checker does not re-prove C-010, C-064, C-108, C-143, C-146, C-158,
or C-161.  It checks the finite incidence implications used after those
accepted inputs and independently decodes the two fixed C-159 controls.
"""

from __future__ import annotations

import hashlib
import itertools
import json


NAMES = {
    "u": 0,
    "x": 1,
    "p": 2,
    "q": 3,
    "r": 4,
    "b": 5,
    "c": 6,
    "d": 7,
    "w": 8,
}

CONTROLS = {
    "dominating-ux": "Mslamztl~fnny~]~_",
    "nondominating-ux": "NslalntvXzn^{~n||^w",
}


def pair(left: int, right: int) -> frozenset[int]:
    if left == right:
        raise ValueError("loops are not graph pairs")
    return frozenset((left, right))


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


def dominates(graph, state: frozenset[int]) -> bool:
    return all(
        vertex in state or bool(graph[vertex] & state)
        for vertex in range(len(graph))
    )


def kernel(graph, size: int = 3):
    states = tuple(
        frozenset(choice)
        for choice in itertools.combinations(range(len(graph)), size)
    )
    family = {state for state in states if dominates(graph, state)}
    ranks: dict[frozenset[int], int] = {}
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


def symbolic_cold_audit():
    u, x, p, q, r, b, c, d, w = (
        NAMES[name] for name in NAMES
    )
    forced_edges = {
        pair(*edge)
        for edge in (
            (u, x), (u, r), (p, r), (q, r), (p, b), (q, c),
            (x, b), (x, c), (b, c), (u, p), (u, q),
            (d, p), (d, q), (d, b), (d, c),
            # Forced inside the cold-witness proof:
            (d, u), (r, w),
        )
    }
    forced_nonedges = {
        pair(*edge)
        for edge in (
            (x, p), (x, q), (p, q), (x, r),
            (b, u), (b, r), (b, q),
            (c, u), (c, r), (c, p),
            (d, x), (d, r),
            (w, u), (w, x), (w, d),
        )
    }
    if forced_edges & forced_nonedges:
        raise AssertionError("inconsistent symbolic incidence")

    optional = ((w, p), (w, q), (w, b), (w, c))
    audited = 0
    for bits in itertools.product((False, True), repeat=len(optional)):
        edges = set(forced_edges)
        nonedges = set(forced_nonedges)
        for endpoints, present in zip(optional, bits):
            (edges if present else nonedges).add(pair(*endpoints))

        def adjacent(left: int, right: int) -> bool:
            endpoints = pair(left, right)
            if endpoints in edges:
                return True
            if endpoints in nonedges:
                return False
            raise AssertionError(f"unresolved queried pair {sorted(endpoints)}")

        I = frozenset((x, r, d))
        J = frozenset((x, w, d))
        U = frozenset((u, b, c))
        if any(
            adjacent(left, right)
            for state in (I, J)
            for left, right in itertools.combinations(state, 2)
        ):
            raise AssertionError("named completion state is not independent")

        # C-108 excludes x at u from J; w is graph-ineligible.  The
        # retained response is therefore exactly d.  C-064 fixes d and
        # swaps r,w, so the r-successor A from I is omitted.
        eligible_J_u = {
            guard for guard in J if adjacent(guard, u)
        }
        if eligible_J_u != {x, d}:
            raise AssertionError("wrong graph-eligible list at J,u")
        retained_J_u = {d}
        if retained_J_u != {d}:
            raise AssertionError("wrong family list at J,u")
        retained_I_u = {
            w if guard == r else r if guard == w else guard
            for guard in retained_J_u
        }
        if retained_I_u != {d}:
            raise AssertionError("C-064 did not fix the d responder")
        omitted_A = frozenset((u, x, d))

        movers = {guard for guard in U if adjacent(guard, d)}
        if movers != U:
            raise AssertionError("not all U guards can move to d")

        terminal = {}
        for mover in sorted(movers):
            successor = U - {mover} | {d}
            if mover == u:
                misses_r = all(
                    not adjacent(guard, r) for guard in successor
                )
                terminal[str(mover)] = {
                    "successor": sorted(successor),
                    "reason": "misses-r",
                    "verified": misses_r,
                }
                if not misses_r:
                    raise AssertionError("u-successor does not miss r")
                continue

            x_movers = {
                guard for guard in successor if adjacent(guard, x)
            }
            expected = {u, c if mover == b else b}
            if x_movers != expected:
                raise AssertionError("wrong second-stage x movers")
            branch_results = []
            for x_mover in sorted(x_movers):
                second = successor - {x_mover} | {x}
                if x_mover == u:
                    verified = all(
                        not adjacent(guard, r) for guard in second
                    )
                    reason = "misses-r"
                else:
                    verified = second == omitted_A
                    reason = "C064-omitted-A"
                if not verified:
                    raise AssertionError("unclosed second-stage branch")
                branch_results.append(
                    {
                        "mover": x_mover,
                        "successor": sorted(second),
                        "reason": reason,
                    }
                )
            terminal[str(mover)] = {
                "successor": sorted(successor),
                "reason": "fails-at-x",
                "branches": branch_results,
                "verified": True,
            }
        audited += 1

    return {
        "optional_assignments": audited,
        "optional_pairs": [list(endpoints) for endpoints in optional],
        "forced_edge_count": len(forced_edges),
        "forced_nonedge_count": len(forced_nonedges),
        "all_U_at_d_branches_excluded": True,
        "terminal_template": terminal,
    }


def audit_control(label: str, record: str):
    graph = decode_graph6(record)
    family, ranks = kernel(graph)
    u, x, p, q, r, b, c = range(7)
    completions = [
        vertex
        for vertex in range(len(graph))
        if vertex not in (x, r)
        and vertex not in graph[x]
        and vertex not in graph[r]
    ]
    if len(completions) != 1:
        raise AssertionError("control must have one x,r completion")
    d = completions[0]
    if not all(vertex in graph[d] for vertex in (p, q, b, c)):
        raise AssertionError("control completion is not four-hit")
    triple = frozenset((u, x, d))
    if not dominates(graph, triple):
        raise AssertionError("control completion triple does not dominate")
    if not dominates(graph, frozenset((u, d))):
        raise AssertionError("control must stop at a dominating u,d pair")

    B = frozenset((u, p, q))
    R = frozenset((u, r, d))
    P = frozenset((u, p, d))
    Q = frozenset((u, q, d))
    rank_vector = [ranks[B], ranks[P], ranks[Q], ranks[R]]
    if rank_vector != [1, 2, 2, 3]:
        raise AssertionError("wrong completion rank diamond")
    I = frozenset((x, r, d))
    if I not in family:
        raise AssertionError("independent completion must survive")

    return {
        "label": label,
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(graph),
        "completion_d": d,
        "completion_hits": [p, q, b, c],
        "completion_triple_dominates": True,
        "u_d_pair_dominates": True,
        "rank_vector_B_P_Q_R": rank_vector,
        "greatest_triple_family_size": len(family),
    }


def evaluate():
    return {
        "schema": "canonical-QQ1-completion-dynamics-audit-v1",
        "status": "VERIFIED",
        "symbolic_cold_witness": symbolic_cold_audit(),
        "controls": {
            label: audit_control(label, record)
            for label, record in CONTROLS.items()
        },
        "scope": (
            "Finite bookkeeping and fixed-control audit only; accepted "
            "C-010/C-064/C-108/C-143/C-146/C-158/C-161 are dependencies."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))


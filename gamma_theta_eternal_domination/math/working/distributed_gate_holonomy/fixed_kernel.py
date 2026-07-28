#!/usr/bin/env python3
"""Inspect deletion ranks for the maximally permissive fixed graph motif.

All unspecified pairs are G-edges.  This script is only a proof-discovery
aid: a human theorem must remain valid when unspecified pairs are changed.
"""

from __future__ import annotations

import argparse
from itertools import combinations


S = frozenset((0, 1, 2))
A, B, C = 0, 1, 2
X0, Y0, Z0, X1, Y1, Z1 = range(3, 9)


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def motif(x_length: int, y_length: int) -> tuple[int, set[tuple[int, int]], set[frozenset[int]]]:
    next_vertex = 9
    x_interior = tuple(range(next_vertex, next_vertex + x_length - 1))
    next_vertex += x_length - 1
    y_interior = tuple(range(next_vertex, next_vertex + y_length - 1))
    next_vertex += y_length - 1
    order = next_vertex

    h_edges = {pair(u, v) for u, v in combinations(S, 2)}
    for x, y, z in ((X0, Y0, Z0), (X1, Y1, Z1)):
        h_edges.update(
            pair(u, v)
            for u, v in ((C, x), (A, y), (B, z), (x, z), (y, z))
        )
    x_path = (X0, *x_interior, X1)
    y_path = (Y0, *y_interior, Y1)
    h_edges.update(
        pair(u, v)
        for u, v in zip(x_path[:-1], x_path[1:], strict=True)
    )
    h_edges.update(
        pair(u, v)
        for u, v in zip(y_path[:-1], y_path[1:], strict=True)
    )

    def direct(vertex: int, omitted: int) -> frozenset[int]:
        return (S - {omitted}) | {vertex}

    forbidden: set[frozenset[int]] = set()
    for vertex in (X0, X1):
        forbidden.add(direct(vertex, C))
    for vertex in (Y0, Y1):
        forbidden.add(direct(vertex, A))
    for vertex in (Z0, Z1):
        forbidden.add(direct(vertex, B))
    for vertex in x_interior:
        forbidden.add(direct(vertex, C))
    for vertex in y_interior:
        forbidden.add(direct(vertex, A))
    return order, h_edges, forbidden


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x-length", type=int, required=True)
    parser.add_argument("--y-length", type=int, required=True)
    args = parser.parse_args()
    order, h_edges, forbidden = motif(args.x_length, args.y_length)

    def g_edge(u: int, v: int) -> bool:
        return u != v and pair(u, v) not in h_edges

    def dominates(state: frozenset[int]) -> bool:
        return all(
            v in state or any(g_edge(v, guard) for guard in state)
            for v in range(order)
        )

    family = {
        frozenset(state)
        for state in combinations(range(order), 3)
        if dominates(frozenset(state)) and frozenset(state) not in forbidden
    }
    rank: dict[frozenset[int], int] = {
        frozenset(state): 0
        for state in combinations(range(order), 3)
        if frozenset(state) not in family
    }
    reason: dict[frozenset[int], tuple[int, tuple[frozenset[int], ...]]] = {}
    round_number = 0
    while True:
        removed: dict[frozenset[int], tuple[int, tuple[frozenset[int], ...]]] = {}
        for state in family:
            for attacked in range(order):
                if attacked in state:
                    continue
                successors = tuple(
                    (state - {guard}) | {attacked}
                    for guard in state
                    if g_edge(guard, attacked)
                )
                if not any(successor in family for successor in successors):
                    removed[state] = (attacked, successors)
                    break
        if not removed:
            break
        round_number += 1
        for state, why in removed.items():
            rank[state] = round_number
            reason[state] = why
        family.difference_update(removed)

    print(f"order={order} kernel={len(family)} rounds={round_number} S_rank={rank.get(S, 'survives')}")

    seen: set[frozenset[int]] = set()

    def show(state: frozenset[int], depth: int = 0) -> None:
        indent = "  " * depth
        state_rank = rank.get(state)
        print(f"{indent}{tuple(sorted(state))} rank={state_rank}")
        if state in seen or state_rank in (None, 0) or depth >= 8:
            return
        seen.add(state)
        attacked, successors = reason[state]
        print(f"{indent} attack {attacked}")
        for successor in successors:
            show(successor, depth + 1)

    show(S)
    for label, state in (
        ("X0-a", (S - {A}) | {X0}),
        ("X0-b", (S - {B}) | {X0}),
        ("Y0-b", (S - {B}) | {Y0}),
        ("Y0-c", (S - {C}) | {Y0}),
        ("Z0-a", (S - {A}) | {Z0}),
        ("Z0-c", (S - {C}) | {Z0}),
        ("X1-a", (S - {A}) | {X1}),
        ("X1-b", (S - {B}) | {X1}),
        ("Y1-b", (S - {B}) | {Y1}),
        ("Y1-c", (S - {C}) | {Y1}),
        ("Z1-a", (S - {A}) | {Z1}),
        ("Z1-c", (S - {C}) | {Z1}),
    ):
        if state not in family:
            print(f"\nrequired {label} deleted")
            show(state)


if __name__ == "__main__":
    main()

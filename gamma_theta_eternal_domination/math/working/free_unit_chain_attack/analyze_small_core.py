#!/usr/bin/env python3
"""Exhaustive seven-vertex analysis of the (2,1) same-marker core."""

from __future__ import annotations

from itertools import combinations


N = 7
D, U, E, S, X, Y, P = range(N)
ANCHORS = (D, U, E)
REFERENCE = sum(1 << vertex for vertex in ANCHORS)
LISTS = {
    S: frozenset((D,)),
    X: frozenset((D, E)),
    Y: frozenset((D, U)),
    P: frozenset(),  # only the omission U is prescribed below
}


def bit_state(items: tuple[int, ...]) -> int:
    return sum(1 << item for item in items)


def direct_state(vertex: int, omitted: int) -> int:
    return (REFERENCE ^ (1 << omitted)) | (1 << vertex)


FIXED_H = {
    tuple(sorted(edge))
    for edge in (
        (D, U), (D, E), (U, E),
        (S, P), (P, X), (S, Y), (X, Y),
    )
}
FIXED_G = {
    tuple(sorted(edge))
    for edge in (
        (S, D),
        (X, D), (X, E),
        (Y, D), (Y, U),
    )
}
ALL_PAIRS = set(combinations(range(N), 2))
UNKNOWN = sorted(ALL_PAIRS - FIXED_H - FIXED_G)

REQUIRED = {
    direct_state(vertex, omitted)
    for vertex, response in LISTS.items()
    if vertex != P
    for omitted in response
}
FORBIDDEN = {
    direct_state(vertex, omitted)
    for vertex, response in LISTS.items()
    if vertex != P
    for omitted in ANCHORS
    if omitted not in response
}
FORBIDDEN.add(direct_state(P, U))


def adjacency_from_h(h_edges: set[tuple[int, int]]) -> list[int]:
    adjacency = [0] * N
    for left, right in ALL_PAIRS - h_edges:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    return adjacency


def dominates(state: int, adjacency: list[int]) -> bool:
    covered = state
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        covered |= adjacency[bit.bit_length() - 1]
    return covered == (1 << N) - 1


def kernel(adjacency: list[int]) -> tuple[set[int], dict[int, int]]:
    family = {
        bit_state(state)
        for state in combinations(range(N), 3)
        if bit_state(state) not in FORBIDDEN
        and dominates(bit_state(state), adjacency)
    }
    rank: dict[int, int] = {}
    round_index = 1
    while True:
        bad = set()
        for state in family:
            for attacked in range(N):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                scan = state & adjacency[attacked]
                if not any(
                    ((state ^ guard_bit) | attacked_bit) in family
                    for guard_bit in (
                        1 << guard
                        for guard in range(N)
                        if scan & (1 << guard)
                    )
                ):
                    bad.add(state)
                    break
        if not bad:
            return family, rank
        for state in bad:
            rank[state] = round_index
        family -= bad
        round_index += 1


def main() -> None:
    if len(UNKNOWN) != 9:
        raise AssertionError(f"unexpected unknown edge count {len(UNKNOWN)}")
    survivors = 0
    best_round = -1
    best = None
    histogram: dict[int, int] = {}
    for mask in range(1 << len(UNKNOWN)):
        h_edges = set(FIXED_H)
        for index, edge in enumerate(UNKNOWN):
            if mask >> index & 1:
                h_edges.add(edge)
        adjacency = adjacency_from_h(h_edges)
        family, rank = kernel(adjacency)
        if REFERENCE in family and REQUIRED <= family:
            survivors += 1
        reference_rank = rank.get(REFERENCE, 10**9 if REFERENCE in family else 0)
        histogram[reference_rank] = histogram.get(reference_rank, 0) + 1
        if reference_rank != 10**9 and reference_rank > best_round:
            best_round = reference_rank
            best = (h_edges, family, rank)
    print(
        f"completions={1 << len(UNKNOWN)} survivors={survivors}"
        f" reference_rank_histogram={dict(sorted(histogram.items()))}"
        f" max_reference_rank={best_round}"
    )
    if best is None:
        return
    h_edges, family, rank = best
    print(f"hardest_H_edges={sorted(h_edges)}")
    print(
        "ranked_states="
        + repr(
            sorted(
                (
                    value,
                    tuple(
                        vertex
                        for vertex in range(N)
                        if state & (1 << vertex)
                    ),
                )
                for state, value in rank.items()
            )
        )
    )
    print(
        "terminal_states="
        + repr(
            sorted(
                tuple(
                    vertex for vertex in range(N) if state & (1 << vertex)
                )
                for state in family
            )
        )
    )


if __name__ == "__main__":
    main()

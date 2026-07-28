#!/usr/bin/env python3
"""Exact scan of two-vertex extensions of the separated-port control.

The nine old vertices induce exactly the complement graph in
``full_list_odd_lollipop_integration``.  Vertices 9 and 10 have arbitrary
complement adjacencies to the old vertices and to each other.  We first
test the static equality conditions

    omega(H) = 3
    every pair has a common H-neighbor,

which are equivalent here to alpha(G) = gamma(G) = 3.  Static survivors
are then checked with the greatest one-guard eternal triple kernel.

This is a bounded diagnostic, not a universe-wide graph exclusion.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
import time
from pathlib import Path


N0 = 9
N = 11
S = (0, 1, 2)
X, R, T, Q, V0, V1 = 3, 4, 5, 6, 7, 8
BASE_H_EDGES = {
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
DESIRED_LISTS = {
    X: frozenset((0, 1, 2)),
    R: frozenset((0, 1)),
    T: frozenset((0, 1)),
    Q: frozenset((0, 1)),
    V0: frozenset((1, 2)),
    V1: frozenset((1, 2)),
}
TRIPLES = tuple(itertools.combinations(range(N), 3))
TRIPLE_MASKS = tuple(sum(1 << v for v in triple) for triple in TRIPLES)
TRIPLE_INDEX = {mask: index for index, mask in enumerate(TRIPLE_MASKS)}
PAIRS = tuple(itertools.combinations(range(N), 2))
ALL = (1 << N) - 1


def base_masks() -> list[int]:
    masks = [0] * N
    for u, v in BASE_H_EDGES:
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return masks


def extension_masks(code: int) -> list[int]:
    """Decode 9+9+1 extension bits into complement-neighborhood masks."""
    masks = base_masks()
    for new_vertex, shift in ((9, 0), (10, 9)):
        old_neighbors = (code >> shift) & ((1 << N0) - 1)
        masks[new_vertex] |= old_neighbors
        for old in range(N0):
            if old_neighbors & (1 << old):
                masks[old] |= 1 << new_vertex
    if code & (1 << 18):
        masks[9] |= 1 << 10
        masks[10] |= 1 << 9
    return masks


def has_k4(masks: list[int]) -> bool:
    for a in range(N):
        for b in range(a + 1, N):
            if not (masks[a] & (1 << b)):
                continue
            common_ab = masks[a] & masks[b] & ~((1 << (b + 1)) - 1)
            while common_ab:
                cbit = common_ab & -common_ab
                c = cbit.bit_length() - 1
                common_abc = (
                    masks[a]
                    & masks[b]
                    & masks[c]
                    & ~((1 << (c + 1)) - 1)
                )
                if common_abc:
                    return True
                common_ab ^= cbit
    return False


def every_pair_has_common_h_neighbor(masks: list[int]) -> bool:
    return all(masks[u] & masks[v] for u, v in PAIRS)


def dominates_triple(mask: int, h_masks: list[int]) -> bool:
    vertices = [v for v in range(N) if mask & (1 << v)]
    return not (h_masks[vertices[0]] & h_masks[vertices[1]] & h_masks[vertices[2]])


def greatest_eternal_kernel(
    h_masks: list[int],
) -> tuple[frozenset[int], dict[int, int]]:
    alive = {
        mask for mask in TRIPLE_MASKS if dominates_triple(mask, h_masks)
    }
    deletion_rank: dict[int, int] = {}
    round_number = 1
    while True:
        dead: set[int] = set()
        for state in alive:
            unoccupied = ALL ^ state
            attack_bits = unoccupied
            while attack_bits:
                abit = attack_bits & -attack_bits
                attack = abit.bit_length() - 1
                response = False
                guard_bits = state
                while guard_bits:
                    gbit = guard_bits & -guard_bits
                    guard = gbit.bit_length() - 1
                    # A move is legal in G exactly when it is not an H-edge.
                    if not (h_masks[guard] & abit):
                        successor = (state ^ gbit) | abit
                        if successor in alive:
                            response = True
                            break
                    guard_bits ^= gbit
                if not response:
                    dead.add(state)
                    break
                attack_bits ^= abit
        if not dead:
            return frozenset(alive), deletion_rank
        for state in dead:
            deletion_rank[state] = round_number
        alive.difference_update(dead)
        round_number += 1


def response_lists(
    kernel: frozenset[int], h_masks: list[int]
) -> dict[int, frozenset[int]]:
    s_mask = sum(1 << v for v in S)
    answer: dict[int, frozenset[int]] = {}
    for target in range(N0):
        if target in S:
            continue
        values = set()
        for guard in S:
            if not (h_masks[guard] & (1 << target)):
                successor = (s_mask ^ (1 << guard)) | (1 << target)
                if successor in kernel:
                    values.add(guard)
        answer[target] = frozenset(values)
    return answer


def graph6_from_h_masks(h_masks: list[int]) -> str:
    """Return graph6 for G (not H), for n <= 62."""
    bits = []
    for j in range(1, N):
        for i in range(j):
            bits.append(0 if h_masks[i] & (1 << j) else 1)
    while len(bits) % 6:
        bits.append(0)
    payload = "".join(
        chr(63 + sum(bits[i + j] << (5 - j) for j in range(6)))
        for i in range(0, len(bits), 6)
    )
    return chr(63 + N) + payload


def main() -> None:
    started = time.monotonic()
    static_count = 0
    eternal_count = 0
    full_count = 0
    exact_count = 0
    records = []
    static_records = []

    for code in range(1 << 19):
        h_masks = extension_masks(code)
        if has_k4(h_masks):
            continue
        if not every_pair_has_common_h_neighbor(h_masks):
            continue
        static_count += 1
        kernel, deletion_rank = greatest_eternal_kernel(h_masks)
        s_mask = sum(1 << v for v in S)
        static_records.append(
            {
                "code": code,
                "graph6_G": graph6_from_h_masks(h_masks),
                "kernel_size": len(kernel),
                "reference_state_deletion_rank": deletion_rank.get(s_mask),
                "H_neighbors_9": [
                    v for v in range(N) if h_masks[9] & (1 << v)
                ],
                "H_neighbors_10": [
                    v for v in range(N) if h_masks[10] & (1 << v)
                ],
            }
        )
        if s_mask not in kernel:
            continue
        eternal_count += 1
        lists = response_lists(kernel, h_masks)
        if lists[X] != frozenset(S):
            continue
        full_count += 1
        exact = all(lists[v] == wanted for v, wanted in DESIRED_LISTS.items())
        if exact:
            exact_count += 1
        if len(records) < 100:
            records.append(
                {
                    "code": code,
                    "graph6_G": graph6_from_h_masks(h_masks),
                    "kernel_size": len(kernel),
                    "lists_old_vertices": {
                        str(v): sorted(lists[v]) for v in sorted(lists)
                    },
                    "exact_old_lists": exact,
                    "H_neighbors_9": [
                        v for v in range(N) if h_masks[9] & (1 << v)
                    ],
                    "H_neighbors_10": [
                        v for v in range(N) if h_masks[10] & (1 << v)
                    ],
                }
            )

    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "status": "PASS",
        "scope": {
            "old_order": N0,
            "new_order": N,
            "extensions": 1 << 19,
            "old_induced_H_exact": True,
        },
        "counts": {
            "static_gamma_alpha_3": static_count,
            "eternal_equality_3": eternal_count,
            "full_x_in_greatest_family": full_count,
            "exact_old_response_lists": exact_count,
        },
        "records_truncated_to": len(records),
        "records": records,
        "static_records": static_records,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "source_sha256": source_hash,
    }
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

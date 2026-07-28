#!/usr/bin/env python3
"""Bitset cross-check of the 32 one-defect mixed-P4 completions.

This implementation intentionally shares no transition or domination code
with ``verify.py``.  It checks only the decisive local-kernel claim and
prints a compact deterministic summary.
"""

from __future__ import annotations

from itertools import combinations
import hashlib
import json


ORDER = 8
FULL = (1 << ORDER) - 1
REFERENCE = 0b111

FIXED_EDGES = (
    (0, 3), (0, 4), (2, 4), (1, 5), (2, 5), (1, 6),
    (2, 3), (2, 6), (3, 5), (3, 6), (4, 6),
    (2, 7), (4, 7), (5, 7),
)
FIXED_NONEDGES = (
    (0, 1), (0, 2), (1, 2),
    (3, 4), (4, 5), (5, 6),
    (0, 7), (1, 7), (3, 7),
)
OPTIONAL = ((1, 3), (1, 4), (0, 5), (0, 6), (6, 7))
LIST_MASK = {
    3: 1 << 0,
    4: (1 << 0) | (1 << 2),
    5: (1 << 1) | (1 << 2),
    6: 1 << 1,
    7: 1 << 2,
}


def triples() -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in state)
        for state in combinations(range(ORDER), 3)
    )


TRIPLES = triples()


def rows_for(mask: int) -> tuple[int, ...]:
    rows = [0] * ORDER
    chosen = list(FIXED_EDGES)
    chosen.extend(
        edge for index, edge in enumerate(OPTIONAL) if mask & (1 << index)
    )
    for first, second in chosen:
        rows[first] |= 1 << second
        rows[second] |= 1 << first
    return tuple(rows)


def dominates(state: int, rows: tuple[int, ...]) -> bool:
    dominated = state
    occupied = state
    while occupied:
        guard = (occupied & -occupied).bit_length() - 1
        dominated |= rows[guard]
        occupied &= occupied - 1
    return dominated == FULL


def restoration_ok(state: int) -> bool:
    missing = REFERENCE & ~state
    restored = 0
    outside = state & ~REFERENCE
    while outside:
        vertex = (outside & -outside).bit_length() - 1
        restored |= LIST_MASK[vertex]
        outside &= outside - 1
    return not (missing & ~restored)


def kernel(mask: int) -> tuple[int, tuple[int, ...], int]:
    rows = rows_for(mask)
    active = {
        state for state in TRIPLES
        if dominates(state, rows) and restoration_ok(state)
    }
    initial_size = len(active)
    reference_round = 0
    round_sizes = []

    while active:
        doomed = set()
        for state in active:
            unoccupied = FULL & ~state
            while unoccupied:
                attacked_bit = unoccupied & -unoccupied
                attacked = attacked_bit.bit_length() - 1
                movable = state & rows[attacked]
                safe = False
                while movable:
                    guard_bit = movable & -movable
                    successor = state ^ guard_bit ^ attacked_bit
                    if successor in active:
                        safe = True
                        break
                    movable &= movable - 1
                if not safe:
                    doomed.add(state)
                    break
                unoccupied &= unoccupied - 1
        if not doomed:
            break
        round_sizes.append(len(doomed))
        if REFERENCE in doomed:
            reference_round = len(round_sizes)
        active.difference_update(doomed)

    return initial_size, tuple(round_sizes), reference_round


def main() -> None:
    all_pairs = set(combinations(range(ORDER), 2))
    fixed_edges = {tuple(sorted(edge)) for edge in FIXED_EDGES}
    fixed_nonedges = {tuple(sorted(edge)) for edge in FIXED_NONEDGES}
    optional = {tuple(sorted(edge)) for edge in OPTIONAL}
    if fixed_edges | fixed_nonedges | optional != all_pairs:
        raise AssertionError("the five optional pairs do not complete K8")
    if (
        fixed_edges & fixed_nonedges
        or fixed_edges & optional
        or fixed_nonedges & optional
    ):
        raise AssertionError("pair categories overlap")

    direct = {REFERENCE}
    for vertex, palette in LIST_MASK.items():
        for anchor in range(3):
            if palette & (1 << anchor):
                direct.add(REFERENCE ^ (1 << anchor) ^ (1 << vertex))

    records = []
    for mask in range(32):
        rows = rows_for(mask)
        initial = {
            state for state in TRIPLES
            if dominates(state, rows) and restoration_ok(state)
        }
        if not direct <= initial:
            raise AssertionError((mask, "required direct state absent"))
        initial_size, round_sizes, reference_round = kernel(mask)
        if sum(round_sizes) != initial_size:
            raise AssertionError((mask, "terminal kernel is nonempty"))
        records.append(
            {
                "mask": mask,
                "initial": initial_size,
                "rounds": list(round_sizes),
                "reference_round": reference_round,
            }
        )

    payload = json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode()
    result = {
        "schema": "mixed-p4-one-defect-bitset-crosscheck-v1",
        "completion_count": len(records),
        "empty_terminal_count": len(records),
        "records_sha256": hashlib.sha256(payload).hexdigest(),
        "records": records,
        "verdict": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()

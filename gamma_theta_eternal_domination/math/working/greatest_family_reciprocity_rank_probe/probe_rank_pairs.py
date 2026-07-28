#!/usr/bin/env python3
"""Discovery-only deletion-rank census for complementary exchanges.

The input is one small graph6 record per line.  The program retains exactly
the graphs with gamma=alpha=gamma_infinity=3, computes the literal greatest
fixed point of dominating triples, and records the two deletion ranks of
every complementary exchange between maximum independent triples.

Rank zero means non-dominating, a positive rank is the synchronous kernel
deletion round, and ``S`` means survival in the greatest family.  This is a
mechanism probe, not a coverage certificate.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import sys


def decode_graph6(record: str) -> tuple[int, ...]:
    values = [ord(char) - 63 for char in record.strip()]
    if not values or not (0 <= values[0] <= 62):
        raise ValueError("only small graph6 records are supported")
    n = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    adj = [0] * n
    cursor = 0
    for column in range(1, n):
        for row in range(column):
            if bits[cursor]:
                adj[row] |= 1 << column
                adj[column] |= 1 << row
            cursor += 1
    return tuple(adj)


def dominates(adj: tuple[int, ...], state: int, all_mask: int) -> bool:
    covered = state
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        covered |= adj[bit.bit_length() - 1]
    return covered == all_mask


def independent(adj: tuple[int, ...], state: int) -> bool:
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        if adj[bit.bit_length() - 1] & scan:
            return False
    return True


def triple_kernel_ranks(
    adj: tuple[int, ...],
) -> tuple[set[int], dict[int, int], set[int]]:
    n = len(adj)
    all_mask = (1 << n) - 1
    triples = {
        sum(1 << vertex for vertex in choice)
        for choice in itertools.combinations(range(n), 3)
    }
    dominating = {
        state for state in triples if dominates(adj, state, all_mask)
    }
    family = set(dominating)
    ranks: dict[int, int] = {}
    round_number = 0
    while True:
        removed: set[int] = set()
        for state in family:
            attacks = all_mask ^ state
            while attacks:
                target_bit = attacks & -attacks
                attacks ^= target_bit
                target = target_bit.bit_length() - 1
                movers = state & adj[target]
                if not any(
                    ((state ^ guard_bit) | target_bit) in family
                    for guard_bit in iter_bits(movers)
                ):
                    removed.add(state)
                    break
        if not removed:
            return family, ranks, dominating
        round_number += 1
        for state in removed:
            ranks[state] = round_number
        family.difference_update(removed)


def iter_bits(mask: int):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit


def no_dominating_pair(adj: tuple[int, ...]) -> bool:
    n = len(adj)
    all_mask = (1 << n) - 1
    closed = tuple(adj[v] | (1 << v) for v in range(n))
    if any(mask == all_mask for mask in closed):
        return False
    return all(
        closed[u] | closed[v] != all_mask
        for u in range(n)
        for v in range(u + 1, n)
    )


def alpha_is_three(adj: tuple[int, ...]) -> tuple[bool, tuple[int, ...]]:
    n = len(adj)
    triples = tuple(
        sum(1 << vertex for vertex in choice)
        for choice in itertools.combinations(range(n), 3)
        if independent(
            adj, sum(1 << vertex for vertex in choice)
        )
    )
    if not triples:
        return False, ()
    for choice in itertools.combinations(range(n), 4):
        state = sum(1 << vertex for vertex in choice)
        if independent(adj, state):
            return False, ()
    return True, triples


def label(
    state: int,
    family: set[int],
    ranks: dict[int, int],
    dominating: set[int],
) -> str:
    if state in family:
        return "S"
    if state not in dominating:
        return "0"
    return str(ranks[state])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-graphs", type=int)
    args = parser.parse_args()
    totals: collections.Counter[str] = collections.Counter()
    ordered_rank_pairs: collections.Counter[str] = collections.Counter()
    static_asymmetry_pairs: collections.Counter[str] = collections.Counter()
    first_survival_violation = None
    first_static_asymmetry = None

    for raw in sys.stdin:
        record = raw.strip()
        if not record or record.startswith(">"):
            continue
        if args.max_graphs and totals["graphs_read"] >= args.max_graphs:
            break
        totals["graphs_read"] += 1
        adj = decode_graph6(record)
        alpha_three, independent_triples = alpha_is_three(adj)
        if not alpha_three or not no_dominating_pair(adj):
            continue
        totals["static_equality_graphs"] += 1
        family, ranks, dominating = triple_kernel_ranks(adj)
        if not family:
            continue
        totals["eternal_equality_graphs"] += 1
        totals["greatest_states"] += len(family)

        for first_index, first in enumerate(independent_triples):
            for second in independent_triples[first_index + 1 :]:
                totals["independent_state_pairs"] += 1
                left = first & ~second
                right = second & ~first
                for ubit in iter_bits(left):
                    for xbit in iter_bits(right):
                        forward = (first ^ ubit) | xbit
                        reverse = (second ^ xbit) | ubit
                        f_label = label(forward, family, ranks, dominating)
                        r_label = label(reverse, family, ranks, dominating)
                        ordered_rank_pairs[f"{f_label},{r_label}"] += 1
                        if (f_label == "S") != (r_label == "S"):
                            totals["survival_violations"] += 1
                            if first_survival_violation is None:
                                first_survival_violation = {
                                    "graph6": record,
                                    "S": vertices(first),
                                    "T": vertices(second),
                                    "u": ubit.bit_length() - 1,
                                    "x": xbit.bit_length() - 1,
                                    "forward_rank": f_label,
                                    "reverse_rank": r_label,
                                }
                        if (f_label == "0") != (r_label == "0"):
                            totals["static_asymmetries"] += 1
                            static_asymmetry_pairs[
                                f"{f_label},{r_label}"
                            ] += 1
                            if first_static_asymmetry is None:
                                first_static_asymmetry = {
                                    "graph6": record,
                                    "S": vertices(first),
                                    "T": vertices(second),
                                    "u": ubit.bit_length() - 1,
                                    "x": xbit.bit_length() - 1,
                                    "forward_rank": f_label,
                                    "reverse_rank": r_label,
                                }

    result = {
        "schema": "greatest-family-reciprocity-rank-probe-v1",
        "classification": "OBSERVED_DISCOVERY_ONLY",
        "totals": dict(sorted(totals.items())),
        "ordered_rank_pairs": dict(sorted(ordered_rank_pairs.items())),
        "static_asymmetry_rank_pairs": dict(
            sorted(static_asymmetry_pairs.items())
        ),
        "first_static_asymmetry": first_static_asymmetry,
        "first_survival_violation": first_survival_violation,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


def vertices(mask: int) -> list[int]:
    return [
        vertex
        for vertex in range(mask.bit_length())
        if mask & (1 << vertex)
    ]


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Discovery probe for the parameter-two projection transversal claim.

Reads short graph6 records, computes the greatest one-guard eternal
two-family directly, and reports the first retained pair whose vertices lie
on the same side of one connected component of the bipartite complement.

This is exploratory code.  The eventual proof artifact must not depend on
the absence of a hit here.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import deque


def decode_graph6(record: str) -> tuple[int, list[int]]:
    data = record.strip().encode("ascii")
    if not data or not 63 <= data[0] <= 125:
        raise ValueError("only short graph6 records are supported")
    n = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * n
    position = 0
    for high in range(1, n):
        for low in range(high):
            if bits[position]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    return n, adjacency


def dominates(state: int, adjacency: list[int], full: int) -> bool:
    covered = state
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        covered |= adjacency[bit.bit_length() - 1]
    return covered == full


def alpha_at_most_two(n: int, adjacency: list[int]) -> bool:
    for a, b, c in itertools.combinations(range(n), 3):
        if (
            not (adjacency[a] >> b) & 1
            and not (adjacency[a] >> c) & 1
            and not (adjacency[b] >> c) & 1
        ):
            return False
    return True


def no_dominating_singleton(n: int, adjacency: list[int]) -> bool:
    full = (1 << n) - 1
    return all((adjacency[v] | (1 << v)) != full for v in range(n))


def greatest_pair_family(n: int, adjacency: list[int]) -> set[int]:
    full = (1 << n) - 1
    family = {
        (1 << u) | (1 << v)
        for u, v in itertools.combinations(range(n), 2)
        if dominates((1 << u) | (1 << v), adjacency, full)
    }
    while True:
        bad: set[int] = set()
        for state in family:
            for attacked in range(n):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                legal = False
                scan = state & adjacency[attacked]
                while scan:
                    guard_bit = scan & -scan
                    scan ^= guard_bit
                    if (state ^ guard_bit) | attacked_bit in family:
                        legal = True
                        break
                if not legal:
                    bad.add(state)
                    break
        if not bad:
            return family
        family -= bad


def complement_components(
    n: int, adjacency: list[int]
) -> tuple[bool, list[int], list[int]]:
    full = (1 << n) - 1
    parity = [-1] * n
    component = [-1] * n
    component_index = 0
    for root in range(n):
        if parity[root] >= 0:
            continue
        parity[root] = 0
        component[root] = component_index
        queue = deque([root])
        while queue:
            u = queue.popleft()
            h_neighbors = (full ^ adjacency[u] ^ (1 << u))
            scan = h_neighbors
            while scan:
                bit = scan & -scan
                scan ^= bit
                v = bit.bit_length() - 1
                if parity[v] < 0:
                    parity[v] = parity[u] ^ 1
                    component[v] = component_index
                    queue.append(v)
                elif parity[v] == parity[u]:
                    return False, parity, component
        component_index += 1
    return True, parity, component


def analyze(record: str) -> dict[str, object]:
    n, adjacency = decode_graph6(record)
    if not alpha_at_most_two(n, adjacency):
        return {"eligible": False}
    if not no_dominating_singleton(n, adjacency):
        return {"eligible": False}
    bipartite, parity, component = complement_components(n, adjacency)
    if not bipartite:
        return {"eligible": False}
    family = greatest_pair_family(n, adjacency)
    if not family:
        return {"eligible": False}
    bad_states = []
    for state in sorted(family):
        vertices = [v for v in range(n) if state >> v & 1]
        u, v = vertices
        if component[u] == component[v] and parity[u] == parity[v]:
            bad_states.append(vertices)
    return {
        "eligible": True,
        "family_size": len(family),
        "bad_states": bad_states,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stop-at-first", action="store_true")
    args = parser.parse_args()
    counts = {
        "records": 0,
        "eligible_parameter_two_equality_graphs": 0,
        "graphs_with_same_side_family_state": 0,
    }
    first = None
    for line in sys.stdin:
        record = line.strip()
        if not record:
            continue
        counts["records"] += 1
        result = analyze(record)
        if not result["eligible"]:
            continue
        counts["eligible_parameter_two_equality_graphs"] += 1
        if result["bad_states"]:
            counts["graphs_with_same_side_family_state"] += 1
            if first is None:
                first = {"graph6": record, **result}
            if args.stop_at_first:
                break
    print(
        json.dumps(
            {
                "schema": "k2-transversal-discovery-v1",
                "counts": counts,
                "first_countermodel": first,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Deterministic search for greatest-family exchange nonreciprocity.

This is a discovery program, not a coverage certificate.  It samples graphs
with a displayed partition into three G-cliques, computes all relevant
parameters and the literal one-guard greatest three-kernel, and stops at the
first pair of independent triples violating complementary-exchange
reciprocity.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import time
from pathlib import Path


def bit_count(mask: int) -> int:
    return mask.bit_count()


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


def greatest_kernel(
    adj: tuple[int, ...], k: int
) -> tuple[frozenset[int], tuple[int, ...]]:
    n = len(adj)
    all_mask = (1 << n) - 1
    states = {
        sum(1 << v for v in comb)
        for comb in itertools.combinations(range(n), k)
        if dominates(adj, sum(1 << v for v in comb), all_mask)
    }
    waves: list[int] = []
    while True:
        remove: set[int] = set()
        for state in states:
            unoccupied = all_mask ^ state
            scan_r = unoccupied
            while scan_r:
                rbit = scan_r & -scan_r
                scan_r ^= rbit
                r = rbit.bit_length() - 1
                movers = state & adj[r]
                ok = False
                while movers:
                    ubit = movers & -movers
                    movers ^= ubit
                    if (state ^ ubit) | rbit in states:
                        ok = True
                        break
                if not ok:
                    remove.add(state)
                    break
        if not remove:
            return frozenset(states), tuple(waves)
        states.difference_update(remove)
        waves.append(len(remove))


def gamma_at_least_three(adj: tuple[int, ...]) -> bool:
    n = len(adj)
    all_mask = (1 << n) - 1
    closed = tuple(adj[v] | (1 << v) for v in range(n))
    if any(mask == all_mask for mask in closed):
        return False
    return all(
        (closed[u] | closed[v]) != all_mask
        for u in range(n)
        for v in range(u + 1, n)
    )


def find_violation(
    adj: tuple[int, ...], family: frozenset[int]
) -> dict[str, object] | None:
    independent_triples = tuple(
        state for state in family if independent(adj, state)
    )
    for index, first in enumerate(independent_triples):
        for second in independent_triples[index + 1 :]:
            left = first & ~second
            right = second & ~first
            scan_u = left
            while scan_u:
                ubit = scan_u & -scan_u
                scan_u ^= ubit
                u = ubit.bit_length() - 1
                scan_x = right
                while scan_x:
                    xbit = scan_x & -scan_x
                    scan_x ^= xbit
                    x = xbit.bit_length() - 1
                    forward_state = (first ^ ubit) | xbit
                    reverse_state = (second ^ xbit) | ubit
                    forward = forward_state in family
                    reverse = reverse_state in family
                    if forward != reverse:
                        return {
                            "S": mask_vertices(first),
                            "T": mask_vertices(second),
                            "u": u,
                            "x": x,
                            "S_minus_u_plus_x": mask_vertices(forward_state),
                            "T_minus_x_plus_u": mask_vertices(reverse_state),
                            "forward_in_greatest_family": forward,
                            "reverse_in_greatest_family": reverse,
                        }
    return None


def mask_vertices(mask: int) -> list[int]:
    return [v for v in range(mask.bit_length()) if mask & (1 << v)]


def graph6(adj: tuple[int, ...]) -> str:
    n = len(adj)
    if n > 62:
        raise ValueError("small graph6 only")
    bits: list[int] = []
    for column in range(1, n):
        for row in range(column):
            bits.append(1 if adj[row] & (1 << column) else 0)
    while len(bits) % 6:
        bits.append(0)
    return chr(n + 63) + "".join(
        chr(
            63
            + sum(
                bits[offset + bit_index] << (5 - bit_index)
                for bit_index in range(6)
            )
        )
        for offset in range(0, len(bits), 6)
    )


def edge_list(adj: tuple[int, ...]) -> list[list[int]]:
    return [
        [u, v]
        for u in range(len(adj))
        for v in range(u + 1, len(adj))
        if adj[u] & (1 << v)
    ]


def generate(
    rng: random.Random, sizes: tuple[int, int, int], probability: float
) -> tuple[int, ...]:
    n = sum(sizes)
    adj = [0] * n
    parts: list[range] = []
    start = 0
    for size in sizes:
        part = range(start, start + size)
        parts.append(part)
        start += size
        for u, v in itertools.combinations(part, 2):
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    for first_part, second_part in itertools.combinations(parts, 2):
        for u in first_part:
            for v in second_part:
                if rng.random() < probability:
                    adj[u] |= 1 << v
                    adj[v] |= 1 << u
    return tuple(adj)


def run(args: argparse.Namespace) -> dict[str, object]:
    rng = random.Random(args.seed)
    start = time.monotonic()
    totals = {
        "generated": 0,
        "gamma_at_least_three": 0,
        "nonempty_greatest_three_kernel": 0,
        "equality_graphs": 0,
        "independent_state_pairs": 0,
    }
    first_violation: dict[str, object] | None = None
    sizes = tuple(int(piece) for piece in args.parts.split(","))
    if len(sizes) != 3 or min(sizes) < 1:
        raise ValueError("--parts must give three positive sizes")

    for _ in range(args.samples):
        adj = generate(rng, sizes, args.probability)
        totals["generated"] += 1
        if not gamma_at_least_three(adj):
            continue
        totals["gamma_at_least_three"] += 1
        family, waves = greatest_kernel(adj, 3)
        if not family:
            continue
        totals["nonempty_greatest_three_kernel"] += 1
        independent_states = tuple(
            state for state in family if independent(adj, state)
        )
        if not independent_states:
            raise AssertionError("alpha=3 should give independent triples")
        totals["equality_graphs"] += 1
        totals["independent_state_pairs"] += (
            len(independent_states) * (len(independent_states) - 1) // 2
        )
        violation = find_violation(adj, family)
        if violation is not None:
            first_violation = {
                "graph6": graph6(adj),
                "order": len(adj),
                "edge_count": sum(bit_count(mask) for mask in adj) // 2,
                "edges": edge_list(adj),
                "greatest_family_size": len(family),
                "greatest_family": [
                    mask_vertices(state) for state in sorted(family)
                ],
                "kernel_deletion_waves": list(waves),
                "violation": violation,
            }
            break

    payload = {
        "schema": "greatest-family-reciprocity-search-v1",
        "status": "COUNTERMODEL_FOUND" if first_violation else "NO_VIOLATION",
        "scope": {
            "generator": "three displayed G-cliques, independent random cross edges",
            "parts": list(sizes),
            "cross_edge_probability": args.probability,
            "seed": args.seed,
            "requested_samples": args.samples,
            "coverage_claim": False,
        },
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one edge",
            "kernel": "literal greatest fixed point over dominating triples",
            "equality_filter": (
                "displayed three-clique partition gives alpha<=3; "
                "gamma>=3; nonempty greatest triple-kernel"
            ),
        },
        "totals": totals,
        "first_violation": first_violation,
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    payload["sha256_without_this_field"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parts", default="3,3,3")
    parser.add_argument("--probability", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=1729)
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = run(args)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()

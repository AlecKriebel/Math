#!/usr/bin/env python3
"""Exact all-length scan for qutrit complete-graph orbit codes.

Discovery only.  The complete graph has adjacency A_ij=1 for i != j.
By permutation symmetry a syndrome is specified by the counts of its
entries 0,1,2.  The script evaluates the signed coset integers K_{a,b}
from notes/agent_qutrit_graph_codes.md by a nine-state transfer, without
enumerating 3^n vectors.
"""

from __future__ import annotations

import argparse
import itertools
import random


def k_value(counts: tuple[int, int, int], a: int, b: int) -> int:
    """Return K_{a,b} for the complete graph and a syndrome histogram."""
    answer = 0
    # T is the final sum of all t_i.  Once T is fixed, the support weight
    # factors locally because (At)_i = T-t_i.
    for target_sum in range(3):
        dp = {(0, 0): 1}
        for syndrome_value, multiplicity in enumerate(counts):
            for _ in range(multiplicity):
                next_dp: dict[tuple[int, int], int] = {}
                for (running_sum, dot), coefficient in dp.items():
                    for t in range(3):
                        z_label = (
                            target_sum - t + a * syndrome_value
                        ) % 3
                        local_weight = -1 if t == 0 and z_label == 0 else 2
                        key = (
                            (running_sum + t) % 3,
                            (dot + syndrome_value * t) % 3,
                        )
                        next_dp[key] = (
                            next_dp.get(key, 0) + coefficient * local_weight
                        )
                dp = next_dp
        answer += dp.get((target_sum, (-b) % 3), 0)
    return answer


def scan(max_n: int) -> None:
    for n in range(1, max_n + 1):
        best: int | None = None
        best_data = None
        for n0 in range(n + 1):
            for n1 in range(n - n0 + 1):
                n2 = n - n0 - n1
                if n1 + n2 == 0:
                    continue
                counts = (n0, n1, n2)
                k00 = k_value(counts, 0, 0)
                lines = (
                    k_value(counts, 1, 0),
                    k_value(counts, 0, 1),
                    k_value(counts, 1, 1),
                    k_value(counts, 1, 2),
                )
                delta = 2 * k00 + min(lines)
                if best is None or delta < best:
                    best = delta
                    best_data = (counts, k00, lines)
                if delta < 0:
                    print("NEGATIVE", n, delta, best_data)
                    return
        print("n", n, "best", best, "data", best_data)


def direct_k(syndrome: tuple[int, ...], a: int, b: int) -> int:
    """Slow defining sum, used only by the independent small self-test."""
    n = len(syndrome)
    answer = 0
    for t in itertools.product(range(3), repeat=n):
        if sum(x * y for x, y in zip(syndrome, t)) % 3 != (-b) % 3:
            continue
        total = sum(t) % 3
        weight = sum(
            t[i] != 0 or (total - t[i] + a * syndrome[i]) % 3 != 0
            for i in range(n)
        )
        answer += (-1) ** (n - weight) * 2**weight
    return answer


def self_test() -> None:
    rng = random.Random(20260728)
    labels = ((0, 0), (1, 0), (0, 1), (1, 1), (1, 2))
    for n in range(1, 7):
        for _ in range(20):
            syndrome = tuple(rng.randrange(3) for _ in range(n))
            if not any(syndrome):
                syndrome = (1,) + syndrome[1:]
            counts = tuple(syndrome.count(x) for x in range(3))
            for a, b in labels:
                assert k_value(counts, a, b) == direct_k(
                    syndrome, a, b
                )
    print("complete-graph exact transfer self-test passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("max_n", type=int)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    scan(args.max_n)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact finite audit of the r=2 stationary-promotion inequality.

This script is deliberately separate from the structural verifier because
the exhaustive rational stationary solves take longer.  Passing this corpus
is finite evidence only, not a proof of the open all-graph inequality.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parent
CHI = OBSTRUCTION / "r2_entropy_certificate" / "chi_square_channel"
COLLISION = OBSTRUCTION / "r2_collision_closure"
sys.path.insert(0, str(CHI))
sys.path.insert(0, str(COLLISION))

from verify_resolvent_identities import solve  # noqa: E402
from verify_direct_flow_screen import (  # noqa: E402
    connected,
    deterministic_graphs,
    exhaustive_graphs,
    matrix_from_edges,
)


def integrated_two_step(P):
    """Return U M_P^2 psi from the closed exact two-defect formula."""
    n = len(P)
    N = n - 1
    baseline = F(2 ** N - 1, N * 2 ** (N - 1))
    row_square = sum(
        (P[v][i] ** 2 for v in range(n) for i in range(n)), F(0)
    )
    columns = [sum((P[v][i] for v in range(n)), F(0)) for i in range(n)]
    column_square = sum((value ** 2 for value in columns), F(0))
    mutual = sum(
        (P[v][i] * P[i][v] for v in range(n) for i in range(n)), F(0)
    )
    defect_1 = row_square - F(n, n - 1)
    defect_2 = (column_square - mutual) - (n - row_square)
    assert defect_1 >= 0
    assert defect_2 >= 0
    if n == 3:
        return baseline + defect_1 / 24

    s = n - 2
    integrated_sum = sum(
        (F(comb(s - 2, j), (j + 1) * (j + 2) ** 2)
         for j in range(s - 1)),
        F(0),
    )
    integrated_half = F(2 ** s - 1, s) - F(2 ** (s + 1) - 1, 2 * (s + 1))
    alpha = (integrated_half - integrated_sum) / (n * 2 ** s)
    beta = integrated_sum / (2 * n * 2 ** s)
    assert alpha > 0
    assert beta > 0
    return baseline + alpha * defect_1 + beta * defect_2


def promotion_margin(weights):
    P, states, _, _, stationary = solve(weights)
    mean = sum(
        (mass * state.bit_count() for mass, state in zip(stationary, states)),
        F(0),
    )
    return 1 / mean - integrated_two_step(P)


def audit(weights, label):
    margin = promotion_margin(weights)
    if margin < 0:
        raise AssertionError((label, margin, weights))
    return margin


def main():
    frozen = [
        ("P3", matrix_from_edges(3, (1, 1, 0))),
        ("P3-1-4", matrix_from_edges(3, (1, 4, 0))),
        ("triangle-1-1-5", matrix_from_edges(3, (1, 5, 1))),
        ("K4-cycle4-diagonal1", matrix_from_edges(4, (4, 1, 4, 4, 1, 4))),
        (
            "n6-split",
            matrix_from_edges(
                6,
                (3, 300, 2, 5, 1, 3, 3, 1, 300, 1, 1, 1, 20, 1, 1),
            ),
        ),
        (
            "n6-rank-tail",
            matrix_from_edges(
                6,
                (1, 3, 3, 1000, 30, 1000, 300, 3, 1, 10, 1, 30, 1, 300, 30),
            ),
        ),
    ]
    for label, weights in frozen:
        margin = audit(weights, label)
        print(label, "PASS", float(margin))

    counts = []
    for n, values in ((3, (0, 1, 2, 5)), (4, (0, 1, 2))):
        count = 0
        zero = 0
        for weights in exhaustive_graphs(n, values):
            if not connected(weights):
                continue
            margin = audit(weights, f"exhaustive-n{n}-{count}")
            zero += margin == 0
            count += 1
        counts.append((n, count))
        print(f"exhaustive n={n}: {count} connected graphs PASS; {zero} kernel equalities")

    count = 0
    for weights in deterministic_graphs(5, 48, 26080805):
        if not connected(weights):
            continue
        audit(weights, f"deterministic-n5-{count}")
        count += 1
    counts.append((5, count))
    print(f"deterministic n=5: {count} connected graphs PASS")
    print("EXACT FINITE PROMOTION SCREEN PASS", counts)
    print("OPEN: universal stationary promotion")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact obstructions to simple subset-root-polynomial proofs at r=2."""

from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
OBSTRUCTION = HERE.parents[1] / "phase4_landmark_closure" / "obstruction"
CHI = OBSTRUCTION / "r2_entropy_certificate" / "chi_square_channel"
COLLISION = OBSTRUCTION / "r2_collision_closure"
sys.path.insert(0, str(CHI))
sys.path.insert(0, str(COLLISION))

from verify_resolvent_identities import solve  # noqa: E402
from verify_direct_flow_screen import matrix_from_edges  # noqa: E402


def level_law(weights):
    _, states, _, _, stationary = solve(weights)
    levels = [F(0) for _ in range(len(weights))]
    for state, mass in zip(states, stationary):
        levels[state.bit_count()] += mass
    assert sum(levels) == 1
    return levels


def main():
    # Complete K4: t(3+3t+t^2)/7 has negative quadratic discriminant.
    complete4 = matrix_from_edges(4, (1, 1, 1, 1, 1, 1))
    levels = level_law(complete4)
    assert levels[1:] == [F(3, 7), F(3, 7), F(1, 7)]
    assert levels[2] ** 2 - 4 * levels[1] * levels[3] == F(-3, 49)

    # The unweighted four-star violates ultra-log-concavity.
    star4 = matrix_from_edges(4, (1, 1, 1, 0, 0, 0))
    levels = level_law(star4)
    assert levels[1:] == [F(25, 36), F(1, 4), F(1, 18)]
    assert levels[2] ** 2 - 3 * levels[1] * levels[3] == F(-23, 432)

    # A connected weighted tree on five vertices violates ordinary
    # log-concavity at the first interior coefficient.
    tree5 = matrix_from_edges(
        5,
        (0, 1000, 7, 0, 0, 0, 7, 0, 7, 0),
    )
    levels = level_law(tree5)
    ordinary_gap = levels[2] ** 2 - levels[1] * levels[3]
    assert ordinary_gap < 0

    # The frozen reversible K6 witness violates subset-rank tail domination
    # while retaining the desired harmonic/mean sign.
    rank_tail6 = matrix_from_edges(
        6,
        (1, 3, 3, 1000, 30, 1000, 300, 3, 1, 10, 1, 30, 1, 300, 30),
    )
    levels = level_law(rank_tail6)
    complete = [F(comb(5, k), 31) for k in range(6)]
    assert sum(levels[2:]) > sum(complete[2:]) == F(26, 31)
    mean = sum(F(k) * levels[k] for k in range(1, 6))
    assert mean < F(80, 31)

    print("PASS: complete K4 subset-root polynomial is not real-rooted")
    print("PASS: exact K1,3 ultra-log-concavity counterexample")
    print("PASS: exact weighted-tree ordinary log-concavity counterexample")
    print("PASS: exact subset-rank tail-domination counterexample with surviving mean sign")
    print("OPEN: direct logarithmic-derivative bound at t=1")


if __name__ == "__main__":
    main()

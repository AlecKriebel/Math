#!/usr/bin/env python3
"""Reproducible numerical screen of regular-kernel midpoint concavity.

This file is a conjecture generator, not a proof certificate.  It samples the
polytope of symmetric stochastic zero-diagonal matrices by hit-and-run and
checks both the complete-graph comparison and midpoint Jensen slack.
"""

from __future__ import annotations

import argparse

import numpy as np

from search_regular_db import (
    hit_and_run,
    matrix_from_edges,
    regular_coordinates,
)
from search_db import baseline, fixation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=8)
    parser.add_argument("--pairs", type=int, default=250)
    parser.add_argument("--seed", type=int, default=20260802)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    for size in range(4, args.max_n + 1):
        edges, _, uniform, null = regular_coordinates(size)
        complete = baseline(size, 2.0)
        minimum_midpoint_slack = np.inf
        maximum_excess = -np.inf
        maximum_residual = 0.0
        for _ in range(args.pairs):
            x = hit_and_run(uniform, null, rng, 15 + 2 * size)
            y = hit_and_run(uniform, null, rng, 15 + 2 * size)
            first = matrix_from_edges(size, edges, uniform + null @ x)
            second = matrix_from_edges(size, edges, uniform + null @ y)
            midpoint = (first + second) / 2
            first_value, first_residual, _ = fixation(first, 2.0)
            second_value, second_residual, _ = fixation(second, 2.0)
            midpoint_value, midpoint_residual, _ = fixation(midpoint, 2.0)
            minimum_midpoint_slack = min(
                minimum_midpoint_slack,
                midpoint_value - (first_value + second_value) / 2,
            )
            maximum_excess = max(
                maximum_excess,
                first_value - complete,
                second_value - complete,
            )
            maximum_residual = max(
                maximum_residual,
                first_residual,
                second_residual,
                midpoint_residual,
            )
        assert maximum_residual < 1e-8
        print(
            f"n={size} pairs={args.pairs} "
            f"max_complete_excess={maximum_excess:.12g} "
            f"min_midpoint_slack={minimum_midpoint_slack:.12g} "
            f"max_residual={maximum_residual:.3g}"
        )

    print(
        "INTERIOR NUMERICAL SCREEN ONLY: the certified near-boundary "
        "order-seven counterexample is in verify_concavity_counterexample.py"
    )


if __name__ == "__main__":
    main()

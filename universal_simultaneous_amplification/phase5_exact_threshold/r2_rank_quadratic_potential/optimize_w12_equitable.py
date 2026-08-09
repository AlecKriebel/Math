#!/usr/bin/env python3
"""Hostile outer optimization against the combined W12 certificate.

Floating discovery only.  Any positive gap must be transferred to the
independent rational verifier before being recorded as an exact result.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import differential_evolution

from hostile_w12_equitable import W12Equitable


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="1,1,1,2,3,5")
    parser.add_argument("--bound", type=float, default=14.0)
    parser.add_argument("--iterations", type=int, default=12)
    parser.add_argument("--popsize", type=int, default=4)
    parser.add_argument("--seed", type=int, default=26080831)
    parser.add_argument("--polish", action="store_true")
    parser.add_argument(
        "--extra",
        default="",
        help="comma-separated extra pair columns accepted by the sparse solver",
    )
    args = parser.parse_args()

    sizes = tuple(int(value) for value in args.sizes.split(","))
    extra_pairs = tuple(name for name in args.extra.split(",") if name)
    quotient = W12Equitable(sizes, extra_pairs)
    entries = [
        (a, b) for a in range(len(sizes)) for b in range(a, len(sizes))
    ]
    best = [-float("inf"), None]
    evaluations = 0

    def objective(logs_tail):
        nonlocal evaluations
        logs = np.concatenate(([0.0], logs_tail))
        weights = np.zeros((len(sizes), len(sizes)))
        for (a, b), value in zip(entries, np.exp(logs)):
            weights[a, b] = weights[b, a] = value
        result = quotient.solve(weights)
        evaluations += 1
        if not result.success:
            return 10.0
        gap = result.fun - quotient.baseline
        if gap > best[0]:
            best[:] = [gap, logs.copy()]
            print("best", evaluations, gap, logs.tolist(), flush=True)
        return -gap

    differential_evolution(
        objective,
        [(-args.bound, args.bound)] * (len(entries) - 1),
        seed=args.seed,
        popsize=args.popsize,
        maxiter=args.iterations,
        polish=args.polish,
        updating="immediate",
    )
    print("sizes", sizes)
    print("extra pairs", extra_pairs)
    print("states", len(quotient.transient), "dimension", len(quotient.keys))
    print("evaluations", evaluations)
    print("best gap", best[0])
    print("best logs", best[1].tolist())


if __name__ == "__main__":
    main()

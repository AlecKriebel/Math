#!/usr/bin/env python3
"""Discovery-only adjoint search for the one-third affine endpoint score.

This deliberately reuses only the transition/adjoint implementation from the
independent hostile-search folder.  Any apparent violation must be rebuilt by
the exact verifier before it can enter the claims ledger.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


HOSTILE = Path(__file__).resolve().parents[1] / "endpoint_hostile_exact"
sys.path.insert(0, str(HOSTILE))
from search_endpoint_adjoint import baseline, fixation_gradient  # noqa: E402


def optimize(n: int, starts: int, seed: int, iterations: int, scale: float) -> None:
    dimension = n * (n - 1) // 2
    best = None
    for start in range(starts):
        rng = np.random.default_rng(seed + start)
        initial = rng.normal(0.0, scale, dimension)

        def loss(logs):
            bd, grad_bd = fixation_gradient(logs, n, "Bd")
            db, grad_db = fixation_gradient(logs, n, "dB")
            x = bd / baseline(n, "Bd")
            y = db / baseline(n, "dB")
            score = (x + 2.0 * y) / 3.0
            gradient = (
                grad_bd / baseline(n, "Bd")
                + 2.0 * grad_db / baseline(n, "dB")
            ) / 3.0
            return -score, -gradient

        result = minimize(
            loss,
            initial,
            jac=True,
            method="L-BFGS-B",
            bounds=[(-24.0, 24.0)] * dimension,
            options={"maxiter": iterations, "ftol": 1e-14, "gtol": 1e-9},
        )
        bd, _ = fixation_gradient(result.x, n, "Bd")
        db, _ = fixation_gradient(result.x, n, "dB")
        x = bd / baseline(n, "Bd")
        y = db / baseline(n, "dB")
        score = (x + 2.0 * y) / 3.0
        spread = float(np.max(result.x) - np.min(result.x))
        print(
            f"start={start} success={result.success} nit={result.nit} "
            f"score={score:.16g} x={x:.16g} y={y:.16g} "
            f"log_spread={spread:.8g}",
            flush=True,
        )
        if best is None or score > best[0]:
            best = (score, x, y, result.x - result.x.mean())
    print("BEST", best, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=7)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=260808)
    parser.add_argument("--iterations", type=int, default=250)
    parser.add_argument("--scale", type=float, default=6.0)
    args = parser.parse_args()
    optimize(args.n, args.starts, args.seed, args.iterations, args.scale)


if __name__ == "__main__":
    main()

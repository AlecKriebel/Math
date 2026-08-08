#!/usr/bin/env python3
"""Discovery search for the exact affine L--C--D dual split.

At r=3/2 put x=m_L/b, z=m_C/b, and y=m_D/d.  The one-third target is

    x + 2*y - 3 = (x + 2*z - 3) + 2*(y-z).

This script separately maximizes the orientation and batching terms on a
complete weighted support.  Numerical output is never a proof.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution


HERE = Path(__file__).resolve()
SIGNED = HERE.parents[2] / "obstruction" / "signed_cut_capacity"
OBSTRUCTION = HERE.parents[2] / "obstruction"
sys.path.insert(0, str(SIGNED))
sys.path.insert(0, str(OBSTRUCTION))

from search_adjoint_split import (  # noqa: E402
    link_fixation,
    weights_from_logs,
)
from search_random import baseline, fixation  # noqa: E402


R = 1.5


def quantities(logs: np.ndarray, n: int) -> tuple[float, float, float, float, float, float]:
    weights = weights_from_logs(n, logs)
    p = weights / weights.sum(axis=1)[:, None]
    x = link_fixation(p) / baseline(n, R, "Bd")
    z = link_fixation(p.T) / baseline(n, R, "Bd")
    y = fixation(weights, R, "dB") / baseline(n, R, "dB")
    orientation = (x + 2.0 * z) / 3.0 - 1.0
    batching = y - z
    target = (x + 2.0 * y) / 3.0 - 1.0
    return orientation, batching, target, x, y, z


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--span", type=float, default=14.0)
    parser.add_argument("--iterations", type=int, default=120)
    parser.add_argument("--popsize", type=int, default=10)
    parser.add_argument("--seed", type=int, default=260808)
    args = parser.parse_args()
    dimension = args.n * (args.n - 1) // 2

    for which, name in ((0, "orientation"), (1, "batching")):
        best = [-np.inf, None]

        def objective(logs: np.ndarray) -> float:
            try:
                value = quantities(logs, args.n)[which]
            except (FloatingPointError, np.linalg.LinAlgError):
                return 1e6
            if value > best[0]:
                best[:] = value, logs.copy()
            return -value

        differential_evolution(
            objective,
            [(-args.span, args.span)] * dimension,
            seed=args.seed + which,
            popsize=args.popsize,
            maxiter=args.iterations,
            polish=True,
            updating="immediate",
            workers=1,
            tol=1e-9,
            x0=np.zeros(dimension),
        )
        assert best[1] is not None
        values = quantities(best[1], args.n)
        print(name, "best", values, flush=True)
        print("weights", weights_from_logs(args.n, best[1]).tolist(), flush=True)


if __name__ == "__main__":
    main()

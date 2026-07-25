#!/usr/bin/env python3
"""Discovery LP for a Delsarte polynomial augmented by a local count."""

from __future__ import annotations

import argparse
import json

import cvxpy as cp
import numpy as np


def gegenbauer_table(points: np.ndarray, degree: int) -> np.ndarray:
    """Normalized dimension-five Gegenbauer polynomials P_0,...,P_degree."""
    table = np.empty((len(points), degree + 1), dtype=float)
    table[:, 0] = 1.0
    if degree:
        table[:, 1] = points
    for k in range(2, degree + 1):
        table[:, k] = (
            (2 * k + 1) * points * table[:, k - 1]
            - (k - 1) * table[:, k - 2]
        ) / (k + 2)
    return table


def solve(degree: int, grid_size: int, solver: str) -> dict[str, object]:
    low = np.linspace(-1.0, 0.25, grid_size, endpoint=False)
    high = np.linspace(0.25, 0.5, max(2, grid_size // 5 + 1))
    low_table = gegenbauer_table(low, degree)
    high_table = gegenbauer_table(high, degree)

    coefficients = cp.Variable(degree + 1)
    low_ceiling = cp.Variable()
    high_ceiling = cp.Variable()
    constraints = [
        coefficients[0] == 1,
        coefficients[1:] >= 0,
        low_table @ coefficients <= low_ceiling,
        high_table @ coefficients <= high_ceiling,
        high_ceiling >= low_ceiling,
    ]
    objective = cp.Minimize(
        cp.sum(coefficients) + 17 * low_ceiling + 23 * high_ceiling
    )
    problem = cp.Problem(objective, constraints)
    problem.solve(
        solver=solver,
        tol_gap_abs=1e-10,
        tol_feas=1e-10,
        tol_gap_rel=1e-10,
        max_iter=200000,
    )
    return {
        "degree": degree,
        "grid_size": grid_size,
        "solver": solver,
        "status": problem.status,
        "objective": problem.value,
        "low_ceiling": float(np.asarray(low_ceiling.value).item()),
        "high_ceiling": float(np.asarray(high_ceiling.value).item()),
        "coefficients": coefficients.value.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=24)
    parser.add_argument("--grid-size", type=int, default=10001)
    parser.add_argument("--solver", default="CLARABEL")
    args = parser.parse_args()
    print(
        json.dumps(
            solve(args.degree, args.grid_size, args.solver),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Discovery only: find and rationalize a local row-energy counterexample.

This script depends on NumPy and SciPy and its optimizer status is never
trusted by the exact verifier.  It starts from random 25-point subsets of
the D5 code, optimizes one anchored row at the stricter cap 0.492, rotates
the anchor to e_1, and rationalizes every other point through the standard
stereographic parametrization of the rational unit sphere.
"""

from __future__ import annotations

from fractions import Fraction as Q
import itertools
import json
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "local_row_energy_counterexample.json"
CAP = 0.492
TOTAL = 25
TRIALS = 48
SEED = 2026072401
MAX_DENOMINATOR = 1_000_000


def d5() -> np.ndarray:
    points = []
    for i, j in itertools.combinations(range(5), 2):
        for first, second in itertools.product((-1, 1), repeat=2):
            point = np.zeros(5)
            point[i] = first / np.sqrt(2)
            point[j] = second / np.sqrt(2)
            points.append(point)
    return np.asarray(points)


def rational_sphere_point(point: np.ndarray) -> list[Q]:
    """Rational point close to point, using the chart away from -e_1."""

    parameters = [
        Q(float(value)).limit_denominator(MAX_DENOMINATOR)
        for value in point[1:] / (1.0 + point[0])
    ]
    norm_square = sum((value * value for value in parameters), Q(0))
    denominator = 1 + norm_square
    return [
        (1 - norm_square) / denominator,
        *(2 * value / denominator for value in parameters),
    ]


def main() -> None:
    roots = d5()
    anchor = roots[0]
    number = TOTAL - 1
    pairs = np.asarray(
        list(itertools.combinations(range(number), 2)), dtype=int
    )

    def objective(flat: np.ndarray) -> float:
        points = flat.reshape(number, 5)
        return -float(np.sum((points @ anchor) ** 2))

    def objective_jacobian(flat: np.ndarray) -> np.ndarray:
        points = flat.reshape(number, 5)
        heights = points @ anchor
        return (-2 * heights[:, None] * anchor).ravel()

    def norms(flat: np.ndarray) -> np.ndarray:
        points = flat.reshape(number, 5)
        return np.sum(points * points, axis=1) - 1

    def cap_constraints(flat: np.ndarray) -> np.ndarray:
        points = flat.reshape(number, 5)
        return np.r_[
            CAP - points @ anchor,
            CAP
            - np.sum(
                points[pairs[:, 0]] * points[pairs[:, 1]], axis=1
            ),
        ]

    rng = np.random.default_rng(SEED)
    best = None
    reports = []
    for trial in range(TRIALS):
        selection = np.sort(
            rng.choice(np.arange(1, 40), size=number, replace=False)
        )
        initial = roots[selection]
        result = minimize(
            objective,
            initial.ravel(),
            jac=objective_jacobian,
            method="SLSQP",
            constraints=[
                {"type": "eq", "fun": norms},
                {"type": "ineq", "fun": cap_constraints},
            ],
            options={"maxiter": 2500, "ftol": 2e-12, "disp": False},
        )
        norm_error = float(np.max(np.abs(norms(result.x))))
        cap_margin = float(np.min(cap_constraints(result.x)))
        feasible = norm_error <= 2e-7 and cap_margin >= -2e-7
        reports.append(
            {
                "trial": trial,
                "success": bool(result.success),
                "feasible_to_tolerance": feasible,
                "off_diagonal_row_energy": -float(result.fun),
                "norm_error": norm_error,
                "cap_margin": cap_margin,
                "iterations": int(result.nit),
            }
        )
        if feasible and (best is None or result.fun < best.fun):
            best = result

    if best is None:
        raise RuntimeError("no numerically feasible candidate")

    # An explicit orthogonal change of coordinates sends the selected D5
    # anchor (-1,-1,0,0,0)/sqrt(2) to e_1.
    points = best.x.reshape(number, 5)
    rotated = np.column_stack(
        (
            -(points[:, 0] + points[:, 1]) / np.sqrt(2),
            (points[:, 0] - points[:, 1]) / np.sqrt(2),
            points[:, 2],
            points[:, 3],
            points[:, 4],
        )
    )
    rational_points = [[Q(1), Q(0), Q(0), Q(0), Q(0)]]
    rational_points.extend(rational_sphere_point(point) for point in rotated)

    def encode(value: Q) -> str:
        return str(value)

    exact_maximum = max(
        sum(
            (left[k] * right[k] for k in range(5)),
            Q(0),
        )
        for left, right in itertools.combinations(rational_points, 2)
    )
    exact_row_energy = sum(
        (point[0] * point[0] for point in rational_points), Q(0)
    )
    payload = {
        "schema": "weighted-common-source.local-row-energy-counterexample.v1",
        "status": "EXACT RATIONAL SPHERICAL CODE COUNTEREXAMPLE",
        "scope": (
            "Refutes only the proposed universal row-square-energy upper "
            "bound 41/5; it is not a 41-point code."
        ),
        "discovery": {
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "seed": SEED,
            "trials": TRIALS,
            "optimization_cap": CAP,
            "maximum_stereographic_denominator": MAX_DENOMINATOR,
            "reports": reports,
        },
        "points": [
            [encode(coordinate) for coordinate in point]
            for point in rational_points
        ],
        "claimed_exact_maximum_inner_product": encode(exact_maximum),
        "claimed_exact_anchor_row_energy": encode(exact_row_energy),
        "comparison_threshold": "41/5",
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "maximum_inner_product": str(exact_maximum),
                "anchor_row_energy": str(exact_row_energy),
                "beats_41_over_5": exact_row_energy > Q(41, 5),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

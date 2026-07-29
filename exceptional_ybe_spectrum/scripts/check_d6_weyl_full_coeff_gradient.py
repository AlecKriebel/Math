#!/usr/bin/env python3
"""Finite-difference audit for the full 19 x 19 Weyl coefficient gradient."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from d6_weyl_full_coeff_search import (
    FRAME_SIZE,
    FullCoefficientModel,
)


SEED = 26073690
WEIGHTS = (0.0, 0.37, 10.0)
EPSILONS = (1e-4, 3e-5, 1e-5, 3e-6)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    model = FullCoefficientModel.build()
    rng = np.random.default_rng(SEED)
    points = {
        "generic": rng.normal(size=FRAME_SIZE * FRAME_SIZE)
        / np.sqrt(FRAME_SIZE),
        "h0": model.h0_coefficients().reshape(-1),
    }
    direction = rng.normal(size=FRAME_SIZE * FRAME_SIZE)
    direction /= np.linalg.norm(direction)

    cases: list[dict[str, object]] = []
    maximum_relative_error = 0.0
    for point_name, point in points.items():
        for cubic_weight in WEIGHTS:
            objective, gradient, diagnostics = model.objective_and_gradient(
                point, cubic_weight
            )
            analytic = float(np.dot(gradient, direction))
            finite_differences = []
            for epsilon in EPSILONS:
                plus, _, _ = model.objective_and_gradient(
                    point + epsilon * direction,
                    cubic_weight,
                )
                minus, _, _ = model.objective_and_gradient(
                    point - epsilon * direction,
                    cubic_weight,
                )
                estimate = (plus - minus) / (2 * epsilon)
                relative_error = abs(estimate - analytic) / max(
                    1.0, abs(analytic), abs(estimate)
                )
                maximum_relative_error = max(
                    maximum_relative_error, relative_error
                )
                finite_differences.append(
                    {
                        "epsilon": epsilon,
                        "estimate": estimate,
                        "relative_error": relative_error,
                    }
                )
            cases.append(
                {
                    "point": point_name,
                    "cubic_weight": cubic_weight,
                    "objective": objective,
                    "analytic_directional_derivative": analytic,
                    "diagnostics": diagnostics,
                    "finite_differences": finite_differences,
                }
            )

    h0 = model.h0_coefficients()
    h0_matrix, h0_involution, h0_cubic = model.residuals(h0)
    payload = {
        "seed": SEED,
        "weights": WEIGHTS,
        "epsilons": EPSILONS,
        "cases": cases,
        "maximum_relative_error_over_all_epsilons": maximum_relative_error,
        "h0": {
            "trace": [
                float(np.trace(h0_matrix).real),
                float(np.trace(h0_matrix).imag),
            ],
            "hermiticity_norm": float(
                np.linalg.norm(h0_matrix - h0_matrix.conj().T)
            ),
            "involution_norm": float(np.linalg.norm(h0_involution)),
            "cubic_norm": float(np.linalg.norm(h0_cubic)),
        },
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    print(rendered)
    # The smallest epsilons are the meaningful calibration; the loose bound
    # catches index/adjoint mistakes while tolerating cancellation at H0.
    meaningful_errors = [
        row["finite_differences"][2]["relative_error"]
        for row in cases
    ]
    assert max(meaningful_errors) < 2e-7
    assert np.linalg.norm(h0_cubic) < 1e-12
    assert abs(np.trace(h0_matrix)) < 1e-12
    print("PASS")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\nPASS\n", encoding="utf-8")


if __name__ == "__main__":
    main()

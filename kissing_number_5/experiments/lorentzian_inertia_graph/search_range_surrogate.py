#!/usr/bin/env python3
"""Discovery-only search for a bounded Lorentzian rank-six surrogate.

For unit rows y_i in R^5, minimize

    4 max_{i<j} <y_i,y_j> - min_{i<j} <y_i,y_j>.

A value below 3 leaves an interval of rational s for which

    A = (K-sJ)/(1-s)

has diagonal one and every off-diagonal entry strictly between -3 and 0.
The committed certificate was obtained by rounding stereographic
coordinates from a run of this search and is verified independently with
exact arithmetic.  No theorem trusts this optimizer or its output.
"""

from __future__ import annotations

import argparse
import json

import numpy as np
from scipy.optimize import minimize


N = 41
D = 5
PAIRS = np.triu_indices(N, 1)


def normalize_rows(flat: np.ndarray) -> np.ndarray:
    matrix = flat.reshape(N, D)
    return matrix / np.linalg.norm(matrix, axis=1)[:, None]


def smooth_objective_gradient(
    flat: np.ndarray, beta: float
) -> tuple[float, np.ndarray]:
    points = normalize_rows(flat)
    left, right = PAIRS
    inner = np.sum(points[left] * points[right], axis=1)

    positive_scaled = beta * inner
    positive_maximum = float(np.max(positive_scaled))
    positive_exponentials = np.exp(
        positive_scaled - positive_maximum
    )
    positive_weights = positive_exponentials / np.sum(positive_exponentials)

    negative_scaled = -beta * inner
    negative_maximum = float(np.max(negative_scaled))
    negative_exponentials = np.exp(
        negative_scaled - negative_maximum
    )
    negative_weights = negative_exponentials / np.sum(negative_exponentials)

    value = (
        4
        * (
            positive_maximum
            + np.log(np.sum(positive_exponentials))
        )
        / beta
        + (
            negative_maximum
            + np.log(np.sum(negative_exponentials))
        )
        / beta
    )

    pair_weights = 4 * positive_weights - negative_weights
    point_gradient = np.zeros_like(points)
    np.add.at(
        point_gradient,
        left,
        pair_weights[:, None] * points[right],
    )
    np.add.at(
        point_gradient,
        right,
        pair_weights[:, None] * points[left],
    )

    raw = flat.reshape(N, D)
    raw_norms = np.linalg.norm(raw, axis=1)
    tangent_gradient = point_gradient - (
        np.sum(point_gradient * points, axis=1)[:, None] * points
    )
    flat_gradient = (tangent_gradient / raw_norms[:, None]).ravel()
    return float(value), flat_gradient


def diagnostics(points: np.ndarray) -> dict[str, float]:
    gram = points @ points.T
    values = gram[PAIRS]
    maximum = float(np.max(values))
    minimum = float(np.min(values))
    return {
        "maximum_inner_product": maximum,
        "minimum_inner_product": minimum,
        "range_objective": 4 * maximum - minimum,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=72541)
    parser.add_argument("--starts", type=int, default=6)
    parser.add_argument("--iterations", type=int, default=400)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    beta_schedule = [5, 10, 20, 40, 80, 160, 320]
    records = []
    best_points = None
    best_value = float("inf")
    for start in range(args.starts):
        flat = rng.normal(size=(N, D)).ravel()
        for beta in beta_schedule:
            result = minimize(
                lambda current: smooth_objective_gradient(current, beta),
                flat,
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": args.iterations,
                    "ftol": 1e-12,
                    "gtol": 1e-8,
                    "maxls": 30,
                },
            )
            flat = result.x
        points = normalize_rows(flat)
        record = {
            "start": start,
            **diagnostics(points),
        }
        records.append(record)
        if record["range_objective"] < best_value:
            best_value = record["range_objective"]
            best_points = points.copy()

    assert best_points is not None
    print(
        json.dumps(
            {
                "schema": "kissing5.lorentzian_range_search.discovery.v1",
                "status": "NUMERICAL_EVIDENCE_ONLY",
                "seed": args.seed,
                "starts": args.starts,
                "iterations_per_beta": args.iterations,
                "beta_schedule": beta_schedule,
                "records": records,
                "best": {
                    **diagnostics(best_points),
                    "coordinates": best_points.tolist(),
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

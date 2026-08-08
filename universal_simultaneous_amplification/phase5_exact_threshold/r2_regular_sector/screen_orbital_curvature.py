#!/usr/bin/env python3
"""Hostile floating screen for transposition-orbital curvature.

For a symmetric stochastic zero-diagonal kernel P and the transposition
sigma=(0 1), write M=(P+P^sigma)/2 and D=(P-P^sigma)/2.  The orbital
fixation profile f(t)=rho_dB(M+tD,2) is even.  This script searches both for
negative endpoint slack f(0)-f(1) and for positive midpoint curvature, which
would provide a local counterexample.  Floating output is discovery only.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import minimize


HERE = Path(__file__).resolve()
REGULAR = HERE.parents[2] / "phase4_landmark_closure" / "obstruction" / "regular_db_max"
DB_MAX = HERE.parents[2] / "phase4_landmark_closure" / "obstruction" / "db_maximizer"
sys.path.insert(0, str(REGULAR))
sys.path.insert(0, str(DB_MAX))

from search_regular_db import (  # noqa: E402
    hit_and_run,
    matrix_from_edges,
    regular_coordinates,
)
from search_db import fixation  # noqa: E402


def conjugate(P: np.ndarray) -> np.ndarray:
    order = np.arange(len(P))
    order[0], order[1] = 1, 0
    return P[np.ix_(order, order)]


def rho(P: np.ndarray) -> float:
    value, residual, _ = fixation(P, 2.0)
    if residual > 2e-8:
        raise np.linalg.LinAlgError(residual)
    return value


def orbital_data(P: np.ndarray, step: float = 1e-3):
    M = (P + conjugate(P)) / 2
    D = (P - conjugate(P)) / 2
    middle = rho(M)
    endpoint = rho(P)
    plus = rho(M + step * D)
    minus = rho(M - step * D)
    curvature = (plus + minus - 2 * middle) / step**2
    return middle - endpoint, curvature, middle, endpoint


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=26080811)
    parser.add_argument("--polish", type=int, default=2)
    args = parser.parse_args()

    edges, _, uniform, null = regular_coordinates(args.n)
    rng = np.random.default_rng(args.seed)
    records = []
    for sample in range(args.samples):
        x = hit_and_run(uniform, null, rng, 8 + args.n)
        P = matrix_from_edges(args.n, edges, uniform + null @ x)
        try:
            gap, curvature, middle, endpoint = orbital_data(P)
        except np.linalg.LinAlgError:
            continue
        records.append((gap, curvature, x, middle, endpoint))
        if sample and sample % 100 == 0:
            print(
                f"sample={sample} min_gap={min(r[0] for r in records):.9g} "
                f"max_curvature={max(r[1] for r in records):.9g}",
                flush=True,
            )

    if not records:
        raise RuntimeError("no valid samples")
    minimum = min(records, key=lambda item: item[0])
    maximum_curvature = max(records, key=lambda item: item[1])
    sample_records = records.copy()

    # Polish the endpoint-gap minimum while retaining positivity of all edge
    # weights.  This is only a hostile numerical search.
    floor = 1e-9

    def objective(x):
        edge_weights = uniform + null @ x
        if np.min(edge_weights) <= floor:
            return 1.0 + float(np.sum(np.minimum(edge_weights - floor, 0) ** 2))
        P = matrix_from_edges(args.n, edges, edge_weights)
        try:
            return orbital_data(P)[0]
        except np.linalg.LinAlgError:
            return 1.0

    starts = [minimum[2], maximum_curvature[2]]
    starts.extend(record[2] for record in sorted(records, key=lambda item: item[0])[: args.polish])
    for start in starts:
        result = minimize(
            objective,
            start,
            method="SLSQP",
            constraints={"type": "ineq", "fun": lambda x: uniform + null @ x - floor},
            options={"maxiter": 1000, "ftol": 1e-14, "disp": False},
        )
        edge_weights = uniform + null @ result.x
        if np.min(edge_weights) > 0:
            P = matrix_from_edges(args.n, edges, edge_weights)
            records.append((*orbital_data(P)[:2], result.x, *orbital_data(P)[2:]))

    # The raw gap has a flat zero manifold D=0.  Minimize the secant quotient
    # gap/||D||^2 as a separate hostile target so polishing cannot manufacture
    # a vacuous optimum by erasing the odd direction.
    def normalized_objective(x):
        edge_weights = uniform + null @ x
        if np.min(edge_weights) <= floor:
            return 10.0
        P = matrix_from_edges(args.n, edges, edge_weights)
        D = (P - conjugate(P)) / 2
        norm = float(np.sum(D * D))
        if norm < 1e-10:
            return 10.0
        try:
            return orbital_data(P)[0] / norm
        except np.linalg.LinAlgError:
            return 10.0

    normalized_records = []
    def sampled_quotient(record):
        candidate = matrix_from_edges(args.n, edges, uniform + null @ record[2])
        odd = (candidate - conjugate(candidate)) / 2
        return record[0] / max(float(np.sum(odd * odd)), 1e-12)

    starts = [
        record[2]
        for record in sorted(sample_records, key=sampled_quotient)[: max(2, args.polish)]
    ]
    for start in starts:
        result = minimize(
            normalized_objective,
            start,
            method="SLSQP",
            constraints={"type": "ineq", "fun": lambda x: uniform + null @ x - floor},
            options={"maxiter": 1500, "ftol": 1e-14, "disp": False},
        )
        if np.min(uniform + null @ result.x) > 0:
            normalized_records.append((normalized_objective(result.x), result.x))

    minimum = min(records, key=lambda item: item[0])
    maximum_curvature = max(records, key=lambda item: item[1])
    print("minimum_gap", minimum[0])
    print("maximum_curvature", maximum_curvature[1])
    if normalized_records:
        quotient, quotient_x = min(normalized_records, key=lambda item: item[0])
        print("minimum_normalized_gap", quotient)
        quotient_P = matrix_from_edges(args.n, edges, uniform + null @ quotient_x)
        print("normalized_min_edge", np.min(uniform + null @ quotient_x))
        print("normalized_P=")
        print(np.array2string(quotient_P, precision=16, max_line_width=240))
    for label, record in (("minimum", minimum), ("curvature", maximum_curvature)):
        edge_weights = uniform + null @ record[2]
        P = matrix_from_edges(args.n, edges, edge_weights)
        print(label, "middle", record[3], "endpoint", record[4])
        print(label, "min_edge", np.min(edge_weights))
        print(label, "P=")
        print(np.array2string(P, precision=16, max_line_width=240))
    print("NUMERICAL DISCOVERY ONLY")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent numerical recomputation of an atomic search result.

This checker does not use CVXPY or solver state.  It rebuilds all moment
matrices and scalar inequalities from the stored masses.  The result remains
numerical evidence, because the masses are floating point.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
import math
from pathlib import Path

import numpy as np

from experiments.continuous_rank_bv_search.search import (
    N,
    coefficient_arrays,
    default_kernels,
    exact_rank_values,
    gegenbauer_5,
    stratified_capacity_rows,
    weighted_capacity_rows,
)


def frame_minimum(nodes, alpha) -> float:
    values = np.array(
        [
            [float(value) for value in gegenbauer_5(node, 3)]
            for node in nodes
        ]
    )
    dimensions = (1, 5, 14, 30)
    subsets = (
        (1,),
        (0, 1),
        (2,),
        (0, 2),
        (1, 2),
        (0, 1, 2),
        (3,),
        (0, 3),
        (1, 3),
        (0, 1, 3),
    )
    minimum = math.inf
    for subset in subsets:
        rank = sum(dimensions[index] for index in subset)
        matrix = np.array(
            [
                [
                    1
                    + np.dot(
                        alpha, values[:, first] * values[:, second]
                    )
                    - N / rank
                    for second in subset
                ]
                for first in subset
            ]
        )
        minimum = min(minimum, float(np.linalg.eigvalsh(matrix)[0]))
    return minimum


def check(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text())
    assert data["schema"] == "continuous-rank-bv-atomic-search-v1"
    nodes = tuple(Q(value) for value in data["grid"])
    orbits = tuple(tuple(item) for item in data["triple_orbits"])
    alpha = np.asarray(data["alpha"], dtype=float)
    nu = np.asarray(data["nu"], dtype=float)
    harmonic_degree = int(
        data["bv_full_radial_harmonic_degrees"].split("..")[1]
    )
    pair_degree = int(data["ordinary_pair_degrees"].split("..")[1])

    constants, alpha_arrays, nu_arrays = coefficient_arrays(
        nodes, orbits, harmonic_degree
    )
    active_eigenvalues = []
    full_eigenvalues = []
    kernel_residual = None
    m = len(nodes)
    for degree in range(harmonic_degree + 1):
        size = m + 1
        matrix = constants[degree] + (
            alpha_arrays[degree] @ alpha + nu_arrays[degree] @ nu
        ).reshape((size, size))
        full_eigenvalues.append(float(np.linalg.eigvalsh(matrix)[0]))
        active = matrix[:m, :m] if degree == 0 else matrix[1:m, 1:m]
        active_eigenvalues.append(float(np.linalg.eigvalsh(active)[0]))
        if degree == 0:
            vector = np.r_[np.full(m, -1 / 40), 1.0]
            kernel_residual = float(np.max(np.abs(matrix @ vector)))

    pair_table = np.array(
        [
            [float(value) for value in gegenbauer_5(node, pair_degree)]
            for node in nodes
        ]
    )
    pair_moments = 1 + pair_table[:, 1:].T @ alpha

    marginal_errors = []
    for index in range(m):
        incidence = np.array(
            [triple.count(index) / 3 for triple in orbits]
        )
        marginal_errors.append(
            float(incidence @ nu - (N - 2) * alpha[index])
        )

    stratified_slacks = []
    for row in stratified_capacity_rows(nodes, orbits):
        left = np.dot(row["nu_coefficients"], nu)
        right = (
            3
            * row["capacity"]
            * np.sum(alpha[list(row["alpha_indices"])])
        )
        stratified_slacks.append(float(right - left))
    weighted_slacks = []
    for row in weighted_capacity_rows(nodes, orbits):
        left = np.dot(row["nu_coefficients"], nu)
        right = 3 * sum(
            capacity * alpha[index]
            for index, capacity in row["capacities"].items()
        )
        weighted_slacks.append(float(right - left))

    kernels = {kernel.name: kernel for kernel in default_kernels("rich")}
    band_slacks = {}
    sharp_slacks = {}
    variance_cell_slacks = {}
    for band in data["rank_outer_bands"]:
        kernel = kernels[band["kernel"]]
        variance, centered, residual = exact_rank_values(
            kernel, nodes, orbits, alpha, nu
        )
        sharp_slacks[kernel.name] = float(residual)
        if band["band_type"] == "fixed-pair-constant":
            bound = float(Q(band["radius"]))
            band_slack = bound - abs(centered)
            variance_slack = math.inf
        elif band["band_type"] == "local-rational-chord":
            lower = float(Q(band["variance_lower"]))
            upper = float(Q(band["variance_upper"]))
            slope = float(Q(band["slope"]))
            intercept = float(Q(band["intercept"]))
            band_slack = slope * variance + intercept - abs(centered)
            variance_slack = min(variance - lower, upper - variance)
        else:
            upper = float(Q(band["variance_upper"]))
            slope = float(Q(band["slope"]))
            band_slack = slope * variance - abs(centered)
            variance_slack = min(variance, upper - variance)
        band_slacks[kernel.name] = float(band_slack)
        variance_cell_slacks[kernel.name] = float(variance_slack)

    report = {
        "schema": "continuous-rank-bv-independent-numerical-check-v1",
        "source": path.name,
        "warning": "NUMERICAL EVIDENCE ONLY: stored masses are floating point",
        "minimum_alpha": float(np.min(alpha)),
        "minimum_nu": float(np.min(nu)),
        "alpha_mass_error": float(np.sum(alpha) - (N - 1)),
        "nu_mass_error": float(np.sum(nu) - (N - 1) * (N - 2)),
        "maximum_marginal_error": max(abs(value) for value in marginal_errors),
        "w0_forced_kernel_residual": kernel_residual,
        "minimum_active_bv_eigenvalue": min(active_eigenvalues),
        "active_bv_eigenvalues": active_eigenvalues,
        "minimum_full_bv_eigenvalue": min(full_eigenvalues),
        "minimum_pair_moment": float(np.min(pair_moments)),
        "minimum_frame_eigenvalue": frame_minimum(nodes, alpha),
        "minimum_stratified_capacity_slack": min(stratified_slacks),
        "minimum_weighted_capacity_slack": min(weighted_slacks),
        "minimum_rank_outer_band_slack": min(band_slacks.values()),
        "minimum_variance_cell_slack": min(variance_cell_slacks.values()),
        "minimum_sharp_rank_residual": min(sharp_slacks.values()),
        "all_sharp_rank_residuals_nonnegative": all(
            value >= 0 for value in sharp_slacks.values()
        ),
        "band_slacks": band_slacks,
        "variance_cell_slacks": variance_cell_slacks,
        "sharp_rank_residuals": sharp_slacks,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = check(args.result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n"
        )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

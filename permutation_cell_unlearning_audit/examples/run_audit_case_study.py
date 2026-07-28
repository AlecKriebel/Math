#!/usr/bin/env python3
"""Reproducible checks for the permutation-cell unlearning audit.

The experiment is intentionally small and inspectable:

* deterministic ridge regression on scikit-learn's bundled diabetes data;
* a fixed-preconditioner, relinearized per-record deletion protocol;
* exact relation-cell algebra and exact retained-data ridge targets;
* all six orders of one selected three-record deletion set;
* a bounded-kernel stochastic route-law audit.

This is a mathematical case study, not a claim about clinical prediction or a
benchmark of production machine-unlearning systems.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
import sklearn
from sklearn.datasets import load_diabetes


SEED = 20260728
RIDGE_LAMBDA = 0.05
STOCHASTIC_REPLICATES = 3000
STOCHASTIC_DELTA = 0.05
STOCHASTIC_EPSILON = 0.10
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def to_builtin(value):
    """Recursively convert NumPy values to JSON-compatible Python values."""
    if isinstance(value, dict):
        return {str(key): to_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_builtin(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def digest_arrays(*arrays: np.ndarray) -> str:
    digest = hashlib.sha256()
    for array in arrays:
        contiguous = np.ascontiguousarray(array)
        digest.update(str(contiguous.shape).encode("utf-8"))
        digest.update(str(contiguous.dtype).encode("utf-8"))
        digest.update(contiguous.tobytes())
    return digest.hexdigest()


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def ridge_state(x: np.ndarray, y: np.ndarray, ridge_lambda: float):
    dimension = x.shape[1]
    hessian = ridge_lambda * np.eye(dimension) + x.T @ x
    linear = x.T @ y
    theta = np.linalg.solve(hessian, linear)
    return hessian, linear, theta


def affine_delete(
    theta: np.ndarray,
    record: int,
    x: np.ndarray,
    y: np.ndarray,
    preconditioner: np.ndarray,
    amplitude: float = 1.0,
) -> np.ndarray:
    feature = x[record]
    residual = float(feature @ theta - y[record])
    return theta + amplitude * (preconditioner @ feature) * residual


def route(
    theta: np.ndarray,
    order: tuple[int, ...],
    x: np.ndarray,
    y: np.ndarray,
    preconditioner: np.ndarray,
    amplitude: float = 1.0,
) -> np.ndarray:
    state = theta.copy()
    for record in order:
        state = affine_delete(
            state, record, x, y, preconditioner, amplitude=amplitude
        )
    return state


def analytic_pair_defect(
    theta: np.ndarray,
    i: int,
    j: int,
    x: np.ndarray,
    y: np.ndarray,
    preconditioner: np.ndarray,
    amplitude: float = 1.0,
) -> np.ndarray:
    xi = x[i]
    xj = x[j]
    ri = float(xi @ theta - y[i])
    rj = float(xj @ theta - y[j])
    alpha = float(xj @ preconditioner @ xi)
    return (
        amplitude**2
        * alpha
        * (preconditioner @ xj * ri - preconditioner @ xi * rj)
    )


def retained_ridge_system(
    hessian: np.ndarray,
    linear: np.ndarray,
    records: tuple[int, ...],
    x: np.ndarray,
    y: np.ndarray,
):
    selected_x = x[list(records)]
    selected_y = y[list(records)]
    retained_hessian = hessian - selected_x.T @ selected_x
    retained_linear = linear - selected_x.T @ selected_y
    return retained_hessian, retained_linear


def solve_retained_target(
    retained_hessian: np.ndarray, retained_linear: np.ndarray
) -> np.ndarray:
    """Validation oracle; never an input to a target-free certificate."""
    return np.linalg.solve(retained_hessian, retained_linear)


def metric_norm(vector: np.ndarray, metric: np.ndarray) -> float:
    squared = float(vector @ metric @ vector)
    return math.sqrt(max(0.0, squared))


def objective_excess(
    theta: np.ndarray, target: np.ndarray, retained_hessian: np.ndarray
) -> float:
    difference = theta - target
    return 0.5 * float(difference @ retained_hessian @ difference)


def minimum_enclosing_ball(points: np.ndarray, tolerance: float = 1e-9):
    """Exhaustive floating-point support enumeration for a small point cloud.

    The minimum enclosing ball of finitely many Euclidean points is supported
    by an affinely independent subset. This routine enumerates all subsets, so
    it is intended only for the six three-request permutation endpoints used
    here.
    """
    count, dimension = points.shape
    best_radius = math.inf
    best_center = None
    best_support = None

    for support_size in range(1, min(count, dimension + 1) + 1):
        for support in itertools.combinations(range(count), support_size):
            selected = points[list(support)]
            base = selected[0]
            if support_size == 1:
                center = base.copy()
                support_radius = 0.0
            else:
                differences = selected[1:] - base
                gram = differences @ differences.T
                if np.linalg.matrix_rank(gram, tol=1e-11) < support_size - 1:
                    continue
                rhs = np.sum(differences * differences, axis=1)
                coefficients = np.linalg.solve(2.0 * gram, rhs)
                center = base + differences.T @ coefficients
                support_radius = float(np.linalg.norm(center - base))

            distances = np.linalg.norm(points - center, axis=1)
            if float(np.max(distances)) <= support_radius + tolerance:
                if support_radius < best_radius:
                    best_radius = support_radius
                    best_center = center
                    best_support = support

    if best_center is None:
        raise RuntimeError("No enclosing-ball support set found")

    distances = np.linalg.norm(points - best_center, axis=1)
    if float(np.max(distances)) > best_radius + 5e-8:
        raise AssertionError("Enclosing-ball verification failed")
    return best_center, best_radius, best_support, distances


def rbf_kernel_sum(
    left: np.ndarray,
    right: np.ndarray,
    bandwidth: float,
    block_size: int = 256,
) -> float:
    total = 0.0
    denominator = 2.0 * bandwidth * bandwidth
    for start in range(0, left.shape[0], block_size):
        block = left[start : start + block_size]
        squared = (
            np.sum(block * block, axis=1)[:, None]
            + np.sum(right * right, axis=1)[None, :]
            - 2.0 * block @ right.T
        )
        np.maximum(squared, 0.0, out=squared)
        total += float(np.exp(-squared / denominator).sum())
    return total


def biased_mmd(
    left: np.ndarray, right: np.ndarray, bandwidth: float
) -> float:
    left_left = rbf_kernel_sum(left, left, bandwidth)
    right_right = rbf_kernel_sum(right, right, bandwidth)
    left_right = rbf_kernel_sum(left, right, bandwidth)
    squared = (
        left_left / (left.shape[0] ** 2)
        + right_right / (right.shape[0] ** 2)
        - 2.0 * left_right / (left.shape[0] * right.shape[0])
    )
    return math.sqrt(max(0.0, squared))


def gaussian_rbf_mmd(
    mean_difference_norm: float,
    dimension: int,
    noise_std: float,
    bandwidth: float,
) -> float:
    common = (1.0 + 2.0 * noise_std**2 / bandwidth**2) ** (
        -dimension / 2.0
    )
    exponent = -(mean_difference_norm**2) / (
        2.0 * (bandwidth**2 + 2.0 * noise_std**2)
    )
    squared = 2.0 * common * (1.0 - math.exp(exponent))
    return math.sqrt(max(0.0, squared))


def affine_basis_check(
    theta: np.ndarray,
    i: int,
    j: int,
    x: np.ndarray,
    y: np.ndarray,
    preconditioner: np.ndarray,
):
    dimension = theta.size
    step = 0.125
    basis = [theta.copy()]
    basis.extend(theta + step * np.eye(dimension)[axis] for axis in range(dimension))

    def direct_defect(state):
        return route(state, (i, j), x, y, preconditioner) - route(
            state, (j, i), x, y, preconditioner
        )

    omega = np.vstack([direct_defect(state) for state in basis])
    basis_matrix = np.column_stack(
        [basis[index] - basis[0] for index in range(1, dimension + 1)]
    )
    output_matrix = np.column_stack(
        [omega[index] - omega[0] for index in range(1, dimension + 1)]
    )
    reconstructed_linear = output_matrix @ np.linalg.inv(basis_matrix)
    reconstructed_constant = omega[0] - reconstructed_linear @ basis[0]

    xi = x[i]
    xj = x[j]
    ai = np.eye(dimension) + np.outer(preconditioner @ xi, xi)
    aj = np.eye(dimension) + np.outer(preconditioner @ xj, xj)
    ci = -(preconditioner @ xi) * y[i]
    cj = -(preconditioner @ xj) * y[j]
    exact_linear = aj @ ai - ai @ aj
    exact_constant = aj @ ci + cj - ai @ cj - ci

    rng = np.random.default_rng(SEED + 17)
    sampled_norms = []
    for _ in range(1000):
        weights = rng.dirichlet(np.ones(dimension + 1))
        state = sum(weight * point for weight, point in zip(weights, basis))
        sampled_norms.append(float(np.linalg.norm(direct_defect(state))))

    return {
        "basis_step": step,
        "linear_reconstruction_error_frobenius": float(
            np.linalg.norm(reconstructed_linear - exact_linear)
        ),
        "constant_reconstruction_error_euclidean_norm": float(
            np.linalg.norm(reconstructed_constant - exact_constant)
        ),
        "maximum_vertex_defect_euclidean_norm": float(
            np.max(np.linalg.norm(omega, axis=1))
        ),
        "maximum_sampled_simplex_defect_euclidean_norm": max(sampled_norms),
        "sampled_simplex_vertex_bound_1000_verified": bool(
            max(sampled_norms)
            <= float(np.max(np.linalg.norm(omega, axis=1))) + 1e-11
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "examples/results/audit_case_study.json",
    )
    arguments = parser.parse_args()

    dataset = load_diabetes()
    x = np.asarray(dataset.data, dtype=float)
    raw_y = np.asarray(dataset.target, dtype=float)
    y = (raw_y - raw_y.mean()) / raw_y.std(ddof=0)
    hessian, linear, theta = ridge_state(x, y, RIDGE_LAMBDA)
    preconditioner = np.linalg.inv(hessian)
    sample_count, dimension = x.shape

    ranked_pairs = []
    maximum_formula_error = 0.0
    for i in range(sample_count):
        for j in range(i + 1, sample_count):
            analytic = analytic_pair_defect(
                theta, i, j, x, y, preconditioner
            )
            direct = route(theta, (i, j), x, y, preconditioner) - route(
                theta, (j, i), x, y, preconditioner
            )
            maximum_formula_error = max(
                maximum_formula_error,
                float(np.linalg.norm(direct - analytic)),
            )
            ranked_pairs.append((float(np.linalg.norm(analytic)), i, j))

    ranked_pairs.sort(reverse=True)
    leading_pairs = []
    for euclidean_defect, i, j in ranked_pairs[:25]:
        z_ij = route(theta, (i, j), x, y, preconditioner)
        z_ji = route(theta, (j, i), x, y, preconditioner)
        direct_defect = z_ij - z_ji
        analytic_defect = analytic_pair_defect(
            theta, i, j, x, y, preconditioner
        )
        formula_error = float(np.linalg.norm(direct_defect - analytic_defect))
        retained_hessian, retained_linear = retained_ridge_system(
            hessian, linear, (i, j), x, y
        )
        metric_defect = metric_norm(direct_defect, retained_hessian)
        half_defect_certificate = metric_defect / 2.0
        order_gap_term = metric_defect**2 / 8.0

        target = solve_retained_target(retained_hessian, retained_linear)
        errors = [
            metric_norm(z_ij - target, retained_hessian),
            metric_norm(z_ji - target, retained_hessian),
        ]
        gaps = [
            objective_excess(z_ij, target, retained_hessian),
            objective_excess(z_ji, target, retained_hessian),
        ]
        midpoint = 0.5 * (z_ij + z_ji)
        midpoint_gap = objective_excess(midpoint, target, retained_hessian)
        mean_gap = 0.5 * (gaps[0] + gaps[1])
        decomposition_error = abs(mean_gap - midpoint_gap - order_gap_term)
        leading_pairs.append(
            {
                "records": [i, j],
                "endpoint_defect_euclidean_norm": euclidean_defect,
                "endpoint_defect_retained_hessian_norm": metric_defect,
                "half_defect_parameter_certificate_retained_hessian_norm": (
                    half_defect_certificate
                ),
                "route_parameter_errors_retained_hessian_norm": errors,
                "worst_route_parameter_error_retained_hessian_norm": max(
                    errors
                ),
                "objective_excesses": gaps,
                "worst_objective_excess": max(gaps),
                "objective_certificate": order_gap_term,
                "mean_objective_excess": mean_gap,
                "midpoint_objective_excess": midpoint_gap,
                "antisymmetric_fraction_of_mean_excess": (
                    order_gap_term / mean_gap if mean_gap > 0.0 else 0.0
                ),
                "decomposition_absolute_error": decomposition_error,
                "formula_absolute_error": formula_error,
            }
        )

    top_norm, top_i, top_j = ranked_pairs[0]
    remaining_candidates = [
        index for index in range(sample_count) if index not in (top_i, top_j)
    ]
    pair_score = {(min(i, j), max(i, j)): value for value, i, j in ranked_pairs}
    third = max(
        remaining_candidates,
        key=lambda index: pair_score[(min(top_i, index), max(top_i, index))]
        + pair_score[(min(top_j, index), max(top_j, index))],
    )
    triple = (top_i, top_j, third)
    orders = list(itertools.permutations(triple))
    endpoints = np.vstack(
        [route(theta, order, x, y, preconditioner) for order in orders]
    )
    triple_hessian, triple_linear = retained_ridge_system(
        hessian, linear, triple, x, y
    )
    cholesky = np.linalg.cholesky(triple_hessian)
    whitened_endpoints = endpoints @ cholesky
    center, radius, support, center_distances = minimum_enclosing_ball(
        whitened_endpoints
    )
    pairwise_distances = np.linalg.norm(
        whitened_endpoints[:, None, :] - whitened_endpoints[None, :, :],
        axis=2,
    )
    diameter = float(np.max(pairwise_distances))
    diameter_support_flat = int(np.argmax(pairwise_distances))
    diameter_left, diameter_right = np.unravel_index(
        diameter_support_flat, pairwise_distances.shape
    )
    diameter_midpoint = 0.5 * (
        whitened_endpoints[diameter_left]
        + whitened_endpoints[diameter_right]
    )
    diameter_midpoint_distances = np.linalg.norm(
        whitened_endpoints - diameter_midpoint, axis=1
    )
    diameter_midpoint_radius = float(np.max(diameter_midpoint_distances))
    diameter_midpoint_encloses_at_half_diameter = bool(
        diameter_midpoint_radius <= diameter / 2.0 + 1e-11
    )

    triple_target = solve_retained_target(triple_hessian, triple_linear)
    whitened_target = triple_target @ cholesky
    target_errors = np.linalg.norm(
        whitened_endpoints - whitened_target, axis=1
    )

    response_order_values = []
    for amplitude in [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]:
        forward = route(
            theta, (top_i, top_j), x, y, preconditioner, amplitude
        )
        reverse = route(
            theta, (top_j, top_i), x, y, preconditioner, amplitude
        )
        endpoint_defect = float(np.linalg.norm(forward - reverse))
        response_order_values.append(
            {
                "amplitude": amplitude,
                "endpoint_defect_euclidean_norm": endpoint_defect,
                "endpoint_defect_euclidean_norm_divided_by_amplitude_squared": (
                    endpoint_defect
                )
                / (amplitude**2),
            }
        )
    log_amplitudes = np.log(
        [item["amplitude"] for item in response_order_values]
    )
    log_defects = np.log(
        [
            item["endpoint_defect_euclidean_norm"]
            for item in response_order_values
        ]
    )
    fitted_order = float(np.polyfit(log_amplitudes, log_defects, 1)[0])

    top_z_ij = route(theta, (top_i, top_j), x, y, preconditioner)
    top_z_ji = route(theta, (top_j, top_i), x, y, preconditioner)
    top_hessian, _ = retained_ridge_system(
        hessian, linear, (top_i, top_j), x, y
    )
    top_cholesky = np.linalg.cholesky(top_hessian)
    mean_ij = top_z_ij @ top_cholesky
    mean_ji = top_z_ji @ top_cholesky
    mean_midpoint = 0.5 * (mean_ij + mean_ji)
    mean_ij = mean_ij - mean_midpoint
    mean_ji = mean_ji - mean_midpoint
    mean_difference_norm = float(np.linalg.norm(mean_ij - mean_ji))
    noise_std = mean_difference_norm / 4.0
    bandwidth = math.sqrt(2.0 * dimension) * noise_std
    rng = np.random.default_rng(SEED)
    samples_ij = mean_ij + rng.normal(
        0.0, noise_std, size=(STOCHASTIC_REPLICATES, dimension)
    )
    samples_ji = mean_ji + rng.normal(
        0.0, noise_std, size=(STOCHASTIC_REPLICATES, dimension)
    )
    empirical_mmd = biased_mmd(samples_ij, samples_ji, bandwidth)
    true_mmd = gaussian_rbf_mmd(
        mean_difference_norm, dimension, noise_std, bandwidth
    )
    per_route_error = math.sqrt(1.0 / STOCHASTIC_REPLICATES) + math.sqrt(
        2.0
        * math.log(2.0 / STOCHASTIC_DELTA)
        / STOCHASTIC_REPLICATES
    )
    pair_lower_bound = max(0.0, empirical_mmd - 2.0 * per_route_error)
    radius_lower_bound = max(
        0.0, empirical_mmd / 2.0 - per_route_error
    )

    affine_check = affine_basis_check(
        theta, top_i, top_j, x, y, preconditioner
    )

    all_checks = {
        "pair_formula_all_97461_pairs": maximum_formula_error < 1e-11,
        "objective_decomposition_top_25_pairs": max(
            item["decomposition_absolute_error"] for item in leading_pairs
        )
        < 1e-11,
        "target_free_parameter_bound_top_25_pairs_retained_hessian_norm": all(
            item["worst_route_parameter_error_retained_hessian_norm"]
            + 1e-12
            >= item[
                "half_defect_parameter_certificate_retained_hessian_norm"
            ]
            for item in leading_pairs
        ),
        "target_free_objective_bound_top_25_pairs": all(
            item["worst_objective_excess"] + 1e-12
            >= item["objective_certificate"]
            for item in leading_pairs
        ),
        "half_diameter_target_bound": float(np.max(target_errors)) + 1e-11
        >= diameter / 2.0,
        "floating_point_meb_consistent_with_half_diameter": (
            abs(radius - diameter / 2.0) < 1e-11
            and diameter_midpoint_encloses_at_half_diameter
        ),
        "response_order_two": abs(fitted_order - 2.0) < 1e-9,
        "affine_basis_reconstruction": affine_check[
            "linear_reconstruction_error_frobenius"
        ]
        < 1e-10
        and affine_check["constant_reconstruction_error_euclidean_norm"]
        < 1e-10,
        "sampled_simplex_vertex_bound_1000": affine_check[
            "sampled_simplex_vertex_bound_1000_verified"
        ],
        "realized_stochastic_lcb_below_closed_form_truth": pair_lower_bound
        <= true_mmd + 1e-12,
        "stochastic_uniform_claim_rejected": pair_lower_bound
        > 2.0 * STOCHASTIC_EPSILON,
        "stochastic_radius_claim_rejected": radius_lower_bound
        > STOCHASTIC_EPSILON,
    }

    results = {
        "metadata": {
            "seed": SEED,
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "scikit_learn": sklearn.__version__,
            "dataset": "sklearn.datasets.load_diabetes",
            "dataset_array_sha256": digest_arrays(x, raw_y),
            "sample_count": sample_count,
            "dimension": dimension,
            "target_transform": "population z-score",
            "ridge_lambda": RIDGE_LAMBDA,
            "study_role": (
                "mathematical non-clinical case study; no predictive or "
                "population-generalization claim"
            ),
            "pair_selection": (
                "exploratory exhaustive deterministic screening before any "
                "stochastic route replicates"
            ),
            "screened_pair_count": len(ranked_pairs),
            "maximum_pair_formula_error_euclidean_norm": (
                maximum_formula_error
            ),
            "reproduction": {
                "working_directory": "project root",
                "command": (
                    "./.venv/bin/python "
                    "examples/run_audit_case_study.py "
                    "--output examples/results/audit_case_study.json"
                ),
                "environment": (
                    "isolated virtual environment installed from "
                    "examples/requirements.txt"
                ),
                "script_sha256": digest_file(Path(__file__).resolve()),
                "requirements_sha256": digest_file(
                    PROJECT_ROOT / "examples/requirements.txt"
                ),
            },
        },
        "top_pair": {
            "records": [top_i, top_j],
            "screening_defect_euclidean_norm": top_norm,
            "details": leading_pairs[0],
        },
        "leading_pair_details": leading_pairs,
        "three_request_audit": {
            "records": list(triple),
            "orders": [list(order) for order in orders],
            "endpoint_count": len(orders),
            "minimum_enclosing_ball_numerical_radius_retained_hessian_metric": (
                radius
            ),
            "diameter_retained_hessian_metric": diameter,
            "target_free_lower_bound_half_diameter": diameter / 2.0,
            "support_order_indices": list(support),
            "support_orders": [list(orders[index]) for index in support],
            "numerical_meb_center_max_distance_retained_hessian_norm": float(
                np.max(center_distances)
            ),
            "diameter_support_order_indices": [
                diameter_left,
                diameter_right,
            ],
            "diameter_support_orders": [
                list(orders[diameter_left]),
                list(orders[diameter_right]),
            ],
            "diameter_midpoint_max_distance_retained_hessian_norm": (
                diameter_midpoint_radius
            ),
            "diameter_midpoint_encloses_at_half_diameter_to_1e-11": (
                diameter_midpoint_encloses_at_half_diameter
            ),
            "worst_route_exact_target_error_retained_hessian_norm": float(
                np.max(target_errors)
            ),
            "best_route_exact_target_error_retained_hessian_norm": float(
                np.min(target_errors)
            ),
            "radius_fraction_of_worst_target_error": radius
            / float(np.max(target_errors)),
        },
        "response_order": {
            "top_pair": [top_i, top_j],
            "values": response_order_values,
            "fitted_log_log_slope": fitted_order,
        },
        "affine_basis_check": affine_check,
        "stochastic_mmd_audit": {
            "routes": [[top_i, top_j], [top_j, top_i]],
            "replicates_per_route": STOCHASTIC_REPLICATES,
            "family_wise_delta": STOCHASTIC_DELTA,
            "route_count": 2,
            "kernel": "Gaussian RBF",
            "kernel_diagonal_bound": 1.0,
            "noise_model": "isotropic Gaussian in retained-Hessian coordinates",
            "randomness_semantics": (
                "conditional on one fixed fitted checkpoint; each complete "
                "route receives fresh independent synthetic output noise"
            ),
            "failure_semantics": (
                "all routes are total in this simulation; no failure event"
            ),
            "selection_semantics": (
                "deliberately powered synthetic illustration: the noise "
                "scale and bandwidth were effect-calibrated from the "
                "deterministic witness, then fixed with the route pair and "
                "tolerance before random-number generation"
            ),
            "noise_std": noise_std,
            "bandwidth": bandwidth,
            "declared_uniform_mmd_tolerance": STOCHASTIC_EPSILON,
            "true_route_mmd_closed_form": true_mmd,
            "empirical_biased_mmd": empirical_mmd,
            "per_route_mean_embedding_error_bound": per_route_error,
            "simultaneous_pair_mmd_lower_bound": pair_lower_bound,
            "simultaneous_radius_lower_bound": radius_lower_bound,
            "pair_rejection_threshold": 2.0 * STOCHASTIC_EPSILON,
            "radius_rejection_threshold": STOCHASTIC_EPSILON,
        },
        "checks": all_checks,
        "all_checks_passed": all(all_checks.values()),
    }

    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(to_builtin(results), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(to_builtin(results["checks"]), indent=2, sort_keys=True))
    print(f"all_checks_passed={results['all_checks_passed']}")
    print(f"output={arguments.output.resolve()}")
    return 0 if results["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Numerical dimension-compression homotopy from S^5 to S^4.

Exact normalized D6-root subsets and independently relaxed random
six-dimensional codes begin with maximum inner product at most 1/2.  A
covariance-eigenvalue homotopy then drives the sixth frame eigenvalue to
zero while a smooth approximation to the maximum pair product is relaxed
on the product of spheres.  Branch perturbations change the candidate
collapse eigendirection.  The final rank-five cloud is projected and
polished in R^5.

This is numerical discovery code, not a construction certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import statistics
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


def unit_rows(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array, dtype=float)
    if array.ndim != 2:
        raise ValueError("coordinates must be a matrix")
    norms = np.linalg.norm(array, axis=1)
    if float(np.min(norms)) <= 1e-13:
        raise ValueError("cannot normalize a zero row")
    return array / norms[:, None]


def pair_indices(n: int):
    return np.triu_indices(n, 1)


def pair_values(array: np.ndarray) -> np.ndarray:
    x = unit_rows(array)
    ii, jj = pair_indices(len(x))
    return np.sum(x[ii] * x[jj], axis=1)


def max_inner(array: np.ndarray) -> float:
    return float(np.max(pair_values(array)))


def covariance_spectrum(array: np.ndarray) -> np.ndarray:
    x = unit_rows(array)
    return np.linalg.eigvalsh(x.T @ x)


def d6_roots() -> tuple[np.ndarray, list[list[int]]]:
    rows = []
    labels = []
    for first in range(6):
        for second in range(first + 1, 6):
            for sign_first in (-1, 1):
                for sign_second in (-1, 1):
                    row = np.zeros(6)
                    row[first] = sign_first / math.sqrt(2.0)
                    row[second] = sign_second / math.sqrt(2.0)
                    rows.append(row)
                    labels.append([first, second, sign_first, sign_second])
    answer = np.asarray(rows)
    if answer.shape != (60, 6):
        raise AssertionError("D6 enumeration failed")
    return answer, labels


def exact_pair_numerator(first: list[int], second: list[int]) -> int:
    row = [0] * 6
    other = [0] * 6
    row[first[0]] = first[2]
    row[first[1]] = first[3]
    other[second[0]] = second[2]
    other[second[1]] = second[3]
    return sum(x * y for x, y in zip(row, other))


def subset_initializations(
    n: int, rng: np.random.Generator
) -> list[tuple[str, np.ndarray, list[list[int]] | None]]:
    roots, labels = d6_roots()
    answer = []

    uniform_indices = rng.choice(60, size=n, replace=False)
    answer.append(
        (
            "exact_D6_uniform_asymmetric_subset",
            roots[uniform_indices],
            [labels[int(index)] for index in uniform_indices],
        )
    )

    # Select antipodal pairs using the canonical first sign -1.
    pairs = []
    for index, label in enumerate(labels):
        antipode_label = [label[0], label[1], -label[2], -label[3]]
        antipode = labels.index(antipode_label)
        if index < antipode:
            pairs.append((index, antipode))
    pair_order = rng.permutation(len(pairs))
    chosen = []
    for pair_index in pair_order[: n // 2]:
        chosen.extend(pairs[int(pair_index)])
    if n % 2:
        used = set(chosen)
        extra = next(index for index in rng.permutation(60) if index not in used)
        chosen.append(int(extra))
    answer.append(
        (
            "exact_D6_antipodal_pair_subset",
            roots[chosen],
            [labels[index] for index in chosen],
        )
    )

    normal = rng.normal(size=6)
    normal /= np.linalg.norm(normal)
    jitter = rng.normal(scale=1e-5, size=60)
    slice_indices = np.argsort(roots @ normal + jitter)[-n:]
    answer.append(
        (
            "exact_D6_random_height_slice",
            roots[slice_indices],
            [labels[int(index)] for index in slice_indices],
        )
    )

    # Search many exact subsets but score them only by a floating covariance
    # diversity diagnostic.  The selected coordinates remain exact D6 roots.
    best_indices = None
    best_score = -math.inf
    for _ in range(180):
        indices = rng.choice(60, size=n, replace=False)
        spectrum = np.linalg.eigvalsh(roots[indices].T @ roots[indices])
        score = float(spectrum[0] - 0.05 * np.var(spectrum))
        if score > best_score:
            best_score = score
            best_indices = indices
    answer.append(
        (
            "exact_D6_covariance_diverse_subset",
            roots[best_indices],
            [labels[int(index)] for index in best_indices],
        )
    )
    return answer


def logsum_pair_value_gradient(
    raw: np.ndarray, n: int, dimension: int, beta: float
):
    points = np.asarray(raw, dtype=float).reshape(n, dimension)
    norms = np.linalg.norm(points, axis=1)
    if float(np.min(norms)) <= 1e-13:
        return 1e30, np.zeros_like(raw)
    x = points / norms[:, None]
    ii, jj = pair_indices(n)
    values = np.sum(x[ii] * x[jj], axis=1)
    top = float(np.max(values))
    exponentials = np.exp(beta * (values - top))
    weights = exponentials / float(np.sum(exponentials))
    value = top + math.log(float(np.sum(exponentials))) / beta
    ambient = np.zeros_like(x)
    np.add.at(ambient, ii, weights[:, None] * x[jj])
    np.add.at(ambient, jj, weights[:, None] * x[ii])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    return float(value), (tangent / norms[:, None]).ravel()


def collapse_value_gradient(
    raw: np.ndarray,
    n: int,
    dimension: int,
    beta: float,
    collapse_weight: float,
):
    smooth, gradient = logsum_pair_value_gradient(
        raw, n, dimension, beta
    )
    points = np.asarray(raw, dtype=float).reshape(n, dimension)
    norms = np.linalg.norm(points, axis=1)
    x = points / norms[:, None]
    eigenvalues, eigenvectors = np.linalg.eigh(x.T @ x)
    direction = eigenvectors[:, 0]
    minimum = float(eigenvalues[0])
    ambient = (2.0 * collapse_weight / n) * (
        (x @ direction)[:, None] * direction[None, :]
    )
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    gradient = gradient.reshape(n, dimension) + tangent / norms[:, None]
    return (
        float(smooth + collapse_weight * minimum / n),
        gradient.ravel(),
    )


def relax_smooth(
    x: np.ndarray, betas: tuple[float, ...], iterations: int
) -> tuple[np.ndarray, list[dict]]:
    x = unit_rows(x)
    history = []
    for beta in betas:
        result = minimize(
            logsum_pair_value_gradient,
            x.ravel(),
            args=(len(x), x.shape[1], beta),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": int(iterations),
                "ftol": 2e-15,
                "gtol": 3e-9,
                "maxls": 60,
                "maxcor": 35,
            },
        )
        x = unit_rows(result.x.reshape(x.shape))
        history.append(
            {
                "beta": float(beta),
                "iterations": int(result.nit),
                "success": bool(result.success),
                "message": str(result.message),
                "smooth_value": float(result.fun),
                "maximum": max_inner(x),
                "covariance_eigenvalues": covariance_spectrum(x).tolist(),
            }
        )
    return x, history


def epigraph_refine(x: np.ndarray, iterations: int) -> tuple[np.ndarray, dict]:
    """Direct nonsmooth minimax polish after dimension compression."""
    x = unit_rows(x)
    n, dimension = x.shape
    ii, jj = pair_indices(n)
    initial = np.r_[x.ravel(), max_inner(x)]

    def objective(variable):
        return float(variable[-1])

    def objective_jac(variable):
        answer = np.zeros_like(variable)
        answer[-1] = 1.0
        return answer

    def inequalities(variable):
        points = variable[:-1].reshape(n, dimension)
        return variable[-1] - np.sum(points[ii] * points[jj], axis=1)

    def inequalities_jac(variable):
        points = variable[:-1].reshape(n, dimension)
        answer = np.zeros((len(ii), len(variable)))
        rows = np.arange(len(ii))
        for coordinate in range(dimension):
            answer[rows, dimension * ii + coordinate] = -points[jj, coordinate]
            answer[rows, dimension * jj + coordinate] = -points[ii, coordinate]
        answer[:, -1] = 1.0
        return answer

    def equalities(variable):
        points = variable[:-1].reshape(n, dimension)
        return np.sum(points * points, axis=1) - 1.0

    def equalities_jac(variable):
        points = variable[:-1].reshape(n, dimension)
        answer = np.zeros((n, len(variable)))
        rows = np.arange(n)
        for coordinate in range(dimension):
            answer[rows, dimension * rows + coordinate] = (
                2.0 * points[:, coordinate]
            )
        return answer

    result = minimize(
        objective,
        initial,
        jac=objective_jac,
        constraints=[
            {"type": "ineq", "fun": inequalities, "jac": inequalities_jac},
            {"type": "eq", "fun": equalities, "jac": equalities_jac},
        ],
        method="SLSQP",
        options={
            "maxiter": int(iterations),
            "ftol": 2e-13,
            "disp": False,
        },
    )
    answer = unit_rows(result.x[:-1].reshape(n, dimension))
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": max_inner(answer),
    }


def random_feasible_six_code(
    n: int, rng: np.random.Generator, iterations: int
) -> tuple[np.ndarray, list[dict]]:
    starts = []
    for attempt in range(4):
        initial = unit_rows(rng.normal(size=(n, 6)))
        candidate, history = relax_smooth(
            initial, (12.0, 36.0, 108.0, 324.0, 972.0, 2916.0), iterations
        )
        starts.append((max_inner(candidate), candidate, history, attempt))
        if starts[-1][0] < 0.495:
            break
    value, x, history, attempt = min(starts, key=lambda item: item[0])
    if value > 0.5:
        # A strict feasible random start is required by this experiment.
        # Perturbing an exact D6 subset provides a fallback basin but every
        # coordinate is then fully released before compression.
        roots, _ = d6_roots()
        indices = rng.choice(60, size=n, replace=False)
        initial = unit_rows(
            roots[indices] + 0.08 * rng.normal(size=(n, 6))
        )
        x, history = relax_smooth(
            initial, (24.0, 72.0, 216.0, 648.0, 1944.0, 5832.0), iterations
        )
        attempt = 4
    if max_inner(x) > 0.5:
        raise RuntimeError(f"failed to make random feasible S5 code for N={n}")
    return x, [{"attempt_selected": attempt}] + history


def branch_perturb(
    x: np.ndarray,
    rng: np.random.Generator,
    scale: float,
) -> np.ndarray:
    x = unit_rows(x)
    _, eigenvectors = np.linalg.eigh(x.T @ x)
    angle = float(rng.uniform(-0.75, 0.75))
    direction = (
        math.cos(angle) * eigenvectors[:, 0]
        + math.sin(angle) * eigenvectors[:, 1]
    )
    compression = -(x @ direction)[:, None] * direction[None, :]
    noise = rng.normal(size=x.shape)
    noise -= np.sum(noise * x, axis=1)[:, None] * x
    tangent = compression + 0.18 * noise
    tangent -= np.sum(tangent * x, axis=1)[:, None] * x
    return unit_rows(x + scale * tangent)


def relax_collapse_stage(
    x: np.ndarray,
    beta: float,
    weight: float,
    iterations: int,
) -> tuple[np.ndarray, dict]:
    x = unit_rows(x)
    result = minimize(
        collapse_value_gradient,
        x.ravel(),
        args=(len(x), 6, beta, weight),
        jac=True,
        method="L-BFGS-B",
        options={
            "maxiter": int(iterations),
            "ftol": 2e-15,
            "gtol": 3e-9,
            "maxls": 70,
            "maxcor": 40,
        },
    )
    x = unit_rows(result.x.reshape(len(x), 6))
    objective = collapse_value_gradient(
        x.ravel(), len(x), 6, beta, weight
    )[0]
    return x, {
        "success": bool(result.success),
        "message": str(result.message),
        "iterations": int(result.nit),
        "evaluations": int(result.nfev),
        "objective": float(objective),
        "maximum": max_inner(x),
        "covariance_eigenvalues": covariance_spectrum(x).tolist(),
    }


def stage_record(
    index: int,
    weight: float,
    beta: float,
    selected: str,
    x: np.ndarray,
    direct: dict,
    branch: dict | None,
) -> dict:
    spectrum = covariance_spectrum(x)
    return {
        "stage": index,
        "collapse_weight": float(weight),
        "beta": float(beta),
        "selected": selected,
        "direct_candidate": direct,
        "branch_candidate": branch,
        "maximum": max_inner(x),
        "gap_above_one_half": max_inner(x) - 0.5,
        "covariance_eigenvalues": spectrum.tolist(),
        # Tiny negative values can arise only from the floating symmetric
        # eigensolver; covariance is mathematically PSD.
        "sixth_fraction": float(max(0.0, spectrum[0]) / len(x)),
        "coordinates_float64": x.tolist(),
    }


def collapse_homotopy(
    initial: np.ndarray,
    rng: np.random.Generator,
    iterations: int,
) -> tuple[np.ndarray, list[dict]]:
    x = unit_rows(initial)
    weights = (0.0, 0.01, 0.03, 0.10, 0.30, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0)
    betas = (36.0, 54.0, 81.0, 122.0, 183.0, 275.0, 412.0, 618.0, 927.0, 1390.0, 2085.0)
    history = []
    for index, (weight, beta) in enumerate(zip(weights, betas)):
        direct_x, direct = relax_collapse_stage(
            x, beta, weight, iterations
        )
        branch = None
        selected = "direct"
        chosen = direct_x
        if index in (2, 4, 6, 8, 10):
            perturbed = branch_perturb(
                x, rng, (0.018, 0.030, 0.045, 0.060, 0.080)[index // 2 - 1]
            )
            branch_x, branch = relax_collapse_stage(
                perturbed, beta, weight, iterations
            )
            if branch["objective"] < direct["objective"]:
                chosen = branch_x
                selected = "branch"
        x = chosen
        history.append(
            stage_record(
                index, weight, beta, selected, x, direct, branch
            )
        )
    return x, history


def project_to_five(x: np.ndarray) -> tuple[np.ndarray, dict]:
    x = unit_rows(x)
    eigenvalues, eigenvectors = np.linalg.eigh(x.T @ x)
    discarded = eigenvectors[:, 0]
    projected = x @ eigenvectors[:, 1:]
    pre_norms = np.linalg.norm(projected, axis=1)
    answer = unit_rows(projected)
    return answer, {
        "discarded_direction": discarded.tolist(),
        "six_dimensional_covariance_eigenvalues": eigenvalues.tolist(),
        "minimum_projected_row_norm": float(np.min(pre_norms)),
        "maximum_projected_row_norm": float(np.max(pre_norms)),
        "maximum_before_projection": max_inner(x),
        "maximum_immediately_after_projection": max_inner(answer),
    }


def active_summary(x: np.ndarray, tolerance: float) -> dict:
    values = pair_values(x)
    top = float(np.max(values))
    ii, jj = pair_indices(len(x))
    chosen = values >= top - tolerance
    edges = np.column_stack([ii[chosen], jj[chosen]])
    degree = np.bincount(edges.ravel(), minlength=len(x))
    unique, counts = np.unique(degree, return_counts=True)
    return {
        "tolerance": tolerance,
        "edge_count": int(len(edges)),
        "degree_histogram": {
            str(int(key)): int(value)
            for key, value in zip(unique, counts)
        },
        "edges": edges.tolist(),
    }


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    values = pair_values(x)
    answer = {
        "dimension": x.shape[1],
        "n": len(x),
        "maximum": float(np.max(values)),
        "gap_above_one_half": float(np.max(values) - 0.5),
        "minimum": float(np.min(values)),
        "row_norm_max_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "covariance_eigenvalues": covariance_spectrum(x).tolist(),
        "gram_eigenvalues": np.linalg.eigvalsh(x @ x.T).tolist(),
        "coordinates_float64": x.tolist(),
    }
    for tolerance in (1e-4, 1e-6, 1e-8):
        answer[f"active_{tolerance:.0e}"] = active_summary(x, tolerance)
    return answer


def compression_barrier(history: list[dict], final: dict) -> dict:
    thresholds = (0.1, 0.03, 0.01, 0.003, 0.001, 1e-4, 1e-6, 1e-8)
    envelope = {}
    for threshold in thresholds:
        eligible = [
            record
            for record in history
            if record["sixth_fraction"] <= threshold
        ]
        envelope[f"{threshold:.0e}"] = (
            min(record["maximum"] for record in eligible)
            if eligible
            else None
        )
    crossing = next(
        (
            {
                "stage": record["stage"],
                "collapse_weight": record["collapse_weight"],
                "sixth_fraction": record["sixth_fraction"],
                "maximum": record["maximum"],
            }
            for record in history
            if record["maximum"] > 0.5 + 1e-10
        ),
        None,
    )
    return {
        "first_positive_threshold_crossing": crossing,
        "maximum_envelope_by_sixth_fraction": envelope,
        "final_five_dimensional_maximum": final["maximum"],
        "final_gap_above_one_half": final["gap_above_one_half"],
    }


def run_path(
    n: int,
    seed: int,
    origin: str,
    initial: np.ndarray,
    exact_labels: list[list[int]] | None,
    initial_relaxation: list[dict] | None,
    iterations: int,
) -> dict:
    rng = np.random.default_rng(seed)
    started = time.time()
    initial = unit_rows(initial)
    collapsed, history = collapse_homotopy(initial, rng, iterations)
    projected, projection = project_to_five(collapsed)
    final, polish = relax_smooth(
        projected, (240.0, 960.0, 3840.0, 15360.0), 2 * iterations
    )
    epigraph_candidate, epigraph = epigraph_refine(
        final, max(900, 6 * iterations)
    )
    epigraph["accepted_by_recomputed_maximum"] = (
        max_inner(epigraph_candidate) <= max_inner(final)
    )
    if epigraph["accepted_by_recomputed_maximum"]:
        final = epigraph_candidate
    final_diagnostics = diagnostics(final)
    return {
        "n": n,
        "seed": int(seed),
        "origin": origin,
        "initial": diagnostics(initial),
        "exact_d6_root_labels": exact_labels,
        "random_initial_relaxation": initial_relaxation,
        "homotopy_history": history,
        "collapsed_six_dimensional": diagnostics(collapsed),
        "projection": projection,
        "five_dimensional_polish": polish,
        "five_dimensional_epigraph": epigraph,
        "final_five_dimensional": final_diagnostics,
        "barrier": compression_barrier(history, final_diagnostics),
        "elapsed_seconds": time.time() - started,
    }


def summarize_barriers(runs: list[dict]) -> dict:
    answer = {}
    for n in sorted({run["n"] for run in runs}):
        current = [run for run in runs if run["n"] == n]
        gaps = [
            run["final_five_dimensional"]["gap_above_one_half"]
            for run in current
        ]
        crossing_maxima = [
            run["barrier"]["first_positive_threshold_crossing"]["maximum"]
            for run in current
            if run["barrier"]["first_positive_threshold_crossing"] is not None
        ]
        answer[str(n)] = {
            "path_count": len(current),
            "best_final_maximum": min(
                run["final_five_dimensional"]["maximum"] for run in current
            ),
            "minimum_final_gap": min(gaps),
            "median_final_gap": statistics.median(gaps),
            "all_paths_crossed_above_half": len(crossing_maxima) == len(current),
            "minimum_first_crossing_maximum": (
                min(crossing_maxima) if crossing_maxima else None
            ),
        }
    return answer


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, default=[41, 42, 43, 44])
    parser.add_argument("--seed", type=int, default=2026072370)
    parser.add_argument("--iterations", type=int, default=170)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    started = time.time()
    runs = []
    master = np.random.default_rng(arguments.seed)
    for n in arguments.n:
        initial_rng = np.random.default_rng(int(master.integers(2**31)))
        initializations = subset_initializations(n, initial_rng)
        random_code, random_history = random_feasible_six_code(
            n, initial_rng, arguments.iterations
        )
        initializations.append(
            ("random_relaxed_feasible_S5_code", random_code, None)
        )
        for origin, initial, labels in initializations:
            path_seed = int(master.integers(2**31))
            print(
                f"N={n} seed={path_seed} origin={origin} "
                f"initial_max={max_inner(initial):.12f}",
                flush=True,
            )
            run = run_path(
                n,
                path_seed,
                origin,
                initial,
                labels,
                random_history if labels is None else None,
                arguments.iterations,
            )
            print(
                "  sixth_fraction="
                f"{run['homotopy_history'][-1]['sixth_fraction']:.3e} "
                "final_max="
                f"{run['final_five_dimensional']['maximum']:.12f}",
                flush=True,
            )
            runs.append(run)
    payload = {
        "status": STATUS,
        "method": (
            "D6/random feasible S5 starts; covariance-smallest-eigenvalue "
            "homotopy with manifold relaxation and branch perturbations; "
            "rank-five projection and independent five-dimensional polish"
        ),
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "parameters": {
            "n": arguments.n,
            "seed": arguments.seed,
            "iterations": arguments.iterations,
        },
        "runs": runs,
        "barrier_summary": summarize_barriers(runs),
        "elapsed_seconds": time.time() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

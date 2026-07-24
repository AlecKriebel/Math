#!/usr/bin/env python3
"""Deterministic active-rigidity escapes for 41--44 points on S^4.

This is numerical discovery code, not a proof or feasibility certificate.

The macro move differs from smooth-max continuation.  It constructs the
linearized contact framework at a stored endpoint, quotients out ambient
rotations, and perturbs along either:

* a genuine or nearly singular non-rotational contact-framework mode; or
* for N=41, a flex exposed by deleting exactly enough active rows from the
  rigid 35-point core to make the retained framework underdetermined.

Each escaped point cloud is polished with a direct epigraph formulation of
the minimax problem.  All pair inequalities and all unit-norm equalities are
present in the SLSQP problem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DIMENSION = 5
ACTIVE_TOLERANCE = 1e-8


def unit_rows(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array, dtype=np.float64)
    norms = np.linalg.norm(array, axis=1)
    if array.ndim != 2 or array.shape[1] != DIMENSION:
        raise ValueError("coordinates must be an N by 5 matrix")
    if float(np.min(norms)) < 1e-14:
        raise ValueError("cannot normalize a zero row")
    return np.ascontiguousarray(array / norms[:, None])


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def maximum_inner_product(array: np.ndarray) -> float:
    x = unit_rows(array)
    ii, jj = pair_indices(len(x))
    return float(np.max(np.sum(x[ii] * x[jj], axis=1)))


def coordinate_hash(array: np.ndarray) -> str:
    x = np.ascontiguousarray(np.asarray(array, dtype="<f8"))
    return hashlib.sha256(x.tobytes(order="C")).hexdigest()


def epigraph_refine(
    initial_points: np.ndarray, max_iterations: int
) -> tuple[np.ndarray, dict]:
    """Direct constrained minimax polishing with analytic Jacobians."""
    x = unit_rows(initial_points)
    n = len(x)
    ii, jj = pair_indices(n)
    initial = np.r_[x.ravel(), maximum_inner_product(x)]

    def objective(variable: np.ndarray) -> float:
        return float(variable[-1])

    def objective_jac(variable: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(variable)
        answer[-1] = 1.0
        return answer

    def inequalities(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(n, DIMENSION)
        return variable[-1] - np.sum(points[ii] * points[jj], axis=1)

    def inequalities_jac(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(n, DIMENSION)
        answer = np.zeros((len(ii), len(variable)))
        rows = np.arange(len(ii))
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * ii + coordinate] = -points[jj, coordinate]
            answer[rows, DIMENSION * jj + coordinate] = -points[ii, coordinate]
        answer[:, -1] = 1.0
        return answer

    def equalities(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(n, DIMENSION)
        return np.sum(points * points, axis=1) - 1.0

    def equalities_jac(variable: np.ndarray) -> np.ndarray:
        points = variable[:-1].reshape(n, DIMENSION)
        answer = np.zeros((n, len(variable)))
        rows = np.arange(n)
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * rows + coordinate] = (
                2.0 * points[:, coordinate]
            )
        return answer

    result = minimize(
        objective,
        initial,
        jac=objective_jac,
        constraints=[
            {
                "type": "ineq",
                "fun": inequalities,
                "jac": inequalities_jac,
            },
            {
                "type": "eq",
                "fun": equalities,
                "jac": equalities_jac,
            },
        ],
        method="SLSQP",
        options={
            "maxiter": max_iterations,
            "ftol": 2e-13,
            "disp": False,
        },
    )
    answer = unit_rows(result.x[:-1].reshape(n, DIMENSION))
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": maximum_inner_product(answer),
    }


def stored_endpoints(repository: Path) -> dict[int, tuple[np.ndarray, str]]:
    answer: dict[int, tuple[np.ndarray, str]] = {}

    input_41 = repository / "experiments/input/spherical_codes_5_41.txt"
    answer[41] = (
        unit_rows(np.loadtxt(input_41, delimiter=",")),
        str(input_41.relative_to(repository)),
    )

    round_9_path = (
        repository
        / "experiments/construction_round9_core_rattler/results/"
        "core_rattler_portfolio.json"
    )
    round_9 = json.loads(round_9_path.read_text())
    for n, run_index in ((42, 1), (43, 2)):
        answer[n] = (
            unit_rows(
                np.asarray(
                    round_9["runs"][run_index]["best"][
                        "coordinates_float64"
                    ]
                )
            ),
            f"{round_9_path.relative_to(repository)}#/runs/{run_index}/best",
        )

    round_6_path = (
        repository
        / "experiments/construction_round6_bundle/results/"
        "bundle_portfolio.json"
    )
    round_6 = json.loads(round_6_path.read_text())
    answer[44] = (
        unit_rows(
            np.asarray(
                round_6["runs"][19]["best"]["coordinates_float64"]
            )
        ),
        f"{round_6_path.relative_to(repository)}#/runs/19/best",
    )
    return answer


def active_edges(x: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    gram = x @ x.T
    np.fill_diagonal(gram, -np.inf)
    maximum = float(np.max(gram))
    edges = np.argwhere(
        np.triu(gram >= maximum - ACTIVE_TOLERANCE, k=1)
    )
    degrees = np.bincount(edges.ravel(), minlength=len(x))
    return maximum, edges, degrees


def rotation_rows(x: np.ndarray) -> np.ndarray:
    rotations = []
    for first in range(DIMENSION):
        for second in range(first + 1, DIMENSION):
            velocity = np.zeros_like(x)
            velocity[:, first] = -x[:, second]
            velocity[:, second] = x[:, first]
            rotations.append(velocity.ravel())
    return np.asarray(rotations)


def constrained_rigidity_matrix(
    x: np.ndarray, edges: np.ndarray
) -> np.ndarray:
    n = len(x)
    rotations = rotation_rows(x)
    answer = np.zeros(
        (len(edges) + n + len(rotations), n * DIMENSION)
    )
    for row, (first, second) in enumerate(edges):
        answer[
            row,
            DIMENSION * first : DIMENSION * (first + 1),
        ] = x[second]
        answer[
            row,
            DIMENSION * second : DIMENSION * (second + 1),
        ] = x[first]
    for point in range(n):
        answer[
            len(edges) + point,
            DIMENSION * point : DIMENSION * (point + 1),
        ] = x[point]
    answer[len(edges) + n :] = rotations
    return answer


def normalized_mode(matrix: np.ndarray, tail_index: int) -> tuple[np.ndarray, dict]:
    _, singular_values, right = np.linalg.svd(matrix, full_matrices=True)
    if tail_index < 1 or tail_index > len(right):
        raise ValueError("invalid tail mode index")
    vector = right[-tail_index].copy()
    vector /= float(
        np.max(np.linalg.norm(vector.reshape(-1, DIMENSION), axis=1))
    )
    rank = int(np.linalg.matrix_rank(matrix))
    return vector.reshape(-1, DIMENSION), {
        "matrix_shape": list(matrix.shape),
        "matrix_rank_binary64": rank,
        "nullity_binary64": int(matrix.shape[1] - rank),
        "tail_index": int(tail_index),
        "selected_residual_2norm": float(np.linalg.norm(matrix @ vector)),
        "smallest_singular_values": [
            float(value) for value in singular_values[-12:]
        ],
    }


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    gram = x @ x.T
    ii, jj = pair_indices(len(x))
    pair_values = gram[ii, jj]
    maximum_index = int(np.argmax(pair_values))
    maximum = float(pair_values[maximum_index])
    frame_spectrum = np.linalg.eigvalsh(x.T @ x)
    gram_spectrum = np.linalg.eigvalsh(gram)
    answer = {
        "n": int(len(x)),
        "maximum_inner_product": maximum,
        "maximizing_pair": [
            int(ii[maximum_index]),
            int(jj[maximum_index]),
        ],
        "maximum_row_norm_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "coordinate_little_endian_float64_sha256": coordinate_hash(x),
        "frame_spectrum": [float(value) for value in frame_spectrum],
        "gram_smallest_eigenvalue": float(gram_spectrum[0]),
        "gram_sixth_largest_eigenvalue": float(gram_spectrum[-6]),
    }
    for tolerance in (1e-8, 1e-6, 1e-4):
        edges = np.argwhere(
            np.triu(gram >= maximum - tolerance, k=1)
        )
        degrees = np.bincount(edges.ravel(), minlength=len(x))
        answer[f"active_{tolerance:.0e}"] = {
            "edge_count": int(len(edges)),
            "minimum_degree": int(np.min(degrees)),
            "maximum_degree": int(np.max(degrees)),
            "zero_degree_count": int(np.sum(degrees == 0)),
        }
    return answer


def candidate_record(
    label: str,
    origin: str,
    initial: np.ndarray,
    refined: np.ndarray,
    solver: dict,
    mode: dict,
    sign: int,
    scale: float,
) -> dict:
    return {
        "label": label,
        "origin": origin,
        "sign": int(sign),
        "scale": float(scale),
        "escaped_maximum": maximum_inner_product(initial),
        "solver": solver,
        "mode": mode,
        "diagnostics": diagnostics(refined),
        "coordinates_float64": unit_rows(refined).tolist(),
    }


def run_soft_modes(
    n: int,
    x: np.ndarray,
    origin: str,
    tail_indices: tuple[int, ...],
    scales: tuple[float, ...],
    max_iterations: int,
) -> tuple[list[dict], np.ndarray]:
    _, edges, _ = active_edges(x)
    matrix = constrained_rigidity_matrix(x, edges)
    records = []
    best = x.copy()
    best_value = maximum_inner_product(best)
    for tail_index in tail_indices:
        mode, mode_record = normalized_mode(matrix, tail_index)
        for sign in (-1, 1):
            for scale in scales:
                escaped = unit_rows(x + sign * scale * mode)
                refined, solver = epigraph_refine(
                    escaped, max_iterations=max_iterations
                )
                record = candidate_record(
                    f"N{n}_tail{tail_index}_sign{sign}_scale{scale:g}",
                    origin,
                    escaped,
                    refined,
                    solver,
                    mode_record,
                    sign,
                    scale,
                )
                records.append(record)
                value = record["diagnostics"]["maximum_inner_product"]
                print(
                    f"N={n} tail={tail_index} sign={sign:+d} "
                    f"scale={scale:g} max={value:.17g}",
                    flush=True,
                )
                if value < best_value:
                    best = refined.copy()
                    best_value = value
    return records, best


def run_41_edge_release(
    x: np.ndarray,
    origin: str,
    seeds: tuple[int, ...],
    scales: tuple[float, ...],
    max_iterations: int,
) -> tuple[list[dict], np.ndarray, dict]:
    _, all_edges, degrees = active_edges(x)
    core_indices = np.flatnonzero(degrees > 0)
    core = x[core_indices]
    if len(core) != 35:
        raise AssertionError("expected the stored N=41 active core to have 35 rows")
    _, core_edges, _ = active_edges(core)
    full_matrix = constrained_rigidity_matrix(core, core_edges)
    full_rank = int(np.linalg.matrix_rank(full_matrix))
    full_nullity = int(full_matrix.shape[1] - full_rank)
    # The core has 4*35 tangent degrees of freedom and 10 rotations.  Keeping
    # at most 129 contact rows forces at least one new non-rotational flex.
    deletion_count = len(core_edges) - 129
    records = []
    best = x.copy()
    best_value = maximum_inner_product(best)
    for seed in seeds:
        rng = np.random.default_rng(seed)
        deleted = np.sort(
            rng.choice(len(core_edges), deletion_count, replace=False)
        )
        retained = np.delete(core_edges, deleted, axis=0)
        matrix = constrained_rigidity_matrix(core, retained)
        mode, mode_record = normalized_mode(matrix, 1)
        mode_record.update(
            {
                "seed": int(seed),
                "deleted_edge_count": int(deletion_count),
                "deleted_edges": [
                    [int(first), int(second)]
                    for first, second in core_edges[deleted]
                ],
                "retained_edge_count": int(len(retained)),
            }
        )
        for sign in (-1, 1):
            for scale in scales:
                escaped = x.copy()
                escaped[core_indices] = unit_rows(
                    core + sign * scale * mode
                )
                refined, solver = epigraph_refine(
                    escaped, max_iterations=max_iterations
                )
                record = candidate_record(
                    f"N41_seed{seed}_sign{sign}_scale{scale:g}",
                    origin,
                    escaped,
                    refined,
                    solver,
                    mode_record,
                    sign,
                    scale,
                )
                records.append(record)
                value = record["diagnostics"]["maximum_inner_product"]
                print(
                    f"N=41 seed={seed} sign={sign:+d} scale={scale:g} "
                    f"max={value:.17g}",
                    flush=True,
                )
                if value < best_value:
                    best = refined.copy()
                    best_value = value
    structure = {
        "active_vertex_count": int(len(core_indices)),
        "inactive_vertex_count": int(len(x) - len(core_indices)),
        "active_core_indices": [int(value) for value in core_indices],
        "active_core_edge_count": int(len(core_edges)),
        "active_core_constrained_rigidity_rank_binary64": full_rank,
        "active_core_constrained_rigidity_nullity_binary64": full_nullity,
        "rotation_dimension": 10,
        "edge_deletion_count_per_trial": int(deletion_count),
    }
    return records, best, structure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("rigidity_softmode_results.json"),
    )
    parser.add_argument("--max-iterations", type=int, default=3000)
    parser.add_argument(
        "--n41-trials",
        type=int,
        default=8,
        help="number of deterministic 24-edge-release trials",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    repository = Path(__file__).resolve().parents[3]
    endpoints = stored_endpoints(repository)
    started = time.time()
    result = {
        "status": STATUS,
        "method": (
            "active-contact rigidity soft modes and row-deletion flexes, "
            "followed by direct epigraph SLSQP"
        ),
        "active_tolerance": ACTIVE_TOLERANCE,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "max_iterations": int(arguments.max_iterations),
            "n41_trials": int(arguments.n41_trials),
            "n41_seeds": [
                int(2026072301 + index)
                for index in range(arguments.n41_trials)
            ],
        },
        "runs": [],
    }

    for n in range(41, 45):
        x, origin = endpoints[n]
        baseline = diagnostics(x)
        if n == 41:
            seeds = tuple(
                2026072301 + index
                for index in range(arguments.n41_trials)
            )
            trials, best, structure = run_41_edge_release(
                x,
                origin,
                seeds,
                scales=(0.03, 0.15, 0.40),
                max_iterations=arguments.max_iterations,
            )
        elif n == 42:
            # Eight tail modes are motions of the two inactive points.  The
            # next three are the softest modes involving the active core.
            trials, best = run_soft_modes(
                n,
                x,
                origin,
                tail_indices=(9, 10, 11),
                scales=(0.01, 0.08, 0.20),
                max_iterations=arguments.max_iterations,
            )
            structure = {}
        elif n == 43:
            trials, best = run_soft_modes(
                n,
                x,
                origin,
                tail_indices=(1, 2, 3),
                scales=(0.01, 0.08, 0.15),
                max_iterations=arguments.max_iterations,
            )
            structure = {}
        else:
            trials, best = run_soft_modes(
                n,
                x,
                origin,
                tail_indices=(1, 2, 3),
                scales=(0.01, 0.10, 0.30),
                max_iterations=arguments.max_iterations,
            )
            structure = {}
        result["runs"].append(
            {
                "n": n,
                "origin": origin,
                "baseline": baseline,
                "structure": structure,
                "trial_count": int(len(trials)),
                "trials": trials,
                "best": {
                    "diagnostics": diagnostics(best),
                    "coordinates_float64": unit_rows(best).tolist(),
                },
                "beat_baseline": bool(
                    maximum_inner_product(best)
                    < baseline["maximum_inner_product"] - 1e-13
                ),
                "reached_half": bool(
                    maximum_inner_product(best) <= 0.5
                ),
            }
        )
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n"
        )

    result["elapsed_seconds"] = float(time.time() - started)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    for run in result["runs"]:
        print(
            f"FINAL N={run['n']} "
            f"baseline={run['baseline']['maximum_inner_product']:.17g} "
            f"best={run['best']['diagnostics']['maximum_inner_product']:.17g}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

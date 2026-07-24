#!/usr/bin/env python3
"""Numerical N=41 challenges seeded by the thirteen exact K40 completions.

This is deliberately unrestricted floating-point discovery code.  Solver
failure or a final maximum above 1/2 is not a proof of nonexistence.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
CLASSIFICATION = (
    HERE.parent / "classification" / "completion_classification.json"
)
CLASSIFICATION_SHA256 = (
    "ccabd04602c5481d40fa16d5979a7cbcb04fa3ece357f3c97d39e881f1bef0a0"
)
STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DIMENSION = 5


def unit_rows(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array, dtype=np.float64)
    norms = np.linalg.norm(array, axis=1)
    if array.ndim != 2 or array.shape[1] != DIMENSION:
        raise ValueError("coordinates must be N by 5")
    if float(np.min(norms)) < 1e-12:
        raise ValueError("cannot normalize a zero row")
    return array / norms[:, None]


def pair_indices(size: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(size, 1)


def pair_values(array: np.ndarray) -> np.ndarray:
    array = unit_rows(array)
    first, second = pair_indices(len(array))
    return np.sum(array[first] * array[second], axis=1)


def maximum(array: np.ndarray) -> float:
    return float(np.max(pair_values(array)))


def smooth_objective(
    raw: np.ndarray,
    size: int,
    beta: float,
) -> tuple[float, np.ndarray]:
    unnormalized = raw.reshape(size, DIMENSION)
    norms = np.linalg.norm(unnormalized, axis=1)
    array = unnormalized / norms[:, None]
    first, second = pair_indices(size)
    products = np.sum(array[first] * array[second], axis=1)
    peak = float(np.max(products))
    exponentials = np.exp(beta * (products - peak))
    weights = exponentials / np.sum(exponentials)
    value = peak + float(np.log(np.sum(exponentials))) / beta
    ambient = np.zeros_like(array)
    np.add.at(ambient, first, weights[:, None] * array[second])
    np.add.at(ambient, second, weights[:, None] * array[first])
    tangent = ambient - np.sum(ambient * array, axis=1)[:, None] * array
    gradient = tangent / norms[:, None]
    return value, gradient.ravel()


def smooth_release(
    initial: np.ndarray,
    betas: tuple[float, ...],
    maxiter: int,
) -> tuple[np.ndarray, list[dict]]:
    array = unit_rows(initial)
    history = []
    for beta in betas:
        before = maximum(array)
        result = minimize(
            smooth_objective,
            array.ravel(),
            args=(len(array), beta),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": maxiter,
                "ftol": 2e-15,
                "gtol": 2e-10,
                "maxls": 50,
            },
        )
        array = unit_rows(result.x.reshape(len(array), DIMENSION))
        history.append(
            {
                "beta": beta,
                "before_maximum": before,
                "after_maximum": maximum(array),
                "solver_success": bool(result.success),
                "solver_status": int(result.status),
                "iterations": int(result.nit),
                "function_evaluations": int(result.nfev),
                "message": str(result.message),
            }
        )
    return array, history


def epigraph_release(
    initial: np.ndarray,
    maxiter: int,
) -> tuple[np.ndarray, dict]:
    array = unit_rows(initial)
    size = len(array)
    first, second = pair_indices(size)
    start = np.r_[array.ravel(), maximum(array) + 2e-9]

    def objective(vector):
        return float(vector[-1])

    def objective_jacobian(vector):
        gradient = np.zeros_like(vector)
        gradient[-1] = 1.0
        return gradient

    def equalities(vector):
        points = vector[:-1].reshape(size, DIMENSION)
        return np.sum(points * points, axis=1) - 1.0

    def equality_jacobian(vector):
        points = vector[:-1].reshape(size, DIMENSION)
        jacobian = np.zeros((size, size * DIMENSION + 1))
        for vertex in range(size):
            jacobian[
                vertex,
                DIMENSION * vertex : DIMENSION * (vertex + 1),
            ] = 2.0 * points[vertex]
        return jacobian

    def inequalities(vector):
        points = vector[:-1].reshape(size, DIMENSION)
        return vector[-1] - np.sum(points[first] * points[second], axis=1)

    def inequality_jacobian(vector):
        points = vector[:-1].reshape(size, DIMENSION)
        jacobian = np.zeros((len(first), size * DIMENSION + 1))
        rows = np.arange(len(first))
        for coordinate in range(DIMENSION):
            jacobian[rows, DIMENSION * first + coordinate] = -points[
                second, coordinate
            ]
            jacobian[rows, DIMENSION * second + coordinate] = -points[
                first, coordinate
            ]
        jacobian[:, -1] = 1.0
        return jacobian

    result = minimize(
        objective,
        start,
        jac=objective_jacobian,
        method="SLSQP",
        constraints=(
            {
                "type": "eq",
                "fun": equalities,
                "jac": equality_jacobian,
            },
            {
                "type": "ineq",
                "fun": inequalities,
                "jac": inequality_jacobian,
            },
        ),
        options={
            "maxiter": maxiter,
            "ftol": 5e-13,
            "disp": False,
        },
    )
    answer = unit_rows(result.x[:-1].reshape(size, DIMENSION))
    values = pair_values(answer)
    return answer, {
        "before_maximum": maximum(array),
        "after_maximum": float(np.max(values)),
        "reported_epigraph": float(result.x[-1]),
        "minimum_reported_inequality_slack": float(
            np.min(inequalities(result.x))
        ),
        "maximum_norm_error_before_retraction": float(
            np.max(np.abs(equalities(result.x)))
        ),
        "solver_success": bool(result.success),
        "solver_status": int(result.status),
        "iterations": int(result.nit),
        "function_evaluations": int(result.nfev),
        "message": str(result.message),
    }


def best_fixed_insertion(
    fixed: np.ndarray,
    rng: np.random.Generator,
    starts: int,
    maxiter: int,
) -> tuple[np.ndarray, dict]:
    fixed = unit_rows(fixed)

    def objective(vector):
        return float(vector[-1])

    def objective_jacobian(vector):
        gradient = np.zeros(6)
        gradient[-1] = 1.0
        return gradient

    def equality(vector):
        return np.array([np.dot(vector[:5], vector[:5]) - 1.0])

    def equality_jacobian(vector):
        return np.r_[2.0 * vector[:5], 0.0][None, :]

    def inequalities(vector):
        return vector[-1] - fixed @ vector[:5]

    def inequality_jacobian(vector):
        return np.column_stack([-fixed, np.ones(len(fixed))])

    seeds = [unit_rows(rng.normal(size=(1, DIMENSION)))[0] for _ in range(starts)]
    covariance = fixed.T @ fixed
    _, eigenvectors = np.linalg.eigh(covariance)
    seeds.extend([eigenvectors[:, 0], -eigenvectors[:, 0]])
    records = []
    best_point = None
    best_maximum = float("inf")
    for start_index, point in enumerate(seeds):
        initial = np.r_[point, float(np.max(fixed @ point)) + 1e-7]
        result = minimize(
            objective,
            initial,
            jac=objective_jacobian,
            method="SLSQP",
            constraints=(
                {"type": "eq", "fun": equality, "jac": equality_jacobian},
                {
                    "type": "ineq",
                    "fun": inequalities,
                    "jac": inequality_jacobian,
                },
            ),
            options={"maxiter": maxiter, "ftol": 2e-13, "disp": False},
        )
        candidate = result.x[:5]
        norm = float(np.linalg.norm(candidate))
        if norm < 1e-12:
            continue
        candidate /= norm
        recomputed = float(np.max(fixed @ candidate))
        records.append(
            {
                "start": start_index,
                "recomputed_maximum": recomputed,
                "reported_epigraph": float(result.x[-1]),
                "solver_success": bool(result.success),
                "solver_status": int(result.status),
                "iterations": int(result.nit),
            }
        )
        if recomputed < best_maximum:
            best_maximum = recomputed
            best_point = candidate.copy()
    if best_point is None:
        raise RuntimeError("all fixed-insertion solves failed")
    return best_point, {
        "restart_count": len(seeds),
        "best_recomputed_maximum": best_maximum,
        "runs": records,
    }


def perturb(
    array: np.ndarray,
    rng: np.random.Generator,
    amplitude: float,
) -> np.ndarray:
    array = unit_rows(array)
    noise = rng.normal(size=array.shape)
    noise -= np.sum(noise * array, axis=1)[:, None] * array
    row_norms = np.linalg.norm(noise, axis=1)
    noise /= np.maximum(row_norms[:, None], 1e-15)
    scales = amplitude * rng.uniform(0.35, 1.0, size=(len(array), 1))
    return unit_rows(array + scales * noise)


def diagnostics(array: np.ndarray) -> dict:
    array = unit_rows(array)
    values = pair_values(array)
    gram = array @ array.T
    eigenvalues = np.linalg.eigvalsh(gram)
    return {
        "maximum": float(np.max(values)),
        "minimum": float(np.min(values)),
        "violating_pairs_above_half": int(np.sum(values > 0.5)),
        "pairs_within_1e-6_of_maximum": int(
            np.sum(values >= float(np.max(values)) - 1e-6)
        ),
        "quantiles": {
            str(level): float(np.quantile(values, level))
            for level in (0.5, 0.9, 0.95, 0.99)
        },
        "gram_eigenvalues": [float(value) for value in eigenvalues],
        "maximum_norm_error": float(
            np.max(np.abs(np.linalg.norm(array, axis=1) - 1.0))
        ),
        "coordinate_sha256_float64": hashlib.sha256(
            np.asarray(array, dtype="<f8").tobytes()
        ).hexdigest(),
    }


def parse_coordinates(entry: dict) -> np.ndarray:
    numerator = np.array(
        [
            [float(Fraction(value)) for value in row]
            for row in entry["coordinates_numerator_over_sqrt2"]
        ],
        dtype=np.float64,
    )
    return unit_rows(numerator)


# Imported late to keep the optimization code's numerical dependencies clear.
from fractions import Fraction


def run_challenge(
    base: np.ndarray,
    atom_index: int,
    known_type: str,
    mode: str,
    seed: int,
    arguments,
) -> dict:
    rng = np.random.default_rng(seed)
    if mode == "insert_release":
        inserted, fixed_record = best_fixed_insertion(
            base,
            rng,
            arguments.hole_starts,
            arguments.hole_maxiter,
        )
        unperturbed = np.vstack([base, inserted])
        deleted_vertex = None
        insertion_records = [fixed_record]
    elif mode == "replace_one_by_two":
        deleted_vertex = int((atom_index * 17 + seed) % 40)
        fixed = np.delete(base, deleted_vertex, axis=0)
        first, first_record = best_fixed_insertion(
            fixed,
            rng,
            arguments.hole_starts,
            arguments.hole_maxiter,
        )
        second, second_record = best_fixed_insertion(
            np.vstack([fixed, first]),
            rng,
            arguments.hole_starts,
            arguments.hole_maxiter,
        )
        unperturbed = np.vstack([fixed, first, second])
        insertion_records = [first_record, second_record]
    else:
        raise ValueError(f"unknown challenge mode {mode}")

    amplitude = arguments.perturbation * (
        0.75 + 0.5 * ((atom_index + seed) % 7) / 6.0
    )
    initial = perturb(unperturbed, rng, amplitude)
    smooth, smooth_history = smooth_release(
        initial,
        tuple(arguments.betas),
        arguments.smooth_maxiter,
    )
    final, epigraph = epigraph_release(smooth, arguments.slsqp_maxiter)
    return {
        "atom_index": atom_index,
        "known_type": known_type,
        "mode": mode,
        "seed": seed,
        "deleted_vertex": deleted_vertex,
        "perturbation_amplitude": amplitude,
        "fixed_insertion": insertion_records,
        "unperturbed_diagnostics": diagnostics(unperturbed),
        "unperturbed_coordinates_float64": unperturbed.tolist(),
        "initial_diagnostics": diagnostics(initial),
        "initial_coordinates_float64": initial.tolist(),
        "smooth_history": smooth_history,
        "epigraph_refinement": epigraph,
        "final_diagnostics": diagnostics(final),
        "final_coordinates_float64": final.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--modes",
        nargs="+",
        choices=("insert_release", "replace_one_by_two"),
        default=("insert_release", "replace_one_by_two"),
    )
    parser.add_argument("--atoms", nargs="*", type=int)
    parser.add_argument("--seed-base", type=int, default=541113)
    parser.add_argument("--hole-starts", type=int, default=6)
    parser.add_argument("--hole-maxiter", type=int, default=600)
    parser.add_argument(
        "--betas",
        nargs="+",
        type=float,
        default=(24.0, 64.0, 160.0, 400.0, 1000.0),
    )
    parser.add_argument("--smooth-maxiter", type=int, default=350)
    parser.add_argument("--slsqp-maxiter", type=int, default=700)
    parser.add_argument("--perturbation", type=float, default=0.035)
    arguments = parser.parse_args()

    digest = hashlib.sha256(CLASSIFICATION.read_bytes()).hexdigest()
    if digest != CLASSIFICATION_SHA256:
        raise RuntimeError("classification certificate hash mismatch")
    classification = json.loads(CLASSIFICATION.read_text())
    selected = set(arguments.atoms) if arguments.atoms else None
    entries = [
        entry
        for entry in classification["entries"]
        if selected is None or entry["atom_index"] in selected
    ]
    if selected is not None and {entry["atom_index"] for entry in entries} != selected:
        raise ValueError("requested atom is absent from the classification")

    runs = []
    for entry_index, entry in enumerate(entries):
        base = parse_coordinates(entry)
        for mode_index, mode in enumerate(arguments.modes):
            seed = (
                arguments.seed_base
                + 1009 * entry["atom_index"]
                + 7919 * mode_index
                + 104729 * entry_index
            )
            run = run_challenge(
                base,
                entry["atom_index"],
                entry["known_type"],
                mode,
                seed,
                arguments,
            )
            runs.append(run)
            print(
                entry["atom_index"],
                mode,
                run["final_diagnostics"]["maximum"],
                flush=True,
            )

    best = min(runs, key=lambda run: run["final_diagnostics"]["maximum"])
    result = {
        "schema": "kissing5.k11_k40_seeded_n41_probe.v1",
        "status": STATUS,
        "classification_source": str(CLASSIFICATION),
        "classification_sha256": digest,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "modes": list(arguments.modes),
            "atoms": [entry["atom_index"] for entry in entries],
            "seed_base": arguments.seed_base,
            "hole_starts": arguments.hole_starts,
            "hole_maxiter": arguments.hole_maxiter,
            "betas": arguments.betas,
            "smooth_maxiter": arguments.smooth_maxiter,
            "slsqp_maxiter": arguments.slsqp_maxiter,
            "perturbation": arguments.perturbation,
        },
        "run_count": len(runs),
        "runs": runs,
        "best": {
            "atom_index": best["atom_index"],
            "known_type": best["known_type"],
            "mode": best["mode"],
            "seed": best["seed"],
            "maximum": best["final_diagnostics"]["maximum"],
            "run_index": runs.index(best),
        },
        "scope_warning": (
            "These are local floating-point optimization runs. Failure to "
            "reach 1/2 is not an obstruction and no coordinate array is an "
            "exact spherical code certificate."
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

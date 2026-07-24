#!/usr/bin/env python3
"""Asymmetric deletion/reinsertion search for 41--44 points on S^4.

NUMERICAL DISCOVERY ONLY.  This program does not certify feasibility or
nonexistence.

The macro move is deliberately different from the round-3 Riemannian
augmented-Lagrangian search.  It repeatedly removes one or two points having
large active-contact stress, solves a maximin-hole problem against the
remaining cloud, reinserts new points, and then releases every coordinate
through a smooth-max continuation.  Uphill moves are accepted with a
deterministic simulated-annealing rule, allowing changes of contact basin.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"


def unit_rows(array: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(array, axis=1)
    if float(np.min(norms)) < 1e-13:
        raise ValueError("zero row in normalization")
    return array / norms[:, None]


def d5_roots() -> np.ndarray:
    roots = []
    for i in range(5):
        for j in range(i + 1, 5):
            for first in (-1.0, 1.0):
                for second in (-1.0, 1.0):
                    vector = np.zeros(5)
                    vector[i] = first / math.sqrt(2.0)
                    vector[j] = second / math.sqrt(2.0)
                    roots.append(vector)
    answer = np.asarray(roots)
    assert answer.shape == (40, 5)
    assert abs(max_inner_product(answer) - 0.5) < 1e-14
    return answer


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(x: np.ndarray) -> np.ndarray:
    ii, jj = pair_indices(len(x))
    return np.sum(x[ii] * x[jj], axis=1)


def max_inner_product(x: np.ndarray) -> float:
    return float(np.max(pair_values(unit_rows(x))))


def logsumexp_weights(values: np.ndarray, beta: float):
    shifted = beta * (values - float(np.max(values)))
    raw = np.exp(shifted)
    weights = raw / float(np.sum(raw))
    value = float(np.max(values)) + math.log(float(np.sum(raw))) / beta
    return value, weights


def smooth_full(flat: np.ndarray, n: int, beta: float):
    raw = flat.reshape(n, 5)
    norms = np.linalg.norm(raw, axis=1)
    x = raw / norms[:, None]
    ii, jj = pair_indices(n)
    products = np.sum(x[ii] * x[jj], axis=1)
    value, weights = logsumexp_weights(products, beta)
    ambient = np.zeros_like(x)
    np.add.at(ambient, ii, weights[:, None] * x[jj])
    np.add.at(ambient, jj, weights[:, None] * x[ii])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    gradient = tangent / norms[:, None]
    return value, gradient.ravel()


def relax(
    x: np.ndarray,
    betas=(40.0, 160.0, 640.0, 2560.0),
    maxiter: int = 280,
):
    x = unit_rows(x)
    history = []
    for beta in betas:
        result = minimize(
            smooth_full,
            x.ravel(),
            args=(len(x), beta),
            jac=True,
            method="L-BFGS-B",
            options={
                "maxiter": maxiter,
                "ftol": 2e-15,
                "gtol": 2e-9,
                "maxls": 50,
                "maxcor": 30,
            },
        )
        x = unit_rows(result.x.reshape(len(x), 5))
        history.append(
            {
                "beta": beta,
                "iterations": int(result.nit),
                "solver_success": bool(result.success),
                "smooth_value": float(result.fun),
                "true_maximum": max_inner_product(x),
            }
        )
    return x, history


def epigraph_refine(x: np.ndarray, maxiter: int = 900):
    """Direct minimax SQP used only after the basin-hopping search."""
    x = unit_rows(x)
    n = len(x)
    ii, jj = pair_indices(n)
    initial = np.r_[x.ravel(), max_inner_product(x)]

    def objective(variable):
        return float(variable[-1])

    def objective_jac(variable):
        answer = np.zeros_like(variable)
        answer[-1] = 1.0
        return answer

    def inequalities(variable):
        points = variable[:-1].reshape(n, 5)
        return variable[-1] - np.sum(points[ii] * points[jj], axis=1)

    def inequalities_jac(variable):
        points = variable[:-1].reshape(n, 5)
        answer = np.zeros((len(ii), len(variable)))
        rows = np.arange(len(ii))
        for coordinate in range(5):
            answer[rows, 5 * ii + coordinate] = -points[jj, coordinate]
            answer[rows, 5 * jj + coordinate] = -points[ii, coordinate]
        answer[:, -1] = 1.0
        return answer

    def equalities(variable):
        points = variable[:-1].reshape(n, 5)
        return np.sum(points * points, axis=1) - 1.0

    def equalities_jac(variable):
        points = variable[:-1].reshape(n, 5)
        answer = np.zeros((n, len(variable)))
        rows = np.arange(n)
        for coordinate in range(5):
            answer[rows, 5 * rows + coordinate] = 2.0 * points[:, coordinate]
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
        options={"maxiter": maxiter, "ftol": 2e-13, "disp": False},
    )
    answer = unit_rows(result.x[:-1].reshape(n, 5))
    return answer, {
        "solver_success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": max_inner_product(answer),
    }


def smooth_hole(raw: np.ndarray, fixed: np.ndarray, beta: float):
    norm = float(np.linalg.norm(raw))
    if norm < 1e-13:
        return 1e6, np.zeros_like(raw)
    y = raw / norm
    products = fixed @ y
    value, weights = logsumexp_weights(products, beta)
    ambient = fixed.T @ weights
    gradient = (ambient - float(ambient @ y) * y) / norm
    return value, gradient


def epigraph_hole(fixed: np.ndarray, start: np.ndarray):
    start = start / np.linalg.norm(start)
    initial = np.r_[start, float(np.max(fixed @ start))]

    def objective(variable):
        return float(variable[-1])

    def objective_jac(variable):
        answer = np.zeros(6)
        answer[-1] = 1.0
        return answer

    def inequalities(variable):
        return variable[-1] - fixed @ variable[:5]

    def inequalities_jac(variable):
        answer = np.empty((len(fixed), 6))
        answer[:, :5] = -fixed
        answer[:, 5] = 1.0
        return answer

    def equality(variable):
        return float(variable[:5] @ variable[:5] - 1.0)

    def equality_jac(variable):
        answer = np.zeros(6)
        answer[:5] = 2.0 * variable[:5]
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
                "fun": equality,
                "jac": equality_jac,
            },
        ],
        method="SLSQP",
        options={"maxiter": 600, "ftol": 2e-13, "disp": False},
    )
    y = result.x[:5]
    y /= np.linalg.norm(y)
    return y, {
        "solver_success": bool(result.success),
        "iterations": int(result.nit),
        "maximum_against_fixed": float(np.max(fixed @ y)),
    }


def largest_hole(
    fixed: np.ndarray,
    rng: np.random.Generator,
    starts: int,
):
    candidates = []
    for _ in range(starts):
        y = rng.normal(size=5)
        y /= np.linalg.norm(y)
        for beta in (20.0, 80.0, 320.0, 1280.0):
            result = minimize(
                smooth_hole,
                y,
                args=(fixed, beta),
                jac=True,
                method="L-BFGS-B",
                options={
                    "maxiter": 220,
                    "ftol": 2e-15,
                    "gtol": 1e-10,
                    "maxls": 50,
                },
            )
            y = result.x / np.linalg.norm(result.x)
        y, audit = epigraph_hole(fixed, y)
        candidates.append((audit["maximum_against_fixed"], y, audit))
    candidates.sort(key=lambda item: item[0])
    return candidates[0][1], candidates[0][2]


def contact_stress(x: np.ndarray, beta: float = 900.0):
    ii, jj = pair_indices(len(x))
    values = np.sum(x[ii] * x[jj], axis=1)
    _, weights = logsumexp_weights(values, beta)
    stress = np.zeros(len(x))
    np.add.at(stress, ii, weights)
    np.add.at(stress, jj, weights)
    return stress


def initial_surgery(n: int, seed: int, rng: np.random.Generator):
    roots = d5_roots()
    delete_count = 7 + (seed % 6)
    deleted = np.sort(rng.choice(40, delete_count, replace=False))
    current = np.delete(roots, deleted, axis=0)
    insertion_log = []
    for insertion in range(delete_count + n - 40):
        point, audit = largest_hole(current, rng, starts=4)
        # A deterministic tangent kick prevents every deleted root from simply
        # being restored before the first all-coordinate release.
        kick = rng.normal(size=5)
        kick -= float(kick @ point) * point
        point = point + (0.035 + 0.005 * (insertion % 3)) * kick
        point /= np.linalg.norm(point)
        current = np.vstack([current, point])
        if insertion % 3 == 2 or len(current) == n:
            current, _ = relax(
                current,
                betas=(30.0, 120.0, 480.0),
                maxiter=120,
            )
        insertion_log.append(audit)
    assert len(current) == n
    current, release_history = relax(current)
    return current, {
        "deleted_d5_indices": deleted.tolist(),
        "delete_count": int(delete_count),
        "hole_insertions": insertion_log,
        "initial_release": release_history,
    }


def active_edges(x: np.ndarray, tolerance: float):
    ii, jj = pair_indices(len(x))
    values = np.sum(x[ii] * x[jj], axis=1)
    maximum = float(np.max(values))
    chosen = np.flatnonzero(values >= maximum - tolerance)
    return [[int(ii[index]), int(jj[index])] for index in chosen]


def diagnostics(x: np.ndarray):
    x = unit_rows(x)
    gram = x @ x.T
    values = pair_values(x)
    eigenvalues = np.linalg.eigvalsh(gram)
    return {
        "maximum_inner_product": float(np.max(values)),
        "gap_above_one_half": float(np.max(values) - 0.5),
        "minimum_inner_product": float(np.min(values)),
        "pairs_below_minus_one_half": int(np.sum(values < -0.5)),
        "norm_error": float(np.max(np.abs(np.sum(x * x, axis=1) - 1.0))),
        "gram_eigenvalues": eigenvalues.tolist(),
        "active_edges_1e-6": active_edges(x, 1e-6),
        "active_edges_1e-8": active_edges(x, 1e-8),
        "coordinate_sha256": hashlib.sha256(
            json.dumps(x.tolist(), separators=(",", ":")).encode()
        ).hexdigest(),
    }


def run_one(n: int, seed: int, moves: int):
    rng = np.random.default_rng(seed)
    started = time.time()
    current, initialization = initial_surgery(n, seed, rng)
    current_value = max_inner_product(current)
    best = current.copy()
    best_value = current_value
    move_log = []

    for move in range(moves):
        remove_count = 2 if move % 6 == 5 else 1
        stress = contact_stress(current)
        # Choose among the most stressed points instead of deterministically
        # cycling a fixed contact graph.
        pool_size = min(len(current), 6 + move % 5)
        pool = np.argsort(stress)[-pool_size:]
        probabilities = stress[pool] + 1e-12
        probabilities /= float(np.sum(probabilities))
        removed = np.sort(
            rng.choice(pool, remove_count, replace=False, p=probabilities)
        )
        candidate = np.delete(current, removed, axis=0)
        hole_log = []
        for _ in range(remove_count):
            point, audit = largest_hole(candidate, rng, starts=5)
            candidate = np.vstack([candidate, point])
            hole_log.append(audit)
        candidate, continuation = relax(
            candidate,
            betas=(60.0, 240.0, 960.0, 3840.0),
            maxiter=180,
        )
        candidate_value = max_inner_product(candidate)
        temperature = 0.004 * (0.82 ** move)
        accepted = candidate_value <= current_value
        if not accepted and temperature > 1e-8:
            accepted = (
                rng.random()
                < math.exp(-(candidate_value - current_value) / temperature)
            )
        if accepted:
            current = candidate
            current_value = candidate_value
        if candidate_value < best_value:
            best = candidate.copy()
            best_value = candidate_value
        move_log.append(
            {
                "move": move,
                "removed_indices_before_reinsertion": removed.tolist(),
                "remove_count": remove_count,
                "hole_searches": hole_log,
                "candidate_maximum": candidate_value,
                "accepted": bool(accepted),
                "temperature": temperature,
                "best_maximum": best_value,
                "continuation": continuation,
            }
        )

    best, final_history = relax(
        best,
        betas=(640.0, 2560.0, 10240.0, 40960.0),
        maxiter=500,
    )
    best, epigraph_history = epigraph_refine(best)
    return {
        "n": n,
        "seed": seed,
        "moves": moves,
        "initialization": initialization,
        "move_log": move_log,
        "final_continuation": final_history,
        "final_epigraph_slsqp": epigraph_history,
        "diagnostics": diagnostics(best),
        "coordinates": best.tolist(),
        "elapsed_seconds": time.time() - started,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, nargs="+", default=[41, 42, 43, 44])
    parser.add_argument("--seeds", type=int, nargs="+", required=True)
    parser.add_argument("--moves", type=int, default=18)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    runs = []
    for n in arguments.n:
        if n < 41 or n > 44:
            raise ValueError("this portfolio is scoped to 41 <= n <= 44")
        for seed in arguments.seeds:
            result = run_one(n, seed, arguments.moves)
            runs.append(result)
            print(
                n,
                seed,
                result["diagnostics"]["maximum_inner_product"],
                flush=True,
            )
    payload = {
        "status": STATUS,
        "mechanism": (
            "asymmetric D5 deletion/reinsertion, maximin-hole solves, "
            "contact-stress basin hopping, all-coordinate smooth-max release"
        ),
        "python": sys.version,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "runs": runs,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Population crossover and inverse-chord continuation on (S^4)^N.

This is numerical discovery code, not a proof or construction certificate.
The main search mechanism is deliberately population based:

* initialize independent asymmetric and inherited numerical configurations;
* locally minimize inverse-chord p-energies for increasing p;
* align two parents by alternating orthogonal Procrustes and Hungarian
  matching, then splice their point rows and add a tangent mutation;
* retain both low-energy elites and a descriptor-diverse individual.

All coordinates are unrestricted after initialization.  A direct minimax
SLSQP solve is used only as a final diagnostic on the best population member.
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
from scipy.optimize import linear_sum_assignment, minimize


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DIMENSION = 5


def unit_rows(array: np.ndarray) -> np.ndarray:
    array = np.asarray(array, dtype=float)
    norms = np.linalg.norm(array, axis=1)
    if array.ndim != 2 or array.shape[1] != DIMENSION:
        raise ValueError("coordinates must be an N by 5 array")
    if float(np.min(norms)) <= 1e-13:
        raise ValueError("cannot normalize a zero row")
    return array / norms[:, None]


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(array: np.ndarray) -> np.ndarray:
    array = unit_rows(array)
    ii, jj = pair_indices(len(array))
    return np.sum(array[ii] * array[jj], axis=1)


def max_inner_product(array: np.ndarray) -> float:
    return float(np.max(pair_values(array)))


def d5_roots() -> np.ndarray:
    roots = []
    scale = 1.0 / math.sqrt(2.0)
    for i in range(5):
        for j in range(i + 1, 5):
            for first in (-1.0, 1.0):
                for second in (-1.0, 1.0):
                    row = np.zeros(5)
                    row[i] = first * scale
                    row[j] = second * scale
                    roots.append(row)
    return np.asarray(roots)


def inverse_chord_objective(
    flat: np.ndarray, n: int, power: float
) -> tuple[float, np.ndarray]:
    """Return a stable logarithmic inverse-chord energy and its gradient.

    The objective is

        (1/p) log sum_{i<j} (1-<x_i,x_j>)^{-p}.

    It converges to ``-log(1-max <x_i,x_j>)`` as p tends to infinity.
    Rows in ``flat`` are normalized inside the objective, so its Euclidean
    gradient includes the normalization derivative.
    """
    if power <= 0:
        raise ValueError("power must be positive")
    raw = np.asarray(flat, dtype=float).reshape(n, DIMENSION)
    norms = np.linalg.norm(raw, axis=1)
    if float(np.min(norms)) <= 1e-13:
        return 1e30, np.zeros_like(flat)
    x = raw / norms[:, None]
    ii, jj = pair_indices(n)
    inner = np.sum(x[ii] * x[jj], axis=1)
    gaps = np.maximum(1.0 - inner, 1e-15)
    logarithms = -power * np.log(gaps)
    shift = float(np.max(logarithms))
    unscaled = np.exp(logarithms - shift)
    weights = unscaled / float(np.sum(unscaled))
    value = (shift + math.log(float(np.sum(unscaled)))) / power

    # d[-log(1-s)]/ds = 1/(1-s).
    edge_weights = weights / gaps
    ambient = np.zeros_like(x)
    np.add.at(ambient, ii, edge_weights[:, None] * x[jj])
    np.add.at(ambient, jj, edge_weights[:, None] * x[ii])
    tangent = ambient - np.sum(ambient * x, axis=1)[:, None] * x
    gradient = tangent / norms[:, None]
    return float(value), gradient.ravel()


def relax_power(
    array: np.ndarray, power: float, max_iterations: int
) -> tuple[np.ndarray, dict]:
    x = unit_rows(array)
    result = minimize(
        inverse_chord_objective,
        x.ravel(),
        args=(len(x), power),
        jac=True,
        method="L-BFGS-B",
        options={
            "maxiter": int(max_iterations),
            "ftol": 2e-15,
            "gtol": 5e-9,
            "maxls": 50,
            "maxcor": 30,
        },
    )
    answer = unit_rows(result.x.reshape(len(x), DIMENSION))
    return answer, {
        "power": float(power),
        "iterations": int(result.nit),
        "evaluations": int(result.nfev),
        "success": bool(result.success),
        "message": str(result.message),
        "energy": float(result.fun),
        "maximum": max_inner_product(answer),
    }


def align_parent(reference: np.ndarray, moving: np.ndarray, rounds: int = 5):
    """Align and relabel ``moving`` to ``reference`` for crossover.

    Orthogonal Procrustes and minimum squared-distance assignment are
    alternated.  This changes neither parent's Gram matrix nor objective.
    """
    reference = unit_rows(reference)
    moving = unit_rows(moving)
    if reference.shape != moving.shape:
        raise ValueError("parent shapes differ")
    # Covariance eigenframes provide a relabeling-invariant initial
    # orientation.  Eigenvector signs are ambiguous, so inspect all 2^5
    # choices and retain the one with the cheapest linear assignment.
    _, reference_frame = np.linalg.eigh(reference.T @ reference)
    _, moving_frame = np.linalg.eigh(moving.T @ moving)
    best_cost = math.inf
    aligned = moving.copy()
    for bits in range(1 << DIMENSION):
        signs = np.asarray(
            [-1.0 if bits & (1 << coordinate) else 1.0
             for coordinate in range(DIMENSION)]
        )
        rotation = (moving_frame * signs[None, :]) @ reference_frame.T
        candidate = moving @ rotation
        cost = 2.0 - 2.0 * (reference @ candidate.T)
        rows, columns = linear_sum_assignment(cost)
        total = float(np.sum(cost[rows, columns]))
        if total < best_cost:
            best_cost = total
            aligned = candidate
    assignment = np.arange(len(reference))
    for _ in range(rounds):
        cost = 2.0 - 2.0 * (reference @ aligned.T)
        rows, columns = linear_sum_assignment(cost)
        if not np.array_equal(rows, np.arange(len(reference))):
            raise ArithmeticError("unexpected assignment row order")
        assignment = assignment[columns]
        aligned = aligned[columns]
        left, _, right = np.linalg.svd(aligned.T @ reference)
        aligned = aligned @ (left @ right)
    return aligned, assignment


def tangent_noise(x: np.ndarray, rng: np.random.Generator, scale: float):
    noise = rng.normal(size=x.shape)
    noise -= np.sum(noise * x, axis=1)[:, None] * x
    return unit_rows(x + scale * noise)


def crossover(
    first: np.ndarray,
    second: np.ndarray,
    rng: np.random.Generator,
    mutation_scale: float,
) -> tuple[np.ndarray, dict]:
    aligned, assignment = align_parent(first, second)
    n = len(first)
    # A random hyperplane selects a geometrically coherent subset of points.
    normal = rng.normal(size=DIMENSION)
    normal /= np.linalg.norm(normal)
    scores = first @ normal
    threshold = float(np.quantile(scores, rng.uniform(0.25, 0.75)))
    use_second = scores >= threshold
    # Randomly choose interpolation or a hard splice.  Negative coefficients
    # deliberately permit extrapolation away from both parental basins.
    if rng.random() < 0.5:
        alpha = float(rng.uniform(-0.20, 1.20))
        child = (1.0 - alpha) * first + alpha * aligned
        mode = "extrapolated_blend"
    else:
        child = first.copy()
        child[use_second] = aligned[use_second]
        alpha = None
        mode = "hyperplane_splice"
    child = tangent_noise(unit_rows(child), rng, mutation_scale)
    return child, {
        "mode": mode,
        "alpha": alpha,
        "second_rows": int(np.sum(use_second)),
        "assignment": assignment.tolist(),
    }


def descriptor(x: np.ndarray) -> np.ndarray:
    """An isometry- and relabeling-invariant diversity descriptor."""
    values = np.sort(pair_values(x))
    quantiles = np.quantile(values, np.linspace(0.0, 1.0, 21))
    gram_eigenvalues = np.linalg.eigvalsh(x @ x.T)[-5:]
    return np.r_[quantiles, gram_eigenvalues / len(x)]


def farthest_sample_insert(
    x: np.ndarray, target_n: int, rng: np.random.Generator, samples: int = 20000
) -> np.ndarray:
    answer = unit_rows(x)
    while len(answer) < target_n:
        candidates = unit_rows(rng.normal(size=(samples, DIMENSION)))
        scores = np.max(candidates @ answer.T, axis=1)
        answer = np.vstack([answer, candidates[int(np.argmin(scores))]])
    return answer


def load_coordinate_runs(path: Path) -> list[tuple[np.ndarray, str]]:
    """Load coordinate arrays from any prior repository JSON shape."""
    with path.open() as stream:
        data = json.load(stream)
    candidates = []
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        records = data.get("runs", [])
    else:
        records = []
    for index, record in enumerate(records):
        raw = (
            record.get("coordinates_float64")
            or record.get("coordinates")
            or record.get("best_coordinates")
        )
        if raw is None:
            continue
        array = np.asarray(raw, dtype=float)
        if array.ndim == 2 and array.shape[1] == DIMENSION:
            candidates.append((unit_rows(array), f"{path.name}:run{index}"))
    return candidates


def inherited_best(paths: list[Path], n: int) -> list[tuple[np.ndarray, str]]:
    answer = []
    for path in paths:
        for array, label in load_coordinate_runs(path):
            if len(array) == n:
                answer.append((array, label))
    answer.sort(key=lambda item: max_inner_product(item[0]))
    return answer


def initial_population(
    n: int,
    population_size: int,
    rng: np.random.Generator,
    inherited: list[tuple[np.ndarray, str]],
) -> tuple[list[np.ndarray], list[str]]:
    population: list[np.ndarray] = []
    origins: list[str] = []
    if inherited:
        population.append(inherited[0][0].copy())
        origins.append("inherited_exact_binary64:" + inherited[0][1])
    for array, label in inherited[: max(1, population_size // 3)]:
        if len(population) >= population_size:
            break
        population.append(tangent_noise(array, rng, 0.05))
        origins.append("inherited_perturbed:" + label)
    if len(population) < population_size:
        population.append(farthest_sample_insert(d5_roots(), n, rng))
        origins.append("D5_plus_sampled_holes")
    while len(population) < population_size:
        population.append(unit_rows(rng.normal(size=(n, DIMENSION))))
        origins.append("asymmetric_gaussian")
    return population, origins


def select_population(candidates: list[np.ndarray], population_size: int):
    """Keep objective elites plus a descriptor-diverse tail."""
    ordered = sorted(candidates, key=max_inner_product)
    keep = ordered[: max(2, population_size - 1)]
    remaining = ordered[len(keep) :]
    if remaining:
        descriptors = [descriptor(x) for x in keep]

        def distance_to_keep(x):
            here = descriptor(x)
            return min(float(np.linalg.norm(here - old)) for old in descriptors)

        keep.append(max(remaining, key=distance_to_keep))
    return keep[:population_size]


def epigraph_refine(x: np.ndarray, max_iterations: int = 1200):
    """Final direct minimax diagnostic; it is not the search mechanism."""
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
        points = variable[:-1].reshape(n, DIMENSION)
        return variable[-1] - np.sum(points[ii] * points[jj], axis=1)

    def inequalities_jac(variable):
        points = variable[:-1].reshape(n, DIMENSION)
        answer = np.zeros((len(ii), len(variable)))
        rows = np.arange(len(ii))
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * ii + coordinate] = -points[jj, coordinate]
            answer[rows, DIMENSION * jj + coordinate] = -points[ii, coordinate]
        answer[:, -1] = 1.0
        return answer

    def equalities(variable):
        points = variable[:-1].reshape(n, DIMENSION)
        return np.sum(points * points, axis=1) - 1.0

    def equalities_jac(variable):
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
            {"type": "ineq", "fun": inequalities, "jac": inequalities_jac},
            {"type": "eq", "fun": equalities, "jac": equalities_jac},
        ],
        method="SLSQP",
        options={"maxiter": max_iterations, "ftol": 2e-13, "disp": False},
    )
    answer = unit_rows(result.x[:-1].reshape(n, DIMENSION))
    return answer, {
        "success": bool(result.success),
        "status": int(result.status),
        "message": str(result.message),
        "iterations": int(result.nit),
        "reported_epigraph": float(result.x[-1]),
        "recomputed_maximum": max_inner_product(answer),
    }


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    n = len(x)
    ii, jj = pair_indices(n)
    values = np.sum(x[ii] * x[jj], axis=1)
    maximum = float(np.max(values))
    answer = {
        "n": n,
        "maximum": maximum,
        "gap_above_one_half": maximum - 0.5,
        "minimum": float(np.min(values)),
        "deep_negative_pairs_below_minus_half": int(np.sum(values < -0.5)),
        "gram_eigenvalues": np.linalg.eigvalsh(x @ x.T).tolist(),
        "coordinates_float64": x.tolist(),
    }
    for tolerance in (1e-4, 1e-6, 1e-8):
        mask = values >= maximum - tolerance
        edges = np.column_stack([ii[mask], jj[mask]])
        degrees = np.bincount(edges.ravel(), minlength=n)
        unique, counts = np.unique(degrees, return_counts=True)
        answer[f"active_{tolerance:.0e}"] = {
            "edge_count": int(len(edges)),
            "degree_histogram": {
                str(int(key)): int(value) for key, value in zip(unique, counts)
            },
            "edges": edges.tolist(),
        }
    return answer


def run_search(
    n: int,
    seed: int,
    population_size: int,
    generations: int,
    iterations: int,
    inherited: list[tuple[np.ndarray, str]],
) -> dict:
    rng = np.random.default_rng(seed)
    population, origins = initial_population(
        n, population_size, rng, inherited
    )
    initial_archive = [x.copy() for x in population]
    history = []
    # Low powers spread random starts without forcing an early contact graph.
    for index in range(len(population)):
        local_history = []
        for power in (1.0, 3.0, 9.0):
            population[index], stage = relax_power(
                population[index], power, iterations
            )
            local_history.append(stage)
        history.append(
            {
                "phase": "initial",
                "member": index,
                "origin": origins[index],
                "stages": local_history,
            }
        )
    population = select_population(
        population + initial_archive, population_size
    )

    powers = np.geomspace(18.0, 1458.0, generations)
    for generation, power in enumerate(powers):
        ordered = sorted(population, key=max_inner_product)
        children = []
        cross_records = []
        child_count = max(3, population_size // 2)
        for child_index in range(child_count):
            first_index = int(rng.integers(0, max(2, population_size // 2)))
            second_index = int(rng.integers(0, population_size))
            if second_index == first_index:
                second_index = (second_index + 1) % population_size
            mutation = 0.16 * (0.55**generation)
            child, cross = crossover(
                ordered[first_index], ordered[second_index], rng, mutation
            )
            child, stage = relax_power(child, float(power), iterations)
            children.append(child)
            cross_records.append(
                {
                    "child": child_index,
                    "parents": [first_index, second_index],
                    "crossover": cross,
                    "relaxation": stage,
                }
            )
        # One independent immigrant prevents premature population collapse.
        immigrant = unit_rows(rng.normal(size=(n, DIMENSION)))
        immigrant, immigrant_stage = relax_power(
            immigrant, float(power), iterations
        )
        population = select_population(
            population + children + [immigrant], population_size
        )
        history.append(
            {
                "phase": "generation",
                "generation": generation,
                "power": float(power),
                "crossovers": cross_records,
                "immigrant": immigrant_stage,
                "population_maxima": [
                    max_inner_product(x) for x in population
                ],
            }
        )

    best = min(population, key=max_inner_product)
    polish_history = []
    for power in (2916.0, 5832.0, 11664.0):
        candidate, stage = relax_power(best, power, 2 * iterations)
        stage["accepted_by_true_maximum"] = (
            max_inner_product(candidate) <= max_inner_product(best)
        )
        if stage["accepted_by_true_maximum"]:
            best = candidate
        polish_history.append(stage)
    candidate, epigraph = epigraph_refine(best)
    epigraph["accepted_by_true_maximum"] = (
        max_inner_product(candidate) <= max_inner_product(best)
    )
    if epigraph["accepted_by_true_maximum"]:
        best = candidate
    return {
        "n": n,
        "seed": int(seed),
        "population_size": population_size,
        "generations": generations,
        "iterations_per_relaxation": iterations,
        "history": history,
        "polish_history": polish_history,
        "epigraph_refinement": epigraph,
        "best": diagnostics(best),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, default=[41, 42, 43, 44])
    parser.add_argument("--seeds", nargs="+", type=int, default=[2026072330])
    parser.add_argument("--population", type=int, default=8)
    parser.add_argument("--generations", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=180)
    parser.add_argument("--inherit", nargs="*", type=Path, default=[])
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    if any(n < 2 for n in arguments.n):
        parser.error("each n must be at least two")
    if arguments.population < 4:
        parser.error("population must be at least four")
    started = time.time()
    inputs = [
        {"path": str(path), "sha256": sha256(path)}
        for path in arguments.inherit
    ]
    runs = []
    for n in arguments.n:
        inherited = inherited_best(arguments.inherit, n)
        for seed in arguments.seeds:
            print(f"N={n} seed={seed}", flush=True)
            run = run_search(
                n,
                seed,
                arguments.population,
                arguments.generations,
                arguments.iterations,
                inherited,
            )
            print(
                f"  best={run['best']['maximum']:.16f}",
                flush=True,
            )
            runs.append(run)
    payload = {
        "status": STATUS,
        "method": "population inverse-chord continuation with aligned crossover",
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "parameters": {
            "n": arguments.n,
            "seeds": arguments.seeds,
            "population": arguments.population,
            "generations": arguments.generations,
            "iterations": arguments.iterations,
        },
        "inherited_inputs": inputs,
        "elapsed_seconds": time.time() - started,
        "runs": runs,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

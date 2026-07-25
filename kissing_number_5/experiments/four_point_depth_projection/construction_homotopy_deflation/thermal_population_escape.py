#!/usr/bin/env python3
"""High-temperature population escapes for spherical minimax codes.

NUMERICAL DISCOVERY ONLY.  This is not a construction certificate.

The macro mechanism is Riemannian population annealing, not a smooth
approximation of the maximum.  Walkers evolve under stochastic Langevin
steps for the literal threshold-hinge energy at 1/2.  During the hot stages,
an explicit history bias penalizes the inherited near-maximum edge set, so
the population is forced away from the known contact basin.  Resampling
retains both low-energy and contact-graph-distant walkers.  Only after this
global melt/cool process are candidates polished by an epigraph SQP with
all-pair constraint generation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DIMENSION = 5
TARGET = 0.5


MILD_SCHEDULE = (
    # bias, temperature, step size, Langevin steps
    (4.0, 1.6e-2, 0.018, 180),
    (4.0, 1.0e-2, 0.020, 180),
    (2.0, 5.0e-3, 0.024, 200),
    (0.5, 2.0e-3, 0.030, 220),
    (0.0, 7.0e-4, 0.035, 260),
    (0.0, 1.3e-4, 0.042, 320),
    (0.0, 1.0e-5, 0.050, 400),
)

STRONG_SCHEDULE = (
    (12.0, 1.0e-1, 0.018, 140),
    (12.0, 6.0e-2, 0.018, 140),
    (6.0, 2.5e-2, 0.022, 160),
    (2.0, 8.0e-3, 0.026, 180),
    (0.0, 2.5e-3, 0.032, 220),
    (0.0, 4.0e-4, 0.040, 280),
    (0.0, 3.0e-5, 0.050, 360),
)


def unit_rows(array: np.ndarray) -> np.ndarray:
    x = np.asarray(array, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != DIMENSION:
        raise ValueError("coordinates must be an N by 5 matrix")
    norms = np.linalg.norm(x, axis=1)
    if float(np.min(norms)) < 1e-14:
        raise ValueError("cannot normalize a zero row")
    return np.ascontiguousarray(x / norms[:, None])


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(x: np.ndarray) -> np.ndarray:
    ii, jj = pair_indices(len(x))
    return np.sum(x[ii] * x[jj], axis=1)


def maximum(x: np.ndarray) -> float:
    return float(np.max(pair_values(unit_rows(x))))


def coordinate_hash(x: np.ndarray) -> str:
    data = np.ascontiguousarray(np.asarray(x, dtype="<f8"))
    return hashlib.sha256(data.tobytes(order="C")).hexdigest()


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_records(repository: Path) -> dict[int, tuple[np.ndarray, str, str]]:
    result_path = (
        repository
        / "experiments/four_point_depth_projection/"
        "construction_active_search/rigidity_softmode_results.json"
    )
    if result_path.exists():
        payload = json.loads(result_path.read_text())
        answer = {}
        for run in payload["runs"]:
            n = int(run["n"])
            answer[n] = (
                unit_rows(run["best"]["coordinates_float64"]),
                (
                    f"{result_path.relative_to(repository)}"
                    f"#/runs/{n - 41}/best"
                ),
                source_hash(result_path),
            )
        if set(answer) == {41, 42, 43, 44}:
            return answer
    raise FileNotFoundError(
        "the completed active-search record is required as a warm start"
    )


def active_edges(x: np.ndarray, tolerance: float = 1e-8) -> np.ndarray:
    gram = x @ x.T
    np.fill_diagonal(gram, -np.inf)
    top = float(np.max(gram))
    return np.argwhere(np.triu(gram >= top - tolerance, k=1))


def edge_set(edges: np.ndarray) -> set[tuple[int, int]]:
    return {(int(first), int(second)) for first, second in edges}


def graph_jaccard(x: np.ndarray, inherited_edges: np.ndarray) -> float:
    first = edge_set(active_edges(x, 1e-5))
    second = edge_set(inherited_edges)
    union = first | second
    return float(len(first & second) / len(union)) if union else 1.0


def threshold_energy_gradient(
    x: np.ndarray,
    inherited_mask: np.ndarray,
    inherited_maximum: float,
    bias: float,
    bias_drop: float,
) -> tuple[float, float, np.ndarray]:
    """Literal half-threshold hinge plus a temporary old-edge history bias."""
    gram = x @ x.T
    excess = np.maximum(gram - TARGET, 0.0)
    np.fill_diagonal(excess, 0.0)
    base_energy = 0.5 * float(np.sum(excess * excess))
    gradient = 2.0 * excess @ x

    bias_energy = 0.0
    if bias > 0.0:
        inherited_excess = (
            np.maximum(
                gram - (inherited_maximum - bias_drop),
                0.0,
            )
            * inherited_mask
        )
        bias_energy = 0.5 * float(
            np.sum(inherited_excess * inherited_excess)
        )
        gradient += 2.0 * bias * inherited_excess @ x

    gradient -= np.sum(gradient * x, axis=1)[:, None] * x
    return base_energy, bias_energy, gradient


def threshold_energy(x: np.ndarray) -> float:
    values = pair_values(unit_rows(x))
    excess = np.maximum(values - TARGET, 0.0)
    return float(excess @ excess)


def coherent_noise(
    x: np.ndarray,
    rng: np.random.Generator,
    step: int,
) -> np.ndarray:
    noise = rng.normal(size=x.shape)
    if step % 23 == 0:
        seed_vertex = int(rng.integers(len(x)))
        products = x @ x[seed_vertex]
        count = min(len(x), 3 + (step // 23) % 10)
        neighborhood = np.argpartition(products, -count)[-count:]
        common = rng.normal(size=DIMENSION)
        noise[neighborhood] += 1.8 * common
    noise -= np.sum(noise * x, axis=1)[:, None] * x
    return noise


def basin_fingerprint(x: np.ndarray) -> str:
    values = np.sort(pair_values(unit_rows(x)))
    quantized = np.rint(values * 1e7).astype("<i8")
    return hashlib.sha256(quantized.tobytes()).hexdigest()


def epigraph_refine(
    initial_points: np.ndarray, max_iterations: int
) -> tuple[np.ndarray, dict]:
    x = unit_rows(initial_points)
    n = len(x)
    all_i, all_j = pair_indices(n)
    constraint_limit = min(240, len(all_i))
    outer_records = []
    previous_active = None
    total_iterations = 0
    last_result = None
    # SLSQP's dense QP workspace grows quickly with all roughly 900 pair
    # constraints.  Constraint generation keeps the 240 currently largest
    # pairs, then performs a literal all-pair scan and replaces the working
    # set.  Thus no omitted violating pair is trusted.
    for outer in range(8):
        values = np.sum(x[all_i] * x[all_j], axis=1)
        active = np.argsort(values)[-constraint_limit:]
        active = np.sort(active)
        ii = all_i[active]
        jj = all_j[active]
        initial = np.r_[x.ravel(), float(np.max(values))]

        def objective(variable: np.ndarray) -> float:
            return float(variable[-1])

        def objective_jac(variable: np.ndarray) -> np.ndarray:
            answer = np.zeros_like(variable)
            answer[-1] = 1.0
            return answer

        def inequalities(variable: np.ndarray) -> np.ndarray:
            points = variable[:-1].reshape(n, DIMENSION)
            return variable[-1] - np.sum(
                points[ii] * points[jj], axis=1
            )

        def inequalities_jac(variable: np.ndarray) -> np.ndarray:
            points = variable[:-1].reshape(n, DIMENSION)
            answer = np.zeros((len(ii), len(variable)))
            rows = np.arange(len(ii))
            for coordinate in range(DIMENSION):
                answer[rows, DIMENSION * ii + coordinate] = -points[
                    jj, coordinate
                ]
                answer[rows, DIMENSION * jj + coordinate] = -points[
                    ii, coordinate
                ]
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
                "maxiter": max(80, max_iterations // 8),
                "ftol": 2e-13,
                "disp": False,
            },
        )
        x = unit_rows(result.x[:-1].reshape(n, DIMENSION))
        total_iterations += int(result.nit)
        rescanned = maximum(x)
        next_values = np.sum(x[all_i] * x[all_j], axis=1)
        next_active = np.sort(
            np.argsort(next_values)[-constraint_limit:]
        )
        stable = previous_active is not None and np.array_equal(
            active, next_active
        )
        outer_records.append(
            {
                "outer_iteration": int(outer),
                "working_constraint_count": int(len(active)),
                "solver_success": bool(result.success),
                "solver_status": int(result.status),
                "solver_message": str(result.message),
                "solver_iterations": int(result.nit),
                "reported_epigraph": float(result.x[-1]),
                "all_pair_rescanned_maximum": float(rescanned),
                "working_set_stable": bool(stable),
            }
        )
        last_result = result
        if stable and rescanned <= float(result.x[-1]) + 2e-10:
            break
        previous_active = active
    answer = unit_rows(x)
    return answer, {
        "success": bool(
            last_result is not None
            and last_result.success
            and maximum(answer) <= float(last_result.x[-1]) + 2e-9
        ),
        "status": int(last_result.status),
        "message": str(last_result.message),
        "iterations": int(total_iterations),
        "reported_epigraph": float(last_result.x[-1]),
        "recomputed_maximum": maximum(answer),
        "constraint_generation": outer_records,
    }


def diagnostics(x: np.ndarray) -> dict:
    x = unit_rows(x)
    gram = x @ x.T
    ii, jj = pair_indices(len(x))
    values = gram[ii, jj]
    maximum_index = int(np.argmax(values))
    top = float(values[maximum_index])
    spectrum = np.linalg.eigvalsh(x.T @ x)
    result = {
        "n": int(len(x)),
        "maximum_inner_product": top,
        "maximizing_pair": [
            int(ii[maximum_index]),
            int(jj[maximum_index]),
        ],
        "threshold_energy": threshold_energy(x),
        "pairs_above_one_half": int(np.sum(values > TARGET)),
        "maximum_row_norm_error": float(
            np.max(np.abs(np.sum(x * x, axis=1) - 1.0))
        ),
        "coordinate_little_endian_float64_sha256": coordinate_hash(x),
        "frame_spectrum": [float(value) for value in spectrum],
    }
    for tolerance in (1e-8, 1e-6, 1e-4):
        edges = np.argwhere(
            np.triu(gram >= top - tolerance, k=1)
        )
        degrees = np.bincount(edges.ravel(), minlength=len(x))
        result[f"active_{tolerance:.0e}"] = {
            "edge_count": int(len(edges)),
            "minimum_degree": int(np.min(degrees)),
            "maximum_degree": int(np.max(degrees)),
            "zero_degree_count": int(np.sum(degrees == 0)),
        }
    return result


def select_archive(
    archive: list[dict], candidate_count: int
) -> list[dict]:
    chosen: list[dict] = []
    seen = set()
    orderings = (
        sorted(archive, key=lambda row: row["threshold_energy"]),
        sorted(archive, key=lambda row: row["maximum"]),
        sorted(archive, key=lambda row: row["old_graph_jaccard"]),
    )
    cursor = [0, 0, 0]
    while len(chosen) < candidate_count:
        progress = False
        for ordering_index, ordering in enumerate(orderings):
            while cursor[ordering_index] < len(ordering):
                row = ordering[cursor[ordering_index]]
                cursor[ordering_index] += 1
                fingerprint = row["fingerprint"]
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                chosen.append(row)
                progress = True
                break
            if len(chosen) >= candidate_count:
                break
        if not progress:
            break
    return chosen


def run_trajectory(
    x0: np.ndarray,
    origin: str,
    origin_hash: str,
    n: int,
    seed: int,
    regime: str,
    population_size: int,
    polish_count: int,
    max_iterations: int,
) -> dict:
    rng = np.random.default_rng(seed)
    x0 = unit_rows(x0)
    inherited_maximum = maximum(x0)
    inherited_edges = active_edges(x0, 1e-5)
    inherited_mask = np.zeros((n, n))
    inherited_mask[inherited_edges[:, 0], inherited_edges[:, 1]] = 1.0
    inherited_mask += inherited_mask.T
    schedule = MILD_SCHEDULE if regime == "mild" else STRONG_SCHEDULE
    bias_drop = 0.025 if regime == "mild" else 0.040

    initial_scales = (
        np.linspace(0.01, 0.12, population_size - 1)
        if regime == "mild"
        else np.linspace(0.04, 0.30, population_size - 1)
    )
    population = [x0.copy()]
    for scale in initial_scales:
        noise = rng.normal(size=x0.shape)
        noise -= np.sum(noise * x0, axis=1)[:, None] * x0
        population.append(unit_rows(x0 + scale * noise))

    archive: list[dict] = []
    stages = []
    for stage_index, (bias, temperature, step_size, steps) in enumerate(
        schedule
    ):
        noise_scale = math.sqrt(2.0 * step_size * temperature)
        for walker_index in range(population_size):
            x = population[walker_index]
            for step in range(steps):
                _, _, gradient = threshold_energy_gradient(
                    x,
                    inherited_mask,
                    inherited_maximum,
                    bias,
                    bias_drop,
                )
                noise = coherent_noise(x, rng, step)
                x = unit_rows(
                    x - step_size * gradient + noise_scale * noise
                )
            population[walker_index] = x

        rows = []
        for walker_index, x in enumerate(population):
            row = {
                "stage": int(stage_index),
                "walker": int(walker_index),
                "threshold_energy": threshold_energy(x),
                "maximum": maximum(x),
                "old_graph_jaccard": graph_jaccard(
                    x, inherited_edges
                ),
                "fingerprint": basin_fingerprint(x),
                "coordinates": x.copy(),
            }
            archive.append(row)
            rows.append(row)

        energy_order = sorted(
            range(population_size),
            key=lambda index: rows[index]["threshold_energy"],
        )
        diversity_order = sorted(
            range(population_size),
            key=lambda index: rows[index]["old_graph_jaccard"],
        )
        retained_indices = list(
            dict.fromkeys(
                energy_order[: max(4, population_size // 2)]
                + diversity_order[: max(3, population_size // 3)]
            )
        )
        parents = [population[index].copy() for index in retained_indices]
        next_population = [parent.copy() for parent in parents]
        while len(next_population) < population_size:
            parent = parents[int(rng.integers(len(parents)))]
            noise = coherent_noise(parent, rng, len(next_population))
            next_population.append(
                unit_rows(parent + 0.25 * noise_scale * noise)
            )
        population = next_population[:population_size]
        stages.append(
            {
                "stage": int(stage_index),
                "bias": float(bias),
                "temperature": float(temperature),
                "step_size": float(step_size),
                "noise_scale": float(noise_scale),
                "langevin_steps": int(steps),
                "best_threshold_energy": float(
                    min(row["threshold_energy"] for row in rows)
                ),
                "best_maximum": float(
                    min(row["maximum"] for row in rows)
                ),
                "minimum_old_graph_jaccard": float(
                    min(row["old_graph_jaccard"] for row in rows)
                ),
                "distinct_fingerprint_count": int(
                    len({row["fingerprint"] for row in rows})
                ),
            }
        )
        print(
            f"N={n} seed={seed} {regime} stage={stage_index} "
            f"E={stages[-1]['best_threshold_energy']:.8g} "
            f"max={stages[-1]['best_maximum']:.12g} "
            f"J={stages[-1]['minimum_old_graph_jaccard']:.4g}",
            flush=True,
        )

    selected = select_archive(archive, polish_count)
    polished_records = []
    best = x0.copy()
    best_value = inherited_maximum
    for candidate_index, row in enumerate(selected):
        refined, solver = epigraph_refine(
            row["coordinates"], max_iterations=max_iterations
        )
        value = maximum(refined)
        record = {
            "candidate_index": int(candidate_index),
            "archive_stage": int(row["stage"]),
            "archive_walker": int(row["walker"]),
            "archive_threshold_energy": float(row["threshold_energy"]),
            "archive_maximum": float(row["maximum"]),
            "archive_old_graph_jaccard": float(
                row["old_graph_jaccard"]
            ),
            "archive_fingerprint": row["fingerprint"],
            "solver": solver,
            "diagnostics": diagnostics(refined),
            "coordinates_float64": unit_rows(refined).tolist(),
        }
        polished_records.append(record)
        print(
            f"N={n} seed={seed} {regime} polish={candidate_index} "
            f"max={value:.17g}",
            flush=True,
        )
        if value < best_value:
            best = refined.copy()
            best_value = value

    return {
        "n": int(n),
        "seed": int(seed),
        "regime": regime,
        "origin": origin,
        "origin_sha256": origin_hash,
        "baseline": {
            "diagnostics": diagnostics(x0),
            # diagnostics() normalizes its input once; store that exact
            # normalization so its binary64 hash describes these rows.
            "coordinates_float64": unit_rows(x0).tolist(),
        },
        "population_size": int(population_size),
        "bias_drop": float(bias_drop),
        "schedule": [
            {
                "bias": float(bias),
                "temperature": float(temperature),
                "step_size": float(step_size),
                "langevin_steps": int(steps),
            }
            for bias, temperature, step_size, steps in schedule
        ],
        "stage_records": stages,
        "archive_state_count": int(len(archive)),
        "polished_candidates": polished_records,
        "best": {
            "diagnostics": diagnostics(best),
            "coordinates_float64": unit_rows(best).tolist(),
        },
        "beat_baseline": bool(best_value < inherited_maximum - 1e-13),
        "reached_half": bool(best_value <= TARGET),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n",
        type=int,
        nargs="+",
        default=[41, 42, 43, 44],
    )
    parser.add_argument(
        "--regimes",
        nargs="+",
        choices=("mild", "strong"),
        default=["mild", "strong"],
    )
    parser.add_argument("--population-size", type=int, default=12)
    parser.add_argument("--polish-count", type=int, default=10)
    parser.add_argument("--max-iterations", type=int, default=2500)
    parser.add_argument("--seed-base", type=int, default=2026075100)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("thermal_portfolio.json"),
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if any(n not in (41, 42, 43, 44) for n in arguments.n):
        raise ValueError("N must be in 41..44")
    repository = Path(__file__).resolve().parents[3]
    records = load_records(repository)
    started = time.time()
    output = {
        "status": STATUS,
        "method": (
            "history-biased Riemannian Langevin population annealing "
            "with diversity resampling and all-pair constraint-generation "
            "epigraph quench"
        ),
        "target": TARGET,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "parameters": {
            "n": [int(n) for n in arguments.n],
            "regimes": list(arguments.regimes),
            "population_size": int(arguments.population_size),
            "polish_count": int(arguments.polish_count),
            "max_iterations": int(arguments.max_iterations),
            "seed_base": int(arguments.seed_base),
        },
        "runs": [],
    }
    for n in arguments.n:
        x0, origin, origin_hash = records[n]
        for regime_index, regime in enumerate(arguments.regimes):
            seed = (
                arguments.seed_base
                + 100 * (n - 41)
                + regime_index
            )
            output["runs"].append(
                run_trajectory(
                    x0,
                    origin,
                    origin_hash,
                    n,
                    seed,
                    regime,
                    arguments.population_size,
                    arguments.polish_count,
                    arguments.max_iterations,
                )
            )
            arguments.output.parent.mkdir(parents=True, exist_ok=True)
            arguments.output.write_text(
                json.dumps(output, indent=2, sort_keys=True) + "\n"
            )
    output["elapsed_seconds"] = float(time.time() - started)
    output["best_by_n"] = {}
    for n in arguments.n:
        runs = [run for run in output["runs"] if run["n"] == n]
        best_run = min(
            runs,
            key=lambda run: run["best"]["diagnostics"][
                "maximum_inner_product"
            ],
        )
        output["best_by_n"][str(n)] = {
            "seed": best_run["seed"],
            "regime": best_run["regime"],
            "diagnostics": best_run["best"]["diagnostics"],
            "coordinates_float64": best_run["best"][
                "coordinates_float64"
            ],
        }
    output["binary64_threshold_hit"] = bool(
        any(run["reached_half"] for run in output["runs"])
    )
    arguments.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    for n, record in output["best_by_n"].items():
        print(
            f"FINAL N={n} "
            f"max={record['diagnostics']['maximum_inner_product']:.17g}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

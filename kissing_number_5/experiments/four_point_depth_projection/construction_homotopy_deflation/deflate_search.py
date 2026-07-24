#!/usr/bin/env python3
"""Rank-five factor search with edge-slack homotopy and active deflation.

This is numerical construction discovery, not a proof.  The state is an
explicit N by 5 factor whose rows stay on the unit sphere.  At every epoch the
program alternates between:

* updating one slack, dual penalty, and IRLS weight for every unordered edge;
* moving the factor by a tangent-space weighted-gradient step; and
* at scheduled epochs, deleting a seeded block of dominant edge constraints
  and later reintroducing them with a decaying penalty boost.

The escaped factors are finally polished against all pair constraints by a
direct epigraph SLSQP solve.  Unlike the earlier alternating-Gram experiment,
no N by N matrix is spectrally projected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import scipy
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEFAULT_OUTPUT = HERE / "deflate_results.json"
STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DIMENSION = 5
THRESHOLD = 0.5


def unit_rows(value: Any) -> np.ndarray:
    points = np.asarray(value, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != DIMENSION:
        raise ValueError("coordinates must be an N by 5 array")
    norms = np.linalg.norm(points, axis=1)
    if np.any(norms < 1e-14):
        raise ValueError("zero or nearly zero coordinate row")
    return np.ascontiguousarray(points / norms[:, None])


def pair_indices(n: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(n, 1)


def pair_values(points: np.ndarray) -> np.ndarray:
    first, second = pair_indices(len(points))
    return np.sum(points[first] * points[second], axis=1)


def maximum_inner_product(points: np.ndarray) -> float:
    return float(np.max(pair_values(unit_rows(points))))


def coordinate_hash(points: np.ndarray) -> str:
    little = np.asarray(points, dtype="<f8", order="C")
    return hashlib.sha256(little.tobytes(order="C")).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def components(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adjacency = [[] for _ in range(n)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    unseen = set(range(n))
    sizes = []
    while unseen:
        root = unseen.pop()
        stack = [root]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def diagnostics(points: np.ndarray) -> dict[str, Any]:
    points = unit_rows(points)
    n = len(points)
    gram = points @ points.T
    first, second = pair_indices(n)
    values = gram[first, second]
    maximum = float(np.max(values))
    maximizing = np.flatnonzero(values == maximum)
    spectrum = np.linalg.eigvalsh(gram)
    active_indices = np.flatnonzero(values >= maximum - 1e-8)
    active_edges = [
        (int(first[index]), int(second[index])) for index in active_indices
    ]
    degrees = np.zeros(n, dtype=np.int64)
    for edge_first, edge_second in active_edges:
        degrees[edge_first] += 1
        degrees[edge_second] += 1
    degree_values, degree_counts = np.unique(degrees, return_counts=True)
    return {
        "n": n,
        "dimension": DIMENSION,
        "coordinate_little_endian_float64_sha256": coordinate_hash(points),
        "maximum_inner_product": maximum,
        "maximum_inner_product_hex": maximum.hex(),
        "gap_above_one_half": maximum - THRESHOLD,
        "minimum_inner_product": float(np.min(values)),
        "maximizing_pairs_binary64": [
            [int(first[index]), int(second[index])] for index in maximizing
        ],
        "pairs_above_one_half": int(np.count_nonzero(values > THRESHOLD)),
        "maximum_row_norm_squared_error": float(
            np.max(np.abs(np.sum(points * points, axis=1) - 1.0))
        ),
        "gram_eigenvalues_ascending": [
            float(value) for value in spectrum
        ],
        "gram_null_spectrum_maximum_absolute": float(
            np.max(np.abs(spectrum[:-5]))
        ),
        "gram_positive_eigenvalues_ascending": [
            float(value) for value in spectrum[-5:]
        ],
        "numerical_rank_at_1e-10": int(
            np.count_nonzero(spectrum > 1e-10)
        ),
        "active_1e-8": {
            "edge_count": len(active_edges),
            "component_sizes": components(n, active_edges),
            "degree_histogram": {
                str(int(degree)): int(count)
                for degree, count in zip(
                    degree_values, degree_counts, strict=True
                )
            },
        },
    }


def load_current_record(n: int) -> tuple[np.ndarray, dict[str, Any]]:
    candidates: list[tuple[np.ndarray, dict[str, Any]]] = []

    rigidity_path = (
        REPO
        / "experiments/four_point_depth_projection/construction_active_search/"
        "rigidity_softmode_results.json"
    )
    rigidity = json.loads(rigidity_path.read_text())
    rigidity_run_index = n - 41
    rigidity_points = unit_rows(
        rigidity["runs"][rigidity_run_index]["best"]["coordinates_float64"]
    )
    candidates.append(
        (
            rigidity_points,
            {
                "source_file": str(rigidity_path.relative_to(REPO)),
                "source_file_sha256": file_hash(rigidity_path),
                "source_locator": f"$.runs[{rigidity_run_index}].best",
            },
        )
    )

    surgery_path = (
        REPO
        / "experiments/four_point_depth_projection/construction_active_search/"
        "surgery_best_configurations.json"
    )
    surgery = json.loads(surgery_path.read_text())
    surgery_points = unit_rows(
        surgery["best_configurations"][str(n)]["diagnostics"][
            "coordinates_float64"
        ]
    )
    candidates.append(
        (
            surgery_points,
            {
                "source_file": str(surgery_path.relative_to(REPO)),
                "source_file_sha256": file_hash(surgery_path),
                "source_locator": (
                    f"$.best_configurations['{n}'].diagnostics"
                ),
            },
        )
    )

    points, source = min(
        candidates, key=lambda item: maximum_inner_product(item[0])
    )
    source = {
        **source,
        "coordinate_little_endian_float64_sha256": coordinate_hash(points),
        "maximum_inner_product": maximum_inner_product(points),
        "candidate_count": len(candidates),
    }
    return points, source


def tangent_perturb(
    points: np.ndarray,
    rng: np.random.Generator,
    scale: float,
) -> np.ndarray:
    if scale <= 0:
        return points.copy()
    noise = rng.normal(size=points.shape)
    noise -= np.sum(noise * points, axis=1)[:, None] * points
    row_sizes = np.linalg.norm(noise, axis=1)
    noise /= np.maximum(row_sizes[:, None], 1e-15)
    amplitudes = scale * rng.uniform(0.35, 1.0, size=len(points))
    return unit_rows(points + amplitudes[:, None] * noise)


def epigraph_refine(
    initial: np.ndarray, max_iterations: int
) -> tuple[np.ndarray, dict[str, Any]]:
    """Polish one escaped factor using all norm and pair constraints."""
    points = unit_rows(initial)
    n = len(points)
    first, second = pair_indices(n)
    pair_count = len(first)
    initial_variable = np.r_[
        points.ravel(), maximum_inner_product(points)
    ]

    def objective(variable: np.ndarray) -> float:
        return float(variable[-1])

    def objective_jacobian(variable: np.ndarray) -> np.ndarray:
        answer = np.zeros_like(variable)
        answer[-1] = 1.0
        return answer

    def inequalities(variable: np.ndarray) -> np.ndarray:
        factor = variable[:-1].reshape(n, DIMENSION)
        return variable[-1] - np.sum(
            factor[first] * factor[second], axis=1
        )

    def inequalities_jacobian(variable: np.ndarray) -> np.ndarray:
        factor = variable[:-1].reshape(n, DIMENSION)
        answer = np.zeros((pair_count, len(variable)))
        rows = np.arange(pair_count)
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * first + coordinate] = -factor[
                second, coordinate
            ]
            answer[rows, DIMENSION * second + coordinate] = -factor[
                first, coordinate
            ]
        answer[:, -1] = 1.0
        return answer

    def equalities(variable: np.ndarray) -> np.ndarray:
        factor = variable[:-1].reshape(n, DIMENSION)
        return np.sum(factor * factor, axis=1) - 1.0

    def equalities_jacobian(variable: np.ndarray) -> np.ndarray:
        factor = variable[:-1].reshape(n, DIMENSION)
        answer = np.zeros((n, len(variable)))
        rows = np.arange(n)
        for coordinate in range(DIMENSION):
            answer[rows, DIMENSION * rows + coordinate] = (
                2.0 * factor[:, coordinate]
            )
        return answer

    result = minimize(
        objective,
        initial_variable,
        jac=objective_jacobian,
        constraints=[
            {
                "type": "ineq",
                "fun": inequalities,
                "jac": inequalities_jacobian,
            },
            {
                "type": "eq",
                "fun": equalities,
                "jac": equalities_jacobian,
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


def aggregate(values: np.ndarray) -> dict[str, float]:
    return {
        "minimum": float(np.min(values)),
        "maximum": float(np.max(values)),
        "mean": float(np.mean(values)),
        "l2": float(np.linalg.norm(values)),
    }


def factor_homotopy(
    initial: np.ndarray,
    rng: np.random.Generator,
    epochs: int,
    warm_start: bool,
    restart: int,
    checkpoint_period: int,
) -> tuple[np.ndarray, np.ndarray, list[np.ndarray], dict[str, Any]]:
    """Run the factor/slack/weight alternation with three deflation windows."""
    points = unit_rows(initial)
    n = len(points)
    first, second = pair_indices(n)
    edge_count = len(first)
    initial_maximum = maximum_inner_product(points)
    best = points.copy()
    best_maximum = initial_maximum
    best_epoch = 0

    dual = np.zeros(edge_count)
    mask = np.ones(edge_count)
    reentry_boost = np.ones(edge_count)
    momentum = np.zeros_like(points)
    checkpoints: list[dict[str, Any]] = []
    deflation_events: list[dict[str, Any]] = []
    snapshots: list[np.ndarray] = []

    event_starts = [
        max(1, int(epochs * fraction)) for fraction in (0.23, 0.48, 0.73)
    ]
    deflation_span = max(20, int(epochs * 0.045))
    event_ends = [start + deflation_span for start in event_starts]
    drop_count = max(8, n // 3)
    active_event: dict[int, np.ndarray] = {}

    last_slack = np.zeros(edge_count)
    last_residual = np.zeros(edge_count)
    last_weights = np.ones(edge_count)
    for epoch in range(epochs):
        dots = np.sum(points[first] * points[second], axis=1)
        progress = min(epoch / max(1, int(epochs * 0.82)), 1.0)
        target = THRESHOLD + 0.80 * (
            initial_maximum - THRESHOLD
        ) * (1.0 - progress) ** 2

        slack = np.maximum(target - dots, 0.0)
        residual = dots - target + slack
        dual = 0.997 * dual + 0.40 * residual
        residual_scale = max(float(np.max(residual)), 1e-15)
        p_value = 3.0 + 11.0 * progress
        irls = (residual / residual_scale) ** (p_value - 2.0)
        dual_scale = max(float(np.max(dual)), 1e-15)
        weights = (
            0.02 + irls + dual / dual_scale
        ) * mask * reentry_boost

        penalty_coefficients = weights * residual
        penalty_sum = float(np.sum(penalty_coefficients))
        if penalty_sum > 0:
            penalty_coefficients /= penalty_sum

        temperature = 70.0 + 150.0 * progress
        shifted = np.maximum(
            temperature * (dots - float(np.max(dots))), -700.0
        )
        guard = np.exp(shifted) * mask
        guard_sum = float(np.sum(guard))
        if guard_sum > 0:
            guard /= guard_sum
        coefficients = penalty_coefficients + 0.40 * guard
        coefficient_sum = float(np.sum(coefficients))
        if coefficient_sum > 0:
            coefficients /= coefficient_sum

        gradient = np.zeros_like(points)
        np.add.at(
            gradient,
            first,
            coefficients[:, None] * points[second],
        )
        np.add.at(
            gradient,
            second,
            coefficients[:, None] * points[first],
        )
        gradient -= (
            np.sum(gradient * points, axis=1)[:, None] * points
        )
        momentum = 0.90 * momentum + 0.10 * gradient
        initial_rate = 0.006 if warm_start else 0.012
        learning_rate = (
            initial_rate * max(0.08, 1.0 - epoch / (epochs * 1.10))
        )
        points = unit_rows(points - learning_rate * momentum)

        if epoch in event_starts:
            event_number = event_starts.index(epoch)
            pool_count = min(edge_count, 5 * drop_count)
            score = dots + 0.05 * (
                dual / max(float(np.max(dual)), 1e-15)
            )
            pool = np.argpartition(score, -pool_count)[-pool_count:]
            selected = np.sort(
                rng.choice(pool, size=drop_count, replace=False)
            )
            mask[selected] = 0.0
            active_event[event_number] = selected
            kick_scale = (
                (0.0025 if warm_start else 0.004)
                * (1.0 + 0.35 * event_number)
                * (1.0 + 0.10 * (restart % 4))
            )
            points = tangent_perturb(points, rng, kick_scale)
            deflation_events.append(
                {
                    "event": event_number,
                    "delete_epoch": epoch,
                    "reentry_epoch": event_ends[event_number],
                    "deleted_edge_count": len(selected),
                    "deleted_edges": [
                        [int(first[index]), int(second[index])]
                        for index in selected
                    ],
                    "tangent_kick_scale": kick_scale,
                    "maximum_before_delete": float(np.max(dots)),
                }
            )

        if epoch in event_ends:
            event_number = event_ends.index(epoch)
            selected = active_event[event_number]
            mask[selected] = 1.0
            reentry_boost[selected] = 10.0
            snapshots.append(points.copy())
            deflation_events[event_number][
                "maximum_at_reentry"
            ] = maximum_inner_product(points)
        reentry_boost = 1.0 + 0.994 * (reentry_boost - 1.0)

        current_maximum = maximum_inner_product(points)
        if current_maximum < best_maximum:
            best = points.copy()
            best_maximum = current_maximum
            best_epoch = epoch + 1
        if current_maximum <= THRESHOLD:
            break

        if checkpoint_period and (
            (epoch + 1) % checkpoint_period == 0 or epoch == 0
        ):
            checkpoints.append(
                {
                    "epoch": epoch + 1,
                    "target": target,
                    "maximum_inner_product": current_maximum,
                    "best_maximum_inner_product": best_maximum,
                    "masked_edge_count": int(np.count_nonzero(mask == 0.0)),
                    "slack": aggregate(slack),
                    "positive_residual_count": int(
                        np.count_nonzero(residual > 0.0)
                    ),
                    "residual": aggregate(residual),
                    "dual": aggregate(dual),
                    "effective_weight": aggregate(weights),
                }
            )
        last_slack = slack.copy()
        last_residual = residual.copy()
        last_weights = weights.copy()

    terminal = unit_rows(points)
    final_dots = np.sum(terminal[first] * terminal[second], axis=1)
    final_slack = np.maximum(THRESHOLD - final_dots, 0.0)
    final_residual = final_dots - THRESHOLD + final_slack
    return best, terminal, snapshots, {
        "epochs_requested": epochs,
        "epochs_completed": epoch + 1,
        "best_epoch": best_epoch,
        "initial_maximum_inner_product": initial_maximum,
        "best_path_maximum_inner_product": best_maximum,
        "terminal_maximum_inner_product": maximum_inner_product(terminal),
        "checkpoint_period": checkpoint_period,
        "checkpoints": checkpoints,
        "deflation_events": deflation_events,
        "edge_order": "lexicographic upper triangle (0,1),(0,2),...",
        "final_edge_state": {
            "slack_at_one_half": [float(value) for value in final_slack],
            "residual_at_one_half": [
                float(value) for value in final_residual
            ],
            "dual_penalty": [float(value) for value in dual],
            "last_homotopy_slack": [
                float(value) for value in last_slack
            ],
            "last_homotopy_residual": [
                float(value) for value in last_residual
            ],
            "last_effective_weight": [
                float(value) for value in last_weights
            ],
        },
    }


def make_initial(
    warm: np.ndarray,
    rng: np.random.Generator,
    restart: int,
    warm_restarts: int,
) -> tuple[np.ndarray, str, float | None]:
    if restart < warm_restarts:
        amplitudes = (0.0, 0.008, 0.025, 0.065, 0.12, 0.20)
        amplitude = amplitudes[restart % len(amplitudes)]
        return tangent_perturb(warm, rng, amplitude), "warm_perturbed", amplitude
    points = rng.normal(size=warm.shape)
    return unit_rows(points), "fresh_asymmetric_gaussian", None


def choose_better(
    points: np.ndarray, current: np.ndarray
) -> bool:
    return (
        maximum_inner_product(points)
        < maximum_inner_product(current) - 1e-13
    )


def run_one(
    n: int,
    warm: np.ndarray,
    source: dict[str, Any],
    restart: int,
    seed: int,
    warm_restarts: int,
    epochs: int,
    checkpoint_period: int,
    polish_iterations: int,
) -> tuple[dict[str, Any], np.ndarray]:
    rng = np.random.default_rng(seed)
    initial, origin, perturbation = make_initial(
        warm, rng, restart, warm_restarts
    )
    path_best, terminal, snapshots, homotopy = factor_homotopy(
        initial,
        rng,
        epochs=epochs,
        warm_start=origin == "warm_perturbed",
        restart=restart,
        checkpoint_period=checkpoint_period,
    )

    polish_inputs = [terminal]
    if snapshots:
        polish_inputs.append(snapshots[len(snapshots) // 2])
    polished_records = []
    candidates = [initial, path_best, terminal]
    for index, polish_input in enumerate(polish_inputs):
        polished, solver = epigraph_refine(
            polish_input, max_iterations=polish_iterations
        )
        candidates.append(polished)
        polished_records.append(
            {
                "input": "terminal" if index == 0 else "middle_reentry",
                "input_maximum_inner_product": maximum_inner_product(
                    polish_input
                ),
                "solver": solver,
                "diagnostics": diagnostics(polished),
            }
        )
    best = min(candidates, key=maximum_inner_product)
    record = {
        "n": n,
        "restart": restart,
        "seed": seed,
        "origin": origin,
        "warm_source": source,
        "initial_tangent_perturbation": perturbation,
        "initial_diagnostics": diagnostics(initial),
        "homotopy": homotopy,
        "polished_candidates": polished_records,
        "best_diagnostics": diagnostics(best),
        "best_coordinates_float64": unit_rows(best).tolist(),
        "beats_warm_record": (
            maximum_inner_product(best)
            < source["maximum_inner_product"] - 1e-13
        ),
        "reaches_one_half_binary64": (
            maximum_inner_product(best) <= THRESHOLD
        ),
    }
    return record, best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, nargs="+", default=[41, 42, 43, 44])
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--warm-restarts", type=int, default=4)
    parser.add_argument("--epochs", type=int, default=12000)
    parser.add_argument("--checkpoint-period", type=int, default=1000)
    parser.add_argument("--polish-iterations", type=int, default=1500)
    parser.add_argument("--seed-base", type=int, default=2026072700)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()
    if not 0 <= arguments.warm_restarts <= arguments.restarts:
        parser.error("warm-restarts must lie between zero and restarts")

    started = time.time()
    result: dict[str, Any] = {
        "schema": "kissing5-factor-slack-deflation-v1",
        "status": STATUS,
        "method": (
            "rank-five factor homotopy with explicit edge slacks, dual/IRLS "
            "penalties, seeded active-edge deletion and re-entry, then "
            "all-edge epigraph polishing"
        ),
        "dimension": DIMENSION,
        "threshold": THRESHOLD,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
            "byteorder": sys.byteorder,
        },
        "parameters": {
            "n": arguments.n,
            "restarts": arguments.restarts,
            "warm_restarts": arguments.warm_restarts,
            "fresh_asymmetric_restarts": (
                arguments.restarts - arguments.warm_restarts
            ),
            "epochs": arguments.epochs,
            "checkpoint_period": arguments.checkpoint_period,
            "polish_iterations": arguments.polish_iterations,
            "seed_base": arguments.seed_base,
            "seed_formula": "seed_base + 100*(N-41) + restart",
        },
        "runs": [],
        "best_by_n": {},
    }

    any_threshold = False
    for n in arguments.n:
        warm, source = load_current_record(n)
        overall_best = warm.copy()
        winning_restart: int | None = None
        print(
            f"N={n} warm={maximum_inner_product(warm):.17g} "
            f"source={source['source_file']}",
            flush=True,
        )
        for restart in range(arguments.restarts):
            seed = (
                arguments.seed_base + 100 * (n - 41) + restart
            )
            record, candidate = run_one(
                n,
                warm,
                source,
                restart=restart,
                seed=seed,
                warm_restarts=arguments.warm_restarts,
                epochs=arguments.epochs,
                checkpoint_period=arguments.checkpoint_period,
                polish_iterations=arguments.polish_iterations,
            )
            result["runs"].append(record)
            candidate_maximum = maximum_inner_product(candidate)
            print(
                f"  restart={restart} seed={seed} origin={record['origin']} "
                f"best={candidate_maximum:.17g}",
                flush=True,
            )
            if choose_better(candidate, overall_best):
                overall_best = candidate.copy()
                winning_restart = restart
                print(
                    f"  RECORD N={n} restart={restart} "
                    f"max={candidate_maximum:.17g}",
                    flush=True,
                )
            if candidate_maximum <= THRESHOLD:
                any_threshold = True
                break

        result["best_by_n"][str(n)] = {
            "warm_source": source,
            "winning_restart": winning_restart,
            "strictly_beats_warm_record": (
                maximum_inner_product(overall_best)
                < source["maximum_inner_product"] - 1e-13
            ),
            "reaches_one_half_binary64": (
                maximum_inner_product(overall_best) <= THRESHOLD
            ),
            "diagnostics": diagnostics(overall_best),
            "coordinates_float64": unit_rows(overall_best).tolist(),
        }
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        result["elapsed_seconds"] = time.time() - started
        result["any_threshold_candidate_found"] = any_threshold
        arguments.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n"
        )

    result["elapsed_seconds"] = time.time() - started
    result["any_threshold_candidate_found"] = any_threshold
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(f"wrote {arguments.output}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

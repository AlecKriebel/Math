#!/usr/bin/env python3
"""X=12-profile and unrestricted construction challenge for N=41,...,44.

This is numerical discovery code.  It combines a smooth maximum-inner-
product objective with optional soft edge-histogram and row-energy-profile
penalties.  Guided runs remove every profile penalty in their final phases.
Separate unrestricted replicas provide a qualitatively different control.

The population uses asymmetric random starts, replica exchange, and an
explicit delete/reinsert topology-changing seed.  Nothing in a failed run
is an upper-bound certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "results" / "portfolio.json"

PROFILE_EDGE_COUNTS = np.asarray(
    [6, 72, 102, 174, 181, 34, 251], dtype=float
)
PROFILE_CENTERS = np.arange(-4, 3, dtype=float) / 4
PROFILE_ROW_TYPES = (
    ((0, 4, 3, 8, 14, 0, 11), 1),
    ((0, 5, 0, 19, 1, 0, 15), 9),
    ((0, 5, 1, 9, 14, 0, 11), 14),
    ((0, 5, 12, 1, 1, 6, 15), 5),
    ((1, 0, 10, 1, 17, 1, 10), 2),
    ((1, 0, 10, 8, 3, 8, 10), 3),
    ((1, 0, 11, 0, 17, 0, 11), 1),
    ((1, 0, 11, 2, 13, 2, 11), 6),
)
PROFILE_SOURCE = (
    ROOT
    / "experiments"
    / "centered_global_count_milp"
    / "spectral_endpoint_audit"
    / "iteration_exclude_x2.json"
)


def normalized(array: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(array, axis=1)
    if np.any(norms == 0):
        raise ValueError("zero row cannot be normalized")
    return array / norms[:, None]


def coordinate_hash(array: np.ndarray) -> str:
    canonical = np.asarray(array, dtype="<f8", order="C")
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def pair_indices(cardinality: int) -> tuple[np.ndarray, np.ndarray]:
    return np.triu_indices(cardinality, 1)


def pair_values(array: np.ndarray) -> np.ndarray:
    first, second = pair_indices(len(array))
    return np.sum(array[first] * array[second], axis=1)


def max_inner(array: np.ndarray) -> float:
    return float(np.max(pair_values(array)))


def target_row_energies(cardinality: int) -> np.ndarray:
    base = []
    colors = np.arange(-4, 3)
    for degree, count in PROFILE_ROW_TYPES:
        energy = sum(
            color * color * multiplicity
            for color, multiplicity in zip(colors, degree)
        ) / 16
        base.extend([energy] * count)
    base = np.sort(np.asarray(base, dtype=float))
    if cardinality == 41:
        return base
    old_quantiles = (np.arange(41) + 0.5) / 41
    new_quantiles = (np.arange(cardinality) + 0.5) / cardinality
    interpolated = np.interp(new_quantiles, old_quantiles, base)
    return interpolated * (cardinality - 1) / 40


def soft_histogram(values: np.ndarray, sigma: float = 0.10) -> np.ndarray:
    logits = -(
        values[:, None] - PROFILE_CENTERS[None, :]
    ) ** 2 / (2 * sigma * sigma)
    logits -= np.max(logits, axis=1, keepdims=True)
    weights = np.exp(logits)
    weights /= np.sum(weights, axis=1, keepdims=True)
    return np.sum(weights, axis=0)


def diagnostics(array: np.ndarray) -> dict[str, object]:
    array = np.asarray(array, dtype=float)
    cardinality = len(array)
    first, second = pair_indices(cardinality)
    values = np.sum(array[first] * array[second], axis=1)
    gram = array @ array.T
    frame = array.T @ array
    row_energy = np.sum(gram * gram, axis=1) - 1
    target_probabilities = PROFILE_EDGE_COUNTS / np.sum(PROFILE_EDGE_COUNTS)
    histogram = soft_histogram(values)
    histogram_probabilities = histogram / len(values)
    target_rows = target_row_energies(cardinality)
    violating = np.maximum(values - 0.5, 0)
    eigenvalues = np.linalg.eigvalsh(frame)
    hard_bins = np.argmin(
        abs(values[:, None] - PROFILE_CENTERS[None, :]), axis=1
    )
    hard_counts = np.bincount(hard_bins, minlength=7)
    return {
        "cardinality": cardinality,
        "maximum_inner_product": float(np.max(values)),
        "minimum_inner_product": float(np.min(values)),
        "gap_above_one_half": float(np.max(values) - 0.5),
        "violating_pair_count": int(np.count_nonzero(violating)),
        "violation_l2": float(np.linalg.norm(violating)),
        "centroid_norm": float(np.linalg.norm(np.mean(array, axis=0))),
        "trace_gram_squared": float(np.sum(frame * frame)),
        "trace_gram_cubed": float(np.trace(frame @ frame @ frame)),
        "frame_eigenvalues": eigenvalues.tolist(),
        "row_energy_mean": float(np.mean(row_energy)),
        "row_energy_sorted_rmse_to_scaled_x12": float(
            np.sqrt(np.mean((np.sort(row_energy) - target_rows) ** 2))
        ),
        "soft_profile_l2": float(
            np.linalg.norm(histogram_probabilities - target_probabilities)
        ),
        "soft_profile_counts_sigma_0p10": histogram.tolist(),
        "nearest_quarter_counts": hard_counts.tolist(),
        "coordinate_little_endian_float64_sha256": coordinate_hash(array),
        "unit_norm_maximum_residual": float(
            np.max(abs(np.sum(array * array, axis=1) - 1))
        ),
    }


def load_baseline(cardinality: int) -> tuple[np.ndarray, dict[str, str]]:
    if cardinality == 41:
        path = ROOT / "experiments" / "input" / "spherical_codes_5_41.txt"
        array = np.loadtxt(path, delimiter=",")
        locator = "comma-separated rows"
    elif cardinality in (42, 43):
        path = (
            ROOT
            / "experiments"
            / "construction_round9_core_rattler"
            / "results"
            / "core_rattler_portfolio.json"
        )
        source = json.loads(path.read_text())
        run_index = cardinality - 41
        array = np.asarray(
            source["runs"][run_index]["best"]["coordinates_float64"],
            dtype=float,
        )
        locator = f"$.runs[{run_index}].best.coordinates_float64"
    elif cardinality == 44:
        path = (
            ROOT
            / "experiments"
            / "construction_round4_surgery"
            / "results"
            / "contact_surgery_portfolio.json"
        )
        source = json.loads(path.read_text())
        array = np.asarray(source["runs"][28]["coordinates"], dtype=float)
        locator = "$.runs[28].coordinates"
    else:
        raise ValueError("baseline is available only for N=41,...,44")
    array = normalized(array)
    if array.shape != (cardinality, 5):
        raise ValueError(f"wrong baseline shape {array.shape}")
    return array, {
        "path": str(path.relative_to(ROOT)),
        "locator": locator,
        "file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "coordinate_sha256": coordinate_hash(array),
    }


def delete_insert_seed(
    array: np.ndarray, rng: np.random.Generator, candidates: int = 4000
) -> tuple[np.ndarray, dict[str, object]]:
    """Delete the most crowded point and greedily insert a new one."""

    gram = array @ array.T
    np.fill_diagonal(gram, -np.inf)
    beta = 80
    shifted = gram - np.max(gram, axis=1, keepdims=True)
    crowding = np.max(gram, axis=1) + np.log(
        np.sum(np.exp(beta * shifted), axis=1)
    ) / beta
    deleted = int(np.argmax(crowding))
    remaining = np.delete(array, deleted, axis=0)
    proposals = normalized(rng.normal(size=(candidates, array.shape[1])))
    proposal_maxima = np.max(proposals @ remaining.T, axis=1)
    selected = int(np.argmin(proposal_maxima))
    answer = np.vstack([remaining, proposals[selected]])
    return answer, {
        "deleted_index": deleted,
        "candidate_count": candidates,
        "selected_candidate_index": selected,
        "inserted_point_maximum": float(proposal_maxima[selected]),
        "initial_maximum": max_inner(array),
        "post_insertion_maximum": max_inner(answer),
    }


def loss_and_gradient(
    array: np.ndarray,
    *,
    beta: float,
    histogram_weight: float,
    row_weight: float,
    center_weight: float,
    histogram_sigma: float,
) -> tuple[float, np.ndarray, dict[str, float]]:
    cardinality = len(array)
    first, second = pair_indices(cardinality)
    values = np.sum(array[first] * array[second], axis=1)

    maximum = float(np.max(values))
    exponentials = np.exp(beta * (values - maximum))
    partition = float(np.sum(exponentials))
    pair_derivative = exponentials / partition
    smooth_maximum = maximum + math.log(partition) / beta
    loss = smooth_maximum

    profile_loss = 0.0
    if histogram_weight:
        logits = -(
            values[:, None] - PROFILE_CENTERS[None, :]
        ) ** 2 / (2 * histogram_sigma**2)
        logits -= np.max(logits, axis=1, keepdims=True)
        weights = np.exp(logits)
        weights /= np.sum(weights, axis=1, keepdims=True)
        histogram = np.sum(weights, axis=0)
        target = PROFILE_EDGE_COUNTS / np.sum(PROFILE_EDGE_COUNTS)
        difference = histogram / len(values) - target
        profile_loss = histogram_weight * float(difference @ difference)
        loss += profile_loss
        histogram_gradient = (
            2 * histogram_weight * difference / len(values)
        )
        mean_center = weights @ PROFILE_CENTERS
        pair_derivative += np.sum(
            histogram_gradient[None, :]
            * weights
            * (
                PROFILE_CENTERS[None, :] - mean_center[:, None]
            )
            / histogram_sigma**2,
            axis=1,
        )

    row_loss = 0.0
    if row_weight:
        gram = array @ array.T
        row_energies = np.sum(gram * gram, axis=1) - 1
        order = np.argsort(row_energies, kind="stable")
        target_rows = target_row_energies(cardinality)
        difference = row_energies[order] - target_rows
        row_loss = row_weight * float(np.mean(difference * difference))
        loss += row_loss
        row_derivative = np.zeros(cardinality)
        row_derivative[order] = (
            2 * row_weight * difference / cardinality
        )
        pair_derivative += (
            2
            * values
            * (row_derivative[first] + row_derivative[second])
        )

    gradient = np.zeros_like(array)
    np.add.at(gradient, first, pair_derivative[:, None] * array[second])
    np.add.at(gradient, second, pair_derivative[:, None] * array[first])

    center_loss = 0.0
    if center_weight:
        centroid = np.mean(array, axis=0)
        center_loss = center_weight * float(centroid @ centroid)
        loss += center_loss
        gradient += 2 * center_weight * centroid[None, :] / cardinality

    gradient -= (
        np.sum(gradient * array, axis=1)[:, None] * array
    )
    return loss, gradient, {
        "smooth_maximum": smooth_maximum,
        "profile_loss": profile_loss,
        "row_loss": row_loss,
        "center_loss": center_loss,
        "hard_maximum": maximum,
    }


def schedule(kind: str, scale: float) -> list[dict[str, float | int | str]]:
    if kind == "profile_guided":
        return [
            {
                "name": "profile_lock",
                "iterations": int(500 * scale),
                "beta": 25.0,
                "learning_rate": 0.012,
                "histogram_weight": 35.0,
                "row_weight": 0.10,
                "center_weight": 1.5,
                "histogram_sigma": 0.14,
            },
            {
                "name": "profile_blend",
                "iterations": int(700 * scale),
                "beta": 55.0,
                "learning_rate": 0.007,
                "histogram_weight": 7.0,
                "row_weight": 0.025,
                "center_weight": 0.25,
                "histogram_sigma": 0.11,
            },
            {
                "name": "release",
                "iterations": int(1100 * scale),
                "beta": 120.0,
                "learning_rate": 0.004,
                "histogram_weight": 0.0,
                "row_weight": 0.0,
                "center_weight": 0.0,
                "histogram_sigma": 0.10,
            },
            {
                "name": "hard_release",
                "iterations": int(700 * scale),
                "beta": 280.0,
                "learning_rate": 0.0018,
                "histogram_weight": 0.0,
                "row_weight": 0.0,
                "center_weight": 0.0,
                "histogram_sigma": 0.10,
            },
        ]
    if kind == "unrestricted":
        return [
            {
                "name": "free_soft",
                "iterations": int(900 * scale),
                "beta": 60.0,
                "learning_rate": 0.006,
                "histogram_weight": 0.0,
                "row_weight": 0.0,
                "center_weight": 0.0,
                "histogram_sigma": 0.10,
            },
            {
                "name": "free_hard",
                "iterations": int(1400 * scale),
                "beta": 180.0,
                "learning_rate": 0.0025,
                "histogram_weight": 0.0,
                "row_weight": 0.0,
                "center_weight": 0.0,
                "histogram_sigma": 0.10,
            },
            {
                "name": "free_polish",
                "iterations": int(700 * scale),
                "beta": 400.0,
                "learning_rate": 0.0012,
                "histogram_weight": 0.0,
                "row_weight": 0.0,
                "center_weight": 0.0,
                "histogram_sigma": 0.10,
            },
        ]
    raise ValueError(f"unknown schedule {kind!r}")


def run_population(
    starts: list[tuple[str, np.ndarray]],
    *,
    kind: str,
    seed: int,
    scale: float,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    temperatures = np.geomspace(0.00025, 0.008, len(starts))
    states = []
    for (origin, array), temperature in zip(starts, temperatures):
        states.append(
            {
                "origin": origin,
                "array": normalized(array.copy()),
                "m": np.zeros_like(array),
                "v": np.zeros_like(array),
                "step": 0,
                "temperature": float(temperature),
            }
        )

    initial_records = [
        {"origin": state["origin"], **diagnostics(state["array"])}
        for state in states
    ]
    best_array = min(
        (state["array"].copy() for state in states), key=max_inner
    )
    best_origin = min(
        states, key=lambda state: max_inner(state["array"])
    )["origin"]
    best_maximum = max_inner(best_array)
    history = []
    phase_records = []
    exchange_attempts = 0
    exchange_accepts = 0

    for phase in schedule(kind, scale):
        iterations = int(phase["iterations"])
        if iterations <= 0:
            continue
        for iteration in range(iterations):
            for state in states:
                array = state["array"]
                _loss, gradient, parts = loss_and_gradient(
                    array,
                    beta=float(phase["beta"]),
                    histogram_weight=float(phase["histogram_weight"]),
                    row_weight=float(phase["row_weight"]),
                    center_weight=float(phase["center_weight"]),
                    histogram_sigma=float(phase["histogram_sigma"]),
                )
                state["step"] += 1
                step = state["step"]
                state["m"] = 0.9 * state["m"] + 0.1 * gradient
                state["v"] = 0.999 * state["v"] + 0.001 * gradient * gradient
                corrected_m = state["m"] / (1 - 0.9**step)
                corrected_v = state["v"] / (1 - 0.999**step)
                direction = corrected_m / (np.sqrt(corrected_v) + 1.0e-8)
                direction -= (
                    np.sum(direction * array, axis=1)[:, None] * array
                )
                noise = rng.normal(size=array.shape)
                noise -= np.sum(noise * array, axis=1)[:, None] * array
                noise_scale = (
                    float(phase["learning_rate"])
                    * state["temperature"]
                    * (1 - iteration / iterations)
                )
                array = normalized(
                    array
                    - float(phase["learning_rate"]) * direction
                    + noise_scale * noise
                )
                state["array"] = array
                current_maximum = max_inner(array)
                if current_maximum < best_maximum:
                    best_maximum = current_maximum
                    best_array = array.copy()
                    best_origin = state["origin"]

            if (iteration + 1) % 75 == 0:
                energies = [max_inner(state["array"]) for state in states]
                parity = (iteration // 75) % 2
                for left in range(parity, len(states) - 1, 2):
                    right = left + 1
                    inverse_difference = (
                        1 / states[left]["temperature"]
                        - 1 / states[right]["temperature"]
                    )
                    log_ratio = (
                        (energies[left] - energies[right])
                        * inverse_difference
                    )
                    exchange_attempts += 1
                    if math.log(rng.random()) < min(0.0, log_ratio):
                        for key in ("array", "m", "v", "origin"):
                            states[left][key], states[right][key] = (
                                states[right][key],
                                states[left][key],
                            )
                        exchange_accepts += 1
            if (iteration + 1) % 200 == 0 or iteration + 1 == iterations:
                history.append(
                    {
                        "phase": phase["name"],
                        "iteration": iteration + 1,
                        "best_maximum": best_maximum,
                        "replica_maxima": [
                            max_inner(state["array"]) for state in states
                        ],
                    }
                )
        replica_records = [
            {"origin": state["origin"], **diagnostics(state["array"])}
            for state in states
        ]
        best_maximum_index = min(
            range(len(states)),
            key=lambda index: replica_records[index][
                "maximum_inner_product"
            ],
        )
        best_profile_index = min(
            range(len(states)),
            key=lambda index: (
                replica_records[index]["soft_profile_l2"]
                + 0.05
                * replica_records[index][
                    "row_energy_sorted_rmse_to_scaled_x12"
                ]
            ),
        )

        def representative(index: int) -> dict[str, object]:
            return {
                **replica_records[index],
                "coordinates_float64": states[index]["array"].tolist(),
            }

        phase_records.append(
            {
                "phase": phase["name"],
                "profile_penalties_released": (
                    phase["histogram_weight"] == 0
                    and phase["row_weight"] == 0
                    and phase["center_weight"] == 0
                ),
                "replicas": replica_records,
                "best_maximum_representative": representative(
                    best_maximum_index
                ),
                "best_profile_representative": representative(
                    best_profile_index
                ),
            }
        )

    # A deterministic, zero-temperature final pass from the best hard-max
    # state prevents replica temperature from obscuring the handoff value.
    array = best_array.copy()
    m = np.zeros_like(array)
    v = np.zeros_like(array)
    step = 0
    polish_iterations = max(1, int(800 * scale))
    for iteration in range(polish_iterations):
        beta = 240.0 if iteration < polish_iterations // 2 else 600.0
        learning_rate = (
            0.0015 if iteration < polish_iterations // 2 else 0.0007
        )
        _loss, gradient, _parts = loss_and_gradient(
            array,
            beta=beta,
            histogram_weight=0,
            row_weight=0,
            center_weight=0,
            histogram_sigma=0.10,
        )
        step += 1
        m = 0.9 * m + 0.1 * gradient
        v = 0.999 * v + 0.001 * gradient * gradient
        direction = (m / (1 - 0.9**step)) / (
            np.sqrt(v / (1 - 0.999**step)) + 1.0e-8
        )
        direction -= np.sum(direction * array, axis=1)[:, None] * array
        candidate = normalized(array - learning_rate * direction)
        if max_inner(candidate) < best_maximum:
            best_maximum = max_inner(candidate)
            best_array = candidate.copy()
            best_origin = f"{best_origin}:zero_temperature_polish"
        array = candidate

    return {
        "kind": kind,
        "seed": seed,
        "temperatures": temperatures.tolist(),
        "initial_replicas": initial_records,
        "phases": phase_records,
        "history": history,
        "replica_exchange": {
            "attempts": exchange_attempts,
            "accepts": exchange_accepts,
        },
        "best_origin": best_origin,
        "best": {
            **diagnostics(best_array),
            "coordinates_float64": best_array.tolist(),
        },
    }


def starts_for(
    cardinality: int,
    baseline: np.ndarray,
    *,
    kind: str,
    seed: int,
    replicas: int,
) -> tuple[list[tuple[str, np.ndarray]], dict[str, object]]:
    rng = np.random.default_rng(seed)
    delete_insert, topology_record = delete_insert_seed(baseline, rng)
    starts: list[tuple[str, np.ndarray]] = [
        ("stored_unrestricted_baseline", baseline),
        ("topology_delete_insert", delete_insert),
    ]
    while len(starts) < replicas:
        index = len(starts)
        if kind == "profile_guided" or index % 2 == 0:
            candidate = normalized(rng.normal(size=baseline.shape))
            origin = f"asymmetric_gaussian_{index}"
        else:
            perturbation = rng.normal(size=baseline.shape)
            perturbation -= (
                np.sum(perturbation * baseline, axis=1)[:, None] * baseline
            )
            candidate = normalized(baseline + 0.08 * perturbation)
            origin = f"asymmetric_baseline_perturbation_{index}"
        starts.append((origin, candidate))
    return starts, topology_record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", nargs="+", type=int, default=[41, 42, 43, 44])
    parser.add_argument("--replicas", type=int, default=6)
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--seed-base", type=int, default=2026072400)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.replicas < 4:
        parser.error("--replicas must be at least four")
    if args.scale <= 0:
        parser.error("--scale must be positive")

    started = time.time()
    profile_source_bytes = PROFILE_SOURCE.read_bytes()
    runs = []
    sources = {}
    for cardinality in args.n:
        baseline, source = load_baseline(cardinality)
        sources[str(cardinality)] = source
        for kind_index, kind in enumerate(("profile_guided", "unrestricted")):
            seed = args.seed_base + 100 * (cardinality - 41) + kind_index
            starts, topology_record = starts_for(
                cardinality,
                baseline,
                kind=kind,
                seed=seed,
                replicas=args.replicas,
            )
            print(
                f"N={cardinality} kind={kind} "
                f"initial_best={min(max_inner(x) for _, x in starts):.12f}",
                flush=True,
            )
            run = run_population(
                starts, kind=kind, seed=seed, scale=args.scale
            )
            run["cardinality"] = cardinality
            run["topology_change"] = topology_record
            run["baseline"] = diagnostics(baseline)
            print(
                f"N={cardinality} kind={kind} "
                f"best={run['best']['maximum_inner_product']:.12f}",
                flush=True,
            )
            runs.append(run)

    best_by_n = {}
    for cardinality in args.n:
        candidates = [
            run for run in runs if run["cardinality"] == cardinality
        ]
        best = min(
            candidates,
            key=lambda run: run["best"]["maximum_inner_product"],
        )
        best_by_n[str(cardinality)] = {
            "kind": best["kind"],
            "maximum_inner_product": best["best"]["maximum_inner_product"],
            "coordinate_sha256": best["best"][
                "coordinate_little_endian_float64_sha256"
            ],
        }

    output = {
        "schema": "kissing5.construction_round11_x12_profile.v1",
        "evidence_status": (
            "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE"
        ),
        "profile_source": str(PROFILE_SOURCE.relative_to(ROOT)),
        "profile_source_sha256": hashlib.sha256(
            profile_source_bytes
        ).hexdigest(),
        "profile_edge_counts": PROFILE_EDGE_COUNTS.astype(int).tolist(),
        "profile_row_types": [
            {"degree": list(degree), "count": count}
            for degree, count in PROFILE_ROW_TYPES
        ],
        "parameters": {
            "cardinalities": args.n,
            "replicas": args.replicas,
            "scale": args.scale,
            "seed_base": args.seed_base,
            "schedules": {
                kind: schedule(kind, args.scale)
                for kind in ("profile_guided", "unrestricted")
            },
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "baseline_sources": sources,
        "runs": runs,
        "best_by_n": best_by_n,
        "elapsed_seconds": time.time() - started,
        "exact_candidate_found": any(
            run["best"]["maximum_inner_product"] <= 0.5
            for run in runs
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()

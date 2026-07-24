#!/usr/bin/env python3
"""Global low-rigidity-mode topology escape for N=41,...,44.

Unlike the deletion/reinsertion searches, this move perturbs every point
coherently.  It removes infinitesimal rotations, kicks along low singular
modes of the tight-edge rigidity matrix, temporarily penalizes survival of
the old tight edges, fully releases that penalty, and applies direct minimax
polish.

This is numerical construction search, not an exact certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PORTFOLIO = HERE / "results" / "portfolio.json"
POLISHED = HERE / "results" / "epigraph_polished.json"
OUTPUT = HERE / "results" / "flex_topology_escape.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


search = load_module("round11_search_flex", HERE / "search.py")
polisher = load_module(
    "round11_polisher_flex", HERE / "epigraph_polish.py"
)


def source_configurations() -> tuple[
    dict[int, np.ndarray], dict[str, str]
]:
    portfolio_bytes = PORTFOLIO.read_bytes()
    polished_bytes = POLISHED.read_bytes()
    portfolio = json.loads(portfolio_bytes)
    polished = json.loads(polished_bytes)
    result = {}
    for cardinality in range(41, 44):
        record = next(
            run
            for run in portfolio["runs"]
            if run["cardinality"] == cardinality
        )
        result[cardinality] = np.asarray(
            record["best"]["coordinates_float64"], dtype=float
        )
    best44 = min(
        (
            record
            for record in polished["records"]
            if record["cardinality"] == 44
        ),
        key=lambda record: record["retained"][
            "maximum_inner_product"
        ],
    )
    result[44] = np.asarray(
        best44["retained"]["coordinates_float64"], dtype=float
    )
    return result, {
        "portfolio_sha256": hashlib.sha256(portfolio_bytes).hexdigest(),
        "polished_sha256": hashlib.sha256(polished_bytes).hexdigest(),
    }


def tight_edges(
    array: np.ndarray, tolerance: float
) -> tuple[float, list[tuple[int, int]]]:
    gram = array @ array.T
    first, second = np.triu_indices(len(array), 1)
    products = gram[first, second]
    maximum = float(np.max(products))
    edges = [
        (int(left), int(right))
        for left, right, product in zip(first, second, products)
        if product >= maximum - tolerance
    ]
    return maximum, edges


def tangent_bases(array: np.ndarray) -> np.ndarray:
    bases = []
    for point in array:
        _left, _singular, right = np.linalg.svd(
            point.reshape(1, 5), full_matrices=True
        )
        basis = right[1:].T
        if np.max(np.abs(basis.T @ basis - np.eye(4))) > 2.0e-14:
            raise RuntimeError("tangent basis lost orthonormality")
        bases.append(basis)
    return np.asarray(bases)


def rotation_modes(
    array: np.ndarray, bases: np.ndarray
) -> np.ndarray:
    cardinality = len(array)
    columns = []
    for first in range(5):
        for second in range(first + 1, 5):
            displacement = np.zeros_like(array)
            displacement[:, first] = -array[:, second]
            displacement[:, second] = array[:, first]
            coordinates = np.concatenate(
                [
                    bases[vertex].T @ displacement[vertex]
                    for vertex in range(cardinality)
                ]
            )
            columns.append(coordinates)
    rotations = np.column_stack(columns)
    if np.linalg.matrix_rank(rotations, tol=1.0e-10) != 10:
        raise RuntimeError("rotation modes do not have dimension ten")
    return rotations


def rigidity_analysis(
    array: np.ndarray,
    edges: list[tuple[int, int]],
    mode_count: int,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    cardinality = len(array)
    bases = tangent_bases(array)
    gram = array @ array.T
    rigidity = np.zeros((len(edges), 4 * cardinality))
    for row, (first, second) in enumerate(edges):
        product = gram[first, second]
        first_gradient = array[second] - product * array[first]
        second_gradient = array[first] - product * array[second]
        rigidity[row, 4 * first : 4 * first + 4] = (
            bases[first].T @ first_gradient
        )
        rigidity[row, 4 * second : 4 * second + 4] = (
            bases[second].T @ second_gradient
        )

    rotations = rotation_modes(array, bases)
    rotation_q, _rotation_r = np.linalg.qr(
        rotations, mode="reduced"
    )
    complete_q, _complete_r = np.linalg.qr(
        rotation_q, mode="complete"
    )
    nonrotating = complete_q[:, 10:]
    reduced = rigidity @ nonrotating
    _left, singular_values, right = np.linalg.svd(
        reduced, full_matrices=True
    )
    nonrotation_dimension = nonrotating.shape[1]
    padded_singular = np.zeros(nonrotation_dimension)
    padded_singular[: len(singular_values)] = singular_values
    count = min(mode_count, nonrotation_dimension)
    selected_indices = np.argsort(padded_singular)[:count]
    modes = nonrotating @ right.T[:, selected_indices]
    mode_residuals = np.linalg.norm(rigidity @ modes, axis=0)
    rotation_residual = float(
        np.linalg.norm(rigidity @ rotation_q, ord=2)
    )
    return bases, modes, {
        "tight_edge_count": len(edges),
        "tangent_dimension": 4 * cardinality,
        "rotation_dimension": 10,
        "nonrotation_dimension": nonrotation_dimension,
        "reduced_rigidity_rank_at_1e-9": int(
            np.count_nonzero(singular_values > 1.0e-9)
        ),
        "reduced_rigidity_nullity_at_1e-9": int(
            nonrotation_dimension
            - np.count_nonzero(singular_values > 1.0e-9)
        ),
        "smallest_reduced_singular_values": np.sort(
            padded_singular
        )[: min(30, len(padded_singular))].tolist(),
        "selected_mode_count": count,
        "selected_mode_rigidity_residuals": (
            mode_residuals.tolist()
        ),
        "rotation_rigidity_operator_norm": rotation_residual,
        "tangent_basis_maximum_residual": float(
            max(
                np.max(
                    np.abs(
                        bases[vertex].T @ bases[vertex]
                        - np.eye(4)
                    )
                )
                for vertex in range(cardinality)
            )
        ),
    }


def geodesic_kick(
    source: np.ndarray,
    bases: np.ndarray,
    modes: np.ndarray,
    coefficients: np.ndarray,
    amplitude: float,
) -> np.ndarray:
    tangent_coordinates = (
        modes @ coefficients
    ).reshape(len(source), 4)
    tangent = np.einsum(
        "nij,nj->ni", bases, tangent_coordinates
    )
    speeds = np.linalg.norm(tangent, axis=1)
    rms = float(np.sqrt(np.mean(speeds * speeds)))
    if rms < 1.0e-14:
        raise RuntimeError("degenerate flex kick")
    tangent *= amplitude / rms
    speeds = np.linalg.norm(tangent, axis=1)
    # Avoid allowing one almost-localized flex mode to move a single point
    # by more than one radian in the discovery kick.
    scale = np.minimum(1, 1.0 / np.maximum(speeds, 1.0e-300))
    tangent *= scale[:, None]
    speeds = np.linalg.norm(tangent, axis=1)
    answer = np.empty_like(source)
    stationary = speeds < 1.0e-14
    answer[stationary] = source[stationary]
    moving = ~stationary
    directions = tangent[moving] / speeds[moving, None]
    answer[moving] = (
        np.cos(speeds[moving])[:, None] * source[moving]
        + np.sin(speeds[moving])[:, None] * directions
    )
    return search.normalized(answer)


def edge_set(
    array: np.ndarray, tolerance: float
) -> set[tuple[int, int]]:
    return set(tight_edges(array, tolerance)[1])


def select_kick(
    source: np.ndarray,
    bases: np.ndarray,
    modes: np.ndarray,
    source_edges: set[tuple[int, int]],
    amplitude: float,
    candidates: int,
    rng: np.random.Generator,
    tolerance: float,
) -> tuple[np.ndarray, dict[str, object]]:
    records = []
    best_score = math.inf
    best = None
    for candidate in range(candidates):
        coefficients = rng.normal(size=modes.shape[1])
        coefficients /= np.linalg.norm(coefficients)
        array = geodesic_kick(
            source, bases, modes, coefficients, amplitude
        )
        maximum = search.max_inner(array)
        current_edges = edge_set(array, tolerance)
        overlap = len(source_edges & current_edges)
        overlap_fraction = overlap / max(1, len(source_edges))
        score = maximum + 0.012 * overlap_fraction
        records.append(
            (
                score,
                maximum,
                overlap,
                len(current_edges),
                candidate,
            )
        )
        if score < best_score:
            best_score = score
            best = array
    assert best is not None
    chosen = min(records)
    return best, {
        "candidate_count": candidates,
        "amplitude_radians_rms_before_clipping": amplitude,
        "selection_objective": (
            "maximum_inner_product + "
            "0.012 * old_tight_edge_overlap_fraction"
        ),
        "selected_candidate": chosen[4],
        "selected_score": chosen[0],
        "selected_maximum_inner_product": chosen[1],
        "selected_old_edge_overlap": chosen[2],
        "selected_tight_edge_count": chosen[3],
        "candidate_maximum_minimum": min(
            record[1] for record in records
        ),
        "candidate_maximum_median": float(
            np.median([record[1] for record in records])
        ),
    }


def old_edge_penalty_gradient(
    array: np.ndarray,
    edges: list[tuple[int, int]],
    *,
    threshold: float,
    beta: float,
    weight: float,
) -> tuple[float, np.ndarray]:
    if not weight:
        return 0.0, np.zeros_like(array)
    first = np.asarray([edge[0] for edge in edges], dtype=int)
    second = np.asarray([edge[1] for edge in edges], dtype=int)
    values = np.sum(array[first] * array[second], axis=1)
    scaled = beta * (values - threshold)
    softplus = np.logaddexp(0, scaled) / beta
    derivatives = np.empty_like(scaled)
    positive = scaled >= 0
    derivatives[positive] = 1 / (
        1 + np.exp(-scaled[positive])
    )
    negative_exponential = np.exp(scaled[~positive])
    derivatives[~positive] = negative_exponential / (
        1 + negative_exponential
    )
    derivatives *= weight / len(edges)
    gradient = np.zeros_like(array)
    np.add.at(
        gradient, first, derivatives[:, None] * array[second]
    )
    np.add.at(
        gradient, second, derivatives[:, None] * array[first]
    )
    gradient -= (
        np.sum(gradient * array, axis=1)[:, None] * array
    )
    return weight * float(np.mean(softplus)), gradient


def optimize_escape(
    initial: np.ndarray,
    old_edges: list[tuple[int, int]],
    source_maximum: float,
    *,
    switch_iterations: int,
    release_iterations: int,
    seed: int,
) -> tuple[np.ndarray, dict[str, object]]:
    rng = np.random.default_rng(seed)
    array = initial.copy()
    moment = np.zeros_like(array)
    square = np.zeros_like(array)
    best = array.copy()
    best_maximum = search.max_inner(array)
    history = []
    total = switch_iterations + release_iterations
    for iteration in range(total):
        in_switch = iteration < switch_iterations
        if in_switch:
            fraction = iteration / max(1, switch_iterations - 1)
            beta = 75.0
            learning_rate = 0.006
            penalty_weight = 2.0 * (1 - fraction) + 0.15 * fraction
        else:
            fraction = (
                iteration - switch_iterations
            ) / max(1, release_iterations - 1)
            beta = 130.0 if fraction < 0.58 else 300.0
            learning_rate = (
                0.0032 if fraction < 0.58 else 0.0014
            )
            penalty_weight = 0.0
        _loss, gradient, _parts = search.loss_and_gradient(
            array,
            beta=beta,
            histogram_weight=0,
            row_weight=0,
            center_weight=0,
            histogram_sigma=0.10,
        )
        penalty, penalty_gradient = old_edge_penalty_gradient(
            array,
            old_edges,
            threshold=source_maximum - 0.004,
            beta=90.0,
            weight=penalty_weight,
        )
        gradient += penalty_gradient
        step = iteration + 1
        moment = 0.9 * moment + 0.1 * gradient
        square = 0.999 * square + 0.001 * gradient * gradient
        direction = (moment / (1 - 0.9**step)) / (
            np.sqrt(square / (1 - 0.999**step)) + 1.0e-8
        )
        direction -= (
            np.sum(direction * array, axis=1)[:, None] * array
        )
        noise_scale = (
            0.00008 * (1 - fraction) if in_switch else 0
        )
        noise = rng.normal(size=array.shape)
        noise -= np.sum(noise * array, axis=1)[:, None] * array
        array = search.normalized(
            array
            - learning_rate * direction
            + noise_scale * noise
        )
        maximum = search.max_inner(array)
        if maximum < best_maximum:
            best = array.copy()
            best_maximum = maximum
        if (
            iteration + 1 in (switch_iterations, total)
            or (iteration + 1) % 400 == 0
        ):
            history.append(
                {
                    "iteration": iteration + 1,
                    "phase": "switch" if in_switch else "release",
                    "maximum": maximum,
                    "best_maximum": best_maximum,
                    "old_edge_penalty": penalty,
                    "old_edge_penalty_weight": penalty_weight,
                }
            )
    return best, {
        "switch_iterations": switch_iterations,
        "release_iterations": release_iterations,
        "old_edge_threshold": source_maximum - 0.004,
        "old_edge_penalty_beta": 90.0,
        "old_edge_penalty_initial_weight": 2.0,
        "old_edge_penalty_final_released_weight": 0.0,
        "history": history,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--seed-base", type=int, default=2026073000)
    parser.add_argument("--mode-count", type=int, default=28)
    parser.add_argument("--kick-candidates", type=int, default=48)
    parser.add_argument("--switch-iterations", type=int, default=900)
    parser.add_argument("--release-iterations", type=int, default=1400)
    parser.add_argument("--epigraph-maxiter", type=int, default=700)
    parser.add_argument("--tight-tolerance", type=float, default=5.0e-4)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    sources, source_hashes = source_configurations()
    amplitudes = [0.08, 0.16, 0.28, 0.45]
    started = time.time()
    analyses = []
    runs = []
    for cardinality in range(41, 45):
        source = search.normalized(sources[cardinality])
        source_maximum, tight = tight_edges(
            source, args.tight_tolerance
        )
        source_edge_set = set(tight)
        bases, modes, mode_analysis = rigidity_analysis(
            source, tight, args.mode_count
        )
        analyses.append(
            {
                "cardinality": cardinality,
                "source": {
                    **search.diagnostics(source),
                    "coordinates_float64": source.tolist(),
                },
                "tight_tolerance": args.tight_tolerance,
                "tight_edges": [list(edge) for edge in tight],
                "rigidity": mode_analysis,
            }
        )
        for restart in range(args.restarts):
            seed = (
                args.seed_base
                + 100 * (cardinality - 41)
                + restart
            )
            rng = np.random.default_rng(seed)
            amplitude = amplitudes[restart % len(amplitudes)]
            kicked, kick_record = select_kick(
                source,
                bases,
                modes,
                source_edge_set,
                amplitude,
                args.kick_candidates,
                rng,
                args.tight_tolerance,
            )
            escaped, optimization = optimize_escape(
                kicked,
                tight,
                source_maximum,
                switch_iterations=args.switch_iterations,
                release_iterations=args.release_iterations,
                seed=seed + 10000,
            )
            polished, solver = polisher.epigraph_refine(
                escaped, args.epigraph_maxiter
            )
            candidates = [kicked, escaped, polished]
            maxima = [
                search.max_inner(candidate)
                for candidate in candidates
            ]
            retained_index = int(np.argmin(maxima))
            retained = candidates[retained_index]
            final_edges = edge_set(
                retained, args.tight_tolerance
            )
            intersection = len(source_edge_set & final_edges)
            union = len(source_edge_set | final_edges)
            record = {
                "cardinality": cardinality,
                "restart": restart,
                "seed": seed,
                "amplitude": amplitude,
                "kick": kick_record,
                "kicked": search.diagnostics(kicked),
                "optimization": optimization,
                "escaped": search.diagnostics(escaped),
                "epigraph_solver": solver,
                "polished": search.diagnostics(polished),
                "retained_stage": [
                    "kicked",
                    "escaped",
                    "polished",
                ][retained_index],
                "retained": {
                    **search.diagnostics(retained),
                    "coordinates_float64": retained.tolist(),
                },
                "tight_graph_comparison": {
                    "source_edges": len(source_edge_set),
                    "retained_edges": len(final_edges),
                    "intersection": intersection,
                    "symmetric_difference": len(
                        source_edge_set ^ final_edges
                    ),
                    "jaccard": intersection / union if union else 1,
                },
                "beats_source": (
                    search.max_inner(retained)
                    < source_maximum - 1.0e-12
                ),
                "crosses_one_half": (
                    search.max_inner(retained) <= 0.5
                ),
            }
            print(
                f"N={cardinality} restart={restart} "
                f"amp={amplitude:.2f} "
                f"nullity={mode_analysis['reduced_rigidity_nullity_at_1e-9']} "
                f"source={source_maximum:.12f} "
                f"retained={record['retained']['maximum_inner_product']:.12f} "
                f"edge_delta={record['tight_graph_comparison']['symmetric_difference']}",
                flush=True,
            )
            runs.append(record)

    best_by_n = {}
    for cardinality in range(41, 45):
        candidates = [
            run for run in runs if run["cardinality"] == cardinality
        ]
        best = min(
            candidates,
            key=lambda run: run["retained"][
                "maximum_inner_product"
            ],
        )
        best_by_n[str(cardinality)] = {
            "restart": best["restart"],
            "maximum_inner_product": best["retained"][
                "maximum_inner_product"
            ],
            "coordinate_sha256": best["retained"][
                "coordinate_little_endian_float64_sha256"
            ],
            "beats_source": best["beats_source"],
            "tight_graph_symmetric_difference": best[
                "tight_graph_comparison"
            ]["symmetric_difference"],
        }
    try:
        output_label = str(args.output.relative_to(ROOT))
    except ValueError:
        output_label = str(args.output)
    output = {
        "schema": "kissing5.flex_topology_escape.v1",
        "evidence_status": (
            "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE"
        ),
        "source_files": {
            "portfolio": str(PORTFOLIO.relative_to(ROOT)),
            "polished": str(POLISHED.relative_to(ROOT)),
            **source_hashes,
        },
        "parameters": vars(args) | {"output": output_label},
        "amplitudes": amplitudes,
        "analyses": analyses,
        "runs": runs,
        "best_by_n": best_by_n,
        "elapsed_seconds": time.time() - started,
        "exact_candidate_found": any(
            run["crosses_one_half"] for run in runs
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()

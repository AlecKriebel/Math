#!/usr/bin/env python3
"""Minimum-tight-edge-cover block deletion and joint reinsertion.

For each N=41,...,44 this experiment:

1. extracts all source edges within 5e-4 of the maximum;
2. proves a minimum vertex cover by an exact bitset maximum-independent-set
   search;
3. removes the entire cover;
4. reinserts every removed point from a separate asymmetric random cap;
5. jointly optimizes the inserted block while freezing its complement;
6. releases all vertices and applies a direct minimax polish.

This is numerical construction search, not an upper-bound argument.
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
from scipy.optimize import nnls


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PORTFOLIO = HERE / "results" / "portfolio.json"
POLISHED = HERE / "results" / "epigraph_polished.json"
OUTPUT = HERE / "results" / "block_reinsertion.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


search = load_module("round11_search_block", HERE / "search.py")
polisher = load_module(
    "round11_polisher_block", HERE / "epigraph_polish.py"
)


def tight_edges(
    array: np.ndarray, tolerance: float
) -> tuple[float, list[tuple[int, int]]]:
    gram = array @ array.T
    first, second = np.triu_indices(len(array), 1)
    values = gram[first, second]
    maximum = float(np.max(values))
    mask = values >= maximum - tolerance
    return maximum, [
        (int(left), int(right))
        for left, right in zip(first[mask], second[mask])
    ]


def maximum_clique(
    adjacency: list[int],
) -> tuple[list[int], int]:
    """Exact Tomita-style bitset search with greedy-color upper bounds."""

    cardinality = len(adjacency)
    best: list[int] = []
    visited_nodes = 0

    def color_sort(candidates: int) -> tuple[list[int], list[int]]:
        order = []
        bounds = []
        uncolored = candidates
        color = 0
        while uncolored:
            color += 1
            available = uncolored
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                order.append(vertex)
                bounds.append(color)
                uncolored ^= bit
                available ^= bit
                available &= ~adjacency[vertex]
        return order, bounds

    def expand(clique: list[int], candidates: int) -> None:
        nonlocal best, visited_nodes
        visited_nodes += 1
        if not candidates:
            if len(clique) > len(best):
                best = clique.copy()
            return
        order, bounds = color_sort(candidates)
        for index in range(len(order) - 1, -1, -1):
            if len(clique) + bounds[index] <= len(best):
                return
            vertex = order[index]
            bit = 1 << vertex
            if candidates & bit:
                expand(clique + [vertex], candidates & adjacency[vertex])
                candidates ^= bit
        if len(clique) > len(best):
            best = clique.copy()

    expand([], (1 << cardinality) - 1)
    return sorted(best), visited_nodes


def minimum_vertex_cover(
    cardinality: int, edges: list[tuple[int, int]]
) -> tuple[list[int], list[int], int]:
    original_adjacency = [0] * cardinality
    for first, second in edges:
        original_adjacency[first] |= 1 << second
        original_adjacency[second] |= 1 << first
    full = (1 << cardinality) - 1
    complement_adjacency = [
        full ^ (1 << vertex) ^ original_adjacency[vertex]
        for vertex in range(cardinality)
    ]
    independent, visited = maximum_clique(complement_adjacency)
    independent_set = set(independent)
    cover = [
        vertex
        for vertex in range(cardinality)
        if vertex not in independent_set
    ]
    if any(
        first not in cover and second not in cover
        for first, second in edges
    ):
        raise RuntimeError("computed cover misses an edge")
    return cover, independent, visited


def equilibrium_stress(
    array: np.ndarray, edges: list[tuple[int, int]]
) -> dict[str, object]:
    cardinality = len(array)
    gram = array @ array.T
    matrix = np.zeros((5 * cardinality + 1, len(edges)))
    matrix[-1] = 1
    for index, (first, second) in enumerate(edges):
        product = gram[first, second]
        matrix[5 * first : 5 * first + 5, index] = (
            array[second] - product * array[first]
        )
        matrix[5 * second : 5 * second + 5, index] = (
            array[first] - product * array[second]
        )
    target = np.zeros(5 * cardinality + 1)
    target[-1] = 1
    weights, residual = nnls(
        matrix, target, maxiter=max(1000, 100 * len(edges))
    )
    support = weights > 1.0e-10
    incidence = np.zeros(cardinality)
    for weight, (first, second) in zip(weights, edges):
        incidence[first] += weight
        incidence[second] += weight
    return {
        "method": "nonnegative_least_squares_tangent_equilibrium",
        "residual_norm": float(residual),
        "weight_sum": float(np.sum(weights)),
        "support_size_at_1e-10": int(np.count_nonzero(support)),
        "minimum_supported_weight": float(
            np.min(weights[support]) if np.any(support) else 0
        ),
        "maximum_weight": float(np.max(weights, initial=0)),
        "weights": weights.tolist(),
        "vertex_incidence_weights": incidence.tolist(),
    }


def cap_point(
    center: np.ndarray,
    radius: float,
    rng: np.random.Generator,
    count: int,
) -> np.ndarray:
    tangent = rng.normal(size=(count, 5))
    tangent -= (tangent @ center)[:, None] * center
    small = np.linalg.norm(tangent, axis=1) < 1.0e-12
    while np.any(small):
        tangent[small] = rng.normal(size=(np.count_nonzero(small), 5))
        tangent[small] -= (
            (tangent[small] @ center)[:, None] * center
        )
        small = np.linalg.norm(tangent, axis=1) < 1.0e-12
    tangent /= np.linalg.norm(tangent, axis=1)[:, None]
    angle = radius * np.sqrt(rng.random(count))
    return (
        np.cos(angle)[:, None] * center
        + np.sin(angle)[:, None] * tangent
    )


def reinsert_from_caps(
    source: np.ndarray,
    cover: list[int],
    independent: list[int],
    rng: np.random.Generator,
    candidates_per_vertex: int,
) -> tuple[np.ndarray, dict[str, object]]:
    answer = source.copy()
    current = [source[index].copy() for index in independent]
    insertion_order = np.asarray(cover)[rng.permutation(len(cover))]
    radii = []
    offsets = []
    selected_maxima = []
    for vertex in insertion_order:
        original = source[vertex]
        direction = rng.normal(size=5)
        direction -= float(direction @ original) * original
        direction /= np.linalg.norm(direction)
        offset = float(rng.uniform(0.25, 0.95))
        center = math.cos(offset) * original + math.sin(offset) * direction
        radius = float(rng.uniform(0.35, 1.15))
        proposals = cap_point(
            center, radius, rng, candidates_per_vertex
        )
        fixed = np.asarray(current)
        products = proposals @ fixed.T
        maxima = np.max(products, axis=1)
        # A small smooth-crowding tiebreaker prevents repeated choices from
        # being controlled by one accidental pair alone.
        shifted = products - maxima[:, None]
        scores = maxima + np.log(
            np.sum(np.exp(35 * shifted), axis=1)
        ) / 35
        selected = int(np.argmin(scores))
        point = proposals[selected]
        answer[vertex] = point
        current.append(point)
        radii.append(radius)
        offsets.append(offset)
        selected_maxima.append(float(maxima[selected]))
    return search.normalized(answer), {
        "insertion_order": insertion_order.astype(int).tolist(),
        "candidates_per_vertex": candidates_per_vertex,
        "cap_radius_minimum": min(radii),
        "cap_radius_maximum": max(radii),
        "cap_center_offset_minimum": min(offsets),
        "cap_center_offset_maximum": max(offsets),
        "selected_insertion_maximum_maximum": max(selected_maxima),
    }


def masked_optimize(
    initial: np.ndarray,
    movable: np.ndarray,
    *,
    iterations: int,
    seed: int,
    frozen_reference: np.ndarray | None,
) -> tuple[np.ndarray, dict[str, object]]:
    rng = np.random.default_rng(seed)
    array = initial.copy()
    moment = np.zeros_like(array)
    square = np.zeros_like(array)
    best = array.copy()
    best_maximum = search.max_inner(array)
    history = []
    for iteration in range(iterations):
        fraction = iteration / max(1, iterations - 1)
        beta = 45.0 if fraction < 0.45 else (
            120.0 if fraction < 0.8 else 300.0
        )
        learning_rate = 0.005 if fraction < 0.45 else (
            0.0025 if fraction < 0.8 else 0.0012
        )
        _loss, gradient, _parts = search.loss_and_gradient(
            array,
            beta=beta,
            histogram_weight=0,
            row_weight=0,
            center_weight=0,
            histogram_sigma=0.10,
        )
        gradient[~movable] = 0
        step = iteration + 1
        moment = 0.9 * moment + 0.1 * gradient
        square = 0.999 * square + 0.001 * gradient * gradient
        direction = (moment / (1 - 0.9**step)) / (
            np.sqrt(square / (1 - 0.999**step)) + 1.0e-8
        )
        direction[~movable] = 0
        direction -= (
            np.sum(direction * array, axis=1)[:, None] * array
        )
        noise = rng.normal(size=array.shape)
        noise -= np.sum(noise * array, axis=1)[:, None] * array
        noise[~movable] = 0
        noise_scale = (
            0.00012 * (1 - fraction) if frozen_reference is not None else 0
        )
        array = search.normalized(
            array - learning_rate * direction + noise_scale * noise
        )
        if frozen_reference is not None:
            array[~movable] = frozen_reference[~movable]
        maximum = search.max_inner(array)
        if maximum < best_maximum:
            best = array.copy()
            best_maximum = maximum
        if (iteration + 1) % 250 == 0 or iteration + 1 == iterations:
            history.append(
                {
                    "iteration": iteration + 1,
                    "maximum": maximum,
                    "best_maximum": best_maximum,
                }
            )
    return best, {
        "iterations": iterations,
        "movable_count": int(np.count_nonzero(movable)),
        "frozen_count": int(np.count_nonzero(~movable)),
        "history": history,
    }


def edge_set(
    array: np.ndarray, tolerance: float
) -> set[tuple[int, int]]:
    return set(tight_edges(array, tolerance)[1])


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=4)
    parser.add_argument("--seed-base", type=int, default=2026072800)
    parser.add_argument("--candidates-per-vertex", type=int, default=350)
    parser.add_argument("--freeze-iterations", type=int, default=1300)
    parser.add_argument("--release-iterations", type=int, default=1300)
    parser.add_argument("--epigraph-maxiter", type=int, default=700)
    parser.add_argument("--tight-tolerance", type=float, default=5.0e-4)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    sources, source_hashes = source_configurations()
    started = time.time()
    analyses = []
    runs = []
    for cardinality in range(41, 45):
        source = search.normalized(sources[cardinality])
        source_maximum, edges = tight_edges(
            source, args.tight_tolerance
        )
        cover, independent, visited = minimum_vertex_cover(
            cardinality, edges
        )
        stress = equilibrium_stress(source, edges)
        analyses.append(
            {
                "cardinality": cardinality,
                "source": {
                    **search.diagnostics(source),
                    "coordinates_float64": source.tolist(),
                },
                "tight_tolerance": args.tight_tolerance,
                "tight_edge_count": len(edges),
                "tight_edges": [list(edge) for edge in edges],
                "minimum_vertex_cover": cover,
                "maximum_independent_set": independent,
                "exact_clique_search_nodes": visited,
                "stress": stress,
            }
        )
        source_edges = set(edges)
        for restart in range(args.restarts):
            seed = (
                args.seed_base + 100 * (cardinality - 41) + restart
            )
            rng = np.random.default_rng(seed)
            inserted, insertion = reinsert_from_caps(
                source,
                cover,
                independent,
                rng,
                args.candidates_per_vertex,
            )
            movable = np.zeros(cardinality, dtype=bool)
            movable[cover] = True
            frozen, freeze_record = masked_optimize(
                inserted,
                movable,
                iterations=args.freeze_iterations,
                seed=seed + 10000,
                frozen_reference=source,
            )
            released, release_record = masked_optimize(
                frozen,
                np.ones(cardinality, dtype=bool),
                iterations=args.release_iterations,
                seed=seed + 20000,
                frozen_reference=None,
            )
            polished, solver = polisher.epigraph_refine(
                released, args.epigraph_maxiter
            )
            candidates = [inserted, frozen, released, polished]
            candidate_maxima = [
                search.max_inner(candidate) for candidate in candidates
            ]
            retained_index = int(np.argmin(candidate_maxima))
            retained = candidates[retained_index]
            final_edges = edge_set(retained, args.tight_tolerance)
            intersection = len(source_edges & final_edges)
            union = len(source_edges | final_edges)
            record = {
                "cardinality": cardinality,
                "restart": restart,
                "seed": seed,
                "cover_size": len(cover),
                "independent_size": len(independent),
                "insertion": insertion,
                "inserted": search.diagnostics(inserted),
                "freeze": freeze_record,
                "frozen": search.diagnostics(frozen),
                "release": release_record,
                "released": search.diagnostics(released),
                "epigraph_solver": solver,
                "polished": search.diagnostics(polished),
                "retained_stage": [
                    "inserted",
                    "frozen",
                    "released",
                    "polished",
                ][retained_index],
                "retained": {
                    **search.diagnostics(retained),
                    "coordinates_float64": retained.tolist(),
                },
                "tight_graph_comparison": {
                    "source_edges": len(source_edges),
                    "retained_edges": len(final_edges),
                    "intersection": intersection,
                    "symmetric_difference": len(
                        source_edges ^ final_edges
                    ),
                    "jaccard": intersection / union if union else 1,
                },
                "beats_source": (
                    search.max_inner(retained) < source_maximum - 1.0e-12
                ),
                "crosses_one_half": search.max_inner(retained) <= 0.5,
            }
            print(
                f"N={cardinality} restart={restart} cover={len(cover)} "
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
            key=lambda run: run["retained"]["maximum_inner_product"],
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
        "schema": "kissing5.construction_round11_block_reinsertion.v1",
        "evidence_status": (
            "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE"
        ),
        "source_files": {
            "portfolio": str(PORTFOLIO.relative_to(ROOT)),
            "polished": str(POLISHED.relative_to(ROOT)),
            **source_hashes,
        },
        "parameters": vars(args) | {"output": output_label},
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

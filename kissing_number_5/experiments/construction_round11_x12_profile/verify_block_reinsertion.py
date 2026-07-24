#!/usr/bin/env python3
"""Independent verifier for the tight-edge block-reinsertion experiment.

This checker does not call the search code or trust optimizer status.  It
recomputes coordinate diagnostics, tight graphs, minimum-cover optimality,
stress residuals, topology certificates, and best-of-run claims.  Stored
coordinates are binary64 approximations, so successful verification remains
NUMERICAL EVIDENCE ONLY.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "block_reinsertion.json"
TOPOLOGY = HERE / "results" / "block_topology.json"
EXPECTED_SOURCE_SHA256 = (
    "56cd11c284f9471df75af2cb77e8a6cb8cfe13372ad570f71d233149cda5f38c"
)
EXPECTED_TOPOLOGY_SHA256 = (
    "962a03d83a10f39a938d7693145bc96a71eabee138ae5108db487560226420e4"
)
EXPECTED_PORTFOLIO_SHA256 = (
    "38860d86b4df9eacf0c2c27c18a76cfa0a8012df6f83e6d53c4ef0328ca86c76"
)
EXPECTED_POLISHED_SHA256 = (
    "091c451b30a733123c5ebcda9da9ed80bd910b640aa1a6b0d1cd0eabad788b72"
)


class VerificationError(RuntimeError):
    """Raised when an independently recomputed claim fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def close(
    left: float, right: float, tolerance: float = 8.0e-13
) -> None:
    require(
        math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance),
        f"floating mismatch: {left!r} versus {right!r}",
    )


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise VerificationError(f"could not load verifier {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def coordinate_hash(array: np.ndarray) -> str:
    canonical = np.asarray(array, dtype="<f8", order="C")
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def explicit_products(
    array: np.ndarray,
) -> list[tuple[int, int, float]]:
    return [
        (
            first,
            second,
            math.fsum(
                float(array[first, coordinate])
                * float(array[second, coordinate])
                for coordinate in range(5)
            ),
        )
        for first in range(len(array))
        for second in range(first + 1, len(array))
    ]


def tight_graph(
    array: np.ndarray, tolerance: float
) -> tuple[float, float, list[tuple[int, int]], list[int]]:
    products = explicit_products(array)
    maximum = max(product for _, _, product in products)
    cutoff = maximum - tolerance
    edges = [
        (first, second)
        for first, second, product in products
        if product >= cutoff
    ]
    clearance = min(
        abs(product - cutoff) for _, _, product in products
    )
    adjacency = [0] * len(array)
    for first, second in edges:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    return maximum, clearance, edges, adjacency


def coordinate_statistics(array: np.ndarray) -> dict[str, object]:
    require(
        array.ndim == 2 and array.shape[1] == 5,
        "coordinate array has wrong shape",
    )
    gram = array @ array.T
    frame = array.T @ array
    first, second = np.triu_indices(len(array), 1)
    products = gram[first, second]
    norms = np.sum(array * array, axis=1)
    maximum = float(np.max(products))
    explicit_maximum = max(
        product for _, _, product in explicit_products(array)
    )
    close(maximum, explicit_maximum, 2.0e-14)
    violations = np.maximum(products - 0.5, 0)
    return {
        "maximum_inner_product": maximum,
        "minimum_inner_product": float(np.min(products)),
        "gap_above_one_half": maximum - 0.5,
        "violating_pair_count": int(
            np.count_nonzero(violations)
        ),
        "violation_l2": float(np.linalg.norm(violations)),
        "centroid_norm": float(
            np.linalg.norm(np.mean(array, axis=0))
        ),
        "trace_gram_squared": float(np.sum(frame * frame)),
        "trace_gram_cubed": float(
            np.trace(frame @ frame @ frame)
        ),
        "frame_eigenvalues": np.linalg.eigvalsh(frame).tolist(),
        "coordinate_little_endian_float64_sha256": (
            coordinate_hash(array)
        ),
        "unit_norm_maximum_residual": float(
            np.max(np.abs(norms - 1))
        ),
    }


def compare_statistics(
    stored: dict[str, object], computed: dict[str, object]
) -> None:
    for key in (
        "maximum_inner_product",
        "minimum_inner_product",
        "gap_above_one_half",
        "violation_l2",
        "centroid_norm",
        "trace_gram_squared",
        "trace_gram_cubed",
        "unit_norm_maximum_residual",
    ):
        close(float(stored[key]), float(computed[key]))
    require(
        stored["violating_pair_count"]
        == computed["violating_pair_count"],
        "violating-pair count mismatch",
    )
    require(
        stored["coordinate_little_endian_float64_sha256"]
        == computed[
            "coordinate_little_endian_float64_sha256"
        ],
        "coordinate hash mismatch",
    )
    require(
        len(stored["frame_eigenvalues"]) == 5,
        "frame spectrum has wrong length",
    )
    for left, right in zip(
        stored["frame_eigenvalues"],
        computed["frame_eigenvalues"],
    ):
        close(float(left), float(right))
    require(
        float(computed["unit_norm_maximum_residual"])
        <= 9.0e-16,
        "binary64 coordinates have excessive norm residual",
    )


def maximum_independent_size(
    adjacency: list[int],
) -> tuple[int, int]:
    """Exact Bron--Kerbosch search in the complement graph."""

    cardinality = len(adjacency)
    full = (1 << cardinality) - 1
    complement = [
        full ^ (1 << vertex) ^ adjacency[vertex]
        for vertex in range(cardinality)
    ]
    best = 0
    visited = 0

    def search(size: int, candidates: int, excluded: int) -> None:
        nonlocal best, visited
        visited += 1
        if size + candidates.bit_count() <= best:
            return
        if not candidates:
            if not excluded:
                best = max(best, size)
            return
        pivot_pool = candidates | excluded
        pivot = -1
        pivot_degree = -1
        while pivot_pool:
            bit = pivot_pool & -pivot_pool
            vertex = bit.bit_length() - 1
            degree = (
                candidates & complement[vertex]
            ).bit_count()
            if degree > pivot_degree:
                pivot = vertex
                pivot_degree = degree
            pivot_pool ^= bit
        branches = (
            candidates & ~complement[pivot] & full
        )
        while branches:
            bit = branches & -branches
            vertex = bit.bit_length() - 1
            search(
                size + 1,
                candidates & complement[vertex],
                excluded & complement[vertex],
            )
            candidates ^= bit
            excluded |= bit
            branches ^= bit
            if size + candidates.bit_count() <= best:
                break

    search(0, full, 0)
    return best, visited


def graph_invariants(adjacency: list[int]) -> dict[str, object]:
    cardinality = len(adjacency)
    degrees = sorted(mask.bit_count() for mask in adjacency)
    triangle_edge_sum = 0
    for first in range(cardinality):
        neighbors = adjacency[first]
        while neighbors:
            bit = neighbors & -neighbors
            second = bit.bit_length() - 1
            if second > first:
                triangle_edge_sum += (
                    adjacency[first] & adjacency[second]
                ).bit_count()
            neighbors ^= bit
    unseen = (1 << cardinality) - 1
    component_sizes = []
    while unseen:
        frontier = unseen & -unseen
        component = 0
        while frontier:
            component |= frontier
            unseen &= ~frontier
            new_frontier = 0
            remaining = frontier
            while remaining:
                bit = remaining & -remaining
                vertex = bit.bit_length() - 1
                new_frontier |= adjacency[vertex]
                remaining ^= bit
            frontier = new_frontier & unseen
        component_sizes.append(component.bit_count())
    return {
        "edge_count": sum(degrees) // 2,
        "degree_sequence": degrees,
        "triangle_count": triangle_edge_sum // 3,
        "component_sizes": sorted(component_sizes),
    }


def verify_mapping(
    first: list[int], second: list[int], mapping: list[int]
) -> None:
    cardinality = len(first)
    require(
        sorted(mapping) == list(range(cardinality)),
        "isomorphism mapping is not a permutation",
    )
    for left in range(cardinality):
        for right in range(cardinality):
            require(
                ((first[left] >> right) & 1)
                == (
                    (
                        second[mapping[left]]
                        >> mapping[right]
                    )
                    & 1
                ),
                "stored mapping does not preserve adjacency",
            )


def verify_stress(
    array: np.ndarray,
    edges: list[tuple[int, int]],
    record: dict[str, object],
) -> float:
    weights = np.asarray(record["weights"], dtype=float)
    require(
        weights.shape == (len(edges),),
        "stress weight vector has wrong length",
    )
    require(
        float(np.min(weights, initial=0)) >= -1.0e-15,
        "stress has a negative weight",
    )
    gram = array @ array.T
    matrix = np.zeros((5 * len(array) + 1, len(edges)))
    matrix[-1] = 1
    incidence = np.zeros(len(array))
    for index, (first, second) in enumerate(edges):
        product = gram[first, second]
        matrix[5 * first : 5 * first + 5, index] = (
            array[second] - product * array[first]
        )
        matrix[5 * second : 5 * second + 5, index] = (
            array[first] - product * array[second]
        )
        incidence[first] += weights[index]
        incidence[second] += weights[index]
    target = np.zeros(5 * len(array) + 1)
    target[-1] = 1
    residual = float(np.linalg.norm(matrix @ weights - target))
    close(
        float(record["weight_sum"]),
        float(np.sum(weights)),
        2.0e-13,
    )
    close(
        float(record["residual_norm"]), residual, 5.0e-15
    )
    require(
        record["support_size_at_1e-10"]
        == int(np.count_nonzero(weights > 1.0e-10)),
        "stress support size mismatch",
    )
    for left, right in zip(
        record["vertex_incidence_weights"], incidence
    ):
        close(float(left), float(right), 2.0e-13)
    require(
        residual <= 2.4e-8,
        "reported approximate equilibrium residual is too large",
    )
    return residual


def exact_binary64_maximum(
    array: np.ndarray,
) -> tuple[Fraction, tuple[int, int]]:
    best: Fraction | None = None
    pair = (-1, -1)
    for first in range(len(array)):
        for second in range(first + 1, len(array)):
            product = sum(
                Fraction.from_float(float(array[first, coordinate]))
                * Fraction.from_float(
                    float(array[second, coordinate])
                )
                for coordinate in range(5)
            )
            if best is None or product > best:
                best = product
                pair = (first, second)
    assert best is not None
    return best, pair


def verify(
    source_path: Path = SOURCE,
    topology_path: Path = TOPOLOGY,
    *,
    enforce_pinned_hashes: bool = True,
) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    topology_bytes = topology_path.read_bytes()
    if enforce_pinned_hashes:
        require(
            hashlib.sha256(source_bytes).hexdigest()
            == EXPECTED_SOURCE_SHA256,
            "block-reinsertion artifact hash mismatch",
        )
        require(
            hashlib.sha256(topology_bytes).hexdigest()
            == EXPECTED_TOPOLOGY_SHA256,
            "topology artifact hash mismatch",
        )
    source = json.loads(source_bytes)
    topology = json.loads(topology_bytes)
    require(
        source["schema"]
        == "kissing5.construction_round11_block_reinsertion.v1",
        "wrong block-reinsertion schema",
    )
    require(
        source["evidence_status"]
        == "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE",
        "unsafe block-reinsertion evidence status",
    )
    require(
        topology["schema"]
        == "kissing5.block_reinsertion_topology.v1",
        "wrong topology schema",
    )
    require(
        "NUMERICAL EVIDENCE ONLY" in topology["evidence_status"],
        "unsafe topology evidence status",
    )
    require(
        topology["source_sha256"]
        == hashlib.sha256(source_bytes).hexdigest(),
        "topology provenance mismatch",
    )

    parameters = source["parameters"]
    require(
        parameters
        == {
            "restarts": 4,
            "seed_base": 2026072800,
            "candidates_per_vertex": 350,
            "freeze_iterations": 1300,
            "release_iterations": 1300,
            "epigraph_maxiter": 700,
            "tight_tolerance": 0.0005,
            "output": (
                "experiments/construction_round11_x12_profile/"
                "results/block_reinsertion.json"
            ),
        },
        "unexpected search parameters",
    )
    tolerance = float(parameters["tight_tolerance"])

    portfolio_path = ROOT / source["source_files"]["portfolio"]
    polished_path = ROOT / source["source_files"]["polished"]
    portfolio_bytes = portfolio_path.read_bytes()
    polished_bytes = polished_path.read_bytes()
    require(
        hashlib.sha256(portfolio_bytes).hexdigest()
        == source["source_files"]["portfolio_sha256"]
        == EXPECTED_PORTFOLIO_SHA256,
        "portfolio provenance mismatch",
    )
    require(
        hashlib.sha256(polished_bytes).hexdigest()
        == source["source_files"]["polished_sha256"]
        == EXPECTED_POLISHED_SHA256,
        "polished provenance mismatch",
    )
    portfolio_verifier = load_module(
        "block_portfolio_verifier", HERE / "verify.py"
    )
    polished_verifier = load_module(
        "block_polished_verifier", HERE / "verify_polished.py"
    )
    portfolio_verifier.verify(portfolio_path)
    polished_verifier.verify(polished_path)

    portfolio = json.loads(portfolio_bytes)
    polished = json.loads(polished_bytes)
    expected_sources: dict[int, np.ndarray] = {}
    for cardinality in range(41, 44):
        run = next(
            candidate
            for candidate in portfolio["runs"]
            if candidate["cardinality"] == cardinality
        )
        raw = np.asarray(
            run["best"]["coordinates_float64"], dtype=float
        )
        expected_sources[cardinality] = (
            raw / np.linalg.norm(raw, axis=1)[:, None]
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
    raw44 = np.asarray(
        best44["retained"]["coordinates_float64"], dtype=float
    )
    expected_sources[44] = (
        raw44 / np.linalg.norm(raw44, axis=1)[:, None]
    )

    analyses = source["analyses"]
    require(len(analyses) == 4, "expected four source analyses")
    analysis_by_n = {
        int(analysis["cardinality"]): analysis
        for analysis in analyses
    }
    require(
        sorted(analysis_by_n) == [41, 42, 43, 44],
        "source analyses do not cover N=41,...,44",
    )
    exact_cover_nodes = {}
    stress_residuals = {}
    source_graphs = {}
    source_arrays = {}
    for cardinality, analysis in analysis_by_n.items():
        array = np.asarray(
            analysis["source"]["coordinates_float64"],
            dtype=float,
        )
        require(
            np.array_equal(array, expected_sources[cardinality]),
            "stored source coordinates do not match provenance",
        )
        compare_statistics(
            analysis["source"], coordinate_statistics(array)
        )
        maximum, clearance, edges, adjacency = tight_graph(
            array, tolerance
        )
        close(
            maximum,
            float(
                analysis["source"]["maximum_inner_product"]
            ),
            2.0e-14,
        )
        require(
            clearance >= 1.0e-5,
            "source tight-graph cutoff is numerically ambiguous",
        )
        stored_edges = [
            tuple(edge) for edge in analysis["tight_edges"]
        ]
        require(edges == stored_edges, "tight-edge list mismatch")
        require(
            analysis["tight_edge_count"] == len(edges),
            "tight-edge count mismatch",
        )
        independent = analysis["maximum_independent_set"]
        cover = analysis["minimum_vertex_cover"]
        require(
            sorted(independent + cover)
            == list(range(cardinality))
            and set(independent).isdisjoint(cover),
            "cover/independent partition mismatch",
        )
        require(
            all(
                not ((adjacency[first] >> second) & 1)
                for index, first in enumerate(independent)
                for second in independent[index + 1 :]
            ),
            "stored independent set contains an edge",
        )
        require(
            all(
                first in cover or second in cover
                for first, second in edges
            ),
            "stored vertex cover misses an edge",
        )
        alpha, visited = maximum_independent_size(adjacency)
        require(
            alpha == len(independent),
            "stored vertex cover is not minimum",
        )
        exact_cover_nodes[str(cardinality)] = visited
        stress_residuals[str(cardinality)] = verify_stress(
            array, edges, analysis["stress"]
        )
        source_graphs[cardinality] = adjacency
        source_arrays[cardinality] = array

    runs = source["runs"]
    require(len(runs) == 16, "expected sixteen restart records")
    seen = set()
    recomputed_runs: dict[tuple[int, int], dict[str, object]] = {}
    for run in runs:
        cardinality = int(run["cardinality"])
        restart = int(run["restart"])
        require(
            (cardinality, restart) not in seen,
            "duplicate restart record",
        )
        seen.add((cardinality, restart))
        require(
            cardinality in analysis_by_n and 0 <= restart < 4,
            "invalid restart target",
        )
        expected_seed = (
            2026072800 + 100 * (cardinality - 41) + restart
        )
        require(run["seed"] == expected_seed, "wrong restart seed")
        analysis = analysis_by_n[cardinality]
        cover = analysis["minimum_vertex_cover"]
        independent = analysis["maximum_independent_set"]
        require(
            run["cover_size"] == len(cover)
            and run["independent_size"] == len(independent),
            "run cover dimensions mismatch",
        )
        require(
            sorted(run["insertion"]["insertion_order"])
            == sorted(cover),
            "insertion order is not a permutation of the cover",
        )
        require(
            run["insertion"]["candidates_per_vertex"] == 350,
            "wrong cap candidate count",
        )
        require(
            0.35
            <= run["insertion"]["cap_radius_minimum"]
            <= run["insertion"]["cap_radius_maximum"]
            <= 1.15
            and 0.25
            <= run["insertion"]["cap_center_offset_minimum"]
            <= run["insertion"]["cap_center_offset_maximum"]
            <= 0.95,
            "asymmetric cap range is out of bounds",
        )
        require(
            run["freeze"]["iterations"] == 1300
            and run["freeze"]["movable_count"] == len(cover)
            and run["freeze"]["frozen_count"]
            == len(independent),
            "frozen-block schedule mismatch",
        )
        require(
            run["release"]["iterations"] == 1300
            and run["release"]["movable_count"] == cardinality
            and run["release"]["frozen_count"] == 0,
            "full-release schedule mismatch",
        )
        for phase in ("freeze", "release"):
            history = run[phase]["history"]
            require(
                history
                and history[-1]["iteration"] == 1300,
                f"{phase} history is incomplete",
            )
        require(
            run["epigraph_solver"]["iterations"] <= 700,
            "epigraph polish exceeded its iteration budget",
        )
        stage_maxima = {
            stage: float(
                run[
                    {
                        "inserted": "inserted",
                        "frozen": "frozen",
                        "released": "released",
                        "polished": "polished",
                    }[stage]
                ]["maximum_inner_product"]
            )
            for stage in (
                "inserted",
                "frozen",
                "released",
                "polished",
            )
        }
        require(
            run["retained_stage"]
            == min(stage_maxima, key=stage_maxima.get),
            "retained stage is not the best stored phase",
        )
        array = np.asarray(
            run["retained"]["coordinates_float64"], dtype=float
        )
        statistics = coordinate_statistics(array)
        compare_statistics(run["retained"], statistics)
        close(
            float(
                run[run["retained_stage"]][
                    "maximum_inner_product"
                ]
            ),
            float(statistics["maximum_inner_product"]),
        )
        maximum, clearance, edges, adjacency = tight_graph(
            array, tolerance
        )
        require(
            clearance >= 1.0e-5,
            "retained tight-graph cutoff is numerically ambiguous",
        )
        source_edges = {
            tuple(edge) for edge in analysis["tight_edges"]
        }
        final_edges = set(edges)
        intersection = len(source_edges & final_edges)
        union = len(source_edges | final_edges)
        comparison = run["tight_graph_comparison"]
        require(
            comparison["source_edges"] == len(source_edges)
            and comparison["retained_edges"] == len(final_edges)
            and comparison["intersection"] == intersection
            and comparison["symmetric_difference"]
            == len(source_edges ^ final_edges),
            "tight-graph comparison mismatch",
        )
        close(
            comparison["jaccard"],
            intersection / union if union else 1.0,
        )
        source_maximum = float(
            analysis["source"]["maximum_inner_product"]
        )
        require(
            run["beats_source"]
            == (maximum < source_maximum - 1.0e-12),
            "source-improvement flag mismatch",
        )
        require(
            run["crosses_one_half"] == (maximum <= 0.5),
            "one-half crossing flag mismatch",
        )
        recomputed_runs[(cardinality, restart)] = {
            "maximum": maximum,
            "hash": coordinate_hash(array),
            "adjacency": adjacency,
            "array": array,
        }

    require(
        not source["exact_candidate_found"]
        and not any(run["crosses_one_half"] for run in runs),
        "artifact incorrectly reports an exact construction",
    )
    best_exact = {}
    for cardinality in range(41, 45):
        candidates = [
            run
            for run in runs
            if run["cardinality"] == cardinality
        ]
        best = min(
            candidates,
            key=lambda run: run["retained"][
                "maximum_inner_product"
            ],
        )
        summary = source["best_by_n"][str(cardinality)]
        require(
            summary["restart"] == best["restart"]
            and summary["coordinate_sha256"]
            == best["retained"][
                "coordinate_little_endian_float64_sha256"
            ]
            and summary["beats_source"] == best["beats_source"],
            "best-by-cardinality summary mismatch",
        )
        close(
            summary["maximum_inner_product"],
            best["retained"]["maximum_inner_product"],
        )
        array = recomputed_runs[
            (cardinality, int(best["restart"]))
        ]["array"]
        rational_maximum, pair = exact_binary64_maximum(array)
        best_exact[str(cardinality)] = {
            "restart": int(best["restart"]),
            "maximizing_pair": list(pair),
            "exact_binary64_dot_numerator": str(
                rational_maximum.numerator
            ),
            "exact_binary64_dot_denominator": str(
                rational_maximum.denominator
            ),
            "decimal_18_digits": (
                f"{float(rational_maximum):.18f}"
            ),
        }

    topology_reports = {
        (int(report["cardinality"]), int(report["restart"])): report
        for report in topology["reports"]
    }
    require(
        len(topology_reports) == 16,
        "topology report count mismatch",
    )
    nonisomorphic_count = 0
    for key, recomputed in recomputed_runs.items():
        cardinality, _restart = key
        report = topology_reports[key]
        source_adjacency = source_graphs[cardinality]
        retained_adjacency = recomputed["adjacency"]
        require(
            report["source_graph"]
            == graph_invariants(source_adjacency)
            and report["retained_graph"]
            == graph_invariants(retained_adjacency),
            "topology invariant mismatch",
        )
        mapping = report["source_to_retained_isomorphism"]
        if report["isomorphic_to_source"]:
            require(mapping is not None, "missing isomorphism")
            verify_mapping(
                source_adjacency, retained_adjacency, mapping
            )
            source_gram = (
                source_arrays[cardinality]
                @ source_arrays[cardinality].T
            )
            retained_array = recomputed["array"]
            retained_gram = retained_array @ retained_array.T
            difference = float(
                np.max(
                    np.abs(
                        source_gram
                        - retained_gram[np.ix_(mapping, mapping)]
                    )
                )
            )
            close(
                report["mapped_gram_maximum_difference"],
                difference,
            )
        else:
            # All negative instances in this artifact have distinct edge
            # counts, a particularly simple exact nonisomorphism witness.
            require(
                report["source_graph"]["edge_count"]
                != report["retained_graph"]["edge_count"],
                "nonisomorphism lacks its edge-count witness",
            )
            require(mapping is None, "unexpected mapping")
            nonisomorphic_count += 1
        require(
            report["topology_changed_up_to_isomorphism"]
            == (not report["isomorphic_to_source"]),
            "topology-change flag mismatch",
        )
    require(
        topology["summary"]
        == {
            "run_count": 16,
            "nonisomorphic_to_source_count": nonisomorphic_count,
            "strict_improvement_count": 0,
        },
        "topology summary mismatch",
    )
    require(
        nonisomorphic_count == 14,
        "unexpected topology-change count",
    )

    return {
        "status": (
            "block-reinsertion numerical artifact independently "
            "verified"
        ),
        "evidence_status": "NUMERICAL EVIDENCE ONLY",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "topology_sha256": hashlib.sha256(
            topology_bytes
        ).hexdigest(),
        "minimum_cover_sizes": {
            str(n): len(
                analysis_by_n[n]["minimum_vertex_cover"]
            )
            for n in range(41, 45)
        },
        "independent_cover_search_nodes": exact_cover_nodes,
        "recomputed_stress_residuals": stress_residuals,
        "nonisomorphic_restart_count": nonisomorphic_count,
        "strict_improvement_count": 0,
        "exact_candidate_found": False,
        "best_binary64_coordinates": best_exact,
    }


def main() -> None:
    try:
        report = verify()
    except (
        AssertionError,
        KeyError,
        TypeError,
        ValueError,
        VerificationError,
    ) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

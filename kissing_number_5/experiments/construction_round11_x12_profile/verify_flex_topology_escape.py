#!/usr/bin/env python3
"""Independent verifier for the global rigidity-mode escape search.

No optimizer code is imported.  Rigidity spectra are recomputed using
eigendecomposition-based tangent bases, different from the SVD bases used
by discovery.  All conclusions remain numerical.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = HERE / "results" / "flex_topology_escape.json"
TOPOLOGY = HERE / "results" / "flex_topology.json"
EXPECTED_SOURCE_SHA256 = (
    "99ced8d38911388276d9c534b254f751ca6498d3c05e60626357bde7615902cc"
)
EXPECTED_TOPOLOGY_SHA256 = (
    "54f87082ccd5633435c7bde5c9daa79a29e7c02ed029e1cc5cf5839ca825ce03"
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
    left: float, right: float, tolerance: float = 1.0e-12
) -> None:
    require(
        math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance),
        f"floating mismatch: {left!r} versus {right!r}",
    )


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise VerificationError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_module(
    "flex_base_independent_verifier",
    HERE / "verify_block_reinsertion.py",
)
portfolio_verifier = load_module(
    "flex_portfolio_independent_verifier", HERE / "verify.py"
)
polished_verifier = load_module(
    "flex_polished_independent_verifier",
    HERE / "verify_polished.py",
)


def alternate_rigidity_spectrum(
    array: np.ndarray, edges: list[tuple[int, int]]
) -> dict[str, object]:
    cardinality = len(array)
    bases = []
    for point in array:
        projector = np.eye(5) - np.outer(point, point)
        eigenvalues, eigenvectors = np.linalg.eigh(projector)
        basis = eigenvectors[:, eigenvalues > 0.5]
        require(
            basis.shape == (5, 4),
            "alternate tangent basis has wrong dimension",
        )
        bases.append(basis)
    bases = np.asarray(bases)
    gram = array @ array.T
    rigidity = np.zeros((len(edges), 4 * cardinality))
    for row, (first, second) in enumerate(edges):
        product = gram[first, second]
        rigidity[row, 4 * first : 4 * first + 4] = (
            bases[first].T
            @ (array[second] - product * array[first])
        )
        rigidity[row, 4 * second : 4 * second + 4] = (
            bases[second].T
            @ (array[first] - product * array[second])
        )

    rotations = []
    for first in range(5):
        for second in range(first + 1, 5):
            displacement = np.zeros_like(array)
            displacement[:, first] = -array[:, second]
            displacement[:, second] = array[:, first]
            rotations.append(
                np.concatenate(
                    [
                        bases[vertex].T
                        @ displacement[vertex]
                        for vertex in range(cardinality)
                    ]
                )
            )
    rotation_matrix = np.column_stack(rotations)
    require(
        np.linalg.matrix_rank(
            rotation_matrix, tol=1.0e-10
        )
        == 10,
        "alternate rotation space has wrong dimension",
    )
    complete_q, _r = np.linalg.qr(
        rotation_matrix, mode="complete"
    )
    rotation_q = complete_q[:, :10]
    nonrotating = complete_q[:, 10:]
    reduced = rigidity @ nonrotating
    singular = np.linalg.svd(reduced, compute_uv=False)
    padded = np.zeros(nonrotating.shape[1])
    padded[: len(singular)] = singular
    padded.sort()
    return {
        "tangent_dimension": 4 * cardinality,
        "nonrotation_dimension": nonrotating.shape[1],
        "rank_at_1e-9": int(np.count_nonzero(padded > 1.0e-9)),
        "nullity_at_1e-9": int(
            np.count_nonzero(padded <= 1.0e-9)
        ),
        "smallest": padded[: min(30, len(padded))],
        "rotation_residual": float(
            np.linalg.norm(rigidity @ rotation_q, ord=2)
        ),
        "basis_residual": float(
            max(
                np.max(
                    np.abs(
                        basis.T @ basis - np.eye(4)
                    )
                )
                for basis in bases
            )
        ),
    }


def expected_sources(
    portfolio: dict[str, object], polished: dict[str, object]
) -> dict[int, np.ndarray]:
    sources = {}
    for cardinality in range(41, 44):
        run = next(
            candidate
            for candidate in portfolio["runs"]
            if candidate["cardinality"] == cardinality
        )
        raw = np.asarray(
            run["best"]["coordinates_float64"], dtype=float
        )
        sources[cardinality] = (
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
    raw = np.asarray(
        best44["retained"]["coordinates_float64"], dtype=float
    )
    sources[44] = raw / np.linalg.norm(raw, axis=1)[:, None]
    return sources


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
            "flex artifact hash mismatch",
        )
        require(
            hashlib.sha256(topology_bytes).hexdigest()
            == EXPECTED_TOPOLOGY_SHA256,
            "flex topology artifact hash mismatch",
        )
    source = json.loads(source_bytes)
    topology = json.loads(topology_bytes)
    require(
        source["schema"] == "kissing5.flex_topology_escape.v1",
        "wrong flex schema",
    )
    require(
        source["evidence_status"]
        == "NUMERICAL EVIDENCE ONLY; NOT AN EXACT CONFIGURATION CERTIFICATE",
        "unsafe flex evidence status",
    )
    require(
        topology["schema"] == "kissing5.flex_topology.v1",
        "wrong flex topology schema",
    )
    require(
        "NUMERICAL EVIDENCE ONLY" in topology["evidence_status"],
        "unsafe topology evidence status",
    )
    require(
        topology["source_sha256"]
        == hashlib.sha256(source_bytes).hexdigest(),
        "flex topology provenance mismatch",
    )
    require(
        source["parameters"]
        == {
            "restarts": 4,
            "seed_base": 2026073000,
            "mode_count": 28,
            "kick_candidates": 48,
            "switch_iterations": 900,
            "release_iterations": 1400,
            "epigraph_maxiter": 700,
            "tight_tolerance": 0.0005,
            "output": (
                "experiments/construction_round11_x12_profile/"
                "results/flex_topology_escape.json"
            ),
        },
        "unexpected flex parameters",
    )
    require(
        source["amplitudes"] == [0.08, 0.16, 0.28, 0.45],
        "wrong flex amplitude schedule",
    )

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
        "polish provenance mismatch",
    )
    portfolio_verifier.verify(portfolio_path)
    polished_verifier.verify(polished_path)
    expected = expected_sources(
        json.loads(portfolio_bytes), json.loads(polished_bytes)
    )

    analyses = {
        int(record["cardinality"]): record
        for record in source["analyses"]
    }
    require(
        sorted(analyses) == [41, 42, 43, 44]
        and len(source["analyses"]) == 4,
        "wrong source-analysis coverage",
    )
    tolerance = float(source["parameters"]["tight_tolerance"])
    source_graphs = {}
    source_arrays = {}
    rigidity_summary = {}
    for cardinality, analysis in analyses.items():
        array = np.asarray(
            analysis["source"]["coordinates_float64"], dtype=float
        )
        require(
            np.array_equal(array, expected[cardinality]),
            "source coordinate provenance mismatch",
        )
        base.compare_statistics(
            analysis["source"], base.coordinate_statistics(array)
        )
        maximum, clearance, edges, adjacency = base.tight_graph(
            array, tolerance
        )
        close(
            maximum,
            analysis["source"]["maximum_inner_product"],
            2.0e-14,
        )
        require(
            clearance >= 1.0e-5,
            "source tight graph is cutoff-ambiguous",
        )
        require(
            edges
            == [tuple(edge) for edge in analysis["tight_edges"]],
            "source tight edges mismatch",
        )
        alternate = alternate_rigidity_spectrum(array, edges)
        stored = analysis["rigidity"]
        require(
            stored["tight_edge_count"] == len(edges)
            and stored["tangent_dimension"]
            == alternate["tangent_dimension"]
            and stored["rotation_dimension"] == 10
            and stored["nonrotation_dimension"]
            == alternate["nonrotation_dimension"],
            "rigidity dimensions mismatch",
        )
        require(
            stored["reduced_rigidity_rank_at_1e-9"]
            == alternate["rank_at_1e-9"]
            and stored["reduced_rigidity_nullity_at_1e-9"]
            == alternate["nullity_at_1e-9"],
            "rigidity rank/nullity mismatch",
        )
        for left, right in zip(
            stored["smallest_reduced_singular_values"],
            alternate["smallest"],
        ):
            close(float(left), float(right), 5.0e-12)
        selected_residuals = np.sort(
            np.asarray(
                stored["selected_mode_rigidity_residuals"],
                dtype=float,
            )
        )
        smallest_selected = alternate["smallest"][
            : stored["selected_mode_count"]
        ]
        require(
            len(selected_residuals)
            == stored["selected_mode_count"] == 28,
            "selected flex-mode count mismatch",
        )
        for left, right in zip(
            selected_residuals, smallest_selected
        ):
            close(float(left), float(right), 5.0e-12)
        require(
            stored["rotation_rigidity_operator_norm"]
            <= 1.0e-14
            and alternate["rotation_residual"] <= 1.0e-14
            and stored["tangent_basis_maximum_residual"]
            <= 2.0e-15
            and alternate["basis_residual"] <= 2.0e-15,
            "rotation/tangent residual too large",
        )
        source_graphs[cardinality] = adjacency
        source_arrays[cardinality] = array
        rigidity_summary[str(cardinality)] = {
            "rank_at_1e-9": alternate["rank_at_1e-9"],
            "nullity_at_1e-9": alternate["nullity_at_1e-9"],
            "smallest_nonrotating_singular_value": float(
                alternate["smallest"][0]
            ),
        }

    runs = source["runs"]
    require(len(runs) == 16, "expected sixteen flex restarts")
    seen = set()
    recomputed = {}
    for run in runs:
        cardinality = int(run["cardinality"])
        restart = int(run["restart"])
        require(
            (cardinality, restart) not in seen,
            "duplicate flex restart",
        )
        seen.add((cardinality, restart))
        require(
            41 <= cardinality <= 44 and 0 <= restart < 4,
            "invalid flex restart",
        )
        require(
            run["seed"]
            == 2026073000 + 100 * (cardinality - 41) + restart,
            "wrong flex seed",
        )
        require(
            run["amplitude"]
            == [0.08, 0.16, 0.28, 0.45][restart],
            "wrong flex amplitude",
        )
        kick = run["kick"]
        require(
            kick["candidate_count"] == 48
            and 0 <= kick["selected_candidate"] < 48
            and kick["selected_old_edge_overlap"]
            <= len(analyses[cardinality]["tight_edges"]),
            "kick selection metadata mismatch",
        )
        close(
            kick["selected_maximum_inner_product"],
            run["kicked"]["maximum_inner_product"],
        )
        optimization = run["optimization"]
        require(
            optimization["switch_iterations"] == 900
            and optimization["release_iterations"] == 1400
            and optimization[
                "old_edge_penalty_final_released_weight"
            ]
            == 0,
            "switch/release schedule mismatch",
        )
        history = optimization["history"]
        require(
            history
            and history[-1]["iteration"] == 2300
            and history[-1]["phase"] == "release"
            and history[-1]["old_edge_penalty_weight"] == 0,
            "penalty-free release is incomplete",
        )
        require(
            run["epigraph_solver"]["iterations"] <= 700,
            "epigraph iteration budget exceeded",
        )
        stage_maxima = {
            stage: float(
                run[stage]["maximum_inner_product"]
            )
            for stage in ("kicked", "escaped", "polished")
        }
        require(
            run["retained_stage"]
            == min(stage_maxima, key=stage_maxima.get),
            "retained flex stage is not best",
        )
        array = np.asarray(
            run["retained"]["coordinates_float64"], dtype=float
        )
        statistics = base.coordinate_statistics(array)
        base.compare_statistics(run["retained"], statistics)
        close(
            stage_maxima[run["retained_stage"]],
            statistics["maximum_inner_product"],
        )
        maximum, clearance, edges, adjacency = base.tight_graph(
            array, tolerance
        )
        require(
            clearance >= 6.0e-6,
            "retained tight graph is cutoff-ambiguous",
        )
        source_edges = {
            tuple(edge)
            for edge in analyses[cardinality]["tight_edges"]
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
            "flex tight-graph comparison mismatch",
        )
        close(
            comparison["jaccard"],
            intersection / union if union else 1,
        )
        source_maximum = float(
            analyses[cardinality]["source"][
                "maximum_inner_product"
            ]
        )
        require(
            run["beats_source"]
            == (maximum < source_maximum - 1.0e-12),
            "flex source-improvement flag mismatch",
        )
        require(
            run["crosses_one_half"] == (maximum <= 0.5),
            "flex threshold flag mismatch",
        )
        recomputed[(cardinality, restart)] = {
            "array": array,
            "maximum": maximum,
            "hash": base.coordinate_hash(array),
            "adjacency": adjacency,
        }
    require(
        not source["exact_candidate_found"]
        and not any(run["crosses_one_half"] for run in runs),
        "flex search incorrectly claims an exact construction",
    )

    exact_best = {}
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
            "flex best-by-N summary mismatch",
        )
        close(
            summary["maximum_inner_product"],
            best["retained"]["maximum_inner_product"],
        )
        rational, pair = base.exact_binary64_maximum(
            recomputed[(cardinality, int(best["restart"]))][
                "array"
            ]
        )
        exact_best[str(cardinality)] = {
            "restart": int(best["restart"]),
            "maximum": float(rational),
            "maximizing_pair": list(pair),
            "numerator": str(rational.numerator),
            "denominator": str(rational.denominator),
        }

    reports = {
        (int(report["cardinality"]), int(report["restart"])): report
        for report in topology["reports"]
    }
    require(len(reports) == 16, "wrong flex topology report count")
    nonisomorphic = 0
    for key, record in recomputed.items():
        cardinality, _restart = key
        report = reports[key]
        source_adjacency = source_graphs[cardinality]
        retained_adjacency = record["adjacency"]
        require(
            report["source_graph"]
            == base.graph_invariants(source_adjacency)
            and report["retained_graph"]
            == base.graph_invariants(retained_adjacency),
            "flex topology invariants mismatch",
        )
        mapping = report["source_to_retained_isomorphism"]
        if report["isomorphic_to_source"]:
            require(mapping is not None, "missing flex isomorphism")
            base.verify_mapping(
                source_adjacency, retained_adjacency, mapping
            )
            source_gram = (
                source_arrays[cardinality]
                @ source_arrays[cardinality].T
            )
            retained_gram = (
                record["array"] @ record["array"].T
            )
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
            require(
                report["source_graph"]["edge_count"]
                != report["retained_graph"]["edge_count"],
                "negative flex isomorphism lacks edge-count witness",
            )
            require(mapping is None, "unexpected flex mapping")
            nonisomorphic += 1
        require(
            report["topology_changed_up_to_isomorphism"]
            == (not report["isomorphic_to_source"]),
            "flex topology-change flag mismatch",
        )
    require(
        topology["summary"]
        == {
            "run_count": 16,
            "nonisomorphic_to_source_count": nonisomorphic,
            "strict_improvement_count": 0,
        }
        and nonisomorphic == 9,
        "flex topology summary mismatch",
    )

    return {
        "status": (
            "global rigidity-mode topology escape "
            "independently verified"
        ),
        "evidence_status": "NUMERICAL EVIDENCE ONLY",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "topology_sha256": hashlib.sha256(
            topology_bytes
        ).hexdigest(),
        "rigidity_at_threshold_1e-9": rigidity_summary,
        "nonisomorphic_restart_count": nonisomorphic,
        "strict_improvement_count": 0,
        "exact_candidate_found": False,
        "best_binary64_coordinates": exact_best,
    }


def main() -> None:
    try:
        result = verify()
    except (
        AssertionError,
        KeyError,
        TypeError,
        ValueError,
        VerificationError,
        base.VerificationError,
    ) as error:
        print(f"verification failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

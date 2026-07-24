#!/usr/bin/env python3
"""Independent numerical verifier for gram_search_results.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEFAULT_INPUT = HERE / "gram_search_results.json"
DEFAULT_OUTPUT = HERE / "gram_verification.json"
TOLERANCE = 5e-13


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coordinate_hash(points: np.ndarray) -> str:
    normalized = points / np.linalg.norm(points, axis=1)[:, None]
    little_endian = np.asarray(normalized, dtype="<f8", order="C")
    return hashlib.sha256(little_endian.tobytes(order="C")).hexdigest()


def recompute(points: np.ndarray) -> dict[str, Any]:
    n = len(points)
    gram = points @ points.T
    upper = np.triu_indices(n, 1)
    values = gram[upper]
    excess = np.maximum(values - 0.5, 0.0)
    eigenvalues = np.linalg.eigvalsh(gram)
    norms_squared = np.sum(points * points, axis=1)
    maximum = float(np.max(values))
    active_edges = [
        (int(i), int(j))
        for i, j, value in zip(*upper, values, strict=True)
        if value >= maximum - 1e-8
    ]
    degree = np.zeros(n, dtype=np.int64)
    adjacency = [[] for _ in range(n)]
    for i, j in active_edges:
        degree[i] += 1
        degree[j] += 1
        adjacency[i].append(j)
        adjacency[j].append(i)
    unseen = set(range(n))
    component_sizes: list[int] = []
    while unseen:
        vertex = unseen.pop()
        stack = [vertex]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        component_sizes.append(size)
    degree_values, degree_counts = np.unique(degree, return_counts=True)
    return {
        "maximum_inner_product": maximum,
        "gap_above_one_half": maximum - 0.5,
        "minimum_inner_product": float(np.min(values)),
        "violating_pair_count": int(np.count_nonzero(values > 0.5)),
        "violation_l2": float(np.linalg.norm(excess)),
        "violation_l1": float(np.sum(excess)),
        "unit_norm_residual": float(np.max(np.abs(norms_squared - 1.0))),
        "gram_eigenvalues_ascending": eigenvalues,
        "gram_minimum_eigenvalue": float(eigenvalues[0]),
        "gram_sixth_largest_eigenvalue_absolute": float(
            np.max(np.abs(eigenvalues[:-5]))
        ),
        "numerical_rank_at_1e-10": int(np.count_nonzero(eigenvalues > 1e-10)),
        "coordinate_little_endian_float64_sha256": coordinate_hash(points),
        "pairs_within_1e-8_of_maximum": len(active_edges),
        "near_max_graph_component_sizes": sorted(component_sizes, reverse=True),
        "near_max_graph_degree_histogram": {
            str(int(value)): int(count)
            for value, count in zip(degree_values, degree_counts, strict=True)
        },
    }


def close(actual: float, expected: float, label: str) -> None:
    if not np.isfinite(actual) or not np.isfinite(expected):
        raise AssertionError(f"{label}: nonfinite value")
    if abs(actual - expected) > TOLERANCE:
        raise AssertionError(f"{label}: {actual!r} != {expected!r}")


def verify_best(n_text: str, record: dict[str, Any]) -> dict[str, Any]:
    n = int(n_text)
    points = np.asarray(record["coordinates_float64"], dtype=np.float64)
    if points.shape != (n, 5):
        raise AssertionError(f"N={n}: coordinate shape {points.shape}")
    if not np.all(np.isfinite(points)):
        raise AssertionError(f"N={n}: nonfinite coordinate")
    check = recompute(points)
    reported_objective = record["best_objective"]
    for key in (
        "maximum_inner_product",
        "gap_above_one_half",
        "violation_l2",
        "violation_l1",
    ):
        close(check[key], float(reported_objective[key]), f"N={n} objective {key}")
    if check["violating_pair_count"] != reported_objective["violating_pair_count"]:
        raise AssertionError(f"N={n}: violation count mismatch")

    reported_diagnostics = record["diagnostics"]
    if (
        check["coordinate_little_endian_float64_sha256"]
        != reported_diagnostics["coordinate_little_endian_float64_sha256"]
    ):
        raise AssertionError(f"N={n}: coordinate hash mismatch")
    close(
        check["maximum_inner_product"],
        reported_diagnostics["maximum_inner_product_binary64"],
        f"N={n} diagnostic maximum",
    )
    close(
        check["minimum_inner_product"],
        reported_diagnostics["minimum_inner_product_binary64"],
        f"N={n} diagnostic minimum",
    )
    if (
        check["pairs_within_1e-8_of_maximum"]
        != reported_diagnostics["pairs_within_1e-8_of_maximum"]
    ):
        raise AssertionError(f"N={n}: active-edge count mismatch")
    if (
        check["near_max_graph_component_sizes"]
        != reported_diagnostics["near_max_graph_component_sizes"]
    ):
        raise AssertionError(f"N={n}: active component mismatch")
    if (
        check["near_max_graph_degree_histogram"]
        != reported_diagnostics["near_max_graph_degree_histogram"]
    ):
        raise AssertionError(f"N={n}: active degree histogram mismatch")

    if check["unit_norm_residual"] > 2e-14:
        raise AssertionError(f"N={n}: unit residual too large")
    if check["gram_minimum_eigenvalue"] < -2e-12:
        raise AssertionError(f"N={n}: Gram matrix is not numerically PSD")
    if check["gram_sixth_largest_eigenvalue_absolute"] > 2e-12:
        raise AssertionError(f"N={n}: Gram matrix is not numerically rank <= 5")
    if check["numerical_rank_at_1e-10"] > 5:
        raise AssertionError(f"N={n}: numerical rank exceeds five")

    meets = check["maximum_inner_product"] <= 0.5
    if meets != record["meets_kissing_threshold_binary64"]:
        raise AssertionError(f"N={n}: threshold boolean mismatch")
    beats = (
        check["maximum_inner_product"]
        < record["warm_start_objective"]["maximum_inner_product"]
    )
    if beats != record["strictly_beats_warm_start"]:
        raise AssertionError(f"N={n}: warm-start comparison mismatch")

    source_path = REPO / record["warm_start"]["source_file"]
    if sha256_file(source_path) != record["warm_start"]["source_file_sha256"]:
        raise AssertionError(f"N={n}: warm-start source hash mismatch")
    return {
        "n": n,
        **{
            key: value.tolist() if isinstance(value, np.ndarray) else value
            for key, value in check.items()
        },
        "meets_kissing_threshold_binary64": meets,
    }


def verify(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text())
    if payload.get("schema") != "kissing5-alternating-gram-search-v1":
        raise AssertionError("unexpected search schema")
    if payload.get("evidence_status") != "NUMERICAL EVIDENCE ONLY":
        raise AssertionError("search result must remain numerical evidence")
    parameters = payload["parameters"]
    expected_runs = len(parameters["n"]) * parameters["restarts"]
    if len(payload["runs"]) != expected_runs:
        raise AssertionError("run count mismatch")
    seen: set[tuple[int, int]] = set()
    for run in payload["runs"]:
        key = (int(run["n"]), int(run["restart"]))
        if key in seen:
            raise AssertionError(f"duplicate run {key}")
        seen.add(key)
        expected_seed = (
            parameters["seed_base"] + 100 * (run["n"] - 41) + run["restart"]
        )
        if run["seed"] != expected_seed:
            raise AssertionError(f"seed mismatch for run {key}")
        if run["iterations_completed"] > run["iterations_requested"]:
            raise AssertionError(f"iteration count mismatch for run {key}")

    checks = [
        verify_best(n_text, record)
        for n_text, record in sorted(payload["best_by_n"].items())
    ]
    found = any(check["meets_kissing_threshold_binary64"] for check in checks)
    if found != payload["candidate_at_or_below_threshold_found"]:
        raise AssertionError("global threshold boolean mismatch")
    return {
        "schema": "kissing5-alternating-gram-verification-v1",
        "status": "PASS",
        "input_file": str(path),
        "input_sha256": sha256_file(path),
        "numpy_version": np.__version__,
        "absolute_comparison_tolerance": TOLERANCE,
        "checks": checks,
        "candidate_at_or_below_threshold_found": found,
        "scope": (
            "binary64 integrity check only; a PASS with no threshold candidate "
            "is not an upper-bound certificate"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, nargs="?", default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = verify(args.input)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for check in result["checks"]:
        print(
            f"N={check['n']} max={check['maximum_inner_product']:.17g} "
            f"rank={check['numerical_rank_at_1e-10']} "
            f"violations={check['violating_pair_count']}"
        )
    print("PASS")


if __name__ == "__main__":
    main()

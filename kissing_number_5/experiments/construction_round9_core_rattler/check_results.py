#!/usr/bin/env python3
"""Independent binary64 integrity checker for the round-9 portfolio.

This module deliberately does not import the discovery implementation.  It
recomputes norms, every pair, Gram spectra, active graphs, the 35-core
decomposition, and the finite extracted graph's independence number.
Nothing here certifies a continuous optimum or nonexistence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE"
DIMENSION = 5
TARGET = 0.5


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized(array) -> np.ndarray:
    x = np.asarray(array, dtype=float)
    if x.ndim != 2 or x.shape[1] != DIMENSION:
        raise AssertionError("coordinate array is not N by 5")
    norms = np.linalg.norm(x, axis=1)
    if float(np.min(norms)) <= 1e-13:
        raise AssertionError("zero coordinate row")
    return x / norms[:, None]


def pairs(x: np.ndarray) -> np.ndarray:
    first, second = np.triu_indices(len(x), 1)
    return np.sum(x[first] * x[second], axis=1)


def connected_components(n: int, edges: list[list[int]]) -> list[list[int]]:
    adjacency = [[] for _ in range(n)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen = set()
    answer = []
    for start in range(n):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        answer.append(sorted(component))
    return sorted(answer, key=lambda item: (-len(item), item))


def active_graph(x: np.ndarray, tolerance: float) -> dict:
    first, second = np.triu_indices(len(x), 1)
    values = np.sum(x[first] * x[second], axis=1)
    top = float(np.max(values))
    chosen = values >= top - tolerance
    edges = np.column_stack([first[chosen], second[chosen]]).astype(int).tolist()
    degrees = np.bincount(
        np.asarray(edges, dtype=int).ravel(), minlength=len(x)
    )
    unique, counts = np.unique(degrees, return_counts=True)
    components = connected_components(len(x), edges)
    return {
        "tolerance": float(tolerance),
        "maximum": top,
        "edge_count": len(edges),
        "edges": edges,
        "degree_sequence": degrees.astype(int).tolist(),
        "degree_histogram": {
            str(int(degree)): int(count)
            for degree, count in zip(unique, counts)
        },
        "components": components,
        "component_sizes": [len(component) for component in components],
        "isolated_vertices": np.flatnonzero(degrees == 0).astype(int).tolist(),
    }


def maximum_independent_set(
    vertex_count: int, edges: list[list[int]]
) -> tuple[list[int], int]:
    adjacency = [0] * vertex_count
    for first, second in edges:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    best = []
    nodes = 0

    def recurse(candidates: int, selected: list[int]) -> None:
        nonlocal best, nodes
        nodes += 1
        if len(selected) + candidates.bit_count() <= len(best):
            return
        if candidates == 0:
            if len(selected) > len(best):
                best = selected.copy()
            return
        vertices = []
        remaining = candidates
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            vertices.append(vertex)
            remaining ^= bit
        pivot = max(
            vertices,
            key=lambda vertex: (adjacency[vertex] & candidates).bit_count(),
        )
        recurse(
            candidates & ~(1 << pivot) & ~adjacency[pivot],
            selected + [pivot],
        )
        recurse(candidates & ~(1 << pivot), selected)

    recurse((1 << vertex_count) - 1, [])
    return sorted(best), nodes


def assert_close(actual: float, recorded: float, tolerance: float, label: str):
    if abs(float(actual) - float(recorded)) > tolerance:
        raise AssertionError(
            f"{label}: recomputed {actual!r}, recorded {recorded!r}"
        )


def verify_best(run: dict) -> dict:
    record = run["best"]
    x = normalized(record["coordinates_float64"])
    n = int(run["n"])
    if x.shape != (n, DIMENSION):
        raise AssertionError(f"N={n}: wrong coordinate shape {x.shape}")
    values = pairs(x)
    gram = x @ x.T
    eigenvalues = np.linalg.eigvalsh(gram)
    maximum = float(np.max(values))
    assert_close(maximum, record["maximum"], 5e-13, f"N={n} maximum")
    assert_close(
        maximum - TARGET,
        record["gap_above_one_half"],
        5e-13,
        f"N={n} threshold gap",
    )
    assert_close(
        float(np.min(values)), record["minimum"], 5e-13, f"N={n} minimum"
    )
    assert_close(
        float(np.max(np.abs(np.sum(x * x, axis=1) - 1.0))),
        record["row_norm_max_error"],
        5e-13,
        f"N={n} norm error",
    )
    if int(np.sum(values > TARGET)) != record["pairs_above_one_half"]:
        raise AssertionError(f"N={n}: pairs-above-threshold mismatch")
    if int(np.sum(values < -TARGET)) != record["pairs_below_minus_one_half"]:
        raise AssertionError(f"N={n}: deep-negative-pair mismatch")
    if not np.allclose(
        eigenvalues,
        np.asarray(record["gram_eigenvalues"]),
        rtol=0.0,
        atol=2e-12,
    ):
        raise AssertionError(f"N={n}: Gram spectrum mismatch")
    for key, quantile in record["pair_quantiles"].items():
        assert_close(
            float(np.quantile(values, float(key))),
            quantile,
            5e-13,
            f"N={n} pair quantile {key}",
        )
    for tolerance in (1e-4, 1e-6, 1e-8):
        key = f"active_{tolerance:.0e}"
        if active_graph(x, tolerance) != record[key]:
            raise AssertionError(f"N={n}: {key} graph mismatch")
    threshold_triggered = maximum <= TARGET
    if threshold_triggered != bool(run["threshold_triggered"]):
        raise AssertionError(f"N={n}: threshold trigger mismatch")
    if threshold_triggered:
        # Search output alone must never be accepted as an exact construction.
        if "exact_or_interval_certificate" not in run:
            raise AssertionError(
                f"N={n}: floating threshold hit lacks mandatory independent "
                "exact/interval reconstruction certificate"
            )
    elif run["disposition"] != "NO THRESHOLD-FEASIBLE FLOATING CANDIDATE":
        raise AssertionError(f"N={n}: incorrect no-hit disposition")
    return {
        "n": n,
        "maximum": maximum,
        "gap": maximum - TARGET,
        "active_edges_1e-8": record["active_1e-08"]["edge_count"],
        "component_sizes_1e-8": record["active_1e-08"]["component_sizes"],
        "positive_gram_eigenvalues": eigenvalues[-DIMENSION:].tolist(),
        "gram_tail_max_abs": float(
            np.max(np.abs(eigenvalues[:-DIMENSION]))
        ),
    }


def verify_inherited_core(payload: dict, run: dict) -> dict:
    input_path = Path(payload["input"]["path"])
    if not input_path.is_absolute():
        project_root = Path(__file__).resolve().parents[2]
        input_path = project_root / input_path
    if not input_path.exists():
        raise AssertionError(f"input file is missing: {input_path}")
    if sha256(input_path) != payload["input"]["sha256"]:
        raise AssertionError("inherited input hash mismatch")
    inherited_payload = json.loads(input_path.read_text())
    n = int(run["n"])
    candidates = []
    for index, old_run in enumerate(inherited_payload["runs"]):
        coordinates = old_run.get("best", {}).get("coordinates_float64")
        if coordinates is None:
            continue
        x = normalized(coordinates)
        if len(x) == n:
            candidates.append((float(np.max(pairs(x))), index, x))
    maximum, index, x = min(candidates)
    if index != run["inherited"]["run_index"]:
        raise AssertionError(f"N={n}: inherited run-index mismatch")
    assert_close(
        maximum, run["inherited"]["maximum"], 5e-13, f"N={n} inherited maximum"
    )
    graph = active_graph(x, 1e-6)
    core = graph["components"][0]
    analysis = run["core_rattler_analysis"]
    if core != analysis["core_indices"]:
        raise AssertionError(f"N={n}: inherited core mismatch")
    rattlers = sorted(
        vertex for component in graph["components"][1:] for vertex in component
    )
    if rattlers != analysis["rattler_indices"]:
        raise AssertionError(f"N={n}: inherited rattlers mismatch")
    position = {vertex: local for local, vertex in enumerate(core)}
    core_edges = [
        [position[first], position[second]]
        for first, second in graph["edges"]
        if first in position and second in position
    ]
    independent, nodes = maximum_independent_set(len(core), core_edges)
    independent_global = [core[local] for local in independent]
    if independent_global != analysis[
        "finite_graph_maximum_independent_set_indices"
    ]:
        raise AssertionError(f"N={n}: independent-set witness mismatch")
    if len(independent) != analysis[
        "finite_graph_maximum_independent_set_size"
    ]:
        raise AssertionError(f"N={n}: independence number mismatch")
    if len(core) - len(independent) != analysis[
        "finite_graph_minimum_vertex_cover_size"
    ]:
        raise AssertionError(f"N={n}: vertex-cover number mismatch")
    if nodes != analysis["finite_graph_branch_nodes"]:
        raise AssertionError(f"N={n}: branch-node count mismatch")
    return {
        "n": n,
        "core_size": len(core),
        "rattler_count": len(rattlers),
        "active_core_edges": len(core_edges),
        "independence_number": len(independent),
        "minimum_vertex_cover": len(core) - len(independent),
        "branch_nodes": nodes,
    }


def verify(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if payload["status"] != STATUS:
        raise AssertionError("portfolio status is not numerical-only")
    runs = payload["runs"]
    if sorted(run["n"] for run in runs) != [41, 42, 43, 44]:
        raise AssertionError("portfolio does not contain exactly N=41..44")
    summaries = []
    cores = []
    for run in runs:
        counts = [record["deleted_count"] for record in run["surgery_records"]]
        if counts != list(range(2, 9)):
            raise AssertionError(
                f"N={run['n']}: deletion counts are not exactly 2..8"
            )
        if run["candidate_count"] < 10:
            raise AssertionError(f"N={run['n']}: unexpectedly small portfolio")
        summaries.append(verify_best(run))
        cores.append(verify_inherited_core(payload, run))
    return {
        "status": "PASS — BINARY64 ARTIFACT INTEGRITY ONLY",
        "portfolio_sha256": sha256(path),
        "runs": summaries,
        "inherited_core_checks": cores,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    arguments = parser.parse_args(argv)
    print(json.dumps(verify(arguments.portfolio), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

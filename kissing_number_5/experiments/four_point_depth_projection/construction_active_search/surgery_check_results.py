#!/usr/bin/env python3
"""Independent binary64 checker for surgery_portfolio.json.

This file deliberately does not import the discovery program.  It verifies
stored coordinates, literal maxima, hashes, Gram spectra, and active graphs.
It is not an exact-real or directed-interval verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def unit_rows(array: np.ndarray) -> np.ndarray:
    x = np.asarray(array, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != 5:
        raise AssertionError("coordinate shape is not N by 5")
    norms = np.sqrt(np.sum(x * x, axis=1))
    if float(np.min(norms)) <= 1e-14:
        raise AssertionError("zero coordinate row")
    return x / norms[:, None]


def pair_data(x: np.ndarray):
    first, second = np.triu_indices(len(x), 1)
    values = np.sum(x[first] * x[second], axis=1)
    return first, second, values


def coordinate_hash(x: np.ndarray) -> str:
    data = np.ascontiguousarray(unit_rows(x), dtype="<f8")
    return hashlib.sha256(data.tobytes()).hexdigest()


def components(n: int, edges: list[list[int]]) -> list[int]:
    adjacency = [set() for _ in range(n)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    seen: set[int] = set()
    answer = []
    for start in range(n):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        answer.append(size)
    return sorted(answer, reverse=True)


def check_graph(x: np.ndarray, stored: dict) -> None:
    first, second, values = pair_data(x)
    top = float(np.max(values))
    chosen = values >= top - float(stored["tolerance"])
    edges = (
        np.column_stack([first[chosen], second[chosen]]).astype(int).tolist()
    )
    assert edges == stored["edges"]
    digest = hashlib.sha256(
        json.dumps(edges, separators=(",", ":")).encode()
    ).hexdigest()
    assert digest == stored["edge_sha256"]
    assert len(edges) == int(stored["edge_count"])
    degree = np.zeros(len(x), dtype=int)
    for i, j in edges:
        degree[i] += 1
        degree[j] += 1
    unique, counts = np.unique(degree, return_counts=True)
    histogram = {
        str(int(value)): int(count)
        for value, count in zip(unique, counts)
    }
    assert histogram == stored["degree_histogram"]
    assert components(len(x), edges) == stored["component_sizes"]


def check_diagnostics(stored: dict) -> dict:
    raw = np.asarray(stored["coordinates_float64"], dtype=np.float64)
    x = unit_rows(raw)
    assert x.shape == (int(stored["n"]), 5)
    assert coordinate_hash(raw) == stored[
        "coordinate_little_endian_float64_sha256"
    ]
    first, second, values = pair_data(x)
    top = float(np.max(values))
    assert top == float(stored["maximum_inner_product_binary64"])
    assert top.hex() == stored["maximum_inner_product_float_hex"]
    maximizing = np.flatnonzero(values == top)
    pairs = [[int(first[k]), int(second[k])] for k in maximizing]
    assert pairs == stored["literal_binary64_maximizing_pairs"]
    assert float(np.min(values)) == float(stored["minimum_inner_product_binary64"])
    assert int(np.sum(values > 0.5)) == int(stored["pairs_above_one_half"])
    assert int(np.sum(values == 0.5)) == int(
        stored["pairs_equal_one_half_binary64"]
    )
    assert bool(top <= 0.5) == bool(stored["meets_threshold_binary64"])
    gram = x @ x.T
    spectrum = np.linalg.eigvalsh(x.T @ x)
    assert np.allclose(
        spectrum,
        np.asarray(stored["positive_gram_eigenvalues"]),
        rtol=0.0,
        atol=8e-13,
    )
    full = np.linalg.eigvalsh(gram)
    tail = float(np.max(np.abs(full[:-5])))
    assert abs(tail - float(stored["gram_tail_max_abs"])) <= 8e-13
    for key in ("active_1e-4", "active_1e-6", "active_1e-8"):
        check_graph(x, stored[key])
    return {
        "n": len(x),
        "maximum": top,
        "maximum_hex": top.hex(),
        "hash": coordinate_hash(raw),
        "positive_gram_eigenvalues": spectrum.tolist(),
        "gram_tail_max_abs": tail,
        "active_edges": {
            key: int(stored[key]["edge_count"])
            for key in ("active_1e-4", "active_1e-6", "active_1e-8")
        },
    }


def check_payload(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if "best_configurations" in payload:
        return check_consolidated(path, payload)
    assert payload["smooth_surrogate_used"] is False
    summaries = []
    by_n: dict[int, list[tuple[float, dict]]] = {}
    threshold = False
    for run in payload["runs"]:
        initial = check_diagnostics(run["initial"])
        best = check_diagnostics(run["best"])
        assert int(run["n"]) == initial["n"] == best["n"]
        assert int(run["seed"]) >= 0
        assert run["origin"] in ("stored_near_miss", "random_greedy")
        by_n.setdefault(int(run["n"]), []).append((best["maximum"], run))
        threshold |= best["maximum"] <= 0.5
        summaries.append(
            {
                "n": int(run["n"]),
                "seed": int(run["seed"]),
                "origin": run["origin"],
                "initial_maximum": initial["maximum"],
                "best": best,
            }
        )
    for n, entries in by_n.items():
        _, chosen = min(entries, key=lambda item: item[0])
        stored = payload["best_by_n"][str(n)]
        assert int(stored["seed"]) == int(chosen["seed"])
        assert stored["origin"] == chosen["origin"]
        assert float(stored["maximum_inner_product_binary64"]) == float(
            chosen["best"]["maximum_inner_product_binary64"]
        )
        assert stored["coordinate_little_endian_float64_sha256"] == chosen[
            "best"
        ]["coordinate_little_endian_float64_sha256"]
    assert bool(payload["binary64_threshold_hit"]) == threshold
    return {
        "portfolio": str(path),
        "runs_checked": len(summaries),
        "binary64_threshold_hit": threshold,
        "runs": summaries,
        "rigor_warning": (
            "Binary64 consistency only; this is not directed interval or "
            "exact-real verification."
        ),
    }


def check_consolidated(path: Path, payload: dict) -> dict:
    source_runs: dict[tuple[str, int], dict] = {}
    all_by_n: dict[int, list[float]] = {}
    for entry in payload["inputs"]:
        source = Path(entry["path"])
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert digest == entry["sha256"]
        source_payload = json.loads(source.read_text())
        for index, run in enumerate(source_payload["runs"]):
            source_runs[(str(source), index)] = run
            all_by_n.setdefault(int(run["n"]), []).append(
                float(run["best"]["maximum_inner_product_binary64"])
            )
    summaries = []
    threshold = False
    for key, item in payload["best_configurations"].items():
        n = int(key)
        assert n == int(item["n"])
        source_key = (item["source_path"], int(item["source_run_index"]))
        source_run = source_runs[source_key]
        assert int(source_run["seed"]) == int(item["seed"])
        assert source_run["origin"] == item["origin"]
        assert source_run["best"] == item["diagnostics"]
        checked = check_diagnostics(item["diagnostics"])
        assert checked["n"] == n
        assert checked["maximum"] == min(all_by_n[n])
        threshold |= checked["maximum"] <= 0.5
        summaries.append(
            {
                "n": n,
                "seed": int(item["seed"]),
                "origin": item["origin"],
                "best": checked,
            }
        )
    assert bool(payload["binary64_threshold_hit"]) == threshold
    return {
        "portfolio": str(path),
        "runs_checked": len(summaries),
        "binary64_threshold_hit": threshold,
        "runs": summaries,
        "rigor_warning": (
            "Binary64 consistency only; this is not directed interval or "
            "exact-real verification."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = check_payload(arguments.portfolio)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if arguments.output is not None:
        arguments.output.write_text(rendered)
    if result["binary64_threshold_hit"]:
        raise SystemExit(
            "A <=1/2 binary64 candidate needs a separate exact or "
            "directed-interval certificate."
        )


if __name__ == "__main__":
    main()

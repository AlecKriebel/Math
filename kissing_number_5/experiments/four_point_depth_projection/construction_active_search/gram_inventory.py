#!/usr/bin/env python3
"""Inventory stored 5-dimensional N=41,...,44 construction coordinates.

This is intentionally independent of the metadata recorded by the search
programs.  Every maximum inner product, norm residual, spectrum, and hash in
the output is recomputed from the stored coordinates after binary64
renormalization.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterator

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEFAULT_OUTPUT = HERE / "gram_inventory.json"
COORDINATE_KEYS = frozenset({"coordinates", "coordinates_float64", "points"})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def coordinate_sha256(points: np.ndarray) -> str:
    array = np.asarray(points, dtype="<f8", order="C")
    return hashlib.sha256(array.tobytes(order="C")).hexdigest()


def iter_coordinate_arrays(
    value: Any, json_path: str = "$"
) -> Iterator[tuple[str, np.ndarray]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{json_path}.{key}"
            if key in COORDINATE_KEYS and isinstance(child, list):
                try:
                    array = np.asarray(child, dtype=np.float64)
                except (TypeError, ValueError):
                    array = np.empty((0, 0))
                if (
                    array.ndim == 2
                    and array.shape[1] == 5
                    and 41 <= array.shape[0] <= 44
                    and np.all(np.isfinite(array))
                ):
                    yield child_path, array
            yield from iter_coordinate_arrays(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_coordinate_arrays(child, f"{json_path}[{index}]")


def component_sizes(n: int, edges: list[tuple[int, int]]) -> list[int]:
    adjacency = [[] for _ in range(n)]
    for i, j in edges:
        adjacency[i].append(j)
        adjacency[j].append(i)
    unseen = set(range(n))
    sizes: list[int] = []
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
    norms = np.linalg.norm(points, axis=1)
    normalized = points / norms[:, None]
    gram = normalized @ normalized.T
    n = len(normalized)
    upper = np.triu_indices(n, 1)
    values = gram[upper]
    maximum = float(np.max(values))
    spectrum = np.linalg.eigvalsh(gram)
    near_max_edges = [
        (int(i), int(j))
        for i, j, value in zip(*upper, values, strict=True)
        if value >= maximum - 1e-8
    ]
    degrees = np.zeros(n, dtype=np.int64)
    for i, j in near_max_edges:
        degrees[i] += 1
        degrees[j] += 1
    degree_values, degree_counts = np.unique(degrees, return_counts=True)
    return {
        "n": n,
        "dimension": 5,
        "coordinate_little_endian_float64_sha256": coordinate_sha256(normalized),
        "maximum_inner_product_binary64": maximum,
        "gap_above_one_half": maximum - 0.5,
        "minimum_inner_product_binary64": float(np.min(values)),
        "unit_norm_residual_before_renormalization": float(
            np.max(np.abs(norms - 1.0))
        ),
        "unit_norm_residual_after_renormalization": float(
            np.max(np.abs(np.sum(normalized * normalized, axis=1) - 1.0))
        ),
        "violating_pair_count": int(np.count_nonzero(values > 0.5)),
        "violation_l2": float(np.linalg.norm(np.maximum(values - 0.5, 0.0))),
        "gram_eigenvalues_ascending": [float(value) for value in spectrum],
        "gram_null_spectrum_maximum_absolute": float(
            np.max(np.abs(spectrum[:-5]))
        ),
        "gram_top_five_eigenvalues_ascending": [
            float(value) for value in spectrum[-5:]
        ],
        "pairs_within_1e-8_of_maximum": len(near_max_edges),
        "near_max_graph_component_sizes": component_sizes(n, near_max_edges),
        "near_max_graph_degree_histogram": {
            str(int(degree)): int(count)
            for degree, count in zip(degree_values, degree_counts, strict=True)
        },
    }


def collect_records() -> list[dict[str, Any]]:
    files = sorted(REPO.glob("experiments/construction*/results/*.json"))
    records: list[dict[str, Any]] = []
    for path in files:
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        relative = path.relative_to(REPO)
        source_hash = sha256_file(path)
        for json_path, points in iter_coordinate_arrays(payload):
            record = diagnostics(points)
            record.update(
                {
                    "source_file": str(relative),
                    "source_file_sha256": source_hash,
                    "source_locator": json_path,
                }
            )
            records.append(record)

    text_path = REPO / "experiments/input/spherical_codes_5_41.txt"
    points = np.loadtxt(text_path, delimiter=",", dtype=np.float64)
    record = diagnostics(points)
    record.update(
        {
            "source_file": str(text_path.relative_to(REPO)),
            "source_file_sha256": sha256_file(text_path),
            "source_locator": "comma-separated rows",
        }
    )
    records.append(record)
    return records


def build_inventory() -> dict[str, Any]:
    records = collect_records()
    unique_hashes = {
        record["coordinate_little_endian_float64_sha256"] for record in records
    }
    best: dict[str, Any] = {}
    for n in range(41, 45):
        candidates = [record for record in records if record["n"] == n]
        if not candidates:
            raise RuntimeError(f"no stored five-dimensional N={n} coordinates")
        chosen = min(
            candidates,
            key=lambda record: (
                record["maximum_inner_product_binary64"],
                record["source_file"],
                record["source_locator"],
            ),
        )
        best[str(n)] = chosen
    return {
        "schema": "kissing5-gram-coordinate-inventory-v1",
        "numpy_version": np.__version__,
        "scan_glob": "experiments/construction*/results/*.json",
        "excluded_dimension_rule": "only arrays of shape N x 5 are admitted",
        "occurrence_count": len(records),
        "unique_binary64_coordinate_count": len(unique_hashes),
        "best_by_n_after_independent_renormalization": best,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build_inventory()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    for n, record in result["best_by_n_after_independent_renormalization"].items():
        print(
            f"N={n} max={record['maximum_inner_product_binary64']:.17g} "
            f"{record['source_file']} {record['source_locator']}"
        )
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()

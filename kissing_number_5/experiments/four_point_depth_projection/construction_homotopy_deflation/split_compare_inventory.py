#!/usr/bin/env python3
"""Compare selected split endpoints with earlier stored coordinate arrays."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
from pathlib import Path

import numpy as np


def descriptor(rows) -> np.ndarray:
    x = np.asarray(rows, dtype=np.float64)
    x /= np.linalg.norm(x, axis=1)[:, None]
    first, second = np.triu_indices(len(x), 1)
    return np.sort(np.sum(x[first] * x[second], axis=1))


def is_coordinate_array(value, cardinalities: set[int]) -> bool:
    return (
        isinstance(value, list)
        and len(value) in cardinalities
        and bool(value)
        and all(
            isinstance(row, list)
            and len(row) == 5
            and all(isinstance(entry, (int, float)) for entry in row)
            for row in value
        )
    )


def walk(value, path: str, cardinalities: set[int]):
    if is_coordinate_array(value, cardinalities):
        yield path, value
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            if isinstance(child, (dict, list)):
                yield from walk(child, f"{path}[{index}]", cardinalities)
    elif isinstance(value, dict):
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                yield from walk(child, f"{path}.{key}", cardinalities)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    portfolio = json.loads(arguments.portfolio.read_text())
    targets = {}
    for key, summary in portfolio["best_by_n"].items():
        n = int(key)
        if "polished_best_by_source_n" in portfolio:
            record = portfolio["polished_best_by_source_n"][
                f"{summary['source']}:{n}"
            ]
            rows = record["selected"]["coordinates_float64"]
        else:
            run = next(
                run
                for run in portfolio["runs"]
                if run["seed"] == summary["seed"]
            )
            rows = run["best"]["coordinates_float64"]
        targets[n] = descriptor(rows)

    nearest = {
        n: {
            "sorted_gram_rms": float("inf"),
            "sorted_gram_maximum": float("inf"),
            "source_file": None,
            "json_path": None,
        }
        for n in targets
    }
    occurrence_count = 0
    files_read = 0
    pattern = str(arguments.repository / "experiments/construction*/**/*.json")
    for filename in sorted(glob.glob(pattern, recursive=True)):
        if "construction_homotopy_deflation" in filename:
            continue
        path = Path(filename)
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        files_read += 1
        for json_path, rows in walk(payload, "root", set(targets)):
            candidate = descriptor(rows)
            n = len(rows)
            difference = candidate - targets[n]
            rms = float(np.sqrt(np.mean(difference * difference)))
            maximum = float(np.max(np.abs(difference)))
            occurrence_count += 1
            if rms < nearest[n]["sorted_gram_rms"]:
                nearest[n] = {
                    "sorted_gram_rms": rms,
                    "sorted_gram_maximum": maximum,
                    "source_file": str(path),
                    "json_path": json_path,
                }
    result = {
        "status": "NUMERICAL INVENTORY COMPARISON ONLY",
        "portfolio": str(arguments.portfolio),
        "portfolio_sha256": hashlib.sha256(
            arguments.portfolio.read_bytes()
        ).hexdigest(),
        "files_read": files_read,
        "coordinate_occurrences_checked": occurrence_count,
        "descriptor": "sorted off-diagonal binary64 Gram multiset",
        "nearest_prior_by_n": {
            str(n): nearest[n] for n in sorted(nearest)
        },
        "scope_warning": (
            "A nonzero discrepancy proves distinction only from the stored "
            "arrays scanned, not novelty relative to unstored computations."
        ),
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

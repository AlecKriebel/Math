#!/usr/bin/env python3
"""Select the literal best stored arrays from surgery portfolio files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolios", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    selected: dict[int, dict] = {}
    inputs = []
    for path in arguments.portfolios:
        payload = json.loads(path.read_text())
        inputs.append({"path": str(path), "sha256": sha256(path)})
        for run_index, run in enumerate(payload["runs"]):
            n = int(run["n"])
            candidate = {
                "n": n,
                "seed": int(run["seed"]),
                "origin": run["origin"],
                "source_path": str(path),
                "source_run_index": run_index,
                "diagnostics": run["best"],
            }
            if (
                n not in selected
                or candidate["diagnostics"]["maximum_inner_product_binary64"]
                < selected[n]["diagnostics"][
                    "maximum_inner_product_binary64"
                ]
            ):
                selected[n] = candidate
    payload = {
        "status": "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE",
        "selection_rule": "minimum literal rowwise binary64 pair scan",
        "inputs": inputs,
        "best_configurations": {
            str(n): selected[n] for n in sorted(selected)
        },
        "binary64_threshold_hit": any(
            item["diagnostics"]["maximum_inner_product_binary64"] <= 0.5
            for item in selected.values()
        ),
        "warning": (
            "The coordinates, maxima, and spectra are floating-point data; "
            "no failed search is an upper bound."
        ),
    }
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    for n in sorted(selected):
        item = selected[n]
        print(
            n,
            item["diagnostics"]["maximum_inner_product_binary64"],
            item["diagnostics"]["maximum_inner_product_float_hex"],
            item["seed"],
            item["origin"],
        )


if __name__ == "__main__":
    main()

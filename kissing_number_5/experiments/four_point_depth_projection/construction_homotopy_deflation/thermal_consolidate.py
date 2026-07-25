#!/usr/bin/env python3
"""Consolidate per-cardinality thermal portfolios without solver imports."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    payloads = [json.loads(path.read_text()) for path in arguments.inputs]
    if not payloads:
        raise ValueError("no inputs")
    first = payloads[0]
    result = {
        "status": first["status"],
        "method": first["method"],
        "target": first["target"],
        "software": first["software"],
        "parameters": dict(first["parameters"]),
        "runs": [],
        "best_by_n": {},
        "inputs": [],
    }
    result["parameters"]["n"] = []
    elapsed = 0.0
    for path, payload in zip(arguments.inputs, payloads):
        for key in ("status", "method", "target", "software"):
            if payload[key] != result[key]:
                raise AssertionError(f"incompatible {key}")
        for key in (
            "regimes",
            "population_size",
            "polish_count",
            "max_iterations",
            "seed_base",
        ):
            if payload["parameters"][key] != result["parameters"][key]:
                raise AssertionError(f"incompatible parameter {key}")
        cardinalities = [int(n) for n in payload["parameters"]["n"]]
        result["parameters"]["n"].extend(cardinalities)
        result["runs"].extend(payload["runs"])
        for n in cardinalities:
            result["best_by_n"][str(n)] = payload["best_by_n"][str(n)]
        elapsed += float(payload["elapsed_seconds"])
        result["inputs"].append(
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    expected = sorted(set(result["parameters"]["n"]))
    if result["parameters"]["n"] != expected:
        raise AssertionError("cardinalities must be unique and ordered")
    result["elapsed_seconds_sum"] = elapsed
    result["binary64_threshold_hit"] = bool(
        any(run["reached_half"] for run in result["runs"])
    )
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    for n in expected:
        value = result["best_by_n"][str(n)]["diagnostics"][
            "maximum_inner_product"
        ]
        print(f"N={n} best={value:.17g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

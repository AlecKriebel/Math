#!/usr/bin/env python3
"""Extract the four concrete best coordinate arrays from the full portfolio."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    payload = json.loads(arguments.portfolio.read_text())
    if not payload.get("completed"):
        raise SystemExit("portfolio is incomplete")
    extracted = {
        "evidence_status": "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE",
        "source_portfolio_sha256": hashlib.sha256(
            arguments.portfolio.read_bytes()
        ).hexdigest(),
        "certified_or_exact_candidate_found": False,
        "configurations": {},
    }
    for n, pointer in sorted(payload["best_by_n"].items(), key=lambda item: int(item[0])):
        run = payload["polished_runs"][pointer["polished_run_index"]]
        maximum = run["final_diagnostics"]["maximum_inner_product"]
        extracted["configurations"][n] = {
            "n": int(n),
            "dimension": 5,
            "source_family": run["source_family"],
            "source_seed": run["source_seed"],
            "maximum_inner_product_binary64": maximum,
            "maximum_inner_product_float_hex": float(maximum).hex(),
            "gap_above_one_half": maximum - 0.5,
            "diagnostics": run["final_diagnostics"],
            "coordinates_float64": run["coordinates_float64"],
        }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(extracted, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()

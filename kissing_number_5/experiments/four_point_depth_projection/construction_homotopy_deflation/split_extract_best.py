#!/usr/bin/env python3
"""Extract compact best-per-source/cardinality split-homotopy endpoints."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    payload = json.loads(arguments.portfolio.read_text())
    records = {}
    for key, summary in payload["best_by_source_n"].items():
        run = next(
            run
            for run in payload["runs"]
            if run["seed"] == summary["seed"]
            and run["source"] == key.split(":")[0]
            and run["n"] == int(key.split(":")[1])
        )
        records[key] = {
            "source": run["source"],
            "n": run["n"],
            "seed": run["seed"],
            "variant": run["variant"],
            "selected_source_parent_indices": run[
                "selected_source_parent_indices"
            ],
            "separation_schedule_radians": run[
                "separation_schedule_radians"
            ],
            "release_radius_schedule": run["release_radius_schedule"],
            "diagnostics": run["best"],
        }
    result = {
        "status": payload["status"],
        "source_portfolio": str(arguments.portfolio),
        "source_portfolio_sha256": hashlib.sha256(
            arguments.portfolio.read_bytes()
        ).hexdigest(),
        "selection_rule": (
            "minimum literal binary64 maximum for each exact source and N"
        ),
        "best_by_source_n": records,
        "best_by_n": payload["best_by_n"],
        "binary64_threshold_hit": payload["binary64_threshold_hit"],
        "warning": payload["warning"],
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(
        json.dumps(
            {
                key: record["diagnostics"][
                    "maximum_inner_product_binary64"
                ]
                for key, record in records.items()
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

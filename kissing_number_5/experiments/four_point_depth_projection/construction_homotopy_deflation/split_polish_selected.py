#!/usr/bin/env python3
"""Final unconstrained epigraph polish of all split-homotopy winners."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from experiments.four_point_depth_projection.construction_homotopy_deflation import (
    split_homotopy_search as search,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("best_configurations", type=Path)
    parser.add_argument("--iterations", type=int, default=1200)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    source = json.loads(arguments.best_configurations.read_text())
    records = {}
    for key in sorted(source["best_by_source_n"]):
        entry = source["best_by_source_n"][key]
        initial_record = entry["diagnostics"]
        x = np.asarray(initial_record["coordinates_float64"], dtype=float)
        n = len(x)
        polished, solver = search.epigraph_refine(
            x,
            movable=list(range(n)),
            split_pairs=[],
            prescribed_pair_inner=None,
            max_iterations=arguments.iterations,
        )
        polished_record = search.diagnostics(polished)
        selected = (
            polished_record
            if polished_record["maximum_inner_product_binary64"]
            < initial_record["maximum_inner_product_binary64"]
            else initial_record
        )
        records[key] = {
            "source": entry["source"],
            "n": entry["n"],
            "seed": entry["seed"],
            "variant": entry["variant"],
            "selected_source_parent_indices": entry[
                "selected_source_parent_indices"
            ],
            "initial": initial_record,
            "solver": solver,
            "polished": polished_record,
            "selected": selected,
            "polish_improved": bool(selected is polished_record),
        }
        print(
            f"{key} {initial_record['maximum_inner_product_binary64']:.17g} "
            f"-> {polished_record['maximum_inner_product_binary64']:.17g}",
            flush=True,
        )
    best_by_n = {}
    for n in (41, 42, 43, 44):
        eligible = [entry for entry in records.values() if entry["n"] == n]
        chosen = min(
            eligible,
            key=lambda entry: entry["selected"][
                "maximum_inner_product_binary64"
            ],
        )
        best_by_n[str(n)] = {
            "source": chosen["source"],
            "seed": chosen["seed"],
            "variant": chosen["variant"],
            "maximum_inner_product_binary64": chosen["selected"][
                "maximum_inner_product_binary64"
            ],
            "maximum_inner_product_float_hex": chosen["selected"][
                "maximum_inner_product_float_hex"
            ],
            "coordinate_little_endian_float64_sha256": chosen["selected"][
                "coordinate_little_endian_float64_sha256"
            ],
        }
    result = {
        "status": "NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE",
        "method": (
            "literal all-coordinate epigraph polish without retained split "
            "equalities"
        ),
        "source_best_file": str(arguments.best_configurations),
        "source_best_sha256": hashlib.sha256(
            arguments.best_configurations.read_bytes()
        ).hexdigest(),
        "iterations": arguments.iterations,
        "polished_best_by_source_n": records,
        "best_by_n": best_by_n,
        "binary64_threshold_hit": any(
            entry["selected"]["maximum_inner_product_binary64"] <= 0.5
            for entry in records.values()
        ),
        "warning": (
            "Binary64 numerical evidence only; local solver failure or "
            "success has no global implication."
        ),
    }
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(best_by_n, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Select the best retained mechanism/cardinality records across seed runs."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sources = []
    chosen: dict[tuple[str, int], dict] = {}
    counts = Counter()
    elapsed = 0.0
    software = None
    for path in args.inputs:
        raw = path.read_bytes()
        data = json.loads(raw)
        if data["status"] != STATUS:
            raise AssertionError(f"{path}: wrong status")
        if data["dimension"] != 5 or data["cardinalities"] != [41, 42, 43, 44]:
            raise AssertionError(f"{path}: wrong problem")
        if software is None:
            software = data["software"]
        elif software != data["software"]:
            raise AssertionError("software metadata differs between sources")
        counts.update({key: int(value) for key, value in data["search_counts"].items()})
        elapsed += float(data["elapsed_seconds"])
        sources.append(
            {
                "filename": path.name,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "seed": int(data["seed"]),
                "search_counts": data["search_counts"],
            }
        )
        for record in data["records"]:
            key = (record["mechanism"], int(record["n"]))
            if (
                key not in chosen
                or float(record["maximum_inner_product_binary64"])
                < float(chosen[key]["maximum_inner_product_binary64"])
            ):
                chosen[key] = record
    records = [chosen[key] for key in sorted(chosen)]
    best_labels = []
    for n in range(41, 45):
        relevant = [record for record in records if int(record["n"]) == n]
        if not relevant:
            raise AssertionError(f"no N={n} record")
        best_labels.append(
            min(
                relevant,
                key=lambda record: float(record["maximum_inner_product_binary64"]),
            )["label"]
        )
    result = {
        "status": STATUS,
        "experiment": (
            "consolidated latitude-layer/evolution/cardinality-changing "
            "construction portfolio"
        ),
        "dimension": 5,
        "cardinalities": [41, 42, 43, 44],
        "seed": -1,
        "consolidated_source_portfolios": sources,
        "command_arguments": {
            "consolidator_inputs": [str(path) for path in args.inputs],
            "output": str(args.output),
        },
        "software": software,
        "deterministic_blas_threads_requested": {
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "VECLIB_MAXIMUM_THREADS": "1",
        },
        "search_counts": dict(counts),
        "elapsed_seconds": elapsed,
        "best_record_labels_by_cardinality": best_labels,
        "records": records,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "records": len(records),
                "best": {
                    str(n): min(
                        float(record["maximum_inner_product_binary64"])
                        for record in records
                        if int(record["n"]) == n
                    )
                    for n in range(41, 45)
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

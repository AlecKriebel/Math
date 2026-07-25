#!/usr/bin/env python3
"""Independently replay a small production range with the NumPy reference."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct

from verify_reference_quotients import reference_count


def score(record: dict[str, object]) -> tuple:
    return (
        int(record["nonzero_lags"]),
        int(record["l1"]),
        int(record["linf"]),
        int(record["quotient_index"]),
        int(record["central_value"]),
        int(record["pair_state"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--allow-large",
        action="store_true",
        help="allow an independent replay of more than eight quotients",
    )
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    if (
        manifest.get("schema")
        != "h668-case26-global-quotient-range-v1"
        or manifest.get("status") != "complete"
    ):
        raise RuntimeError("input is not a complete production range")
    start = int(manifest["start"])
    states = int(manifest["states"])
    if states > 8 and not args.allow_large:
        raise RuntimeError(
            "independent NumPy replay is capped at eight quotients; "
            "pass --allow-large deliberately"
        )

    digest = hashlib.sha256()
    survivors = 0
    exact_records: list[dict[str, object]] = []
    best: dict[str, object] | None = None
    for quotient_index in range(start, start + states):
        result = reference_count(
            quotient_index, enumerate_records=True
        )
        records = result["records"]
        survivors += len(records)
        for record in records:
            residuals = list(map(int, record["normalized_residuals"]))
            digest.update(
                struct.pack(
                    "<IBQ20h",
                    int(record["quotient_index"]),
                    int(record["central_value"]),
                    int(record["pair_state"]),
                    *residuals,
                )
            )
            if int(record["nonzero_lags"]) == 0:
                exact_records.append(record)
            if best is None or score(record) < score(best):
                best = record

    expected = {
        "joint_mod6_supports": survivors,
        "integer_polynomial_checks": survivors,
        "bitpacked_physical_replays": survivors,
        "exact_integer_supports": len(exact_records),
        "survivor_stream_sha256": digest.hexdigest(),
        "best_witness": best,
        "exact_candidates": exact_records,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise AssertionError(
                f"independent replay mismatch at {key}"
            )
    print(
        json.dumps(
            {
                "status": "PASS",
                "manifest": str(args.manifest),
                "start": start,
                "states": states,
                **expected,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

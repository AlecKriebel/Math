#!/usr/bin/env python3
"""Demonstrate the missing 4,368-to-192 dependency in the old seven-port gate.

The primary and reviewer both select only records with three missing support
ports.  This bounded diagnostic removes every other census record in memory
and proves that all predicates they use to identify the residual universe are
unchanged.  It does not modify the publication certificate.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


EXPECTED_PIDS = {629, 644, 649, 650, 685, 700, 705, 706}


def digest_bytes(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def residual(records: list[dict]) -> list[dict]:
    return [row for row in records if row["missing_rigid_support_ports"] == 3]


def residual_key_set(records: list[dict]) -> set[tuple[int, int]]:
    return {(row["presentation_index"], row["permutation_index"]) for row in residual(records)}


def audit(path: Path) -> dict:
    original_raw = path.read_bytes()
    census = json.loads(original_raw)
    original_records = census["records"]
    selected = residual(original_records)
    mutated = dict(census)
    mutated["records"] = selected
    mutated_raw = (json.dumps(mutated, indent=2, sort_keys=True) + "\n").encode()

    expected = {(pid, permutation) for pid in EXPECTED_PIDS for permutation in range(24)}
    original_keys = residual_key_set(original_records)
    mutated_keys = residual_key_set(mutated["records"])
    primary_predicates_unchanged = (
        len(selected) == 192
        and len(mutated["records"]) == 192
        and {row["presentation_index"] for row in selected} == EXPECTED_PIDS
    )
    reviewer_predicates_unchanged = original_keys == mutated_keys == expected
    return {
        "census": str(path),
        "original_sha256": digest_bytes(original_raw),
        "mutated_sha256": digest_bytes(mutated_raw),
        "original_records": len(original_records),
        "records_after_deleting_nonresidual_rows": len(mutated["records"]),
        "deleted_records": len(original_records) - len(mutated["records"]),
        "primary_residual_selection_predicates_unchanged": primary_predicates_unchanged,
        "reviewer_residual_set_predicates_unchanged": reviewer_predicates_unchanged,
        "mutation_escapes_4368_to_192_dependency": primary_predicates_unchanged and reviewer_predicates_unchanged,
        "interpretation": (
            "The old primary/reviewer certify the conditional 192-to-1686 computation. "
            "They do not certify that the 192 rows exhaust the preceding 4,368 equality universe."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.census), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

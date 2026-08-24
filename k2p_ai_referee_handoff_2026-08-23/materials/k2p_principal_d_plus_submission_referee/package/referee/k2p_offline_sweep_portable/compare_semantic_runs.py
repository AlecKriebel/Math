#!/usr/bin/env python3
"""Compare mathematical record content while excluding implementation/run diagnostics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

MATHEMATICAL_FIELDS = (
    "source_index", "canonical_class_id", "descriptor_sha256", "source_graph_sha256",
    "target_graph_sha256", "direction", "incoming_roles", "port_match", "port_matches",
    "omitted_roles", "source_rank", "target_rank", "stratum", "status", "certificate",
    "certificate_payload_sha256", "restoration_parent_id", "child_requests", "members",
)


def normalized(row: dict) -> dict:
    return {field: row.get(field) for field in MATHEMATICAL_FIELDS}


def digest(value: dict) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def records(root: Path) -> dict[tuple[int, int], Path]:
    result = {}
    for path in root.glob("source_*/records/class_*.json"):
        row = json.loads(path.read_text())
        key = (row["source_index"], row["canonical_class_id"])
        if key in result:
            raise SystemExit(f"duplicate record {key} under {root}")
        result[key] = path
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    baseline, candidate = records(args.baseline), records(args.candidate)
    if not baseline or not candidate:
        raise SystemExit("both run roots must contain records")
    if set(baseline) != set(candidate):
        raise SystemExit({
            "missing_from_candidate": sorted(set(baseline) - set(candidate)),
            "extra_in_candidate": sorted(set(candidate) - set(baseline)),
        })
    if not args.allow_partial:
        counts = (536, 747, 276, 276, 64, 32)
        expected = {(source, class_id) for source, count in enumerate(counts) for class_id in range(count)}
        if set(baseline) != expected:
            raise SystemExit("comparison is not a complete 1,931-record sweep; use --allow-partial for a sample")
    mismatches = []
    combined = hashlib.sha256()
    for key in sorted(baseline):
        left = normalized(json.loads(baseline[key].read_text()))
        right = normalized(json.loads(candidate[key].read_text()))
        if left != right:
            mismatches.append(key)
        combined.update(f"{key[0]}:{key[1]}:{digest(right)}\n".encode())
    if mismatches:
        raise SystemExit(f"MATHEMATICAL_RECORD_MISMATCH: {mismatches[:20]}")
    print(json.dumps({
        "semantic_records_equal": True,
        "record_count": len(baseline),
        "combined_sha256": combined.hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

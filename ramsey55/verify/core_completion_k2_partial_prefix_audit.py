#!/usr/bin/env python3
"""Audit complete fixed-width records in interrupted K2SCRN01 partials."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import atomic_json, sha256_file  # noqa: E402
from core_completion_k2_compact import (  # noqa: E402
    HEADER_BYTES,
    PAIRS_PER_LINE,
    RECORD_BYTES,
    STATUS_LIMIT,
    STATUS_UNSAT,
    _read_header_from,
    _unpack_record,
    _validate_record,
)


def audit_partial(path: Path, catalog_sha256: str) -> dict[str, object]:
    with path.open("rb") as handle:
        header = _read_header_from(handle, path)
        if header.catalog_sha256 != catalog_sha256.lower():
            raise ValueError(f"{path}: catalog SHA-256 mismatch")
        size = os.fstat(handle.fileno()).st_size
        if size < HEADER_BYTES:
            raise ValueError(f"{path}: shorter than compact header")
        payload_bytes = size - HEADER_BYTES
        complete_records, trailing_bytes = divmod(
            payload_bytes, RECORD_BYTES
        )
        if complete_records >= header.record_count:
            raise ValueError(f"{path}: partial is not actually incomplete")
        unsat_count = 0
        limit_count = 0
        total_nodes = 0
        max_nodes = 0
        max_elapsed_microseconds = 0
        for index in range(complete_records):
            raw = handle.read(RECORD_BYTES)
            if len(raw) != RECORD_BYTES:
                raise ValueError(f"{path}: truncated complete record {index}")
            record = _unpack_record(raw)
            _validate_record(path, record, index, header.line_start)
            unsat_count += record.status == STATUS_UNSAT
            limit_count += record.status == STATUS_LIMIT
            total_nodes += record.nodes
            max_nodes = max(max_nodes, record.nodes)
            max_elapsed_microseconds = max(
                max_elapsed_microseconds, record.elapsed_microseconds
            )
    complete_lines, next_line_records = divmod(
        complete_records, PAIRS_PER_LINE
    )
    return {
        "path": str(path.resolve()),
        "sha256": sha256_file(path),
        "size_bytes": size,
        "declared_line_start": header.line_start,
        "declared_line_end": header.line_end,
        "declared_record_count": header.record_count,
        "complete_valid_records": complete_records,
        "trailing_incomplete_record_bytes": trailing_bytes,
        "complete_catalog_lines": complete_lines,
        "next_catalog_line": header.line_start + complete_lines,
        "complete_records_in_next_line": next_line_records,
        "unsat_count": unsat_count,
        "limit_count": limit_count,
        "total_nodes": total_nodes,
        "max_nodes": max_nodes,
        "max_elapsed_microseconds": max_elapsed_microseconds,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partial", required=True, type=Path, nargs="+")
    parser.add_argument("--catalog-sha256", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    audits = [
        audit_partial(path, args.catalog_sha256) for path in args.partial
    ]
    result = {
        "schema": "ramsey55.core_completion_k2_partial_prefix_audit.v1",
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": True,
        "evidence_category": "INTERRUPTED-PREFIX DIAGNOSTIC",
        "scope": (
            "complete fixed-width records physically present before a "
            "resource stop; negative statuses remain unchecked observations"
        ),
        "catalog_sha256": args.catalog_sha256.lower(),
        "partial_count": len(audits),
        "complete_valid_record_count": sum(
            int(item["complete_valid_records"]) for item in audits
        ),
        "unsat_count": sum(int(item["unsat_count"]) for item in audits),
        "limit_count": sum(int(item["limit_count"]) for item in audits),
        "negative_certified_count": 0,
        "proof_generation": False,
        "proof_replay": False,
        "partials": audits,
        "runtime_seconds": time.monotonic() - started,
        "checker_source_sha256": sha256_file(Path(__file__)),
    }
    if args.output:
        if args.output.exists():
            raise SystemExit("partial-prefix audit output already exists")
        atomic_json(args.output, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

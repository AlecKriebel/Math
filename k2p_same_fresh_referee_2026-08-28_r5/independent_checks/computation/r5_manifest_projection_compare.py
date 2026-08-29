#!/usr/bin/env python3
"""Compare all residual manifest summaries while excluding only row byte hashes.

This is reviewer-owned and uses only the Python standard library.  It does not
import the submitted compiler, comparator, canonicalizer, or certificate code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED_COUNTS = (536, 747, 276, 276, 64, 32)
EXCLUDED_ROW_FIELDS = frozenset(("record_sha256", "semantic_record_sha256"))


class DuplicateName(ValueError):
    pass


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateName(key)
        result[key] = value
    return result


def load_strict(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if not isinstance(value, dict):
        raise ValueError(f"not an object: {path}")
    return value


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def projection(row: dict[str, object]) -> dict[str, object]:
    missing = EXCLUDED_ROW_FIELDS - row.keys()
    if missing:
        raise ValueError(f"row lacks excluded provenance fields: {sorted(missing)}")
    return {key: value for key, value in row.items() if key not in EXCLUDED_ROW_FIELDS}


def collect(root: Path) -> tuple[dict[tuple[int, int], dict[str, object]], dict[str, object]]:
    records: dict[tuple[int, int], dict[str, object]] = {}
    top_level = {}
    for source_index, expected_count in enumerate(EXPECTED_COUNTS):
        path = root / f"source_{source_index}" / "residual_manifest.json"
        manifest = load_strict(path)
        rows = manifest.get("records")
        if not isinstance(rows, list) or len(rows) != expected_count:
            raise ValueError(f"wrong record count in {path}: {len(rows) if isinstance(rows, list) else None}")
        if manifest.get("source_index") != source_index:
            raise ValueError(f"wrong source index in {path}")
        if manifest.get("record_count") != expected_count:
            raise ValueError(f"wrong declared record count in {path}")
        for expected_id, row in enumerate(rows):
            if not isinstance(row, dict):
                raise ValueError(f"non-object row in {path}")
            class_id = row.get("canonical_class_id")
            if class_id != expected_id:
                raise ValueError(f"noncontiguous class id in {path}: expected {expected_id}, got {class_id}")
            key = (source_index, expected_id)
            if key in records:
                raise ValueError(f"duplicate record key: {key}")
            records[key] = projection(row)
        top_level[str(source_index)] = {
            key: value for key, value in manifest.items() if key != "records"
        }
    return records, top_level


def root_hash(records: dict[tuple[int, int], dict[str, object]]) -> str:
    combined = hashlib.sha256()
    for (source_index, class_id), row in sorted(records.items()):
        row_hash = hashlib.sha256(canonical(row)).hexdigest()
        combined.update(f"{source_index}:{class_id}:{row_hash}\n".encode("ascii"))
    return combined.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    baseline, baseline_top = collect(args.baseline)
    candidate, candidate_top = collect(args.candidate)
    if baseline.keys() != candidate.keys():
        raise SystemExit("MANIFEST_PROJECTION_KEY_MISMATCH")
    mismatches = [key for key in baseline if baseline[key] != candidate[key]]
    if mismatches:
        raise SystemExit(f"MANIFEST_PROJECTION_MISMATCH:{mismatches[:20]}")

    baseline_root = root_hash(baseline)
    candidate_root = root_hash(candidate)
    differing_top_fields: dict[str, list[str]] = {}
    for source_index in baseline_top:
        differing_top_fields[source_index] = sorted(
            key
            for key in baseline_top[source_index].keys() | candidate_top[source_index].keys()
            if baseline_top[source_index].get(key) != candidate_top[source_index].get(key)
        )

    payload = {
        "baseline_projection_sha256": baseline_root,
        "candidate_projection_sha256": candidate_root,
        "differing_top_level_fields_by_source": differing_top_fields,
        "excluded_row_fields": sorted(EXCLUDED_ROW_FIELDS),
        "record_count": len(candidate),
        "semantic_projections_equal": True,
        "status": "PASS",
    }
    payload_hash = hashlib.sha256(canonical(payload)).hexdigest()
    result = {**payload, "payload_sha256": payload_hash}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical(result) + b"\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

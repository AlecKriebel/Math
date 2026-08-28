#!/usr/bin/env python3
"""Fail-closed merge and cross-check of the six source residual manifests."""
from __future__ import annotations

if not __debug__:
    raise SystemExit("K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN")

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_driver(path: Path):
    spec = importlib.util.spec_from_file_location("portable_driver", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--allow-incomplete", action="store_true")
    parser.add_argument("--allow-unresolved", action="store_true")
    args = parser.parse_args()

    package_root = args.package_root.resolve()
    driver = load_driver(package_root / "resumable_four_port_driver.py")
    input_lock = json.loads((package_root / "INPUT_LOCK.json").read_text())
    observed_hashes = driver.validate_input_lock(package_root, input_lock)
    input_lock_hash = sha(package_root / "INPUT_LOCK.json")
    expected_counts = input_lock["expected_source_class_counts"]
    hard_hash = observed_hashes["certificates/direct_hard_cases.json"]
    atlas = driver.load_module(package_root / "atlas" / "k2p_atlas_core.py")
    compiler_hash, canonicalizer_hash = driver.current_hashes(package_root / "atlas", atlas)
    expected_bindings = {
        "compiler_sha256": compiler_hash,
        "canonicalizer_sha256": canonicalizer_hash,
        "descriptor_pickle_sha256": observed_hashes["atlas/descriptors_4.pkl"],
        "rank_pickle_sha256": observed_hashes["atlas/rank_certs_4.pkl"],
        "output_schema_sha256": observed_hashes["schemas/four_port_record_v3.schema.json"],
        "input_lock_sha256": input_lock_hash,
        "hard_certificate_sha256": hard_hash,
    }
    if input_lock.get("compiler_sha256") != compiler_hash:
        raise SystemExit("current compiler disagrees with INPUT_LOCK")
    if input_lock.get("canonicalizer_sha256") != canonicalizer_hash:
        raise SystemExit("current canonicalizer disagrees with INPUT_LOCK")

    rows, bindings, seen, totals = [], None, set(), {}
    binding_keys = (
        "compiler_sha256", "canonicalizer_sha256", "descriptor_pickle_sha256",
        "rank_pickle_sha256", "output_schema_sha256", "input_lock_sha256",
        "hard_certificate_sha256",
    )
    for source, expected_count in enumerate(expected_counts):
        source_dir = args.run_root / f"source_{source}"
        path = source_dir / "residual_manifest.json"
        if not path.exists():
            raise SystemExit(f"missing {path}")
        row = json.loads(path.read_text())
        if row.get("schema") != driver.MANIFEST_SCHEMA or row.get("source_index") != source:
            raise SystemExit(f"wrong schema/source index in {path}")
        current = {key: row.get(key) for key in binding_keys}
        if current != expected_bindings:
            raise SystemExit(f"manifest disagrees with current package bindings in {path}")
        if bindings is None:
            bindings = current
        elif current != bindings:
            raise SystemExit(f"input binding disagreement in {path}")
        if current["hard_certificate_sha256"] != hard_hash:
            raise SystemExit(f"hard certificate binding disagreement in {path}")
        if current["input_lock_sha256"] != input_lock_hash:
            raise SystemExit(f"current INPUT_LOCK binding disagreement in {path}")
        if row.get("canonical_class_count") != expected_count:
            raise SystemExit(f"wrong canonical class count in {path}")

        manifest_records = row.get("records")
        if not isinstance(manifest_records, list):
            raise SystemExit(f"invalid record list in {path}")
        ids = [record.get("canonical_class_id") for record in manifest_records]
        if len(ids) != len(set(ids)) or any(not isinstance(class_id, int) for class_id in ids):
            raise SystemExit(f"duplicate/invalid class id in {path}")
        if row.get("record_count") != len(manifest_records):
            raise SystemExit(f"record count disagreement in {path}")

        for record_summary in manifest_records:
            class_id = record_summary["canonical_class_id"]
            record_path = source_dir / "records" / f"class_{class_id:06d}.json"
            if not record_path.is_file():
                raise SystemExit(f"missing record {record_path}")
            record = json.loads(record_path.read_text())
            driver.validate_record_semantics(record, record_path, hard_hash)
            if record.get("source_index") != source or record.get("canonical_class_id") != class_id:
                raise SystemExit(f"record source/class identity disagreement: {record_path}")
            expected_summary = {
                "canonical_class_id": class_id,
                "status": record["status"],
                "stratum": record["stratum"],
                "descriptor_sha256": record["descriptor_sha256"],
                "record_sha256": sha(record_path),
                "semantic_record_sha256": record["semantic_record_sha256"],
                "omitted_roles": record["omitted_roles"],
                "child_requests": record["child_requests"],
            }
            if record_summary != expected_summary:
                raise SystemExit(f"record summary disagreement in {path}: class {class_id}")
            for key, value in current.items():
                if record.get(key) != value:
                    raise SystemExit(f"record binding disagreement: {record_path}: {key}")

        exact_ids = set(range(expected_count))
        complete = set(ids) == exact_ids and len(ids) == expected_count
        if bool(row.get("complete")) != complete:
            raise SystemExit(f"false completion flag in {path}")
        if not complete and not args.allow_incomplete:
            raise SystemExit(f"incomplete source manifest: {path}")
        expected_unresolved = sorted(
            record["canonical_class_id"] for record in manifest_records
            if record["status"] == "unresolved"
        )
        expected_restoration = sorted(
            record["canonical_class_id"] for record in manifest_records
            if record["status"] == "restoration_parent"
        )
        if row.get("unresolved") != expected_unresolved:
            raise SystemExit(f"unresolved summary disagreement in {path}")
        if row.get("restoration_candidates") != expected_restoration:
            raise SystemExit(f"restoration summary disagreement in {path}")
        manifest_immutable = {"schema": driver.SCHEMA, **current}
        expected_semantic_manifest = driver.semantic_manifest_hash(
            source, expected_count, manifest_immutable, manifest_records
        )
        if row.get("semantic_manifest_sha256") != expected_semantic_manifest:
            raise SystemExit(f"semantic manifest hash disagreement in {path}")
        for status in driver.VALID_STATUSES:
            totals[status] = totals.get(status, 0) + sum(
                record["status"] == status for record in manifest_records
            )
        rows.append({
            "source_index": source,
            "manifest_sha256": sha(path),
            "semantic_manifest_sha256": expected_semantic_manifest,
            "complete": complete,
            "canonical_class_count": expected_count,
            "record_count": len(manifest_records),
            "unresolved": expected_unresolved,
            "restoration_candidates": expected_restoration,
        })
        seen.add(source)

    payload = {
        "schema": "k2p-four-port-six-source-merge-v2",
        "bindings": bindings,
        "sources": rows,
        "all_six_sources_present": seen == set(range(6)),
        "all_manifests_complete": all(row["complete"] for row in rows),
        "total_status_counts": totals,
        "unresolved_by_source": {
            str(row["source_index"]): row["unresolved"] for row in rows if row["unresolved"]
        },
        "restoration_candidate_counts": {
            str(row["source_index"]): len(row["restoration_candidates"]) for row in rows
        },
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["payload_sha256_without_hash"] = hashlib.sha256(raw).hexdigest()
    payload["semantic_sweep_sha256"] = driver.sha_object({
        "schema": payload["schema"],
        "bindings": bindings,
        "sources": [
            {
                "source_index": row["source_index"],
                "canonical_class_count": row["canonical_class_count"],
                "semantic_manifest_sha256": row["semantic_manifest_sha256"],
            }
            for row in rows
        ],
    })
    out = args.run_root / "FOUR_PORT_SWEEP_MERGED_STATUS.json"
    driver.atomic_json(out, payload)
    print(json.dumps({
        "output": str(out), "complete": payload["all_manifests_complete"],
        "counts": totals, "unresolved_by_source": payload["unresolved_by_source"],
    }, sort_keys=True))
    if payload["unresolved_by_source"] and not args.allow_unresolved:
        raise SystemExit("unresolved classes remain (use --allow-unresolved only for exploratory merges)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent audit of the metadata-only schema-3 shard-0 migration."""

from __future__ import annotations

from pathlib import Path
import copy
import hashlib
import json

from graph_model import digest, stable_json


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIMARY = ROOT / "primary/certificates"

EXPECTED_FULL_SUMMARY = "791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65"
EXPECTED_BEFORE = "1c10a0ec402a43a0cce6609b0dedc75e2ec9b94131cb1d28f2bea18cc2ba3127"
EXPECTED_AFTER = "326be8f0ba7a02d07d47c5e2beebcca7b88418dd204f35fbdb44e3f770feddff"
CONVENTION = "rooted_selected_side_masks_before_zero_sum_complement_zip"


def sha(path):
    answer = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def main():
    failures = []
    full_summary_path = PRIMARY / "hard_cover_schema3_n3_full_summary.json"
    migration_path = PRIMARY / "hard_cover_schema3_n3_s0_metadata_migration.json"
    migration = json.loads(migration_path.read_text())
    summaries = [
        json.loads((PRIMARY / f"hard_cover_schema3_n3_s{index}_summary.json").read_text())
        for index in range(4)
    ]
    if sha(full_summary_path) != EXPECTED_FULL_SUMMARY:
        failures.append(("full summary SHA-256", sha(full_summary_path), EXPECTED_FULL_SUMMARY))
    shard_zero_path = PRIMARY / "hard_cover_schema3_n3_s0_summary.json"
    if sha(shard_zero_path) != EXPECTED_AFTER:
        failures.append(("shard-0 after SHA-256", sha(shard_zero_path), EXPECTED_AFTER))
    if migration.get("after_summary_sha256") != EXPECTED_AFTER:
        failures.append(("migration after hash", migration.get("after_summary_sha256")))
    if migration.get("before_summary_sha256") != EXPECTED_BEFORE:
        failures.append(("migration before hash", migration.get("before_summary_sha256")))
    field = migration.get("field_added")
    if field != {"runs[0].bounded_summary.descriptor_mask_convention": CONVENTION}:
        failures.append(("migration field", field))
    if migration.get("mathematical_or_stream_bytes_changed") is not False:
        failures.append(("migration change declaration", migration.get("mathematical_or_stream_bytes_changed")))

    reconstructed_before = copy.deepcopy(summaries[0])
    actual_convention = reconstructed_before["runs"][0]["bounded_summary"].pop(
        "descriptor_mask_convention", None,
    )
    if actual_convention != CONVENTION:
        failures.append(("shard-0 convention", actual_convention, CONVENTION))
    reconstructed_bytes = (json.dumps(reconstructed_before, indent=2) + "\n").encode()
    reconstructed_before_hash = hashlib.sha256(reconstructed_bytes).hexdigest()
    if reconstructed_before_hash != EXPECTED_BEFORE:
        failures.append(("reconstructed pre-migration hash", reconstructed_before_hash, EXPECTED_BEFORE))

    normalized_bounded = []
    for index, summary in enumerate(summaries):
        bounded = copy.deepcopy(summary["runs"][0]["bounded_summary"])
        convention = bounded.pop("descriptor_mask_convention", None)
        bounded.pop("elapsed_seconds", None)
        if convention != CONVENTION:
            failures.append(("shard convention", index, convention))
        normalized_bounded.append(bounded)
    if any(value != normalized_bounded[0] for value in normalized_bounded[1:]):
        failures.append("shard bounded summaries differ beyond timing/convention metadata")

    full_summary = json.loads(full_summary_path.read_text())
    shard_input_hashes = full_summary.get("merged_shard_inputs", {})
    checked_inputs = {}
    for raw_path, expected in sorted(shard_input_hashes.items()):
        path = Path(raw_path)
        if not path.is_absolute():
            path = ROOT / path
        actual = sha(path)
        checked_inputs[str(path)] = actual
        if actual != expected:
            failures.append(("merged shard input hash", str(path), actual, expected))

    cert = {
        "schema": 1,
        "status": "VERIFIED" if not failures else "FALSE",
        "full_summary_sha256": sha(full_summary_path),
        "migration_file_sha256": sha(migration_path),
        "shard_zero_before_sha256_reconstructed": reconstructed_before_hash,
        "shard_zero_after_sha256": sha(shard_zero_path),
        "field_added": field,
        "normalized_bounded_summary_commitment": digest(normalized_bounded[0]),
        "all_four_bounded_summaries_equal_after_metadata_removal": (
            not any(value != normalized_bounded[0] for value in normalized_bounded[1:])
        ),
        "merged_shard_input_count": len(checked_inputs),
        "merged_shard_input_hashes": checked_inputs,
        "mathematical_or_stream_bytes_changed_by_reconstructed_migration": False,
        "failure_count": len(failures),
        "first_failures": failures[:50],
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    output = HERE / "certificates/schema3_n3_metadata_migration_audit.json"
    output.write_text(stable_json(cert) + "\n")
    print(stable_json({
        "status": cert["status"], "checked_inputs": len(checked_inputs),
        "hash": cert["normalized_sha256_without_hash"],
    }))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

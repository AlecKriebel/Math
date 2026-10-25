#!/usr/bin/env python3
"""Adversarial omission, duplication, false-rank, and optimized-mode tests."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from ledger_common import AUDIT_ROOT, atomic_json, deterministic_gzip, fail, sha_file, sha_object


def invoke(artifact_root: Path, optimized: bool = False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(
        [
            "-B",
            str(AUDIT_ROOT / "verify_raw_ledger.py"),
            "--artifact-root",
            str(artifact_root),
            "--quick",
        ]
    )
    environment = dict(os.environ)
    environment.pop("PYTHONOPTIMIZE", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        cwd=AUDIT_ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=180,
    )


def require_rejection(result, marker: bytes, label: str) -> None:
    output = result.stdout + result.stderr
    if result.returncode == 0 or marker not in output:
        fail(
            "RAW_LEDGER_MUTATION_FALSE_ACCEPT",
            {"case": label, "returncode": result.returncode, "output": output[-2000:]},
        )
    print(
        f"RAW_LEDGER_MUTATION_REJECTED case={label} "
        f"output_sha256={hashlib.sha256(output).hexdigest()}"
    )


def ledger_rows(path: Path):
    with gzip.open(path, "rb") as handle:
        return list(handle)


def rewrite_ledger(root: Path, rows: list[bytes]) -> None:
    path = root / "raw_directional_ledger.jsonl.gz"
    plain_hash, plain_bytes = deterministic_gzip(path, rows)
    summary = json.loads((root / "raw_ledger_summary.json").read_text())
    metadata = summary["artifacts"]["raw_directional_ledger.jsonl.gz"]
    metadata.update(
        {
            "sha256": sha_file(path),
            "uncompressed_sha256": plain_hash,
            "uncompressed_bytes": plain_bytes,
        }
    )
    summary.pop("payload_sha256_without_hash", None)
    summary["payload_sha256_without_hash"] = sha_object(summary)
    atomic_json(root / "raw_ledger_summary.json", summary)


def main() -> None:
    if not __debug__:
        fail("RAW_LEDGER_MUTATION_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, default=AUDIT_ROOT / "artifacts")
    parser.add_argument(
        "--report",
        type=Path,
        default=AUDIT_ROOT / "artifacts/raw_ledger_mutation_report.json",
    )
    args = parser.parse_args()
    source = args.artifact_root.resolve()
    baseline_result = invoke(source)
    if baseline_result.returncode != 0 or b"RAW_LEDGER_EXACT_RANK_UPPER_PASS" not in baseline_result.stdout:
        fail("RAW_LEDGER_MUTATION_BASELINE_FAIL", baseline_result.stdout + baseline_result.stderr)
    require_rejection(
        invoke(source, optimized=True),
        b"RAW_LEDGER_OPTIMIZED_MODE_FORBIDDEN",
        "optimized_mode",
    )
    with tempfile.TemporaryDirectory(prefix="k2p_raw_ledger_mutations_") as temporary:
        temporary_root = Path(temporary)
        for label in (
            "omitted_raw_row",
            "duplicated_raw_row",
            "topology_witness_corruption",
            "false_rank_exclusion",
            "retained_class_reassignment",
            "rank_upper_binding_corruption",
        ):
            case_root = temporary_root / label
            shutil.copytree(source, case_root)
            if label == "rank_upper_binding_corruption":
                path = case_root / "rank_upper_binding.json.gz"
                payload = json.loads(gzip.decompress(path.read_bytes()))
                payload["descriptors"][0]["exact_rank"] -= 1
                plain_hash, plain_bytes = deterministic_gzip(
                    path, (canonical_line(payload),)
                )
                summary = json.loads(
                    (case_root / "raw_ledger_summary.json").read_text()
                )
                summary["artifacts"]["rank_upper_binding.json.gz"].update(
                    {
                        "sha256": sha_file(path),
                        "uncompressed_sha256": plain_hash,
                        "uncompressed_bytes": plain_bytes,
                    }
                )
                summary.pop("payload_sha256_without_hash", None)
                summary["payload_sha256_without_hash"] = sha_object(summary)
                atomic_json(case_root / "raw_ledger_summary.json", summary)
                require_rejection(
                    invoke(case_root),
                    b"RAW_LEDGER_UPPER_ROW_BINDING_FAIL",
                    label,
                )
                continue
            rows = ledger_rows(case_root / "raw_directional_ledger.jsonl.gz")
            if label == "omitted_raw_row":
                del rows[12345]
                marker = b"RAW_LEDGER_RAW_ID_CENSUS_FAIL"
            elif label == "duplicated_raw_row":
                rows.insert(12345, rows[12345])
                marker = b"RAW_LEDGER_RAW_ID_CENSUS_FAIL"
            elif label == "topology_witness_corruption":
                mutated = False
                for index, raw in enumerate(rows):
                    row = json.loads(raw)
                    reason = row.get("topology_exclusion_reason")
                    if reason in {"quartet", "tree_sunlet"}:
                        row["topology_exclusion_reason"] = (
                            "tree_sunlet" if reason == "quartet" else "quartet"
                        )
                        rows[index] = canonical_line(row)
                        mutated = True
                        break
                if not mutated:
                    fail("RAW_LEDGER_TOPOLOGY_MUTATION_TARGET_MISSING")
                marker = b"RAW_LEDGER_TOPOLOGY_REASON_CENSUS_FAIL"
            elif label == "false_rank_exclusion":
                mutated = False
                for index, raw in enumerate(rows):
                    row = json.loads(raw)
                    if row.get("category") == "retained_terminal":
                        row["category"] = "rank_excluded"
                        for key in (
                            "class_id",
                            "status",
                            "restoration_obligation_id",
                        ):
                            row.pop(key, None)
                        rows[index] = canonical_line(row)
                        mutated = True
                        break
                if not mutated:
                    fail("RAW_LEDGER_MUTATION_TARGET_MISSING")
                marker = b"RAW_LEDGER_FALSE_RANK_EXCLUSION"
            else:
                class_payload = json.loads(
                    gzip.decompress(
                        (case_root / "retained_class_partition.json.gz").read_bytes()
                    )
                )
                terminal_by_source = {}
                for class_row in class_payload["classes"]:
                    if class_row["ledger_category"] == "retained_terminal":
                        terminal_by_source.setdefault(class_row["source_index"], []).append(class_row)
                mutated = False
                for index, raw in enumerate(rows):
                    row = json.loads(raw)
                    if row.get("category") != "retained_terminal":
                        continue
                    alternatives = [
                        candidate
                        for candidate in terminal_by_source[row["source_index"]]
                        if candidate["canonical_class_id"] != row["class_id"]
                        and candidate["descriptor_sha256"] != row["descriptor_sha256"]
                    ]
                    if alternatives:
                        row["class_id"] = alternatives[0]["canonical_class_id"]
                        rows[index] = canonical_line(row)
                        mutated = True
                        break
                if not mutated:
                    fail("RAW_LEDGER_CLASS_REASSIGNMENT_TARGET_MISSING")
                marker = b"RAW_LEDGER_CLASS_REFERENCE_BINDING_FAIL"
            rewrite_ledger(case_root, rows)
            require_rejection(invoke(case_root), marker, label)
    report = {
        "schema": "k2p-four-port-raw-ledger-mutation-report-v1",
        "status": "PASS",
        "mutations_rejected": 7,
        "survivors": 0,
        "tests": [
            "optimized_mode",
            "omitted_raw_row",
            "duplicated_raw_row",
            "topology_witness_corruption",
            "false_rank_exclusion",
            "retained_class_reassignment",
            "rank_upper_binding_corruption",
        ],
    }
    atomic_json(args.report.resolve(), report)
    print("RAW_LEDGER_MUTATIONS_PASS rejected=7 survivors=0")


def canonical_line(value: dict) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n"


if __name__ == "__main__":
    main()

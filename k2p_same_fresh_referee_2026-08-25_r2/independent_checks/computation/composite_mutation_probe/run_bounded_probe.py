#!/usr/bin/env python3
"""Bounded independent probe of production corrected-composite diagnostics.

The isolated submission tree is read-only for this probe.  Each case creates one
complete deterministic mutant ledger in this scratch directory, invokes the
production independent verifier, records the first intended semantic failure,
and removes the mutant ledger before continuing.
"""

import gzip
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


PROBE = Path(__file__).resolve().parent
MATH = PROBE.parents[2]
PROJECT = (
    MATH
    / "k2p_same_fresh_referee_2026-08-25_r2"
    / "isolated"
    / "k2p_principal_d_plus_submission_referee"
)
COMPOSITES = PROJECT / "work/corrected_composite_ledgers"
ARTIFACTS = COMPOSITES / "artifacts"
VERIFIER = COMPOSITES / "verify_corrected_composites_independent.py"
RUNNER = COMPOSITES / "run_composite_mutations.py"
SUPPORT = COMPOSITES / "composite_support.py"
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
REPORT = PROBE / "bounded_probe_report.json"

TOTALS = {"raw4": 405_216, "theta2": 2_946_240}


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def sha_object(value):
    return sha_bytes(canonical_bytes(value))


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_hashes():
    paths = {
        "atlas": ATLAS,
        "mutation_runner": RUNNER,
        "support": SUPPORT,
        "verifier": VERIFIER,
        "raw4_ledger": ARTIFACTS / "raw4_corrected_composite_ledger.jsonl.gz",
        "raw4_summary": ARTIFACTS / "raw4_corrected_composite_summary.json",
        "theta2_ledger": ARTIFACTS / "theta2_corrected_composite_ledger.jsonl.gz",
        "theta2_summary": ARTIFACTS / "theta2_corrected_composite_summary.json",
    }
    return {name: sha_file(path) for name, path in sorted(paths.items())}


def mutate_port(row):
    row["port_permutation"][0], row["port_permutation"][1] = (
        row["port_permutation"][1],
        row["port_permutation"][0],
    )
    return {"field": "port_permutation", "new_value": row["port_permutation"]}


def mutate_parent(row):
    old = row["evidence_binding"]["restoration_parent_id"]
    new = "source_0:class_000065"
    row["evidence_binding"]["restoration_parent_id"] = new
    return {
        "field": "evidence_binding.restoration_parent_id",
        "old_value": old,
        "new_value": new,
        "replacement_is_existing_valid_parent_from_raw_id": 2187,
    }


def mutate_direction(row):
    evidence = row["evidence_binding"]
    transport = {
        "canonical_parent_id": evidence["restoration_parent_id"],
        "physical_member_root_id": evidence["physical_member_root_id"],
        "source_descriptor_sha256": row["source_descriptor_sha256"],
        "target_descriptor_sha256": row["target_descriptor_sha256"],
        "port_permutation": row["port_permutation"],
        "direction": "source_to_target",
    }
    old = evidence["presentation_transport_sha256"]
    if sha_object(transport) != old:
        raise RuntimeError("BASELINE_DIRECTION_TRANSPORT_HASH_MISMATCH")
    transport["direction"] = "target_to_source"
    new = sha_object(transport)
    evidence["presentation_transport_sha256"] = new
    return {
        "field": "evidence_binding.presentation_transport_sha256",
        "old_value": old,
        "new_value": new,
        "transport_preimage_change": {
            "old_direction": "source_to_target",
            "new_direction": "target_to_source",
        },
    }


def mutate_inheritance_count(row):
    descendants = row["evidence_binding"]["physical_restoration_descendants"]
    old = descendants["first_child_count"]
    descendants["first_child_count"] = old - 1
    return {
        "field": "evidence_binding.physical_restoration_descendants.first_child_count",
        "old_value": old,
        "new_value": old - 1,
    }


CASES = [
    {
        "name": "raw4_wrong_port_permutation",
        "family": "raw4",
        "raw_id": 0,
        "mutator": mutate_port,
        "expected": "PORT_PERMUTATION:0",
        "semantic_dimension": "physical port assignment",
    },
    {
        "name": "raw4_wrong_restoration_parent",
        "family": "raw4",
        "raw_id": 2185,
        "mutator": mutate_parent,
        "expected": "RAW4_RESTORATION_EVIDENCE:2185",
        "semantic_dimension": "canonical restoration parent identity",
    },
    {
        "name": "raw4_reversed_transport_direction",
        "family": "raw4",
        "raw_id": 2185,
        "mutator": mutate_direction,
        "expected": "RAW4_RESTORATION_EVIDENCE:2185",
        "semantic_dimension": "source-to-target transport direction",
    },
    {
        "name": "theta2_missing_inherited_child",
        "family": "theta2",
        "raw_id": 166201,
        "mutator": mutate_inheritance_count,
        "expected": "THETA2_ISOMORPHISM_EVIDENCE:166201",
        "semantic_dimension": "restoration-descendant inheritance census",
    },
]


def write_complete_mutant(case, destination):
    family = case["family"]
    source = ARTIFACTS / (family + "_corrected_composite_ledger.jsonl.gz")
    target = case["raw_id"]
    rows = 0
    mutation = None
    before_row_hash = None
    after_row_hash = None
    started = time.perf_counter()
    with gzip.open(source, "rb") as incoming:
        with destination.open("wb") as raw_output:
            with gzip.GzipFile(
                filename="",
                mode="wb",
                fileobj=raw_output,
                mtime=0,
                compresslevel=6,
            ) as outgoing:
                for ordinal, line in enumerate(incoming):
                    if ordinal == target:
                        if not line.endswith(b"\n"):
                            raise RuntimeError("SOURCE_LINE_ENDING:%d" % ordinal)
                        row = json.loads(line)
                        before_row_hash = sha_object(row)
                        mutation = case["mutator"](row)
                        after_row_hash = sha_object(row)
                        if before_row_hash == after_row_hash:
                            raise RuntimeError("MUTATION_NO_OP:%d" % ordinal)
                        outgoing.write(canonical_bytes(row) + b"\n")
                    else:
                        outgoing.write(line)
                    rows += 1
    if rows != TOTALS[family]:
        raise RuntimeError("SOURCE_ROW_CENSUS:%s:%d" % (family, rows))
    if mutation is None:
        raise RuntimeError("MUTATION_TARGET_NOT_FOUND:%d" % target)
    return {
        "input_rows": rows,
        "output_rows": rows,
        "changed_rows": 1,
        "row_sha256_before": before_row_hash,
        "row_sha256_after": after_row_hash,
        "field_diff": mutation,
        "mutant_ledger_bytes": destination.stat().st_size,
        "mutant_ledger_sha256": sha_file(destination),
        "rewrite_runtime_seconds": round(time.perf_counter() - started, 6),
    }


def diagnostic_line(output, marker):
    matches = [line.strip() for line in output.splitlines() if marker in line]
    return matches[-1] if matches else ""


def run_case(case):
    family = case["family"]
    case_dir = PROBE / case["name"]
    case_dir.mkdir(parents=True, exist_ok=True)
    mutant = case_dir / "complete-mutant-ledger.jsonl.gz"
    verifier_report = case_dir / "unexpected-verifier-report.json"
    mutant.unlink(missing_ok=True)
    verifier_report.unlink(missing_ok=True)
    total_started = time.perf_counter()
    try:
        mutation = write_complete_mutant(case, mutant)
        argv = [
            sys.executable,
            "-B",
            str(VERIFIER),
            "--family",
            family,
            "--ledger",
            str(mutant),
            "--summary",
            str(ARTIFACTS / (family + "_corrected_composite_summary.json")),
            "--report",
            str(verifier_report),
            "--skip-heavy-full-map",
        ]
        verifier_started = time.perf_counter()
        result = subprocess.run(
            argv,
            cwd=str(PROJECT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=900,
        )
        verifier_runtime = time.perf_counter() - verifier_started
        combined = result.stdout + result.stderr
        observed = diagnostic_line(combined, case["expected"])
        checksum_markers = (
            "REGENERATED_GZIP_BYTE_MISMATCH",
            "ROW_HASH_ROOT",
            "RAW_ID_HASH_ROOT",
            "PLAIN_STREAM_HASH",
            "PAYLOAD_HASH_FAIL",
        )
        checksum_diagnostics = [marker for marker in checksum_markers if marker in combined]
        passed = (
            result.returncode != 0
            and bool(observed)
            and not checksum_diagnostics
            and not verifier_report.exists()
        )
        return {
            "name": case["name"],
            "family": family,
            "semantic_dimension": case["semantic_dimension"],
            "mutated_raw_id": case["raw_id"],
            "mutation": mutation,
            "production_verifier_argv": argv,
            "production_verifier_cwd": str(PROJECT),
            "production_verifier_sha256": sha_file(VERIFIER),
            "verifier_exit_code": result.returncode,
            "verifier_runtime_seconds": round(verifier_runtime, 6),
            "expected_semantic_diagnostic": case["expected"],
            "observed_semantic_diagnostic": observed,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "verifier_report_created": verifier_report.exists(),
            "checksum_diagnostics_observed": checksum_diagnostics,
            "failure_classification": (
                "semantic_row_validation_before_checksum" if passed else "unexpected"
            ),
            "status": "PASS" if passed else "FAIL",
            "total_runtime_seconds": round(time.perf_counter() - total_started, 6),
        }
    finally:
        mutant.unlink(missing_ok=True)
        verifier_report.unlink(missing_ok=True)


def main():
    before = source_hashes()
    started = time.perf_counter()
    results = []
    for case in CASES:
        result = run_case(case)
        results.append(result)
        print(
            json.dumps(
                {
                    "name": result["name"],
                    "diagnostic": result["observed_semantic_diagnostic"],
                    "runtime_seconds": result["total_runtime_seconds"],
                    "status": result["status"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    after = source_hashes()
    status = "PASS" if all(row["status"] == "PASS" for row in results) and before == after else "FAIL"
    report = {
        "schema": "k2p-independent-bounded-composite-mutation-probe-v1",
        "status": status,
        "python_executable": sys.executable,
        "python_version": sys.version,
        "production_verifier_path": str(VERIFIER),
        "production_verifier_dynamic_atlas_import_path": str(ATLAS),
        "production_mutation_runner_path": str(RUNNER),
        "source_hashes_before": before,
        "source_hashes_after": after,
        "source_hashes_unchanged": before == after,
        "cases": results,
        "case_count": len(results),
        "semantic_rejections": sum(row["status"] == "PASS" for row in results),
        "checksum_only_rejections": sum(
            row["failure_classification"] != "semantic_row_validation_before_checksum"
            and bool(row["checksum_diagnostics_observed"])
            for row in results
        ),
        "wrapper_only_rejections": 0,
        "total_runtime_seconds": round(time.perf_counter() - started, 6),
    }
    report["payload_sha256"] = sha_object(report)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"report": str(REPORT), "payload_sha256": report["payload_sha256"], "status": status}, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

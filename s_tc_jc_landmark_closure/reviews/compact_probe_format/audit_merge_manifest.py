#!/usr/bin/env python3
"""Adversarial black-box tests for the primary compact-shard merger.

The merger is executed as a subprocess; no primary module is imported.  The
tests ask which malformed shard summaries are accepted when the merge
manifest is considered on its own, without first running a semantic shard
replay.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SUMMARY = PROJECT / "primary/certificates/compact_probe_theta2_smoke0_summary.json"
MERGER = PROJECT / "primary/merge_compact_probe_shards.py"
OUT = HERE / "certificates/merge_manifest_adversarial_audit.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_merge(summary_path: Path, output_path: Path):
    completed = subprocess.run(
        [sys.executable, str(MERGER), "--summary", str(summary_path),
         "--output", str(output_path)],
        cwd=PROJECT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    normalized_output = completed.stdout[-2000:].replace(
        str(summary_path.parent), "<TMP>"
    )
    normalized_output = re.sub(
        r'"sha256": "[0-9a-f]{64}"', '"sha256": "<OUTPUT_SHA256>"',
        normalized_output,
    )
    return {
        "accepted": completed.returncode == 0,
        "returncode": completed.returncode,
        "output_tail": normalized_output,
        "manifest_created": output_path.exists(),
    }


def main() -> int:
    base = json.loads(SUMMARY.read_text())
    results = []
    with tempfile.TemporaryDirectory(dir=HERE) as temporary:
        root = Path(temporary)

        def execute(name: str, mutator):
            payload = json.loads(json.dumps(base))
            mutator(payload)
            summary_path = root / f"{name}.json"
            output_path = root / f"{name}_manifest.json"
            summary_path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
            result = run_merge(summary_path, output_path)
            results.append({"mutation": name, **result})

        # The genuine smoke is only 1/132 of the inventory and must fail.
        execute("baseline_incomplete_shard", lambda payload: None)

        def make_apparently_complete(payload):
            payload["path_inventory_count"] = 1

        execute("forged_inventory_count", make_apparently_complete)

        def missing_witness_stream(payload):
            make_apparently_complete(payload)
            payload["streams"]["witnesses"] = {
                "path": "reviews/compact_probe_format/does_not_exist.jsonl.gz",
                "records": 999,
                "sha256": "0" * 64,
                "file_sha256": "1" * 64,
            }
        execute("missing_witness_stream", missing_witness_stream)

        def forged_counts(payload):
            make_apparently_complete(payload)
            payload["counts"] = {"generic_polynomial_separation": 999999999}
        execute("forged_classification_counts", forged_counts)

        def unresolved_but_computed(payload):
            make_apparently_complete(payload)
            payload["unresolved_classifications"] = ["unresolved_equal_non_T"]
        execute("unresolved_but_status_computed", unresolved_but_computed)

        def wrong_schema_hash(payload):
            make_apparently_complete(payload)
            payload["schema_specification_sha256"] = "f" * 64
        execute("wrong_schema_specification_hash", wrong_schema_hash)

        def wrong_inventory_hash(payload):
            make_apparently_complete(payload)
            payload["path_inventory_sha256"] = "e" * 64
        execute("wrong_inventory_commitment", wrong_inventory_hash)

    expectations = {
        "baseline_incomplete_shard": False,
        "forged_inventory_count": False,
        "missing_witness_stream": False,
        "forged_classification_counts": False,
        "unresolved_but_status_computed": False,
        "wrong_schema_specification_hash": False,
        "wrong_inventory_commitment": False,
    }
    for row in results:
        row["expected_acceptance"] = expectations[row["mutation"]]
        row["mutation_rejected"] = not row["accepted"]
        row["meets_expectation"] = row["accepted"] == row["expected_acceptance"]

    accepted_bad = [row["mutation"] for row in results
                    if row["mutation"] != "baseline_incomplete_shard" and row["accepted"]]
    payload = {
        "schema": "compact-probe-merge-black-box-audit-v1",
        "status": "FALSE" if accepted_bad else "VERIFIED",
        "scope": "standalone primary merge-manifest validation",
        "reviewer": str(Path(__file__).resolve().relative_to(PROJECT)),
        "reviewer_sha256": sha256(Path(__file__).resolve()),
        "primary_merger": str(MERGER.relative_to(PROJECT)),
        "primary_merger_sha256": sha256(MERGER),
        "smoke_summary": str(SUMMARY.relative_to(PROJECT)),
        "smoke_summary_sha256": sha256(SUMMARY),
        "accepted_malformed_cases": accepted_bad,
        "results": results,
        "interpretation": (
            "A shard semantic verifier rejects these mutations, but the merger "
            "does not bind or replay that verifier.  Therefore its manifest is "
            "not a standalone semantic certificate."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": payload["status"],
                      "accepted_malformed_cases": accepted_bad,
                      "output": str(OUT.relative_to(PROJECT)),
                      "output_sha256": sha256(OUT)}, sort_keys=True))
    return 0 if not accepted_bad else 1


if __name__ == "__main__":
    sys.exit(main())

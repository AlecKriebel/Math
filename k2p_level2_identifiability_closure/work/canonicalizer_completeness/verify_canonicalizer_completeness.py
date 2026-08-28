#!/usr/bin/env python3
"""Fail-closed replay of the canonicalizer completeness certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import StrictJSONError, decode_json_document  # noqa: E402

CERTIFICATE = HERE / "canonicalizer_completeness_certificate.json"
MUTATIONS = HERE / "canonicalizer_completeness_mutation_certificate.json"
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RAW = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
MUTATION_DIAGNOSTICS = {
    "accept_nonordinary_split_heads": (
        "CANONICALIZER_COMPLETENESS_FAIL:NONORDINARY_ATLAS_ACCEPTED"
    ),
    "erase_without_marking_selected_triangle": (
        "CANONICALIZER_COMPLETENESS_FAIL:SELECTED_TRIANGLE_ATLAS_ACCEPTED: triangle"
    ),
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition, code):
    if not condition:
        raise SystemExit(f"CANONICALIZER_COMPLETENESS_REPLAY_FAIL:{code}")


def load_plain_json(path: Path):
    try:
        return decode_json_document(
            path.read_bytes(), label=path.name, require_object=True
        )
    except (OSError, StrictJSONError) as error:
        raise SystemExit(
            f"CANONICALIZER_COMPLETENESS_REPLAY_FAIL:STRICT_JSON:{error}"
        ) from error


def check_payload(certificate):
    payload = dict(certificate)
    expected = payload.pop("payload_sha256")
    require(hashlib.sha256(canonical(payload)).hexdigest() == expected, "PAYLOAD_HASH")
    require(certificate["schema"] == "k2p-canonicalizer-completeness-v1", "SCHEMA")
    require(certificate["status"] == "PASS", "STATUS")
    require(
        certificate["inputs"]["auditor_sha256"]
        == sha_file(HERE / "canonicalizer_audit.py"),
        "AUDITOR_HASH",
    )
    require(certificate["inputs"]["atlas_sha256"] == sha_file(ATLAS), "ATLAS_HASH")
    require(certificate["inputs"]["raw_ledger_sha256"] == sha_file(RAW), "RAW_HASH")
    descriptor = certificate["descriptor_audit"]
    require(descriptor["primitive_archetypes_compared"] == 10_084, "DESCRIPTOR_COUNT")
    require(descriptor["slow_fast_disagreements"] == 0, "DESCRIPTOR_DISAGREEMENT")
    relation = certificate["relation_audit"]
    require(relation["rank_and_topology_eligible_presentations"] == 4_012, "RELATION_COUNT")
    require(relation["disagreements"] == 0, "RELATION_DISAGREEMENT")
    require(relation["strict_triangle_presentations"] == 54, "TRIANGLE_COUNT")
    contract = certificate["semantic_mutation_contract"]
    require(contract["nonordinary_triangle"]["conclusion"] == "rejected", "NONORDINARY")
    require(contract["selected_triangle_mismatch"]["conclusion"] == "rejected", "MARKER")


def check_mutations(report):
    payload = dict(report)
    expected = payload.pop("payload_sha256")
    require(hashlib.sha256(canonical(payload)).hexdigest() == expected, "MUTATION_PAYLOAD_HASH")
    require(report["schema"] == "k2p-canonicalizer-completeness-mutations-v2", "MUTATION_SCHEMA")
    require(report["status"] == "PASS", "MUTATION_STATUS")
    require(report["atlas_sha256"] == sha_file(ATLAS), "MUTATION_ATLAS_HASH")
    require(
        report["auditor_sha256"] == sha_file(HERE / "canonicalizer_audit.py"),
        "MUTATION_AUDITOR_HASH",
    )
    require(
        report.get("mutation_runner_sha256")
        == sha_file(HERE / "test_canonicalizer_mutations.py"),
        "MUTATION_RUNNER_HASH",
    )
    require(report["rejected"] == 2 and report["survived"] == 0, "MUTATION_CENSUS")
    require(report.get("diagnostic_contract") == MUTATION_DIAGNOSTICS, "MUTATION_DIAGNOSTIC_CONTRACT")
    baseline = report.get("clean_baseline")
    require(
        isinstance(baseline, dict)
        and baseline.get("returncode") == 0
        and baseline.get("status") == "PASS"
        and baseline.get("mode") == "semantic-only"
        and baseline.get("artifact_contract")
        == (
            "The semantic-only auditor reports PASS on stdout and intentionally "
            "must not create the supplied --output success artifact."
        )
        and baseline.get("success_artifact_absent") is True
        and baseline.get("timeout") is False
        and baseline.get("signal") is False
        and baseline.get("semantic_mutation_contract")
        == load_plain_json(CERTIFICATE)["semantic_mutation_contract"],
        "MUTATION_BASELINE",
    )
    rows = report.get("mutations")
    require(
        isinstance(rows, list) and [row.get("name") for row in rows] == list(MUTATION_DIAGNOSTICS),
        "MUTATION_NAMES",
    )
    mutated_hashes = [row.get("mutated_atlas_sha256") for row in rows]
    require(
        all(
            isinstance(digest, str)
            and len(digest) == 64
            and all(character in "0123456789abcdef" for character in digest)
            and digest != report["atlas_sha256"]
            for digest in mutated_hashes
        )
        and len(set(mutated_hashes)) == len(mutated_hashes),
        "MUTATION_ATLAS_HASHES",
    )
    for row in rows:
        expected = MUTATION_DIAGNOSTICS[row["name"]]
        require(
            row.get("rejected") is True
            and row.get("exit_code") == 1
            and row.get("expected_diagnostic") == expected
            and row.get("observed_diagnostic") == expected
            and row.get("success_artifact_absent") is True
            and row.get("timeout") is False
            and row.get("signal") is False,
            f"MUTATION_REJECTION:{row['name']}",
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--jobs", type=int, default=8)
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("CANONICALIZER_COMPLETENESS_REPLAY_FAIL:OPTIMIZED_MODE")
    certificate = load_plain_json(CERTIFICATE)
    check_payload(certificate)
    check_mutations(load_plain_json(MUTATIONS))
    semantic = subprocess.run(
        [sys.executable, "-B", str(HERE / "canonicalizer_audit.py"), "--semantic-only"],
        cwd=PROJECT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    require(semantic.returncode == 0 and '"status": "PASS"' in semantic.stdout, "SEMANTIC_REPLAY")
    if args.full:
        with tempfile.TemporaryDirectory(prefix="k2p-canonicalizer-replay-") as temporary:
            output = Path(temporary) / CERTIFICATE.name
            command = [
                sys.executable,
                "-B",
                str(HERE / "canonicalizer_audit.py"),
                "--output",
                str(output),
                "--jobs",
                str(args.jobs),
            ]
            completed = subprocess.run(
                command,
                cwd=PROJECT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            require(completed.returncode == 0, f"FULL_EXIT:{completed.stdout[-1000:]}")
            require(output.read_bytes() == CERTIFICATE.read_bytes(), "FULL_BYTE_MISMATCH")
    print(
        "K2P_CANONICALIZER_COMPLETENESS_PASS "
        f"full={args.full} descriptors=10084 relations=4012"
    )


if __name__ == "__main__":
    main()

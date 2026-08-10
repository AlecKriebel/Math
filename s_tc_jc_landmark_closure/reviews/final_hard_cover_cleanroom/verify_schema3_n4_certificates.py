#!/usr/bin/env python3
"""Fail-closed release check for the active schema-3 n=4 theta-2 base gate."""

from __future__ import annotations

from pathlib import Path
import gzip
import hashlib
import json


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERTIFICATES = HERE / "certificates"

EXPECTED_SUMMARY_SHA256 = (
    "915bed0a3add001c1a94d6d862a2359e6ad75b3489f8d71b7adf006952b5ce37"
)
EXPECTED_FULL_AUDIT_SHA256 = (
    "5cea78208f1ccbce93b22fb7f5c71e73999a9abea51e23d7182b9cfa4f1be1c6"
)
EXPECTED_MUTATION_SHA256 = (
    "c5cceff673c84ff0f654438adc0ef9aead969101549a4daa645a26911d0ad2e6"
)


def stable(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(stable(value).encode()).hexdigest()


def file_sha256(path):
    answer = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def load_jsonl_gzip(path):
    with gzip.open(path, "rt") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def verify_self_hash(record, expected):
    claimed = record.get("normalized_sha256_without_hash")
    if claimed != expected:
        raise AssertionError(("unexpected certificate hash", claimed, expected))
    body = dict(record)
    del body["normalized_sha256_without_hash"]
    actual = digest(body)
    if actual != claimed:
        raise AssertionError(("invalid certificate self-hash", actual, claimed))


def require_equal(actual, expected, label):
    if actual != expected:
        raise AssertionError((label, actual, expected))


def main():
    summary_path = ROOT / "primary/certificates/hard_cover_schema3_theta2_full_summary.json"
    require_equal(file_sha256(summary_path), EXPECTED_SUMMARY_SHA256, "summary SHA-256")

    audit_path = CERTIFICATES / "schema3_n4_theta2_full_audit.json"
    mutation_path = CERTIFICATES / "schema3_n4_theta2_mutation_certificate.json"
    terminals_path = CERTIFICATES / "schema3_n4_theta2_terminal_records.jsonl.gz"
    audit = json.loads(audit_path.read_text())
    mutation = json.loads(mutation_path.read_text())
    verify_self_hash(audit, EXPECTED_FULL_AUDIT_SHA256)
    verify_self_hash(mutation, EXPECTED_MUTATION_SHA256)
    require_equal(audit["status"], "VERIFIED", "full-audit status")
    require_equal(mutation["status"], "VERIFIED", "mutation status")
    require_equal(audit["failure_count"], 0, "full-audit failure count")
    require_equal(audit["first_failures"], [], "full-audit first failures")

    for relative, expected in audit["inputs"].items():
        require_equal(file_sha256(ROOT / relative), expected, f"input hash: {relative}")

    require_equal(audit["root_case_records"], 132, "root cases")
    require_equal(audit["state_records"], 2_106, "states")
    require_equal(audit["graph_records"], 606, "graphs")
    require_equal(audit["polynomial_records"], 19, "primary polynomial bodies")

    path = audit["path_audit"]
    require_equal(path["path_count"], 2_106, "path count")
    require_equal(path["refined_state_count"], 114, "refinement states")
    require_equal(path["normalized_state_count"], 2_106, "normalized states")
    require_equal(path["normalized_collision_classes"], 0, "normalized collisions")
    require_equal(
        path["merged_provenance_child_disagreements"], 0,
        "merged-provenance child disagreements",
    )

    normalization = audit["descriptor_normalization_audit"]
    require_equal(normalization["graph_count"], 606, "normalization graph count")
    require_equal(normalization["standard_mixed_groups"], 474, "mixed groups")
    require_equal(normalization["multi_root_groups"], 66, "multi-root groups")
    require_equal(
        normalization["minimum_normalization_root_invariance_failures"], 0,
        "active-normalization root-invariance failures",
    )
    require_equal(
        normalization["no_normalization_root_invariance_failures"], 66,
        "normalization-removal detections",
    )
    require_equal(
        normalization["wrong_normalization_root_invariance_failures"], 66,
        "wrong-universe normalization detections",
    )
    require_equal(
        normalization["graphs_changed_without_normalization"], 606,
        "graphs changed without normalization",
    )
    require_equal(
        normalization["graphs_changed_under_wrong_normalization"], 606,
        "graphs changed under wrong normalization",
    )

    terminal = audit["terminal_audit"]
    require_equal(
        terminal["terminal_counts"],
        {
            "generic_polynomial_separation": 1_860,
            "support_prefix_labelled_isomorphism": 132,
        },
        "terminal counts",
    )
    require_equal(terminal["independent_terminal_record_count"], 1_992, "terminal rows")
    terminal_rows = load_jsonl_gzip(terminals_path)
    require_equal(len(terminal_rows), 1_992, "stored terminal rows")
    require_equal(
        digest(terminal_rows), terminal["terminal_record_commitment"],
        "terminal-record commitment",
    )

    binding = terminal["polynomial_binding_audit"]
    require_equal(binding["generic_state_count"], 1_860, "generic states")
    require_equal(binding["primary_polynomial_bodies"], 19, "polynomial bodies")
    require_equal(binding["primary_polynomial_bodies_referenced"], 19, "referenced bodies")
    require_equal(binding["descriptor_invariant_binding_classes"], 415, "binding classes")
    require_equal(binding["descriptor_invariant_binding_conflicts"], 0, "binding conflicts")
    require_equal(binding["primary_exact_hash_conflicts"], 0, "primary hash conflicts")
    require_equal(binding["independent_same_quartet_separator_count"], 1_860, "same-quartet witnesses")
    require_equal(binding["independent_dynamic_nullspace_separator_count"], 32, "dynamic witnesses")
    require_equal(binding["independent_fallback_quartet_count"], 0, "fallback witnesses")

    require_equal(
        mutation["full_audit_sha256"], EXPECTED_FULL_AUDIT_SHA256,
        "mutation/full-audit binding",
    )
    require_equal(len(mutation["mutations"]), 13, "mutation count")
    failed_mutations = sorted(
        name for name, result in mutation["mutations"].items()
        if not result.get("rejected")
    )
    require_equal(failed_mutations, [], "accepted mutations")

    active_probe_outputs = sorted(
        path.name for path in CERTIFICATES.glob("schema3_n4_theta2_probe*")
    )
    require_equal(active_probe_outputs, [], "active superseded probe certificates")

    print(stable({
        "gate": "schema3_n4_theta2_base",
        "status": "VERIFIED",
        "summary_sha256": EXPECTED_SUMMARY_SHA256,
        "full_audit_sha256": EXPECTED_FULL_AUDIT_SHA256,
        "mutation_sha256": EXPECTED_MUTATION_SHA256,
        "probe_extension_status": "UNRESOLVED",
    }))


if __name__ == "__main__":
    main()

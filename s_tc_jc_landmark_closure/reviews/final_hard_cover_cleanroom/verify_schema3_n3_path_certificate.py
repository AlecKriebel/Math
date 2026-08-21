#!/usr/bin/env python3
"""Lightweight fail-closed check of the frozen n=3 path-only certificate."""

from pathlib import Path
import hashlib
import json


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CERTIFICATE = HERE / "certificates/schema3_n3_path_audit.json"
EXPECTED_SUMMARY = "8ea833f92f8fe2777043fb95b643e0478ce162871e6694ef3c403f5f1c854cf8"
EXPECTED_CERTIFICATE = "329510a396326e978aad8dfc77642f60048e26681014b733570a4c76c037fb3b"


def stable(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(stable(value).encode()).hexdigest()


def sha(path):
    answer = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def require(actual, expected, label):
    if actual != expected:
        raise AssertionError((label, actual, expected))


def main():
    certificate = json.loads(CERTIFICATE.read_text())
    claimed = certificate.get("normalized_sha256_without_hash")
    require(claimed, EXPECTED_CERTIFICATE, "certificate commitment")
    body = dict(certificate)
    del body["normalized_sha256_without_hash"]
    require(digest(body), claimed, "certificate self-hash")
    require(certificate["status"], "VERIFIED", "path status")
    require(certificate["failure_count"], 0, "path failure count")
    require(certificate["first_failures"], [], "path failures")

    for relative, expected in certificate["inputs"].items():
        require(sha(ROOT / relative), expected, f"input hash: {relative}")
    require(
        sha(ROOT / "primary/certificates/hard_cover_schema3_n3_full_summary.json"),
        EXPECTED_SUMMARY, "summary SHA-256",
    )
    require(certificate["root_case_records"], 5_344, "root cases")
    require(certificate["state_records"], 68_584, "states")
    require(certificate["graph_records"], 14_482, "graphs")
    path = certificate["path_audit"]
    require(path["path_count"], 68_584, "path bindings")
    require(path["refined_state_count"], 8_349, "refinement states")
    require(path["normalized_state_count"], 68_584, "normalized states")
    require(path["normalized_collision_classes"], 0, "normalized collisions")
    require(path["merged_provenance_child_disagreements"], 0,
            "merged-provenance child disagreements")
    normalization = certificate["descriptor_normalization_audit"]
    require(normalization["minimum_normalization_root_invariance_failures"], 0,
            "active-normalization root failures")
    require(certificate["terminal_audit"], {"skipped": True}, "terminal layer must be skipped")

    active_terminal = sorted(
        path.name for path in (HERE / "certificates").glob("schema3_n3_terminal*")
    )
    require(active_terminal, [], "active withdrawn terminal artifacts")
    print(stable({
        "gate": "schema3_n3_graph_path_only",
        "status": "VERIFIED",
        "certificate_sha256": EXPECTED_CERTIFICATE,
        "terminal_layer": "WITHDRAWN_INCOMPATIBLE_WITH_TWO_ACTIVE_LABELS",
        "complete_n3_gate": "UNRESOLVED",
    }))


if __name__ == "__main__":
    main()

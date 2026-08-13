#!/usr/bin/env python3
"""Fast integrity check for the verified schema-3 n=4 theta-2 subgate."""

from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""): h.update(block)
    return h.hexdigest()


def logical(path):
    h = hashlib.sha256(); count = 0
    with gzip.open(path, "rb") as stream:
        for line in stream: h.update(line); count += 1
    return h.hexdigest(), count


def cert(name):
    path = HERE / "certificates" / name
    obj = json.loads(path.read_text())
    if obj["status"] != "VERIFIED": raise AssertionError((name, obj["status"]))
    return path, obj


def main():
    full_path, full = cert("schema3_n4_theta2_full_audit.json")
    structure_path, structure = cert("schema3_n4_theta2_probe_structure_audit.json")
    algebra_path, algebra = cert("schema3_n4_theta2_probe_algebra_audit.json")
    _, base_mutation = cert("schema3_n4_theta2_mutation_certificate.json")
    _, probe_mutation = cert("schema3_n4_theta2_probe_mutation_certificate.json")
    if base_mutation["full_audit_sha256"] != full["normalized_sha256_without_hash"]:
        raise AssertionError("base mutation certificate is not bound to full audit")
    if probe_mutation["algebra_audit_sha256"] != algebra["normalized_sha256_without_hash"]:
        raise AssertionError("probe mutation certificate is not bound to algebra audit")
    if algebra["inputs"][str(structure_path.relative_to(ROOT))] != sha(structure_path):
        raise AssertionError("algebra audit is not bound to current structure certificate")

    summary = json.loads((ROOT / "primary/certificates/probe_extension_theta2_schema3_summary.json").read_text())
    for name, entry in summary["streams"].items():
        path = ROOT / entry["path"]
        actual, count = logical(path)
        if actual != entry["sha256"] or count != entry["records"]:
            raise AssertionError((name, actual, count, entry))

    evidence_path = ROOT / algebra["evidence"]["path"]
    evidence_sha, evidence_count = logical(evidence_path)
    if evidence_sha != algebra["evidence"]["logical_stream_sha256"] or evidence_count != algebra["evidence"]["records"]:
        raise AssertionError("independent algebra evidence stream mismatch")
    if sha(evidence_path) != algebra["evidence"]["physical_file_sha256"]:
        raise AssertionError("independent algebra evidence gzip mismatch")
    print(json.dumps({
        "status": "VERIFIED",
        "base_full_audit": full["normalized_sha256_without_hash"],
        "probe_structure_audit": structure["normalized_sha256_without_hash"],
        "probe_algebra_audit": algebra["normalized_sha256_without_hash"],
        "probe_evidence_records": evidence_count,
        "probe_evidence_sha256": evidence_sha,
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__": main()

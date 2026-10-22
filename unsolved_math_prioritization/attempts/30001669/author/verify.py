#!/usr/bin/env python3
"""Check a pinned audit package and arithmetic, not the published theorem.

Usage: python -B verify.py --manifest-sha256 EXTERNAL_SHA256 [--root DIR]
All checks remain enabled under Python -O. No third-party dependencies.
"""
import argparse
import hashlib
import json
import pathlib
import stat

PAYLOAD = {"REPORT.md", "PUBLIC_METADATA.json", "verify.py", "VERIFICATION.json", "audit_checks.py"}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify(root, pin):
    need(not root.is_symlink() and root.is_dir(), "Root must be a real directory")
    entries = list(root.iterdir())
    need({p.name for p in entries} == PAYLOAD | {"MANIFEST.json"}, "Unexpected inventory")
    for p in entries:
        st = p.lstat()
        need(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, "Nonregular or aliased entry")
    raw = (root / "MANIFEST.json").read_bytes()
    need(sha(raw) == pin, "External manifest pin mismatch")
    manifest = json.loads(raw)
    need(set(manifest) == {"schema", "files"}, "Manifest keys differ")
    need(manifest["schema"] == "strict-flat-sha256-v1", "Manifest schema differs")
    need(set(manifest["files"]) == PAYLOAD, "Manifest inventory differs")
    for name in sorted(PAYLOAD):
        b = (root / name).read_bytes()
        need(manifest["files"][name] == {"bytes": len(b), "sha256": sha(b)}, "Payload mismatch: " + name)
    m = json.loads((root / "PUBLIC_METADATA.json").read_text())
    need(m["problem_id"] == 30001669 and m["problem_number"] == "OWR-4791-028", "Problem identity differs")
    need(m["disposition"] == "already_resolved_negatively_published_2015", "Disposition differs")
    need(m["novel_resolution_claim"] is False, "Invalid novelty claim")
    s = m["theorem_specialization"]
    need(s["finite"] is True and s["graph_class"] == "general_directed_graphs", "Graph scope differs")
    need(s["witness_orientation"] == "v_to_every_u" and s["subset_quantifier"] == "at_most", "Domination semantics differ")
    need(s["cycle_length_upper_bound_question"] == 100, "Question bound differs")
    need(s["dominated_subset_limit"] == 100, "Domination bound differs")
    k, ell = s["girth_lower_bound"], s["dominated_subset_limit"]
    need(type(k) is int and k == 101, "Girth bound must exclude length 100")
    need(k > s["cycle_length_upper_bound_question"], "No contradiction to question")
    power = ell - 1
    base = (k - 1) * power + 1
    need(power == 99 and base == 9901, "Construction parameters differ")
    need(s["power_minimum_walk_length"] == 1, "Zero-length walks create loops")
    need(s["power_maximum_walk_length"] == power and s["base_girth_lower_bound"] == base, "Power data differs")
    need(all(1 <= t * power < base for t in range(1, 101)), "Cycle lifting bound failed")
    need(m["source_theorem"]["number"] == 11 and m["source_theorem"]["printed_page"] == 83, "Theorem citation differs")
    need(m["source_theorem"]["doi"] == "10.4230/LIPIcs.APPROX-RANDOM.2015.78", "Theorem DOI differs")
    need(m["statement_identity"]["sha256"] == "2117b75dcc957ad67a89583a8434249e2f924eca4e28d39ed1641a5602e26fda", "Statement identity differs")
    r = m["full_record_review"]
    need(r["sha256"] == "d155d5ff1ec1c49ab26c0c03207cd027a66c48aedc993a29fe538d941b2b4bc4" and r["bytes"] == 3626, "Review identity differs")
    need(r["matches_catalog"] is True and r["report_present"] is False, "Review match flags differ")
    need(m["computational_counterexample_claim"] is False, "No adjacency certificate supplied")
    return {"status": "pass", "payload_files": len(PAYLOAD), "cycle_lifting_inequalities": 100,
            "mathematical_scope": "Integrity, metadata semantics, and integer parameter checks only; not a proof of the cited theorem."}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent)
    p.add_argument("--manifest-sha256", required=True)
    a = p.parse_args()
    print(json.dumps(verify(a.root, a.manifest_sha256), sort_keys=True))


if __name__ == "__main__":
    main()

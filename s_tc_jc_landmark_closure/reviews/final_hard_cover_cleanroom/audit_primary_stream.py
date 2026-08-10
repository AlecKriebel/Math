#!/usr/bin/env python3
"""Comparison-only audit of primary hard-cover path binding and deduplication."""

from pathlib import Path
from collections import Counter, defaultdict
import argparse
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FILES = [
    "hard_cover_n3_sig0_all.jsonl.gz", "hard_cover_n3_sig1_all.jsonl.gz",
    "hard_cover_n3_sig2_all.jsonl.gz", "hard_cover_n3_sig3_5_all.jsonl.gz",
    "hard_cover_n3_sig6_7_all.jsonl.gz",
]


def stable(obj): return json.dumps(obj, sort_keys=True, separators=(",", ":"))
def digest(obj): return hashlib.sha256(stable(obj).encode()).hexdigest()
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--record-known-failure", action="store_true",
        help="write the exact failure certificate but do not return a failing exit status",
    )
    args = parser.parse_args()
    records = {}; parent_to_children = defaultdict(set); paths = {}; roots = set(); duplicate_conflicts = []
    hashes = {}
    for name in FILES:
        path = ROOT / "primary/certificates" / name; hashes[name] = sha(path)
        with gzip.open(path, "rt") as f:
            for line in f:
                rec = json.loads(line); sid = rec["state_id"]
                if sid in records and records[sid] != rec: duplicate_conflicts.append(sid)
                records[sid] = rec
                for cov in rec["raw_coverage"]:
                    pid = cov["path_binding_id"]
                    if pid in paths and paths[pid] != (sid, cov): duplicate_conflicts.append(pid)
                    paths[pid] = (sid, cov); roots.add(cov["root_case_id"])
                    parent = cov["parent_path_binding_id"]
                    if parent is not None: parent_to_children[parent].add(sid)
    merged_child_set_disagreements = []; missing_child_bindings = []; declared_mismatches = []
    refined = 0
    for sid, rec in sorted(records.items()):
        if rec["terminal_classification"] != "refined_by_next_restoration": continue
        refined += 1; per_path = []
        for cov in rec["raw_coverage"]:
            child_set = tuple(sorted(parent_to_children.get(cov["path_binding_id"], ())))
            per_path.append((cov["path_binding_id"], child_set))
            if not child_set: missing_child_bindings.append({"state_id": sid, "path_binding_id": cov["path_binding_id"]})
        distinct = sorted({x for _, x in per_path})
        declared = tuple(sorted(rec["children"]))
        if len(distinct) != 1:
            merged_child_set_disagreements.append({
                "state_id": sid, "declared_children": declared,
                "per_path_children": per_path,
            })
        if any(x != declared for _, x in per_path):
            declared_mismatches.append({"state_id": sid, "declared_children": declared, "per_path_children": per_path})
    cert = {
        "schema": 1, "input_sha256": hashes,
        "record_count": len(records), "root_case_count": len(roots), "path_count": len(paths),
        "refined_state_count": refined, "duplicate_identifier_conflicts": len(duplicate_conflicts),
        "merged_child_set_disagreement_count": len(merged_child_set_disagreements),
        "missing_child_binding_count": len(missing_child_bindings),
        "declared_child_mismatch_count": len(declared_mismatches),
        "first_merged_child_set_disagreement": merged_child_set_disagreements[:1],
        "first_missing_child_bindings": missing_child_bindings[:10],
        "status": "FALSE" if merged_child_set_disagreements or missing_child_bindings or duplicate_conflicts else "VERIFIED",
        "interpretation": (
            "The current stream does not carry a full child provenance for every raw presentation merged into a canonical state. "
            "Its declared child list therefore cannot certify fixed-full-relation path coherence."
        ),
    }
    cert["normalized_sha256_without_hash"] = digest(cert)
    out = HERE / "certificates"; out.mkdir(exist_ok=True)
    (out / "primary_path_binding_audit.json").write_text(stable(cert) + "\n")
    print(stable(cert))
    if cert["status"] != "VERIFIED" and not args.record_known_failure:
        raise SystemExit(1)


if __name__ == "__main__": main()

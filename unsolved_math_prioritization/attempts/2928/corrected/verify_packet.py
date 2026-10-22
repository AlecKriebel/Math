#!/usr/bin/env python3
"""Fail-closed integrity/scope check; this is not a mathematical proof verifier."""
import argparse
import hashlib
import json
from pathlib import Path

ALLOWED = {
    "README.md", "PROOF.md", "REPORT.md", "research_log.json", "status.json",
    "sources.json", "verification_metadata.json", "verify_packet.py", "FILES_SHA256.json"
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)


def check(root):
    entries = list(root.iterdir())
    require({p.name for p in entries} == ALLOWED, "unexpected or missing packet entry")
    require(all(p.is_file() and not p.is_symlink() for p in entries), "non-regular packet entry")
    manifest = read_json(root / "FILES_SHA256.json")
    require(set(manifest) == ALLOWED - {"FILES_SHA256.json"}, "manifest file set mismatch")
    for name, item in manifest.items():
        require(set(item) == {"bytes", "sha256"}, "manifest schema mismatch")
        data = (root / name).read_bytes()
        require(type(item["bytes"]) is int and item["bytes"] == len(data), "byte count mismatch: " + name)
        require(hashlib.sha256(data).hexdigest() == item["sha256"], "hash mismatch: " + name)
    status = read_json(root / "status.json")
    require(type(status.get("problem_id")) is int and status["problem_id"] == 2928, "wrong problem")
    require(status.get("problem_number") == "KP-4.52", "wrong problem code")
    require(status.get("disposition") == "unsolved", "unsupported disposition")
    for key in ("full_problem_solved", "new_solution_claimed", "counterexample_claimed"):
        require(status.get(key) is False, "unsupported claim: " + key)
    require(status.get("conditional_results_only") is True, "conditional scope missing")
    require(type(status.get("turns_used")) is int and status["turns_used"] == 3, "incorrect turn count")
    require(type(status.get("turn_limit")) is int and status["turn_limit"] == 5, "incorrect turn limit")
    log = read_json(root / "research_log.json")
    require([v.get("turn") for v in log.get("approaches", [])] == [1, 2, 3], "approach accounting mismatch")
    gate = log.get("gate", {})
    require(gate.get("decision") == "pass_literature_triage_only", "gate decision mismatch")
    require(gate.get("full_record_inspected") is True and gate.get("associated_report_empty") is True,
            "inherited record gate missing")
    require(gate.get("substantive_inherited_proof_or_computation") is False, "inherited substantive work")
    meta = read_json(root / "verification_metadata.json")
    require(meta.get("source_contents_included") is False and meta.get("dataset_contents_included") is False,
            "source or dataset contents not allowed")
    require(meta.get("statement_sha256") == "e1c2fc3f4719c4aa4fccd0bd7874dff67288523a5a3b82158093b6c24bb8fa1e",
            "statement identity mismatch")
    require(meta.get("paired_record_sha256") == "d97f40398ba42a49e0499ac4d5ed0a4919e31facd4956cf65b62535b2b9c1bc9",
            "record identity mismatch")
    sources = read_json(root / "sources.json")
    require(len(sources) == 8 and {s.get("id") for s in sources} == {"K3", "KNV", "HU", "KP", "KL", "HKPR", "SE", "SEF"},
            "source identifiers mismatch")
    require(all(isinstance(s.get("url"), str) and s["url"].startswith("https://") for s in sources),
            "non-public source reference")
    return {"result": "PASS", "problem_id": 2928, "files_checked": len(manifest),
            "disposition": "unsolved", "turns_used": 3,
            "scope": "packet integrity and conservative fields only; no mathematical proof certification"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(check(args.root), sort_keys=True))


if __name__ == "__main__":
    main()

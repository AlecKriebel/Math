#!/usr/bin/env python3
"""Read-only fail-closed packet verification. Trust this verifier and an external manifest pin."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

def require(condition, message):
    if not condition:
        raise ValueError(message)

def strict_json(path):
    def pairs(items):
        d = {}
        for k, v in items:
            require(k not in d, "Duplicate JSON key: " + k)
            d[k] = v
        return d
    def bad_constant(value):
        raise ValueError("Nonfinite JSON constant: " + value)
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=bad_constant)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical_record(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-manifest", required=True)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    require(re.fullmatch(r"[0-9a-f]{64}", args.expected_manifest) is not None,
            "Expected manifest must be a lowercase SHA-256 pin")
    root = Path(__file__).resolve().parent
    manifest_path = root / "MANIFEST.json"
    require(not manifest_path.is_symlink(), "Manifest symlink forbidden")
    require(digest(manifest_path.read_bytes()) == args.expected_manifest, "Manifest pin mismatch")
    manifest = strict_json(manifest_path)
    require(type(manifest) is dict and set(manifest) == {"schema", "files"}, "Manifest schema invalid")
    require(type(manifest["schema"]) is int and manifest["schema"] == 1, "Manifest version invalid")
    require(type(manifest["files"]) is list and bool(manifest["files"]), "Manifest files invalid")
    names = set()
    for entry in manifest["files"]:
        require(type(entry) is dict and set(entry) == {"name", "bytes", "sha256"}, "Entry schema invalid")
        name = entry["name"]
        require(type(name) is str and re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", name) is not None,
                "Unsafe member name")
        require(name != "MANIFEST.json" and name not in names, "Duplicate or recursive manifest entry")
        names.add(name)
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0, "Invalid byte count")
        require(type(entry["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None,
                "Invalid member digest")
        p = root / name
        require(not p.is_symlink() and p.is_file(), "Missing, nonregular, or symlink member: " + name)
        data = p.read_bytes()
        require(len(data) == entry["bytes"] and digest(data) == entry["sha256"], "Member mismatch: " + name)
    require({p.name for p in root.iterdir()} == names | {"MANIFEST.json"}, "Exact packet inventory mismatch")
    for required in ["CLAIM.json", "check_math.py", "MATH_RESULTS.json", "PROVENANCE.json", "PROOF.md"]:
        require(required in names, "Required file is unbound: " + required)
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("packet_math", root / "check_math.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.check_claim(strict_json(root / "CLAIM.json"))
    math_results = module.run_controls()
    require(math_results == strict_json(root / "MATH_RESULTS.json"), "Mathematical control receipt mismatch")
    source_state = "NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES"
    if args.source_root is not None:
        provenance = strict_json(root / "PROVENANCE.json")
        for entry in provenance["external_files"]:
            p = args.source_root / entry["replay_name"]
            require(not p.is_symlink() and p.is_file(), "Missing or symlink source: " + entry["replay_name"])
            data = p.read_bytes()
            require(len(data) == entry["bytes"] and digest(data) == entry["sha256"], "Source mismatch: " + entry["replay_name"])
        problems = strict_json(args.source_root / "problems.json")
        selected = [row for row in problems if row.get("id") == 30003467]
        require(len(selected) == 1, "Expected one selected problem record")
        require(digest(canonical_record(selected[0])) == provenance["selected_record_sha256"], "Selected record mismatch")
        research = strict_json(args.source_root / "research_results.json")
        require("OWR-15427-009" not in research, "Unexpected exact research-result key")
        source_state = "PASS_EXTERNAL_BYTE_PINS_AND_SELECTED_RECORD"
    print(json.dumps({"packet": "PASS", "bound_files": len(names),
                      "scope": "credited_prior_negative_resolution",
                      "source_verification": source_state,
                      "geometry": "EXTERNAL_PUBLISHED_THEOREM_NOT_RECOMPUTED"}, sort_keys=True, indent=2))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)

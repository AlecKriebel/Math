#!/usr/bin/env python3
"""Verify the public reader manifest, reviewed proof pins, and checker derivation.

Uses only the Python standard library and explicit failure conditions.
It checks integrity, not the truth of an analytic proof or source authorship.
"""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main():
    manifest = read_json("integrity/PACKAGE_MANIFEST.json")
    expected = {entry["path"] for entry in manifest["files"]}
    require(len(expected) == len(manifest["files"]), "Duplicate manifest path")
    excluded = {"integrity/PACKAGE_MANIFEST.json"}
    actual = set()
    for path in ROOT.rglob("*"):
        require(not path.is_symlink(), "Symlink is not an authorized package artifact")
        if path.is_file():
            rel = path.relative_to(ROOT).as_posix()
            require("__pycache__" not in path.parts, "Unexpected Python cache")
            actual.add(rel)
    require(actual == expected | excluded, "Unexpected or missing package file")
    for entry in manifest["files"]:
        rel = Path(entry["path"])
        require(not rel.is_absolute() and ".." not in rel.parts, "Unsafe manifest path")
        data = (ROOT / rel).read_bytes()
        require(len(data) == entry["bytes"], "Byte-count mismatch: " + str(rel))
        require(digest(data) == entry["sha256"], "Digest mismatch: " + str(rel))
    mapping = read_json("integrity/ORIGINAL_ARTIFACT_MAP.json")
    by_name = {}
    for item in mapping["artifacts"]:
        data = (ROOT / item["output_path"]).read_bytes()
        require(len(data) == item["output_bytes"] and digest(data) == item["output_sha256"], "Output mapping mismatch")
        if item["byte_identical"]:
            require(len(data) == item["original_bytes"] and digest(data) == item["original_sha256"], "Original byte pin mismatch")
            require(not item["transformation"], "Identical file has unexpected transformation")
        by_name[Path(item["original_artifact"]).name] = item
    review = read_json("geometry/CROSS_REVIEW_RECEIPT.json")
    for item in review["files"]:
        mapped = by_name[item["artifact_name"]]
        require(item["byte_count"] == mapped["output_bytes"] and item["sha256"] == mapped["output_sha256"], "Cross-review proof pin mismatch")
    derivation = read_json("integrity/CHECKER_DERIVATION.json")
    original = (ROOT / derivation["original_path"]).read_bytes()
    derived = (ROOT / derivation["derived_path"]).read_bytes()
    require(digest(original) == derivation["original_sha256"], "Original checker pin mismatch")
    require(digest(derived) == derivation["derived_sha256"], "Derived checker pin mismatch")
    rebuilt = bytearray()
    cursor = 0
    for edit in derivation["edits"]:
        start, stop = edit["original_byte_start"], edit["original_byte_end_exclusive"]
        require(cursor <= start < stop <= len(original), "Overlapping or invalid edit")
        require(digest(original[start:stop]) == edit["original_fragment_sha256"], "Edited fragment pin mismatch")
        replacement = edit["replacement_utf8"].encode("utf-8")
        require(digest(replacement) == edit["replacement_sha256"], "Replacement pin mismatch")
        rebuilt.extend(original[cursor:start]); rebuilt.extend(replacement); cursor = stop
    rebuilt.extend(original[cursor:])
    require(bytes(rebuilt) == derived, "Derived checker differs outside the exact edit map")
    count_original = sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(original)))
    count_derived = sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(derived)))
    require(count_original == 5 and count_derived == 0, "Unexpected assertion counts")
    require(len(derivation["edits"]) == 5, "Expected exactly five conditional-raise edits")
    print(json.dumps({"status": "PASS", "manifest_files_verified": len(expected), "manifest_self_hash": "external archive receipt", "original_output_mappings_verified": len(mapping["artifacts"]), "cross_review_proof_pins_verified": len(review["files"]), "exact_checker_reconstruction": "PASS", "mathematical_proof_certification": False}, indent=2))


if __name__ == "__main__":
    main()

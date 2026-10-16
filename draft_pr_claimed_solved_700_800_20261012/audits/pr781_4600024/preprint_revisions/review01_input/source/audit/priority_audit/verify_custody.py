#!/usr/bin/env python3
"""Verify this flat priority bundle against a caller-supplied manifest SHA256.

Use python3 -B or python3 -O -B. EXTERNAL_PIN.txt is a convenience copy,
never the trust input. No asserts, network access, imports of bundled code or writes.
"""
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath

HEAD = "4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f"
EXCEPTIONS = ["EXTERNAL_PIN.txt", "FROZEN_MANIFEST.json"]


class CustodyError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CustodyError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    require(isinstance(value, str) and bool(value), "invalid relative path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and "." not in path.parts and ".." not in path.parts,
            "unsafe relative path: " + value)
    require(str(path) == value and "\\" not in value, "noncanonical path: " + value)
    return path


def regular(path):
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise CustodyError("missing/inaccessible file: " + str(path)) from exc
    require(stat.S_ISREG(mode), "not a regular file: " + str(path))


def check_record(root, row):
    require(set(row) == {"relative_input", "bytes", "sha256"}, "bad input receipt")
    name = row["relative_input"]
    relative(name)
    cursor = root
    for part in PurePosixPath(name).parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), "input symlink: " + str(cursor))
    regular(cursor)
    data = cursor.read_bytes()
    require(type(row["bytes"]) is int and row["bytes"] >= 0, "bad input byte count")
    require(len(data) == row["bytes"], "input byte count: " + name)
    require(sha(data) == row["sha256"], "input digest: " + name)


def verify(root, input_root, expected):
    require(re.fullmatch(r"[0-9a-f]{64}", expected) is not None, "invalid external pin")
    regular(root / "FROZEN_MANIFEST.json")
    manifest_bytes = (root / "FROZEN_MANIFEST.json").read_bytes()
    require(sha(manifest_bytes) == expected, "external manifest pin mismatch")
    manifest = json.loads(manifest_bytes, object_pairs_hook=unique_object)
    require(manifest.get("schema") == "priority-custody/v1", "manifest schema")
    require(manifest.get("target") == {"pr": 781, "problem_id": 4600024, "head": HEAD},
            "target mismatch")
    require(manifest.get("explicit_exceptions") == EXCEPTIONS, "exception list mismatch")
    require(isinstance(manifest.get("files"), list), "missing manifest file list")
    names = set()
    for row in manifest["files"]:
        require(set(row) == {"path", "bytes", "sha256"}, "malformed artifact entry")
        name = row["path"]
        relative(name)
        require(len(PurePosixPath(name).parts) == 1, "bundle must be flat")
        require(name not in names and name not in EXCEPTIONS, "duplicate/excepted entry")
        names.add(name)
        require(type(row["bytes"]) is int and row["bytes"] >= 0, "bad byte count")
        require(isinstance(row["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]),
                "bad artifact digest")
        path = root / name
        regular(path)
        data = path.read_bytes()
        require(len(data) == row["bytes"], "artifact byte count: " + name)
        require(sha(data) == row["sha256"], "artifact digest: " + name)
    entries = list(root.iterdir())
    require({p.name for p in entries} == names | set(EXCEPTIONS), "unexpected/missing inventory")
    for path in entries:
        regular(path)
    pin_bytes = (root / "EXTERNAL_PIN.txt").read_bytes()
    require(pin_bytes == (expected + "\n").encode("ascii"), "convenience pin content mismatch")
    receipts = read_json(root / "INPUT_RECEIPTS.json")
    require(isinstance(receipts, list) and len(receipts) > 0, "input receipts missing")
    seen_inputs = set()
    for row in receipts:
        require(row["relative_input"] not in seen_inputs, "duplicate input receipt")
        seen_inputs.add(row["relative_input"])
        check_record(input_root, row)
    return {"result": "PASS", "head": HEAD, "manifest_sha256": expected,
            "artifact_files": len(names), "input_receipts": len(receipts),
            "explicit_exceptions": EXCEPTIONS, "optimized": not __debug__}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--input-root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    input_root = (args.input_root or root.parent).resolve()
    try:
        result = verify(root, input_root, args.expected_manifest_sha256)
    except (CustodyError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

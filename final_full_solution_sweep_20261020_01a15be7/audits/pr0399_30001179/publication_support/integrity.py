#!/usr/bin/env python3
"""Strict standard-library bundle integrity checks, active with Python -O.

This code verifies bytes and inventory, not mathematical correctness. A manifest
is not a signature or an externally authenticated trust anchor.
"""
import hashlib
import json
import os
import pathlib
import re
import stat


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON object key: " + key)
        result[key] = value
    return result


def load_json(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=_unique_object)


def safe_relative(value):
    require(type(value) is str and bool(value), "path must be a nonempty string")
    require("\\" not in value and ":" not in value and "\x00" not in value,
            "noncanonical path")
    pure = pathlib.PurePosixPath(value)
    require(not pure.is_absolute(), "absolute manifest path")
    require(all(part not in ("", ".", "..") for part in value.split("/")),
            "unsafe path component")
    require(str(pure) == value, "noncanonical manifest path")
    return value


def _inventory(root):
    result = set()
    require(root.is_dir() and not root.is_symlink(), "bundle root is not a real directory")
    for directory, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            path = pathlib.Path(directory) / name
            mode = path.lstat().st_mode
            require(not stat.S_ISLNK(mode), "symlink forbidden: " + str(path))
            require(stat.S_ISREG(mode) or stat.S_ISDIR(mode),
                    "nonregular bundle entry: " + str(path))
        for name in files:
            result.add((pathlib.Path(directory) / name).relative_to(root).as_posix())
    return result


def verify_bundle(root, manifest_name="FILES.json"):
    root = pathlib.Path(root)
    safe_relative(manifest_name)
    actual = _inventory(root)
    require(manifest_name in actual, "manifest missing")
    manifest = load_json(root / manifest_name)
    require(type(manifest) is dict and set(manifest) == {"schema", "files"},
            "manifest must have exactly schema and files keys")
    require(type(manifest["schema"]) is int and manifest["schema"] == 1,
            "schema must be exact integer 1")
    require(type(manifest["files"]) is list, "files must be a list")
    expected = {}
    for entry in manifest["files"]:
        require(type(entry) is dict and set(entry) == {"path", "bytes", "sha256"},
                "file record must have exactly path, bytes, sha256")
        name = safe_relative(entry["path"])
        require(name != manifest_name and name not in expected,
                "self-reference or duplicate file path")
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0,
                "bytes must be an exact nonnegative integer")
        require(type(entry["sha256"]) is str and
                re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]) is not None,
                "sha256 must be 64 lowercase hexadecimal characters")
        expected[name] = entry
    require(actual == set(expected) | {manifest_name},
            "inventory mismatch; missing=%r extra=%r" %
            (sorted(set(expected) - actual),
             sorted(actual - set(expected) - {manifest_name})))
    for name, entry in expected.items():
        data = (root / name).read_bytes()
        require(len(data) == entry["bytes"], "byte length mismatch: " + name)
        require(hashlib.sha256(data).hexdigest() == entry["sha256"],
                "sha256 mismatch: " + name)
    return {"files_verified": len(expected), "schema": 1,
            "scope": "Exact inventory and byte integrity only; not proof certification."}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=pathlib.Path)
    parser.add_argument("--manifest", default="FILES.json")
    args = parser.parse_args()
    try:
        print(json.dumps(verify_bundle(args.root, args.manifest), indent=2, sort_keys=True))
    except (ValueError, OSError) as exc:
        parser.exit(1, "integrity failure: %s\n" % exc)

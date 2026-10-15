#!/usr/bin/env python3
"""Pinned data-integrity replay only. Does not execute or certify mathematics."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

PINS = {
    "author": {
        "archive_sha256": "a23e5104041c2bd7aaf64e9da505a2d07dbd89b4ac599c23a8f008402cd49e3a",
        "archive_bytes": 11445,
        "manifest_sha256": "5c61737da81e41aae246c33ee3360a10ea71dfc75a48014cca3c2c519585f65d",
        "manifest_bytes": 1476,
        "inventory_count": 6,
    },
    "audit": {
        "archive_sha256": "74c8026f97819c0f90644398fd1cd474a70b7dc029bfea7f0b287a1544747803",
        "archive_bytes": 27319,
        "manifest_sha256": "2c534e174a7de5d3b5fe2191350c91f4aed8a37283dea8da96114e13b8f1e663",
        "manifest_bytes": 2416,
        "inventory_count": 12,
    },
}

class Invalid(Exception):
    pass

def require(test, message):
    if not test:
        raise Invalid(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def json_pairs(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, "duplicate JSON key")
        result[k] = v
    return result

def bad_constant(_):
    raise Invalid("non-finite JSON constant")

def parse(raw):
    return json.loads(raw.decode("utf-8", errors="strict"),
                      object_pairs_hook=json_pairs, parse_constant=bad_constant)

def safe_name(name):
    require(isinstance(name, str) and name, "empty/nonstring path")
    require("\\" not in name and ":" not in name and "\x00" not in name,
            "nonportable path")
    require(not any(ord(c) < 32 for c in name), "control in path")
    parts = name.split("/")
    require(all(p not in ("", ".", "..") for p in parts), "unsafe path component")
    require(not PurePosixPath(name).is_absolute(), "absolute member")
    require(PurePosixPath(name).as_posix() == name, "noncanonical path")
    require(PurePosixPath(name).suffix in (".md", ".json"), "unexpected file type")
    return name

def regular_read(path):
    p = Path(os.path.abspath(path))
    for q in [p] + list(p.parents):
        require(not stat.S_ISLNK(q.lstat().st_mode), "symlink in path")
    fd = os.open(p, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        mode = os.fstat(fd).st_mode
        require(stat.S_ISREG(mode), "input is not regular file")
        require(not (mode & 0o111), "input has executable permissions")
        with os.fdopen(fd, "rb", closefd=False) as f:
            raw = f.read(10000001)
        require(len(raw) <= 10000000, "input exceeds size limit")
        return raw
    finally:
        os.close(fd)

def rows_map(rows):
    require(type(rows) is list, "inventory is not a list")
    result = {}
    for row in rows:
        require(type(row) is dict and set(row) == {"path", "bytes", "sha256"},
                "inventory row schema")
        name = safe_name(row["path"])
        require(name not in result, "duplicate inventory path")
        require(type(row["bytes"]) is int and 0 <= row["bytes"] < 1000000,
                "invalid byte count")
        h = row["sha256"]
        require(type(h) is str and len(h) == 64 and
                all(c in "0123456789abcdef" for c in h), "invalid SHA-256")
        result[name] = row
    return result

def verify_members(raw, expected):
    """Structural validation using a supplied already-trusted closed inventory."""
    data = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos = z.infolist()
        require(len(infos) == len(expected), "member count mismatch")
        names = [safe_name(i.filename) for i in infos]
        require(len(names) == len(set(names)), "duplicate ZIP member")
        require(set(names) == set(expected), "closed ZIP inventory mismatch")
        require(not z.comment, "unexpected ZIP comment")
        for info in infos:
            name = info.filename
            mode = info.external_attr >> 16
            require(info.create_system == 3 and stat.S_ISREG(mode),
                    "nonregular ZIP entry")
            require(not mode & 0o111, "executable ZIP entry")
            require(not info.flag_bits & 1, "encrypted ZIP entry")
            require(info.file_size == expected[name]["bytes"], "ZIP size mismatch")
            require(not info.is_dir(), "directory ZIP entry")
            content = z.read(info)
            require(len(content) == expected[name]["bytes"], "readback size mismatch")
            require(sha(content) == expected[name]["sha256"], "content SHA mismatch")
            content.decode("utf-8", errors="strict")
            if name.endswith(".json"):
                parse(content)
            data[name] = content
    return data

def verify_inner(data):
    root_manifest = parse(data["MANIFEST.json"])
    rows = root_manifest.get("inventory", root_manifest.get("files"))
    inventory = rows_map(rows)
    expected_names = set(data) - {"MANIFEST.json"}
    require(set(inventory) == expected_names, "inner closed inventory mismatch")
    for name in expected_names:
        raw = data[name]
        require(inventory[name]["bytes"] == len(raw) and
                inventory[name]["sha256"] == sha(raw), "inner inventory mismatch")
    if "author/MANIFEST.json" in data:
        historical = {k[len("author/"):]:v for k,v in data.items()
                      if k.startswith("author/")}
        verify_inner(historical)

def verify_tree(tree, data):
    root = Path(os.path.abspath(tree))
    require(root.is_dir() and not root.is_symlink(), "invalid extraction root")
    expected_dirs = {"."}
    for name in data:
        for p in PurePosixPath(name).parents:
            expected_dirs.add(p.as_posix())
    actual_dirs, actual_files = {"."}, set()
    for current, dirs, files in os.walk(root, followlinks=False):
        for n in dirs:
            p = Path(current) / n
            require(not p.is_symlink(), "directory symlink")
            actual_dirs.add(p.relative_to(root).as_posix())
        for n in files:
            p = Path(current) / n
            name = p.relative_to(root).as_posix()
            require(name in data, "unexpected extraction file")
            actual_files.add(name)
            require(regular_read(p) == data[name], "extraction byte mismatch")
    require(actual_files == set(data), "extraction missing file")
    require(actual_dirs == expected_dirs, "extraction directory mismatch")

def verify(kind, archive, manifest, tree=None):
    pin = PINS[kind]
    raw_manifest = regular_read(manifest)
    require(len(raw_manifest) == pin["manifest_bytes"] and
            sha(raw_manifest) == pin["manifest_sha256"], "external manifest pin mismatch")
    metadata = parse(raw_manifest)
    require(metadata["archive_bytes"] == pin["archive_bytes"] and
            metadata["archive_sha256"] == pin["archive_sha256"], "archive metadata pin mismatch")
    expected = rows_map(metadata["inventory"])
    require(len(expected) == pin["inventory_count"], "pinned inventory count mismatch")
    raw = regular_read(archive)
    require(len(raw) == pin["archive_bytes"] and sha(raw) == pin["archive_sha256"],
            "archive pin mismatch")
    data = verify_members(raw, expected)
    verify_inner(data)
    if tree is not None:
        verify_tree(tree, data)
    return {"result":"PASS", "kind":kind, "archive_sha256":sha(raw),
            "manifest_sha256":sha(raw_manifest), "file_count":len(data),
            "tree_verified":tree is not None,
            "optimized_python":bool(sys.flags.optimize),
            "scope":"data integrity only, not machine verification of mathematics"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=sorted(PINS))
    p.add_argument("archive")
    p.add_argument("manifest")
    p.add_argument("--tree")
    a = p.parse_args()
    try:
        result = verify(a.kind, a.archive, a.manifest, a.tree)
    except (Invalid, OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        print(json.dumps({"result":"FAIL", "reason":str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())

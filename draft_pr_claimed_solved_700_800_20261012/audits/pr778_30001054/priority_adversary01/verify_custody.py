#!/usr/bin/env python3
"""Read-only exact recursive inventory verifier; requires a separately pinned hash."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys


def need(ok, message):
    if not ok:
        raise ValueError(message)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key")
        out[key] = value
    return out


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_regular(path):
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), "not regular: " + str(path))
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path), flags)
    try:
        observed = os.fstat(fd)
        need((observed.st_dev, observed.st_ino) == (before.st_dev, before.st_ino), "changed inode")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read()
        after = os.fstat(fd)
        need((observed.st_size, observed.st_mtime_ns) == (after.st_size, after.st_mtime_ns), "changed while reading")
        need(len(data) == after.st_size, "short read")
        return data
    finally:
        os.close(fd)


def verify(root, pinned):
    need(re.fullmatch(r"[0-9a-f]{64}", pinned) is not None, "invalid external SHA256")
    need(root.is_dir() and not root.is_symlink(), "invalid root")
    manifest_path = root / "MANIFEST.json"
    raw = read_regular(manifest_path)
    need(digest(raw) == pinned, "external manifest hash mismatch")
    manifest = json.loads(raw, object_pairs_hook=unique_object)
    need(manifest.get("schema") == "exact-recursive-authored-inventory-v1", "schema")
    need(isinstance(manifest.get("sealed_at_utc"), str), "sealed time")
    sealed = datetime.datetime.fromisoformat(manifest["sealed_at_utc"].replace("Z", "+00:00"))
    need(sealed.tzinfo is not None and sealed.utcoffset() == datetime.timedelta(0), "non-UTC seal")
    items = manifest.get("files")
    need(isinstance(items, list) and len(items) > 0, "files")
    expected = {}
    for item in items:
        need(isinstance(item, dict), "bad item")
        relative = item.get("path")
        need(isinstance(relative, str) and relative != "MANIFEST.json", "invalid path")
        pp = PurePosixPath(relative)
        need(not pp.is_absolute() and ".." not in pp.parts and str(pp) == relative, "unsafe path")
        need(relative not in expected, "duplicate file")
        need(type(item.get("bytes")) is int and item["bytes"] >= 0, "invalid length")
        need(isinstance(item.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None, "invalid digest")
        expected[relative] = item
    found = {}
    def walk(folder):
        entries = list(os.scandir(folder))
        need(len(entries) > 0, "empty directory: " + str(folder))
        for entry in entries:
            p = Path(entry.path)
            relative = p.relative_to(root).as_posix()
            info = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode):
                walk(p)
            else:
                need(stat.S_ISREG(info.st_mode), "symlink/special: " + relative)
                if relative != "MANIFEST.json":
                    body = read_regular(p)
                    found[relative] = {"path": relative, "bytes": len(body), "sha256": digest(body)}
    walk(root)
    need(set(found) == set(expected), "inventory mismatch")
    for path, item in expected.items():
        need(item == found[path], "byte/hash mismatch: " + path)
    return {"status": "PASS", "manifest_sha256": pinned, "files": len(found),
            "hidden_included": True, "excluded_only": "MANIFEST.json",
            "no_empty_directories_symlinks_or_special_files": True, "read_only": True,
            "absolute_filesystem_or_preserved_mtime_required": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root.absolute(), args.manifest_sha256), sort_keys=True))
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

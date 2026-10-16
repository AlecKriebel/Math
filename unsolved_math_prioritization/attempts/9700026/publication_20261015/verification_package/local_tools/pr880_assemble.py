#!/usr/bin/env python3
"""Materialize an externally pinned explicit PR880 file allowlist and index. No supplied code is executed.
Authenticate startup bytes independently before execution. Standard library only.
"""
import argparse
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile
import zipfile

MAX_FILE = 256 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_INDEX = 4 * 1024 * 1024


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError("nonfinite JSON constant: " + value)
    def finite_float(value):
        number = float(value)
        require(math.isfinite(number), "nonfinite JSON number")
        return number
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=finite_float)


def safe_name(name):
    require(isinstance(name, str) and bool(name) and len(name) <= 512,
            "invalid relative path")
    require("\\" not in name and "\x00" not in name and
            all(ord(c) >= 32 and ord(c) != 127 for c in name), "unsafe relative path")
    p = PurePosixPath(name)
    require(not p.is_absolute() and all(x not in ("", ".", "..") for x in name.split("/"))
            and str(p) == name and ":" not in name, "unsafe relative path: " + name)
    return name


def pin_row(row, git=False):
    require(isinstance(row, dict) and set(row) ==
            ({"path", "bytes", "sha256", "git_blob"} if git else {"path", "bytes", "sha256"}),
            "invalid inventory row")
    safe_name(row["path"])
    require(type(row["bytes"]) is int and 0 <= row["bytes"] <= MAX_FILE,
            "invalid pinned byte count")
    require(isinstance(row["sha256"], str) and re.fullmatch("[0-9a-f]{64}", row["sha256"]),
            "invalid SHA256")
    if git:
        require(isinstance(row["git_blob"], str) and re.fullmatch("[0-9a-f]{40}", row["git_blob"]),
                "invalid Git blob identifier")
    return row


def rows_map(rows, git=False):
    require(isinstance(rows, list) and 0 < len(rows) <= 10000, "invalid inventory list")
    result = {}
    for row in rows:
        pin_row(row, git)
        require(row["path"] not in result, "duplicate inventory path")
        result[row["path"]] = row
    require(sum(row["bytes"] for row in rows) <= MAX_TOTAL, "inventory size limit")
    for name in result:
        require(not any(str(p) in result for p in PurePosixPath(name).parents if str(p) != "."),
                "file/directory inventory collision")
    return result


def read_regular(path, expected_size=None, limit=MAX_FILE):
    # Root/ancestor aliases outside a chosen tree are allowed. The caller rejects
    # aliases within a package tree. Always reject a leaf alias before open.
    mode = path.lstat().st_mode
    require(stat.S_ISREG(mode), "nonregular input: " + path.name)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(stat.S_ISREG(info.st_mode), "nonregular opened input: " + path.name)
        require(info.st_size <= limit, "input size limit: " + path.name)
        if expected_size is not None:
            require(info.st_size == expected_size, "byte count mismatch: " + path.name)
        bound = expected_size if expected_size is not None else limit
        raw = stream.read(bound + 1)
        require(len(raw) <= bound and len(raw) == info.st_size, "bounded read mismatch: " + path.name)
    return raw


def within(root, name):
    safe_name(name)
    p = root
    for part in PurePosixPath(name).parts[:-1]:
        p = p / part
        require(stat.S_ISDIR(p.lstat().st_mode), "nonregular input directory: " + part)
    return root / name


def authenticate(raw, row, label):
    require(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "pin mismatch: " + label)


def closed_tree(root, names):
    require(stat.S_ISDIR(root.lstat().st_mode), "package root must be directory")
    expected = set(names)
    directories = {str(p) for n in expected for p in PurePosixPath(n).parents if str(p) != "."}
    seen = set()
    def visit(folder, prefix=""):
        for entry in os.scandir(folder):
            name = prefix + entry.name
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(name in directories, "unlisted directory: " + name)
                visit(Path(entry.path), name + "/")
            else:
                require(stat.S_ISREG(mode), "nonregular inventory entry: " + name)
                require(name in expected, "unlisted file: " + name)
                seen.add(name)
    visit(root)
    require(seen == expected, "missing inventory file")


def isolated():
    require(sys.version_info >= (3, 10), "Python 3.10 or newer required")
    require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,
            "run Python with -I -S -B")


def rejected_main(main):
    try:
        isolated()
        main()
    except (ValueError, OSError, KeyError, TypeError, RuntimeError, OverflowError, RecursionError, zipfile.BadZipFile,
            subprocess.TimeoutExpired, UnicodeError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, sort_keys=True))
        sys.exit(1)


def selected_root(path):
    require(stat.S_ISDIR(path.lstat().st_mode), "root must be an ordinary directory")
    return path.resolve()



def main():
    parser = argparse.ArgumentParser(description="Assemble only an externally pinned explicit file allowlist; no discovery or publication.")
    parser.add_argument("base", type=Path)
    parser.add_argument("spec", type=Path)
    parser.add_argument("spec_sha256")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    base = selected_root(args.base)
    require(re.fullmatch("[0-9a-f]{64}", args.spec_sha256 or ""), "external spec digest syntax")
    raw = read_regular(args.spec, limit=MAX_INDEX)
    require(sha(raw) == args.spec_sha256, "external assembly spec pin mismatch")
    spec = strict_json(raw)
    require(type(spec) is dict and set(spec) == {"schema", "kind", "files"}
            and spec["schema"] == "city-ode-explicit-assembly-v1"
            and spec["kind"] in ("portable", "outer"), "assembly spec schema")
    require(type(spec["files"]) is list and 0 < len(spec["files"]) <= 10000, "assembly list")
    blobs, sources, rows = {}, [], []
    for item in spec["files"]:
        require(type(item) is dict and set(item) == {"source", "path", "bytes", "sha256"}, "assembly row schema")
        safe_name(item["source"])
        row = {key: item[key] for key in ("path", "bytes", "sha256")}
        pin_row(row)
        require(row["path"] not in blobs, "assembly destination collision")
        source = within(base, item["source"])
        data = read_regular(source, row["bytes"])
        authenticate(data, row, item["source"])
        if row["path"].endswith(".json"):
            strict_json(data)
        blobs[row["path"]] = data
        rows.append(row)
        sources.append(source.resolve())
    rows_map(rows)
    index_name = "package_index.json" if spec["kind"] == "portable" else "PUBLICATION_MANIFEST.json"
    schema = "city-ode-verification-v1" if spec["kind"] == "portable" else "city-ode-current-publication-v1"
    require(not any(name == index_name or name.startswith(index_name + "/")
                    or index_name.startswith(name + "/") for name in blobs),
            "generated index file/directory collision")
    if spec["kind"] == "portable":
        require({"check_originals.py", "verify_package.py", "build_verification.py", "root_evidence/SOURCE_MANIFEST.json"} <= set(blobs), "portable required entries")
        original_manifest = blobs["root_evidence/SOURCE_MANIFEST.json"]
        require(sha(original_manifest) == "b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b", "original manifest pin")
        original = rows_map(strict_json(original_manifest)["files"], git=True)
        require({name[7:] for name in blobs if name.startswith("source/")} == set(original), "all forty source files must be explicit")
        for name, row in original.items():
            authenticate(blobs["source/" + name], row, "frozen original " + name)
    else:
        require({"README.md", "RESEARCH_LOG.md", "CURRENT_PUBLICATION.json", "verify_current_publication.py"} <= set(blobs), "outer required entries")
    index_raw = (json.dumps({"schema": schema, "problem_id": "9700026", "files": sorted(rows, key=lambda row: row["path"])}, indent=2, sort_keys=True) + "\n").encode()
    blobs[index_name] = index_raw
    require(not args.output.is_symlink(), "assembly output alias")
    output = args.output.resolve()
    require(all(output != source and output not in source.parents and source not in output.parents for source in sources), "assembly output/input collision")
    if output.exists():
        require(stat.S_ISDIR(output.lstat().st_mode) and not any(output.iterdir()), "assembly output must be fresh or empty")
    else:
        output.mkdir(parents=True)
    for name, data in blobs.items():
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        target.chmod(0o644)
    closed_tree(output, blobs)
    print(json.dumps({"status": "ASSEMBLED_REQUIRES_INDEPENDENT_VERIFICATION", "kind": spec["kind"], "output": str(output), "file_count": len(blobs), "index_name": index_name, "index_sha256": sha(index_raw)}, sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

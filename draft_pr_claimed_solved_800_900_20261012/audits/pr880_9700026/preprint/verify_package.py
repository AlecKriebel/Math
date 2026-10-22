#!/usr/bin/env python3
"""Authenticate an externally pinned closed PR880 portable inventory before optional finite replay.
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

def package_inputs(root, index_sha256):
    require(isinstance(index_sha256, str) and re.fullmatch("[0-9a-f]{64}", index_sha256),
            "external index SHA256 required")
    index_raw = read_regular(root / "package_index.json", limit=MAX_INDEX)
    require(sha(index_raw) == index_sha256, "external index pin mismatch")
    index = strict_json(index_raw)
    require(isinstance(index, dict) and set(index) == {"schema", "problem_id", "files"}
            and index["schema"] == "city-ode-verification-v1"
            and index["problem_id"] == "9700026", "portable index identity/schema")
    pins = rows_map(index["files"])
    require("package_index.json" not in pins and
            {"check_originals.py", "verify_package.py", "build_verification.py", "root_evidence/SOURCE_MANIFEST.json"} <= set(pins),
            "portable inventory required files")
    closed_tree(root, set(pins) | {"package_index.json"})
    blobs = {"package_index.json": index_raw}
    for name, row in pins.items():
        raw = read_regular(within(root, name), row["bytes"])
        authenticate(raw, row, name)
        if name.endswith(".json"):
            strict_json(raw)
        blobs[name] = raw
    return pins, blobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index_sha256")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--pdf-2012", type=Path, help="Explicit ordinary-file path overriding cities-2012.pdf")
    for name in ("catalog", "problems", "reports", "pdf-dir"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    values = [args.catalog, args.problems, args.reports, args.pdf_dir]
    require(all(values) or not any(values), "supply all four source locations or none")
    require(not args.pdf_2012 or all(values), "--pdf-2012 requires all four source locations")
    require(args.full or not any(values), "source replay requires --full")
    root = selected_root(args.root)
    pins, blobs = package_inputs(root, args.index_sha256)
    require(read_regular(Path(__file__).resolve()) == blobs["verify_package.py"], "startup verifier copy mismatch")
    result = {"status": "PASS", "scope": "Closed inventory and finite diagnostics; not proof or priority certification.",
              "indexed_file_count": len(pins), "package_member_count": len(blobs),
              "index_sha256": args.index_sha256, "full_replay": "NOT_RUN"}
    if args.full:
        # Execute a verified in-memory byte copy, not a later read of the package.
        with tempfile.TemporaryDirectory(prefix="city ODE portable verification ") as td:
            copy = Path(td) / "authenticated package"
            copy.mkdir()
            for name, raw in blobs.items():
                target = copy / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
                target.chmod(0o644)
            command = [sys.executable, "-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
            command += [str(copy / "check_originals.py"), "--root", str(copy)]
            for name, value in zip(("catalog", "problems", "reports", "pdf-dir"), values):
                if value is not None:
                    command += ["--" + name, str(value.absolute())]
            if args.pdf_2012 is not None:
                command += ["--pdf-2012", str(args.pdf_2012.absolute())]
            proc = subprocess.run(command, cwd=td, capture_output=True, timeout=700)
            require(proc.returncode == 0 and not proc.stderr, "authenticated original checker failed")
            replay = strict_json(proc.stdout)
            require(replay.get("status") == "PASS", "original checker result")
            result["full_replay"] = replay
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

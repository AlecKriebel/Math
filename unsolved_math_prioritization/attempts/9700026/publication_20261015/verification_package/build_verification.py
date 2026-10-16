#!/usr/bin/env python3
"""Build a deterministic verification ZIP from an externally authenticated closed PR880 assembly.
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assembly", type=Path)
    parser.add_argument("index_sha256")
    parser.add_argument("verifier_sha256")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = selected_root(args.assembly)
    require(stat.S_ISDIR(root.lstat().st_mode), "assembly must be directory")
    require(re.fullmatch("[0-9a-f]{64}", args.index_sha256 or "") and
            re.fullmatch("[0-9a-f]{64}", args.verifier_sha256 or ""), "external digest syntax")
    # Reject special files before reading either startup trust anchor.
    raw = read_regular(root / "package_index.json", limit=MAX_INDEX)
    require(sha(raw) == args.index_sha256, "external index pin mismatch")
    index = strict_json(raw)
    require(isinstance(index, dict) and set(index) == {"schema", "problem_id", "files"}
            and index["schema"] == "city-ode-verification-v1"
            and index["problem_id"] == "9700026", "portable index identity/schema")
    pins = rows_map(index["files"])
    require("package_index.json" not in pins and
            {"check_originals.py", "verify_package.py", "build_verification.py", "root_evidence/SOURCE_MANIFEST.json"} <= set(pins),
            "portable inventory required files")
    require(pins["verify_package.py"]["sha256"] == args.verifier_sha256,
            "startup verifier external pin mismatch")
    closed_tree(root, set(pins) | {"package_index.json"})
    blobs = {"package_index.json": raw}
    for name, row in pins.items():
        data = read_regular(within(root, name), row["bytes"])
        authenticate(data, row, name)
        if name.endswith(".json"):
            strict_json(data)
        blobs[name] = data
    require(sha(blobs["verify_package.py"]) == args.verifier_sha256,
            "startup verifier external pin mismatch")
    require(read_regular(Path(__file__).resolve()) == blobs["build_verification.py"], "startup builder copy mismatch")
    # Resolve existing ancestor aliases for containment, but reject a leaf alias.
    require(not args.output.is_symlink(), "output directory leaf alias")
    out = args.output.resolve()
    require(out != root and root not in out.parents, "output must be outside assembly")
    if out.exists():
        require(stat.S_ISDIR(out.lstat().st_mode) and not any(out.iterdir()), "output must be fresh or empty")
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
    # The external verifier digest is checked before its copied bytes execute.
    with tempfile.TemporaryDirectory(prefix="city ODE authenticated builder ") as td:
        copy = Path(td) / "verified input"
        copy.mkdir()
        for name, data in blobs.items():
            target = copy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            target.chmod(0o644)
        command = [sys.executable, "-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
        command += [str(copy / "verify_package.py"), args.index_sha256, "--root", str(copy), "--full"]
        proc = subprocess.run(command, cwd=td, capture_output=True, timeout=700)
        require(proc.returncode == 0 and not proc.stderr, "verified assembly replay failed")
        result = strict_json(proc.stdout)
        require(result.get("status") == "PASS", "verified assembly result")
    # Recheck fresh output after replay; no output is written on validation failure.
    if out.exists():
        require(not any(out.iterdir()), "output changed during validation")
    else:
        out.mkdir()
    archive = out / "verification.zip"
    with archive.open("xb") as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for name in sorted(blobs):
                info = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, blobs[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = read_regular(archive)
    print(json.dumps({"status": "PASS", "archive": str(archive), "bytes": len(data), "sha256": sha(data),
                      "member_count": len(blobs), "fixed_zip_timestamp_utc": "2026-10-15T00:00:00Z",
                      "reproducibility_scope": "Same input bytes, Python ZIP implementation and zlib; no cross-runtime compressed-byte claim.",
                      "python_version": sys.version.split()[0],
                      "zlib_runtime": __import__("zlib").ZLIB_RUNTIME_VERSION, "assembly_replay": result}, sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

#!/usr/bin/env python3
"""PR883 artifact authentication and finite replay only. Authenticate startup independently.
Standard library; no novelty, mathematical-proof, human-review or publication approval.
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
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib

MAX_FILE = 256 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_INDEX = 4 * 1024 * 1024
SOURCE_MANIFEST_SHA256 = "53bba0a85fa099146f7bb6d7520bc8a3a423894b702a9e8e4cb9f63ded3a48ab"
FROZEN_HEAD = "af25d26e21945a1a132aace5e600485152777070"
REQUIRED = {"check_originals.py", "verify_package.py", "build_verification.py", "root_evidence/SOURCE_MANIFEST.json"}


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
    def number(value):
        result = float(value)
        require(math.isfinite(result), "overflow/nonfinite JSON number")
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=number)


def digest(value):
    require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "SHA256 syntax")
    return value


def safe_name(name):
    require(type(name) is str and 0 < len(name) <= 512 and
            re.fullmatch(r"[A-Za-z0-9_./-]+", name), "relative path alphabet/length")
    require(all(p not in ("", ".", "..") for p in name.split("/")) and
            not PurePosixPath(name).is_absolute() and str(PurePosixPath(name)) == name,
            "unsafe relative path: " + name)
    return name


def pin_row(row, git=False):
    keys = {"path", "bytes", "sha256"} | ({"git_blob"} if git else set())
    require(type(row) is dict and set(row) == keys, "inventory row schema")
    safe_name(row["path"])
    require(type(row["bytes"]) is int and 0 <= row["bytes"] <= MAX_FILE, "typed byte count")
    digest(row["sha256"])
    if git:
        require(type(row["git_blob"]) is str and re.fullmatch(r"[0-9a-f]{40}", row["git_blob"]), "Git blob syntax")
    return row


def rows_map(rows, git=False):
    require(type(rows) is list and 0 < len(rows) <= 10000, "inventory list")
    result, aliases = {}, set()
    for row in rows:
        pin_row(row, git)
        name = row["path"]
        require(name.casefold() not in aliases, "duplicate/aliased inventory path")
        aliases.add(name.casefold())
        result[name] = row
    require(sum(r["bytes"] for r in rows) <= MAX_TOTAL, "inventory total limit")
    for name in result:
        require(not any(str(p).casefold() in aliases for p in PurePosixPath(name).parents if str(p) != "."), "file/directory collision")
    # Reject directory spellings that alias even when leaf names differ.
    directories = {}
    for name in result:
        for p in PurePosixPath(name).parents:
            if str(p) != ".":
                key = str(p).casefold()
                require(key not in directories or directories[key] == str(p), "directory name alias")
                directories[key] = str(p)
    return result


def read_regular(path, expected_size=None, limit=MAX_FILE):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "nonregular input: " + path.name)
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        require(stat.S_ISREG(info.st_mode) and (info.st_dev, info.st_ino) == (before.st_dev, before.st_ino), "input changed during open")
        require(info.st_size <= limit and (expected_size is None or info.st_size == expected_size), "input size mismatch/limit: " + path.name)
        bound = expected_size if expected_size is not None else limit
        raw = stream.read(bound + 1)
        require(len(raw) == info.st_size and len(raw) <= bound, "bounded input read mismatch")
        after = os.fstat(stream.fileno())
        require((after.st_size, after.st_mtime_ns) == (info.st_size, info.st_mtime_ns), "input changed during read")
    return raw


def stream_pin(path, size, expected):
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size == size, "source input type/size")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    h, count = hashlib.sha256(), 0
    with os.fdopen(fd, "rb") as stream:
        opened = os.fstat(stream.fileno())
        require(stat.S_ISREG(opened.st_mode) and (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino), "source input changed")
        while True:
            chunk = stream.read(min(1024 * 1024, size + 1 - count))
            if not chunk:
                break
            h.update(chunk)
            count += len(chunk)
            require(count <= size, "source input exceeds pin")
        after = os.fstat(stream.fileno())
        require((after.st_size, after.st_mtime_ns) == (opened.st_size, opened.st_mtime_ns), "source changed during hash")
    require(count == size and h.hexdigest() == expected, "complete streaming source pin mismatch")


def within(root, name):
    safe_name(name)
    p = root
    for part in PurePosixPath(name).parts[:-1]:
        p = p / part
        require(stat.S_ISDIR(p.lstat().st_mode), "nonregular input directory: " + part)
    return root / name


def authenticate(raw, row, label):
    require(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "pin mismatch: " + label)


def selected_root(path):
    require(stat.S_ISDIR(path.lstat().st_mode), "root must be ordinary directory")
    return path.resolve()


def closed_tree(root, names):
    require(stat.S_ISDIR(root.lstat().st_mode), "root must be ordinary directory")
    expected = set(names)
    rows_map([{"path": n, "bytes": 0, "sha256": "0" * 64} for n in sorted(expected)])
    directories = {str(p) for n in expected for p in PurePosixPath(n).parents if str(p) != "."}
    seen = set()
    def visit(folder, prefix=""):
        with os.scandir(folder) as entries:
            for entry in entries:
                name = prefix + entry.name
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    require(name in directories, "unlisted directory: " + name)
                    visit(Path(entry.path), name + "/")
                else:
                    require(stat.S_ISREG(mode), "nonregular tree entry: " + name)
                    require(name in expected, "unlisted file: " + name)
                    seen.add(name)
    visit(root)
    require(seen == expected, "missing inventory file")


def zip_payloads(raw, expected, generated=False):
    # Closed representation: contiguous local records from byte zero, contiguous
    # central records, one terminal EOCD; no extraction, prefixes, gaps or trailers.
    require(len(raw) >= 22, "ZIP truncated")
    end_at = len(raw) - 22
    end = struct.unpack_from("<4s4H2IH", raw, end_at)
    require(end[0] == b"PK\x05\x06" and end[1] == end[2] == end[7] == 0 and
            end[3] == end[4] == len(expected) and end[6] + end[5] == end_at, "ZIP end metadata/extent")
    result = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        require(archive.start_dir == end[6] and not archive.comment and
                [i.filename for i in infos] == sorted(expected), "ZIP closed sorted member set")
        cursor, central = 0, end[6]
        for info in infos:
            name = safe_name(info.filename)
            want = expected[name]
            require(type(want) is bytes and len(want) <= MAX_FILE, "ZIP expected payload bound")
            mode = info.external_attr >> 16
            require(info.create_system == 3 and info.create_version == info.extract_version == 20 and
                    info.external_attr == ((stat.S_IFREG | (0o644 if generated else stat.S_IMODE(mode))) << 16) and
                    stat.S_ISREG(mode) and stat.S_IMODE(mode) in ((0o644,) if generated else (0o444, 0o644)) and
                    info.flag_bits in (0, 0x800) and info.compress_type == zipfile.ZIP_DEFLATED and
                    not info.extra and not info.comment and info.volume == info.internal_attr == 0 and
                    (not generated or info.date_time == (2026, 10, 15, 0, 0, 0)), "ZIP unsafe central metadata: " + name)
            require(info.file_size == len(want) and info.header_offset == cursor and cursor + 30 <= end[6], "ZIP local offset/size")
            local = struct.unpack_from("<4s5H3I2H", raw, cursor)
            dosdate = ((info.date_time[0] - 1980) << 9) | (info.date_time[1] << 5) | info.date_time[2]
            dostime = (info.date_time[3] << 11) | (info.date_time[4] << 5) | (info.date_time[5] // 2)
            require(local[:9] == (b"PK\x03\x04", 20, info.flag_bits, 8, dostime, dosdate, info.CRC, info.compress_size, info.file_size) and local[10] == 0, "ZIP local/central metadata disagreement")
            encoded = name.encode("utf-8" if info.flag_bits & 0x800 else "cp437")
            start = cursor + 30
            require(local[9] == len(encoded) and raw[start:start + local[9]] == encoded, "ZIP local name disagreement")
            cursor = start + local[9] + info.compress_size
            require(cursor <= end[6], "ZIP local payload boundary")
            require(central + 46 <= end_at, "ZIP central truncation")
            c = struct.unpack_from("<4s6H3I5H2I", raw, central)
            require(c == (b"PK\x01\x02", (3 << 8) | 20, 20, info.flag_bits, 8, dostime, dosdate,
                    info.CRC, info.compress_size, info.file_size, len(encoded), 0, 0, 0, 0, info.external_attr, info.header_offset), "ZIP raw central disagreement")
            require(raw[central + 46:central + 46 + len(encoded)] == encoded, "ZIP raw central name")
            central += 46 + len(encoded)
            # ZipExtFile accepts unused bytes after the first DEFLATE stream.
            # Validate the complete declared raw region independently, with one
            # extra output byte as an expansion bound. EOF plus empty suffix and
            # tail are necessary even when the expected output bytes match.
            compressed = raw[start + local[9]:cursor]
            decoder = zlib.decompressobj(-15)
            inflated = decoder.decompress(compressed, len(want) + 1)
            consumed = len(compressed) - len(decoder.unused_data) - len(decoder.unconsumed_tail)
            require(inflated == want and decoder.eof and not decoder.unused_data and
                    not decoder.unconsumed_tail and consumed == info.compress_size == len(compressed),
                    "ZIP raw DEFLATE exact-consumption mismatch: " + name)
            with archive.open(info) as stream:
                payload = stream.read(len(want) + 1)
                require(not stream.read(1), "ZIP expanded bound")
            require(payload == want, "ZIP byte-exact member mismatch: " + name)
            if name.endswith(".json"):
                strict_json(payload)
            result[name] = payload
        require(cursor == end[6] and central == end_at, "ZIP local/central gap")
    return result


def package_inputs(root, index_sha256, startup=None):
    digest(index_sha256)
    raw = read_regular(root / "package_index.json", limit=MAX_INDEX)
    require(sha(raw) == index_sha256, "external index pin mismatch")
    index = strict_json(raw)
    require(type(index) is dict and set(index) == {"schema", "problem_id", "files"} and
            index["schema"] == "diffuse-9900008-verification-v1" and index["problem_id"] == "9900008", "portable typed identity/schema")
    pins = rows_map(index["files"])
    require("package_index.json" not in pins and REQUIRED <= set(pins), "portable required inventory")
    closed_tree(root, set(pins) | {"package_index.json"})
    blobs = {"package_index.json": raw}
    for name, row in pins.items():
        data = read_regular(within(root, name), row["bytes"])
        authenticate(data, row, name)
        if name.endswith(".json"):
            strict_json(data)
        blobs[name] = data
    if startup:
        require(read_regular(Path(__file__).resolve()) == blobs[startup], "startup copy mismatch")
    return pins, blobs


def materialize(root, blobs):
    root.mkdir()
    for name, data in blobs.items():
        target = root / safe_name(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        target.chmod(0o644)


def isolated():
    require(sys.version_info >= (3, 10), "Python >=3.10 required")
    require(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode, "run with -I -S -B")


def rejected_main(main):
    try:
        isolated()
        main()
    except (ValueError, OSError, KeyError, TypeError, RuntimeError, OverflowError, RecursionError,
            zipfile.BadZipFile, zlib.error, subprocess.TimeoutExpired, UnicodeError, struct.error) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, sort_keys=True))
        sys.exit(1)

def run_originals(blobs, index_sha256, values, verify_only=False):
    with tempfile.TemporaryDirectory(prefix="diffuse portable verification ") as td:
        root = Path(td) / "authenticated"
        materialize(root, blobs)
        command = [sys.executable, "-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
        command += [str(root / "check_originals.py"), index_sha256, "--root", str(root)]
        if verify_only:
            command += ["--verify-only"]
        for name, value in zip(("catalog", "problems", "reports", "pdf-dir"), values):
            if value is not None:
                command += ["--" + name, str(value.absolute())]
        proc = subprocess.run(command, cwd=td, capture_output=True, timeout=1600)
        require(proc.returncode == 0 and not proc.stderr, "authenticated original checker failed")
        result = strict_json(proc.stdout)
        require(type(result) is dict and result.get("status") == "PASS" and result.get("original_files") == 26 and
                result.get("direct_subprocess_count") == (0 if verify_only else 6) and
                result.get("nested_author_subprocess_count") == (0 if verify_only else 16) and
                result.get("historical_executable_audit_replayed") is False, "original checker exact receipt contract")
        return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("index_sha256")
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--verify-only", action="store_true", help="Authenticate all files and original structure; omit every archival replay.")
    for name in ("catalog", "problems", "reports", "pdf-dir"):
        p.add_argument("--" + name, type=Path)
    args = p.parse_args()
    values = [args.catalog, args.problems, args.reports, args.pdf_dir]
    require(all(values) or not any(values), "supply all four source locations or none")
    pins, blobs = package_inputs(selected_root(args.root), args.index_sha256, "verify_package.py")
    replay = run_originals(blobs, args.index_sha256, values, args.verify_only)
    print(json.dumps({"status": "PASS", "scope": "Artifact authentication and finite replay only; no proof, novelty, priority or publication approval.",
                      "index_sha256": args.index_sha256, "indexed_file_count": len(pins), "package_member_count": len(blobs),
                      "originals": replay}, sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

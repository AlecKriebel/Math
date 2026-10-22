#!/usr/bin/env python3
"""Authenticate the externally pinned current PR872 repository package and its portable copy.
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
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile,
            subprocess.TimeoutExpired, UnicodeError) as exc:
        print(json.dumps({"status": "REJECTED", "reason": str(exc)}, sort_keys=True))
        sys.exit(1)

SOURCE_MANIFEST_SHA256 = "4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8"
FROZEN_HEAD = "e3d77731b45b5f463df46e769faa01d65fe193ec"
PREPRINT = "publication_20261015/preprint/"
PORTABLE = "publication_20261015/verification_package/"
CORE_FILES = {
    "note.tex", "output/pdf/note.pdf", "README.md", "metadata.json",
    "CURRENT_PRIORITY.md", "check_originals.py", "verify_package.py",
    "build_verification.py", "package_index.json", "verification.zip",
    "zenodo-deposit.json",
}
DEPOSIT_FILES = [
    {"path": "output/pdf/note.pdf", "name": "property-t-free-product-note.pdf"},
    {"path": "verification.zip", "name": "property-t-free-product-verification.zip"},
]


def outer_inputs(root, manifest_sha256):
    require(isinstance(manifest_sha256, str) and re.fullmatch("[0-9a-f]{64}", manifest_sha256),
            "external outer manifest SHA256 required")
    raw = read_regular(root / "PUBLICATION_MANIFEST.json", limit=MAX_INDEX)
    require(sha(raw) == manifest_sha256, "external outer manifest pin mismatch")
    manifest = strict_json(raw)
    require(isinstance(manifest, dict) and set(manifest) == {"schema", "problem_id", "files"}
            and manifest["schema"] == "random-property-t-current-publication-v1"
            and manifest["problem_id"] == "30006628", "current outer identity/schema")
    pins = rows_map(manifest["files"])
    require("PUBLICATION_MANIFEST.json" not in pins and
            {"README.md", "RESEARCH_LOG.md", "CURRENT_PUBLICATION.json", "verify_current_publication.py"}
            <= set(pins), "current outer required files")
    closed_tree(root, set(pins) | {"PUBLICATION_MANIFEST.json"})
    blobs = {"PUBLICATION_MANIFEST.json": raw}
    for name, row in pins.items():
        data = read_regular(within(root, name), row["bytes"])
        authenticate(data, row, name)
        blobs[name] = data
    # An outer manifest is not a trust anchor for the code that is already
    # running. Authenticate startup bytes independently before invoking this
    # file. This check also prevents using a different wrapper with --root.
    startup = read_regular(Path(__file__).resolve())
    require(startup == blobs["verify_current_publication.py"], "outer startup copy mismatch")
    return pins, blobs


def portable_inputs(blobs):
    preprint = {name[len(PREPRINT):]: raw for name, raw in blobs.items() if name.startswith(PREPRINT)}
    require(set(preprint) == CORE_FILES, "current preprint core file set")
    portable = {name[len(PORTABLE):]: raw for name, raw in blobs.items() if name.startswith(PORTABLE)}
    require("package_index.json" in portable, "portable index missing")
    index_raw = portable["package_index.json"]
    require(len(index_raw) <= MAX_INDEX, "portable index size limit")
    index = strict_json(index_raw)
    require(isinstance(index, dict) and set(index) == {"schema", "problem_id", "files"}
            and index["schema"] == "random-property-t-verification-v1"
            and index["problem_id"] == "30006628", "portable index identity/schema")
    pins = rows_map(index["files"])
    require("package_index.json" not in pins and
            {"check_originals.py", "verify_package.py", "root_evidence/SOURCE_MANIFEST.json"}
            <= set(pins), "portable required files")
    require(set(portable) == set(pins) | {"package_index.json"}, "portable closed member set")
    for name, row in pins.items():
        authenticate(portable[name], row, "portable " + name)
    copies = {
        "note.tex": "note.tex", "output/pdf/note.pdf": "note.pdf",
        "README.md": "README.md", "metadata.json": "metadata.json",
        "CURRENT_PRIORITY.md": "CURRENT_PRIORITY.md",
        "check_originals.py": "check_originals.py", "verify_package.py": "verify_package.py",
        "build_verification.py": "build_verification.py", "package_index.json": "package_index.json",
    }
    for pre_name, inner_name in copies.items():
        require(inner_name in portable and preprint[pre_name] == portable[inner_name],
                "preprint/portable copy mismatch: " + pre_name)
    current = strict_json(blobs["CURRENT_PUBLICATION.json"])
    metadata = strict_json(preprint["metadata.json"])
    deposit = strict_json(preprint["zenodo-deposit.json"])
    require(isinstance(current, dict) and isinstance(metadata, dict) and isinstance(deposit, dict),
            "current metadata object required")
    require(set(deposit) == {"metadata", "files"} and deposit["files"] == DEPOSIT_FILES,
            "deposit upload file binding")
    require(current.get("zenodo_metadata") == metadata == deposit["metadata"]
            == strict_json(portable["metadata.json"]), "current metadata copies differ")
    return preprint, portable, sha(index_raw)


def original_copies(blobs, portable):
    manifest_raw = portable["root_evidence/SOURCE_MANIFEST.json"]
    require(sha(manifest_raw) == SOURCE_MANIFEST_SHA256, "frozen source manifest pin mismatch")
    manifest = strict_json(manifest_raw)
    require(isinstance(manifest, dict) and
            set(manifest) == {"timestamp_utc", "problem_id", "pr", "frozen_head", "source_prefix", "files"}
            and manifest["problem_id"] == 30006628 and manifest["pr"] == 872
            and manifest["frozen_head"] == FROZEN_HEAD
            and manifest["source_prefix"] == "random_property_t_30006628/", "frozen source identity")
    pins = rows_map(manifest["files"], git=True)
    require(len(pins) == 15, "frozen original file count")
    source = {name[len("source/"):]: raw for name, raw in portable.items() if name.startswith("source/")}
    require(set(source) == set(pins), "frozen source closed file set")
    preserved = set(pins) - {"README.md", "PUBLICATION_MANIFEST.json"}
    for name, row in pins.items():
        raw = source[name]
        authenticate(raw, row, "frozen original " + name)
        git_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        require(git_blob == row["git_blob"], "frozen original Git blob mismatch: " + name)
        if name in preserved:
            require(name in blobs and blobs[name] == raw, "preserved root original mismatch: " + name)
    return len(pins), len(preserved)


def archive_copies(raw, portable):
    # No archive extraction occurs. Declared size is checked against previously
    # authenticated bytes before a bounded member read, including under -O.
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(names == sorted(portable), "verification ZIP closed sorted member set")
        require(not archive.comment, "verification ZIP archive comment")
        for info in infos:
            name = safe_name(info.filename)
            require(not info.is_dir() and info.create_system == 3
                    and info.external_attr == ((stat.S_IFREG | 0o644) << 16)
                    and info.flag_bits in (0, 0x800)
                    and info.compress_type == zipfile.ZIP_DEFLATED
                    and info.date_time == (2026, 10, 15, 0, 0, 0)
                    and not info.extra and not info.comment,
                    "verification ZIP unsafe metadata: " + name)
            expected = portable[name]
            require(info.file_size == len(expected), "verification ZIP declared size mismatch: " + name)
            with archive.open(info) as stream:
                data = stream.read(len(expected) + 1)
            require(data == expected, "verification ZIP member differs: " + name)
    return len(infos)


def inner_replay(portable, index_sha256, full, values):
    # Only authenticated in-memory bytes are written and then executed. Never
    # import code from either input tree or run the historical wrapper.
    with tempfile.TemporaryDirectory(prefix="property T current publication ") as td:
        copy = Path(td) / "authenticated portable package"
        copy.mkdir()
        for name, raw in portable.items():
            target = copy / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        command = [sys.executable, "-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
        command += [str(copy / "verify_package.py"), index_sha256, "--root", str(copy)]
        if full:
            command += ["--full"]
        for name, value in zip(("catalog", "problems", "reports", "pdf-dir"), values):
            if value is not None:
                # Do not resolve a supplied leaf alias before inner guards see it.
                command += ["--" + name, str(value.absolute())]
        proc = subprocess.run(command, cwd=td, capture_output=True, timeout=750)
        require(proc.returncode == 0 and not proc.stderr, "authenticated inner verifier failed")
        result = strict_json(proc.stdout)
        require(isinstance(result, dict) and result.get("status") == "PASS"
                and result.get("index_sha256") == index_sha256
                and result.get("package_member_count") == len(portable), "inner verifier result mismatch")
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest_sha256")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--full", action="store_true")
    for name in ("catalog", "problems", "reports", "pdf-dir"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    values = [args.catalog, args.problems, args.reports, args.pdf_dir]
    require(all(values) or not any(values), "supply all four source locations or none")
    require(args.full or not any(values), "source replay requires --full")
    root = args.root.resolve()
    pins, blobs = outer_inputs(root, args.manifest_sha256)
    preprint, portable, index_sha256 = portable_inputs(blobs)
    original_count, preserved_count = original_copies(blobs, portable)
    zip_count = archive_copies(preprint["verification.zip"], portable)
    result = inner_replay(portable, index_sha256, args.full, values)
    print(json.dumps({
        "status": "PASS",
        "scope": "Artifact authentication, copy consistency and finite diagnostics only; no mathematical proof or priority certificate.",
        "outer_manifest_sha256": args.manifest_sha256,
        "outer_indexed_file_count": len(pins), "outer_file_count": len(blobs),
        "preprint_core_file_count": len(preprint), "portable_member_count": len(portable),
        "verification_zip_member_count": zip_count,
        "original_file_count": original_count, "preserved_root_original_count": preserved_count,
        "historical_wrapper_executed": False, "inner_verifier_result": result,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

#!/usr/bin/env python3
"""Authenticate all frozen PR872 originals and replay finite diagnostics. No mathematical or priority certificate.
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
BUNDLES = [
    ("RANDOM_PROPERTY_T_30006628_AUTHOR_SAFE_FREEZE.zip", "RANDOM_PROPERTY_T_30006628_AUTHOR_EXTERNAL_MANIFEST.json", 12),
    ("RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT.zip", "RANDOM_PROPERTY_T_30006628_INDEPENDENT_AUDIT_MANIFEST.json", 7),
    ("RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_SAFE.zip", "RANDOM_PROPERTY_T_30006628_SECOND_INDEPENDENT_REVIEW_EXTERNAL_MANIFEST.json", 7),
]


def original_inputs(root):
    raw = read_regular(within(root, "root_evidence/SOURCE_MANIFEST.json"), limit=65536)
    require(sha(raw) == SOURCE_MANIFEST_SHA256, "frozen source manifest pin mismatch")
    manifest = strict_json(raw)
    require(set(manifest) == {"timestamp_utc", "problem_id", "pr", "frozen_head", "source_prefix", "files"}
            and manifest["problem_id"] == 30006628 and manifest["pr"] == 872
            and manifest["frozen_head"] == FROZEN_HEAD
            and manifest["source_prefix"] == "random_property_t_30006628/", "source manifest identity")
    pins = rows_map(manifest["files"], git=True)
    require(len(pins) == 15, "frozen source count")
    source = within(root, "source/placeholder").parent
    closed_tree(source, pins)
    blobs = {}
    for name, row in pins.items():
        raw = read_regular(within(source, name), row["bytes"])
        authenticate(raw, row, name)
        blob_id = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        require(blob_id == row["git_blob"], "Git blob identifier mismatch: " + name)
        blobs[name] = raw
    outer = strict_json(blobs["PUBLICATION_MANIFEST.json"])
    require(set(outer) == {"files", "note", "problem_id", "schema"}
            and outer["schema"] == "publication-file-manifest-v1"
            and outer["problem_id"] == "30006628", "historical outer schema")
    outer_pins = rows_map(outer["files"])
    require(set(outer_pins) == set(pins) - {"PUBLICATION_MANIFEST.json"}, "historical outer inventory")
    for name, row in outer_pins.items():
        authenticate(blobs[name], row, "historical outer " + name)
    members = {}
    inventories = []
    for archive, manifest_name, count in BUNDLES:
        external = strict_json(blobs[manifest_name])
        require(external["problem_id"] == "30006628", "archive problem identity")
        archive_pin = external.get("zip", external.get("archive"))
        require(isinstance(archive_pin, dict) and archive_pin.get("filename") == archive,
                "archive filename binding")
        authenticate(blobs[archive], archive_pin, archive)
        expected = rows_map(external["members"])
        require(len(expected) == count, "archive member count")
        with zipfile.ZipFile(io.BytesIO(blobs[archive])) as z:
            infos = z.infolist()
            names = [i.filename for i in infos]
            require(len(names) == len(set(names)) and set(names) == set(expected), "archive member set")
            for info in infos:
                name = safe_name(info.filename)
                mode = info.external_attr >> 16
                require(not info.is_dir() and stat.S_IFMT(mode) in (0, stat.S_IFREG)
                        and not mode & 0o111 and not info.flag_bits & 1 and not info.external_attr & 0x10
                        and info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
                        "nonregular or unsafe ZIP metadata")
                row = expected[name]
                require(info.file_size == row["bytes"], "ZIP declared size mismatch")
                with z.open(info) as stream:
                    raw = stream.read(row["bytes"] + 1)
                authenticate(raw, row, "ZIP member " + name)
                require(name not in members, "cross-archive duplicate")
                members[name] = raw
        inventories.append({"archive": archive, "members_verified": count})
    for member, loose in [
        ("random_property_t_30006628/PROOF.md", "PROOF.md"),
        ("random_property_t_30006628_independent_audit/INDEPENDENT_MATHEMATICAL_AUDIT.md", "INDEPENDENT_MATHEMATICAL_AUDIT.md"),
        ("random_property_t_30006628_second_review/INDEPENDENT_MATHEMATICAL_REVIEW.md", "SECOND_INDEPENDENT_MATHEMATICAL_REVIEW.md"),
    ]:
        require(members[member] == blobs[loose], "readable copy differs: " + loose)
    # Strictly parse all original JSON, while retaining its bytes unchanged.
    for name, raw in list(blobs.items()) + list(members.items()):
        if name.endswith(".json"):
            strict_json(raw)
    return blobs, members, inventories


def supplied_inputs(members, sources):
    pins = strict_json(members["random_property_t_30006628/sources.json"])
    result = {}
    pdf_dir = sources["pdf_dir"].resolve()
    require(stat.S_ISDIR(pdf_dir.lstat().st_mode), "PDF input directory missing")
    paths = [(sources[key], pins["corpus"][key]) for key in ("catalog", "problems", "reports")]
    paths += [(within(pdf_dir, row["filename"]), row) for row in pins["primary_sources"]]
    # Screen every supplied leaf before reading any source payload. The actual
    # bounded read repeats lstat/fstat checks, so this preflight is no substitute.
    for path, row in paths:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode), "nonregular input: " + path.name)
        require(info.st_size == row["bytes"], "byte count mismatch: " + path.name)
    for key in ("catalog", "problems", "reports"):
        row = pins["corpus"][key]
        safe_name(row["filename"])
        require("/" not in row["filename"], "source filename must be leaf")
        raw = read_regular(sources[key], row["bytes"])
        authenticate(raw, row, "supplied " + key)
        strict_json(raw)
        result[row["filename"]] = raw
    pdf_dir = sources["pdf_dir"].resolve()
    require(stat.S_ISDIR(pdf_dir.lstat().st_mode), "PDF input directory missing")
    for row in pins["primary_sources"]:
        safe_name(row["filename"])
        require("/" not in row["filename"], "PDF filename must be leaf")
        raw = read_regular(within(pdf_dir, row["filename"]), row["bytes"])
        authenticate(raw, row, "supplied PDF " + row["filename"])
        require(row["filename"] not in result, "duplicate source filename")
        result["pdfs/" + row["filename"]] = raw
    return result, pins


def replay(root, sources=None, verify_only=False):
    blobs, members, inventories = original_inputs(root)
    checked = supplied_inputs(members, sources)[0] if sources else {}
    records = []
    if not verify_only:
        with tempfile.TemporaryDirectory(prefix="property T relocated diagnostics ") as td:
            workroot = Path(td)
            cwd = workroot / "unrelated working directory"
            cwd.mkdir()
            for name, raw in {**blobs, **members}.items():
                target = workroot / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            duplicate = workroot / "random_property_t_30006628/safe/PROOF.md"
            duplicate.parent.mkdir()
            duplicate.write_bytes(blobs["PROOF.md"])
            extra = []
            if sources:
                private = workroot / "supplied inputs"
                private.mkdir()
                for name, raw in checked.items():
                    target = private / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(raw)
                pins = strict_json(members["random_property_t_30006628/sources.json"])
                for key in ("catalog", "problems", "reports"):
                    extra += ["--" + key, str(private / pins["corpus"][key]["filename"])]
                extra += ["--pdf-dir", str(private / "pdfs")]
            def execute(mode, script, args, expected=None, reason=None):
                flags = ["-I", "-S", "-B"] + (["-O"] if mode == "optimized" else [])
                proc = subprocess.run([sys.executable, *flags, str(workroot / script), *args],
                                      cwd=cwd, capture_output=True, timeout=300)
                require(not proc.stderr, "unexpected diagnostic stderr: " + script)
                data = strict_json(proc.stdout)
                if reason is None:
                    require(proc.returncode == 0 and data.get("status") == "PASS"
                            and proc.stdout == members[expected], "positive diagnostic mismatch: " + script)
                else:
                    require(proc.returncode == 1 and data == {"status": "REJECTED", "reason": reason},
                            "diagnostic intended rejection mismatch: " + script)
                records.append({"mode": mode, "script": script, "kind": "negative" if reason else "positive",
                                "mutant": args[-1] if reason else None, "exit_code": proc.returncode,
                                "stdout_bytes": len(proc.stdout), "stdout_sha256": sha(proc.stdout),
                                "expected_output_or_reason_matched": True})
            for mode in ("normal", "optimized"):
                execute(mode, "random_property_t_30006628/checker.py", [],
                        "random_property_t_30006628/checker_normal.json")
                execute(mode, "random_property_t_30006628_independent_audit/independent_kernel_check.py", [],
                        "random_property_t_30006628_independent_audit/independent_kernel_results.json")
                execute(mode, "random_property_t_30006628_second_review/independent_checks.py",
                        ["--workspace", str(workroot)], "random_property_t_30006628_second_review/independent_checks_normal.json")
                for mutant, reason in [("missing_edge", "exact expected-link kernel mismatch"),
                                       ("wrong_boundary", "exact expected-link kernel mismatch"),
                                       ("two_factor_strict", "two-factor strict gap is false"),
                                       ("critical_density", "density exponent must be positive")]:
                    execute(mode, "random_property_t_30006628/checker.py", ["--mutant", mutant], reason=reason)
                if sources:
                    execute(mode, "random_property_t_30006628/verify_sources.py", extra,
                            "random_property_t_30006628/source_verification_normal.json")
                    for mutant, reason in [("source_hash", "SHA256 mismatch: problems.json"),
                                           ("pair_hash", "complete-record pair hash mismatch")]:
                        execute(mode, "random_property_t_30006628/verify_sources.py", extra + ["--mutant", mutant], reason=reason)
    return {"status": "PASS", "scope": "Original-byte authentication and finite diagnostics only; no asymptotic proof or priority certificate.",
            "original_file_count": len(blobs), "historical_outer_file_count": 14,
            "archive_member_count": len(members), "inventories": inventories,
            "source_replay": "PASS" if sources and not verify_only else "NOT_RUN",
            "source_inputs_authenticated": bool(sources), "verify_only": verify_only,
            "receipts": records, "historical_wrapper_executed": False,
            "child_flags": ["-I", "-S", "-B"], "original_artifacts_changed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--verify-only", action="store_true")
    for name in ("catalog", "problems", "reports", "pdf-dir"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    values = [args.catalog, args.problems, args.reports, args.pdf_dir]
    require(all(values) or not any(values), "supply all four source locations or none")
    sources = dict(zip(("catalog", "problems", "reports", "pdf_dir"), values)) if all(values) else None
    print(json.dumps(replay(args.root.resolve(), sources, args.verify_only), sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

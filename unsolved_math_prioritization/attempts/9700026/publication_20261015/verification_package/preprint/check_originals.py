#!/usr/bin/env python3
"""Authenticate all frozen PR880 originals and replay finite diagnostics. No mathematical or priority certificate.
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

SOURCE_MANIFEST_SHA256 = "b0b0cdc72798cfcffc5fefeec1de30ff422f54bde83d0f8a91fd2e6a87311d8b"
FROZEN_HEAD = "fba74a301786f9648e48722e76f440097b0746c2"
PAIR_PIN = (4409, "7b18458d71482e2c4e1c62601be1824eba6ad6243c78135d90d1b75223e8e193")
INPUT_PINS = {
    "catalog.json": (21735099, "891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566"),
    "problems.json": (68931837, "04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf"),
    "research_results.json": (80334822, "8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b"),
    "cities-notes.pdf": (295226, "9cfbe9da2660fcea7e44d7ef013cb7a8a1604ff54a9e7734e71ef76959c38b89"),
    "cities-2012.pdf": (398185, "eeecb371b6e6c2860c01e1b73d812468b619ddb7e3c4cd1d0e3affc056e8a077"),
}
BUNDLES = [
    ("CITY_STABILITY_9700026_AUTHOR_SAFE_FREEZE.zip", "CITY_STABILITY_9700026_AUTHOR_EXTERNAL_MANIFEST.json", "author", 8),
    ("CITY_STABILITY_9700026_INDEPENDENT_AUDIT_SAFE.zip", "CITY_STABILITY_9700026_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json", "audit_a", 19),
]


def zip_payloads(raw, rows, label):
    expected = rows_map(rows)
    result = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)) and set(names) == set(expected), "ZIP member inventory: " + label)
        require(not archive.comment, "ZIP archive comment: " + label)
        for info in infos:
            name = safe_name(info.filename)
            mode = info.external_attr >> 16
            require(not info.is_dir() and info.create_system == 3 and stat.S_ISREG(mode)
                    and stat.S_IMODE(mode) in (0o444, 0o644)
                    and not info.flag_bits & 1 and not info.external_attr & 0x10
                    and info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED),
                    "unsafe ZIP metadata: " + label + ":" + name)
            row = expected[name]
            require(row["bytes"] <= 1000000 and info.file_size == row["bytes"], "ZIP declared size mismatch")
            with archive.open(info) as stream:
                payload = stream.read(row["bytes"] + 1)
                require(not stream.read(1), "ZIP expanded size exceeds pin")
            authenticate(payload, row, label + ":" + name)
            if name.endswith(".json"):
                strict_json(payload)
            result[name] = payload
    return result


def original_inputs(root):
    raw = read_regular(within(root, "root_evidence/SOURCE_MANIFEST.json"), limit=65536)
    require(sha(raw) == SOURCE_MANIFEST_SHA256, "frozen source manifest pin mismatch")
    manifest = strict_json(raw)
    require(type(manifest) is dict and set(manifest) == {"timestamp_utc", "problem_id", "pr", "frozen_head", "source_prefix", "files"}
            and type(manifest["problem_id"]) is int and manifest["problem_id"] == 9700026
            and type(manifest["pr"]) is int and manifest["pr"] == 880
            and manifest["frozen_head"] == FROZEN_HEAD
            and manifest["source_prefix"] == "unsolved_math_prioritization/attempts/9700026/", "source manifest identity")
    pins = rows_map(manifest["files"], git=True)
    require(len(pins) == 40 and sum(row["bytes"] for row in pins.values()) == 276581, "frozen source count/bytes")
    source = within(root, "source/placeholder").parent
    closed_tree(source, pins)
    blobs = {}
    for name, row in pins.items():
        path = within(source, name)
        require(stat.S_IMODE(path.lstat().st_mode) == 0o644, "source permission mode differs: " + name)
        payload = read_regular(path, row["bytes"])
        authenticate(payload, row, name)
        require(hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest() == row["git_blob"], "Git blob identifier mismatch: " + name)
        if name.endswith(".json"):
            strict_json(payload)
        blobs[name] = payload
    outer = strict_json(blobs["PUBLICATION_MANIFEST.json"])
    require(type(outer) is dict and set(outer) == {"files", "problem_id", "schema"}
            and outer["schema"] == "city-ode-publication-manifest-v1" and outer["problem_id"] == "9700026", "historical outer schema")
    outer_pins = rows_map(outer["files"])
    require(set(outer_pins) == set(pins) - {"PUBLICATION_MANIFEST.json"}, "historical outer inventory")
    for name, row in outer_pins.items():
        authenticate(blobs[name], row, "historical outer " + name)
    inventories = []
    bundles = {}
    for archive_name, manifest_name, folder, count in BUNDLES:
        external = strict_json(blobs[manifest_name])
        require(external["problem_id"] == "9700026" and type(external["zip"]) is dict
                and set(external["zip"]) == {"filename", "bytes", "sha256"}
                and external["zip"]["filename"] == archive_name, "archive filename binding")
        row = {"path": archive_name, "bytes": external["zip"]["bytes"], "sha256": external["zip"]["sha256"]}
        pin_row(row)
        authenticate(blobs[archive_name], row, archive_name)
        members = zip_payloads(blobs[archive_name], external["files"], archive_name)
        require(len(members) == count, "original archive member count")
        for name, data in members.items():
            require(blobs[folder + "/" + name] == data, "expanded duplicate differs: " + folder + "/" + name)
        bundles[folder] = members
        inventories.append({"archive": archive_name, "members_verified": count})
    author_zip = blobs[BUNDLES[0][0]]
    author_manifest = blobs[BUNDLES[0][1]]
    require(blobs["audit_a/AUTHOR_SAFE_FREEZE.zip"] == bundles["audit_a"]["AUTHOR_SAFE_FREEZE.zip"] == author_zip, "nested author ZIP duplicate differs")
    require(blobs["audit_a/AUTHOR_EXTERNAL_MANIFEST.json"] == bundles["audit_a"]["AUTHOR_EXTERNAL_MANIFEST.json"] == author_manifest, "nested author external manifest differs")
    nested = zip_payloads(bundles["audit_a"]["AUTHOR_SAFE_FREEZE.zip"], strict_json(author_manifest)["files"], "nested author ZIP")
    require(nested == bundles["author"], "nested author members differ")
    for name, data in nested.items():
        require(blobs["audit_a/author/" + name] == data, "nested expanded author duplicate differs")
    for folder, manifest_name in [("author", "MANIFEST.json"), ("audit_a", "MANIFEST.json"), ("review_b", "MANIFEST_B.json")]:
        inner = strict_json(blobs[folder + "/" + manifest_name])
        require(inner["problem_id"] == "9700026", "inner manifest identity")
        inner_pins = rows_map(inner["files"])
        actual = {n[len(folder)+1:] for n in blobs if n.startswith(folder + "/")}
        require(actual == set(inner_pins) | {manifest_name}, "inner manifest inventory: " + folder)
        for name, row in inner_pins.items():
            authenticate(blobs[folder + "/" + name], row, "inner manifest " + folder + "/" + name)
    return blobs, inventories


def supplied_inputs(sources):
    """Authenticate complete inputs sequentially; retain only the target records."""
    pdf_dir = selected_root(sources["pdf_dir"])
    paths = {"catalog.json": sources["catalog"], "problems.json": sources["problems"],
             "research_results.json": sources["reports"], "cities-notes.pdf": within(pdf_dir, "cities-notes.pdf"),
             "cities-2012.pdf": sources.get("pdf_2012") or within(pdf_dir, "cities-2012.pdf")}
    for name, path in paths.items():
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size == INPUT_PINS[name][0], "input type/size mismatch: " + name)
    cat = record = report = None
    for name, path in paths.items():
        size, digest = INPUT_PINS[name]
        raw = read_regular(path, size)
        require(sha(raw) == digest, "complete input pin mismatch: " + name)
        if name.endswith(".json"):
            loaded = strict_json(raw)
            if name != "research_results.json":
                require(type(loaded) is list and all(type(row) is dict for row in loaded), "corpus record-array schema")
                exact = [row for row in loaded if type(row.get("id")) in (str, int) and str(row["id"]) == "9700026"]
                require(len(exact) == 1, "strict exact-ID uniqueness")
                if name == "catalog.json":
                    cat = exact[0]
                else:
                    record = exact[0]
            else:
                require(type(loaded) is dict and "AMR-096-0026" in loaded, "missing exact-code report")
                report = loaded["AMR-096-0026"]
            del loaded
        del raw
    require(type(cat["rank"]) is int and cat["rank"] == 934
            and cat["problem_number"] == record["problem_number"] == "AMR-096-0026"
            and type(cat["title"]) is str and cat["title"] == record["title"], "canonical input identity")
    pair = json.dumps([record, report], sort_keys=True).encode()
    require((len(pair), sha(pair)) == PAIR_PIN and cat["review_hash"] == PAIR_PIN[1], "canonical complete pair mismatch")
    require(type(record["statement"]) is str and sha(record["statement"].encode()) == cat["statement_hash"]
            == "5544971834bd618005b3fdf611f753b4cf41bab24b857d0e96a7a067ee3f7b7e", "canonical statement mismatch")
    return paths


def expected_outputs(blobs):
    author = strict_json(blobs["author/verification_results.json"])["executions"]
    audit = strict_json(blobs["audit_a/AUDIT_TEST_RESULTS.json"])["checker_executions"]
    result = {}
    for self_test, kind in [(False, "certificate"), (True, "adversarial")]:
        author_rows = [row for row in author if row["mode"] == kind]
        audit_rows = [row for row in audit if row["checker"] == "independent" and row["self_test"] is self_test]
        require(author_rows and audit_rows, "historical expected outputs missing")
        a, b = author_rows[0]["result"], dict(audit_rows[0]["result"])
        require(all(row["result"] == a for row in author_rows) and all(row["result"] == b for row in audit_rows), "historical expected outputs inconsistent")
        if not self_test:
            require(a["exact_influence_sample_checks"] == 216 and a["comparison_ode_algebra_checks"] == 4
                    and a["lower_bound"] == "1/4096" and a["upper_bound"] == "2047/2048"
                    and b["independent_influence_checks"] == 600 and b["comparison_algebra_checks"] == 5
                    and b["gradient_identity_checks"] == 27, "finite diagnostic invariants")
            b["audit_manifest_verified"] = True
        else:
            require(len(a["rejected_adversarial_cases"]) == 16 and len(a["accepted_positive_controls"]) == 2
                    and len(b["negative_controls"]) == 13 and len(b["positive_controls"]) == 2, "self-test invariants")
        result[("author/verify.py", self_test)] = a
        result[("audit_a/verify_audit.py", self_test)] = b
    source_rows = strict_json(blobs["audit_a/SOURCE_CHECK_RESULTS.json"])["executions"]
    expected_source = source_rows[0]["result"]
    require(all(row["result"] == expected_source for row in source_rows)
            and expected_source["canonical_pair_bytes"] == PAIR_PIN[0]
            and expected_source["canonical_pair_sha256"] == PAIR_PIN[1]
            and expected_source["exact_id_count"] == 1, "source output invariants")
    result[("audit_a/verify_sources.py", False)] = expected_source
    return result


def replay(root, sources=None, verify_only=False):
    blobs, inventories = original_inputs(root)
    expected = expected_outputs(blobs)
    paths = supplied_inputs(sources) if sources else None
    records = []
    if not verify_only:
        with tempfile.TemporaryDirectory(prefix="city ODE relocated diagnostics ") as td:
            work = Path(td)
            relocated = work / "authenticated frozen files"
            relocated.mkdir()
            for name, raw in blobs.items():
                target = relocated / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
                target.chmod(0o644)  # New byte copies only; never a private input.
            cwd = work / "unrelated working directory"
            cwd.mkdir()
            if paths:
                corpus = work / "private corpus"
                pdfs = work / "private PDFs"
                corpus.mkdir()
                pdfs.mkdir()
                for name, path in paths.items():
                    target = (corpus if name.endswith(".json") else pdfs) / name
                    os.link(path, target, follow_symlinks=False)
                    size, digest = INPUT_PINS[name]
                    require(sha(read_regular(target, size)) == digest, "linked input pin mismatch: " + name)
            def execute(mode, script, self_test=False):
                flags = ["-I", "-S", "-B"] + (["-O"] if mode == "optimized" else [])
                args = ["--self-test"] if self_test else ([str(corpus), str(pdfs)] if script.endswith("verify_sources.py") else [])
                proc = subprocess.run([sys.executable, *flags, str(relocated / script), *args], cwd=cwd, capture_output=True, timeout=300)
                raw_expected = (json.dumps(expected[(script, self_test)], sort_keys=True, indent=2) + "\n").encode()
                require(proc.returncode == 0 and not proc.stderr and proc.stdout == raw_expected, "finite diagnostic exact-output mismatch: " + script)
                require(strict_json(proc.stdout)["status"] == "PASS", "finite diagnostic status")
                records.append({"mode": mode, "script": script, "self_test": self_test, "exit_code": proc.returncode,
                                "stdout_bytes": len(proc.stdout), "stdout_sha256": sha(proc.stdout), "expected_output_matched": True})
            for mode in ("normal", "optimized"):
                for script in ("author/verify.py", "audit_a/verify_audit.py"):
                    for self_test in (False, True):
                        execute(mode, script, self_test)
                if paths:
                    execute(mode, "audit_a/verify_sources.py")
    return {"status": "PASS", "scope": "Frozen-byte authentication and finite diagnostics only; no mathematical proof or priority certificate.",
            "original_file_count": len(blobs), "original_bytes": sum(map(len, blobs.values())), "historical_outer_file_count": 39,
            "inventories": inventories, "nested_author_members_verified": 8,
            "source_replay": "PASS" if sources and not verify_only else "NOT_RUN", "source_inputs_authenticated": bool(sources),
            "source_fixture_method": "Authenticated ordinary-file hardlinks with required legacy basenames; no input writes, chmod or truncate." if sources and not verify_only else "NOT_USED",
            "canonical_pair_bytes": PAIR_PIN[0] if sources else None, "canonical_pair_sha256": PAIR_PIN[1] if sources else None,
            "verify_only": verify_only, "finite_diagnostics": "NOT_RUN" if verify_only else "PASS", "receipts": records,
            "historical_wrapper_executed": False, "child_flags": ["-I", "-S", "-B"], "original_artifacts_changed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--verify-only", action="store_true")
    for name in ("catalog", "problems", "reports", "pdf-dir"):
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--pdf-2012", type=Path, help="Explicit ordinary-file path overriding cities-2012.pdf")
    args = parser.parse_args()
    values = [args.catalog, args.problems, args.reports, args.pdf_dir]
    require(all(values) or not any(values), "supply all four source locations or none")
    require(not args.pdf_2012 or all(values), "--pdf-2012 requires all four source locations")
    sources = dict(zip(("catalog", "problems", "reports", "pdf_dir"), values)) if all(values) else None
    if sources and args.pdf_2012:
        sources["pdf_2012"] = args.pdf_2012
    print(json.dumps(replay(selected_root(args.root), sources, args.verify_only), sort_keys=True, indent=2))


if __name__ == "__main__":
    rejected_main(main)

#!/usr/bin/env python3
"""Narrow repair evidence on actual old/revised ZIPs; no external actions.

Reproduces the two schema-type acceptances before repair, repeats every
review01 parser/control family after repair, and tests rehashed expected data.
All mutations occur in disposable local copies within this repair directory.
"""
from pathlib import Path, PurePosixPath
import copy
import datetime as dt
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
OLD = AUDIT / "preprint/prior_review_01_full/preprint/publication/fixed-birational-cycle-nonlimit-verification.zip"
NEW = AUDIT / "preprint/publication/fixed-birational-cycle-nonlimit-verification.zip"
WORK = HERE / "disposable_checks"


def require(test, message):
    if not test:
        raise RuntimeError(message)


def extract(path, dest):
    dest.mkdir(parents=True)
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate ZIP member")
        require(archive.testzip() is None, "ZIP CRC failure")
        for item in archive.infolist():
            p = PurePosixPath(item.filename)
            require(not p.is_absolute() and ".." not in p.parts and "\\" not in item.filename
                    and str(p) == item.filename and stat.S_ISREG(item.external_attr >> 16),
                    "Unsafe ZIP member")
            target = dest / str(p)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(item))
    return dest / "birational-cycle-verification"


def edit_manifest(root, transform):
    p = root / "MANIFEST.json"
    obj = json.loads(p.read_text())
    transform(obj)
    p.write_text(json.dumps(obj, indent=2) + "\n")


def append(root, name):
    p = root / name
    p.write_bytes(p.read_bytes() + b"\n")


def rehashed_expected(root):
    p = root / "expected_checks.json"
    value = json.loads(p.read_text())
    value["exact_checks"] += 1
    p.write_text(json.dumps(value))
    def update(manifest):
        for item in manifest["files"]:
            if item["path"] == "expected_checks.json":
                item.update(bytes=p.stat().st_size,
                            sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    edit_manifest(root, update)


def run(root, optimized, extra=None, interpreter=None):
    command = [interpreter or sys.executable] + (["-O"] if optimized else [])
    command += ["-B", str(root / "verify.py")] + (extra or [])
    p = subprocess.run(command, text=True, capture_output=True, timeout=30)
    return {"optimized": optimized, "exit_code": p.returncode,
            "stdout": p.stdout, "stderr_tail": p.stderr[-1200:]}


def main():
    require(not WORK.exists(), "Disposable work directory already exists")
    old = extract(OLD, WORK / "old")
    new = extract(NEW, WORK / "new")
    before = []
    for name, schema in [("schema_true", True), ("schema_float", 1.0)]:
        target = WORK / ("before_" + name)
        shutil.copytree(old, target)
        edit_manifest(target, lambda m: m.update(schema=schema))
        for optimized in (False, True):
            result = run(target, optimized)
            require(result["exit_code"] == 0, "Old type defect did not reproduce")
            before.append({"case": name, "expected_historical_behavior": "ACCEPT", **result})

    valid = []
    for interpreter in [sys.executable,
                        "/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"]:
        version = subprocess.run([interpreter, "--version"], capture_output=True, text=True,
                                 check=True).stdout.strip()
        for optimized in (False, True):
            result = run(new, optimized, interpreter=interpreter)
            require(result["exit_code"] == 0, "Repaired actual archive failed replay")
            parsed = json.loads(result["stdout"])
            require(parsed["finite_checks"] == 147619 and parsed["manifest_files_verified"] == 64,
                    "Unexpected valid replay")
            valid.append({"python": version, "result": parsed, **result})

    cases = {
        "schema_true": lambda r: edit_manifest(r, lambda m: m.update(schema=True)),
        "schema_float": lambda r: edit_manifest(r, lambda m: m.update(schema=1.0)),
        "schema_two": lambda r: edit_manifest(r, lambda m: m.update(schema=2)),
        "schema_extra": lambda r: edit_manifest(r, lambda m: m.update(extra=1)),
        "bytes_boolean": lambda r: edit_manifest(r, lambda m: m["files"][0].update(bytes=True)),
        "bytes_float": lambda r: edit_manifest(r, lambda m: m["files"][0].update(bytes=float(m["files"][0]["bytes"]))),
        "duplicate_member": lambda r: edit_manifest(r, lambda m: m["files"].append(copy.deepcopy(m["files"][0]))),
        "path_parent": lambda r: edit_manifest(r, lambda m: m["files"][0].update(path="../outside")),
        "path_absolute": lambda r: edit_manifest(r, lambda m: m["files"][0].update(path="/outside")),
        "path_backslash": lambda r: edit_manifest(r, lambda m: m["files"][0].update(path="x\\y")),
        "proof_modified": lambda r: append(r, "paper/main.tex"),
        "checker_modified": lambda r: append(r, "check_math.py"),
        "expected_modified": lambda r: append(r, "expected_checks.json"),
        "file_extra": lambda r: (r / "EXTRA").write_text("unexpected\n"),
        "file_missing": lambda r: (r / "LICENSE.txt").unlink(),
        "file_symlink": lambda r: ((r / "LICENSE.txt").unlink(), (r / "LICENSE.txt").symlink_to("../outside")),
        "directory_symlink": lambda r: (r / "EXTRA").symlink_to("/tmp", target_is_directory=True),
        "manifest_symlink": lambda r: ((r / "MANIFEST.json").rename(r / "other-manifest.json"),
                                       (r / "MANIFEST.json").symlink_to("other-manifest.json")),
        "expected_result_rehashed": rehashed_expected,
    }
    rejected = []
    for name, mutate in cases.items():
        target = WORK / ("after_" + name)
        shutil.copytree(new, target)
        mutate(target)
        for optimized in (False, True):
            result = run(target, optimized)
            require(result["exit_code"] != 0, "Malformed package accepted: " + name)
            if name in ("schema_true", "schema_float"):
                require("Unknown manifest schema" in result["stderr_tail"],
                        "Schema control rejected for an unexpected reason")
            rejected.append({"case": name, "expected": "REJECT", **result})
    for optimized in (False, True):
        result = run(new, optimized, extra=["--limit", "3"])
        require(result["exit_code"] != 0, "Command-line override accepted")
        rejected.append({"case": "command_line_override", "expected": "REJECT", **result})

    # Replays and negative tests must not mutate either extracted source tree.
    for root in (old, new):
        manifest = json.loads((root / "MANIFEST.json").read_text())
        expected = {item["path"] for item in manifest["files"]} | {"MANIFEST.json"}
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
        require(actual == expected, "Replay changed extracted file set")
        for item in manifest["files"]:
            b = (root / item["path"]).read_bytes()
            require(len(b) == item["bytes"] and hashlib.sha256(b).hexdigest() == item["sha256"],
                    "Replay changed source payload")
    receipt = {"timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "finding": "P280-PKG-01",
               "status": "PASS", "before_schema_acceptances_reproduced": len(before),
               "revised_actual_archive_replays": len(valid),
               "after_negative_attempts": len(rejected), "after_rejected": len(rejected),
               "before": before, "valid_replays": valid, "negative_controls": rejected,
               "prior_review_negative_control_families_retained": 19,
               "additional_family": "Rehashed tampered expected result",
               "scope": "Local narrow wrapper repair validation; no scientific or publication clearance"}
    (HERE / "REPAIR_TESTS.json").write_text(json.dumps(receipt, indent=2) + "\n")
    shutil.rmtree(WORK)
    print(json.dumps({key: receipt[key] for key in ["status", "before_schema_acceptances_reproduced",
                     "revised_actual_archive_replays", "after_negative_attempts", "after_rejected"]}, indent=2))


if __name__ == "__main__":
    main()

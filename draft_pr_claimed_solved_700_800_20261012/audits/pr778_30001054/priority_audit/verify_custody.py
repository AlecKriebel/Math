#!/usr/bin/env python3
"""Read-only, mtime-independent closure check. Supply the externally reported seal hash."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

sys.dont_write_bytecode = True

def need(ok, message):
    if not ok:
        raise SystemExit("FAIL: " + message)

def pin(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def inventory(base):
    result = {}
    def walk(folder):
        count = 0
        for entry in sorted(os.scandir(folder), key=lambda e: e.name):
            mode = entry.stat(follow_symlinks=False).st_mode
            rel = Path(entry.path).relative_to(base).as_posix()
            need(not stat.S_ISLNK(mode), "symlink: " + rel)
            if stat.S_ISDIR(mode):
                descendants = walk(Path(entry.path))
                need(descendants > 0, "empty directory: " + rel)
                count += descendants
            else:
                need(stat.S_ISREG(mode), "special file: " + rel)
                count += 1
                if rel != "MANIFEST.json":
                    result[rel] = pin(Path(entry.path).read_bytes())
        return count
    need(base.is_dir() and not base.is_symlink(), "packet root is not a plain directory")
    walk(base)
    return result

def current_inputs(base):
    records = json.loads((base / "INPUT_PINS.json").read_text())
    anchor = base.parent
    for rec in records["required_sibling_inputs"]:
        rel = Path(rec["relative_to_audit_parent"])
        need(not rel.is_absolute() and ".." not in rel.parts, "unsafe input path")
        current = anchor
        for part in rel.parts:
            current = current / part
            need(not current.is_symlink(), "input symlink: " + str(rel))
        need(current.is_file(), "missing current input: " + str(rel))
        need(pin(current.read_bytes()) == {"bytes": rec["bytes"], "sha256": rec["sha256"]}, "input pin: " + str(rel))
    return len(records["required_sibling_inputs"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--inputs", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).absolute().parent
    raw = (base / "MANIFEST.json").read_bytes()
    need(hashlib.sha256(raw).hexdigest() == args.manifest_sha256.lower(), "external manifest seal")
    manifest = json.loads(raw)
    need(manifest.get("schema") == 1 and manifest.get("excluded") == ["MANIFEST.json"], "manifest schema/exclusion")
    expected = {}
    for rec in manifest["files"]:
        rel = rec["path"]
        path = Path(rel)
        need(not path.is_absolute() and ".." not in path.parts and rel != "MANIFEST.json", "unsafe manifest path")
        need(rel not in expected, "duplicate manifest path")
        expected[rel] = {"bytes": rec["bytes"], "sha256": rec["sha256"]}
    actual = inventory(base)
    need(actual == expected, "recursive inventory/content differs")
    history = json.loads((base / "AUTHORED_HISTORY.json").read_text())
    for name in history["immutable_early_files"]:
        need(actual[name] == history["observed_authored_files"][name], "changed early file: " + name)
    initial = json.loads((base / "INITIAL_POSITION.json").read_text())
    independent = json.loads((base / "INDEPENDENT_FINDINGS.json").read_text())
    need(initial["historical_reports_read"] is False, "initial historical-report flag")
    need("ENOSPC" in initial["first_write_failed"], "initial custody limitation missing")
    need(independent["before_historical_peer_reports"] is True, "independent checkpoint flag")
    checked = current_inputs(base) if args.inputs else 0
    flags = ["-B"] + (["-O"] if sys.flags.optimize else [])
    word = subprocess.run([sys.executable] + flags + [str(base / "check_word.py")], check=True, capture_output=True, text=True)
    result = json.loads(word.stdout)
    need(result["status"] == "PASS", "finite check")
    need(inventory(base) == actual, "checker mutated authored files")
    need((base / "MANIFEST.json").read_bytes() == raw, "checker mutated manifest")
    print(json.dumps({"status": "PASS", "authored_files_excluding_manifest": len(actual), "hidden_files_included": True, "symlinks_special_empty_directories": False, "mtime_independent": True, "read_only_before_after": True, "immutable_early_history_files": len(history["immutable_early_files"]), "current_sibling_inputs_checked": checked, "python_optimization": sys.flags.optimize, "finite_word": result}, sort_keys=True))

if __name__ == "__main__":
    main()

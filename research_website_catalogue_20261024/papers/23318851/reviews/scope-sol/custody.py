#!/usr/bin/env python3
"""Data-only finite custody reader; no project imports or scientific execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parent.parent / "sources"
PINS = {
    "SOURCE_FINAL.json": "c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317",
    "SOURCE_MANIFEST.json": "ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8",
}
TERMINALS = {"INITIAL_MANIFEST.json", "INITIAL_SEAL.json"}

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def digest(data, algorithm="sha256"):
    return hashlib.new(algorithm, data).hexdigest()

def write_json(name, value):
    path = LANE / name
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    path.chmod(0o644)

def inventory(root, terminal_payload_exclusions=()):
    entries = []
    for path in [root] + sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        relative = "." if path == root else path.relative_to(root).as_posix()
        info = path.lstat()
        row = {"path": relative, "mode_octal": oct(stat.S_IMODE(info.st_mode))}
        if stat.S_ISDIR(info.st_mode):
            row.update(kind="directory", empty=not any(path.iterdir()))
        elif stat.S_ISREG(info.st_mode):
            row["kind"] = "file"
            if relative in terminal_payload_exclusions:
                row["payload_exclusion"] = "exact already-created recursive terminal control"
            else:
                content = path.read_bytes()
                row.update(bytes=len(content), sha256=digest(content), md5=digest(content, "md5"))
        else:
            raise AssertionError("Unsupported or symbolic object: " + str(path))
        entries.append(row)
    return entries

def authenticate_source():
    entries = inventory(SOURCE)
    by_path = {entry["path"]: entry for entry in entries}
    for name, expected in PINS.items():
        assert by_path[name]["sha256"] == expected, ("terminal pin", name, by_path[name])
        assert by_path[name]["mode_octal"] == "0o644", ("terminal mode", name)
    manifest = json.loads((SOURCE / "SOURCE_MANIFEST.json").read_text())
    final = json.loads((SOURCE / "SOURCE_FINAL.json").read_text())
    assert manifest["schema"] == "source-custody-finite-manifest-v1"
    assert final["schema"] == "native-source-acquisition-final-v1"
    assert set(manifest["excluded_control_files"]) == set(PINS)
    assert manifest["other_exclusions"] == []
    expected = {entry["path"]: entry for entry in manifest["entries"]}
    assert set(by_path) == set(expected) | set(PINS), ("whole topology", sorted(set(by_path) ^ (set(expected) | set(PINS))))
    for name, expected_entry in expected.items():
        actual = by_path[name]
        for key, value in expected_entry.items():
            assert actual.get(key) == value, ("source entry", name, key, value, actual.get(key))
    files = sum(entry["kind"] == "file" for entry in entries)
    dirs = sum(entry["kind"] == "directory" for entry in entries)
    assert files == final["regular_files"] == 95, files
    assert dirs - 1 == final["child_directories"] == 16, dirs
    assert manifest["file_count"] == files - 2
    assert manifest["directory_count"] == dirs
    return {"schema": "scope-original-source-custody-v1", "source": str(SOURCE),
            "files": files, "child_directories": dirs - 1, "pins": PINS,
            "all_hidden_empty_modes_and_topology": True, "entries": entries}

def main():
    assert len(sys.argv) == 2 and sys.argv[1] in {"before", "freeze"}
    actual = authenticate_source()
    if sys.argv[1] == "before":
        assert not (LANE / "SOURCE_BEFORE.json").exists()
        write_json("SOURCE_BEFORE.json", actual)
        print("SOURCE_BEFORE_EXACT: 95 files; 16 child directories; complete original namespace and controls")
        return
    baseline = json.loads((LANE / "SOURCE_BEFORE.json").read_text())
    assert actual == baseline, "Whole original namespace changed"
    write_json("SOURCE_AFTER.json", actual)
    for name in TERMINALS:
        path = LANE / name
        assert not path.exists(), "Terminal already exists: " + name
        path.write_text("{}\n")
        path.chmod(0o644)
    entries = inventory(LANE, TERMINALS)
    files = sum(entry["kind"] == "file" for entry in entries)
    dirs = sum(entry["kind"] == "directory" for entry in entries)
    timestamp = utc()
    manifest = {"schema": "scope-initial-finite-manifest-v1", "UTC": timestamp,
                "root": str(LANE), "regular_files_including_terminals": files,
                "child_directories": dirs - 1, "entries": entries,
                "all_actual_hidden_empty_modes_topology_included": True,
                "exact_already_created_terminal_payload_exclusions": sorted(TERMINALS),
                "other_exclusions": []}
    write_json("INITIAL_MANIFEST.json", manifest)
    content = (LANE / "INITIAL_MANIFEST.json").read_bytes()
    seal = {"schema": "scope-initial-seal-v1", "UTC": timestamp,
            "status": "FROZEN_ORIGINAL_ONLY_INITIAL_STOP_PENDING_ROOT_CHECKPOINT_AND_EXPLICIT_RESUME",
            "root": str(LANE), "regular_files_including_terminals": files,
            "child_directories": dirs - 1,
            "manifest": {"path": "INITIAL_MANIFEST.json", "bytes": len(content),
                         "sha256": digest(content), "mode_octal": "0o644"},
            "terminal_modes": {name: "0o644" for name in sorted(TERMINALS)},
            "source_entire_namespace_before_after_exact": True,
            "source_files": 95, "source_child_directories": 16, "source_pins": PINS,
            "initial_deliverable_completion_percent": 100,
            "best_guess_full_review_completion_percent": 80,
            "scientific_code_or_support_execution": False,
            "packaged_support_opinions_or_primary_bodies_read": False,
            "follow_up": None,
            "freeze_rule": "No further writes to this namespace; continuation requires a new sibling and explicit root resume."}
    write_json("INITIAL_SEAL.json", seal)
    print(json.dumps({"status": "INITIAL_FROZEN", "UTC": timestamp, "files": files,
                      "child_directories": dirs - 1, "manifest_sha256": digest(content),
                      "seal_sha256": digest((LANE / "INITIAL_SEAL.json").read_bytes())}))

if __name__ == "__main__":
    main()

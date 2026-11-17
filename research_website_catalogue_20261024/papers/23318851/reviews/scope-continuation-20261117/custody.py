#!/usr/bin/env python3
"""Own data-only custody utility. Reads JSON/bytes; never imports project code."""
import datetime
import hashlib
import json
from pathlib import Path
import stat
import sys

LANE = Path(__file__).resolve().parent
SOURCE = LANE.parent.parent / "sources"
INITIAL = LANE.parent / "scope-sol"
CONTROLS = {
    SOURCE / "SOURCE_FINAL.json": "c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317",
    SOURCE / "SOURCE_MANIFEST.json": "ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8",
    INITIAL / "INITIAL_MANIFEST.json": "d8c5cae0c0a22d22b33f42650d0a6f5481cf7c65f4723e2256e854035a3450e7",
    INITIAL / "INITIAL_SEAL.json": "4577c9660992856d5762f93019d92ff4a4f144d27b1696c28beefbe7b5fce7e6",
}
TERMINALS = {"FINAL_MANIFEST.json", "FINAL_SEAL.json"}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(name, data):
    path = LANE / name
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    path.chmod(0o644)

def inventory(root, excluded=()):
    rows = []
    for path in [root] + sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        rel = "." if path == root else path.relative_to(root).as_posix()
        st = path.lstat()
        row = {"path": rel, "mode_octal": oct(stat.S_IMODE(st.st_mode))}
        if stat.S_ISDIR(st.st_mode):
            row.update(kind="directory", empty=not any(path.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            row["kind"] = "file"
            if rel in excluded:
                row["payload_exclusion"] = "exact already-created recursive terminal control"
            else:
                data = path.read_bytes()
                row.update(bytes=len(data), sha256=sha(data), md5=hashlib.md5(data).hexdigest())
        else:
            raise AssertionError("Unexpected object: " + str(path))
        rows.append(row)
    return rows

def guard():
    for path, expected in CONTROLS.items():
        assert sha(path.read_bytes()) == expected, str(path)
    result = {}
    for name, root, files, dirs, control, exclusions in [
        ("source", SOURCE, 95, 16, "SOURCE_MANIFEST.json", {"SOURCE_FINAL.json", "SOURCE_MANIFEST.json"}),
        ("initial", INITIAL, 24, 0, "INITIAL_MANIFEST.json", {"INITIAL_MANIFEST.json", "INITIAL_SEAL.json"}),
    ]:
        actual = inventory(root)
        by_path = {row["path"]: row for row in actual}
        manifest = json.loads((root / control).read_text())
        expected = {row["path"]: row for row in manifest["entries"]}
        assert set(by_path) == set(expected) | exclusions, (name, "topology")
        for rel, entry in expected.items():
            for key, value in entry.items():
                if key != "payload_exclusion":
                    assert by_path[rel].get(key) == value, (name, rel, key)
        assert sum(row["kind"] == "file" for row in actual) == files
        assert sum(row["kind"] == "directory" for row in actual) - 1 == dirs
        result[name] = {"root": str(root), "files": files, "child_directories": dirs, "entries": actual}
    return result

def main():
    assert len(sys.argv) == 2 and sys.argv[1] in {"before", "after", "freeze"}
    phase = sys.argv[1]
    actual = guard()
    if phase == "before":
        assert not (LANE / "GUARD_BEFORE.json").exists()
        write("GUARD_BEFORE.json", actual)
        print("BEFORE_EXACT source95/16 INITIAL24/0")
        return
    assert actual == json.loads((LANE / "GUARD_BEFORE.json").read_text()), "Whole protected namespace changed"
    if phase == "after":
        write("GUARD_AFTER.json", actual)
        print("AFTER_EXACT source95/16 INITIAL24/0")
        return
    write("GUARD_FINAL.json", actual)
    for name in TERMINALS:
        path = LANE / name
        assert not path.exists(), "Already frozen"
        path.write_text("{}\n")
        path.chmod(0o644)
    entries = inventory(LANE, TERMINALS)
    stamp = now()
    files = sum(row["kind"] == "file" for row in entries)
    dirs = sum(row["kind"] == "directory" for row in entries) - 1
    write("FINAL_MANIFEST.json", {"schema": "scope-continuation-finite-manifest-v1", "UTC": stamp,
          "root": str(LANE), "regular_files": files, "child_directories": dirs, "entries": entries,
          "all_hidden_empty_modes_topology_included": True,
          "exact_already_created_terminal_payload_exclusions": sorted(TERMINALS), "other_exclusions": []})
    content = (LANE / "FINAL_MANIFEST.json").read_bytes()
    write("FINAL_SEAL.json", {"schema": "scope-continuation-final-seal-v1", "UTC": stamp,
          "status": "FROZEN_STOP_PENDING_ROOT_DISPOSITION", "root": str(LANE),
          "regular_files": files, "child_directories": dirs,
          "manifest": {"path": "FINAL_MANIFEST.json", "bytes": len(content), "sha256": sha(content)},
          "terminal_modes": {name: "0o644" for name in sorted(TERMINALS)},
          "source95_16_and_initial24_0_whole_preserved": True,
          "completion_percent": 100, "follow_up": None})
    print(json.dumps({"UTC": stamp, "files": files, "child_directories": dirs,
          "manifest_sha256": sha(content), "seal_sha256": sha((LANE / "FINAL_SEAL.json").read_bytes())}))

if __name__ == "__main__":
    main()

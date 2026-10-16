#!/usr/bin/env python3
"""Strict self-excluding authored-manifest verifier and in-memory controls."""
from pathlib import Path
import copy
import hashlib
import json

HERE = Path(__file__).resolve().parent
MANIFEST = "authored_manifest.json"

def validate(m):
    if m.get("schema") != 1 or m.get("excluded") != [MANIFEST, "tmp/**"]:
        return False
    listed = []
    for item in m.get("files", []):
        p = Path(item["path"])
        if p.is_absolute() or ".." in p.parts or p.as_posix() != item["path"]:
            return False
        if item["path"] == MANIFEST or not p.parts or p.parts[0] == "tmp":
            return False
        f = HERE / p
        if not f.is_file() or f.is_symlink():
            return False
        data = f.read_bytes()
        if len(data) != item["size"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            return False
        listed.append(item["path"])
    if not listed or listed != sorted(set(listed)):
        return False
    actual = sorted(f.relative_to(HERE).as_posix() for f in HERE.rglob("*")
                    if f.is_file() and f.relative_to(HERE).parts[0] != "tmp"
                    and f.relative_to(HERE).as_posix() != MANIFEST)
    return listed == actual

m=json.loads((HERE / MANIFEST).read_text())
assert validate(m), "authored manifest failed"
controls={"unaltered_strict_manifest":"PASS"}
for label, mutation in (
    ("corrupt_digest", lambda c: c["files"][0].update(sha256="0"*64)),
    ("corrupt_size", lambda c: c["files"][0].update(size=c["files"][0]["size"]+1)),
    ("missing_authored_entry", lambda c: c["files"].pop()),
    ("duplicate_authored_entry", lambda c: c["files"].append(c["files"][0].copy())),
    ("manifest_self_inclusion", lambda c: c["files"].append({"path":MANIFEST,"size":0,"sha256":"0"*64})),
    ("foreign_tmp_inclusion", lambda c: c["files"].append({"path":"tmp/foreign.pdf","size":0,"sha256":"0"*64})),
    ("path_traversal", lambda c: c["files"][0].update(path="../source_snapshot/PARTIAL.md")),
    ("unknown_authored_path", lambda c: c["files"].append({"path":"unknown.md","size":0,"sha256":"0"*64})),
):
    changed=copy.deepcopy(m); mutation(changed)
    assert not validate(changed), label+" was not rejected"
    controls[label]="PASS"
print(json.dumps({"passed":len(controls),"failed":0,"authored_file_count":len(m["files"]),"scope":"Own family folder only; manifest excludes itself and ignored foreign tmp. All corruption controls are in-memory and leave authored/frozen files unchanged.","checks":controls},indent=2))

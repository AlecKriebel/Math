#!/usr/bin/env python3
"""Read-only finite current-packet/body integrity check. No scientific inference."""
import argparse, hashlib, json, stat
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parent
MANIFEST = HERE / "FROZEN_SCIENTIFIC_PACKAGE_MANIFEST_01.json"

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def read_regular(root, relative):
    p = Path(relative)
    need(not p.is_absolute() and all(x not in ("", ".", "..") for x in p.parts),
         "Noncanonical relative path")
    candidate = root / p
    need(candidate.resolve() == candidate.absolute(), "Symlink or noncanonical path")
    s = candidate.lstat()
    need(stat.S_ISREG(s.st_mode), "Expected regular file")
    return candidate.read_bytes()

def match(body, row):
    return len(body) == row["bytes"] and hashlib.sha256(body).hexdigest() == row["sha256"]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--existing-root", type=Path,
                    help="Repository root containing the ten existing published files; default current repository")
    args = ap.parse_args()
    m = json.loads(MANIFEST.read_bytes())
    need(m["schema"] == "pr211-current-scientific-package-freeze-v1", "Wrong schema")
    rows = m["files"]
    need(len(rows) == m["file_count"] and len({r["case_path"] for r in rows}) == len(rows),
         "Duplicate/count mismatch")
    need([r["case_path"] for r in rows] == sorted(r["case_path"] for r in rows), "Unsorted selection")
    by_path = {}
    for row in rows:
        body = read_regular(CASE, row["case_path"])
        need(match(body, row), "Selected body mismatch: " + row["case_path"])
        by_path[row["case_path"]] = body
    for group in m["original_authored_family_mapping"]:
        sm = json.loads(by_path[group["manifest_case_path"]])
        source_rows = sm["files"]
        need(len(group["rows"]) == len(source_rows), "Incomplete family mapping")
        for source, mapping in zip(source_rows, group["rows"]):
            old = source.get("path", source.get("relative_path"))
            need(old == mapping["original_relative_path"], "Source family mapping order")
            need(match(by_path[mapping["case_path"]], source), "Mapped original payload mismatch")
    existing_root = (args.existing_root or CASE.parents[2]).resolve()
    for row in m["existing_published_files"]:
        body = read_regular(existing_root, row["path"])
        need(match(body, row), "Existing publication mismatch: " + row["path"])
        oid = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
        need(oid == row["sha"], "Existing native blob mismatch")
    print(json.dumps({
        "schema": "pr211-current-scientific-package-readonly-integrity-result-v1",
        "status": "PASS", "selected_files": len(rows),
        "selected_bytes": sum(r["bytes"] for r in rows),
        "original_authored_families": len(m["original_authored_family_mapping"]),
        "existing_published_full_bodies": len(m["existing_published_files"]),
        "scope": "Finite file/body integrity only; no theorem, priority, reviewer-independence or completion certificate",
        "writes_network_subprocess_historical_helper_execution": False
    }, sort_keys=True))
if __name__ == "__main__":
    main()

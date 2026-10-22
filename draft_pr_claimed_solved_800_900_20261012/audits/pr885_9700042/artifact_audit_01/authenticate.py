"""Independently authenticate the frozen packet without importing packet code.

Invocation: python3 -I -S -B authenticate.py REPOSITORY SOURCE EXTERNAL_MANIFEST OUTPUT
Only OUTPUT is written. All Git operations are read-only object inspection.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HEAD = "4b1ef9bbeb723a4171949a6c3934db98962ac615"
PREFIX = "unsolved_math_prioritization/attempts/9700042/"
EXTERNAL_SHA256 = "6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    repository, source, manifest, output = map(Path, sys.argv[1:])
    external_bytes = manifest.read_bytes()
    if digest(external_bytes) != EXTERNAL_SHA256:
        raise ValueError("External source-manifest digest differs from assigned pin")
    external = json.loads(external_bytes)
    tree = subprocess.run(["git", "-C", str(repository), "ls-tree", "-rz", HEAD, "--", PREFIX], check=True, capture_output=True).stdout
    entries = {}
    for line in tree.split(b"\0"):
        if line:
            meta, name = line.split(b"\t", 1)
            mode, kind, blob = meta.decode().split()
            entries[name.decode()[len(PREFIX):]] = (mode, kind, blob)
    expected = {entry["path"]: entry for entry in external["files"]}
    actual = {}
    nonregular = []
    directories = []
    for root, dirs, files in os.walk(source, followlinks=False):
        for name in dirs + files:
            path = Path(root) / name
            rel = path.relative_to(source).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                directories.append(rel)
            elif stat.S_ISREG(mode):
                actual[rel] = path
            else:
                nonregular.append(rel)
    results = []
    for rel, record in expected.items():
        path = actual.get(rel)
        if path is None:
            raise ValueError("Missing original: " + rel)
        data = path.read_bytes()
        mode, kind, blob = entries[rel]
        git_data = subprocess.run(["git", "-C", str(repository), "cat-file", "blob", HEAD + ":" + PREFIX + rel], check=True, capture_output=True).stdout
        computed_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        checks = {
            "regular_file": stat.S_ISREG(path.lstat().st_mode),
            "bytes_match": len(data) == record["bytes"],
            "sha256_match": digest(data) == record["sha256"],
            "tree_mode_100644": mode == "100644",
            "tree_kind_blob": kind == "blob",
            "tree_blob_matches_external": blob == record["git_blob"],
            "computed_blob_matches_tree": computed_blob == blob,
            "actual_git_blob_bytes_equal": data == git_data,
        }
        results.append({"path": rel, "bytes": len(data), "sha256": digest(data), "git_blob": blob, "git_mode": mode, "checks": checks})
    invariants = {
        "assigned_head": external["head"] == HEAD,
        "assigned_prefix": external["prefix"] == PREFIX,
        "original_effort_5_of_5": external["original_effort"] == "5/5",
        "exact_file_inventory": set(actual) == set(expected) == set(entries),
        "no_nonregular_entries": not nonregular,
        "original_count_30": len(actual) == external["original_file_count"] == 30,
        "original_bytes_214980": sum(r["bytes"] for r in results) == external["original_total_bytes"] == 214980,
    }
    passed = all(invariants.values()) and all(all(r["checks"].values()) for r in results)
    receipt = {"head": HEAD, "prefix": PREFIX, "external_manifest_sha256": digest(external_bytes), "source_role": "parent-frozen-originals", "git_role": "actual-objects-at-assigned-head", "invariants": invariants, "directories": sorted(directories), "nonregular_entries": nonregular, "files": results, "pass": passed}
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pass": passed, "original_files": len(actual), "original_bytes": sum(r["bytes"] for r in results), "original_effort": external["original_effort"]}, sort_keys=True))
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())

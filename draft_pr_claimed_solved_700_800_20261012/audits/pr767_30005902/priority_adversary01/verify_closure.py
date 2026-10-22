#!/usr/bin/env python3
"""Read-only closure verification. No assertions, writes, network or Git actions."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import sys

def sha(data):
    return hashlib.sha256(data).hexdigest()

def fail(message):
    raise RuntimeError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-current-input", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    expected = {row["path"]: row for row in manifest["files"]}
    if len(expected) != len(manifest["files"]):
        fail("duplicate manifest path")
    actual = {}
    latest_ns = 0
    for item in root.rglob("*"):
        mode = item.lstat().st_mode
        if stat.S_ISLNK(mode):
            fail("symlink: " + str(item))
        if stat.S_ISDIR(mode):
            if not any(item.iterdir()):
                fail("empty directory: " + str(item))
            continue
        if not stat.S_ISREG(mode):
            fail("special file: " + str(item))
        rel = item.relative_to(root).as_posix()
        if rel == "MANIFEST.json":
            continue
        actual[rel] = {"path": rel, "bytes": item.stat().st_size,
                       "sha256": sha(item.read_bytes())}
        latest_ns = max(latest_ns, item.stat().st_mtime_ns)
    if set(actual) != set(expected):
        fail("manifest inventory mismatch: " + repr(sorted(set(actual) ^ set(expected))))
    for rel in actual:
        if actual[rel] != expected[rel]:
            fail("manifest hash/size mismatch: " + rel)
    if manifest_path.stat().st_mtime_ns < latest_ns:
        fail("manifest older than a listed file")
    identity = json.loads((root / "INPUT_IDENTITY.json").read_text())
    if sha((root / "INITIAL_POSITION.md").read_bytes()) != identity["initial_position_sha256"]:
        fail("initial position changed")
    input_result = "not requested; closure is independent of later input changes"
    if args.check_current_input:
        audit = root.parent
        record = json.loads((audit / "private_sources/selected_record.json").read_text())
        statement = record["problem"]["statement"].encode()
        if len(statement) != identity["statement_bytes"] or sha(statement) != identity["statement_sha256"]:
            fail("current statement mismatch")
        if record["review_hash"] != identity["review_hash"] or record["prior_research"] != {}:
            fail("current review identity mismatch")
        proof = audit / "original/unsolved_math_prioritization/attempts/30005902/author/PROOF.md"
        if sha(proof.read_bytes()) != identity["proof_sha256"]:
            fail("current proof mismatch")
        input_result = "matches recorded source identity"
    print(json.dumps({"closure": "PASS", "files": len(actual),
                      "manifest_sha256": sha(manifest_path.read_bytes()),
                      "report_sha256": sha((root / "REPORT.md").read_bytes()),
                      "verdict_sha256": sha((root / "VERDICT.json").read_bytes()),
                      "current_input": input_result}, sort_keys=True))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)


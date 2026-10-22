#!/usr/bin/env python3
"""Read-only, closed flat custody verification with two externally supplied pins."""
import argparse
import hashlib
import json
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath

HEAD = "4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f"
EXCEPTIONS = ["MANIFEST.json"]

class CustodyError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise CustodyError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, "duplicate JSON key: " + key)
        obj[key] = value
    return obj

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)

def digest_pin(value, label):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
            "invalid external " + label + " pin")

def regular(path):
    require(stat.S_ISREG(path.lstat().st_mode), "not a regular file: " + str(path))

def safe_relative(name):
    require(isinstance(name, str) and bool(name), "invalid relative name")
    rel = PurePosixPath(name)
    require(not rel.is_absolute() and "." not in rel.parts and ".." not in rel.parts,
            "unsafe path: " + name)
    require(str(rel) == name and chr(92) not in name, "noncanonical path: " + name)
    return rel

def check_bytes(path, row, label):
    regular(path)
    data = path.read_bytes()
    require(type(row.get("bytes")) is int and row["bytes"] >= 0, "bad byte count: " + label)
    digest_pin(row.get("sha256"), label)
    require(len(data) == row["bytes"], "byte count mismatch: " + label)
    require(sha(data) == row["sha256"], "digest mismatch: " + label)

def verify(root, source_root, manifest_pin, checker_pin):
    digest_pin(manifest_pin, "manifest")
    digest_pin(checker_pin, "checker")
    require(not root.is_symlink() and root.is_dir(), "root is not a regular directory")
    require(Path(__file__).absolute() == root / "verify_custody.py",
            "checker must be invoked from the reviewed packet")
    regular(root / "verify_custody.py")
    require(sha((root / "verify_custody.py").read_bytes()) == checker_pin,
            "external checker pin mismatch")
    regular(root / "MANIFEST.json")
    raw = (root / "MANIFEST.json").read_bytes()
    require(sha(raw) == manifest_pin, "external manifest pin mismatch")
    manifest = json.loads(raw, object_pairs_hook=unique)
    require(manifest.get("schema") == "pr781-priority-adversary-custody/v1", "manifest schema")
    require(manifest.get("head") == HEAD and manifest.get("pr") == 781
            and manifest.get("problem_id") == 4600024, "target mismatch")
    require(manifest.get("explicit_exceptions") == EXCEPTIONS, "exception mismatch")
    files = manifest.get("files")
    require(isinstance(files, dict) and len(files) >= 20, "manifest inventory missing")
    require(set(p.name for p in root.iterdir()) == set(files) | set(EXCEPTIONS),
            "closed inventory mismatch")
    for name, row in files.items():
        rel = safe_relative(name)
        require(len(rel.parts) == 1 and name not in EXCEPTIONS, "packet must be flat")
        require(Path(name).suffix in {".md", ".json", ".py"}, "unapproved body/file type")
        require(isinstance(row, dict) and set(row) == {"bytes", "sha256"}, "invalid artifact row")
        check_bytes(root / name, row, name)
    inputs = read_json(root / "INPUTS.json")
    require(inputs.get("exact_head") == HEAD, "input head mismatch")
    require(isinstance(inputs.get("inputs"), dict) and len(inputs["inputs"]) == 3,
            "expected three independent input pins")
    for name, row in inputs["inputs"].items():
        rel = safe_relative(name)
        cursor = source_root
        require(not cursor.is_symlink(), "source root symlink")
        for part in rel.parts:
            cursor = cursor / part
            require(not cursor.is_symlink(), "source path symlink: " + name)
        check_bytes(cursor, row, "input:" + name)
    head_binding = read_json(root / "HEAD_BINDING.json")
    require(head_binding.get("head") == HEAD and len(head_binding.get("checks", [])) == 2,
            "head binding missing")
    for row in head_binding["checks"]:
        require(row.get("matches_local_original") is True, "exact-head input did not match")
        key = "original/" + row["path"]
        require(inputs["inputs"][key]["sha256"] == row["sha256"], "head/input digest disagreement")
    freeze = read_json(root / "INDEPENDENCE_FREEZE.json")
    require(freeze.get("before_peer_access") is True, "independent pre-peer freeze missing")
    for file_name, key in [("INDEPENDENT_REPORT.md", "report_sha256"),
                           ("INDEPENDENT_VERDICT.json", "verdict_sha256"),
                           ("INITIAL_POSITION.md", "initial_position_sha256")]:
        require(sha((root / file_name).read_bytes()) == freeze[key], "pre-peer freeze mismatch")
    original_position = read_json(root / "POSITION_FROZEN.json")
    require(original_position["verdict_sha256"] == freeze["verdict_sha256"],
            "independent verdict freeze chain mismatch")
    require(original_position["initial_position_sha256"] == freeze["initial_position_sha256"],
            "initial position freeze chain mismatch")
    verdict = read_json(root / "VERDICT.json")
    require(verdict.get("exact_head") == HEAD and verdict.get("verdict") == "bounded_inconclusive_priority",
            "verdict scope mismatch")
    for key in ["firstness_established", "global_openness_established",
                "sourceproof_changes", "git_mutations", "external_contacts"]:
        require(verdict.get(key) is False, "scope/authorization mismatch: " + key)
    require(verdict.get("peer_or_root_priority_conclusions_read") is True,
            "final peer-exposure declaration missing")
    peer = read_json(root / "PEER_REPLAY.json")
    require(peer["peer_manifest_sha256"] == freeze["peer_manifest_pin_supplied_by_root"],
            "peer pin chain mismatch")
    require(peer["query_count_claimed"] == peer["query_count_counted"] == 52,
            "peer query count mismatch")
    require(len(peer["replays"]) == 2, "peer replay count mismatch")
    for replay in peer["replays"]:
        require(replay["returncode"] == 0 and json.loads(replay["stdout"])["result"] == "PASS",
                "peer replay failed")
    command = [sys.executable, "-B"]
    if sys.flags.optimize:
        command.append("-O")
    command.append(str(root / "verify_comparison.py"))
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    require(result.returncode == 0, "comparison controls failed: " + result.stderr)
    require(json.loads(result.stdout) == read_json(root / "COMPARISON_PROBES.json"),
            "comparison receipt mismatch")
    return {
        "result": "PASS", "head": HEAD,
        "manifest_sha256": manifest_pin, "checker_sha256": checker_pin,
        "artifact_files": len(files), "input_files": len(inputs["inputs"]),
        "optimized": bool(sys.flags.optimize),
        "explicit_exceptions": EXCEPTIONS,
        "comparison_controls": "PASS",
        "peer_replays": "ordinary and optimized PASS",
        "novelty": "UNESTABLISHED"
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--expected-checker-sha256", required=True)
    args = parser.parse_args()
    root = args.root.absolute()
    source_root = (args.source_root or root.parent).absolute()
    try:
        result = verify(root, source_root, args.expected_manifest_sha256,
                        args.expected_checker_sha256)
    except (CustodyError, OSError, ValueError, TypeError, KeyError,
            subprocess.TimeoutExpired) as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())

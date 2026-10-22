#!/usr/bin/env python3
"""Strict independent safe-payload inventory and deterministic replay."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import subprocess
import sys

AUTHOR_MANIFEST_SHA256 = "b8f24c4403ad0c93be653da10572689ecb683741e4e387b97996ebb05a717609"
REVIEW_SHA256 = "a7ba968e284b4b4b467dcb2029da7bc249bc87135f05c936fadf91551909160d"
VERDICT = "PASS_SCOPED_PARTIALS_ORIGINAL_UNRESOLVED"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, "duplicate JSON key: " + key)
        out[key] = value
    return out


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def inventory(root):
    manifest_path = root / "AUDIT_MANIFEST.json"
    require(not manifest_path.is_symlink(), "root manifest is a symlink")
    manifest = read_json(manifest_path)
    require(manifest.get("schema") == "math-independent-audit-v1" and
            type(manifest.get("problem_id")) is int and manifest["problem_id"] == 6200010,
            "wrong audit manifest identity")
    entries = manifest.get("files")
    require(isinstance(entries, list) and entries, "malformed inventory")
    wanted = {}
    for item in entries:
        require(isinstance(item, dict) and set(item) == {"path", "bytes", "sha256"}, "malformed entry")
        name = item["path"]
        require(isinstance(name, str) and name and "\\" not in name, "invalid path")
        pp = PurePosixPath(name)
        require(not pp.is_absolute() and ".." not in pp.parts and pp.as_posix() == name
                and name != "AUDIT_MANIFEST.json", "unsafe or noncanonical path")
        require(name not in wanted, "duplicate inventory path")
        require(type(item["bytes"]) is int and item["bytes"] >= 0, "invalid byte count")
        require(isinstance(item["sha256"], str) and
                re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None, "invalid digest")
        wanted[name] = item
    actual = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), "symlink in audit payload")
        if path.is_file() and path != manifest_path:
            actual.add(path.relative_to(root).as_posix())
    require(actual == set(wanted), "inventory mismatch")
    for name, item in wanted.items():
        data = (root / name).read_bytes()
        require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],
                "hash or size mismatch: " + name)
    am = root / "author" / "MANIFEST.json"
    require(hashlib.sha256(am.read_bytes()).hexdigest() == AUTHOR_MANIFEST_SHA256,
            "immutable author manifest changed")
    # Validate author bytes against their original immutable inventory as well.
    for item in read_json(am)["files"]:
        data = (root / "author" / item["path"]).read_bytes()
        require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],
                "immutable author member changed")
    return len(wanted)


def replay(path):
    command = [sys.executable] + (["-O"] if sys.flags.optimize else []) + [str(path)]
    proc = subprocess.run(command, cwd=path.parent, capture_output=True, text=True, timeout=180)
    require(proc.returncode == 0, "replay failed: " + proc.stderr.strip())
    return json.loads(proc.stdout, object_pairs_hook=unique_object)


def main():
    root = Path(__file__).resolve().parent
    count = inventory(root)
    status = read_json(root / "AUDIT_STATUS.json")
    require(status.get("problem_id") == 6200010 and status.get("verdict") == VERDICT and
            status.get("original_problem_resolved") is False and status.get("turns_used") == 5,
            "wrong audit disposition")
    identity = read_json(root / "IDENTITY_RECHECK.json")
    require(identity.get("review_sha256") == REVIEW_SHA256 and identity.get("full_record_and_report_recomputed") is True,
            "wrong reviewed input identity")
    author = replay(root / "author" / "verify.py")
    require(author.get("status") == "PASS" and author.get("finite_checks") == 32400,
            "author replay result changed")
    independent = replay(root / "independent_checks.py")
    require(independent == read_json(root / "INDEPENDENT_RESULTS.json"), "independent result changed")
    require(independent.get("checks") == 5055 and independent.get("original_problem_resolved") is False,
            "independent scope changed")
    print(json.dumps({"status": "PASS", "problem_id": 6200010, "files_verified": count,
                      "verdict": VERDICT, "optimized": bool(sys.flags.optimize),
                      "author_checks": 32400, "independent_checks": 5055,
                      "original_problem_resolved": False, "turns_used": 5}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)

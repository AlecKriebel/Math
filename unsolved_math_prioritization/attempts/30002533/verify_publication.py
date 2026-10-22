#!/usr/bin/env python3
"""Portable artifact/supplemental checks; never claims source-free source verification."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

AUTHOR = "e4a387aec4351158d9b723f72122831696b4901ee4f721f94239bff5a4bde7fe"
AUDIT = "19322f26b6a68e1e1eb4647ddb28ee0f1c9457915ff4e8df2a3bb23a6484a8b1"
CORRECTED_TEXT = "731b595e70d72ca9ec4e3931603afd324bf2ed05e7d4ce76d88b56ab72d481a2"
CORRECTION = "73b29947c3b7fca9e32853b57ee410b7c18739af5c27f019ad9efea9c4722d87"


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root, name, expected):
    require(root.is_dir() and not root.is_symlink(), "invalid root")
    require(not any(p.is_symlink() for p in root.rglob("*")), "symlink rejected")
    p = root / name
    require(sha(p) == expected, "external manifest binding mismatch")
    entries = json.loads(p.read_text())["files"]
    names = [e["path"] for e in entries]
    require(len(names) == len(set(names)), "duplicate manifest path")
    for n in names:
        q = Path(n)
        require(not q.is_absolute() and ".." not in q.parts and n != name,
                "unsafe manifest path")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    require(actual == set(names) | {name}, "publication file-set mismatch")
    for e in entries:
        p = root / e["path"]
        require(p.is_file() and p.stat().st_size == e["bytes"] and sha(p) == e["sha256"],
                "payload mismatch: " + e["path"])
    return {"result": "PASS_IMMUTABLE_BINDING", "payload_count": len(entries),
            "manifest_sha256": expected}


def run(argv):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, text=True)
    require(not p.stderr, "unexpected validator stderr")
    return p.returncode, json.loads(p.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected-manifest-sha256", required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    result = {"publication": manifest(root, "PUBLICATION_MANIFEST.json", args.expected_manifest_sha256)}
    author, audit = root / "safe_freeze", root / "independent_audit_corrected"
    result["author"] = manifest(author, "MANIFEST.json", AUTHOR)
    result["audit"] = manifest(audit, "MANIFEST.json", AUDIT)
    require(sha(audit / "AUDIT.md") == CORRECTED_TEXT, "corrected audit text binding")
    require(sha(audit / "CORRECTION_RECEIPT.json") == CORRECTION, "correction receipt binding")
    code, check = run([audit / "independent_checks.py", "--candidate-dir", author, "--mutations"])
    require(code == 2, "source-free independent validator must exit 2")
    require(check["independent_source_bytes"]["result"] == "NOT_RUN_MISSING_SOURCES", "missing-source semantics")
    require(check["author_portable_replay"]["exit_code"] == 2, "source-free author validator must exit 2")
    require(check["author_portable_replay"]["output"]["sources"]["result"] == "NOT_RUN_MISSING_SOURCES", "author missing-source semantics")
    require(check["author_math_only_replay"]["exit_code"] == 0, "author math replay")
    require(check["author_math_only_replay"]["output"]["mathematics"]["assertion_count"] == 156, "author control count")
    require(check["arithmetic"]["count"] == 20, "independent control count")
    require(check["adversarial_mutations"]["count"] == 8, "portable mutation count")
    result.update(result="PASS_PORTABLE_ARTIFACT_AND_SUPPLEMENTAL_CHECKS",
                  author_arithmetic_controls=156, independent_abstract_controls=20,
                  source_free_mutation_controls=8, source_verification="NOT_RUN_MISSING_SOURCES",
                  source_free_validator_exit_codes={"author": 2, "independent": 2},
                  source_retrieval_replayed=False, source_inspection_replayed=False,
                  formal_mathematical_proof_verification=False)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}, sort_keys=True))
        sys.exit(1)

#!/usr/bin/env python3
"""Fail-closed archive integrity and exact finite replay. Writes no files."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import runpy
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise RuntimeError(message)


def main():
    require(len(sys.argv) == 1, "No command-line overrides are accepted")
    manifest_path = ROOT / "MANIFEST.json"
    require(not manifest_path.is_symlink(), "Manifest may not be a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(set(manifest) == {"schema", "files"}
            and type(manifest["schema"]) is int and manifest["schema"] == 1,
            "Unknown manifest schema")
    expected = {}
    for item in manifest["files"]:
        require(set(item) == {"path", "bytes", "sha256"}, "Unknown file-entry schema")
        name = item["path"]
        q = PurePosixPath(name)
        require(isinstance(name, str) and str(q) == name and not q.is_absolute()
                and ".." not in q.parts and "\\" not in name
                and name not in (".", "MANIFEST.json") and name not in expected,
                "Unsafe or duplicate manifest member")
        expected[name] = item
    actual = set()
    for path in ROOT.rglob("*"):
        require(not path.is_symlink(), "Archive tree contains a symlink")
        if path.is_file():
            actual.add(path.relative_to(ROOT).as_posix())
        else:
            require(path.is_dir(), "Unexpected archive filesystem object")
    require(actual == set(expected) | {"MANIFEST.json"}, "Missing or unexpected archive file")
    for name, item in expected.items():
        data = (ROOT / name).read_bytes()
        require(type(item["bytes"]) is int and len(data) == item["bytes"], "Length mismatch: " + name)
        require(hashlib.sha256(data).hexdigest() == item["sha256"], "Hash mismatch: " + name)
    module = runpy.run_path(str(ROOT / "check_math.py"))
    result = module["calculate"]()
    baseline = json.loads((ROOT / "expected_checks.json").read_text(encoding="utf-8"))
    require(result == baseline, "Exact finite replay differs from recorded baseline")
    extension = runpy.run_path(str(ROOT / "check_all_odd_primes.py"))["calculate"]()
    extension_baseline = json.loads((ROOT / "expected_all_odd_checks.json").read_text(encoding="utf-8"))
    require(extension == extension_baseline, "All-odd-prime regular/completion replay differs")
    print(json.dumps({"status": "PASS", "manifest_files_verified": len(expected),
                      "finite_checks": result["exact_checks"],
                      "admissible_primes": result["admissible_primes"],
                      "raw_graph_points": result["raw_graph_points"],
                      "all_odd_prime_checks": extension["exact_checks"],
                      "all_odd_primes": extension["odd_primes"],
                      "regular_graph_points": extension["regular_graph_points"],
                      "scope": "Integrity and finite reproducibility only; analytic proof remains essential"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

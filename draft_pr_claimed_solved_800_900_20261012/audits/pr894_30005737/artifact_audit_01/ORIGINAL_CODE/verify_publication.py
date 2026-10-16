#!/usr/bin/env python3
"""Verify preserved packet integrity and finite diagnostics; not a theorem prover."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent

def require(test, message):
    if not test:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    manifest = json.loads((ROOT / "PUBLICATION_MANIFEST.json").read_text())
    names = [f["path"] for f in manifest["files"]]
    require(len(names) == len(set(names)), "duplicate manifest paths")
    expected = set(names) | {"PUBLICATION_MANIFEST.json"}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
              if p.is_file() and "__pycache__" not in p.parts}
    require(actual == expected, "unlisted or missing packet files")
    for entry in manifest["files"]:
        path = Path(entry["path"])
        require(not path.is_absolute() and ".." not in path.parts, "unsafe manifest path")
        data = (ROOT / path).read_bytes()
        require(len(data) == entry["bytes"], "size mismatch: " + str(path))
        require(digest(data) == entry["sha256"], "hash mismatch: " + str(path))
    original = json.loads((ROOT / "authored/MANIFEST.json").read_text())
    original_names = {entry["path"] for entry in original["files"]}
    require(len(original_names) == 8, "unexpected original payload count")
    for entry in original["files"]:
        data = (ROOT / "authored" / entry["path"]).read_bytes()
        require(len(data) == entry["bytes"] and digest(data) == entry["sha256"],
                "original freeze mismatch: " + entry["path"])
    archive_names = original_names | {"MANIFEST.json"}
    with zipfile.ZipFile(ROOT / "AUTHOR_CANDIDATE.zip") as archive:
        require(len(archive.namelist()) == 9 and set(archive.namelist()) == archive_names,
                "original archive membership mismatch")
        for name in archive_names:
            require(archive.read(name) == (ROOT / "authored" / name).read_bytes(),
                    "archive byte mismatch: " + name)
        require(not any("AUDIT" in name for name in archive.namelist()),
                "audit incorrectly included in original archive")
    expected_output = (ROOT / "authored/CHECK_RESULTS.json").read_bytes()
    for flags in ([], ["-O"]):
        process = subprocess.run([sys.executable, *flags, str(ROOT / "authored/check_algebra.py")],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        require(process.stdout == expected_output, "diagnostic output changed: " + repr(flags))
        result = json.loads(process.stdout)
        require(result["checks"] == 2896 and result["invalid_R_identity_detected"] is True,
                "diagnostic scope/control mismatch")
    print(json.dumps({"integrity": "passed", "packet_files": len(expected),
                      "original_archive_members": 9, "later_audits": 2,
                      "finite_diagnostic_conditions_per_run": 2896,
                      "normal_and_optimized_outputs_match": True,
                      "scope": "Integrity and finite diagnostics only; not a formal proof."},
                     indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

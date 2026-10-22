#!/usr/bin/env python3
"""Fail-closed local integrity check against an externally authenticated manifest."""
import hashlib
import json
from pathlib import Path
import sys

EXPECTED = {"README.md", "PROOF.md", "APPROACHES.md", "SOURCE_AUDIT.md",
            "PUBLIC_METADATA.json", "STATUS.json", "check_calculations.py",
            "calculation_results.json", "verify_release.py"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def main():
    require(len(sys.argv)==1,"Unexpected arguments")
    root=Path(__file__).resolve().parent
    observed={p.name for p in root.iterdir()}
    require(observed==EXPECTED|{"MANIFEST.json"},"Unexpected or missing package entries")
    for p in root.iterdir():
        require(not p.is_symlink() and p.is_file(),"Package entries must be regular files")
    manifest=json.loads((root/"MANIFEST.json").read_text(), object_pairs_hook=unique_object)
    require(set(manifest)=={"format_version","files"},"Unexpected manifest schema")
    require(type(manifest["format_version"]) is int and manifest["format_version"]==1,
            "Unexpected manifest version")
    require(isinstance(manifest["files"],dict),"Manifest files must be an object")
    require(set(manifest["files"])==EXPECTED,"Manifest allowlist mismatch")
    for name in sorted(EXPECTED):
        item=manifest["files"][name]
        require(isinstance(item,dict) and set(item)=={"bytes","sha256"},"Invalid file metadata")
        data=(root/name).read_bytes()
        require(type(item["bytes"]) is int and len(data)==item["bytes"],f"Byte count mismatch: {name}")
        require(hashlib.sha256(data).hexdigest()==item["sha256"],f"SHA-256 mismatch: {name}")
    print(json.dumps({"result":"PASS_LOCAL_MANIFEST_INTEGRITY","files":len(EXPECTED)},sort_keys=True))


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}",file=sys.stderr)
        sys.exit(1)

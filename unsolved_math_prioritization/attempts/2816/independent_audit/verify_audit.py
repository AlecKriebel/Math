#!/usr/bin/env python3
"""Local audit integrity only; authenticate the external digest separately."""
import hashlib
import json
from pathlib import Path
import re
import sys

EXPECTED = {
    "ACCEPTANCE.json", "ACCEPTANCE.md", "ARTIFACT_VERIFICATION.json",
    "AUDITOR_SELF_TESTS.json", "CORPUS_VERIFICATION.json", "MATHEMATICAL_AUDIT.md",
    "ORIGINAL_PRESERVATION.json", "PDF_VERIFICATION.json", "README.md",
    "REPLAY_RESULTS.json", "SOURCE_INSPECTIONS.json", "SOURCE_REVIEW.md",
    "independent_calculations.json", "independent_calculations.py",
    "replay_independent.py", "verify_audit.py",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,"duplicate JSON key")
        out[key]=value
    return out


def main():
    require(len(sys.argv)==1,"unexpected arguments")
    root=Path(__file__).resolve().parent
    require({p.name for p in root.iterdir()}==EXPECTED|{"MANIFEST.json"},"audit member allowlist")
    for p in root.iterdir():
        require(p.is_file() and not p.is_symlink(),"audit members must be regular files")
    m=json.loads((root/"MANIFEST.json").read_bytes(),object_pairs_hook=unique)
    require(type(m) is dict and set(m)=={"format_version","files"},"manifest schema")
    require(type(m["format_version"]) is int and m["format_version"]==1,"manifest version")
    require(type(m["files"]) is dict and set(m["files"])==EXPECTED,"manifest file allowlist")
    for name,item in m["files"].items():
        require(type(item) is dict and set(item)=={"bytes","sha256"},"file metadata schema")
        require(type(item["bytes"]) is int and item["bytes"]>=0,"byte count type")
        require(type(item["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}",item["sha256"]),"digest syntax")
        b=(root/name).read_bytes()
        require(len(b)==item["bytes"],"byte count mismatch: "+name)
        require(hashlib.sha256(b).hexdigest()==item["sha256"],"digest mismatch: "+name)
    print(json.dumps({"result":"PASS_AUDIT_LOCAL_INTEGRITY","files":len(EXPECTED)+1},sort_keys=True))


if __name__=="__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: "+str(exc),file=sys.stderr)
        sys.exit(1)

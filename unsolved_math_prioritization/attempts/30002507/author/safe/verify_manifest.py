#!/usr/bin/env python3
"""Strict flat safe-payload integrity checker, independent of working directory."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

EXPECTED = {
    "README.md", "SCOPE.md", "RESEARCH_LOG.md", "SOURCE_REVIEW.md",
    "SOURCE_VERIFICATION.json", "REPOSITORY_CHECK.json", "STATUS.json",
    "TURN_1_RECURRENCE.md", "TURN_2_MOBIUS.md", "TURN_3_EULER_PERTURBATION.md",
    "TURN_4_REPRESENTATION.md", "TURN_5_GENERALIZED_ROUNDING.md",
    "verify.py", "CONTROL_RESULTS.json", "verify_manifest.py",
    "negative_controls.py", "NEGATIVE_CONTROL_RESULTS.json"
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def verify(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "unsafe root")
    actual = list(root.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in actual), "nonregular entry")
    require({p.name for p in actual} == EXPECTED | {"MANIFEST.json"}, "inventory mismatch")
    manifest = json.loads((root/"MANIFEST.json").read_text())
    require(set(manifest) == {"schema", "files"}, "manifest keys")
    require(manifest["schema"] == "dirichlet-single-zero-manifest-v1", "schema")
    rows = manifest["files"]
    require(isinstance(rows,list) and len(rows)==len(EXPECTED), "manifest row count")
    require(all(isinstance(r,dict) and set(r)=={"path","bytes","sha256"} for r in rows), "row keys")
    require({r["path"] for r in rows}==EXPECTED, "path set")
    require(len({r["path"] for r in rows})==len(rows), "duplicate path")
    for row in rows:
        name=row["path"]
        require(isinstance(name,str) and Path(name).name==name and name not in {".",".."}, "unsafe path")
        require(type(row["bytes"]) is int and row["bytes"]>=0,"byte count type")
        require(isinstance(row["sha256"],str) and len(row["sha256"])==64,"hash format")
        data=(root/name).read_bytes()
        require(len(data)==row["bytes"], "size mismatch: "+name)
        require(hashlib.sha256(data).hexdigest()==row["sha256"], "hash mismatch: "+name)
    return len(rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument("--replay",action="store_true")
    args=ap.parse_args()
    count=verify(args.root)
    if args.replay:
        out=subprocess.check_output([sys.executable,"-B",str(args.root/"verify.py")],text=True)
        require(out==(args.root/"CONTROL_RESULTS.json").read_text(),"control replay mismatch")
    print(json.dumps({"result":"PASS","payload_files":count,"replay":args.replay},sort_keys=True))


if __name__ == "__main__":
    main()

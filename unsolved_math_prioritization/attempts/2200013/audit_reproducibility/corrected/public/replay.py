#!/usr/bin/env python3
"""Validate externally pinned file manifest, then run exact controls in isolation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

FILES = {"PROOF.md", "README.md", "RESULT.json", "certificate.json", "replay.py", "sources.json", "verify_math.py"}


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key")
        out[key] = value
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--manifest-sha256", required=True)
    a = p.parse_args()
    try:
        need(re.fullmatch("[0-9a-f]{64}", a.manifest_sha256) is not None, "invalid external manifest pin")
        need(a.root.is_dir() and not a.root.is_symlink(), "nonsymlink root required")
        need(a.manifest.is_file() and not a.manifest.is_symlink(), "regular nonsymlink manifest required")
        raw = a.manifest.read_bytes()
        need(hashlib.sha256(raw).hexdigest() == a.manifest_sha256, "external manifest digest mismatch")
        m = json.loads(raw, object_pairs_hook=unique)
        need(type(m) is dict and set(m) == {"schema", "files"} and m["schema"] == "authored-slice-manifest-v1", "manifest schema")
        need(type(m["files"]) is list and len(m["files"]) == len(FILES), "manifest entry count")
        need({x.name for x in a.root.iterdir()} == FILES, "slice allowlist mismatch")
        seen = set()
        for item in m["files"]:
            need(type(item) is dict and set(item) == {"path", "bytes", "sha256"}, "entry schema")
            name = item["path"]
            need(type(name) is str and name in FILES and name not in seen, "manifest path or duplicate")
            seen.add(name)
            need(type(item["bytes"]) is int and 0<=item["bytes"]<1000000, "entry size")
            need(type(item["sha256"]) is str and re.fullmatch("[0-9a-f]{64}",item["sha256"]) is not None, "entry digest")
            path = a.root/name
            need(path.is_file() and not path.is_symlink(), "regular nonsymlink slice file required")
            data = path.read_bytes()
            need(len(data) == item["bytes"], "file size mismatch: "+name)
            need(hashlib.sha256(data).hexdigest() == item["sha256"], "file digest mismatch: "+name)
        need(seen == FILES, "manifest coverage")
        mode = ["-"+"O"*sys.flags.optimize] if sys.flags.optimize else []
        cp = subprocess.run([sys.executable,"-I","-B",*mode,str((a.root/"verify_math.py").resolve()),str((a.root/"certificate.json").resolve())], capture_output=True,text=True,timeout=60)
        need(cp.returncode == 0, "math controls failed: "+cp.stdout+cp.stderr)
        result = json.loads(cp.stdout, object_pairs_hook=unique)
        need(result.get("status") == "PASS", "math result missing PASS")
        print(json.dumps({"status":"PASS","manifest_sha256":a.manifest_sha256,"file_count":len(FILES),"optimization":sys.flags.optimize,"math":result},sort_keys=True))
        return 0
    except (ValueError,TypeError,KeyError,OSError,subprocess.SubprocessError) as exc:
        print(json.dumps({"status":"REJECT","reason":str(exc)},sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())

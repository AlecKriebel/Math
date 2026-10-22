#!/usr/bin/env python3
"""Strict external-manifest verification followed by pinned exact checks."""
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys

FILES = {"README.md", "RESULT.md", "APPROACHES.md", "SOURCES.json",
         "PROVENANCE.json", "EXPECTED.json", "certificate.py", "verify.py", "controls.py"}
CERTIFICATE_SHA256 = "731e6a9ebafd45e2e43e186f8480dfbb2b7ee0a48feb186bb377b774ad56b29b"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def no_duplicates(pairs):
    out={}
    for k,v in pairs:
        need(k not in out, "duplicate JSON key")
        out[k]=v
    return out


def parse(data):
    return json.loads(data, object_pairs_hook=no_duplicates)


def inventory(root):
    need(stat.S_ISDIR(root.lstat().st_mode), "package root is not a real directory")
    found=set()
    for p in root.iterdir():
        need(stat.S_ISREG(p.lstat().st_mode), "nonregular package node: "+p.name)
        found.add(p.name)
    need(found == FILES, "package inventory mismatch")


def run(manifest_path):
    root=Path(__file__).absolute().parent
    inventory(root)
    need(stat.S_ISREG(manifest_path.lstat().st_mode), "manifest is not a regular file")
    manifest_bytes=manifest_path.read_bytes()
    m=parse(manifest_bytes)
    need(type(m) is dict and set(m)=={"schema","problem_id","files"}, "manifest schema keys")
    need(type(m["schema"]) is int and m["schema"]==1, "manifest schema version")
    need(type(m["problem_id"]) is int and m["problem_id"]==30001707, "problem id")
    need(type(m["files"]) is dict and set(m["files"])==FILES, "manifest inventory mismatch")
    for name in sorted(FILES):
        entry=m["files"][name]
        need(type(entry) is dict and set(entry)=={"bytes","sha256"}, "file record keys")
        need(type(entry["bytes"]) is int and entry["bytes"]>=0, "file byte count")
        need(type(entry["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}",entry["sha256"]), "file hash format")
        data=(root/name).read_bytes()
        need(len(data)==entry["bytes"], "size mismatch: "+name)
        need(digest(data)==entry["sha256"], "hash mismatch: "+name)
    need(digest((root/"certificate.py").read_bytes())==CERTIFICATE_SHA256,
         "certificate source pin mismatch; execution refused")
    args=[sys.executable]+(["-O"] if sys.flags.optimize else [])+["-B",str(root/"certificate.py")]
    completed=subprocess.run(args,cwd=root,capture_output=True,text=True,timeout=30,check=False)
    need(completed.returncode==0 and not completed.stderr, "certificate process failed")
    actual=parse(completed.stdout)
    need(actual==parse((root/"EXPECTED.json").read_bytes()), "certificate result mismatch")
    inventory(root)
    # Detect mutations during execution as well as before it.
    for name,entry in m["files"].items():
        data=(root/name).read_bytes()
        need(len(data)==entry["bytes"] and digest(data)==entry["sha256"], "post-execution hash mismatch")
    return {"verified":True,"schema":1,"files":len(FILES),
            "manifest_sha256":digest(manifest_bytes),
            "certificate_source_pinned_before_execution":True,
            "scope":"sealed files and exact consistency checks only; no original-conjecture resolution"}


if __name__=="__main__":
    try:
        need(len(sys.argv)==2,"usage: verify.py EXTERNAL_MANIFEST.json")
        print(json.dumps(run(Path(sys.argv[1]).absolute()),sort_keys=True,indent=2))
    except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as error:
        print("VERIFICATION FAILED: "+str(error),file=sys.stderr)
        sys.exit(1)

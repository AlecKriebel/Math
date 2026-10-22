#!/usr/bin/env python3
"""Verify an externally pinned snapshot, then execute its verified byte strings."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

def require(ok,msg):
    if not ok: raise ValueError(msg)

def objpairs(items):
    out={}
    for k,v in items:
        require(k not in out,"duplicate JSON key")
        out[k]=v
    return out

def bad_constant(value): raise ValueError("non-finite JSON constant")
def finite_json(value):
    if type(value) is float:
        require(math.isfinite(value), "non-finite JSON number")
    elif type(value) is list:
        for item in value: finite_json(item)
    elif type(value) is dict:
        for item in value.values(): finite_json(item)
def strict(raw):
    value=json.loads(raw,object_pairs_hook=objpairs,parse_constant=bad_constant)
    finite_json(value)
    return value
def sha(raw):return hashlib.sha256(raw).hexdigest()

def main():
    require(len(sys.argv)==5,"usage: bootstrap.py PUBLIC MANIFEST EXPECTED_SHA256 MODE")
    root=Path(sys.argv[1]); manifest=Path(sys.argv[2]); pin=sys.argv[3]; mode=sys.argv[4]
    require(re.fullmatch(r"[0-9a-f]{64}",pin) is not None,"invalid pin")
    require(mode in ("normal","O","OO"),"invalid optimization mode")
    require(not root.is_symlink() and root.is_dir(),"invalid package root")
    raw=manifest.read_bytes()
    require(sha(raw)==pin,"manifest pin mismatch")
    m=strict(raw)
    require(type(m) is dict and set(m)=={"schema_version","files"},"manifest shape")
    require(type(m["schema_version"]) is int and m["schema_version"]==1,"manifest version")
    require(type(m["files"]) is list and 1<=len(m["files"])<=100,"manifest file list")
    snapshots={}
    for f in m["files"]:
        require(type(f) is dict and set(f)=={"name","bytes","sha256"},"file record shape")
        name=f["name"]
        require(type(name) is str and re.fullmatch(r"[A-Za-z0-9_.-]+",name) is not None,
                "unsafe or nested filename")
        require(name not in (".","..") and name not in snapshots,"duplicate/unsafe filename")
        require(type(f["bytes"]) is int and 0<=f["bytes"]<=1000000,"invalid byte count")
        require(type(f["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}",f["sha256"]),"bad hash")
        p=root/name
        require(not p.is_symlink() and p.is_file(),"missing/nonregular package file")
        b=p.read_bytes()
        require(len(b)==f["bytes"] and sha(b)==f["sha256"],"file integrity mismatch")
        snapshots[name]=b
    require({p.name for p in root.iterdir()}==set(snapshots),"unexpected/missing package entry")
    require("verify.py" in snapshots and "fixtures.json" in snapshots,"missing audit inputs")
    # Snapshot bytes are passed directly, avoiding a hash/read race in verifier input.
    code=snapshots["verify.py"].decode("utf-8")
    flags=[] if mode=="normal" else ["-"+mode]
    command=[sys.executable,"-I","-B",*flags,"-c",code,"--stdin"]
    result=subprocess.run(command,input=snapshots["fixtures.json"],capture_output=True,check=False)
    require(result.returncode==0,"verified checker failed: "+result.stderr.decode("utf-8","replace"))
    output=strict(result.stdout)
    require(type(output) is dict and output.get("ok") is True,"checker did not accept")
    print(json.dumps({"ok":True,"manifest_sha256":pin,"mode":mode,
          "uid":os.getuid(),"euid":os.geteuid(),"verifier_result":output},sort_keys=True,allow_nan=False))

if __name__=="__main__":
    try:main()
    except (ValueError,TypeError,KeyError,OSError,UnicodeError) as exc:
        print(json.dumps({"ok":False,"error":str(exc)},allow_nan=False),file=sys.stderr)
        sys.exit(1)

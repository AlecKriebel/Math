#!/usr/bin/env python3
"""Retain prelaunch sources and full streams for one actual local execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

if sys.flags.optimize:
    raise RuntimeError("Capture controller requires nonoptimized execution.")
if len(sys.argv) != 3 or not re.fullmatch(r"[A-Za-z0-9_-]+", sys.argv[1]):
    raise RuntimeError("Usage: python -B run_capture.py NEW_LABEL verify|optimized|negative|build")
label, mode = sys.argv[1:]
if mode not in ("verify", "optimized", "negative", "build"):
    raise RuntimeError("Unknown execution mode")
root = Path(__file__).resolve().parent
folder = root/"captures"/label
folder.mkdir(parents=True, exist_ok=False)
target = root/("build_archive.py" if mode == "build" else "verify.py")
source = target.read_bytes()
controller = Path(__file__).read_bytes()
(folder/"source.py").write_bytes(source)
(folder/"controller.py").write_bytes(controller)
argv = [sys.executable]
if mode == "optimized":
    argv += ["-O"]
argv += ["-B", str(target)]
if mode == "negative":
    argv += ["--negative-control"]
environment = {
    "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C",
    "PYTHONHASHSEED": "0", "PYTHONNOUSERSITE": "1",
    "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8",
}
def digest(body):
    return hashlib.sha256(body).hexdigest()
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs = {}
for name in ("paper.tex", "verify.py", "build_archive.py", "SOURCE_BINDING.json",
             "source/CANDIDATE.md", "zenodo_metadata.json", "primary_source_scope.json"):
    p = root/name
    if p.exists():
        b = p.read_bytes()
        inputs[name] = {"bytes":len(b),"sha256":digest(b)}
record = {
    "scope": "Actual local execution, not mathematical or publication approval",
    "mode": mode, "controller_pid": os.getpid(), "prelaunch_UTC": utc(),
    "argv": argv, "cwd": str(root), "environment": environment,
    "python_version": sys.version, "controller_optimization": sys.flags.optimize,
    "source_bytes": len(source), "source_sha256": digest(source),
    "controller_bytes": len(controller), "controller_sha256": digest(controller),
    "prelaunch_inputs": inputs, "child_launched": False,
}
(folder/"PRELAUNCH.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
with (folder/"stdout.txt").open("wb") as out, (folder/"stderr.txt").open("wb") as err:
    child = subprocess.Popen(argv, cwd=root, env=environment, stdout=out, stderr=err)
    record["child_launched"] = True
    record["child_pid"] = child.pid
    record["launch_return_UTC"] = utc()
    (folder/"LAUNCH.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    code = child.wait()
record["end_UTC"] = utc()
record["returncode"] = code
record["source_unchanged"] = target.read_bytes() == source
record["expected_outcome"] = "nonzero deliberate rejection" if mode in ("negative","optimized") else "zero successful run"
record["outcome_as_expected"] = (code != 0 if mode in ("negative","optimized") else code == 0)
for name in ("stdout.txt","stderr.txt"):
    body = (folder/name).read_bytes()
    record[name] = {"bytes":len(body),"sha256":digest(body)}
(folder/"CAPTURE.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
print(json.dumps(record,indent=2,sort_keys=True))
if not record["source_unchanged"] or not record["outcome_as_expected"]:
    raise RuntimeError("Unexpected outcome retained in capture "+label)

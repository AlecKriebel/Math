#!/usr/bin/env python3
"""Capture actual subprocess evidence; never invent execution metadata."""
import argparse, datetime, hashlib, json, pathlib, subprocess, sys

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(path):
    b = path.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

p = argparse.ArgumentParser()
p.add_argument("label")
p.add_argument("--cwd", default=str(pathlib.Path(__file__).resolve().parent))
p.add_argument("argv", nargs=argparse.REMAINDER)
a = p.parse_args()
argv = a.argv[1:] if a.argv[:1] == ["--"] else a.argv
if not argv:
    p.error("argv required")
root = pathlib.Path(__file__).resolve().parent
out = root / "process_evidence" / a.label
out.mkdir(parents=True, exist_ok=False)
started = utc()
with (out / "stdout.bin").open("wb") as so, (out / "stderr.bin").open("wb") as se:
    child = subprocess.Popen(argv, cwd=a.cwd, stdout=so, stderr=se)
    pid = child.pid
    code = child.wait()
ended = utc()
result = {"argv": argv, "cwd": a.cwd, "pid": pid, "started_utc": started,
          "ended_utc": ended, "exit_code": code,
          "stdout": pin(out / "stdout.bin"), "stderr": pin(out / "stderr.bin")}
(out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
sys.exit(code)

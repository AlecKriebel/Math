#!/usr/bin/env python3
"""First-party prelaunch and completed receipts for isolated, scoped reruns."""
import datetime, hashlib, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
label, cwd, source, *argv = sys.argv[1:]
out = ROOT / "captures" / label
out.mkdir(parents=True, exist_ok=False)
operator = pathlib.Path(__file__).resolve()
(out / "prelaunch_operator.py").write_bytes(operator.read_bytes())
source_path = pathlib.Path(source).resolve()
meta = {"schema": "pr47-gauge-family-actual-capture/v1", "label": label,
        "argv": argv, "cwd": str(pathlib.Path(cwd).resolve()), "started_utc": utc(),
        "source": digest(source_path), "operator": digest(operator),
        "pid": None, "exit_code": None, "actual_execution": False, "completed": False,
        "stdin_supplied": False}
(out / "PRELAUNCH.json").write_text(json.dumps(meta, indent=2)+"\n")
with (out / "stdout.bin").open("wb") as stdout, (out / "stderr.bin").open("wb") as stderr:
    child = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
    pid = child.pid
    rc = child.wait()
meta.update({"pid": pid, "exit_code": rc, "actual_execution": True, "completed": True,
             "finished_utc": utc(), "source_unchanged": digest(source_path)==meta["source"],
             "operator_unchanged": digest(operator)==meta["operator"],
             "stdout": digest(out / "stdout.bin"), "stderr": digest(out / "stderr.bin")})
(out / "CAPTURE.json").write_text(json.dumps(meta, indent=2)+"\n")
print(json.dumps({"label":label,"pid":pid,"exit_code":rc,"completed":True,
                  "stdout":meta["stdout"],"stderr":meta["stderr"]},indent=2))
sys.exit(rc)

#!/usr/bin/env python3
"""Bounded, immutable actual-process custody for this independent review."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, time

def require(value, message):
    if not value:
        raise RuntimeError(message)

root = pathlib.Path(__file__).resolve().parent
require(len(sys.argv) >= 3, "label and argv required")
label, argv = sys.argv[1], sys.argv[2:]
require(label.replace("_", "").isalnum(), "unsafe label")
out = root / "process_receipts" / label
out.mkdir(exist_ok=False)
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
p = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
try:
    stdout, stderr = p.communicate(timeout=60)
except subprocess.TimeoutExpired:
    p.kill()
    stdout, stderr = p.communicate()
    raise RuntimeError("process exceeded 60-second deadline")
require(len(stdout) <= 131072 and len(stderr) <= 131072, "unexpected large output")
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
pins = {}
for name, body in (("stdout.txt", stdout), ("stderr.txt", stderr)):
    (out / name).write_bytes(body)
    pins[name] = {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
receipt = {"schema": "pr110-geometric-actual-process/v1", "operator_pid": os.getpid(),
           "child_pid": p.pid, "argv": argv, "cwd": str(root), "started_utc": start,
           "finished_utc": end, "elapsed_seconds": time.monotonic() - t0,
           "exit_code": p.returncode, "deadline_seconds": 60, "reaped": True,
           "full_output_pins": pins}
(out / "RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
sys.stdout.write(stdout.decode("utf-8", errors="replace"))
sys.stderr.write(stderr.decode("utf-8", errors="replace"))
sys.exit(p.returncode)

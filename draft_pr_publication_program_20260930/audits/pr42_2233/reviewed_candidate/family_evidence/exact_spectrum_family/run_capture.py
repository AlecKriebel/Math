#!/usr/bin/env python3
"""Preserve actual private-process source hashes, clocks, PID, and streams."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
def utc(): return datetime.now(timezone.utc).isoformat()
label, target = sys.argv[1:3]
dest = HERE / "runs" / label
dest.mkdir(parents=True, exist_ok=False)
src = HERE / target
(dest / "source.py").write_bytes(src.read_bytes())
start, tick = utc(), time.monotonic_ns()
process = subprocess.Popen([sys.executable, str(src)], cwd=HERE,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
meta = {"start_utc": start, "finish_utc": utc(), "elapsed_ns": time.monotonic_ns()-tick,
        "pid": process.pid, "argv": [sys.executable, str(src)], "cwd": str(HERE),
        "returncode": process.returncode, "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
        "stdout_bytes": len(stdout), "stderr_bytes": len(stderr),
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr).hexdigest()}
(dest / "stdout.txt").write_bytes(stdout)
(dest / "stderr.txt").write_bytes(stderr)
(dest / "metadata.json").write_text(json.dumps(meta, indent=2)+"\n")
print(json.dumps(meta, indent=2))
sys.exit(process.returncode)

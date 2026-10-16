#!/usr/bin/env python3
"""Repeat a primary fetch with actual nested PID and stream provenance."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
url = "https://www.erdosproblems.com/653"
start = datetime.now(timezone.utc).isoformat()
tick = time.monotonic_ns()
cmd = ["curl", "--location", "--show-error", "--dump-header",
       str(HERE / "sources/primary653_refetch.headers"), url]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
body, stderr = process.communicate()
(HERE / "sources/primary653_refetch.html").write_bytes(body)
sys.stderr.buffer.write(stderr)
print(json.dumps({"url": url, "start_utc": start,
    "finish_utc": datetime.now(timezone.utc).isoformat(), "elapsed_ns":time.monotonic_ns()-tick,
    "curl_pid": process.pid, "curl_argv": cmd, "curl_returncode": process.returncode,
    "body_bytes": len(body), "body_sha256": hashlib.sha256(body).hexdigest(),
    "stderr_bytes": len(stderr), "stderr_sha256": hashlib.sha256(stderr).hexdigest()}, indent=2))
sys.exit(process.returncode)

"""Capture exactly one own passive-checker invocation and literal streams."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
assert ROOT.name == "d4-canonical-potential-editorial-fact-sol-20261117"
assert all(not (ROOT / name).exists() for name in ("reader.stdout.txt", "reader.stderr.txt", "reader.exit.txt", "READER_RUN.json"))
argv = [sys.executable, str(ROOT / "data_check.py")]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
clock_start = time.monotonic()
result = subprocess.run(argv, cwd=ROOT, capture_output=True)
finished = datetime.datetime.now(datetime.timezone.utc).isoformat()
elapsed = time.monotonic() - clock_start
(ROOT / "reader.stdout.txt").write_bytes(result.stdout)
(ROOT / "reader.stderr.txt").write_bytes(result.stderr)
(ROOT / "reader.exit.txt").write_text(str(result.returncode) + "\n")
receipt = {"argv": argv, "cwd": str(ROOT), "UTC_start": started, "UTC_end": finished,
           "elapsed_seconds": elapsed, "exit": result.returncode, "attempt_count": 1,
           "repair_or_retry_count": 0,
           "checker_SHA256": hashlib.sha256((ROOT / "data_check.py").read_bytes()).hexdigest(),
           "stdout_bytes": len(result.stdout), "stdout_SHA256": hashlib.sha256(result.stdout).hexdigest(),
           "stderr_bytes": len(result.stderr), "stderr_SHA256": hashlib.sha256(result.stderr).hexdigest(),
           "native_scientific_source_producer_helper_execution": 0,
           "W_Git_network_Sheet_UI_stage_deploy_redirect_operations": 0}
(ROOT / "READER_RUN.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
sys.exit(result.returncode)

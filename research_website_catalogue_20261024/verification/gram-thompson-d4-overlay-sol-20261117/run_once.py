"""Capture exactly one own stage-builder invocation and preserve literal failure."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
assert ROOT.name == "gram-thompson-d4-overlay-sol-20261117"
assert all(not (ROOT / name).exists() for name in ("builder.stdout.txt", "builder.stderr.txt", "builder.exit.txt", "BUILDER_RUN.json"))
argv = [sys.executable, str(ROOT / "build_overlay.py")]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
clock_start = time.monotonic()
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
result = subprocess.run(argv, cwd=ROOT, capture_output=True, env=environment)
finished = datetime.datetime.now(datetime.timezone.utc).isoformat()
elapsed = time.monotonic() - clock_start
(ROOT / "builder.stdout.txt").write_bytes(result.stdout)
(ROOT / "builder.stderr.txt").write_bytes(result.stderr)
(ROOT / "builder.exit.txt").write_text(str(result.returncode) + "\n")
receipt = {"argv": argv, "cwd": str(ROOT), "UTC_start": started, "UTC_end": finished, "elapsed_seconds": elapsed,
           "exit": result.returncode, "attempt_count": 1, "repair_or_retry_count": 0,
           "environment_change": {"PYTHONDONTWRITEBYTECODE": "1"},
           "builder_SHA256": hashlib.sha256((ROOT / "build_overlay.py").read_bytes()).hexdigest(),
           "stdout_bytes": len(result.stdout), "stdout_SHA256": hashlib.sha256(result.stdout).hexdigest(),
           "stderr_bytes": len(result.stderr), "stderr_SHA256": hashlib.sha256(result.stderr).hexdigest(),
           "W_mutations_Git_network_Sheet_scientific_oldhelper_server_install_deploy_operations": 0}
(ROOT / "BUILDER_RUN.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
sys.exit(result.returncode)

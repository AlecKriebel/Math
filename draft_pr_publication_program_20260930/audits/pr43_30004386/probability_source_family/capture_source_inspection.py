"""Prelaunch operator for a genuine, scoped read-only source-inspection process."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

here = Path(__file__).resolve().parent
source = here / "inspect_sources_and_snapshot.py"
label = sys.argv[1] if len(sys.argv) > 1 else "source_inspection"
command = [sys.executable, str(source), label]
started = datetime.now(timezone.utc).isoformat()
source_digest = hashlib.sha256(source.read_bytes()).hexdigest()
process = subprocess.Popen(command, cwd=here, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate()
for name, data in [(label + ".stdout.txt", out), (label + ".stderr.txt", err)]:
    (here / "captures" / name).write_bytes(data)
receipt = {"schema": "genuine-readonly-source-inspection-capture/v1",
           "operator_pid": os.getpid(), "child_pid": process.pid, "command": command,
           "started_utc": started, "ended_utc": datetime.now(timezone.utc).isoformat(),
           "returncode": process.returncode, "prelaunch_source_sha256": source_digest,
           "postlaunch_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
           "stdout_sha256": hashlib.sha256(out).hexdigest(), "stderr_sha256": hashlib.sha256(err).hexdigest(),
           "stdout_bytes": len(out), "stderr_bytes": len(err),
           "scope": "Actual process capture for own source predicates, never candidate helper execution."}
(here / "captures" / (label + "_capture.json")).write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
if process.returncode:
    sys.exit(process.returncode)

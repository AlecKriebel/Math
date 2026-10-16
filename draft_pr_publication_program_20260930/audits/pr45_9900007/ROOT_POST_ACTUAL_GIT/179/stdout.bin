#!/usr/bin/env python3
"""Independent operator recording prelaunch source, PID, UTC and complete streams."""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent
source = pathlib.Path(sys.argv[1]).resolve()
name = sys.argv[2]
run = root / "actual_runs" / name
run.mkdir(exist_ok=False)
stamp = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
body = source.read_bytes()
operator = pathlib.Path(__file__).resolve().read_bytes()
(run / "prelaunch_source.py").write_bytes(body)
(run / "prelaunch_operator.py").write_bytes(operator)
metadata = {
    "operator_pid": os.getpid(), "prelaunch_utc": stamp(),
    "source_path": str(source), "source_sha256": hashlib.sha256(body).hexdigest(),
    "operator_sha256": hashlib.sha256(operator).hexdigest(),
    "argv": [sys.executable, "-B", str(source), *sys.argv[3:]],
    "cwd": str(root), "publication_allowed": True,
}
(run / "PRELAUNCH.json").write_text(json.dumps(metadata, indent=2) + "\n")
with (run / "stdout.bin").open("wb") as out, (run / "stderr.bin").open("wb") as err:
    proc = subprocess.Popen(metadata["argv"], cwd=root, stdout=out, stderr=err)
    metadata["child_pid"] = proc.pid
    metadata["launch_utc"] = stamp()
    (run / "LAUNCHED.json").write_text(json.dumps(metadata, indent=2) + "\n")
    metadata["exit_code"] = proc.wait()
metadata["end_utc"] = stamp()
for stream in ("stdout", "stderr"):
    data = (run / (stream + ".bin")).read_bytes()
    metadata[stream + "_bytes"] = len(data)
    metadata[stream + "_sha256"] = hashlib.sha256(data).hexdigest()
(run / "CAPTURE.json").write_text(json.dumps(metadata, indent=2) + "\n")
print(json.dumps(metadata, indent=2))
sys.exit(metadata["exit_code"])

#!/usr/bin/env python3
"""Capture real native command evidence within this review namespace."""
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

def native_utc():
    command = ["/bin/date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors="replace"))
    return result.stdout.decode().strip()

def run(label, argv):
    receipts = ROOT / "native_receipts"
    receipts.mkdir(exist_ok=True)
    started = native_utc()
    before = time.monotonic_ns()
    metadata = {"label": label, "argv": argv, "cwd": str(ROOT),
                "utc_start": started, "clock_argv": ["/bin/date", "-u", "+%Y-%m-%dT%H:%M:%SZ"],
                "stdout_file": label + ".stdout", "stderr_file": label + ".stderr",
                "state": "started"}
    meta_path = receipts / (label + ".json")
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n")
    with (receipts / (label + ".stdout")).open("wb") as out, (receipts / (label + ".stderr")).open("wb") as err:
        completed = subprocess.run(argv, cwd=ROOT, stdout=out, stderr=err, check=False)
    metadata.update({"utc_end": native_utc(), "elapsed_monotonic_ns": time.monotonic_ns()-before,
                     "exit_status": completed.returncode, "state": "completed"})
    meta_path.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))
    print("--- complete stdout ---")
    print((receipts / (label + ".stdout")).read_text(errors="replace"), end="")
    print("--- complete stderr ---")
    print((receipts / (label + ".stderr")).read_text(errors="replace"), end="")
    return completed.returncode

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("usage: capture_native.py LABEL COMMAND [ARG ...]")
    raise SystemExit(run(sys.argv[1], sys.argv[2:]))

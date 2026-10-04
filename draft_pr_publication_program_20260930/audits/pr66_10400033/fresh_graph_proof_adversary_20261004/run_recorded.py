#!/usr/bin/env python3
"""Run an explicitly supplied child command and preserve its complete receipt."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    label = sys.argv[1]
    assert sys.argv[2] == "--"
    argv = sys.argv[3:]
    root = Path(__file__).resolve().parent
    assert label and "/" not in label and ".." not in label
    stdout_path = root / (label + ".stdout")
    stderr_path = root / (label + ".stderr")
    receipt_path = root / (label + ".receipt.json")
    if any(p.exists() for p in [stdout_path, stderr_path, receipt_path]):
        raise SystemExit("Refusing to replace an existing recorded run")
    started = utc()
    process = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = process.pid
    stdout, stderr = process.communicate()
    ended = utc()
    stdout_path.write_bytes(stdout)
    stderr_path.write_bytes(stderr)
    receipt = {
        "argv": argv,
        "pid": pid,
        "cwd": str(root),
        "start_utc": started,
        "end_utc": ended,
        "exit_code": process.returncode,
        "stdout_file": stdout_path.name,
        "stdout_bytes": len(stdout),
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stderr_file": stderr_path.name,
        "stderr_bytes": len(stderr),
        "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
    }
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(stdout.decode(), end="")
    if stderr:
        print(stderr.decode(), end="", file=sys.stderr)
    print("RECEIPT " + json.dumps(receipt, sort_keys=True))
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())

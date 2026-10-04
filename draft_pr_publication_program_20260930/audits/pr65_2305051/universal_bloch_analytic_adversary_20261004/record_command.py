#!/usr/bin/env python3
"""Run an audit command, preserving real child PID, UTC times, exit and streams."""
import datetime as dt
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
COMMANDS = ROOT / "commands"
COMMANDS.mkdir(exist_ok=True)
label, *argv = sys.argv[1:]
if not argv:
    raise SystemExit("Usage: record_command.py LABEL command arg...")
started = dt.datetime.now(dt.timezone.utc).isoformat()
with (COMMANDS / f"{label}.stdout").open("wb") as stdout, (COMMANDS / f"{label}.stderr").open("wb") as stderr:
    p = subprocess.Popen(argv, cwd="/Users/alec/Documents/Math", stdout=stdout, stderr=stderr)
    pid = p.pid
    code = p.wait()
ended = dt.datetime.now(dt.timezone.utc).isoformat()
record = {"label": label, "argv": argv, "cwd": "/Users/alec/Documents/Math", "pid": pid,
          "started_utc": started, "ended_utc": ended, "exit_code": code,
          "stdout": f"commands/{label}.stdout", "stderr": f"commands/{label}.stderr"}
with (ROOT / "ACTUAL_COMMANDS.jsonl").open("a") as f:
    f.write(json.dumps(record, sort_keys=True) + "\n")
print(json.dumps(record, sort_keys=True))
raise SystemExit(code)

#!/usr/bin/env python3
"""Bounded private preparation capture. No publication/native/Git mutation authority."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(b):
    return hashlib.sha256(b).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def identity(path):
    b = path.read_bytes()
    return {"path": str(path), "bytes": len(b), "sha256": digest(b)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--cwd", required=True)
    p.add_argument("--source", action="append", default=[])
    p.add_argument("argv", nargs=argparse.REMAINDER)
    a = p.parse_args()
    if not a.name or any(x not in "abcdefghijklmnopqrstuvwxyz0123456789_-" for x in a.name):
        raise ValueError("one simple capture name required")
    argv = a.argv[1:] if a.argv[:1] == ["--"] else a.argv
    if not argv:
        raise ValueError("literal argv required")
    cwd = Path(a.cwd).resolve(strict=True)
    captures = ROOT / "captures"
    captures.mkdir(exist_ok=True)
    cap = captures / a.name
    cap.mkdir()  # Existing failed captures must never be overwritten.
    self_path = Path(__file__).resolve()
    shutil.copyfile(self_path, cap / "OPERATOR_PRELAUNCH.py")
    sources = []
    for i, s in enumerate(a.source):
        original = Path(s).resolve(strict=True)
        if not original.is_file():
            raise ValueError("source must be a regular readable file")
        saved = cap / ("SOURCE_PRELAUNCH_%02d" % i + original.suffix)
        shutil.copyfile(original, saved)
        original_id, saved_id = identity(original), identity(saved)
        assert original_id["bytes"] == saved_id["bytes"] and original_id["sha256"] == saved_id["sha256"]
        sources.append({"original": original_id, "saved": saved_id})
    begin = {"schema": "pr51-private-command-prelaunch/v1", "utc": utc(),
             "wrapper_pid": os.getpid(), "wrapper_argv": sys.argv, "argv": argv,
             "cwd": str(cwd), "operator": identity(cap / "OPERATOR_PRELAUNCH.py"),
             "sources": sources, "child_pid": None, "completed": False}
    write_json(cap / "PRELAUNCH.json", begin)
    started_monotonic = time.monotonic()
    try:
        child = subprocess.Popen(argv, cwd=str(cwd), stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        out, err = b"", traceback.format_exc().encode("utf-8")
        (cap / "STDOUT.bin").write_bytes(out)
        (cap / "STDERR.bin").write_bytes(err)
        write_json(cap / "COMPLETE.json", {
            "schema": "pr51-private-command-launch-failure/v1", "utc": utc(),
            "child_pid": None, "wrapper_pid": os.getpid(), "argv": argv,
            "cwd": str(cwd), "completed": True, "child_started": False,
            "exit_code": None, "wrapper_exit_code": 127,
            "elapsed_seconds": time.monotonic() - started_monotonic,
            "prelaunch": identity(cap / "PRELAUNCH.json"),
            "stdout": identity(cap / "STDOUT.bin"),
            "stderr": identity(cap / "STDERR.bin")})
        print(json.dumps({"capture": str(cap), "child_pid": None,
                          "child_started": False, "wrapper_exit_code": 127}))
        return 127
    started = {"schema": "pr51-private-command-started/v1", "utc": utc(),
               "child_pid": child.pid, "argv": argv, "cwd": str(cwd)}
    write_json(cap / "STARTED.json", started)
    out, err = child.communicate()
    (cap / "STDOUT.bin").write_bytes(out)
    (cap / "STDERR.bin").write_bytes(err)
    completed = {"schema": "pr51-private-command-completed/v1", "utc": utc(),
                 "child_pid": child.pid, "argv": argv, "cwd": str(cwd),
                 "exit_code": child.returncode, "completed": True,
                 "elapsed_seconds": time.monotonic() - started_monotonic,
                 "prelaunch": identity(cap / "PRELAUNCH.json"),
                 "started": identity(cap / "STARTED.json"),
                 "stdout": identity(cap / "STDOUT.bin"),
                 "stderr": identity(cap / "STDERR.bin")}
    write_json(cap / "COMPLETE.json", completed)
    print(json.dumps({"capture": str(cap), "pid": child.pid,
                      "exit_code": child.returncode, "completed": True,
                      "stdout_bytes": len(out), "stderr_bytes": len(err)}))
    return child.returncode


if __name__ == "__main__":
    sys.exit(main())

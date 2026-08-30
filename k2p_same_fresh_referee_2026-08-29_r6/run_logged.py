#!/usr/bin/env python3
"""Run one referee command and record byte-exact output and resource metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("missing command after --")

    args.log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = args.log_dir / f"{args.name}.stdout"
    stderr_path = args.log_dir / f"{args.name}.stderr"
    report_path = args.log_dir / f"{args.name}.json"
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    timed_out = False
    try:
        result = subprocess.run(
            command,
            cwd=args.cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.timeout,
            check=False,
        )
        returncode = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        returncode = 124
        stdout = error.stdout or b""
        stderr = error.stderr or b""
    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    stdout_path.write_bytes(stdout)
    stderr_path.write_bytes(stderr)
    report = {
        "schema": "k2p-independent-referee-command-v1",
        "name": args.name,
        "cwd": str(args.cwd.resolve()),
        "command": command,
        "started_at_utc": started_at,
        "elapsed_seconds": round(elapsed, 6),
        "returncode": returncode,
        "timed_out": timed_out,
        "maximum_resident_set_size_bytes": int(usage.ru_maxrss),
        "stdout_bytes": len(stdout),
        "stdout_sha256": digest(stdout),
        "stderr_bytes": len(stderr),
        "stderr_sha256": digest(stderr),
        "combined_output_sha256": digest(stdout + stderr),
        "pythondontwritebytecode": environment["PYTHONDONTWRITEBYTECODE"],
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True), flush=True)
    if stdout:
        print(stdout[-4000:].decode("utf-8", "replace"), end="")
    if stderr:
        print(stderr[-4000:].decode("utf-8", "replace"), end="")
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())

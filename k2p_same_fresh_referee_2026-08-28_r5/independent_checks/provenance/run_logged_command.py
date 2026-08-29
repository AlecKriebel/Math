#!/usr/bin/env python3
"""Run one command once and retain byte-exact output plus execution metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import time
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--stderr", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("missing command after --")

    for path in (args.stdout, args.stderr, args.metadata):
        path.parent.mkdir(parents=True, exist_ok=True)
    started_wall = time.time()
    started_mono = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    result = subprocess.run(
        command,
        cwd=args.cwd,
        env=os.environ.copy(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    elapsed = time.perf_counter() - started_mono
    args.stdout.write_bytes(result.stdout)
    args.stderr.write_bytes(result.stderr)
    metadata = {
        "schema": "k2p-r5-command-execution-v1",
        "name": args.name,
        "command": command,
        "cwd": str(args.cwd.resolve()),
        "started_unix": started_wall,
        "wall_seconds": round(elapsed, 6),
        "exit_status": result.returncode,
        "stdout_bytes": len(result.stdout),
        "stdout_sha256": sha256(result.stdout),
        "stderr_bytes": len(result.stderr),
        "stderr_sha256": sha256(result.stderr),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "rusage_children": {
            "max_rss": after.ru_maxrss,
            "max_rss_unit": "bytes" if platform.system() == "Darwin" else "KiB",
            "user_seconds": round(after.ru_utime - before.ru_utime, 6),
            "system_seconds": round(after.ru_stime - before.ru_stime, 6),
        },
    }
    encoded = json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    args.metadata.write_text(encoded, encoding="utf-8")
    print(json.dumps(metadata, sort_keys=True))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

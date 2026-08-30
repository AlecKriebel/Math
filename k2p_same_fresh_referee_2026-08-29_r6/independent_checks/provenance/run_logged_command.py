#!/usr/bin/env python3
"""Run one command and record exact timing, hashes, status, and resource use."""

from __future__ import annotations

import argparse
import hashlib
import json
import resource
import subprocess
import time
from pathlib import Path


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("missing command")

    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.time()
    result = subprocess.run(
        command,
        cwd=args.cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    elapsed = time.time() - started
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    # macOS ru_maxrss is bytes.  It is a high-water mark for all children of
    # this runner, so it is an upper bound when earlier children existed.
    record = {
        "schema": "k2p-r6-command-record-v1",
        "command": command,
        "cwd": str(args.cwd.resolve()),
        "exit_status": result.returncode,
        "wall_seconds": elapsed,
        "stdout_bytes": len(result.stdout),
        "stdout_sha256": digest(result.stdout),
        "stderr_bytes": len(result.stderr),
        "stderr_sha256": digest(result.stderr),
        "maximum_resident_set_size_bytes": max(
            int(before.ru_maxrss), int(after.ru_maxrss)
        ),
        "started_unix": started,
    }
    unsigned = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    record["payload_sha256"] = digest(unsigned)
    args.record.parent.mkdir(parents=True, exist_ok=True)
    args.record.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    args.record.with_suffix(args.record.suffix + ".stdout").write_bytes(result.stdout)
    args.record.with_suffix(args.record.suffix + ".stderr").write_bytes(result.stderr)
    print(json.dumps(record, sort_keys=True))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

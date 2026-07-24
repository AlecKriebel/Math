#!/usr/bin/env python3
"""Run one command only after a free-space gate, with a file-size hard limit."""

from __future__ import annotations

import argparse
import os
import resource
from pathlib import Path


def available_bytes(path: Path) -> int:
    stats = os.statvfs(path)
    return stats.f_bavail * stats.f_frsize


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--filesystem", type=Path, required=True)
    parser.add_argument("--minimum-free-bytes", type=int, required=True)
    parser.add_argument("--maximum-file-bytes", type=int, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command and args.command[0] == "--":
        args.command = args.command[1:]
    if not args.filesystem.exists():
        parser.error("--filesystem must exist")
    if args.minimum_free_bytes <= 0 or args.maximum_file_bytes <= 0:
        parser.error("byte limits must be positive")
    if not args.command:
        parser.error("a command is required after --")
    observed = available_bytes(args.filesystem)
    if observed < args.minimum_free_bytes:
        parser.error(
            "free-space gate failed: "
            f"{observed} < {args.minimum_free_bytes} bytes"
        )
    resource.setrlimit(
        resource.RLIMIT_FSIZE,
        (args.maximum_file_bytes, args.maximum_file_bytes),
    )
    environment = os.environ.copy()
    environment.update(
        {
            "RAMSEY55_GATE_AVAILABLE_BYTES": str(observed),
            "RAMSEY55_GATE_MINIMUM_FREE_BYTES": str(args.minimum_free_bytes),
            "RAMSEY55_GATE_MAXIMUM_FILE_BYTES": str(args.maximum_file_bytes),
        }
    )
    os.execvpe(args.command[0], args.command, environment)
    raise AssertionError("os.execvpe unexpectedly returned")


if __name__ == "__main__":
    raise SystemExit(main())

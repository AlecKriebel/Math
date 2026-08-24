#!/usr/bin/env python3
"""Build/check the byte-stable principal-D+ theorem release lock."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from release_common import (
    HERE,
    ReleaseFailure,
    lock_payload,
    validate_runtime_environment,
)


LOCK = HERE / "RELEASE_LOCK.json"


def pretty_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    if not __debug__:
        raise SystemExit("FINAL_RELEASE_LOCK_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    validate_runtime_environment()
    payload = lock_payload()
    expected = pretty_bytes(payload)
    if args.require_ready and not payload["promotion_ready"]:
        raise SystemExit(
            "FINAL_RELEASE_LOCK_NOT_READY:"
            + json.dumps(payload["blockers"], sort_keys=True)
        )
    if args.check:
        if not LOCK.is_file() or LOCK.read_bytes() != expected:
            raise SystemExit("FINAL_RELEASE_LOCK_DRIFT")
        print("K2P_FINAL_RELEASE_LOCK_CHECK_PASS")
    else:
        temporary = LOCK.with_name(f"{LOCK.name}.tmp.{os.getpid()}")
        with temporary.open("wb") as handle:
            handle.write(expected)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, LOCK)
        print("K2P_FINAL_RELEASE_LOCK_WRITTEN")
    print(
        json.dumps(
            {
                "payload_sha256": payload["payload_sha256"],
                "promotion_ready": payload["promotion_ready"],
                "blockers": payload["blockers"],
                "locked_files": len(payload["files"]),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReleaseFailure as error:
        raise SystemExit(f"FINAL_RELEASE_LOCK_FAIL:{error}") from error

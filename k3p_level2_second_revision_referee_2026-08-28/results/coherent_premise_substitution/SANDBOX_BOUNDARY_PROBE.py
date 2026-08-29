#!/usr/bin/env python3
"""Reviewer-owned negative probes for the credited substitution sandbox."""

from __future__ import annotations

import errno
import hashlib
import os
from pathlib import Path
import socket
import sys


ROOT = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_second_revision_referee_2026-08-28"
)
TEST_ROOT = ROOT / "tmp/coherent-premise-substitution-sandboxed.QeuPXv"
SOURCE_FILE = (
    ROOT
    / "package_copy/proof_package/cut_recovery/strong_crossbridge/"
    "global_transfer/build_global_transfer.py"
)
SOURCE_WRITE_PROBE = ROOT / "package_copy/.coherent_substitution_write_probe"
ACTIVE_REVIEW_DIRECTORY = ROOT / "package_copy/review_runs"
SIBLING_FILE = Path("/Users/alec/Documents/Math/AGENTS.md")
CREDENTIAL_DIRECTORY = Path("/Users/alec/.ssh")


def require_permission_denied(action, label: str) -> None:
    try:
        action()
    except PermissionError as error:
        if error.errno not in {errno.EACCES, errno.EPERM}:
            raise AssertionError((label, "wrong errno", error.errno)) from error
        print(f"{label}_DENIED errno={error.errno}")
        return
    except OSError as error:
        raise AssertionError((label, "non-permission failure", error.errno)) from error
    raise AssertionError((label, "unexpectedly allowed"))


def environment_probe() -> None:
    sensitive_fragments = (
        "TOKEN", "SECRET", "PASSWORD", "PASSWD", "COOKIE", "CREDENTIAL",
        "AWS_", "GITHUB_", "GH_", "OPENAI_", "ANTHROPIC_", "SSH_",
    )
    names = sorted(os.environ)
    leaked = [name for name in names if any(part in name.upper() for part in sensitive_fragments)]
    if leaked:
        raise AssertionError(("credential-like environment names", leaked))
    print("CLEAN_ENVIRONMENT names=" + ",".join(names))


def network_probe() -> None:
    def connect() -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
            stream.settimeout(1.0)
            stream.connect(("127.0.0.1", 9))

    require_permission_denied(connect, "NETWORK")


def credential_probe() -> None:
    require_permission_denied(lambda: os.listdir(CREDENTIAL_DIRECTORY), "CREDENTIAL_READ")


def sibling_probe() -> None:
    require_permission_denied(lambda: SIBLING_FILE.read_bytes(), "SIBLING_READ")


def active_review_probe() -> None:
    require_permission_denied(
        lambda: os.listdir(ACTIVE_REVIEW_DIRECTORY), "ACTIVE_REVIEW_READ"
    )


def source_read_probe() -> None:
    digest = hashlib.sha256(SOURCE_FILE.read_bytes()).hexdigest()
    expected = "d99ae6579fbacf18c713f0dac3045e49ccc93a42a8bed2f6861a3ad34f8a273b"
    if digest != expected:
        raise AssertionError(("source hash", digest, expected))
    print(f"SOURCE_READ_ALLOWED sha256={digest}")


def source_write_probe() -> None:
    require_permission_denied(
        lambda: SOURCE_WRITE_PROBE.write_text("forbidden\n", encoding="utf-8"),
        "SOURCE_WRITE",
    )


def disposable_write_probe() -> None:
    path = TEST_ROOT / "allowed_write_probe.txt"
    path.write_text("allowed\n", encoding="utf-8")
    if path.read_text(encoding="utf-8") != "allowed\n":
        raise AssertionError("disposable write round trip")
    print("DISPOSABLE_WRITE_ALLOWED")


MODES = {
    "environment": environment_probe,
    "network": network_probe,
    "credential": credential_probe,
    "sibling": sibling_probe,
    "active-review": active_review_probe,
    "source-read": source_read_probe,
    "source-write": source_write_probe,
    "disposable-write": disposable_write_probe,
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in MODES:
        print("usage: SANDBOX_BOUNDARY_PROBE.py MODE", file=sys.stderr)
        return 64
    MODES[sys.argv[1]]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

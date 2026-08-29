#!/usr/bin/env python3
"""Launch one package review phase with a clean environment and hard lock.

This trusted referee-side wrapper is outside the reviewed package.  It gives
the package runner only an explicit non-secret environment, places it inside
the default-deny macOS sandbox, prevents a concurrent second launch, and
terminates the complete descendant tree if the supervisor is interrupted.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


ROOT = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_second_revision_referee_2026-08-28"
)
PACKAGE = ROOT / "package_copy"
PROFILE = ROOT / "logs/offline_credential_free.sb"
PYTHON = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_identifiability_final/.venv/bin/python"
)
RUNNER = PACKAGE / "referee_tools/run_active_verifiers.py"
LOCK = ROOT / "execution/active_review.lock"


def process_table() -> dict[int, list[int]]:
    completed = subprocess.run(
        ["/bin/ps", "-axo", "pid=,ppid="],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
    )
    children: dict[int, list[int]] = {}
    for line in completed.stdout.splitlines():
        pid_text, parent_text = line.split()
        children.setdefault(int(parent_text), []).append(int(pid_text))
    return children


def descendants(root_pid: int) -> list[int]:
    table = process_table()
    result: list[int] = []

    def visit(pid: int) -> None:
        for child in table.get(pid, []):
            visit(child)
            result.append(child)

    visit(root_pid)
    return result


def signal_tree(root_pid: int, sig: int) -> list[int]:
    targets = descendants(root_pid) + [root_pid]
    signalled: list[int] = []
    for pid in targets:
        try:
            os.kill(pid, sig)
            signalled.append(pid)
        except ProcessLookupError:
            pass
    return signalled


def kill_survivors(pids: list[int]) -> list[int]:
    killed: list[int] = []
    for pid in pids:
        try:
            os.kill(pid, 0)
            os.kill(pid, signal.SIGKILL)
            killed.append(pid)
        except ProcessLookupError:
            pass
    return killed


def clean_environment(mode: str) -> dict[str, str]:
    home = PACKAGE / "review_runs/empty_home"
    temporary = PACKAGE / "review_runs/supervisor_tmp"
    home.mkdir(parents=True, exist_ok=True)
    temporary.mkdir(parents=True, exist_ok=True)
    environment = {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "HOME": str(home),
        "TMPDIR": str(temporary),
        "__CF_USER_TEXT_ENCODING": "0x1F5:0:0",
    }
    if mode in {"regenerate", "all"}:
        environment["K3P_REFEREE_CONFIRM_REGENERATION"] = "YES"
    return environment


def acquire_lock(mode: str) -> None:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(LOCK, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump({"pid": os.getpid(), "mode": mode}, handle, sort_keys=True)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("plan", "verify", "regenerate", "all"))
    arguments = parser.parse_args()
    mode = arguments.mode
    try:
        acquire_lock(mode)
    except FileExistsError:
        print(f"refusing concurrent review; lock exists: {LOCK}", file=sys.stderr)
        return 73

    process: subprocess.Popen[str] | None = None
    interrupted = False

    def interrupt(_number: int, _frame: object) -> None:
        nonlocal interrupted
        interrupted = True
        raise KeyboardInterrupt

    old_handlers = {
        number: signal.signal(number, interrupt)
        for number in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
    }
    try:
        command = [
            "/usr/bin/sandbox-exec",
            "-f",
            str(PROFILE),
            str(PYTHON),
            str(RUNNER),
            "--package-root",
            str(PACKAGE),
            "--python",
            str(PYTHON),
            "--mode",
            mode,
        ]
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=clean_environment(mode),
            text=True,
            start_new_session=True,
        )
        return process.wait()
    except KeyboardInterrupt:
        if process is not None and process.poll() is None:
            terminated = signal_tree(process.pid, signal.SIGTERM)
            time.sleep(0.5)
            killed = kill_survivors(terminated)
            print(
                json.dumps(
                    {
                        "status": "INTERRUPTED",
                        "term_signalled": terminated,
                        "kill_signalled": killed,
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
        return 130
    finally:
        for number, handler in old_handlers.items():
            signal.signal(number, handler)
        try:
            LOCK.unlink()
        except FileNotFoundError:
            if not interrupted:
                raise


if __name__ == "__main__":
    raise SystemExit(main())

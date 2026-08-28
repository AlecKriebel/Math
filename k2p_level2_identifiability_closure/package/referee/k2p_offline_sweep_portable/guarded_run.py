#!/usr/bin/env python3
"""Launch the sweep with disk/RSS gates and resumable fail-safe termination."""
from __future__ import annotations

if not __debug__:
    raise SystemExit("K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN")

import argparse
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

GIB = 1024 ** 3


class ResourceLimit(RuntimeError):
    pass


def descendant_rss_bytes(root_pid: int) -> int:
    result = subprocess.run(
        ["ps", "-axo", "pid=,ppid=,rss="], text=True, capture_output=True, check=True
    )
    children: dict[int, list[int]] = {}
    rss: dict[int, int] = {}
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) != 3:
            continue
        pid, parent, kib = map(int, fields)
        children.setdefault(parent, []).append(pid)
        rss[pid] = kib * 1024
    stack, seen = [root_pid], set()
    while stack:
        pid = stack.pop()
        if pid in seen:
            continue
        seen.add(pid)
        stack.extend(children.get(pid, ()))
    return sum(rss.get(pid, 0) for pid in seen)


def stop_group(process: subprocess.Popen, reason: str) -> None:
    print(f"RESOURCE_GUARD_STOP: {reason}", file=sys.stderr, flush=True)
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def main() -> None:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("output_root", type=Path)
    parser.add_argument("--python", default=os.environ.get("PYTHON_BIN", "python3"))
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument("--min-start-free-gib", type=float, default=20.0)
    parser.add_argument("--min-runtime-free-gib", type=float, default=10.0)
    parser.add_argument("--max-rss-gib", type=float)
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--nice", type=int, default=10)
    parser.add_argument("--skip-package-verify", action="store_true")
    args = parser.parse_args()

    output_root = args.output_root.resolve()
    output_root.parent.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(output_root.parent).free
    if free < args.min_start_free_gib * GIB:
        raise SystemExit(
            f"RESOURCE_GUARD_PREFLIGHT_FAIL: {free/GIB:.2f} GiB free; "
            f"requires {args.min_start_free_gib:.2f} GiB"
        )
    max_rss_gib = args.max_rss_gib
    if max_rss_gib is None:
        max_rss_gib = 3.5 if args.workers == 1 else 5.0

    environment = os.environ.copy()
    environment.update({
        "PYTHON_BIN": args.python,
        "K2P_WORKERS": str(args.workers),
        "PYTHONHASHSEED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
    })
    if not args.skip_package_verify:
        subprocess.run([
            "nice", "-n", str(args.nice), args.python, str(root / "verify_package.py"),
            "--skip-smoke", "--skip-mutations", "--skip-prepared-audit",
        ], env=environment, check=True)
    command = ["nice", "-n", str(args.nice), "bash", str(root / "run_all_sources.sh"), str(output_root)]
    print("RESOURCE_GUARD_START " + " ".join(command), flush=True)
    process = subprocess.Popen(command, env=environment, start_new_session=True)
    previous_handlers = {}

    def guardian_signal(signum, _frame):
        raise KeyboardInterrupt(f"guardian received signal {signum}")

    for signum in (signal.SIGTERM, signal.SIGHUP):
        previous_handlers[signum] = signal.signal(signum, guardian_signal)
    try:
        while process.poll() is None:
            free = shutil.disk_usage(output_root.parent).free
            if free < args.min_runtime_free_gib * GIB:
                raise ResourceLimit(
                    f"disk free {free/GIB:.2f} GiB below {args.min_runtime_free_gib:.2f} GiB"
                )
            rss = descendant_rss_bytes(process.pid)
            if rss > max_rss_gib * GIB:
                raise ResourceLimit(f"sweep RSS {rss/GIB:.2f} GiB above {max_rss_gib:.2f} GiB")
            time.sleep(args.poll_seconds)
    except ResourceLimit as exc:
        stop_group(process, str(exc))
        raise SystemExit(75)
    except KeyboardInterrupt:
        stop_group(process, "guardian interrupted")
        raise
    finally:
        for signum, previous in previous_handlers.items():
            signal.signal(signum, previous)
    if process.returncode:
        raise SystemExit(process.returncode)
    print("RESOURCE_GUARD_COMPLETE", flush=True)


if __name__ == "__main__":
    main()

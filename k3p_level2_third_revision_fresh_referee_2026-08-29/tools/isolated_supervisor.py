#!/usr/bin/env python3
"""Launch exactly one package review phase inside the referee sandbox."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import threading
import time


AUDIT = Path(__file__).resolve().parents[1]
PACKAGE = AUDIT / "package_copy"
PROFILE = AUDIT / "logs/offline_credential_free.sb"
PYTHON = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_identifiability_final/.venv/bin/python"
)
RUNNER = PACKAGE / "referee_tools/run_active_verifiers.py"
LOCK = AUDIT / "execution/active_review.lock"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(root: Path, *, exclude_top: set[str] | None = None) -> dict:
    excluded = exclude_top or set()
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if relative.split("/", 1)[0] in excluded:
            continue
        metadata = path.lstat()
        mode = format(stat.S_IMODE(metadata.st_mode), "04o")
        if stat.S_ISLNK(metadata.st_mode):
            row = {"path": relative, "type": "symlink", "mode": mode,
                   "target": os.readlink(path)}
        elif stat.S_ISDIR(metadata.st_mode):
            row = {"path": relative, "type": "directory", "mode": mode}
        elif stat.S_ISREG(metadata.st_mode):
            row = {"path": relative, "type": "file", "mode": mode,
                   "bytes": metadata.st_size, "sha256": sha256_file(path)}
        else:
            raise RuntimeError(("unexpected filesystem object", relative))
        rows.append(row)
    return {"root": str(root), "entry_count": len(rows), "entries": rows}


def write_exclusive(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def process_table() -> dict[int, list[int]]:
    result = subprocess.run(
        ["/bin/ps", "-axo", "pid=,ppid="], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
    )
    table: dict[int, list[int]] = {}
    for line in result.stdout.splitlines():
        pid_text, parent_text = line.split()
        table.setdefault(int(parent_text), []).append(int(pid_text))
    return table


def descendants(pid: int) -> list[int]:
    table = process_table()
    answer: list[int] = []

    def visit(parent: int) -> None:
        for child in table.get(parent, []):
            visit(child)
            answer.append(child)

    visit(pid)
    return answer


def terminate_tree(pid: int) -> None:
    targets = descendants(pid) + [pid]
    for sig, pause in ((signal.SIGTERM, 0.5), (signal.SIGKILL, 0.0)):
        for target in targets:
            try:
                os.kill(target, sig)
            except ProcessLookupError:
                pass
        if pause:
            time.sleep(pause)


def environment(mode: str) -> dict[str, str]:
    runtime = PACKAGE / "review_runs"
    home = runtime / "supervisor_home"
    temporary = runtime / "supervisor_tmp"
    home.mkdir(parents=True, exist_ok=True)
    temporary.mkdir(parents=True, exist_ok=True)
    value = {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(home),
        "TMPDIR": str(temporary),
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "K3P_REFEREE_EXTERNAL_SANDBOX": "YES",
        "__CF_USER_TEXT_ENCODING": "0x1F5:0:0",
    }
    if mode in {"regenerate", "all"}:
        value["K3P_REFEREE_CONFIRM_REGENERATION"] = "YES"
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("plan", "verify", "regenerate", "all"))
    parser.add_argument("--wall-timeout-seconds", type=int)
    args = parser.parse_args()
    limits = {"plan": 900, "verify": 18_000, "regenerate": 21_600,
              "all": 28_800}
    wall_timeout = args.wall_timeout_seconds or limits[args.mode]
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(LOCK, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        print(f"refusing duplicate launch; lock exists: {LOCK}", file=sys.stderr)
        return 73
    lock_metadata = os.fstat(descriptor)
    lock_identity = (lock_metadata.st_dev, lock_metadata.st_ino)
    with os.fdopen(descriptor, "w", encoding="utf-8", closefd=False) as handle:
        json.dump({"pid": os.getpid(), "mode": args.mode}, handle, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())

    child: subprocess.Popen[str] | None = None
    started_utc = dt.datetime.now(dt.timezone.utc).isoformat()
    started = time.monotonic()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    external_log = AUDIT / "logs" / f"supervisor_{args.mode}_{stamp}.log"
    summary_path = AUDIT / "execution" / f"supervisor_{args.mode}_{stamp}.json"
    package_before_path = AUDIT / "execution" / f"package_before_{args.mode}_{stamp}.json"
    package_after_path = AUDIT / "execution" / f"package_after_{args.mode}_{stamp}.json"
    venv_before_path = AUDIT / "execution" / f"venv_before_{args.mode}_{stamp}.json"
    venv_after_path = AUDIT / "execution" / f"venv_after_{args.mode}_{stamp}.json"
    package_before = inventory(PACKAGE, exclude_top={"review_runs"})
    venv_root = PYTHON.parent.parent
    venv_before = inventory(venv_root)
    write_exclusive(package_before_path, canonical_json(package_before))
    write_exclusive(venv_before_path, canonical_json(venv_before))
    log_descriptor = os.open(
        external_log, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
    )
    stop_reason: str | None = None

    def interrupt(number: int, _frame: object) -> None:
        nonlocal stop_reason
        stop_reason = f"signal:{number}"
        raise KeyboardInterrupt

    old_handlers = {
        number: signal.signal(number, interrupt)
        for number in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
    }
    try:
        command = [
            "/usr/bin/sandbox-exec", "-f", str(PROFILE), str(PYTHON),
            str(RUNNER), "--package-root", str(PACKAGE),
            "--python", str(PYTHON), "--mode", args.mode,
        ]
        child = subprocess.Popen(
            command, cwd=PACKAGE, env=environment(args.mode), text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        assert child.stdout is not None

        def drain() -> None:
            for chunk in iter(lambda: child.stdout.read(65_536), ""):
                encoded = chunk.encode("utf-8", errors="replace")
                os.write(log_descriptor, encoded)
                os.write(sys.stdout.fileno(), encoded)

        drain_thread = threading.Thread(target=drain, daemon=True)
        drain_thread.start()
        try:
            returncode = child.wait(timeout=wall_timeout)
        except subprocess.TimeoutExpired:
            stop_reason = "wall_timeout"
            terminate_tree(child.pid)
            returncode = child.wait(timeout=30)
        drain_thread.join(timeout=30)
        if drain_thread.is_alive():
            raise RuntimeError("external transcript drain did not finish")
        os.fsync(log_descriptor)
        package_after = inventory(PACKAGE, exclude_top={"review_runs"})
        venv_after = inventory(venv_root)
        write_exclusive(package_after_path, canonical_json(package_after))
        write_exclusive(venv_after_path, canonical_json(venv_after))
        summary = {
            "schema": "k3p-third-revision-external-supervisor-v1",
            "mode": args.mode,
            "status": "PASS" if returncode == 0 and stop_reason is None else "FAIL",
            "returncode": returncode,
            "stop_reason": stop_reason,
            "started_utc": started_utc,
            "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "elapsed_seconds": time.monotonic() - started,
            "wall_timeout_seconds": wall_timeout,
            "sandbox_profile": str(PROFILE),
            "sandbox_profile_sha256": sha256_file(PROFILE),
            "external_transcript": str(external_log),
            "external_transcript_sha256": sha256_file(external_log),
            "package_payload_unchanged": package_before == package_after,
            "venv_unchanged": venv_before == venv_after,
            "inventories": {
                "package_before": str(package_before_path),
                "package_after": str(package_after_path),
                "venv_before": str(venv_before_path),
                "venv_after": str(venv_after_path),
            },
        }
        write_exclusive(summary_path, canonical_json(summary))
        return returncode if stop_reason is None else 124
    except KeyboardInterrupt:
        stop_reason = stop_reason or "keyboard_interrupt"
        if child is not None and child.poll() is None:
            terminate_tree(child.pid)
        return 130
    finally:
        for number, handler in old_handlers.items():
            signal.signal(number, handler)
        os.close(log_descriptor)
        os.close(descriptor)
        try:
            metadata = LOCK.lstat()
            if (metadata.st_dev, metadata.st_ino) != lock_identity:
                raise RuntimeError("outer supervisor lock was replaced")
            LOCK.unlink()
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())

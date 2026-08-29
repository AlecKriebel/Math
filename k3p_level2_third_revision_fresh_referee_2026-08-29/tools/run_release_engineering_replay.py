#!/usr/bin/env python3
"""Run and independently bind the excluded release-engineering suite."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time


AUDIT = Path(__file__).resolve().parents[1]
EXECUTION = AUDIT / "execution/release_engineering_738b"
REPOSITORY = EXECUTION / "repo"
PROJECT = REPOSITORY / "k3p_level2_identifiability_final"
PROFILE = AUDIT / "logs/release_engineering_738b.sb"
TRANSCRIPT = AUDIT / "logs/release_engineering_738b_transcript.log"
SUMMARY = AUDIT / "results/RELEASE_ENGINEERING_REPLAY.json"
PYTHON = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_identifiability_final/.venv/bin/python"
)
SCRIPT = PROJECT / "reproducibility/test_release_engineering_mutations.py"
STORED = PROJECT / "reproducibility/RELEASE_ENGINEERING_MUTATION_REPORT.json"
GIT = "/opt/homebrew/bin/git"
EXPECTED_COMMIT = "738b662aa9c4e6201277f60b249afd4de9bcd9d6"
EXPECTED_PAYLOAD = "9448e3a0904ef6103dee7de817336f1724523298cd6edb4499c6c57027d0f6c9"
EXPECTED_PRETTY = "db2d4a0ec932634ad6b8d2eeeb7cb1499b59b488c76f9bc5264c60cddb758d6f"


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def environment() -> dict[str, str]:
    home = EXECUTION / "runtime_home"
    temporary = EXECUTION / "runtime_tmp"
    home.mkdir(parents=True, exist_ok=True)
    temporary.mkdir(parents=True, exist_ok=True)
    return {
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(home), "TMPDIR": str(temporary),
        "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
        "SOURCE_DATE_EPOCH": "1788019048",
        "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0", "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/usr/bin/false", "SSH_ASKPASS": "/usr/bin/false",
        "GIT_CEILING_DIRECTORIES": str(EXECUTION),
        "__CF_USER_TEXT_ENCODING": "0x1F5:0:0",
    }


def git(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [GIT, "-C", str(REPOSITORY), *arguments], env=environment(),
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False, timeout=120,
    )


def terminate(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)


def parse_report(output: bytes) -> dict:
    sentinel = b"K3P_RELEASE_ENGINEERING_MUTATIONS_PASS\n"
    require(output.endswith(sentinel) and output.count(sentinel) == 1,
            "release mutation sentinel")
    payload = output[:-len(sentinel)].strip()
    value = json.loads(payload)
    require(isinstance(value, dict), "release report object")
    return value


def main() -> int:
    require(not TRANSCRIPT.exists() and not SUMMARY.exists(),
            "refusing to overwrite replay evidence")
    require(not (REPOSITORY / ".git/objects/info/alternates").exists(),
            "checkout uses alternates")
    head = git(["rev-parse", "HEAD"])
    status = git(["status", "--porcelain=v1", "--untracked-files=all"])
    require(head.returncode == 0 and head.stdout.strip() == EXPECTED_COMMIT,
            "exact checkout commit")
    require(status.returncode == 0 and status.stdout == "", "checkout not clean")
    stored = json.loads(STORED.read_text(encoding="utf-8"))
    require(stored.get("payload_sha256") == EXPECTED_PAYLOAD and
            sha256_file(STORED) == EXPECTED_PRETTY, "stored report identity")
    started_utc = dt.datetime.now(dt.timezone.utc).isoformat()
    started = time.monotonic()
    command = [
        "/usr/bin/sandbox-exec", "-f", str(PROFILE), str(PYTHON),
        str(SCRIPT), "--no-write-report",
    ]
    process = subprocess.Popen(
        command, cwd=PROJECT, env=environment(), stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=900)
    except subprocess.TimeoutExpired as error:
        terminate(process)
        raise AuditFailure("release mutation replay timeout") from error
    require(process.returncode == 0, ("release mutation returncode", process.returncode,
                                      output[-2000:]))
    descriptor = os.open(TRANSCRIPT, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(output); handle.flush(); os.fsync(handle.fileno())
    fresh = parse_report(output)
    require(fresh == stored, "fresh release report differs from sealed report")
    require(fresh.get("mutation_count") == fresh.get("rejected") == 32 and
            fresh.get("survived") == 0 and len(fresh.get("controls", [])) == 11,
            "fresh release mutation/control census")
    logical = dict(fresh); logical.pop("payload_sha256", None)
    observed_payload = sha256_bytes(json.dumps(
        logical, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii"))
    require(observed_payload == EXPECTED_PAYLOAD, "fresh logical payload")
    final_status = git(["status", "--porcelain=v1", "--untracked-files=all"])
    require(final_status.returncode == 0 and final_status.stdout == "",
            ("checkout drift", final_status.stdout))
    summary = {
        "schema": "k3p-third-revision-release-engineering-replay-v1",
        "status": "PASS",
        "source_commit": EXPECTED_COMMIT,
        "checkout_self_contained": True,
        "checkout_alternates": False,
        "mutation_count": 32, "rejected": 32, "survived": 0,
        "control_count": 11,
        "payload_sha256": observed_payload,
        "pretty_report_sha256": sha256_file(STORED),
        "fresh_equals_sealed_report": True,
        "transcript": {"path": str(TRANSCRIPT), "bytes": len(output),
                       "sha256": sha256_file(TRANSCRIPT)},
        "sandbox_profile_sha256": sha256_file(PROFILE),
        "started_utc": started_utc,
        "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - started,
        "clean_before_and_after": True,
    }
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(SUMMARY, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write((json.dumps(summary, indent=2, sort_keys=True) + "\n").encode())
        handle.flush(); os.fsync(handle.fileno())
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

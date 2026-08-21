#!/usr/bin/env python3
"""Produce and replay an LRAT layer for the frozen C5 certificate.

This program is intentionally standalone and fail-closed.  It uses only the
Python standard library, writes only inside its new certificate directory
(apart from an optional replay-log path), and never modifies the accepted
CNF or binary-DRAT run.  Heavy children are serialized by the campaign lock.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Mapping, Sequence


CERTIFICATE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]

CNF_RELATIVE = Path(
    "results/synthesis_k3_hole5_signature_package/instance.cnf"
)
DRAT_RELATIVE = Path(
    "results/synthesis_k3_hole5_signature_seed0_600s_binary"
    "/proof.additions.bdrat"
)
DRAT_TRIM_RELATIVE = Path("tools/drat_trim_2023_05_22/drat-trim")
LRAT_CHECK_RELATIVE = Path("tools/drat_trim_2023_05_22/lrat-check")
DRAT_TRIM_SOURCE_RELATIVE = Path(
    "tools/drat_trim_2023_05_22/drat-trim.c"
)
LRAT_CHECK_SOURCE_RELATIVE = Path(
    "tools/drat_trim_2023_05_22/lrat-check.c"
)
MAKEFILE_RELATIVE = Path("tools/drat_trim_2023_05_22/Makefile")
ARCHIVE_RELATIVE = Path("tools/drat_trim_2023_05_22.tar.gz")

CNF = ROOT / CNF_RELATIVE
DRAT = ROOT / DRAT_RELATIVE
DRAT_TRIM = ROOT / DRAT_TRIM_RELATIVE
LRAT_CHECK = ROOT / LRAT_CHECK_RELATIVE

LRAT_RELATIVE = Path("proof/hole5-c033.lrat")
GENERATOR_STDOUT_RELATIVE = Path("generator/drat-trim.stdout")
GENERATOR_STDERR_RELATIVE = Path("generator/drat-trim.stderr")
CHECKER_STDOUT_RELATIVE = Path("checker/lrat-check.stdout")
CHECKER_STDERR_RELATIVE = Path("checker/lrat-check.stderr")
MANIFEST_RELATIVE = Path("manifest.json")
REPLAY_RELATIVE = Path("repro/hole5_lrat_replay.py")

SOURCE_COMMIT = "6f3ef0a0970b7214c34018fe32ea1ceeb5764d17"
PACKAGE_COMMIT = "dff45f4239e4acabc461533a0a213beec18ec56d"
CNF_GIT_BLOB = "94137d461c59108179042aa772ddde0726209d64"
DRAT_GIT_BLOB = "c223215d60809236d0c2061d959f96511b1ca427"
DRAT_TRIM_COMMIT = "2e5e29cb0019d5cfd547d4208dca1b3ec290349f"
DRAT_TRIM_VERSION = "v05.22.2023"

EXPECTED_STATIC = {
    str(CNF_RELATIVE): (
        754323,
        "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd"
        "55f0b0152703d104",
    ),
    str(DRAT_RELATIVE): (
        6337621,
        "c6c24853e30073e66fb396441edb176a0160d062a8558e25f"
        "a18a955f33927c3",
    ),
    str(DRAT_TRIM_RELATIVE): (
        70088,
        "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bca"
        "d241271812beb",
    ),
    str(LRAT_CHECK_RELATIVE): (
        36520,
        "5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edf"
        "c8fda1f26c7a2",
    ),
    str(DRAT_TRIM_SOURCE_RELATIVE): (
        59498,
        "f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165"
        "742eb1ba9a26",
    ),
    str(LRAT_CHECK_SOURCE_RELATIVE): (
        17332,
        "05b3c92f6734fdfc9ee5c72217c9935540c1255b58bc9bdc134"
        "b6b26f5b43c9f",
    ),
    str(MAKEFILE_RELATIVE): (
        493,
        "1f3c7128b1dd739723257edd95cc28a2ee747779ca01ae80ed925"
        "2f02ec5149d",
    ),
    str(ARCHIVE_RELATIVE): (
        7290624,
        "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb"
        "6c7139949108",
    ),
}

SCHEMA = "gamma-theta-hole5-c033-lrat-certificate-v1"
REPLAY_SCHEMA = "gamma-theta-hole5-c033-lrat-replay-v1"
CLAIM_SCOPE = (
    "The exact retained S6-signature-broken hole5 CNF only; this adds an "
    "LRAT verification layer and makes no broader mathematical claim."
)

GIB = 1024**3
MIB = 1024**2
LRAT_LIMIT_BYTES = 2 * GIB
DISK_RESERVE_BYTES = 8 * GIB
DISK_HEADROOM_BYTES = 512 * MIB
ADDRESS_SPACE_LIMIT_BYTES = 4 * GIB
GENERATOR_INTERNAL_TIMEOUT_SECONDS = 1200
GENERATOR_WALL_TIMEOUT_SECONDS = 1500
CHECKER_WALL_TIMEOUT_SECONDS = 1200
CPU_LIMIT_SECONDS = 1350
MIN_START_MEMORY_FREE_PERCENT = 20
MIN_RUNNING_MEMORY_FREE_PERCENT = 10
MAX_START_LOAD_PER_CPU = 1.8

GENERATOR_TIME = re.compile(
    rb"c verification time: [0-9]+(?:\.[0-9]+)? seconds"
)
CHECKER_TIME = re.compile(
    rb"c verification time = [0-9]+(?:\.[0-9]+)? secs"
)
MEMORY_FREE = re.compile(rb"free percentage:\s*([0-9]+)%")
TRANSIENT_NAME = re.compile(r"(?:^\.|\.partial(?:\.|$)|\.tmp$|\.lock$)")


class CertificateFailure(RuntimeError):
    """A permanent artifact or verification failure."""


class UnsafeNow(CertificateFailure):
    """Current resource pressure makes a heavy launch unsafe."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateFailure(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("ascii")


def static_record(relative: Path) -> dict[str, object]:
    path = ROOT / relative
    expected_size, expected_hash = EXPECTED_STATIC[str(relative)]
    information = path.stat()
    require(stat.S_ISREG(information.st_mode), f"not regular: {relative}")
    require(information.st_nlink == 1, f"not single-link: {relative}")
    actual_hash = sha256_file(path)
    require(information.st_size == expected_size, f"size mismatch: {relative}")
    require(actual_hash == expected_hash, f"hash mismatch: {relative}")
    return {
        "path": str(relative),
        "sha256": actual_hash,
        "size_bytes": information.st_size,
    }


def run_git(arguments: Sequence[str]) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        completed.returncode == 0 and not completed.stderr,
        f"Git command failed: {' '.join(arguments)}",
    )
    return completed.stdout


def git_object(commit: str, relative: Path) -> bytes:
    prefix = run_git(["rev-parse", "--show-prefix"]).decode("ascii").strip()
    require(prefix and prefix.endswith("/"), "unexpected Git worktree prefix")
    spec = f"{commit}:{prefix}{relative.as_posix()}"
    payload = run_git(["show", spec])
    expected_blob = (
        CNF_GIT_BLOB if relative == CNF_RELATIVE else DRAT_GIT_BLOB
    )
    actual_blob = run_git(["rev-parse", spec]).decode("ascii").strip()
    require(actual_blob == expected_blob, f"Git blob mismatch: {relative}")
    return payload


def validate_static_inputs() -> dict[str, object]:
    records = {
        str(relative): static_record(relative)
        for relative in (
            CNF_RELATIVE,
            DRAT_RELATIVE,
            DRAT_TRIM_RELATIVE,
            LRAT_CHECK_RELATIVE,
            DRAT_TRIM_SOURCE_RELATIVE,
            LRAT_CHECK_SOURCE_RELATIVE,
            MAKEFILE_RELATIVE,
            ARCHIVE_RELATIVE,
        )
    }
    require(os.access(DRAT_TRIM, os.X_OK), "drat-trim is not executable")
    require(os.access(LRAT_CHECK, os.X_OK), "lrat-check is not executable")
    require(
        git_object(SOURCE_COMMIT, CNF_RELATIVE) == CNF.read_bytes(),
        "CNF differs from source-commit blob",
    )
    require(
        git_object(PACKAGE_COMMIT, DRAT_RELATIVE) == DRAT.read_bytes(),
        "proof differs from package-commit blob",
    )
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", SOURCE_COMMIT, PACKAGE_COMMIT],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(
        completed.returncode == 0
        and not completed.stdout
        and not completed.stderr,
        "source commit is not an ancestor of package commit",
    )
    return records


def memory_free_percent() -> int:
    completed = subprocess.run(
        ["/usr/bin/memory_pressure", "-Q"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr:
        raise UnsafeNow("cannot read memory-pressure status")
    match = MEMORY_FREE.search(completed.stdout)
    if match is None:
        raise UnsafeNow("cannot parse memory-pressure status")
    return int(match.group(1))


def free_disk_bytes() -> int:
    return shutil.disk_usage(ROOT).free


def initial_resource_gate() -> dict[str, object]:
    free_disk = free_disk_bytes()
    required_disk = (
        DISK_RESERVE_BYTES + LRAT_LIMIT_BYTES + DISK_HEADROOM_BYTES
    )
    if free_disk < required_disk:
        raise UnsafeNow(
            f"free disk {free_disk} is below safe launch threshold "
            f"{required_disk}"
        )
    free_percent = memory_free_percent()
    if free_percent < MIN_START_MEMORY_FREE_PERCENT:
        raise UnsafeNow(
            f"memory free percentage {free_percent} is below "
            f"{MIN_START_MEMORY_FREE_PERCENT}"
        )
    cpus = os.cpu_count() or 1
    load_one = os.getloadavg()[0]
    load_limit = cpus * MAX_START_LOAD_PER_CPU
    if load_one > load_limit:
        raise UnsafeNow(
            f"one-minute load {load_one:.2f} exceeds safe threshold "
            f"{load_limit:.2f}"
        )
    return {
        "cpu_count": cpus,
        "disk_free_before_bytes": free_disk,
        "memory_free_before_percent": free_percent,
        "one_minute_load_before": round(load_one, 2),
    }


class HeavyChildLock:
    def __init__(self) -> None:
        digest = sha256_bytes(str(ROOT.resolve()).encode("utf-8"))[:20]
        self.path = (
            Path(tempfile.gettempdir())
            / f"gamma-theta-k3-heavy-child-{digest}.lock"
        )
        self.descriptor: int | None = None

    def __enter__(self) -> "HeavyChildLock":
        descriptor = os.open(self.path, os.O_CREAT | os.O_RDWR, 0o600)
        information = os.fstat(descriptor)
        require(
            stat.S_ISREG(information.st_mode)
            and information.st_nlink == 1,
            "campaign heavy-child lock is unsafe",
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            os.close(descriptor)
            raise UnsafeNow("another campaign heavy child is active") from error
        self.descriptor = descriptor
        return self

    def __exit__(self, *ignored: object) -> None:
        require(self.descriptor is not None, "heavy-child lock was not held")
        fcntl.flock(self.descriptor, fcntl.LOCK_UN)
        os.close(self.descriptor)
        self.descriptor = None


def child_limits() -> None:
    os.nice(10)
    resource.setrlimit(
        resource.RLIMIT_AS,
        (ADDRESS_SPACE_LIMIT_BYTES, ADDRESS_SPACE_LIMIT_BYTES),
    )
    resource.setrlimit(
        resource.RLIMIT_FSIZE,
        (LRAT_LIMIT_BYTES, LRAT_LIMIT_BYTES),
    )
    resource.setrlimit(
        resource.RLIMIT_CPU,
        (CPU_LIMIT_SECONDS, CPU_LIMIT_SECONDS + 5),
    )
    os.setsid()


def terminate_child(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)


def run_guarded(
    command: Sequence[str],
    *,
    stdout_path: Path,
    stderr_path: Path,
    wall_timeout_seconds: int,
    growing_artifact: Path | None,
) -> int:
    require(not stdout_path.exists(), f"output exists: {stdout_path}")
    require(not stderr_path.exists(), f"output exists: {stderr_path}")
    with stdout_path.open("xb") as stdout_handle:
        with stderr_path.open("xb") as stderr_handle:
            process = subprocess.Popen(
                list(command),
                cwd=ROOT,
                stdin=subprocess.DEVNULL,
                stdout=stdout_handle,
                stderr=stderr_handle,
                preexec_fn=child_limits,
            )
            started = time.monotonic()
            last_pressure_check = 0.0
            abort_reason: str | None = None
            try:
                while process.poll() is None:
                    now = time.monotonic()
                    if now - started > wall_timeout_seconds:
                        abort_reason = (
                            f"wall timeout exceeded: {wall_timeout_seconds}s"
                        )
                        break
                    if free_disk_bytes() < DISK_RESERVE_BYTES:
                        abort_reason = "free disk fell below 8 GiB reserve"
                        break
                    if (
                        growing_artifact is not None
                        and growing_artifact.exists()
                        and growing_artifact.stat().st_size > LRAT_LIMIT_BYTES
                    ):
                        abort_reason = "LRAT exceeded 2 GiB"
                        break
                    if now - last_pressure_check >= 5:
                        if (
                            memory_free_percent()
                            < MIN_RUNNING_MEMORY_FREE_PERCENT
                        ):
                            abort_reason = (
                                "memory free percentage fell below running "
                                "safety threshold"
                            )
                            break
                        last_pressure_check = now
                    time.sleep(0.25)
            except BaseException:
                terminate_child(process)
                raise
            if abort_reason is not None:
                terminate_child(process)
                raise CertificateFailure(abort_reason)
            return process.wait()


def normalized_output(payload: bytes, pattern: re.Pattern[bytes]) -> bytes:
    payload = payload.replace(b"\r", b"\n")
    matches = pattern.findall(payload)
    require(len(matches) == 1, "expected exactly one timing line")
    return pattern.sub(b"c verification time: <elapsed>", payload)


def validate_generator_log(stdout: bytes, stderr: bytes) -> dict[str, object]:
    text = stdout.replace(b"\r", b"\n").decode("ascii")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    require(not stderr, "drat-trim emitted stderr")
    require(lines.count("s VERIFIED") == 1, "missing unique s VERIFIED")
    require(not any("TIMEOUT" in line for line in lines), "drat-trim timed out")
    require(
        not any("NOT VERIFIED" in line for line in lines),
        "drat-trim reported NOT VERIFIED",
    )
    require(
        not any("WARNING" in line.upper() for line in lines),
        "drat-trim emitted a warning",
    )
    rat_lines = [line for line in lines if "RAT lemmas in core" in line]
    require(
        len(rat_lines) == 1 and "c 0 RAT lemmas in core;" in rat_lines[0],
        "drat-trim did not report zero RAT lemmas",
    )
    stable = normalized_output(stdout, GENERATOR_TIME)
    return {
        "stderr_empty": True,
        "unique_verified_marker": True,
        "timeout_marker_absent": True,
        "warning_marker_absent": True,
        "zero_rat_lemmas": True,
        "normalized_stdout_sha256": sha256_bytes(stable),
    }


def validate_checker_log(stdout: bytes, stderr: bytes) -> dict[str, object]:
    text = stdout.replace(b"\r", b"\n").decode("ascii")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    require(not stderr, "lrat-check emitted stderr")
    require(lines.count("c VERIFIED") == 1, "missing unique c VERIFIED")
    require(
        not any("NOT VERIFIED" in line for line in lines),
        "lrat-check reported NOT VERIFIED",
    )
    require(
        not any("failed" in line.lower() for line in lines),
        "lrat-check reported a failure",
    )
    stable = normalized_output(stdout, CHECKER_TIME)
    return {
        "stderr_empty": True,
        "unique_verified_marker": True,
        "not_verified_marker_absent": True,
        "failure_marker_absent": True,
        "normalized_stdout_sha256": sha256_bytes(stable),
    }


def scan_lrat(path: Path) -> dict[str, int]:
    additions = 0
    deletions = 0
    empty_additions = 0
    line_count = 0
    last_addition_identifier = 0
    maximum_identifier = 0
    maximum_hint = 0
    maximum_clause_length = 0
    last_was_empty_addition = False
    with path.open("rb") as handle:
        for raw_line in handle:
            line_count += 1
            require(raw_line.endswith(b"\n"), "LRAT line lacks newline")
            require(b"\r" not in raw_line, "LRAT contains carriage return")
            tokens = raw_line[:-1].split()
            require(tokens, "LRAT contains blank line")
            try:
                identifier = int(tokens[0])
            except ValueError as error:
                raise CertificateFailure("noninteger LRAT identifier") from error
            require(identifier > 0, "nonpositive LRAT identifier")
            maximum_identifier = max(maximum_identifier, identifier)
            last_was_empty_addition = False
            if len(tokens) >= 2 and tokens[1] == b"d":
                deletions += 1
                require(tokens[-1] == b"0", "unterminated LRAT deletion")
                try:
                    deleted = [int(token) for token in tokens[2:-1]]
                except ValueError as error:
                    raise CertificateFailure(
                        "noninteger LRAT deletion identifier"
                    ) from error
                require(
                    all(deleted_identifier > 0 for deleted_identifier in deleted),
                    "invalid LRAT deletion identifier",
                )
                continue
            try:
                values = [int(token) for token in tokens[1:]]
            except ValueError as error:
                raise CertificateFailure("noninteger LRAT token") from error
            require(values.count(0) == 2, "LRAT addition needs two zeros")
            split = values.index(0)
            clause = values[:split]
            hints = values[split + 1 : -1]
            require(values[-1] == 0, "unterminated LRAT hint sequence")
            require(identifier > last_addition_identifier, "LRAT IDs regress")
            require(
                all(literal != 0 and abs(literal) <= 6886 for literal in clause),
                "LRAT clause literal out of range",
            )
            clause_set = set(clause)
            require(
                len(clause_set) == len(clause)
                and not any(-literal in clause_set for literal in clause),
                "duplicate or complementary LRAT clause literal",
            )
            require(hints and all(hint > 0 for hint in hints), "invalid RUP hints")
            additions += 1
            last_addition_identifier = identifier
            maximum_clause_length = max(maximum_clause_length, len(clause))
            maximum_hint = max(maximum_hint, max(hints))
            if not clause:
                empty_additions += 1
                last_was_empty_addition = True
    require(line_count > 0, "empty LRAT file")
    require(additions > 0, "LRAT has no additions")
    require(empty_additions == 1, "LRAT lacks unique empty addition")
    require(last_was_empty_addition, "LRAT does not end in empty addition")
    return {
        "addition_count": additions,
        "deletion_count": deletions,
        "empty_addition_count": empty_additions,
        "line_count": line_count,
        "maximum_clause_identifier": maximum_identifier,
        "maximum_clause_length": maximum_clause_length,
        "maximum_hint_identifier": maximum_hint,
    }


def artifact_record(relative: Path) -> dict[str, object]:
    path = CERTIFICATE / relative
    information = path.stat()
    require(stat.S_ISREG(information.st_mode), f"not regular: {relative}")
    require(information.st_nlink == 1, f"not single-link: {relative}")
    return {
        "path": str(relative),
        "sha256": sha256_file(path),
        "size_bytes": information.st_size,
    }


def install_new(source: Path, destination: Path) -> None:
    require(source.is_file(), f"install source missing: {source}")
    require(not destination.exists(), f"install target exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.link(source, destination)
    source.unlink()


def write_new_atomic(path: Path, payload: bytes) -> None:
    frozen_run = ROOT / DRAT_RELATIVE.parent
    resolved = path.resolve(strict=False)
    require(
        frozen_run not in resolved.parents,
        "refusing to write inside frozen run",
    )
    require(
        resolved == (CERTIFICATE / MANIFEST_RELATIVE).resolve(strict=False)
        or (resolved != CERTIFICATE and CERTIFICATE not in resolved.parents),
        "replay output must remain outside certificate directory",
    )
    require(path.parent.is_dir(), "output parent does not exist")
    require(not path.exists() and not path.is_symlink(), "output exists")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.partial.",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    installed = False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
        temporary.unlink()
        installed = True
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if not installed and temporary.exists():
            temporary.unlink()


def normalized_commands() -> dict[str, list[str]]:
    return {
        "generator": [
            "$DRAT_TRIM",
            "$CNF",
            "$ADDITION_ONLY_BINARY_DRAT",
            "-i",
            "-W",
            "-U",
            "-L",
            "$LRAT",
            "-t",
            str(GENERATOR_INTERNAL_TIMEOUT_SECONDS),
        ],
        "checker": ["$LRAT_CHECK", "$CNF", "$LRAT"],
    }


def actual_generator_command(lrat: Path) -> list[str]:
    return [
        str(DRAT_TRIM),
        str(CNF),
        str(DRAT),
        "-i",
        "-W",
        "-U",
        "-L",
        str(lrat),
        "-t",
        str(GENERATOR_INTERNAL_TIMEOUT_SECONDS),
    ]


def actual_checker_command(lrat: Path) -> list[str]:
    return [str(LRAT_CHECK), str(CNF), str(lrat)]


def source_binding() -> dict[str, object]:
    return {
        "cnf_git_blob": CNF_GIT_BLOB,
        "package_commit": PACKAGE_COMMIT,
        "proof_git_blob": DRAT_GIT_BLOB,
        "source_commit": SOURCE_COMMIT,
        "source_is_ancestor_of_package": True,
    }


def tool_binding(static: Mapping[str, object]) -> dict[str, object]:
    return {
        "archive": static[str(ARCHIVE_RELATIVE)],
        "commit": DRAT_TRIM_COMMIT,
        "drat_trim": {
            "binary": static[str(DRAT_TRIM_RELATIVE)],
            "source": static[str(DRAT_TRIM_SOURCE_RELATIVE)],
        },
        "lrat_check": {
            "binary": static[str(LRAT_CHECK_RELATIVE)],
            "source": static[str(LRAT_CHECK_SOURCE_RELATIVE)],
        },
        "makefile": static[str(MAKEFILE_RELATIVE)],
        "version": DRAT_TRIM_VERSION,
    }


def resource_policy() -> dict[str, object]:
    return {
        "address_space_limit_bytes": ADDRESS_SPACE_LIMIT_BYTES,
        "checker_wall_timeout_seconds": CHECKER_WALL_TIMEOUT_SECONDS,
        "cpu_limit_seconds": CPU_LIMIT_SECONDS,
        "disk_reserve_bytes": DISK_RESERVE_BYTES,
        "generator_internal_timeout_seconds": (
            GENERATOR_INTERNAL_TIMEOUT_SECONDS
        ),
        "generator_wall_timeout_seconds": GENERATOR_WALL_TIMEOUT_SECONDS,
        "lrat_limit_bytes": LRAT_LIMIT_BYTES,
        "maximum_start_load_per_cpu": MAX_START_LOAD_PER_CPU,
        "minimum_running_memory_free_percent": (
            MIN_RUNNING_MEMORY_FREE_PERCENT
        ),
        "minimum_start_memory_free_percent": MIN_START_MEMORY_FREE_PERCENT,
        "one_heavy_child_lock": True,
        "process_niceness": 10,
    }


def reproduction_record() -> dict[str, object]:
    return {
        "command": ["python3", str(REPLAY_RELATIVE), "verify"],
        "fresh_lrat_checker_replay": True,
        "production_solver_rerun": False,
    }


def claim_boundary() -> dict[str, bool]:
    return {
        "exact_c5_branch_only": True,
        "order12_k3_slice_claimed_by_this_layer": False,
        "universal_conjecture_resolved": False,
    }


def build_manifest(
    static: Mapping[str, object],
    *,
    scan: Mapping[str, int],
    generator_checks: Mapping[str, object],
    checker_checks: Mapping[str, object],
) -> dict[str, object]:
    artifacts = {
        str(relative): artifact_record(relative)
        for relative in (
            LRAT_RELATIVE,
            GENERATOR_STDOUT_RELATIVE,
            GENERATOR_STDERR_RELATIVE,
            CHECKER_STDOUT_RELATIVE,
            CHECKER_STDERR_RELATIVE,
            REPLAY_RELATIVE,
        )
    }
    require(
        int(artifacts[str(LRAT_RELATIVE)]["size_bytes"])
        <= LRAT_LIMIT_BYTES,
        "retained LRAT exceeds 2 GiB",
    )
    return {
        "schema": SCHEMA,
        "status": "LRAT_VERIFIED_FINITE_CERTIFICATE_LAYER",
        "claim_status": "NO_NEW_MATHEMATICAL_CLAIM",
        "scope": CLAIM_SCOPE,
        "source_binding": source_binding(),
        "inputs": {
            str(CNF_RELATIVE): static[str(CNF_RELATIVE)],
            str(DRAT_RELATIVE): static[str(DRAT_RELATIVE)],
        },
        "tools": tool_binding(static),
        "commands": normalized_commands(),
        "resource_policy": resource_policy(),
        "generator_verification": {
            "exit_code": 0,
            **generator_checks,
        },
        "lrat_checker_verification": {
            "exit_code": 0,
            **checker_checks,
        },
        "lrat_scan": dict(scan),
        "artifacts": artifacts,
        "reproduction": reproduction_record(),
        "claim_boundary": claim_boundary(),
    }


def expected_certificate_files() -> set[str]:
    return {
        str(MANIFEST_RELATIVE),
        str(LRAT_RELATIVE),
        str(GENERATOR_STDOUT_RELATIVE),
        str(GENERATOR_STDERR_RELATIVE),
        str(CHECKER_STDOUT_RELATIVE),
        str(CHECKER_STDERR_RELATIVE),
        str(REPLAY_RELATIVE),
    }


def audit_certificate_tree() -> None:
    actual: set[str] = set()
    for path in CERTIFICATE.rglob("*"):
        relative = path.relative_to(CERTIFICATE).as_posix()
        if path.is_dir():
            continue
        require(not path.is_symlink(), f"symlink in certificate: {relative}")
        require(
            not TRANSIENT_NAME.search(path.name),
            f"transient file in certificate: {relative}",
        )
        information = path.stat()
        require(
            stat.S_ISREG(information.st_mode) and information.st_nlink == 1,
            f"unsafe certificate entry: {relative}",
        )
        actual.add(relative)
    require(
        actual == expected_certificate_files(),
        f"certificate file set mismatch: {sorted(actual)}",
    )


def validate_manifest(
    manifest: Mapping[str, object],
    static: Mapping[str, object],
) -> None:
    require(manifest.get("schema") == SCHEMA, "manifest schema mismatch")
    require(
        manifest.get("status") == "LRAT_VERIFIED_FINITE_CERTIFICATE_LAYER",
        "manifest status mismatch",
    )
    require(
        manifest.get("claim_status") == "NO_NEW_MATHEMATICAL_CLAIM",
        "manifest claim status mismatch",
    )
    require(manifest.get("scope") == CLAIM_SCOPE, "manifest scope mismatch")
    require(
        manifest.get("commands") == normalized_commands(),
        "manifest command mismatch",
    )
    inputs = manifest.get("inputs")
    require(isinstance(inputs, dict), "manifest inputs missing")
    require(
        inputs
        == {
            str(CNF_RELATIVE): static[str(CNF_RELATIVE)],
            str(DRAT_RELATIVE): static[str(DRAT_RELATIVE)],
        },
        "manifest input binding mismatch",
    )
    artifacts = manifest.get("artifacts")
    require(isinstance(artifacts, dict), "manifest artifacts missing")
    require(
        set(artifacts) == expected_certificate_files() - {str(MANIFEST_RELATIVE)},
        "manifest artifact set mismatch",
    )
    for name, retained in artifacts.items():
        require(isinstance(retained, dict), f"bad artifact record: {name}")
        require(
            retained == artifact_record(Path(name)),
            f"artifact binding mismatch: {name}",
        )
    retained_scan = manifest.get("lrat_scan")
    require(
        retained_scan == scan_lrat(CERTIFICATE / LRAT_RELATIVE),
        "LRAT scan mismatch",
    )
    generator_checks = manifest.get("generator_verification")
    checker_checks = manifest.get("lrat_checker_verification")
    require(
        isinstance(generator_checks, dict)
        and generator_checks.get("exit_code") == 0,
        "generator verification record missing",
    )
    require(
        isinstance(checker_checks, dict)
        and checker_checks.get("exit_code") == 0,
        "checker verification record missing",
    )
    fresh_generator_checks = validate_generator_log(
        (CERTIFICATE / GENERATOR_STDOUT_RELATIVE).read_bytes(),
        (CERTIFICATE / GENERATOR_STDERR_RELATIVE).read_bytes(),
    )
    fresh_checker_checks = validate_checker_log(
        (CERTIFICATE / CHECKER_STDOUT_RELATIVE).read_bytes(),
        (CERTIFICATE / CHECKER_STDERR_RELATIVE).read_bytes(),
    )
    require(
        generator_checks == {"exit_code": 0, **fresh_generator_checks},
        "generator verification content mismatch",
    )
    require(
        checker_checks == {"exit_code": 0, **fresh_checker_checks},
        "checker verification content mismatch",
    )


def produce() -> int:
    manifest_path = CERTIFICATE / MANIFEST_RELATIVE
    require(not manifest_path.exists(), "manifest already exists")
    static = validate_static_inputs()
    preflight = initial_resource_gate()
    expected_before = {str(REPLAY_RELATIVE)}
    actual_before = {
        path.relative_to(CERTIFICATE).as_posix()
        for path in CERTIFICATE.rglob("*")
        if path.is_file()
    }
    require(
        actual_before == expected_before,
        f"unexpected pre-production files: {sorted(actual_before)}",
    )
    scratch = Path(
        tempfile.mkdtemp(prefix=".lrat-production.", dir=CERTIFICATE)
    )
    lrat = scratch / "proof.lrat"
    generator_stdout = scratch / "generator.stdout"
    generator_stderr = scratch / "generator.stderr"
    checker_stdout = scratch / "checker.stdout"
    checker_stderr = scratch / "checker.stderr"
    try:
        with HeavyChildLock():
            generator_exit = run_guarded(
                actual_generator_command(lrat),
                stdout_path=generator_stdout,
                stderr_path=generator_stderr,
                wall_timeout_seconds=GENERATOR_WALL_TIMEOUT_SECONDS,
                growing_artifact=lrat,
            )
            require(generator_exit == 0, f"drat-trim exit {generator_exit}")
            require(lrat.is_file(), "drat-trim did not create LRAT")
            require(0 < lrat.stat().st_size <= LRAT_LIMIT_BYTES, "bad LRAT size")
            generator_checks = validate_generator_log(
                generator_stdout.read_bytes(),
                generator_stderr.read_bytes(),
            )
            scan = scan_lrat(lrat)
            checker_exit = run_guarded(
                actual_checker_command(lrat),
                stdout_path=checker_stdout,
                stderr_path=checker_stderr,
                wall_timeout_seconds=CHECKER_WALL_TIMEOUT_SECONDS,
                growing_artifact=None,
            )
            require(checker_exit == 0, f"lrat-check exit {checker_exit}")
            checker_checks = validate_checker_log(
                checker_stdout.read_bytes(),
                checker_stderr.read_bytes(),
            )
        require(
            free_disk_bytes() >= DISK_RESERVE_BYTES,
            "free disk is below 8 GiB after verification",
        )
        install_new(lrat, CERTIFICATE / LRAT_RELATIVE)
        install_new(
            generator_stdout,
            CERTIFICATE / GENERATOR_STDOUT_RELATIVE,
        )
        install_new(
            generator_stderr,
            CERTIFICATE / GENERATOR_STDERR_RELATIVE,
        )
        install_new(checker_stdout, CERTIFICATE / CHECKER_STDOUT_RELATIVE)
        install_new(checker_stderr, CERTIFICATE / CHECKER_STDERR_RELATIVE)
        manifest = build_manifest(
            static,
            scan=scan,
            generator_checks=generator_checks,
            checker_checks=checker_checks,
        )
        write_new_atomic(manifest_path, canonical_json_bytes(manifest))
    finally:
        if scratch.exists():
            require(
                scratch.parent == CERTIFICATE
                and scratch.name.startswith(".lrat-production."),
                "unsafe scratch cleanup target",
            )
            shutil.rmtree(scratch)
    audit_certificate_tree()
    manifest_hash = sha256_file(manifest_path)
    print(
        json.dumps(
            {
                "manifest_sha256": manifest_hash,
                "preflight": preflight,
                "status": "LRAT_VERIFIED_FINITE_CERTIFICATE_LAYER",
            },
            sort_keys=True,
        )
    )
    return 0


def verify(output: Path | None) -> int:
    static = validate_static_inputs()
    audit_certificate_tree()
    manifest_path = CERTIFICATE / MANIFEST_RELATIVE
    manifest_payload = manifest_path.read_bytes()
    try:
        manifest = json.loads(manifest_payload)
    except json.JSONDecodeError as error:
        raise CertificateFailure("manifest is not JSON") from error
    require(isinstance(manifest, dict), "manifest root is not an object")
    require(
        canonical_json_bytes(manifest) == manifest_payload,
        "manifest is not canonical JSON",
    )
    validate_manifest(manifest, static)
    initial_resource_gate()
    scratch = Path(tempfile.mkdtemp(prefix=".lrat-replay.", dir=CERTIFICATE))
    checker_stdout = scratch / "checker.stdout"
    checker_stderr = scratch / "checker.stderr"
    try:
        with HeavyChildLock():
            exit_code = run_guarded(
                actual_checker_command(CERTIFICATE / LRAT_RELATIVE),
                stdout_path=checker_stdout,
                stderr_path=checker_stderr,
                wall_timeout_seconds=CHECKER_WALL_TIMEOUT_SECONDS,
                growing_artifact=None,
            )
        require(exit_code == 0, f"fresh lrat-check exit {exit_code}")
        checks = validate_checker_log(
            checker_stdout.read_bytes(),
            checker_stderr.read_bytes(),
        )
        retained = manifest["lrat_checker_verification"]
        require(
            isinstance(retained, dict)
            and retained["normalized_stdout_sha256"]
            == checks["normalized_stdout_sha256"],
            "fresh checker transcript differs after timing normalization",
        )
        replay = {
            "schema": REPLAY_SCHEMA,
            "status": "PASS",
            "claim_status": "NO_NEW_MATHEMATICAL_CLAIM",
            "scope": CLAIM_SCOPE,
            "manifest_sha256": sha256_bytes(manifest_payload),
            "cnf_sha256": EXPECTED_STATIC[str(CNF_RELATIVE)][1],
            "lrat_sha256": sha256_file(CERTIFICATE / LRAT_RELATIVE),
            "lrat_size_bytes": (CERTIFICATE / LRAT_RELATIVE).stat().st_size,
            "lrat_scan": manifest["lrat_scan"],
            "checker": {
                "binary_sha256": EXPECTED_STATIC[
                    str(LRAT_CHECK_RELATIVE)
                ][1],
                "exit_code": 0,
                **checks,
            },
            "output_directory_modified": False,
            "production_solver_rerun": False,
        }
        payload = canonical_json_bytes(replay)
        if output is None:
            sys.stdout.buffer.write(payload)
        else:
            write_new_atomic(output, payload)
            print(sha256_bytes(payload))
    finally:
        if scratch.exists():
            require(
                scratch.parent == CERTIFICATE
                and scratch.name.startswith(".lrat-replay."),
                "unsafe replay scratch cleanup target",
            )
            shutil.rmtree(scratch)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="produce or replay the frozen hole5 C033 LRAT layer"
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)
    subparsers.add_parser("produce")
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    try:
        if arguments.mode == "produce":
            return produce()
        return verify(arguments.output)
    except UnsafeNow as error:
        print(f"UNSAFE_NOW: {error}", file=sys.stderr)
        return 75
    except CertificateFailure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

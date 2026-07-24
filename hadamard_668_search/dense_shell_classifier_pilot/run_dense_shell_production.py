#!/usr/bin/env python3
"""Memory-capped, hash-pinned runner for complete dense-shell prefix shards."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any

from production_common import (
    BURNSIDE,
    MANIFEST_SCHEMA,
    PREFIX_COUNT,
    PRODUCTION_SCHEMA,
    RESULT_SCHEMA,
    RUNNER_VERSION,
    SHELLS,
    parse_key_value_output,
    partition_audit,
    prefix_cells,
    require_nonnegative_integer,
    shard_id,
    workload_audit,
)


HERE = Path(__file__).resolve().parent
CPP = HERE / "dense_shell_classifier_pilot.cpp"
DEFAULT_OUTPUT = HERE / "output" / "production"
MAX_WORKERS = 8
MAX_AGGREGATE_CHILD_RSS_MIB = 3_072
BUILD_FLAGS = (
    "-O3",
    "-DNDEBUG",
    "-std=c++20",
    "-Wall",
    "-Wextra",
    "-Wpedantic",
    "-Werror",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def compile_once(
    output: Path,
) -> tuple[Path, str, str, list[str], dict[str, object]]:
    source_hash = sha256(CPP)
    compiler_name = os.environ.get("CXX", "clang++")
    compiler_path = shutil.which(compiler_name)
    if compiler_path is None:
        raise RuntimeError(f"compiler not found: {compiler_name}")
    compiler_path = str(Path(compiler_path).resolve())
    version = subprocess.run(
        [compiler_path, "--version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    provenance = {
        "compiler_path": compiler_path,
        "compiler_version": version,
        "flags": list(BUILD_FLAGS),
    }
    cache_material = json.dumps(
        {
            "source_sha256": source_hash,
            **provenance,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    build_key = hashlib.sha256(cache_material).hexdigest()
    binary = output / "bin" / f"dense-shell-{build_key[:20]}"
    binary.parent.mkdir(parents=True, exist_ok=True)
    build_command = [
        compiler_path,
        *BUILD_FLAGS,
        str(CPP),
        "-o",
        str(binary),
    ]
    if not binary.exists():
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{binary.name}.", suffix=".tmp", dir=binary.parent
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        actual_command = [*build_command[:-1], str(temporary)]
        try:
            completed = subprocess.run(
                actual_command,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if completed.returncode:
                raise RuntimeError(
                    "production compile failed:\n" + completed.stdout
                )
            temporary.chmod(0o755)
            os.replace(temporary, binary)
        finally:
            temporary.unlink(missing_ok=True)
    provenance["cache_key_sha256"] = build_key
    return (
        binary,
        source_hash,
        sha256(binary),
        build_command,
        provenance,
    )


def command_for(
    binary: Path, shell: str, first: int, second: int
) -> list[str]:
    return [
        str(binary),
        "--shell",
        shell,
        "--complete-shard",
        "--prefix",
        str(first),
        str(second),
    ]


def expected_manifest(
    output: Path,
    binary: Path,
    source_hash: str,
    binary_hash: str,
    build_command: list[str],
    build_provenance: dict[str, object],
) -> dict[str, object]:
    return {
        "schema": MANIFEST_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "created_utc": None,
        "source_path": str(CPP),
        "source_sha256": source_hash,
        "binary_path": str(binary),
        "binary_sha256": binary_hash,
        "build_command": build_command,
        "build_provenance": build_provenance,
        "build_output_policy": (
            "command shown with final output path; compilation is written "
            "to an adjacent temporary file and atomically renamed"
        ),
        "production_command_template": [
            str(binary),
            "--shell",
            "{h1|h0}",
            "--complete-shard",
            "--prefix",
            "{0..26}",
            "{0..26}",
        ],
        "memory_policy": {
            "max_workers": MAX_WORKERS,
            "max_aggregate_child_rss_mib":
                MAX_AGGREGATE_CHILD_RSS_MIB,
            "mechanism": (
                "parent polls resident memory and terminates its child "
                "pool before the aggregate reaches 4 GiB; Darwin "
                "RLIMIT_AS is deliberately not used"
            ),
        },
        "result_directory": str(output / "results"),
        "expected_shards": {
            shell: [
                cell.identifier for cell in prefix_cells(shell)
            ]
            for shell in SHELLS
        },
        "partition_audit": partition_audit(),
        "workload_audit": workload_audit(),
    }


def prepare_manifest(
    output: Path,
    binary: Path,
    source_hash: str,
    binary_hash: str,
    build_command: list[str],
    build_provenance: dict[str, object],
) -> dict[str, object]:
    path = output / "manifest.json"
    expected = expected_manifest(
        output,
        binary,
        source_hash,
        binary_hash,
        build_command,
        build_provenance,
    )
    if path.exists():
        actual = read_json(path)
        comparison = dict(actual)
        comparison["created_utc"] = None
        if comparison != expected:
            raise RuntimeError(
                f"{path} does not match this source/binary/audit; "
                "use a fresh output directory"
            )
        return actual
    expected["created_utc"] = utc_now()
    atomic_json(path, expected)
    return expected


def validate_result(
    result: object,
    *,
    shell: str,
    first: int,
    second: int,
    source_hash: str,
    binary_hash: str,
    command: list[str],
) -> dict[str, object]:
    if not isinstance(result, dict):
        raise ValueError("result is not a JSON object")
    identifier = shard_id(shell, first, second)
    expected_fields = {
        "schema": RESULT_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "shard_id": identifier,
        "shell": shell,
        "prefix_first": first,
        "prefix_second": second,
        "source_sha256": source_hash,
        "binary_sha256": binary_hash,
        "command": command,
        "returncode": 0,
        "complete": True,
        "candidate": False,
    }
    for key, expected in expected_fields.items():
        if result.get(key) != expected:
            raise ValueError(
                f"{identifier}: {key} mismatch "
                f"({result.get(key)!r} != {expected!r})"
            )
    parsed = result.get("parsed")
    if not isinstance(parsed, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in parsed.items()
    ):
        raise ValueError(f"{identifier}: malformed parsed output")
    required_text = {
        "schema": PRODUCTION_SCHEMA,
        "mode": "complete_shard",
        "shell": shell,
        "shard_id": identifier,
        "prefix_first": str(first),
        "prefix_second": str(second),
        "upper_exact_scope": "char2_mod9_intersection",
        "shard_complete": "1",
        "witness_exact_present": "0",
    }
    for key, expected in required_text.items():
        if parsed.get(key) != expected:
            raise ValueError(
                f"{identifier}: output {key} mismatch "
                f"({parsed.get(key)!r} != {expected!r})"
            )
    if require_nonnegative_integer(parsed, "exact_zero_hits"):
        raise ValueError(f"{identifier}: complete result contains exact hit")
    return result


@dataclass(frozen=True)
class Job:
    shell: str
    first: int
    second: int
    result_path: Path
    command: list[str]
    workload_proxy: int

    @property
    def identifier(self) -> str:
        return shard_id(self.shell, self.first, self.second)


@dataclass
class Active:
    job: Job
    process: subprocess.Popen[bytes]
    transcript: Path
    started: float


def aggregate_child_rss_mib(active: dict[int, Active]) -> float:
    if not active:
        return 0.0
    completed = subprocess.run(
        [
            "/bin/ps",
            "-o",
            "rss=",
            "-p",
            ",".join(str(pid) for pid in sorted(active)),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in (0, 1):
        raise RuntimeError(
            "could not audit child RSS: " + completed.stderr.strip()
        )
    kib = sum(
        int(line.strip())
        for line in completed.stdout.splitlines()
        if line.strip()
    )
    return kib / 1024.0


def cleanup_active(active: dict[int, Active]) -> None:
    for item in active.values():
        if item.process.poll() is None:
            item.process.terminate()
    for item in active.values():
        try:
            item.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            item.process.kill()
            item.process.wait()
        item.transcript.unlink(missing_ok=True)
    active.clear()


def classify_transcript(
    active: Active,
    source_hash: str,
    binary_hash: str,
) -> tuple[dict[str, object], bool]:
    output = active.transcript.read_text(
        encoding="utf-8", errors="replace"
    )
    parsed = parse_key_value_output(output)
    candidate = (
        active.process.returncode == 2
        and parsed.get("shard_complete") == "0"
        and parsed.get("witness_exact_present") == "1"
        and require_nonnegative_integer(parsed, "exact_zero_hits") > 0
    )
    result = {
        "schema": RESULT_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "recorded_utc": utc_now(),
        "shard_id": active.job.identifier,
        "shell": active.job.shell,
        "prefix_first": active.job.first,
        "prefix_second": active.job.second,
        "source_sha256": source_hash,
        "binary_sha256": binary_hash,
        "command": active.job.command,
        "returncode": active.process.returncode,
        "complete": active.process.returncode == 0,
        "candidate": candidate,
        "wall_seconds_runner": time.monotonic() - active.started,
        "parsed": parsed,
        "transcript": output,
    }
    return result, candidate


def selected_shells(value: str) -> tuple[str, ...]:
    return SHELLS if value == "both" else (value,)


def parse_args() -> argparse.Namespace:
    default_workers = min(
        MAX_WORKERS, max(1, (os.cpu_count() or 2) - 2)
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT
    )
    parser.add_argument(
        "--shell", choices=("both", *SHELLS), default="both"
    )
    parser.add_argument(
        "--workers", type=int, default=default_workers
    )
    parser.add_argument(
        "--aggregate-rss-limit-mib",
        type=int,
        default=MAX_AGGREGATE_CHILD_RSS_MIB,
    )
    parser.add_argument(
        "--max-shards",
        type=int,
        help="bounded runner validation; omit for every missing shard",
    )
    parser.add_argument(
        "--prefix",
        nargs=2,
        type=int,
        metavar=("FIRST", "SECOND"),
        help="run only one prefix (requires --shell h1 or h0)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="compile/audit/list missing shards without searching",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if not (1 <= args.workers <= MAX_WORKERS):
        raise SystemExit(f"--workers must lie in [1,{MAX_WORKERS}]")
    if not (
        128
        <= args.aggregate_rss_limit_mib
        <= MAX_AGGREGATE_CHILD_RSS_MIB
    ):
        raise SystemExit(
            "--aggregate-rss-limit-mib must lie in "
            f"[128,{MAX_AGGREGATE_CHILD_RSS_MIB}]"
        )
    if args.max_shards is not None and args.max_shards < 0:
        raise SystemExit("--max-shards must be nonnegative")
    if args.prefix is not None:
        if args.shell == "both":
            raise SystemExit("--prefix requires --shell h1 or h0")
        if any(not 0 <= value < 27 for value in args.prefix):
            raise SystemExit("--prefix indices must lie in [0,26]")

    output.mkdir(parents=True, exist_ok=True)
    (
        binary,
        source_hash,
        binary_hash,
        build_command,
        build_provenance,
    ) = compile_once(output)
    prepare_manifest(
        output,
        binary,
        source_hash,
        binary_hash,
        build_command,
        build_provenance,
    )

    candidate_directory = output / "candidates"
    existing_candidates = sorted(candidate_directory.glob("*.json"))
    if existing_candidates:
        raise SystemExit(
            "candidate record already exists; investigate before "
            f"resuming: {existing_candidates[0]}"
        )

    jobs: list[Job] = []
    completed = 0
    for shell in selected_shells(args.shell):
        for cell in prefix_cells(shell):
            if args.prefix is not None and (
                cell.first,
                cell.second,
            ) != tuple(args.prefix):
                continue
            path = output / "results" / f"{cell.identifier}.json"
            command = command_for(
                binary, shell, cell.first, cell.second
            )
            if path.exists():
                try:
                    validate_result(
                        read_json(path),
                        shell=shell,
                        first=cell.first,
                        second=cell.second,
                        source_hash=source_hash,
                        binary_hash=binary_hash,
                        command=command,
                    )
                except (ValueError, OSError, json.JSONDecodeError) as error:
                    raise SystemExit(
                        f"refusing to overwrite invalid result {path}: "
                        f"{error}"
                    ) from error
                completed += 1
            else:
                jobs.append(
                    Job(
                        shell=shell,
                        first=cell.first,
                        second=cell.second,
                        result_path=path,
                        command=command,
                        workload_proxy=cell.raw_decorations,
                    )
                )

    jobs.sort(
        key=lambda job: (
            -job.workload_proxy,
            job.shell,
            job.first,
            job.second,
        )
    )
    if args.max_shards is not None:
        jobs = jobs[: args.max_shards]
    print(
        f"hash-pinned manifest ready; {completed} already complete, "
        f"{len(jobs)} selected missing shards, "
        f"{args.workers} workers, aggregate child RSS stop at "
        f"{args.aggregate_rss_limit_mib} MiB"
    )
    if args.dry_run or not jobs:
        return 0

    temporary_directory = output / "tmp"
    temporary_directory.mkdir(parents=True, exist_ok=True)
    active: dict[int, Active] = {}
    next_job = 0
    failure = False
    candidate_found = False
    last_rss_check = 0.0
    try:
        while next_job < len(jobs) or active:
            while (
                not failure
                and not candidate_found
                and next_job < len(jobs)
                and len(active) < args.workers
            ):
                job = jobs[next_job]
                next_job += 1
                descriptor, name = tempfile.mkstemp(
                    prefix=f".{job.identifier}.",
                    suffix=".transcript",
                    dir=temporary_directory,
                )
                transcript = Path(name)
                stream = os.fdopen(descriptor, "wb")
                try:
                    process = subprocess.Popen(
                        job.command,
                        stdout=stream,
                        stderr=subprocess.STDOUT,
                    )
                except BaseException:
                    transcript.unlink(missing_ok=True)
                    raise
                finally:
                    stream.close()
                active[process.pid] = Active(
                    job=job,
                    process=process,
                    transcript=transcript,
                    started=time.monotonic(),
                )

            now = time.monotonic()
            if active and now - last_rss_check >= 0.5:
                rss_mib = aggregate_child_rss_mib(active)
                last_rss_check = now
                if rss_mib > args.aggregate_rss_limit_mib:
                    raise RuntimeError(
                        "aggregate child RSS safety stop: "
                        f"{rss_mib:.1f} MiB > "
                        f"{args.aggregate_rss_limit_mib} MiB"
                    )

            finished = [
                pid
                for pid, item in active.items()
                if item.process.poll() is not None
            ]
            if not finished:
                time.sleep(0.1)
                continue

            for pid in finished:
                item = active.pop(pid)
                try:
                    record, candidate = classify_transcript(
                        item, source_hash, binary_hash
                    )
                    if candidate:
                        candidate_path = (
                            candidate_directory
                            / f"{item.job.identifier}.json"
                        )
                        atomic_json(candidate_path, record)
                        candidate_found = True
                        print(
                            "EXACT-ZERO CANDIDATE: stopped shard and "
                            "saved detached witness to "
                            f"{candidate_path}",
                            file=sys.stderr,
                        )
                        continue
                    if item.process.returncode:
                        failure = True
                        failure_path = (
                            output
                            / "failures"
                            / (
                                f"{item.job.identifier}-"
                                f"{time.time_ns()}.json"
                            )
                        )
                        atomic_json(failure_path, record)
                        print(
                            f"shard failed; retained {failure_path}",
                            file=sys.stderr,
                        )
                        continue
                    validate_result(
                        record,
                        shell=item.job.shell,
                        first=item.job.first,
                        second=item.job.second,
                        source_hash=source_hash,
                        binary_hash=binary_hash,
                        command=item.job.command,
                    )
                    atomic_json(item.job.result_path, record)
                    print(f"complete {item.job.identifier}")
                except BaseException:
                    failure = True
                    raise
                finally:
                    item.transcript.unlink(missing_ok=True)

            if candidate_found:
                return 2

        return 1 if failure else 0
    finally:
        cleanup_active(active)


if __name__ == "__main__":
    raise SystemExit(main())

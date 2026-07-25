#!/usr/bin/env python3
"""Run a resumable, RSS-guarded case-26 quotient census in atomic ranges."""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

import verify_global_quotient_plan as plan


HERE = Path(__file__).resolve().parent
CORE_SOURCE = HERE / "benchmark_global_quotient.cpp"
PRODUCTION_SOURCE = HERE / "global_quotient_census.cpp"
SCHEMA = "h668-case26-global-quotient-production-v1"
RANGE_SCHEMA = "h668-case26-global-quotient-range-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def producer_sources_sha256() -> str:
    digest = hashlib.sha256()
    for path in (CORE_SOURCE, PRODUCTION_SOURCE):
        digest.update(path.name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def atomic_write(path: Path, content: bytes, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if executable:
            temporary.chmod(0o755)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_json(path: Path, payload: dict[str, object]) -> None:
    atomic_write(
        path,
        (
            json.dumps(payload, indent=2, sort_keys=True) + "\n"
        ).encode(),
    )


def output_bytes(root: Path) -> int:
    return sum(
        path.stat().st_size
        for path in root.rglob("*")
        if path.is_file()
    )


def compile_binary(target: Path) -> tuple[list[str], str]:
    compiler = shutil.which("clang++")
    if compiler is None:
        raise RuntimeError("clang++ is required")
    command = [
        compiler,
        "-O3",
        "-DNDEBUG",
        "-std=c++20",
        "-Wall",
        "-Wextra",
        "-pedantic",
        str(PRODUCTION_SOURCE),
        "-o",
    ]
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=target.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        subprocess.run(
            command + [str(temporary)],
            check=True,
            capture_output=True,
            text=True,
        )
        temporary.chmod(0o755)
        binary_sha = sha256_file(temporary)
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    return command + ["<atomic-target>"], binary_sha


def expected_ranges(
    start: int, stop: int, chunk_size: int
) -> list[tuple[int, int]]:
    return [
        (left, min(chunk_size, stop - left))
        for left in range(start, stop, chunk_size)
    ]


def range_path(root: Path, start: int, states: int) -> Path:
    return (
        root
        / "ranges"
        / f"range_{start:06d}_{start + states:06d}.json"
    )


def validate_range(
    payload: dict[str, object],
    start: int,
    states: int,
    source_sha: str,
    model_sha: str,
    reflection_gauge: bool,
) -> None:
    expected = {
        "schema": RANGE_SCHEMA,
        "status": "complete",
        "case": 26,
        "block": "S",
        "q_index": 12,
        "start": start,
        "states": states,
        "stop": start + states,
        "central_values_per_state": 2,
        "reflection_gauge": reflection_gauge,
        "join_rows": states
        * (
            ((1 << 19) if reflection_gauge else (1 << 20))
            + (1 << 18)
        )
        * 2,
        "producer_sources_sha256": source_sha,
        "model_sha256": model_sha,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise RuntimeError(
                f"range {start} has invalid {key}: "
                f"{payload.get(key)!r} != {value!r}"
            )
    survivors = payload.get("joint_mod6_supports")
    if not isinstance(survivors, int) or survivors < 0:
        raise RuntimeError(f"range {start} has invalid survivor count")
    for key in (
        "integer_polynomial_checks",
        "bitpacked_physical_replays",
    ):
        if payload.get(key) != survivors:
            raise RuntimeError(
                f"range {start} did not replay every survivor"
            )
    representatives = payload.get("joined_representatives")
    reflected = payload.get("reconstructed_reflection_mates")
    if reflection_gauge:
        if (
            not isinstance(representatives, int)
            or representatives * 2 != survivors
            or reflected != representatives
        ):
            raise RuntimeError(
                f"range {start} has invalid reflection-orbit counts"
            )
    elif representatives != survivors or reflected != 0:
        raise RuntimeError(
            f"range {start} has invalid ungauged counts"
        )
    for key in ("survivor_stream_sha256",):
        value = payload.get(key)
        if (
            not isinstance(value, str)
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise RuntimeError(f"range {start} has invalid {key}")
    exact = payload.get("exact_integer_supports")
    candidates = payload.get("exact_candidates")
    if (
        not isinstance(exact, int)
        or exact < 0
        or not isinstance(candidates, list)
        or len(candidates) != exact
    ):
        raise RuntimeError(
            f"range {start} has inconsistent exact candidates"
        )


def child_rss_mib(processes: list[subprocess.Popen]) -> float:
    pids = [str(process.pid) for process in processes if process.poll() is None]
    if not pids:
        return 0.0
    result = subprocess.run(
        ["ps", "-o", "rss=", "-p", ",".join(pids)],
        check=True,
        capture_output=True,
        text=True,
    )
    return sum(int(line.strip()) for line in result.stdout.splitlines()) / 1024


def prepare(args: argparse.Namespace) -> tuple[dict[str, object], Path, Path]:
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=True)
    model_path = root / "case26-model.bin"
    binary_path = root / "global_quotient_census"
    config_path = root / "RUN_CONFIG.json"

    result = plan.derive()
    encoded_model = plan.model_bytes(result)
    model_sha = hashlib.sha256(encoded_model).hexdigest()
    source_sha = producer_sources_sha256()
    ranges = expected_ranges(args.start, args.stop, args.chunk_size)
    desired = {
        "schema": SCHEMA,
        "case": 26,
        "block": "S",
        "q_index": 12,
        "quotient_dimension": 18,
        "start": args.start,
        "stop": args.stop,
        "chunk_size": args.chunk_size,
        "range_count": len(ranges),
        "reflection_gauge": not args.ungauged,
        "producer_sources_sha256": source_sha,
        "core_source_sha256": sha256_file(CORE_SOURCE),
        "production_source_sha256": sha256_file(PRODUCTION_SOURCE),
        "model_sha256": model_sha,
        "model_bytes": len(encoded_model),
        "model_generator_sha256": sha256_file(
            HERE / "verify_global_quotient_plan.py"
        ),
        "runner_sha256": sha256_file(Path(__file__).resolve()),
    }

    if model_path.exists():
        if sha256_file(model_path) != model_sha:
            raise RuntimeError("existing model does not match current derivation")
    else:
        atomic_write(model_path, encoded_model)

    if config_path.exists():
        pinned = json.loads(config_path.read_text())
        for key, value in desired.items():
            if pinned.get(key) != value:
                raise RuntimeError(
                    f"run configuration pin changed at {key}"
                )
        if not binary_path.exists():
            _, binary_sha = compile_binary(binary_path)
            if binary_sha != pinned.get("binary_sha256"):
                raise RuntimeError(
                    "recompiled binary differs from the pinned binary"
                )
        elif sha256_file(binary_path) != pinned.get("binary_sha256"):
            raise RuntimeError("existing binary hash differs from the pin")
        config = pinned
    else:
        compile_command, binary_sha = compile_binary(binary_path)
        config = {
            **desired,
            "binary_sha256": binary_sha,
            "compile_command": compile_command,
        }
        atomic_json(config_path, config)
    return config, model_path, binary_path


def terminate_all(processes: dict[subprocess.Popen, tuple[int, int]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()
    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def run(args: argparse.Namespace) -> None:
    config, model_path, binary_path = prepare(args)
    root = args.output.resolve()
    source_sha = str(config["producer_sources_sha256"])
    model_sha = str(config["model_sha256"])
    reflection_gauge = bool(config["reflection_gauge"])
    pending: deque[tuple[int, int]] = deque()
    completed = 0
    for start, states in expected_ranges(
        args.start, args.stop, args.chunk_size
    ):
        path = range_path(root, start, states)
        if path.exists():
            payload = json.loads(path.read_text())
            validate_range(
                payload,
                start,
                states,
                source_sha,
                model_sha,
                reflection_gauge,
            )
            completed += 1
        else:
            pending.append((start, states))
    if args.max_ranges is not None:
        pending = deque(list(pending)[: args.max_ranges])
    if args.prepare_only:
        print(
            json.dumps(
                {
                    "status": "prepared",
                    "completed_ranges": completed,
                    "pending_ranges_selected": len(pending),
                    "output": str(root),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    running: dict[subprocess.Popen, tuple[int, int]] = {}
    newly_completed = 0
    try:
        while pending or running:
            while pending and len(running) < args.workers:
                start, states = pending.popleft()
                command = [
                    str(binary_path),
                    str(model_path),
                    "--start",
                    str(start),
                    "--states",
                    str(states),
                    "--source-sha",
                    source_sha,
                    "--model-sha",
                    model_sha,
                    "--mode",
                    "gauged" if reflection_gauge else "ungauged",
                ]
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                running[process] = (start, states)

            rss = child_rss_mib(list(running))
            if rss > args.rss_limit_mib:
                raise RuntimeError(
                    f"aggregate child RSS {rss:.1f} MiB exceeds "
                    f"{args.rss_limit_mib:.1f} MiB"
                )
            finished = [
                process
                for process in running
                if process.poll() is not None
            ]
            if not finished:
                time.sleep(0.1)
                continue
            for process in finished:
                start, states = running.pop(process)
                stdout, stderr = process.communicate()
                if process.returncode != 0:
                    raise RuntimeError(
                        f"range {start} failed: {stderr.strip()}"
                    )
                try:
                    payload = json.loads(stdout)
                except json.JSONDecodeError as error:
                    raise RuntimeError(
                        f"range {start} emitted invalid JSON: {error}"
                    ) from error
                validate_range(
                    payload,
                    start,
                    states,
                    source_sha,
                    model_sha,
                    reflection_gauge,
                )
                atomic_json(range_path(root, start, states), payload)
                newly_completed += 1
                if output_bytes(root) > args.output_limit_mib * (1 << 20):
                    raise RuntimeError(
                        "output-size guard exceeded after a range commit"
                    )
    except BaseException:
        terminate_all(running)
        raise

    print(
        json.dumps(
            {
                "status": "complete"
                if not any(
                    not range_path(root, start, states).exists()
                    for start, states in expected_ranges(
                        args.start, args.stop, args.chunk_size
                    )
                )
                else "partial",
                "previously_completed_ranges": completed,
                "newly_completed_ranges": newly_completed,
                "output_bytes": output_bytes(root),
                "output": str(root),
            },
            indent=2,
            sort_keys=True,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int, default=1 << 18)
    parser.add_argument("--chunk-size", type=int, default=1024)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--rss-limit-mib", type=float, default=8192)
    parser.add_argument("--output-limit-mib", type=float, default=100)
    parser.add_argument("--max-ranges", type=int)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument(
        "--ungauged",
        action="store_true",
        help="retain the full 20+18 join as a validation control",
    )
    args = parser.parse_args()
    if not 0 <= args.start < args.stop <= 1 << 18:
        parser.error("require 0 <= start < stop <= 2^18")
    if args.chunk_size < 1:
        parser.error("chunk size must be positive")
    if not 1 <= args.workers <= 8:
        parser.error("workers must lie in 1,...,8")
    if args.rss_limit_mib <= 0 or args.output_limit_mib <= 0:
        parser.error("resource limits must be positive")
    if args.max_ranges is not None and args.max_ranges < 1:
        parser.error("max ranges must be positive")
    return args


if __name__ == "__main__":
    run(parse_args())

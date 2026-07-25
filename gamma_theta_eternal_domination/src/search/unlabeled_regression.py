"""Resumable A/B regression on one canonical ``geng`` shard."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path

from search.differential import compare_graph


NAUTY_ARCHIVE_SHA256 = (
    "9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b"
)


def _atomic_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _summary(
    *,
    status: str,
    configuration: dict[str, object],
    processed: int,
    digest: hashlib._Hash,
    counters: Counter[str],
    histogram: Counter[tuple[int, int, int, int, int]],
    started_wall: float,
    started_counter: float,
    last_record: str | None,
    generator_stderr: str = "",
) -> dict[str, object]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "status": status,
        "configuration": configuration,
        "processed": processed,
        "last_graph6": last_record,
        "graph_stream_sha256_prefix": digest.hexdigest(),
        "counters": dict(sorted(counters.items())),
        "parameter_histogram": {
            ",".join(map(str, key)): value
            for key, value in sorted(histogram.items())
        },
        "started_unix": started_wall,
        "updated_unix": time.time(),
        "wall_seconds_this_process": time.perf_counter() - started_counter,
        "user_cpu_seconds_this_process": usage.ru_utime,
        "system_cpu_seconds_this_process": usage.ru_stime,
        "maximum_resident_set_size_raw": usage.ru_maxrss,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "nauty_archive_sha256": NAUTY_ARCHIVE_SHA256,
        "generator_stderr": generator_stderr,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--residue", type=int, default=0)
    parser.add_argument("--modulus", type=int, default=1)
    parser.add_argument("--geng", type=Path, required=True)
    parser.add_argument("--checkpoint-every", type=int, default=100)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--optimum-only",
        action="store_true",
        help="compare parameters but not greatest families at every k",
    )
    arguments = parser.parse_args()
    if arguments.order < 1:
        raise SystemExit("connected graph order must be positive")
    if arguments.modulus < 1 or not 0 <= arguments.residue < arguments.modulus:
        raise SystemExit("require 0 <= residue < modulus")
    if not arguments.geng.is_file():
        raise SystemExit(f"geng not found: {arguments.geng}")

    command = [
        str(arguments.geng.resolve()),
        "-cq",
        str(arguments.order),
        f"{arguments.residue}/{arguments.modulus}",
    ]
    configuration: dict[str, object] = {
        "order": arguments.order,
        "residue": arguments.residue,
        "modulus": arguments.modulus,
        "generator_command": command,
        "connected_only": True,
        "check_all_guard_counts": not arguments.optimum_only,
    }

    resume_at = 0
    resumed_counters: Counter[str] = Counter()
    resumed_histogram: Counter[tuple[int, int, int, int, int]] = Counter()
    if arguments.checkpoint.exists():
        with arguments.checkpoint.open(encoding="utf-8") as handle:
            previous = json.load(handle)
        if previous.get("configuration") != configuration:
            raise SystemExit("checkpoint configuration does not match this run")
        if previous.get("status") != "complete":
            resume_at = int(previous.get("processed", 0))
            resumed_counters.update(previous.get("counters", {}))
            for key, value in previous.get("parameter_histogram", {}).items():
                parsed = tuple(int(item) for item in key.split(","))
                if len(parsed) != 5:
                    raise SystemExit("malformed checkpoint histogram")
                resumed_histogram[parsed] = int(value)

    started_wall = time.time()
    started_counter = time.perf_counter()
    digest = hashlib.sha256()
    counters: Counter[str] = resumed_counters
    histogram: Counter[tuple[int, int, int, int, int]] = resumed_histogram
    processed = 0
    last_record: str | None = None
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="ascii",
    )
    assert process.stdout is not None
    try:
        for index, line in enumerate(process.stdout):
            record = line.strip()
            if not record:
                continue
            digest.update(record.encode("ascii") + b"\n")
            last_record = record
            if index < resume_at:
                processed = index + 1
                continue
            parameters = compare_graph(
                record, check_all_guard_counts=not arguments.optimum_only
            )
            gamma, independent_domination, independence, gamma_inf, cover = (
                parameters
            )
            if not (
                gamma
                <= independent_domination
                <= independence
                <= gamma_inf
                <= cover
            ):
                raise AssertionError(("parameter chain", record, parameters))
            histogram[parameters] += 1
            counters["graphs"] += 1
            counters["gamma_equals_alpha"] += gamma == independence
            counters["gamma_equals_gamma_infinity"] += gamma == gamma_inf
            counters["gamma_infinity_less_than_theta"] += gamma_inf < cover
            counters["alpha_equals_gamma_infinity_less_than_theta"] += (
                independence == gamma_inf < cover
            )
            counters["gamma_equals_gamma_infinity_less_than_theta"] += (
                gamma == gamma_inf < cover
            )
            counters["gamma_equals_gamma_infinity_equals_theta"] += (
                gamma == gamma_inf == cover
            )
            processed = index + 1
            if counters["graphs"] % arguments.checkpoint_every == 0:
                _atomic_json(
                    arguments.checkpoint,
                    _summary(
                        status="running",
                        configuration=configuration,
                        processed=processed,
                        digest=digest,
                        counters=counters,
                        histogram=histogram,
                        started_wall=started_wall,
                        started_counter=started_counter,
                        last_record=last_record,
                    ),
                )
    except BaseException:
        process.terminate()
        process.wait()
        _atomic_json(
            arguments.checkpoint,
            _summary(
                status="failed",
                configuration=configuration,
                processed=processed,
                digest=digest,
                counters=counters,
                histogram=histogram,
                started_wall=started_wall,
                started_counter=started_counter,
                last_record=last_record,
            ),
        )
        raise

    stderr = process.stderr.read() if process.stderr is not None else ""
    return_code = process.wait()
    if return_code != 0:
        raise SystemExit(f"geng exited {return_code}: {stderr}")
    result = _summary(
        status="complete",
        configuration=configuration,
        processed=processed,
        digest=digest,
        counters=counters,
        histogram=histogram,
        started_wall=started_wall,
        started_counter=started_counter,
        last_record=last_record,
        generator_stderr=stderr,
    )
    result["graph_stream_sha256"] = result.pop("graph_stream_sha256_prefix")
    result["outcome"] = "all A/B comparisons agreed"
    _atomic_json(arguments.checkpoint, result)
    _atomic_json(arguments.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

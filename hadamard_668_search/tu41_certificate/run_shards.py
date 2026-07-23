#!/usr/bin/env python3
"""Run deterministic TU enumeration shards serially and resumably."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def read_cubes(path: Path) -> list[str]:
    cubes: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.removeprefix("cube=").strip()
        if line and set(line) <= {"0", "1"}:
            cubes.append(line)
    if not cubes:
        raise ValueError("cube file contains no binary prefixes")
    if len(cubes) != len(set(cubes)):
        raise ValueError("cube file contains duplicate prefixes")
    lengths = {len(cube) for cube in cubes}
    if len(lengths) != 1:
        raise ValueError("cube prefixes do not all have the same length")
    return cubes


def parse_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in output.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        parsed[key] = value
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--enumerator", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cubes", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--bounds-depth", type=int, default=14)
    parser.add_argument("--seconds-per-shard", type=float, default=0.0)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    enumerator = args.enumerator.resolve()
    source = args.source.resolve()
    cubes_path = args.cubes.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    source_digest = sha256(source)
    binary_digest = sha256(enumerator)
    cubes_digest = sha256(cubes_path)
    cubes = read_cubes(cubes_path)
    end = len(cubes) if args.end is None else min(args.end, len(cubes))
    if not (0 <= args.start <= end):
        raise SystemExit("invalid shard range")

    completed = 0
    skipped = 0
    started = time.monotonic()
    for index in range(args.start, end):
        cube = cubes[index]
        report_path = output_dir / f"shard_{index:04d}_{cube}.json"
        if report_path.exists():
            try:
                old = json.loads(report_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                old = {}
            if (
                old.get("source_sha256") == source_digest
                and old.get("cube_file_sha256") == cubes_digest
                and old.get("enumerator_sha256") == binary_digest
                and old.get("cube") == cube
                and old.get("parsed", {}).get("complete") == "true"
                and old.get("parsed", {}).get("solutions") == "0"
                and old.get("parsed", {}).get("prefix") == cube
                and old.get("returncode") == 20
            ):
                skipped += 1
                print(
                    f"[{index + 1}/{end}] skip verified-empty {cube}",
                    flush=True,
                )
                continue

        command = [
            str(enumerator),
            "--n",
            "41",
            "--prefix",
            cube,
            "--bounds-depth",
            str(args.bounds_depth),
        ]
        if args.seconds_per_shard > 0:
            command += ["--seconds", str(args.seconds_per_shard)]
        shard_started = time.monotonic()
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        elapsed = time.monotonic() - shard_started
        parsed = parse_output(result.stdout)
        report = {
            "schema": "tu41-outside-in-shard-v1",
            "index": index,
            "cube": cube,
            "cube_file": cubes_path.name,
            "cube_file_sha256": cubes_digest,
            "source_file": source.name,
            "source_sha256": source_digest,
            "enumerator_sha256": binary_digest,
            "command": command,
            "returncode": result.returncode,
            "wall_seconds": elapsed,
            "parsed": parsed,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_dir,
            prefix=report_path.name + ".",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            json.dump(report, temporary, indent=2, sort_keys=True)
            temporary.write("\n")
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, report_path)

        empty = (
            result.returncode == 20
            and parsed.get("complete") == "true"
            and parsed.get("solutions") == "0"
            and parsed.get("prefix") == cube
        )
        print(
            f"[{index + 1}/{end}] cube={cube} rc={result.returncode} "
            f"nodes={parsed.get('nodes', '?')} wall={elapsed:.3f}s "
            f"empty={str(empty).lower()}",
            flush=True,
        )
        if not empty:
            print(result.stdout, end="")
            print(result.stderr, end="")
            return 1
        completed += 1

    print(
        f"PASS shards={end - args.start} completed={completed} skipped={skipped} "
        f"wall_seconds={time.monotonic() - started:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

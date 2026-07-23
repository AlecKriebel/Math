#!/usr/bin/env python3
"""Strictly validate TU(41) shard reports and write one summary manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


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
        if line:
            cubes.append(line)
    if any(len(cube) != 19 or set(cube) - {"0", "1"} for cube in cubes):
        raise AssertionError("malformed cube")
    if len(cubes) != len(set(cubes)):
        raise AssertionError("duplicate cube")
    return cubes


def require_equal(report: dict[str, Any], key: str, expected: Any) -> None:
    actual = report.get(key)
    if actual != expected:
        raise AssertionError(f"{key}: expected {expected!r}, got {actual!r}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--enumerator", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cubes", type=Path, required=True)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--index-output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    enumerator = args.enumerator.resolve()
    source = args.source.resolve()
    cubes_path = args.cubes.resolve()
    reports_path = args.reports.resolve()
    cubes = read_cubes(cubes_path)
    source_digest = sha256(source)
    binary_digest = sha256(enumerator)
    cubes_digest = sha256(cubes_path)

    report_files = sorted(reports_path.glob("shard_*.json"))
    if len(report_files) != len(cubes):
        raise AssertionError(
            f"expected {len(cubes)} report files, found {len(report_files)}"
        )

    total_nodes = 0
    total_reported_wall = 0.0
    maximum_reported_wall = 0.0
    report_hash_chain = hashlib.sha256()
    shard_index_records: list[dict[str, Any]] = []
    expected_paths: set[Path] = set()
    for index, cube in enumerate(cubes):
        report_path = reports_path / f"shard_{index:04d}_{cube}.json"
        expected_paths.add(report_path)
        report = json.loads(report_path.read_text(encoding="utf-8"))
        require_equal(report, "schema", "tu41-outside-in-shard-v1")
        require_equal(report, "index", index)
        require_equal(report, "cube", cube)
        require_equal(report, "cube_file_sha256", cubes_digest)
        require_equal(report, "source_sha256", source_digest)
        require_equal(report, "enumerator_sha256", binary_digest)
        require_equal(report, "returncode", 20)

        parsed = report.get("parsed")
        if not isinstance(parsed, dict):
            raise AssertionError(f"report {index} has no parsed result")
        expected_parsed = {
            "n": "41",
            "primary_variables": "78",
            "steps": "20",
            "prefix": cube,
            "complete": "true",
            "solutions": "0",
            "emitted_prefixes": "0",
        }
        for key, expected in expected_parsed.items():
            require_equal(parsed, key, expected)
        nodes = int(parsed["nodes"])
        if nodes <= 0:
            raise AssertionError(f"report {index} has invalid node count")
        nodes_by_depth = [int(value) for value in parsed["nodes_by_depth"].split(",")]
        if len(nodes_by_depth) != 21 or sum(nodes_by_depth) != nodes:
            raise AssertionError(f"report {index} has inconsistent depth counts")

        wall = float(report["wall_seconds"])
        if wall < 0:
            raise AssertionError(f"report {index} has negative wall time")
        total_nodes += nodes
        total_reported_wall += wall
        maximum_reported_wall = max(maximum_reported_wall, wall)
        report_digest = sha256(report_path)
        report_hash_chain.update(index.to_bytes(4, "big"))
        report_hash_chain.update(bytes.fromhex(report_digest))
        shard_index_records.append(
            {
                "index": index,
                "cube": cube,
                "report_sha256": report_digest,
                "nodes": nodes,
                "nodes_by_depth": nodes_by_depth,
                "enumerator_elapsed_seconds": float(parsed["elapsed_seconds"]),
                "runner_wall_seconds": wall,
            }
        )

    if set(report_files) != expected_paths:
        unexpected = set(report_files) - expected_paths
        missing = expected_paths - set(report_files)
        raise AssertionError(
            f"report filename mismatch: unexpected={len(unexpected)} missing={len(missing)}"
        )

    index_document: dict[str, Any] = {
        "schema": "tu41-outside-in-shard-index-v1",
        "source_sha256": source_digest,
        "enumerator_sha256": binary_digest,
        "cube_file_sha256": cubes_digest,
        "shards": shard_index_records,
    }
    index_rendered = json.dumps(index_document, indent=2, sort_keys=True) + "\n"
    index_digest = hashlib.sha256(index_rendered.encode("utf-8")).hexdigest()

    summary: dict[str, Any] = {
        "schema": "tu41-outside-in-certificate-v1",
        "result": "UNSAT",
        "n_short": 41,
        "long_length": 42,
        "primary_variables": 78,
        "cube_depth_steps": 5,
        "cube_prefix_bits": 19,
        "cube_count": len(cubes),
        "source_file": source.name,
        "source_sha256": source_digest,
        "enumerator_sha256": binary_digest,
        "cube_file": cubes_path.name,
        "cube_file_sha256": cubes_digest,
        "report_hash_chain_sha256": report_hash_chain.hexdigest(),
        "shard_index_sha256": index_digest,
        "total_nodes": total_nodes,
        "total_reported_wall_seconds": total_reported_wall,
        "maximum_shard_wall_seconds": maximum_reported_wall,
    }
    canonical = json.dumps(summary, sort_keys=True, separators=(",", ":")).encode()
    summary["summary_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"

    def atomic_write(path: Path, content: str) -> None:
        path = path.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=path.name + ".",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, path)
        os.chmod(path, 0o644)

    if args.index_output is not None:
        atomic_write(args.index_output, index_rendered)
        print(f"PASS wrote {args.index_output.resolve()}")

    if args.output is None:
        print(rendered, end="")
    else:
        atomic_write(args.output, rendered)
        print(f"PASS wrote {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Verify the committed TU(41) certificate manifest and shard index."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=directory / "enumerate_tu.cpp")
    parser.add_argument("--cubes", type=Path, default=directory / "cubes_depth5.txt")
    parser.add_argument(
        "--certificate", type=Path, default=directory / "certificate.json"
    )
    parser.add_argument(
        "--shard-index", type=Path, default=directory / "shard_results.json"
    )
    return parser.parse_args()


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    args = parse_args()
    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    shard_index = json.loads(args.shard_index.read_text(encoding="utf-8"))
    cube_lines = args.cubes.read_text(encoding="utf-8").splitlines()
    if any(not line.startswith("cube=") for line in cube_lines):
        raise AssertionError("cube file line lacks exact 'cube=' prefix")
    cubes = [line[len("cube=") :] for line in cube_lines]
    if any(len(cube) != 19 or set(cube) - {"0", "1"} for cube in cubes):
        raise AssertionError("cube file contains a malformed 19-bit prefix")

    require_equal(certificate["schema"], "tu41-outside-in-certificate-v1", "schema")
    require_equal(certificate["result"], "UNSAT", "result")
    require_equal(certificate["n_short"], 41, "short length")
    require_equal(certificate["long_length"], 42, "long length")
    require_equal(certificate["primary_variables"], 78, "primary variables")
    require_equal(certificate["cube_count"], 461, "cube count")
    require_equal(len(cubes), 461, "cube file line count")
    require_equal(len(set(cubes)), 461, "unique cube count")

    source_digest = sha256(args.source)
    cube_digest = sha256(args.cubes)
    index_digest = sha256(args.shard_index)
    require_equal(certificate["source_sha256"], source_digest, "source digest")
    require_equal(certificate["cube_file_sha256"], cube_digest, "cube digest")
    require_equal(certificate["shard_index_sha256"], index_digest, "index digest")
    require_equal(shard_index["source_sha256"], source_digest, "index source digest")
    require_equal(shard_index["cube_file_sha256"], cube_digest, "index cube digest")
    require_equal(
        shard_index["enumerator_sha256"],
        certificate["enumerator_sha256"],
        "enumerator digest",
    )

    records = shard_index["shards"]
    require_equal(len(records), 461, "shard record count")
    total_nodes = 0
    total_wall = 0.0
    maximum_wall = 0.0
    for index, (cube, record) in enumerate(zip(cubes, records, strict=True)):
        require_equal(record["index"], index, f"record {index} index")
        require_equal(record["cube"], cube, f"record {index} cube")
        if len(record["report_sha256"]) != 64:
            raise AssertionError(f"record {index} malformed report digest")
        nodes = int(record["nodes"])
        depth_counts = [int(value) for value in record["nodes_by_depth"]]
        if nodes <= 0 or len(depth_counts) != 21 or sum(depth_counts) != nodes:
            raise AssertionError(f"record {index} invalid node counts")
        wall = float(record["runner_wall_seconds"])
        if wall < 0:
            raise AssertionError(f"record {index} negative wall time")
        total_nodes += nodes
        total_wall += wall
        maximum_wall = max(maximum_wall, wall)

    require_equal(certificate["total_nodes"], total_nodes, "total nodes")
    require_equal(
        certificate["total_reported_wall_seconds"], total_wall, "total wall time"
    )
    require_equal(
        certificate["maximum_shard_wall_seconds"], maximum_wall, "maximum wall time"
    )

    payload = dict(certificate)
    claimed_payload_digest = payload.pop("summary_payload_sha256")
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    require_equal(
        claimed_payload_digest,
        hashlib.sha256(canonical).hexdigest(),
        "summary payload digest",
    )
    print("PASS TU(41) certificate manifest: 461/461 empty shards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Audit and aggregate a complete residue partition of unlabeled regressions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import Counter
from pathlib import Path
from typing import Sequence


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def aggregate_logs(
    paths: Sequence[Path],
    *,
    order: int,
    modulus: int,
    expected_count: int | None = None,
) -> dict[str, object]:
    """Return a fail-closed coverage summary for residues ``0..modulus-1``."""

    if order < 1 or modulus < 1 or len(paths) != modulus:
        raise ValueError("paths must give one positive-modulus residue partition")
    counters: Counter[str] = Counter()
    histogram: Counter[str] = Counter()
    shard_records: list[dict[str, object]] = []
    nauty_hash: str | None = None
    for residue, path in enumerate(paths):
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        configuration = payload.get("configuration")
        expected_configuration = {
            "order": order,
            "residue": residue,
            "modulus": modulus,
            "connected_only": True,
            "check_all_guard_counts": True,
        }
        if not isinstance(configuration, dict):
            raise ValueError(f"{path}: missing configuration")
        for key, value in expected_configuration.items():
            if configuration.get(key) != value:
                raise ValueError(
                    f"{path}: configuration {key!r} is "
                    f"{configuration.get(key)!r}, expected {value!r}"
                )
        generator_command = configuration.get("generator_command")
        if (
            not isinstance(generator_command, list)
            or len(generator_command) != 4
            or not isinstance(generator_command[0], str)
            or generator_command[1:]
            != ["-cq", str(order), f"{residue}/{modulus}"]
        ):
            raise ValueError(f"{path}: malformed geng residue command")
        if payload.get("status") != "complete":
            raise ValueError(f"{path}: shard is not complete")
        if payload.get("outcome") != "all A/B comparisons agreed":
            raise ValueError(f"{path}: evaluator agreement is not recorded")
        processed = payload.get("processed")
        shard_counters = payload.get("counters")
        shard_histogram = payload.get("parameter_histogram")
        if (
            type(processed) is not int
            or processed < 0
            or not isinstance(shard_counters, dict)
            or not isinstance(shard_histogram, dict)
        ):
            raise ValueError(f"{path}: malformed counts")
        if shard_counters.get("graphs") != processed:
            raise ValueError(f"{path}: graph counter differs from processed")
        if sum(shard_histogram.values()) != processed:
            raise ValueError(f"{path}: histogram does not cover the shard")
        for key, value in shard_counters.items():
            if not isinstance(key, str) or type(value) is not int or value < 0:
                raise ValueError(f"{path}: malformed counter")
            counters[key] += value
        for key, value in shard_histogram.items():
            if (
                not isinstance(key, str)
                or type(value) is not int
                or value < 0
            ):
                raise ValueError(f"{path}: malformed histogram")
            histogram[key] += value
        shard_nauty_hash = payload.get("nauty_archive_sha256")
        if not isinstance(shard_nauty_hash, str) or len(shard_nauty_hash) != 64:
            raise ValueError(f"{path}: malformed nauty archive hash")
        if nauty_hash is None:
            nauty_hash = shard_nauty_hash
        elif nauty_hash != shard_nauty_hash:
            raise ValueError("shards used different nauty archives")
        stream_hash = payload.get("graph_stream_sha256")
        if not isinstance(stream_hash, str) or len(stream_hash) != 64:
            raise ValueError(f"{path}: malformed graph-stream hash")
        shard_records.append(
            {
                "residue": residue,
                "path": str(path),
                "file_sha256": _sha256(path),
                "graph_stream_sha256": stream_hash,
                "processed": processed,
            }
        )

    total = sum(int(record["processed"]) for record in shard_records)
    if counters["graphs"] != total or sum(histogram.values()) != total:
        raise AssertionError("aggregate counts are internally inconsistent")
    if expected_count is not None and total != expected_count:
        raise ValueError(f"aggregate has {total} graphs, expected {expected_count}")
    set_digest = hashlib.sha256()
    for record in shard_records:
        set_digest.update(
            (
                f"{record['residue']} {record['file_sha256']} "
                f"{record['graph_stream_sha256']} {record['processed']}\n"
            ).encode("ascii")
        )
    return {
        "status": "complete",
        "coverage": {
            "order": order,
            "connected_only": True,
            "modulus": modulus,
            "residues": list(range(modulus)),
            "expected_count": expected_count,
            "processed": total,
            "check_all_guard_counts": True,
            "nauty_archive_sha256": nauty_hash,
        },
        "counters": dict(sorted(counters.items())),
        "parameter_histogram": dict(sorted(histogram.items())),
        "shards": shard_records,
        "ordered_shard_set_sha256": set_digest.hexdigest(),
        "outcome": "complete residue coverage; all A/B comparisons agreed",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--modulus", type=int, required=True)
    parser.add_argument(
        "--pattern",
        required=True,
        help="input path pattern containing a Python {residue:02d} field",
    )
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    paths = tuple(
        Path(arguments.pattern.format(residue=residue))
        for residue in range(arguments.modulus)
    )
    result = aggregate_logs(
        paths,
        order=arguments.order,
        modulus=arguments.modulus,
        expected_count=arguments.expected_count,
    )
    _atomic_json(arguments.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

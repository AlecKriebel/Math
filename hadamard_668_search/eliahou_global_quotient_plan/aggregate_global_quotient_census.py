#!/usr/bin/env python3
"""Validate and aggregate every atomic case-26 quotient range manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import run_global_quotient_census as runner


AGGREGATE_SCHEMA = "h668-case26-global-quotient-aggregate-v1"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.output.resolve()
    config_path = root / "RUN_CONFIG.json"
    if not config_path.exists():
        raise RuntimeError("RUN_CONFIG.json is missing")
    config = json.loads(config_path.read_text())
    if config.get("schema") != runner.SCHEMA:
        raise RuntimeError("run configuration schema changed")
    source_sha = str(config["producer_sources_sha256"])
    model_sha = str(config["model_sha256"])
    reflection_gauge = bool(config["reflection_gauge"])
    ranges = runner.expected_ranges(
        int(config["start"]),
        int(config["stop"]),
        int(config["chunk_size"]),
    )

    total_survivors = 0
    total_exact = 0
    total_join_rows = 0
    total_kernel_seconds = 0.0
    exact_candidates: list[dict[str, object]] = []
    best: dict[str, object] | None = None
    digest = hashlib.sha256()

    def score(record: dict[str, object]) -> tuple:
        return (
            int(record["nonzero_lags"]),
            int(record["l1"]),
            int(record["linf"]),
            int(record["quotient_index"]),
            int(record["central_value"]),
            int(record["pair_state"]),
        )

    for start, states in ranges:
        path = runner.range_path(root, start, states)
        if not path.exists():
            raise RuntimeError(
                f"range {start}:{start + states} is incomplete"
            )
        payload = json.loads(path.read_text())
        runner.validate_range(
            payload,
            start,
            states,
            source_sha,
            model_sha,
            reflection_gauge,
        )
        survivors = int(payload["joint_mod6_supports"])
        exact = int(payload["exact_integer_supports"])
        total_survivors += survivors
        total_exact += exact
        total_join_rows += int(payload["join_rows"])
        total_kernel_seconds += float(payload["kernel_seconds"])
        exact_candidates.extend(payload["exact_candidates"])
        candidate = payload.get("best_witness")
        if candidate is not None and (
            best is None or score(candidate) < score(best)
        ):
            best = candidate
        digest.update(start.to_bytes(4, "little"))
        digest.update(states.to_bytes(4, "little"))
        digest.update(
            bytes.fromhex(str(payload["survivor_stream_sha256"]))
        )

    expected_join_rows = (
        (int(config["stop"]) - int(config["start"]))
        * (
            ((1 << 19) if reflection_gauge else (1 << 20))
            + (1 << 18)
        )
        * 2
    )
    if total_join_rows != expected_join_rows:
        raise RuntimeError("aggregate join-row count changed")
    if len(exact_candidates) != total_exact:
        raise RuntimeError("aggregate exact-candidate count changed")
    aggregate = {
        "schema": AGGREGATE_SCHEMA,
        "status": "complete",
        "case": 26,
        "block": "S",
        "q_index": 12,
        "start": int(config["start"]),
        "stop": int(config["stop"]),
        "quotient_states": int(config["stop"]) - int(config["start"]),
        "range_count": len(ranges),
        "central_values_per_state": 2,
        "reflection_gauge": reflection_gauge,
        "join_rows": total_join_rows,
        "joint_mod6_supports": total_survivors,
        "integer_polynomial_checks": total_survivors,
        "bitpacked_physical_replays": total_survivors,
        "exact_integer_supports": total_exact,
        "exact_candidates": exact_candidates,
        "best_witness": best,
        "range_digest_sha256": digest.hexdigest(),
        "producer_sources_sha256": source_sha,
        "model_sha256": model_sha,
        "binary_sha256": config["binary_sha256"],
        "sum_kernel_seconds": total_kernel_seconds,
        "output_bytes_before_aggregate": runner.output_bytes(root),
    }
    runner.atomic_json(root / "AGGREGATE.json", aggregate)
    print(json.dumps(aggregate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

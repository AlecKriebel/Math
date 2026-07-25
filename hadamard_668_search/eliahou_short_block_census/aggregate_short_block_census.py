#!/usr/bin/env python3
"""Validate and aggregate every range of one short-block census."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import run_short_block_census as runner


AGGREGATE_SCHEMA = "h668-eliahou-short-block-aggregate-v1"


def score(record: dict[str, object]) -> tuple[int, ...]:
    return (
        int(record["nonzero_lags"]),
        int(record["l1"]),
        int(record["linf"]),
        int(record["quotient_index"]),
        int(record["central_value"]),
        int(record["pair_state"]),
    )


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

    case_number = int(config["case"])
    q_index = int(config["q_index"])
    source_sha = str(config["producer_sources_sha256"])
    model_sha = str(config["model_sha256"])
    reflection_gauge = bool(config["reflection_gauge"])
    exceptional_indices = tuple(
        map(int, config["S_fallback_quotient_indices"])
    )
    ranges = runner.expected_ranges(
        int(config["start"]),
        int(config["stop"]),
        int(config["chunk_size"]),
    )
    totals = {
        "states": 0,
        "L_gauge_states": 0,
        "S_fallback_gauge_states": 0,
        "join_rows": 0,
        "joint_mod6_supports": 0,
        "exact_integer_supports": 0,
    }
    kernel_seconds = 0.0
    exact_candidates: list[dict[str, object]] = []
    best: dict[str, object] | None = None
    digest = hashlib.sha256()

    for start, states in ranges:
        path = runner.range_path(root, start, states)
        if not path.exists():
            raise RuntimeError(
                f"range {start}:{start + states} is incomplete"
            )
        payload = json.loads(path.read_text())
        runner.validate_range(
            payload,
            case_number=case_number,
            q_index=q_index,
            start=start,
            states=states,
            source_sha=source_sha,
            model_sha=model_sha,
            reflection_gauge=reflection_gauge,
            exceptional_indices=exceptional_indices,
        )
        totals["states"] += states
        for key in (
            "L_gauge_states",
            "S_fallback_gauge_states",
            "join_rows",
            "joint_mod6_supports",
            "exact_integer_supports",
        ):
            totals[key] += int(payload[key])
        kernel_seconds += float(payload["kernel_seconds"])
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

    expected_l, expected_s, expected_rows = runner.gauge_counts(
        int(config["start"]),
        int(config["stop"]) - int(config["start"]),
        exceptional_indices,
        reflection_gauge,
    )
    if (
        totals["L_gauge_states"],
        totals["S_fallback_gauge_states"],
        totals["join_rows"],
    ) != (expected_l, expected_s, expected_rows):
        raise RuntimeError("aggregate dynamic-gauge accounting changed")
    if len(exact_candidates) != totals["exact_integer_supports"]:
        raise RuntimeError("aggregate exact-candidate count changed")

    aggregate = {
        "schema": AGGREGATE_SCHEMA,
        "status": "complete",
        "case": case_number,
        "block": "S",
        "q_index": q_index,
        "start": int(config["start"]),
        "stop": int(config["stop"]),
        "quotient_states": totals["states"],
        "range_count": len(ranges),
        "central_values_per_state": 2,
        "reflection_gauge": reflection_gauge,
        "reflection_gauge_rule":
            "lowest odd noncentral L pair, else S pair, has y=0",
        "L_gauge_states": totals["L_gauge_states"],
        "S_fallback_gauge_states":
            totals["S_fallback_gauge_states"],
        "join_rows": totals["join_rows"],
        "joint_mod6_supports": totals["joint_mod6_supports"],
        "integer_polynomial_checks": totals["joint_mod6_supports"],
        "bitpacked_physical_replays": totals["joint_mod6_supports"],
        "exact_integer_supports": totals["exact_integer_supports"],
        "exact_candidates": exact_candidates,
        "best_witness": best,
        "range_digest_sha256": digest.hexdigest(),
        "producer_sources_sha256": source_sha,
        "model_sha256": model_sha,
        "binary_sha256": config["binary_sha256"],
        "sum_kernel_seconds": kernel_seconds,
        "output_bytes_before_aggregate": runner.output_bytes(root),
    }
    runner.atomic_json(root / "AGGREGATE.json", aggregate)
    print(json.dumps(aggregate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

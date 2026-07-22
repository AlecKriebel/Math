#!/usr/bin/env python3
"""Move a variable-q checkpoint to its canonical global-alternation shard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from variable_q_base import (
    LONG,
    MARGIN_SHARDS,
    SHORT,
    alternating_sum,
    base_correlations,
    base_to_special,
    canonical_alternation_transform,
    sign_sum,
)


def load_sequences(payload: object) -> tuple[tuple[int, ...], ...]:
    if not isinstance(payload, dict):
        raise ValueError("candidate JSON must contain an object")
    result = []
    for label, length in zip("abcd", (LONG, LONG, SHORT, SHORT), strict=True):
        raw = payload.get(label)
        if not isinstance(raw, list) or len(raw) != length:
            raise ValueError(f"field {label} must contain {length} signs")
        sequence = tuple(raw)
        if any(type(value) is not int or value not in (-1, 1) for value in sequence):
            raise ValueError(f"field {label} is not a sign sequence")
        result.append(sequence)
    return tuple(result)


def rewrite_payload(
    payload: object,
    sequences: tuple[tuple[int, ...], ...],
    source_field: str,
    source: str,
) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise ValueError("candidate JSON must contain an object")
    ordinary = tuple(sign_sum(sequence) for sequence in sequences)
    alternating = tuple(alternating_sum(sequence) for sequence in sequences)
    try:
        shard = MARGIN_SHARDS.index((ordinary, alternating))
    except ValueError as error:
        raise ValueError("transformed margins do not identify a shard") from error

    correlations = base_correlations(*sequences)
    half = tuple(value // 2 for value in correlations[1:])
    if any(value % 2 for value in correlations[1:]):
        raise AssertionError("base residual was not even")
    s, q = base_to_special(*sequences)
    result: dict[str, object] = dict(payload)
    result.update(
        {
            "shard": shard,
            "ordinary_sums": list(ordinary),
            "alternating_sums": list(alternating),
            "a": list(sequences[0]),
            "b": list(sequences[1]),
            "c": list(sequences[2]),
            "d": list(sequences[3]),
            "s": list(s),
            "q": list(q),
            "base_correlations": list(correlations),
            "half_base_residuals_1_through_83": list(half),
            "energy_half_base": sum(value * value for value in half),
            "energy_base": sum(value * value for value in correlations[1:]),
            "bad_lag_count": sum(value != 0 for value in correlations[1:]),
            "odd_half_residual_count": sum(abs(value) % 2 for value in half),
            "max_abs_base_residual": max(map(abs, correlations[1:])),
            "l1_base_residual": sum(map(abs, correlations[1:])),
            "exact": not any(correlations[1:]),
            "hadamard_verified": False,
            source_field: source,
        }
    )
    search = result.get("search")
    if isinstance(search, dict):
        result["search"] = {**search, "global_alternation_canonicalized": True}
    return result


def alternate_payload(payload: object, source: str) -> dict[str, object]:
    sequences = canonical_alternation_transform(*load_sequences(payload))
    return rewrite_payload(
        payload, sequences, "global_alternation_source", source
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    transformed = alternate_payload(payload, str(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(transformed, indent=2) + "\n", encoding="utf-8")
    print(f"source_shard={payload.get('shard') if isinstance(payload, dict) else 'unknown'}")
    print(f"target_shard={transformed['shard']}")
    print(f"energy_half={transformed['energy_half_base']}")
    print(f"wrote={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Dependency-free verifier for variable-q BS(84,83) candidates.

Accepted JSON may contain ``a,b,c,d``, ``s,q``, or both.  A successful check
reconstructs the special Golay quadruple and then expands and verifies the
entire order-668 Goethals-Seidel matrix with exact integer row products.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from construction import goethals_seidel, verify_hadamard
from seed import N, special_quadruple, summed_aperiodic_correlations, validate_sign_sequence
from variable_q_base import (
    LONG,
    SHORT,
    base_correlations,
    base_to_special,
    self_test,
    special_to_base,
)


def sign_tuple(value: Any, length: int, label: str) -> tuple[int, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a JSON array")
    result = tuple(value)
    try:
        validate_sign_sequence(result, length)
    except ValueError as error:
        raise ValueError(f"invalid {label}: {error}") from error
    return result


def extract_candidate(
    payload: Any,
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
]:
    if not isinstance(payload, dict):
        raise ValueError("candidate JSON must contain an object")

    has_base = all(label in payload for label in "abcd")
    has_special = "s" in payload and "q" in payload
    if not has_base and not has_special:
        raise ValueError("candidate must contain a,b,c,d or s,q")

    base = None
    if has_base:
        base = (
            sign_tuple(payload["a"], LONG, "a"),
            sign_tuple(payload["b"], LONG, "b"),
            sign_tuple(payload["c"], SHORT, "c"),
            sign_tuple(payload["d"], SHORT, "d"),
        )
    special = None
    if has_special:
        special = (
            sign_tuple(payload["s"], N, "s"),
            sign_tuple(payload["q"], N, "q"),
        )

    if base is None:
        assert special is not None
        base = special_to_base(*special)
    if special is None:
        special = base_to_special(*base)
    if special_to_base(*special) != base or base_to_special(*base) != special:
        raise ValueError("base sequences and s,q fields are inconsistent")
    return (*base, *special)


def verify_payload(payload: Any) -> tuple[int, int]:
    a, b, c, d, s, q = extract_candidate(payload)
    base_values = base_correlations(a, b, c, d)
    bad_base = sum(value != 0 for value in base_values[1:])
    if base_values[0] != 334 or bad_base:
        return bad_base, -1

    quadruple = special_quadruple(s, q)
    special_values = summed_aperiodic_correlations(quadruple)
    bad_special = sum(value != 0 for value in special_values[1:])
    if bad_special:
        return bad_base, bad_special

    matrix = goethals_seidel(quadruple)
    verify_hadamard(matrix)
    return 0, 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        print("self_test=passed")
        if args.candidate is None:
            return 0
    if args.candidate is None:
        print("error=a candidate path or --self-test is required", file=sys.stderr)
        return 2

    try:
        payload = json.loads(args.candidate.read_text(encoding="utf-8"))
        bad_base, bad_special = verify_payload(payload)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    print(f"candidate={args.candidate}")
    print(f"bad_base_lag_count={bad_base}")
    print(f"bad_special_lag_count={bad_special if bad_special >= 0 else 'not_checked'}")
    valid = bad_base == 0 and bad_special == 0
    print(f"hadamard_order=668")
    print(f"hadamard_verified={str(valid).lower()}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

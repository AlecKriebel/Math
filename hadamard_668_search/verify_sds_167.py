#!/usr/bin/env python3
"""Strictly verify a cyclic-SDS candidate and its order-668 GS matrix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from construction import goethals_seidel, verify_hadamard
from good_167 import summed_periodic_correlations
from sds_167 import ORDER, ROW_SUM_PROFILES, validate_cyclic_sds


def verify_payload(payload: object) -> tuple[tuple[int, ...], ...]:
    if not isinstance(payload, dict):
        raise ValueError("candidate must be a JSON object")
    if payload.get("kind") != "cyclic_sds_167":
        raise ValueError("candidate kind must be cyclic_sds_167")
    if type(payload.get("order")) is not int or payload["order"] != ORDER:
        raise ValueError(f"candidate order must be exactly {ORDER}")
    if (
        type(payload.get("hadamard_order")) is not int
        or payload["hadamard_order"] != 4 * ORDER
    ):
        raise ValueError(f"candidate hadamard_order must be exactly {4 * ORDER}")
    raw_sequences = payload.get("sequences")
    if not isinstance(raw_sequences, list):
        raise ValueError("candidate must contain a sequences list")
    sequences = validate_cyclic_sds(raw_sequences, ORDER)
    row_sums = tuple(sum(sequence) for sequence in sequences)
    raw_row_sums = payload.get("row_sums")
    if (
        not isinstance(raw_row_sums, list)
        or any(type(value) is not int for value in raw_row_sums)
        or tuple(raw_row_sums) != row_sums
    ):
        raise ValueError("candidate row_sums do not match the four sequences")
    profile = payload.get("profile")
    if (
        type(profile) is not int
        or not 0 <= profile < len(ROW_SUM_PROFILES)
        or row_sums != ROW_SUM_PROFILES[profile]
    ):
        raise ValueError("candidate profile does not match its normalized row sums")
    correlations = summed_periodic_correlations(sequences)
    raw_correlations = payload.get("periodic_correlation_sums")
    if (
        not isinstance(raw_correlations, list)
        or any(type(value) is not int for value in raw_correlations)
        or tuple(raw_correlations) != correlations
    ):
        raise ValueError("stored periodic correlations do not match the sequences")
    matrix = goethals_seidel(sequences)
    verify_hadamard(matrix)
    if len(matrix) != 4 * ORDER:
        raise AssertionError("Goethals-Seidel order mismatch")
    return sequences


def self_test() -> None:
    # One constant and three nonconstant length-three rows have PAF sum zero.
    fixture = (
        (1, 1, 1),
        (1, 1, -1),
        (1, -1, 1),
        (-1, 1, 1),
    )
    sequences = validate_cyclic_sds(fixture, 3)
    verify_hadamard(goethals_seidel(sequences))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("PASS: exact cyclic-SDS H(12) regression")
    if args.candidate is None:
        if args.self_test:
            return 0
        parser.error("provide a candidate JSON file or --self-test")
    sequences = verify_payload(json.loads(args.candidate.read_text(encoding="utf-8")))
    print(f"PASS: exact cyclic SDS of order {ORDER}")
    print(f"PASS: exact Hadamard matrix of order {4 * ORDER}")
    print(f"row_sums={tuple(sum(sequence) for sequence in sequences)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

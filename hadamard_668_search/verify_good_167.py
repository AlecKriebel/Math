#!/usr/bin/env python3
"""Independently verify a circulant-good-matrix candidate and its H(4n)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from construction import goethals_seidel, verify_hadamard
from good_167 import (
    GOOD_167_ROW_SUM_PROFILES,
    ORDER,
    product_cycle_order,
    summed_periodic_correlations,
    validate_good_quadruple,
)


def verify_payload(payload: object) -> tuple[tuple[int, ...], ...]:
    if not isinstance(payload, dict):
        raise ValueError("candidate must be a JSON object")
    if payload.get("kind") != "circulant_good_matrices":
        raise ValueError("candidate kind must be circulant_good_matrices")
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
    sequences = validate_good_quadruple(raw_sequences, ORDER)
    n = len(sequences[0])
    row_sums = tuple(sum(sequence) for sequence in sequences[1:])
    raw_row_sums = payload.get("row_sums")
    if (
        not isinstance(raw_row_sums, list)
        or any(type(value) is not int for value in raw_row_sums)
        or tuple(raw_row_sums) != row_sums
    ):
        raise ValueError("candidate row_sums do not match B, C, and D")
    matrix = goethals_seidel(sequences)
    verify_hadamard(matrix)
    if len(matrix) != 4 * n:
        raise AssertionError("Goethals-Seidel order mismatch")
    for row in range(4 * n):
        for column in range(4 * n):
            expected = 2 if row == column else 0
            if matrix[row][column] + matrix[column][row] != expected:
                raise ValueError(
                    "Goethals-Seidel candidate is Hadamard but not normalized skew: "
                    f"entry ({row},{column})"
                )
    return sequences


def self_test() -> None:
    if GOOD_167_ROW_SUM_PROFILES != ((-21, -1, 15), (-9, 15, 19)):
        raise AssertionError(f"unexpected order-167 profiles: {GOOD_167_ROW_SUM_PROFILES}")
    if product_cycle_order() != 83:
        raise AssertionError("doubling should be one 83-cycle modulo sign at order 167")
    # Correlations of arbitrary structural sequences need not be complementary,
    # but their symmetry must make lag k equal lag n-k.
    a = (1,) + (1,) * 83 + (-1,) * 83
    b = (1,) * 167
    correlations = summed_periodic_correlations((a, b, b, b))
    if any(correlations[k] != correlations[-k] for k in range(1, 84)):
        raise AssertionError("periodic PAF reflection identity failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("PASS: order-167 arithmetic and PAF reflection self-test")
    if args.candidate is None:
        if args.self_test:
            return 0
        parser.error("provide a candidate JSON file or --self-test")

    sequences = verify_payload(json.loads(args.candidate.read_text()))
    n = len(sequences[0])
    print(f"PASS: exact circulant good matrices of order {n}")
    print(f"PASS: exact skew Hadamard matrix of order {4*n}")
    print(f"row_sums={tuple(sum(sequence) for sequence in sequences)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

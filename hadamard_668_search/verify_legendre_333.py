#!/usr/bin/env python3
"""Exact verifier for fixed-compression Legendre-pair candidates of length 333.

The accepted JSON form is either ``{"a": [...], "b": [...]}`` or the
canonical payload written by ``search_legendre_333_cp_sat.py``.  Acceptance
uses integer periodic autocorrelations at every independent lag; no solver or
floating-point calculation is trusted as a certificate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from construction import two_circulant_legendre, verify_hadamard
from legendre_333 import (
    CRT_INDEX_TABLE,
    FIXED_PLUS_COUNTS_A,
    FIXED_PLUS_COUNTS_B,
    N,
    compression_9,
    crt_matrix,
    load_candidate,
    periodic_autocorrelation,
    sequence_from_crt_matrix,
    sequences_from_candidate,
    verify_fixed_seed_identities,
    verify_legendre_pair,
    xor_distance,
)


def deterministic_margin_sequence(plus_counts: tuple[int, ...]) -> tuple[int, ...]:
    """Construct a reproducible sign vector with the requested CRT column sums."""

    sequence = [-1] * N
    for column, count in enumerate(plus_counts):
        for row in range(count):
            sequence[CRT_INDEX_TABLE[row][column]] = 1
    return tuple(sequence)


def run_self_test() -> None:
    """Exercise the seed identities, CRT map, and independent PAF/XOR checks."""

    verify_fixed_seed_identities()
    a = deterministic_margin_sequence(FIXED_PLUS_COUNTS_A)
    b = deterministic_margin_sequence(FIXED_PLUS_COUNTS_B)

    if sequence_from_crt_matrix(crt_matrix(a)) != a:
        raise AssertionError("CRT matrix round trip failed")
    if sequence_from_crt_matrix(crt_matrix(b)) != b:
        raise AssertionError("CRT matrix round trip failed")

    report = verify_legendre_pair(a, b)
    if not report.fixed_compression_matches or report.sum_a != 1 or report.sum_b != 1:
        raise AssertionError("deterministic margin fixture failed compression checks")
    if report.valid or not report.bad_lags:
        raise AssertionError("non-Legendre fixture unexpectedly passed")

    # PAF(X,s) = n - 2*d_H(X,shift_s(X)).  Check both independent exact
    # implementations at every relevant lag.
    for lag, correlation_sum in enumerate(report.correlation_sums):
        expected = 2 * N - 2 * (xor_distance(a, lag) + xor_distance(b, lag))
        if correlation_sum != expected:
            raise AssertionError(f"PAF/XOR mismatch at lag {lag}")
        direct = periodic_autocorrelation(a, lag) + periodic_autocorrelation(b, lag)
        if correlation_sum != direct:
            raise AssertionError(f"PAF implementations disagree at lag {lag}")

    loaded_a, loaded_b = sequences_from_candidate({"a": list(a), "b": list(b)})
    if loaded_a != a or loaded_b != b:
        raise AssertionError("candidate JSON extraction failed")
    if len(compression_9(a)) != 9:
        raise AssertionError("length-9 compression has the wrong length")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path, nargs="?")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run deterministic arithmetic and CRT regression tests",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="optionally write the full exact verification report as JSON",
    )
    parser.add_argument(
        "--bad-lag-limit",
        type=int,
        default=20,
        help="maximum number of failed lags to print (default: 20)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        run_self_test()
        print("self_test=passed")
        if args.candidate is None:
            return 0
    if args.candidate is None:
        print("error: a candidate path or --self-test is required", file=sys.stderr)
        return 2

    try:
        a, b = load_candidate(args.candidate)
        result = verify_legendre_pair(a, b)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    print(f"candidate={args.candidate}")
    print(f"valid={str(result.valid).lower()}")
    print(f"sum_a={result.sum_a}")
    print(f"sum_b={result.sum_b}")
    print(
        "fixed_compression_matches="
        f"{str(result.fixed_compression_matches).lower()}"
    )
    print(f"bad_lag_count={len(result.bad_lags)}")
    for lag, value in result.bad_lags[: max(0, args.bad_lag_limit)]:
        print(f"bad_lag={lag} correlation_sum={value}")

    hadamard_verified = False
    if result.valid:
        try:
            matrix = two_circulant_legendre(a, b)
            verify_hadamard(matrix)
            hadamard_verified = True
        except ValueError as error:
            print(f"error=Hadamard construction failed: {error}", file=sys.stderr)
    print(f"hadamard_order={2 * N + 2}")
    print(f"hadamard_verified={str(hadamard_verified).lower()}")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(result.as_dict(), indent=2) + "\n", encoding="utf-8"
        )
        print(f"report={args.report}")
    if result.valid and not hadamard_verified:
        return 3
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

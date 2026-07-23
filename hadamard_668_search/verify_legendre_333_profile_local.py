#!/usr/bin/env python3
"""Strictly verify a fixed-row-and-column LP(333) local near miss.

Success certifies only an internally exact nonzero-energy checkpoint on one
prescribed compression-profile fiber.  It never certifies H(668).  A zero-
energy pair belongs exclusively to ``verify_legendre_333.py``, which builds
and checks the full bordered two-circulant matrix.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from legendre_333 import (
    CRT_INDEX_TABLE,
    FIXED_COMPRESSION_A,
    FIXED_COMPRESSION_B,
    FIXED_PLUS_COUNTS_A,
    FIXED_PLUS_COUNTS_B,
    N,
    periodic_autocorrelation,
    validate_sign_sequence,
    xor_distance,
)
from legendre_333_profile_catalog import EXACT_COMBINED_PAF, ROW_SUM_PROFILES


SCHEMA = "hadamard668.legendre333-row-column-local-checkpoint.v1"
KIND = "legendre333_row_column_local_checkpoint"
PARAMETERIZATION = "crt_row_column_margins"
INDEPENDENT_LAGS = (N - 1) // 2
EXACT_MOD9_PAF = EXACT_COMBINED_PAF


def _strict_int(payload: dict[str, object], field: str) -> int:
    value = payload.get(field)
    if type(value) is not int:
        raise ValueError(f"{field} must be an integer")
    return value


def _strict_int_vector(
    payload: dict[str, object], field: str, length: int
) -> tuple[int, ...]:
    raw = payload.get(field)
    if (
        not isinstance(raw, list)
        or len(raw) != length
        or any(type(value) is not int for value in raw)
    ):
        raise ValueError(f"{field} must contain exactly {length} integers")
    return tuple(raw)


def _sign_vector(payload: dict[str, object], field: str) -> tuple[int, ...]:
    raw = payload.get(field)
    if not isinstance(raw, list):
        raise ValueError(f"{field} must be a sign-vector array")
    sequence = tuple(raw)
    validate_sign_sequence(sequence)
    return sequence


def _compression(sequence: tuple[int, ...], modulus: int) -> tuple[int, ...]:
    return tuple(
        sum(sequence[index] for index in range(residue, N, modulus))
        for residue in range(modulus)
    )


def _cyclic_paf(sequence: tuple[int, ...]) -> tuple[int, ...]:
    length = len(sequence)
    return tuple(
        sum(sequence[index] * sequence[(index + lag) % length]
            for index in range(length))
        for lag in range(length)
    )


def verify_profile_checkpoint(payload: object) -> dict[str, int]:
    if not isinstance(payload, dict):
        raise ValueError("checkpoint must be a JSON object")
    if payload.get("schema") != SCHEMA:
        raise ValueError("checkpoint schema is missing or unsupported")
    if payload.get("kind") != KIND:
        raise ValueError(f"kind must be {KIND}")
    if payload.get("status") != "near_miss" or payload.get("exact") is not False:
        raise ValueError("profile checkpoints must be explicitly nonexact near misses")
    if payload.get("parameterization") != PARAMETERIZATION:
        raise ValueError(f"parameterization must be {PARAMETERIZATION}")
    if _strict_int(payload, "length") != N:
        raise ValueError(f"length must be {N}")
    if _strict_int(payload, "hadamard_order") != 2 * N + 2:
        raise ValueError(f"hadamard_order must be {2 * N + 2}")
    profile = _strict_int(payload, "profile")
    if not 0 <= profile < len(ROW_SUM_PROFILES):
        raise ValueError("profile index is unsupported")
    expected_rows_a, expected_rows_b = ROW_SUM_PROFILES[profile]
    if _strict_int_vector(payload, "row_sums_a", 9) != expected_rows_a:
        raise ValueError("row_sums_a does not match the indexed profile")
    if _strict_int_vector(payload, "row_sums_b", 9) != expected_rows_b:
        raise ValueError("row_sums_b does not match the indexed profile")
    expected_row_plus_a = tuple((37 + value) // 2 for value in expected_rows_a)
    expected_row_plus_b = tuple((37 + value) // 2 for value in expected_rows_b)
    recorded_row_plus_a = _strict_int_vector(payload, "row_plus_counts_a", 9)
    recorded_row_plus_b = _strict_int_vector(payload, "row_plus_counts_b", 9)
    if recorded_row_plus_a != expected_row_plus_a:
        raise ValueError("row_plus_counts_a does not match the indexed profile")
    if recorded_row_plus_b != expected_row_plus_b:
        raise ValueError("row_plus_counts_b does not match the indexed profile")
    if _strict_int_vector(payload, "column_sums_a", 37) != FIXED_COMPRESSION_A:
        raise ValueError("column_sums_a is not the prescribed compression")
    if _strict_int_vector(payload, "column_sums_b", 37) != FIXED_COMPRESSION_B:
        raise ValueError("column_sums_b is not the prescribed compression")
    recorded_column_plus_a = _strict_int_vector(
        payload, "column_plus_counts_a", 37
    )
    recorded_column_plus_b = _strict_int_vector(
        payload, "column_plus_counts_b", 37
    )
    if recorded_column_plus_a != FIXED_PLUS_COUNTS_A:
        raise ValueError("column_plus_counts_a is not the prescribed compression")
    if recorded_column_plus_b != FIXED_PLUS_COUNTS_B:
        raise ValueError("column_plus_counts_b is not the prescribed compression")
    if (
        _strict_int_vector(payload, "mod9_combined_paf_0_through_8", 9)
        != EXACT_MOD9_PAF
    ):
        raise ValueError("recorded length-9 PAF vector is not exact")
    if not isinstance(payload.get("search"), dict):
        raise ValueError("search metadata must be an object")

    a = _sign_vector(payload, "a")
    b = _sign_vector(payload, "b")
    actual_column_plus_a = tuple(
        sum(a[CRT_INDEX_TABLE[row][column]] == 1 for row in range(9))
        for column in range(37)
    )
    actual_column_plus_b = tuple(
        sum(b[CRT_INDEX_TABLE[row][column]] == 1 for row in range(9))
        for column in range(37)
    )
    if actual_column_plus_a != recorded_column_plus_a:
        raise ValueError("recorded column_plus_counts_a is incorrect")
    if actual_column_plus_b != recorded_column_plus_b:
        raise ValueError("recorded column_plus_counts_b is incorrect")
    actual_columns_a = tuple(
        sum(a[CRT_INDEX_TABLE[row][column]] for row in range(9))
        for column in range(37)
    )
    actual_columns_b = tuple(
        sum(b[CRT_INDEX_TABLE[row][column]] for row in range(9))
        for column in range(37)
    )
    if actual_columns_a != FIXED_COMPRESSION_A:
        raise ValueError("A does not have the prescribed CRT-column sums")
    if actual_columns_b != FIXED_COMPRESSION_B:
        raise ValueError("B does not have the prescribed CRT-column sums")
    rows_a = _compression(a, 9)
    rows_b = _compression(b, 9)
    actual_row_plus_a = tuple(
        sum(a[index] == 1 for index in range(row, N, 9)) for row in range(9)
    )
    actual_row_plus_b = tuple(
        sum(b[index] == 1 for index in range(row, N, 9)) for row in range(9)
    )
    if actual_row_plus_a != recorded_row_plus_a:
        raise ValueError("recorded row_plus_counts_a is incorrect")
    if actual_row_plus_b != recorded_row_plus_b:
        raise ValueError("recorded row_plus_counts_b is incorrect")
    if rows_a != expected_rows_a or rows_b != expected_rows_b:
        raise ValueError("A,B do not have the indexed CRT-row profile")
    compressed_paf = tuple(
        left + right
        for left, right in zip(_cyclic_paf(rows_a), _cyclic_paf(rows_b), strict=True)
    )
    if compressed_paf != EXACT_MOD9_PAF:
        raise ValueError("expanded sequences fail the exact length-9 PAF profile")

    full_correlations = tuple(
        periodic_autocorrelation(a, lag) + periodic_autocorrelation(b, lag)
        for lag in range(N)
    )
    for lag in range(1, INDEPENDENT_LAGS + 1):
        if full_correlations[lag] != full_correlations[N - lag]:
            raise ValueError("full PAF reflection identity failed")
        xor_value = 2 * N - 2 * (xor_distance(a, lag) + xor_distance(b, lag))
        if full_correlations[lag] != xor_value:
            raise ValueError("integer PAF and XOR-distance computations disagree")
    lifted = tuple(
        sum(full_correlations[lag] for lag in range(residue, N, 9))
        for residue in range(9)
    )
    if lifted != compressed_paf:
        raise ValueError("compression-lift PAF identity failed")

    independent = full_correlations[1 : INDEPENDENT_LAGS + 1]
    residuals = []
    for lag, correlation in enumerate(independent, start=1):
        if (correlation + 2) % 4:
            raise ValueError(f"lag {lag} residual violates cyclic parity")
        residuals.append((correlation + 2) // 2)
    residual_vector = tuple(residuals)
    if (
        _strict_int_vector(
            payload, "periodic_correlation_sums_1_through_166", INDEPENDENT_LAGS
        )
        != independent
    ):
        raise ValueError("recorded periodic correlation vector is incorrect")
    if (
        _strict_int_vector(
            payload, "half_paf_residuals_1_through_166", INDEPENDENT_LAGS
        )
        != residual_vector
    ):
        raise ValueError("recorded half-PAF residual vector is incorrect")

    energy = sum(value * value for value in residual_vector)
    bad_lags = sum(value != 0 for value in residual_vector)
    paf_residuals = tuple(correlation + 2 for correlation in independent)
    max_abs = max(map(abs, paf_residuals), default=0)
    l1 = sum(map(abs, paf_residuals))
    for field, expected in (
        ("energy_half_paf", energy),
        ("energy_paf", 4 * energy),
        ("bad_lag_count", bad_lags),
        ("max_abs_paf_residual", max_abs),
        ("l1_paf_residual", l1),
    ):
        if _strict_int(payload, field) != expected:
            raise ValueError(f"recorded {field} is incorrect")
    if energy == 0 or bad_lags == 0:
        raise ValueError(
            "zero-energy states belong exclusively to verify_legendre_333.py"
        )
    return {
        "energy_half_paf": energy,
        "bad_lag_count": bad_lags,
        "max_abs_paf_residual": max_abs,
        "l1_paf_residual": l1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    args = parser.parse_args()
    diagnostics = verify_profile_checkpoint(json.loads(args.checkpoint.read_text()))
    print("VERIFIED NONEXACT PROFILE CHECKPOINT — NOT H(668)")
    print(
        f"energy_half_paf={diagnostics['energy_half_paf']} "
        f"bad_lag_count={diagnostics['bad_lag_count']} "
        f"max_abs_paf_residual={diagnostics['max_abs_paf_residual']} "
        f"l1_paf_residual={diagnostics['l1_paf_residual']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Exact primitives for the fixed-compression ``LP(333)`` search.

The search uses the conjectural 9-compression proposed for lengths
``p*q^2`` with ``p=37`` and ``q=3``.  All arithmetic in this module is
integer arithmetic; floating-point Fourier transforms are deliberately not
used for acceptance or rejection.

The CRT array convention is

    matrix[row][column] = sequence[i]

where ``i == row (mod 9)`` and ``i == column (mod 37)``.  Consequently the
37 column sums are the factor-9 compression, and the 9 row sums are the
factor-37 compression.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from construction import two_circulant_legendre, verify_hadamard


N = 333
ROW_MODULUS = 9
COLUMN_MODULUS = 37
TARGET_HADAMARD_ORDER = 2 * N + 2


def validate_sign_sequence(sequence: Sequence[int], length: int = N) -> None:
    """Raise ``ValueError`` unless ``sequence`` is a sign vector of ``length``."""

    if len(sequence) != length:
        raise ValueError(f"expected length {length}, got {len(sequence)}")
    if any(type(value) is not int or value not in (-1, 1) for value in sequence):
        raise ValueError("sequence entries must all be +1 or -1")


def legendre_symbol_37(value: int) -> int:
    """Return the quadratic character of ``value`` modulo 37."""

    residue = value % COLUMN_MODULUS
    if residue == 0:
        return 0
    criterion = pow(residue, (COLUMN_MODULUS - 1) // 2, COLUMN_MODULUS)
    if criterion == 1:
        return 1
    if criterion == COLUMN_MODULUS - 1:
        return -1
    raise AssertionError("Euler criterion returned an impossible value")


def fixed_legendre_compressions() -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the prescribed length-37 compressed pair ``(C(37,3),D(37,3))``."""

    a = (1,) + tuple(3 * legendre_symbol_37(index) for index in range(1, 37))
    b = (1,) + tuple(-3 * legendre_symbol_37(index) for index in range(1, 37))
    return a, b


FIXED_COMPRESSION_A, FIXED_COMPRESSION_B = fixed_legendre_compressions()


def plus_count_from_compressed_sum(value: int, block_size: int = ROW_MODULUS) -> int:
    """Convert a sign sum over ``block_size`` positions to its number of +1s."""

    if not -block_size <= value <= block_size:
        raise ValueError("compressed sum is outside the block-size range")
    if (block_size + value) % 2:
        raise ValueError("compressed sum has the wrong parity")
    return (block_size + value) // 2


FIXED_PLUS_COUNTS_A = tuple(
    plus_count_from_compressed_sum(value) for value in FIXED_COMPRESSION_A
)
FIXED_PLUS_COUNTS_B = tuple(
    plus_count_from_compressed_sum(value) for value in FIXED_COMPRESSION_B
)


def crt_index(row: int, column: int) -> int:
    """Map ``Z/9 x Z/37`` coordinates to the canonical index in ``Z/333``."""

    if not 0 <= row < ROW_MODULUS:
        raise ValueError(f"row must be in [0,{ROW_MODULUS})")
    if not 0 <= column < COLUMN_MODULUS:
        raise ValueError(f"column must be in [0,{COLUMN_MODULUS})")

    # Every solution is column + 37*t.  Since 37 == 1 (mod 9), choose
    # t == row-column (mod 9).
    result = column + COLUMN_MODULUS * ((row - column) % ROW_MODULUS)
    if result % ROW_MODULUS != row or result % COLUMN_MODULUS != column:
        raise AssertionError("internal CRT map failure")
    return result


def crt_coordinates(index: int) -> tuple[int, int]:
    """Return the CRT row and column of an index in ``Z/333``."""

    if not 0 <= index < N:
        raise ValueError(f"index must be in [0,{N})")
    return index % ROW_MODULUS, index % COLUMN_MODULUS


CRT_INDEX_TABLE = tuple(
    tuple(crt_index(row, column) for column in range(COLUMN_MODULUS))
    for row in range(ROW_MODULUS)
)


def crt_matrix(sequence: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    """Arrange a length-333 sequence as its exact 9 by 37 CRT matrix."""

    validate_sign_sequence(sequence)
    return tuple(
        tuple(sequence[CRT_INDEX_TABLE[row][column]] for column in range(37))
        for row in range(9)
    )


def sequence_from_crt_matrix(matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Invert :func:`crt_matrix`."""

    if len(matrix) != ROW_MODULUS:
        raise ValueError(f"expected {ROW_MODULUS} CRT rows")
    if any(len(row) != COLUMN_MODULUS for row in matrix):
        raise ValueError(f"every CRT row must have length {COLUMN_MODULUS}")
    result = [0] * N
    for row in range(ROW_MODULUS):
        for column in range(COLUMN_MODULUS):
            value = matrix[row][column]
            if type(value) is not int or value not in (-1, 1):
                raise ValueError("CRT matrix entries must all be +1 or -1")
            result[CRT_INDEX_TABLE[row][column]] = value
    return tuple(result)


def compress_to_modulus(sequence: Sequence[int], modulus: int) -> tuple[int, ...]:
    """Sum entries in each residue class modulo ``modulus``."""

    validate_sign_sequence(sequence)
    if modulus <= 0 or N % modulus:
        raise ValueError("compression modulus must be a positive divisor of 333")
    return tuple(
        sum(sequence[index] for index in range(residue, N, modulus))
        for residue in range(modulus)
    )


def compression_37(sequence: Sequence[int]) -> tuple[int, ...]:
    """Return the factor-9 compression of length 37."""

    return compress_to_modulus(sequence, COLUMN_MODULUS)


def compression_9(sequence: Sequence[int]) -> tuple[int, ...]:
    """Return the factor-37 compression of length 9."""

    return compress_to_modulus(sequence, ROW_MODULUS)


def periodic_autocorrelation(sequence: Sequence[int], lag: int) -> int:
    """Compute one periodic autocorrelation coefficient exactly."""

    validate_sign_sequence(sequence)
    if not 0 <= lag < N:
        raise ValueError(f"lag must be in [0,{N})")
    return sum(sequence[index] * sequence[(index + lag) % N] for index in range(N))


def periodic_autocorrelations(
    sequence: Sequence[int], last_lag: int = N - 1
) -> tuple[int, ...]:
    """Compute exact PAF coefficients from lag zero through ``last_lag``."""

    validate_sign_sequence(sequence)
    if not 0 <= last_lag < N:
        raise ValueError(f"last_lag must be in [0,{N})")
    return tuple(periodic_autocorrelation(sequence, lag) for lag in range(last_lag + 1))


def xor_distance(sequence: Sequence[int], lag: int) -> int:
    """Count positions whose signs differ after a cyclic shift by ``lag``."""

    validate_sign_sequence(sequence)
    if not 0 <= lag < N:
        raise ValueError(f"lag must be in [0,{N})")
    return sum(sequence[index] != sequence[(index + lag) % N] for index in range(N))


def verify_fixed_compression(
    a: Sequence[int], b: Sequence[int]
) -> tuple[bool, tuple[int, ...], tuple[int, ...]]:
    """Check and return the two prescribed length-37 compressions."""

    actual_a = compression_37(a)
    actual_b = compression_37(b)
    valid = actual_a == FIXED_COMPRESSION_A and actual_b == FIXED_COMPRESSION_B
    return valid, actual_a, actual_b


@dataclass(frozen=True)
class LegendreVerification:
    """Exact verification result for a normalized fixed-compression pair."""

    sum_a: int
    sum_b: int
    compression_a: tuple[int, ...]
    compression_b: tuple[int, ...]
    fixed_compression_matches: bool
    correlation_sums: tuple[int, ...]
    bad_lags: tuple[tuple[int, int], ...]

    @property
    def valid(self) -> bool:
        return (
            self.sum_a == 1
            and self.sum_b == 1
            and self.fixed_compression_matches
            and not self.bad_lags
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "sum_a": self.sum_a,
            "sum_b": self.sum_b,
            "fixed_compression_matches": self.fixed_compression_matches,
            "compression_a": list(self.compression_a),
            "compression_b": list(self.compression_b),
            "bad_lags": [
                {"lag": lag, "correlation_sum": value}
                for lag, value in self.bad_lags
            ],
            "periodic_correlation_sums_0_through_166": list(
                self.correlation_sums
            ),
        }


def verify_legendre_pair(a: Sequence[int], b: Sequence[int]) -> LegendreVerification:
    """Verify every defining equation for the prescribed ``LP(333)`` route."""

    validate_sign_sequence(a)
    validate_sign_sequence(b)
    fixed, compression_a, compression_b = verify_fixed_compression(a, b)
    paf_a = periodic_autocorrelations(a, (N - 1) // 2)
    paf_b = periodic_autocorrelations(b, (N - 1) // 2)
    correlation_sums = tuple(x + y for x, y in zip(paf_a, paf_b, strict=True))
    bad_lags = tuple(
        (lag, correlation_sums[lag])
        for lag in range(1, (N - 1) // 2 + 1)
        if correlation_sums[lag] != -2
    )
    return LegendreVerification(
        sum_a=sum(a),
        sum_b=sum(b),
        compression_a=compression_a,
        compression_b=compression_b,
        fixed_compression_matches=fixed,
        correlation_sums=correlation_sums,
        bad_lags=bad_lags,
    )


def candidate_payload(a: Sequence[int], b: Sequence[int]) -> dict[str, Any]:
    """Build the canonical JSON payload for an exactly verified solution."""

    report = verify_legendre_pair(a, b)
    if not report.valid:
        raise ValueError("candidate is not an exact fixed-compression LP(333)")
    hadamard = two_circulant_legendre(a, b)
    verify_hadamard(hadamard)
    return {
        "kind": "fixed-compression-legendre-pair",
        "length": N,
        "hadamard_order": TARGET_HADAMARD_ORDER,
        "hadamard_construction": "bordered-two-circulant",
        "hadamard_verified": True,
        "a": list(a),
        "b": list(b),
        "a_plus_support": [index for index, value in enumerate(a) if value == 1],
        "b_plus_support": [index for index, value in enumerate(b) if value == 1],
        "verification": report.as_dict(),
    }


def sequences_from_candidate(payload: Any) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Extract ``a`` and ``b`` from the canonical or a minimal candidate object."""

    if not isinstance(payload, dict):
        raise ValueError("candidate JSON must contain an object")
    if "a" in payload and "b" in payload:
        raw_a, raw_b = payload["a"], payload["b"]
    elif isinstance(payload.get("sequences"), dict):
        raw_a = payload["sequences"].get("a")
        raw_b = payload["sequences"].get("b")
    else:
        raise ValueError("candidate JSON must contain 'a' and 'b' sequences")
    if not isinstance(raw_a, list) or not isinstance(raw_b, list):
        raise ValueError("candidate sequences must be JSON arrays")
    a = tuple(raw_a)
    b = tuple(raw_b)
    validate_sign_sequence(a)
    validate_sign_sequence(b)
    return a, b


def load_candidate(path: Path) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Load sign sequences from a candidate JSON file."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    return sequences_from_candidate(payload)


def save_verified_candidate(path: Path, a: Sequence[int], b: Sequence[int]) -> None:
    """Verify and write a canonically formatted candidate JSON file."""

    payload = candidate_payload(a, b)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def verify_fixed_seed_identities() -> None:
    """Assert the exact arithmetic identities of the prescribed compression."""

    a = FIXED_COMPRESSION_A
    b = FIXED_COMPRESSION_B
    if sum(a) != 1 or sum(b) != 1:
        raise AssertionError("fixed compressed sequences must both sum to one")
    if sum(value * value for value in a + b) != 650:
        raise AssertionError("fixed compressed pair has the wrong zero-lag norm")

    def compressed_paf(sequence: Sequence[int], lag: int) -> int:
        return sum(
            sequence[index] * sequence[(index + lag) % COLUMN_MODULUS]
            for index in range(COLUMN_MODULUS)
        )

    for lag in range(1, (COLUMN_MODULUS - 1) // 2 + 1):
        paf_a = compressed_paf(a, lag)
        paf_b = compressed_paf(b, lag)
        character = legendre_symbol_37(lag)
        if paf_a != -9 + 6 * character or paf_b != -9 - 6 * character:
            raise AssertionError(
                f"fixed compressed spectra failed at lag {lag}: {paf_a}, {paf_b}"
            )
        total = paf_a + paf_b
        if total != -18:
            raise AssertionError(
                f"fixed compressed pair failed at lag {lag}: {total}"
            )

    if sum(FIXED_PLUS_COUNTS_A) != 167 or sum(FIXED_PLUS_COUNTS_B) != 167:
        raise AssertionError("fixed column weights do not normalize to sign sum one")

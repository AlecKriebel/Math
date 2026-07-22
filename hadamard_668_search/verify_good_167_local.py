#!/usr/bin/env python3
"""Independently verify a structured local-search near miss.

Success means only that the checkpoint is an internally exact, nonzero-energy
state in the normalized good-matrix search space.  It is explicitly not an
H(668) certificate.  Zero-energy candidates must instead pass
``verify_good_167.py``, including construction of the full 668x668 matrix.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

from good_167 import ORDER, periodic_autocorrelation, product_theorem_holds
from good_167_linear import derive_s, skew_from_negative_mask, symmetric_from_negative_mask
from verify_good_167_stream import derive_a_from_s_b


HALF = (ORDER - 1) // 2
SCHEMA = "hadamard668.good167-local-checkpoint.v1"
ORIENTED_SUMS = ((15, -1, -21), (15, -9, 19))
MASK_PATTERN = re.compile(r"0x[0-7][0-9a-f]{20}\Z")
STATE_PATTERN = re.compile(r"0x[0-9a-f]{1,16}\Z")


def _strict_int(payload: dict[str, object], field: str) -> int:
    value = payload.get(field)
    if type(value) is not int:
        raise ValueError(f"{field} must be an integer")
    return value


def _mask(payload: dict[str, object], name: str) -> int:
    raw = payload.get(f"{name}_mask")
    if not isinstance(raw, str) or MASK_PATTERN.fullmatch(raw) is None:
        raise ValueError(f"{name}_mask is not canonical fixed-width hexadecimal")
    return int(raw, 16)


def verify_local_checkpoint(payload: object) -> dict[str, int]:
    if not isinstance(payload, dict):
        raise ValueError("checkpoint must be a JSON object")
    if payload.get("schema") != SCHEMA:
        raise ValueError("local checkpoint schema is missing or unsupported")
    if payload.get("kind") != "good_matrix_local_checkpoint":
        raise ValueError("kind must be good_matrix_local_checkpoint")
    if payload.get("status") != "near_miss" or payload.get("exact") is not False:
        raise ValueError("local checkpoints must be explicitly nonexact near misses")
    if _strict_int(payload, "order") != ORDER:
        raise ValueError(f"order must be {ORDER}")
    if _strict_int(payload, "hadamard_order") != 4 * ORDER:
        raise ValueError(f"hadamard_order must be {4 * ORDER}")
    profile = _strict_int(payload, "profile")
    if profile not in (0, 1):
        raise ValueError("profile must be 0 or 1")
    if payload.get("parameterization") != "local_sbc":
        raise ValueError("parameterization must be local_sbc")
    expected_sums = ORIENTED_SUMS[profile]
    if payload.get("row_sums") != list(expected_sums):
        raise ValueError("row_sums do not match the profile")
    move = _strict_int(payload, "move")
    seed = _strict_int(payload, "random_seed")
    if move < 0 or not 0 <= seed < 1 << 64:
        raise ValueError("move and random_seed must be nonnegative 64-bit metadata")
    rng_state = payload.get("rng_state")
    if not isinstance(rng_state, str) or STATE_PATTERN.fullmatch(rng_state) is None:
        raise ValueError("rng_state is not canonical hexadecimal")

    masks = {name: _mask(payload, name) for name in ("s", "a", "b", "c", "d")}
    if masks["a"] & 1:
        raise ValueError("A[1]=+1 normalization is missing")
    expected_weights = (38, (42, 44)[profile], (47, 37)[profile])
    if tuple(masks[name].bit_count() for name in ("b", "c", "d")) != expected_weights:
        raise ValueError("B,C,D masks do not have the exact profile weights")
    if masks["s"] != masks["c"] ^ masks["d"]:
        raise ValueError("S is not C xor D")
    if masks["s"].bit_count() % 2 != 1:
        raise ValueError("S must have odd half-weight")

    a = skew_from_negative_mask(masks["a"])
    b = symmetric_from_negative_mask(masks["b"])
    c = symmetric_from_negative_mask(masks["c"])
    d = symmetric_from_negative_mask(masks["d"])
    s = symmetric_from_negative_mask(masks["s"])
    if tuple(sum(sequence) for sequence in (b, c, d)) != expected_sums:
        raise ValueError("expanded B,C,D row sums are incorrect")
    if derive_s(a, b) != s:
        raise ValueError("S is not the product-theorem quotient of A,B")
    if derive_a_from_s_b(s, b) != a:
        raise ValueError("S,B recurrence does not recover A")
    if tuple(left * right for left, right in zip(s, c, strict=True)) != d:
        raise ValueError("D is not the pointwise product S*C")
    if not product_theorem_holds(a, b, c, d):
        raise ValueError("good-matrix product theorem fails")

    full_residuals = []
    for lag in range(1, ORDER):
        residual = sum(
            periodic_autocorrelation(sequence, lag)
            for sequence in (a, b, c, d)
        )
        if residual % 4:
            raise ValueError(f"lag {lag} residual is not divisible by four")
        full_residuals.append(residual // 4)
    quarter_residuals = full_residuals[:HALF]
    if any(
        full_residuals[lag - 1] != full_residuals[ORDER - lag - 1]
        for lag in range(1, HALF + 1)
    ):
        raise ValueError("PAF reflection identity fails")
    raw_residuals = payload.get("quarter_residuals")
    if (
        not isinstance(raw_residuals, list)
        or len(raw_residuals) != HALF
        or any(type(value) is not int for value in raw_residuals)
        or raw_residuals != quarter_residuals
    ):
        raise ValueError("quarter_residuals are not the exact 83-lag vector")
    energy = sum(value * value for value in quarter_residuals)
    bad_lags = sum(value != 0 for value in quarter_residuals)
    max_abs_quarter = max(map(abs, quarter_residuals), default=0)
    for field, expected in (
        ("energy", energy),
        ("bad_lags", bad_lags),
        ("max_abs_quarter", max_abs_quarter),
    ):
        if _strict_int(payload, field) != expected:
            raise ValueError(f"recorded {field} is incorrect")
    if energy == 0 or bad_lags == 0:
        raise ValueError("zero-energy states belong exclusively to the exact verifier")
    return {
        "energy": energy,
        "bad_lags": bad_lags,
        "max_abs_quarter": max_abs_quarter,
        "s_weight": masks["s"].bit_count(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    args = parser.parse_args()
    diagnostics = verify_local_checkpoint(json.loads(args.checkpoint.read_text()))
    print("VERIFIED NONEXACT CHECKPOINT — NOT H(668)")
    print(
        f"energy={diagnostics['energy']} bad_lags={diagnostics['bad_lags']} "
        f"max_abs_quarter={diagnostics['max_abs_quarter']} "
        f"s_weight={diagnostics['s_weight']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Independently verify a C++ good-matrix streaming checkpoint.

The checkpoint is a near-miss, not a construction certificate.  This script
replays its local RNG state, rebuilds the Python GF(2) system, verifies the
affine C solution and exact C,D weights, and recomputes every integer PAF
residual.  Exact candidates use the separate ``verify_good_167.py`` path.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from good_167 import ORDER, periodic_autocorrelation, product_theorem_holds
from good_167_linear import (
    c_linear_system,
    skew_from_negative_mask,
    solve_linear_system,
    symmetric_from_negative_mask,
)


HALF = (ORDER - 1) // 2
MASK64 = (1 << 64) - 1
MASK83 = (1 << HALF) - 1
ORIENTED_SUMS = ((15, -1, -21), (15, -9, 19))


class SplitMix64:
    """The exact explicitly specified generator used by the C++ sampler."""

    def __init__(self, state: int):
        if not 0 <= state <= MASK64:
            raise ValueError("SplitMix64 state is outside 64 bits")
        self.state = state

    def next(self) -> int:
        self.state = (self.state + 0x9E3779B97F4A7C15) & MASK64
        value = self.state
        value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & MASK64
        value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & MASK64
        return value ^ (value >> 31)

    def bounded(self, bound: int) -> int:
        if bound <= 0:
            raise ValueError("bound must be positive")
        threshold = ((-bound) & MASK64) % bound
        while True:
            value = self.next()
            if value >= threshold:
                return value % bound


def _parse_hex_mask(value: object, bits: int, field: str) -> int:
    if not isinstance(value, str) or not value.startswith("0x"):
        raise ValueError(f"{field} must be a hexadecimal string")
    try:
        parsed = int(value, 16)
    except ValueError as error:
        raise ValueError(f"{field} is not hexadecimal") from error
    if not 0 <= parsed < 1 << bits:
        raise ValueError(f"{field} exceeds {bits} bits")
    return parsed


def replay_trial_state(state: int) -> tuple[int, int, int]:
    """Return ``(A mask, B mask, next state)`` for one production trial."""

    rng = SplitMix64(state)
    a_mask = (rng.next() | ((rng.next() & ((1 << 19) - 1)) << 64)) & MASK83
    a_mask &= ~1
    indices = list(range(HALF))
    b_mask = 0
    for index in range(38):
        chosen = index + rng.bounded(HALF - index)
        indices[index], indices[chosen] = indices[chosen], indices[index]
        b_mask |= 1 << indices[index]
    return a_mask, b_mask, rng.state


def replay_b_state(state: int) -> tuple[int, int]:
    """Return ``(B mask, next state)`` for one S,B inner-loop trial."""

    rng = SplitMix64(state)
    indices = list(range(HALF))
    b_mask = 0
    for index in range(38):
        chosen = index + rng.bounded(HALF - index)
        indices[index], indices[chosen] = indices[chosen], indices[index]
        b_mask |= 1 << indices[index]
    return b_mask, rng.state


def derive_a_from_s_b(s: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    """Invert the product quotient along the order-83 doubling cycle."""

    a = [0] * ORDER
    a[0] = 1
    a[1] = 1
    index = 1
    for step in range(HALF):
        next_index = 2 * index % ORDER
        next_sign = -s[index] * a[index] * b[index]
        if step + 1 == HALF:
            if next_index != 1 or next_sign != 1:
                raise ValueError("S,B doubling recurrence does not close")
        else:
            if next_index == 1 or a[next_index] != 0:
                raise ValueError("doubling cycle repeats before closure")
            a[next_index] = next_sign
        index = next_index
    for index in range(1, ORDER):
        if a[index] == 0 and a[-index] != 0:
            a[index] = -a[-index]
    if any(a[index] != -a[-index] for index in range(1, HALF + 1)):
        raise ValueError("recovered A is not skew")
    return tuple(a)


def is_maximal_doubling_necklace(mask: int) -> bool:
    cycle = []
    value = 1
    for _ in range(HALF):
        representative = min(value, ORDER - value)
        cycle.append(representative - 1)
        value = 2 * value % ORDER
    if value != 1 or len(set(cycle)) != HALF:
        raise AssertionError("unexpected order-167 doubling cycle")
    word = tuple((mask >> variable) & 1 for variable in cycle)
    return all(word >= word[shift:] + word[:shift] for shift in range(1, HALF))


def verify_checkpoint(payload: object) -> dict[str, int]:
    if not isinstance(payload, dict):
        raise ValueError("checkpoint must be a JSON object")
    if payload.get("kind") != "good_matrix_stream_checkpoint":
        raise ValueError("checkpoint kind is not good_matrix_stream_checkpoint")
    if type(payload.get("order")) is not int or payload["order"] != ORDER:
        raise ValueError(f"checkpoint order must be {ORDER}")
    profile = payload.get("profile")
    if type(profile) is not int or profile not in (0, 1):
        raise ValueError("profile must be 0 or 1")
    expected_sums = ORIENTED_SUMS[profile]
    if payload.get("row_sums") != list(expected_sums):
        raise ValueError("checkpoint row sums do not match its profile")

    parameterization = payload.get("parameterization", "ab")
    if parameterization not in ("ab", "sb"):
        raise ValueError("parameterization must be ab or sb")
    masks = {
        name: _parse_hex_mask(payload.get(f"{name}_mask"), HALF, f"{name}_mask")
        for name in ("a", "b", "c", "d")
    }
    if masks["a"] & 1:
        raise ValueError("A[1]=+1 normalization is missing")
    if masks["b"].bit_count() != 38:
        raise ValueError("B does not have half-weight 38")

    trial_state = _parse_hex_mask(
        payload.get("trial_rng_state"), 64, "trial_rng_state"
    )
    expected_next_state = _parse_hex_mask(
        payload.get("next_rng_state"), 64, "next_rng_state"
    )
    if parameterization == "ab":
        replay_a, replay_b, replay_next = replay_trial_state(trial_state)
        if (replay_a, replay_b, replay_next) != (
            masks["a"],
            masks["b"],
            expected_next_state,
        ):
            raise ValueError("checkpoint does not replay from its saved RNG state")
    else:
        replay_b, replay_next = replay_b_state(trial_state)
        if (replay_b, replay_next) != (masks["b"], expected_next_state):
            raise ValueError("checkpoint B does not replay from its saved RNG state")

    a = skew_from_negative_mask(masks["a"])
    b = symmetric_from_negative_mask(masks["b"])
    c = symmetric_from_negative_mask(masks["c"])
    d = symmetric_from_negative_mask(masks["d"])
    if sum(b) != expected_sums[0] or sum(c) != expected_sums[1] or sum(d) != expected_sums[2]:
        raise ValueError("sequence masks do not have the recorded row sums")

    system, s = c_linear_system(a, b)
    derived_s_mask = sum(
        1 << (index - 1) for index in range(1, HALF + 1) if s[index] == -1
    )
    if "s_mask" in payload:
        recorded_s_mask = _parse_hex_mask(payload["s_mask"], HALF, "s_mask")
        if recorded_s_mask != derived_s_mask:
            raise ValueError("recorded S is not the product quotient")
    else:
        recorded_s_mask = derived_s_mask
    if parameterization == "sb":
        minimum, maximum = ((5, 77), (7, 81))[profile]
        if not (
            minimum <= recorded_s_mask.bit_count() <= maximum
            and recorded_s_mask.bit_count() % 2 == 1
        ):
            raise ValueError("S weight is infeasible for the checkpoint profile")
        if not is_maximal_doubling_necklace(recorded_s_mask):
            raise ValueError("S is not the canonical doubling necklace")
        if derive_a_from_s_b(s, b) != a:
            raise ValueError("S,B recurrence does not recover the recorded A")
    if system.early_rejection is not None:
        raise ValueError(f"Python reducer rejects checkpoint early: {system.early_rejection}")
    solution = solve_linear_system(system)
    if solution is None or solution.inconsistent:
        raise ValueError("Python reducer says the checkpoint system is inconsistent")
    if type(payload.get("rank")) is not int or payload["rank"] != solution.rank:
        raise ValueError("recorded GF(2) rank is incorrect")
    if any(
        (coefficient_mask & masks["c"]).bit_count() % 2 != rhs
        for coefficient_mask, rhs in system.rows
    ):
        raise ValueError("C does not satisfy the Python GF(2) system")
    if masks["d"] != masks["c"] ^ recorded_s_mask:
        raise ValueError("D is not S*C")
    if not product_theorem_holds(a, b, c, d):
        raise ValueError("good-matrix product theorem fails")

    quarter_residuals = []
    for lag in range(1, HALF + 1):
        residual = sum(periodic_autocorrelation(sequence, lag) for sequence in (a, b, c, d))
        if residual % 4:
            raise ValueError(f"lag {lag} residual is not divisible by four")
        quarter_residuals.append(residual // 4)
    if payload.get("quarter_residuals") != quarter_residuals:
        raise ValueError("recorded quarter residual vector is incorrect")
    energy = sum(value * value for value in quarter_residuals)
    bad_lags = sum(value != 0 for value in quarter_residuals)
    max_abs_quarter = max(map(abs, quarter_residuals), default=0)
    for field, expected in (
        ("energy", energy),
        ("bad_lags", bad_lags),
        ("max_abs_quarter", max_abs_quarter),
    ):
        if type(payload.get(field)) is not int or payload[field] != expected:
            raise ValueError(f"recorded {field} is incorrect")
    if energy == 0:
        raise ValueError("an exact candidate must use verify_good_167.py, not a near-miss checkpoint")
    return {
        "rank": solution.rank,
        "energy": energy,
        "bad_lags": bad_lags,
        "max_abs_quarter": max_abs_quarter,
    }


def self_test() -> None:
    rng = SplitMix64(668)
    expected = (
        0xC33416AAE473D238,
        0x3B8136E0FF77E131,
        0x60589B6AE8406F3F,
        0x58EDD5F5ED8CB9C0,
    )
    if tuple(rng.next() for _ in expected) != expected:
        raise AssertionError("SplitMix64 fixture failed")
    a_mask, b_mask, _ = replay_trial_state(668)
    if a_mask & 1 or b_mask.bit_count() != 38:
        raise AssertionError("trial generator structural fixture failed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("PASS: streaming RNG self-test")
    if args.checkpoint is None:
        if args.self_test:
            return 0
        parser.error("provide a checkpoint or --self-test")
    diagnostics = verify_checkpoint(json.loads(args.checkpoint.read_text()))
    print("PASS: C++ checkpoint matches the independent Python reducer")
    print(
        f"rank={diagnostics['rank']} energy={diagnostics['energy']} "
        f"bad_lags={diagnostics['bad_lags']} "
        f"max_abs_quarter={diagnostics['max_abs_quarter']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

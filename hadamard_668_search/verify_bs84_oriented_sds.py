#!/usr/bin/env python3
"""Strict, dependency-free verifier for prime-83 oriented-SDS candidates.

The accepted artifact is produced by ``search_bs84_oriented_sds.py``.  It
contains four negative-entry sets ``X,Y,Z,W`` for the endpoint fold

    U[0]=0, V[0]=2, U/V otherwise binary, C/D binary.

The verifier independently checks all 82 periodic correlations, all 82
oriented supplementary-difference-set equations, the canonical size profile,
and every redundant sequence field.  If a modulo-84 lift is present, it also
checks all 83 aperiodic ``BS(84,83)`` equations and expands and verifies the
full order-668 Goethals--Seidel matrix.

Only the Python standard library and the repository's exact construction
helpers are used.  In particular, this verifier does not import OR-Tools.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import itertools
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


PRIME = 83
HALF = 41
ENERGY = 334
FORMAT = "h668-oriented-sds-v1"
CHECKPOINT_FORMAT = "h668-oriented-sds-local-checkpoint-v1"


def periodic(sequence: tuple[int, ...], lag: int) -> int:
    length = len(sequence)
    return sum(
        sequence[index] * sequence[(index + lag) % length]
        for index in range(length)
    )


def aperiodic(sequence: tuple[int, ...], lag: int) -> int:
    return sum(
        sequence[index] * sequence[index + lag]
        for index in range(len(sequence) - lag)
    )


@lru_cache(maxsize=1)
def canonical_profiles() -> tuple[tuple[int, int, int, int], ...]:
    """Return the 45 anchored-canonical size profiles in stable order."""

    profiles = []
    for x_size in range(HALF + 1):
        for y_size in range(PRIME):
            for z_size in range(HALF + 1):
                for w_size in range(z_size, HALF + 1):
                    row_sums = (
                        82 - 2 * x_size,
                        84 - 2 * y_size,
                        83 - 2 * z_size,
                        83 - 2 * w_size,
                    )
                    if sum(value * value for value in row_sums) == ENERGY:
                        profiles.append((x_size, y_size, z_size, w_size))
    if len(profiles) != 45:
        raise AssertionError(f"expected 45 profiles, got {len(profiles)}")
    return tuple(profiles)


def strict_integer(value: Any, label: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{label} must be an integer")
    return value


def strict_set(value: Any, label: str, *, omit_zero: bool) -> frozenset[int]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a JSON array")
    entries = tuple(
        strict_integer(entry, f"{label}[{index}]")
        for index, entry in enumerate(value)
    )
    if entries != tuple(sorted(entries)):
        raise ValueError(f"{label} must be strictly increasing")
    if len(set(entries)) != len(entries):
        raise ValueError(f"{label} contains a duplicate")
    if any(not 0 <= entry < PRIME for entry in entries):
        raise ValueError(f"{label} contains a residue outside 0..82")
    if omit_zero and 0 in entries:
        raise ValueError(f"{label} must omit the anomalous residue zero")
    return frozenset(entries)


def strict_sequence(value: Any, length: int, label: str) -> tuple[int, ...]:
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"{label} must be a JSON array of length {length}")
    result = tuple(
        strict_integer(entry, f"{label}[{index}]")
        for index, entry in enumerate(value)
    )
    return result


def folded_sequences(
    x_set: frozenset[int],
    y_set: frozenset[int],
    z_set: frozenset[int],
    w_set: frozenset[int],
) -> tuple[tuple[int, ...], ...]:
    u = tuple(
        0 if index == 0 else (-1 if index in x_set else 1)
        for index in range(PRIME)
    )
    v = tuple(
        2 if index == 0 else (-1 if index in y_set else 1)
        for index in range(PRIME)
    )
    c = tuple(-1 if index in z_set else 1 for index in range(PRIME))
    d = tuple(-1 if index in w_set else 1 for index in range(PRIME))
    return u, v, c, d


def difference_count(block: frozenset[int], lag: int) -> int:
    return sum(1 for value in block if (value + lag) % PRIME in block)


PAIR_STATES = tuple(
    bits
    for bits in itertools.product((0, 1), repeat=4)
    if (bits[0] + bits[1] - bits[2] - bits[3]) % 2 == 0
)


def pair_state_counts(state: tuple[int, int, int, int]) -> tuple[int, int]:
    return state[0] + state[1], state[2] + state[3]


def xy_pair_states(
    x_set: frozenset[int], y_set: frozenset[int]
) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        (
            int(lag in x_set),
            int(PRIME - lag in x_set),
            int(lag in y_set),
            int(PRIME - lag in y_set),
        )
        for lag in range(1, HALF + 1)
    )


def xy_move_count(
    states: tuple[tuple[int, int, int, int], ...], support: int
) -> int:
    """Replay the C++ support-two or support-three transition count."""

    if support not in (2, 3):
        raise ValueError("pair-state support must be two or three")
    result = 1
    if support == 2:
        for old in states:
            target = pair_state_counts(old)
            result += sum(
                candidate != old and pair_state_counts(candidate) == target
                for candidate in PAIR_STATES
            )
    for positions in itertools.combinations(range(HALF), support):
        target_x = sum(pair_state_counts(states[position])[0] for position in positions)
        target_y = sum(pair_state_counts(states[position])[1] for position in positions)
        old_tuple = tuple(states[position] for position in positions)
        for candidates in itertools.product(PAIR_STATES, repeat=support):
            if candidates == old_tuple:
                continue
            if (
                sum(pair_state_counts(candidate)[0] for candidate in candidates)
                == target_x
                and sum(
                    pair_state_counts(candidate)[1] for candidate in candidates
                )
                == target_y
            ):
                result += 1
    return result


def transform(
    sequence: tuple[int, ...], multiplier: int, shift: int = 0
) -> tuple[int, ...]:
    return tuple(
        sequence[(multiplier * index + shift) % PRIME]
        for index in range(PRIME)
    )


def reconstruct_lift(
    folded: tuple[tuple[int, ...], ...],
    multiplier: int,
    shift_c: int,
    shift_d: int,
) -> tuple[tuple[int, ...], ...]:
    u, v, c, d = folded
    transformed_u = transform(u, multiplier)
    transformed_v = transform(v, multiplier)
    transformed_c = transform(c, multiplier, shift_c)
    transformed_d = transform(d, multiplier, shift_d)
    if transformed_u[0] != 0 or transformed_v[0] != 2:
        raise AssertionError("common multiplier moved an anomalous coordinate")
    a = (1, *transformed_u[1:], -1)
    b = (1, *transformed_v[1:], 1)
    return a, b, transformed_c, transformed_d


def special_quadruple_from_base(
    base: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Reconstruct ``(s,s',sq,(sq)')`` without importing search code."""

    a, b, c, d = base
    return (
        (*a, *c),
        (*a, *(-value for value in c)),
        (*b, *d),
        (*b, *(-value for value in d)),
    )


def summed_aperiodic(
    sequences: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    length = len(sequences[0])
    if any(len(sequence) != length for sequence in sequences):
        raise ValueError("special sequences have unequal lengths")
    return tuple(
        sum(aperiodic(sequence, lag) for sequence in sequences)
        for lag in range(length)
    )


def circulant(first_row: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    length = len(first_row)
    return tuple(
        tuple(first_row[(column - row) % length] for column in range(length))
        for row in range(length)
    )


def transpose(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(matrix[row][column] for row in range(len(matrix)))
                 for column in range(len(matrix)))


def reverse_columns(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(reversed(row)) for row in matrix)


def negate(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(-entry for entry in row) for row in matrix)


def goethals_seidel(
    sequences: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Expand the exact Goethals--Seidel array in Eliahou's convention."""

    if len(sequences) != 4 or any(
        len(sequence) != len(sequences[0]) for sequence in sequences
    ):
        raise ValueError("Goethals--Seidel requires four equal-length rows")
    a, b, c, d = tuple(circulant(sequence) for sequence in sequences)
    br = reverse_columns(b)
    cr = reverse_columns(c)
    dr = reverse_columns(d)
    btr = reverse_columns(transpose(b))
    ctr = reverse_columns(transpose(c))
    dtr = reverse_columns(transpose(d))
    block_rows = (
        (a, negate(br), negate(cr), negate(dr)),
        (br, a, negate(dtr), ctr),
        (cr, dtr, a, negate(btr)),
        (dr, negate(ctr), btr, a),
    )
    result = []
    block_size = len(a)
    for blocks in block_rows:
        for row_index in range(block_size):
            row = []
            for block in blocks:
                row.extend(block[row_index])
            result.append(tuple(row))
    return tuple(result)


def verify_hadamard(matrix: tuple[tuple[int, ...], ...]) -> None:
    """Check every row pair exactly using packed Python integers."""

    order = len(matrix)
    if order == 0:
        raise ValueError("Hadamard matrix is empty")
    packed = []
    for row in matrix:
        if len(row) != order or any(entry not in (-1, 1) for entry in row):
            raise ValueError("Hadamard candidate is not a square sign matrix")
        value = 0
        for index, entry in enumerate(row):
            if entry == 1:
                value |= 1 << index
        packed.append(value)
    for left_index, left in enumerate(packed):
        for right_index in range(left_index):
            difference = left ^ packed[right_index]
            # ``int.bit_count`` is absent from the repository's older solver
            # environment, so retain a dependency-free compatibility path.
            count = (
                difference.bit_count()
                if hasattr(difference, "bit_count")
                else bin(difference).count("1")
            )
            dot = order - 2 * count
            if dot:
                raise ValueError(
                    "Hadamard orthogonality failed for rows "
                    f"{right_index},{left_index}: dot={dot}"
                )


def verify_payload(
    payload: Any, *, allow_checkpoint: bool = False
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("candidate JSON must contain an object")
    artifact_format = payload.get("format")
    checkpoint = artifact_format == CHECKPOINT_FORMAT
    if artifact_format != FORMAT and not (allow_checkpoint and checkpoint):
        expected = f"{FORMAT!r}"
        if allow_checkpoint:
            expected += f" or {CHECKPOINT_FORMAT!r}"
        raise ValueError(f"format must be {expected}")
    if strict_integer(payload.get("modulus"), "modulus") != PRIME:
        raise ValueError("modulus must be 83")

    x_set = strict_set(payload.get("x"), "x", omit_zero=True)
    y_set = strict_set(payload.get("y"), "y", omit_zero=True)
    z_set = strict_set(payload.get("z"), "z", omit_zero=False)
    w_set = strict_set(payload.get("w"), "w", omit_zero=False)
    sizes = (len(x_set), len(y_set), len(z_set), len(w_set))

    profile_index = strict_integer(payload.get("profile_index"), "profile_index")
    profiles = canonical_profiles()
    if not 0 <= profile_index < len(profiles):
        raise ValueError("profile_index is outside 0..44")
    if sizes != profiles[profile_index]:
        raise ValueError(
            f"set sizes {sizes} do not equal profile {profile_index}: "
            f"{profiles[profile_index]}"
        )
    profile = payload.get("profile")
    expected_profile = dict(zip(("x", "y", "z", "w"), sizes))
    if profile != expected_profile:
        raise ValueError(f"profile must equal {expected_profile}")

    folded = folded_sequences(x_set, y_set, z_set, w_set)
    for label, expected in zip(
        ("fold_u", "fold_v", "fold_c", "fold_d"), folded
    ):
        if label in payload:
            supplied = strict_sequence(payload[label], PRIME, label)
            if supplied != expected:
                raise ValueError(f"{label} disagrees with its negative-entry set")

    row_sums = tuple(sum(sequence) for sequence in folded)
    expected_row_sums = (
        82 - 2 * sizes[0],
        84 - 2 * sizes[1],
        83 - 2 * sizes[2],
        83 - 2 * sizes[3],
    )
    if row_sums != expected_row_sums:
        raise AssertionError("row-sum reconstruction failed")
    if sum(value * value for value in row_sums) != ENERGY:
        raise ValueError("row sums do not have squared norm 334")
    if row_sums[0] < 0 or row_sums[2] < row_sums[3] or row_sums[3] < 0:
        raise ValueError("size profile is not anchored-canonical")

    sets = (x_set, y_set, z_set, w_set)
    total_size = sum(sizes)
    target = total_size - PRIME
    paf = []
    osds_left = []
    for lag in range(PRIME):
        direct = sum(periodic(sequence, lag) for sequence in folded)
        paf.append(direct)
        if lag == 0:
            if direct != ENERGY:
                raise ValueError(f"periodic energy is {direct}, not {ENERGY}")
            continue
        ex = int(lag in x_set) + int((-lag) % PRIME in x_set)
        ey = int(lag in y_set) + int((-lag) % PRIME in y_set)
        if (ex - ey) % 2:
            raise ValueError(f"inverse-pair parity fails at lag {lag}")
        left = (
            sum(difference_count(block, lag) for block in sets)
            + (ex - ey) // 2
        )
        osds_left.append(left)
        if direct != 4 * (left - target):
            raise ValueError(
                f"oriented-SDS formula disagrees with direct PAF at lag {lag}"
            )
        if not checkpoint and left != target:
            raise ValueError(
                f"oriented-SDS equation fails at lag {lag}: "
                f"{left} != {target}"
            )
        if not checkpoint and direct != 0:
            raise ValueError(f"periodic complementarity fails at lag {lag}")

    if "periodic_paf_sum" in payload:
        supplied_paf = strict_sequence(
            payload["periodic_paf_sum"], PRIME, "periodic_paf_sum"
        )
        if supplied_paf != tuple(paf):
            raise ValueError("periodic_paf_sum is inconsistent")

    quarter_values = tuple(value // 4 for value in paf[1 : HALF + 1])
    if any(value % 4 for value in paf[1 : HALF + 1]):
        raise ValueError("an independent periodic residual is not divisible by four")
    quarter_energy = sum(value * value for value in quarter_values)
    bad_independent_lags = sum(value != 0 for value in quarter_values)
    maximum_absolute_quarter_residual = max(
        (abs(value) for value in quarter_values), default=0
    )
    if checkpoint:
        expected_checkpoint_fields = {
            "quarter_energy": quarter_energy,
            "bad_independent_lags": bad_independent_lags,
            "maximum_absolute_quarter_residual": (
                maximum_absolute_quarter_residual
            ),
        }
        for label, expected in expected_checkpoint_fields.items():
            if strict_integer(payload.get(label), label) != expected:
                raise ValueError(f"{label} is inconsistent")
        if quarter_energy == 0:
            raise ValueError("an energy-zero artifact must use the exact format")
        audit = payload.get("finite_neighborhood_audit")
        if audit is not None:
            if not isinstance(audit, dict):
                raise ValueError("finite_neighborhood_audit must be an object")
            regular_completed = audit.get("regular_completed")
            deep_completed = audit.get("deep_completed")
            if type(regular_completed) is not bool or type(deep_completed) is not bool:
                raise ValueError("finite-neighborhood completion flags must be Boolean")
            states = xy_pair_states(x_set, y_set)
            expected_counts = {
                "xy_support_at_most_two_moves": (
                    xy_move_count(states, 2) if regular_completed else 0
                ),
                "c_single_exchange_moves": (
                    1 + sizes[2] * (PRIME - sizes[2])
                    if regular_completed
                    else 0
                ),
                "d_single_exchange_moves": (
                    1 + sizes[3] * (PRIME - sizes[3])
                    if regular_completed
                    else 0
                ),
                "c_double_exchange_moves": (
                    1 + comb(sizes[2], 2) * comb(PRIME - sizes[2], 2)
                    if deep_completed
                    else 0
                ),
                "d_double_exchange_moves": (
                    1 + comb(sizes[3], 2) * comb(PRIME - sizes[3], 2)
                    if deep_completed
                    else 0
                ),
                "xy_support_at_most_three_moves": (
                    xy_move_count(states, 3) if deep_completed else 0
                ),
            }
            for label, expected in expected_counts.items():
                supplied = strict_integer(audit.get(label), label)
                if supplied != expected:
                    raise ValueError(
                        f"finite-neighborhood count {label} is inconsistent"
                    )

    result: dict[str, Any] = {
        "profile_index": profile_index,
        "sizes": sizes,
        "row_sums": row_sums,
        "prime_fold_verified": not checkpoint,
        "checkpoint_verified": checkpoint,
        "quarter_energy": quarter_energy,
        "bad_independent_lags": bad_independent_lags,
        "lift_present": False,
        "hadamard_verified": False,
    }

    lift = payload.get("lift")
    if lift is None:
        return result
    if checkpoint:
        raise ValueError("a nonexact checkpoint cannot contain a lift")
    if not isinstance(lift, dict):
        raise ValueError("lift must be null or an object")
    multiplier = strict_integer(lift.get("common_multiplier"), "common_multiplier")
    shift_c = strict_integer(lift.get("shift_c"), "shift_c")
    shift_d = strict_integer(lift.get("shift_d"), "shift_d")
    if not 1 <= multiplier < PRIME:
        raise ValueError("common_multiplier must lie in 1..82")
    if not 0 <= shift_c < PRIME or not 0 <= shift_d < PRIME:
        raise ValueError("phase shifts must lie in 0..82")

    base = reconstruct_lift(folded, multiplier, shift_c, shift_d)
    for label, expected, length in zip(
        ("a", "b", "c", "d"), base, (84, 84, 83, 83)
    ):
        supplied = strict_sequence(lift.get(label), length, f"lift.{label}")
        if supplied != expected:
            raise ValueError(f"lift.{label} disagrees with the recorded action")
        if any(entry not in (-1, 1) for entry in supplied):
            raise ValueError(f"lift.{label} is not binary")

    correlations = tuple(
        sum(
            aperiodic(sequence, lag)
            for sequence in base
            if lag < len(sequence)
        )
        for lag in range(84)
    )
    if correlations != (ENERGY,) + (0,) * 83:
        bad = tuple(index for index, value in enumerate(correlations[1:], 1) if value)
        raise ValueError(f"lift is not BS(84,83); bad lags={bad}")

    quadruple = special_quadruple_from_base(base)
    if summed_aperiodic(quadruple) != (4 * 167,) + (0,) * 166:
        raise ValueError("special length-167 Golay reconstruction failed")
    matrix = goethals_seidel(quadruple)
    verify_hadamard(matrix)
    result["lift_present"] = True
    result["hadamard_verified"] = True
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--allow-checkpoint",
        action="store_true",
        help="also accept and fully replay a nonzero local-search checkpoint",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.candidate.read_text(encoding="utf-8"))
        result = verify_payload(payload, allow_checkpoint=args.allow_checkpoint)
    except (OSError, ValueError, json.JSONDecodeError, AssertionError) as error:
        print(f"error={error}", file=sys.stderr)
        return 1
    print(f"candidate={args.candidate}")
    print(f"profile_index={result['profile_index']}")
    print(f"sizes={','.join(str(value) for value in result['sizes'])}")
    print(f"row_sums={','.join(str(value) for value in result['row_sums'])}")
    print(
        f"checkpoint_verified={str(result['checkpoint_verified']).lower()}"
    )
    print(
        f"quarter_energy={result['quarter_energy']}"
    )
    print(
        f"bad_independent_lags={result['bad_independent_lags']}"
    )
    print(
        f"prime_fold_verified={str(result['prime_fold_verified']).lower()}"
    )
    print(f"lift_present={str(result['lift_present']).lower()}")
    print(f"hadamard_order={668 if result['lift_present'] else 'not_checked'}")
    print(f"hadamard_verified={str(result['hadamard_verified']).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

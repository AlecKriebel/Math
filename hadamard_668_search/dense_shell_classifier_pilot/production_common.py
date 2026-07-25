#!/usr/bin/env python3
"""Exact shared constants and audits for dense-shell production shards.

Nothing in this module searches phase assignments.  It independently
reconstructs the 27-state prefix partition, the Burnside totals, and the
residue-stratified affine-union workload bound used by the runner and strict
aggregator.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


PRODUCTION_SCHEMA = "dense-shell-production-shard-v2"
MANIFEST_SCHEMA = "dense-shell-production-manifest-v2"
RESULT_SCHEMA = "dense-shell-production-result-v2"
AGGREGATE_SCHEMA = "dense-shell-production-aggregate-v2"
PARTITION_SCHEMA = "dense-shell-prefix-partition-audit-v1"
RUNNER_VERSION = "dense-shell-production-runner-v2"
EXACT_ORBIT_POLICY = {
    "mode": "exhaustive_per_prefix_shard",
    "deduplication_key": (
        "lexicographically canonical 24 profile identifiers "
        "followed by exact target index"
    ),
    "verification": (
        "every retained orbit is independently replayed at all "
        "37 physical lags before its result is accepted"
    ),
}

SHELLS = ("h1", "h0")
PREFIX_SIZE = 27
PREFIX_COUNT = PREFIX_SIZE * PREFIX_SIZE

ADDITIVE_COUNTER_KEYS = (
    "raw_skeletons_seen",
    "raw_decorations_seen",
    "canonical_decorations_seen",
    "canonical_decorations_processed",
    "weighted_decorations_processed",
    "high_phase_cases",
    "rejected_local_phase_cases",
    "primitive_flag_phase_leaves",
    "weighted_primitive_flag_phase_leaves",
    "affine_aggregate_hits",
    "weighted_affine_aggregate_hits",
    "exact_target_hits",
    "char2_hits",
    "mod9_hits",
    "char2_mod9_hits",
    "post_mod9_lambda_hits",
    "char2_post_mod9_lambda_hits",
    "mod27_hits",
    "exact_zero_hits",
    "detached_replays",
    "weighted_exact_target_hits",
    "weighted_char2_hits",
    "weighted_mod9_hits",
    "weighted_post_mod9_lambda_hits",
    "weighted_exact_zero_hits",
)

DIAGNOSTIC_COUNTER_KEYS = (
    "diagnostic_assignment_idlex_mod9_hits",
    "diagnostic_weighted_assignment_idlex_mod9_hits",
)

WITNESS_NAMES = (
    "witness_char2_mod9",
    "witness_post_mod9_lambda",
    "witness_exact",
)

TARGETS = (
    (-3, -3, -4, -2), (-3, -3, -2, 2), (-3, 0, -3, -3),
    (-3, 0, 0, 3), (-1, -2, -5, -1), (-1, -2, -4, 1),
    (0, 3, -4, -2), (0, 3, -2, 2), (1, -1, 2, -2),
    (1, -1, 4, 2), (1, 2, -5, -1), (1, 2, -4, 1),
    (2, -2, -4, -2), (2, -2, -2, 2), (2, 1, 2, -2),
    (2, 1, 4, 2), (3, 0, 0, -3), (3, 0, 3, 3),
    (4, -1, 0, 0), (4, 2, -4, -2), (4, 2, -2, 2),
    (5, 1, 0, 0),
)

BURNSIDE = {
    "h1": {
        "medium_total": 15,
        "raw_skeletons": 59_743_488,
        "raw_decorations": 537_691_392,
        "canonical_decorations": 22_426_752,
        "fixed_decorations": (
            537_691_392, 275_328, 275_328, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        ),
    },
    "h0": {
        "medium_total": 18,
        "raw_skeletons": 47_730_304,
        "raw_decorations": 47_730_304,
        "canonical_decorations": 1_999_128,
        "fixed_decorations": (
            47_730_304, 67_776, 67_776, 0, 32, 0, 0, 0,
            208, 24, 24, 0, 112_640, 0, 0, 0,
            208, 24, 24, 0, 32, 0, 0, 0,
        ),
    },
}

EXPECTED_WORKLOAD = {
    "h1": {
        "one_rhs_affine_upper": 15_012_043_331_328,
        "residue_union_affine_upper": 30_006_842_465_088,
        "primitive_leaf_upper": 45_036_129_993_984,
    },
    "h0": {
        "one_rhs_affine_upper": 8_914_445_186_688,
        "residue_union_affine_upper": 17_848_209_316_608,
        "primitive_leaf_upper": 26_743_335_560_064,
    },
}


def legal_local_states() -> tuple[tuple[int, int, int, int], ...]:
    """Return the C++ lexicographic 27-state local alphabet."""
    result = []
    for a0 in range(-1, 2):
        for a1 in range(-1, 2):
            for b0 in range(-1, 2):
                for b1 in range(-1, 2):
                    if (-a0 + a1 + b0 - b1) % 3 == 0:
                        result.append((a0, a1, b0, b1))
    if len(result) != PREFIX_SIZE:
        raise AssertionError("legal local-state count changed")
    return tuple(result)


LOCAL_STATES = legal_local_states()
LOCAL_WEIGHTS = tuple(
    sum(value != 0 for value in state) for state in LOCAL_STATES
)


def shard_id(shell: str, first: int, second: int) -> str:
    if shell not in SHELLS:
        raise ValueError(f"unknown shell {shell!r}")
    if not (0 <= first < PREFIX_SIZE and 0 <= second < PREFIX_SIZE):
        raise ValueError("prefix indices must lie in [0,26]")
    return f"{shell}-p{first:02d}-p{second:02d}"


def parse_key_value_output(output: str) -> dict[str, str]:
    """Parse the machine-readable portion of classifier stdout."""
    parsed: dict[str, str] = {}
    for line in output.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if not key or key in parsed:
            raise ValueError(f"duplicate/empty output key {key!r}")
        parsed[key] = value
    return parsed


def require_nonnegative_integer(
    parsed: dict[str, str], key: str
) -> int:
    try:
        text = parsed[key]
    except KeyError as error:
        raise ValueError(f"missing output key {key}") from error
    if not text.isdigit():
        raise ValueError(f"{key} is not a nonnegative integer: {text!r}")
    return int(text)


def _remaining_weight_counts(length: int) -> tuple[int, ...]:
    counts = [0] * (4 * length + 1)
    counts[0] = 1
    for _ in range(length):
        following = [0] * len(counts)
        for used, ways in enumerate(counts):
            if not ways:
                continue
            for weight in LOCAL_WEIGHTS:
                following[used + weight] += ways
        counts = following
    return tuple(counts)


REMAINING_FOUR = _remaining_weight_counts(4)


@dataclass(frozen=True)
class PrefixCell:
    shell: str
    first: int
    second: int
    first_weight: int
    second_weight: int
    raw_skeletons: int
    raw_decorations: int

    @property
    def identifier(self) -> str:
        return shard_id(self.shell, self.first, self.second)

    def as_dict(self) -> dict[str, int | str]:
        return {
            "shard_id": self.identifier,
            "shell": self.shell,
            "prefix_first": self.first,
            "prefix_second": self.second,
            "prefix_first_weight": self.first_weight,
            "prefix_second_weight": self.second_weight,
            "raw_skeletons": self.raw_skeletons,
            "raw_decorations": self.raw_decorations,
        }


def prefix_cells(shell: str) -> tuple[PrefixCell, ...]:
    target = int(BURNSIDE[shell]["medium_total"])
    high_positions = 9 if shell == "h1" else 1
    result = []
    for first, first_weight in enumerate(LOCAL_WEIGHTS):
        for second, second_weight in enumerate(LOCAL_WEIGHTS):
            residual = target - first_weight - second_weight
            skeletons = (
                REMAINING_FOUR[residual]
                if 0 <= residual < len(REMAINING_FOUR)
                else 0
            )
            result.append(
                PrefixCell(
                    shell=shell,
                    first=first,
                    second=second,
                    first_weight=first_weight,
                    second_weight=second_weight,
                    raw_skeletons=skeletons,
                    raw_decorations=skeletons * high_positions,
                )
            )
    if len(result) != PREFIX_COUNT:
        raise AssertionError("prefix partition size changed")
    return tuple(result)


def validate_burnside(shell: str) -> None:
    expected = BURNSIDE[shell]
    fixed = tuple(int(value) for value in expected["fixed_decorations"])
    if len(fixed) != 24:
        raise AssertionError(f"{shell}: Burnside vector length changed")
    if sum(fixed) % 24:
        raise AssertionError(f"{shell}: nonintegral Burnside sum")
    if sum(fixed) // 24 != expected["canonical_decorations"]:
        raise AssertionError(f"{shell}: Burnside canonical total changed")
    if fixed[0] != expected["raw_decorations"]:
        raise AssertionError(f"{shell}: Burnside identity count changed")


def partition_audit(shells: Iterable[str] = SHELLS) -> dict[str, object]:
    shell_rows: dict[str, object] = {}
    for shell in shells:
        validate_burnside(shell)
        cells = prefix_cells(shell)
        expected = BURNSIDE[shell]
        raw_skeletons = sum(cell.raw_skeletons for cell in cells)
        raw_decorations = sum(cell.raw_decorations for cell in cells)
        if raw_skeletons != expected["raw_skeletons"]:
            raise AssertionError(f"{shell}: prefix skeleton union changed")
        if raw_decorations != expected["raw_decorations"]:
            raise AssertionError(f"{shell}: prefix decoration union changed")
        shell_rows[shell] = {
            "prefix_count": len(cells),
            "raw_skeletons": raw_skeletons,
            "raw_decorations": raw_decorations,
            "canonical_decorations": expected["canonical_decorations"],
            "fixed_decorations": list(expected["fixed_decorations"]),
            "cells": [cell.as_dict() for cell in cells],
        }
    return {"schema": PARTITION_SCHEMA, "shells": shell_rows}


def _rho(a: int, b: int) -> tuple[int, int, int]:
    return a % 3, b % 3, (2 * a - b) % 9


def target_residue_multiplicities() -> dict[tuple[int, int], int]:
    """Number of distinct lambda^3 target RHS pairs for each scalar type."""
    residues: dict[
        tuple[int, int],
        set[tuple[tuple[int, int, int], tuple[int, int, int]]],
    ] = defaultdict(set)
    for a0, a1, b0, b1 in TARGETS:
        residues[(a0 % 3, b0 % 3)].add(
            (_rho(a0, a1), _rho(b0, b1))
        )
    result = {key: len(values) for key, values in residues.items()}
    expected = {
        (0, 0): 2,
        (0, 1): 1,
        (0, 2): 1,
        (1, 0): 1,
        (2, 0): 1,
        (1, 1): 3,
        (1, 2): 3,
        (2, 1): 3,
        (2, 2): 3,
    }
    if result != expected:
        raise AssertionError("target residue multiplicities changed")
    return result


def workload_audit() -> dict[str, object]:
    """Reproduce the one-RHS, union-RHS, and primitive phase bounds.

    The state is ``(n,r,alpha,beta)`` after each quartet.  ``n`` is the
    number of medium entries, ``r`` the number of nonempty quartets, and the
    final two coordinates identify the channel aggregate scalar type.
    """
    states: dict[tuple[int, int, int, int], int] = {(0, 0, 0, 0): 1}
    for quartet in range(6):
        epsilon = 1 if quartet % 2 == 0 else -1
        following: dict[tuple[int, int, int, int], int] = defaultdict(int)
        for (n, r, alpha, beta), count in states.items():
            for a0, a1, b0, b1 in LOCAL_STATES:
                medium = sum(
                    value != 0 for value in (a0, a1, b0, b1)
                )
                key = (
                    n + medium,
                    r + (medium > 0),
                    (alpha - epsilon * (a0 + a1)) % 3,
                    (beta + epsilon * (b0 + b1)) % 3,
                )
                following[key] += count
        states = dict(following)

    multiplicity = target_residue_multiplicities()
    rows: dict[str, object] = {}
    for shell in SHELLS:
        n_target = int(BURNSIDE[shell]["medium_total"])
        high_factor = 27 if shell == "h1" else 1
        one_rhs_before_high = 0
        union_before_high = 0
        primitive_before_high = 0
        collapsed: dict[tuple[int, int], int] = defaultdict(int)
        for (n, r, alpha, beta), count in states.items():
            if n != n_target:
                continue
            dimension = n - (r + 1)
            if dimension < 0:
                raise AssertionError("negative affine dimension")
            k = multiplicity[(alpha, beta)]
            collapsed[(r, k)] += count
            one_rhs_before_high += count * 3 ** dimension
            union_before_high += count * k * 3 ** dimension
            primitive_before_high += count * 3 ** (n - r)

        row = {
            "before_high": {
                "one_rhs_affine_upper": one_rhs_before_high,
                "residue_union_affine_upper": union_before_high,
                "primitive_leaf_upper": primitive_before_high,
            },
            "orientation_factor": high_factor,
            "one_rhs_affine_upper": one_rhs_before_high * high_factor,
            "residue_union_affine_upper": union_before_high * high_factor,
            "primitive_leaf_upper": primitive_before_high * high_factor,
            "collapsed_signed_skeletons_by_r_and_target_multiplicity": {
                f"r{r}_k{k}": value
                for (r, k), value in sorted(collapsed.items())
            },
        }
        for key, expected in EXPECTED_WORKLOAD[shell].items():
            if row[key] != expected:
                raise AssertionError(
                    f"{shell}: {key} changed: {row[key]} != {expected}"
                )
        rows[shell] = row

    return {
        "schema": "dense-shell-residue-workload-audit-v1",
        "target_residue_multiplicities": {
            f"{alpha},{beta}": value
            for (alpha, beta), value in sorted(multiplicity.items())
        },
        "shells": rows,
        "combined_residue_union_affine_upper": sum(
            int(rows[shell]["residue_union_affine_upper"])
            for shell in SHELLS
        ),
        "combined_primitive_leaf_upper": sum(
            int(rows[shell]["primitive_leaf_upper"])
            for shell in SHELLS
        ),
    }


if __name__ == "__main__":
    import json

    print(
        json.dumps(
            {
                "partition": partition_audit(),
                "workload": workload_audit(),
            },
            indent=2,
            sort_keys=True,
        )
    )

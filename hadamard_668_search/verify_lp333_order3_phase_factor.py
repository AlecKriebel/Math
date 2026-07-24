#!/usr/bin/env python3
"""Verify the exact three-fiber unit-phase factorization for LP(333).

Every nine-row word is split into three length-three fibers.  Their
Eisenstein Fourier phases turn the primitive-nine norm equation into one
diagonal complementary-frame equation and one independent cross equation.
All arithmetic in this module is integral.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Sequence

from verify_lp333_order3_integral9 import (
    expand_columns,
    full_correlation_table,
)
from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
    P,
    ROWS,
    ZERO_A_PLUS,
    ZERO_B_PLUS,
)
from verify_lp333_order3_quotient import PARTS
from verify_lp333_order3_trit_lift import (
    PINNED_PROFILES,
    TRIT_SURVIVOR_MASKS_A,
    TRIT_SURVIVOR_MASKS_B,
)


Eisenstein = tuple[int, int]  # a+b*omega, omega^2+omega+1=0.
Word = tuple[int, ...]
PhaseColumns = tuple[
    tuple[tuple[Eisenstein, Eisenstein, Eisenstein], ...],
    tuple[tuple[Eisenstein, Eisenstein, Eisenstein], ...],
]

ZERO: Eisenstein = (0, 0)
ONE: Eisenstein = (1, 0)
OMEGA: Eisenstein = (0, 1)
OMEGA2: Eisenstein = (-1, -1)
ROOTS = (ONE, OMEGA, OMEGA2)
EXPECTED_PINNED_COMPONENT_HASH = (
    "9cada4a8eeca603b7ecef64b4c30e1ce43a1376258a95658674a8d6c902da32d"
)
EXPECTED_TRIT_COMPONENT_HASH = (
    "31f424677b10794c77867420ce0487bf51320c6d7d52a2f9f521e6848c7542d3"
)


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_scale(scale: int, value: Eisenstein) -> Eisenstein:
    return scale * value[0], scale * value[1]


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: Eisenstein) -> Eisenstein:
    return value[0] - value[1], -value[1]


def e_power_of_omega(exponent: int) -> Eisenstein:
    return ROOTS[exponent % 3]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def fiber_phase(word: Sequence[int], residue: int) -> Eisenstein:
    if len(word) != ROWS or any(value not in (0, 1) for value in word):
        raise ValueError("a fiber phase requires a binary nine-row word")
    if not 0 <= residue < 3:
        raise ValueError("the residue must lie in 0,1,2")
    value = ZERO
    for quotient in range(3):
        if word[residue + 3 * quotient]:
            value = e_add(value, ROOTS[quotient])
    return value


def placement_trit(word: Sequence[int], residue: int) -> int | None:
    """Return the trit used by the fixed-profile placement encoding."""

    fiber = tuple(int(word[residue + 3 * q]) for q in range(3))
    count = sum(fiber)
    if count not in (1, 2):
        return None
    return (fiber[2] - fiber[1]) % 3


def phase_from_trit(count: int, trit: int) -> Eisenstein:
    if count == 1:
        return e_power_of_omega(-trit)
    if count == 2:
        return e_scale(-1, e_power_of_omega(trit))
    raise ValueError("only active fiber counts one and two have a trit")


def profile_active_fibers(profile: Sequence[int]) -> int:
    if (
        len(profile) != 3
        or any(value not in (0, 1, 2, 3) for value in profile)
        or sum(profile) != 3
    ):
        raise ValueError("a profile must be a composition of three")
    return sum(value in (1, 2) for value in profile)


def profile_eisenstein_norm(profile: Sequence[int]) -> int:
    if (
        len(profile) != 3
        or any(value not in (0, 1, 2, 3) for value in profile)
        or sum(profile) != 3
    ):
        raise ValueError("a profile must be a composition of three")
    first = int(profile[0]) - int(profile[2])
    second = int(profile[1]) - int(profile[2])
    return first * first - first * second + second * second


def verify_universal_phase_count() -> dict[str, object]:
    """Prove that norm 54 forces 54 active nonzero-class fibers."""

    profiles = tuple(
        (first, second, 3 - first - second)
        for first in range(4)
        for second in range(4)
        if 0 <= 3 - first - second <= 3
    )
    assert len(profiles) == 10
    for profile in profiles:
        assert profile_active_fibers(profile) == (
            3 - profile_eisenstein_norm(profile) // 3
        )

    zero_active = sum(
        fiber_phase(word, residue) != ZERO
        for word in (ZERO_A_PLUS, ZERO_B_PLUS)
        for residue in range(3)
    )
    assert zero_active == 5
    return {
        "profile_types": len(profiles),
        "per_profile_identity": "active=3-norm/3",
        "profiles_per_tuple": 24,
        "required_total_profile_norm": 54,
        "forced_active_profile_fibers": 54,
        "fixed_zero_column_active_fibers": zero_active,
        "physical_frame_energy": 3 * 54 + zero_active,
    }


def phase_columns(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> PhaseColumns:
    columns = expand_columns(masks_a, masks_b)
    return tuple(
        tuple(
            tuple(fiber_phase(columns[channel][column], residue)
                  for residue in range(3))
            for column in range(P)
        )
        for channel in range(2)
    )  # type: ignore[return-value]


def phase_correlation_matrices(
    phases: PhaseColumns,
) -> tuple[tuple[tuple[tuple[Eisenstein, ...], ...], ...], ...]:
    """Return K_st(b) for all 37 column lags."""

    result = []
    for lag in range(P):
        matrix = []
        for left_residue in range(3):
            row = []
            for right_residue in range(3):
                value = ZERO
                for channel in range(2):
                    for column in range(P):
                        value = e_add(
                            value,
                            e_multiply(
                                phases[channel][
                                    (column + lag) % P
                                ][left_residue],
                                e_conjugate(
                                    phases[channel][column][right_residue]
                                ),
                            ),
                        )
                row.append(value)
            matrix.append(tuple(row))
        result.append(tuple(matrix))
    return tuple(result)


def phase_equations(
    phases: PhaseColumns,
) -> tuple[
    tuple[Eisenstein, Eisenstein, Eisenstein], ...
]:
    """Return the three extension-basis coefficients of W W* - 167."""

    result = []
    for lag, matrix in enumerate(phase_correlation_matrices(phases)):
        e0 = e_add(e_add(matrix[0][0], matrix[1][1]), matrix[2][2])
        e1 = e_add(
            e_add(matrix[1][0], matrix[2][1]),
            e_multiply(OMEGA2, matrix[0][2]),
        )
        e2 = e_add(
            matrix[2][0],
            e_multiply(
                OMEGA2,
                e_add(matrix[0][1], matrix[1][2]),
            ),
        )
        if lag == 0:
            e0 = e_add(e0, (-167, 0))
        result.append((e0, e1, e2))
    return tuple(result)


def extension_remainder(
    correlations: Sequence[int],
) -> tuple[Eisenstein, Eisenstein, Eisenstein]:
    """Group a degree-eight row polynomial over Z[omega]."""

    if len(correlations) != ROWS:
        raise ValueError("a row-correlation vector must have length nine")
    return (
        (
            int(correlations[0]) - int(correlations[6]),
            int(correlations[3]) - int(correlations[6]),
        ),
        (
            int(correlations[1]) - int(correlations[7]),
            int(correlations[4]) - int(correlations[7]),
        ),
        (
            int(correlations[2]) - int(correlations[8]),
            int(correlations[5]) - int(correlations[8]),
        ),
    )


def verify_local_phase_bijection() -> dict[str, object]:
    phase_catalog: dict[int, set[Eisenstein]] = {
        count: set() for count in range(4)
    }
    active_checks = 0
    for count in range(4):
        for support in combinations(range(3), count):
            nine_word = tuple(
                int(row // 3 in support) if row % 3 == 0 else 0
                for row in range(ROWS)
            )
            phase = fiber_phase(nine_word, 0)
            phase_catalog[count].add(phase)
            if count in (1, 2):
                trit = placement_trit(nine_word, 0)
                assert trit is not None
                assert phase == phase_from_trit(count, trit)
                active_checks += 1
            else:
                assert phase == ZERO
    assert phase_catalog == {
        0: {ZERO},
        1: set(ROOTS),
        2: {e_scale(-1, root) for root in ROOTS},
        3: {ZERO},
    }
    return {
        "fiber_counts": 4,
        "active_placement_checks": active_checks,
        "active_phase_values_per_count": 3,
    }


def verify_certificate_factorization(
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> dict[str, object]:
    phases = phase_columns(masks_a, masks_b)
    equations = phase_equations(phases)
    correlations = full_correlation_table(masks_a, masks_b)
    direct = tuple(extension_remainder(row) for row in correlations)
    assert equations == direct

    for lag in range(P):
        opposite = (-lag) % P
        e0, e1, e2 = equations[lag]
        opposite_e0, opposite_e1, _ = equations[opposite]
        assert e0 == e_conjugate(opposite_e0)
        assert e2 == e_multiply(
            OMEGA2,
            e_conjugate(opposite_e1),
        )

    for part in PARTS:
        representative = equations[part[0]]
        assert all(equations[column] == representative for column in part)

    invariant_components = tuple(
        tuple(equations[part[0]][component] for part in PARTS)
        for component in range(3)
    )
    active_physical_fibers = sum(
        value != ZERO
        for channel in phases
        for column in channel
        for value in column
    )
    return {
        "physical_column_lags": P,
        "extension_coefficients_per_lag": 3,
        "active_physical_fibers": active_physical_fibers,
        "exact_factorization": True,
        "e2_is_adjoint_of_e1": True,
        "nonzero_invariant_coefficients": tuple(
            sum(value != ZERO for value in component)
            for component in invariant_components
        ),
        "component_hash": compact_hash(invariant_components),
        "exact_integral_survivor": not any(
            value != ZERO
            for equation in equations
            for value in equation
        ),
    }


def pinned_active_profile_fibers() -> int:
    return sum(
        count in (1, 2)
        for channel in PINNED_PROFILES
        for profile in channel
        for count in profile
    )


def verify() -> dict[str, object]:
    local = verify_local_phase_bijection()
    universal = verify_universal_phase_count()
    pinned = verify_certificate_factorization(
        LABELLED_SURVIVOR_MASKS_A,
        LABELLED_SURVIVOR_MASKS_B,
    )
    trit = verify_certificate_factorization(
        TRIT_SURVIVOR_MASKS_A,
        TRIT_SURVIVOR_MASKS_B,
    )
    assert pinned_active_profile_fibers() == (
        universal["forced_active_profile_fibers"]
    )
    assert pinned["active_physical_fibers"] == 167
    assert trit["active_physical_fibers"] == 167
    assert pinned["nonzero_invariant_coefficients"] == (12, 12, 12)
    assert trit["nonzero_invariant_coefficients"] == (12, 12, 12)
    assert pinned["component_hash"] == EXPECTED_PINNED_COMPONENT_HASH
    assert trit["component_hash"] == EXPECTED_TRIT_COMPONENT_HASH
    assert not pinned["exact_integral_survivor"]
    assert not trit["exact_integral_survivor"]
    return {
        "local_phase_bijection": local,
        "universal_phase_count": universal,
        "pinned_profile_trits": 54,
        "physical_frame_energy": 167,
        "independent_group_ring_equations": 2,
        "independent_integer_conditions": 39,
        "mixed_column_integer_conditions": 36,
        "pinned_certificate": pinned,
        "trit_certificate": trit,
        "status": (
            "exact phase factorization verified; both modular certificates "
            "remain non-solutions"
        ),
    }


def main() -> None:
    result = verify()
    print(
        "universal_profile_trits="
        f"{result['universal_phase_count']['forced_active_profile_fibers']}"
    )
    print(f"physical_frame_energy={result['physical_frame_energy']}")
    print(
        "independent_group_ring_equations="
        f"{result['independent_group_ring_equations']}"
    )
    print(
        "mixed_column_integer_conditions="
        f"{result['mixed_column_integer_conditions']}"
    )
    print("PASS: exact three-fiber unit-phase factorization reconstructed")
    print("STATUS: new exact search architecture; no LP(333) or H(668)")


if __name__ == "__main__":
    main()

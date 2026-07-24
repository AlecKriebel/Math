#!/usr/bin/env python3
"""Verify the adjacent-42 reduction for repairing Eliahou's H(668) seed.

This checker is dependency-free and uses exact integer arithmetic.  It
proves a distance bound, a cyclic group-ring reduction of the minimum base
shell, and a complete low-weight reciprocal-skeleton/Fourier classification.

It does not find a base sequence or a Hadamard matrix.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from math import comb
from random import Random
from typing import Iterable, Sequence


LONG = 84
SHORT = 83
FOLD = 42

ELIAHOU_Q_RUNS = (83, 2, 81, 1)
ELIAHOU_S_RUNS = (
    (4,) * 5
    + (2, 1, 1) * 5
    + (1, 5)
    + (4,) * 4
    + (2, 1, 1) * 6
    + (4,) * 4
    + (3,)
    + (1, 2, 1) * 5
    + (3,)
    + (4,) * 4
    + (3,)
    + (1, 2, 1) * 5
)

EXPECTED_BASE_RESIDUALS = {
    4: -256,
    8: 192,
    12: -128,
    16: 64,
    26: -32,
    30: 64,
    34: -96,
    38: 128,
    42: -160,
    46: 128,
    50: -96,
    54: 64,
    58: -32,
}

EXPECTED_TRANSFER_COEFFICIENT_80 = (
    16734850903642159814868855513591696065526686023680
)

Polynomial = tuple[int, ...]
Quadruple = tuple[Polynomial, Polynomial, Polynomial, Polynomial]
LocalState = tuple[int, int, int]


def decode_runs(runs: Iterable[int]) -> tuple[int, ...]:
    result: list[int] = []
    sign = 1
    for run in runs:
        result.extend((sign,) * run)
        sign = -sign
    return tuple(result)


def eliahou_base() -> Quadruple:
    s_value = decode_runs(ELIAHOU_S_RUNS)
    q_value = decode_runs(ELIAHOU_Q_RUNS)
    if len(s_value) != 167 or len(q_value) != 167:
        raise AssertionError("seed run data has the wrong length")
    product_value = tuple(
        left * right for left, right in zip(s_value, q_value)
    )
    return (
        s_value[:LONG],
        product_value[:LONG],
        s_value[LONG:],
        product_value[LONG:],
    )


def aperiodic_correlation(sequence: Sequence[int], lag: int) -> int:
    return sum(
        sequence[index] * sequence[index + lag]
        for index in range(len(sequence) - lag)
    )


def base_correlations(sequences: Quadruple) -> tuple[int, ...]:
    return tuple(
        sum(
            aperiodic_correlation(sequence, lag)
            for sequence in sequences
            if lag < len(sequence)
        )
        for lag in range(LONG)
    )


def fold42(sequence: Sequence[int]) -> Polynomial:
    """Compress a length-84/83 row modulo 42."""

    if len(sequence) not in (LONG, SHORT):
        raise ValueError("the adjacent-42 fold expects length 84 or 83")
    return tuple(
        sequence[index]
        + (sequence[index + FOLD] if index + FOLD < len(sequence) else 0)
        for index in range(FOLD)
    )


def fold_quadruple(sequences: Quadruple) -> Quadruple:
    return tuple(fold42(sequence) for sequence in sequences)  # type: ignore[return-value]


def periodic_correlation(sequence: Sequence[int], lag: int) -> int:
    length = len(sequence)
    return sum(
        sequence[index] * sequence[(index + lag) % length]
        for index in range(length)
    )


def summed_periodic_correlations(sequences: Quadruple) -> tuple[int, ...]:
    return tuple(
        sum(periodic_correlation(sequence, lag) for sequence in sequences)
        for lag in range(FOLD)
    )


def fold_correlations_from_aperiodic(
    correlations: Sequence[int],
) -> tuple[int, ...]:
    """Recover the 42-fold cyclic PAF from aperiodic norm coefficients."""

    if len(correlations) != LONG:
        raise ValueError("expected correlations at lags 0 through 83")
    result = [correlations[0] + 2 * correlations[42]]
    for lag in range(1, 21):
        result.append(
            correlations[lag]
            + correlations[42 - lag]
            + correlations[42 + lag]
            + correlations[84 - lag]
        )
    result.append(2 * (correlations[21] + correlations[63]))
    result.extend(reversed(result[1:21]))
    return tuple(result)


def expected_seed_fold() -> Quadruple:
    a_value = [0] * FOLD
    b_value = [0] * FOLD
    c_value = [0] * FOLD
    d_value = [0] * FOLD
    a_value[41] = -2
    c_value[0] = 2
    c_value[41] = 1
    d_value[40] = -2
    d_value[41] = 1
    return (
        tuple(a_value),
        tuple(b_value),
        tuple(c_value),
        tuple(d_value),
    )


def equal_separation_pairs(sequences: Quadruple) -> int:
    return sum(
        sequence[index] == sequence[index + FOLD]
        for sequence in sequences
        for index in range(len(sequence) - FOLD)
    )


def hamming_distance(
    left: Sequence[Sequence[int]], right: Sequence[Sequence[int]]
) -> int:
    return sum(
        left_value != right_value
        for left_row, right_row in zip(left, right)
        for left_value, right_value in zip(left_row, right_row)
    )


def cross_correlations(
    left: Quadruple, right: Quadruple
) -> tuple[int, ...]:
    return tuple(
        sum(
            sum(
                left_row[index] * right_row[(index + lag) % FOLD]
                + right_row[index] * left_row[(index + lag) % FOLD]
                for index in range(FOLD)
            )
            for left_row, right_row in zip(left, right)
        )
        for lag in range(FOLD)
    )


def add_scaled(
    left: Quadruple, scale: int, right: Quadruple
) -> Quadruple:
    return tuple(
        tuple(
            left_value + scale * right_value
            for left_value, right_value in zip(left_row, right_row)
        )
        for left_row, right_row in zip(left, right)
    )  # type: ignore[return-value]


def shell_equation(g_value: Quadruple) -> tuple[int, ...]:
    """Return cross(F0,G)+2*N(G), targeted to (160,0,...,0)."""

    seed_fold = expected_seed_fold()
    cross = cross_correlations(seed_fold, g_value)
    norm = summed_periodic_correlations(g_value)
    return tuple(
        cross_value + 2 * norm_value
        for cross_value, norm_value in zip(cross, norm)
    )


def multiply_polynomials(
    left: dict[int, int], right: dict[int, int]
) -> dict[int, int]:
    result: dict[int, int] = {}
    for left_degree, left_value in left.items():
        for right_degree, right_value in right.items():
            degree = left_degree + right_degree
            result[degree] = (
                result.get(degree, 0) + left_value * right_value
            )
    return result


def polynomial_power(base: dict[int, int], exponent: int) -> dict[int, int]:
    result = {0: 1}
    for _ in range(exponent):
        result = multiply_polynomials(result, base)
    return result


HALF_PAIR_STATES: tuple[LocalState, ...] = (
    (0, 0, 0),  # unchanged
    (1, 0, 1),  # flip the lower endpoint
    (0, 1, 1),  # flip the upper endpoint
)


def local_component_polynomial(
    allowed: tuple[bool, bool, bool, bool],
) -> dict[int, int]:
    """Enumerate one reflected pair of two-row half-pair components.

    Variables are row A/B (or C/D) at half-pair indices j and sigma(j).
    The reciprocal q skeleton equates lower parity on one side with upper
    parity on the reflected side, and conversely.
    """

    state_lists = tuple(
        HALF_PAIR_STATES if is_allowed else (HALF_PAIR_STATES[0],)
        for is_allowed in allowed
    )
    result: dict[int, int] = {}
    for first_j, first_reflected, second_j, second_reflected in product(
        *state_lists
    ):
        if (
            first_j[0] ^ second_j[0]
            != first_reflected[1] ^ second_reflected[1]
        ):
            continue
        if (
            first_j[1] ^ second_j[1]
            != first_reflected[0] ^ second_reflected[0]
        ):
            continue

        # This is also the short-fold boundary reciprocity condition:
        # selected_C(j)+selected_D(j) is reflection invariant.
        assert (
            first_j[2] ^ second_j[2]
            == first_reflected[2] ^ second_reflected[2]
        )
        weight = (
            first_j[2]
            + first_reflected[2]
            + second_j[2]
            + second_reflected[2]
        )
        result[weight] = result.get(weight, 0) + 1
    return result


def center_component_polynomial() -> dict[int, int]:
    result: dict[int, int] = {}
    for first, second in product(HALF_PAIR_STATES, repeat=2):
        if first[0] ^ second[0] != first[1] ^ second[1]:
            continue
        weight = first[2] + second[2]
        result[weight] = result.get(weight, 0) + 1
    return result


def transfer_polynomial() -> dict[int, int]:
    generic = local_component_polynomial((True, True, True, True))
    long_exception = local_component_polynomial((True, False, True, True))
    short_exception = local_component_polynomial((False, True, True, False))
    center = center_component_polynomial()
    result = polynomial_power(generic, 39)
    for factor in (long_exception, short_exception, center):
        result = multiply_polynomials(result, factor)
    return result


def special_change_case_split(total_distance: int) -> tuple[
    tuple[int, int, int], ...
]:
    """Return (s-only,q-only,both) counts compatible with base distance >=80."""

    result = []
    for s_only in range(total_distance + 1):
        for q_only in range(total_distance + 1):
            for both in range(total_distance // 2 + 1):
                if s_only + q_only + 2 * both != total_distance:
                    continue
                base_distance = 2 * s_only + q_only + both
                if base_distance >= 80:
                    result.append((s_only, q_only, both))
    return tuple(result)


def reciprocal_q_masks_of_weight_at_most_two() -> dict[int, tuple[tuple[int, ...], ...]]:
    """Homogeneous differences of two reciprocal q-skeleton words."""

    weight_one = ((LONG + 41,),)
    weight_two = []
    weight_two.extend((index, 83 - index) for index in range(42))
    weight_two.extend(
        (LONG + index, LONG + 82 - index) for index in range(41)
    )
    return {0: ((),), 1: weight_one, 2: tuple(weight_two)}


def q_pair_fold_signature(
    sequence: Sequence[int], first_index: int
) -> tuple[int, int] | None:
    """Return H(1),H(-1) for one reciprocal q-pair on the base shell."""

    reflected = len(sequence) - 1 - first_index
    coordinates = (first_index, reflected)
    pair_indices = tuple(index % FOLD for index in coordinates)
    if pair_indices[0] == pair_indices[1]:
        return None

    for index in coordinates:
        mate = index + FOLD if index < FOLD else index - FOLD
        if mate >= len(sequence) or sequence[index] == sequence[mate]:
            return None

    folded_delta = [0] * FOLD
    for index in coordinates:
        folded_delta[index % FOLD] += -sequence[index]
    ordinary = sum(folded_delta)
    alternating = sum(
        value if index % 2 == 0 else -value
        for index, value in enumerate(folded_delta)
    )
    return ordinary, alternating


def q_pair_signature_catalogs() -> tuple[
    dict[tuple[int, int], tuple[int, ...]],
    dict[tuple[int, int], tuple[int, ...]],
]:
    _, b_value, _, d_value = eliahou_base()
    long_catalog: dict[tuple[int, int], list[int]] = {}
    short_catalog: dict[tuple[int, int], list[int]] = {}
    for index in range(42):
        signature = q_pair_fold_signature(b_value, index)
        if signature is not None:
            long_catalog.setdefault(signature, []).append(index)
    for index in range(41):
        signature = q_pair_fold_signature(d_value, index)
        if signature is not None:
            short_catalog.setdefault(signature, []).append(index)
    return (
        {key: tuple(value) for key, value in long_catalog.items()},
        {key: tuple(value) for key, value in short_catalog.items()},
    )


def long_root_energy(
    root: int, l_value: int, h_value: int, s_value: int
) -> int:
    if root == 1:
        return (
            (-2 + 2 * l_value) ** 2
            + (2 * (l_value + h_value)) ** 2
            + (3 + 2 * s_value) ** 2
            + (-1 + 2 * s_value) ** 2
        )
    if root == -1:
        return (
            (2 + 2 * l_value) ** 2
            + (2 * (l_value + h_value)) ** 2
            + (1 + 2 * s_value) ** 2
            + (-3 + 2 * s_value) ** 2
        )
    raise ValueError("root must be +1 or -1")


def short_root_energy(
    root: int, l_value: int, h_value: int, s_value: int
) -> int:
    if root == 1:
        return (
            (-2 + 2 * l_value) ** 2
            + (2 * l_value) ** 2
            + (3 + 2 * s_value) ** 2
            + (-1 + 2 * s_value + 2 * h_value) ** 2
        )
    if root == -1:
        return (
            (2 + 2 * l_value) ** 2
            + (2 * l_value) ** 2
            + (1 + 2 * s_value) ** 2
            + (-3 + 2 * s_value + 2 * h_value) ** 2
        )
    raise ValueError("root must be +1 or -1")


def joined_root_profiles(
    ordinary_h: int, alternating_h: int, q_pair_in_long_block: bool
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    """Join exact root +1/-1 row-sum profiles for 39 common s flips."""

    energy_function = (
        long_root_energy if q_pair_in_long_block else short_root_energy
    )
    root_profiles: dict[int, list[tuple[int, int]]] = {1: [], -1: []}
    for root, h_value in ((1, ordinary_h), (-1, alternating_h)):
        for l_value in range(-20, 21):
            for s_value in range(-20, 21):
                # L and S together have odd support 39.
                if (l_value + s_value) % 2 != 1:
                    continue
                if energy_function(root, l_value, h_value, s_value) == 334:
                    root_profiles[root].append((l_value, s_value))

    result = []
    for ordinary in root_profiles[1]:
        for alternating in root_profiles[-1]:
            # For one signed support, evaluation at +1 and -1 has the same
            # parity.  Apply this independently to L and S.
            if (
                (ordinary[0] - alternating[0]) % 2 == 0
                and (ordinary[1] - alternating[1]) % 2 == 0
            ):
                result.append((ordinary, alternating))
    return tuple(sorted(result))


def verify_center_q_flip_obstruction() -> None:
    """Exclude the unique weight-one q-skeleton change at distance 41."""

    solutions = [
        (l_value, s_value)
        for l_value in range(-20, 21)
        for s_value in range(-20, 21)
        if l_value * (l_value + 1) + s_value * s_value == 41
    ]
    assert not solutions
    # Equivalently (2l+1)^2 + (2s)^2 = 165, impossible because 3 and 11
    # occur to odd exponent in 165.


def verify() -> dict[str, object]:
    base = eliahou_base()
    correlations = base_correlations(base)
    residuals = {
        lag: value
        for lag, value in enumerate(correlations)
        if lag and value
    }
    assert correlations[0] == 334
    assert residuals == EXPECTED_BASE_RESIDUALS

    folded = fold_quadruple(base)
    assert folded == expected_seed_fold()
    folded_correlations = summed_periodic_correlations(folded)
    assert folded_correlations == (14,) + (0,) * 41
    assert fold_correlations_from_aperiodic(correlations) == folded_correlations

    # The thirteen residuals collapse to four cancelling triples and the
    # energy defect at lag 42.
    assert {
        lag: (
            correlations[lag]
            + correlations[42 - lag]
            + correlations[42 + lag]
            + correlations[84 - lag]
        )
        for lag in (4, 8, 12, 16)
    } == {4: 0, 8: 0, 12: 0, 16: 0}
    assert correlations[0] + 2 * correlations[42] == 14

    # Check the fold identity independently on random small-integer rows.
    rng = Random(66842)
    for _ in range(24):
        fixture: Quadruple = (
            tuple(rng.randrange(-3, 4) for _ in range(LONG)),
            tuple(rng.randrange(-3, 4) for _ in range(LONG)),
            tuple(rng.randrange(-3, 4) for _ in range(SHORT)),
            tuple(rng.randrange(-3, 4) for _ in range(SHORT)),
        )
        direct = summed_periodic_correlations(fold_quadruple(fixture))
        derived = fold_correlations_from_aperiodic(
            base_correlations(fixture)
        )
        assert direct == derived

    assert equal_separation_pairs(base) == 3
    assert folded_correlations[0] == 2 + 4 * equal_separation_pairs(base)
    target_equal_pairs = (334 - 2) // 4
    assert target_equal_pairs == 83
    minimum_base_distance = target_equal_pairs - equal_separation_pairs(base)
    assert minimum_base_distance == 80

    # Verify the shell norm expansion on random integer G.
    seed_fold = expected_seed_fold()
    for _ in range(24):
        g_value: Quadruple = tuple(
            tuple(rng.randrange(-1, 2) for _ in range(FOLD))
            for _ in range(4)
        )  # type: ignore[assignment]
        expanded = summed_periodic_correlations(
            add_scaled(seed_fold, 2, g_value)
        )
        predicted = tuple(
            seed_value + 2 * shell_value
            for seed_value, shell_value in zip(
                summed_periodic_correlations(seed_fold),
                shell_equation(g_value),
            )
        )
        assert expanded == predicted

    generic = local_component_polynomial((True, True, True, True))
    long_exception = local_component_polynomial((True, False, True, True))
    short_exception = local_component_polynomial((False, True, True, False))
    center = center_component_polynomial()
    assert generic == {0: 1, 2: 12, 4: 8}
    assert long_exception == {0: 1, 2: 6}
    assert short_exception == {0: 1, 2: 2}
    assert center == {0: 1, 2: 4}
    transfer = transfer_polynomial()
    assert transfer[80] == EXPECTED_TRANSFER_COEFFICIENT_80
    assert set(degree % 2 for degree in transfer) == {0}
    assert max(transfer) == 162
    unconstrained_shell = comb(163, 80) * (1 << 80)

    # Convert the base-row bound to the natural (s,q) Hamming metric.
    assert special_change_case_split(40) == ((40, 0, 0),)
    assert special_change_case_split(41) == (
        (39, 2, 0),
        (40, 1, 0),
        (41, 0, 0),
    )
    reciprocal_masks = reciprocal_q_masks_of_weight_at_most_two()
    assert {weight: len(masks) for weight, masks in reciprocal_masks.items()} == {
        0: 1,
        1: 1,
        2: 83,
    }
    assert reciprocal_masks[1] == ((125,),)
    verify_center_q_flip_obstruction()

    # Of 83 reciprocal q pairs, exactly 80 can lie on the minimum base shell.
    # Roots +1 and -1 leave 21 long and 18 short pairs.
    long_catalog, short_catalog = q_pair_signature_catalogs()
    assert Counter(
        {signature: len(indices) for signature, indices in long_catalog.items()}
    ) == Counter({(-2, 0): 6, (0, 2): 15, (0, -2): 15, (2, 0): 6})
    assert Counter(
        {signature: len(indices) for signature, indices in short_catalog.items()}
    ) == Counter({(2, -2): 10, (0, 0): 18, (-2, 2): 10})
    assert sum(map(len, long_catalog.values())) == 42
    assert sum(map(len, short_catalog.values())) == 38

    expected_long_profiles = {
        (-2, 0): (
            ((-3, 4), (-5, -4)),
            ((6, -5), (4, 5)),
        ),
        (0, 2): (
            ((-4, -5), (-6, 5)),
            ((5, 4), (3, -4)),
        ),
    }
    expected_short_profiles = {
        (0, 0): (
            ((-4, -5), (4, 5)),
            ((5, 4), (-5, -4)),
        )
    }
    for signature in long_catalog:
        profiles = joined_root_profiles(*signature, True)
        assert profiles == expected_long_profiles.get(signature, ())
    for signature in short_catalog:
        profiles = joined_root_profiles(*signature, False)
        assert profiles == expected_short_profiles.get(signature, ())

    surviving_long = {
        signature: indices
        for signature, indices in long_catalog.items()
        if joined_root_profiles(*signature, True)
    }
    surviving_short = {
        signature: indices
        for signature, indices in short_catalog.items()
        if joined_root_profiles(*signature, False)
    }
    assert sum(map(len, surviving_long.values())) == 21
    assert sum(map(len, surviving_short.values())) == 18
    assert sum(map(len, surviving_long.values())) + sum(
        map(len, surviving_short.values())
    ) == 39

    return {
        "status": "verified necessary repair reduction; no H(668) found",
        "seed_bad_base_lags": sorted(residuals),
        "seed_folded_periodic_energy": 14,
        "seed_equal_separation42_pairs": 3,
        "exact_target_equal_separation42_pairs": 83,
        "minimum_base_row_hamming_distance": minimum_base_distance,
        "minimum_special_sq_hamming_distance": 41,
        "minimum_base_shell_group_ring": (
            "cross(F0,G)+2*N(G)=160 with |supp(G)|=80"
        ),
        "unconstrained_base_distance80_shell": unconstrained_shell,
        "reciprocal_skeleton_shell_count": transfer[80],
        "distance41_cases": [
            {"s_only": s_only, "q_only": q_only, "both": both}
            for s_only, q_only, both in special_change_case_split(41)
        ],
        "distance41_weight1_q_case": "infeasible at root -1",
        "distance41_weight2_q_pairs_before_roots": 80,
        "distance41_weight2_q_pairs_after_roots_1_2": 39,
        "distance41_outer_root_profiles_per_pair": 2,
        "scope": (
            "the 42-fold and root filters are necessary, not sufficient, "
            "for BS(84,83)"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

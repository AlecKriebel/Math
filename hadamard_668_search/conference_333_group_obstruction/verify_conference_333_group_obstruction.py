#!/usr/bin/env python3
"""Verify the group-developed conference obstruction at order 334."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "CONFERENCE_333_GROUP_CERTIFICATE.json"

GROUP_ORDER = 333
KERNEL_ORDER = 37
QUOTIENT_ORDER = 9
IDENTITY_CORRELATION = GROUP_ORDER - KERNEL_ORDER
NONIDENTITY_CORRELATION = -KERNEL_ORDER


def cyclic_correlation(word: tuple[int, ...], shift: int) -> int:
    """Return the integral periodic correlation at ``shift``."""

    length = len(word)
    return sum(word[index] * word[(index + shift) % length]
               for index in range(length))


def c3_profiles() -> list[tuple[int, int, int]]:
    """Solve the pushed C3 equations with their forced parities."""

    profiles: list[tuple[int, int, int]] = []
    for first in range(-14, 15, 2):
        for second in range(-15, 16, 2):
            third = -first - second
            if third % 2 == 0 or not -15 <= third <= 15:
                continue
            if first * first + second * second + third * third != 222:
                continue
            if first * second + second * third + third * first != -111:
                continue
            profiles.append((first, second, third))
    return profiles


def triples(total: int, first_even: bool) -> list[tuple[int, int, int, int]]:
    """Enumerate one C9 residue-class triple and its square energy."""

    even = tuple(range(-16, 17, 2))
    odd = tuple(range(-17, 18, 2))
    first_domain = even if first_even else odd
    result: list[tuple[int, int, int, int]] = []
    for first in first_domain:
        for second in odd:
            third = total - first - second
            if third not in odd:
                continue
            square_sum = first * first + second * second + third * third
            if square_sum <= IDENTITY_CORRELATION:
                result.append((first, second, third, square_sum))
    return result


def c9_profile_census(profile: tuple[int, int, int]) -> tuple[int, int]:
    """Count energy candidates and full C9 correlation survivors."""

    classes = [
        triples(profile[0], first_even=True),
        triples(profile[1], first_even=False),
        triples(profile[2], first_even=False),
    ]
    tail_by_energy: dict[int, list[tuple[tuple[int, ...], tuple[int, ...]]]]
    tail_by_energy = defaultdict(list)
    for second in classes[1]:
        for third in classes[2]:
            tail_by_energy[second[3] + third[3]].append((second, third))

    energy_candidates = 0
    survivors = 0
    for first in classes[0]:
        for second, third in tail_by_energy.get(
                IDENTITY_CORRELATION - first[3], ()):
            word = [0] * QUOTIENT_ORDER
            word[0], word[3], word[6] = first[:3]
            word[1], word[4], word[7] = second[:3]
            word[2], word[5], word[8] = third[:3]
            frozen = tuple(word)

            assert sum(frozen) == 0
            assert cyclic_correlation(frozen, 0) == IDENTITY_CORRELATION
            assert frozen[0] % 2 == 0
            assert all(value % 2 for value in frozen[1:])

            energy_candidates += 1
            if all(cyclic_correlation(frozen, shift)
                   == NONIDENTITY_CORRELATION
                   for shift in range(1, 5)):
                survivors += 1
    return energy_candidates, survivors


POINTS = tuple((first, second)
               for first in range(3)
               for second in range(3))


def line_index(direction: int, point: tuple[int, int]) -> int:
    """Index the line of one of the four directions through ``point``."""

    first, second = point
    return (
        first,
        second,
        (first + second) % 3,
        (first - second) % 3,
    )[direction]


def c3x3_profiles(
    base_profiles: list[tuple[int, int, int]],
) -> tuple[int, list[tuple[int, ...]]]:
    """Reconstruct all perfect signed coset-sum profiles on C3 x C3."""

    assignments = 0
    profiles: list[tuple[int, ...]] = []
    for first in range(4):
        for second in range(4):
            for third in range(4):
                for fourth in range(4):
                    assignments += 1
                    lines = tuple(
                        base_profiles[index]
                        for index in (first, second, third, fourth)
                    )
                    numerators = tuple(
                        sum(lines[direction][line_index(direction, point)]
                            for direction in range(4))
                        for point in POINTS
                    )
                    if any(value % 3 for value in numerators):
                        continue
                    word = tuple(value // 3 for value in numerators)

                    if any(
                        sum(word[index] for index, point in enumerate(POINTS)
                            if line_index(direction, point) == coset)
                        != lines[direction][coset]
                        for direction in range(4)
                        for coset in range(3)
                    ):
                        continue
                    assert word[0] % 2 == 0
                    assert all(value % 2 for value in word[1:])
                    assert sum(word) == 0
                    assert sum(value * value for value in word) \
                        == IDENTITY_CORRELATION

                    for delta in POINTS[1:]:
                        correlation = sum(
                            word[index] * word[POINTS.index((
                                (point[0] + delta[0]) % 3,
                                (point[1] + delta[1]) % 3,
                            ))]
                            for index, point in enumerate(POINTS)
                        )
                        assert correlation == NONIDENTITY_CORRELATION
                    profiles.append(word)
    return assignments, profiles


def inverse_word(word: tuple[int, ...]) -> tuple[int, ...]:
    """Apply inversion on the additive group C3 x C3."""

    return tuple(
        word[POINTS.index(((-point[0]) % 3, (-point[1]) % 3))]
        for point in POINTS
    )


def gl2_matrices() -> list[tuple[int, int, int, int]]:
    """Return GL(2,3) in row-major coordinates."""

    result: list[tuple[int, int, int, int]] = []
    for first in range(3):
        for second in range(3):
            for third in range(3):
                for fourth in range(3):
                    if (first * fourth - second * third) % 3:
                        result.append((first, second, third, fourth))
    assert len(result) == 48
    return result


def transform_word(
    word: tuple[int, ...],
    matrix: tuple[int, int, int, int],
    sign: int,
) -> tuple[int, ...]:
    """Pull ``word`` back by one element of GL(2,3), then apply a sign."""

    first, second, third, fourth = matrix
    transformed: list[int] = []
    for target in POINTS:
        source = next(
            point
            for point in POINTS
            if (
                (first * point[0] + second * point[1]) % 3,
                (third * point[0] + fourth * point[1]) % 3,
            ) == target
        )
        transformed.append(sign * word[POINTS.index(source)])
    return tuple(transformed)


def recompute() -> dict[str, object]:
    """Recompute the complete semantic certificate."""

    # Sylow: n_37 divides 9 and is 1 modulo 37, hence n_37=1.  The
    # order-nine quotient is abelian and has a quotient C3.  Inflating a
    # nonprincipal order-three character and using F=F^(-1), chi(F) is a
    # real Eisenstein integer, hence an ordinary integer.  Equation (1)
    # would require chi(F)^2=333, which is impossible.
    possible_sylow_37_counts = [
        count
        for count in (1, 3, 9)
        if count % 37 == 1
    ]
    assert possible_sylow_37_counts == [1]
    square_root = math.isqrt(GROUP_ORDER)
    assert square_root * square_root != GROUP_ORDER

    profiles = c3_profiles()
    per_profile: list[int] = []
    c9_survivors = 0
    for profile in profiles:
        candidate_count, survivor_count = c9_profile_census(profile)
        per_profile.append(candidate_count)
        c9_survivors += survivor_count
    assert len(set(per_profile)) == 1

    radon_assignments, elementary_profiles = c3x3_profiles(profiles)
    distinct_elementary = set(elementary_profiles)
    assert len(distinct_elementary) == len(elementary_profiles)
    inversion_symmetric = sum(
        inverse_word(profile) == profile
        for profile in elementary_profiles
    )
    representative = elementary_profiles[0]
    symmetry_orbit = {
        transform_word(representative, matrix, sign)
        for matrix in gl2_matrices()
        for sign in (1, -1)
    }
    assert symmetry_orbit == distinct_elementary

    # If a,b are membership indicators of g in D and D^(-1), the reduction
    # D+D^(-1)=0 modulo two forces a=b coefficient by coefficient.
    assert all(((first + second) % 2 == 0) == (first == second)
               for first in (0, 1)
               for second in (0, 1))

    return {
        "schema": "h668-conference-333-group-obstruction-v3",
        "group_order": GROUP_ORDER,
        "kernel_order": KERNEL_ORDER,
        "possible_sylow_37_counts": possible_sylow_37_counts,
        "quotient_order": QUOTIENT_ORDER,
        "quotient_has_order_3_character": True,
        "real_eisenstein_character_values_are_integers": True,
        "required_character_square": GROUP_ORDER,
        "required_character_square_is_integer_square": False,
        "prime_quotient_character_obstruction": True,
        "negative_coefficients": (GROUP_ORDER - 1) // 2,
        "inversion_forced_by_mod2": True,
        "identity_correlation": IDENTITY_CORRELATION,
        "nonidentity_correlation": NONIDENTITY_CORRELATION,
        "identity_coset_parity": 0,
        "nonidentity_coset_parity": 1,
        "c3_profiles": [list(profile) for profile in profiles],
        "c9_energy_candidates_per_c3_profile": per_profile[0],
        "c9_energy_candidates_total": sum(per_profile),
        "c9_full_survivors": c9_survivors,
        "c3x3_radon_assignments": radon_assignments,
        "c3x3_integral_profiles": len(elementary_profiles),
        "c3x3_perfect_profiles": len(elementary_profiles),
        "c3x3_identity_sum_histogram": {
            str(value): sum(profile[0] == value
                            for profile in elementary_profiles)
            for value in sorted({profile[0]
                                 for profile in elementary_profiles})
        },
        "c3x3_inversion_symmetric_profiles": inversion_symmetric,
        "c3x3_gl2_sign_orbit_size": len(symmetry_orbit),
        "c3x3_representative": list(representative),
        "group_developed_conference_cores": 0,
    }


def main() -> None:
    expected = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    actual = recompute()
    if actual != expected:
        raise SystemExit(
            "certificate mismatch\n"
            f"expected={json.dumps(expected, sort_keys=True)}\n"
            f"actual={json.dumps(actual, sort_keys=True)}"
        )
    print(json.dumps(actual, indent=2, sort_keys=True))
    print("PASS: no group-developed conference matrix of order 334")


if __name__ == "__main__":
    main()

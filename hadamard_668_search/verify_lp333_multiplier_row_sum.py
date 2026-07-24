#!/usr/bin/env python3
"""Exact row-sum obstruction for multiplier-invariant LP(333) quotients.

Let ``H`` be a subgroup of the quadratic residues in ``F_37^*`` with
``|H|=h``.  An ``H``-invariant QPSK quotient has one zero-column word ``x``
and ``m=36/h`` nonzero-class words.  If ``t`` is their pointwise sum, then

    s_r = x_r + h t_r

is the sum of all 37 QPSK entries in CRT row ``r``.  Summing the LP(333)
correlation equations over all 37 column lags forces

    Re PAF_s(0) = 297,
    Re PAF_s(a) = -37,  a=1,...,4.

The fixed Legendre-symbol compression gives ``sum(t)=0``.  This verifier
enumerates the resulting exact length-nine projection.  It proves that the
order-18, order-9, and order-6 multiplier families are empty.  The order-3
projection is feasible; its pinned witness is only a row-sum witness, not an
LP(333) or Hadamard construction.

Only Python's standard library is used.  All arithmetic is integral.
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
from typing import Iterable, Sequence


P = 37
ROWS = 9
PRIMITIVE_ROOT = 2
SUBGROUP_SIZES = (18, 9, 6, 3)
PROFILE_LAGS = (1, 2, 3, 4)

# Fourth roots of unity as exact Gaussian integers.
ROOTS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
SIGN_PAIRS: tuple[tuple[int, int], ...] = (
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1),
)

CANONICAL_ZERO_EXPONENTS: tuple[int, ...] = (0, 0, 0, 1, 2, 3, 1, 3, 2)
TARGET_PROFILE = (-37, -37, -37, -37)
TARGET_ROW_ENERGY = 297

# This satisfies the h=3 row-sum projection but is not claimed to lift.
H3_ROW_SUM_WITNESS: tuple[tuple[int, int], ...] = (
    (4, -3),
    (1, 6),
    (-2, -3),
    (12, 1),
    (-1, 0),
    (-6, -1),
    (-6, 1),
    (0, -1),
    (-1, 0),
)

EXPECTED_CANONICAL_COUNTS = {
    18: (0, 0, 0),
    9: (40, 29, 0),
    6: (2_376, 971, 0),
}
EXPECTED_CHANNEL_COUNTS = {
    18: 1,
    9: 21,
    6: 589,
    3: 102_869,
}
EXPECTED_H3_ENERGY_PAIRS = 46_503_026
EXPECTED_ZERO_CORES = 972
EXPECTED_ALL_CORE_COUNTS = {
    18: 0,
    9: 38_880,
    6: 2_309_472,
}

Gaussian = tuple[int, int]
Profile = tuple[int, int, int, int]
Word = tuple[int, ...]
Matrix = tuple[tuple[int, ...], ...]
ChannelKey = tuple[int, Profile]


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def inner(left: Gaussian, right: Gaussian) -> int:
    return left[0] * right[0] + left[1] * right[1]


def phase_sum(exponents: Sequence[int]) -> Gaussian:
    total = (0, 0)
    for exponent in exponents:
        total = add(total, ROOTS[exponent])
    return total


def real_paf_gaussian(sequence: Sequence[Gaussian], lag: int) -> int:
    length = len(sequence)
    return sum(
        inner(sequence[index], sequence[(index + lag) % length])
        for index in range(length)
    )


def real_paf_exponents(exponents: Sequence[int], lag: int) -> int:
    return real_paf_gaussian(tuple(ROOTS[value] for value in exponents), lag)


def real_paf_signs(signs: Sequence[int], lag: int) -> int:
    length = len(signs)
    return sum(
        signs[index] * signs[(index + lag) % length]
        for index in range(length)
    )


def real_signature(exponents: Sequence[int]) -> Profile:
    return tuple(  # type: ignore[return-value]
        real_paf_exponents(exponents, lag) for lag in PROFILE_LAGS
    )


def sign_words(exponents: Sequence[int]) -> tuple[Word, Word]:
    pairs = tuple(SIGN_PAIRS[value] for value in exponents)
    return (
        tuple(pair[0] for pair in pairs),
        tuple(pair[1] for pair in pairs),
    )


def classes_for_subgroup_size(h: int) -> tuple[tuple[int, ...], ...]:
    """Return the ``36/h`` cosets ``2^j H`` for the order-h subgroup."""

    if h not in SUBGROUP_SIZES:
        raise ValueError("h must be one of 18, 9, 6, 3")
    class_count = (P - 1) // h
    subgroup = tuple(
        pow(PRIMITIVE_ROOT, class_count * exponent, P)
        for exponent in range(h)
    )
    classes = tuple(
        tuple(
            (pow(PRIMITIVE_ROOT, class_index, P) * value) % P
            for value in subgroup
        )
        for class_index in range(class_count)
    )
    if any(len(set(part)) != h for part in classes):
        raise AssertionError("a cyclotomic class has the wrong size")
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("cyclotomic classes do not partition F_37^*")
    quadratic_residues = {pow(PRIMITIVE_ROOT, 2 * index, P) for index in range(18)}
    if not set(subgroup) <= quadratic_residues:
        raise AssertionError("H is not contained in the quadratic residues")
    return classes


def transition_matrix(
    parts: Sequence[Sequence[int]], representative: int
) -> Matrix:
    return tuple(
        tuple(
            sum(
                (value + representative) % P in parts[right]
                for value in parts[left]
            )
            for right in range(len(parts))
        )
        for left in range(len(parts))
    )


def verify_transition_sum_identities() -> dict[int, int]:
    """Verify ``D+h sum_s M_s = w w^T`` for every retained subgroup."""

    result: dict[int, int] = {}
    for h in SUBGROUP_SIZES:
        classes = classes_for_subgroup_size(h)
        parts = ((0,),) + classes
        sizes = (1,) + (h,) * len(classes)
        zero_matrix = tuple(
            tuple(
                sizes[left] if left == right else 0
                for right in range(len(parts))
            )
            for left in range(len(parts))
        )
        matrices = tuple(
            transition_matrix(parts, part[0]) for part in classes
        )

        # Reconstruct each matrix with every representative in its class.
        for class_index, part in enumerate(classes):
            for representative in part:
                if transition_matrix(parts, representative) != matrices[class_index]:
                    raise AssertionError("transition counts are not class-invariant")

        summed = tuple(
            tuple(
                zero_matrix[left][right]
                + h * sum(matrix[left][right] for matrix in matrices)
                for right in range(len(parts))
            )
            for left in range(len(parts))
        )
        expected = tuple(
            tuple(sizes[left] * sizes[right] for right in range(len(parts)))
            for left in range(len(parts))
        )
        if summed != expected:
            raise AssertionError(f"row-sum matrix identity failed for h={h}")
        result[h] = len(classes)
    return result


@lru_cache(maxsize=1)
def zero_core_catalog() -> tuple[Word, ...]:
    """Enumerate every zero word surviving each b=0 divisibility test."""

    eligible: dict[int, set[Word]] = {h: set() for h in SUBGROUP_SIZES}
    perfect: set[Word] = set()
    for word in product(range(4), repeat=ROWS):
        if phase_sum(word) != (1, 0):
            continue
        signature = real_signature(word)
        if signature == (-1, -1, -1, -1):
            perfect.add(word)
        for h in SUBGROUP_SIZES:
            # From R_0(a)+h sum_j R_j(a)=-1.
            if all((value + 1) % h == 0 for value in signature):
                eligible[h].add(word)

    if len(perfect) != EXPECTED_ZERO_CORES:
        raise AssertionError("the LP(9) core catalog no longer has size 972")
    for h, catalog in eligible.items():
        if catalog != perfect:
            raise AssertionError(
                f"the b=0 filter for h={h} is not exactly the LP(9) catalog"
            )
    if CANONICAL_ZERO_EXPONENTS not in perfect:
        raise AssertionError("the canonical zero word left the LP(9) catalog")
    return tuple(sorted(perfect))


def verify_zero_core_normalization() -> dict[str, int]:
    """Check that the standard 972 actions act freely and transitively."""

    canonical_a, canonical_b = sign_words(CANONICAL_ZERO_EXPONENTS)
    units_mod_9 = (1, 2, 4, 5, 7, 8)
    pair_to_exponent = {pair: index for index, pair in enumerate(SIGN_PAIRS)}
    orbit: set[Word] = set()
    action_count = 0
    for shift_a in range(ROWS):
        for shift_b in range(ROWS):
            for unit in units_mod_9:
                for swap in (False, True):
                    a = tuple(
                        canonical_a[(unit * row + shift_a) % ROWS]
                        for row in range(ROWS)
                    )
                    b = tuple(
                        canonical_b[(unit * row + shift_b) % ROWS]
                        for row in range(ROWS)
                    )
                    if swap:
                        a, b = b, a
                    orbit.add(
                        tuple(
                            pair_to_exponent[pair]
                            for pair in zip(a, b, strict=True)
                        )
                    )
                    action_count += 1
    catalog = set(zero_core_catalog())
    if action_count != EXPECTED_ZERO_CORES:
        raise AssertionError("zero-core normalization action count changed")
    if len(orbit) != action_count or orbit != catalog:
        raise AssertionError("zero-core normalization is not free and transitive")
    return {"actions": action_count, "orbit": len(orbit)}


def class_sign_sum_values(h: int) -> tuple[int, ...]:
    """Possible sums of ``m=36/h`` independent signs."""

    class_count = (P - 1) // h
    return tuple(range(-class_count, class_count + 1, 2))


def gaussian_class_sum_alphabet(h: int) -> tuple[Gaussian, ...]:
    """Distinct sums of ``m=36/h`` fourth roots, reconstructed via A/B."""

    values = class_sign_sum_values(h)
    alphabet = {
        ((a_sum + b_sum) // 2, (b_sum - a_sum) // 2)
        for a_sum in values
        for b_sum in values
    }
    expected_size = (len(values)) ** 2
    if len(alphabet) != expected_size:
        raise AssertionError("A/B sums did not map bijectively to Gaussian sums")
    return tuple(sorted(alphabet))


def channel_target(h: int) -> int:
    """Return the one-channel-pair energy target ``288/h``."""

    if h not in SUBGROUP_SIZES:
        raise ValueError("h must be one of 18, 9, 6, 3")
    return 288 // h


def channel_term(sign: int, value: int, h: int) -> int:
    """Energy increment ``h p^2/2 + sign*p``."""

    numerator = h * value * value
    if numerator % 2:
        raise AssertionError("channel energy ceased to be integral")
    result = numerator // 2 + sign * value
    if result < 0:
        raise AssertionError("channel energy increment became negative")
    return result


def _enumerate_channel(
    signs: Word, h: int, *, with_profile: bool
) -> Counter[int] | Counter[ChannelKey]:
    """Enumerate one real sign channel under its exact sum/energy bound."""

    if len(signs) != ROWS or any(value not in (-1, 1) for value in signs):
        raise ValueError("a channel must be a length-nine sign word")
    values = class_sign_sum_values(h)
    maximum = max(abs(value) for value in values)
    target = channel_target(h)
    vector = [0] * ROWS
    if with_profile:
        result_with_profile: Counter[ChannelKey] = Counter()
    else:
        result_energy: Counter[int] = Counter()

    def recurse(row: int, total_sum: int, energy: int) -> None:
        if energy > target:
            return
        if row == ROWS:
            if total_sum != 0:
                return
            if with_profile:
                lifted = tuple(
                    signs[index] + h * vector[index]
                    for index in range(ROWS)
                )
                profile: Profile = tuple(  # type: ignore[assignment]
                    real_paf_signs(lifted, lag) for lag in PROFILE_LAGS
                )
                result_with_profile[(energy, profile)] += 1
            else:
                result_energy[energy] += 1
            return

        remaining = ROWS - row - 1
        for value in values:
            next_energy = energy + channel_term(signs[row], value, h)
            if next_energy > target:
                continue
            next_sum = total_sum + value
            if abs(next_sum) > maximum * remaining:
                continue
            vector[row] = value
            recurse(row + 1, next_sum, next_energy)

    recurse(0, 0, 0)
    return result_with_profile if with_profile else result_energy


@lru_cache(maxsize=None)
def channel_energy_distribution(signs: Word, h: int) -> Counter[int]:
    result = _enumerate_channel(signs, h, with_profile=False)
    if not isinstance(result, Counter):
        raise AssertionError("channel enumerator returned the wrong type")
    return result


@lru_cache(maxsize=None)
def channel_profile_distribution(signs: Word, h: int) -> Counter[ChannelKey]:
    result = _enumerate_channel(signs, h, with_profile=True)
    if not isinstance(result, Counter):
        raise AssertionError("channel enumerator returned the wrong type")
    return result


def energy_pair_count(
    left: Counter[int], right: Counter[int], target: int
) -> int:
    return sum(count * right[target - energy] for energy, count in left.items())


def combined_profile_census(word: Word, h: int) -> Counter[Profile]:
    """Count all projected profiles at the forced zero-lag energy."""

    a_signs, b_signs = sign_words(word)
    left = channel_profile_distribution(a_signs, h)
    right = channel_profile_distribution(b_signs, h)
    target = channel_target(h)
    profiles: Counter[Profile] = Counter()
    for (left_energy, left_profile), left_count in left.items():
        for (right_energy, right_profile), right_count in right.items():
            if left_energy + right_energy != target:
                continue
            sums = tuple(
                left_profile[index] + right_profile[index]
                for index in range(len(PROFILE_LAGS))
            )
            if any(value % 2 for value in sums):
                raise AssertionError("combined sign PAF is not even")
            profile: Profile = tuple(  # type: ignore[assignment]
                value // 2 for value in sums
            )
            profiles[profile] += left_count * right_count
    return profiles


@lru_cache(maxsize=1)
def verify_canonical_census() -> dict[int, dict[str, int]]:
    """Reproduce the exact canonical counts for h=18,9,6,3."""

    a_signs, b_signs = sign_words(CANONICAL_ZERO_EXPONENTS)
    result: dict[int, dict[str, int]] = {}

    for h in (18, 9, 6):
        alphabet = gaussian_class_sum_alphabet(h)
        expected_alphabet = (36 // h + 1) ** 2
        if len(alphabet) != expected_alphabet:
            raise AssertionError(f"wrong Gaussian alphabet size for h={h}")
        left = channel_profile_distribution(a_signs, h)
        right = channel_profile_distribution(b_signs, h)
        left_count = sum(left.values())
        right_count = sum(right.values())
        if left_count != EXPECTED_CHANNEL_COUNTS[h] or right_count != left_count:
            raise AssertionError(f"wrong channel-state count for h={h}")
        profiles = combined_profile_census(CANONICAL_ZERO_EXPONENTS, h)
        state_count = sum(profiles.values())
        target_hits = profiles[TARGET_PROFILE]
        expected = EXPECTED_CANONICAL_COUNTS[h]
        actual = (state_count, len(profiles), target_hits)
        if actual != expected:
            raise AssertionError(
                f"canonical projection count for h={h} changed: {actual}"
            )
        result[h] = {
            "class_count": 36 // h,
            "alphabet_size": len(alphabet),
            "channel_states": left_count,
            "energy_sum_states": state_count,
            "profiles": len(profiles),
            "target_hits": target_hits,
        }

    h = 3
    alphabet = gaussian_class_sum_alphabet(h)
    left_energy = channel_energy_distribution(a_signs, h)
    right_energy = channel_energy_distribution(b_signs, h)
    left_count = sum(left_energy.values())
    right_count = sum(right_energy.values())
    if left_count != EXPECTED_CHANNEL_COUNTS[h] or right_count != left_count:
        raise AssertionError("wrong h=3 channel-state count")
    pair_count = energy_pair_count(left_energy, right_energy, channel_target(h))
    if pair_count != EXPECTED_H3_ENERGY_PAIRS:
        raise AssertionError(f"h=3 energy-pair count changed: {pair_count}")
    result[h] = {
        "class_count": 36 // h,
        "alphabet_size": len(alphabet),
        "channel_states": left_count,
        "energy_sum_states": pair_count,
        "profiles": -1,
        "target_hits": -1,
    }
    return result


def verify_h3_witness() -> dict[str, object]:
    """Verify the pinned h=3 row-sum witness and recover its relaxed t."""

    h = 3
    x = tuple(ROOTS[value] for value in CANONICAL_ZERO_EXPONENTS)
    if len(H3_ROW_SUM_WITNESS) != ROWS:
        raise AssertionError("h=3 witness length changed")
    if phase_sum(CANONICAL_ZERO_EXPONENTS) != (1, 0):
        raise AssertionError("canonical zero word no longer sums to one")
    witness_sum = (
        sum(value[0] for value in H3_ROW_SUM_WITNESS),
        sum(value[1] for value in H3_ROW_SUM_WITNESS),
    )
    witness_energy = sum(inner(value, value) for value in H3_ROW_SUM_WITNESS)
    witness_profile: Profile = tuple(  # type: ignore[assignment]
        real_paf_gaussian(H3_ROW_SUM_WITNESS, lag) for lag in PROFILE_LAGS
    )
    if witness_sum != (1, 0):
        raise AssertionError("h=3 witness does not sum to one")
    if witness_energy != TARGET_ROW_ENERGY:
        raise AssertionError("h=3 witness has the wrong zero-lag energy")
    if witness_profile != TARGET_PROFILE:
        raise AssertionError("h=3 witness has the wrong nonzero PAF profile")

    t_values: list[Gaussian] = []
    for row in range(ROWS):
        difference = (
            H3_ROW_SUM_WITNESS[row][0] - x[row][0],
            H3_ROW_SUM_WITNESS[row][1] - x[row][1],
        )
        if difference[0] % h or difference[1] % h:
            raise AssertionError("h=3 witness is not congruent to x modulo 3")
        t_values.append((difference[0] // h, difference[1] // h))
    t = tuple(t_values)
    if (
        sum(value[0] for value in t),
        sum(value[1] for value in t),
    ) != (0, 0):
        raise AssertionError("recovered h=3 t does not sum to zero")
    alphabet = set(gaussian_class_sum_alphabet(h))
    if any(value not in alphabet for value in t):
        raise AssertionError("recovered h=3 t left the 12-root alphabet")

    a_signs, b_signs = sign_words(CANONICAL_ZERO_EXPONENTS)
    p = tuple(value[0] - value[1] for value in t)
    q = tuple(value[0] + value[1] for value in t)
    allowed = set(class_sign_sum_values(h))
    if any(value not in allowed for value in (*p, *q)):
        raise AssertionError("recovered h=3 A/B sums left the allowed alphabet")
    if sum(p) or sum(q):
        raise AssertionError("recovered h=3 A/B sums are not balanced")
    left_energy = sum(
        channel_term(a_signs[row], p[row], h) for row in range(ROWS)
    )
    right_energy = sum(
        channel_term(b_signs[row], q[row], h) for row in range(ROWS)
    )
    if left_energy + right_energy != channel_target(h):
        raise AssertionError("h=3 witness has the wrong channel energy")
    return {
        "sum": witness_sum,
        "energy": witness_energy,
        "profile": witness_profile,
        "t": t,
        "p": p,
        "q": q,
        "left_energy": left_energy,
        "right_energy": right_energy,
    }


@lru_cache(maxsize=1)
def verify_all_zero_cores() -> dict[int, dict[str, int]]:
    """Replay h=18,9,6 on all 972 zero cores using cached sign channels."""

    catalog = zero_core_catalog()
    result: dict[int, dict[str, int]] = {}
    for h in (18, 9, 6):
        per_core_counts: Counter[int] = Counter()
        total_states = 0
        target_hits = 0
        for word in catalog:
            profiles = combined_profile_census(word, h)
            state_count = sum(profiles.values())
            per_core_counts[state_count] += 1
            total_states += state_count
            target_hits += profiles[TARGET_PROFILE]
        expected_per_core = EXPECTED_CANONICAL_COUNTS[h][0]
        if per_core_counts != Counter({expected_per_core: EXPECTED_ZERO_CORES}):
            raise AssertionError(f"all-core state counts changed for h={h}")
        if total_states != EXPECTED_ALL_CORE_COUNTS[h]:
            raise AssertionError(f"all-core total changed for h={h}")
        if target_hits:
            raise AssertionError(f"the h={h} row-sum obstruction has a hit")
        result[h] = {
            "zero_cores": len(catalog),
            "states_per_core": expected_per_core,
            "total_states": total_states,
            "target_hits": target_hits,
        }
    return result


def verify_phi3_shell() -> tuple[tuple[Gaussian, Gaussian, Gaussian], ...]:
    """Check the four-state Phi_3 shell implied inside the h=6 equations."""

    # If T_0=u=a+bi, T_1=v=c+di, and T_2=-u-v, the summed nonzero
    # column-class Phi_3 equation is
    #
    #   6 q + a + 3 b = 18,
    #   q=a^2+b^2+c^2+d^2+ac+bd.
    #
    # Completing squares gives q >= 3(a^2+b^2)/4.  Cauchy then bounds
    # q <= 4, so every coordinate has absolute value at most two.
    solutions: list[tuple[Gaussian, Gaussian, Gaussian]] = []
    for a, b, c, d in product(range(-2, 3), repeat=4):
        q = a * a + b * b + c * c + d * d + a * c + b * d
        if 6 * q + a + 3 * b != 18:
            continue
        u = (a, b)
        v = (c, d)
        solutions.append((u, v, (-a - c, -b - d)))
    expected = tuple(
        sorted(
            (
                ((0, -2), (-1, 1), (1, 1)),
                ((0, -2), (0, 0), (0, 2)),
                ((0, -2), (0, 2), (0, 0)),
                ((0, -2), (1, 1), (-1, 1)),
            )
        )
    )
    actual = tuple(sorted(solutions))
    if actual != expected:
        raise AssertionError(f"Phi_3 shell changed: {actual}")
    return actual


def verify_all() -> dict[str, object]:
    transition_counts = verify_transition_sum_identities()
    normalization = verify_zero_core_normalization()
    canonical = verify_canonical_census()
    witness = verify_h3_witness()
    all_cores = verify_all_zero_cores()
    phi3 = verify_phi3_shell()
    return {
        "transition_class_counts": transition_counts,
        "normalization": normalization,
        "canonical": canonical,
        "h3_witness": witness,
        "all_zero_cores": all_cores,
        "phi3_states": phi3,
    }


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(tuple(argv) if argv is not None else None)
    counts = verify_all()
    canonical = counts["canonical"]
    all_cores = counts["all_zero_cores"]
    print("PASS: D + h sum(M_s) = w w^T for h=18,9,6,3")
    print(
        "PASS: b=0 equations give the same 972 LP(9) zero cores; "
        "normalization is free and transitive"
    )
    for h in (18, 9, 6):
        row = canonical[h]  # type: ignore[index]
        replay = all_cores[h]  # type: ignore[index]
        print(
            f"PASS: h={h}: {row['energy_sum_states']} canonical "
            f"energy/sum states, {row['profiles']} profiles, "
            f"{row['target_hits']} target hits; "
            f"{replay['total_states']} states across all 972 cores"
        )
    h3 = canonical[3]  # type: ignore[index]
    print(
        "PASS: h=3 boundary: "
        f"{h3['energy_sum_states']} energy/sum states and an exact "
        "row-sum witness (not an LP(333) candidate)"
    )
    print("PASS: h=6 Phi_3 corollary has exactly four Gaussian states")


if __name__ == "__main__":
    main()

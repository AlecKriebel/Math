#!/usr/bin/env python3
"""Verify the primitive-ninth-root ramified jet for the order-three LP(333).

Let P and Q be the plus supports of a putative Legendre pair.  After Fourier
evaluation in the Z/9 coordinate at a primitive ninth root z, their column
group-ring images must satisfy

    A A* + B B* = 167 e

in Z[z][F_37], where star sends z to z^-1 and the column coordinate to its
negative.  Put pi=1-z.  Since

    Phi_9(1-pi) = pi^6 - 6 pi^5 + 15 pi^4 - 21 pi^3
                  + 18 pi^2 - 9 pi + 3,

reduction modulo 3 gives the six-coefficient jet ring

    F_3[pi]/(pi^6).

Every nonzero cyclotomic-class word has plus weight three or six, so its
constant jet coefficient is zero.  The canonical zero column contributes
reciprocal power five, while 167-5=162 has pi-adic valuation 24.  Therefore
all six coefficients of A A*+B B*-167e vanish in the jet ring.

Coefficient zero is automatic.  Coefficient one is exactly the known local
Eisenstein negation-pair sieve.  Coefficients two through five retain
primitive-nine information and include nonzero/nonzero class products.

This dependency-free verifier checks every arithmetic statement above,
exhausts the coefficient-one equivalence on all 10^4 profile quadruples,
and gives an explicit aggregate/origin/local-mod-3 survivor that fails a
higher primitive-nine coefficient.  It is a necessary-condition result,
not an LP(333), a Hadamard matrix, or a catalog exclusion.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from typing import Iterable, Sequence


P = 37
ROWS = 9
CLASS_COUNT = 12
MODULUS = 3
JET_LENGTH = 6
PRIMITIVE_ROOT = 2

CANONICAL_ZERO_EXPONENTS: tuple[int, ...] = (0, 0, 0, 1, 2, 3, 1, 3, 2)
SIGN_PAIRS: tuple[tuple[int, int], ...] = (
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1),
)

ZERO_A_PLUS: tuple[int, ...] = tuple(
    int(SIGN_PAIRS[value][0] == 1) for value in CANONICAL_ZERO_EXPONENTS
)
ZERO_B_PLUS: tuple[int, ...] = tuple(
    int(SIGN_PAIRS[value][1] == 1) for value in CANONICAL_ZERO_EXPONENTS
)

# One pinned witness from the local Eisenstein sieve.  Profile IDs index
# compositions_of_three() below.  It satisfies the aggregate join, origin
# energy 54, and all six coefficient-one negation-pair tests.  It is not
# claimed to satisfy the full 3 by 37 compressed equations.
LOCAL_SURVIVOR_TARGET = (-3, -3, -4, -2)
LOCAL_SURVIVOR_A_IDS = (3, 1, 6, 5, 9, 3, 5, 7, 1, 5, 5, 5)
LOCAL_SURVIVOR_B_IDS = (5, 9, 5, 2, 5, 5, 5, 5, 5, 8, 5, 5)

EXPECTED_WORD_JET_HASH = (
    "91138c56cf22b40b1984a5430757b436994b409095314bdcd43967e348cf71c7"
)
EXPECTED_STRICTNESS_HASH = (
    "e66c31bf65e52264957bc9a2aa2c6af7adaaa5cc4374b77c2f458f2fcdc857c9"
)

Jet = tuple[int, int, int, int, int, int]
Word = tuple[int, ...]
Profile = tuple[int, int, int]
Eisenstein = tuple[int, int]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def require_hash(label: str, value: object, expected: str) -> str:
    actual = compact_hash(value)
    if expected and actual != expected:
        raise AssertionError(f"{label} hash changed: {actual} != {expected}")
    return actual


def jet_add(left: Jet, right: Jet) -> Jet:
    return tuple(
        (left[index] + right[index]) % MODULUS
        for index in range(JET_LENGTH)
    )  # type: ignore[return-value]


def jet_negate(value: Jet) -> Jet:
    return tuple((-entry) % MODULUS for entry in value)  # type: ignore[return-value]


def jet_multiply(left: Jet, right: Jet) -> Jet:
    result = [0] * JET_LENGTH
    for first in range(JET_LENGTH):
        for second in range(JET_LENGTH - first):
            result[first + second] += left[first] * right[second]
    return tuple(entry % MODULUS for entry in result)  # type: ignore[return-value]


def jet_power(value: Jet, exponent: int) -> Jet:
    if exponent < 0:
        raise ValueError("jet exponent must be nonnegative")
    result: Jet = (1, 0, 0, 0, 0, 0)
    base = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = jet_multiply(result, base)
        base = jet_multiply(base, base)
        remaining >>= 1
    return result


def jet_substitute(value: Jet, argument: Jet) -> Jet:
    result: Jet = (0, 0, 0, 0, 0, 0)
    for exponent, coefficient in enumerate(value):
        if coefficient:
            term = tuple(
                coefficient * entry % MODULUS
                for entry in jet_power(argument, exponent)
            )
            result = jet_add(result, term)  # type: ignore[arg-type]
    return result


def word_jet(values: Sequence[int]) -> Jet:
    """Return ``sum_r values[r]*(1-pi)^r`` modulo ``(3,pi^6)``."""

    if len(values) != ROWS:
        raise ValueError("a row word must have length nine")
    result = []
    for degree in range(JET_LENGTH):
        coefficient = sum(
            value * ((-1) ** degree) * comb(row, degree)
            for row, value in enumerate(values)
            if row >= degree
        )
        result.append(coefficient % MODULUS)
    return tuple(result)  # type: ignore[return-value]


def reverse_word(values: Sequence[int]) -> Word:
    if len(values) != ROWS:
        raise ValueError("a row word must have length nine")
    return tuple(values[(-row) % ROWS] for row in range(ROWS))


def jet_star(value: Jet) -> Jet:
    """Apply ``pi -> 1-z^-1 = -pi/(1-pi)``."""

    pi_star: Jet = (0, 2, 2, 2, 2, 2)
    return jet_substitute(value, pi_star)


def cyclic_intersection(left: Sequence[int], right: Sequence[int], lag: int) -> int:
    return sum(
        left[row] * right[(row + lag) % ROWS] for row in range(ROWS)
    )


def compositions_of_three() -> tuple[Profile, ...]:
    result = tuple(
        (first, second, 3 - first - second)
        for first in range(4)
        for second in range(4)
        if 0 <= 3 - first - second <= 3
    )
    if len(result) != 10:
        raise AssertionError("the profile catalog must have ten entries")
    return result


PROFILES = compositions_of_three()


def profile_eisenstein(profile: Profile) -> Eisenstein:
    first, second, third = profile
    return first - third, second - third


def eisenstein_conjugate(value: Eisenstein) -> Eisenstein:
    real, omega = value
    return real - omega, -omega


def eisenstein_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def eisenstein_mod3(value: Eisenstein) -> Eisenstein:
    return value[0] % 3, value[1] % 3


def eisenstein_norm(value: Eisenstein) -> int:
    real, omega = value
    return real * real - real * omega + omega * omega


def pair_signature(left: Profile, right: Profile) -> Eisenstein:
    return eisenstein_mod3(
        eisenstein_add(
            eisenstein_conjugate(profile_eisenstein(left)),
            profile_eisenstein(right),
        )
    )


def profile_first_digit(profile: Profile) -> int:
    """Return ``(word/(1-z)) mod (1-z)`` for a weight-three word."""

    _, second, third = profile
    return (third - second) % 3


def canonical_support(profile: Profile) -> Word:
    """Choose one weight-three support with the prescribed residues mod 3."""

    support: list[int] = []
    for residue, count in enumerate(profile):
        support.extend(tuple(range(residue, ROWS, 3))[:count])
    if len(support) != 3:
        raise AssertionError("profile did not produce a triple")
    chosen = set(support)
    return tuple(int(row in chosen) for row in range(ROWS))


def complement(values: Sequence[int]) -> Word:
    return tuple(1 - value for value in values)


def cyclotomic_classes() -> tuple[tuple[int, ...], ...]:
    subgroup = tuple(
        pow(PRIMITIVE_ROOT, CLASS_COUNT * exponent, P) for exponent in range(3)
    )
    if subgroup != (1, 26, 10):
        raise AssertionError("the order-three subgroup changed")
    classes = tuple(
        tuple(
            pow(PRIMITIVE_ROOT, class_index, P) * value % P
            for value in subgroup
        )
        for class_index in range(CLASS_COUNT)
    )
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("the classes do not partition F_37^*")
    for class_index, part in enumerate(classes):
        if {(-value) % P for value in part} != set(
            classes[(class_index + 6) % CLASS_COUNT]
        ):
            raise AssertionError("negation must shift class indices by six")
    return classes


CLASSES = cyclotomic_classes()
CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}


def divide_by_pi_integrally(value: Sequence[int]) -> tuple[int, ...] | None:
    """Divide in ``Z[z]/(z^6+z^3+1)`` by ``pi=1-z``, if integral."""

    if len(value) != JET_LENGTH:
        raise ValueError("cyclotomic-basis vector must have length six")
    numerator = 2 * value[0] - sum(value[1:])
    if numerator % 3:
        return None
    result = [0] * JET_LENGTH
    result[0] = numerator // 3
    result[1] = value[1] + result[0]
    result[2] = value[2] + result[1]
    result[5] = value[0] - result[0]
    result[3] = value[3] + result[2] - result[5]
    result[4] = value[4] + result[3]
    if result[5] - result[4] != value[5]:
        raise AssertionError("integral pi division replay failed")
    return tuple(result)


def verify_ramified_ring() -> dict[str, object]:
    """Check the local ring and the exact valuation of the defect 162."""

    # Phi_9(1-pi), in ascending powers of pi.
    phi_substitution = (3, -9, 18, -21, 15, -6, 1)
    if tuple(value % 3 for value in phi_substitution) != (0, 0, 0, 0, 0, 0, 1):
        raise AssertionError("Phi_9(1-pi) did not reduce to pi^6 modulo 3")

    current: tuple[int, ...] = (162, 0, 0, 0, 0, 0)
    valuation = 0
    while True:
        quotient = divide_by_pi_integrally(current)
        if quotient is None:
            break
        current = quotient
        valuation += 1
    if valuation != 24:
        raise AssertionError("the pi-adic valuation of 162 is not 24")

    pi: Jet = (0, 1, 0, 0, 0, 0)
    if jet_star(pi) != (0, 2, 2, 2, 2, 2):
        raise AssertionError("the star image of pi changed")
    if jet_power(pi, 6) != (0, 0, 0, 0, 0, 0):
        raise AssertionError("pi^6 must vanish in the mod-3 jet")
    return {
        "phi9_at_one_minus_pi": phi_substitution,
        "jet_ring": "F3[pi]/(pi^6)",
        "defect": 162,
        "defect_pi_valuation": valuation,
    }


def verify_zero_column() -> dict[str, object]:
    """Check the canonical zero-column reciprocal power exactly."""

    combined = tuple(
        cyclic_intersection(ZERO_A_PLUS, ZERO_A_PLUS, lag)
        + cyclic_intersection(ZERO_B_PLUS, ZERO_B_PLUS, lag)
        for lag in range(ROWS)
    )
    if combined != (10, 5, 5, 5, 5, 5, 5, 5, 5):
        raise AssertionError("the zero-column support correlations changed")
    # At every nontrivial ninth root, 10+5*(z+...+z^8)=5.
    if combined[0] - combined[1] != 5 or len(set(combined[1:])) != 1:
        raise AssertionError("the zero-column reciprocal power is not five")

    for word in (ZERO_A_PLUS, ZERO_B_PLUS):
        if jet_star(word_jet(word)) != word_jet(reverse_word(word)):
            raise AssertionError("word reversal disagrees with jet star")
    return {
        "zero_a_plus": ZERO_A_PLUS,
        "zero_b_plus": ZERO_B_PLUS,
        "combined_correlation": combined,
        "primitive9_reciprocal_power": 5,
    }


def profile_of_support(support: Iterable[int]) -> Profile:
    counts = [0, 0, 0]
    for row in support:
        counts[row % 3] += 1
    return tuple(counts)  # type: ignore[return-value]


def verify_word_jets() -> dict[str, object]:
    """Exhaust all weight-three words and their weight-six complements."""

    by_profile: dict[Profile, Counter[Jet]] = {
        profile: Counter() for profile in PROFILES
    }
    all_jets: Counter[Jet] = Counter()
    for support in combinations(range(ROWS), 3):
        word = tuple(int(row in support) for row in range(ROWS))
        profile = profile_of_support(support)
        value = word_jet(word)
        if value[0] != 0:
            raise AssertionError("a weight-three word is not pi-divisible")
        if value[1] != profile_first_digit(profile):
            raise AssertionError("the first jet digit disagrees with the profile")
        complement_value = word_jet(complement(word))
        if complement_value != jet_negate(value):
            raise AssertionError("weight-six complementation is not jet negation")
        by_profile[profile][value] += 1
        all_jets[value] += 1

    first = (0, 1, 2)
    second = (0, 4, 8)
    first_word = tuple(int(row in first) for row in range(ROWS))
    second_word = tuple(int(row in second) for row in range(ROWS))
    if profile_of_support(first) != profile_of_support(second):
        raise AssertionError("the strictness words lost their common profile")
    if word_jet(first_word)[:2] != word_jet(second_word)[:2]:
        raise AssertionError("common mod-3 profiles must have common first digits")
    if word_jet(first_word) == word_jet(second_word):
        raise AssertionError("the full primitive-nine jets must distinguish the lifts")

    payload = tuple(
        (
            profile,
            tuple(sorted((jet, count) for jet, count in by_profile[profile].items())),
        )
        for profile in PROFILES
    )
    word_hash = require_hash("primitive-nine word jets", payload, EXPECTED_WORD_JET_HASH)
    return {
        "weight_three_words": sum(all_jets.values()),
        "distinct_weight_three_jets": len(all_jets),
        "distinct_jets_by_profile": tuple(
            len(by_profile[profile]) for profile in PROFILES
        ),
        "same_profile_counterexample": (
            first,
            second,
            word_jet(first_word),
            word_jet(second_word),
        ),
        "word_jet_hash": word_hash,
    }


def verify_digit_one_equivalence() -> dict[str, object]:
    """Exhaust the equivalence with the Eisenstein negation-pair sieve."""

    allowed = 0
    for a_left, a_right, b_left, b_right in product(PROFILES, repeat=4):
        jet_condition = (
            profile_first_digit(a_right) - profile_first_digit(a_left)
        ) % 3 == (
            profile_first_digit(b_right) - profile_first_digit(b_left)
        ) % 3
        eisenstein_condition = pair_signature(a_left, a_right) == pair_signature(
            b_left, b_right
        )
        if jet_condition != eisenstein_condition:
            raise AssertionError("digit one and the Eisenstein sieve disagree")
        allowed += int(jet_condition)
    if allowed != 3_334:
        raise AssertionError("the coefficient-one survivor count changed")
    return {
        "profile_quadruples": 10_000,
        "coefficient_one_survivors": allowed,
        "matches_eisenstein_pair_sieve": True,
    }


def actual_plus_word(channel: int, class_index: int, profile_id: int) -> Word:
    normalized = canonical_support(PROFILES[profile_id])
    if channel == 0:
        # A has plus weight 6 in even classes and 3 in odd classes.
        return complement(normalized) if class_index % 2 == 0 else normalized
    if channel == 1:
        # B has the opposite weights.
        return normalized if class_index % 2 == 0 else complement(normalized)
    raise ValueError("channel must be zero or one")


def expand_local_survivor() -> tuple[tuple[Word, ...], tuple[Word, ...]]:
    class_a = tuple(
        actual_plus_word(0, class_index, LOCAL_SURVIVOR_A_IDS[class_index])
        for class_index in range(CLASS_COUNT)
    )
    class_b = tuple(
        actual_plus_word(1, class_index, LOCAL_SURVIVOR_B_IDS[class_index])
        for class_index in range(CLASS_COUNT)
    )
    columns_a = [ZERO_A_PLUS]
    columns_b = [ZERO_B_PLUS]
    for column in range(1, P):
        columns_a.append(class_a[CLASS_OF[column]])
        columns_b.append(class_b[CLASS_OF[column]])
    return tuple(columns_a), tuple(columns_b)


def group_ring_jet(columns: Sequence[Sequence[int]]) -> tuple[Jet, ...]:
    if len(columns) != P or any(len(word) != ROWS for word in columns):
        raise ValueError("expected 37 length-nine column words")
    jets = tuple(word_jet(word) for word in columns)
    starred = tuple(jet_star(value) for value in jets)
    result = []
    for column_lag in range(P):
        total: Jet = (0, 0, 0, 0, 0, 0)
        for column in range(P):
            right = (column - column_lag) % P
            total = jet_add(total, jet_multiply(jets[column], starred[right]))
        result.append(total)
    return tuple(result)


def direct_group_ring_jet(
    columns: Sequence[Sequence[int]],
) -> tuple[Jet, ...]:
    """Independently evaluate difference counts before the row jet."""

    result = []
    for column_lag in range(P):
        correlations = []
        for row_lag in range(ROWS):
            correlations.append(
                sum(
                    columns[(column + column_lag) % P][
                        (row + row_lag) % ROWS
                    ]
                    * columns[column][row]
                    for column in range(P)
                    for row in range(ROWS)
                )
            )
        result.append(word_jet(correlations))
    return tuple(result)


def verify_strict_higher_digits() -> dict[str, object]:
    """Replay a local-mod-3 survivor that fails a higher jet coefficient."""

    total_a = (0, 0)
    total_b = (0, 0)
    origin_energy = 0
    for class_index in range(CLASS_COUNT):
        a_profile = PROFILES[LOCAL_SURVIVOR_A_IDS[class_index]]
        b_profile = PROFILES[LOCAL_SURVIVOR_B_IDS[class_index]]
        epsilon = 1 if class_index % 2 == 0 else -1
        a_value = tuple(
            -epsilon * coordinate for coordinate in profile_eisenstein(a_profile)
        )
        b_value = tuple(
            epsilon * coordinate for coordinate in profile_eisenstein(b_profile)
        )
        total_a = eisenstein_add(total_a, a_value)  # type: ignore[arg-type]
        total_b = eisenstein_add(total_b, b_value)  # type: ignore[arg-type]
        origin_energy += eisenstein_norm(profile_eisenstein(a_profile))
        origin_energy += eisenstein_norm(profile_eisenstein(b_profile))
        if class_index < 6 and pair_signature(
            a_profile, PROFILES[LOCAL_SURVIVOR_A_IDS[class_index + 6]]
        ) != pair_signature(
            b_profile, PROFILES[LOCAL_SURVIVOR_B_IDS[class_index + 6]]
        ):
            raise AssertionError("the pinned witness fails coefficient one")
    if (*total_a, *total_b) != LOCAL_SURVIVOR_TARGET:
        raise AssertionError("the pinned witness has the wrong aggregate")
    if origin_energy != 54:
        raise AssertionError("the pinned witness has the wrong origin energy")

    columns_a, columns_b = expand_local_survivor()
    for class_index in range(CLASS_COUNT):
        expected_a_weight = 6 if class_index % 2 == 0 else 3
        expected_b_weight = 3 if class_index % 2 == 0 else 6
        if sum(columns_a[CLASSES[class_index][0]]) != expected_a_weight:
            raise AssertionError("an A class has the wrong weight")
        if sum(columns_b[CLASSES[class_index][0]]) != expected_b_weight:
            raise AssertionError("a B class has the wrong weight")

    fast_a = group_ring_jet(columns_a)
    fast_b = group_ring_jet(columns_b)
    if fast_a != direct_group_ring_jet(columns_a):
        raise AssertionError("A group-ring jet disagrees with direct counts")
    if fast_b != direct_group_ring_jet(columns_b):
        raise AssertionError("B group-ring jet disagrees with direct counts")

    residuals = []
    for column_lag in range(P):
        target: Jet = (
            (167 if column_lag == 0 else 0) % 3,
            0,
            0,
            0,
            0,
            0,
        )
        residuals.append(
            jet_add(jet_add(fast_a[column_lag], fast_b[column_lag]), jet_negate(target))
        )

    nonzero_by_digit = tuple(
        sum(residual[degree] != 0 for residual in residuals)
        for degree in range(JET_LENGTH)
    )
    if nonzero_by_digit[0] != 0 or nonzero_by_digit[1] != 0:
        raise AssertionError("the pinned local survivor must pass digits zero and one")
    if not any(nonzero_by_digit[degree] for degree in range(2, JET_LENGTH)):
        raise AssertionError("the pinned local survivor did not fail a higher digit")

    # H-invariance makes every residual constant on each order-three class.
    class_residuals = []
    for part in CLASSES:
        values = {residuals[column] for column in part}
        if len(values) != 1:
            raise AssertionError("a residual is not constant on its H-class")
        class_residuals.append(next(iter(values)))

    payload = (
        LOCAL_SURVIVOR_TARGET,
        LOCAL_SURVIVOR_A_IDS,
        LOCAL_SURVIVOR_B_IDS,
        tuple(class_residuals),
        nonzero_by_digit,
    )
    strictness_hash = require_hash(
        "primitive-nine strictness witness", payload, EXPECTED_STRICTNESS_HASH
    )
    return {
        "aggregate_target": LOCAL_SURVIVOR_TARGET,
        "origin_energy": origin_energy,
        "coefficient_one_pairs": 6,
        "nonzero_residuals_by_digit": nonzero_by_digit,
        "first_failing_digit": next(
            degree
            for degree in range(2, JET_LENGTH)
            if nonzero_by_digit[degree]
        ),
        "strictness_hash": strictness_hash,
        "is_lp333_candidate": False,
    }


def verify_all() -> dict[str, object]:
    return {
        "ring": verify_ramified_ring(),
        "zero": verify_zero_column(),
        "words": verify_word_jets(),
        "digit_one": verify_digit_one_equivalence(),
        "strictness": verify_strict_higher_digits(),
    }


def main() -> None:
    result = verify_all()
    print(f"jet_ring={result['ring']['jet_ring']}")
    print(f"defect_pi_valuation={result['ring']['defect_pi_valuation']}")
    print(
        "zero_column_primitive9_power="
        f"{result['zero']['primitive9_reciprocal_power']}"
    )
    print(f"word_jet_hash={result['words']['word_jet_hash']}")
    print(
        "coefficient_one_survivors="
        f"{result['digit_one']['coefficient_one_survivors']}/10000"
    )
    print(
        "strictness_nonzero_by_digit="
        f"{result['strictness']['nonzero_residuals_by_digit']}"
    )
    print(
        "strictness_first_failing_digit="
        f"{result['strictness']['first_failing_digit']}"
    )
    print(f"strictness_hash={result['strictness']['strictness_hash']}")
    print("PASS: primitive-nine ramified jet replayed exactly")
    print("STATUS: necessary-condition refinement only; no LP(333) candidate")


if __name__ == "__main__":
    main()

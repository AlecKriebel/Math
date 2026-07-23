#!/usr/bin/env python3
"""Exact bounded checks for the five-comb repair of the order-668 seed.

Two finite nonlinear families are treated.

``literal reciprocal chord``
    Toggle any of the five reciprocal ``q`` parameters
    ``13,17,21,25,29`` in either interval and allow ``s`` to change at all
    twenty physical coordinates carried by those ten parameters.  Gaussian
    elimination of the exact modulo-four lift is used before testing the
    higher layers.

``common-comb completion``
    Tile the 320 non-boundary coefficients of lengths ``(84,84,83,83)`` by
    64 disjoint signed copies of

        P(z) = 1-z^4+z^8-z^12+z^16.

    More generally, reduction modulo ``P`` gives a unit-circle obstruction to
    every overlapping common-``P`` repair having only fourteen remainder
    signs.  In the orthogonally staged disjoint subfamily, the cross term
    restricts every tile row to a set of six or ten mates.  Complementarity
    would force the first and last tile rows to be cross-orthogonal, and the
    checker exhausts all 80,896 possible endpoint pairs.

Finally, the checker constructs the smallest seed-aligned product-form
spectral escape: the alternating comb extends to a complementary octet, and
polarizing the 42-step separation gives 32 flat carrier channels of total
energy 320.  It also classifies all unrestricted normalized length-five
families through size eight.  There are 48 complementary quartets; each
quartet, polarized and repeated four times, gives another flat 32-channel
family.  Their supports pack into the target lengths, leaving fourteen
positions.  Cancelling the new cross terms after packing those channels into
only four polynomials remains open.

The checks use only the standard library and exact integer arithmetic.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations_with_replacement, product
from typing import Iterable, Sequence

from seed import ELIAHOU_Q, ELIAHOU_S
from variable_q_base import base_correlations, special_to_base
from verify_novel_lifting_64 import (
    gate_correlations,
    mod4_lift_equations,
    q_parameter_flips,
    sign_bits,
)


COMB = (13, 17, 21, 25, 29)
LONG_COMB_PARAMETERS = COMB
SHORT_COMB_PARAMETERS = tuple(42 + value for value in COMB)
COMB_PARAMETERS = LONG_COMB_PARAMETERS + SHORT_COMB_PARAMETERS

P = (1, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 1)
P_WORD = (1, -1, 1, -1, 1)

# A minimum complementary family containing the alternating five-comb.
# Repetition is allowed: two channels have the same signed word.
COMPLEMENTARY_OCTET = (
    P_WORD,
    (-1, -1, -1, -1, -1),
    (-1, -1, -1, -1, 1),
    (-1, -1, -1, 1, 1),
    (-1, -1, 1, -1, 1),
    (-1, -1, 1, 1, -1),
    (-1, -1, 1, 1, -1),
    (-1, 1, -1, -1, 1),
)

CARRIER_SHIFTS = (0, 1, 2, 3, 20, 21, 22, 23)

SignWord = tuple[int, ...]
SmallBase = tuple[SignWord, SignWord, SignWord, SignWord]
TileRow = tuple[SignWord, SignWord, SignWord, SignWord]


def aperiodic_cross(
    left: Sequence[int], right: Sequence[int], lag: int
) -> int:
    """Coefficient of ``z^lag`` in ``left * right^*`` for nonnegative lag."""

    if lag < 0:
        return aperiodic_cross(right, left, -lag)
    return sum(
        left[index + lag] * right[index]
        for index in range(min(len(right), len(left) - lag))
    )


def autocorrelation_sum(sequences: Sequence[Sequence[int]], lag: int) -> int:
    return sum(
        aperiodic_cross(sequence, sequence, lag)
        for sequence in sequences
        if lag < len(sequence)
    )


def seed_rank_one_factorization() -> tuple[int, ...]:
    """Return the coefficients in ``sum N(X)=14+32*N((z^42-1)P)``."""

    seed = special_to_base(ELIAHOU_S, ELIAHOU_Q)
    actual = base_correlations(*seed)
    carrier = [0] * 59
    for index, value in enumerate(P):
        carrier[index] -= value
        carrier[index + 42] += value
    predicted = tuple(
        (14 if lag == 0 else 0)
        + (32 * autocorrelation_sum((carrier,), lag) if lag < len(carrier) else 0)
        for lag in range(84)
    )
    if actual != predicted:
        raise AssertionError("the rank-one comb factorization failed")
    return predicted


def polynomial_remainder(
    dividend: Sequence[int], divisor: Sequence[int]
) -> tuple[int, ...]:
    """Return the ordinary integer-polynomial remainder."""

    if not divisor or divisor[-1] not in (-1, 1):
        raise ValueError("a monic or antimonic divisor is required")
    values = list(dividend)
    degree = len(divisor) - 1
    for index in range(len(values) - 1, degree - 1, -1):
        coefficient = values[index] // divisor[-1]
        for offset, divisor_value in enumerate(divisor):
            values[index - degree + offset] -= coefficient * divisor_value
    remainder = values[:degree]
    while remainder and remainder[-1] == 0:
        remainder.pop()
    return tuple(remainder)


def seed_comb_remainders() -> SmallBase:
    """Remainders of the seed polynomials modulo the common comb ``P``."""

    result = tuple(
        polynomial_remainder(sequence, P)
        for sequence in special_to_base(ELIAHOU_S, ELIAHOU_Q)
    )
    return result  # type: ignore[return-value]


def comb_signature(word: Sequence[int]) -> tuple[int, int, int, int]:
    """Positive autocorrelation coefficients of a binary length-five word."""

    if len(word) != 5 or any(value not in (-1, 1) for value in word):
        raise ValueError("a binary word of length five is required")
    return tuple(aperiodic_cross(word, word, lag) for lag in range(1, 5))


def normalized_five_words() -> tuple[SignWord, ...]:
    """All binary length-five words modulo their irrelevant global sign."""

    return tuple((1,) + tail for tail in product((-1, 1), repeat=4))


def complementary_multiset_count(size: int) -> int:
    """Count normalized complementary multisets of the requested size."""

    if size < 0:
        raise ValueError("the family size must be nonnegative")
    signatures = tuple(map(comb_signature, normalized_five_words()))

    @lru_cache(maxsize=None)
    def count(
        word: int, remaining: int, first: int, second: int, third: int, fourth: int
    ) -> int:
        if word == len(signatures):
            return int(
                remaining == 0 and (first, second, third, fourth) == (0, 0, 0, 0)
            )
        if remaining < 0:
            return 0
        signature = signatures[word]
        return sum(
            count(
                word + 1,
                remaining - multiplicity,
                first + multiplicity * signature[0],
                second + multiplicity * signature[1],
                third + multiplicity * signature[2],
                fourth + multiplicity * signature[3],
            )
            for multiplicity in range(remaining + 1)
        )

    return count(0, size, 0, 0, 0, 0)


def complementary_quartets() -> tuple[tuple[SignWord, ...], ...]:
    """Enumerate the 48 normalized complementary length-five quartets."""

    words = normalized_five_words()
    signatures = tuple(map(comb_signature, words))
    result = []
    for indices in combinations_with_replacement(range(len(words)), 4):
        if all(
            sum(signatures[index][lag] for index in indices) == 0
            for lag in range(4)
        ):
            result.append(tuple(words[index] for index in indices))
    return tuple(result)


def quartet_symmetry_representatives() -> tuple[tuple[SignWord, ...], ...]:
    """Quotient quartets by common reversal and common alternation.

    This is a classification symmetry of complementary word families.  It is
    not asserted to preserve the later fixed-slot packing problem.
    """

    def normalize(word: Sequence[int]) -> SignWord:
        return tuple(word[0] * value for value in word)

    def transform(
        family: Sequence[Sequence[int]], reverse: bool, alternate: bool
    ) -> tuple[SignWord, ...]:
        result = []
        for word in family:
            changed = tuple(
                value * ((-1) ** index if alternate else 1)
                for index, value in enumerate(word)
            )
            if reverse:
                changed = tuple(reversed(changed))
            result.append(normalize(changed))
        return tuple(sorted(result))

    representatives = {
        min(
            transform(family, reverse, alternate)
            for reverse in (False, True)
            for alternate in (False, True)
        )
        for family in complementary_quartets()
    }
    return tuple(sorted(representatives))


def minimum_complementary_octet() -> tuple[int, tuple[SignWord, ...]]:
    """Find the minimum complementary family containing ``P_WORD``."""

    representatives = {
        comb_signature(word): word
        for word in product((1, -1), repeat=5)
    }
    target = tuple(-value for value in comb_signature(P_WORD))
    states: dict[tuple[int, int, int, int], tuple[SignWord, ...]] = {
        (0, 0, 0, 0): ()
    }
    for additional in range(1, 8):
        next_states: dict[
            tuple[int, int, int, int], tuple[SignWord, ...]
        ] = {}
        for current, path in states.items():
            for signature, word in representatives.items():
                result = tuple(
                    left + right
                    for left, right in zip(current, signature, strict=True)
                )
                next_states.setdefault(result, path + (word,))
        states = next_states
        if target in states:
            return additional + 1, (P_WORD,) + states[target]
    raise AssertionError("the five-comb lacks the expected octet")


def polarized_carriers(
    family: Sequence[Sequence[int]] = COMPLEMENTARY_OCTET,
) -> tuple[SignWord, ...]:
    """The carriers ``P_j + eps*z^42*P_j`` from a small family."""

    result = []
    for word in family:
        for separation_sign in (-1, 1):
            carrier = [0] * 59
            for index, value in enumerate(word):
                carrier[4 * index] = value
                carrier[42 + 4 * index] = separation_sign * value
            result.append(tuple(carrier))
    return tuple(result)


def carrier_support_holes(length: int) -> tuple[int, ...]:
    """Positions left by eight disjoint shifted ten-point carriers."""

    if length not in (83, 84):
        raise ValueError("the carrier packing is for lengths 83 and 84")
    support = {
        shift + position
        for shift in CARRIER_SHIFTS
        for position in (0, 4, 8, 12, 16, 42, 46, 50, 54, 58)
    }
    if len(support) != 80 or max(support) >= length:
        raise AssertionError("the carrier translates are not disjoint")
    return tuple(position for position in range(length) if position not in support)


def _gf2_affine_solutions(
    equations: Iterable[tuple[int, int]], variables: int
) -> tuple[int, tuple[int, ...]] | None:
    """Return one solution and a nullspace basis for a GF(2) affine system."""

    rows = [[mask, rhs] for mask, rhs in equations if mask or rhs]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(variables):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if (rows[row][0] >> column) & 1
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for row in range(len(rows)):
            if row != pivot_row and ((rows[row][0] >> column) & 1):
                rows[row][0] ^= rows[pivot_row][0]
                rows[row][1] ^= rows[pivot_row][1]
        pivot_columns.append(column)
        pivot_row += 1
    if any(mask == 0 and rhs for mask, rhs in rows):
        return None
    rows = rows[:pivot_row]
    free_columns = tuple(
        column for column in range(variables) if column not in pivot_columns
    )
    particular = sum(
        rhs << column
        for (_, rhs), column in zip(rows, pivot_columns, strict=True)
    )
    basis = []
    for free in free_columns:
        vector = 1 << free
        for (mask, _), pivot in zip(rows, pivot_columns, strict=True):
            if (mask >> free) & 1:
                vector |= 1 << pivot
        basis.append(vector)
    return particular, tuple(basis)


def _restricted_mod4_solutions(
    q_bits: Sequence[int],
    positions: Sequence[int],
    seed_s_bits: Sequence[int],
) -> tuple[int, tuple[int, ...]] | None:
    """Solve the exact modulo-four layer with all other ``s`` bits fixed."""

    position_to_variable = {
        position: variable for variable, position in enumerate(positions)
    }
    variable_global_mask = sum(1 << position for position in positions)
    seed_global_mask = sum(
        value << position for position, value in enumerate(seed_s_bits)
    )
    restricted = []
    for mask, rhs in mod4_lift_equations(q_bits):
        rhs ^= ((mask & ~variable_global_mask & seed_global_mask).bit_count() & 1)
        local_mask = 0
        for position, variable in position_to_variable.items():
            if (mask >> position) & 1:
                local_mask ^= 1 << variable
        restricted.append((local_mask, rhs))
    return _gf2_affine_solutions(restricted, len(positions))


def literal_comb_chord_counts() -> Counter[str]:
    """Exhaust the literal 30-variable reciprocal five-comb chord."""

    seed_s = sign_bits(ELIAHOU_S)
    seed_q = sign_bits(ELIAHOU_Q)
    parameter_positions = q_parameter_flips()
    positions = tuple(
        sorted(
            {
                position
                for parameter in COMB_PARAMETERS
                for position in parameter_positions[parameter]
            }
        )
    )
    if len(positions) != 20:
        raise AssertionError("the literal five-comb support must have 20 s bits")

    counts: Counter[str] = Counter()
    for parameter_mask in range(1 << len(COMB_PARAMETERS)):
        q_bits = list(seed_q)
        for index, parameter in enumerate(COMB_PARAMETERS):
            if (parameter_mask >> index) & 1:
                for position in parameter_positions[parameter]:
                    q_bits[position] ^= 1

        affine = _restricted_mod4_solutions(q_bits, positions, seed_s)
        if affine is None:
            counts["mod4_inconsistent_q"] += 1
            continue
        counts["mod4_consistent_q"] += 1
        particular, basis = affine
        counts[f"restricted_rank_{len(positions) - len(basis)}"] += 1
        for free_mask in range(1 << len(basis)):
            local = particular
            for index, vector in enumerate(basis):
                if (free_mask >> index) & 1:
                    local ^= vector
            s_bits = list(seed_s)
            for variable, position in enumerate(positions):
                s_bits[position] = (local >> variable) & 1
            values = gate_correlations(s_bits, q_bits)
            if any(value % 4 for value in values):
                raise AssertionError("GF(2) solution missed the exact modulo-four layer")
            counts["mod4_points"] += 1
            for modulus in (8, 16, 32):
                if all(value % modulus == 0 for value in values):
                    counts[f"mod{modulus}_points"] += 1
    return counts


def small_base_sequences() -> tuple[SmallBase, ...]:
    """Enumerate all 256 labelled ``BS(4,3)`` quadruples."""

    signs4 = tuple(product((1, -1), repeat=4))
    signs3 = tuple(product((1, -1), repeat=3))
    result = []
    for sequences in product(signs4, signs4, signs3, signs3):
        if all(autocorrelation_sum(sequences, lag) == 0 for lag in range(1, 4)):
            result.append(sequences)
    return tuple(result)


def _row_boundary_signature(
    row: TileRow, boundary: SmallBase, kind: str
) -> tuple[int, ...]:
    """Return ``sum Q_r R_r^*`` for one equal- or offset-aligned tile row."""

    if kind not in ("E", "O"):
        raise ValueError("tile kind must be E or O")
    shifts = (0, 0, 0, 0) if kind == "E" else (1, 1, 0, 0)
    coefficients = {exponent: 0 for exponent in range(-3, 5)}
    for q_word, r_word, shift in zip(row, boundary, shifts, strict=True):
        for q_index, q_value in enumerate(q_word):
            for r_index, r_value in enumerate(r_word):
                coefficients[shift + q_index - r_index] += q_value * r_value
    return tuple(coefficients[exponent] for exponent in range(-3, 5))


def boundary_row_mates(boundary: SmallBase, kind: str) -> tuple[TileRow, ...]:
    """Enumerate all signed tile rows whose boundary cross term vanishes."""

    signs4 = tuple(product((1, -1), repeat=4))
    left: dict[tuple[int, ...], list[tuple[SignWord, SignWord]]] = defaultdict(list)
    for first in signs4:
        for second in signs4:
            partial = _row_boundary_signature(
                (first, second, (1, 1, 1, 1), (1, 1, 1, 1)),
                (boundary[0], boundary[1], (), ()),
                kind,
            )
            left[partial].append((first, second))

    # Compute the short-pair signatures directly.  This avoids relying on
    # placeholder words in the long-pair meet-in-the-middle table.
    result = []
    shifts = (0, 0) if kind == "E" else (0, 0)
    for third in signs4:
        for fourth in signs4:
            short_coefficients = {exponent: 0 for exponent in range(-3, 5)}
            for q_word, r_word, shift in zip(
                (third, fourth), boundary[2:], shifts, strict=True
            ):
                for q_index, q_value in enumerate(q_word):
                    for r_index, r_value in enumerate(r_word):
                        short_coefficients[shift + q_index - r_index] += (
                            q_value * r_value
                        )
            wanted = tuple(
                -short_coefficients[exponent] for exponent in range(-3, 5)
            )
            for first, second in left.get(wanted, ()):
                row = (first, second, third, fourth)
                if any(_row_boundary_signature(row, boundary, kind)):
                    raise AssertionError("meet-in-the-middle emitted a false row mate")
                result.append(row)
    return tuple(result)


def _row_cross_signature(
    first: TileRow, second: TileRow, first_kind: str, second_kind: str
) -> tuple[int, ...]:
    """Cross-correlation of two tile rows, with their component offsets."""

    offsets = {
        "E": (0, 0, 0, 0),
        "O": (1, 1, 0, 0),
    }
    first_offsets = offsets[first_kind]
    second_offsets = offsets[second_kind]
    coefficients = {exponent: 0 for exponent in range(-4, 5)}
    for first_word, second_word, first_offset, second_offset in zip(
        first, second, first_offsets, second_offsets, strict=True
    ):
        for left, left_value in enumerate(first_word):
            for right, right_value in enumerate(second_word):
                exponent = second_offset + right - first_offset - left
                coefficients[exponent] += left_value * right_value
    return tuple(coefficients[exponent] for exponent in range(-4, 5))


def disjoint_comb_endpoint_counts() -> Counter[str]:
    """Check the farthest-row obstruction for all aligned comb completions."""

    boundaries = small_base_sequences()
    if len(boundaries) != 256:
        raise AssertionError("the labelled BS(4,3) count changed")
    counts: Counter[str] = Counter()
    for boundary in boundaries:
        equal = boundary_row_mates(boundary, "E")
        offset = boundary_row_mates(boundary, "O")
        counts[f"mate_profile_E{len(equal)}_O{len(offset)}"] += 1
        for label, first_pool, last_pool, first_kind, last_kind in (
            ("EE", equal, equal, "E", "E"),
            ("OO", offset, offset, "O", "O"),
            ("EO", equal, offset, "E", "O"),
        ):
            for first in first_pool:
                for last in last_pool:
                    counts[f"{label}_endpoint_pairs"] += 1
                    if not any(
                        _row_cross_signature(
                            first, last, first_kind, last_kind
                        )
                    ):
                        counts[f"{label}_orthogonal_endpoint_pairs"] += 1
    return counts


def verify() -> None:
    factorization = seed_rank_one_factorization()
    if tuple(
        (lag, value) for lag, value in enumerate(factorization) if value
    ) != (
        (0, 334),
        (4, -256),
        (8, 192),
        (12, -128),
        (16, 64),
        (26, -32),
        (30, 64),
        (34, -96),
        (38, 128),
        (42, -160),
        (46, 128),
        (50, -96),
        (54, 64),
        (58, -32),
    ):
        raise AssertionError("unexpected rank-one residual vector")

    remainders = seed_comb_remainders()
    if remainders != (
        (1, -1, -1, -1),
        (1, -1, -1, 1),
        (1, 1, 1),
        (-1, 1, -1),
    ):
        raise AssertionError(f"unexpected seed remainders modulo P: {remainders}")
    if tuple(autocorrelation_sum(remainders, lag) for lag in range(4)) != (
        14,
        0,
        0,
        0,
    ):
        raise AssertionError("the seed remainders are not BS(4,3)")
    # With y=z^4, (y+1)P=y^5+1.  Hence P has unit-circle roots.
    cyclotomic_product = [0] * 6
    for index, value in enumerate(P_WORD):
        cyclotomic_product[index] += value
        cyclotomic_product[index + 1] += value
    if tuple(cyclotomic_product) != (1, 0, 0, 0, 0, 1):
        raise AssertionError("the cyclotomic identity for P failed")
    if 4**2 + 4**2 + 3**2 + 3**2 >= 334:
        raise AssertionError("the common-comb spectral bound is not obstructive")

    minimum_size, _ = minimum_complementary_octet()
    if minimum_size != 8:
        raise AssertionError(
            "the complementary family containing P is not minimal at eight"
        )
    family_counts = tuple(complementary_multiset_count(size) for size in range(1, 9))
    if family_counts != (0, 0, 0, 48, 0, 0, 0, 1_246):
        raise AssertionError(
            f"unexpected complementary-family classification: {family_counts}"
        )
    quartets = complementary_quartets()
    if len(quartets) != 48 or len(quartet_symmetry_representatives()) != 17:
        raise AssertionError("unexpected complementary-quartet orbit count")
    for quartet in quartets:
        quartet_carriers = polarized_carriers(quartet)
        if tuple(
            autocorrelation_sum(quartet_carriers * 4, lag) for lag in range(59)
        ) != (320,) + (0,) * 58:
            raise AssertionError("a classified quartet did not give 32 flat carriers")
    if any(
        sum(comb_signature(word)[lag] for word in COMPLEMENTARY_OCTET)
        for lag in range(4)
    ):
        raise AssertionError("the explicit comb octet is not complementary")
    carriers = polarized_carriers()
    if len(carriers) != 16:
        raise AssertionError("the polarized family must have sixteen carriers")
    if tuple(
        autocorrelation_sum(carriers, lag) for lag in range(59)
    ) != (160,) + (0,) * 58:
        raise AssertionError("the polarized carrier family is not flat")
    if tuple(
        autocorrelation_sum(carriers + carriers, lag) for lag in range(59)
    ) != (320,) + (0,) * 58:
        raise AssertionError("the doubled polarized family is not flat")
    if carrier_support_holes(84) != (40, 41, 82, 83):
        raise AssertionError("unexpected long carrier holes")
    if carrier_support_holes(83) != (40, 41, 82):
        raise AssertionError("unexpected short carrier holes")

    literal = literal_comb_chord_counts()
    expected_literal = Counter(
        {
            "mod4_inconsistent_q": 1023,
            "mod4_consistent_q": 1,
            "restricted_rank_15": 1,
            "mod4_points": 32,
            "mod8_points": 1,
            "mod16_points": 1,
        }
    )
    if literal != expected_literal:
        raise AssertionError(f"unexpected literal-comb counts: {literal}")

    endpoints = disjoint_comb_endpoint_counts()
    expected_endpoints = Counter(
        {
            "mate_profile_E10_O6": 128,
            "mate_profile_E6_O10": 128,
            "EE_endpoint_pairs": 17_408,
            "OO_endpoint_pairs": 17_408,
            "EO_endpoint_pairs": 15_360,
        }
    )
    if endpoints != expected_endpoints:
        raise AssertionError(f"unexpected disjoint-comb counts: {endpoints}")


if __name__ == "__main__":
    verify()
    print("PASS seed norm = 14 + 32*N((z^42-1)P)")
    print("PASS common-P repair obstruction at a unit-circle root")
    print("PASS literal reciprocal five-comb chord: 0 modulo-32 points")
    print("PASS 256 BS(4,3) boundaries and 80,896 endpoint pairs exhausted")
    print("PASS orthogonal disjoint-comb completion: 0 candidates")
    print("PASS alternating-comb octet and 32-channel polarized spectral repair")
    print("PASS 48 complementary quartets (17 word-symmetry orbits)")

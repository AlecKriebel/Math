#!/usr/bin/env python3
"""Dependency-free verifier for generalized five-comb paired lobes.

The original five-comb construction uses eight carriers

    C_i(z) = P_i(z^4) (1 + epsilon_i z^42).

Its self-correlation is flat exactly when the four words with each value of
``epsilon`` form complementary quartets.  A strictly larger construction
pairs two possibly different words:

    D_{j,epsilon}(z) = P_j(z^4) + epsilon z^42 Q_j(z^4),
    j = 1,...,4, epsilon in {-1,+1}.

Adding the two polarities cancels every P/Q cross term.  The eight resulting
carriers therefore have flat self-correlation exactly when the combined
multiset of the four P words and four Q words is a complementary octet.

This program verifies those identities directly, exhaustively classifies the
normalized length-five word inventories, and independently reconstructs the
word-independent modulo-four projective quotient.  It uses only the Python
standard library and exact integer arithmetic.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations_with_replacement, product
from math import factorial, prod
from typing import Iterable, Iterator, Sequence


Word = tuple[int, ...]
Signature = tuple[int, int, int, int]
IndexMultiset = tuple[int, ...]

WORDS: tuple[Word, ...] = tuple(
    (1,) + tail for tail in product((-1, 1), repeat=4)
)

LENGTHS = (84, 84, 83, 83)
SHIFTS = (0, 1, 2, 3, 20, 21, 22, 23)
HOLES = (
    (40, 41, 82, 83),
    (40, 41, 82, 83),
    (40, 41, 82),
    (40, 41, 82),
)
HOLE_POSITIONS = tuple(
    (row, position)
    for row, positions in enumerate(HOLES)
    for position in positions
)

H4 = (
    (1, 1, 1, 1),
    (1, -1, 1, -1),
    (1, 1, -1, -1),
    (1, -1, -1, 1),
)
MUB_TWIST = (1, 1, 1, -1)
VECTORS = tuple(
    tuple(
        H4[row][column] * (MUB_TWIST[row] if basis else 1)
        for row in range(4)
    )
    for basis in range(2)
    for column in range(4)
)

EXPECTED_OCTET_SHA256 = (
    "81b45bd47e3b12f9a0bc27e3ce31e4ac1db713e70f344c628398f63f40213fbc"
)
EXPECTED_PROFILE_SHA256 = (
    "d05912cf1df6dcc2f2ed5ddbb0b87d6d6eff30f6c4d1c7ec90a2e5eadbe30b5e"
)
EXPECTED_DECOMPOSABLE_SHA256 = (
    "ea0e821fae89c3c116a3f7339aacb8792fdf7063dd102ec3dee917cb1848c4d3"
)
EXPECTED_DIRECTED_PAIR_SHA256 = (
    "32b52c913aab1ac7185d929b88f7527e92be558365bd33102744e7223c4e1230"
)
EXPECTED_RREF_SHA256 = (
    "3034b63324239048f856d8abcd07770d40e65cc15e0aa8c1a54fe8a5e490690a"
)
EXPECTED_MOD4_SHA256 = (
    "2d6a0a97180cdcee2b68168aeff49ae00696da4fcd758641532ac28325cb83f0"
)


def aperiodic_cross(
    left: Sequence[int], right: Sequence[int], lag: int
) -> int:
    """Coefficient at a nonnegative lag in ``left * right^*``."""

    if lag < 0:
        return aperiodic_cross(right, left, -lag)
    return sum(
        left[index + lag] * right[index]
        for index in range(min(len(right), len(left) - lag))
    )


def positive_norm(sequence: Sequence[int]) -> tuple[int, ...]:
    """Return all nonnegative aperiodic autocorrelation coefficients."""

    return tuple(
        aperiodic_cross(sequence, sequence, lag)
        for lag in range(len(sequence))
    )


def word_signature(word: Sequence[int]) -> Signature:
    """Return the four positive autocorrelations of a length-five word."""

    if len(word) != 5 or any(value not in (-1, 1) for value in word):
        raise ValueError("a binary word of length five is required")
    return tuple(
        aperiodic_cross(word, word, lag) for lag in range(1, 5)
    )  # type: ignore[return-value]


SIGNATURES: tuple[Signature, ...] = tuple(map(word_signature, WORDS))


def signature_sum(indices: Iterable[int]) -> Signature:
    """Sum the four word signatures indexed by ``indices``."""

    total = [0, 0, 0, 0]
    for index in indices:
        for lag, value in enumerate(SIGNATURES[index]):
            total[lag] += value
    return tuple(total)  # type: ignore[return-value]


def is_complementary(indices: Iterable[int]) -> bool:
    return signature_sum(indices) == (0, 0, 0, 0)


def normalized_reverse(word: Sequence[int]) -> Word:
    """Reverse a normalized word and restore its first coordinate to +1."""

    changed = tuple(reversed(word))
    return tuple(changed[0] * value for value in changed)


def normalized_alternation(word: Sequence[int]) -> Word:
    """Multiply tooth ``t`` by ``(-1)^t``."""

    return tuple(value * (-1) ** tooth for tooth, value in enumerate(word))


def verify_signature_fibers() -> tuple[int, int, int]:
    """Verify the exact reversal fibers of the ten signatures."""

    word_index = {word: index for index, word in enumerate(WORDS)}
    reversal = tuple(
        word_index[normalized_reverse(word)] for word in WORDS
    )
    fibers: defaultdict[Signature, list[int]] = defaultdict(list)
    for index, signature in enumerate(SIGNATURES):
        fibers[signature].append(index)

    if len(fibers) != 10:
        raise AssertionError("the number of word signatures changed")
    for indices in fibers.values():
        expected = {indices[0], reversal[indices[0]]}
        if set(indices) != expected:
            raise AssertionError(
                "a signature fiber is not exactly one reversal orbit"
            )
    paired = sum(len(indices) == 2 for indices in fibers.values())
    fixed = sum(len(indices) == 1 for indices in fibers.values())
    if (paired, fixed) != (6, 4):
        raise AssertionError("the reversal-fiber distribution changed")
    for word, signature in zip(WORDS, SIGNATURES, strict=True):
        alternated = word_signature(normalized_alternation(word))
        expected = (
            -signature[0],
            signature[1],
            -signature[2],
            signature[3],
        )
        if alternated != expected:
            raise AssertionError("the common-alternation signature law failed")
    return len(fibers), paired, fixed


def complementary_multisets(size: int) -> tuple[IndexMultiset, ...]:
    """Enumerate complementary normalized word multisets of fixed size."""

    return tuple(
        indices
        for indices in combinations_with_replacement(range(len(WORDS)), size)
        if is_complementary(indices)
    )


def comma_record_hash(rows: Iterable[Sequence[int]]) -> str:
    """Hash comma-separated integer records, each terminated by LF."""

    digest = sha256()
    for row in rows:
        digest.update((",".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def profile_hash(profiles: Iterable[Sequence[Signature]]) -> str:
    """Hash profiles with commas within signatures and semicolons between."""

    digest = sha256()
    for profile in profiles:
        record = ";".join(
            ",".join(map(str, signature)) for signature in profile
        )
        digest.update((record + "\n").encode())
    return digest.hexdigest()


def dilated_word(word: Sequence[int]) -> tuple[int, ...]:
    """Return ``P(z^4)`` for a length-five coefficient word."""

    result = [0] * 17
    for tooth, value in enumerate(word):
        result[4 * tooth] = value
    return tuple(result)


def paired_carrier(
    first: Sequence[int], second: Sequence[int], epsilon: int
) -> tuple[int, ...]:
    """Return ``P(z^4) + epsilon*z^42*Q(z^4)``."""

    if epsilon not in (-1, 1):
        raise ValueError("epsilon must be a sign")
    result = [0] * 59
    for tooth in range(5):
        result[4 * tooth] = first[tooth]
        result[42 + 4 * tooth] = epsilon * second[tooth]
    return tuple(result)


def padded_dilated_norm(word: Sequence[int]) -> tuple[int, ...]:
    """Autocorrelation of ``P(z^4)``, padded to carrier lag 58."""

    result = [0] * 59
    norm = positive_norm(dilated_word(word))
    result[: len(norm)] = norm
    return tuple(result)


def add_vectors(*vectors: Sequence[int]) -> tuple[int, ...]:
    if not vectors:
        return ()
    if any(len(vector) != len(vectors[0]) for vector in vectors):
        raise ValueError("vectors must have one common length")
    return tuple(sum(values) for values in zip(*vectors, strict=True))


def verify_paired_norm_identity() -> None:
    """Verify cancellation of distinct-lobe cross terms for all 256 pairs."""

    dilated_norms = tuple(map(padded_dilated_norm, WORDS))
    for first in range(16):
        for second in range(16):
            observed = add_vectors(
                positive_norm(paired_carrier(WORDS[first], WORDS[second], 1)),
                positive_norm(
                    paired_carrier(WORDS[first], WORDS[second], -1)
                ),
            )
            expected = tuple(
                2 * (left + right)
                for left, right in zip(
                    dilated_norms[first],
                    dilated_norms[second],
                    strict=True,
                )
            )
            if observed != expected:
                raise AssertionError(
                    f"paired-lobe identity failed for words {first},{second}"
                )


def verify_same_word_theorem(
    quartets: Sequence[IndexMultiset],
) -> int:
    """Verify all 48^2 same-word polarized quartet inventories."""

    # The base and cross shells have disjoint positive-lag supports.  The
    # lag-42 coefficient of one carrier is 5*epsilon, forcing four carriers
    # of each polarity.  The remaining shell equations say that the two
    # four-word autocorrelation sums are equal; the base equations say their
    # sum is zero.  Thus both polarity classes are complementary quartets.
    base_support = {4, 8, 12, 16}
    cross_support = {42 + 4 * delta for delta in range(-4, 5)}
    if base_support & cross_support:
        raise AssertionError("the base and cross supports should be disjoint")
    if len(quartets) != 48:
        raise AssertionError("the complementary-quartet count changed")

    # Mechanically check the "only if" reduction on every attainable
    # four-word signature sum.  Once lag 42 forces a 4+4 polarity split,
    # flatness is equivalent to both the sum and difference of the two
    # polarity-class signatures vanishing.
    if [
        positive_count
        for positive_count in range(9)
        if 5 * (positive_count - (8 - positive_count)) == 0
    ] != [4]:
        raise AssertionError("lag 42 did not force a four-plus-four split")
    four_word_sums = {
        signature_sum(indices)
        for indices in combinations_with_replacement(range(16), 4)
    }
    for negative_signature in four_word_sums:
        for positive_signature in four_word_sums:
            flat_equations = all(
                negative_signature[lag] + positive_signature[lag] == 0
                and positive_signature[lag] - negative_signature[lag] == 0
                for lag in range(4)
            )
            separate_quartets = (
                negative_signature == (0, 0, 0, 0)
                and positive_signature == (0, 0, 0, 0)
            )
            if flat_equations != separate_quartets:
                raise AssertionError(
                    "the same-word flatness equivalence failed"
                )

    group_norms: dict[int, tuple[tuple[int, ...], ...]] = {}
    for epsilon in (-1, 1):
        group_norms[epsilon] = tuple(
            add_vectors(
                *(
                    positive_norm(
                        paired_carrier(WORDS[index], WORDS[index], epsilon)
                    )
                    for index in quartet
                )
            )
            for quartet in quartets
        )

    flat = (80,) + (0,) * 58
    count = 0
    for negative in range(len(quartets)):
        for positive in range(len(quartets)):
            observed = add_vectors(
                group_norms[-1][negative], group_norms[1][positive]
            )
            if observed != flat:
                raise AssertionError(
                    "a polarized pair of complementary quartets is not flat"
                )
            count += 1
    if count != 48**2:
        raise AssertionError("the same-word inventory count changed")
    return count


def classify_octets(
    quartets: Sequence[IndexMultiset],
) -> tuple[
    tuple[IndexMultiset, ...],
    tuple[tuple[Signature, ...], ...],
    frozenset[IndexMultiset],
    dict[str, int],
]:
    """Classify complementary octets and their abstract self profiles."""

    octets = complementary_multisets(8)
    if len(octets) != 1_246:
        raise AssertionError("the complementary-octet count changed")
    if comma_record_hash(octets) != EXPECTED_OCTET_SHA256:
        raise AssertionError("the complementary-octet digest changed")

    profiles = tuple(
        sorted(
            {
                tuple(sorted(SIGNATURES[index] for index in octet))
                for octet in octets
            }
        )
    )
    if len(profiles) != 35:
        raise AssertionError("the octet signature-profile count changed")
    if profile_hash(profiles) != EXPECTED_PROFILE_SHA256:
        raise AssertionError("the octet signature-profile digest changed")

    decomposable = frozenset(
        tuple(sorted(left + right))
        for index, left in enumerate(quartets)
        for right in quartets[index:]
    )
    if len(decomposable) != 689:
        raise AssertionError("the decomposable-octet count changed")
    if not decomposable <= frozenset(octets):
        raise AssertionError("a union of two quartets is not an octet")
    if (
        comma_record_hash(sorted(decomposable))
        != EXPECTED_DECOMPOSABLE_SHA256
    ):
        raise AssertionError("the decomposable-octet digest changed")

    decomposable_profiles = {
        tuple(sorted(SIGNATURES[index] for index in octet))
        for octet in decomposable
    }
    if (len(decomposable_profiles), len(profiles) - len(decomposable_profiles)) != (
        14,
        21,
    ):
        raise AssertionError("the decomposable-profile split changed")

    def alternate_signature(signature: Signature) -> Signature:
        return (
            -signature[0],
            signature[1],
            -signature[2],
            signature[3],
        )

    profile_set = set(profiles)
    alternation = {
        profile: tuple(
            sorted(alternate_signature(signature) for signature in profile)
        )
        for profile in profiles
    }
    if set(alternation.values()) != profile_set:
        raise AssertionError("common alternation does not preserve profiles")
    fixed = sum(alternation[profile] == profile for profile in profiles)
    orbits = {
        min(profile, alternation[profile]) for profile in profiles
    }
    if (len(orbits), fixed, (len(profiles) - fixed) // 2) != (22, 9, 13):
        raise AssertionError("the common-alternation profile orbits changed")

    return (
        octets,
        profiles,
        decomposable,
        {
            "decomposable_profiles": len(decomposable_profiles),
            "genuinely_new_profiles": len(profiles)
            - len(decomposable_profiles),
            "alternation_orbits": len(orbits),
            "alternation_fixed": fixed,
            "alternation_pairs": (len(profiles) - fixed) // 2,
        },
    )


def valid_directed_pair_inventories() -> Iterator[tuple[int, int, int, int]]:
    """Yield all self-cancelling four-pair inventories in lexicographic order.

    Pair code ``16*P+Q`` represents the directed normalized word pair
    ``(P,Q)``.  A two-pair meet-in-the-middle signature index makes the
    768,512-state enumeration small while preserving exact lexicographic
    output order.
    """

    pair_signatures = tuple(
        tuple(
            SIGNATURES[first][lag] + SIGNATURES[second][lag]
            for lag in range(4)
        )
        for first in range(16)
        for second in range(16)
    )
    codes_by_signature: defaultdict[Signature, list[int]] = defaultdict(list)
    for code, signature in enumerate(pair_signatures):
        codes_by_signature[signature].append(code)

    for first in range(256):
        first_signature = pair_signatures[first]
        for second in range(first, 256):
            second_signature = pair_signatures[second]
            remaining = tuple(
                -first_signature[lag] - second_signature[lag]
                for lag in range(4)
            )
            for third in range(second, 256):
                third_signature = pair_signatures[third]
                target = tuple(
                    remaining[lag] - third_signature[lag]
                    for lag in range(4)
                )
                for fourth in codes_by_signature.get(target, ()):
                    if fourth >= third:
                        yield first, second, third, fourth


def classify_directed_pair_inventories(
    octets: Sequence[IndexMultiset],
) -> dict[str, object]:
    """Verify the complete 256-pair, four-multiset classification."""

    octet_set = frozenset(octets)
    digest = sha256()
    count = 0
    both_sides_quartets = 0
    diagonal = 0
    ordered_count = 0
    multiplicity_shapes: Counter[tuple[int, ...]] = Counter()
    endpoint_split: Counter[tuple[int, int]] = Counter()

    for inventory in valid_directed_pair_inventories():
        digest.update((",".join(map(str, inventory)) + "\n").encode())
        count += 1

        multiplicities = Counter(inventory)
        shape = tuple(sorted(multiplicities.values(), reverse=True))
        multiplicity_shapes[shape] += 1
        ordered_count += factorial(4) // prod(
            factorial(value) for value in multiplicities.values()
        )

        first_words = tuple(code // 16 for code in inventory)
        second_words = tuple(code % 16 for code in inventory)
        combined = tuple(sorted(first_words + second_words))
        if combined not in octet_set:
            raise AssertionError(
                "a directed-pair inventory is not a complementary octet"
            )
        first_flat = is_complementary(first_words)
        second_flat = is_complementary(second_words)
        both_sides_quartets += int(first_flat and second_flat)
        diagonal += int(
            all(code // 16 == code % 16 for code in inventory)
        )
        endpoint_split[
            (
                sum(WORDS[index][-1] > 0 for index in first_words),
                sum(WORDS[index][-1] > 0 for index in second_words),
            )
        ] += 1

    if count != 768_512:
        raise AssertionError("the directed-pair inventory count changed")
    if digest.hexdigest() != EXPECTED_DIRECTED_PAIR_SHA256:
        raise AssertionError("the directed-pair inventory digest changed")
    if (both_sides_quartets, count - both_sides_quartets, diagonal) != (
        46_528,
        721_984,
        48,
    ):
        raise AssertionError("the directed-pair quartet split changed")
    if ordered_count != 18_264_960:
        raise AssertionError("the ordered directed-pair count changed")
    if multiplicity_shapes != Counter(
        {
            (1, 1, 1, 1): 753_832,
            (2, 1, 1): 14_152,
            (2, 2): 528,
        }
    ):
        raise AssertionError("the directed-pair multiplicities changed")
    if endpoint_split != Counter(
        {
            (0, 4): 11_398,
            (1, 3): 175_968,
            (2, 2): 393_780,
            (3, 1): 175_968,
            (4, 0): 11_398,
        }
    ):
        raise AssertionError("the endpoint-sign split changed")

    return {
        "count": count,
        "both_sides_quartets": both_sides_quartets,
        "genuinely_distinct_lobe": count - both_sides_quartets,
        "diagonal": diagonal,
        "ordered_count": ordered_count,
        "multiplicity_shapes": multiplicity_shapes,
        "endpoint_split": endpoint_split,
        "sha256": digest.hexdigest(),
    }


def parity(value: int) -> int:
    return value.bit_count() & 1


def position_incidence(row: int, position: int) -> int:
    """Return the 83-bit modulo-four effect of toggling one entry."""

    length = LENGTHS[row]
    return sum(
        (
            ((position + lag < length) ^ (position >= lag))
            << (lag - 1)
        )
        for lag in range(1, 84)
    )


def xor_basis(vectors: Iterable[int]) -> dict[int, int]:
    """Construct a high-pivot GF(2) basis."""

    basis: dict[int, int] = {}
    for original in vectors:
        vector = original
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in basis:
                vector ^= basis[pivot]
            else:
                basis[pivot] = vector
                break
    return basis


HOLE_BASIS = xor_basis(
    position_incidence(row, position)
    for row, position in HOLE_POSITIONS
)


def quotient(vector: int) -> int:
    """Reduce an 83-bit syndrome modulo the fourteen-hole span."""

    for pivot in sorted(HOLE_BASIS, reverse=True):
        if (vector >> pivot) & 1:
            vector ^= HOLE_BASIS[pivot]
    return vector


POSITION_QUOTIENTS = {
    (row, position): quotient(position_incidence(row, position))
    for row, length in enumerate(LENGTHS)
    for position in range(length)
}
MOD4_TARGET = quotient((1 << 83) - 1)


def projective_slot_syndrome(slot: int, label: int) -> int:
    """Reference quotient contribution with both scalar words all positive."""

    shift = SHIFTS[slot]
    result = 0
    for row in range(4):
        if VECTORS[label][row] < 0:
            for tooth in range(5):
                result ^= POSITION_QUOTIENTS[(row, shift + 4 * tooth)]
                result ^= POSITION_QUOTIENTS[
                    (row, shift + 42 + 4 * tooth)
                ]
    return result


PROJECTIVE_SLOT_STATES = tuple(
    tuple(projective_slot_syndrome(slot, label) for label in range(8))
    for slot in range(8)
)


def gf2_rref(
    equations: Iterable[tuple[int, int]], width: int
) -> tuple[tuple[int, int], ...]:
    """Return a reduced GF(2) system as ``(coefficient_mask, rhs)`` rows."""

    rows = [
        mask | ((right_hand_side & 1) << width)
        for mask, right_hand_side in equations
    ]
    rank = 0
    for column in range(width):
        pivot = next(
            (
                index
                for index in range(rank, len(rows))
                if (rows[index] >> column) & 1
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(len(rows)):
            if index != rank and (rows[index] >> column) & 1:
                rows[index] ^= rows[rank]
        rank += 1

    mask_limit = (1 << width) - 1
    if any(
        not (row & mask_limit) and ((row >> width) & 1)
        for row in rows
    ):
        raise AssertionError("an inconsistent GF(2) equation was derived")
    reduced = tuple(
        (row & mask_limit, (row >> width) & 1)
        for row in rows
        if row & mask_limit
    )
    if len(reduced) != rank or len({mask for mask, _rhs in reduced}) != rank:
        raise AssertionError("the reduced system contains duplicate rows")
    return reduced


def derive_projective_rref() -> tuple[tuple[tuple[int, ...], int], ...]:
    """Derive the exact affine equations on the 24 projective-label bits."""

    width = 24
    for slot, states in enumerate(PROJECTIVE_SLOT_STATES):
        for label in range(8):
            recovered = states[0]
            for bit in range(3):
                if (label >> bit) & 1:
                    recovered ^= states[1 << bit] ^ states[0]
            if recovered != states[label]:
                raise AssertionError(
                    f"slot {slot} is not affine in its three label bits"
                )

    baseline = MOD4_TARGET
    for states in PROJECTIVE_SLOT_STATES:
        baseline ^= states[0]

    raw_equations: list[tuple[int, int]] = []
    for quotient_bit in range(83):
        coefficients = 0
        for slot, states in enumerate(PROJECTIVE_SLOT_STATES):
            for bit in range(3):
                delta = states[1 << bit] ^ states[0]
                if (delta >> quotient_bit) & 1:
                    coefficients ^= 1 << (3 * slot + bit)
        right_hand_side = (baseline >> quotient_bit) & 1
        if coefficients:
            raw_equations.append((coefficients, right_hand_side))
        elif right_hand_side:
            raise AssertionError("the projective quotient is inconsistent")

    return tuple(
        (
            tuple(
                variable
                for variable in range(width)
                if (mask >> variable) & 1
            ),
            right_hand_side,
        )
        for mask, right_hand_side in gf2_rref(raw_equations, width)
    )


def rref_hash(
    equations: Iterable[tuple[Sequence[int], int]],
) -> str:
    digest = sha256()
    for variables, right_hand_side in equations:
        digest.update(
            (
                ",".join(map(str, variables))
                + "="
                + str(right_hand_side)
                + "\n"
            ).encode()
        )
    return digest.hexdigest()


def enumerate_normalized_labelings(
    rref: Sequence[tuple[Sequence[int], int]],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate all solutions after fixing the first label to zero."""

    width = 24
    equations = [
        (sum(1 << variable for variable in variables), right_hand_side)
        for variables, right_hand_side in rref
    ]
    equations.extend((1 << bit, 0) for bit in range(3))
    normalized_rref = gf2_rref(equations, width)
    # The pivot is the least set bit because elimination scans columns upward.
    pivots = tuple(
        (mask & -mask).bit_length() - 1
        for mask, _right_hand_side in normalized_rref
    )
    if len(set(pivots)) != len(pivots):
        raise AssertionError("normalized RREF pivots are not unique")
    free = tuple(
        variable for variable in range(width) if variable not in pivots
    )

    solutions = []
    for assignment in range(1 << len(free)):
        bits = 0
        for index, variable in enumerate(free):
            if (assignment >> index) & 1:
                bits |= 1 << variable
        for (mask, right_hand_side), pivot in zip(
            normalized_rref, pivots, strict=True
        ):
            without_pivot = mask ^ (1 << pivot)
            value = right_hand_side ^ parity(bits & without_pivot)
            if value:
                bits |= 1 << pivot
        if any(parity(bits & mask) != rhs for mask, rhs in normalized_rref):
            raise AssertionError("the normalized GF(2) solve failed")
        labels = tuple(
            sum(
                ((bits >> (3 * slot + bit)) & 1) << bit
                for bit in range(3)
            )
            for slot in range(8)
        )
        solutions.append(labels)
    return tuple(solutions)


def row_pair_swap_orbit(labels: Sequence[int]) -> frozenset[tuple[int, ...]]:
    """Orbit under the independent A/B and C/D row-pair swaps."""

    if len(labels) != 8 or labels[0] != 0:
        raise ValueError("expected eight normalized projective labels")
    result = set()
    for toggle_low, toggle_high in product((0, 1), repeat=2):
        changed = []
        for label in labels:
            low = label & 1
            middle = (label >> 1) & 1
            high = (label >> 2) & 1
            middle ^= (toggle_low & low) ^ (toggle_high & high)
            changed.append(low | (middle << 1) | (high << 2))
        result.add(tuple(changed))
    return frozenset(result)


def verify_mod4_word_independence() -> tuple[int, str]:
    """Exhaust all 65,536 scalar-word states and hash their exact images."""

    # On every carrier position, a scalar sign change toggles all four rows.
    # Its quotient effect is zero, which is the conceptual reason the words,
    # polarity, and carrier orientation disappear.
    occupied_positions = {
        shift + offset
        for shift in SHIFTS
        for tooth in range(5)
        for offset in (4 * tooth, 42 + 4 * tooth)
    }
    for position in occupied_positions:
        effect = 0
        for row in range(4):
            effect ^= POSITION_QUOTIENTS[(row, position)]
        if effect:
            raise AssertionError(
                f"scalar cancellation failed at position {position}"
            )

    digest = sha256()
    count = 0
    for slot, shift in enumerate(SHIFTS):
        for label in range(8):
            expected = PROJECTIVE_SLOT_STATES[slot][label]
            for first in range(16):
                for second in range(16):
                    for epsilon_bit, epsilon in enumerate((-1, 1)):
                        for orientation_bit, orientation in enumerate((-1, 1)):
                            observed = 0
                            for row in range(4):
                                projective_sign = VECTORS[label][row]
                                for tooth in range(5):
                                    if (
                                        orientation
                                        * projective_sign
                                        * WORDS[first][tooth]
                                        < 0
                                    ):
                                        observed ^= POSITION_QUOTIENTS[
                                            (row, shift + 4 * tooth)
                                        ]
                                    if (
                                        orientation
                                        * projective_sign
                                        * epsilon
                                        * WORDS[second][tooth]
                                        < 0
                                    ):
                                        observed ^= POSITION_QUOTIENTS[
                                            (row, shift + 42 + 4 * tooth)
                                        ]
                            if observed != expected:
                                raise AssertionError(
                                    "the word-independent modulo-four "
                                    "quotient failed"
                                )
                            digest.update(
                                bytes(
                                    (
                                        slot,
                                        label,
                                        first,
                                        second,
                                        epsilon_bit,
                                        orientation_bit,
                                    )
                                )
                            )
                            digest.update(observed.to_bytes(11, "little"))
                            count += 1

    if count != 65_536:
        raise AssertionError("the modulo-four audit size changed")
    if digest.hexdigest() != EXPECTED_MOD4_SHA256:
        raise AssertionError("the modulo-four audit digest changed")
    return count, digest.hexdigest()


def verify_projective_quotient() -> dict[str, object]:
    """Verify rank nine, 4,096 normalized maps, and 1,440 row orbits."""

    if len(HOLE_BASIS) != 6:
        raise AssertionError("the hole quotient rank changed")
    rref = derive_projective_rref()
    if len(rref) != 9:
        raise AssertionError("the projective quotient rank changed")
    if rref_hash(rref) != EXPECTED_RREF_SHA256:
        raise AssertionError("the projective RREF digest changed")

    labelings = enumerate_normalized_labelings(rref)
    if len(labelings) != 4_096 or len(set(labelings)) != 4_096:
        raise AssertionError("the normalized projective-map count changed")
    labeling_set = set(labelings)
    representatives = set()
    for labeling in labelings:
        orbit = row_pair_swap_orbit(labeling)
        if not orbit <= labeling_set:
            raise AssertionError(
                "a row-pair swap left the projective solution set"
            )
        representatives.add(min(orbit))
    if len(representatives) != 1_440:
        raise AssertionError("the projective row-orbit count changed")

    audit_count, audit_hash = verify_mod4_word_independence()
    return {
        "hole_rank": len(HOLE_BASIS),
        "projective_rank": len(rref),
        "normalized_labelings": len(labelings),
        "row_orbits": len(representatives),
        "rref_sha256": rref_hash(rref),
        "audit_count": audit_count,
        "audit_sha256": audit_hash,
    }


def main() -> None:
    signature_count, reversal_pairs, reversal_fixed = (
        verify_signature_fibers()
    )
    verify_paired_norm_identity()

    quartets = complementary_multisets(4)
    same_word = verify_same_word_theorem(quartets)
    octets, profiles, decomposable, octet_stats = classify_octets(quartets)
    directed = classify_directed_pair_inventories(octets)
    projective = verify_projective_quotient()

    print(
        "word_signatures="
        f"{signature_count} reversal_pairs={reversal_pairs} "
        f"reversal_fixed={reversal_fixed}"
    )
    print(
        f"same_word_quartets={len(quartets)} "
        f"ordered_inventories={same_word}"
    )
    print(
        f"octets={len(octets)} profiles={len(profiles)} "
        f"decomposable={len(decomposable)} "
        f"genuinely_new={len(octets) - len(decomposable)}"
    )
    print(
        "decomposable_profiles="
        f"{octet_stats['decomposable_profiles']} genuinely_new_profiles="
        f"{octet_stats['genuinely_new_profiles']} "
        f"common_alternation_orbits={octet_stats['alternation_orbits']} "
        f"fixed={octet_stats['alternation_fixed']} "
        f"paired={octet_stats['alternation_pairs']}"
    )
    print(
        "directed_pair_inventories="
        f"{directed['count']} both_sides_quartets="
        f"{directed['both_sides_quartets']} genuinely_distinct_lobe="
        f"{directed['genuinely_distinct_lobe']} diagonal="
        f"{directed['diagonal']}"
    )
    print(
        "projective_rank="
        f"{projective['projective_rank']} normalized_labelings="
        f"{projective['normalized_labelings']} "
        f"row_orbits={projective['row_orbits']} "
        f"mod4_states={projective['audit_count']}"
    )
    print(f"octet_sha256={EXPECTED_OCTET_SHA256}")
    print(f"profile_sha256={EXPECTED_PROFILE_SHA256}")
    print(f"decomposable_sha256={EXPECTED_DECOMPOSABLE_SHA256}")
    print(f"directed_pair_sha256={EXPECTED_DIRECTED_PAIR_SHA256}")
    print(f"rref_sha256={EXPECTED_RREF_SHA256}")
    print(f"mod4_sha256={EXPECTED_MOD4_SHA256}")
    print("all paired-lobe checks passed")


if __name__ == "__main__":
    main()

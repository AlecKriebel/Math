#!/usr/bin/env python3
"""Dependency-free exact verifier for the residual C3 sextic reduction.

The decimation ``d=226`` is 1 modulo 9 and ``2^2`` modulo 37.  It therefore
fixes the CRT row and zero column while rotating sextic classes by two.  Its
cube is 64 modulo 333, an element of the order-six multiplier subgroup already
quotiented out, so the residual action has order three.

This verifier reconstructs the class/matrix equivariance, both 28-signature
catalogs, all 298 compatible aggregate vectors, and all 1,658,700 compatible
ordered signature sextuples.  It checks the low-memory tie predicate against
the literal lexicographic minimum of all three cyclic rotations on every
signature sextuple.  Exactly 18 signature sextuples are fixed, and exactly
552,912 signature-sextuple representatives remain, agreeing with Burnside's
lemma.  This is not a count of full QPSK word or LP(333) solution orbits.

The verifier also audits the commuting B-only involution
``B(r,c) -> B(3-r,c)``.  On physical length-333 indices it is
``B'[n]=B[260*n+111]``; reversal and multiplier-73 invariance preserve every
B autocorrelation.  The action fixes the canonical zero column, all class
signatures, and every signature shard.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from itertools import product

from check_lp333_sextic_quotient import (
    CLASSES,
    N,
    P,
    ROOTS,
    ROWS,
    SKELETON_EXPONENTS,
    TRANSITION_MATRICES,
    ZERO_COLUMN_MATRIX,
    expand_crt_array,
    expand_length333,
    phase_sum,
    qpsk_to_sign_pair,
    real_paf_exponents,
    sequence_correlation_real,
)


C3_DECIMATION = 226
CLASS_ROTATION = 2
CANONICAL_ZERO_EXPONENTS = (0, 0, 0, 1, 2, 3, 1, 3, 2)
UNITS_MOD_9 = (1, 2, 4, 5, 7, 8)
SIGN_PAIR_TO_EXPONENT = {
    (1, 1): 0,
    (-1, 1): 1,
    (-1, -1): 2,
    (1, -1): 3,
}


def real_signature(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(real_paf_exponents(word, lag) for lag in range(1, 5))


@lru_cache(maxsize=2)
def target_signatures(imaginary_sum: int) -> tuple[tuple[int, ...], ...]:
    if imaginary_sum not in (-3, 3):
        raise ValueError("target imaginary sum must be -3 or +3")
    target = (0, imaginary_sum)
    return tuple(
        sorted(
            {
                real_signature(word)
                for word in product(range(4), repeat=ROWS)
                if phase_sum(word) == target
            }
        )
    )


@lru_cache(maxsize=1)
def triples_by_aggregate() -> dict[
    tuple[int, ...], tuple[tuple[int, int, int], ...]
]:
    signatures = target_signatures(-3)
    buckets: defaultdict[tuple[int, ...], list[tuple[int, int, int]]] = (
        defaultdict(list)
    )
    for triple in product(range(len(signatures)), repeat=3):
        vector = tuple(
            sum(signatures[index][coordinate] for index in triple)
            for coordinate in range(4)
        )
        buckets[vector].append(triple)
    return {
        vector: tuple(triples)
        for vector, triples in sorted(buckets.items())
    }


def negate(vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(-coordinate for coordinate in vector)


def literal_c3_canonical(pair_codes: tuple[int, int, int]) -> bool:
    """Test canonicality by directly comparing all three rotations."""

    rotations = (
        pair_codes,
        pair_codes[1:] + pair_codes[:1],
        pair_codes[2:] + pair_codes[:2],
    )
    return pair_codes == min(rotations)


def low_memory_c3_canonical(pair_codes: tuple[int, int, int]) -> bool:
    """The exact two-tie predicate used by the CP-SAT model."""

    first, second, third = pair_codes
    return (
        first <= second
        and first <= third
        and (first != third or first == second)
    )


def verify_decimation_action() -> None:
    if C3_DECIMATION % ROWS != 1:
        raise AssertionError("decimation does not fix CRT rows")
    if C3_DECIMATION % P != pow(2, CLASS_ROTATION, P):
        raise AssertionError("decimation does not rotate classes by two")
    if pow(C3_DECIMATION, 3, N) != 64:
        raise AssertionError("decimation cube is not the multiplier 64")
    if pow(64, 6, N) != 1:
        raise AssertionError("64 left the audited multiplier subgroup")

    for class_index, part in enumerate(CLASSES):
        target = set(CLASSES[(class_index + CLASS_ROTATION) % len(CLASSES)])
        image = {(C3_DECIMATION * value) % P for value in part}
        if image != target:
            raise AssertionError("decimation class rotation failed")
        if class_index % 2 != (
            class_index + CLASS_ROTATION
        ) % len(CLASSES) % 2:
            raise AssertionError("class rotation changed compression parity")

    part_permutation = (0,) + tuple(
        ((class_index + CLASS_ROTATION) % len(CLASSES)) + 1
        for class_index in range(len(CLASSES))
    )
    for class_index, matrix in enumerate(TRANSITION_MATRICES):
        shifted = TRANSITION_MATRICES[
            (class_index + CLASS_ROTATION) % len(CLASSES)
        ]
        for left in range(7):
            for right in range(7):
                if matrix[left][right] != shifted[
                    part_permutation[left]
                ][part_permutation[right]]:
                    raise AssertionError("transition-matrix C3 equivariance failed")
    for left in range(7):
        for right in range(7):
            if ZERO_COLUMN_MATRIX[left][right] != ZERO_COLUMN_MATRIX[
                part_permutation[left]
            ][part_permutation[right]]:
                raise AssertionError("zero-column matrix is not C3 invariant")


def verify_zero_word_transitivity() -> dict[str, int]:
    """Reconstruct the exact 972-word orbit of the canonical LP(9) word."""

    zero_catalog = {
        word
        for word in product(range(4), repeat=ROWS)
        if phase_sum(word) == (1, 0)
        and real_signature(word) == (-1, -1, -1, -1)
    }
    if len(zero_catalog) != 972:
        raise AssertionError("LP(9) zero-word catalog no longer has size 972")

    canonical_pairs = tuple(
        qpsk_to_sign_pair(ROOTS[exponent])
        for exponent in CANONICAL_ZERO_EXPONENTS
    )
    canonical_a = tuple(pair[0] for pair in canonical_pairs)
    canonical_b = tuple(pair[1] for pair in canonical_pairs)
    orbit: set[tuple[int, ...]] = set()
    transformation_count = 0
    for shift_a in range(ROWS):
        for shift_b in range(ROWS):
            for unit in UNITS_MOD_9:
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
                    word = tuple(
                        SIGN_PAIR_TO_EXPONENT[pair]
                        for pair in zip(a, b, strict=True)
                    )
                    orbit.add(word)
                    transformation_count += 1

    if transformation_count != ROWS * ROWS * len(UNITS_MOD_9) * 2:
        raise AssertionError("zero-word normalization group size changed")
    if len(orbit) != transformation_count:
        raise AssertionError("zero-word normalization action is not free")
    if orbit != zero_catalog:
        raise AssertionError("zero-word normalization action is not transitive")

    # An odd class rotation reverses the alternating compression parity and
    # therefore requires A/B swap.  That swap moves the canonical zero word.
    # Since the 972-element action above is free, the unique normalization
    # returning the swapped zero word is the swap itself; it cancels the
    # parity-correcting swap.  Hence odd class rotations do not survive the
    # canonical normalization.  Even rotations preserve parity and zero word,
    # leaving exactly rotations 0,2,4, i.e. C3.
    swapped_zero = tuple(
        SIGN_PAIR_TO_EXPONENT[(pair[1], pair[0])]
        for pair in canonical_pairs
    )
    if swapped_zero == CANONICAL_ZERO_EXPONENTS:
        raise AssertionError("A/B swap unexpectedly fixed the canonical zero word")
    source_pairs = tuple(
        qpsk_to_sign_pair(ROOTS[exponent])
        for exponent in swapped_zero
    )
    source_a = tuple(pair[0] for pair in source_pairs)
    source_b = tuple(pair[1] for pair in source_pairs)
    returning_transformations: list[tuple[int, int, int, bool]] = []
    for shift_a in range(ROWS):
        for shift_b in range(ROWS):
            for unit in UNITS_MOD_9:
                for swap in (False, True):
                    a = tuple(
                        source_a[(unit * row + shift_a) % ROWS]
                        for row in range(ROWS)
                    )
                    b = tuple(
                        source_b[(unit * row + shift_b) % ROWS]
                        for row in range(ROWS)
                    )
                    if swap:
                        a, b = b, a
                    word = tuple(
                        SIGN_PAIR_TO_EXPONENT[pair]
                        for pair in zip(a, b, strict=True)
                    )
                    if word == CANONICAL_ZERO_EXPONENTS:
                        returning_transformations.append(
                            (shift_a, shift_b, unit, swap)
                        )
    if returning_transformations != [(0, 0, 1, True)]:
        raise AssertionError(
            "the unique normalization of the swapped zero word is not A/B swap"
        )
    return {
        "zero_words": len(zero_catalog),
        "normalization_group_actions": transformation_count,
        "class_rotation_normalization_actions": (
            transformation_count * len(CLASSES)
        ),
        "distinct_zero_word_images": len(orbit),
        "surviving_class_rotations": 3,
    }


def rotate_quotient_classes(
    exponents: tuple[tuple[int, ...], ...],
    actions: int = 1,
) -> tuple[tuple[int, ...], ...]:
    """Apply the quotient action induced by ``x[n] -> x[226*n]``."""

    shift = CLASS_ROTATION * actions
    return tuple(
        (
            row[0],
            *(
                row[1 + ((class_index + shift) % len(CLASSES))]
                for class_index in range(len(CLASSES))
            ),
        )
        for row in exponents
    )


def deterministic_quotient_fixtures() -> tuple[
    tuple[tuple[int, ...], ...], ...
]:
    """Return two fixed-compression 9 by 7 arrays for physical replay."""

    base = tuple(
        (CANONICAL_ZERO_EXPONENTS[row], *SKELETON_EXPONENTS[row][1:])
        for row in range(ROWS)
    )
    column_rotated = tuple(
        (
            CANONICAL_ZERO_EXPONENTS[row],
            *(
                SKELETON_EXPONENTS[
                    (row + class_index + 1) % ROWS
                ][class_index + 1]
                for class_index in range(len(CLASSES))
            ),
        )
        for row in range(ROWS)
    )
    return base, column_rotated


def verify_full_expanded_action() -> dict[str, int]:
    """Replay decimation and all 333 correlation permutations physically."""

    if tuple(
        CANONICAL_ZERO_EXPONENTS[
            (C3_DECIMATION * row) % ROWS
        ]
        for row in range(ROWS)
    ) != CANONICAL_ZERO_EXPONENTS:
        raise AssertionError("canonical zero column is not fixed pointwise")

    correlation_checks = 0
    fixtures = deterministic_quotient_fixtures()
    for exponents in fixtures:
        if tuple(row[0] for row in exponents) != CANONICAL_ZERO_EXPONENTS:
            raise AssertionError("fixture lost the canonical zero column")
        for class_index in range(len(CLASSES)):
            actual = phase_sum(
                tuple(row[class_index + 1] for row in exponents)
            )
            expected = (0, -3 if class_index % 2 == 0 else 3)
            if actual != expected:
                raise AssertionError("fixture lost alternating fixed compression")

        sequence = expand_length333(expand_crt_array(exponents))
        rotated = rotate_quotient_classes(exponents)
        rotated_sequence = expand_length333(expand_crt_array(rotated))
        physical_decimation = tuple(
            sequence[(C3_DECIMATION * index) % N] for index in range(N)
        )
        if rotated_sequence != physical_decimation:
            raise AssertionError("quotient rotation disagrees with d=226 decimation")

        for lag in range(N):
            transformed_correlation = sequence_correlation_real(
                rotated_sequence, lag
            )
            permuted_correlation = sequence_correlation_real(
                sequence, (C3_DECIMATION * lag) % N
            )
            if transformed_correlation != permuted_correlation:
                raise AssertionError(
                    f"correlation permutation failed at lag {lag}"
                )
            correlation_checks += 1

        after_three = rotate_quotient_classes(exponents, 3)
        if after_three != exponents:
            raise AssertionError("three quotient C3 actions are not trivial")
        physical_after_three = tuple(
            sequence[(pow(C3_DECIMATION, 3, N) * index) % N]
            for index in range(N)
        )
        multiplier_64 = tuple(
            sequence[(64 * index) % N] for index in range(N)
        )
        if physical_after_three != multiplier_64 or multiplier_64 != sequence:
            raise AssertionError(
                "multiplier 64 is not trivial on the expanded invariant array"
            )
    return {
        "expanded_fixtures": len(fixtures),
        "full_correlation_checks": correlation_checks,
        "canonical_zero_columns_fixed": len(fixtures),
        "multiplier_64_replays": len(fixtures),
    }


def verify_all_signature_shards_invariant() -> int:
    """Check closure of both triple tables for every one of the 298 shards."""

    triples = triples_by_aggregate()
    compatible = tuple(vector for vector in triples if negate(vector) in triples)
    for vector in compatible:
        for target in (vector, negate(vector)):
            family = triples[target]
            family_set = set(family)
            for triple in family:
                rotations = (
                    triple[1:] + triple[:1],
                    triple[2:] + triple[:2],
                )
                if any(rotation not in family_set for rotation in rotations):
                    raise AssertionError(
                        f"signature shard {vector} is not C3 invariant"
                    )
    return len(compatible)


def b_reflect_exponents(
    exponents: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Apply ``A'=A, B'(r,c)=B(3-r,c)`` to a QPSK quotient."""

    result = []
    for row in range(ROWS):
        reflected_row = (3 - row) % ROWS
        transformed = []
        for column in range(7):
            a_sign = qpsk_to_sign_pair(ROOTS[exponents[row][column]])[0]
            b_sign = qpsk_to_sign_pair(
                ROOTS[exponents[reflected_row][column]]
            )[1]
            transformed.append(SIGN_PAIR_TO_EXPONENT[(a_sign, b_sign)])
        result.append(tuple(transformed))
    return tuple(result)


def sign_sequences(
    exponents: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    qpsk = expand_length333(expand_crt_array(exponents))
    pairs = tuple(qpsk_to_sign_pair(value) for value in qpsk)
    return (
        tuple(pair[0] for pair in pairs),
        tuple(pair[1] for pair in pairs),
    )


def sign_paf(sequence: tuple[int, ...], lag: int) -> int:
    return sum(
        sequence[index] * sequence[(index + lag) % len(sequence)]
        for index in range(len(sequence))
    )


def verify_b_reflection_action() -> dict[str, int]:
    """Audit the commuting B-only involution on full quotient fibers."""

    canonical_pairs = tuple(
        qpsk_to_sign_pair(ROOTS[exponent])
        for exponent in CANONICAL_ZERO_EXPONENTS
    )
    canonical_a = tuple(pair[0] for pair in canonical_pairs)
    canonical_b = tuple(pair[1] for pair in canonical_pairs)
    reflected_a = tuple(canonical_a[(3 - row) % ROWS] for row in range(ROWS))
    reflected_b = tuple(canonical_b[(3 - row) % ROWS] for row in range(ROWS))
    if reflected_b != canonical_b:
        raise AssertionError("canonical zero B word lost its reflection")
    if reflected_a == canonical_a:
        raise AssertionError("canonical zero A word unexpectedly has the reflection")

    affine_multiplier = 260
    affine_translation = 111
    if affine_multiplier % ROWS != -1 % ROWS:
        raise AssertionError("physical B reflection has the wrong row multiplier")
    if affine_multiplier % P != 1 or affine_translation % P != 0:
        raise AssertionError("physical B reflection does not fix CRT columns")
    if affine_translation % ROWS != 3:
        raise AssertionError("physical B reflection has the wrong row translation")
    if affine_multiplier % N != (-73) % N:
        raise AssertionError("260 is not reversal times multiplier 73")
    if 73 not in tuple(pow(64, exponent, N) for exponent in range(6)):
        raise AssertionError("73 left the multiplier-64 subgroup")

    # The 54-bit permutation has six fixed bits and 24 transpositions.  The
    # first member of each transposition occurs in the same order as the only
    # potentially decisive comparisons in the full row-major lex word.
    permutation = tuple(
        ((3 - row) % ROWS) * len(CLASSES) + class_index
        for row in range(ROWS)
        for class_index in range(len(CLASSES))
    )
    if any(permutation[permutation[index]] != index for index in range(54)):
        raise AssertionError("B reflection bit permutation is not an involution")
    fixed_bits = sum(permutation[index] == index for index in range(54))
    early_pairs = tuple(
        index for index in range(54) if index < permutation[index]
    )
    if fixed_bits != 6 or len(early_pairs) != 24:
        raise AssertionError("B reflection must have six fixed bits and 24 pairs")

    paf_checks = 0
    signature_checks = 0
    fixtures = deterministic_quotient_fixtures()
    for exponents in fixtures:
        transformed = b_reflect_exponents(exponents)
        if b_reflect_exponents(transformed) != exponents:
            raise AssertionError("B reflection is not an involution")
        if tuple(row[0] for row in transformed) != CANONICAL_ZERO_EXPONENTS:
            raise AssertionError("B reflection moved the canonical zero column")
        if b_reflect_exponents(rotate_quotient_classes(exponents)) != (
            rotate_quotient_classes(transformed)
        ):
            raise AssertionError("B reflection does not commute with residual C3")

        for class_index in range(len(CLASSES)):
            before_word = tuple(
                row[class_index + 1] for row in exponents
            )
            after_word = tuple(
                row[class_index + 1] for row in transformed
            )
            if phase_sum(before_word) != phase_sum(after_word):
                raise AssertionError("B reflection changed fixed compression")
            if real_signature(before_word) != real_signature(after_word):
                raise AssertionError("B reflection changed a class signature")
            signature_checks += 1

        a, b = sign_sequences(exponents)
        transformed_a, transformed_b = sign_sequences(transformed)
        if transformed_a != a:
            raise AssertionError("B reflection changed the A sequence")
        physical_b = tuple(
            b[(affine_multiplier * index + affine_translation) % N]
            for index in range(N)
        )
        if transformed_b != physical_b:
            raise AssertionError("quotient and physical B reflections disagree")
        if tuple(b[(64 * index) % N] for index in range(N)) != b:
            raise AssertionError("fixture B sequence is not multiplier-64 invariant")
        for lag in range(N):
            if sign_paf(transformed_b, lag) != sign_paf(b, lag):
                raise AssertionError(
                    f"B reflection changed periodic autocorrelation at lag {lag}"
                )
            if (
                sign_paf(transformed_a, lag) + sign_paf(transformed_b, lag)
                != sign_paf(a, lag) + sign_paf(b, lag)
            ):
                raise AssertionError(
                    f"B reflection changed the LP equation at lag {lag}"
                )
            paf_checks += 1
    return {
        "b_reflection_fixtures": len(fixtures),
        "b_reflection_paf_checks": paf_checks,
        "b_reflection_signature_checks": signature_checks,
        "b_reflection_fixed_bits": fixed_bits,
        "b_reflection_transpositions": len(early_pairs),
    }


@lru_cache(maxsize=1)
def verify_c3_reduction() -> dict[str, int]:
    verify_decimation_action()
    zero_counts = verify_zero_word_transitivity()
    expanded_counts = verify_full_expanded_action()
    reflection_counts = verify_b_reflection_action()
    negative = target_signatures(-3)
    positive = target_signatures(3)
    if negative != positive or len(negative) != 28:
        raise AssertionError("the two target sums lost their common 28 signatures")

    triples = triples_by_aggregate()
    compatible = tuple(vector for vector in triples if negate(vector) in triples)
    if len(compatible) != 298:
        raise AssertionError("compatible aggregate count changed")
    invariant_shards = verify_all_signature_shards_invariant()
    if invariant_shards != len(compatible):
        raise AssertionError("not every signature shard was C3 invariant")

    total = 0
    fixed = 0
    canonical = 0
    for vector in compatible:
        for even in triples[vector]:
            for odd in triples[negate(vector)]:
                pair_codes = tuple(
                    len(negative) * even[index] + odd[index]
                    for index in range(3)
                )
                literal = literal_c3_canonical(pair_codes)
                low_memory = low_memory_c3_canonical(pair_codes)
                if literal != low_memory:
                    raise AssertionError(
                        f"C3 tie encoding failed on pair codes {pair_codes}"
                    )
                total += 1
                canonical += int(literal)
                fixed += int(pair_codes[0] == pair_codes[1] == pair_codes[2])

    if total != 1_658_700:
        raise AssertionError("ordered signature sextuple count changed")
    if fixed != 18:
        raise AssertionError("C3 fixed-point count changed")
    burnside = (total + 2 * fixed) // 3
    if burnside != 552_912 or canonical != burnside:
        raise AssertionError(
            f"C3 orbit count changed: canonical={canonical}, Burnside={burnside}"
        )
    return {
        "ordered_signature_sextuples": total,
        "fixed_points": fixed,
        "signature_sextuple_c3_orbits": burnside,
        "canonical_signature_sextuples": canonical,
        "compatible_signature_shards": len(compatible),
        **zero_counts,
        **expanded_counts,
        **reflection_counts,
    }


def main() -> None:
    counts = verify_c3_reduction()
    print("PASS: d=226 fixes rows and rotates sextic classes by two")
    print("PASS: transition matrices and compression parity are C3 invariant")
    print(
        "PASS: canonical zero word normalization is free and transitive "
        f"({counts['distinct_zero_word_images']}/"
        f"{counts['normalization_group_actions']} distinct images; "
        f"{counts['class_rotation_normalization_actions']} combined "
        "class/normalization actions)"
    )
    print(
        "PASS: odd class rotations are removed by zero-word normalization; "
        f"{counts['surviving_class_rotations']} even rotations survive"
    )
    print(
        "PASS: every signature shard and deterministic full expansion is "
        "C3 invariant "
        f"({counts['compatible_signature_shards']} shards; "
        f"{counts['full_correlation_checks']} correlation checks)"
    )
    print(
        "PASS: commuting B-only affine reflection preserves all tested "
        "signatures and PAFs "
        f"({counts['b_reflection_signature_checks']} signatures; "
        f"{counts['b_reflection_paf_checks']} PAF checks)"
    )
    print(
        "PASS: exact pair-rotation lex leader including every tie case "
        f"({counts['ordered_signature_sextuples']} sextuples)"
    )
    print(
        "PASS: signature-sextuple Burnside count "
        f"({counts['fixed_points']} fixed; "
        f"{counts['signature_sextuple_c3_orbits']} C3 orbits)"
    )


if __name__ == "__main__":
    main()

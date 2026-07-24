#!/usr/bin/env python3
"""Exact verifier for an order-three LP(333) pure-axis lift.

This file is deliberately dependency-free: it imports only the Python
standard library and reconstructs all finite-field, QPSK, incidence, and
correlation objects that it checks.

The verified object lifts one exact row-sum word through twelve order-three
cyclotomic class words.  It satisfies the fixed compression and every
zero-column-lag equation.  It is *not* a Legendre pair: 51 of the 54
reversal-independent equations at nonzero column lag still fail.
"""

from __future__ import annotations

import argparse
import csv
from hashlib import sha256
from io import StringIO
from itertools import combinations, product
import json
from pathlib import Path
from typing import Iterable, Sequence


P = 37
ROWS = 9
CLASS_COUNT = 12
SUBGROUP_ORDER = 3
PRIMITIVE_ROOT = 2

ROOTS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
SIGN_PAIRS: tuple[tuple[int, int], ...] = (
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1),
)
PAIR_TO_EXPONENT = {
    pair: exponent for exponent, pair in enumerate(SIGN_PAIRS)
}
REAL_PHASE_DIFFERENCE = (1, 0, -1, 0)

CANONICAL_ZERO_EXPONENTS: tuple[int, ...] = (0, 0, 0, 1, 2, 3, 1, 3, 2)

CATALOG_RELATIVE_PATH = Path("output/lp333_order3_row_sum_catalog.csv")
CATALOG_SHA256 = (
    "e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea"
)
CATALOG_DATA_ROWS = 1_756
CATALOG_WITNESS_INDEX = 695
CATALOG_HEADER: tuple[str, ...] = tuple(
    coordinate
    for row in range(ROWS)
    for coordinate in (f"s{row}_real", f"s{row}_imag")
)
CATALOG_WITNESS: tuple[tuple[int, int], ...] = (
    (-2, 3),
    (-8, -3),
    (7, 0),
    (6, 1),
    (2, 3),
    (-3, -4),
    (6, 1),
    (-3, -4),
    (-4, 3),
)

# IDs index itertools.combinations(range(9), 3) in lexicographic order.
# Within each group, positions 0,...,5 correspond to the six classes of the
# indicated parity in increasing class order.
GROUP_NAMES = ("A_even", "A_odd", "B_even", "B_odd")
BLOCK_IDS: tuple[tuple[int, ...], ...] = (
    (45, 60, 43, 55, 42, 11),
    (56, 30, 55, 53, 43, 81),
    (61, 62, 13, 34, 21, 26),
    (41, 49, 81, 6, 6, 25),
)

WITNESS_CLASS_EXPONENTS: tuple[tuple[int, ...], ...] = (
    (3, 2, 0, 3, 3, 2, 0, 0, 2),
    (1, 2, 0, 1, 3, 1, 1, 3, 1),
    (3, 3, 1, 3, 3, 2, 0, 3, 1),
    (1, 0, 3, 2, 2, 0, 1, 1, 1),
    (0, 2, 3, 0, 0, 2, 2, 3, 3),
    (1, 1, 0, 1, 0, 2, 3, 1, 2),
    (3, 0, 2, 0, 1, 3, 2, 3, 3),
    (2, 2, 0, 0, 1, 1, 1, 1, 3),
    (0, 2, 3, 3, 1, 3, 3, 3, 1),
    (2, 3, 1, 1, 1, 0, 0, 1, 2),
    (1, 3, 2, 3, 3, 3, 0, 2, 0),
    (2, 1, 1, 1, 1, 0, 3, 2, 0),
)

# Entries are C(a,b)+1 for b in C_0,...,C_11 and a=0,...,4.
# The first row repeats after six entries because C(0,b)=C(0,-b).
EXPECTED_NONZERO_CLASS_RESIDUALS: tuple[tuple[int, ...], ...] = (
    (-6, 8, -12, 20, -4, -6, -6, 8, -12, 20, -4, -6),
    (-12, 8, -4, -22, 12, 30, 2, 2, -2, -12, -8, 6),
    (-4, 0, 28, 12, 10, 8, -10, 6, -8, 6, -30, -18),
    (0, -20, -8, -12, -2, -4, 22, 12, -2, -2, 14, 2),
    (-6, -14, 0, 20, 18, -10, 14, -2, 8, -10, -10, -8),
)

EXPECTED_BLOCK_IDS_HASH = (
    "695dc576aedc69e07e4d1d870b77c442e203187f4a2b580d5a0a1046a1cc7685"
)
EXPECTED_CLASS_WORDS_HASH = (
    "44bb6d660e741a7d720f5c959ce5a55131bad15680b00a933b612754cf6619c0"
)
EXPECTED_CLASSES_HASH = (
    "1689ef309edea5ae5e6425f22168ef6dee45bf929a976bd4bcb4cb257336a2ec"
)
EXPECTED_EXPANDED_QUOTIENT_HASH = (
    "8987d9920fb70d2b7b7f1473b8d6a8092aafe1ffd7d001704a7e4bdf5ef690e3"
)
EXPECTED_RESIDUALS_HASH = (
    "890b1044c0daf8ada89b6cf4ed3f4d96e621a14653cfd879298824656f4ea3c5"
)

Gaussian = tuple[int, int]
Word = tuple[int, ...]
Triple = tuple[int, int, int]
Array = tuple[tuple[int, ...], ...]


def compact_hash(value: object) -> str:
    """Hash the pinned compact-JSON serialization of ``value``."""

    serialization = json.dumps(value, separators=(",", ":"))
    return sha256(serialization.encode("ascii")).hexdigest()


def require_compact_hash(label: str, value: object, expected: str) -> None:
    actual = compact_hash(value)
    if actual != expected:
        raise AssertionError(f"{label} hash changed: {actual} != {expected}")


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def scale(factor: int, value: Gaussian) -> Gaussian:
    return factor * value[0], factor * value[1]


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
    length = len(exponents)
    return sum(
        REAL_PHASE_DIFFERENCE[
            (exponents[index] - exponents[(index + lag) % length]) % 4
        ]
        for index in range(length)
    )


def real_paf_signs(signs: Sequence[int], lag: int) -> int:
    length = len(signs)
    return sum(
        signs[index] * signs[(index + lag) % length]
        for index in range(length)
    )


def sign_words(exponents: Sequence[int]) -> tuple[Word, Word]:
    pairs = tuple(SIGN_PAIRS[exponent] for exponent in exponents)
    return (
        tuple(pair[0] for pair in pairs),
        tuple(pair[1] for pair in pairs),
    )


def plus_set(signs: Sequence[int]) -> Triple:
    result = tuple(index for index, sign in enumerate(signs) if sign == 1)
    if len(result) != 3:
        raise AssertionError(f"binary word does not have plus-weight three: {signs}")
    return result  # type: ignore[return-value]


def triple_catalog() -> tuple[Triple, ...]:
    catalog = tuple(combinations(range(ROWS), 3))
    if len(catalog) != 84:
        raise AssertionError("the three-subset catalog no longer has size 84")
    return catalog


def block_sets() -> dict[str, tuple[Triple, ...]]:
    catalog = triple_catalog()
    require_compact_hash(
        "difference-family block IDs", BLOCK_IDS, EXPECTED_BLOCK_IDS_HASH
    )
    return {
        name: tuple(catalog[index] for index in identifiers)
        for name, identifiers in zip(GROUP_NAMES, BLOCK_IDS, strict=True)
    }


def reconstruct_class_words() -> tuple[Word, ...]:
    """Rebuild all twelve QPSK words from the 24 normalized triples."""

    blocks = block_sets()
    result: list[Word] = []
    for class_index in range(CLASS_COUNT):
        parity_index = class_index // 2
        if class_index % 2 == 0:
            normalized_a = set(blocks["A_even"][parity_index])
            normalized_b = set(blocks["B_even"][parity_index])
            # A has original plus-weight six and was complemented.
            a = tuple(-1 if row in normalized_a else 1 for row in range(ROWS))
            b = tuple(1 if row in normalized_b else -1 for row in range(ROWS))
        else:
            normalized_a = set(blocks["A_odd"][parity_index])
            normalized_b = set(blocks["B_odd"][parity_index])
            a = tuple(1 if row in normalized_a else -1 for row in range(ROWS))
            # B has original plus-weight six and was complemented.
            b = tuple(-1 if row in normalized_b else 1 for row in range(ROWS))
        result.append(
            tuple(
                PAIR_TO_EXPONENT[pair]
                for pair in zip(a, b, strict=True)
            )
        )

    reconstructed = tuple(result)
    if reconstructed != WITNESS_CLASS_EXPONENTS:
        raise AssertionError("block IDs no longer reconstruct the pinned class words")
    require_compact_hash(
        "order-three class words",
        reconstructed,
        EXPECTED_CLASS_WORDS_HASH,
    )
    return reconstructed


def cyclotomic_classes() -> tuple[tuple[int, ...], ...]:
    """Return ``C_j=2^j <2^12>`` for j=0,...,11 in F_37."""

    subgroup = tuple(
        pow(PRIMITIVE_ROOT, 12 * exponent, P)
        for exponent in range(SUBGROUP_ORDER)
    )
    if subgroup != (1, 26, 10):
        raise AssertionError("the reconstructed order-three subgroup changed")
    classes = tuple(
        tuple(
            (pow(PRIMITIVE_ROOT, class_index, P) * element) % P
            for element in subgroup
        )
        for class_index in range(CLASS_COUNT)
    )
    if any(len(set(part)) != SUBGROUP_ORDER for part in classes):
        raise AssertionError("a cyclotomic class has the wrong size")
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("the cyclotomic classes do not partition F_37^*")
    for class_index in range(CLASS_COUNT):
        if set((-value) % P for value in classes[class_index]) != set(
            classes[(class_index + 6) % CLASS_COUNT]
        ):
            raise AssertionError("negation does not shift class index by six")
    require_compact_hash(
        "order-three cyclotomic classes", classes, EXPECTED_CLASSES_HASH
    )
    return classes


def expand_quotient(
    class_words: Sequence[Sequence[int]] = WITNESS_CLASS_EXPONENTS,
) -> Array:
    """Expand the zero word and twelve class words to a 9 by 37 array."""

    classes = cyclotomic_classes()
    class_of = {
        value: class_index
        for class_index, part in enumerate(classes)
        for value in part
    }
    expanded = tuple(
        tuple(
            CANONICAL_ZERO_EXPONENTS[row]
            if column == 0
            else class_words[class_of[column]][row]
            for column in range(P)
        )
        for row in range(ROWS)
    )
    if len(expanded) != ROWS or any(len(row) != P for row in expanded):
        raise AssertionError("expanded quotient has the wrong shape")
    require_compact_hash(
        "expanded order-three quotient",
        expanded,
        EXPECTED_EXPANDED_QUOTIENT_HASH,
    )
    return expanded


def parse_catalog_word(row: Sequence[str]) -> tuple[Gaussian, ...]:
    if len(row) != 2 * ROWS:
        raise AssertionError("a row-sum catalog row has the wrong width")
    entries = tuple(int(value) for value in row)
    return tuple(
        (entries[2 * index], entries[2 * index + 1])
        for index in range(ROWS)
    )


def is_sum_of_twelve_roots(value: Gaussian) -> bool:
    l1_norm = abs(value[0]) + abs(value[1])
    return l1_norm <= 12 and (12 - l1_norm) % 2 == 0


def verify_catalog(path: Path | None = None) -> dict[str, object]:
    """Pin and semantically replay all 1,756 row-sum catalog entries."""

    catalog_path = (
        path
        if path is not None
        else Path(__file__).resolve().parent / CATALOG_RELATIVE_PATH
    )
    payload = catalog_path.read_bytes()
    actual_hash = sha256(payload).hexdigest()
    if actual_hash != CATALOG_SHA256:
        raise AssertionError(
            f"row-sum catalog SHA-256 changed: {actual_hash} != {CATALOG_SHA256}"
        )

    rows = list(csv.reader(StringIO(payload.decode("ascii"), newline="")))
    if not rows or tuple(rows[0]) != CATALOG_HEADER:
        raise AssertionError("row-sum catalog header changed")
    data = tuple(parse_catalog_word(row) for row in rows[1:])
    if len(data) != CATALOG_DATA_ROWS:
        raise AssertionError(
            f"row-sum catalog count changed: {len(data)} != {CATALOG_DATA_ROWS}"
        )
    if len(set(data)) != CATALOG_DATA_ROWS:
        raise AssertionError("row-sum catalog contains duplicate words")
    if data[CATALOG_WITNESS_INDEX] != CATALOG_WITNESS:
        raise AssertionError("the pinned row-sum witness moved or changed")

    zero = tuple(ROOTS[exponent] for exponent in CANONICAL_ZERO_EXPONENTS)
    for word in data:
        if tuple(map(sum, zip(*word, strict=True))) != (1, 0):
            raise AssertionError("a catalog word has the wrong total")
        if real_paf_gaussian(word, 0) != 297:
            raise AssertionError("a catalog word has the wrong energy")
        if tuple(real_paf_gaussian(word, lag) for lag in range(1, 5)) != (
            -37,
            -37,
            -37,
            -37,
        ):
            raise AssertionError("a catalog word has the wrong PAF profile")

        t_word: list[Gaussian] = []
        for entry, zero_entry in zip(word, zero, strict=True):
            difference = (
                entry[0] - zero_entry[0],
                entry[1] - zero_entry[1],
            )
            if difference[0] % 3 != 0 or difference[1] % 3 != 0:
                raise AssertionError("a catalog word is not x+3t")
            t_entry = difference[0] // 3, difference[1] // 3
            if not is_sum_of_twelve_roots(t_entry):
                raise AssertionError("a t entry is not a sum of twelve roots")
            t_word.append(t_entry)
        if tuple(map(sum, zip(*t_word, strict=True))) != (0, 0):
            raise AssertionError("a catalog t word does not sum to zero")

    return {
        "sha256": actual_hash,
        "data_rows": len(data),
        "unique_rows": len(set(data)),
        "witness_index": CATALOG_WITNESS_INDEX,
        "witness": data[CATALOG_WITNESS_INDEX],
    }


def cyclic_intersection_size(block: Iterable[int], lag: int) -> int:
    points = set(block)
    return sum((point + lag) % ROWS in points for point in points)


def normalized_blocks_from_words(
    class_words: Sequence[Sequence[int]],
) -> dict[str, tuple[Triple, ...]]:
    groups: dict[str, list[Triple]] = {name: [] for name in GROUP_NAMES}
    for class_index, word in enumerate(class_words):
        a, b = sign_words(word)
        if class_index % 2 == 0:
            groups["A_even"].append(plus_set(tuple(-value for value in a)))
            groups["B_even"].append(plus_set(b))
        else:
            groups["A_odd"].append(plus_set(a))
            groups["B_odd"].append(plus_set(tuple(-value for value in b)))
    return {name: tuple(groups[name]) for name in GROUP_NAMES}


def verify_difference_family_equivalence() -> dict[str, object]:
    """Replay the sign normalization and the exact difference-family formula."""

    # The QPSK/sign-pair identity is checked locally for every possible pair.
    for left, right in product(range(4), repeat=2):
        qpsk_twice = 2 * REAL_PHASE_DIFFERENCE[(left - right) % 4]
        a_left, b_left = SIGN_PAIRS[left]
        a_right, b_right = SIGN_PAIRS[right]
        binary_sum = a_left * a_right + b_left * b_right
        if qpsk_twice != binary_sum:
            raise AssertionError("the QPSK/sign-pair correlation identity failed")

    # For every possible plus-weight-three binary word, verify
    # PAF(S,a)=-3+4|S intersect (S-a)|.
    for block in triple_catalog():
        signs = tuple(1 if row in block else -1 for row in range(ROWS))
        for lag in range(1, 5):
            expected = -3 + 4 * cyclic_intersection_size(block, lag)
            if real_paf_signs(signs, lag) != expected:
                raise AssertionError("the three-set PAF identity failed")
            if real_paf_signs(
                tuple(-value for value in signs), lag
            ) != expected:
                raise AssertionError("binary complementation changed a PAF")

    class_words = reconstruct_class_words()
    actual_blocks = normalized_blocks_from_words(class_words)
    if actual_blocks != block_sets():
        raise AssertionError("class-word normalization changed the 24 blocks")

    # Fixed compression forces the stated alternating high/low weights.
    phase_sums = tuple(phase_sum(word) for word in class_words)
    expected_phase_sums = tuple(
        (0, -3 if class_index % 2 == 0 else 3)
        for class_index in range(CLASS_COUNT)
    )
    if phase_sums != expected_phase_sums:
        raise AssertionError("class phase sums do not alternate -3i,+3i")

    total_intersections = tuple(
        sum(
            cyclic_intersection_size(block, lag)
            for blocks in actual_blocks.values()
            for block in blocks
        )
        for lag in range(1, 5)
    )
    if total_intersections != (18, 18, 18, 18):
        raise AssertionError("the 24 blocks lost the difference-family target")

    signature_sum = tuple(
        sum(real_paf_exponents(word, lag) for word in class_words)
        for lag in range(1, 5)
    )
    formula_values = tuple(
        -36 + 2 * intersection for intersection in total_intersections
    )
    if signature_sum != formula_values or signature_sum != (0, 0, 0, 0):
        raise AssertionError("the difference-family/signature equivalence failed")

    # Once the 24 block sizes are fixed at three, the displayed affine formula
    # makes the claimed iff literal.  Replay it over the entire possible
    # integer range (each one-block intersection is at most three).
    for total in range(24 * 3 + 1):
        if ((-36 + 2 * total == 0) != (total == 18)):
            raise AssertionError("the signature-zero iff test failed")

    roots_by_class = tuple(
        tuple(ROOTS[exponent] for exponent in word)
        for word in class_words
    )
    t_word = tuple(
        (
            sum(roots_by_class[class_index][row][0] for class_index in range(12)),
            sum(roots_by_class[class_index][row][1] for class_index in range(12)),
        )
        for row in range(ROWS)
    )

    blocks = block_sets()
    incidence_differences: list[tuple[int, int]] = []
    for row, t_entry in enumerate(t_word):
        e_a = sum(row in block for block in blocks["A_even"])
        o_a = sum(row in block for block in blocks["A_odd"])
        e_b = sum(row in block for block in blocks["B_even"])
        o_b = sum(row in block for block in blocks["B_odd"])
        left = o_a - e_a
        right = e_b - o_b
        expected_left = (t_entry[0] - t_entry[1]) // 2
        expected_right = (t_entry[0] + t_entry[1]) // 2
        if 2 * expected_left != t_entry[0] - t_entry[1]:
            raise AssertionError("the A incidence target is not integral")
        if 2 * expected_right != t_entry[0] + t_entry[1]:
            raise AssertionError("the B incidence target is not integral")
        if (left, right) != (expected_left, expected_right):
            raise AssertionError("a row incidence-difference equation failed")
        incidence_differences.append((left, right))

    zero = tuple(ROOTS[exponent] for exponent in CANONICAL_ZERO_EXPONENTS)
    lifted_s = tuple(
        add(zero_entry, scale(3, t_entry))
        for zero_entry, t_entry in zip(zero, t_word, strict=True)
    )
    if lifted_s != CATALOG_WITNESS:
        raise AssertionError("the 24 blocks do not lift the pinned catalog row")

    return {
        "blocks": sum(len(blocks) for blocks in actual_blocks.values()),
        "block_size": 3,
        "phase_sums": phase_sums,
        "intersection_totals": total_intersections,
        "signature_sum": signature_sum,
        "t": t_word,
        "incidence_differences": tuple(incidence_differences),
        "lifted_catalog_word": lifted_s,
    }


def quotient_correlation(array: Array, row_lag: int, column_lag: int) -> int:
    return sum(
        REAL_PHASE_DIFFERENCE[
            (
                array[row][column]
                - array[(row + row_lag) % ROWS][
                    (column + column_lag) % P
                ]
            )
            % 4
        ]
        for row in range(ROWS)
        for column in range(P)
    )


def verify_expansion_and_pure_axis() -> dict[str, object]:
    """Verify compression, row-sum target, and the zero-column-lag axis."""

    class_words = reconstruct_class_words()
    classes = cyclotomic_classes()
    array = expand_quotient(class_words)

    # Every entry is constant on an order-three class, and each class word has
    # the required fixed Legendre compression.
    for class_index, part in enumerate(classes):
        for row in range(ROWS):
            values = {array[row][column] for column in part}
            if values != {class_words[class_index][row]}:
                raise AssertionError("expanded quotient is not class-invariant")
        expected_sum = (0, -3 if class_index % 2 == 0 else 3)
        if phase_sum(class_words[class_index]) != expected_sum:
            raise AssertionError("a class word has the wrong compression")

    zero_word = tuple(ROOTS[value] for value in CANONICAL_ZERO_EXPONENTS)
    if phase_sum(CANONICAL_ZERO_EXPONENTS) != (1, 0):
        raise AssertionError("canonical zero word does not sum to one")
    if tuple(
        real_paf_exponents(CANONICAL_ZERO_EXPONENTS, lag)
        for lag in range(1, 5)
    ) != (-1, -1, -1, -1):
        raise AssertionError("canonical zero word is not an LP(9) core")

    row_sums = tuple(
        (
            sum(ROOTS[array[row][column]][0] for column in range(P)),
            sum(ROOTS[array[row][column]][1] for column in range(P)),
        )
        for row in range(ROWS)
    )
    if row_sums != CATALOG_WITNESS:
        raise AssertionError("expanded quotient has the wrong row-sum word")
    row_sum_profile = tuple(
        real_paf_gaussian(row_sums, lag) for lag in range(ROWS)
    )
    if row_sum_profile != (297,) + (-37,) * 8:
        raise AssertionError("expanded quotient lost the row-sum PAF target")

    full_phase_sum = tuple(
        sum(ROOTS[entry][coordinate] for row in array for entry in row)
        for coordinate in (0, 1)
    )
    if full_phase_sum != (1, 0):
        raise AssertionError("expanded QPSK sequence does not sum to one")

    flattened = tuple(entry for row in array for entry in row)
    full_a, full_b = sign_words(flattened)
    if (sum(full_a), sum(full_b)) != (1, 1):
        raise AssertionError("expanded binary sequences lost fixed compression")

    zero_column_lag = tuple(
        quotient_correlation(array, row_lag, 0)
        for row_lag in range(ROWS)
    )
    if zero_column_lag != (333,) + (-1,) * 8:
        raise AssertionError("the zero-column-lag pure axis is not exact")

    # Replay the identity sum_b C(a,b)=PAF_s(a), which explains why the
    # row-sum projection constrains weighted residual sums.
    for row_lag in range(ROWS):
        summed = sum(
            quotient_correlation(array, row_lag, column_lag)
            for column_lag in range(P)
        )
        if summed != row_sum_profile[row_lag]:
            raise AssertionError("row-sum/correlation aggregation identity failed")

    return {
        "shape": (ROWS, P),
        "classes": CLASS_COUNT,
        "class_size": SUBGROUP_ORDER,
        "full_phase_sum": full_phase_sum,
        "binary_sums": (sum(full_a), sum(full_b)),
        "row_sums": row_sums,
        "row_sum_profile": row_sum_profile,
        "zero_column_lag_profile": zero_column_lag,
    }


def verify_nonzero_class_residuals() -> dict[str, object]:
    """Pin all residuals and prove that the lift is not an LP(333)."""

    array = expand_quotient()
    classes = cyclotomic_classes()

    # Correlations must be constant on each multiplier class.  Check every
    # representative, not just the pinned first representative.
    correlation_by_row_and_class: list[list[int]] = []
    for row_lag in range(ROWS):
        row_values: list[int] = []
        for part in classes:
            values = {
                quotient_correlation(array, row_lag, column_lag)
                for column_lag in part
            }
            if len(values) != 1:
                raise AssertionError("correlation is not constant on an H-class")
            row_values.append(next(iter(values)))
        correlation_by_row_and_class.append(row_values)

    # Independently audit reversal C(a,b)=C(-a,-b).
    for row_lag in range(ROWS):
        for column_lag in range(P):
            if quotient_correlation(
                array, row_lag, column_lag
            ) != quotient_correlation(
                array, (-row_lag) % ROWS, (-column_lag) % P
            ):
                raise AssertionError("correlation reversal symmetry failed")

    residuals = tuple(
        tuple(value + 1 for value in correlation_by_row_and_class[row_lag])
        for row_lag in range(5)
    )
    if residuals != EXPECTED_NONZERO_CLASS_RESIDUALS:
        raise AssertionError("the pinned nonzero-class residual matrix changed")
    require_compact_hash(
        "order-three residual matrix", residuals, EXPECTED_RESIDUALS_HASH
    )

    if residuals[0][:6] != residuals[0][6:]:
        raise AssertionError("the a=0 reversal duplication changed")
    independent = residuals[0][:6] + tuple(
        value for row in residuals[1:] for value in row
    )
    if len(independent) != 54:
        raise AssertionError("the independent residual count changed")
    bad = sum(value != 0 for value in independent)
    energy = sum(value * value for value in independent)
    maximum = max(map(abs, independent))
    if (bad, energy, maximum) != (51, 8_320, 30):
        raise AssertionError("the pinned residual statistics changed")

    weighted_row_sums = tuple(
        SUBGROUP_ORDER * sum(row) for row in residuals
    )
    if weighted_row_sums != (0, 0, 0, 0, 0):
        raise AssertionError("weighted residual cancellation changed")

    # In particular, the geometric column axis a=0,b!=0 fails in all six
    # reversal-independent classes.  This guards against calling the object a
    # candidate or claiming that both coordinate axes are solved.
    column_axis_bad = sum(value != 0 for value in residuals[0][:6])
    if column_axis_bad != 6:
        raise AssertionError("the nonzero-column pure-axis failure count changed")

    return {
        "residuals": residuals,
        "reversal_independent_equations": len(independent),
        "bad_equations": bad,
        "residual_energy": energy,
        "max_abs_residual": maximum,
        "weighted_row_residual_sums": weighted_row_sums,
        "nonzero_column_axis_bad_classes": column_axis_bad,
        "is_lp333_candidate": False,
    }


def verify_all(catalog_path: Path | None = None) -> dict[str, object]:
    return {
        "catalog": verify_catalog(catalog_path),
        "difference_family": verify_difference_family_equivalence(),
        "expansion": verify_expansion_and_pure_axis(),
        "residual": verify_nonzero_class_residuals(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalog",
        type=Path,
        default=None,
        help="override the pinned row-sum catalog path",
    )
    args = parser.parse_args()
    result = verify_all(args.catalog)

    catalog = result["catalog"]
    family = result["difference_family"]
    expansion = result["expansion"]
    residual = result["residual"]
    assert isinstance(catalog, dict)
    assert isinstance(family, dict)
    assert isinstance(expansion, dict)
    assert isinstance(residual, dict)

    print(f"catalog_sha256={catalog['sha256']}")
    print(f"catalog_data_rows={catalog['data_rows']}")
    print(f"catalog_witness_index={catalog['witness_index']}")
    print(f"normalized_blocks={family['blocks']}")
    print(f"difference_totals={family['intersection_totals']}")
    print(f"class_signature_sum={family['signature_sum']}")
    print(f"expanded_shape={expansion['shape']}")
    print(f"row_sum_profile={expansion['row_sum_profile']}")
    print(f"zero_column_lag_profile={expansion['zero_column_lag_profile']}")
    print(
        "nonzero_class_bad="
        f"{residual['bad_equations']}/"
        f"{residual['reversal_independent_equations']}"
    )
    print(f"nonzero_class_residual_energy={residual['residual_energy']}")
    print(f"nonzero_class_max_abs_residual={residual['max_abs_residual']}")
    print(
        "weighted_row_residual_sums="
        f"{residual['weighted_row_residual_sums']}"
    )
    print("status=pure-axis lift verified; explicitly not an LP(333) candidate")


if __name__ == "__main__":
    main()

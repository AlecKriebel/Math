#!/usr/bin/env python3
"""Verify the coupled order-three row-sum theorem for fixed LP(333).

The multipliers 121 and 211 act on the CRT coordinates Z/9 x F_37 as

    (r,c) -> (4r,10c)   and   (r,c) -> (4r,26c).

Both therefore force the complete Gaussian row sum to be invariant under
``r -> 4r``.  This dependency-free verifier exhausts the resulting small
integer system, imposes the exact fixed-column lift, and checks the two pure
row-axis Legendre equations.

Nothing verified here is a Legendre pair or a Hadamard matrix.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from typing import Iterable


N = 333
ROW_MODULUS = 9
COLUMN_MODULUS = 37
ALPHA = 4
BETA = 10
BETA_INVERSE = 26
MULTIPLIERS = (121, 211)

Gaussian = tuple[int, int]
RowWord = tuple[Gaussian, Gaussian, Gaussian, Gaussian, Gaussian]
BinaryRowWord = tuple[int, int, int, int, int]
AxisPair = tuple[int, int]

ROOTS: tuple[Gaussian, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))
GENERIC_CATALOG_SHA256 = (
    "2a44ef09e87e6a364c105c1660e923076cc244c867b816722ec4791f4ba2fc28"
)
FIXED_MARGIN_CATALOG_SHA256 = (
    "4c03c95355e161dca2bca94c635f377f73ec069baf36aa1be8143fd351ea2965"
)


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def dot(left: Gaussian, right: Gaussian) -> int:
    return left[0] * right[0] + left[1] * right[1]


def norm(value: Gaussian) -> int:
    return dot(value, value)


def is_qpsk_sum(value: Gaussian, number_of_roots: int) -> bool:
    """Return whether ``value`` is a sum of ``number_of_roots`` fourth roots."""

    taxicab_norm = abs(value[0]) + abs(value[1])
    return (
        taxicab_norm <= number_of_roots
        and (number_of_roots - taxicab_norm) % 2 == 0
    )


@lru_cache(maxsize=1)
def qpsk_row_sums() -> tuple[Gaussian, ...]:
    """All Gaussian sums of 37 fourth roots."""

    return tuple(
        (real, imag)
        for real in range(-37, 38)
        for imag in range(-37, 38)
        if is_qpsk_sum((real, imag), 37)
    )


def twisted_pair_value(d_value: Gaussian, e_value: Gaussian) -> int:
    """The positive-definite left side forced to equal 37."""

    return (
        3
        * (
            norm(d_value)
            + norm(e_value)
            + dot(d_value, e_value)
        )
        - d_value[0]
        - e_value[0]
    )


@lru_cache(maxsize=1)
def unrestricted_twisted_pairs() -> tuple[tuple[Gaussian, Gaussian], ...]:
    """All Gaussian-integer solutions of the twisted pair equation.

    The quadratic form is at least half the squared Euclidean norm of the
    four coordinates.  If that norm is at least 6, Cauchy--Schwarz makes the
    left side strictly larger than 37.  Thus the box [-5,5]^4 is complete.
    """

    values = range(-5, 6)
    return tuple(
        sorted(
            ((dx, dy), (ex, ey))
            for dx, dy, ex, ey in product(values, repeat=4)
            if twisted_pair_value((dx, dy), (ex, ey)) == 37
        )
    )


@lru_cache(maxsize=1)
def realizable_twisted_pairs() -> tuple[tuple[Gaussian, Gaussian], ...]:
    """Twisted pairs whose entries can each be sums of 37 fourth roots."""

    return tuple(
        pair
        for pair in unrestricted_twisted_pairs()
        if is_qpsk_sum(pair[0], 37) and is_qpsk_sum(pair[1], 37)
    )


def abc_target(
    d_value: Gaussian, e_value: Gaussian
) -> tuple[Gaussian, int]:
    """Return the required sum and energy of the three fixed-row values."""

    pair_sum = add(d_value, e_value)
    target_sum = (1 - 3 * pair_sum[0], -3 * pair_sum[1])
    target_energy = 297 - 3 * (norm(d_value) + norm(e_value))
    return target_sum, target_energy


@lru_cache(maxsize=None)
def abc_completions(
    target_sum: Gaussian, target_energy: int
) -> tuple[tuple[Gaussian, Gaussian, Gaussian], ...]:
    """Enumerate ordered QPSK-row-sum triples with given sum and energy."""

    result: list[tuple[Gaussian, Gaussian, Gaussian]] = []
    for a_value in qpsk_row_sums():
        for b_value in qpsk_row_sums():
            c_value = (
                target_sum[0] - a_value[0] - b_value[0],
                target_sum[1] - a_value[1] - b_value[1],
            )
            if (
                is_qpsk_sum(c_value, 37)
                and norm(a_value) + norm(b_value) + norm(c_value)
                == target_energy
            ):
                result.append((a_value, b_value, c_value))
    return tuple(result)


@lru_cache(maxsize=1)
def generic_row_sum_catalog() -> tuple[RowWord, ...]:
    """All invariant row-sum words satisfying the complete row projection."""

    result = []
    for d_value, e_value in realizable_twisted_pairs():
        target_sum, target_energy = abc_target(d_value, e_value)
        for a_value, b_value, c_value in abc_completions(
            target_sum, target_energy
        ):
            result.append((a_value, b_value, c_value, d_value, e_value))
    return tuple(sorted(result))


def root_to_binary_pair(root: Gaussian) -> tuple[int, int]:
    """Invert q=(A+B+i(B-A))/2 at one QPSK entry."""

    real, imag = root
    return real - imag, real + imag


@lru_cache(maxsize=1)
def zero_column_fixed_triples() -> tuple[
    tuple[Gaussian, Gaussian, Gaussian], ...
]:
    """Possible QPSK values at CRT rows 0,3,6 in the zero column."""

    result = []
    for roots in product(ROOTS, repeat=3):
        binary_pairs = tuple(root_to_binary_pair(root) for root in roots)
        if (
            sum(pair[0] for pair in binary_pairs) == 1
            and sum(pair[1] for pair in binary_pairs) == 1
        ):
            result.append(roots)
    return tuple(result)


def zero_column_compatible(word: RowWord) -> bool:
    """Check the exact fixed-row congruence forced by the zero column."""

    fixed_values = word[:3]
    return any(
        all(
            (value[0] - root[0]) % 3 == 0
            and (value[1] - root[1]) % 3 == 0
            for value, root in zip(fixed_values, roots)
        )
        for roots in zero_column_fixed_triples()
    )


@lru_cache(maxsize=1)
def fixed_margin_row_sum_catalog() -> tuple[RowWord, ...]:
    """The generic catalog after the zero-column/fixed-margin condition."""

    return tuple(
        word for word in generic_row_sum_catalog() if zero_column_compatible(word)
    )


def expand_row_word(word: RowWord) -> tuple[Gaussian, ...]:
    """Expand (a,b,c,d,e) to rows (a,d,e,b,d,e,c,d,e)."""

    a_value, b_value, c_value, d_value, e_value = word
    return (
        a_value,
        d_value,
        e_value,
        b_value,
        d_value,
        e_value,
        c_value,
        d_value,
        e_value,
    )


def real_periodic_paf(sequence: tuple[Gaussian, ...], lag: int) -> int:
    return sum(
        dot(sequence[index], sequence[(index + lag) % len(sequence)])
        for index in range(len(sequence))
    )


def binary_periodic_paf(sequence: tuple[int, ...], lag: int) -> int:
    return sum(
        sequence[index] * sequence[(index + lag) % len(sequence)]
        for index in range(len(sequence))
    )


def binary_rows(word: RowWord, sequence_index: int) -> BinaryRowWord:
    """Recover the five invariant row sums of binary sequence A or B."""

    if sequence_index not in (0, 1):
        raise ValueError("sequence_index must be 0 (A) or 1 (B)")
    if sequence_index == 0:
        return tuple(value[0] - value[1] for value in word)  # type: ignore[return-value]
    return tuple(value[0] + value[1] for value in word)  # type: ignore[return-value]


def sign_word(plus_positions: Iterable[int]) -> tuple[int, ...]:
    result = [-1] * 9
    for position in plus_positions:
        result[position] = 1
    return tuple(result)


def binary_orbit_row_signature(sequence: tuple[int, ...]) -> BinaryRowWord:
    """Contribution of one three-column orbit to five invariant row sums."""

    return (
        3 * sequence[0],
        3 * sequence[3],
        3 * sequence[6],
        sequence[1] + sequence[4] + sequence[7],
        sequence[2] + sequence[5] + sequence[8],
    )


@lru_cache(maxsize=None)
def binary_orbit_row_signatures(weight: int) -> frozenset[BinaryRowWord]:
    if weight not in (3, 6):
        raise ValueError("the nonzero fixed-column weight must be 3 or 6")
    return frozenset(
        binary_orbit_row_signature(sign_word(positions))
        for positions in combinations(range(9), weight)
    )


@lru_cache(maxsize=1)
def binary_zero_column_words() -> tuple[tuple[int, ...], ...]:
    """The six invariant weight-five binary zero columns."""

    result = []
    for fixed0, fixed3, fixed6, moving1, moving2 in product(
        (-1, 1), repeat=5
    ):
        if fixed0 + fixed3 + fixed6 + 3 * moving1 + 3 * moving2 == 1:
            result.append(
                (
                    fixed0,
                    moving1,
                    moving2,
                    fixed3,
                    moving1,
                    moving2,
                    fixed6,
                    moving1,
                    moving2,
                )
            )
    return tuple(result)


@lru_cache(maxsize=1)
def reachable_binary_row_sums() -> frozenset[BinaryRowWord]:
    """Exact row sums reachable from all 37 prescribed column margins."""

    states: set[BinaryRowWord] = {(0, 0, 0, 0, 0)}
    for signatures in (
        (binary_orbit_row_signatures(3),) * 6
        + (binary_orbit_row_signatures(6),) * 6
    ):
        states = {
            tuple(left[index] + right[index] for index in range(5))  # type: ignore[misc]
            for left in states
            for right in signatures
        }

    zero_signatures = {
        (
            sequence[0],
            sequence[3],
            sequence[6],
            sequence[1],
            sequence[2],
        )
        for sequence in binary_zero_column_words()
    }
    return frozenset(
        tuple(state[index] + zero[index] for index in range(5))  # type: ignore[misc]
        for state in states
        for zero in zero_signatures
    )


def catalog_bytes(catalog: Iterable[RowWord]) -> bytes:
    rows = []
    for word in sorted(catalog):
        flat = [coordinate for value in word for coordinate in value]
        rows.append(",".join(str(value) for value in flat) + "\n")
    return "".join(rows).encode("ascii")


def catalog_digest(catalog: Iterable[RowWord]) -> str:
    return sha256(catalog_bytes(catalog)).hexdigest()


def rotate_fixed_rows(word: RowWord) -> RowWord:
    a_value, b_value, c_value, d_value, e_value = word
    return b_value, c_value, a_value, d_value, e_value


def reflect_rows(word: RowWord) -> RowWord:
    a_value, b_value, c_value, d_value, e_value = word
    return a_value, c_value, b_value, e_value, d_value


def conjugate_word(word: RowWord) -> RowWord:
    return tuple((value[0], -value[1]) for value in word)  # type: ignore[return-value]


def row_symmetry_orbit(word: RowWord, include_conjugation: bool) -> frozenset[RowWord]:
    result: set[RowWord] = set()
    rotated = word
    for _ in range(3):
        result.add(rotated)
        result.add(reflect_rows(rotated))
        if include_conjugation:
            result.add(conjugate_word(rotated))
            result.add(conjugate_word(reflect_rows(rotated)))
        rotated = rotate_fixed_rows(rotated)
    return frozenset(result)


def count_row_symmetry_orbits(include_conjugation: bool) -> tuple[int, Counter[int]]:
    catalog = frozenset(fixed_margin_row_sum_catalog())
    unseen = set(catalog)
    sizes: Counter[int] = Counter()
    count = 0
    while unseen:
        word = min(unseen)
        orbit = row_symmetry_orbit(word, include_conjugation)
        if not orbit <= catalog:
            raise AssertionError("catalog is not closed under the claimed symmetry")
        unseen.difference_update(orbit)
        sizes[len(orbit)] += 1
        count += 1
    return count, sizes


@lru_cache(maxsize=1)
def six_weight_three_axis_states() -> frozenset[tuple[int, ...]]:
    """Joint row-sum/axis-PAF states for six weight-three orbit columns."""

    signatures = set()
    for positions in combinations(range(9), 3):
        sequence = sign_word(positions)
        row_signature = binary_orbit_row_signature(sequence)
        paf1 = sum(binary_periodic_paf(sequence, lag) for lag in (1, 4, 7))
        paf3 = 3 * binary_periodic_paf(sequence, 3)
        signatures.add(row_signature + (paf1, paf3))

    states: set[tuple[int, ...]] = {(0, 0, 0, 0, 0, 0, 0)}
    for _ in range(6):
        states = {
            tuple(left[index] + right[index] for index in range(7))
            for left in states
            for right in signatures
        }
    return frozenset(states)


@lru_cache(maxsize=1)
def six_axis_states_by_row() -> dict[BinaryRowWord, frozenset[AxisPair]]:
    grouped: defaultdict[BinaryRowWord, set[AxisPair]] = defaultdict(set)
    for state in six_weight_three_axis_states():
        grouped[state[:5]].add((state[5], state[6]))  # type: ignore[arg-type]
    return {row: frozenset(values) for row, values in grouped.items()}


@lru_cache(maxsize=None)
def binary_axis_options(target: BinaryRowWord) -> frozenset[AxisPair]:
    """Exact attainable (PAF(1,0),PAF(3,0)) for one binary sequence."""

    grouped = six_axis_states_by_row()
    result: set[AxisPair] = set()
    for zero_sequence in binary_zero_column_words():
        zero_row = (
            zero_sequence[0],
            zero_sequence[3],
            zero_sequence[6],
            zero_sequence[1],
            zero_sequence[2],
        )
        zero_axis = (
            binary_periodic_paf(zero_sequence, 1),
            binary_periodic_paf(zero_sequence, 3),
        )
        delta = tuple(target[index] - zero_row[index] for index in range(5))
        for left_row, left_axes in grouped.items():
            # A weight-six word is the complement of a weight-three word:
            # its row signature is negated while both PAFs are unchanged.
            right_row = tuple(
                left_row[index] - delta[index] for index in range(5)
            )
            right_axes = grouped.get(right_row)
            if right_axes is None:
                continue
            for left_axis in left_axes:
                for right_axis in right_axes:
                    result.add(
                        (
                            zero_axis[0] + left_axis[0] + right_axis[0],
                            zero_axis[1] + left_axis[1] + right_axis[1],
                        )
                    )
    return frozenset(result)


def survives_pure_row_axis(word: RowWord) -> bool:
    options_a = binary_axis_options(binary_rows(word, 0))
    options_b = binary_axis_options(binary_rows(word, 1))
    return any(
        (-2 - paf_a[0], -2 - paf_a[1]) in options_b
        for paf_a in options_a
    )


def legendre_symbol_37(value: int) -> int:
    residue = value % 37
    if residue == 0:
        return 0
    return 1 if pow(residue, 18, 37) == 1 else -1


@lru_cache(maxsize=1)
def column_exponent_reversal() -> tuple[int, ...]:
    """A permutation pi with pi(10c)=26*pi(c), orbit by orbit."""

    permutation = [-1] * 37
    permutation[0] = 0
    seen = {0}
    for column in range(1, 37):
        if column in seen:
            continue
        orbit_set = {
            column,
            BETA * column % 37,
            BETA * BETA * column % 37,
        }
        representative = min(orbit_set)
        orbit = (
            representative,
            BETA * representative % 37,
            BETA * BETA * representative % 37,
        )
        for exponent, source in enumerate(orbit):
            permutation[source] = orbit[(-exponent) % 3]
        seen.update(orbit)
    return tuple(permutation)


def check_crt_actions_and_orientation_reversal() -> None:
    """Check the exact relationship between the 121 and 211 lanes."""

    assert gcd(121, N) == gcd(211, N) == 1
    assert (121 % 9, 121 % 37) == (ALPHA, BETA)
    assert (211 % 9, 211 % 37) == (ALPHA, BETA_INVERSE)
    assert pow(ALPHA, 3, 9) == 1
    assert pow(BETA, 3, 37) == 1
    assert BETA * BETA_INVERSE % 37 == 1

    permutation = column_exponent_reversal()
    assert sorted(permutation) == list(range(37))
    for column in range(37):
        assert (
            permutation[BETA * column % 37]
            == BETA_INVERSE * permutation[column] % 37
        )
        assert legendre_symbol_37(permutation[column]) == legendre_symbol_37(
            column
        )
    assert permutation[4] != (permutation[1] + permutation[3]) % 37

    # Swapping A,B after decimation by u=298 acts as complex conjugation on
    # row sums and preserves the fixed compression.
    nonresidue_decimation = 298
    assert nonresidue_decimation % 9 == 1
    assert nonresidue_decimation % 37 == 2
    assert legendre_symbol_37(2) == -1


def verify() -> dict[str, object]:
    check_crt_actions_and_orientation_reversal()

    assert len(qpsk_row_sums()) == 1444
    assert len(unrestricted_twisted_pairs()) == 36
    assert len(realizable_twisted_pairs()) == 12

    completion_counts = Counter()
    for d_value, e_value in realizable_twisted_pairs():
        target = abc_target(d_value, e_value)
        count = len(abc_completions(*target))
        completion_counts[count] += 1
    assert completion_counts == Counter({504: 12})

    generic = generic_row_sum_catalog()
    assert len(generic) == 6048
    assert len(set(generic)) == len(generic)
    assert catalog_digest(generic) == GENERIC_CATALOG_SHA256
    for word in generic:
        expanded = expand_row_word(word)
        assert (
            sum(value[0] for value in expanded),
            sum(value[1] for value in expanded),
        ) == (1, 0)
        assert real_periodic_paf(expanded, 0) == 297
        assert tuple(real_periodic_paf(expanded, lag) for lag in range(1, 5)) == (
            -37,
            -37,
            -37,
            -37,
        )

    assert len(zero_column_fixed_triples()) == 9
    filtered = fixed_margin_row_sum_catalog()
    assert len(filtered) == 1296
    assert catalog_digest(filtered) == FIXED_MARGIN_CATALOG_SHA256

    assert len(binary_orbit_row_signatures(3)) == 20
    assert len(binary_orbit_row_signatures(6)) == 20
    reachable = reachable_binary_row_sums()
    assert len(reachable) == 186576
    for word in generic:
        exact_margin_lift = (
            binary_rows(word, 0) in reachable
            and binary_rows(word, 1) in reachable
        )
        assert exact_margin_lift == zero_column_compatible(word)

    dihedral_count, dihedral_sizes = count_row_symmetry_orbits(False)
    extended_count, extended_sizes = count_row_symmetry_orbits(True)
    assert (dihedral_count, dihedral_sizes) == (216, Counter({6: 216}))
    assert (extended_count, extended_sizes) == (108, Counter({12: 108}))

    axis_states = six_weight_three_axis_states()
    assert len(axis_states) == 21953
    assert len(six_axis_states_by_row()) == 3430
    binary_targets = {
        binary_rows(word, sequence_index)
        for word in filtered
        for sequence_index in (0, 1)
    }
    assert len(binary_targets) == 147
    axis_option_histogram = Counter(
        len(binary_axis_options(target)) for target in binary_targets
    )
    assert axis_option_histogram == Counter(
        {25: 24, 27: 24, 32: 24, 31: 24, 28: 18, 26: 18, 33: 9, 34: 6}
    )
    pure_axis_survivors = sum(survives_pure_row_axis(word) for word in filtered)
    assert pure_axis_survivors == 1296

    return {
        "status": "verified projected theorem; no LP(333) or H(668) found",
        "multipliers": list(MULTIPLIERS),
        "unrestricted_twisted_pairs": 36,
        "qpsk_realizable_twisted_pairs": 12,
        "generic_row_sum_words": len(generic),
        "generic_catalog_sha256": GENERIC_CATALOG_SHA256,
        "fixed_margin_row_sum_words": len(filtered),
        "fixed_margin_catalog_sha256": FIXED_MARGIN_CATALOG_SHA256,
        "common_row_dihedral_orbits": dihedral_count,
        "extended_equivalence_orbits": extended_count,
        "distinct_binary_row_targets": len(binary_targets),
        "six_column_axis_states": len(axis_states),
        "pure_row_axis_survivors": pure_axis_survivors,
        "orientation_reversal_scope": (
            "fixed margins, row sums, and b=0 correlations only"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

#!/usr/bin/env python3
"""Replay the order-three LP(333) Eisenstein and mod-3 reductions.

This verifier is dependency-free.  It checks, with exact integer arithmetic,
that the 100 Gaussian row-compression states factor as two ten-state binary
profiles, that the 3 by 37 compressed correlation problem is equivalent to a
pair of complementary Eisenstein sequences of energy 167, that only thirteen
of the twenty reversal-independent real equations remain independent, and
that a local mod-3 condition leaves exactly 3,334 of 10,000 choices on each
of the six negation pairs.

The reduction is a necessary-condition sieve, not a Legendre pair and not a
Hadamard matrix.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import csv
import json
from math import comb
from pathlib import Path
from typing import Sequence


P = 37
ROWS = 9
CLASS_COUNT = 12
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
CANONICAL_ZERO_EXPONENTS: tuple[int, ...] = (0, 0, 0, 1, 2, 3, 1, 3, 2)

CATALOG_RELATIVE_PATH = Path("output/lp333_order3_row_sum_catalog.csv")
CATALOG_SHA256 = (
    "e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea"
)
CATALOG_DATA_ROWS = 1_756

EXPECTED_PROFILE_HASH = (
    "1caec75c4e44fc144fcb86e89db63a1b8d7c9acd92ebb05d417ef1cafd2708f0"
)
EXPECTED_STATE_MULTIPLICITY_HASH = (
    "7e04ca5139fb759d663d2b2263951f81accc21ef98def39733ba4d9e93165489"
)
EXPECTED_T_SHARD_HASH = (
    "fe575c38060412cd15fa0bad385c1aaee988bbb3303b9b2493463d2feb421e4d"
)
EXPECTED_MOD3_PAIR_HASH = (
    "77cdcd5adc7fd8d301b8a66d5edc91810e2a2861e395e75fe2244b1b25aeacdb"
)
EXPECTED_MOD3_SHARD_WITNESS_HASH = (
    "4903107d03fc757a72d14d52d555cb9cc257aa0e8480ca22c7474ba365cf6ddc"
)

# Each entry is
#   (class-aggregate Eisenstein target A_real,A_omega,B_real,B_omega,
#    twelve A profile IDs, twelve B profile IDs).
# Profile IDs index PROFILES.  These are witnesses only for the aggregate,
# origin-energy, and local mod-3 conditions, not for the full correlations.
MOD3_SHARD_WITNESSES: tuple[
    tuple[tuple[int, int, int, int], tuple[int, ...], tuple[int, ...]], ...
] = (
    ((-3, -3, -4, -2), (3, 1, 6, 5, 9, 3, 5, 7, 1, 5, 5, 5), (5, 9, 5, 2, 5, 5, 5, 5, 5, 8, 5, 5)),
    ((-3, -3, -2, 2), (3, 6, 5, 5, 3, 3, 7, 1, 6, 5, 5, 5), (8, 5, 2, 9, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((-3, 0, -3, -3), (2, 5, 9, 5, 5, 2, 2, 7, 9, 5, 5, 6), (0, 8, 5, 6, 5, 5, 5, 5, 5, 1, 5, 4)),
    ((-3, 0, 0, 3), (8, 6, 0, 5, 9, 1, 8, 7, 3, 5, 5, 6), (3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((-1, -2, -5, -1), (3, 5, 6, 5, 3, 3, 4, 1, 4, 5, 5, 5), (1, 4, 5, 7, 5, 5, 5, 5, 1, 6, 5, 5)),
    ((-1, -2, -4, 1), (9, 1, 1, 5, 9, 9, 1, 7, 6, 5, 5, 5), (2, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((0, 3, -4, -2), (1, 6, 1, 5, 9, 2, 6, 1, 1, 5, 5, 5), (3, 8, 5, 6, 5, 5, 5, 4, 5, 6, 5, 6)),
    ((0, 3, -2, 2), (0, 7, 5, 5, 9, 3, 7, 1, 6, 5, 5, 9), (2, 5, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((1, -1, 2, -2), (9, 5, 1, 0, 0, 9, 2, 2, 6, 5, 5, 5), (7, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5, 5)),
    ((1, -1, 4, 2), (3, 2, 5, 0, 5, 3, 1, 8, 2, 5, 5, 5), (8, 0, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5)),
    ((1, 2, -5, -1), (0, 1, 1, 5, 9, 3, 2, 7, 6, 5, 5, 5), (1, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((1, 2, -4, 1), (3, 6, 1, 5, 9, 7, 5, 6, 7, 5, 5, 5), (6, 7, 5, 7, 5, 5, 7, 7, 5, 6, 5, 8)),
    ((2, -2, -4, -2), (3, 1, 1, 5, 9, 9, 1, 1, 1, 5, 5, 5), (4, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((2, -2, -2, 2), (9, 9, 1, 5, 9, 9, 1, 4, 6, 5, 5, 5), (2, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((2, 1, 2, -2), (5, 5, 6, 0, 0, 9, 0, 1, 7, 5, 5, 5), (8, 2, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5)),
    ((2, 1, 4, 2), (9, 0, 1, 9, 5, 9, 1, 2, 7, 5, 5, 5), (8, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((3, 0, 0, -3), (0, 9, 9, 5, 3, 5, 4, 1, 5, 5, 5, 7), (7, 2, 5, 5, 5, 8, 5, 5, 5, 5, 5, 5)),
    ((3, 0, 3, 3), (1, 0, 1, 2, 5, 9, 8, 5, 7, 5, 5, 9), (5, 5, 5, 8, 5, 1, 6, 5, 5, 5, 5, 1)),
    ((4, -1, 0, 0), (7, 8, 1, 0, 4, 0, 1, 8, 6, 9, 5, 5), (5, 5, 5, 5, 7, 5, 5, 5, 5, 5, 2, 5)),
    ((4, 2, -4, -2), (5, 2, 1, 9, 0, 3, 6, 4, 6, 5, 5, 5), (4, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((4, 2, -2, 2), (3, 7, 1, 5, 9, 3, 2, 6, 1, 5, 5, 5), (6, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((5, 1, 0, 0), (5, 5, 1, 3, 0, 0, 6, 8, 6, 9, 5, 5), (5, 1, 5, 5, 5, 5, 1, 5, 5, 5, 5, 5)),
)

Gaussian = tuple[int, int]
Eisenstein = tuple[int, int]  # a+b*w, where w^2+w+1=0.
Profile = tuple[int, int, int]
BinaryTriple = tuple[int, int, int]
CompressedQpsk = tuple[Gaussian, Gaussian, Gaussian]


def compact_hash(value: object) -> str:
    serialization = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(serialization.encode("ascii")).hexdigest()


def require_hash(label: str, value: object, expected: str) -> str:
    actual = compact_hash(value)
    if expected and actual != expected:
        raise AssertionError(f"{label} hash changed: {actual} != {expected}")
    return actual


def g_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def phase_sum(exponents: Sequence[int]) -> Gaussian:
    total = (0, 0)
    for exponent in exponents:
        total = g_add(total, ROOTS[exponent])
    return total


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] + right[0], left[1] + right[1]


def e_sub(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return left[0] - right[0], left[1] - right[1]


def e_scale(factor: int, value: Eisenstein) -> Eisenstein:
    return factor * value[0], factor * value[1]


def e_conjugate(value: Eisenstein) -> Eisenstein:
    """Conjugate ``a+b*w`` using ``conjugate(w)=w^2=-1-w``."""

    a, b = value
    return a - b, -b


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_norm(value: Eisenstein) -> int:
    a, b = value
    return a * a - a * b + b * b


def profiles() -> tuple[Profile, ...]:
    """Return all three-part compositions of three in lexicographic order."""

    result = tuple(
        (first, second, 3 - first - second)
        for first in range(4)
        for second in range(4)
        if 0 <= 3 - first - second <= 3
    )
    if len(result) != 10:
        raise AssertionError("the ternary profile catalog must have size ten")
    return result


PROFILES = profiles()


def normalized_binary_triple(profile: Profile) -> BinaryTriple:
    """Compress a plus-weight-three sign word into its three residue sums."""

    return tuple(2 * count - 3 for count in profile)  # type: ignore[return-value]


def profile_eisenstein(profile: Profile) -> Eisenstein:
    """Return ``p0+p1*w+p2*w^2`` in the basis ``1,w``."""

    first, second, third = profile
    return first - third, second - third


def binary_to_eisenstein(values: BinaryTriple) -> Eisenstein:
    """Return one half of the nontrivial Z/3 Fourier coefficient."""

    if (values[0] - values[2]) % 2 or (values[1] - values[2]) % 2:
        raise AssertionError("binary compression differences must be even")
    return (
        (values[0] - values[2]) // 2,
        (values[1] - values[2]) // 2,
    )


def actual_binary_triples(
    class_index: int,
    a_profile: Profile,
    b_profile: Profile,
) -> tuple[BinaryTriple, BinaryTriple]:
    """Undo the alternating high-weight binary complementations."""

    parity_sign = 1 if class_index % 2 == 0 else -1
    normalized_a = normalized_binary_triple(a_profile)
    normalized_b = normalized_binary_triple(b_profile)
    # A is complemented in even classes; B is complemented in odd classes.
    actual_a = tuple(-parity_sign * value for value in normalized_a)
    actual_b = tuple(parity_sign * value for value in normalized_b)
    return actual_a, actual_b  # type: ignore[return-value]


def qpsk_compression_from_binary(
    a_values: BinaryTriple,
    b_values: BinaryTriple,
) -> CompressedQpsk:
    result = []
    for a_value, b_value in zip(a_values, b_values, strict=True):
        if (a_value + b_value) % 2 or (b_value - a_value) % 2:
            raise AssertionError("binary sums did not produce Gaussian integers")
        result.append(
            ((a_value + b_value) // 2, (b_value - a_value) // 2)
        )
    return tuple(result)  # type: ignore[return-value]


def profile_lift_count(profile: Profile) -> int:
    return comb(3, profile[0]) * comb(3, profile[1]) * comb(3, profile[2])


def verify_profile_factorization() -> dict[str, object]:
    profile_data = tuple(
        (
            profile,
            normalized_binary_triple(profile),
            profile_eisenstein(profile),
            e_norm(profile_eisenstein(profile)),
            profile_lift_count(profile),
        )
        for profile in PROFILES
    )
    profile_hash = require_hash(
        "ten-state profile catalog", profile_data, EXPECTED_PROFILE_HASH
    )

    norm_histogram = Counter(entry[3] for entry in profile_data)
    if norm_histogram != Counter({3: 6, 9: 3, 0: 1}):
        raise AssertionError("the profile norm census changed")
    if sum(profile_lift_count(profile) for profile in PROFILES) != 84:
        raise AssertionError("profile lift counts no longer total C(9,3)")

    state_sets: list[set[CompressedQpsk]] = []
    multiplicities: list[Counter[CompressedQpsk]] = []
    multiplicity_histograms: list[Counter[int]] = []
    for parity in (0, 1):
        states: set[CompressedQpsk] = set()
        counts: Counter[CompressedQpsk] = Counter()
        for a_profile in PROFILES:
            for b_profile in PROFILES:
                actual_a, actual_b = actual_binary_triples(
                    parity, a_profile, b_profile
                )
                compressed = qpsk_compression_from_binary(actual_a, actual_b)
                states.add(compressed)
                counts[compressed] += (
                    profile_lift_count(a_profile)
                    * profile_lift_count(b_profile)
                )
        if len(states) != 100 or len(counts) != 100:
            raise AssertionError("a parity catalog did not have 100 states")
        if sum(counts.values()) != 7_056:
            raise AssertionError("a parity catalog did not have 7,056 lifts")
        expected_phase = (0, -3 if parity == 0 else 3)
        for compressed in states:
            total = tuple(
                sum(value[coordinate] for value in compressed)
                for coordinate in (0, 1)
            )
            if total != expected_phase:
                raise AssertionError("a compressed state has the wrong phase sum")
        state_sets.append(states)
        multiplicities.append(counts)
        multiplicity_histograms.append(Counter(counts.values()))

    expected_histogram = Counter(
        {1: 9, 9: 36, 27: 6, 81: 36, 243: 12, 729: 1}
    )
    if any(histogram != expected_histogram for histogram in multiplicity_histograms):
        raise AssertionError("the 100-state lift-multiplicity census changed")

    # Conjugation changes -3i to +3i and bijects the two catalogs.
    conjugated_even = {
        tuple((real, -imag) for real, imag in state)
        for state in state_sets[0]
    }
    if conjugated_even != state_sets[1]:
        raise AssertionError("the two parity catalogs are not conjugate")

    multiplicity_payload = tuple(
        sorted((count, number) for count, number in histogram.items())
        for histogram in multiplicity_histograms
    )
    multiplicity_hash = require_hash(
        "state lift multiplicities",
        multiplicity_payload,
        EXPECTED_STATE_MULTIPLICITY_HASH,
    )
    return {
        "profile_hash": profile_hash,
        "profiles": len(PROFILES),
        "profile_norm_histogram": tuple(sorted(norm_histogram.items())),
        "compressed_states_per_parity": tuple(map(len, state_sets)),
        "word_lifts_per_parity": tuple(sum(c.values()) for c in multiplicities),
        "state_multiplicity_histogram": tuple(
            tuple(sorted(histogram.items()))
            for histogram in multiplicity_histograms
        ),
        "state_multiplicity_hash": multiplicity_hash,
    }


def cyclotomic_classes() -> tuple[tuple[int, ...], ...]:
    subgroup = tuple(pow(PRIMITIVE_ROOT, 12 * exponent, P) for exponent in range(3))
    if subgroup != (1, 26, 10):
        raise AssertionError("the order-three subgroup changed")
    classes = tuple(
        tuple((pow(PRIMITIVE_ROOT, index, P) * value) % P for value in subgroup)
        for index in range(CLASS_COUNT)
    )
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("the cyclotomic classes do not partition F_37^*")
    for index, part in enumerate(classes):
        if {(-value) % P for value in part} != set(classes[(index + 6) % 12]):
            raise AssertionError("class negation no longer shifts by six")
    return classes


CLASSES = cyclotomic_classes()
CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}


def cyclic_inner(left: BinaryTriple, right: BinaryTriple, lag: int) -> int:
    return sum(left[index] * right[(index + lag) % 3] for index in range(3))


def verify_local_fourier_identity() -> dict[str, object]:
    """Exhaust the bilinear identity behind the Eisenstein reduction."""

    zero_a: BinaryTriple = (-1, 1, 1)
    zero_b: BinaryTriple = (3, -1, -1)
    alphabet = {zero_a, zero_b}
    for profile in PROFILES:
        normalized = normalized_binary_triple(profile)
        alphabet.add(normalized)
        alphabet.add(tuple(-value for value in normalized))

    checks = 0
    for left, right in product(sorted(alphabet), repeat=2):
        c0, c1, c2 = (
            cyclic_inner(left, right, lag) for lag in range(3)
        )
        product_value = e_multiply(
            binary_to_eisenstein(left),
            e_conjugate(binary_to_eisenstein(right)),
        )
        if e_scale(4, product_value) != (c0 - c1, c2 - c1):
            raise AssertionError("the local Z/3 Fourier identity failed")
        checks += 1

    if binary_to_eisenstein(zero_a) != (-1, 0):
        raise AssertionError("the A zero column must map to -1")
    if binary_to_eisenstein(zero_b) != (2, 0):
        raise AssertionError("the B zero column must map to 2")
    return {"local_vectors": len(alphabet), "bilinear_checks": checks}


def fixed_row_total_sequences() -> tuple[tuple[int, ...], tuple[int, ...]]:
    a_values = [1]
    b_values = [1]
    for column in range(1, P):
        class_index = CLASS_OF[column]
        a_value = 3 if class_index % 2 == 0 else -3
        a_values.append(a_value)
        b_values.append(-a_value)
    return tuple(a_values), tuple(b_values)


def periodic_scalar_correlation(
    left: Sequence[int], right: Sequence[int], lag: int
) -> int:
    return sum(
        left[index] * right[(index + lag) % len(left)]
        for index in range(len(left))
    )


def verify_equation_reduction() -> dict[str, object]:
    """Verify the fixed k=0 channel and count the independent equations."""

    a_values, b_values = fixed_row_total_sequences()
    fixed_correlations = tuple(
        periodic_scalar_correlation(a_values, a_values, lag)
        + periodic_scalar_correlation(b_values, b_values, lag)
        for lag in range(P)
    )
    if fixed_correlations != (650,) + (-18,) * 36:
        raise AssertionError("the fixed row-total autocorrelation changed")

    # If R=((D0-D1)+(D2-D1)w)/4 and D0+D1+D2=K, solve the
    # resulting three linear equations at zero and nonzero column lag.
    def solve_d(k_total: int, r_value: Eisenstein) -> tuple[int, int, int]:
        x, y = e_scale(4, r_value)
        # D0=D1+x, D2=D1+y, so K=3*D1+x+y.
        numerator = k_total - x - y
        if numerator % 3:
            raise AssertionError("the Fourier equations did not have an integer lift")
        d1 = numerator // 3
        return d1 + x, d1, d1 + y

    zero_binary = solve_d(650, (167, 0))
    nonzero_binary = solve_d(-18, (0, 0))
    if zero_binary != (662, -6, -6):
        raise AssertionError("the origin binary targets changed")
    if nonzero_binary != (-6, -6, -6):
        raise AssertionError("the nonzero binary targets changed")
    if tuple(value // 2 for value in zero_binary) != (331, -3, -3):
        raise AssertionError("the origin QPSK targets changed")
    if tuple(value // 2 for value in nonzero_binary) != (-3, -3, -3):
        raise AssertionError("the nonzero QPSK targets changed")

    original_reversal_independent = 2 + 6 + 12
    independent_eisenstein = 1 + 2 * 6
    dependencies = original_reversal_independent - independent_eisenstein
    if (original_reversal_independent, independent_eisenstein, dependencies) != (
        20,
        13,
        7,
    ):
        raise AssertionError("the independent-equation count changed")
    return {
        "fixed_k0_profile": fixed_correlations,
        "original_reversal_independent_equations": original_reversal_independent,
        "independent_integer_equations": independent_eisenstein,
        "linear_dependencies": dependencies,
        "eisenstein_target": ((0, (167, 0)), ("nonzero", (0, 0))),
        "binary_targets": (zero_binary, nonzero_binary),
        "qpsk_targets": (
            tuple(value // 2 for value in zero_binary),
            tuple(value // 2 for value in nonzero_binary),
        ),
    }


def parse_row_sum(row: dict[str, str]) -> tuple[Gaussian, ...]:
    return tuple(
        (int(row[f"s{index}_real"]), int(row[f"s{index}_imag"]))
        for index in range(ROWS)
    )


def zero_gaussian_word() -> tuple[Gaussian, ...]:
    return tuple(ROOTS[exponent] for exponent in CANONICAL_ZERO_EXPONENTS)


def aggregate_t(row_sum: Sequence[Gaussian]) -> CompressedQpsk:
    zero = zero_gaussian_word()
    t_values = []
    for value, zero_value in zip(row_sum, zero, strict=True):
        difference = value[0] - zero_value[0], value[1] - zero_value[1]
        if difference[0] % 3 or difference[1] % 3:
            raise AssertionError("a row-sum word is not congruent to the zero word")
        t_values.append((difference[0] // 3, difference[1] // 3))
    return tuple(
        tuple(
            sum(t_values[index][coordinate] for index in range(residue, 9, 3))
            for coordinate in (0, 1)
        )
        for residue in range(3)
    )  # type: ignore[return-value]


def class_binary_aggregates(
    aggregate: CompressedQpsk,
) -> tuple[BinaryTriple, BinaryTriple]:
    a_values = tuple(real - imag for real, imag in aggregate)
    b_values = tuple(real + imag for real, imag in aggregate)
    return a_values, b_values  # type: ignore[return-value]


def verify_t_shards(catalog_path: Path | None = None) -> dict[str, object]:
    path = (
        catalog_path
        if catalog_path is not None
        else Path(__file__).resolve().parent / CATALOG_RELATIVE_PATH
    )
    payload = path.read_bytes()
    actual_catalog_hash = sha256(payload).hexdigest()
    if actual_catalog_hash != CATALOG_SHA256:
        raise AssertionError("the row-sum catalog byte hash changed")

    rows = list(csv.DictReader(payload.decode("ascii").splitlines()))
    if len(rows) != CATALOG_DATA_ROWS:
        raise AssertionError("the row-sum catalog row count changed")
    shard_counts = Counter(aggregate_t(parse_row_sum(row)) for row in rows)
    if len(shard_counts) != 22:
        raise AssertionError("the row-sum catalog must collapse to 22 T shards")

    zero_a: BinaryTriple = (-1, 1, 1)
    zero_b: BinaryTriple = (3, -1, -1)
    shard_payload = []
    norm_pairs: Counter[tuple[int, int]] = Counter()
    class_eisenstein_targets: set[tuple[int, int, int, int]] = set()
    for aggregate, count in sorted(shard_counts.items()):
        class_a, class_b = class_binary_aggregates(aggregate)
        class_eisenstein_a = binary_to_eisenstein(class_a)
        class_eisenstein_b = binary_to_eisenstein(class_b)
        class_eisenstein_targets.add(
            (*class_eisenstein_a, *class_eisenstein_b)
        )
        full_a = tuple(zero_a[index] + 3 * class_a[index] for index in range(3))
        full_b = tuple(zero_b[index] + 3 * class_b[index] for index in range(3))
        eisenstein_a = binary_to_eisenstein(full_a)
        eisenstein_b = binary_to_eisenstein(full_b)
        norm_pair = e_norm(eisenstein_a), e_norm(eisenstein_b)
        if sum(norm_pair) != 167:
            raise AssertionError("a T shard lost the norm-167 condition")
        norm_pairs[norm_pair] += 1
        shard_payload.append(
            (
                aggregate,
                count,
                class_a,
                class_b,
                eisenstein_a,
                eisenstein_b,
                norm_pair,
            )
        )

    expected_norm_pairs = Counter(
        {
            (19, 148): 4,
            (28, 139): 4,
            (64, 103): 2,
            (91, 76): 8,
            (100, 67): 2,
            (163, 4): 2,
        }
    )
    if norm_pairs != expected_norm_pairs:
        raise AssertionError("the 22-shard norm-pair census changed")
    if len(class_eisenstein_targets) != 22:
        raise AssertionError("the T shards lost distinct Eisenstein join keys")
    shard_hash = require_hash(
        "22 aggregate T shards", tuple(shard_payload), EXPECTED_T_SHARD_HASH
    )
    return {
        "catalog_sha256": actual_catalog_hash,
        "catalog_rows": len(rows),
        "aggregate_shards": len(shard_counts),
        "shard_size_multiset": tuple(sorted(shard_counts.values())),
        "norm_pair_census": tuple(sorted(norm_pairs.items())),
        "class_eisenstein_targets": tuple(sorted(class_eisenstein_targets)),
        "shard_hash": shard_hash,
    }


def e_mod3(value: Eisenstein) -> Eisenstein:
    return value[0] % 3, value[1] % 3


def pair_signature(left: Profile, right: Profile) -> Eisenstein:
    return e_mod3(
        e_add(e_conjugate(profile_eisenstein(left)), profile_eisenstein(right))
    )


def signed_profile_value(
    channel: int, class_index: int, profile_id: int
) -> Eisenstein:
    if channel not in (0, 1):
        raise ValueError("channel must be zero for A or one for B")
    if not 0 <= profile_id < len(PROFILES):
        raise ValueError("profile ID is outside the ten-state catalog")
    epsilon = 1 if class_index % 2 == 0 else -1
    factor = -epsilon if channel == 0 else epsilon
    return e_scale(factor, profile_eisenstein(PROFILES[profile_id]))


def verify_mod3_pair_sieve(
    expected_targets: Sequence[tuple[int, int, int, int]] | None = None,
) -> dict[str, object]:
    """Replay the local necessary condition on each pair C_s,-C_s."""

    profile_values = tuple(profile_eisenstein(profile) for profile in PROFILES)
    for value in profile_values:
        # Modulo (1-w), w=1, so divisibility is a+b == 0 (mod 3).
        if sum(value) % 3:
            raise AssertionError("a profile coefficient is not divisible by 1-w")
    for left, right in product(profile_values, repeat=2):
        value = e_multiply(left, e_conjugate(right))
        if value[0] % 3 or value[1] % 3:
            raise AssertionError("a nonzero/nonzero product is not divisible by 3")

    signatures = Counter(
        pair_signature(left, right)
        for left, right in product(PROFILES, repeat=2)
    )
    expected_signatures = Counter({(0, 0): 34, (1, 2): 33, (2, 1): 33})
    if signatures != expected_signatures:
        raise AssertionError("the mod-3 pair-signature census changed")

    allowed = 0
    for a_left, a_right, b_left, b_right in product(PROFILES, repeat=4):
        if pair_signature(a_left, a_right) == pair_signature(b_left, b_right):
            allowed += 1
    if allowed != 3_334:
        raise AssertionError("the mod-3 negation-pair survivor count changed")
    if allowed != sum(count * count for count in signatures.values()):
        raise AssertionError("the pair-join count disagrees with direct enumeration")

    raw_six_pair_space = 10**24
    sieved_six_pair_space = allowed**6
    mod3_payload = (
        tuple(sorted(signatures.items())),
        allowed,
        raw_six_pair_space,
        sieved_six_pair_space,
    )
    mod3_hash = require_hash(
        "mod-3 pair sieve", mod3_payload, EXPECTED_MOD3_PAIR_HASH
    )

    witness_targets: set[tuple[int, int, int, int]] = set()
    for target, a_ids, b_ids in MOD3_SHARD_WITNESSES:
        if len(a_ids) != CLASS_COUNT or len(b_ids) != CLASS_COUNT:
            raise AssertionError("a mod-3 shard witness has the wrong length")
        if target in witness_targets:
            raise AssertionError("the mod-3 shard witness table has a duplicate")
        witness_targets.add(target)

        total_a = (0, 0)
        total_b = (0, 0)
        total_norm = 0
        for class_index in range(CLASS_COUNT):
            total_a = e_add(
                total_a,
                signed_profile_value(0, class_index, a_ids[class_index]),
            )
            total_b = e_add(
                total_b,
                signed_profile_value(1, class_index, b_ids[class_index]),
            )
            total_norm += e_norm(profile_eisenstein(PROFILES[a_ids[class_index]]))
            total_norm += e_norm(profile_eisenstein(PROFILES[b_ids[class_index]]))
        if (*total_a, *total_b) != target:
            raise AssertionError("a mod-3 shard witness has the wrong aggregate")
        if total_norm != 54:
            raise AssertionError("a mod-3 shard witness has the wrong origin energy")

        for class_index in range(6):
            a_signature = pair_signature(
                PROFILES[a_ids[class_index]],
                PROFILES[a_ids[class_index + 6]],
            )
            b_signature = pair_signature(
                PROFILES[b_ids[class_index]],
                PROFILES[b_ids[class_index + 6]],
            )
            if a_signature != b_signature:
                raise AssertionError("a shard witness fails the local mod-3 sieve")

    if expected_targets is None:
        expected_targets = verify_t_shards()["class_eisenstein_targets"]
    if witness_targets != set(expected_targets):
        raise AssertionError("the mod-3 witnesses do not cover exactly the 22 T shards")
    witness_hash = require_hash(
        "mod-3 T-shard witnesses",
        MOD3_SHARD_WITNESSES,
        EXPECTED_MOD3_SHARD_WITNESS_HASH,
    )
    return {
        "pair_signatures": tuple(sorted(signatures.items())),
        "raw_choices_per_negation_pair": 10_000,
        "survivors_per_negation_pair": allowed,
        "raw_six_pair_space": raw_six_pair_space,
        "sieved_six_pair_space": sieved_six_pair_space,
        "mod3_hash": mod3_hash,
        "aggregate_shards_surviving": len(witness_targets),
        "shard_witness_hash": witness_hash,
        "is_decisive": False,
    }


def verify_all(catalog_path: Path | None = None) -> dict[str, object]:
    shards = verify_t_shards(catalog_path)
    return {
        "profiles": verify_profile_factorization(),
        "fourier": verify_local_fourier_identity(),
        "equations": verify_equation_reduction(),
        "shards": shards,
        "mod3": verify_mod3_pair_sieve(shards["class_eisenstein_targets"]),
    }


def main() -> None:
    result = verify_all()
    profiles_result = result["profiles"]
    fourier_result = result["fourier"]
    equations_result = result["equations"]
    shards_result = result["shards"]
    mod3_result = result["mod3"]

    print(f"profile_hash={profiles_result['profile_hash']}")
    print(
        "compressed_states_per_parity="
        f"{profiles_result['compressed_states_per_parity']}"
    )
    print(
        "state_multiplicity_hash="
        f"{profiles_result['state_multiplicity_hash']}"
    )
    print(f"local_bilinear_checks={fourier_result['bilinear_checks']}")
    print(
        "equations="
        f"{equations_result['original_reversal_independent_equations']} "
        f"independent={equations_result['independent_integer_equations']} "
        f"dependencies={equations_result['linear_dependencies']}"
    )
    print(f"catalog_sha256={shards_result['catalog_sha256']}")
    print(f"aggregate_shards={shards_result['aggregate_shards']}")
    print(f"norm_pair_census={shards_result['norm_pair_census']}")
    print(f"t_shard_hash={shards_result['shard_hash']}")
    print(f"mod3_pair_signatures={mod3_result['pair_signatures']}")
    print(
        "mod3_pair_survivors="
        f"{mod3_result['survivors_per_negation_pair']}/"
        f"{mod3_result['raw_choices_per_negation_pair']}"
    )
    print(f"mod3_hash={mod3_result['mod3_hash']}")
    print(
        "mod3_aggregate_shards_surviving="
        f"{mod3_result['aggregate_shards_surviving']}/22"
    )
    print(f"mod3_shard_witness_hash={mod3_result['shard_witness_hash']}")
    print("PASS: exact Eisenstein equivalence and mod-3 sieve replayed")
    print("STATUS: necessary-condition reduction only; no LP(333) candidate")


if __name__ == "__main__":
    main()

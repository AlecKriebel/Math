"""Exact helpers for the variable-q special Golay lane at length 167.

Changing both ``s`` and ``q`` removes the fixed-q obstruction.  Splitting at
Eliahou's half-sign involution gives the bijection

    A = s[:84],       B = (s*q)[:84],
    C = s[84:],       D = (s*q)[84:],

between special quadruples and base-sequence candidates ``BS(84, 83)``.
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import permutations, product
from math import prod

from seed import (
    N,
    aperiodic_autocorrelation,
    pointwise,
    special_quadruple,
    summed_aperiodic_correlations,
    validate_sign_sequence,
)


LONG = 84
SHORT = 83


def special_to_base(
    s: Sequence[int], q: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Map a special length-167 pair ``(s,q)`` to ``(A,B,C,D)``."""

    validate_sign_sequence(s, N)
    validate_sign_sequence(q, N)
    sq = pointwise(s, q)
    return tuple(s[:LONG]), tuple(sq[:LONG]), tuple(s[LONG:]), tuple(sq[LONG:])


def base_to_special(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Invert :func:`special_to_base`, returning ``(s,q)``."""

    validate_sign_sequence(a, LONG)
    validate_sign_sequence(b, LONG)
    validate_sign_sequence(c, SHORT)
    validate_sign_sequence(d, SHORT)
    s = tuple(a) + tuple(c)
    q = pointwise(a, b) + pointwise(c, d)
    return s, q


def base_correlations(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[int, ...]:
    """Return the base-sequence norm coefficients at lags 0,...,83."""

    sequences = (a, b, c, d)
    for sequence, length in zip(sequences, (LONG, LONG, SHORT, SHORT), strict=True):
        validate_sign_sequence(sequence, length)
    return tuple(
        sum(
            aperiodic_autocorrelation(sequence, lag)
            for sequence in sequences
            if lag < len(sequence)
        )
        for lag in range(LONG)
    )


def correlation_term_product(sequence: Sequence[int], lag: int) -> int:
    """Product of the individual terms in one aperiodic correlation."""

    validate_sign_sequence(sequence)
    if not 0 <= lag <= len(sequence):
        raise ValueError("lag is out of range")
    return prod(sequence[index] * sequence[index + lag] for index in range(len(sequence) - lag))


def base_term_products(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[int, ...]:
    """Products of all base-correlation terms at lags 0,...,83."""

    sequences = (a, b, c, d)
    return tuple(
        prod(
            correlation_term_product(sequence, lag)
            for sequence in sequences
            if lag <= len(sequence)
        )
        for lag in range(LONG)
    )


def base_quad_products(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return the paired-endpoint products for the two equal-length pairs."""

    for sequence, length in zip((a, b, c, d), (LONG, LONG, SHORT, SHORT), strict=True):
        validate_sign_sequence(sequence, length)
    long_products = tuple(
        a[index] * a[LONG - 1 - index]
        * b[index] * b[LONG - 1 - index]
        for index in range(LONG // 2)
    )
    short_products = tuple(
        c[index] * c[SHORT - 1 - index]
        * d[index] * d[SHORT - 1 - index]
        for index in range(SHORT // 2)
    )
    return long_products, short_products


def endpoint_products_from_quads(
    long_products: Sequence[int], short_products: Sequence[int]
) -> tuple[int, ...]:
    """Express the 83 telescoped endpoint products in the quad basis."""

    if len(long_products) != LONG // 2 or len(short_products) != SHORT // 2:
        raise ValueError("wrong quad-product dimensions")
    result = []
    for lag in range(LONG - 1):
        if lag < SHORT // 2:
            result.append(long_products[lag] * short_products[lag])
        elif lag == SHORT // 2:
            result.append(long_products[lag])
        else:
            reflected = LONG - 2 - lag
            result.append(long_products[reflected + 1] * short_products[reflected])
    return tuple(result)


def is_base_sequence(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> bool:
    correlations = base_correlations(a, b, c, d)
    return correlations[0] == 2 * (LONG + SHORT) and not any(correlations[1:])


def sign_sum(sequence: Sequence[int]) -> int:
    validate_sign_sequence(sequence)
    return sum(sequence)


def alternating_sum(sequence: Sequence[int]) -> int:
    validate_sign_sequence(sequence)
    return sum(value if index % 2 == 0 else -value for index, value in enumerate(sequence))


def globally_alternate(sequence: Sequence[int]) -> tuple[int, ...]:
    """Multiply coordinate ``i`` by ``(-1)^i``."""

    validate_sign_sequence(sequence)
    return tuple(
        value if index % 2 == 0 else -value
        for index, value in enumerate(sequence)
    )


def row_sum_profiles() -> tuple[tuple[int, int, int, int], ...]:
    """Canonical nonnegative row-sum magnitudes forced by evaluation at 1.

    Independent negations make all four sums nonnegative, while exchanging
    the equal-length sequences permits ``a >= b`` and ``c >= d``.
    """

    profiles = []
    for a in range(0, LONG + 1, 2):
        for b in range(0, a + 1, 2):
            for c in range(1, SHORT + 1, 2):
                for d in range(1, c + 1, 2):
                    if a * a + b * b + c * c + d * d == 2 * (LONG + SHORT):
                        profiles.append((a, b, c, d))
    return tuple(profiles)


ROW_SUM_PROFILES = row_sum_profiles()


def compatible_alternating_profiles(
    ordinary: tuple[int, int, int, int],
) -> tuple[tuple[int, int, int, int], ...]:
    """Return the 24 canonical alternating-sum assignments for one shard.

    Reversal of either even-length sequence changes the sign of its
    alternating sum, so its sign is made nonnegative.  Reversal preserves the
    alternating sums of the odd-length sequences, whose two signs remain.
    Coordinate-parity feasibility is imposed before a model is built.
    """

    result: set[tuple[int, int, int, int]] = set()
    for magnitudes in ROW_SUM_PROFILES:
        for even in set(permutations(magnitudes[:2])):
            # Each parity class in a length-84 sequence has 42 terms, so its
            # sign sum is even: (S+T)/2 and (S-T)/2 are both even.
            if any((ordinary[index] - even[index]) % 4 for index in range(2)):
                continue
            for odd_magnitudes in set(permutations(magnitudes[2:])):
                for signs in product((-1, 1), repeat=2):
                    odd = tuple(
                        magnitude * sign
                        for magnitude, sign in zip(odd_magnitudes, signs, strict=True)
                    )
                    # The even and odd coordinate classes of a length-83
                    # sequence have sizes 42 and 41 respectively.
                    if any(
                        (ordinary[index] + odd[index - 2]) % 4
                        for index in (2, 3)
                    ):
                        continue
                    result.add(even + odd)
    return tuple(sorted(result))


def all_margin_shards() -> tuple[
    tuple[tuple[int, int, int, int], tuple[int, int, int, int]], ...
]:
    return tuple(
        (ordinary, alternating)
        for ordinary in ROW_SUM_PROFILES
        for alternating in compatible_alternating_profiles(ordinary)
    )


MARGIN_SHARDS = all_margin_shards()


def canonical_alternated_margins(
    ordinary: tuple[int, int, int, int],
    alternating: tuple[int, int, int, int],
) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    """Canonical margins after globally alternating all four sequences.

    Global alternation exchanges ordinary and alternating sums.  Independent
    negations make the new ordinary sums nonnegative, reversal makes the two
    even-length alternating sums nonnegative, and equal-length sequences are
    reordered by their new ordinary sums.  These are exactly the
    normalizations used to define :data:`MARGIN_SHARDS`.
    """

    if (ordinary, alternating) not in MARGIN_SHARDS:
        raise ValueError("margins do not describe a canonical shard")
    new_ordinary = list(alternating)
    new_alternating = list(ordinary)
    for index in range(4):
        if new_ordinary[index] < 0:
            new_ordinary[index] = -new_ordinary[index]
            new_alternating[index] = -new_alternating[index]
    for index in (0, 1):
        if new_alternating[index] < 0:
            new_alternating[index] = -new_alternating[index]
    for left, right in ((0, 1), (2, 3)):
        if new_ordinary[left] < new_ordinary[right]:
            new_ordinary[left], new_ordinary[right] = (
                new_ordinary[right],
                new_ordinary[left],
            )
            new_alternating[left], new_alternating[right] = (
                new_alternating[right],
                new_alternating[left],
            )
    return tuple(new_ordinary), tuple(new_alternating)


def canonical_alternation_transform(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Apply global alternation and restore the canonical margin chamber."""

    sequences = [tuple(sequence) for sequence in (a, b, c, d)]
    lengths = (LONG, LONG, SHORT, SHORT)
    for sequence, length in zip(sequences, lengths, strict=True):
        validate_sign_sequence(sequence, length)

    ordinary = [sign_sum(sequence) for sequence in sequences]
    alternating = [alternating_sum(sequence) for sequence in sequences]
    transformed = [globally_alternate(sequence) for sequence in sequences]
    new_ordinary = alternating[:]
    new_alternating = ordinary[:]
    for index in range(4):
        if new_ordinary[index] < 0:
            transformed[index] = tuple(-value for value in transformed[index])
            new_ordinary[index] = -new_ordinary[index]
            new_alternating[index] = -new_alternating[index]
    for index in (0, 1):
        if new_alternating[index] < 0:
            transformed[index] = tuple(reversed(transformed[index]))
            new_alternating[index] = -new_alternating[index]
    for left, right in ((0, 1), (2, 3)):
        if new_ordinary[left] < new_ordinary[right]:
            transformed[left], transformed[right] = transformed[right], transformed[left]
            new_ordinary[left], new_ordinary[right] = (
                new_ordinary[right],
                new_ordinary[left],
            )
            new_alternating[left], new_alternating[right] = (
                new_alternating[right],
                new_alternating[left],
            )

    expected = canonical_alternated_margins(tuple(ordinary), tuple(alternating))
    actual = (
        tuple(sign_sum(sequence) for sequence in transformed),
        tuple(alternating_sum(sequence) for sequence in transformed),
    )
    if actual != expected:
        raise AssertionError("canonical alternation margin mismatch")
    return tuple(transformed)  # type: ignore[return-value]


def canonical_margin_transform(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """Restore the sign, reversal, and equal-length margin normalizations."""

    transformed = [tuple(sequence) for sequence in (a, b, c, d)]
    for sequence, length in zip(transformed, (LONG, LONG, SHORT, SHORT), strict=True):
        validate_sign_sequence(sequence, length)
    for index in range(4):
        if sign_sum(transformed[index]) < 0:
            transformed[index] = tuple(-value for value in transformed[index])
    for index in (0, 1):
        if alternating_sum(transformed[index]) < 0:
            transformed[index] = tuple(reversed(transformed[index]))
    for left, right in ((0, 1), (2, 3)):
        if sign_sum(transformed[left]) < sign_sum(transformed[right]):
            transformed[left], transformed[right] = transformed[right], transformed[left]
    return tuple(transformed)  # type: ignore[return-value]


def switch_short_quads(
    c: Sequence[int], d: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Apply Djokovic's norm-preserving BS-quad transposition ``(4 5)``.

    In each paired-endpoint quad of ``(C;D)``, labels 4 and 5 are negatives
    of each other.  The transformation negates every such quad and leaves all
    other quads and the central column unchanged.  Its domain is a pair whose
    endpoint quads all have product ``+1`` (the BS-quad parity condition); on
    that domain it preserves ``N_C + N_D`` exactly.
    """

    validate_sign_sequence(c, SHORT)
    validate_sign_sequence(d, SHORT)
    left = list(c)
    right = list(d)
    for index in range(SHORT // 2):
        reflected = SHORT - 1 - index
        if (
            left[index]
            * left[reflected]
            * right[index]
            * right[reflected]
            != 1
        ):
            raise ValueError("short pair contains a non-BS endpoint quad")
        is_four_or_five = (
            left[index] == -left[reflected]
            and right[index] == -right[reflected]
            and left[index] == -right[index]
        )
        if is_four_or_five:
            left[index] = -left[index]
            left[reflected] = -left[reflected]
            right[index] = -right[index]
            right[reflected] = -right[reflected]
    return tuple(left), tuple(right)


_MARGIN_SHARD_INDEX = {margins: index for index, margins in enumerate(MARGIN_SHARDS)}
ALTERNATION_SHARD_PARTNERS = tuple(
    _MARGIN_SHARD_INDEX[canonical_alternated_margins(ordinary, alternating)]
    for ordinary, alternating in MARGIN_SHARDS
)
MARGIN_SHARD_REPRESENTATIVES = tuple(
    index
    for index, partner in enumerate(ALTERNATION_SHARD_PARTNERS)
    if index <= partner
)
ALTERNATION_FIXED_SHARDS = tuple(
    index
    for index, partner in enumerate(ALTERNATION_SHARD_PARTNERS)
    if index == partner
)


def verify_special_base_identity(s: Sequence[int], q: Sequence[int]) -> None:
    """Check the coefficient identity ``special = 2 * base`` exactly."""

    base = special_to_base(s, q)
    base_values = base_correlations(*base)
    special_values = summed_aperiodic_correlations(special_quadruple(s, q))
    expected = tuple(2 * value for value in base_values) + (0,) * (N - LONG)
    if special_values != expected:
        raise AssertionError("special/base correlation identity failed")


def self_test() -> None:
    if len(ROW_SUM_PROFILES) != 12:
        raise AssertionError(f"expected 12 row-sum profiles, got {len(ROW_SUM_PROFILES)}")
    if len(MARGIN_SHARDS) != 288:
        raise AssertionError(f"expected 288 margin shards, got {len(MARGIN_SHARDS)}")
    if any(len(compatible_alternating_profiles(profile)) != 24 for profile in ROW_SUM_PROFILES):
        raise AssertionError("each ordinary profile should have 24 alternating profiles")
    if len(MARGIN_SHARD_REPRESENTATIVES) != 156:
        raise AssertionError(
            "global alternation should leave exactly 156 shard representatives"
        )
    if len(ALTERNATION_FIXED_SHARDS) != 24:
        raise AssertionError("global alternation should fix exactly 24 shards")
    if any(
        ALTERNATION_SHARD_PARTNERS[partner] != index
        for index, partner in enumerate(ALTERNATION_SHARD_PARTNERS)
    ):
        raise AssertionError("global-alternation shard map is not an involution")
    # Deterministic, non-symmetric data exercise every index in both halves.
    s = tuple(1 if (17 * index + 5) % 29 < 14 else -1 for index in range(N))
    q = tuple(1 if (11 * index + 7) % 31 < 16 else -1 for index in range(N))
    verify_special_base_identity(s, q)
    a, b, c, d = special_to_base(s, q)
    if base_to_special(a, b, c, d) != (s, q):
        raise AssertionError("special/base maps are not inverse")

    # Check every index in the telescoping identity used by the endpoint XORs.
    term_products = base_term_products(a, b, c, d)
    for lag in range(LONG - 1):
        endpoint_product = (
            a[lag]
            * a[LONG - 1 - lag]
            * b[lag]
            * b[LONG - 1 - lag]
            * c[lag]
            * c[SHORT - 1 - lag]
            * d[lag]
            * d[SHORT - 1 - lag]
        )
        if term_products[lag] * term_products[lag + 1] != endpoint_product:
            raise AssertionError(f"term-product telescope failed at lag {lag}")

    # The sparse four-literal quad basis and the original eight-literal
    # endpoint telescope are exactly the same XOR system.  This identity is
    # independent of whether the random fixture satisfies either target.
    long_products, short_products = base_quad_products(a, b, c, d)
    direct_endpoints = tuple(
        a[lag]
        * a[LONG - 1 - lag]
        * b[lag]
        * b[LONG - 1 - lag]
        * c[lag]
        * c[SHORT - 1 - lag]
        * d[lag]
        * d[SHORT - 1 - lag]
        for lag in range(LONG - 1)
    )
    if endpoint_products_from_quads(long_products, short_products) != direct_endpoints:
        raise AssertionError("quad/endpoint product identity failed")

    quad_c = c
    quad_d = list(d)
    for index in range(SHORT // 2):
        reflected = SHORT - 1 - index
        quad_d[reflected] = (
            quad_c[index] * quad_c[reflected] * quad_d[index]
        )
    quad_d = tuple(quad_d)
    switched_c, switched_d = switch_short_quads(quad_c, quad_d)
    if tuple(
        aperiodic_autocorrelation(quad_c, lag)
        + aperiodic_autocorrelation(quad_d, lag)
        for lag in range(SHORT)
    ) != tuple(
        aperiodic_autocorrelation(switched_c, lag)
        + aperiodic_autocorrelation(switched_d, lag)
        for lag in range(SHORT)
    ):
        raise AssertionError("short-pair quad switching changed its norm")
    if switch_short_quads(switched_c, switched_d) != (quad_c, quad_d):
        raise AssertionError("short-pair quad switching is not an involution")


if __name__ == "__main__":
    self_test()
    print(f"PASS special/base identity; {len(ROW_SUM_PROFILES)} profiles; {len(MARGIN_SHARDS)} shards")

#!/usr/bin/env python3
"""Verify the five-comb projective-core-zero obstruction exactly.

This checker is self-contained and uses only the Python standard library.
It proves a row-square obstruction for the normalized projective core

    alpha = beta = u5 = u6 = u7 = 0.

In that core every projective label is 0 or 2.  The corresponding row-sign
vectors force the carrier row sums to have the form ``(x,x,y,y)``.  The
label-independent physical hole fiber then turns the necessary row-square
identity into

    X^2 + (Y+t)^2 = 165 + t^2,       t in {-1,0,1}.

Neither 165 nor 166 is a sum of two integer squares, so the entire core is
impossible.  The argument applies to both the common-word and distinct-lobe
five-comb constructions; it does not assume a particular word inventory.

The checker also reconstructs:

* all 128 normalized projective maps in core zero;
* the exact fixed-physical-fiber lag-81--78 boundary catalog, including the
  eight projected and 288 full rows that the new theorem eliminates; and
* the four possible z=1 carrier-amplitude profiles of all 768,512 normalized
  distinct-lobe paired inventories.
"""

from __future__ import annotations

from bisect import bisect_left
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
from math import isqrt
from typing import Iterable, Sequence


PARAMETER_COUNT = 12
CORE_PARAMETER_COUNT = 5
GAUGE_SIGN_COUNT = 7

EXPECTED_CORE_LABEL_COUNT = 128
EXPECTED_CORE_LABEL_SHA256 = (
    "234ef7430031ac08f814b72a5ddf8d11dfdffbe0f9de68dfe616046945e1305b"
)

EXPECTED_E2_FULL_ROW_COUNT = 10_934
EXPECTED_E2_PARAMETER_ROW_COUNT = 2_434
EXPECTED_E2_FULL_SHA256 = (
    "441c25786c4a0bc56f9e86c84bf9c8c8252595a9f75298aad960c31320aeb6b4"
)
EXPECTED_E2_PARAMETER_SHA256 = (
    "85972db2c71b3e1415705017b0f3f1e57aab3f7cba880104c8f60d83c687d2c0"
)
EXPECTED_E2_CORE_FULL_ROW_COUNT = 288
EXPECTED_E2_CORE_PARAMETER_ROW_COUNT = 8
EXPECTED_E2_CORE_FULL_SHA256 = (
    "4aee0cf4786f3cdf35fd2bdeae8017ba4db461eb29d2a4765c29b45930e4853f"
)
EXPECTED_E2_CORE_PARAMETER_SHA256 = (
    "a6ba346dbf51e2466fc5118cc1a3c0014f93c49eb7f89d5e0211b7e12da13be6"
)

EXPECTED_PAIRED_INVENTORY_COUNT = 768_512
EXPECTED_ROOT_PROFILE_COUNTS = {
    (0, 0, 0, 0, 2, 2, 6, 6): 43_948,
    (0, 0, 0, 2, 2, 2, 2, 8): 38_544,
    (0, 0, 2, 2, 2, 4, 4, 6): 569_956,
    (2, 2, 2, 2, 4, 4, 4, 4): 116_064,
}
EXPECTED_ROOT_PROFILE_SHA256 = (
    "a3191dabf274d25391fd1d1551b4ff8656e2b679530adb4ed0028a66113fecfc"
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
PHI = tuple(sum(vector) for vector in VECTORS)

WORDS = tuple((1,) + tail for tail in product((-1, 1), repeat=4))


def comma_record_hash(rows: Iterable[Sequence[int]]) -> str:
    """Hash comma-separated integer records, each terminated by LF."""

    digest = sha256()
    for row in rows:
        digest.update((",".join(map(str, row)) + "\n").encode())
    return digest.hexdigest()


def canonical_byte_rows_hash(rows: Iterable[Sequence[int]]) -> str:
    """Hash sorted byte rows using the boundary catalog's serialization."""

    canonical = tuple(sorted(tuple(row) for row in rows))
    if not canonical:
        raise ValueError("at least one row is required")
    width = len(canonical[0])
    if any(len(row) != width for row in canonical):
        raise ValueError("rows must have one uniform width")
    if any(
        any(type(value) is not int or not 0 <= value <= 255 for value in row)
        for row in canonical
    ):
        raise ValueError("rows must consist of bytes")
    return sha256(b"".join(bytes(row) for row in canonical)).hexdigest()


def normalized_projective_labels(
    parameters: Sequence[int],
) -> tuple[int, ...]:
    """Evaluate the exact twelve-bit normalized projective parametrization."""

    values = tuple(parameters)
    if len(values) != PARAMETER_COUNT or any(
        value not in (0, 1) for value in values
    ):
        raise ValueError("twelve Boolean projective parameters are required")
    (
        alpha,
        beta,
        u5,
        u6,
        u7,
        y1,
        y2,
        y3,
        y4,
        y5,
        y6,
        y7,
    ) = values
    low = (0, 0, beta, alpha, 0, 0, alpha, beta)
    middle = (0, y1, y2, y3, y4, y5, y6, y7)
    high = (
        0,
        beta ^ u7,
        alpha ^ beta ^ u6,
        alpha ^ u5,
        0,
        u5,
        u6,
        u7,
    )
    return tuple(
        low[slot] + 2 * middle[slot] + 4 * high[slot]
        for slot in range(8)
    )


def core_zero_label_maps() -> tuple[tuple[int, ...], ...]:
    """Return all normalized label maps in structural projective core zero."""

    result = tuple(
        normalized_projective_labels((0, 0, 0, 0, 0, *middle))
        for middle in product((0, 1), repeat=7)
    )
    if result != tuple(sorted(result)):
        raise AssertionError("core-zero labels are not in canonical order")
    return result


def verify_core_zero_labels() -> tuple[int, str]:
    """Verify that core zero is exactly the 128 maps into {V_0,V_2}."""

    labels = core_zero_label_maps()
    if len(labels) != EXPECTED_CORE_LABEL_COUNT or len(set(labels)) != len(
        labels
    ):
        raise AssertionError("the core-zero label count changed")
    expected = tuple(
        (0,) + tuple(2 * bit for bit in middle)
        for middle in product((0, 1), repeat=7)
    )
    if labels != expected:
        raise AssertionError("the sparse core-zero parametrization changed")
    if VECTORS[0] != (1, 1, 1, 1) or VECTORS[2] != (1, 1, -1, -1):
        raise AssertionError("the two core-zero projective vectors changed")
    if any(
        vector[0] != vector[1] or vector[2] != vector[3]
        for vector in (VECTORS[0], VECTORS[2])
    ):
        raise AssertionError("core-zero vectors do not identify the row pairs")
    digest = comma_record_hash(labels)
    if digest != EXPECTED_CORE_LABEL_SHA256:
        raise AssertionError("the core-zero label hash changed")
    return len(labels), digest


def prime_factorization(value: int) -> dict[int, int]:
    """Return the positive integer's exact prime factorization."""

    if value <= 0:
        raise ValueError("a positive integer is required")
    remaining = value
    factor = 2
    result: dict[int, int] = {}
    while factor * factor <= remaining:
        while remaining % factor == 0:
            result[factor] = result.get(factor, 0) + 1
            remaining //= factor
        factor += 1
    if remaining > 1:
        result[remaining] = result.get(remaining, 0) + 1
    return result


def is_sum_of_two_squares(value: int) -> bool:
    """Decide the small nonnegative case directly."""

    if value < 0:
        return False
    squares = {
        integer * integer for integer in range(isqrt(value) + 1)
    }
    return any(value - square in squares for square in squares)


def physical_hole_sums(
    free_signs: Sequence[int],
) -> tuple[int, int, int, int]:
    """Return row sums under the six label-independent hole relations.

    The free signs are ``h0,h1,h2,h3,h8,h9,h10,h12``.  The other signs are

        h4=h0, h5=h1, h6=h2, h7=-h3, h11=h8, h13=h10.
    """

    values = tuple(free_signs)
    if len(values) != 8 or any(value not in (-1, 1) for value in values):
        raise ValueError("eight physical hole signs are required")
    h0, h1, h2, h3, h8, h9, h10, h12 = values
    return (
        h0 + h1 + h2 + h3,
        h0 + h1 + h2 - h3,
        h8 + h9 + h10,
        h8 + h12 + h10,
    )


def verify_row_square_obstruction() -> tuple[int, int]:
    """Verify the exact sum-of-two-squares obstruction and a finite replay."""

    expected_factorizations = {
        165: {3: 1, 5: 1, 11: 1},
        166: {2: 1, 83: 1},
    }
    for value, expected in expected_factorizations.items():
        factors = prime_factorization(value)
        if factors != expected:
            raise AssertionError(f"the factorization of {value} changed")
        if not any(
            prime % 4 == 3 and exponent % 2 == 1
            for prime, exponent in factors.items()
        ):
            raise AssertionError(
                f"{value} lost its sum-of-two-squares obstruction"
            )
        if is_sum_of_two_squares(value):
            raise AssertionError(f"{value} unexpectedly became two squares")

    # Algebraic replay.  If carrier row sums are (x,x,y,y), write the first
    # three common long-row hole signs as a, the common short-row signs as b,
    # and the remaining signs as d,e,f.  Then the four completed row sums are
    # (X+d,X-d,Y+e,Y+f), where X=x+a and Y=y+b.  With
    # t=(e+f)/2, their square sum is
    #
    #   2 * (X^2 + (Y+t)^2 - t^2 + 2).
    #
    # Equality to 334 would force X^2+(Y+t)^2=165+t^2.
    for signs in product((-1, 1), repeat=8):
        h0, h1, h2, h3, h8, h9, h10, h12 = signs
        a = h0 + h1 + h2
        b = h8 + h10
        d, e, f = h3, h9, h12
        t = (e + f) // 2
        if t not in (-1, 0, 1):
            raise AssertionError("the short-hole parameter left {-1,0,1}")
        # Test a few symbolic integer representatives of x and y.
        for x, y in ((0, 0), (7, -9), (-13, 16)):
            row_sums = physical_hole_sums(signs)
            observed = sum(
                value * value
                for value in (
                    x + row_sums[0],
                    x + row_sums[1],
                    y + row_sums[2],
                    y + row_sums[3],
                )
            )
            X, Y = x + a, y + b
            expected = 2 * (X * X + (Y + t) ** 2 - t * t + 2)
            if observed != expected:
                raise AssertionError("the row-square reduction failed")

    # Complete bounded replay for every possible paired-lobe z=1 carrier
    # sum: the largest of the four amplitude profiles has total magnitude 24.
    checks = 0
    closest = 10**9
    for x in range(-24, 25):
        for y in range(-24, 25):
            for signs in product((-1, 1), repeat=8):
                holes = physical_hole_sums(signs)
                energy = sum(
                    value * value
                    for value in (
                        x + holes[0],
                        x + holes[1],
                        y + holes[2],
                        y + holes[3],
                    )
                )
                checks += 1
                closest = min(closest, abs(energy - 334))
                if energy == 334:
                    raise AssertionError("core zero passed the row-square test")
    if checks != 614_656 or closest != 2:
        raise AssertionError("the bounded row-square replay changed")
    return checks, closest


def boundary_equations(
    parameters: Sequence[int],
    gauge_signs: Sequence[int],
) -> tuple[int, int, int, int]:
    """Return the physical e=2 lag-81--78 boundary equations."""

    parameter_values = tuple(parameters)
    sign_values = tuple(gauge_signs)
    if len(parameter_values) != PARAMETER_COUNT or any(
        value not in (0, 1) for value in parameter_values
    ):
        raise ValueError("twelve Boolean parameters are required")
    if len(sign_values) != GAUGE_SIGN_COUNT or any(
        value not in (-1, 1) for value in sign_values
    ):
        raise ValueError("seven gauge signs are required")

    labels = normalized_projective_labels(parameter_values)
    alpha, beta = parameter_values[:2]
    sigma1, sigma2, sigma3, tau4, tau5, tau6, tau7 = sign_values
    e_direction = 2
    return (
        tau7 * PHI[labels[7]]
        + sigma1 * PHI[labels[1] ^ e_direction]
        + 2 * beta * sigma2,
        tau6 * PHI[labels[6]]
        + sigma1 * tau7 * PHI[labels[1] ^ labels[7]]
        + sigma2 * PHI[labels[2] ^ e_direction]
        + 2 * alpha * sigma3,
        tau5 * PHI[labels[5]]
        + sigma1 * tau6 * PHI[labels[1] ^ labels[6]]
        + sigma2 * tau7 * PHI[labels[2] ^ labels[7]]
        + sigma3 * PHI[labels[3] ^ e_direction],
        tau4 * PHI[labels[4]]
        + sigma1 * tau5 * PHI[labels[1] ^ labels[5]]
        + sigma2 * tau6 * PHI[labels[2] ^ labels[6]]
        + sigma3 * tau7 * PHI[labels[3] ^ labels[7]],
    )


def e2_boundary_rows() -> tuple[tuple[int, ...], ...]:
    """Reconstruct the full fixed-physical-fiber high-lag table."""

    result = []
    for parameters in product((0, 1), repeat=PARAMETER_COUNT):
        for sign_bits in product((0, 1), repeat=GAUGE_SIGN_COUNT):
            signs = tuple(-1 if bit else 1 for bit in sign_bits)
            if boundary_equations(parameters, signs) == (0, 0, 0, 0):
                result.append(parameters + sign_bits)
    rows = tuple(result)
    if rows != tuple(sorted(rows)):
        raise AssertionError("the high-lag rows are not canonically ordered")
    return rows


def verify_high_lag_core_zero_counts() -> dict[str, int | str]:
    """Verify exactly how many high-lag rows the theorem removes."""

    full_rows = e2_boundary_rows()
    parameter_rows = tuple(
        sorted({row[:PARAMETER_COUNT] for row in full_rows})
    )
    if len(full_rows) != EXPECTED_E2_FULL_ROW_COUNT:
        raise AssertionError("the e=2 full boundary-row count changed")
    if len(parameter_rows) != EXPECTED_E2_PARAMETER_ROW_COUNT:
        raise AssertionError("the e=2 parameter-row count changed")
    if canonical_byte_rows_hash(full_rows) != EXPECTED_E2_FULL_SHA256:
        raise AssertionError("the e=2 full boundary-row hash changed")
    if canonical_byte_rows_hash(parameter_rows) != EXPECTED_E2_PARAMETER_SHA256:
        raise AssertionError("the e=2 parameter-row hash changed")

    zero_prefix = (0,) * CORE_PARAMETER_COUNT
    core_full = tuple(
        row for row in full_rows if row[:CORE_PARAMETER_COUNT] == zero_prefix
    )
    core_parameters = tuple(
        row
        for row in parameter_rows
        if row[:CORE_PARAMETER_COUNT] == zero_prefix
    )
    if len(core_full) != EXPECTED_E2_CORE_FULL_ROW_COUNT:
        raise AssertionError("the core-zero full boundary count changed")
    if len(core_parameters) != EXPECTED_E2_CORE_PARAMETER_ROW_COUNT:
        raise AssertionError("the core-zero parameter count changed")
    if comma_record_hash(core_full) != EXPECTED_E2_CORE_FULL_SHA256:
        raise AssertionError("the core-zero full boundary hash changed")
    if (
        comma_record_hash(core_parameters)
        != EXPECTED_E2_CORE_PARAMETER_SHA256
    ):
        raise AssertionError("the core-zero parameter hash changed")

    expected_middle = tuple(
        (first, second, third, 1, 1 ^ third, 1 ^ second, 1 ^ first)
        for first, second, third in product((0, 1), repeat=3)
    )
    if tuple(row[CORE_PARAMETER_COUNT:] for row in core_parameters) != (
        expected_middle
    ):
        raise AssertionError("the eight surviving core-zero maps changed")
    return {
        "full_rows": len(full_rows),
        "parameter_rows": len(parameter_rows),
        "core_full_rows": len(core_full),
        "core_parameter_rows": len(core_parameters),
        "core_full_sha256": comma_record_hash(core_full),
        "core_parameter_sha256": comma_record_hash(core_parameters),
    }


def word_signature(word: Sequence[int]) -> tuple[int, ...]:
    """Return the four positive aperiodic correlations of a length-five word."""

    return tuple(
        sum(word[index] * word[index + lag] for index in range(5 - lag))
        for lag in range(1, 5)
    )


def paired_root_profile_counts() -> tuple[Counter[tuple[int, ...]], int]:
    """Classify every self-complementary four-directed-pair inventory."""

    signatures = tuple(map(word_signature, WORDS))
    word_sums = tuple(map(sum, WORDS))
    pair_signatures = tuple(
        tuple(
            signatures[first][lag] + signatures[second][lag]
            for lag in range(4)
        )
        for first in range(16)
        for second in range(16)
    )
    pair_magnitudes = tuple(
        tuple(
            sorted(
                (
                    abs(word_sums[first] + word_sums[second]),
                    abs(word_sums[first] - word_sums[second]),
                )
            )
        )
        for first in range(16)
        for second in range(16)
    )

    by_sum: defaultdict[tuple[int, ...], list[tuple[int, int]]]
    by_sum = defaultdict(list)
    left_states = []
    for first in range(256):
        for second in range(first, 256):
            aggregate = tuple(
                pair_signatures[first][lag] + pair_signatures[second][lag]
                for lag in range(4)
            )
            by_sum[aggregate].append((first, second))
            left_states.append((first, second, aggregate))
    if len(left_states) != 32_896:
        raise AssertionError("the pair-of-pair state count changed")
    for rows in by_sum.values():
        rows.sort()

    profiles: Counter[tuple[int, ...]] = Counter()
    inventory_count = 0
    for first, second, aggregate in left_states:
        complement = tuple(-value for value in aggregate)
        rows = by_sum.get(complement, ())
        start = bisect_left(rows, (second, -1))
        for third, fourth in rows[start:]:
            profile = tuple(
                sorted(
                    pair_magnitudes[first]
                    + pair_magnitudes[second]
                    + pair_magnitudes[third]
                    + pair_magnitudes[fourth]
                )
            )
            profiles[profile] += 1
            inventory_count += 1
    return profiles, inventory_count


def root_profile_hash(profiles: Counter[tuple[int, ...]]) -> str:
    """Hash ``comma-separated-profile:count`` records in profile order."""

    digest = sha256()
    for profile, count in sorted(profiles.items()):
        digest.update(
            (
                ",".join(map(str, profile))
                + ":"
                + str(count)
                + "\n"
            ).encode()
        )
    return digest.hexdigest()


def verify_paired_root_profiles() -> tuple[int, str]:
    """Verify the four exact z=1 paired-lobe amplitude profiles."""

    profiles, inventory_count = paired_root_profile_counts()
    if inventory_count != EXPECTED_PAIRED_INVENTORY_COUNT:
        raise AssertionError("the directed-pair inventory count changed")
    if dict(profiles) != EXPECTED_ROOT_PROFILE_COUNTS:
        raise AssertionError("the four root-profile counts changed")
    if any(sum(value * value for value in profile) != 80 for profile in profiles):
        raise AssertionError("a root profile lost total carrier energy 80")
    digest = root_profile_hash(profiles)
    if digest != EXPECTED_ROOT_PROFILE_SHA256:
        raise AssertionError("the root-profile hash changed")
    return inventory_count, digest


def verify_all() -> dict[str, int | str]:
    """Run every exact reconstruction and return the headline data."""

    core_count, core_hash = verify_core_zero_labels()
    bounded_checks, closest = verify_row_square_obstruction()
    boundary = verify_high_lag_core_zero_counts()
    inventory_count, profile_hash = verify_paired_root_profiles()
    return {
        "core_label_maps": core_count,
        "core_label_sha256": core_hash,
        "bounded_row_square_checks": bounded_checks,
        "closest_row_square_residual": closest,
        **boundary,
        "paired_inventories": inventory_count,
        "root_profile_sha256": profile_hash,
    }


def main() -> None:
    result = verify_all()
    print(
        "PASS: core zero has "
        f"{result['core_label_maps']} normalized projective maps"
    )
    print(
        "PASS: row-square obstruction checked on "
        f"{result['bounded_row_square_checks']} bounded states; "
        f"closest residual {result['closest_row_square_residual']}"
    )
    print(
        "PASS: high-lag catalog "
        f"{result['core_parameter_rows']}/{result['parameter_rows']} "
        "projected core-zero rows and "
        f"{result['core_full_rows']}/{result['full_rows']} full rows"
    )
    print(
        "PASS: four z=1 amplitude profiles classify "
        f"{result['paired_inventories']} paired-lobe inventories"
    )
    print(f"core_label_sha256={result['core_label_sha256']}")
    print(f"core_parameter_sha256={result['core_parameter_sha256']}")
    print(f"core_full_sha256={result['core_full_sha256']}")
    print(f"root_profile_sha256={result['root_profile_sha256']}")


if __name__ == "__main__":
    main()

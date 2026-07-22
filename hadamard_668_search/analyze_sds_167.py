#!/usr/bin/env python3
"""Exact arithmetic audit of cyclic GS/SDS subfamilies at base order 167."""

from __future__ import annotations

from itertools import combinations_with_replacement
from math import isqrt

from good_167 import ORDER, good_row_sum_profiles


def four_square_profiles(n: int = ORDER) -> tuple[tuple[int, int, int, int], ...]:
    """Positive odd row-sum magnitudes with square sum ``4*n``."""

    bound = isqrt(4 * n)
    values = range(1, bound + 1, 2)
    return tuple(
        profile
        for profile in combinations_with_replacement(values, 4)
        if sum(value * value for value in profile) == 4 * n
    )


def gs_parameters_from_row_sums(
    row_sums: tuple[int, int, int, int], n: int = ORDER
) -> tuple[tuple[int, int, int, int], int]:
    """Return canonical block sizes and lambda for a cyclic GS family."""

    sizes = tuple(sorted(((n - abs(value)) // 2 for value in row_sums), reverse=True))
    lam = sum(sizes) - n
    if sum(size * (size - 1) for size in sizes) != lam * (n - 1):
        raise AssertionError("SDS parameter identity failed")
    return sizes, lam


def gs_parameter_sets(n: int = ORDER) -> tuple[tuple[tuple[int, ...], int], ...]:
    return tuple(gs_parameters_from_row_sums(profile, n) for profile in four_square_profiles(n))


def normalized_symmetric_sums(
    magnitudes: tuple[int, int, int, int], n: int = ORDER
) -> tuple[int, int, int, int]:
    """Signs forced by first entry +1 for four symmetric sequences."""

    return tuple(value if value % 4 == n % 4 else -value for value in magnitudes)


def williamson_product_counts(
    magnitudes: tuple[int, int, int, int], n: int = ORDER
) -> tuple[int, int]:
    """Return total negative half-entries and triple-negative positions.

    Williamson's odd-order product theorem requires one or three negative
    signs at every independent coordinate.  If ``M`` is the total number of
    negative half-entries and ``t`` positions have three negatives, then
    ``M=(n-1)/2+2t``.
    """

    signed = normalized_symmetric_sums(magnitudes, n)
    total = sum((n - value) // 4 for value in signed)
    numerator = total - (n - 1) // 2
    if numerator % 2:
        raise AssertionError("Williamson product parity fails")
    triples = numerator // 2
    return total, triples


def common_multiplier_orbit_compatible(
    sizes: tuple[int, ...], subgroup_order: int
) -> bool:
    """Necessary size test for blocks that are unions of multiplier orbits.

    In ``Z_p``, a multiplier subgroup of order ``d`` has nonzero orbits of
    size ``d`` and the singleton orbit ``{0}``.  Hence every block size is
    congruent to zero or one modulo ``d``.
    """

    return all(size % subgroup_order in (0, 1) for size in sizes)


def good_parameter_sets(n: int = ORDER) -> tuple[tuple[tuple[int, ...], int], ...]:
    """Canonical SDS parameters for a skew first block and symmetric rest."""

    result = []
    skew_size = (n - 1) // 2
    for profile in good_row_sum_profiles(n):
        sizes = tuple(
            sorted(
                (skew_size, *((n - abs(value)) // 2 for value in profile)),
                reverse=True,
            )
        )
        lam = sum(sizes) - n
        if sum(size * (size - 1) for size in sizes) != lam * (n - 1):
            raise AssertionError("good SDS parameter identity failed")
        result.append((sizes, lam))
    return tuple(result)


def main() -> None:
    profiles = four_square_profiles()
    parameters = gs_parameter_sets()
    print(f"base_order={ORDER}")
    print(f"cyclic_GS_parameter_count={len(parameters)}")
    for index, (profile, (sizes, lam)) in enumerate(zip(profiles, parameters, strict=True)):
        signed = normalized_symmetric_sums(profile)
        total, triples = williamson_product_counts(profile)
        print(
            f"GS[{index}] rows={profile} sizes={sizes} lambda={lam} "
            f"Williamson_sums={signed} negative_half_total={total} "
            f"triple_positions={triples}"
        )
    print(f"good_parameter_sets={good_parameter_sets()}")
    surviving_83 = tuple(
        index
        for index, (sizes, _lam) in enumerate(parameters)
        if common_multiplier_orbit_compatible(sizes, 83)
    )
    print(f"common_multiplier_order_83_survivors={surviving_83}")


if __name__ == "__main__":
    main()

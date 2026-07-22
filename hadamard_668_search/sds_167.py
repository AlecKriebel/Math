"""Exact helpers for unrestricted cyclic SDS quadruples at order 167.

Four length-``n`` sign sequences with complementary periodic
autocorrelations give a Goethals-Seidel Hadamard matrix of order ``4*n``.
Unlike the good-matrix lane, this route imposes no skew or symmetry condition
on the four sequences.
"""

from __future__ import annotations

from collections.abc import Sequence

from analyze_sds_167 import four_square_profiles
from good_167 import summed_periodic_correlations
from seed import validate_sign_sequence


ORDER = 167
ROW_SUM_PROFILES = four_square_profiles(ORDER)


def validate_cyclic_sds(
    sequences: Sequence[Sequence[int]],
    n: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Return an immutable quadruple or raise unless it is exactly cyclic SDS."""

    if len(sequences) != 4:
        raise ValueError("exactly four sequences are required")
    immutable = tuple(tuple(sequence) for sequence in sequences)
    if n is None:
        n = len(immutable[0])
    if n <= 0 or n % 2 != 1:
        raise ValueError("the cyclic base order must be positive and odd")
    for sequence in immutable:
        validate_sign_sequence(sequence, n)
    profile = tuple(sorted(abs(sum(sequence)) for sequence in immutable))
    if profile not in four_square_profiles(n):
        raise ValueError(f"row-sum magnitudes {profile} violate the four-square equation")
    correlations = summed_periodic_correlations(immutable)
    expected = (4 * n,) + (0,) * (n - 1)
    if correlations != expected:
        bad = tuple(
            index
            for index, value in enumerate(correlations)
            if value != expected[index]
        )
        raise ValueError(f"periodic complementarity fails at lags {bad[:12]}")
    return immutable


if __name__ == "__main__":
    print(f"order={ORDER}")
    print(f"row_sum_profiles={ROW_SUM_PROFILES}")

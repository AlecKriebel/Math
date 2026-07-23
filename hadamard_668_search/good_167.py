"""Exact helpers for the circulant-good-matrix lane at order 167.

A normalized good quadruple consists of four sign sequences ``A,B,C,D`` of
odd length ``n``.  ``A`` is skew (``a[0]=1`` and ``a[-i]=-a[i]``), while
``B,C,D`` are symmetric with first entry one.  Their periodic
autocorrelations sum to ``4*n`` at lag zero and to zero elsewhere.

Such a quadruple gives a skew Hadamard matrix of order ``4*n``.  At ``n=167``
this is a genuinely independent route to ``H(668)``.
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import combinations_with_replacement
from math import isqrt

from seed import validate_sign_sequence


ORDER = 167
HALF = (ORDER - 1) // 2


def periodic_autocorrelation(sequence: Sequence[int], lag: int) -> int:
    """Return the periodic autocorrelation at ``lag`` exactly."""

    validate_sign_sequence(sequence)
    n = len(sequence)
    if n == 0:
        raise ValueError("a nonempty sequence is required")
    lag %= n
    return sum(sequence[index] * sequence[(index + lag) % n] for index in range(n))


def summed_periodic_correlations(
    sequences: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    """Return the summed PAF vector of equal-length sign sequences."""

    if len(sequences) != 4:
        raise ValueError("exactly four sequences are required")
    n = len(sequences[0])
    for sequence in sequences:
        validate_sign_sequence(sequence, n)
    return tuple(
        sum(periodic_autocorrelation(sequence, lag) for sequence in sequences)
        for lag in range(n)
    )


def is_skew(sequence: Sequence[int]) -> bool:
    """Whether ``sequence`` is normalized skew at odd length."""

    validate_sign_sequence(sequence)
    n = len(sequence)
    return n % 2 == 1 and sequence[0] == 1 and all(
        sequence[index] == -sequence[-index] for index in range(1, (n + 1) // 2)
    )


def is_symmetric(sequence: Sequence[int]) -> bool:
    """Whether ``sequence`` is normalized symmetric at odd length."""

    validate_sign_sequence(sequence)
    n = len(sequence)
    return n % 2 == 1 and sequence[0] == 1 and all(
        sequence[index] == sequence[-index] for index in range(1, (n + 1) // 2)
    )


def good_row_sum_profiles(n: int = ORDER) -> tuple[tuple[int, int, int], ...]:
    """Canonical signed row sums for normalized symmetric ``B,C,D``.

    Evaluation at the trivial character gives

    ``sum(B)^2 + sum(C)^2 + sum(D)^2 = 4*n - 1``.

    If the first entry of a symmetric odd-length sequence is one, its sum is
    congruent to ``n`` modulo four.  Sorting is safe because ``B,C,D`` may be
    permuted.
    """

    if n <= 0 or n % 2 != 1:
        raise ValueError("n must be a positive odd integer")
    bound = isqrt(4 * n - 1)
    values = tuple(
        value for value in range(-bound, bound + 1) if value % 4 == n % 4
    )
    return tuple(
        profile
        for profile in combinations_with_replacement(values, 3)
        if sum(value * value for value in profile) == 4 * n - 1
    )


GOOD_167_ROW_SUM_PROFILES = good_row_sum_profiles()


def product_theorem_holds(
    a: Sequence[int],
    b: Sequence[int],
    c: Sequence[int],
    d: Sequence[int],
) -> bool:
    """Check the Bright-Dokovic-Kotsireas-Ganesh product theorem.

    In the normalization ``b[0]=c[0]=d[0]=1``, every good quadruple obeys
    ``a[k]*b[k]*c[k]*d[k] == -a[2*k mod n]`` for nonzero ``k``.
    """

    sequences = (a, b, c, d)
    n = len(a)
    for sequence in sequences:
        validate_sign_sequence(sequence, n)
    if b[0] != 1 or c[0] != 1 or d[0] != 1:
        raise ValueError("the normalized product theorem requires b[0]=c[0]=d[0]=1")
    return all(
        a[k] * b[k] * c[k] * d[k] == -a[(2 * k) % n]
        for k in range(1, n)
    )


def validate_good_quadruple(
    sequences: Sequence[Sequence[int]],
    n: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Return an immutable quadruple or raise unless it is exactly good."""

    if len(sequences) != 4:
        raise ValueError("exactly four sequences are required")
    immutable = tuple(tuple(sequence) for sequence in sequences)
    if n is None:
        n = len(immutable[0])
    for sequence in immutable:
        validate_sign_sequence(sequence, n)
    a, b, c, d = immutable
    if not is_skew(a):
        raise ValueError("A is not normalized skew")
    if not all(is_symmetric(sequence) for sequence in (b, c, d)):
        raise ValueError("B, C, and D must be normalized symmetric")
    if not product_theorem_holds(a, b, c, d):
        raise ValueError("the good-matrix product theorem fails")
    correlations = summed_periodic_correlations(immutable)
    expected = (4 * n,) + (0,) * (n - 1)
    if correlations != expected:
        bad = tuple(index for index, value in enumerate(correlations) if value != expected[index])
        raise ValueError(f"periodic complementarity fails at lags {bad[:12]}")
    return immutable


def product_cycle_order(n: int = ORDER) -> int:
    """Order of doubling on nonzero indices modulo sign, for diagnostics."""

    if n <= 1 or n % 2 != 1:
        raise ValueError("n must be odd and greater than one")
    value = 2 % n
    order = 1
    while value not in (1, n - 1):
        value = (2 * value) % n
        order += 1
        if order > n:
            raise ValueError("doubling is not invertible modulo n")
    return order


if __name__ == "__main__":
    print(f"order={ORDER}")
    print(f"row_sum_profiles={GOOD_167_ROW_SUM_PROFILES}")
    print(f"doubling_order_modulo_sign={product_cycle_order()}")

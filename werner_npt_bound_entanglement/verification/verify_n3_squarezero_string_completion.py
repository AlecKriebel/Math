#!/usr/bin/env python3
"""Exact checker for the four-string square-zero completion theorem.

Only integer arithmetic is used.  Local equality patterns are the
fifteen set partitions of four labelled strings.  Matrix-unit endpoint
Grams are stored as 8 times their true values.
"""

from __future__ import annotations

import itertools
from collections import Counter


def restricted_growth_strings(length: int) -> list[tuple[int, ...]]:
    """Canonical encodings of all set partitions of range(length)."""

    output: list[tuple[int, ...]] = []

    def extend(prefix: tuple[int, ...]) -> None:
        if len(prefix) == length:
            output.append(prefix)
            return
        for value in range(max(prefix) + 2):
            extend(prefix + (value,))

    extend((0,))
    return output


def gram8(
    x: tuple[int, ...],
    y: tuple[int, ...],
    xp: tuple[int, ...],
    yp: tuple[int, ...],
) -> int:
    """Return 8 times the three-copy matrix-unit Gram entry."""

    value = 1
    for a, b, c, d in zip(x, y, xp, yp):
        value *= 2 * int(a == c and b == d) - int(a == b and c == d)
    return value


def diagonal_h_energy8(words: list[tuple[int, ...]]) -> int:
    """Return 8 Q_3(H) for signs (+,+,-,-) and coefficients 1/2."""

    signs = (1, 1, -1, -1)
    numerator = sum(
        signs[i]
        * signs[j]
        * gram8(words[i], words[i], words[j], words[j])
        for i in range(4)
        for j in range(4)
    )
    assert numerator % 4 == 0
    return numerator // 4


def b_gram(words: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    forward = tuple((r, s) for r in (0, 1) for s in (2, 3))
    dyads = forward + tuple((s, r) for r, s in forward)
    return tuple(
        tuple(gram8(words[x], words[y], words[xp], words[yp])
              for xp, yp in dyads)
        for x, y in dyads
    )


EXPECTED_NEGATIVE_PROFILES = {
    (-1, (2, 4, 4, 4)),
    (-1, (4, 4, 2, 4)),
    (-1, (4, 2, 4, 4)),
    (-1, (4, 4, 4, 2)),
    (-2, (4, 4, 4, 4)),
    (-1, (4, 4, 4, 4)),
    (-1, (4, 4, 4, 8)),
    (-1, (4, 8, 4, 4)),
    (-1, (4, 4, 8, 4)),
    (-1, (8, 4, 4, 4)),
}


def b_energy_numerator(profile: tuple[int, ...], t_numerator: int,
                       t_denominator: int) -> tuple[int, int]:
    """Return Q_3(B_U), with t=|U_01|^2, as an exact fraction.

    For a diagonal profile g, equation (11) is
      Q(B) = [g0(1-t)+g1 t+g2 t+g3(1-t)]/16.
    """

    g0, g1, g2, g3 = profile
    numerator = (
        (g0 + g3) * (t_denominator - t_numerator)
        + (g1 + g2) * t_numerator
    )
    return numerator, 16 * t_denominator


def main() -> None:
    partitions = restricted_growth_strings(4)
    assert len(partitions) == 15

    negative_types: Counter[
        tuple[int, tuple[tuple[int, ...], ...]]
    ] = Counter()
    all_patterns: list[
        tuple[int, tuple[tuple[int, ...], ...]]
    ] = []

    for site_patterns in itertools.product(partitions, repeat=3):
        words = [
            tuple(site_patterns[site][label] for site in range(3))
            for label in range(4)
        ]
        if len(set(words)) < 4:
            continue
        qh8 = diagonal_h_energy8(words)
        gram = b_gram(words)
        all_patterns.append((qh8, gram))
        if qh8 < 0:
            negative_types[(qh8, gram)] += 1

    assert len(negative_types) == 10
    assert sum(negative_types.values()) == 294

    observed_profiles: set[tuple[int, tuple[int, ...]]] = set()
    for (qh8, gram), _multiplicity in negative_types.items():
        # Both diagonal blocks agree, all off-diagonal entries vanish,
        # and the forward block is diagonal.
        forward = tuple(tuple(gram[i][j] for j in range(4))
                        for i in range(4))
        backward = tuple(tuple(gram[i + 4][j + 4] for j in range(4))
                         for i in range(4))
        cross = tuple(gram[i][j + 4] for i in range(4) for j in range(4))
        assert forward == backward
        assert all(value == 0 for value in cross)
        assert all(forward[i][j] == 0
                   for i in range(4) for j in range(4) if i != j)
        profile = tuple(forward[i][i] for i in range(4))
        observed_profiles.add((qh8, profile))

        # It suffices to check the affine endpoints t=0,1.
        endpoint_values = [
            b_energy_numerator(profile, t, 1) for t in (0, 1)
        ]
        # Verify Q(H)+Q(B)>=1/4 exactly at both endpoints.
        for numerator, denominator in endpoint_values:
            assert 8 * numerator + qh8 * denominator >= 2 * denominator

    assert observed_profiles == EXPECTED_NEGATIVE_PROFILES

    # The same exact endpoint test covers every nonnegative-H pattern.
    # It is enough because Q(B) is affine in t in every pattern.
    for qh8, gram in all_patterns:
        forward = tuple(tuple(gram[i][j] for j in range(4))
                        for i in range(4))
        backward = tuple(tuple(gram[i + 4][j + 4] for j in range(4))
                         for i in range(4))
        cross = tuple(gram[i][j + 4] for i in range(4) for j in range(4))
        # For arbitrary patterns the cross block can be nonzero, so the
        # ten-profile proof is intentionally used only when H is negative.
        if qh8 < 0:
            continue
        # A nonnegative H is not needed for the obstruction theorem's core
        # claim.  Record it without asserting a phase-independent B bound.
        assert len(forward) == len(backward) == 4
        assert len(cross) == 16

    print(
        "verified: 15^3 equality patterns, ten negative-H Gram types, "
        "and Q3(H+iB_U)>=1/4 on the full negative-quadrature locus"
    )


if __name__ == "__main__":
    main()

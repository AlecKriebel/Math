"""Exact length-9 compression profiles for bounded LP(333) fiber searches.

Each entry fixes the nine CRT row sums of A and B.  Every pair has sequence
sums one and combined cyclic PAF ``(594,-74,...,-74)``.  These are necessary
compressed conditions, not Legendre pairs or H(668) certificates.
"""

from __future__ import annotations

from collections.abc import Sequence


ROW_SUM_PROFILES: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...] = (
    (
        (-21, 3, 5, 5, 1, 5, 1, -1, 3),
        (-3, 3, 3, -3, -3, 1, 1, 3, -1),
    ),
    (
        (15, 5, -9, 3, -5, 1, -7, 1, -3),
        (11, 3, -3, 1, -1, -3, -1, -3, -3),
    ),
    (
        (9, 5, 5, 5, -5, 1, -3, -1, -15),
        (7, 3, -3, 3, -1, 1, 3, -9, -3),
    ),
    (
        (11, 9, -13, 1, -5, 1, -1, -3, 1),
        (5, 5, 1, -5, 5, -9, -1, 1, -1),
    ),
    (
        (9, 7, 1, 3, 1, -1, 3, -9, -13),
        (7, 1, -3, 5, -5, 1, -7, 5, -3),
    ),
    (
        (9, 7, -3, -3, -13, -1, 5, 5, -5),
        (7, -1, -5, 5, -5, 5, 1, 1, -7),
    ),
    (
        (11, 7, -9, 5, 3, -7, -5, -5, 1),
        (7, -1, 5, -3, 7, -5, -5, 1, -5),
    ),
    (
        (17, 3, 1, -3, -5, -3, -1, -3, -5),
        (11, -3, -3, -3, 3, 1, 3, -1, -7),
    ),
    (
        (9, 5, -5, 1, -3, -7, 1, -5, 5),
        (7, 3, 3, -13, 1, 7, -7, 3, -3),
    ),
    (
        (15, 3, -5, -5, 1, -7, 1, 1, -3),
        (7, 5, 1, -7, 1, -5, 7, -7, -1),
    ),
    (
        (13, 5, -9, -3, -5, 1, 1, -1, -1),
        (11, -1, 1, 1, -9, -1, 1, 5, -7),
    ),
    (
        (9, 9, 1, -1, -9, 1, -3, 1, -7),
        (9, -5, -5, -1, 5, 1, 7, -1, -9),
    ),
    (
        (11, 5, -3, 5, -11, 1, -3, -1, -3),
        (7, 3, 7, -3, -7, -3, 7, -5, -5),
    ),
    (
        (13, 9, -7, 3, -11, -1, -1, 1, -5),
        (7, -1, -3, -3, 5, 3, 1, -3, -5),
    ),
    (
        (13, 11, -7, -1, -1, 1, -9, 3, -9),
        (5, 3, 3, -1, -3, -1, -1, -5, 1),
    ),
    (
        (11, 7, -5, -1, -3, -5, 7, -15, 5),
        (5, 1, 3, -1, -1, -1, -5, -1, 1),
    ),
    (
        (11, 7, -1, -1, -5, -3, 1, 3, -11),
        (11, 3, 3, -3, -9, 1, -1, 1, -5),
    ),
    (
        (11, 7, 1, -1, -1, -5, 1, -11, -1),
        (9, 1, -7, 3, 3, 1, -7, 5, -7),
    ),
    (
        (11, 9, -3, 3, 3, -3, -1, -9, -9),
        (7, -3, 1, 1, 3, 3, -5, 3, -9),
    ),
    (
        (13, 1, 1, -3, -1, -13, 7, -5, 1),
        (7, 5, -1, -5, -3, 5, 1, -3, -5),
    ),
    (
        (7, 1, 1, -1, -1, -5, 1, -1, -1),
        (5, 3, 1, 3, 3, 1, 3, -21, 3),
    ),
)

EXACT_COMBINED_PAF = (594,) + (-74,) * 8


def cyclic_paf(vector: Sequence[int]) -> tuple[int, ...]:
    """Return the complete integer cyclic PAF of a short vector."""

    length = len(vector)
    if length == 0:
        raise ValueError("a nonempty vector is required")
    return tuple(
        sum(vector[index] * vector[(index + lag) % length]
            for index in range(length))
        for lag in range(length)
    )


def combined_paf(
    profile: tuple[Sequence[int], Sequence[int]],
) -> tuple[int, ...]:
    left, right = map(cyclic_paf, profile)
    return tuple(a + b for a, b in zip(left, right, strict=True))


def plus_counts(row_sums: Sequence[int]) -> tuple[int, ...]:
    if len(row_sums) != 9 or any(
        type(value) is not int or value % 2 == 0 or not -37 <= value <= 37
        for value in row_sums
    ):
        raise ValueError("row sums must be nine odd integers in [-37,37]")
    return tuple((37 + value) // 2 for value in row_sums)


def _image(
    vector: Sequence[int], multiplier: int, reflection: int, shift: int
) -> tuple[int, ...]:
    return tuple(
        vector[(reflection * multiplier * index + shift) % 9]
        for index in range(9)
    )


def canonical_profile(
    a: Sequence[int], b: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Lex-maximize under the 1,944-element compressed profile symmetry."""

    return max(profile_orbit(a, b))


def profile_orbit(
    a: Sequence[int], b: Sequence[int]
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Return the distinct images under the full compressed-profile symmetry."""

    if len(a) != 9 or len(b) != 9:
        raise ValueError("compressed profiles must have length nine")
    images = set()
    for swap in (False, True):
        left, right = (b, a) if swap else (a, b)
        for multiplier in (1, 2, 4):
            for left_reflection in (-1, 1):
                for right_reflection in (-1, 1):
                    for left_shift in range(9):
                        left_image = _image(
                            left, multiplier, left_reflection, left_shift
                        )
                        for right_shift in range(9):
                            right_image = _image(
                                right, multiplier, right_reflection, right_shift
                            )
                            images.add((left_image, right_image))
    return tuple(sorted(images))


def validate_catalog() -> None:
    seen_orbits = set()
    for index, profile in enumerate(ROW_SUM_PROFILES):
        a, b = profile
        plus_counts(a)
        plus_counts(b)
        if sum(a) != 1 or sum(b) != 1:
            raise AssertionError(f"profile {index} has the wrong sequence sum")
        if combined_paf(profile) != EXACT_COMBINED_PAF:
            raise AssertionError(f"profile {index} fails the compressed PAF")
        representative = canonical_profile(a, b)
        if representative in seen_orbits:
            raise AssertionError(f"profile {index} duplicates an earlier orbit")
        seen_orbits.add(representative)


validate_catalog()

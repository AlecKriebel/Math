#!/usr/bin/env python3
"""Verify inversion-structure obstructions for a Legendre pair of length 333.

This checker uses only integer arithmetic and a finite enumeration of the
possible length-three compression entries.  It does not depend on CP-SAT.
"""

from __future__ import annotations


N = 333
COMPRESSION_LENGTH = 3
BLOCK_SIZE = N // COMPRESSION_LENGTH
LP_NONZERO_PAF_SUM = -2


def compressed_energy_target() -> int:
    """Return the combined energy forced after compression modulo three."""

    # The zero PAF of two sign sequences is 2*N.  Among the 111 original
    # lags divisible by three, the other 110 all have combined PAF -2.
    return 2 * N + (BLOCK_SIZE - 1) * LP_NONZERO_PAF_SUM


def symmetric_mod3_compression(parameter: int) -> tuple[int, int, int]:
    """Return the only possible normalized symmetric compression for ``v``.

    Inversion exchanges residue classes 1 and 2 modulo three, so their sums
    are equal to some odd integer ``v``.  Normalization forces residue zero
    to have sum ``1 - 2*v``.
    """

    return (1 - 2 * parameter, parameter, parameter)


def skew_mod3_compression(parameter: int) -> tuple[int, int, int]:
    """Return the normalized inversion-skew compression ``(1,v,-v)``."""

    return (1, parameter, -parameter)


def admissible_compression(compression: tuple[int, int, int]) -> bool:
    """Whether three values can be sums of 111 signs."""

    return all(
        -BLOCK_SIZE <= value <= BLOCK_SIZE and value % 2
        for value in compression
    )


def verify_obstruction() -> int:
    target = compressed_energy_target()
    if target != 446:
        raise AssertionError(f"unexpected mod-3 energy target {target}")

    # A residue class contains 111 signs, so its sum is an odd integer in
    # [-111,111].  Exhaust exactly the admissible compressed cases,
    # independently of the norm certificates below.  In the symmetric case
    # the derived first coordinate 1-2*v supplies an additional range check.
    parameters = range(-BLOCK_SIZE, BLOCK_SIZE + 1, 2)
    compression_types = {
        "symmetric": symmetric_mod3_compression,
        "skew": skew_mod3_compression,
    }
    feasible: list[tuple[str, str, int, int]] = []
    cases_checked = 0
    for left_name, left_compression in compression_types.items():
        for right_name, right_compression in compression_types.items():
            for v in parameters:
                a = left_compression(v)
                if sum(a) != 1:
                    raise AssertionError("normalization identity failed")
                if not admissible_compression(a):
                    continue
                for w in parameters:
                    b = right_compression(w)
                    if sum(b) != 1:
                        raise AssertionError("normalization identity failed")
                    if not admissible_compression(b):
                        continue
                    cases_checked += 1
                    energy = sum(value * value for value in a + b)
                    if energy == target:
                        feasible.append((left_name, right_name, v, w))
    if cases_checked != 28_224:
        raise AssertionError(f"unexpected admissible-case count {cases_checked}")
    if feasible:
        raise AssertionError(f"unexpected inversion-eigen compression: {feasible}")

    # The same contradiction has the compact certificate x^2+y^2=668.
    # Directly enumerate the only relevant square range as a second check.
    square_representations = [
        (x, y)
        for x in range(-26, 27)
        for y in range(-26, 27)
        if x * x + y * y == 668
    ]
    if square_representations:
        raise AssertionError(
            f"668 unexpectedly represented as two squares: {square_representations}"
        )

    if any(
        x * x + y * y == 222
        for x in range(-15, 16)
        for y in range(-15, 16)
    ):
        raise AssertionError("222 unexpectedly represented as two squares")
    if any(
        x * x + 3 * y * y == 667
        for x in range(-26, 27)
        for y in range(-15, 16)
    ):
        raise AssertionError("667 unexpectedly represented by x^2+3y^2")
    return cases_checked


def main() -> int:
    cases_checked = verify_obstruction()
    print("mod3_compressed_energy_target=446")
    print("symmetric_symmetric_certificate=x^2+y^2=668")
    print("skew_skew_certificate=x^2+y^2=222")
    print("mixed_certificate=x^2+3y^2=667")
    print(f"inversion_structured_compression_cases_checked={cases_checked}")
    print("result=two symmetric-or-skew sequences cannot form LP(333)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

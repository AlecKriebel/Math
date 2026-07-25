#!/usr/bin/env python3
"""Intersect the first nonconstant plane-pencil over-code with all quotients.

Input is the canonical dump produced by the promoted exact quotient census:

    census_z37_quotients --dump-canonical > canonical.txt

The expected SHA-256 is frozen in the promoted certificate.  This detached
audit uses only the diagonal profiles, so it is independent of the
matrix-pencil over-code enumerator.  It also checks the 6/3 trace law for
the tiny exceptional residue left by that enumerator.

This is an audit of a formal diagonal over-code.  Surviving assignments are
not projectors, binary circulant blocks, a conference matrix, or H(668).
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
from pathlib import Path
import sys


P = 37
EXPECTED_DUMP_SHA256 = (
    "c5d8765da49deb39c2ff3407b9d0f265e3ca56c1015d5b0075355c53ca60fb5b"
)
DIAGONAL_UPPER_INDICES = (0, 9, 17, 24, 30, 35, 39, 42, 44)

# Exact exceptional words emitted by
# search_first_nonconstant_plane_pencil.cpp for (alpha,beta)=(19,20).
# A one means cyclic coefficient 19 rather than 18.
EXCEPTIONAL_WORDS = {
    18: (
        "010011010000111011110111000010110010",
        "101100101111000100001000111101001101",
    ),
    24: ("011101011100101111111101001110101110",),
    12: ("100010100011010000000010110001010001",),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_canonical_dump(path: Path) -> list[tuple[int, tuple[int, ...]]]:
    data = path.read_bytes()
    require(
        sha256(data).hexdigest() == EXPECTED_DUMP_SHA256,
        "canonical quotient dump hash changed",
    )
    result: list[tuple[int, tuple[int, ...]]] = []
    for line in data.decode().splitlines():
        if not line.startswith("canonical_upper "):
            continue
        fields = line.split()
        class_index = int(fields[1])
        upper = tuple(map(int, fields[2:]))
        require(len(upper) == 45, "canonical upper triangle has wrong size")
        diagonal_degrees = tuple(
            sorted((36 - upper[index]) // 2
                   for index in DIAGONAL_UPPER_INDICES)
        )
        result.append((class_index, diagonal_degrees))
    require(len(result) == 625, "canonical quotient class count changed")
    require(
        [index for index, _ in result] == list(range(1, 626)),
        "canonical quotient class indices changed",
    )
    return result


def quadratic_character(value: int) -> int:
    value %= P
    if value == 0:
        return 0
    return 1 if pow(value, 18, P) == 1 else -1


def trace_compatible_assignments(
    profile: tuple[int, ...],
) -> tuple[int, int]:
    choices = [EXCEPTIONAL_WORDS[weight] for weight in profile]
    positive = 0
    negative = 0
    for assignment in product(*choices):
        incidences = [
            sum(int(word[lag - 1]) for word in assignment)
            for lag in range(1, P)
        ]
        desired_positive = [
            6 if quadratic_character(lag) == 1 else 3
            for lag in range(1, P)
        ]
        desired_negative = [9 - value for value in desired_positive]
        positive += incidences == desired_positive
        negative += incidences == desired_negative
    return positive, negative


def main() -> None:
    path = (
        Path(sys.argv[1])
        if len(sys.argv) == 2
        else Path("/tmp/z37_quotients_canonical.txt")
    )
    require(path.is_file(), f"missing canonical dump: {path}")
    classes = parse_canonical_dump(path)

    all_weight_18 = [
        index for index, profile in classes if set(profile) <= {18}
    ]
    exceptional_14 = [
        index
        for index, profile in classes
        if set(profile) <= {14, 18, 22}
    ]
    exceptional_12 = [
        index
        for index, profile in classes
        if set(profile) <= {12, 18, 24}
    ]
    require(not all_weight_18, "an all-weight-18 quotient appeared")
    require(not exceptional_14, "the 14/18/22 exception gained a quotient")
    require(
        exceptional_12 == [107, 110, 222, 223],
        "the 12/18/24 residual quotient classes changed",
    )

    residual_profiles = {
        profile for index, profile in classes if index in exceptional_12
    }
    require(
        residual_profiles
        == {(12, 12, 18, 18, 18, 18, 18, 24, 24)},
        "the residual quotient diagonal profile changed",
    )
    profile = next(iter(residual_profiles))

    residue_word = "".join(
        "1" if quadratic_character(lag) == 1 else "0"
        for lag in range(1, P)
    )
    require(
        set(EXCEPTIONAL_WORDS[18])
        == {residue_word, "".join("1" if bit == "0" else "0"
                                  for bit in residue_word)},
        "the two weight-18 words are no longer the Paley pair",
    )
    require(
        all(
            sum(map(int, word)) == weight
            for weight, words in EXCEPTIONAL_WORDS.items()
            for word in words
        ),
        "an exceptional word has the wrong weight",
    )
    require(
        all(
            int(left) + int(right) == 1
            for left, right in zip(
                EXCEPTIONAL_WORDS[12][0], EXCEPTIONAL_WORDS[24][0]
            )
        ),
        "weight-12 and weight-24 words stopped being complements",
    )

    positive, negative = trace_compatible_assignments(profile)
    require((positive, negative) == (5, 5), "trace assignment count changed")

    print(f"canonical_dump_sha256={EXPECTED_DUMP_SHA256}")
    print("quotient_classes=625")
    print("all_weight_18_compatible_classes=0")
    print("weight_14_18_22_compatible_classes=0")
    print(
        "weight_12_18_24_compatible_classes="
        + ",".join(map(str, exceptional_12))
    )
    print(
        "symmetric_plane_pencil_compatible_classes="
        + ",".join(map(str, exceptional_12))
    )
    print("residual_diagonal_profile=" + ",".join(map(str, profile)))
    print(f"trace_orientation_plus_assignments_per_class={positive}")
    print(f"trace_orientation_minus_assignments_per_class={negative}")
    print("residual_scope=formal_diagonal_overcode_only")
    print("symmetric_diagonal_overcode_status=RESIDUAL_4_CLASSES")
    print("certificate=PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Dependency-free structural check of the packaged quotient certificate."""

from __future__ import annotations

import hashlib
from pathlib import Path


ORDER = 9
EXPECTED_SHA256 = (
    "c5d8765da49deb39c2ff3407b9d0f265"
    "e3ca56c1015d5b0075355c53ca60fb5b"
)
EXPECTED_SUMMARIES = {
    "rooted_solutions": "7016",
    "orderly_terminal_matrices": "7016",
    "equivalence_classes": "625",
    "self_negative_classes": "3",
    "sign_permutation_classes": "314",
    "all_labelled_matrices": "196560000",
    "diagonal_multisets": "111",
    "zero_diagonal_classes": "0",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expand_upper_triangle(values: tuple[int, ...]) -> list[list[int]]:
    require(len(values) == ORDER * (ORDER + 1) // 2, "wrong triangle size")
    matrix = [[0] * ORDER for _ in range(ORDER)]
    cursor = 0
    for row in range(ORDER):
        for column in range(row, ORDER):
            matrix[row][column] = values[cursor]
            matrix[column][row] = values[cursor]
            cursor += 1
    return matrix


def verify_quotient(matrix: list[list[int]]) -> None:
    require(all(sum(row) == 0 for row in matrix), "nonzero quotient row sum")
    for row in range(ORDER):
        require(
            matrix[row][row] in {-16, -12, -8, -4, 0, 4, 8, 12, 16},
            "invalid diagonal entry",
        )
        for column in range(ORDER):
            value = matrix[row][column]
            if row != column:
                require(value % 2 != 0 and abs(value) <= 15, "invalid off-diagonal")
            product = sum(
                matrix[row][index] * matrix[index][column]
                for index in range(ORDER)
            )
            target = 333 * (row == column) - 37
            require(product == target, "quotient square identity failed")


def main() -> None:
    package = Path(__file__).resolve().parent
    dump_path = package / "z37_quotient_census_canonical_625.txt"
    digest_path = package / "z37_quotient_census_canonical_625.sha256"

    payload = dump_path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    require(digest == EXPECTED_SHA256, "canonical dump SHA-256 mismatch")

    digest_fields = digest_path.read_text(encoding="ascii").split()
    require(
        digest_fields
        == [EXPECTED_SHA256, "z37_quotient_census_canonical_625.txt"],
        "digest sidecar mismatch",
    )

    lines = payload.decode("ascii").splitlines()
    summaries: dict[str, str] = {}
    triangles: list[tuple[int, ...]] = []
    indices: list[int] = []
    for line in lines:
        fields = line.split()
        if not fields:
            continue
        if fields[0] in EXPECTED_SUMMARIES and len(fields) == 2:
            summaries[fields[0]] = fields[1]
        if fields[0] == "canonical_upper":
            require(len(fields) == 47, "malformed canonical_upper record")
            indices.append(int(fields[1]))
            triangles.append(tuple(map(int, fields[2:])))

    require(summaries == EXPECTED_SUMMARIES, "census summaries changed")
    require(indices == list(range(1, 626)), "canonical indices changed")
    require(len(set(triangles)) == 625, "duplicate canonical triangle")

    all_zero_diagonals = 0
    for triangle in triangles:
        matrix = expand_upper_triangle(triangle)
        verify_quotient(matrix)
        all_zero_diagonals += all(matrix[index][index] == 0 for index in range(ORDER))
    require(all_zero_diagonals == 0, "an all-zero quotient diagonal appeared")

    print(
        "package certificate OK:"
        f" sha256={digest}, canonical_classes={len(triangles)},"
        " all_zero_diagonals=0"
    )


if __name__ == "__main__":
    main()

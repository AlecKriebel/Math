#!/usr/bin/env python3
"""Independent exact verifier for the maximal K11 quarter-grid extensions.

The search program is not trusted.  For every selected K11 atom this verifier
reconstructs the complete list of possible additional points from 7^5 exact
basis-correlation rows.  It then checks a clique and a proper coloring of the
resulting compatibility graph with the same cardinality.  Those two elementary
witnesses prove the graph's clique number exactly.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE_PATH = HERE.parent / "direct_k11_triangle_extension.json"
CERTIFICATE_PATH = HERE / "maximal_quarter_grid_extensions.json"
SOURCE_SHA256 = (
    "f02f52aed4d843434ef6b16c31d03e6176f0566d0a9fa12d02b50b0ec0aee54a"
)
CERTIFICATE_SHA256 = (
    "c0d75a0d9422a9aef646d90280c0f0d0d984e9981ac77da1bf0063818d7b2465"
)
SOURCE_SCHEMA = "kissing5.centered_quarter_direct_k11_triangle_extension.v1"
CERTIFICATE_SCHEMA = "kissing5.k11_quarter_grid_maximal_extensions.v1"
EDGE_KEY = "edge_color_indices_lexicographic_pairs_0_to_10"
VALUES = (-4, -3, -2, -1, 0, 1, 2)
VALUE_SET = frozenset(VALUES)
PAIRS11 = tuple(itertools.combinations(range(11), 2))
EXPECTED_ATOMS_REACHING_40 = (
    6,
    7,
    9,
    10,
    18,
    23,
    27,
    41,
    43,
    44,
    47,
    49,
    50,
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Exact fraction-free Bareiss determinant, with row pivoting."""

    size = len(matrix)
    require(size > 0, "empty determinant requested")
    require(
        all(len(row) == size for row in matrix),
        "determinant input is not square",
    )
    work = [list(row) for row in matrix]
    sign = 1
    previous_pivot = 1
    for column in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for other_column in range(column + 1, size):
                numerator = (
                    work[row][other_column] * pivot
                    - work[row][column] * work[column][other_column]
                )
                require(
                    numerator % previous_pivot == 0,
                    "nonintegral Bareiss division",
                )
                work[row][other_column] = numerator // previous_pivot
            work[row][column] = 0
        previous_pivot = pivot
    return sign * work[-1][-1]


def adjugate(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Return the exact adjugate, adj(A)[i,j] = cofactor(A)[j,i]."""

    size = len(matrix)
    require(size >= 2, "adjugate implementation requires size at least two")
    return tuple(
        tuple(
            (-1 if (row + column) % 2 else 1)
            * determinant(
                tuple(
                    tuple(
                        matrix[source_row][source_column]
                        for source_column in range(size)
                        if source_column != row
                    )
                    for source_row in range(size)
                    if source_row != column
                )
            )
            for column in range(size)
        )
        for row in range(size)
    )


def bilinear(
    left: tuple[int, ...],
    matrix: tuple[tuple[int, ...], ...],
    right: tuple[int, ...],
) -> int:
    return sum(
        left[row] * matrix[row][column] * right[column]
        for row in range(len(left))
        for column in range(len(right))
    )


def integer(value: Any, label: str) -> int:
    require(type(value) is int, f"{label} is not an integer")
    return value


def integer_list(value: Any, label: str) -> list[int]:
    require(type(value) is list, f"{label} is not a list")
    return [integer(item, f"{label}[{index}]") for index, item in enumerate(value)]


def reconstruct_gram(atom: dict[str, Any], atom_index: int) -> tuple[
    tuple[tuple[int, ...], ...],
    int,
    tuple[tuple[int, ...], ...],
]:
    require(EDGE_KEY in atom, f"atom {atom_index}: missing edge list")
    edges = integer_list(atom[EDGE_KEY], f"atom {atom_index} edges")
    require(len(edges) == len(PAIRS11), f"atom {atom_index}: wrong edge count")
    require(
        all(0 <= color < len(VALUES) for color in edges),
        f"atom {atom_index}: edge color outside the seven-value grid",
    )
    gram = [[4 if row == column else 0 for column in range(11)] for row in range(11)]
    for (first, second), color in zip(PAIRS11, edges, strict=True):
        gram[first][second] = VALUES[color]
        gram[second][first] = VALUES[color]
    immutable_gram = tuple(tuple(row) for row in gram)
    base = tuple(tuple(row[:5]) for row in immutable_gram[:5])
    leading_minors = tuple(
        determinant(tuple(tuple(base[row][column] for column in range(size)) for row in range(size)))
        for size in range(1, 6)
    )
    require(
        all(value > 0 for value in leading_minors),
        f"atom {atom_index}: first five vertices are not positive definite",
    )
    determinant_base = leading_minors[-1]
    adj = adjugate(base)
    for row in range(5):
        for column in range(5):
            product = sum(base[row][middle] * adj[middle][column] for middle in range(5))
            target = determinant_base if row == column else 0
            require(
                product == target,
                f"atom {atom_index}: adjugate identity failed",
            )
    basis_rows = tuple(tuple(row[:5]) for row in immutable_gram)
    for first in range(11):
        for second in range(11):
            require(
                bilinear(basis_rows[first], adj, basis_rows[second])
                == determinant_base * immutable_gram[first][second],
                (
                    f"atom {atom_index}: source Gram entry ({first},{second}) "
                    "is inconsistent with rank five"
                ),
            )
    return immutable_gram, determinant_base, adj


def enumerate_candidates(
    gram: tuple[tuple[int, ...], ...],
    determinant_base: int,
    adj: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate every unit point having grid correlations to the K11 atom."""

    candidates: list[tuple[int, ...]] = []
    for row in itertools.product(VALUES, repeat=5):
        if bilinear(row, adj, row) != 4 * determinant_base:
            continue
        for vertex in range(5, 11):
            numerator = bilinear(gram[vertex][:5], adj, row)
            if (
                numerator % determinant_base != 0
                or numerator // determinant_base not in VALUE_SET
            ):
                break
        else:
            candidates.append(row)
    return tuple(candidates)


def compatibility_graph(
    candidates: tuple[tuple[int, ...], ...],
    determinant_base: int,
    adj: tuple[tuple[int, ...], ...],
) -> tuple[int, ...]:
    neighbors = [0] * len(candidates)
    for first, row in enumerate(candidates):
        for second in range(first):
            numerator = bilinear(row, adj, candidates[second])
            compatible = (
                numerator % determinant_base == 0
                and numerator // determinant_base in VALUE_SET
            )
            if compatible:
                neighbors[first] |= 1 << second
                neighbors[second] |= 1 << first
    return tuple(neighbors)


def verify_entry(
    source_atom: dict[str, Any],
    entry: dict[str, Any],
    expected_atom_index: int,
) -> dict[str, int]:
    require(type(entry) is dict, f"entry {expected_atom_index} is not an object")
    atom_index = integer(entry.get("atom_index"), f"entry {expected_atom_index} atom index")
    require(atom_index == expected_atom_index, f"entry {expected_atom_index}: atom order mismatch")
    require(
        entry.get("basis_vertex_indices") == [0, 1, 2, 3, 4],
        f"atom {atom_index}: unexpected basis",
    )
    gram, determinant_base, adj = reconstruct_gram(source_atom, atom_index)
    require(
        integer(entry.get("basis_determinant"), f"atom {atom_index} basis determinant")
        == determinant_base,
        f"atom {atom_index}: wrong basis determinant",
    )
    candidates = enumerate_candidates(gram, determinant_base, adj)
    candidate_count = integer(entry.get("candidate_count"), f"atom {atom_index} candidate count")
    require(candidate_count == len(candidates), f"atom {atom_index}: candidate list is incomplete")
    neighbors = compatibility_graph(candidates, determinant_base, adj)

    maximum = integer(
        entry.get("maximum_additional_points"),
        f"atom {atom_index} maximum additional points",
    )
    require(maximum >= 1, f"atom {atom_index}: invalid claimed maximum")
    require(
        integer(entry.get("maximum_total_points"), f"atom {atom_index} maximum total")
        == 11 + maximum,
        f"atom {atom_index}: total does not equal 11 plus the extension",
    )

    colors = integer_list(entry.get("candidate_colors"), f"atom {atom_index} colors")
    require(len(colors) == len(candidates), f"atom {atom_index}: wrong coloring length")
    require(
        all(0 <= color < maximum for color in colors),
        f"atom {atom_index}: color outside the claimed palette",
    )
    require(
        set(colors) == set(range(maximum)),
        f"atom {atom_index}: the claimed palette is not used exactly",
    )
    for first in range(len(candidates)):
        earlier_neighbors = neighbors[first] & ((1 << first) - 1)
        while earlier_neighbors:
            bit = earlier_neighbors & -earlier_neighbors
            second = bit.bit_length() - 1
            require(
                colors[first] != colors[second],
                (
                    f"atom {atom_index}: adjacent candidates {first} and "
                    f"{second} share color {colors[first]}"
                ),
            )
            earlier_neighbors ^= bit

    clique = integer_list(
        entry.get("clique_candidate_indices"),
        f"atom {atom_index} clique",
    )
    require(len(clique) == maximum, f"atom {atom_index}: wrong clique length")
    require(len(set(clique)) == len(clique), f"atom {atom_index}: repeated clique vertex")
    require(
        all(0 <= vertex < len(candidates) for vertex in clique),
        f"atom {atom_index}: clique index outside candidate list",
    )
    for position, first in enumerate(clique):
        for second in clique[:position]:
            require(
                neighbors[first] >> second & 1 == 1,
                f"atom {atom_index}: candidates {first} and {second} are not compatible",
            )
    return {
        "candidate_count": candidate_count,
        "maximum_additional_points": maximum,
        "maximum_total_points": 11 + maximum,
    }


def verify(
    source_path: Path = SOURCE_PATH,
    certificate_path: Path = CERTIFICATE_PATH,
    expected_source_sha256: str = SOURCE_SHA256,
    expected_certificate_sha256: str = CERTIFICATE_SHA256,
) -> dict[str, Any]:
    require(
        file_sha256(source_path) == expected_source_sha256,
        "source K11 certificate SHA-256 mismatch",
    )
    require(
        file_sha256(certificate_path) == expected_certificate_sha256,
        "maximal-extension certificate SHA-256 mismatch",
    )
    source = json.loads(source_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    require(type(source) is dict, "source certificate is not an object")
    require(type(certificate) is dict, "extension certificate is not an object")
    require(source.get("schema") == SOURCE_SCHEMA, "wrong source schema")
    require(certificate.get("schema") == CERTIFICATE_SCHEMA, "wrong certificate schema")
    require(source.get("positive_atom_count") == 51, "source does not contain 51 positive atoms")
    source_atoms = source.get("atoms")
    entries = certificate.get("entries")
    require(type(source_atoms) is list and len(source_atoms) == 51, "wrong source atom count")
    require(type(entries) is list and len(entries) == 51, "wrong extension entry count")
    require(
        certificate.get("source_sha256") == expected_source_sha256,
        "embedded source SHA-256 mismatch",
    )
    require(
        certificate.get("grid_scaled_by_four") == list(VALUES),
        "wrong quarter grid",
    )

    summaries = [
        verify_entry(source_atom, entry, atom_index)
        for atom_index, (source_atom, entry) in enumerate(
            zip(source_atoms, entries, strict=True)
        )
    ]
    totals = [summary["maximum_total_points"] for summary in summaries]
    reaching_40 = tuple(
        index for index, total in enumerate(totals) if total == 40
    )
    require(min(totals) == 18, "unexpected minimum maximal total")
    require(max(totals) == 40, "a selected atom exceeds total size 40")
    require(
        reaching_40 == EXPECTED_ATOMS_REACHING_40,
        "unexpected list of atoms reaching total size 40",
    )
    require(
        certificate.get("minimum_maximum_total_points") == min(totals),
        "wrong summary minimum",
    )
    require(
        certificate.get("maximum_maximum_total_points") == max(totals),
        "wrong summary maximum",
    )
    require(
        certificate.get("atoms_reaching_40") == list(reaching_40),
        "wrong summary list of atoms reaching 40",
    )
    return {
        "status": "PASS",
        "atoms_checked": len(summaries),
        "basis_rows_tested_per_atom": len(VALUES) ** 5,
        "candidate_count_minimum": min(
            summary["candidate_count"] for summary in summaries
        ),
        "candidate_count_maximum": max(
            summary["candidate_count"] for summary in summaries
        ),
        "maximum_additional_points_minimum": min(
            summary["maximum_additional_points"] for summary in summaries
        ),
        "maximum_additional_points_maximum": max(
            summary["maximum_additional_points"] for summary in summaries
        ),
        "maximum_total_points_minimum": min(totals),
        "maximum_total_points_maximum": max(totals),
        "atoms_reaching_40": list(reaching_40),
        "certificate_sha256": expected_certificate_sha256,
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

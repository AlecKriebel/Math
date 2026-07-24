#!/usr/bin/env python3
"""Standard-library exact verifier for the four-feature K6 flag repair."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "psd4_repair_certificate.json"
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CATALOG_SHA256 = (
    "45634e27071b348b66c02b4bbbfe9f23db713d2f3798589cbbd1c3750b0dcb68"
)
DISCOVERY_SHA256 = (
    "196e96f7622716731f8292665982b2bce49b8a8be71a1e101e3dc2e58d73cfbb"
)

PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
LOCAL_PAIRS = tuple(itertools.combinations(range(4), 2))
KERNEL = {
    2: 494,
    3: 9139,
    4: 329004,
}


class VerificationError(Exception):
    """Raised when an exact certificate check fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix) -> Q:
    size = len(matrix)
    work = [[Q(entry) for entry in row] for row in matrix]
    answer = Q(1)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            scale = work[row][column] / pivot_value
            for entry in range(column + 1, size):
                work[row][entry] -= scale * work[column][entry]
    return answer


def rational_rank(matrix) -> int:
    work = [[Q(entry) for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def edge(edges, first, second):
    return edges[PAIR_INDEX6[tuple(sorted((first, second)))]]


def gram(edges):
    matrix = [[4 if row == column else 0 for column in range(6)] for row in range(6)]
    for (first, second), color in zip(PAIRS6, edges):
        value = color - 4
        matrix[first][second] = value
        matrix[second][first] = value
    return tuple(tuple(row) for row in matrix)


def verify_rank_five_psd(edges):
    matrix = gram(edges)
    require(rational_rank(matrix) == 5, "an atom does not have rank five")
    for size in range(1, 7):
        for subset in itertools.combinations(range(6), size):
            principal = tuple(
                tuple(matrix[first][second] for second in subset)
                for first in subset
            )
            require(
                determinant(principal) >= 0,
                f"negative atom principal minor on {subset}",
            )


def feature(edges, first_root, second_root, first, second):
    q = edge(edges, first_root, second_root) - 4
    a = edge(edges, first_root, first) - 4
    b = edge(edges, second_root, first) - 4
    c = edge(edges, first_root, second) - 4
    d = edge(edges, second_root, second) - 4
    e = edge(edges, first, second) - 4
    return (e, e * (a + c), q * e, a * d + c * b)


def atomic_moment(edges):
    matrix = [[0] * 4 for _ in range(4)]
    for first_root, second_root in itertools.permutations(range(6), 2):
        residual = [
            vertex
            for vertex in range(6)
            if vertex not in (first_root, second_root)
        ]
        extensions = tuple(itertools.combinations(range(4), 2))
        values = [
            feature(
                edges,
                first_root,
                second_root,
                residual[first],
                residual[second],
            )
            for first, second in extensions
        ]
        for left, left_extension in enumerate(extensions):
            for right, right_extension in enumerate(extensions):
                coefficient = KERNEL[
                    len(set(left_extension) | set(right_extension))
                ]
                for row in range(4):
                    for column in range(4):
                        matrix[row][column] += (
                            coefficient
                            * values[left][row]
                            * values[right][column]
                        )
    require(
        all(
            matrix[row][column] == matrix[column][row]
            for row in range(4)
            for column in range(4)
        ),
        "atomic moment is not symmetric",
    )
    return tuple(tuple(row) for row in matrix)


def verify_catalog_rows(data):
    catalog = ROOT / data["catalog"]
    require(
        sha256(catalog) == CATALOG_SHA256 == data["catalog_sha256"],
        "catalog hash mismatch",
    )
    wanted = {atom["catalog_index"]: atom for atom in data["atoms"]}
    require(
        len(wanted) == len(data["atoms"]),
        "duplicate catalog index in certificate",
    )
    found = set()
    for index, line in enumerate(catalog.read_text().splitlines()[1:]):
        if index not in wanted:
            continue
        fields = list(map(int, line.split(",")))
        require(
            fields[:15]
            == wanted[index][
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ],
            f"catalog edge data mismatch at row {index}",
        )
        require(
            fields[15:] == wanted[index]["triangle_orbit_indices"],
            f"catalog face data mismatch at row {index}",
        )
        found.add(index)
    require(found == set(wanted), "certificate catalog rows not all found")


def verify(certificate_path=CERTIFICATE):
    data = json.loads(certificate_path.read_text())
    require(
        data["schema"] == "kissing5.global_flag_psd4_repair.v1",
        "unexpected certificate schema",
    )
    source_path = ROOT / data["source_certificate"]
    discovery_path = ROOT / data["discovery_report"]
    require(
        sha256(source_path) == SOURCE_SHA256 == data["source_sha256"],
        "source certificate hash mismatch",
    )
    require(
        sha256(discovery_path)
        == DISCOVERY_SHA256
        == data["discovery_report_sha256"],
        "discovery report hash mismatch",
    )
    verify_catalog_rows(data)

    source = json.loads(source_path.read_text())
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    atoms = data["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    require(all(weight > 0 for weight in weights), "weight is not positive")
    require(sum(weights) == 1, "weights do not sum to one")

    triangle_masses = [Q(0)] * 51
    atomic_matrices = []
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        require(
            len(edges) == 15 and all(0 <= color <= 6 for color in edges),
            "invalid atom edge colors",
        )
        verify_rank_five_psd(edges)

        induced_faces = []
        for vertices in itertools.combinations(range(6), 3):
            colors = tuple(
                sorted(
                    edge(edges, first, second)
                    for first, second in itertools.combinations(vertices, 2)
                )
            )
            induced_faces.append(triple_index[colors])
        require(
            sorted(induced_faces) == atom["triangle_orbit_indices"],
            "stored atom triangle orbits are wrong",
        )
        for face in induced_faces:
            triangle_masses[face] += weight
        atomic_matrices.append(atomic_moment(edges))

    require(
        triangle_masses == [Q(value) / 78 for value in source["nu"]],
        "triangle marginal mismatch",
    )

    moment = tuple(
        tuple(
            sum(
                weight * atomic[row][column]
                for weight, atomic in zip(weights, atomic_matrices)
            )
            for column in range(4)
        )
        for row in range(4)
    )
    expected_moment = tuple(
        tuple(Q(value) for value in row) for row in data["moment_matrix"]
    )
    require(moment == expected_moment, "stored moment matrix mismatch")

    principal_minors = {}
    for size in range(1, 5):
        for subset in itertools.combinations(range(4), size):
            value = determinant(
                tuple(
                    tuple(moment[row][column] for column in subset)
                    for row in subset
                )
            )
            require(
                value > 0,
                f"nonpositive moment principal minor on {subset}",
            )
            principal_minors[",".join(map(str, subset))] = str(value)
    require(
        principal_minors == data["principal_minors"],
        "stored principal minors mismatch",
    )

    old_separator_direction = (8, -3, 0, 0)
    old_separator_value = sum(
        old_separator_direction[row]
        * moment[row][column]
        * old_separator_direction[column]
        for row in range(4)
        for column in range(4)
    )
    require(
        old_separator_value > 0,
        "the old separator direction was not strictly repaired",
    )

    report = {
        "status": "PASS",
        "atoms": len(atoms),
        "minimum_weight": str(min(weights)),
        "rank_five_PSD_atoms": len(atoms),
        "triangle_marginal": "PASS",
        "moment_matrix": "positive definite",
        "old_polynomial_separator_direction_value": str(
            old_separator_value
        ),
        "certificate_sha256": sha256(certificate_path),
    }
    return report


def main():
    require(len(sys.argv) <= 2, "usage: verify_psd4_repair.py [certificate]")
    certificate_path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    print(json.dumps(verify(certificate_path), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

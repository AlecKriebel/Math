#!/usr/bin/env python3
"""Exact verifier for the centered degree-two rooted-edge K6 repair.

Only the Python standard library is used.  All arithmetic after parsing the
certificate is integer or ``fractions.Fraction`` arithmetic.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "centered_degree2_repair_certificate.json"

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CATALOG_SHA256 = (
    "45634e27071b348b66c02b4bbbfe9f23db713d2f3798589cbbd1c3750b0dcb68"
)

FEATURE_NAMES = (
    "1",
    "q",
    "e",
    "a+c",
    "b+d",
    "q^2",
    "q*e",
    "e^2",
    "q*(a+c)",
    "q*(b+d)",
    "e*(a+c)",
    "e*(b+d)",
    "a^2+c^2",
    "b^2+d^2",
    "a*b+c*d",
    "a*c",
    "b*d",
    "a*d+b*c",
)
QUOTIENT_INDICES = (0, 1, 5, 7, 12, 13, 14)


def vector(**entries):
    result = [0] * 18
    for name, value in entries.items():
        result[FEATURE_NAMES.index(name)] = value
    return tuple(result)


CENTERED_KERNELS = (
    vector(**{"1": 152, "q": 38, "a+c": 741}),
    vector(**{"1": 152, "q": 38, "b+d": 741}),
    vector(**{"1": 74, "q": -1, "e": 741}),
    vector(**{"q": 152, "q^2": 38, "q*(a+c)": 741}),
    vector(**{"q": 152, "q^2": 38, "q*(b+d)": 741}),
    vector(**{"q": 74, "q^2": -1, "q*e": 741}),
    vector(
        **{
            "1": -608,
            "q": -304,
            "q^2": -38,
            "a^2+c^2": 741,
            "a*c": 56316,
        }
    ),
    vector(
        **{
            "1": -608,
            "q": -304,
            "q^2": -38,
            "b^2+d^2": 741,
            "b*d": 56316,
        }
    ),
    vector(
        **{
            "1": -608,
            "q": -304,
            "q^2": -38,
            "a*b+c*d": 741,
            "a*d+b*c": 28158,
        }
    ),
    vector(
        **{
            "a+c": 4,
            "e*(a+c)": 38,
            "a^2+c^2": 1,
            "a*b+c*d": 1,
        }
    ),
    vector(
        **{
            "b+d": 4,
            "e*(b+d)": 38,
            "b^2+d^2": 1,
            "a*b+c*d": 1,
        }
    ),
)

PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
KERNEL_BY_UNION_SIZE = {2: 494, 3: 9139, 4: 329004}


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
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [
            entry / pivot_value for entry in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def edge(edges, first, second):
    return edges[PAIR_INDEX6[tuple(sorted((first, second)))]]


def gram(edges):
    matrix = [
        [4 if row == column else 0 for column in range(6)]
        for row in range(6)
    ]
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


def feature(edges, i, j, p, r):
    q = edge(edges, i, j) - 4
    a = edge(edges, i, p) - 4
    b = edge(edges, j, p) - 4
    c = edge(edges, i, r) - 4
    d = edge(edges, j, r) - 4
    e = edge(edges, p, r) - 4
    return (
        1,
        q,
        e,
        a + c,
        b + d,
        q * q,
        q * e,
        e * e,
        q * (a + c),
        q * (b + d),
        e * (a + c),
        e * (b + d),
        a * a + c * c,
        b * b + d * d,
        a * b + c * d,
        a * c,
        b * d,
        a * d + b * c,
    )


def atomic_moment(edges):
    matrix = [[0] * 18 for _ in range(18)]
    for i, j in itertools.permutations(range(6), 2):
        residual = [
            vertex for vertex in range(6) if vertex not in (i, j)
        ]
        extensions = tuple(itertools.combinations(range(4), 2))
        values = [
            feature(
                edges,
                i,
                j,
                residual[first],
                residual[second],
            )
            for first, second in extensions
        ]
        for left, first_extension in enumerate(extensions):
            for right, second_extension in enumerate(extensions):
                coefficient = KERNEL_BY_UNION_SIZE[
                    len(set(first_extension) | set(second_extension))
                ]
                for row in range(18):
                    scaled_left = coefficient * values[left][row]
                    for column in range(18):
                        matrix[row][column] += (
                            scaled_left * values[right][column]
                        )
    require(
        all(
            matrix[row][column] == matrix[column][row]
            for row in range(18)
            for column in range(18)
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
    lines = catalog.read_text().splitlines()
    require(lines[0] == data["catalog_header"], "catalog header mismatch")
    for index, line in enumerate(lines[1:]):
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
        data["schema"] == "kissing5.centered_degree2_flag_repair.v1",
        "unexpected certificate schema",
    )
    require(data["target_cardinality"] == 41, "wrong target cardinality")
    require(data["local_size"] == 6, "wrong local size")
    require(
        tuple(data["feature_names"]) == FEATURE_NAMES,
        "feature basis mismatch",
    )
    require(
        tuple(data["quotient_indices"]) == QUOTIENT_INDICES,
        "quotient indices mismatch",
    )
    require(
        tuple(tuple(row) for row in data["centered_kernel_vectors"])
        == CENTERED_KERNELS,
        "centered kernel vectors mismatch",
    )
    require(
        {
            int(union_size): coefficient
            for union_size, coefficient in data[
                "kernel_by_union_size"
            ].items()
        }
        == KERNEL_BY_UNION_SIZE,
        "exchangeability coefficients mismatch",
    )

    source_path = ROOT / data["source_certificate"]
    require(
        sha256(source_path) == SOURCE_SHA256 == data["source_sha256"],
        "source certificate hash mismatch",
    )
    verify_catalog_rows(data)
    source = json.loads(source_path.read_text())
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    require(len(triple_index) == 51, "wrong number of triangle orbits")

    atoms = data["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    require(len(atoms) == 73, "wrong number of atoms")
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
            for column in range(18)
        )
        for row in range(18)
    )
    expected_moment = tuple(
        tuple(Q(value) for value in row) for row in data["moment_matrix"]
    )
    require(moment == expected_moment, "stored moment matrix mismatch")
    require(
        all(
            moment[row][column] == moment[column][row]
            for row in range(18)
            for column in range(18)
        ),
        "moment matrix is not symmetric",
    )

    # Each centered identity lies in the exact radical of the flag block.
    for kernel in CENTERED_KERNELS:
        for column in range(18):
            require(
                sum(
                    kernel[row] * moment[row][column]
                    for row in range(18)
                )
                == 0,
                "centered kernel does not annihilate the moment",
            )

    coordinate_vectors = []
    for index in QUOTIENT_INDICES:
        coordinate = [0] * 18
        coordinate[index] = 1
        coordinate_vectors.append(tuple(coordinate))
    require(
        rational_rank(CENTERED_KERNELS + tuple(coordinate_vectors)) == 18,
        "kernel and quotient vectors do not span feature space",
    )

    quotient = tuple(
        tuple(moment[row][column] for column in QUOTIENT_INDICES)
        for row in QUOTIENT_INDICES
    )
    require(
        quotient
        == tuple(
            tuple(Q(value) for value in row)
            for row in data["quotient_matrix"]
        ),
        "stored quotient matrix mismatch",
    )
    principal_minors = {}
    for size in range(1, 8):
        for subset in itertools.combinations(range(7), size):
            value = determinant(
                tuple(
                    tuple(quotient[row][column] for column in subset)
                    for row in subset
                )
            )
            require(
                value > 0,
                f"nonpositive quotient principal minor on {subset}",
            )
            principal_minors[",".join(map(str, subset))] = str(value)
    require(
        principal_minors == data["quotient_principal_minors"],
        "stored quotient principal minors mismatch",
    )
    require(rational_rank(moment) == 7, "full moment rank is not seven")

    report = {
        "status": "PASS",
        "atoms": len(atoms),
        "minimum_weight": str(min(weights)),
        "rank_five_PSD_atoms": len(atoms),
        "triangle_marginal": "PASS",
        "centered_kernel_dimension": 11,
        "full_moment_rank": 7,
        "quotient_matrix": "positive definite",
        "certificate_sha256": sha256(certificate_path),
    }
    return report


def main():
    require(
        len(sys.argv) <= 2,
        "usage: verify_centered_degree2_repair.py [certificate]",
    )
    certificate_path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    print(json.dumps(verify(certificate_path), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact verifier for finite-exchangeability rooted flag-square rows.

The search programs that produced the local K6--K11 pseudodistributions are
not imported.  This verifier uses only Python's standard library, authenticates
each input file, and recomputes every reported rational from the stored atoms.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "global_flag_exchangeability_certificate.json"

SOURCES = (
    (
        "direct_K6",
        ROOT
        / "experiments"
        / "centered_quarter_k6_rank"
        / "direct_k6_triangle_extension.json",
        "32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba",
    ),
    (
        "direct_K7",
        ROOT
        / "experiments"
        / "centered_quarter_k6_rank"
        / "k7"
        / "direct_k7_triangle_extension.json",
        "e666aea9882e10b25be7d73bd288a959f3df7bf8dd8f68dc6bb02f2fdf96ce19",
    ),
    (
        "direct_K8",
        ROOT
        / "experiments"
        / "centered_quarter_k6_rank"
        / "k8"
        / "direct_k8_triangle_extension.json",
        "9499977c14f3de72cd0b55d83872a645f2727f120182d010967832106b65b195",
    ),
    (
        "direct_K9",
        ROOT
        / "experiments"
        / "centered_quarter_k6_rank"
        / "k9"
        / "direct_k9_triangle_extension.json",
        "b0ead73d99ea050a002a36bfd78f549348d37d19244c147228bee26ad692b148",
    ),
    (
        "direct_K10",
        ROOT
        / "experiments"
        / "centered_quarter_k6_rank"
        / "k10"
        / "direct_k10_triangle_extension.json",
        "542f3061bfe282d98580955e62e756bfd9646890a45747f0baad8b11f750cc28",
    ),
    (
        "direct_K11",
        ROOT
        / "experiments"
        / "centered_quarter_k6_rank"
        / "k11"
        / "direct_k11_triangle_extension.json",
        "f02f52aed4d843434ef6b16c31d03e6176f0566d0a9fa12d02b50b0ec0aee54a",
    ),
    (
        "K6_product_74",
        ROOT
        / "experiments"
        / "four_point_depth_projection"
        / "k6_product_audit"
        / "productpool_extension.json",
        "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991",
    ),
    (
        "K7_product_53",
        ROOT
        / "experiments"
        / "four_point_depth_projection"
        / "k7_product_audit"
        / "candidate_k7_product_extension.json",
        "1b5e262592e1872cfe9f26b344d82da5066d8332efc5104a34a433d9d5564b00",
    ),
)

EDGE_KEY_PREFIX = "edge_color_indices"


class VerificationError(Exception):
    """Raised when an exact certificate check fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pairs(size: int):
    return tuple(itertools.combinations(range(size), 2))


def infer_size(edge_count: int) -> int:
    size = 0
    while size * (size - 1) // 2 < edge_count:
        size += 1
    require(
        size * (size - 1) // 2 == edge_count,
        "edge count is not triangular",
    )
    return size


def edge_key(atom: dict[str, object]) -> str:
    keys = [key for key in atom if key.startswith(EDGE_KEY_PREFIX)]
    require(len(keys) == 1, "atom does not have one edge-color field")
    return keys[0]


def edge_lookup(edges: tuple[int, ...], size: int):
    return dict(zip(pairs(size), edges))


def edge(
    lookup: dict[tuple[int, int], int], first: int, second: int
) -> int:
    return lookup[tuple(sorted((first, second)))]


def union_sums(
    values: dict[tuple[int, int], int], residual_count: int
) -> tuple[int, int, int]:
    """Return ordered-pair products grouped by union size 2, 3, and 4."""

    degree_two = sum(value * value for value in values.values())
    degree_three = 0
    for triple in itertools.combinations(range(residual_count), 3):
        local = [
            values[tuple(sorted(pair))]
            for pair in itertools.combinations(triple, 2)
        ]
        degree_three += sum(local) ** 2 - sum(value * value for value in local)
    degree_four = 0
    for first, second, third, fourth in itertools.combinations(
        range(residual_count), 4
    ):
        degree_four += 2 * (
            values[first, second] * values[third, fourth]
            + values[first, third] * values[second, fourth]
            + values[first, fourth] * values[second, third]
        )
    return degree_two, degree_three, degree_four


def scaled_polynomial_flag_value(
    lookup: dict[tuple[int, int], int],
    size: int,
    first_root: int,
    second_root: int,
) -> tuple[int, int, int]:
    """Union sums for 16*f, with f=e(2-3(a+c)).

    The quarter grid is represented by the exact scaled values
    ``4*g = -4,-3,...,2``.  Thus

      16*f = (4e) * (8 - 3(4a+4c))

    is integral.
    """

    residual = [
        vertex
        for vertex in range(size)
        if vertex not in (first_root, second_root)
    ]
    values = {}
    for local_first, local_second in itertools.combinations(
        range(size - 2), 2
    ):
        first = residual[local_first]
        second = residual[local_second]
        scaled_e = edge(lookup, first, second) - 4
        scaled_a = edge(lookup, first_root, first) - 4
        scaled_c = edge(lookup, first_root, second) - 4
        values[local_first, local_second] = scaled_e * (
            8 - 3 * (scaled_a + scaled_c)
        )
    return union_sums(values, size - 2)


def evaluate_pseudodistribution(path: Path, expected_hash: str) -> Q:
    """Evaluate the continuous polynomial flag square at N=41 exactly."""

    require(sha256(path) == expected_hash, f"source hash mismatch: {path}")
    data = json.loads(path.read_text())
    atoms = data["atoms"]
    require(
        sum((Q(atom["weight"]) for atom in atoms), Q(0)) == 1,
        f"source weights do not sum to one: {path}",
    )
    key = edge_key(atoms[0])
    size = infer_size(len(atoms[0][key]))
    residual_count = size - 2
    coefficients = {
        union_size: Q(
            math.comb(39, union_size),
            math.comb(residual_count, union_size),
        )
        for union_size in (2, 3, 4)
    }
    total_scaled = Q(0)
    for atom in atoms:
        require(edge_key(atom) == key, "inconsistent atom edge field")
        edges = tuple(atom[key])
        require(
            len(edges) == size * (size - 1) // 2,
            "atom has the wrong edge count",
        )
        lookup = edge_lookup(edges, size)
        atom_sums = [0, 0, 0]
        for first_root, second_root in itertools.permutations(
            range(size), 2
        ):
            for index, value in enumerate(
                scaled_polynomial_flag_value(
                    lookup, size, first_root, second_root
                )
            ):
                atom_sums[index] += value
        atom_value = sum(
            coefficients[union_size] * atom_sums[union_size - 2]
            for union_size in (2, 3, 4)
        )
        total_scaled += Q(atom["weight"]) * atom_value
    # The integer feature used above is 16*f, so its square is 256*f^2.
    return total_scaled / 256


def d5_vectors():
    result = []
    for first, second in itertools.combinations(range(5), 2):
        for first_sign, second_sign in itertools.product((-1, 1), repeat=2):
            vector = [0] * 5
            vector[first] = first_sign
            vector[second] = second_sign
            result.append(tuple(vector))
    require(len(result) == 40, "D5 construction does not have 40 vectors")
    return tuple(result)


def d5_polynomial_square() -> Q:
    """Direct global square on D5, with no sampling or local relaxation."""

    vectors = d5_vectors()

    def scaled_inner(first: int, second: int) -> int:
        # D5 vectors are stored without the factor 1/sqrt(2), so 4<x,y>
        # equals twice their integral dot product.
        return 2 * sum(
            left * right for left, right in zip(vectors[first], vectors[second])
        )

    total_scaled = 0
    for first_root, second_root in itertools.permutations(range(40), 2):
        residual = [
            vertex
            for vertex in range(40)
            if vertex not in (first_root, second_root)
        ]
        rooted_sum = 0
        for first, second in itertools.combinations(residual, 2):
            scaled_e = scaled_inner(first, second)
            scaled_a = scaled_inner(first_root, first)
            scaled_c = scaled_inner(first_root, second)
            rooted_sum += scaled_e * (8 - 3 * (scaled_a + scaled_c))
        total_scaled += rooted_sum * rooted_sum
    return Q(total_scaled, 256)


CONTINUOUS_ATOM = (
    ("1", "-3/4", "1/4", "-1/4", "-1/4", "-1/4", "-1/4"),
    ("-3/4", "1", "1/4", "-1/4", "-1/4", "-1/4", "-1/4"),
    ("1/4", "1/4", "1", "0", "-2/3", "-2/3", "-2/3"),
    ("-1/4", "-1/4", "0", "1", "1/3", "1/3", "1/3"),
    ("-1/4", "-1/4", "-2/3", "1/3", "1", "1/3", "1/3"),
    ("-1/4", "-1/4", "-2/3", "1/3", "1/3", "1", "1/3"),
    ("-1/4", "-1/4", "-2/3", "1/3", "1/3", "1/3", "1"),
)


def determinant(matrix: tuple[tuple[Q, ...], ...]) -> Q:
    size = len(matrix)
    if size == 0:
        return Q(1)
    work = [list(row) for row in matrix]
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


def rational_rank(matrix: tuple[tuple[Q, ...], ...]) -> int:
    work = [list(row) for row in matrix]
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
    return pivot_row


def verify_continuous_atom_geometry():
    gram = tuple(tuple(Q(entry) for entry in row) for row in CONTINUOUS_ATOM)
    require(
        all(gram[index][index] == 1 for index in range(7)),
        "continuous atom does not have unit diagonal",
    )
    require(
        all(
            gram[first][second] == gram[second][first] <= Q(1, 2)
            for first in range(7)
            for second in range(first + 1, 7)
        ),
        "continuous atom is not symmetric or violates the kissing bound",
    )
    require(rational_rank(gram) == 5, "continuous atom rank is not five")
    for size in range(1, 8):
        for subset in itertools.combinations(range(7), size):
            principal = tuple(
                tuple(gram[first][second] for second in subset)
                for first in subset
            )
            require(
                determinant(principal) >= 0,
                f"negative continuous-atom principal minor on {subset}",
            )
    return gram


def continuous_atom_qe_row(gram) -> Q:
    """Polynomial row f=q*e on the pure seven-point orbit, at N=41."""

    coefficients = {
        union_size: Q(math.comb(39, union_size), math.comb(5, union_size))
        for union_size in (2, 3, 4)
    }
    total = Q(0)
    for first_root, second_root in itertools.permutations(range(7), 2):
        residual = [
            vertex
            for vertex in range(7)
            if vertex not in (first_root, second_root)
        ]
        values = {
            local_pair: gram[first_root][second_root]
            * gram[residual[local_pair[0]]][residual[local_pair[1]]]
            for local_pair in itertools.combinations(range(5), 2)
        }
        sums = union_sums(values, 5)
        total += sum(
            coefficients[union_size] * sums[union_size - 2]
            for union_size in (2, 3, 4)
        )
    return total


def continuous_atom_hg_row() -> Q:
    """Coarse H/G square at the distinguished root (y,z).

    The five residual vertices consist of one G point and four H points.
    The feature is +1 on an H-G pair, -3 on an H-H pair, and zero otherwise.
    """

    residual_types = ("G", "H", "H", "H", "H")
    values = {}
    for first, second in itertools.combinations(range(5), 2):
        types = {residual_types[first], residual_types[second]}
        if types == {"G", "H"}:
            value = 1
        elif residual_types[first] == residual_types[second] == "H":
            value = -3
        else:
            value = 0
        values[first, second] = value
    sums = union_sums(values, 5)
    coefficients = {
        union_size: Q(math.comb(39, union_size), math.comb(5, union_size))
        for union_size in (2, 3, 4)
    }
    return sum(
        coefficients[union_size] * sums[union_size - 2]
        for union_size in (2, 3, 4)
    )


def verify(certificate_path=CERTIFICATE):
    expected = json.loads(certificate_path.read_text())
    require(
        expected.get("schema") == "kissing5.global_flag_exchangeability.v1",
        "unexpected certificate schema",
    )
    require(expected.get("target_cardinality") == 41, "wrong target size")
    results = {}
    for name, path, expected_hash in SOURCES:
        value = evaluate_pseudodistribution(path, expected_hash)
        require(
            value == Q(expected["pseudodistributions"][name]["value"]),
            f"stored pseudodistribution value mismatch for {name}",
        )
        require(value < 0, f"row is not negative for {name}")
        results[name] = str(value)

    d5_value = d5_polynomial_square()
    require(
        d5_value == Q(expected["D5"]["direct_global_square"]),
        "stored D5 square mismatch",
    )
    require(d5_value > 0, "D5 positive control is not positive")

    gram = verify_continuous_atom_geometry()
    qe_value = continuous_atom_qe_row(gram)
    hg_value = continuous_atom_hg_row()
    require(
        qe_value == Q(expected["continuous_counteratom"]["q_times_e_row"]),
        "stored continuous q-times-e value mismatch",
    )
    require(
        hg_value == Q(expected["continuous_counteratom"]["H_G_row"]),
        "stored continuous H/G value mismatch",
    )
    require(
        qe_value < 0 and hg_value < 0,
        "continuous counteratom rows are not both negative",
    )

    report = {
        "status": "PASS",
        "theorem_scope": (
            "finite-exchangeability necessary condition for every real "
            "symmetric array; no finite inner-product alphabet or Gram-rank "
            "hypothesis is used"
        ),
        "D5_direct_global_square": str(d5_value),
        "continuous_counteratom": {
            "rank": rational_rank(gram),
            "q_times_e_row": str(qe_value),
            "H_G_row": str(hg_value),
        },
        "negative_pseudodistribution_rows": results,
    }
    return report


def main():
    require(
        len(sys.argv) <= 2,
        "usage: verify_global_flag_exchangeability.py [certificate]",
    )
    certificate_path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    print(json.dumps(verify(certificate_path), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

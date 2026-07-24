#!/usr/bin/env python3
"""Generate an exact K6 repair for a four-feature global flag block.

The active support and six free rounded coordinates came from the separate
floating cutting-plane search.  This script solves all remaining coordinates
with exact rational Gaussian elimination and then checks every equation and
every principal minor before writing the certificate.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CATALOG = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "results"
    / "direct_k6_5000.csv"
)
DISCOVERY = HERE / "discovery_result.json"
OUTPUT = HERE / "psd4_repair_certificate.json"

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CATALOG_SHA256 = (
    "45634e27071b348b66c02b4bbbfe9f23db713d2f3798589cbbd1c3750b0dcb68"
)

ACTIVE = (
    42,
    164,
    198,
    201,
    234,
    563,
    1085,
    1088,
    4561,
    5019,
    5684,
    8066,
    8201,
    9665,
    10014,
    10113,
    11355,
    16580,
    18132,
    19358,
    20675,
    27544,
    37314,
    38120,
    39909,
    42048,
    47100,
    51146,
    55741,
    59900,
    60112,
    60113,
    60995,
    61595,
    62224,
    62236,
    65654,
    70941,
    71561,
    71589,
    72820,
    93216,
    94303,
    100864,
    102473,
    103149,
    105514,
    105530,
    105531,
    120035,
    132576,
    132643,
    135843,
    136712,
    137074,
    137157,
    137295,
)

# Positions within ACTIVE.  Their floating values are rounded to denominator
# 10^12; the other 51 coordinates are then solved exactly.
FREE_POSITIONS = (1, 23, 30, 31, 39, 50)
FREE_NUMERATORS = (
    1239231745,
    24335525048,
    60800063012,
    228500073871,
    5525283068,
    7960754748,
)
ROUNDING_DENOMINATOR = 10**12

# Independent equation rows among normalization followed by 51 triangle rows.
INDEPENDENT_ROWS = (
    28,
    12,
    47,
    36,
    51,
    34,
    19,
    26,
    35,
    29,
    21,
    44,
    15,
    1,
    49,
    42,
    30,
    10,
    22,
    27,
    41,
    38,
    5,
    11,
    8,
    13,
    3,
    9,
    33,
    25,
    40,
    24,
    6,
    23,
    20,
    2,
    46,
    18,
    31,
    14,
    37,
    45,
    17,
    50,
    39,
    7,
    4,
    32,
    43,
    48,
    16,
)

PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
LOCAL_PAIRS = tuple(itertools.combinations(range(4), 2))
KERNEL = tuple(
    tuple(
        {
            2: 494,
            3: 9139,
            4: 329004,
        }[len(set(first) | set(second))]
        for second in LOCAL_PAIRS
    )
    for first in LOCAL_PAIRS
)
MATRIX_KEYS = tuple((i, j) for i in range(4) for j in range(i, 4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def solve_square(matrix: list[list[Q]], rhs: list[Q]) -> list[Q]:
    size = len(rhs)
    assert len(matrix) == size and all(len(row) == size for row in matrix)
    work = [
        [Q(entry) for entry in row] + [Q(value)]
        for row, value in zip(matrix, rhs)
    ]
    for column in range(size):
        pivot = next(
            row
            for row in range(column, size)
            if work[row][column] != 0
        )
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [entry / scale for entry in work[column]]
        for row in range(size):
            if row == column or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column])
            ]
    return [work[index][-1] for index in range(size)]


def parse_selected_catalog():
    assert sha256(CATALOG) == CATALOG_SHA256
    wanted = set(ACTIVE)
    selected = {}
    lines = CATALOG.read_text().splitlines()
    header = lines[0]
    for index, line in enumerate(lines[1:]):
        if index not in wanted:
            continue
        fields = tuple(map(int, line.split(",")))
        assert len(fields) == 35
        selected[index] = (fields[:15], fields[15:])
    assert set(selected) == wanted
    return header, tuple(selected[index] for index in ACTIVE)


def edge(edges, first, second):
    return edges[PAIR_INDEX6[tuple(sorted((first, second)))]]


def feature_vector(edges, first_root, second_root, first, second):
    scaled_q = edge(edges, first_root, second_root) - 4
    scaled_a = edge(edges, first_root, first) - 4
    scaled_b = edge(edges, second_root, first) - 4
    scaled_c = edge(edges, first_root, second) - 4
    scaled_d = edge(edges, second_root, second) - 4
    scaled_e = edge(edges, first, second) - 4
    return (
        scaled_e,
        scaled_e * (scaled_a + scaled_c),
        scaled_q * scaled_e,
        scaled_a * scaled_d + scaled_c * scaled_b,
    )


def atomic_moment(edges):
    matrix = [[0] * 4 for _ in range(4)]
    for first_root, second_root in itertools.permutations(range(6), 2):
        residual = [
            vertex
            for vertex in range(6)
            if vertex not in (first_root, second_root)
        ]
        vectors = [
            feature_vector(
                edges,
                first_root,
                second_root,
                residual[first],
                residual[second],
            )
            for first, second in LOCAL_PAIRS
        ]
        for left, left_vector in enumerate(vectors):
            for right, right_vector in enumerate(vectors):
                coefficient = KERNEL[left][right]
                for row in range(4):
                    for column in range(row, 4):
                        matrix[row][column] += (
                            coefficient
                            * left_vector[row]
                            * right_vector[column]
                        )
    for row in range(4):
        for column in range(row):
            matrix[row][column] = matrix[column][row]
    return tuple(tuple(row) for row in matrix)


def determinant(matrix):
    size = len(matrix)
    work = [list(map(Q, row)) for row in matrix]
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


def main():
    assert sha256(SOURCE) == SOURCE_SHA256
    source = json.loads(SOURCE.read_text())
    catalog_header, selected = parse_selected_catalog()

    rows = [[Q(1)] * len(selected)]
    for triangle_index in range(51):
        rows.append(
            [
                Q(triangles.count(triangle_index))
                for _edges, triangles in selected
            ]
        )
    targets = [Q(1)] + [Q(value) / 78 for value in source["nu"]]

    pivot_positions = tuple(
        position
        for position in range(len(selected))
        if position not in FREE_POSITIONS
    )
    assert len(pivot_positions) == len(INDEPENDENT_ROWS) == 51
    weights = [Q(0)] * len(selected)
    for position, numerator in zip(FREE_POSITIONS, FREE_NUMERATORS):
        weights[position] = Q(numerator, ROUNDING_DENOMINATOR)
    residual = [
        targets[row]
        - sum(rows[row][position] * weights[position] for position in FREE_POSITIONS)
        for row in INDEPENDENT_ROWS
    ]
    pivot_matrix = [
        [rows[row][position] for position in pivot_positions]
        for row in INDEPENDENT_ROWS
    ]
    pivot_weights = solve_square(pivot_matrix, residual)
    for position, weight in zip(pivot_positions, pivot_weights):
        weights[position] = weight

    assert all(weight > 0 for weight in weights)
    assert all(
        sum(coefficient * weight for coefficient, weight in zip(row, weights))
        == target
        for row, target in zip(rows, targets)
    )

    atomic_matrices = [atomic_moment(edges) for edges, _faces in selected]
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
    principal_minors = {}
    for size in range(1, 5):
        for subset in itertools.combinations(range(4), size):
            value = determinant(
                tuple(
                    tuple(moment[row][column] for column in subset)
                    for row in subset
                )
            )
            assert value > 0
            principal_minors[",".join(map(str, subset))] = qstr(value)

    atoms = [
        {
            "catalog_index": catalog_index,
            "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45": list(
                edges
            ),
            "triangle_orbit_indices": list(triangles),
            "weight": qstr(weight),
        }
        for catalog_index, (edges, triangles), weight in zip(
            ACTIVE, selected, weights
        )
    ]
    certificate = {
        "schema": "kissing5.global_flag_psd4_repair.v1",
        "status": (
            "exact positive rank-five K6 mixture matching the fixed triangle "
            "marginal and a positive-definite four-feature global flag block"
        ),
        "scope_warning": (
            "This is a local K6 pseudomarginal, not an overlapping-subset "
            "consistent 41-point code. The discovery catalog is incomplete."
        ),
        "source_certificate": str(SOURCE.relative_to(ROOT)),
        "source_sha256": SOURCE_SHA256,
        "catalog": str(CATALOG.relative_to(ROOT)),
        "catalog_header": catalog_header,
        "catalog_sha256": CATALOG_SHA256,
        "discovery_report": str(DISCOVERY.relative_to(ROOT)),
        "discovery_report_sha256": sha256(DISCOVERY),
        "target_cardinality": 41,
        "local_size": 6,
        "normalization": (
            "weights sum to one; expected K6 triangle counts are nu/78"
        ),
        "scaled_features": [
            "F0 = 4*g_pq",
            "F1 = (4*g_pq)*(4*g_ip + 4*g_iq)",
            "F2 = (4*g_ij)*(4*g_pq)",
            "F3 = (4*g_ip)*(4*g_jq) + (4*g_iq)*(4*g_jp)",
        ],
        "kernel_by_union_size": {
            "2": 494,
            "3": 9139,
            "4": 329004,
        },
        "kernel_note": (
            "These are four times binom(39,u)/binom(4,u); multiplying the "
            "universal flag-square block by four does not change PSD."
        ),
        "rounding_denominator": ROUNDING_DENOMINATOR,
        "free_support_positions": list(FREE_POSITIONS),
        "independent_equation_rows": list(INDEPENDENT_ROWS),
        "moment_matrix": [[qstr(value) for value in row] for row in moment],
        "principal_minors": principal_minors,
        "atoms": atoms,
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)
    print(sha256(OUTPUT))
    print("minimum_weight", min(weights))
    print("minimum_principal_minor", min(map(Q, principal_minors.values())))


if __name__ == "__main__":
    main()

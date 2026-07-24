#!/usr/bin/env python3
"""Generate the exact centered degree-two rooted-edge K6 repair."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
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
OUTPUT = HERE / "centered_degree2_repair_certificate.json"

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CATALOG_SHA256 = (
    "45634e27071b348b66c02b4bbbfe9f23db713d2f3798589cbbd1c3750b0dcb68"
)

ACTIVE = (
    20,
    165,
    910,
    2745,
    3810,
    5630,
    5790,
    9500,
    9570,
    9580,
    9600,
    9665,
    10285,
    10570,
    12945,
    15455,
    17700,
    17980,
    18132,
    27220,
    37314,
    44285,
    50770,
    50940,
    50950,
    59660,
    59708,
    59755,
    59840,
    59861,
    59870,
    60110,
    60113,
    60115,
    61555,
    62224,
    64285,
    64465,
    68510,
    71560,
    72200,
    72800,
    72830,
    84225,
    95940,
    97125,
    97360,
    100952,
    101395,
    101800,
    103790,
    104365,
    107065,
    107230,
    110230,
    110575,
    122455,
    124610,
    130060,
    132575,
    132576,
    132643,
    132650,
    132755,
    133850,
    134465,
    134570,
    135335,
    135345,
    135843,
    137025,
    137031,
    137295,
)

FREE_POSITION = 62
FREE_NUMERATOR = 296896361880
ROUNDING_DENOMINATOR = 10**14

INDEPENDENT_ROWS = (
    0,
    31,
    15,
    23,
    19,
    1,
    28,
    153,
    89,
    17,
    32,
    37,
    24,
    47,
    27,
    25,
    3,
    8,
    50,
    38,
    9,
    42,
    26,
    13,
    6,
    11,
    18,
    2,
    93,
    30,
    45,
    35,
    43,
    21,
    46,
    41,
    33,
    14,
    10,
    36,
    16,
    20,
    180,
    12,
    44,
    40,
    111,
    95,
    49,
    34,
    22,
    48,
    181,
    114,
    7,
    5,
    100,
    177,
    4,
    29,
    39,
    112,
    99,
    175,
    96,
    110,
    68,
    79,
    109,
    72,
    108,
    78,
)

PIVOT_POSITIONS = (
    72,
    7,
    3,
    61,
    52,
    42,
    47,
    44,
    1,
    4,
    20,
    41,
    12,
    64,
    58,
    71,
    0,
    9,
    15,
    38,
    45,
    66,
    19,
    27,
    65,
    40,
    2,
    34,
    25,
    6,
    10,
    16,
    35,
    51,
    14,
    68,
    46,
    5,
    50,
    57,
    17,
    29,
    22,
    63,
    69,
    70,
    18,
    13,
    43,
    39,
    11,
    33,
    23,
    56,
    54,
    53,
    59,
    55,
    49,
    8,
    32,
    37,
    21,
    28,
    60,
    30,
    36,
    26,
    67,
    48,
    31,
    24,
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
LOCAL_PAIRS = tuple(itertools.combinations(range(4), 2))
KERNEL = {
    2: 494,
    3: 9139,
    4: 329004,
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def solve_square(matrix, rhs):
    size = len(rhs)
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


def determinant(matrix):
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


def edge(edges, first, second):
    return edges[PAIR_INDEX6[tuple(sorted((first, second)))]]


def feature(edges, i, j, p, q):
    base = edge(edges, i, j) - 4
    a = edge(edges, i, p) - 4
    b = edge(edges, j, p) - 4
    c = edge(edges, i, q) - 4
    d = edge(edges, j, q) - 4
    e = edge(edges, p, q) - 4
    return (
        1,
        base,
        e,
        a + c,
        b + d,
        base * base,
        base * e,
        e * e,
        base * (a + c),
        base * (b + d),
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
        residual = [vertex for vertex in range(6) if vertex not in (i, j)]
        extensions = tuple(itertools.combinations(range(4), 2))
        values = [
            feature(edges, i, j, residual[first], residual[second])
            for first, second in extensions
        ]
        for left, first_extension in enumerate(extensions):
            for right, second_extension in enumerate(extensions):
                coefficient = KERNEL[
                    len(set(first_extension) | set(second_extension))
                ]
                for row in range(18):
                    left_value = coefficient * values[left][row]
                    for column in range(18):
                        matrix[row][column] += (
                            left_value * values[right][column]
                        )
    return tuple(tuple(row) for row in matrix)


def bilinear(left, matrix, right):
    return sum(
        left[row] * matrix[row][column] * right[column]
        for row in range(18)
        for column in range(18)
    )


def parse_catalog():
    assert sha256(CATALOG) == CATALOG_SHA256
    selected = {}
    wanted = set(ACTIVE)
    lines = CATALOG.read_text().splitlines()
    for index, line in enumerate(lines[1:]):
        if index not in wanted:
            continue
        fields = tuple(map(int, line.split(",")))
        selected[index] = (fields[:15], fields[15:])
    assert set(selected) == wanted
    return lines[0], tuple(selected[index] for index in ACTIVE)


def main():
    assert sha256(SOURCE) == SOURCE_SHA256
    source = json.loads(SOURCE.read_text())
    header, selected = parse_catalog()
    atomic = [atomic_moment(edges) for edges, _faces in selected]

    rows = [[Q(1)] * len(selected)]
    targets = [Q(1)]
    labels = ["normalization"]
    for triangle in range(51):
        rows.append(
            [
                Q(faces.count(triangle))
                for _edges, faces in selected
            ]
        )
        targets.append(Q(source["nu"][triangle]) / 78)
        labels.append(f"triangle_{triangle}")
    quotient_vectors = []
    for index in QUOTIENT_INDICES:
        item = [0] * 18
        item[index] = 1
        quotient_vectors.append(tuple(item))
    for kernel_index, kernel in enumerate(CENTERED_KERNELS):
        for quotient_index, quotient in enumerate(quotient_vectors):
            rows.append(
                [Q(bilinear(kernel, matrix, quotient)) for matrix in atomic]
            )
            targets.append(Q(0))
            labels.append(f"kernel_{kernel_index}_quotient_{quotient_index}")
    for first, left in enumerate(CENTERED_KERNELS):
        for second in range(first, len(CENTERED_KERNELS)):
            rows.append(
                [
                    Q(bilinear(left, matrix, CENTERED_KERNELS[second]))
                    for matrix in atomic
                ]
            )
            targets.append(Q(0))
            labels.append(f"kernel_{first}_kernel_{second}")
    assert len(rows) == 195

    weights = [Q(0)] * len(selected)
    weights[FREE_POSITION] = Q(
        FREE_NUMERATOR, ROUNDING_DENOMINATOR
    )
    residual = [
        targets[row] - rows[row][FREE_POSITION] * weights[FREE_POSITION]
        for row in INDEPENDENT_ROWS
    ]
    solution = solve_square(
        [
            [rows[row][position] for position in PIVOT_POSITIONS]
            for row in INDEPENDENT_ROWS
        ],
        residual,
    )
    for position, weight in zip(PIVOT_POSITIONS, solution):
        weights[position] = weight
    assert all(weight > 0 for weight in weights)
    assert all(
        sum(coefficient * weight for coefficient, weight in zip(row, weights))
        == target
        for row, target in zip(rows, targets)
    )

    moment = tuple(
        tuple(
            sum(
                weight * matrix[row][column]
                for weight, matrix in zip(weights, atomic)
            )
            for column in range(18)
        )
        for row in range(18)
    )
    assert all(
        sum(kernel[row] * moment[row][column] for row in range(18)) == 0
        for kernel in CENTERED_KERNELS
        for column in range(18)
    )
    quotient = tuple(
        tuple(moment[row][column] for column in QUOTIENT_INDICES)
        for row in QUOTIENT_INDICES
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
            assert value > 0
            principal_minors[",".join(map(str, subset))] = qstr(value)

    atoms = [
        {
            "catalog_index": catalog_index,
            "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45": list(
                edges
            ),
            "triangle_orbit_indices": list(faces),
            "weight": qstr(weight),
        }
        for catalog_index, (edges, faces), weight in zip(
            ACTIVE, selected, weights
        )
    ]
    certificate = {
        "schema": "kissing5.centered_degree2_flag_repair.v1",
        "status": (
            "exact positive rank-five K6 mixture matching the fixed triangle "
            "marginal and the full centered symmetric degree-two rooted-edge "
            "flag PSD block"
        ),
        "scope_warning": (
            "Atomic K6 PSD and one local flag block do not imply consistency "
            "between overlapping K6 subsets of one 41-point array."
        ),
        "source_certificate": str(SOURCE.relative_to(ROOT)),
        "source_sha256": SOURCE_SHA256,
        "catalog": str(CATALOG.relative_to(ROOT)),
        "catalog_header": header,
        "catalog_sha256": CATALOG_SHA256,
        "target_cardinality": 41,
        "local_size": 6,
        "feature_names": FEATURE_NAMES,
        "feature_scaling": "q,a,b,c,d,e are four times the inner products",
        "kernel_by_union_size": {"2": 494, "3": 9139, "4": 329004},
        "kernel_note": (
            "The kernel is four times binom(39,u)/binom(4,u)."
        ),
        "centered_kernel_vectors": CENTERED_KERNELS,
        "quotient_indices": QUOTIENT_INDICES,
        "moment_matrix": [[qstr(value) for value in row] for row in moment],
        "quotient_matrix": [
            [qstr(value) for value in row] for row in quotient
        ],
        "quotient_principal_minors": principal_minors,
        "rounding_denominator": ROUNDING_DENOMINATOR,
        "free_position": FREE_POSITION,
        "independent_equation_rows": INDEPENDENT_ROWS,
        "independent_equation_labels": [
            labels[index] for index in INDEPENDENT_ROWS
        ],
        "atoms": atoms,
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)
    print(sha256(OUTPUT))
    print("minimum_weight", min(weights))
    print("quotient_determinant", determinant(quotient))


if __name__ == "__main__":
    main()

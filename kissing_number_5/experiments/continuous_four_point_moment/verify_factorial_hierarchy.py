#!/usr/bin/env python3
"""Exact verifier for the K6/K7 falling-factorial hierarchy.

Only Python standard-library rational arithmetic is used.  The verifier
checks the two named witness separators, all univariate cap rows, a
two-row Farkas ray for the 1,782-column K7 pool, an explicit rank-five
repair atom, and a three-multiplier joint-moment Farkas ray for the
once-augmented pool.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K6 = (
    ROOT
    / "experiments"
    / "four_point_depth_projection"
    / "k6_product_audit"
    / "productpool_extension.json"
)
K7 = (
    ROOT
    / "experiments"
    / "four_point_depth_projection"
    / "k7_product_audit"
    / "candidate_k7_product_extension.json"
)
POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
K6_SHA256 = (
    "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991"
)
K7_SHA256 = (
    "1b5e262592e1872cfe9f26b344d82da5066d8332efc5104a34a433d9d5564b00"
)
POOL_SHA256 = (
    "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623"
)

K6_EDGE_KEY = (
    "edge_color_indices_"
    "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
)
K7_EDGE_KEY = (
    "edge_color_indices_"
    "01_02_03_04_05_06_12_13_14_15_16_"
    "23_24_25_26_34_35_36_45_46_56"
)

CAPACITY_FAMILIES = (
    (1, 5, 6),
    (1, 6, 0),
    (2, 6, 1),
    (3, 6, 3),
    (4, 6, 6),
    (5, 6, 7),
    (6, 6, 7),
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generalized_binomial(value: int, degree: int) -> Q:
    answer = Q(1)
    for offset in range(degree):
        answer *= Q(value - offset, offset + 1)
    return answer


def binomial_coefficients(values: list[Q]) -> tuple[Q, ...]:
    """Newton coefficients: p(x)=sum_t Delta^t p(0) binom(x,t)."""

    coefficients = []
    work = values[:]
    while work:
        coefficients.append(work[0])
        work = [
            work[index + 1] - work[index]
            for index in range(len(work) - 1)
        ]
    return tuple(coefficients)


def cap_polynomial_coefficients(
    capacity: int, left_degree: int, right_degree: int
) -> tuple[Q, ...]:
    degree = left_degree + right_degree
    return binomial_coefficients(
        [
            generalized_binomial(value, left_degree)
            * generalized_binomial(capacity - value, right_degree)
            for value in range(degree + 1)
        ]
    )


def depth_polynomial_coefficients(
    required: int, left_degree: int, right_degree: int
) -> tuple[Q, ...]:
    degree = left_degree + right_degree
    return binomial_coefficients(
        [
            generalized_binomial(value - required, left_degree)
            * generalized_binomial(39 - value, right_degree)
            for value in range(degree + 1)
        ]
    )


def unbiased_estimator(
    coefficients: tuple[Q, ...], sample_size: int, observed: int
) -> Q:
    return sum(
        coefficient
        * Q(math.comb(39, degree), math.comb(sample_size, degree))
        * math.comb(observed, degree)
        for degree, coefficient in enumerate(coefficients)
    )


def edge_data(vertex_count: int):
    pairs = tuple(itertools.combinations(range(vertex_count), 2))
    return pairs, {pair: index for index, pair in enumerate(pairs)}


def edge_color(
    edges: tuple[int, ...],
    pair_index: dict[tuple[int, int], int],
    first: int,
    second: int,
) -> int:
    return edges[pair_index[tuple(sorted((first, second)))]]


def cap_row_slack(
    data: dict[str, object],
    vertex_count: int,
    edge_key: str,
    base_color: int,
    high_color: int,
    capacity: int,
    left_degree: int,
    right_degree: int,
) -> Q:
    sample_size = vertex_count - 2
    pairs, pair_index = edge_data(vertex_count)
    coefficients = cap_polynomial_coefficients(
        capacity, left_degree, right_degree
    )
    slack = Q(0)
    for atom in data["atoms"]:
        weight = Q(atom["weight"])
        edges = tuple(atom[edge_key])
        for position, (first, second) in enumerate(pairs):
            if edges[position] != base_color:
                continue
            common = sum(
                edge_color(edges, pair_index, first, vertex) >= high_color
                and edge_color(edges, pair_index, second, vertex) >= high_color
                for vertex in range(vertex_count)
                if vertex not in (first, second)
            )
            slack += weight * unbiased_estimator(
                coefficients, sample_size, common
            )
    return slack


def depth_row_slack(
    data: dict[str, object],
    vertex_count: int,
    edge_key: str,
    base_color: int,
    required: int,
    membership: set[tuple[int, int]],
) -> Q:
    """Slack for binom(H-required,3), summed over oriented bases."""

    sample_size = vertex_count - 2
    pairs, pair_index = edge_data(vertex_count)
    coefficients = depth_polynomial_coefficients(required, 3, 0)
    slack = Q(0)
    for atom in data["atoms"]:
        weight = Q(atom["weight"])
        edges = tuple(atom[edge_key])
        for position, (first, second) in enumerate(pairs):
            if edges[position] != base_color:
                continue
            remaining = [
                vertex
                for vertex in range(vertex_count)
                if vertex not in (first, second)
            ]
            for oriented_first, oriented_second in (
                (first, second),
                (second, first),
            ):
                depth = sum(
                    (
                        edge_color(
                            edges, pair_index, oriented_first, vertex
                        ),
                        edge_color(
                            edges, pair_index, oriented_second, vertex
                        ),
                    )
                    in membership
                    for vertex in remaining
                )
                slack += weight * unbiased_estimator(
                    coefficients, sample_size, depth
                )
    return slack


def all_cap_rows(
    data: dict[str, object],
    vertex_count: int,
    edge_key: str,
) -> list[tuple[Q, tuple[int, int, int, int]]]:
    sample_size = vertex_count - 2
    answer = []
    for family_index, (base, high, capacity) in enumerate(
        CAPACITY_FAMILIES
    ):
        for total_degree in range(1, sample_size + 1):
            for left_degree in range(total_degree + 1):
                right_degree = total_degree - left_degree
                slack = cap_row_slack(
                    data,
                    vertex_count,
                    edge_key,
                    base,
                    high,
                    capacity,
                    left_degree,
                    right_degree,
                )
                answer.append(
                    (
                        slack,
                        (
                            family_index,
                            left_degree,
                            right_degree,
                            total_degree,
                        ),
                    )
                )
    return answer


def parse_pool() -> tuple[tuple[int, ...], ...]:
    lines = POOL.read_text().splitlines()
    assert lines[0] == (
        "# source_k6_atoms=51 rank_five_labeled=2012 "
        "distinct_triangle_count_vectors=1782"
    )
    records = tuple(
        tuple(int(field) for field in line.split(",")) for line in lines[1:]
    )
    assert len(records) == 1782 and all(len(record) == 56 for record in records)
    return records


def triangle_faces(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    pairs, pair_index = edge_data(7)
    del pairs
    faces = []
    for first, second, third in itertools.combinations(range(7), 3):
        faces.append(
            triple_index[
                tuple(
                    sorted(
                        (
                            edge_color(edges, pair_index, first, second),
                            edge_color(edges, pair_index, first, third),
                            edge_color(edges, pair_index, second, third),
                        )
                    )
                )
            ]
        )
    return tuple(sorted(faces))


def pool_cap_farkas(
    records: tuple[tuple[int, ...], ...],
    triples: tuple[tuple[int, int, int], ...],
    alpha: tuple[Q, ...],
    nu: tuple[Q, ...],
) -> dict[str, object]:
    pairs, pair_index = edge_data(7)
    triple_index = {triple: index for index, triple in enumerate(triples)}
    type_466 = triple_index[(4, 6, 6)]

    first_coefficients = cap_polynomial_coefficients(6, 1, 3)
    second_coefficients = cap_polynomial_coefficients(6, 0, 5)
    assert first_coefficients == (Q(0), Q(10), Q(-12), Q(9), Q(-4))
    assert second_coefficients == (
        Q(6),
        Q(-5),
        Q(4),
        Q(-3),
        Q(2),
        Q(-1),
    )
    r1_values = tuple(
        Q(10, 39) * unbiased_estimator(first_coefficients, 5, common)
        for common in range(6)
    )
    r2_values = tuple(
        Q(10, 3) * unbiased_estimator(second_coefficients, 5, common)
        for common in range(6)
    )
    assert r1_values == (0, 20, -188, 1485, -9724, -65450)
    assert r2_values == (20, -110, 748, -6545, 78540, -1452990)
    for common in range(4):
        assert (
            Q(13, 12) * r1_values[common]
            + Q(1, 4) * r2_values[common]
            == 5 - Q(65, 6) * common
        )

    maximum_common = 0
    column_residuals = []
    for record in records:
        edges = record[:21]
        faces = record[21:]
        assert triangle_faces(edges, triple_index) == tuple(faces)
        edge_count = 0
        common_total = 0
        first_row = Q(0)
        second_row = Q(0)
        for position, (first, second) in enumerate(pairs):
            if edges[position] != 4:
                continue
            edge_count += 1
            common = sum(
                edge_color(edges, pair_index, first, vertex) >= 6
                and edge_color(edges, pair_index, second, vertex) >= 6
                for vertex in range(7)
                if vertex not in (first, second)
            )
            maximum_common = max(maximum_common, common)
            common_total += common
            first_row += r1_values[common]
            second_row += r2_values[common]
        assert common_total == sum(face == type_466 for face in faces)
        residual = (
            Q(13, 12) * first_row
            + Q(1, 4) * second_row
            - 5 * edge_count
            + Q(65, 6) * common_total
        )
        assert residual == 0
        column_residuals.append(residual)
    assert maximum_common == 3
    assert set(column_residuals) == {Q(0)}

    expected_edges = Q(21, 40) * alpha[4]
    expected_common = Q(7, 312) * nu[type_466]
    assert expected_edges == Q(39881456212194023, 5920000000000000)
    assert expected_common == Q(81384983628501, 20800000000000)
    target = 5 * expected_edges - Q(65, 6) * expected_common
    assert target == Q(
        -10305950358714927, 1184000000000000
    ) < 0
    return {
        "maximum_pool_sample_common_count": maximum_common,
        "farkas_column_residual": "0 on all 1782 columns",
        "farkas_target": target,
    }


def determinant(matrix: list[list[int]]) -> int:
    """Integer Bareiss determinant."""

    size = len(matrix)
    work = [row[:] for row in matrix]
    previous = 1
    sign = 1
    for index in range(size - 1):
        pivot_row = next(
            (row for row in range(index, size) if work[row][index]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != index:
            work[index], work[pivot_row] = work[pivot_row], work[index]
            sign *= -1
        pivot = work[index][index]
        for row in range(index + 1, size):
            for column in range(index + 1, size):
                numerator = (
                    pivot * work[row][column]
                    - work[row][index] * work[index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def synthetic_atom(
    triples: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Rank-five K7 with a zero base and four common 1/2-neighbors."""

    pairs, pair_index = edge_data(7)
    edges = [4] * 21

    def set_color(first: int, second: int, color: int) -> None:
        edges[pair_index[tuple(sorted((first, second)))]] = color

    for vertex in range(2, 6):
        set_color(0, vertex, 6)
        set_color(1, vertex, 6)
    for first in (2, 3):
        for second in (4, 5):
            set_color(first, second, 6)

    # This is the Gram matrix of e1,e2, four points using +/-e3,+/-e4
    # above (e1+e2)/2, and e5.  Check PSD and rank exactly five from all
    # principal minors of the matrix scaled by four.
    scaled_nodes = (-4, -3, -2, -1, 0, 1, 2)
    gram = [[4 if i == j else 0 for j in range(7)] for i in range(7)]
    for (first, second), color in zip(pairs, edges):
        gram[first][second] = scaled_nodes[color]
        gram[second][first] = scaled_nodes[color]
    positive_fifth = False
    for size in range(1, 8):
        for indices in itertools.combinations(range(7), size):
            minor = [[gram[i][j] for j in indices] for i in indices]
            value = determinant(minor)
            assert value >= 0
            if size == 5 and value > 0:
                positive_fifth = True
            if size >= 6:
                assert value == 0
    assert positive_fifth

    triple_index = {triple: index for index, triple in enumerate(triples)}
    faces = triangle_faces(tuple(edges), triple_index)
    common = sum(
        edge_color(tuple(edges), pair_index, 0, vertex) >= 6
        and edge_color(tuple(edges), pair_index, 1, vertex) >= 6
        for vertex in range(2, 7)
    )
    assert edges[pair_index[(0, 1)]] == 4 and common == 4
    return tuple(edges), faces


def joint_farkas(
    records: tuple[tuple[int, ...], ...],
    synthetic: tuple[tuple[int, ...], tuple[int, ...]],
    nodes: tuple[Q, ...],
    triples: tuple[tuple[int, int, int], ...],
    nu: tuple[Q, ...],
) -> dict[str, object]:
    pairs, pair_index = edge_data(7)
    triple_index = {triple: index for index, triple in enumerate(triples)}
    type_155 = triple_index[(1, 5, 5)]
    augmented = [
        (record[:21], record[21:]) for record in records
    ] + [synthetic]

    atom_coefficients = []
    for edges, faces in augmented:
        local_01 = 0
        local_41 = 0
        for position, (first, second) in enumerate(pairs):
            if edges[position] != 1:
                continue
            remaining = [
                vertex
                for vertex in range(7)
                if vertex not in (first, second)
            ]
            depth = sum(
                nodes[edge_color(edges, pair_index, first, vertex)]
                + nodes[edge_color(edges, pair_index, second, vertex)]
                < 0
                for vertex in remaining
            )
            common = sum(
                edge_color(edges, pair_index, first, vertex) >= 5
                and edge_color(edges, pair_index, second, vertex) >= 5
                for vertex in remaining
            )
            local_01 += common
            local_41 += math.comb(depth, 4) * common
        triangle_count = sum(face == type_155 for face in faces)
        coefficient = local_01 - 2109 * local_41 - triangle_count
        assert coefficient >= 0
        atom_coefficients.append(coefficient)
    assert Counter(atom_coefficients) == Counter({0: 1783})

    # Coefficients of the representing-state columns in the Farkas ray.
    state_coefficients = []
    for common in range(7):
        for depth in range(7, 40 - common):
            coefficient = common * (
                -Q(5, 39)
                + Q(2109, math.comb(39, 5)) * math.comb(depth, 4)
            )
            assert coefficient >= 0
            state_coefficients.append(coefficient)
    assert min(state_coefficients) == 0

    target = -Q(7, 312) * nu[type_155]
    assert target == Q(
        -44522548762943617, 22510800000000000000
    ) < 0
    assert 2109 == Q(
        5 * math.comb(39, 5), 39 * math.comb(7, 4)
    )
    return {
        "augmented_pool_columns": len(augmented),
        "atom_coefficient_distribution": {"0": len(augmented)},
        "minimum_state_coefficient": min(state_coefficients),
        "joint_farkas_target": target,
    }


def verify() -> dict[str, object]:
    assert digest(SOURCE) == SOURCE_SHA256
    assert digest(K6) == K6_SHA256
    assert digest(K7) == K7_SHA256
    assert digest(POOL) == POOL_SHA256
    source = json.loads(SOURCE.read_text())
    k6 = json.loads(K6.read_text())
    k7 = json.loads(K7.read_text())
    nodes = tuple(Q(value) for value in source["grid"])
    alpha = tuple(Q(value) for value in source["alpha"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    nu = tuple(Q(value) for value in source["nu"])

    cap6 = all_cap_rows(k6, 6, K6_EDGE_KEY)
    cap7 = all_cap_rows(k7, 7, K7_EDGE_KEY)
    assert len(cap6) == 98 and sum(value < 0 for value, _ in cap6) == 11
    assert len(cap7) == 140 and sum(value < 0 for value, _ in cap7) == 19

    named_cap6 = cap_row_slack(k6, 6, K6_EDGE_KEY, 3, 6, 3, 0, 2)
    named_cap7 = cap_row_slack(k7, 7, K7_EDGE_KEY, 3, 6, 3, 0, 2)
    assert 2 * named_cap6 == Q(
        -2140627536537754284359159627634757733160323647,
        541912518143754136926852222590400000000000000,
    )
    assert 10 * named_cap7 == Q(
        -6736085935767064980586375943764744500321533,
        1055807876370816511457923512000000000000000,
    )

    k6_membership = {
        (3, 6),
        (4, 5),
        (4, 6),
        (5, 4),
        (5, 5),
        (5, 6),
        (6, 3),
        (6, 4),
        (6, 5),
        (6, 6),
    }
    k7_membership = {
        (first, second)
        for first in (5, 6)
        for second in range(7)
    }
    depth6 = depth_row_slack(
        k6, 6, K6_EDGE_KEY, 2, 5, k6_membership
    )
    depth7 = depth_row_slack(
        k7, 7, K7_EDGE_KEY, 1, 6, k7_membership
    )
    assert depth6 == Q(
        -335088953912079644930181112156948583173852442167,
        541912518143754136926852222590400000000000000,
    )
    assert depth7 == Q(
        -5474547853162314272355901181772000729446603803,
        120362097906273082306203280368000000000000000,
    )

    records = parse_pool()
    cap_farkas = pool_cap_farkas(records, triples, alpha, nu)
    repair_atom = synthetic_atom(triples)
    joint = joint_farkas(records, repair_atom, nodes, triples, nu)

    return {
        "status": "PASS",
        "sampling": {
            "K6_residual_sample": "4 of 39",
            "K7_residual_sample": "5 of 39",
        },
        "K6_cap_rows": len(cap6),
        "K6_cap_violations": sum(value < 0 for value, _ in cap6),
        "K7_cap_rows": len(cap7),
        "K7_cap_violations": sum(value < 0 for value, _ in cap7),
        "named_K6_cap_cleared_slack": str(2 * named_cap6),
        "named_K7_cap_cleared_slack": str(10 * named_cap7),
        "named_K6_depth_degree3_slack": str(depth6),
        "named_K7_depth_degree3_slack": str(depth7),
        "pool_cap_farkas": {
            key: str(value) if isinstance(value, Q) else value
            for key, value in cap_farkas.items()
        },
        "synthetic_repair_atom": (
            "rank exactly five; q=0 base with four common 1/2-neighbors"
        ),
        "joint_farkas": {
            key: str(value) if isinstance(value, Q) else value
            for key, value in joint.items()
        },
        "scope": (
            "exact local-witness and finite-pool obstructions; "
            "not a continuous K7 enumeration or kissing-number bound"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

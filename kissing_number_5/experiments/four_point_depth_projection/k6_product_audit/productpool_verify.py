#!/usr/bin/env python3
"""Exact standard-library verifier for the 74-atom K6 product extension."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

from experiments.four_point_depth_projection.k5_product_audit import (
    verify_product_extension_independent as direction_source,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "results"
    / "direct_k6_5000.csv"
)
EXTENSION = Path(__file__).with_name("productpool_extension.json")
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
POOL_SHA256 = (
    "45634e27071b348b66c02b4bbbfe9f23db713d2f3798589cbbd1c3750b0dcb68"
)
EXTENSION_SHA256 = (
    "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991"
)
DIRECTION_PARTITION_SHA256 = (
    "f351abd19eb17f2e4adcb14b8309bfd6cd212b7ac474fe57f283142927c9c756"
)
DIRECTION_SOURCE_SHA256 = (
    "62e3b6e1384b1b0740c832af656f1a9b99767d3b2337b6e7561382c18ba7a9d4"
)

N = 41
PAIRS = tuple((i, j) for i in range(6) for j in range(i + 1, 6))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix: list[list[int]]) -> int:
    """Bareiss determinant over the integers."""

    size = len(matrix)
    if size == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(pivot_index, size)
                if work[row][pivot_index]
            ),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = (
                work[pivot_row],
                work[pivot_index],
            )
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    pivot * work[row][column]
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def assert_rank_five_psd(edges: tuple[int, ...], values: tuple[int, ...]) -> int:
    matrix = [[4 if i == j else 0 for j in range(6)] for i in range(6)]
    for (i, j), color in zip(PAIRS, edges):
        matrix[i][j] = values[color]
        matrix[j][i] = values[color]
    fifth_minors = []
    for size in range(1, 7):
        for indices in itertools.combinations(range(6), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            value = determinant(minor)
            assert value >= 0
            if size == 5:
                fifth_minors.append(value)
            if size == 6:
                assert value == 0
    positive = [value for value in fifth_minors if value > 0]
    assert positive
    return min(positive)


def edge_color(edges: tuple[int, ...], first: int, second: int) -> int:
    return edges[PAIR_INDEX[tuple(sorted((first, second)))]]


def triangle_indices(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for i, j, k in itertools.combinations(range(6), 3):
        colors = tuple(
            sorted(
                (
                    edge_color(edges, i, j),
                    edge_color(edges, i, k),
                    edge_color(edges, j, k),
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def k6_state_slack_twice(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    capacity: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Twice the symmetrized K6 product slack, by direct local counts.

    A singleton among the 39 global residual vertices is retained in a
    six-set with conditional probability 4/39.  An ordered distinct pair is
    retained with probability 2/247.  Hence one oriented sampled row is

      39 M h + 39 r g - 4 r M - 494 c - 39 i >= 0,

    where i is the depth/common intersection and c=h*g-i.
    """

    slack = 0
    for position, (first, second) in enumerate(PAIRS):
        if edges[position] != base_index:
            continue
        remaining = [
            vertex for vertex in range(6) if vertex not in (first, second)
        ]
        gamma = {
            vertex: (
                edge_color(edges, first, vertex) >= threshold_index
                and edge_color(edges, second, vertex) >= threshold_index
            )
            for vertex in remaining
        }
        common = sum(gamma.values())
        for oriented_first, oriented_second in (
            (first, second),
            (second, first),
        ):
            depth = 0
            intersection = 0
            for vertex in remaining:
                first_color = edge_color(edges, oriented_first, vertex)
                second_color = edge_color(edges, oriented_second, vertex)
                in_depth = bool(table[7 * first_color + second_color])
                depth += int(in_depth)
                intersection += int(in_depth and gamma[vertex])
            distinct = depth * common - intersection
            slack += (
                39 * capacity * depth
                + 39 * required * common
                - 4 * required * capacity
                - 494 * distinct
                - 39 * intersection
            )
    return slack


def authenticate_pool_rows(
    active: tuple[int, ...],
    atoms: list[dict[str, object]],
) -> None:
    wanted = set(active)
    selected: dict[int, tuple[int, ...]] = {}
    with POOL.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == (
            "# positive_definite_k5_catalog=101272 selected_bases=5000 "
            "quadratic_rows=12005000 rank_five_labeled=157083 "
            "distinct_triangle_count_vectors=137296"
        )
        for index, line in enumerate(stream):
            if index in wanted:
                selected[index] = tuple(int(value) for value in line.split(","))
    assert set(selected) == wanted
    for index, atom in zip(active, atoms):
        fields = selected[index]
        assert len(fields) == 35
        assert tuple(
            atom[
                "edge_color_indices_"
                "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        ) == fields[:15]
        assert tuple(atom["triangle_orbit_indices"]) == fields[15:]


def verify(
    source_path: Path = SOURCE,
    pool_path: Path = POOL,
    extension_path: Path = EXTENSION,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(pool_path) == POOL_SHA256
    assert digest(extension_path) == EXTENSION_SHA256
    assert digest(Path(direction_source.__file__).resolve()) == DIRECTION_SOURCE_SHA256
    assert (
        digest(
            ROOT
            / "experiments"
            / "four_point_depth_projection"
            / "centered_quarter_pair_depth"
            / "verify.py"
        )
        == DIRECTION_PARTITION_SHA256
    )

    source = json.loads(source_path.read_text())
    extension = json.loads(extension_path.read_text())
    assert source["schema"] == "kissing5.centered_quarter_bv_pseudodistribution.v1"
    assert extension["schema"] == "kissing5.rank5_k6_product_extension.v1"
    assert extension["source_sha256"] == SOURCE_SHA256
    assert extension["pool_sha256"] == POOL_SHA256
    assert "not a complete enumeration" in extension["scope_warning"]
    assert extension["positive_atom_count"] == 74

    grid = tuple(Q(value) for value in source["grid"])
    scaled_values = tuple(int(4 * value) for value in grid)
    assert grid == (
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    )
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])

    atoms = extension["atoms"]
    active = tuple(extension["active_pool_indices"])
    assert len(atoms) == len(active) == len(set(active)) == 74
    authenticate_pool_rows(active, atoms)
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    parsed_atoms = []
    edge_marginal = [Q(0)] * 7
    triangle_marginal = [Q(0)] * 51
    minimum_fifth = None
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_"
                "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        assert len(edges) == 15 and all(0 <= color < 7 for color in edges)
        fifth = assert_rank_five_psd(edges, scaled_values)
        minimum_fifth = fifth if minimum_fifth is None else min(minimum_fifth, fifth)
        faces = triangle_indices(edges, triple_index)
        assert faces == tuple(atom["triangle_orbit_indices"])
        parsed_atoms.append(edges)
        for color in edges:
            edge_marginal[color] += weight
        for face in faces:
            triangle_marginal[face] += weight
    assert edge_marginal == [3 * value / 8 for value in alpha]
    assert triangle_marginal == [value / 78 for value in nu]

    families = direction_source.capacity_families(grid)
    assert families == (
        (1, 5, 6),
        (1, 6, 0),
        (2, 6, 1),
        (3, 6, 3),
        (4, 6, 6),
        (5, 6, 7),
        (6, 6, 7),
    )
    family_summary = []
    zero_keys = []
    minimum_positive = None
    rows_checked = 0
    for family_index, (
        base_index,
        threshold_index,
        capacity,
    ) in enumerate(families):
        states, coverage, feasible = direction_source.direction_states(
            base_index, grid, triples
        )
        for edges in parsed_atoms:
            for position, (first, second) in enumerate(PAIRS):
                if edges[position] != base_index:
                    continue
                for vertex in range(6):
                    if vertex in (first, second):
                        continue
                    pair = (
                        edge_color(edges, first, vertex),
                        edge_color(edges, second, vertex),
                    )
                    assert pair in feasible and pair[::-1] in feasible

        family_minimum = None
        family_zeros = 0
        for state_index, (required, table) in enumerate(states):
            slack = sum(
                weight
                * k6_state_slack_twice(
                    edges,
                    base_index,
                    threshold_index,
                    capacity,
                    required,
                    table,
                )
                for edges, weight in zip(parsed_atoms, weights)
            )
            assert slack >= 0
            rows_checked += 1
            family_minimum = (
                slack
                if family_minimum is None or slack < family_minimum
                else family_minimum
            )
            if slack == 0:
                family_zeros += 1
                zero_keys.append([family_index, state_index, required])
            elif minimum_positive is None or slack < minimum_positive:
                minimum_positive = slack
        family_summary.append(
            {
                "base_inner_product": str(grid[base_index]),
                "high_threshold": str(grid[threshold_index]),
                "capacity": capacity,
                "distinct_direction_states": coverage["distinct_states"],
                "zero_rows": family_zeros,
                "minimum_twice_symmetrized_slack": str(family_minimum),
            }
        )

    assert rows_checked == 560
    assert zero_keys == extension["zero_product_row_keys"]
    assert len(zero_keys) == 113
    assert [
        {
            key: item[key]
            for key in (
                "base_inner_product",
                "high_threshold",
                "capacity",
                "distinct_direction_states",
            )
        }
        for item in family_summary
    ] == extension["product_family_summary"]
    assert minimum_positive is not None and minimum_positive > 0

    return {
        "status": "PASS",
        "conclusion": (
            "the exact 74-atom rank-five K6 mixture matches the centered "
            "triangle marginal and passes all 560 product rows"
        ),
        "source_sha256": SOURCE_SHA256,
        "pool_sha256": POOL_SHA256,
        "extension_sha256": EXTENSION_SHA256,
        "positive_atoms": len(atoms),
        "minimum_positive_scaled_fifth_minor": minimum_fifth,
        "edge_marginal": "exact 3 alpha/8",
        "triangle_marginal": "exact nu/78",
        "product_rows": rows_checked,
        "zero_product_rows": len(zero_keys),
        "minimum_positive_twice_symmetrized_slack": minimum_positive,
        "product_families": family_summary,
        "scope": (
            "positive local K6 construction from an incomplete discovery "
            "pool; not a global code or complete K6 enumeration"
        ),
    }


if __name__ == "__main__":
    report = verify()
    print(
        json.dumps(
            {
                key: str(value) if isinstance(value, Q) else value
                for key, value in report.items()
            },
            indent=2,
            sort_keys=True,
        )
    )

#!/usr/bin/env python3
"""Independent exact verifier for the candidate rank-five K7 mixture.

This standard-library verifier does not import the floating-point search
program and does not use its compressed product-feature formula.  It
authenticates the selected catalog rows, reconstructs each Gram matrix and
all triangle types, checks every principal minor, recomputes both marginals,
and evaluates all 560 product inequalities directly from local set counts.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

from experiments.four_point_depth_projection.k5_product_audit import (
    verify_product_extension_independent as direction_source,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
POOL = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)
CANDIDATE = HERE / "candidate_k7_product_extension.json"

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
POOL_SHA256 = (
    "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623"
)
CANDIDATE_SHA256 = (
    "1b5e262592e1872cfe9f26b344d82da5066d8332efc5104a34a433d9d5564b00"
)
DIRECTION_SOURCE_SHA256 = (
    "62e3b6e1384b1b0740c832af656f1a9b99767d3b2337b6e7561382c18ba7a9d4"
)
DIRECTION_PARTITION_SHA256 = (
    "f351abd19eb17f2e4adcb14b8309bfd6cd212b7ac474fe57f283142927c9c756"
)

PAIRS = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}
EDGE_KEY = (
    "edge_color_indices_"
    "01_02_03_04_05_06_12_13_14_15_16_"
    "23_24_25_26_34_35_36_45_46_56"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix: list[list[int]]) -> int:
    """Compute an integer determinant by fraction-free Bareiss elimination."""

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
                if work[row][pivot_index] != 0
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


def gram(edges: tuple[int, ...], scaled_values: tuple[int, ...]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(7)] for i in range(7)]
    assert len(PAIRS) == len(edges)
    for (first, second), color in zip(PAIRS, edges):
        matrix[first][second] = scaled_values[color]
        matrix[second][first] = scaled_values[color]
    return matrix


def assert_rank_five_psd(
    edges: tuple[int, ...],
    scaled_values: tuple[int, ...],
) -> int:
    """Check PSD and rank exactly five via all principal minors."""

    matrix = gram(edges, scaled_values)
    positive_fifth = []
    for size in range(1, 8):
        for indices in itertools.combinations(range(7), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            value = determinant(minor)
            assert value >= 0
            if size == 5 and value > 0:
                positive_fifth.append(value)
            if size >= 6:
                assert value == 0
    assert positive_fifth
    return min(positive_fifth)


def edge_color(edges: tuple[int, ...], first: int, second: int) -> int:
    return edges[PAIR_INDEX[tuple(sorted((first, second)))]]


def triangle_indices(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for first, second, third in itertools.combinations(range(7), 3):
        colors = tuple(
            sorted(
                (
                    edge_color(edges, first, second),
                    edge_color(edges, first, third),
                    edge_color(edges, second, third),
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def authenticate_pool_rows(
    active: tuple[int, ...],
    atoms: list[dict[str, object]],
    pool_path: Path,
) -> None:
    wanted = set(active)
    selected: dict[int, tuple[int, ...]] = {}
    with pool_path.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == (
            "# source_k6_atoms=51 rank_five_labeled=2012 "
            "distinct_triangle_count_vectors=1782"
        )
        for index, line in enumerate(stream):
            if index in wanted:
                selected[index] = tuple(int(value) for value in line.split(","))
    assert set(selected) == wanted
    assert len(active) == len(atoms)
    for index, atom in zip(active, atoms):
        fields = selected[index]
        assert len(fields) == 56
        assert tuple(atom[EDGE_KEY]) == fields[:21]
        assert tuple(atom["triangle_orbit_indices"]) == fields[21:]


def k7_product_slack_oriented_sum(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    capacity: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Evaluate the K7 product slack by direct membership counting.

    Fixing an oriented base edge leaves 39 global residual vertices.  A K7
    face retains five.  If h,g,i,c are respectively the sampled depth count,
    common-neighbor count, intersection count, and ordered distinct-pair
    count, the finite-population row is

      78 M h + 78 r g - 10 r M - 741 c - 78 i >= 0.

    We sum this expression over both orientations of every base-colored edge.
    """

    slack = 0
    for position, (first, second) in enumerate(PAIRS):
        if edges[position] != base_index:
            continue
        remaining = [
            vertex for vertex in range(7) if vertex not in (first, second)
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
                78 * capacity * depth
                + 78 * required * common
                - 10 * required * capacity
                - 741 * distinct
                - 78 * intersection
            )
    return slack


def verify(
    source_path: Path = SOURCE,
    pool_path: Path = POOL,
    candidate_path: Path = CANDIDATE,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(pool_path) == POOL_SHA256
    assert digest(candidate_path) == CANDIDATE_SHA256
    assert digest(Path(direction_source.__file__).resolve()) == (
        DIRECTION_SOURCE_SHA256
    )
    assert digest(
        ROOT
        / "experiments"
        / "four_point_depth_projection"
        / "centered_quarter_pair_depth"
        / "verify.py"
    ) == DIRECTION_PARTITION_SHA256

    source = json.loads(source_path.read_text())
    candidate = json.loads(candidate_path.read_text())
    assert source["schema"] == "kissing5.centered_quarter_bv_pseudodistribution.v1"
    assert candidate["schema"] == "kissing5.rank5_k7_product_extension.v1"
    assert candidate["source_sha256"] == SOURCE_SHA256
    assert candidate["pool_sha256"] == POOL_SHA256
    assert "not a complete enumeration" in candidate["scope_warning"]

    grid = tuple(Q(value) for value in source["grid"])
    assert grid == (
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    )
    scaled_values = tuple(int(4 * value) for value in grid)
    assert all(
        Q(value, 4) == node
        for value, node in zip(scaled_values, grid)
    )
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert len(triple_index) == 51
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])

    atoms = candidate["atoms"]
    active = tuple(candidate["active_pool_indices"])
    assert len(atoms) == len(active) == len(set(active))
    assert len(atoms) == candidate["positive_atom_count"] == 53
    authenticate_pool_rows(active, atoms, pool_path)
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    parsed_atoms = []
    edge_counts = [Q(0)] * 7
    triangle_counts = [Q(0)] * 51
    minimum_positive_fifth = None
    assert len(atoms) == len(weights)
    for atom, weight in zip(atoms, weights):
        edges = tuple(atom[EDGE_KEY])
        assert len(edges) == 21 and all(0 <= color < 7 for color in edges)
        fifth = assert_rank_five_psd(edges, scaled_values)
        minimum_positive_fifth = (
            fifth
            if minimum_positive_fifth is None
            else min(minimum_positive_fifth, fifth)
        )
        faces = triangle_indices(edges, triple_index)
        assert faces == tuple(atom["triangle_orbit_indices"])
        parsed_atoms.append(edges)
        for color in edges:
            edge_counts[color] += weight
        for face in faces:
            triangle_counts[face] += weight

    assert edge_counts == [Q(21) * value / 40 for value in alpha]
    assert triangle_counts == [Q(7) * value / 312 for value in nu]

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
    rows_checked = 0
    zero_keys = []
    family_summary = []
    minimum_positive = None
    for family_index, (
        base_index,
        threshold_index,
        capacity,
    ) in enumerate(families):
        states, coverage, feasible = direction_source.direction_states(
            base_index, grid, triples
        )
        assert len(states) == coverage["distinct_states"]
        for edges in parsed_atoms:
            for position, (first, second) in enumerate(PAIRS):
                if edges[position] != base_index:
                    continue
                for vertex in range(7):
                    if vertex in (first, second):
                        continue
                    pair = (
                        edge_color(edges, first, vertex),
                        edge_color(edges, second, vertex),
                    )
                    assert pair in feasible and pair[::-1] in feasible

        family_zeros = 0
        family_minimum = None
        for state_index, (required, table) in enumerate(states):
            slack = sum(
                weight
                * k7_product_slack_oriented_sum(
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
                "minimum_oriented_sum_slack": str(family_minimum),
            }
        )

    assert rows_checked == 560
    assert zero_keys == candidate["zero_product_row_keys"]
    assert minimum_positive is not None
    assert str(minimum_positive) == (
        candidate["minimum_positive_twice_symmetrized_slack"]
    )
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
    ] == candidate["product_family_summary"]

    return {
        "status": "PASS",
        "conclusion": (
            "the exact 53-atom rank-five K7 mixture matches alpha/40 and "
            "nu/1560 and passes all 560 currently proved product rows"
        ),
        "source_sha256": SOURCE_SHA256,
        "pool_sha256": POOL_SHA256,
        "candidate_sha256": CANDIDATE_SHA256,
        "positive_atoms": len(atoms),
        "minimum_positive_scaled_fifth_minor": minimum_positive_fifth,
        "edge_marginal": "exact alpha/40 per uniformly sampled K7 edge",
        "triangle_marginal": "exact nu/1560 per uniformly sampled K7 triangle",
        "product_rows": rows_checked,
        "zero_product_rows": len(zero_keys),
        "minimum_positive_oriented_sum_slack": str(minimum_positive),
        "product_families": family_summary,
        "scope": (
            "positive local K7 construction from an incomplete discovery "
            "pool; not a global code or overlapping-face/Lasserre certificate"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

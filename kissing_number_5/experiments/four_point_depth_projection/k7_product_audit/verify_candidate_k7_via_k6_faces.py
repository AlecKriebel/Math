#!/usr/bin/env python3
"""Second exact audit of the K7 candidate through its seven K6 faces.

This verifier uses an exact LDL^T/Schur factorization rather than principal
minors to prove that every Gram atom is PSD of rank five.  It also evaluates
the product rows only after deleting each of the seven vertices and applying
the already-derived K6 finite-population expression.  Thus it does not reuse
the K7 compressed feature implementation used during discovery.
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

PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
EDGE_KEY = (
    "edge_color_indices_"
    "01_02_03_04_05_06_12_13_14_15_16_"
    "23_24_25_26_34_35_36_45_46_56"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gram7(
    edges: tuple[int, ...],
    scaled_values: tuple[int, ...],
) -> list[list[Q]]:
    matrix = [[Q(4 if i == j else 0) for j in range(7)] for i in range(7)]
    for (first, second), color in zip(PAIRS7, edges):
        matrix[first][second] = Q(scaled_values[color])
        matrix[second][first] = Q(scaled_values[color])
    return matrix


def positive_ldlt(
    matrix: list[list[Q]],
    indices: tuple[int, ...],
) -> tuple[list[list[Q]], list[Q]] | None:
    """Return a positive LDL^T factorization, or None if a pivot is nonpositive."""

    size = len(indices)
    lower = [[Q(0) for _ in range(size)] for _ in range(size)]
    diagonal = [Q(0)] * size
    for row in range(size):
        lower[row][row] = Q(1)
        for column in range(row):
            numerator = matrix[indices[row]][indices[column]]
            numerator -= sum(
                lower[row][prior]
                * diagonal[prior]
                * lower[column][prior]
                for prior in range(column)
            )
            lower[row][column] = numerator / diagonal[column]
        diagonal[row] = matrix[indices[row]][indices[row]] - sum(
            lower[row][prior] ** 2 * diagonal[prior]
            for prior in range(row)
        )
        if diagonal[row] <= 0:
            return None
    return lower, diagonal


def assert_rank_five_psd_ldlt(
    edges: tuple[int, ...],
    scaled_values: tuple[int, ...],
) -> Q:
    """Prove A = X D X^T with exactly five positive diagonal entries."""

    matrix = gram7(edges, scaled_values)
    for base in itertools.combinations(range(7), 5):
        factorization = positive_ldlt(matrix, base)
        if factorization is not None:
            break
    else:
        raise AssertionError("no positive definite principal five-block")
    lower, diagonal = factorization
    complement = tuple(index for index in range(7) if index not in base)

    # Coordinates of the two remaining rows in the positive five-block's
    # LDL basis.
    extension_rows = []
    for vertex in complement:
        row = [Q(0)] * 5
        for column in range(5):
            numerator = matrix[vertex][base[column]]
            numerator -= sum(
                row[prior]
                * diagonal[prior]
                * lower[column][prior]
                for prior in range(column)
            )
            row[column] = numerator / diagonal[column]
        extension_rows.append(row)

    # Exact zero Schur complement proves the full matrix is PSD and has the
    # same rank as the positive five-block.
    for first_position, first in enumerate(complement):
        for second_position, second in enumerate(complement):
            residual = matrix[first][second] - sum(
                extension_rows[first_position][index]
                * diagonal[index]
                * extension_rows[second_position][index]
                for index in range(5)
            )
            assert residual == 0
    return min(diagonal)


def edge7(edges: tuple[int, ...], first: int, second: int) -> int:
    return edges[PAIR_INDEX7[tuple(sorted((first, second)))]]


def delete_vertex(edges: tuple[int, ...], omitted: int) -> tuple[int, ...]:
    kept = tuple(vertex for vertex in range(7) if vertex != omitted)
    return tuple(edge7(edges, kept[first], kept[second]) for first, second in PAIRS6)


def edge6(edges: tuple[int, ...], first: int, second: int) -> int:
    return edges[PAIR_INDEX6[tuple(sorted((first, second)))]]


def k6_product_slack_oriented_sum(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    capacity: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Direct K6 count for 494c+39i <= 39Mh+39rg-4rM."""

    slack = 0
    for position, (first, second) in enumerate(PAIRS6):
        if edges[position] != base_index:
            continue
        remaining = [
            vertex for vertex in range(6) if vertex not in (first, second)
        ]
        gamma = {
            vertex: (
                edge6(edges, first, vertex) >= threshold_index
                and edge6(edges, second, vertex) >= threshold_index
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
                in_depth = bool(
                    table[
                        7 * edge6(edges, oriented_first, vertex)
                        + edge6(edges, oriented_second, vertex)
                    ]
                )
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


def triangle_types7(edges: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        tuple(
            sorted(
                (
                    edge7(edges, first, second),
                    edge7(edges, first, third),
                    edge7(edges, second, third),
                )
            )
        )
        for first, second, third in itertools.combinations(range(7), 3)
    )


def authenticate_pool(
    active: tuple[int, ...],
    atoms: list[dict[str, object]],
) -> None:
    wanted = set(active)
    selected = {}
    with POOL.open() as stream:
        assert next(stream).rstrip("\n") == (
            "# source_k6_atoms=51 rank_five_labeled=2012 "
            "distinct_triangle_count_vectors=1782"
        )
        for index, line in enumerate(stream):
            if index in wanted:
                selected[index] = tuple(int(field) for field in line.split(","))
    assert set(selected) == wanted
    for index, atom in zip(active, atoms):
        assert tuple(atom[EDGE_KEY]) == selected[index][:21]
        assert tuple(atom["triangle_orbit_indices"]) == selected[index][21:]


def verify() -> dict[str, object]:
    assert digest(SOURCE) == SOURCE_SHA256
    assert digest(POOL) == POOL_SHA256
    assert digest(CANDIDATE) == CANDIDATE_SHA256
    source = json.loads(SOURCE.read_text())
    candidate = json.loads(CANDIDATE.read_text())
    assert candidate["schema"] == "kissing5.rank5_k7_product_extension.v1"

    grid = tuple(Q(value) for value in source["grid"])
    scaled_values = tuple(int(4 * value) for value in grid)
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])

    atoms = candidate["atoms"]
    active = tuple(candidate["active_pool_indices"])
    assert len(atoms) == len(active) == 53
    authenticate_pool(active, atoms)
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    parsed = []
    deleted = []
    edge_marginal = [Q(0)] * 7
    triangle_marginal = [Q(0)] * 51
    minimum_positive_ldl_pivot = None
    for atom, weight in zip(atoms, weights):
        edges = tuple(atom[EDGE_KEY])
        pivot = assert_rank_five_psd_ldlt(edges, scaled_values)
        minimum_positive_ldl_pivot = (
            pivot
            if minimum_positive_ldl_pivot is None
            else min(minimum_positive_ldl_pivot, pivot)
        )
        types = triangle_types7(edges)
        feature = tuple(sorted(triple_index[item] for item in types))
        assert feature == tuple(atom["triangle_orbit_indices"])
        parsed.append(edges)
        deleted.append(tuple(delete_vertex(edges, omitted) for omitted in range(7)))
        for color in edges:
            edge_marginal[color] += weight
        for item in types:
            triangle_marginal[triple_index[item]] += weight
    assert edge_marginal == [Q(21) * value / 40 for value in alpha]
    assert triangle_marginal == [Q(7) * value / 312 for value in nu]

    rows_checked = 0
    zero_keys = []
    minimum_positive = None
    for family_index, (
        base_index,
        threshold_index,
        capacity,
    ) in enumerate(direction_source.capacity_families(grid)):
        states, _coverage, _feasible = direction_source.direction_states(
            base_index, grid, triples
        )
        for state_index, (required, table) in enumerate(states):
            # For each original oriented K7 base edge, its five residual
            # deletions give the five containing K6 faces.  The K7 cleared
            # slack is exactly half their sum.
            twice_slack = sum(
                weight
                * sum(
                    k6_product_slack_oriented_sum(
                        face,
                        base_index,
                        threshold_index,
                        capacity,
                        required,
                        table,
                    )
                    for face in faces
                )
                for faces, weight in zip(deleted, weights)
            )
            assert twice_slack >= 0
            slack = twice_slack / 2
            rows_checked += 1
            if slack == 0:
                zero_keys.append([family_index, state_index, required])
            elif minimum_positive is None or slack < minimum_positive:
                minimum_positive = slack

    assert rows_checked == 560
    assert zero_keys == candidate["zero_product_row_keys"]
    assert minimum_positive is not None
    assert str(minimum_positive) == (
        candidate["minimum_positive_twice_symmetrized_slack"]
    )
    return {
        "status": "PASS",
        "conclusion": (
            "exact LDL/Schur atom audit and deletion-to-K6 product audit "
            "both confirm the 53-atom K7 candidate"
        ),
        "candidate_sha256": CANDIDATE_SHA256,
        "positive_atoms": len(atoms),
        "minimum_positive_ldl_pivot": str(minimum_positive_ldl_pivot),
        "edge_marginal": "exact alpha/40",
        "triangle_marginal": "exact nu/1560",
        "product_rows_via_k6_faces": rows_checked,
        "zero_product_rows": len(zero_keys),
        "minimum_positive_k7_slack": str(minimum_positive),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

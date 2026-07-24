#!/usr/bin/env python3
"""Exact semantic audit of depth/common-product rows on the K5 extension.

The stored K5 representatives are understood symmetrically: choose a
representative with its stored weight, then relabel it by a uniform element
of S_5.  All statistics below are sums over the ten base edges, so their
values can be computed on one representative without expanding its orbit.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
from typing import NamedTuple


N = 41
DELTA = Q(1, 300)
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
EXTENSION_SHA256 = (
    "133e8b502653b3bb1e1c4c3eb6c0452705020f65128959dc9d0cb34a8c0645ef"
)
EDGE_POSITIONS = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)


class Row(NamedTuple):
    base_index: int
    base: Q
    threshold: Q
    capacity: int

    @property
    def name(self) -> str:
        return (
            f"q={rational_string(self.base)},"
            f"b={rational_string(self.threshold)},M={self.capacity}"
        )


def rational_string(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix: list[list[int]]) -> int:
    """Tiny exact determinant, sufficient for principal orders at most five."""

    size = len(matrix)
    answer = 0
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        product = 1
        for row, column in enumerate(permutation):
            product *= matrix[row][column]
        answer += (-1 if inversions % 2 else 1) * product
    return answer


def edge_dictionary(edges: tuple[int, ...]) -> dict[tuple[int, int], int]:
    return dict(zip(EDGE_POSITIONS, edges))


def triangle_types(edges: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    edge = edge_dictionary(edges)
    return tuple(
        tuple(sorted((edge[(i, j)], edge[(i, k)], edge[(j, k)])))
        for i in range(5)
        for j in range(i + 1, 5)
        for k in range(j + 1, 5)
    )


def scaled_gram(edges: tuple[int, ...], scaled_values: list[int]) -> list[list[int]]:
    matrix = [[4 if i == j else 0 for j in range(5)] for i in range(5)]
    for color, (i, j) in zip(edges, EDGE_POSITIONS):
        matrix[i][j] = scaled_values[color]
        matrix[j][i] = scaled_values[color]
    return matrix


def assert_gram_psd(matrix: list[list[int]]) -> None:
    for size in range(1, 6):
        for indices in itertools.combinations(range(5), size):
            principal = [
                [matrix[i][j] for j in indices]
                for i in indices
            ]
            assert determinant(principal) >= 0


def negative_sum_tail(base: Q, first: Q, second: Q) -> bool:
    """Test first+second < -delta*sqrt(2+2*base) without rounding."""

    if base <= -1:
        raise ValueError("the y+z direction is undefined for an antipodal base")
    total = first + second
    return (
        total < 0
        and total * total > DELTA * DELTA * (2 + 2 * base)
    )


def common_neighbor(first: Q, second: Q, threshold: Q) -> bool:
    assert threshold > 0
    return first >= threshold and second >= threshold


def common_pair_capacity(base: Q, threshold: Q) -> int | None:
    """The exact endpoint conventions of the proved capacity rows."""

    assert 0 < threshold <= Q(1, 2)
    if base == -1:
        return 0
    if base <= 0:
        projected = 2 * threshold * threshold / (1 + base)
        if projected > 1:
            return 0
        if projected > Q(3, 4):
            return 1
        if projected > Q(2, 3):
            return 2
        if projected > Q(5, 8):
            return 3
        if projected > Q(1, 2):
            return 4
        if projected == Q(1, 2):
            return 6
        return None
    if threshold == Q(1, 2):
        # The separately proved positive-base common-contact cap.
        return 7
    return None


def strongest_quarter_grid_rows(grid: list[Q]) -> tuple[Row, ...]:
    """One strongest row for every distinct quarter-grid neighbor set.

    Between consecutive positive support nodes the selected common-neighbor
    set is unchanged.  Capacity is nonincreasing with the threshold, so the
    right endpoint is strongest.  The antipodal base is omitted because the
    robust y+z direction defining H is then undefined.
    """

    rows = []
    for threshold in (Q(1, 4), Q(1, 2)):
        for base_index, base in enumerate(grid):
            if base == -1:
                continue
            capacity = common_pair_capacity(base, threshold)
            if capacity is not None:
                rows.append(Row(base_index, base, threshold, capacity))
    return tuple(rows)


def relabel_edges(
    edges: tuple[int, ...], permutation: tuple[int, ...]
) -> tuple[int, ...]:
    old = edge_dictionary(edges)
    new: dict[tuple[int, int], int] = {}
    for (i, j), color in old.items():
        new[tuple(sorted((permutation[i], permutation[j])))] = color
    return tuple(new[position] for position in EDGE_POSITIONS)


def atom_row_counts(
    edges: tuple[int, ...], grid: list[Q], row: Row
) -> tuple[int, int, int, int]:
    """Return B, h, g, p=sum_e h_e*g_e for one labeled K5 atom."""

    edge = edge_dictionary(edges)
    base_count = 0
    depth_count = 0
    common_count = 0
    product_count = 0
    for i, j in EDGE_POSITIONS:
        if edge[(i, j)] != row.base_index:
            continue
        base_count += 1
        local_depth = 0
        local_common = 0
        for vertex in range(5):
            if vertex in (i, j):
                continue
            first = grid[edge[tuple(sorted((i, vertex)))]]
            second = grid[edge[tuple(sorted((j, vertex)))]]
            in_depth = negative_sum_tail(row.base, first, second)
            in_common = common_neighbor(first, second, row.threshold)
            # Strictly negative sum versus sum at least 2b>0.
            assert not (in_depth and in_common)
            local_depth += int(in_depth)
            local_common += int(in_common)
        depth_count += local_depth
        common_count += local_common
        # The two sets are disjoint, so this is an ordered distinct pair
        # count, not a diagonal-contaminated second moment.
        product_count += local_depth * local_common
    return base_count, depth_count, common_count, product_count


def verify(source_path: Path, extension_path: Path) -> dict[str, object]:
    assert sha256(source_path) == SOURCE_SHA256
    assert sha256(extension_path) == EXTENSION_SHA256
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    extension = json.loads(extension_path.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert extension["schema"] == (
        "kissing5.centered_quarter_k5_extension.v1"
    )
    assert extension["source_certificate"] == source_path.name
    assert extension["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert extension["edge_order"] == [
        "01",
        "02",
        "03",
        "04",
        "12",
        "13",
        "14",
        "23",
        "24",
        "34",
    ]

    grid = [Q(value) for value in source["grid"]]
    scaled_values = [int(4 * value) for value in grid]
    assert all(Q(value, 4) == node for value, node in zip(scaled_values, grid))
    alpha = [Q(value) for value in source["alpha"]]
    nu = [Q(value) for value in source["nu"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert sum(alpha) == N - 1
    assert sum(nu) == (N - 1) * (N - 2)

    atoms = extension["atoms"]
    weights = [Q(atom["weight"]) for atom in atoms]
    assert len(atoms) == extension["positive_atom_count"] == 51
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    edge_marginal = [Q(0)] * len(grid)
    triangle_marginal = [Q(0)] * len(triples)
    parsed_atoms: list[tuple[tuple[int, ...], Q]] = []
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        assert len(edges) == 10
        assert all(0 <= color < len(grid) for color in edges)
        faces = triangle_types(edges)
        assert all(face in triple_index for face in faces)
        feature = tuple(sorted(triple_index[face] for face in faces))
        assert feature == tuple(atom["triangle_orbit_indices"])
        assert_gram_psd(scaled_gram(edges, scaled_values))
        for color in edges:
            edge_marginal[color] += weight
        for index in feature:
            triangle_marginal[index] += weight
        parsed_atoms.append((edges, weight))

    assert all(
        observed == target / 4
        for observed, target in zip(edge_marginal, alpha)
    )
    assert all(
        observed == target / 156
        for observed, target in zip(triangle_marginal, nu)
    )

    rows = strongest_quarter_grid_rows(grid)
    assert tuple(row.name for row in rows) == (
        "q=-3/4,b=1/4,M=6",
        "q=-3/4,b=1/2,M=0",
        "q=-1/2,b=1/2,M=1",
        "q=-1/4,b=1/2,M=3",
        "q=0,b=1/2,M=6",
        "q=1/4,b=1/2,M=7",
        "q=1/2,b=1/2,M=7",
    )

    # On this grid the exact strict radical test is equivalent to sum < 0:
    # every sum is a multiple of 1/4, while
    # delta*sqrt(2+2q) <= sqrt(3)/300 < 1/4.
    for base in grid[1:]:
        for first in grid:
            for second in grid:
                assert negative_sum_tail(base, first, second) == (
                    first + second < 0
                )

    totals = {
        row.name: {
            "base": Q(0),
            "depth": Q(0),
            "common": Q(0),
            "product": Q(0),
        }
        for row in rows
    }
    permutations = tuple(itertools.permutations(range(5)))
    for edges, weight in parsed_atoms:
        original = {
            row.name: atom_row_counts(edges, grid, row)
            for row in rows
        }
        # This explicitly checks that no orbit-size or automorphism factor is
        # missing when a stored representative is uniformly relabeled.
        for permutation in permutations:
            relabeled = relabel_edges(edges, permutation)
            assert all(
                atom_row_counts(relabeled, grid, row)
                == original[row.name]
                for row in rows
            )
        for row in rows:
            base, depth, common, product = original[row.name]
            totals[row.name]["base"] += weight * base
            totals[row.name]["depth"] += weight * depth
            totals[row.name]["common"] += weight * common
            totals[row.name]["product"] += weight * product

    row_reports = []
    violations = []
    for row in rows:
        values = totals[row.name]
        base = values["base"]
        depth = values["depth"]
        common = values["common"]
        product = values["product"]
        assert base == alpha[row.base_index] / 4

        # Conditional on a fixed global edge, a uniform K5 retains three of
        # its 39 residual vertices.  Thus E[h]=H/13, E[g]=Gamma/13, and,
        # because the sets are disjoint, E[h*g]=H*Gamma/247.
        decoded_depth = Q(13) * depth / base
        decoded_common = Q(13) * common / base
        decoded_product = Q(247) * product / base

        residual = (
            Q(247) * product
            - Q(13 * row.capacity) * depth
            - Q(91) * common
            + Q(7 * row.capacity) * base
        )
        decoded_slack = -residual / base
        assert decoded_depth >= 7
        assert decoded_common <= row.capacity
        assert decoded_slack == (
            row.capacity * decoded_depth
            + 7 * decoded_common
            - 7 * row.capacity
            - decoded_product
        )
        passes = residual <= 0
        if not passes:
            violations.append(row.name)
        row_reports.append(
            {
                "row": row.name,
                "expected_base_edges_per_k5": rational_string(base),
                "expected_sampled_depth_incidents": rational_string(depth),
                "expected_sampled_common_incidents": rational_string(common),
                "expected_sampled_ordered_product_pairs": rational_string(
                    product
                ),
                "decoded_mean_H": rational_string(decoded_depth),
                "decoded_mean_Gamma": rational_string(decoded_common),
                "decoded_mean_H_Gamma": rational_string(decoded_product),
                "decoded_slack_rhs_minus_lhs": rational_string(
                    decoded_slack
                ),
                "raw_scaled_residual_must_be_nonpositive": rational_string(
                    residual
                ),
                "passes_product_row": passes,
            }
        )

    assert violations == [
        "q=-1/2,b=1/2,M=1",
        "q=-1/4,b=1/2,M=3",
    ]
    return {
        "status": "PASS",
        "meaning": (
            "the semantic audit passes; the stored K5 extension itself "
            "violates two necessary depth/common-product rows"
        ),
        "source_sha256": SOURCE_SHA256,
        "extension_sha256": EXTENSION_SHA256,
        "normalization": {
            "sampled_depth": "E[h_e | e]=H_e/13",
            "sampled_common": "E[g_e | e]=Gamma_e/13",
            "sampled_product": "E[h_e*g_e | e]=H_e*Gamma_e/247",
            "atom_row": (
                "sum_A w_A sum_e "
                "(247 h_e g_e-13 M_e h_e-91 g_e+7 M_e) <= 0"
            ),
        },
        "rows_checked": len(rows),
        "violating_rows": violations,
        "rows": row_reports,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    report = verify(
        root / "certificates" / "centered_quarter_bv_pseudodistribution.json",
        root / "certificates" / "centered_quarter_k5_extension.json",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

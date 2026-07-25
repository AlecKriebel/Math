#!/usr/bin/env python3
"""Independent exact verifier for the 64-atom K5 product extension.

This verifier does not import or execute the floating-point discovery
program.  It reconstructs the continuum direction states from the separately
audited exact projective-line partition and evaluates the product inequality
directly from local counts.  In particular, it does not reuse the discovery
program's compressed feature formula.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

from experiments.four_point_depth_projection.centered_quarter_pair_depth import (
    verify as direction_audit,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
EXTENSION = Path(__file__).with_name(
    "centered_quarter_k5_product_extension.json"
)

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
EXTENSION_SHA256 = (
    "cf369d35fbe448cfba6668fedcd6bb2f53b4e7ed12c3b00cae5826a63a1b8a8c"
)
DIRECTION_AUDIT_SHA256 = (
    "f351abd19eb17f2e4adcb14b8309bfd6cd212b7ac474fe57f283142927c9c756"
)

N = 41
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
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGE_POSITIONS)}
PERMUTATIONS = tuple(itertools.permutations(range(5)))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstring(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


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


def edge_map(edges: tuple[int, ...]) -> dict[tuple[int, int], int]:
    return dict(zip(EDGE_POSITIONS, edges))


def triangle_types(edges: tuple[int, ...]) -> tuple[tuple[int, int, int], ...]:
    edge = edge_map(edges)
    return tuple(
        tuple(sorted((edge[(i, j)], edge[(i, k)], edge[(j, k)])))
        for i in range(5)
        for j in range(i + 1, 5)
        for k in range(j + 1, 5)
    )


def assert_local_gram_psd(edges: tuple[int, ...], values: list[int]) -> None:
    matrix = [[4 if i == j else 0 for j in range(5)] for i in range(5)]
    for (i, j), color in zip(EDGE_POSITIONS, edges):
        matrix[i][j] = values[color]
        matrix[j][i] = values[color]
    for size in range(1, 6):
        for indices in itertools.combinations(range(5), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            assert determinant(minor) >= 0


def canonical_orbit(edges: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    old = edge_map(edges)
    relabeled = set()
    for permutation in PERMUTATIONS:
        new = {
            tuple(sorted((permutation[i], permutation[j]))): color
            for (i, j), color in old.items()
        }
        relabeled.add(tuple(new[position] for position in EDGE_POSITIONS))
    return min(relabeled), len(relabeled)


def capacity(base: Q, threshold: Q) -> int | None:
    assert -1 < base <= Q(1, 2)
    assert 0 < threshold <= Q(1, 2)
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
        return 7
    return None


def capacity_families(grid: tuple[Q, ...]) -> tuple[tuple[int, int, int], ...]:
    families = []
    for base_index, base in enumerate(grid):
        if base == -1:
            continue
        for threshold in (Q(1, 4), Q(1, 2)):
            bound = capacity(base, threshold)
            if bound is not None:
                families.append(
                    (base_index, grid.index(threshold), bound)
                )
    return tuple(families)


def feasible_incident_pairs(
    base_index: int,
    triples: tuple[tuple[int, int, int], ...],
) -> set[tuple[int, int]]:
    pairs = set()
    for triple in triples:
        for position in range(3):
            if triple[position] != base_index:
                continue
            others = [
                triple[other]
                for other in range(3)
                if other != position
            ]
            pairs.add((others[0], others[1]))
            pairs.add((others[1], others[0]))
    return pairs


def direction_states(
    base_index: int,
    grid: tuple[Q, ...],
    triples: tuple[tuple[int, int, int], ...],
) -> tuple[
    tuple[tuple[int, tuple[int, ...]], ...],
    dict[str, int],
    set[tuple[int, int]],
]:
    """Regenerate every relevant strict-tail state on the projective line."""

    base = grid[base_index]
    assert base > -1
    feasible_indices = feasible_incident_pairs(base_index, triples)
    event_pairs = {
        (grid[first], grid[second])
        for first, second in feasible_indices
    }
    event_pairs.update(((Q(1), base), (base, Q(1))))
    roots = direction_audit.critical_roots(base, event_pairs)
    samples = direction_audit.open_cell_samples(roots)
    states: set[tuple[int, tuple[int, ...]]] = set()

    def add_rational(slope: Q, orientation: int) -> None:
        endpoints = sum(
            direction_audit.rational_qualifies(
                first, second, base, slope, orientation
            )
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        table = tuple(
            int(
                direction_audit.rational_qualifies(
                    first, second, base, slope, orientation
                )
            )
            for first in grid
            for second in grid
        )
        states.add((7 - endpoints, table))

    def add_root(root: direction_audit.ExactRoot, orientation: int) -> None:
        endpoints = sum(
            direction_audit.root_qualifies(
                first, second, base, root, orientation
            )
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        table = tuple(
            int(
                direction_audit.root_qualifies(
                    first, second, base, root, orientation
                )
            )
            for first in grid
            for second in grid
        )
        states.add((7 - endpoints, table))

    for sample in samples:
        for orientation in (1, -1):
            add_rational(sample, orientation)
    strict_boundary_events = 0
    for root in roots:
        boundary_pairs = []
        for first, second in event_pairs:
            boundary_sign = root.sign_polynomial(
                first * first - direction_audit.DELTA_SQUARED,
                2
                * (
                    first * second
                    - direction_audit.DELTA_SQUARED * base
                ),
                second * second - direction_audit.DELTA_SQUARED,
            )
            if boundary_sign == 0:
                boundary_pairs.append((first, second))
        assert boundary_pairs
        # At the orientation making a nonzero boundary projection positive,
        # strict equality is excluded.  Zero projection is excluded too.
        for first, second in boundary_pairs:
            for orientation in (1, -1):
                assert not direction_audit.root_qualifies(
                    first, second, base, root, orientation
                )
        strict_boundary_events += len(boundary_pairs)
        for orientation in (1, -1):
            add_root(root, orientation)

    for direction in ((Q(0), Q(1)), (Q(0), Q(-1))):
        endpoints = sum(
            direction_audit.direction_qualifies(
                first, second, base, direction
            )
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        table = tuple(
            int(
                direction_audit.direction_qualifies(
                    first, second, base, direction
                )
            )
            for first in grid
            for second in grid
        )
        states.add((7 - endpoints, table))

    return (
        tuple(sorted(states)),
        {
            "critical_roots": len(roots),
            "open_cells": len(samples),
            "raw_oriented_cases": 2 * len(samples) + 2 * len(roots) + 2,
            "distinct_states": len(states),
            "strict_boundary_event_pairs": strict_boundary_events,
        },
        feasible_indices,
    )


def atom_state_slack_twice(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    bound: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Twice the symmetrized atom slack, evaluated by direct local counts.

    For an oriented base let h be the strict-tail count, g the common
    count, and i their intersection count among the three sampled residual
    vertices.  Exact sampling without replacement gives the necessary row

      13 M h + 13 r g - r M - 247 h g + 234 i >= 0.

    Both orientations of every unordered base are summed, clearing the
    factor 1/2 from uniform symmetrization.
    """

    edge = edge_map(edges)
    slack = 0
    for first, second in EDGE_POSITIONS:
        if edge[(first, second)] != base_index:
            continue
        remaining = [
            vertex
            for vertex in range(5)
            if vertex not in (first, second)
        ]
        gamma = {
            vertex: (
                edge[tuple(sorted((first, vertex)))] >= threshold_index
                and edge[tuple(sorted((second, vertex)))] >= threshold_index
            )
            for vertex in remaining
        }
        common_count = sum(gamma.values())
        for oriented_first, oriented_second in (
            (first, second),
            (second, first),
        ):
            depth_count = 0
            intersection_count = 0
            for vertex in remaining:
                first_color = edge[
                    tuple(sorted((oriented_first, vertex)))
                ]
                second_color = edge[
                    tuple(sorted((oriented_second, vertex)))
                ]
                in_depth = bool(table[7 * first_color + second_color])
                depth_count += int(in_depth)
                intersection_count += int(in_depth and gamma[vertex])
            slack += (
                13 * bound * depth_count
                + 13 * required * common_count
                - required * bound
                - 247 * depth_count * common_count
                + 234 * intersection_count
            )
    return slack


def verify(
    source_path: Path = SOURCE,
    extension_path: Path = EXTENSION,
) -> dict[str, object]:
    direction_path = Path(direction_audit.__file__).resolve()
    assert digest(source_path) == SOURCE_SHA256
    assert digest(extension_path) == EXTENSION_SHA256
    assert digest(direction_path) == DIRECTION_AUDIT_SHA256

    source = json.loads(source_path.read_text())
    extension = json.loads(extension_path.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert extension["schema"] == (
        "kissing5.centered_quarter_k5_product_extension.v1"
    )
    assert extension["source_certificate"] == source_path.name
    assert extension["source_sha256"] == SOURCE_SHA256
    assert extension["positive_atom_count"] == 64
    enumeration_path = (
        ROOT
        / "experiments"
        / "centered_atomic_bv_barrier"
        / "results"
        / extension["enumeration_file"]
    )
    assert digest(enumeration_path) == extension["enumeration_sha256"]

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
    scaled_grid = [int(4 * value) for value in grid]
    assert all(Q(value, 4) == node for value, node in zip(scaled_grid, grid))
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert all(value > 0 for value in alpha + nu)
    assert sum(alpha) == N - 1
    assert sum(nu) == (N - 1) * (N - 2)

    atoms = extension["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert len(atoms) == len(weights) == 64
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1
    active_columns = tuple(extension["active_column_indices"])
    assert len(active_columns) == len(set(active_columns)) == len(atoms)
    assert tuple(sorted(active_columns)) == active_columns

    parsed_atoms = []
    edge_marginal = [Q(0)] * len(grid)
    triangle_marginal = [Q(0)] * len(triples)
    canonical_atoms = set()
    orbit_sizes: Counter[int] = Counter()
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        assert len(edges) == 10
        assert all(0 <= color < len(grid) for color in edges)
        assert_local_gram_psd(edges, scaled_grid)
        faces = triangle_types(edges)
        assert all(face in triple_index for face in faces)
        feature = tuple(sorted(triple_index[face] for face in faces))
        assert feature == tuple(atom["triangle_orbit_indices"])
        canonical, orbit_size = canonical_orbit(edges)
        assert canonical not in canonical_atoms
        canonical_atoms.add(canonical)
        orbit_sizes[orbit_size] += 1
        for color in edges:
            edge_marginal[color] += weight
        for index in feature:
            triangle_marginal[index] += weight
        parsed_atoms.append((edges, weight))

    assert edge_marginal == [value / 4 for value in alpha]
    assert triangle_marginal == [value / 156 for value in nu]

    # Authenticate the claimed discovery provenance without trusting it for
    # feasibility: local PSD and all feature identities were already checked
    # independently above.
    selected_lines = {}
    with enumeration_path.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == (
            "# feasible_labeled_k5=12087822 "
            "distinct_triangle_count_vectors=105930"
        )
        wanted = set(active_columns)
        for column, line in enumerate(stream):
            if column in wanted:
                selected_lines[column] = line.rstrip("\n")
    assert set(selected_lines) == set(active_columns)
    for column, atom in zip(active_columns, atoms):
        fields = selected_lines[column].split(",")
        assert len(fields) == 11
        stored_key = int(fields[0])
        stored_edges = tuple(map(int, fields[1:]))
        atom_edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        assert stored_edges == atom_edges
        reconstructed_key = 0
        for index in atom["triangle_orbit_indices"]:
            reconstructed_key = (reconstructed_key << 6) | index
        assert stored_key == reconstructed_key

    # Independent derivation of the diagonal correction for arbitrary
    # directions.  A residual vertex is retained with probability 1/13 and
    # an ordered distinct residual pair with probability 1/247.
    singleton_probability = Q(3, N - 2)
    pair_probability = Q(3 * 2, (N - 2) * (N - 3))
    assert singleton_probability == Q(1, 13)
    assert pair_probability == Q(1, 247)
    assert 247 * singleton_probability - 1 == 18
    # Hence H*Gamma = 247 E[h*g] - 234 E[intersection].
    assert 18 * 13 == 234

    states_by_base = {}
    coverage_by_base = {}
    feasible_by_base = {}
    for base_index in range(1, len(grid)):
        states, coverage, feasible = direction_states(
            base_index, grid, triples
        )
        states_by_base[base_index] = states
        coverage_by_base[qstring(grid[base_index])] = coverage
        feasible_by_base[base_index] = feasible

    expected_state_counts = {
        "-3/4": 62,
        "-1/2": 80,
        "-1/4": 88,
        "0": 92,
        "1/4": 92,
        "1/2": 84,
    }
    assert {
        base: data["distinct_states"]
        for base, data in coverage_by_base.items()
    } == expected_state_counts

    families = capacity_families(grid)
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
    minimum_positive: Q | None = None
    rows_checked = 0
    for family_index, (
        base_index,
        threshold_index,
        bound,
    ) in enumerate(families):
        feasible = feasible_by_base[base_index]
        # Every incident pair actually used by an atom is among the events
        # whose exact critical roots generated the projective partition.
        for edges, _weight in parsed_atoms:
            edge = edge_map(edges)
            for first, second in EDGE_POSITIONS:
                if edge[(first, second)] != base_index:
                    continue
                for vertex in range(5):
                    if vertex in (first, second):
                        continue
                    pair = (
                        edge[tuple(sorted((first, vertex)))],
                        edge[tuple(sorted((second, vertex)))],
                    )
                    assert pair in feasible
                    assert (pair[1], pair[0]) in feasible

        states = states_by_base[base_index]
        family_minimum: Q | None = None
        family_zeros = 0
        for state_index, (required, table) in enumerate(states):
            assert required in (5, 6, 7)
            slack_twice = sum(
                weight
                * atom_state_slack_twice(
                    edges,
                    base_index,
                    threshold_index,
                    bound,
                    required,
                    table,
                )
                for edges, weight in parsed_atoms
            )
            assert slack_twice >= 0
            rows_checked += 1
            if family_minimum is None or slack_twice < family_minimum:
                family_minimum = slack_twice
            if slack_twice == 0:
                family_zeros += 1
                zero_keys.append([family_index, state_index, required])
            elif minimum_positive is None or slack_twice < minimum_positive:
                minimum_positive = slack_twice
        assert family_minimum is not None
        family_summary.append(
            {
                "base_inner_product": qstring(grid[base_index]),
                "high_threshold": qstring(grid[threshold_index]),
                "capacity": bound,
                "distinct_direction_states": len(states),
                "zero_rows": family_zeros,
                "minimum_twice_symmetrized_slack": qstring(
                    family_minimum
                ),
            }
        )

    assert rows_checked == 560
    assert len(zero_keys) == 89
    assert zero_keys == extension["zero_product_row_keys"]
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

    # Isolate the symmetric direction -(y+z), which was the original
    # negative-sum product row.  The two rows that refuted the old extension
    # are now saturated exactly.
    negative_sum_rows = []
    for base_index, threshold_index, bound in families:
        base = grid[base_index]
        endpoints = sum(
            direction_audit.direction_qualifies(
                first, second, base, (Q(-1), Q(-1))
            )
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        assert endpoints == 0
        table = tuple(
            int(
                direction_audit.direction_qualifies(
                    first, second, base, (Q(-1), Q(-1))
                )
            )
            for first in grid
            for second in grid
        )
        slack_twice = sum(
            weight
            * atom_state_slack_twice(
                edges,
                base_index,
                threshold_index,
                bound,
                7,
                table,
            )
            for edges, weight in parsed_atoms
        )
        assert slack_twice >= 0
        negative_sum_rows.append(
            {
                "base_inner_product": qstring(base),
                "high_threshold": qstring(grid[threshold_index]),
                "capacity": bound,
                "twice_symmetrized_slack": qstring(slack_twice),
            }
        )
    assert {
        (row["base_inner_product"], row["high_threshold"]): row[
            "twice_symmetrized_slack"
        ]
        for row in negative_sum_rows
        if row["base_inner_product"] in ("-1/2", "-1/4")
    } == {
        ("-1/2", "1/2"): "0",
        ("-1/4", "1/2"): "0",
    }

    return {
        "status": "PASS",
        "conclusion": (
            "the 64-atom symmetric local Gram-PSD K5 extension passes all "
            "560 distinct pair-conditioned depth/capacity product states"
        ),
        "source_sha256": SOURCE_SHA256,
        "extension_sha256": EXTENSION_SHA256,
        "direction_partition_sha256": DIRECTION_AUDIT_SHA256,
        "positive_atoms": len(atoms),
        "orbit_size_histogram": {
            str(size): count for size, count in sorted(orbit_sizes.items())
        },
        "edge_marginal": "exact alpha/4",
        "triangle_marginal": "exact nu/156",
        "continuum_coverage": coverage_by_base,
        "product_families": family_summary,
        "negative_sum_rows": negative_sum_rows,
        "distinct_product_rows_checked": rows_checked,
        "zero_product_rows": len(zero_keys),
        "minimum_positive_twice_symmetrized_slack": qstring(
            minimum_positive
        ),
        "scope": (
            "local symmetric five-subset distribution only; not a global "
            "41-point code and not a five-point Lasserre moment-PSD "
            "certificate"
        ),
    }


def main() -> None:
    report = verify()
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

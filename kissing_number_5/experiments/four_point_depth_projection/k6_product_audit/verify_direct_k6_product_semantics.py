#!/usr/bin/env python3
"""Exact product-row audit of the direct rank-five K6 extension."""

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
from experiments.four_point_depth_projection.k5_product_audit import (
    verify_product_extension_independent as state_audit,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CERTIFICATE = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "direct_k6_triangle_extension.json"
)

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CERTIFICATE_SHA256 = (
    "32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba"
)
DIRECTION_AUDIT_SHA256 = (
    "f351abd19eb17f2e4adcb14b8309bfd6cd212b7ac474fe57f283142927c9c756"
)
STATE_AUDIT_SHA256 = (
    "62e3b6e1384b1b0740c832af656f1a9b99767d3b2337b6e7561382c18ba7a9d4"
)

N = 41
PAIRS6 = tuple((i, j) for i in range(6) for j in range(i + 1, 6))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
PERMUTATIONS6 = tuple(itertools.permutations(range(6)))

EXPECTED_WORST_SLACK = -Q(
    34774569534004858111024638332474125643044200329,
    356018544845649389857262695513200000000000000,
)
EXPECTED_NEGATIVE_SUM_VIOLATION = Q(
    34774569534004858111024638332474125643044200329,
    712037089691298779714525391026400000000000000,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstring(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def determinant(matrix: list[list[int]]) -> int:
    """Exact Bareiss determinant."""

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
    return dict(zip(PAIRS6, edges))


def triangle_indices(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    edge = edge_map(edges)
    result = []
    for i in range(6):
        for j in range(i + 1, 6):
            for k in range(j + 1, 6):
                colors = tuple(
                    sorted((edge[(i, j)], edge[(i, k)], edge[(j, k)]))
                )
                result.append(triple_index[colors])
    return tuple(sorted(result))


def scaled_gram(edges: tuple[int, ...], values: tuple[int, ...]):
    matrix = [[4 if i == j else 0 for j in range(6)] for i in range(6)]
    for (i, j), color in zip(PAIRS6, edges):
        matrix[i][j] = values[color]
        matrix[j][i] = values[color]
    return matrix


def principal_determinants(matrix: list[list[int]]) -> dict[int, list[int]]:
    return {
        size: [
            determinant([[matrix[i][j] for j in indices] for i in indices])
            for indices in itertools.combinations(range(6), size)
        ]
        for size in range(1, 7)
    }


def canonical_orbit(edges: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    old = edge_map(edges)
    relabeled = set()
    for permutation in PERMUTATIONS6:
        new = {
            tuple(sorted((permutation[i], permutation[j]))): color
            for (i, j), color in old.items()
        }
        relabeled.add(tuple(new[pair] for pair in PAIRS6))
    return min(relabeled), len(relabeled)


def atom_state_slack_twice(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    bound: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Twice the S6-symmetrized K6 slack by direct local counting.

    Four of the 39 residual vertices are sampled.  For an oriented base,
    let h and g be the sampled depth and common counts and i their sampled
    intersection.  The exact necessary row is

      39 M h + 39 r g - 4 r M - 494 h g + 455 i >= 0.

    Summing both orientations of each unordered base clears the factor 1/2
    introduced by uniform symmetrization.
    """

    edge = edge_map(edges)
    slack = 0
    for first, second in PAIRS6:
        if edge[(first, second)] != base_index:
            continue
        remaining = [
            vertex
            for vertex in range(6)
            if vertex not in (first, second)
        ]
        assert len(remaining) == 4
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
                39 * bound * depth_count
                + 39 * required * common_count
                - 4 * required * bound
                - 494 * depth_count * common_count
                + 455 * intersection_count
            )
    return slack


def verify(
    source_path: Path = SOURCE,
    certificate_path: Path = CERTIFICATE,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(certificate_path) == CERTIFICATE_SHA256
    assert digest(Path(direction_audit.__file__).resolve()) == (
        DIRECTION_AUDIT_SHA256
    )
    assert digest(Path(state_audit.__file__).resolve()) == STATE_AUDIT_SHA256

    source = json.loads(source_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert certificate["schema"] == (
        "kissing5.centered_quarter_direct_k6_triangle_extension.v1"
    )
    assert certificate["source_sha256"] == SOURCE_SHA256
    assert certificate["grid"] == source["grid"]

    grid = tuple(Q(value) for value in source["grid"])
    scaled_grid = tuple(int(4 * value) for value in grid)
    assert all(Q(value, 4) == node for value, node in zip(scaled_grid, grid))
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert len(triples) == len(triple_index) == 51
    assert sum(alpha) == N - 1
    assert sum(nu) == (N - 1) * (N - 2)

    catalog_path = ROOT / certificate["discovery_catalog"]
    report_path = ROOT / certificate["discovery_numerical_report"]
    assert digest(catalog_path) == certificate["discovery_catalog_sha256"]
    assert digest(report_path) == certificate[
        "discovery_numerical_report_sha256"
    ]
    report = json.loads(report_path.read_text())
    assert report["success"]
    active_columns = tuple(report["active_columns"])

    atoms = certificate["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert len(atoms) == len(weights) == certificate[
        "positive_atom_count"
    ] == len(active_columns) == 51
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    parsed_atoms = []
    edge_marginal = [Q(0)] * len(grid)
    triangle_marginal = [Q(0)] * len(triples)
    minimum_principal = {size: None for size in range(1, 7)}
    minimum_positive_fifth = None
    canonical_atoms = set()
    orbit_sizes: Counter[int] = Counter()
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_"
                "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        assert len(edges) == 15
        assert all(0 <= color < len(grid) for color in edges)
        matrix = scaled_gram(edges, scaled_grid)
        minors = principal_determinants(matrix)
        assert all(
            value >= 0 for values in minors.values() for value in values
        )
        assert minors[6] == [0]
        positive_fifth = [value for value in minors[5] if value > 0]
        assert positive_fifth
        local_fifth = min(positive_fifth)
        minimum_positive_fifth = (
            local_fifth
            if minimum_positive_fifth is None
            else min(minimum_positive_fifth, local_fifth)
        )
        for size, values in minors.items():
            local = min(values)
            old = minimum_principal[size]
            minimum_principal[size] = (
                local if old is None else min(old, local)
            )

        feature = triangle_indices(edges, triple_index)
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

    assert edge_marginal == [3 * value / 8 for value in alpha]
    assert triangle_marginal == [value / 78 for value in nu]
    assert minimum_principal[6] == 0
    assert minimum_positive_fifth == 6

    # Check the selected rows against the authenticated discovery catalog.
    selected_lines = {}
    with catalog_path.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == certificate["discovery_catalog_header"]
        wanted = set(active_columns)
        for column, line in enumerate(stream):
            if column in wanted:
                selected_lines[column] = tuple(map(int, line.split(",")))
    assert set(selected_lines) == set(active_columns)
    for column, atom in zip(active_columns, atoms):
        fields = selected_lines[column]
        assert len(fields) == 35
        edges = tuple(
            atom[
                "edge_color_indices_"
                "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        assert fields[:15] == edges
        assert fields[15:] == tuple(atom["triangle_orbit_indices"])

    # Four-of-39 finite-population coefficients.
    singleton_probability = Q(4, 39)
    ordered_pair_probability = Q(4 * 3, 39 * 38)
    assert ordered_pair_probability == Q(2, 247)
    # E[h*g] = p2*H*Gamma + (p1-p2)*I and E[i] = p1*I.
    assert singleton_probability - ordered_pair_probability == Q(70, 741)
    assert Q(247, 2) * ordered_pair_probability == 1
    assert (
        Q(247, 2)
        * (singleton_probability - ordered_pair_probability)
        * Q(39, 4)
        == Q(455, 4)
    )
    # Multiplying the decoded pointwise inequality by four gives the
    # integer form used in atom_state_slack_twice.
    assert Q(39, 4) * 4 == 39
    assert Q(247, 2) * 4 == 494

    states_by_base = {}
    feasible_by_base = {}
    coverage = {}
    for base_index in range(1, len(grid)):
        states, data, feasible = state_audit.direction_states(
            base_index, grid, triples
        )
        states_by_base[base_index] = states
        feasible_by_base[base_index] = feasible
        coverage[qstring(grid[base_index])] = data

    families = state_audit.capacity_families(grid)
    assert families == (
        (1, 5, 6),
        (1, 6, 0),
        (2, 6, 1),
        (3, 6, 3),
        (4, 6, 6),
        (5, 6, 7),
        (6, 6, 7),
    )
    family_reports = []
    violations = []
    zero_rows = 0
    rows_checked = 0
    for family_index, (
        base_index,
        threshold_index,
        bound,
    ) in enumerate(families):
        feasible = feasible_by_base[base_index]
        for edges, _weight in parsed_atoms:
            edge = edge_map(edges)
            for first, second in PAIRS6:
                if edge[(first, second)] != base_index:
                    continue
                for vertex in range(6):
                    if vertex in (first, second):
                        continue
                    pair = (
                        edge[tuple(sorted((first, vertex)))],
                        edge[tuple(sorted((second, vertex)))],
                    )
                    assert pair in feasible
                    assert (pair[1], pair[0]) in feasible

        family_slacks = []
        family_violations = 0
        family_zeros = 0
        for state_index, (required, table) in enumerate(
            states_by_base[base_index]
        ):
            slack = sum(
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
            rows_checked += 1
            family_slacks.append(slack)
            if slack < 0:
                family_violations += 1
                violations.append(
                    {
                        "family_index": family_index,
                        "state_index": state_index,
                        "base_inner_product": qstring(grid[base_index]),
                        "high_threshold": qstring(grid[threshold_index]),
                        "capacity": bound,
                        "required_residual_depth": required,
                        "twice_symmetrized_slack": qstring(slack),
                    }
                )
            elif slack == 0:
                family_zeros += 1
                zero_rows += 1
        family_reports.append(
            {
                "base_inner_product": qstring(grid[base_index]),
                "high_threshold": qstring(grid[threshold_index]),
                "capacity": bound,
                "direction_states": len(family_slacks),
                "violations": family_violations,
                "zero_rows": family_zeros,
                "minimum_twice_symmetrized_slack": qstring(
                    min(family_slacks)
                ),
            }
        )

    assert rows_checked == 560
    assert len(violations) == 41
    assert zero_rows == 62
    assert all(
        item["base_inner_product"] == "-1/4"
        and item["high_threshold"] == "1/2"
        and item["capacity"] == 3
        for item in violations
    )
    worst = min(Q(item["twice_symmetrized_slack"]) for item in violations)
    assert worst == EXPECTED_WORST_SLACK

    # Directly isolate the original disjoint negative -(y+z) row.
    negative_sum_reports = []
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
        negative_sum_reports.append(
            {
                "base_inner_product": qstring(base),
                "high_threshold": qstring(grid[threshold_index]),
                "capacity": bound,
                "twice_symmetrized_slack": qstring(slack_twice),
            }
        )
    target_negative = next(
        item
        for item in negative_sum_reports
        if item["base_inner_product"] == "-1/4"
        and item["high_threshold"] == "1/2"
    )
    assert Q(target_negative["twice_symmetrized_slack"]) == (
        -2 * EXPECTED_NEGATIVE_SUM_VIOLATION
    )

    return {
        "status": "PASS",
        "audit_conclusion": (
            "the semantic verifier passes; the stored 51-atom rank-exact-"
            "five K6 extension violates 41 necessary product rows"
        ),
        "source_sha256": SOURCE_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "positive_atoms": len(atoms),
        "rank": "every atom exactly 5",
        "minimum_scaled_principal_determinants": minimum_principal,
        "minimum_positive_scaled_fifth_minor": minimum_positive_fifth,
        "orbit_size_histogram": {
            str(size): count for size, count in sorted(orbit_sizes.items())
        },
        "edge_marginal": "exact 3*alpha/8; uniform edge alpha/40",
        "triangle_marginal": "exact nu/78; uniform face nu/1560",
        "normalization": {
            "sampled_singleton_probability": "4/39",
            "sampled_ordered_distinct_pair_probability": "2/247",
            "general_atom_row": (
                "39*M*h+39*r*g-4*r*M-494*h*g+455*i >= 0"
            ),
            "equivalent_distinct_pair_row": (
                "494*c+39*i <= 39*M*h+39*r*g-4*r*M"
            ),
        },
        "continuum_coverage": coverage,
        "rows_checked": rows_checked,
        "violating_rows": len(violations),
        "zero_rows": zero_rows,
        "worst_twice_symmetrized_slack": qstring(worst),
        "negative_sum_left_minus_right_violation": qstring(
            EXPECTED_NEGATIVE_SUM_VIOLATION
        ),
        "family_reports": family_reports,
        "negative_sum_reports": negative_sum_reports,
        "scope": (
            "refutes only this stored symmetric local K6 distribution; "
            "does not refute another rank-five K6 distribution with the "
            "same triangle marginal, a global 41-point code, or a "
            "six-point Lasserre moment certificate"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

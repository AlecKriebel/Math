#!/usr/bin/env python3
"""Exact audit of the K5 marginal induced by the direct K6 certificate.

The source K6 measure is symmetrized by a uniform permutation of its six
vertices.  Deleting a uniformly chosen vertex therefore gives a symmetric
K5 measure.  This verifier constructs that marginal exactly and checks all
560 pair-conditioned depth/common-capacity product states.

The product form is implemented twice:

* on each of the six deleted K5 faces, using the 3-of-39 normalization;
* directly on the parent K6 atom, using the 4-of-39 normalization.

The two integer forms are required to agree atom by atom and row by row.
No floating-point values from the discovery LP are used.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path

from experiments.four_point_depth_projection.centered_quarter_pair_depth import (
    verify as direction_audit,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
K6_CERTIFICATE = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "direct_k6_triangle_extension.json"
)

SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
K6_CERTIFICATE_SHA256 = (
    "32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba"
)
DIRECTION_AUDIT_SHA256 = (
    "f351abd19eb17f2e4adcb14b8309bfd6cd212b7ac474fe57f283142927c9c756"
)
CATALOG_SHA256 = (
    "45634e27071b348b66c02b4bbbfe9f23db713d2f3798589cbbd1c3750b0dcb68"
)
NUMERICAL_REPORT_SHA256 = (
    "7dc402e7df82dd9141dc7bfed7c4c3e9ee526db5825fd646101b726160e2f779"
)

N = 41
K6_EDGE_KEY = (
    "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
)
PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
PAIRS5 = tuple(itertools.combinations(range(5), 2))
PAIR_INDEX5 = {pair: index for index, pair in enumerate(PAIRS5)}
PERMUTATIONS5 = tuple(itertools.permutations(range(5)))

EXPECTED_STRONGEST_SLACK = Q(
    -34774569534004858111024638332474125643044200329,
    2136111269073896339143576173079200000000000000,
)
EXPECTED_MINIMUM_POSITIVE_SLACK = Q(
    30005782001270397740286808179413918992046900141,
    40586114112404030443727947288504800000000000000,
)


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


def gram6(edges: tuple[int, ...], scaled_grid: tuple[int, ...]):
    matrix = [[4 if i == j else 0 for j in range(6)] for i in range(6)]
    for (first, second), color in zip(PAIRS6, edges):
        matrix[first][second] = scaled_grid[color]
        matrix[second][first] = scaled_grid[color]
    return matrix


def principal_determinants(matrix: list[list[int]]):
    result: dict[int, list[int]] = {}
    for size in range(1, len(matrix) + 1):
        result[size] = []
        for indices in itertools.combinations(range(len(matrix)), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            result[size].append(determinant(minor))
    return result


def triangle_indices6(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for first, second, third in itertools.combinations(range(6), 3):
        colors = tuple(
            sorted(
                (
                    edges[PAIR_INDEX6[(first, second)]],
                    edges[PAIR_INDEX6[(first, third)]],
                    edges[PAIR_INDEX6[(second, third)]],
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def triangle_indices5(
    edges: tuple[int, ...],
    triple_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    result = []
    for first, second, third in itertools.combinations(range(5), 3):
        colors = tuple(
            sorted(
                (
                    edges[PAIR_INDEX5[(first, second)]],
                    edges[PAIR_INDEX5[(first, third)]],
                    edges[PAIR_INDEX5[(second, third)]],
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def delete_vertex(edges: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    remaining = [vertex for vertex in range(6) if vertex != deleted]
    return tuple(
        edges[
            PAIR_INDEX6[
                tuple(sorted((remaining[first], remaining[second])))
            ]
        ]
        for first, second in PAIRS5
    )


def edge_map5(edges: tuple[int, ...]) -> dict[tuple[int, int], int]:
    return dict(zip(PAIRS5, edges))


def edge_map6(edges: tuple[int, ...]) -> dict[tuple[int, int], int]:
    return dict(zip(PAIRS6, edges))


def canonical_k5(edges: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    """Canonical representative and labeled orbit size under S5."""

    old = edge_map5(edges)
    relabeled = set()
    for permutation in PERMUTATIONS5:
        new = {
            tuple(sorted((permutation[first], permutation[second]))): color
            for (first, second), color in old.items()
        }
        relabeled.add(tuple(new[position] for position in PAIRS5))
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


def capacity_families(
    grid: tuple[Q, ...],
) -> tuple[tuple[int, int, int], ...]:
    result = []
    for base_index, base in enumerate(grid):
        if base == -1:
            continue
        for threshold in (Q(1, 4), Q(1, 2)):
            bound = capacity(base, threshold)
            if bound is not None:
                result.append((base_index, grid.index(threshold), bound))
    return tuple(result)


def feasible_incident_pairs(
    base_index: int,
    triples: tuple[tuple[int, int, int], ...],
) -> set[tuple[int, int]]:
    result = set()
    for triple in triples:
        for position in range(3):
            if triple[position] != base_index:
                continue
            others = [
                triple[other]
                for other in range(3)
                if other != position
            ]
            result.add((others[0], others[1]))
            result.add((others[1], others[0]))
    return result


def direction_states(
    base_index: int,
    grid: tuple[Q, ...],
    triples: tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    """Enumerate all strict half-plane states on the projective line."""

    base = grid[base_index]
    feasible = feasible_incident_pairs(base_index, triples)
    event_pairs = {
        (grid[first], grid[second]) for first, second in feasible
    }
    event_pairs.update(((Q(1), base), (base, Q(1))))
    roots = direction_audit.critical_roots(base, event_pairs)
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

    for sample in direction_audit.open_cell_samples(roots):
        for orientation in (1, -1):
            add_rational(sample, orientation)
    for root in roots:
        for orientation in (1, -1):
            add_root(root, orientation)

    # Projective infinities, lambda = 0 and mu = +/-1.
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
    return tuple(sorted(states))


def k5_product_coefficient(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    bound: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Twice-symmetrized 3-of-39 product slack on one labeled K5 face.

    For each oriented base, h and g are singleton counts, i is their
    intersection count, and c=h*g-i counts ordered distinct residual pairs.
    The returned right-minus-left form is

      13*M*h + 13*r*g - r*M - 247*c - 13*i.
    """

    base_edges, h_total, g_total, i_total, c_total = k5_product_totals(
        edges,
        base_index,
        threshold_index,
        table,
    )
    return (
        13 * bound * h_total
        + 13 * required * g_total
        - required * bound * base_edges
        - 247 * c_total
        - 13 * i_total
    )


def k5_product_totals(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    table: tuple[int, ...],
) -> tuple[int, int, int, int, int]:
    """Oriented totals (base edges, h, g, intersection, distinct pairs)."""

    edge = edge_map5(edges)
    base_edges = 0
    h_total = 0
    g_total = 0
    i_total = 0
    c_total = 0
    for first, second in PAIRS5:
        if edge[(first, second)] != base_index:
            continue
        residual = [
            vertex for vertex in range(5) if vertex not in (first, second)
        ]
        common = {
            vertex: (
                edge[tuple(sorted((first, vertex)))] >= threshold_index
                and edge[tuple(sorted((second, vertex)))] >= threshold_index
            )
            for vertex in residual
        }
        g_count = sum(common.values())
        for oriented_first, oriented_second in (
            (first, second),
            (second, first),
        ):
            base_edges += 1
            h_count = 0
            i_count = 0
            for vertex in residual:
                first_color = edge[
                    tuple(sorted((oriented_first, vertex)))
                ]
                second_color = edge[
                    tuple(sorted((oriented_second, vertex)))
                ]
                in_tail = bool(table[7 * first_color + second_color])
                h_count += int(in_tail)
                i_count += int(in_tail and common[vertex])
            c_count = h_count * g_count - i_count
            h_total += h_count
            g_total += g_count
            i_total += i_count
            c_total += c_count
    return base_edges, h_total, g_total, i_total, c_total


def k6_product_coefficient(
    edges: tuple[int, ...],
    base_index: int,
    threshold_index: int,
    bound: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Direct 4-of-39 product slack on one labeled K6 atom.

    Singleton retention is 4/39 and ordered-distinct-pair retention is
    (4)_2/(39)_2=2/247.  Clearing denominators gives, per oriented base,

      39*M*h + 39*r*g - 4*r*M - 494*c - 39*i.

    This equals the sum of the K5 coefficients over all six deleted faces.
    """

    edge = edge_map6(edges)
    answer = 0
    for first, second in PAIRS6:
        if edge[(first, second)] != base_index:
            continue
        residual = [
            vertex for vertex in range(6) if vertex not in (first, second)
        ]
        common = {
            vertex: (
                edge[tuple(sorted((first, vertex)))] >= threshold_index
                and edge[tuple(sorted((second, vertex)))] >= threshold_index
            )
            for vertex in residual
        }
        g_count = sum(common.values())
        for oriented_first, oriented_second in (
            (first, second),
            (second, first),
        ):
            h_count = 0
            i_count = 0
            for vertex in residual:
                first_color = edge[
                    tuple(sorted((oriented_first, vertex)))
                ]
                second_color = edge[
                    tuple(sorted((oriented_second, vertex)))
                ]
                in_tail = bool(table[7 * first_color + second_color])
                h_count += int(in_tail)
                i_count += int(in_tail and common[vertex])
            c_count = h_count * g_count - i_count
            answer += (
                39 * bound * h_count
                + 39 * required * g_count
                - 4 * required * bound
                - 494 * c_count
                - 39 * i_count
            )
    return answer


def parse_and_verify_k6(
    source: dict[str, object],
    certificate: dict[str, object],
) -> tuple[
    tuple[Q, ...],
    tuple[tuple[int, int, int], ...],
    list[tuple[tuple[int, ...], Q, tuple[tuple[int, ...], ...]]],
    dict[int, int],
]:
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
    scaled_grid = tuple(int(4 * value) for value in grid)
    assert all(Q(value, 4) == node for value, node in zip(scaled_grid, grid))
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}
    assert len(triples) == len(triple_index) == 51
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])

    atoms = certificate["atoms"]
    assert len(atoms) == certificate["positive_atom_count"] == 51
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    edge_counts = [Q(0)] * len(grid)
    triangle_counts = [Q(0)] * len(triples)
    minimum_principal: dict[int, int | None] = {
        size: None for size in range(1, 7)
    }
    parsed = []
    for atom, weight in zip(atoms, weights):
        edges = tuple(atom[K6_EDGE_KEY])
        assert len(edges) == 15
        assert all(0 <= color < len(grid) for color in edges)
        matrix = gram6(edges, scaled_grid)
        minors = principal_determinants(matrix)
        assert all(value >= 0 for values in minors.values() for value in values)
        assert minors[6] == [0]
        assert any(value > 0 for value in minors[5])
        for size, values in minors.items():
            local = min(values)
            old = minimum_principal[size]
            minimum_principal[size] = local if old is None else min(old, local)

        feature = triangle_indices6(edges, triple_index)
        assert feature == tuple(atom["triangle_orbit_indices"])
        for color in edges:
            edge_counts[color] += weight
        for index in feature:
            triangle_counts[index] += weight
        faces = tuple(delete_vertex(edges, deleted) for deleted in range(6))
        parsed.append((edges, weight, faces))

    assert edge_counts == [3 * value / 8 for value in alpha]
    assert triangle_counts == [value / 78 for value in nu]
    assert all(value is not None for value in minimum_principal.values())
    return (
        grid,
        triples,
        parsed,
        {size: int(value) for size, value in minimum_principal.items()},
    )


def verify_discovery_provenance(certificate: dict[str, object]) -> dict[str, object]:
    """Authenticate, but do not trust, the numerical discovery catalog."""

    catalog = ROOT / certificate["discovery_catalog"]
    numerical_report = ROOT / certificate["discovery_numerical_report"]
    assert digest(catalog) == certificate["discovery_catalog_sha256"]
    assert digest(catalog) == CATALOG_SHA256
    assert digest(numerical_report) == certificate[
        "discovery_numerical_report_sha256"
    ]
    assert digest(numerical_report) == NUMERICAL_REPORT_SHA256
    report = json.loads(numerical_report.read_text())
    assert report["status"] == "NUMERICAL EVIDENCE ONLY"
    assert report["catalog_header"] == certificate["discovery_catalog_header"]
    active = tuple(report["active_columns"])
    assert len(active) == len(set(active)) == 51
    selected = {}
    wanted = set(active)
    with catalog.open() as stream:
        header = next(stream).rstrip("\n")
        assert header == certificate["discovery_catalog_header"]
        for index, line in enumerate(stream):
            if index in wanted:
                fields = tuple(map(int, line.rstrip("\n").split(",")))
                assert len(fields) == 35
                selected[index] = (fields[:15], fields[15:])
    assert set(selected) == wanted
    for index, atom in zip(active, certificate["atoms"]):
        edges, feature = selected[index]
        assert edges == tuple(atom[K6_EDGE_KEY])
        assert feature == tuple(atom["triangle_orbit_indices"])
    return {
        "catalog_columns": report["catalog_columns"],
        "selected_columns": len(active),
        "floating_report_status": report["status"],
        "trusted_for_product_audit": False,
    }


def induced_k5_marginal(
    parsed_atoms: list[
        tuple[tuple[int, ...], Q, tuple[tuple[int, ...], ...]]
    ],
    triples: tuple[tuple[int, int, int], ...],
    source: dict[str, object],
) -> tuple[dict[tuple[int, ...], Q], dict[str, int]]:
    triple_index = {triple: index for index, triple in enumerate(triples)}
    edge_counts = [Q(0)] * 7
    triangle_counts = [Q(0)] * len(triples)
    marginal: dict[tuple[int, ...], Q] = defaultdict(Q)
    for _edges6, weight, faces in parsed_atoms:
        for face in faces:
            face_weight = weight / 6
            canonical, _orbit_size = canonical_k5(face)
            marginal[canonical] += face_weight
            for color in face:
                edge_counts[color] += face_weight
            for index in triangle_indices5(face, triple_index):
                triangle_counts[index] += face_weight
    assert len(parsed_atoms) * 6 == 306
    assert len(marginal) == 266
    assert all(weight > 0 for weight in marginal.values())
    assert sum(marginal.values()) == 1

    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])
    assert edge_counts == [value / 4 for value in alpha]
    assert triangle_counts == [value / 156 for value in nu]
    histogram = Counter(canonical_k5(edges)[1] for edges in marginal)
    assert histogram == {
        5: 1,
        10: 4,
        12: 1,
        20: 3,
        30: 32,
        60: 90,
        120: 135,
    }
    return marginal, {
        str(size): count for size, count in sorted(histogram.items())
    }


def verify(
    source_path: Path = SOURCE,
    k6_certificate_path: Path = K6_CERTIFICATE,
    authenticate_catalog: bool = True,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(k6_certificate_path) == K6_CERTIFICATE_SHA256
    assert digest(Path(direction_audit.__file__).resolve()) == (
        DIRECTION_AUDIT_SHA256
    )
    source = json.loads(source_path.read_text())
    certificate = json.loads(k6_certificate_path.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert certificate["schema"] == (
        "kissing5.centered_quarter_direct_k6_triangle_extension.v1"
    )
    assert certificate["source_sha256"] == SOURCE_SHA256
    assert certificate["grid"] == source["grid"]

    provenance = (
        verify_discovery_provenance(certificate)
        if authenticate_catalog
        else {
            "catalog_authentication_skipped": True,
            "trusted_for_product_audit": False,
        }
    )
    grid, triples, parsed_atoms, principal_minima = parse_and_verify_k6(
        source, certificate
    )
    marginal, orbit_histogram = induced_k5_marginal(
        parsed_atoms, triples, source
    )

    # Use one common integer denominator for the exact weighted audit.
    common_denominator = 1
    for _edges, weight, _faces in parsed_atoms:
        common_denominator = math.lcm(
            common_denominator, weight.denominator
        )
    integer_weights = [
        weight.numerator * (common_denominator // weight.denominator)
        for _edges, weight, _faces in parsed_atoms
    ]
    assert sum(integer_weights) == common_denominator

    states_by_base = {
        base_index: direction_states(base_index, grid, triples)
        for base_index in range(1, len(grid))
    }
    expected_state_counts = {
        1: 62,
        2: 80,
        3: 88,
        4: 92,
        5: 92,
        6: 84,
    }
    assert {
        base_index: len(states)
        for base_index, states in states_by_base.items()
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

    family_reports = []
    violations = []
    zero_rows = []
    positive_rows = []
    total_rows = 0
    normalization_equalities = 0
    for family_index, (
        base_index,
        threshold_index,
        bound,
    ) in enumerate(families):
        family_values = []
        for state_index, (required, table) in enumerate(
            states_by_base[base_index]
        ):
            numerator = 0
            for integer_weight, (
                edges6,
                _weight,
                faces,
            ) in zip(integer_weights, parsed_atoms):
                direct = k6_product_coefficient(
                    edges6,
                    base_index,
                    threshold_index,
                    bound,
                    required,
                    table,
                )
                by_deletion = sum(
                    k5_product_coefficient(
                        face,
                        base_index,
                        threshold_index,
                        bound,
                        required,
                        table,
                    )
                    for face in faces
                )
                assert direct == by_deletion
                normalization_equalities += 1
                numerator += integer_weight * direct

            # Each deleted K5 face has probability weight/6.
            slack = Q(numerator, 6 * common_denominator)
            key = [family_index, state_index, required]
            family_values.append(slack)
            total_rows += 1
            if slack < 0:
                violations.append(
                    {
                        "row_key": key,
                        "base_inner_product": qstring(grid[base_index]),
                        "high_threshold": qstring(grid[threshold_index]),
                        "capacity": bound,
                        "right_minus_left_slack": qstring(slack),
                        "left_minus_right_violation": qstring(-slack),
                    }
                )
            elif slack == 0:
                zero_rows.append(key)
            else:
                positive_rows.append((slack, key))

        family_reports.append(
            {
                "base_inner_product": qstring(grid[base_index]),
                "high_threshold": qstring(grid[threshold_index]),
                "capacity": bound,
                "direction_states": len(family_values),
                "violated_rows": sum(value < 0 for value in family_values),
                "zero_rows": sum(value == 0 for value in family_values),
                "minimum_right_minus_left_slack": qstring(
                    min(family_values)
                ),
            }
        )

    assert total_rows == 560
    assert normalization_equalities == 51 * 560
    assert len(violations) == 41
    assert len(zero_rows) == 62
    assert all(item["base_inner_product"] == "-1/4" for item in violations)
    assert all(item["high_threshold"] == "1/2" for item in violations)
    assert all(item["capacity"] == 3 for item in violations)
    assert all(key[0] == 1 for key in zero_rows)
    strongest_item = min(
        violations,
        key=lambda item: Q(item["right_minus_left_slack"]),
    )
    strongest_value = Q(strongest_item["right_minus_left_slack"])
    assert strongest_value == EXPECTED_STRONGEST_SLACK
    assert strongest_item["row_key"] == [3, 77, 7]
    assert min(positive_rows)[0] == EXPECTED_MINIMUM_POSITIVE_SLACK

    # Identify the strongest row without relying on its sorted state index.
    base_index, threshold_index, bound = families[3]
    base = grid[base_index]
    negative_sum_direction = (Q(-1), Q(-1))
    endpoints = sum(
        direction_audit.direction_qualifies(
            first, second, base, negative_sum_direction
        )
        for first, second in ((Q(1), base), (base, Q(1)))
    )
    assert endpoints == 0
    negative_sum_state = (
        7,
        tuple(
            int(
                direction_audit.direction_qualifies(
                    first,
                    second,
                    base,
                    negative_sum_direction,
                )
            )
            for first in grid
            for second in grid
        ),
    )
    negative_sum_state_index = states_by_base[base_index].index(
        negative_sum_state
    )
    assert negative_sum_state_index == 77
    negative_sum_totals = [Q(0)] * 5
    for _edges6, weight, faces in parsed_atoms:
        for face in faces:
            totals = k5_product_totals(
                face,
                base_index,
                threshold_index,
                negative_sum_state[1],
            )
            for index, value in enumerate(totals):
                negative_sum_totals[index] += weight * value / 6
    (
        expected_base_edges,
        expected_depth,
        expected_common,
        expected_intersection,
        expected_distinct_pairs,
    ) = negative_sum_totals
    assert expected_intersection == 0
    negative_sum_right = (
        13 * bound * expected_depth
        + 13 * 7 * expected_common
        - 7 * bound * expected_base_edges
    )
    negative_sum_left = (
        247 * expected_distinct_pairs + 13 * expected_intersection
    )
    assert negative_sum_right - negative_sum_left == strongest_value

    return {
        "status": "CERTIFIED_VIOLATIONS",
        "conclusion": (
            "the symmetric K5 marginal induced by the direct rank-five "
            "K6 certificate violates 41 of the 560 exact "
            "depth/common-capacity product rows"
        ),
        "source_sha256": SOURCE_SHA256,
        "k6_certificate_sha256": K6_CERTIFICATE_SHA256,
        "direction_partition_sha256": DIRECTION_AUDIT_SHA256,
        "discovery_provenance": provenance,
        "k6_positive_atoms": len(parsed_atoms),
        "k6_minimum_scaled_principal_determinants": principal_minima,
        "induced_raw_labeled_faces": 306,
        "induced_positive_unlabeled_k5_orbits": len(marginal),
        "induced_k5_orbit_size_histogram": orbit_histogram,
        "induced_k5_edge_marginal": "exact alpha/4",
        "induced_k5_triangle_marginal": "exact nu/156",
        "normalization": {
            "k5_singleton_retention": "1/13",
            "k5_ordered_distinct_pair_retention": "1/247",
            "k6_singleton_retention": "4/39",
            "k6_ordered_distinct_pair_retention": "2/247",
            "deleted_face_probability": "1/6",
            "atom_row_equalities_checked": normalization_equalities,
        },
        "families": family_reports,
        "distinct_product_rows_checked": total_rows,
        "violated_product_rows": len(violations),
        "zero_product_rows": len(zero_rows),
        "strongest_violation": strongest_item,
        "strongest_violation_direction": "-(y+z)",
        "strongest_violation_expected_oriented_totals": {
            "base_edges": qstring(expected_base_edges),
            "depth_incidences": qstring(expected_depth),
            "common_incidences": qstring(expected_common),
            "tail_common_intersections": qstring(expected_intersection),
            "ordered_distinct_tail_common_pairs": qstring(
                expected_distinct_pairs
            ),
            "left_side": qstring(negative_sum_left),
            "right_side": qstring(negative_sum_right),
        },
        "minimum_positive_right_minus_left_slack": qstring(
            min(positive_rows)[0]
        ),
        "violation_rows": violations,
        "scope": (
            "rejects this exact symmetrized K6 distribution only; does not "
            "exclude a different K6 extension or a global 41-point code"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

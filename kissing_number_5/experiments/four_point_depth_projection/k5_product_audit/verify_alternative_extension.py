#!/usr/bin/env python3
"""Exact verifier for the alternative K5 product-row extension.

The checker uses only the standard library.  It does not import or trust the
SciPy discovery search, its active columns, or the original K5 extension.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CERTIFICATE = Path(__file__).with_name(
    "centered_quarter_k5_product_extension.json"
)
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)

from experiments.four_point_depth_projection.centered_quarter_pair_depth.verify import (  # noqa: E402
    critical_roots,
    direction_qualifies,
    event_weights,
    open_cell_samples,
    rational_qualifies,
    root_qualifies,
)
from verifiers.verify_centered_quarter_k5_extension import (  # noqa: E402
    EDGE_POSITIONS,
    gram_psd,
    scaled_gram,
    triangle_types,
)


EDGE_INDEX = {edge: index for index, edge in enumerate(EDGE_POSITIONS)}


def edge_color(edges: tuple[int, ...], first: int, second: int) -> int:
    if first > second:
        first, second = second, first
    return edges[EDGE_INDEX[first, second]]


def capacity_rows(grid: list[Q]) -> tuple[tuple[int, Q, int], ...]:
    rows = []
    for base_index, base in enumerate(grid):
        for high in (Q(1, 4), Q(1, 2)):
            capacity = None
            if base == -1:
                capacity = 0
            elif base <= 0:
                parameter = 2 * high * high / (1 + base)
                if parameter > 1:
                    capacity = 0
                elif parameter > Q(3, 4):
                    capacity = 1
                elif parameter > Q(2, 3):
                    capacity = 2
                elif parameter > Q(5, 8):
                    capacity = 3
                elif parameter > Q(1, 2):
                    capacity = 4
                elif parameter == Q(1, 2):
                    capacity = 6
            elif high == Q(1, 2):
                capacity = 7
            if capacity is not None and base != -1:
                rows.append((base_index, high, capacity))
    return tuple(rows)


def direction_states(
    base_index: int,
    grid: list[Q],
    triples: list[tuple[int, int, int]],
    nu: list[Q],
) -> tuple[tuple[int, tuple[int, ...]], ...]:
    base = grid[base_index]
    assert base > -1
    occupied = event_weights(base_index, grid, triples, nu)
    event_pairs = set(occupied)
    event_pairs.update(((Q(1), base), (base, Q(1))))
    roots = critical_roots(base, event_pairs)
    states: set[tuple[int, tuple[int, ...]]] = set()

    for slope in open_cell_samples(roots):
        for orientation in (1, -1):
            endpoint_count = sum(
                rational_qualifies(
                    first, second, base, slope, orientation
                )
                for first, second in ((Q(1), base), (base, Q(1)))
            )
            table = tuple(
                int(
                    rational_qualifies(
                        first, second, base, slope, orientation
                    )
                )
                for first in grid
                for second in grid
            )
            states.add((7 - endpoint_count, table))

    for root in roots:
        for orientation in (1, -1):
            endpoint_count = sum(
                root_qualifies(
                    first, second, base, root, orientation
                )
                for first, second in ((Q(1), base), (base, Q(1)))
            )
            table = tuple(
                int(
                    root_qualifies(
                        first, second, base, root, orientation
                    )
                )
                for first in grid
                for second in grid
            )
            states.add((7 - endpoint_count, table))

    for direction in ((Q(0), Q(1)), (Q(0), Q(-1))):
        endpoint_count = sum(
            direction_qualifies(first, second, base, direction)
            for first, second in ((Q(1), base), (base, Q(1)))
        )
        table = tuple(
            int(direction_qualifies(first, second, base, direction))
            for first in grid
            for second in grid
        )
        states.add((7 - endpoint_count, table))
    return tuple(sorted(states))


def product_coefficient(
    edges: tuple[int, ...],
    base_index: int,
    high_index: int,
    capacity: int,
    required: int,
    table: tuple[int, ...],
) -> int:
    """Twice the symmetrized K5 form.

    With H2, I2, C2 denoting sums over both base orientations, and G,E
    denoting unoriented common-incidence and base-edge counts, the form is

      13 M H2 + 26 r G - 2 r M E - 247 C2 - 13 I2.

    This is the exact without-replacement scaling of
    (H-r)(M-Gamma)>=0, including the triple diagonal I=H intersect Gamma.
    """

    h_twice = 0
    common = 0
    intersection_twice = 0
    distinct_product_twice = 0
    base_edges = 0
    for edge_position, (first, second) in enumerate(EDGE_POSITIONS):
        if edges[edge_position] != base_index:
            continue
        base_edges += 1
        remaining = [
            vertex
            for vertex in range(5)
            if vertex not in (first, second)
        ]
        gamma = []
        for vertex in remaining:
            gamma.append(
                edge_color(edges, first, vertex) >= high_index
                and edge_color(edges, second, vertex) >= high_index
            )
        gamma_count = sum(gamma)
        common += gamma_count
        for oriented_first, oriented_second in (
            (first, second),
            (second, first),
        ):
            halfplane = [
                bool(
                    table[
                        7 * edge_color(edges, oriented_first, vertex)
                        + edge_color(edges, oriented_second, vertex)
                    ]
                )
                for vertex in remaining
            ]
            h_count = sum(halfplane)
            intersection = sum(
                in_halfplane and in_gamma
                for in_halfplane, in_gamma in zip(halfplane, gamma)
            )
            h_twice += h_count
            intersection_twice += intersection
            distinct_product_twice += (
                h_count * gamma_count - intersection
            )

    return (
        13 * capacity * h_twice
        + 26 * required * common
        - 2 * required * capacity * base_edges
        - 247 * distinct_product_twice
        - 13 * intersection_twice
    )


def verify() -> dict[str, object]:
    source_bytes = SOURCE.read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256
    source = json.loads(source_bytes)
    certificate = json.loads(CERTIFICATE.read_text())
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert certificate["schema"] == (
        "kissing5.centered_quarter_k5_product_extension.v1"
    )
    assert certificate["source_certificate"] == SOURCE.name
    assert certificate["source_sha256"] == SOURCE_SHA256

    grid = [Q(value) for value in source["grid"]]
    scaled_values = [int(4 * value) for value in grid]
    assert all(Q(value, 4) == node for value, node in zip(scaled_values, grid))
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    triple_index = {triple: index for index, triple in enumerate(triples)}
    nu = [Q(value) for value in source["nu"]]

    atoms = certificate["atoms"]
    assert len(atoms) == certificate["positive_atom_count"] == 64
    weights = [Q(atom["weight"]) for atom in atoms]
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    triangle_marginal = [Q(0)] * len(triples)
    edge_marginal = [Q(0)] * len(grid)
    parsed_edges = []
    principal_minima = {size: None for size in range(1, 6)}
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_01_02_03_04_12_13_14_23_24_34"
            ]
        )
        parsed_edges.append(edges)
        assert len(edges) == 10
        assert all(0 <= color < len(grid) for color in edges)
        faces = triangle_types(edges)
        assert all(face in triple_index for face in faces)
        stored_faces = tuple(sorted(triple_index[face] for face in faces))
        assert stored_faces == tuple(atom["triangle_orbit_indices"])
        matrix = scaled_gram(edges, scaled_values)
        is_psd, minima = gram_psd(matrix)
        assert is_psd
        for size, value in minima.items():
            old = principal_minima[size]
            principal_minima[size] = value if old is None else min(old, value)
        for face in stored_faces:
            triangle_marginal[face] += weight
        for color in edges:
            edge_marginal[color] += weight

    assert all(
        observed == target / 156
        for observed, target in zip(triangle_marginal, nu)
    )
    assert all(
        observed == target / 4
        for observed, target in zip(edge_marginal, alpha)
    )

    family_reports = []
    zero_keys = []
    total_states = 0
    global_minimum = None
    for family_index, (base_index, high, capacity) in enumerate(
        capacity_rows(grid)
    ):
        states = direction_states(base_index, grid, triples, nu)
        total_states += len(states)
        high_index = grid.index(high)
        minimum = None
        zero_count = 0
        for state_index, (required, table) in enumerate(states):
            slack = sum(
                weight
                * product_coefficient(
                    edges,
                    base_index,
                    high_index,
                    capacity,
                    required,
                    table,
                )
                for edges, weight in zip(parsed_edges, weights)
            )
            assert slack >= 0
            minimum = slack if minimum is None else min(minimum, slack)
            if slack == 0:
                zero_count += 1
                zero_keys.append([family_index, state_index, required])
        global_minimum = (
            minimum
            if global_minimum is None
            else min(global_minimum, minimum)
        )
        family_reports.append(
            {
                "base_inner_product": str(grid[base_index]),
                "high_threshold": str(high),
                "capacity": capacity,
                "direction_states": len(states),
                "minimum_scaled_slack": str(minimum),
                "zero_rows": zero_count,
            }
        )

    expected_summary = certificate["product_family_summary"]
    assert [
        {
            "base_inner_product": item["base_inner_product"],
            "high_threshold": item["high_threshold"],
            "capacity": item["capacity"],
            "distinct_direction_states": item["direction_states"],
        }
        for item in family_reports
    ] == expected_summary
    assert zero_keys == certificate["zero_product_row_keys"]
    assert total_states == 560
    assert global_minimum == 0

    return {
        "status": "PASS",
        "scope": (
            "symmetric local Gram-PSD K5 extension satisfying all 560 "
            "averaged product rows; not a global configuration and not a "
            "five-point Lasserre/moment certificate"
        ),
        "positive_atoms": len(atoms),
        "minimum_scaled_principal_determinants": principal_minima,
        "triangle_marginal": "exact nu/156",
        "edge_marginal": "exact alpha/4",
        "product_families": family_reports,
        "product_direction_states": total_states,
        "global_minimum_product_slack": global_minimum,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")

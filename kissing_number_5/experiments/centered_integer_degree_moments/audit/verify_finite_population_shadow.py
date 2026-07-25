#!/usr/bin/env python3
"""Exact verifier for the centered finite-population incidence shadows."""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WEIGHTS = (-4, -3, -2, -1, 0, 1, 2)


def incident_pair_multiplicity(
    triple: tuple[int, int, int],
    first_color: int,
    second_color: int,
) -> int:
    edge = {
        frozenset((0, 1)): triple[0],
        frozenset((0, 2)): triple[1],
        frozenset((1, 2)): triple[2],
    }
    return sum(
        edge[frozenset((base, first))] == first_color
        and edge[frozenset((base, second))] == second_color
        for base, first, second in itertools.permutations(range(3))
    )


def erdos_gallai(sequence: list[int]) -> bool:
    degrees = sorted(sequence, reverse=True)
    if sum(degrees) % 2:
        return False
    for size in range(1, len(degrees) + 1):
        if sum(degrees[:size]) > size * (size - 1) + sum(
            min(size, degree) for degree in degrees[size:]
        ):
            return False
    return True


def verify(certificate_path: Path, source_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    assert certificate["schema"] == (
        "kissing5.centered_finite_population_shadow.v1"
    )
    assert certificate["source_certificate"] == source_path.name
    assert certificate["source_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    mixture_path = (
        ROOT
        / "certificates"
        / certificate["row_support_certificate"]
    )
    mixture_bytes = mixture_path.read_bytes()
    mixture = json.loads(mixture_bytes)
    assert certificate["row_support_sha256"] == hashlib.sha256(
        mixture_bytes
    ).hexdigest()
    assert certificate["grid_numerators_over_four"] == list(WEIGHTS)
    triples = [tuple(row) for row in source["triple_orbits"]]
    assert len(triples) == len(set(triples)) == 51

    obstruction = certificate["named_repaired_witness_divisibility_obstruction"]
    pair_counts = [Q(41) * Q(value) for value in source["alpha"]]
    triangle_counts_named = [Q(41, 6) * Q(value) for value in source["nu"]]
    assert obstruction["directed_pair_counts_41_alpha"] == [
        str(value) for value in pair_counts
    ]
    assert obstruction["unordered_triangle_counts_41_nu_over_6"] == [
        str(value) for value in triangle_counts_named
    ]
    assert sum(value.denominator == 1 for value in pair_counts) == (
        obstruction["integral_directed_pair_count"]
    ) == 0
    assert sum(value.denominator == 1 for value in triangle_counts_named) == (
        obstruction["integral_unordered_triangle_count"]
    ) == 0

    shadow = certificate["finite_row_triangle_incidence_shadow"]
    rows = [tuple(row) for row in shadow["row_types"]]
    multiplicities = shadow["row_multiplicities"]
    triangle_counts = shadow["feasible_triangle_orbit_counts"]
    assert len(rows) == len(multiplicities)
    mixture_rows = {
        tuple(atom["degree_vector"]) for atom in mixture["atoms"]
    }
    assert set(rows).issubset(mixture_rows)
    assert all(isinstance(value, int) and value >= 0 for value in multiplicities)
    assert sum(multiplicities) == 41
    for row in rows:
        assert len(row) == 7
        assert all(isinstance(value, int) and value >= 0 for value in row)
        assert sum(row) == 40
        assert sum(weight * value for weight, value in zip(WEIGHTS, row)) == -4
        assert row[0] <= 1
    assert len(triangle_counts) == len(triples)
    assert all(isinstance(value, int) and value >= 0 for value in triangle_counts)
    assert sum(triangle_counts) == 41 * 40 * 39 // 6

    half_edge_counts = [
        sum(multiplicity * row[color] for multiplicity, row in zip(multiplicities, rows))
        for color in range(7)
    ]
    assert all(value % 2 == 0 for value in half_edge_counts)
    for i in range(7):
        for j in range(i, 7):
            row_side = sum(
                multiplicity
                * (row[i] * row[j] - (row[i] if i == j else 0))
                for multiplicity, row in zip(multiplicities, rows)
            )
            triangle_side = sum(
                count * incident_pair_multiplicity(triple, i, j)
                for count, triple in zip(triangle_counts, triples)
            )
            assert row_side == triangle_side
    for color in range(7):
        triangle_edge_incidence = sum(
            count * triple.count(color)
            for count, triple in zip(triangle_counts, triples)
        )
        assert triangle_edge_incidence == 39 * half_edge_counts[color] // 2

    graph = certificate["separate_colored_complete_graph_degree_shadow"]
    vertex_types = graph["vertex_row_type_indices"]
    assert len(vertex_types) == 41
    assert Counter(vertex_types) == Counter(
        {
            index: multiplicity
            for index, multiplicity in enumerate(multiplicities)
            if multiplicity
        }
    )
    edge_colors = graph["edge_colors"]
    expected_edges = {
        (i, j) for i in range(41) for j in range(i + 1, 41)
    }
    assert len(edge_colors) == len(expected_edges)
    edge_map: dict[tuple[int, int], int] = {}
    for first, second, color in edge_colors:
        assert 0 <= first < second < 41
        assert (first, second) not in edge_map
        assert isinstance(color, int) and 0 <= color < 7
        edge_map[(first, second)] = color
    assert set(edge_map) == expected_edges

    observed_rows = [[0] * 7 for _ in range(41)]
    for (first, second), color in edge_map.items():
        observed_rows[first][color] += 1
        observed_rows[second][color] += 1
    expected_rows = [rows[index] for index in vertex_types]
    assert [tuple(row) for row in observed_rows] == expected_rows
    assert all(
        erdos_gallai([row[color] for row in expected_rows])
        for color in range(7)
    )

    feasible = set(triples)
    infeasible = Counter()
    for first, second, third in itertools.combinations(range(41), 3):
        triple = tuple(
            sorted(
                (
                    edge_map[(first, second)],
                    edge_map[(first, third)],
                    edge_map[(second, third)],
                )
            )
        )
        if triple not in feasible:
            infeasible[triple] += 1
    stored_infeasible = {
        tuple(map(int, key.split(","))): value
        for key, value in graph[
            "expected_gram_infeasible_triangle_type_counts"
        ].items()
    }
    assert dict(infeasible) == stored_infeasible
    assert sum(infeasible.values()) == graph[
        "expected_gram_infeasible_triangle_count"
    ] == 649

    return {
        "status": "PASS",
        "named_repaired_witness": (
            "exactly obstructed by pair and triangle divisibility"
        ),
        "finite_incidence_shadow": {
            "vertices": sum(multiplicities),
            "edges_by_color": [value // 2 for value in half_edge_counts],
            "feasible_triangle_counts": sum(triangle_counts),
            "row_triangle_incidence_equalities": 28,
        },
        "graphical_degree_shadow": {
            "complete_graph_edges_colored": len(edge_map),
            "all_color_degree_sequences_graphical": True,
            "gram_infeasible_triangles": sum(infeasible.values()),
        },
        "scope": (
            "the incidence and graphical shadows are separate; their "
            "coupling with triangle feasibility is not certified"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).resolve().parent / "finite_population_shadow.json",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            ROOT
            / "experiments"
            / "centered_integer_degree_moments"
            / "repaired_pair_triple_local_3.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.source), indent=2))


if __name__ == "__main__":
    main()

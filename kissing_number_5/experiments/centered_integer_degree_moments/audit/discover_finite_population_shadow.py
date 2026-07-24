#!/usr/bin/env python3
"""Construct a finite-population incidence shadow and a colored degree graph.

The row/triangle counts were found by a small integer linear program.  They
are embedded below because the exact verifier checks them directly.  A
second MILP realizes the same row multiset as a coloring of every edge of
K_41; this graphical realization is deliberately recorded even though some
of its triangles are not Gram feasible.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


ROOT = Path(__file__).resolve().parents[3]
SOURCE = (
    ROOT
    / "experiments"
    / "centered_integer_degree_moments"
    / "repaired_pair_triple_local_3.json"
)
MIXTURE = ROOT / "certificates" / "centered_quarter_integer_degree_mixture.json"
OUTPUT = Path(__file__).resolve().parent / "finite_population_shadow.json"

ROW_TYPES = (
    (0, 4, 6, 4, 14, 0, 12),
    (0, 4, 7, 3, 13, 1, 12),
)
ROW_MULTIPLICITIES = (1, 40)
TRIANGLE_COUNTS = (
    0,
    0,
    0,
    0,
    246,
    574,
    160,
    410,
    0,
    496,
    0,
    0,
    0,
    0,
    1066,
    0,
    0,
    0,
    0,
    60,
    795,
    126,
    612,
    0,
    0,
    553,
    0,
    1432,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    194,
    120,
    0,
    0,
    0,
    744,
    103,
    200,
    1955,
    0,
    0,
    0,
    0,
    0,
    240,
    574,
)


def main() -> None:
    source_bytes = SOURCE.read_bytes()
    source = json.loads(source_bytes)
    mixture_bytes = MIXTURE.read_bytes()
    mixture = json.loads(mixture_bytes)
    mixture_rows = {
        tuple(atom["degree_vector"]) for atom in mixture["atoms"]
    }
    assert set(ROW_TYPES).issubset(mixture_rows)
    vertex_rows = [ROW_TYPES[0], *([ROW_TYPES[1]] * 40)]
    edges = [(i, j) for i in range(41) for j in range(i + 1, 41)]
    active_colors = tuple(range(1, 7))
    variable_count = len(edges) * len(active_colors)

    equation_count = len(edges) + 41 * len(active_colors)
    matrix = np.zeros((equation_count, variable_count))
    target: list[int] = []
    equation = 0
    for edge_index, _edge in enumerate(edges):
        matrix[
            equation,
            edge_index * len(active_colors) : (edge_index + 1)
            * len(active_colors),
        ] = 1
        target.append(1)
        equation += 1
    for vertex in range(41):
        for local_color, color in enumerate(active_colors):
            for edge_index, edge in enumerate(edges):
                if vertex in edge:
                    matrix[
                        equation,
                        edge_index * len(active_colors) + local_color,
                    ] = 1
            target.append(vertex_rows[vertex][color])
            equation += 1
    assert equation == equation_count

    target_array = np.asarray(target)
    result = milp(
        np.zeros(variable_count),
        integrality=np.ones(variable_count),
        bounds=Bounds(np.zeros(variable_count), np.ones(variable_count)),
        constraints=LinearConstraint(matrix, target_array, target_array),
        options={"time_limit": 180},
    )
    assert result.success, result.message
    rounded = np.rint(result.x).astype(int)
    assert np.max(abs(matrix @ rounded - target_array)) == 0
    coloring = [
        [u, v, active_colors[int(np.argmax(
            rounded[
                edge_index * len(active_colors) : (edge_index + 1)
                * len(active_colors)
            ]
        ))]]
        for edge_index, (u, v) in enumerate(edges)
    ]

    pair_counts = [str(Q(41) * Q(value)) for value in source["alpha"]]
    triangle_counts = [
        str(Q(41, 6) * Q(value)) for value in source["nu"]
    ]
    certificate = {
        "schema": "kissing5.centered_finite_population_shadow.v1",
        "status": (
            "exact row/feasible-triangle incidence shadow and a separate "
            "simultaneous colored-graph degree realization; the graph has "
            "Gram-infeasible triangles and is not a code"
        ),
        "source_certificate": SOURCE.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "row_support_certificate": MIXTURE.name,
        "row_support_sha256": hashlib.sha256(mixture_bytes).hexdigest(),
        "grid_numerators_over_four": [-4, -3, -2, -1, 0, 1, 2],
        "named_repaired_witness_divisibility_obstruction": {
            "directed_pair_counts_41_alpha": pair_counts,
            "unordered_triangle_counts_41_nu_over_6": triangle_counts,
            "integral_directed_pair_count": 0,
            "integral_unordered_triangle_count": 0,
        },
        "finite_row_triangle_incidence_shadow": {
            "row_types": [list(row) for row in ROW_TYPES],
            "row_multiplicities": list(ROW_MULTIPLICITIES),
            "feasible_triangle_orbit_counts": list(TRIANGLE_COUNTS),
        },
        "separate_colored_complete_graph_degree_shadow": {
            "vertex_row_type_indices": [0, *([1] * 40)],
            "edge_colors": coloring,
            "expected_gram_infeasible_triangle_count": 649,
            "expected_gram_infeasible_triangle_type_counts": {
                "1,1,1": 5,
                "1,1,2": 46,
                "1,1,3": 19,
                "1,1,4": 76,
                "1,2,2": 80,
                "1,2,3": 81,
                "1,5,6": 53,
                "1,6,6": 289,
            },
        },
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)
    print(hashlib.sha256(OUTPUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()

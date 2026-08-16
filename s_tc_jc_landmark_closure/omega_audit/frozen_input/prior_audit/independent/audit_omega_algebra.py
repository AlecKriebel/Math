#!/usr/bin/env python3
"""Independent exact algebraic replay of the Omega certificate.

The Fourier coordinates are rebuilt by direct displayed-tree enumeration from
``exact_fourier.py``.  No original project engine, symbolic parameterization,
or rank routine is imported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from exact_fourier import (
    JC_FOUR_LEAF_REPRESENTATIVES,
    determinant,
    dual_variables,
    evaluate,
    reticulations,
    zero_sum_assignments,
)


RANK_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 9)
N16_COLUMNS = (0, 1, 2, 3, 4, 7, 8, 9, 10)
N26_COLUMNS = (0, 1, 2, 3, 5, 7, 8, 9, 10)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction(value: str) -> Fraction:
    return Fraction(value)


def unpack(certificate):
    networks = {}
    for model_name, model in certificate["root_models"].items():
        encoding = certificate["network_encodings"][str(model["census_index"])]
        networks[model_name] = {
            "index": model["census_index"],
            "arcs": tuple(tuple(arc) for arc in encoding["arcs_in_parameter_order"]),
            "labels": dict(zip(encoding["leaves_in_port_order"], model["port_labels"])),
        }
    return networks


def inheritance_map(arcs, values):
    return dict(zip(reticulations(arcs), values))


def exact_point_replay(certificate, networks):
    points = certificate["exact_common_points"]
    common = None
    records = {}
    for name, network in networks.items():
        values = tuple(fraction(value) for value in points[name])
        edges, inheritances = values[:-2], values[-2:]
        assert all(0 < value < 1 for value in values)
        coordinates = evaluate(
            network["arcs"], network["labels"], zero_sum_assignments(4),
            edges, inheritance_map(network["arcs"], inheritances), "JC",
        )
        if common is None:
            common = coordinates
        else:
            assert coordinates == common

        duals = dual_variables(values)
        dual_coordinates = evaluate(
            network["arcs"], network["labels"], JC_FOUR_LEAF_REPRESENTATIVES,
            duals[:-2], inheritance_map(network["arcs"], duals[-2:]), "JC",
        )
        columns = N16_COLUMNS if network["index"] == 16 else N26_COLUMNS
        matrix = [
            [dual_coordinates[row + 1].gradient[column] for column in columns]
            for row in RANK_ROWS
        ]
        minor = determinant(matrix)
        expected = fraction(certificate["dimension_and_rank"]["rank_nine_minors"][name])
        assert minor == expected and minor != 0
        records[name] = {
            "all_parameters_strictly_in_Theta0": True,
            "zero_sum_coordinates": len(coordinates),
            "rank_nine_minor": str(minor),
        }
    return records, common


def symbolic_correspondence(networks):
    source = networks["N16_source"]
    target = networks["N16_target"]
    A, B, C, D, E, F, P, Q, R = sp.symbols("A B C D E F P Q R")
    half = sp.Rational(1, 2)
    G = E + 2 * F
    H = A * F + 2 * E
    source_edges = (A, B, C, D, E, half, half, F, P, Q, R, half)
    target_edges = (
        2 * F * (4 - A) / G,
        D / (4 - A),
        C,
        2 * B * H / G,
        4 * E * R * (4 - A) / H,
        half,
        half,
        2 * A * R * G / H,
        Q,
        P,
        G / 8,
        half,
    )
    assignments = zero_sum_assignments(4)
    source_coordinates = evaluate(
        source["arcs"], source["labels"], assignments, source_edges,
        inheritance_map(source["arcs"], (half, half)), "JC",
    )
    target_coordinates = evaluate(
        target["arcs"], target["labels"], assignments, target_edges,
        inheritance_map(target["arcs"], (half, half)), "JC",
    )
    differences = [sp.cancel(left - right) for left, right in zip(source_coordinates, target_coordinates)]
    assert all(difference == 0 for difference in differences)
    return {
        "zero_sum_identities": len(differences),
        "free_source_dimension": 9,
        "denominators": ["E+2*F", "A*F+2*E", "4-A"],
        "identically_zero_differences": len(differences),
    }


def symbolic_rank(networks):
    network = networks["N16_source"]
    parameters = sp.symbols("x0:14")
    core_coordinates = tuple(sp.factor(coordinate) for coordinate in evaluate(
        network["arcs"], network["labels"], JC_FOUR_LEAF_REPRESENTATIVES,
        parameters[:8] + (1, 1, 1, 1),
        inheritance_map(network["arcs"], parameters[12:]), "JC",
    ))
    core_parameters = parameters[:8] + parameters[12:]
    core_jacobian = sp.Matrix(core_coordinates[1:]).jacobian(core_parameters)
    core_rank = DomainMatrix.from_Matrix(core_jacobian).rank()
    assert core_rank == 6

    # Four pendant torus parameters add at most four tangent directions.  The
    # fourth is already in the core tangent space by this exact Euler identity,
    # independently checked coordinate by coordinate.  Thus rank <= 6+4-1=9.
    euler_differences = []
    for assignment, coordinate in zip(JC_FOUR_LEAF_REPRESENTATIVES[1:], core_coordinates[1:]):
        difference = sp.factor(
            parameters[4] * sp.diff(coordinate, parameters[4])
            + parameters[7] * sp.diff(coordinate, parameters[7])
            - int(assignment[3] != 0) * coordinate
        )
        euler_differences.append(difference)
    assert all(difference == 0 for difference in euler_differences)
    return {
        "method": "exact core row reduction plus pendant-torus Euler upper bound and independent nonzero minor",
        "core_jacobian_shape": list(core_jacobian.shape),
        "core_generic_rank": core_rank,
        "pendant_torus_directions": 4,
        "euler_dependency_identities": len(euler_differences),
        "complete_rank_upper_bound": 9,
        "complete_rank_lower_bound_from_exact_minors": 9,
        "complete_generic_rank": 9,
    }


def audit(path: Path):
    certificate = json.loads(path.read_text())
    networks = unpack(certificate)
    points, common = exact_point_replay(certificate, networks)
    return {
        "status": "EXACTLY COMPUTED",
        "implementation": "independent direct displayed-tree enumeration",
        "input": {"path": str(path), "sha256": file_hash(path)},
        "symbolic_parameter_correspondence": symbolic_correspondence(networks),
        "exact_common_point": {
            "networks": points,
            "complete_coordinate_equality": True,
            "common_coordinate_count": len(common),
        },
        "generic_rank": symbolic_rank(networks),
        "interpretation": (
            "The JC Omega algebraic collision is correct on its stated rooted/weak-tree-child "
            "graphs.  The separate graph audit shows those semi-directed graphs are not "
            "strongly tree-child under the standard every-rooting convention."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.certificate.resolve())
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()

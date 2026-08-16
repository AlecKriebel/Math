#!/usr/bin/env python3
"""Exact, human-readable Omega core-rank certificate.

This verifier rebuilds the source tensor from the frozen graph by direct
displayed-tree enumeration.  It records the rational-function core rank, an
explicit strict-point minor, and the Euler identities used in the rank-nine
upper bound.  It imports no discovery implementation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INDEPENDENT = ROOT / "omega_audit/frozen_input/prior_audit/independent"
CERTIFICATE = ROOT / "omega_audit/frozen_input/historical/jc_omega_move.json"
DEFAULT_OUTPUT = HERE / "output/omega_rank_readability.json"


def load_exact_fourier():
    path = INDEPENDENT / "exact_fourier.py"
    spec = importlib.util.spec_from_file_location("omega_rank_exact_fourier", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rational(value: str) -> sp.Rational:
    item = Fraction(value)
    return sp.Rational(item.numerator, item.denominator)


def build_record() -> dict:
    fourier = load_exact_fourier()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    model = certificate["root_models"]["N16_source"]
    encoding = certificate["network_encodings"][str(model["census_index"])]
    arcs = tuple(tuple(arc) for arc in encoding["arcs_in_parameter_order"])
    labels = dict(zip(encoding["leaves_in_port_order"], model["port_labels"]))

    parameters = sp.symbols("x0:14")
    inheritances = dict(zip(fourier.reticulations(arcs), parameters[12:]))
    core_coordinates = tuple(
        sp.factor(coordinate)
        for coordinate in fourier.evaluate(
            arcs,
            labels,
            fourier.JC_FOUR_LEAF_REPRESENTATIVES,
            parameters[:8] + (1, 1, 1, 1),
            inheritances,
            "JC",
        )
    )
    core_parameters = parameters[:8] + parameters[12:]
    jacobian = sp.Matrix(core_coordinates[1:]).jacobian(core_parameters)
    generic_rank = DomainMatrix.from_Matrix(jacobian).rank()
    if generic_rank != 6:
        raise AssertionError(f"core rank changed: {generic_rank}")

    point = tuple(
        rational(value)
        for value in certificate["exact_common_points"]["N16_source"]
    )
    point_jacobian = jacobian.subs(dict(zip(parameters, point)))
    rows = tuple(range(6))
    columns = (0, 1, 2, 3, 4, 7)
    minor = sp.factor(point_jacobian.extract(rows, columns).det())
    expected_minor = -sp.Rational(723, 8589934592)
    if minor != expected_minor:
        raise AssertionError(f"core minor changed: {minor}")

    euler_remainders = []
    for assignment, coordinate in zip(
        fourier.JC_FOUR_LEAF_REPRESENTATIVES[1:], core_coordinates[1:]
    ):
        euler_remainders.append(
            sp.factor(
                parameters[4] * sp.diff(coordinate, parameters[4])
                + parameters[7] * sp.diff(coordinate, parameters[7])
                - int(assignment[3] != 0) * coordinate
            )
        )
    if any(remainder != 0 for remainder in euler_remainders):
        raise AssertionError("Euler dependency changed")

    return {
        "status": "EXACTLY COMPUTED",
        "implementation": "independent direct displayed-tree enumeration",
        "core_jacobian_shape": list(jacobian.shape),
        "core_parameter_order": [str(value) for value in core_parameters],
        "generic_core_rank": generic_rank,
        "strict_point_minor": {
            "orbit_rows_zero_based": list(rows),
            "orbit_assignments": [
                list(fourier.JC_FOUR_LEAF_REPRESENTATIVES[index + 1])
                for index in rows
            ],
            "parameter_columns_zero_based": list(columns),
            "parameters": [str(core_parameters[index]) for index in columns],
            "determinant": str(minor),
        },
        "euler_identity": (
            "x4*d(c_g)/dx4+x7*d(c_g)/dx7=1[g4!=0]*c_g"
        ),
        "euler_identities_checked": len(euler_remainders),
        "complete_rank_upper_bound": 9,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    record = build_record()
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cross-check the 74-atom K6 replacement through its deleted K5 faces.

This verifier deliberately uses the K5-deletion and direct-K6 forms from
``verify_induced_k5_product`` rather than the replacement certificate's
primary direct-K6 verifier.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path

from experiments.four_point_depth_projection.k6_product_audit.verify_induced_k5_product import (
    SOURCE,
    SOURCE_SHA256,
    capacity_families,
    delete_vertex,
    direction_states,
    k5_product_coefficient,
    k6_product_coefficient,
)


CERTIFICATE = Path(__file__).with_name("productpool_extension.json")
CERTIFICATE_SHA256 = (
    "def805e0c73fb5a5306f230ad21866a5b0fcab1a3708f6f7daaa3b175dc54991"
)
ATOM_KEY = (
    "edge_color_indices_"
    "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
)
EXPECTED_MINIMUM_POSITIVE_INDUCED_SLACK = Q(
    4741606889923, 75000000000000
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstring(value: Q) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def verify(
    source_path: Path = SOURCE,
    certificate_path: Path = CERTIFICATE,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(certificate_path) == CERTIFICATE_SHA256
    source = json.loads(source_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    assert certificate["schema"] == "kissing5.rank5_k6_product_extension.v1"
    assert certificate["source_sha256"] == SOURCE_SHA256

    grid = tuple(Q(value) for value in source["grid"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    atoms = certificate["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    edges = tuple(tuple(atom[ATOM_KEY]) for atom in atoms)
    assert len(atoms) == len(weights) == len(edges) == 74
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1
    assert all(
        len(atom_edges) == 15
        and all(0 <= color < len(grid) for color in atom_edges)
        for atom_edges in edges
    )

    common_denominator = 1
    for weight in weights:
        common_denominator = math.lcm(
            common_denominator, weight.denominator
        )
    integer_weights = tuple(
        weight.numerator * (common_denominator // weight.denominator)
        for weight in weights
    )
    assert sum(integer_weights) == common_denominator

    states_by_base = {
        base_index: direction_states(base_index, grid, triples)
        for base_index in range(1, len(grid))
    }
    slacks = []
    zero_keys = []
    identity_checks = 0
    for family_index, (
        base_index,
        threshold_index,
        bound,
    ) in enumerate(capacity_families(grid)):
        for state_index, (required, table) in enumerate(
            states_by_base[base_index]
        ):
            numerator = 0
            for integer_weight, atom_edges in zip(integer_weights, edges):
                direct = k6_product_coefficient(
                    atom_edges,
                    base_index,
                    threshold_index,
                    bound,
                    required,
                    table,
                )
                deleted = sum(
                    k5_product_coefficient(
                        delete_vertex(atom_edges, vertex),
                        base_index,
                        threshold_index,
                        bound,
                        required,
                        table,
                    )
                    for vertex in range(6)
                )
                assert direct == deleted
                identity_checks += 1
                numerator += integer_weight * direct
            induced_slack = Q(numerator, 6 * common_denominator)
            assert induced_slack >= 0
            key = [family_index, state_index, required]
            slacks.append((induced_slack, key))
            if induced_slack == 0:
                zero_keys.append(key)

    assert len(slacks) == 560
    assert identity_checks == 74 * 560
    assert len(zero_keys) == 113
    assert zero_keys == certificate["zero_product_row_keys"]
    positive = [item for item in slacks if item[0] > 0]
    assert positive
    assert min(positive)[0] == EXPECTED_MINIMUM_POSITIVE_INDUCED_SLACK
    assert next(value for value, key in slacks if key == [3, 77, 7]) == 0

    return {
        "status": "PASS",
        "conclusion": (
            "the K5 marginal induced by the 74-atom replacement passes "
            "all 560 product rows"
        ),
        "certificate_sha256": CERTIFICATE_SHA256,
        "positive_k6_atoms": len(atoms),
        "deleted_k5_faces_with_multiplicity": 6 * len(atoms),
        "product_rows_checked": len(slacks),
        "atomwise_k6_equals_deleted_k5_checks": identity_checks,
        "negative_rows": 0,
        "zero_rows": len(zero_keys),
        "minimum_positive_induced_k5_slack": qstring(
            min(positive)[0]
        ),
        "formerly_violated_negative_sum_slack": "0",
        "scope": (
            "cross-check of product semantics only; geometry and pool "
            "provenance are checked by the two primary replacement verifiers"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))

#!/usr/bin/env python3
"""Mutation-sensitivity checks for the clean-room root/cut audit."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from fractions import Fraction
from pathlib import Path

from audit_gate1_algebra import (
    invariant_orbit,
    invariant_pullback,
    parse_template_data,
    quartet_tensor,
    record_network,
)
from audit_gate3 import (
    THREE_ASSIGNMENTS,
    endpoint_value,
    polynomial_up_to_sign,
    tensor_coordinates,
    two_by_two_minors,
    verify_expression_factor_certificate,
    verify_inheritance_bernstein_certificate,
)
from exact_poly import Polynomial
from graph_conventions import (
    MixedEdge,
    ordinary_triangle_quotient,
    ordinary_triangle_status,
    suppress_root_once,
    validate_literal_standard,
)
from tensor_models import (
    TREE_TENSOR,
    enumerate_nonroot_tensors,
    enumerate_root_tensors,
    load_cores,
)


DEFAULT_PROJECT = Path(
    "/Users/alec/Documents/Math/strong_level2_phylo_identifiability"
)


def rejected(action) -> str:
    try:
        action()
    except Exception:
        return "REJECTED"
    raise AssertionError("mutation was accepted")


def wrong_central_port_blocks():
    names = ("a", "b", "c", "t", "A", "B", "C", "T", "z")
    variables = [Polynomial.variable(len(names), index) for index in range(len(names))]
    a, b, c, t, A, B, C, T, z = variables
    blocks = {}
    for character_sum in range(4):
        pairs = tuple(
            pair
            for pair in itertools.product(range(4), repeat=2)
            if pair[0] ^ pair[1] == character_sum
        )
        matrix = []
        for g1, g3 in pairs:
            line = []
            for g2, g4 in pairs:
                connector = g1 ^ g2
                left = endpoint_value((g1, g2, connector), a, b, c, t)
                # Deliberate mutation: put Q's connector at port 1 rather than
                # at its designated third port.
                right = endpoint_value((connector, g3, g4), A, B, C, T)
                line.append(left * right * (z if connector else 1))
            matrix.append(line)
        blocks[character_sum] = matrix
    return blocks, variables


def audit(project: Path) -> dict[str, object]:
    rows = {}

    # Gate 1: a real serialized failure must remain rejected by the literal
    # standard convention.
    failure_path = Path(__file__).with_name("failures") / "gate1_nonstandard_root_suppression_failures.json"
    failure = json.loads(failure_path.read_text())["failures"][0]
    network = failure["network"]
    labels = {
        str(leaf): int(label)
        for leaf, label in network["selected_leaf_labels"].items()
    }
    literal, _reticulations = suppress_root_once(
        str(network["root"]),
        tuple((str(tail), str(head)) for tail, head in network["arcs"]),
    )
    check = validate_literal_standard(literal, labels)
    if check["valid_standard_strong"] or "parallel_mixed_edge" not in check["failures"]:
        raise AssertionError("known literal-standard failure was lost")
    rows["gate1_parallel_root_collision"] = "REJECTED"

    # Gate 1: blindly erasing triangle arrows is not an implementation of T.
    triangle = [
        MixedEdge.make("u", "v"),
        MixedEdge.make("u", "r", ("r",)),
        MixedEdge.make("v", "r", ("r",)),
        MixedEdge.make("u", "a"),
        MixedEdge.make("v", "b"),
        MixedEdge.make("r", "c"),
    ]
    labels_triangle = {"a": 1, "b": 2, "c": 3}
    if not ordinary_triangle_status(triangle, labels_triangle)["ordinary"]:
        raise AssertionError("ordinary triangle fixture is malformed")
    mutated_triangle = [
        edge
        if edge.endpoints != frozenset(("u", "a"))
        else MixedEdge.make("u", "a", ("a",))
        for edge in triangle
    ]
    rows["nonordinary_triangle_T_quotient"] = rejected(
        lambda: ordinary_triangle_quotient(mutated_triangle, labels_triangle)
    )

    # Gate 1: mutate the term count bound to ensure the reconstructed exact
    # pullback, rather than the PASS string, is load-bearing.
    frozen_path = project / "AUDIT/INDEPENDENT_IMPLEMENTATION/gate1_root_full_completion_audit.json"
    templates_path = project / "src/jc_root_spanning_atlas_data.py"
    frozen = json.loads(frozen_path.read_text())
    invariants = invariant_orbit(parse_template_data(templates_path))
    level = frozen["levels"]["6"]
    pair = level["strict_directed_filters"]["source_subset_target_rows"][0]
    certificate = pair["source_zero_target_nonzero_certificate"]
    quartet_index, invariant_index = divmod(int(certificate["bit_index"]), 60)
    quartet = tuple(itertools.combinations(range(1, 7), 4))[quartet_index]
    targets = {
        record["signature_sha256"]: record
        for record in level["target"]["signature_class_representatives"]
    }
    arcs, target_labels = record_network(targets[pair["target_signature_sha256"]])
    polynomial = invariant_pullback(
        quartet_tensor(arcs, target_labels, quartet), invariants[invariant_index]
    )
    mutated_term_count = int(certificate["target_polynomial_terms"]) + 1
    rows["gate1_separator_term_count"] = rejected(
        lambda: (
            None
            if len(polynomial.terms) == mutated_term_count
            else (_ for _ in ()).throw(AssertionError("term mismatch"))
        )
    )
    expected_pair_counts = {"6": 44, "7": 192, "8": 120}
    removed_counts = {
        port: len(
            frozen["levels"][port]["strict_directed_filters"]["source_subset_target_rows"]
        )
        - int(port == "7")
        for port in expected_pair_counts
    }
    rows["gate1_omitted_separator_row"] = rejected(
        lambda: (
            None
            if removed_counts == expected_pair_counts
            else (_ for _ in ()).throw(AssertionError("pair coverage mismatch"))
        )
    )

    # Gate 3 endpoint certificates: alter a constant and one hard inheritance
    # coefficient expression.
    submitted = json.loads((project / "WORK/gate3_two_blob_three_port_signs.json").read_text())
    algebra = json.loads((project / "AUDIT/INDEPENDENT_IMPLEMENTATION/gate3_crossing_certificate_audit.json").read_text())
    algebra_by_id = {int(record["tensor_id"]): record for record in algebra["records"]}
    regular = next(
        record
        for record in submitted["records"]
        if algebra_by_id[int(record["tensor_id"])]["F_method"]
        == "factor_then_full_bernstein"
    )
    tensor_id = int(regular["tensor_id"])
    signatures = tuple(tuple(int(value) for value in row) for row in regular["signatures"])
    reticulations = int(regular["reticulation_count"])
    names = tuple(
        [f"x{index}" for index in range(len(signatures))]
        + [f"l{index}" for index in range(reticulations)]
    )
    coordinates = tensor_coordinates(signatures, reticulations, names)
    F = coordinates["a"] * coordinates["b"] * coordinates["c"] - coordinates["t"] ** 2
    bad_factor = copy.deepcopy(algebra_by_id[tensor_id]["F_certificate"])
    bad_factor["constant"] = str(Fraction(str(bad_factor["constant"])) + 1)
    rows["gate3_factor_product_mutation"] = rejected(
        lambda: verify_expression_factor_certificate(F, bad_factor, names)
    )

    hard = next(
        record
        for record in submitted["records"]
        if algebra_by_id[int(record["tensor_id"])]["F_method"]
        == "inheritance_bernstein"
    )
    hard_id = int(hard["tensor_id"])
    hard_signatures = tuple(
        tuple(int(value) for value in row) for row in hard["signatures"]
    )
    hard_reticulations = int(hard["reticulation_count"])
    hard_names = tuple(
        [f"x{index}" for index in range(len(hard_signatures))]
        + [f"l{index}" for index in range(hard_reticulations)]
    )
    hard_coordinates = tensor_coordinates(
        hard_signatures, hard_reticulations, hard_names
    )
    hard_F = (
        hard_coordinates["a"]
        * hard_coordinates["b"]
        * hard_coordinates["c"]
        - hard_coordinates["t"] ** 2
    )
    hard_certificate = copy.deepcopy(
        hard["F_inheritance_Bernstein_certificate"]
    )
    first_nonzero = next(row for row in hard_certificate["coefficients"] if not row["zero"])
    first_nonzero["factored_coefficient"] = (
        f"({first_nonzero['factored_coefficient']})+1"
    )
    rows["gate3_inheritance_coefficient_mutation"] = rejected(
        lambda: verify_inheritance_bernstein_certificate(
            hard_F,
            hard_names,
            hard_id,
            len(hard_signatures),
            hard_certificate,
        )
    )

    # Gate 3 one-active universe: omitting any independently regenerated tensor
    # must break the exact hash-set join.
    cores = load_cores(
        json.loads(
            (project / "AUDIT/INDEPENDENT_IMPLEMENTATION/level2_orientation_core_audit.json").read_text()
        )
    )
    root, _root_metrics, _ = enumerate_root_tensors(cores)
    incoming, _incoming_metrics, _ = enumerate_nonroot_tensors(
        cores, outgoing_count=3, include_incoming=True
    )
    outgoing, _outgoing_metrics, _ = enumerate_nonroot_tensors(
        cores, outgoing_count=4, include_incoming=False
    )
    universe = root | incoming | outgoing | {TREE_TENSOR}
    removed = set(universe)
    removed.pop()
    rows["gate3_omitted_tensor_type"] = rejected(
        lambda: (
            None
            if removed == universe
            else (_ for _ in ()).throw(AssertionError("tensor universe mismatch"))
        )
    )

    # The old central-port ordering must fail to contain the four decisive
    # equations, making this convention mutation visible.
    wrong_blocks, variables = wrong_central_port_blocks()
    a, b, c, t, A, B, C, T, z = variables
    wrong_minors = two_by_two_minors(wrong_blocks)
    decisive = (
        a * A - z**2 * B * C * b * c,
        z * T * t - z**2 * B * C * b * c,
        z * C * (A * t - z * T * b * c),
        z * c * (z * B * C * t - T * a),
    )
    if all(polynomial_up_to_sign(value) in wrong_minors for value in decisive):
        raise AssertionError("central-port mutation unexpectedly retained all equations")
    rows["gate3_wrong_central_port_order"] = "REJECTED"

    return {
        "tests": rows,
        "all_mutations_rejected": all(value == "REJECTED" for value in rows.values()),
        "status": "EXACTLY COMPUTED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = audit(arguments.project.resolve())
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
